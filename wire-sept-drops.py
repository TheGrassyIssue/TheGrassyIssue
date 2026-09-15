"""Wire The Drop Report: homepage card + canonical slideTexts + sitemap +
brand mentions for all eleven brands covered.

PAYNTR: not in brands.json at all, despite us having already published "The
PAYNTR Collab Edit". The mentions gate says no entry = no coverage page, so it
was silently missing from /brands. Added here. Footwear goes under `apparel` —
`shoes` is not in build-brands.py's fixed CATS list and adding it throws
KeyError.

After this: gen-post-thumbs.py --apply, then the full brands chain, ENDING with
build-brand-index.py --apply, then generate-search-index.py and build-ig.py.
"""
import re, json, sys

SLUG  = "the-drop-report-september-2026"
URL   = f"/drops/{SLUG}"
KEY   = "dropreport"
TITLE = "The Drop Report &mdash; Everything That Landed, Brand by Brand"
PLAIN = "The Drop Report — Everything That Landed, Brand by Brand"
IMG   = "/images/sept-drops/"
TODAY = "2026-09-14"

SLIDES = [
 ("malbon-shards", "Malbon Golf", "Arsham Shards Hoodie &middot; $178",
  "Twenty-six brands checked, eleven with something new. Malbon put fourteen Arsham pieces up on 9/10 with no press release, no journal post and no coverage anywhere &mdash; the drop exists only in the product feed."),
 ("ssc-tiago", "Sugarloaf Social Club", "SSC &times; First Tee &middot; $105",
  "Five headcovers designed by named junior golfers, published 9/13. Sugarloaf's own line: all proceeds from the collaboration go to the First Tee."),
 ("mogshade-onlyhuman", "Mogshade", "Only Human 2.0 &middot; Sold Out",
  "British artist David Shillinglaw with a Lisbon art space, fifteen made from rescued cloth woven in the Serra da Estrela. Gone in five days &mdash; as was every other partner-credited Mogshade piece this month."),
 ("seamus-palmer", "Seamus Golf", "Arnold Palmer Umbrella &middot; $155",
  "Citrus Brisa leather under all-over Palmer signature umbrella embroidery, handcrafted in Oregon. Six pieces cover the bag, and personalisation is switched off across the line."),
 ("gamut-lonewolf", "Gamut Golf", "Lone Wolf Headcover &middot; $108",
  "Black suede over waxed slate canvas. Three drops in six weeks from a very small shop, three of five pieces sold out, and the alignment sticks now on V4 in square-profile hickory."),
]

# brands.json slug -> already in the index?
MENTIONS = ["malbon", "sugarloaf-social-club", "mogshade", "seamus", "gamut-golf",
            "eastside-golf", "siegelman-stable", "students-golf", "apres-golf",
            "jones-sports-co", "payntr"]

NEW_BRANDS = [
 {"slug": "payntr", "name": "PAYNTR Golf", "loc": "UK / USA", "regions": ["europe", "usa"],
  "cats": ["apparel"],
  "line": "Spikeless golf footwear built on carbon plates and Clarino uppers — and a collaboration habit, five partner shoes in six weeks.",
  "img": f"{IMG}payntr-vessel.jpg", "tags": ["design-nerd"]},
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
      <a href="{URL}" class="card-link">See all 23 ↗</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

# both arrows must carry the inline handler or this carousel dies silently
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
        notes.append("removed existing Drop Report card")

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
for nb in NEW_BRANDS:
    e = dict(nb); e["url"] = URL; e["added"] = TODAY; e["attrs"] = ["new-to-index"]
    drift = set(e) - known
    if drift:
        raise SystemExit(f"brands.json schema drift: {drift}")
    if e["slug"] in have:
        continue
    brands.append(e); added.append(e["slug"])
brands.sort(key=lambda b: b["slug"])

CATS_OK = {"apparel", "equipment", "bags", "headcovers", "headwear",
           "accessories", "grips", "art", "community"}
for nb in NEW_BRANDS:
    bad = set(nb["cats"]) - CATS_OK
    if bad:
        raise SystemExit(f"build-brands.py CATS is a fixed list; {bad} will KeyError")

# ---------------------------------------------------------------- 3. mentions
mm = json.load(open("data/brand-mentions.json"))
slugs_now = {b["slug"] for b in brands}
missing = [s for s in MENTIONS if s not in slugs_now]
if missing:
    raise SystemExit(f"mention targets not in brands.json: {missing}")
ent = {"url": URL, "title": PLAIN, "profile": False}
for bslug in MENTIONS:
    lst = [e for e in mm.setdefault(bslug, []) if e.get("url") != URL]
    lst.append(ent)
    bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
    if bad:
        raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
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
    print(f"  mentions on: {MENTIONS}")
for n in notes:
    print(" ", n)
