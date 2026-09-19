#!/usr/bin/env python3
"""
delete-bold-tees.py — retire /drops/bold-tees-carousel. 18 September 2026.

Lenny: "let's delete it then rebuild a fresh post tomorrow."

WHY IT IS GOING RATHER THAN BEING FIXED. The page was a homepage feed card
pasted into a page shell: window.gearSlide was never defined so the carousel was
dead, half the site stylesheet was missing so the nav and footer rendered
unstyled, and all twelve write-ups lived in a JavaScript array where a crawler
sees 165 words. On top of that, re-verification on 18 Sept found FIVE of the
twelve products no longer exist (Quiet Golf's pocket tee, Random Golf Club's
S.F.E. tee and both Walker tees are discontinued; Merrill's Target Practice is
sold out). There was no version of this page worth saving.

THE URL MUST NOT 404. Seven steps, because a delete is never just a delete:
  1. 301 /drops/bold-tees-carousel -> the closest live tee post.
  2. REPOINT THE EXISTING REDIRECT. vercel.json already sent
     /drops/12-bold-tees-that-belong-in-your-bag -> /drops/bold-tees-carousel.
     Left alone that becomes a redirect chain ending in a 404, which is worse
     than the original problem. It now points at the same live destination.
  3. Cut the homepage feed card.
  4. Drop the sitemap row and the search-index record.
  5. Drop it from the More-from-TGI catalogue so no future grid rebuild can
     resurrect it.
  6. Repoint every remaining internal link — 10 brand pages and several posts —
     at the live destination directly, rather than letting them ride the 301.
  7. Delete the file.

The page is tracked in git, so the content is recoverable if tomorrow's rebuild
wants the old write-ups back.

Idempotent. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SLUG = "/drops/bold-tees-carousel"
PAGE = ROOT / "drops/bold-tees-carousel.html"
DEST = "/drops/the-tee-edit-14-independent-tees-for-the-fairway-and-beyond"
OLD_ALIAS = "/drops/12-bold-tees-that-belong-in-your-bag"


def edit(path, fn, apply_, label):
    p = ROOT / path
    if not p.exists():
        return f"{label}: missing"
    t0 = p.read_text(encoding="utf-8")
    t = fn(t0)
    if t == t0:
        return f"{label}: no change"
    if apply_:
        p.write_text(t, encoding="utf-8")
    return f"{label}: updated ({len(t0):,} -> {len(t):,} bytes)"


def cut_feed_card(t):
    """Remove the homepage card whose title links at the dead slug."""
    i = t.find(f'href="{SLUG}"')
    while i >= 0:
        start = t.rfind('<div class="card"', 0, i)
        if start < 0:
            break
        cstart = t.rfind("<!--", 0, start)
        if cstart > 0 and t.count("\n", cstart, start) <= 2:
            start = cstart
        nxt = t.find('<div class="card"', i)
        if nxt < 0:
            break
        nc = t.rfind("<!--", i, nxt)
        end = nc if nc > i else nxt
        t = t[:start] + t[end:]
        i = t.find(f'href="{SLUG}"')
    return t


def fix_vercel(t):
    d = json.loads(t)
    reds = d.setdefault("redirects", [])
    for r in reds:
        if r.get("destination") == SLUG:
            r["destination"] = DEST          # step 2: no chain into a 404
    if not any(r.get("source") == SLUG for r in reds):
        reds.append({"source": SLUG, "destination": DEST, "permanent": True})
    return json.dumps(d, indent=2) + "\n"


def fix_sitemap(t):
    return re.sub(r"\s*<url>\s*<loc>[^<]*" + re.escape(SLUG) + r"</loc>.*?</url>",
                  "", t, flags=re.S)


def fix_search(t):
    recs = json.loads(t)
    recs = [r for r in recs if r.get("u", "").rstrip("/") != SLUG]
    return json.dumps(recs, ensure_ascii=False) + "\n"


def fix_catalogue(t):
    cat = json.loads(t)
    cat.pop(SLUG, None)
    return json.dumps(cat, indent=1, ensure_ascii=False) + "\n"


def repoint(t):
    return t.replace(f'href="{SLUG}"', f'href="{DEST}"')


def run(apply_):
    print("== supporting files ==")
    for path, fn, label in [
        ("vercel.json", fix_vercel, "vercel.json (301 + de-chain)"),
        ("sitemap.xml", fix_sitemap, "sitemap.xml"),
        ("search-index.json", fix_search, "search-index.json"),
        ("research/more-catalogue.json", fix_catalogue, "more-catalogue.json"),
        ("index.html", lambda t: repoint(cut_feed_card(t)), "index.html (card cut)"),
    ]:
        print("  " + edit(path, fn, apply_, label))

    print("\n== repointing internal links ==")
    n = 0
    for p in sorted(ROOT.glob("**/*.html")):
        if p == PAGE or "drafts" in p.parts or "research" in p.parts:
            continue
        t0 = p.read_text(encoding="utf-8", errors="ignore")
        if f'href="{SLUG}"' not in t0:
            continue
        if apply_:
            p.write_text(repoint(t0), encoding="utf-8")
        n += 1
    print(f"  {n} file(s) repointed at {DEST}")

    if apply_ and PAGE.exists():
        PAGE.unlink()
        print(f"\n  deleted {PAGE.name}")

    # ---- guards, run against the finished state ----
    print("\n== verification ==")
    ok = True
    if apply_:
        live = ROOT / "drops" / (DEST[len("/drops/"):] + ".html")
        checks = [
            ("page is gone", not PAGE.exists()),
            ("redirect target exists", live.exists()),
            # SCOPE. Only PUBLISHED pages matter. The first version swept
            # ROOT/**/*.html and fired on 18 archived copies under
            # research/btk/backups* and drafts/ — files that are not served and
            # are deliberately frozen snapshots of how pages used to look.
            # Rewriting a backup to "fix" a link would corrupt the very record
            # it exists to preserve.
            ("no PUBLISHED page still links at the dead slug",
             not any(f'href="{SLUG}"' in q.read_text(encoding="utf-8", errors="ignore")
                     for q in _published())),
            ("not in sitemap", SLUG not in (ROOT / "sitemap.xml").read_text()),
            ("not in search index", SLUG not in (ROOT / "search-index.json").read_text()),
            ("not in the More catalogue",
             SLUG not in (ROOT / "research/more-catalogue.json").read_text()),
            ("301 exists for the dead slug",
             any(r.get("source") == SLUG for r in
                 json.loads((ROOT / "vercel.json").read_text())["redirects"])),
            ("no redirect still points INTO the dead slug",
             not any(r.get("destination") == SLUG for r in
                     json.loads((ROOT / "vercel.json").read_text())["redirects"])),
            ("old alias now lands somewhere live",
             any(r.get("source") == OLD_ALIAS and r.get("destination") == DEST
                 for r in json.loads((ROOT / "vercel.json").read_text())["redirects"])),
            ("sitemap still parses", _xml_ok(ROOT / "sitemap.xml")),
        ]
        for label, passed in checks:
            print(f"  {'OK  ' if passed else 'FAIL'} {label}")
            ok &= passed
        if not ok:
            sys.exit("\n! verification failed — check git status before proceeding")
    print("\n  done" if apply_ else "\n  dry run — pass --apply")


def _published():
    """Every HTML file that actually gets served."""
    skip = {"research", "drafts", "mockups", "node_modules"}
    for q in ROOT.glob("**/*.html"):
        if skip & set(q.parts):
            continue
        yield q


def _xml_ok(p):
    import xml.dom.minidom
    try:
        xml.dom.minidom.parse(str(p)); return True
    except Exception as e:
        print("     xml error:", e); return False


if __name__ == "__main__":
    run("--apply" in sys.argv)
