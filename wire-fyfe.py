"""Wire Brand to Know — Fyfe Golf.

Homepage card + canonical slideTexts + sitemap + brand index rewiring.

DIFFERENT FROM THE USUAL WIRE SCRIPT: Fyfe is ALREADY in brands.json, and its
"profile" pointer was aimed at /drops/the-fyfe-putter-cover-edit — an Edit page,
not a profile. This script moves the profile to the new BTK in three places that
must agree or /brands goes inconsistent:
  1. brands.json  url  -> the BTK
  2. brands.json  img  -> a headcover (the putter-cover lead undersold the range)
  3. brand-mentions.json — profile:true moves to the BTK, and the putter cover
     edit is demoted to profile:false rather than removed. build-brands.py pins
     whichever entry carries profile:true to the top of the coverage page and
     badges it "The Profile"; two true entries would double-badge.

Also bumps the MacKenzie mention so the collab page keeps its entry, and
rewrites the stale "20 editions" count on the every-edition page (21 and 22
landed 2026-08-11).

After this: gen-post-thumbs.py --apply, then the full brands chain, ENDING with
build-brand-index.py --apply, then generate-search-index.py and build-ig.py.
"""
import re, json, sys

SLUG  = "brand-to-know-fyfe-golf"
URL   = f"/drops/{SLUG}"
OLD   = "/drops/the-fyfe-putter-cover-edit"
MACK  = "/drops/fyfe-x-mackenzie-every-edition"
KEY   = "fyfe"
TITLE = ("Brand to Know: Fyfe Golf &mdash; Harris Tweed, RAF Flight Suits and a "
         "Workshop in Fife")
PLAIN = ("Brand to Know: Fyfe Golf — Harris Tweed, RAF Flight Suits and a Workshop "
         "in Fife")
IMG   = "/images/fyfe-btk/"
TODAY = "2026-09-14"

SLIDES = [
 ("rothesay", "Fyfe Golf", "Rothesay Harris Tweed &middot; &pound;75",
  "Neil Rennie spent years walking into Scottish pro shops and finding nothing in them made in Scotland. He came out of fashion, knew who still wove cloth, and launched Fyfe in November 2021. Everything is cut and sewn to order in a workshop in Fife."),
 ("jura-mini", "Fyfe Golf", "Jura Sunset Mini Driver &middot; &pound;69",
  "Harris Tweed from the Isle of Harris, tartans from Perthshire and Selkirk, waxed canvas from Halley Stevensons in Dundee, merino from Todd &amp; Duncan at Loch Leven. Fyfe names every mill it buys from, which is rarer than it sounds."),
 ("black-grouse-hc", "Fyfe Golf", "Black Grouse Houndstooth &middot; &pound;65",
  "Twenty-three headcovers on the page, all in stock. The house build is two cloths seamed together — a body and a contrast band — over organic cotton fleece, with a leather or woven seam label."),
 ("marine-suede-tan", "Fyfe Golf", "Marine Suede Blade &middot; &pound;69",
  "Marine suede from the Clyde, chosen in Fyfe's words for the particular quality of a material that improves with exposure. The Between Tides collection was built around cloth that records use rather than resisting it."),
 ("harbour-seersucker", "Fyfe Golf", "Harbour Seersucker Blade &middot; &pound;69",
  "Then there are the projects: RAF flight suits cut into covers, Augusta caddie coveralls reworked on Masters Wednesday, twelve per style. Seven collections in four years built from cloth that had a previous job."),
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
        notes.append("removed existing Fyfe BTK card")

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
if h.find(anchor) == -1:
    raise SystemExit("canonical window._slideTexts map not found — do NOT fall back "
                     "to a registration block, nothing reads __slideTexts")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)
k = h.find(anchor)
def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&pound;", "£"),
                 ("&times;", "×"), ("&rsquo;", "'"), ("&amp;", "&")]:
        t = t.replace(a, b)
    return t
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

# Both arrows in OUR card need the inline onclick or this carousel dies silently.
# Scope the check to CARD — index.html still carries ~170 legacy cards whose
# arrows predate the handler, so a site-wide count comparison always fails.
if (CARD.count('onclick="gearSlide(this, -1)"') != 1
        or CARD.count('onclick="gearSlide(this, 1)"') != 1):
    raise SystemExit("the new card's gear-arrows are missing their inline onclick")
if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")

# ------------------------------------------------- 2. brands.json: move profile
brands = json.load(open("data/brands.json"))
fy = next((b for b in brands if b["slug"] == "fyfe-golf"), None)
if fy is None:
    raise SystemExit("fyfe-golf missing from brands.json — expected it to exist")
fy["url"] = URL
fy["img"] = f"{IMG}rothesay.jpg"
fy["line"] = ("Harris Tweed and tartan headcovers made to order in Fife &mdash; plus "
              "RAF flight suits and Augusta coveralls cut into covers.").replace("&mdash;", "—")
fy["cats"] = sorted(set(fy["cats"]) | {"headcovers", "accessories"})
fy["tags"] = sorted(set(fy.get("tags", [])) | {"made-by-hand", "design-nerd"})
known = set().union(*(set(b) for b in brands))
drift = set(fy) - known
if drift:
    raise SystemExit(f"brands.json schema drift on fyfe-golf: {drift}")

# ------------------------------------------- 3. mentions: profile flag moves
mm = json.load(open("data/brand-mentions.json"))
ent = {"url": URL, "title": PLAIN, "profile": True}
lst = [e for e in mm.setdefault("fyfe-golf", []) if e.get("url") != URL]
for e in lst:                                  # demote the old profile
    if e.get("url") == OLD:
        e["profile"] = False
lst.insert(0, ent)
bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
if bad:
    raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
if sum(1 for e in lst if e["profile"]) != 1:
    raise SystemExit("fyfe-golf must carry exactly one profile:true entry")
mm["fyfe-golf"] = lst

mk = [e for e in mm.setdefault("mackenzie", []) if e.get("url") != URL]
mk.append({"url": URL, "title": PLAIN, "profile": False})
mm["mackenzie"] = mk

# ------------------------------------------------------------- 4. sitemap
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

# ------------------------------- 5. the MacKenzie page still says 20 editions
mkp = f"drops/{MACK.split('/')[-1]}.html"
mh = open(mkp, encoding="utf-8").read()
before = mh
mh = mh.replace("20 editions", "22 editions").replace("twenty editions", "twenty-two editions")
mh = mh.replace("Twenty editions", "Twenty-two editions").replace("20 Editions", "22 Editions")
mack_note = (f"{mkp}: edition count updated" if mh != before
             else f"{mkp}: no literal '20 editions' string found — CHECK BY HAND")

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    open(mkp, "w", encoding="utf-8").write(mh)
    print(f"card inserted at top of feed + {len(SLIDES)} captions in the canonical map")
    print(f"brands.json: fyfe-golf profile -> {URL}, lead image -> rothesay.jpg")
    print(f"mentions: fyfe-golf has {len(lst)} entries, 1 profile; mackenzie +1")
else:
    print("DRY RUN — pass --apply")
    print(f"  card {len(CARD)} chars, {len(SLIDES)} captions")
    print(f"  fyfe-golf url {OLD} -> {URL}")
    print(f"  mentions: {len(lst)} entries, profile on {[e['url'] for e in lst if e['profile']]}")
for n in notes + [mack_note]:
    print(" ", n)
