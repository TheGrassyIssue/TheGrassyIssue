"""Wire The Dyneema Edit: homepage card + canonical slideTexts + sitemap + a
Sentinel Golf coverage mention. Adapted from wire-apres.py (same three traps:
inline onclick on the arrows, splice into `window._slideTexts = {`,
brand-mentions schema {url,title,profile}). No brands.json entry — Sentinel is
already in the index; Hawbuck/DSPTCH/Ultralitesacks are not golf brands.
Idempotent.
"""
import re, json, sys, os

SLUG  = "the-dyneema-edit"
URL   = f"/drops/{SLUG}"
KEY   = "dyneema"
BRAND = "sentinel-golf"
TITLE = "The Dyneema Edit &mdash; A Golf Bag, a Pouch, a Wallet and a Sling in the Fiber That Floats"
PLAIN = "The Dyneema Edit — A Golf Bag, a Pouch, a Wallet and a Sling in the Fiber That Floats"
IMG   = "/images/dyneema/"
TODAY = "2026-09-10"

SLIDES = [
 ("walker-2", "Sentinel Golf &times; MacKenzie", "Basecamp Walker, Black Dyneema &middot; $890",
  "Dyneema is a polyethylene fibre its maker calls fifteen times stronger than steel by weight and light enough to float. Sentinel has MacKenzie build the Walker in it: two pounds, leather trim, made to order in Beaverton."),
 ("pouch-1", "Sentinel Golf", "Basecamp Pouch, Clay Dyneema &middot; $64",
  "Nine and a half by six inches with the fibre grid showing through the front, a carabiner loop for a bag ring and a YKK AquaGuard zip. Cut and sewn in New York."),
 ("hawbuck-1", "Hawbuck", "Lean Wallet H01 &middot; $35",
  "Five grams and under a millimetre thick, in the Hybrid composite with a woven polyester face. It will not absorb water, which is the whole case for it after a rain delay."),
 ("dsptch-1", "DSPTCH", "Zero-1 Bag, RND Edition &middot; $248",
  "A six-litre sling in 5.0 oz Dyneema Composite Fabric bonded to perforated EVA foam, with a Fidlock strap. The piece for nine holes after work when the bag stays in the car."),
 ("ditty-1", "Ultralitesacks", "Ultralight Zip Ditty Bag &middot; from $17",
  "Sewn in Yellville, Arkansas in Ultra, the other UHMWPE laminate, at 13 to 33 grams. Four sizes to organise the inside of a golf bag: balls, cables, the rain glove."),
]
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
      <a href="{URL}" class="card-link">See all 28 ↗</a>
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
        print("removed existing Dyneema card")

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
                          re.sub(r'&times;', '×', t)))), ensure_ascii=False)
    for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

# ------------------------------------------------------------- 2. brand index
mm = json.load(open("data/brand-mentions.json"))
ent = {"url": URL, "title": PLAIN, "profile": False}
lst = mm.setdefault(BRAND, [])
lst = [e for e in lst if e.get("url") != URL]
lst.append(ent)
bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
if bad:
    raise SystemExit(f"brand-mentions schema drift, refusing to write: {bad[:2]}")
mm[BRAND] = lst

# ----------------------------------------------------------------- 4. sitemap
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
    print(f"card inserted at top of feed + {len(SLIDES)} captions in the canonical map")
    print(f"brand-mentions.json: {BRAND} -> {len(mm[BRAND])} entry/entries")
    print(sitemap_note)
else:
    print("DRY RUN — pass --apply")
    print(f"  would insert card ({len(CARD)} chars) + {len(SLIDES)} captions")
    print(f"  would add brand-mentions {BRAND} ({len(mm[BRAND])} total)")
    print(f"  {sitemap_note}")
