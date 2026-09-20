#!/usr/bin/env python3
"""Wire the AXXA Brand to Know: homepage card, slide captions, brands.json,
brand-mentions, sitemap. 20 September 2026.

DIFFERENT FROM wire-birds-of-condor.py IN ONE IMPORTANT WAY. That script MOVED an
existing brands.json entry and demoted an old roundup from profile to mention.
AXXA is new to the site — it is not in brands.json, not in brand-mentions, and
not in the Australian brands roundup (that post covers Big Dog, Birds of Condor,
Gray + Haast, Jet Set, Mackem, Okka, Penta and Random Golf Club). So this APPENDS
rather than moves, and there is no profile pointer to demote. A guard below
refuses to run if AXXA turns out to already exist, because appending a duplicate
brand is how the index grows two cards for one label.

PRICES IN THE SLIDE CAPTIONS ARE AUD AND SAY SO. The homepage feed shows these
captions with no surrounding context, so "$159" there would read as US dollars to
most of the audience. AXXA's storefront converts by location and would show a US
reader about US$116 for the same knit. Every caption carries the A$ prefix for
the same reason the post does.

After this: gen-post-thumbs.py --apply, then the brands chain ending with
build-brand-index.py --apply, then generate-search-index.py.
Affiliate activation is SEPARATE — see data/affiliates.json and
apply-affiliates.py. Nothing here writes a ref parameter.
"""
import json, re, sys

SLUG = "brand-to-know-axxa"
URL = f"/drops/{SLUG}"
KEY = "axxa"
BRAND = "axxa"
TITLE = "Brand to Know &mdash; AXXA"
PLAIN = "Brand to Know — AXXA"
IMG = "/images/axxa/"
TODAY = "2026-09-20"

# The five Lenny picked from the 18-grid.
SLIDES = [
 ("golfer-knit", "AXXA", "Golfer Knit &middot; A$159",
  "730g of cotton with the golfer knitted into it rather than printed on top &mdash; jacquard, worked on the machine. AXXA publish the weight, which not everyone does."),
 ("birdies-please-hoodie", "AXXA", "Birdies Please Hoodie &middot; A$119",
  "420GSM fleece at a 75/25 cotton-poly blend, cut slightly oversized, screen and puff printed. The house weight for everything they make in fleece."),
 ("golf-surf-club-hoodie", "AXXA", "Golf-Surf Club Hoodie &middot; A$119",
  "AGSC is the core line and this is the piece the brand is built on &mdash; seven colourways and by some distance the deepest stock in the catalogue."),
 ("blossom-bogey-polo", "AXXA", "Blossom Bogey Polo &middot; A$59",
  "Their own GolfComfort fabric, a polyester-spandex blend they describe as moisture-wicking and quick-drying. Down from A$80."),
 ("golf-bag-cap", "AXXA", "Golf Bag Cap &middot; A$59",
  "Canvas crown, corduroy brim, an embroidered golf bag on the front and Axxa stitched across the back. Two left at time of writing."),
]

_ENT = re.compile(r"&[a-z]+;|&#\d+;")


def _alt(b, n):
    return re.sub(r"\s+", " ", _ENT.sub("", f"{b} {n}")).strip()


CARD = f'''      <div class="card" data-type="drops">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
''' + "".join(
f'''          <div class="gear-slide">
            <a href="{URL}">
              <img src="{IMG}{s}.jpg" alt="{_alt(b, n)}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{b}</div><div class="gear-slide-name">{n}</div></div>
            </a>
          </div>
''' for s, b, n, _ in SLIDES) + f'''        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="{URL}" class="card-link">Read the profile &#8599;</a>
    </div>
  </div>
'''

ENTRY = {
    "slug": BRAND,
    "name": "AXXA",
    "loc": "Sydney, Australia",
    "regions": ["australia"],
    "cats": ["apparel", "headwear"],
    # TAGS MUST COME FROM THE EXISTING TASTE TAXONOMY. The first version invented
    # "surf-adjacent" and "new-school" because they described AXXA well. Neither
    # exists, and /brands/tag/<slug> is generated from these values — so each
    # would have produced a tag page with exactly one brand on it. Guarded below.
    # post-round-friendly: the catalogue is mostly fleece, knitwear and trackies.
    # design-nerd: jacquard-knitted motifs, published GSM weights, own fabric name.
    "tags": ["independent", "post-round-friendly", "design-nerd"],
    "line": ("Northern Beaches label built between surf and golf. Founded 2022, "
             "jacquard-knitted heavyweight knits, and its own GolfComfort polo fabric."),
    "url": URL,
    "attrs": [],
    "added": TODAY,
    "img": f"{IMG}golfer-knit.jpg",
}

apply_ = "--apply" in sys.argv
notes = []

if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")
if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the card's gear-arrows lost their inline onclick")
# Captions are shown without context on the homepage; an unlabelled $ there
# would read as USD to most of the audience.
for _, _, n, t in SLIDES:
    if re.search(r"(?<![A])\$\d", n + " " + t):
        raise SystemExit(f"unlabelled dollar figure in a slide caption: {n}")

# ---------------------------------------------------------------- 1. homepage
h = open("index.html", encoding="utf-8").read()
i = h.find(URL)
if i != -1:
    s = h.rfind('<div class="card"', 0, i)
    depth, j, end = 0, s, None
    while j < len(h):
        m = re.compile(r"<div\b|</div>").search(h, j)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end(); break
        j = m.end()
    if end and URL in h[s:end]:
        # CUT WHOLE LINES. Slicing exactly from the opening <div to the matching
        # </div> leaves the opening line's indent and the closing line's newline
        # behind, so every rerun deposited six spaces and a blank line — 8 bytes
        # a run, and index.html stopped being byte-stable. Extend the cut to the
        # start of the first line and the end of the last.
        s = h.rfind("\n", 0, s) + 1
        nl = h.find("\n", end)
        end = len(h) if nl < 0 else nl + 1
        h = h[:s] + h[end:]
        h = re.sub(r"\n[ \t]+\n", "\n\n", h)
        h = re.sub(r"\n{3,}", "\n\n", h)
        notes.append("removed existing card (rerun)")

before_cards = len(re.findall(r'<div class="card"', h))
m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
if h.find(anchor) == -1:
    raise SystemExit("canonical window._slideTexts map not found")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)
k = h.find(anchor)


def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&times;", "×"),
                 ("&rsquo;", "'"), ("&amp;", "&")]:
        t = t.replace(a, b)
    return t


entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

after_cards = len(re.findall(r'<div class="card"', h))
if after_cards != before_cards + 1:
    raise SystemExit(f"card count went {before_cards} -> {after_cards}, expected +1")

# ------------------------------------------------------------- 2. brands.json
brands = json.load(open("data/brands.json"))
existing = [b for b in brands if b["slug"] == BRAND]
if existing and existing[0].get("url") != URL:
    raise SystemExit(f"{BRAND} already in brands.json pointing elsewhere — this "
                     "script appends a NEW brand and will not silently overwrite")
if existing:
    existing[0].update(ENTRY); notes.append("brands.json: entry refreshed (rerun)")
else:
    brands.append(ENTRY); notes.append(f"brands.json: appended {BRAND} ({len(brands)} total)")
if sum(1 for b in brands if b["slug"] == BRAND) != 1:
    raise SystemExit("duplicate AXXA entry in brands.json")
# Compare against the UNION of keys across all entries, not brands[0]. Not every
# brand carries every field — brands[0] has no "img" — so checking one arbitrary
# record reported drift on a key that 100+ other records use.
known = set().union(*(set(b) for b in brands))
if not set(ENTRY) <= known:
    raise SystemExit(f"schema drift: unknown keys {sorted(set(ENTRY) - known)}")
required = {"slug", "name", "url", "line", "cats"}
if not required <= set(ENTRY):
    raise SystemExit(f"new entry missing required keys {sorted(required - set(ENTRY))}")

# Every tag, cat and region must already be in use. /brands/tag/<slug> and the
# category and region filters are all generated from these lists, so a value
# invented here produces a page with a single brand on it.
others = [b for b in brands if b["slug"] != BRAND]
for field in ("tags", "cats", "regions"):
    known_vals = set().union(*(set(b.get(field, [])) for b in others))
    novel = [v for v in ENTRY.get(field, []) if v not in known_vals]
    if novel:
        raise SystemExit(
            f"{field} value(s) not in the existing taxonomy: {novel}. "
            f"Pick from {sorted(known_vals)} or add the tag deliberately elsewhere.")

# ---------------------------------------------------------------- 3. mentions
mm = json.load(open("data/brand-mentions.json"))
lst = [e for e in mm.get(BRAND, []) if e.get("url") != URL]
lst.insert(0, {"url": URL, "title": PLAIN, "profile": True})
bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
if bad:
    raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
if sum(1 for e in lst if e["profile"]) != 1:
    raise SystemExit("AXXA must carry exactly one profile:true entry")
mm[BRAND] = lst
notes.append("brand-mentions: profile registered")

# ----------------------------------------------------------------- 4. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                    f'<changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    notes.append("sitemap: row added")
else:
    sm = re.sub(r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[0-9-]+(</lastmod>)",
                lambda m: m.group(1) + TODAY + m.group(2), sm)
    notes.append("sitemap: lastmod bumped")
if sm.count(loc) != 1:
    raise SystemExit("AXXA appears in the sitemap more than once")

# every slide image must exist, or the homepage card renders holes
import os
for s, _, _, _ in SLIDES:
    if not os.path.exists(f"images/axxa/{s}.jpg"):
        raise SystemExit(f"missing slide image: images/axxa/{s}.jpg")

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"card inserted + {len(SLIDES)} captions | AXXA registered as a new brand")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print(" ", n)
