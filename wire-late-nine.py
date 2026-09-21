#!/usr/bin/env python3
"""wire-late-nine.py — homepage card, brand index, sitemap, search.
21 September 2026.

Five jobs, idempotent, each verified against the FINISHED FILE.

THE BRAND INDEX ENTRY IS THE ONE THAT MATTERS.

Late Nine has a post on this site and has never been in data/brands.json. That
means it has never appeared on /brands, never had a brand page, and never been
reachable by anyone browsing the directory — the same defect Lenny caught with
Local Rule ("Local rule isnt showing up on the brands index page"). A post that
only the homepage feed links to is half-published.

THE CARD IS A CAROUSEL WITH THE GRASS TAG, because that is what every Brand to
Know card on the homepage is. The five slides are Lenny's picks. Slide text
goes in the CENTRAL window._slideTexts registry — the one the slider actually
reads — not an inline window.__slideTexts block, which a number of cards write
to and nothing consumes.

PRICES. Every figure below is SEK, read 21 September 2026 and re-verified live
the same day. Nothing converted. A guard refuses a bare dollar figure.

Dry run by default.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
BRANDS = ROOT / "data/brands.json"
SITEMAP = ROOT / "sitemap.xml"
SEARCH = ROOT / "search-index.json"
POST = ROOT / "drops/late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf.html"

SLUG = "late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf"
MARK = "<!-- BRAND REVISITED — LATE NINE -->"
TITLE = "Brand Revisited &mdash; Late Nine"
KEY = "latenine"   # the key the EXISTING card already uses — see wire_index
SHOP = "https://late-nine.com"
IMG = "/images/late-nine"
DATE = "2026-09-21"

# Lenny's five, in his order. slug, name, price SEK, handle, caption-brand.
SLIDES = [
    ("ribbed-polo-taupe", "Ribbed Jersey Polo Taupe", 1800,
     "Fleetwood&rsquo;s Masters polo"),
    ("5-pocket-cords-navy", "5-Pocket Cords Navy", 2700,
     "New for FW26 &middot; UK corduroy"),
    ("five-pocket-chino-fawn", "Five-pocket Chino Fawn", 2700,
     "Every size live"),
    ("cable-knit-polo-burgundy", "Cable Knit Polo Burgundy", 2950,
     "First-shearing merino"),
    ("country-club-cap-beige", "Twilight Cap Beige", 500,
     "The cheapest way in"),
]

SLIDE_TEXTS = [
    "The taupe ribbed jersey polo Tommy Fleetwood played the 2026 Masters in, as "
    "a free agent with no apparel deal. Hefty cotton, contrast-stripe collar, "
    "oversized buttons. 1,800 SEK and down to one size of five.",

    "Baby cotton corduroy milled in the UK at 215g, full straight leg, deepened "
    "front pockets and a ticket pocket. New for FW26 and the newest thing in the "
    "store. 2,700 SEK.",

    "The chino half of the same family, and the only pick here with every size "
    "live. Cut tighter than the pleated trouser &mdash; Late Nine&rsquo;s own "
    "sizing note says size up between. 2,700 SEK.",

    "Ultra-fine merino from the first shearing, nodding to the classic knits "
    "worn by icons of past decades. The most colour anywhere in the range. "
    "2,950 SEK.",

    "Modelled on the vintage members caps of the nineties. At 500 SEK it does "
    "more work than anything else Late Nine make, and it is the cheapest way "
    "into the whole look.",
]

BRAND_ENTRY = {
    "slug": "late-nine",
    "name": "Late Nine",
    "loc": "Stockholm, Sweden",
    "regions": ["europe"],
    "cats": ["apparel"],
    "line": ("Maxim Lundh&rsquo;s Stockholm label, built on late-nineties tour "
             "golf &mdash; pleated slacks, ribbed jersey polos and merino knits, "
             "with no elastane in sight."),
    "url": f"/drops/{SLUG}",
    "tags": ["quiet-luxury", "post-round-friendly"],
    "added": DATE,
    "attrs": [],
    "img": f"{IMG}/ribbed-polo-taupe.jpg",
}


def card_html():
    slides = "".join(
        f'''          <div class="gear-slide">
            <a href="{SHOP}/products/{slug}" target="_blank" rel="noopener">
              <img src="{IMG}/{slug}.jpg" alt="Late Nine {name}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{cap}</div><div class="gear-slide-name">{name} &middot; {price:,} SEK</div></div>
            </a>
          </div>
'''
        for slug, name, price, cap in SLIDES)
    return f'''{MARK}
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{slides}        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDE_TEXTS[0]}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <a href="/drops/{SLUG}" class="card-link">Read the profile &#8599;</a>
    </div>
  </div>
'''


ANCHOR = "<!--TGI-SC-HOME-->"


def card_bounds(h):
    """(start, end) of the Late Nine card block, or (-1, -1) if it is absent.

    THE BUG THIS FIXES. The first version looked for MARK, did not find it
    (because the existing card predates this script and carries no marker),
    and inserted a second Late Nine card. The homepage would have shown the
    brand twice: the old stub card under the old title, and the new one.
    A marker-only lookup can only ever find cards this script wrote.

    So: find MARK if present, otherwise find the existing card by its link to
    our slug. The replacement carries MARK so later runs are cheap.
    """
    i = h.find(MARK)
    if i < 0:
        hit = h.find(f"/drops/{SLUG}")
        if hit < 0:
            return -1, -1
        i = h.rfind('<div class="card"', 0, hit)
        if i < 0:
            sys.exit("! found a link to the post but no card around it")

    # BOTH LINK CLASSES EXIST IN THE WILD. The card we are replacing ends
    # with .card-readmore; the one we emit ends with .card-link. Bounding on
    # one class only failed on a correct page — the same over-narrow-match
    # mistake as looking for the card by our own marker.
    j = min((x for x in (h.find('class="card-link"', i),
                         h.find('class="card-readmore"', i)) if x > 0),
            default=-1)
    if j < 0:
        sys.exit("! existing card found but no card-link/card-readmore "
                 "to bound it")
    j = h.find("</div>", h.find("</a>", j))
    j = h.find("</div>", j + 6) + 6

    # take the card's whole line, so excising it does not strand its indent
    k = h.rfind("\n", 0, i) + 1
    if h[k:i].strip() == "":
        i = k
    # and the blank line(s) it sat on, so repeat runs do not accumulate them
    while j < len(h) and h[j] == "\n":
        j += 1
    return i, j


def wire_index(h):
    """Put the Late Nine card in the TOP slot of the homepage feed.

    Lenny: "replace the old card with this ... and push to new top slot."
    Replacing in place is not enough — the card has to MOVE. So this excises
    the existing card wherever it sits and re-inserts the new one immediately
    after the feed anchor, which is where new cards go.

    Cut-then-insert rather than edit-in-place, because a move that leaves the
    original behind is exactly the duplicate-card failure above, in a new
    costume. The card count is guarded either side of this in main().
    """
    if ANCHOR not in h:
        sys.exit("! feed anchor not found")
    new = card_html().strip()
    notes = []

    i, j = card_bounds(h)
    if i >= 0:
        old = h[i:j]
        n = old.count('<div class="card"')
        if n != 1:
            sys.exit(f"! card bounds wrong — slice holds {n} cards")
        was_top = h[:i].rstrip().endswith(ANCHOR)
        current = old.strip() == new
        h = h[:i] + h[j:]
        notes.append("card already current" if current else "card REPLACED")
        notes.append("card already in top slot" if was_top
                     else "card MOVED to top slot")
    else:
        notes.append("card inserted in top slot")

    return h.replace(ANCHOR, ANCHOR + "\n  " + new + "\n", 1), notes


def wire_slidetexts(h):
    """The CENTRAL registry — window._slideTexts, one underscore. Inline
    __slideTexts blocks exist on this page and the slider never reads them."""
    lines = ",\n".join('      "' + t.replace('"', '\\"') + '"' for t in SLIDE_TEXTS)
    block = f'"{KEY}": [\n{lines}\n    ],'
    # The existing card already registers this key with the OLD copy. Replace
    # that block, do not skip it — skipping left the new five slides paired
    # with the previous card's text.
    existing = re.search(rf'"{re.escape(KEY)}": \[.*?\n    \],', h, re.S)
    if existing:
        if existing.group(0) == block:
            return h, ["slideTexts already current"]
        return h[:existing.start()] + block + h[existing.end():], \
            [f"slideTexts REPLACED ({len(SLIDE_TEXTS)} lines)"]
    anchor = "window._slideTexts = {"
    if anchor not in h:
        sys.exit("! window._slideTexts registry not found")
    return h.replace(anchor, f'{anchor}\n    {block}', 1), \
        [f"slideTexts + {len(SLIDE_TEXTS)} lines"]


def wire_brands(rows):
    if any(r.get("slug") == "late-nine" for r in rows):
        return rows, ["brand index already has Late Nine"]
    rows.append(BRAND_ENTRY)
    rows.sort(key=lambda r: r.get("name", "").lower())
    return rows, ["brand index + Late Nine (FIRST TIME — it was never listed)"]


def wire_sitemap(x):
    loc = f"https://thegrassyissue.com/drops/{SLUG}"
    if loc in x:
        # already there; refresh lastmod because the page was rebuilt
        x2 = re.sub(rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]*(</lastmod>)",
                    lambda m: m.group(1) + DATE + m.group(2), x)
        return x2, ["sitemap lastmod refreshed"]
    entry = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{DATE}</lastmod>\n"
             f"    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n"
             f"  </url>\n</urlset>")
    return x.replace("</urlset>", entry, 1), ["sitemap + the post"]


def wire_search(j):
    """Short keys — u/t/d/g/i/k."""
    url = f"/drops/{SLUG}"
    entry = {
        "u": url,
        "t": "Brand Revisited — Late Nine",
        "d": ("Maxim Lundh's Stockholm label, built on late-nineties tour golf. "
              "Pleated slacks, ribbed jersey polos, merino knits — and why a brand "
              "from a country of public courses reads right on a muni. Prices in "
              "SEK, read 21 September 2026."),
        "g": "Drops & Brands",
        "i": f"{IMG}/ribbed-polo-taupe.jpg",
        "k": ("Late Nine Stockholm Sweden Maxim Lundh CQP golf apparel pleated "
              "slacks double pleat ribbed jersey polo cable knit merino Twilight "
              "Cap Orbit Cap five-pocket chino corduroy Tommy Fleetwood Masters "
              "Ryder Cup nineties SEK"),
    }
    for i, e in enumerate(j):
        if e.get("u") == url:
            if e == entry:
                return j, ["search index already current"]
            j[i] = entry
            return j, ["search index entry REFRESHED"]
    j.append(entry)
    return j, ["search index + the post"]


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")
    rows = json.loads(BRANDS.read_text(encoding="utf-8"))
    x = SITEMAP.read_text(encoding="utf-8")
    js = json.loads(SEARCH.read_text(encoding="utf-8"))

    # A MOVE MUST NOT LOSE A NEIGHBOUR. Cut-and-paste across a 215-card file
    # is exactly the operation that quietly drops the card next door, so the
    # feed is counted before and after and the two must agree.
    cards_before = h.count('<div class="card"')

    h2, c1 = wire_index(h)
    h2, c2 = wire_slidetexts(h2)
    rows2, c3 = wire_brands(rows)
    x2, c4 = wire_sitemap(x)
    js2, c5 = wire_search(js)
    for c in c1 + c2 + c3 + c4 + c5:
        print("  " + c)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    INDEX.write_text(h2, encoding="utf-8")
    BRANDS.write_text(json.dumps(rows2, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    SITEMAP.write_text(x2, encoding="utf-8")
    SEARCH.write_text(json.dumps(js2, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")

    # ---- VERIFY THE FINISHED FILES ON DISK ----
    hh = INDEX.read_text(encoding="utf-8")
    rr = json.loads(BRANDS.read_text(encoding="utf-8"))
    xx = SITEMAP.read_text(encoding="utf-8")
    jj = json.loads(SEARCH.read_text(encoding="utf-8"))
    bad = []

    if MARK not in hh: bad.append("card missing")
    if hh.count(MARK) != 1: bad.append("card duplicated")
    i = hh.find(MARK)

    # ---- THE TOP SLOT, read off the finished file ----
    if hh.count('<div class="card"') != cards_before:
        bad.append(f"feed went from {cards_before} cards to "
                   f"{hh.count(chr(60) + 'div class=' + chr(34) + 'card' + chr(34))}")
    # nothing that opens a card may sit between the anchor and our card
    gap = hh[hh.find(ANCHOR) + len(ANCHOR):i]
    if gap.strip():
        bad.append(f"card is not first in the feed — {gap.strip()[:60]!r} "
                   "sits above it")
    # and the card that used to be first must still be there, just below us
    if '<!-- ON OUR RADAR — WILD SPRING DUNES -->' not in hh:
        bad.append("the previous top card was lost in the move")
    seg = hh[i:hh.find("</div>\n", hh.find('class="card-link"', i))]

    if 'data-type="drop"' not in seg: bad.append("card is not typed as a drop")
    if 'card-tag grass' not in seg: bad.append("card tag is not the house grass tag")
    if seg.count('<div class="gear-slide">') != len(SLIDES):
        bad.append(f"{seg.count(chr(60) + 'div class=')} slides, expected {len(SLIDES)}")
    if seg.count("gear-slide-info") != len(SLIDES):
        bad.append("a slide is missing its caption")
    if seg.count("gear-arrow") != 2: bad.append("carousel arrows wrong")
    for attr in ("data-slidetext", "data-dots", "data-counter"):
        if f'{attr}="{KEY}"' not in seg: bad.append(f"missing {attr}")
    if hh.count(f'data-carousel="{KEY}"') != 1:
        bad.append(f"carousel key {KEY!r} is not unique")

    # every slide image must be local AND exist
    for m in re.finditer(r'<img src="([^"]+)"', seg):
        s = m.group(1)
        if s.startswith("http"): bad.append(f"hot-linked slide image: {s[:50]}")
        elif not (ROOT / s.lstrip("/")).is_file(): bad.append(f"missing image {s}")

    # currency
    for m in re.finditer(r"\$\s?[\d,]+", seg):
        bad.append(f"dollar figure in a SEK card: {m.group(0)!r}")

    # the registry the slider actually reads
    reg = re.search(r"window\._slideTexts = \{(.*?)\n  \};", hh, re.S)
    if not reg or f'"{KEY}"' not in reg.group(1):
        bad.append(f"{KEY!r} is not in the _slideTexts registry")
    else:
        blk = re.search(rf'"{KEY}": \[(.*?)\n    \]', reg.group(1), re.S).group(1)
        n = len(re.findall(r'\n      "', blk))
        if n != len(SLIDES):
            bad.append(f"{n} slide texts for {len(SLIDES)} slides")

    ent = [r for r in rr if r.get("slug") == "late-nine"]
    if len(ent) != 1:
        bad.append(f"{len(ent)} brands.json entries for late-nine, expected 1")
    else:
        # `img` is optional — the file holds 75 rows with it and 61 without,
        # so comparing against one arbitrary sibling fails on a correct entry.
        # Compare against the REQUIRED set instead.
        required = {"slug", "name", "loc", "regions", "cats", "line", "url",
                    "tags", "added", "attrs"}
        missing = required - set(ent[0])
        extra = set(ent[0]) - required - {"img"}
        if missing: bad.append(f"brands.json entry missing keys: {sorted(missing)}")
        if extra: bad.append(f"brands.json entry has unknown keys: {sorted(extra)}")
        if not (ROOT / ent[0]["img"].lstrip("/")).is_file():
            bad.append(f"brand index image missing: {ent[0]['img']}")

    if SLUG not in xx: bad.append("sitemap entry missing")
    ours = [e for e in jj if e.get("u") == f"/drops/{SLUG}"]
    if len(ours) != 1: bad.append(f"{len(ours)} search entries, expected 1")
    else:
        sib = next((e for e in jj if e.get("u") != f"/drops/{SLUG}"), None)
        if sib and set(ours[0]) != set(sib):
            bad.append(f"search keys {sorted(ours[0])} != schema {sorted(sib)}")

    if not POST.exists(): bad.append("the post itself is not on disk")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified on disk: card ({len(SLIDES)} slides), slideTexts, "
          f"brand index, sitemap, search index")


if __name__ == "__main__":
    main("--apply" in sys.argv)
