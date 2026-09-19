#!/usr/bin/env python3
"""
wire-bold-tees.py — put The Bold Tee Edit into the feed, the sitemap, the search
index and the More catalogue, and reclaim both retired URLs. 19 September 2026.

FIVE jobs, each guarded independently so a failure in one cannot half-write
another:

1. INDEX.HTML — a 6-slide gear carousel card at the TOP of the feed.
2. SITEMAP.XML — one <url> row with today's lastmod.
3. SEARCH-INDEX.JSON — one record in the index's own compact u/t/d/g/i/k shape.
4. MORE-CATALOGUE.JSON — so the sitewide More-from-TGI rotation can surface it.
   The old carousel was REMOVED from this file when it was retired; without this
   step the new post is invisible to every other page's More grid.
5. VERCEL.JSON — RECLAIM BOTH RETIRED URLS, which is the whole point of the
   rebuild. Today both /drops/bold-tees-carousel and
   /drops/12-bold-tees-that-belong-in-your-bag 301 to the 14-tee edit, which was
   the correct holding position when the page was deleted yesterday. They now
   point here instead. That recovers four months of equity and ten brand-page
   inbound links that were pointing at the old carousel.

   REPOINT, DO NOT APPEND. Adding a second rule for a source that already has
   one leaves two rules for the same path — Vercel takes the first, so a
   carelessly appended rule is either dead or, worse, wins and creates a chain.
   The guard below asserts exactly one rule per source and no chains.

Idempotent: detects its own marker and exits clean. Dry run by default.
"""
import json, pathlib, re, sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = ROOT / "research/bold-tees.json"
IDX  = ROOT / "index.html"
SMAP = ROOT / "sitemap.xml"
SIDX = ROOT / "search-index.json"
CAT  = ROOT / "research/more-catalogue.json"
VERC = ROOT / "vercel.json"

SLUG  = "/drops/the-bold-tee-edit"
MARK  = "<!-- THE EDIT — Bold Tees -->"
CAR   = "boldtees1"
TITLE = "The Bold Tee Edit &mdash; The Graphic Tee Grew Up"
BLURB = ("Twenty-seven graphic tees from independent golf brands, priced off each "
         "brand&rsquo;s own store on 19 September 2026. Heavyweight cotton, real "
         "screen printing, made-in-USA runs &mdash; and two Austin shops printing "
         "their own.")
TODAY = date.today().isoformat()

# The two URLs being reclaimed. Both currently 301 elsewhere.
RECLAIM = ["/drops/bold-tees-carousel",
           "/drops/12-bold-tees-that-belong-in-your-bag"]

# Six slides chosen for RANGE, not price order: the two Austin shops, a
# made-in-USA spec sheet, the heaviest cotton, and two graphics that read at
# thumbnail size. A carousel has to say "look at these", not "here is a list".
SLIDES = [
    ("muni",   "butler-pitch-and-putt", "m"),
    ("weight", "badlands",              "w"),
    ("art",    "swag-golf",             "a"),
    ("muni",   "southside-golf-co",     "m"),
    ("weight", "gumtree-golf",          "w"),
    ("art",    "devereux-golf",         "a"),
]


def plain(s):
    return (s.replace("&mdash;", "—").replace("&middot;", "·")
             .replace("&amp;", "&").replace("&rsquo;", "’")
             .replace("&ldquo;", "“").replace("&rdquo;", "”"))


def build_card(spec):
    slides = []
    for key, bslug, pref in SLIDES:
        row = next(r for r in spec[key] if r[0] == bslug)
        _s, brand, name, price, cur, _purl, _img, _d = row
        img = f"/images/bold-tees/{pref}-{bslug}.jpg"
        tag = f"{price} {cur}" if cur != "USD" else price
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="{img}" alt="{plain(brand + " " + name)}" loading="lazy" />\n'
            f'              <div class="gear-slide-info">'
            f'<div class="gear-slide-brand">{brand}</div>'
            f'<div class="gear-slide-name">{name} &middot; {tag}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    return (
        f'{MARK}\n'
        f'  <div class="card" data-type="drop">\n'
        f'    <div class="card-media" style="position:relative;">\n'
        f'      <span class="card-tag grass">[Drops &amp; Brands]</span>\n'
        f'      <div class="gear-carousel" data-carousel="{CAR}">\n'
        f'        <div class="gear-carousel-track">\n'
        + "\n".join(slides) + "\n"
        f'        </div>\n'
        f'        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>\n'
        f'        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>\n'
        f'      </div>\n    </div>\n'
        f'    <div class="card-body">\n'
        f'      <div class="card-title"><a href="{SLUG}" style="color:inherit;'
        f'text-decoration:none;border-bottom:none;">{TITLE}</a></div>\n'
        f'      <div class="card-text" data-slidetext="{CAR}">{BLURB}</div>\n'
        f'      <div class="gear-dots" data-dots="{CAR}"></div>\n'
        f'      <div class="gear-counter" data-counter="{CAR}">1 / {len(SLIDES)}</div>\n'
        f'      <div class="card-source">Prices read 19 September 2026</div>\n'
        f'      <a href="{SLUG}" class="card-readmore" style="display:inline-block;'
        f"margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;"
        f'letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid '
        f'var(--ink);padding-bottom:2px;">See All 27 Tees &rarr;</a>\n'
        f'    </div>\n  </div>\n')


def wire_index(spec, apply_):
    """Put the card at the true front of the feed, and MOVE it if it is not.

    Anchoring on `<!-- ... -->\\s*<div class="card"` does not work in this file:
    the oldest cards are preceded by `<!--TGI-HLS-->` with no spaces, so a
    space-requiring regex skips 23 real cards and "inserts at the front" at DOM
    position 24. Find the first card directly and back up to its own comment.
    """
    h = IDX.read_text(encoding="utf-8")
    before_cards = len(re.findall(r'<div class="card"', h))
    card = build_card(spec)
    # A FIRST INSERT LEGITIMATELY ADDS ONE CARD; a re-run excises its own card
    # first and so must come out level. The first version of the guard asserted
    # equality in both cases and failed a correct fresh insert at 211 vs 210.
    # The expected delta depends on which path we take, so record it here.
    had_card = MARK in h
    expect = before_cards + (0 if had_card else 1)

    if MARK in h:
        # Already present — excise so a wrong position can be corrected. Cut to
        # the START OF THE NEXT CARD, an unambiguous boundary; matching the first
        # '\n  </div>\n' instead once ate 55 neighbouring cards. And skip OUR OWN
        # opening div first, or the cut removes the comment and leaves the body.
        s = h.index(MARK)
        mine = h.find('<div class="card"', s + len(MARK))
        nxt = h.find('<div class="card"', mine + 10) if mine > 0 else -1
        if nxt < 0:
            sys.exit("! Bold Tee card is the last card — cannot isolate")
        cstart = h.rfind("<!--", s + len(MARK), nxt)
        h = h[:s] + h[(cstart if cstart > s else nxt):]

    feed = h.find('class="feed"')
    first = h.find('<div class="card"', feed if feed > 0 else 0)
    if first < 0:
        sys.exit("! could not find any feed card")
    cstart = h.rfind("<!--", 0, first)
    at = cstart if cstart > 0 and h.count("\n", cstart, first) <= 2 else first
    out = h[:at] + card.rstrip() + "\n\n  " + h[at:]

    mark_at = out.index(MARK)
    earlier = [m.start() for m in re.finditer(r'<div class="card"', out)
               if m.start() < mark_at]
    now = len(re.findall(r'<div class="card"', out))
    checks = [
        ("exactly one Bold Tee card", out.count(MARK) == 1, ""),
        # Compare against EVERY card offset, not just the next one. A guard that
        # only proves the marker precedes the following card passes at any
        # position, which is how the Hoodie card shipped at DOM position 24.
        ("NO card appears before it anywhere in the document",
         not earlier, f"{len(earlier)} card(s) still ahead of it"),
        # Measure against the count read at entry, never a magic number.
        ("no cards were lost", now == expect,
         f"{now} vs {expect} expected ({'moved' if had_card else 'fresh insert'})"),
        (f"{len(SLIDES)} slides", card.count('class="gear-slide"') == len(SLIDES), ""),
        ("every slide image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/bold-tees/[^"]+)"', card)), ""),
        ("slides are six distinct products",
         len(set(re.findall(r'src="(/images/bold-tees/[^"]+)"', card))) == len(SLIDES), ""),
        ("tags balance in the card", card.count("<div") == card.count("</div>"), ""),
        ("document still closes", out.rstrip().endswith("</html>"), ""),
    ]
    ok = _report(checks)
    if not ok:
        sys.exit("! refusing to write index.html")
    if apply_:
        IDX.write_text(out, encoding="utf-8")


def wire_sitemap(apply_):
    t = SMAP.read_text(encoding="utf-8")
    if SLUG in t:
        print("  no change — already in the sitemap"); return
    row = (f"  <url>\n    <loc>https://thegrassyissue.com{SLUG}</loc>\n"
           f"    <lastmod>{TODAY}</lastmod>\n"
           f"    <changefreq>monthly</changefreq>\n"
           f"    <priority>0.8</priority>\n  </url>\n")
    out = t.replace("</urlset>", row + "</urlset>", 1)
    ok = _report([
        ("one new <url>", out.count("<url>") == t.count("<url>") + 1, ""),
        ("loc tags balance", out.count("<loc>") == out.count("</loc>"), ""),
        ("no retired slug reappears",
         not any(s in out for s in RECLAIM), ""),
        ("still closes", out.rstrip().endswith("</urlset>"), ""),
    ])
    if not ok:
        sys.exit("! refusing to write sitemap.xml")
    if apply_:
        SMAP.write_text(out, encoding="utf-8")


def wire_search(spec, apply_):
    """Add one record in the index's OWN compact key shape (u/t/d/g/i/k).

    Reading an existing record and mirroring its keys is the only safe way to
    add to this file; inventing a "url" key writes a record the search overlay
    can never match.
    """
    recs = json.loads(SIDX.read_text(encoding="utf-8"))
    before = len(recs)
    if any(r.get("u", "").rstrip("/") == SLUG for r in recs):
        print("  no change — already in the search index"); return
    allrows = spec["muni"] + spec["weight"] + spec["art"]
    template = recs[0]
    rec = {
        "u": SLUG, "t": plain(TITLE), "d": plain(BLURB), "g": "Drops & Brands",
        "i": "/images/bold-tees/m-butler-pitch-and-putt.jpg",
        "k": " ".join(f"{plain(r[1])} {plain(r[2])} {plain(r[3])}" for r in allrows),
    }
    rec = {k: rec.get(k, "") for k in template}       # exact key order + shape
    recs.insert(0, rec)
    ok = _report([
        ("one new record", len(recs) == before + 1, ""),
        ("keys match the existing shape exactly", list(rec) == list(template), ""),
        ("image exists", (ROOT / rec["i"].lstrip("/")).exists(), ""),
        ("keywords name every brand",
         all(plain(r[1]) in rec["k"] for r in allrows), ""),
    ])
    if not ok:
        sys.exit("! refusing to write search-index.json")
    if apply_:
        SIDX.write_text(json.dumps(recs, ensure_ascii=False) + "\n", encoding="utf-8")


def wire_catalogue(apply_):
    """Add the post to the More-from-TGI catalogue.

    The retired carousel was DELETED from this file by delete-bold-tees.py, so
    without this step the rebuild never appears in any other page's More grid.
    """
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    before = len(cat)
    if SLUG in cat:
        print("  no change — already in the More catalogue"); return
    sample = cat[next(iter(cat))]
    entry = {"name": TITLE, "img": "/images/bold-tees/m-butler-pitch-and-putt.jpg",
             "tag": "The Edit"}
    entry = {k: entry.get(k, "") for k in sample}
    cat[SLUG] = entry
    ok = _report([
        ("one new entry", len(cat) == before + 1, ""),
        ("entry shape matches the file", list(cat[SLUG]) == list(sample), ""),
        ("image exists", (ROOT / entry["img"].lstrip("/")).exists(), ""),
        ("no retired slug was resurrected",
         not any(s in cat for s in RECLAIM), ""),
    ])
    if not ok:
        sys.exit("! refusing to write more-catalogue.json")
    if apply_:
        CAT.write_text(json.dumps(cat, indent=1, ensure_ascii=False) + "\n",
                       encoding="utf-8")


def wire_redirects(apply_):
    """RECLAIM BOTH RETIRED URLS. Repoint in place; never append a duplicate."""
    d = json.loads(VERC.read_text(encoding="utf-8"))
    reds = d.setdefault("redirects", [])
    for src in RECLAIM:
        hits = [r for r in reds if r.get("source") == src]
        if hits:
            for r in hits:
                r["destination"] = SLUG
                r["permanent"] = True
        else:
            reds.append({"source": src, "destination": SLUG, "permanent": True})

    srcs = [r.get("source") for r in reds]
    dests = {r.get("source"): r.get("destination") for r in reds}
    ok = _report([
        ("both retired URLs point at the new post",
         all(dests.get(s) == SLUG for s in RECLAIM),
         str({s: dests.get(s) for s in RECLAIM})),
        # Two rules for one source means the second is dead or wins by accident.
        ("exactly one rule per reclaimed source",
         all(srcs.count(s) == 1 for s in RECLAIM),
         str({s: srcs.count(s) for s in RECLAIM})),
        # A 301 into a path that itself 301s costs a hop and can loop.
        ("no redirect chains anywhere in the file",
         not [s for s in srcs if s in dests.values()],
         str([s for s in srcs if s in dests.values()])),
        ("nothing redirects INTO the new post's own slug being itself a source",
         SLUG not in srcs, ""),
        ("the destination page actually exists",
         (ROOT / "drops" / (SLUG[len("/drops/"):] + ".html")).exists(), ""),
        ("no rule lost", len(reds) >= len(json.loads(VERC.read_text())["redirects"]), ""),
    ])
    if not ok:
        sys.exit("! refusing to write vercel.json")
    if apply_:
        VERC.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")


def _report(checks):
    ok = True
    for label, passed, detail in checks:
        print(f"  {'OK  ' if passed else 'FAIL'} {label}"
              f"{('  ' + detail) if detail and not passed else ''}")
        ok &= passed
    return ok


if __name__ == "__main__":
    a = "--apply" in sys.argv
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    print("== feed card ==");      wire_index(spec, a)
    print("== sitemap ==");        wire_sitemap(a)
    print("== search ==");         wire_search(spec, a)
    print("== More catalogue =="); wire_catalogue(a)
    print("== redirects ==");      wire_redirects(a)
    print("\n  written" if a else "\n  dry run — pass --apply")
