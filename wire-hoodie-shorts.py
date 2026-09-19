#!/usr/bin/env python3
"""
wire-hoodie-shorts.py — put the Hoodie and Shorts Edit into the feed, the
sitemap and the search index. 18 September 2026.

Three separate jobs, each guarded independently so a failure in one does not
half-write another:

1. INDEX.HTML — a 6-slide gear carousel card at the TOP of the feed. Top, not
   slotted among the older Edits: a card at position 10 reads as archive. Same
   lesson as the Merrill Revisited card, which went in above Devereux and had to
   be moved.
2. SITEMAP.XML — one <url> row with today's lastmod.
3. SEARCH-INDEX.JSON — one record so the site search overlay can find it.

The six carousel slides are picked to show the RANGE rather than the top six by
price: a $70 hoodie next to a $188 one, a mesh short next to a Coolcore short.
The card has to sell "these two things go together", not "here is a list".

Idempotent: detects its own marker and exits clean. Dry run by default.
"""
import json, pathlib, re, sys
from datetime import date

ROOT  = pathlib.Path(__file__).resolve().parent
SPEC  = ROOT / "research/hoodie-shorts.json"
IDX   = ROOT / "index.html"
SMAP  = ROOT / "sitemap.xml"
SIDX  = ROOT / "search-index.json"

SLUG  = "/drops/the-hoodie-and-shorts-edit"
MARK  = "<!-- THE EDIT — Hoodie and Shorts -->"
CAR   = "hoodieshorts1"
TITLE = ("Hoodie and Shorts &mdash; The Best Fall Combo")
BLURB = ("Twelve hoodies and twelve shorts from the brands we follow, priced off "
         "each brand&rsquo;s own store on 18 September 2026. The one outfit that "
         "covers a 58-degree tee time, an 84-degree back nine and the whole "
         "football afternoon that follows.")
TODAY = date.today().isoformat()

# (section key, brand slug, image prefix) — chosen for range, not for price order
SLIDES = [
    ("hoodies",       "birds-of-condor",       "h"),
    ("shorts_casual", "birds-of-condor",       "sc"),
    ("hoodies",       "sentinel-golf",         "h"),
    ("shorts_golf",   "malbon",                "sg"),
    ("hoodies",       "walker-golf-things",    "h"),
    ("shorts_casual", "devereux-golf",         "sc"),
]


def plain(s):
    return (s.replace("&mdash;", "—").replace("&middot;", "·")
             .replace("&amp;", "&").replace("&reg;", "®")
             .replace("&pound;", "£").replace("&rsquo;", "’"))


def build_card(spec):
    slides = []
    for key, bslug, pref in SLIDES:
        row = next(r for r in spec[key] if r[0] == bslug)
        _s, brand, name, price, cur, _purl, _img, _d = row
        ext = ".png" if (ROOT / f"images/hoodie-shorts/{pref}-{bslug}.png").exists() else ".jpg"
        img = f"/images/hoodie-shorts/{pref}-{bslug}{ext}"
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
        f'      <div class="card-source">Prices read 18 September 2026</div>\n'
        f'      <a href="{SLUG}" class="card-readmore" style="display:inline-block;'
        f"margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;"
        f'letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid '
        f'var(--ink);padding-bottom:2px;">See All 24 Pieces &rarr;</a>\n'
        f'    </div>\n  </div>\n')


def wire_index(spec, apply_):
    """Put the card at the true front of the feed, and MOVE it if it is not.

    THE BUG THIS REPLACES. The first attempt anchored on the regex
    `<!-- ... -->\s*<div class="card"`, which requires spaces inside the comment.
    The oldest cards in this file are preceded by `<!--TGI-HLS-->` and
    `<!--/TGI-HIROKI-->` — no spaces — so the regex skipped 23 real cards and
    "inserted at the front" at DOM position 24.

    The guard missed it too, for a separate reason: it only asserted that the
    marker came before the NEXT comment-and-card, which is true of any position.
    That is the mis-scoped-guard mistake, not a typo. The check below now
    compares against EVERY card offset in the document, so the only way to pass
    is to actually be first.
    """
    h = IDX.read_text(encoding="utf-8")
    before_cards = len(re.findall(r'<div class="card"', h))
    card = build_card(spec)

    if MARK in h:
        # Already present — excise it so a wrong position can be corrected.
        # DO NOT match on the first '\n  </div>\n' after the marker: card
        # indentation varies across this file, so that regex ate 55 neighbouring
        # cards (266 -> 211). Cut instead to the START OF THE NEXT CARD, which is
        # an unambiguous boundary, and rebuild the card fresh from the spec.
        s = h.index(MARK)
        # Skip OUR OWN opening <div class="card"> before hunting for the next
        # card. Searching from the marker found this card's own div, so the cut
        # removed only the comment and left the card body behind (212 vs 211).
        mine = h.find('<div class="card"', s + len(MARK))
        nxt = h.find('<div class="card"', mine + 10) if mine > 0 else -1
        if nxt < 0:
            sys.exit("! Hoodie and Shorts card is the last card — cannot isolate")
        cstart = h.rfind("<!--", s + len(MARK), nxt)
        end = cstart if cstart > s else nxt
        h = h[:s] + h[end:]

    feed = h.find('class="feed"')
    first = h.find('<div class="card"', feed if feed > 0 else 0)
    if first < 0:
        sys.exit("! could not find any feed card")
    # back up to that card's own preceding comment so we land above it, not inside
    cstart = h.rfind("<!--", 0, first)
    at = cstart if cstart > 0 and h.count("\n", cstart, first) <= 2 else first

    out = h[:at] + card.rstrip() + "\n\n  " + h[at:]

    mark_at = out.index(MARK)
    others = [mm.start() for mm in re.finditer(r'<div class="card"', out)
              if mm.start() > mark_at + len(card)]
    earlier = [mm.start() for mm in re.finditer(r'<div class="card"', out)
               if mm.start() < mark_at]
    checks = [
        ("exactly one Hoodie and Shorts card", out.count(MARK) == 1),
        ("NO card appears before it anywhere in the document",
         not earlier, f"{len(earlier)} card(s) still ahead of it"),
        # Compare to the count taken from the file at entry, NOT to a magic
        # number. The >=265 I first wrote was invented from a browser .card
        # count (266) that includes elements this regex does not match; the real
        # file has 211, so a correct document failed. A guard must measure the
        # thing it is guarding.
        ("no cards were lost",
         len(re.findall(r'<div class="card"', out)) == before_cards,
         f'{len(re.findall(chr(60)+chr(100)+"iv class=" + chr(34) + "card" + chr(34), out))} vs {before_cards}'),
        (f"{len(SLIDES)} slides", card.count('class="gear-slide"') == len(SLIDES)),
        ("every slide image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/hoodie-shorts/[^"]+)"', card))),
        ("tags balance in the card", card.count("<div") == card.count("</div>")),
        ("document still closes", out.rstrip().endswith("</html>")),
    ]
    ok = True
    for c in checks:
        l, p_ = c[0], c[1]; d = c[2] if len(c) > 2 else ""
        print(f"  {'OK  ' if p_ else 'FAIL'} {l} {d if not p_ else ''}"); ok &= p_
    if not ok:
        sys.exit("! refusing to write index.html")
    if apply_:
        IDX.write_text(out, encoding="utf-8")
    return True


def wire_sitemap(apply_):
    t = SMAP.read_text(encoding="utf-8")
    if SLUG in t:
        print("  no change — already in the sitemap"); return False
    row = (f"  <url>\n    <loc>https://thegrassyissue.com{SLUG}</loc>\n"
           f"    <lastmod>{TODAY}</lastmod>\n"
           f"    <changefreq>monthly</changefreq>\n"
           f"    <priority>0.8</priority>\n  </url>\n")
    out = t.replace("</urlset>", row + "</urlset>", 1)
    ok = [("one new <url>", out.count("<url>") == t.count("<url>") + 1),
          ("loc/url tags balance", out.count("<loc>") == out.count("</loc>")),
          ("still closes", out.rstrip().endswith("</urlset>"))]
    good = True
    for l, p in ok:
        print(f"  {'OK  ' if p else 'FAIL'} {l}"); good &= p
    if not good:
        sys.exit("! refusing to write sitemap.xml")
    if apply_:
        SMAP.write_text(out, encoding="utf-8")
    return True


def wire_search(apply_):
    """Add one record in the index's OWN compact key shape.

    The real schema is single-letter keys — u/t/d/g/i/k — not the url/title/text
    I first guessed. Reading one existing record and mirroring its keys is the
    only safe way to add to a file like this; inventing a "url" key would have
    written a record the search overlay can never match.
    """
    recs = json.loads(SIDX.read_text(encoding="utf-8"))
    before = len(recs)
    if any(r.get("u", "").rstrip("/") == SLUG for r in recs):
        print("  no change — already in the search index"); return False

    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    allrows = spec["hoodies"] + spec["shorts_casual"] + spec["shorts_golf"]
    keywords = " ".join(f'{plain(r[1])} {plain(r[2])} {plain(r[3])}' for r in allrows)

    template = recs[0]
    rec = {
        "u": SLUG,
        "t": plain(TITLE),
        "d": plain(BLURB),
        "g": "Drops & Brands",
        "i": "/images/hoodie-shorts/h-sugarloaf-social-club.jpg",
        "k": keywords,
    }
    rec = {k: rec.get(k, "") for k in template}      # exact key order + shape
    recs.insert(0, rec)

    ok = [("one new record", len(recs) == before + 1),
          ("record has a url in the 'u' key", bool(rec.get("u"))),
          ("keys match the existing shape exactly", list(rec) == list(template)),
          ("image exists", (ROOT / rec["i"].lstrip("/")).exists() if rec.get("i") else True),
          ("keywords name every brand",
           all(plain(r[1]) in rec["k"] for r in allrows))]
    good = True
    for l, p_ in ok:
        print(f"  {'OK  ' if p_ else 'FAIL'} {l}"); good &= p_
    if not good:
        sys.exit("! refusing to write search-index.json")
    if apply_:
        SIDX.write_text(json.dumps(recs, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


if __name__ == "__main__":
    a = "--apply" in sys.argv
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    print("== feed card =="); wire_index(spec, a)
    print("== sitemap ==");   wire_sitemap(a)
    print("== search ==");    wire_search(a)
    print("\n  written" if a else "\n  dry run — pass --apply")
