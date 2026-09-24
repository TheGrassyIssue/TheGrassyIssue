#!/usr/bin/env python3
"""fix-more-card-images.py — stop the More from TGI grid showing the logo.
20 September 2026.

THE BUG, AS LENNY SAW IT: "the more from TGI is repeating me logo image."

WHAT IS ACTUALLY HAPPENING. Every More-from-TGI card carries a thumbnail. When
whatever generated the card could not find a lead image for the post it was
linking to, it fell back to /images/og-image.jpg — the site's Open Graph card,
which is the TGI wordmark. One of those is a shrug. On a page with four cards,
two or three wordmarks in a row reads as broken, and it is not confined to the
new post: 122 cards across 95 pages, pointing at 32 distinct posts.

THE FIX IS TO ASK THE TARGET POST WHAT IT LOOKS LIKE. For each of the 32 posts
being linked to, this opens that post and takes, in order:

  1. its own og:image, unless that is og-image.jpg too (a post with no hero
     often inherits the same fallback, so trusting og:image blindly would
     replace the logo with the logo),
  2. its first .drop-hero-img — the masthead band,
  3. its first .product-img — the lead product shot,
  4. its first content <img> that is not a logo, icon or the OG card.

A post that offers none of those keeps the fallback and is REPORTED, because a
link to a real post with a missing thumbnail is a content gap to go and fix,
not something to paper over with a different placeholder.

EVERY REPLACEMENT IS CHECKED ON DISK. An <img> pointing at a file that is not
there is a worse bug than the logo, since it renders as nothing at all.

Idempotent — a card already carrying a real image is left alone. Dry run by
default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
FALLBACK = "/images/og-image.jpg"

# Things that are chrome rather than content.
SKIP_IMG = re.compile(r"(og-image|favicon|apple-touch|logo|wordmark|sprite|icon)", re.I)

CARD = re.compile(
    r'(<a href="(?P<href>[^"]+)" class="more-card">\s*'
    r'<div class="more-card-img"><img src=")(?P<src>[^"]+)(")')


def page_for(href):
    """/drops/foo -> drops/foo.html, /brands/foo -> brands/foo.html."""
    p = ROOT / (href.lstrip("/") + ".html")
    return p if p.exists() else None


def thumbs(_c={}):
    """data/post-thumbs.json — the site's own thumbnail index."""
    if not _c:
        import json
        f = ROOT / "data/post-thumbs.json"
        _c["d"] = json.loads(f.read_text()) if f.is_file() else {}
    return _c["d"]


def lead_image(href, _cache={}):
    """The best real image the target post publishes, or None."""
    if href in _cache:
        return _cache[href]

    # ASK THE THUMBNAIL INDEX FIRST. data/post-thumbs.json is the site's own
    # answer to "what does this post look like", and it is better than anything
    # derived by scraping the page: it survived /drops/manors-ss26 and
    # /drops/sugarloaf-ss26, which publish no og:image and no hero band, so the
    # derivation below gave up on both and left twelve cards on the logo.
    e = thumbs().get(href)
    if isinstance(e, dict) and e.get("img"):
        c = e["img"]
        if c.startswith("/images/") and c != FALLBACK and not SKIP_IMG.search(c) \
                and (ROOT / c.lstrip("/")).exists():
            _cache[href] = c
            return c

    p = page_for(href)
    if p is None:
        _cache[href] = None
        return None
    h = p.read_text(encoding="utf-8", errors="ignore")

    # SCOPE ABOVE THE TAIL. The target page has its own More-from-TGI grid at
    # the bottom, full of thumbnails belonging to OTHER posts. The first cut of
    # this script scanned every <img> on the page and so "resolved" three posts
    # to pictures they do not own — sugarloaf-ss26 came back with the golf
    # magazines cover. Same scoping mistake as the donor-name guard on the
    # Local Rule build, in a different file.
    i = h.find('<div class="more">')
    if i > 0:
        h = h[:i]

    candidates = []

    m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
    if m:
        candidates.append(re.sub(r"^https?://thegrassyissue\.com", "", m.group(1)))

    m = re.search(r'class="drop-hero-img"[^>]*src="([^"]+)"', h) or \
        re.search(r'<div class="drop-hero-img"><img src="([^"]+)"', h)
    if m:
        candidates.append(m.group(1))

    m = re.search(r'<div class="product-img"><img src="([^"]+)"', h)
    if m:
        candidates.append(m.group(1))

    for m in re.finditer(r'<img[^>]+src="(/images/[^"]+)"', h):
        candidates.append(m.group(1))

    for c in candidates:
        if not c.startswith("/images/"):
            continue
        if c == FALLBACK or SKIP_IMG.search(c):
            continue
        if (ROOT / c.lstrip("/")).exists():
            _cache[href] = c
            return c
    _cache[href] = None
    return None


def files():
    out = []
    for pat in ("drops/*.html", "brands/*.html", "*.html", "guides/*.html"):
        out += sorted(ROOT.glob(pat))
    return [f for f in out if f.is_file()]


def main(apply_):
    locked = []
    fixed, unfixable, untouched = 0, {}, 0
    changed_files = []

    for f in files():
        # macOS Cloud-sync holds a file open mid-sync and the read raises
        # Errno 35. Skipping and reporting beats dying halfway through a
        # 200-file pass with some pages fixed and some not.
        try:
            h = f.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            locked.append((f.name, e.errno))
            continue
        if FALLBACK not in h:
            continue
        orig = h

        def repl(m):
            nonlocal fixed, untouched
            if m.group("src") != FALLBACK:
                untouched += 1
                return m.group(0)
            img = lead_image(m.group("href"))
            if img is None:
                unfixable.setdefault(m.group("href"), 0)
                unfixable[m.group("href")] += 1
                return m.group(0)
            fixed += 1
            return m.group(1) + img + m.group(4)

        h = CARD.sub(repl, h)
        if h != orig:
            changed_files.append(f)
            if apply_:
                f.write_text(h, encoding="utf-8")

    print(f"  {fixed} logo thumbnails replaced across {len(changed_files)} pages")
    if unfixable:
        print(f"\n  {sum(unfixable.values())} card(s) left on the fallback — these posts "
              f"publish no usable image:")
        for k, v in sorted(unfixable.items(), key=lambda x: -x[1]):
            print(f"    {v:3}  {k}")

    if locked:
        print(f"\n  {len(locked)} file(s) skipped — locked by Cloud sync, rerun later:")
        for n, e in locked[:8]:
            print(f"      {n}  (errno {e})")
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK ----
    bad, still = [], 0
    for f in files():
        # same Cloud-sync guard as the write pass; a locked file was not
        # written either, so skipping it here keeps the two passes consistent
        try:
            h = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        page_imgs = []
        for m in CARD.finditer(h):
            src = m.group("src")
            page_imgs.append(src)
            if src == FALLBACK:
                still += 1
            elif not (ROOT / src.lstrip("/")).exists():
                bad.append(f"{f.name}: more-card points at missing {src}")
        # THE ORIGINAL COMPLAINT WAS REPETITION, so check for it directly:
        # a grid of four cards showing the same picture is the same defect
        # wearing a different image.
        real = [s for s in page_imgs if s != FALLBACK]
        if len(real) > 1 and len(set(real)) == 1:
            bad.append(f"{f.name}: all {len(real)} more-cards show the same image {real[0]}")

    if bad:
        for b in bad[:20]:
            print("  ! " + b)
        sys.exit(f"\n! {len(bad)} problem(s) after the pass")
    print(f"\n  verified on disk: every more-card image exists; "
          f"{still} card(s) still on the fallback (reported above)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
