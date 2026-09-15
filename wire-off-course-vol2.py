#!/usr/bin/env python3
"""Wire Off Course Vol 2: homepage card + canonical slideTexts + sitemap +
brand mentions + five new brands.json entries.

WHICH OF THE 24 GET A brands.json ENTRY
---------------------------------------
Fourteen were already in the index. Five more are added here because they are
product brands the index is for and they were simply missing: Whim Golf (we
covered its Reebok collab in Vol 1 and never indexed it), Golf Gods, Foray Golf,
TravisMathew and PXG.

SEVEN ARE DELIBERATELY NOT ADDED, and therefore carry no mention:
  - Pinehurst, Sand Valley, Cabot Saint Lucia, Bandon Dunes — resorts, not
    brands. The index is a brand directory; resort pro shops would change what
    it is.
  - The Golfer's Journal and Fried Egg Golf — media companies with pro shops
    attached. Both belong in the magazine roundup, and TGJ already is.
  - Sweetens Cove — a spirits company named after a golf course. Genuinely
    ambiguous, and there is no CATS value that fits a bottle of bourbon.
If Lenny wants any of these indexed, that is his call, not a silent one made
inside a wiring script.

CATS IS A FIXED LIST in build-brands.py — apparel, equipment, bags, headcovers,
headwear, accessories, grips, art, community. Anything else throws KeyError.
Women's apparel goes under `apparel`; there is no separate value.

After this: gen-post-thumbs.py --apply FIRST, then the full brands chain,
ENDING with build-brand-index.py --apply, then generate-search-index.py and
build-ig.py --apply.
"""
import re, json, sys

SLUG  = "off-course-vol-2-golf-brands-doing-non-golf-things"
URL   = f"/drops/{SLUG}"
KEY   = "offcourse2"
TITLE = "Off Course, Vol. 2 &mdash; Golf Brands Doing Non-Golf Things"
PLAIN = "Off Course, Vol. 2 — Golf Brands Doing Non-Golf Things"
IMG   = "/images/off-course-vol2/"
TODAY = "2026-09-15"

SLIDES = [
 ("gumtree-almond", "Gumtree Golf &amp; Nature Club", "Almond Single Fin Surfboard &middot; $1,950",
  "Twenty-four things made by golf brands that are not golf products, from twenty-four different brands. Gumtree's is a mid-length single fin shaped in California by Almond, based on a board from the founder's own quiver."),
 ("foray-planter", "Foray Golf", "1962 Vintage Book Planter &middot; $68",
  "A ceramic planter made in Japan in 1962, shaped as a stack of books spined Fishing, Hunting, Bowling and Golf. Foray is not manufacturing these &mdash; it is sourcing dated antiques and selling them one at a time."),
 ("whim-cupola", "Whim Golf", "La Cupola Paperweight &middot; $149",
  "Seven and a half pounds of hand-poured concrete and gypsum with a removable flag set into a coffered dome, scaled down from Whim's Milan Design Week installation. Edition of ten."),
 ("tgj-quietplease", "The Golfer&rsquo;s Journal", "Quiet, Please &middot; $185",
  "Two hundred and fifty pages, Smyth-sewn and case-bound on gallery paper, in a clamshell case. Words by Tom Coyne, photographs by Kohjiro Kinno and Christian Hafer."),
 ("bettinardi-plate", "Bettinardi Golf", "Milled License Plate Holder &middot; $110",
  "Cut from a single block of 6061 aluminium on the same CNC machines as the putters, carrying the same honeycomb face-milling pattern. Silver only &mdash; the black is already gone."),
]

# brands.json slugs that get a mention. Resorts and the magazine are absent on
# purpose — see the docstring.
#
# Dormie Workshop and Swag Golf were HERE until 2026-09-15, when Lenny cut the
# belt and the YETI lunch box. Their mentions must come back OUT, which is why
# the URL is purged from every brand below before this list is re-applied —
# otherwise a removed product leaves a dead mention pointing at a post that no
# longer covers that brand.
MENTIONS = ["gumtree-golf", "mogshade", "metalwood-studio", "stitch-golf",
            "birds-of-condor", "vessel", "random-golf-club",
            "rhoback", "no-laying-up", "sugarloaf-social-club", "sunday-golf",
            "bettinardi", "whim-golf", "golf-gods", "foray-golf", "travismathew", "pxg"]

NEW_BRANDS = [
 {"slug": "whim-golf", "name": "Whim Golf", "loc": "Los Angeles, California",
  "regions": ["usa"], "cats": ["apparel", "accessories", "art"],
  "line": "A design-led golf label that treats objects as seriously as garments — concrete paperweights, gallery installations, and the Reebok Classic Leather.",
  "img": f"{IMG}whim-cupola.jpg", "tags": ["design-nerd", "independent"]},
 {"slug": "golf-gods", "name": "Golf Gods", "loc": "Australia",
  "regions": ["australia"], "cats": ["apparel", "accessories"],
  "line": "Australian golf apparel and accessories with the volume turned up, from headcovers to insulated stubby holders.",
  "img": f"{IMG}golfgods-koozie.jpg", "tags": ["loud-on-purpose", "post-round-friendly"]},
 {"slug": "foray-golf", "name": "Foray Golf", "loc": "New York, New York",
  "regions": ["usa"], "cats": ["apparel", "accessories"],
  "line": "Women's golf apparel out of New York, alongside a curated capsule of genuinely vintage homeware sold one piece at a time.",
  "img": f"{IMG}foray-planter.jpg", "tags": ["collector", "independent"],
  "attrs_extra": ["women-founded"]},
 {"slug": "travismathew", "name": "TravisMathew", "loc": "Huntington Beach, California",
  "regions": ["usa"], "cats": ["apparel", "headwear", "accessories"],
  "line": "California golf and lifestyle apparel, plus an eyewear line made from Italian acetate.",
  "img": f"{IMG}travismathew-offdaze.jpg", "tags": ["post-round-friendly"]},
 {"slug": "pxg", "name": "PXG", "loc": "Scottsdale, Arizona",
  "regions": ["usa"], "cats": ["equipment", "apparel", "accessories"],
  "line": "Bob Parsons' clubmaker, and the Darkness iconography that runs across everything from irons to an eight-dollar coaster.",
  "img": f"{IMG}pxg-coaster.jpg", "tags": ["design-nerd"],
  "attrs_extra": ["tour-proven"]},
]

_ENT = re.compile(r'&[a-z]+;|&#\d+;')
def _alt(b, n):
    return re.sub(r'\s+', ' ', _ENT.sub('', f"{b} {n}")).strip()

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
      <a href="{URL}" class="card-link">See all 24 ↗</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

# both arrows must carry the inline handler or this carousel dies silently.
# Scoped to the NEW card: ~170 legacy cards site-wide lack the handler and a
# site-wide count would always fail.
if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the new card's gear-arrows are missing their inline onclick")
if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")

# ---------------------------------------------------------------- 1. homepage
h = open("index.html", encoding="utf-8").read()
i = h.find(URL)
if i != -1:
    s = h.rfind('<div class="card"', 0, i)
    depth, j, end = 0, s, None
    while j < len(h):
        m = re.compile(r'<div\b|</div>').search(h, j)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end()
                break
        j = m.end()
    if end and URL in h[s:end]:
        h = h[:s] + h[end:]
        notes.append("removed existing Off Course Vol 2 card")

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
                 ("&rsquo;", "'"), ("&amp;", "&"), ("&egrave;", "è")]:
        t = t.replace(a, b)
    return t
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

# ------------------------------------------------------------- 2. brands.json
brands = json.load(open("data/brands.json"))
known = set().union(*(set(b) for b in brands))
have = {b["slug"] for b in brands}
added = []

CATS_OK = {"apparel", "equipment", "bags", "headcovers", "headwear",
           "accessories", "grips", "art", "community"}
TAGS_OK = {t for b in brands for t in b.get("tags", [])}
ATTRS_OK = {a for b in brands for a in b.get("attrs", [])}
REGIONS_OK = {r for b in brands for r in b.get("regions", [])}

for nb in NEW_BRANDS:
    e = dict(nb)
    extra = e.pop("attrs_extra", [])
    e["url"] = URL
    e["added"] = TODAY
    e["attrs"] = ["new-to-index"] + extra
    bad = set(e["cats"]) - CATS_OK
    if bad:
        raise SystemExit(f"build-brands.py CATS is a fixed list; {bad} will KeyError")
    if set(e["tags"]) - TAGS_OK:
        raise SystemExit(f"{e['slug']}: unknown taste tag {set(e['tags'])-TAGS_OK}")
    if set(e["attrs"]) - ATTRS_OK:
        raise SystemExit(f"{e['slug']}: unknown attr {set(e['attrs'])-ATTRS_OK}")
    if set(e["regions"]) - REGIONS_OK:
        raise SystemExit(f"{e['slug']}: unknown region {set(e['regions'])-REGIONS_OK}")
    if len(e["tags"]) > 3:
        raise SystemExit(f"{e['slug']}: three taste tags maximum (house rule)")
    drift = set(e) - known
    if drift:
        raise SystemExit(f"brands.json schema drift: {drift}")
    if e["slug"] in have:
        continue
    brands.append(e)
    added.append(e["slug"])
brands.sort(key=lambda b: b["slug"])

# ---------------------------------------------------------------- 3. mentions
mm = json.load(open("data/brand-mentions.json"))
slugs_now = {b["slug"] for b in brands}
missing = [s for s in MENTIONS if s not in slugs_now]
if missing:
    raise SystemExit(f"mention targets not in brands.json: {missing}")
for gone in ("dormie-workshop", "swag-golf"):
    if gone in MENTIONS:
        raise SystemExit(f"{gone}'s product was cut from the post on 9/15 — "
                         "it must not carry a mention of it")
ent = {"url": URL, "title": PLAIN, "profile": False}
# purge this post from EVERY brand first, so a product cut from the post also
# loses its mention. Re-applied below only to the brands still covered.
purged = []
for bslug, lst in mm.items():
    keep = [e for e in lst if e.get("url") != URL]
    if len(keep) != len(lst) and bslug not in MENTIONS:
        purged.append(bslug)
    mm[bslug] = keep
if purged:
    notes.append(f"mentions purged from no-longer-covered brands: {purged}")
for bslug in MENTIONS:
    lst = [e for e in mm.setdefault(bslug, []) if e.get("url") != URL]
    lst.append(ent)
    bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
    if bad:
        raise SystemExit(f"brand-mentions schema drift on {bslug}: {bad[:2]}")
    if sum(1 for e in lst if e["profile"]) > 1:
        raise SystemExit(f"{bslug} has more than one profile:true entry")
    mm[bslug] = lst

# ----------------------------------------------------------------- 4. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    row = (f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
           f'<changefreq>monthly</changefreq><priority>0.8</priority></url>\n')
    sm = sm.replace("</urlset>", row + "</urlset>")
    notes.append("sitemap: row added")
else:
    sm = re.sub(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                lambda m: m.group(1) + TODAY + m.group(2), sm)
    notes.append("sitemap: lastmod bumped")

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"card inserted at top of feed + {len(SLIDES)} captions in the canonical map")
    print(f"brands.json: +{len(added)} ({len(brands)} total) {added}")
    print(f"mentions added on {len(MENTIONS)} brands")
else:
    print("DRY RUN — pass --apply")
    print(f"  card {len(CARD)} chars, {len(SLIDES)} captions")
    print(f"  would add brands: {added}")
    print(f"  mentions on {len(MENTIONS)}: {MENTIONS}")
for n in notes:
    print(" ", n)
