#!/usr/bin/env python3
"""
fix-more-and-related.py — two sitewide changes Lenny asked for. 18 Sept 2026.

JOB A — "More from TGI" must show FOUR post recommendations, always different.
  Today 184 posts show three cards and only two show four. Worse, the three are
  drawn from a pool of just 23 posts, so the same handful recirculates across the
  whole site and a reader who opens two posts sees the same suggestions twice.
  This rebuilds every grid to four cards, drawn from a catalogue of all 196 posts
  that have both a title and a local hero image.

  "ALWAYS DIFFERENT" IS IMPLEMENTED AS A DETERMINISTIC ROTATION, not rng.
  Each page takes a start offset from a stable hash of its own slug and then
  strides through the catalogue. That gives three properties at once:
    · different pages get different sets (that is the ask),
    · no page links to itself,
    · and the same page produces the SAME four every run, so the build stays
      byte-stable. A random.shuffle() would satisfy the ask and break
      idempotency, which is the trade this comment exists to flag.

JOB B — remove the "If You Like <brand>" section, link to the brand index.
  37 pages carry <section class="more" data-btk="related"> holding four BRAND
  cards. Lenny wants the section gone and a plain link to /brands in its place.
  The section already contains an "Explore the Brand Index" link, so the link
  survives; the four brand cards do not.

Idempotent. Dry run by default.
"""
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
DROPS = ROOT / "drops"
CAT = json.loads((ROOT / "research/more-catalogue.json").read_text(encoding="utf-8"))
# The .more-* rules, harvested verbatim from austin-coffee-guide.html. Needed
# because 11 pages had no More grid at all and therefore never carried its CSS;
# inserting the markup alone put eight unstyled classes on those pages, which
# verify-post caught as "every class used has a CSS rule". Same rules, so the
# 11 late pages render identically to the 186 that always had one.
MORECSS = (ROOT / "research/more-css.txt").read_text(encoding="utf-8").strip()
KEYS = sorted(CAT)                      # sorted => stable across runs and machines

BRANDLINK = (
    '<div class="more" data-brandindex="1">\n'
    '  <div class="more-hdr">\n'
    '    <span class="more-label">The Brand Index</span>\n'
    '    <a href="/brands" class="more-link">Explore All Brands &rarr;</a>\n'
    '  </div>\n'
    '</div>\n')


def pick(slug, n=4):
    """Four catalogue entries for this page: deterministic, distinct, never self."""
    pool = [k for k in KEYS if k != slug]
    if len(pool) < n:
        sys.exit(f"! catalogue too small ({len(pool)}) to fill {n} slots")
    h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
    start = h % len(pool)
    # A stride coprime with len(pool) walks the whole pool without repeating.
    stride = 1 + (h // len(pool)) % (len(pool) - 1)
    while _gcd(stride, len(pool)) != 1:
        stride += 1
    return [pool[(start + i * stride) % len(pool)] for i in range(n)]


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def more_html(slug):
    cards = []
    for k in pick(slug):
        c = CAT[k]
        cards.append(
            f'    <a href="{k}" class="more-card">\n'
            f'      <div class="more-card-img"><img src="{c["img"]}" '
            f'alt="{_plain(c["name"])}" loading="lazy" /></div>\n'
            f'      <div class="more-card-body"><div class="more-card-name">{c["name"]}</div>'
            f'<div class="more-card-tag">{c["tag"]}</div></div>\n'
            f'    </a>')
    return ('<!-- More from the Feed -->\n<div class="more">\n  <div class="more-hdr">\n'
            '    <span class="more-label">More from TGI</span>\n'
            '    <a href="/" class="more-link">See All &rarr;</a>\n  </div>\n'
            '  <div class="more-grid">\n' + "\n".join(cards) + '\n  </div>\n</div>\n')


def _plain(s):
    return (s.replace("&mdash;", "—").replace("&amp;", "&").replace("&middot;", "·")
             .replace("&rsquo;", "’").replace("&ldquo;", "“").replace("&rdquo;", "”")
             .replace('"', "&quot;"))


def strip_related(t):
    """JOB B. Replace the whole data-btk="related" section with the index link.

    Cut on the SECTION boundaries, not on a card count: these sections hold four
    brand cards today but nothing guarantees that, and a count-based cut would
    leave orphans behind on any page that differs.
    """
    out, n = t, 0
    while True:
        i = out.find('<section class="more" data-btk="related">')
        if i < 0:
            break
        j = out.find("</section>", i)
        if j < 0:
            sys.exit("! unterminated related section")
        out = out[:i] + BRANDLINK + out[j + len("</section>"):]
        n += 1
    return out, n


def _cut_block(t, start, tag):
    """Return (i, j) spanning the element opening at `start`, counting `tag`.

    TWO BUGS THIS REPLACES, both caught by the guard rather than by reading:
      1. The first version used a non-greedy regex ending in
         </div>\\s*</div>\\s*</div>, which stops at the first triple-close —
         and that close is INSIDE the first card, not at the end of the grid.
      2. The second version counted <div> only. But 162 of the 223 grids are
         <section class="more">, not <div class="more">, so nothing matched, the
         old grid survived, the new one was appended, and every page carried
         seven cards. Count the tag you actually opened.
    """
    i = start
    depth = 0
    ot, ct = "<" + tag, "</" + tag + ">"
    while i < len(t):
        a = t.find(ot, i)
        b = t.find(ct, i)
        if b < 0:
            return None
        if 0 <= a < b:
            depth += 1; i = a + len(ot)
        else:
            depth -= 1; i = b + len(ct)
            if depth == 0:
                return start, i
    return None


def swap_more(t, slug):
    """JOB A. Replace the existing More-from-the-Feed grid, or insert one."""
    new_html = more_html(slug)
    for tag in ("section", "div"):
        search = 0
        needle = '<%s class="more"' % tag
        while True:
            i = t.find(needle, search)
            if i < 0:
                break
            span = _cut_block(t, i, tag)
            if not span:
                break
            blk = t[span[0]:span[1]]
            if 'more-grid' in blk and 'data-brandindex' not in blk:
                cs = t.rfind("<!-- More from the Feed -->", 0, i)
                s = cs if cs >= 0 and i - cs < 40 else i
                return t[:s] + new_html + t[span[1]:].lstrip("\n"), "replaced"
            search = span[1]
    foot = t.find("<footer")
    if foot < 0:
        return t, "no footer — skipped"
    return t[:foot] + new_html + "\n" + t[foot:], "inserted"


def run(apply_):
    changed = repl = ins = rel = 0
    fails = []
    for p in sorted(DROPS.glob("*.html")):
        slug = "/drops/" + p.stem
        t0 = p.read_text(encoding="utf-8")
        t, nrel = strip_related(t0)
        t, how = swap_more(t, slug)
        # CSS goes in wherever the markup ends up, not just on the insert path.
        # First attempt only injected while inserting, so the seven pages that
        # already had unstyled markup from an earlier run took the REPLACE path
        # and never got their rules. Condition on the finished document.
        if 'class="more-card"' in t and ".more-card-img{" not in t:
            k = t.rfind("</style>")
            if k > 0:
                t = t[:k] + "\n" + MORECSS + "\n" + t[k:]

        hrefs = re.findall(r'<a href="([^"]+)" class="more-card"', t)
        posthrefs = [h for h in hrefs if h.startswith("/drops/")]
        bad = []
        if len(posthrefs) != 4:            bad.append(f"{len(posthrefs)} post cards")
        if len(set(posthrefs)) != 4:       bad.append("duplicate cards")
        if slug in posthrefs:              bad.append("links to itself")
        if 'data-btk="related"' in t:      bad.append("related section survived")
        if t.count("<div") != t.count("</div>"): bad.append("div imbalance")
        if 'class="more-card"' in t and ".more-card-img{" not in t:
            bad.append("more markup with no CSS behind it")
        for h in posthrefs:
            if not (DROPS / (h[len("/drops/"):] + ".html")).exists():
                bad.append(f"dead link {h}")
        if bad:
            fails.append((p.name, bad)); continue

        if t != t0:
            changed += 1
            repl += how == "replaced"; ins += how == "inserted"; rel += nrel
            if apply_:
                p.write_text(t, encoding="utf-8")

    print(f"  pages changed          {changed}")
    print(f"    grids replaced       {repl}")
    print(f"    grids inserted       {ins}")
    print(f"    related sections cut {rel}")
    print(f"  FAILURES               {len(fails)}")
    for n, b in fails[:12]:
        print(f"    {n}: {', '.join(b)}")
    if fails:
        sys.exit("\n! refusing to write — fix the failures above")
    print("\n  written" if apply_ else "\n  dry run — pass --apply")


if __name__ == "__main__":
    run("--apply" in sys.argv)
