#!/usr/bin/env python3
"""Wire the Birds of Condor Brand to Know: homepage card, canonical slideTexts,
sitemap, and — the point of the whole exercise — MOVE THE PROFILE POINTER.

THE PROFILE MOVE IS THE REASON THIS POST EXISTS. birds-of-condor carried 14
mentions and its profile:true entry pointed at /drops/australian-golf-brands-and-trips,
a six-brand roundup. /brands/birds-of-condor therefore presented a shared
roundup as the brand's coverage. This script demotes that entry to profile:false
(it stays as a mention — the roundup does still cover them) and installs the new
page as the profile.

EXACTLY ONE profile:true per brand. Guarded below. The demote-don't-delete
pattern is the same one wire-fyfe.py used on 2026-09-14.

brands.json: birds-of-condor already exists, so only `url` and `img` move. Do
not append a duplicate entry.

After this: gen-post-thumbs.py --apply FIRST, then the full brands chain,
ENDING with build-brand-index.py --apply, then generate-search-index.py and
build-ig.py --apply.
"""
import re, json, sys

SLUG = "brand-to-know-birds-of-condor"
URL = f"/drops/{SLUG}"
OLD = "/drops/australian-golf-brands-and-trips"
KEY = "birdsofcondor"
TITLE = "Brand to Know &mdash; Birds of Condor"
PLAIN = "Brand to Know — Birds of Condor"
IMG = "/images/birds-of-condor/"
TODAY = "2026-09-15"
BRAND = "birds-of-condor"

SLIDES = [
 ("tokyo-snapback", "Birds of Condor", "Tokyo Country Club Snapback &middot; $50",
  "Frankie Kimpton booked bands in Melbourne before he made golf hats, and started with ten of them out of a garage. This is the best-selling one &mdash; a Japanese country club that does not exist."),
 ("eldrick", "Birds of Condor", "Eldrick Snapback &middot; $50",
  "Custom tiger camo on black rope. Eldrick is Tiger Woods' actual first name, and that is the entire gag."),
 ("lawnpawn-umbrella", "Birds of Condor", "Lawn Pawn Umbrella &middot; $80",
  "A full-size golf umbrella in mow-line plaid, with “Peace Love & Putts” printed across the inside of the canopy where only the person holding it can read it."),
 ("playing-cards", "Birds of Condor", "Golf Life Playing Cards &middot; $15",
  "Fifty-four cards on black-core stock with green foil edges, in an embossed box sealed with a Triple Eagle sticker. Sold on their US store and nowhere else."),
 ("norm-cover", "Birds of Condor", "Norm Mallet Putter Cover &middot; $50",
  "Blue tie-dye, a cartoon shark in a cap, and a name one syllable from a lawsuit. Tentile shell, crystal velvet lining, biodegradable packaging."),
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
      <a href="{URL}" class="card-link">Read the profile ↗</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

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
                end = m.end(); break
        j = m.end()
    if end and URL in h[s:end]:
        h = h[:s] + h[end:]; notes.append("removed existing card")

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

# ------------------------------------------------------------- 2. brands.json
brands = json.load(open("data/brands.json"))
hit = [b for b in brands if b["slug"] == BRAND]
if not hit:
    raise SystemExit(f"{BRAND} is not in brands.json — this script only moves an existing entry")
b = hit[0]
b["url"] = URL
b["img"] = f"{IMG}tokyo-snapback.jpg"
notes.append(f"brands.json: {BRAND} url -> {URL}")

# ---------------------------------------------------------------- 3. mentions
mm = json.load(open("data/brand-mentions.json"))
lst = mm.setdefault(BRAND, [])
# demote the old roundup rather than deleting it — it still mentions the brand
for e in lst:
    if e.get("url") == OLD and e.get("profile"):
        e["profile"] = False
        notes.append(f"demoted {OLD} from profile to mention")
lst = [e for e in lst if e.get("url") != URL]
lst.insert(0, {"url": URL, "title": PLAIN, "profile": True})
bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
if bad:
    raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
n_prof = sum(1 for e in lst if e["profile"])
if n_prof != 1:
    raise SystemExit(f"{BRAND} must carry exactly one profile:true entry, found {n_prof}")
if not any(e["url"] == OLD for e in lst):
    raise SystemExit("the Australian roundup should stay as a mention, not disappear")
mm[BRAND] = lst

# ----------------------------------------------------------------- 4. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                    f'<changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
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
    print(f"card inserted + {len(SLIDES)} captions | profile moved off the roundup")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print(" ", n)
