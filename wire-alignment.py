"""Wire The Alignment Stick Edit: homepage card + canonical slideTexts + sitemap +
brands.json entries for the 11 makers not yet in the Index (+ a mention for
Gamut, already indexed). Adapted from wire-dyneema.py; same three traps. After
this: run the brands chain and END with build-brand-index.py --apply.
"""
import re, json, sys, os

SLUG  = "the-alignment-stick-edit"
URL   = f"/drops/{SLUG}"
KEY   = "alignsticks"
TITLE = "The Alignment Stick Edit &mdash; Twelve Hand-Painted Pairs for Better Practice, in Hickory, Ash and Walnut"
PLAIN = "The Alignment Stick Edit — Twelve Hand-Painted Pairs for Better Practice, in Hickory, Ash and Walnut"
IMG   = "/images/alignment/"
TODAY = "2026-09-14"

SLIDES = [
 ("thwack-1", "Thwack Sporting Co.", "Pioneer Series &middot; $109",
  "Twelve pairs of alignment sticks, every one wood and painted or wrapped by hand, from small shops in West Virginia, Minnesota, New York, North Dakota, Florida, Scotland and Sweden. Thwack wraps American hickory in waxed Irish linen thread."),
 ("bubbawhips-1", "BubbaWhips USA", "Custom Builder &middot; $99",
  "The original: Erik Heltne started painting hickory in Minnesota in 2017, and the sticks were in Ryder Cup bags by that autumn. Pick a base and ring colours; nail caps, matte seal."),
 ("hazy-1", "Hazy Golf &times; Sun Mountain", "Limited Edition &middot; $130",
  "Fifty numbered pairs in red, white and navy with brass caps, finished by hand in Newburgh, New York, to mark Sun Mountain’s Hometown USA bag."),
 ("ekorre-1", "Ekorre Golf", "Three Stripes &middot; 2,400 kr",
  "Six strips of Swedish ash laminated into a hexagon the way a split-cane fly rod is built, by a cabinetmaker in Sigtuna who caddied in Chile as a boy. About $255 before duty."),
 ("scotchskins-1", "Scotch &amp; Skins", "Sawgrass &middot; $75",
  "Appalachian hickory stained green, sealed in beeswax and capped in bronze, from the glove company. Plus three drills that make any pair earn its place in the bag."),
]

NEW_BRANDS = [
 {"slug":"thwack-sporting-co","name":"Thwack Sporting Co.","loc":"West Virginia","regions":["usa"],"cats":["accessories"],
  "line":"American hickory alignment sticks wrapped by hand in waxed Irish linen thread — a first run out of West Virginia, 2026.","img":f"{IMG}thwack-1.jpg","tags":["made-by-hand","design-nerd"]},
 {"slug":"bubbawhips","name":"BubbaWhips USA","loc":"Minnesota","regions":["usa"],"cats":["accessories"],
  "line":"The original hickory alignment stick, hand painted in Minnesota since 2017 and in Ryder Cup bags the same year.","img":f"{IMG}bubbawhips-1.jpg","tags":["made-by-hand"]},
 {"slug":"scotch-and-skins","name":"Scotch & Skins","loc":"USA","regions":["usa"],"cats":["accessories"],
  "line":"A glove company that also turns Appalachian hickory into beeswax-sealed, bronze-capped alignment sticks.","img":f"{IMG}scotchskins-1.jpg","tags":["made-by-hand","quiet-luxury"]},
 {"slug":"noreaster-sticks","name":"Nor'easter Sticks","loc":"New England","regions":["usa"],"cats":["accessories"],
  "line":"Custom hickory alignment sticks, painted and laser-etched to order, with a Nantucket streak.","img":f"{IMG}noreaster-1.jpg","tags":["made-by-hand"]},
 {"slug":"hazy-golf","name":"Hazy Golf","loc":"Newburgh, NY","regions":["usa"],"cats":["accessories"],
  "line":"Hickory alignment sticks finished by hand in the Hudson Valley, named for the founder's daughters; a numbered Sun Mountain edition in 2026.","img":f"{IMG}hazy-1.jpg","tags":["made-by-hand","quiet-luxury"]},
 {"slug":"clutch-golf-company","name":"Clutch Golf Company","loc":"USA","regions":["usa"],"cats":["accessories"],
  "line":"Handmade 42-inch hickory alignment sticks at $55, from a shop founded on making the gear it couldn't find.","img":f"{IMG}clutch-1.jpg","tags":["made-by-hand","muni-energy"]},
 {"slug":"hickory-and-heath","name":"Hickory & Heath","loc":"USA","regions":["usa"],"cats":["accessories"],
  "line":"Family-owned; cuts, stains and paints hickory alignment sticks to your colours and stripe design.","img":f"{IMG}hickoryheath-1.jpg","tags":["made-by-hand"]},
 {"slug":"beavertail-golf-co","name":"Beavertail Golf Co.","loc":"Dickinson, ND","regions":["usa"],"cats":["accessories"],
  "line":"Hunter Myran hand paints hickory alignment sticks in North Dakota, names on both ends included, since 2024.","img":f"{IMG}beavertail-1.jpg","tags":["made-by-hand","muni-energy"]},
 {"slug":"out-west-atelier","name":"Out West Atelier","loc":"Panama City Beach, FL","regions":["usa"],"cats":["accessories"],
  "line":"Small-batch hardwood goods from the Florida panhandle — the only black walnut alignment sticks in the category.","img":f"{IMG}outwest-1.jpg","tags":["made-by-hand","quiet-luxury"]},
 {"slug":"scotsticks","name":"ScotSticks","loc":"Scotland","regions":["europe"],"cats":["accessories"],
  "line":"Ash alignment sticks made to order in Scotland by a maker with an R&A-funded PhD in golf-ball design.","img":f"{IMG}scotsticks-1.jpg","tags":["made-by-hand"]},
 {"slug":"ekorre-golf","name":"Ekorre Golf","loc":"Sigtuna, Sweden","regions":["europe"],"cats":["accessories"],
  "line":"A cabinetmaker's hexagonal ash alignment sticks, laminated like a split-cane fly rod so they flex and return straight.","img":f"{IMG}ekorre-1.jpg","tags":["made-by-hand","design-nerd"]},
]
MENTION_ALSO = ["gamut-golf"]
_ENT = re.compile(r'&[a-z]+;|&#\d+;')
def _alt(b, n):
    """Plain-text alt: strip entities first, THEN collapse whitespace, or the
    gap left by a stripped &mdash; survives as a double space."""
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
      <a href="{URL}" class="card-link">See all 12 ↗</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv

# ---------------------------------------------------------------- 1. homepage
h = open("index.html", encoding="utf-8").read()

# drop any previous version of this card (idempotency)
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
        print("removed existing Alignment card")

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
k = h.find(anchor)
if k == -1:
    raise SystemExit("canonical window._slideTexts map not found — do NOT fall "
                     "back to a registration block, nothing reads __slideTexts")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)
k = h.find(anchor)
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(re.sub(r'&mdash;', '—',
                          re.sub(r'&middot;', '·',
                          re.sub(r'&egrave;', 'è',
                          re.sub(r'&times;', '×', re.sub(r'&amp;', '&', t))))), ensure_ascii=False)
    for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

# ------------------------------------------------------------- 2. brand index
brands = json.load(open("data/brands.json"))
known = set().union(*(set(b) for b in brands))
have = {b["slug"] for b in brands}
added = []
for nb in NEW_BRANDS:
    e = dict(nb); e["url"] = URL; e["added"] = TODAY; e["attrs"] = ["new-to-index"]
    drift = set(e) - known
    if drift: raise SystemExit(f"brands.json schema drift: {drift}")
    if e["slug"] in have: continue
    brands.append(e); added.append(e["slug"])
brands.sort(key=lambda b: b["slug"])

mm = json.load(open("data/brand-mentions.json"))
ent = {"url": URL, "title": PLAIN, "profile": False}
for bslug in [nb["slug"] for nb in NEW_BRANDS] + MENTION_ALSO:
    lst = [e for e in mm.setdefault(bslug, []) if e.get("url") != URL]
    lst.append(ent)
    bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
    if bad: raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
    mm[bslug] = lst

sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    row = (f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
           f'<changefreq>monthly</changefreq><priority>0.8</priority></url>\n')
    sm = sm.replace("</urlset>", row + "</urlset>")
    sitemap_note = "sitemap: added"
else:
    sm = re.sub(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                lambda m: m.group(1) + TODAY + m.group(2), sm)
    sitemap_note = "sitemap: lastmod bumped"

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    print(f"card inserted at top of feed + {len(SLIDES)} captions in the canonical map")
    print(f"brands.json: +{len(added)} ({len(brands)} total); mentions on {len(NEW_BRANDS)+len(MENTION_ALSO)} brands")
    print(sitemap_note)
else:
    print("DRY RUN — pass --apply")
    print(f"  would insert card ({len(CARD)} chars) + {len(SLIDES)} captions")
    print(f"  would add {len(added)} brands + mentions")
    print(f"  {sitemap_note}")
