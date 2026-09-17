#!/usr/bin/env python3
"""Refresh the homepage feed card for the rebuilt Accessory Edit.

WHAT WAS THERE. A legacy six-slide card in the old format: data-type="drop"
(singular), per-slide .card-text inline rather than in the canonical
window._slideTexts map, a .card-source row of six outbound brand links, and a
"See the Full Post →" anchor styled inline. Two of its six slides pointed at
dead destinations — the Sentinel slug had been inherited by a different product
and the Depeche link had decayed to a bare homepage — and two carried prices a
year out of date. Every slide sent the reader OFF the site rather than to the
post.

WHAT REPLACES IT. The current house card for a multi-brand roundup:
data-type="drops", the [Drops & Brands] chip, five slides that all link to
/drops/accessories-on-and-off-the-course, captions in the canonical
window._slideTexts literal, and "See all 19 ↗".

FIVE SLIDES, ONE BRAND EACH, chosen to span all three sections of the page so a
reader who sees only one slide still gets the premise: a scorecard holder that
lives in a back pocket, a hand-forged tool that only makes sense on a green, a
ground chair from outside golf entirely, a milled brass crayon, and a $15
squeeze bottle. Prices match the page, which matches the brands' own stores as
read on 17 September 2026.

CAPTIONS ARE WRITTEN FRESH, not lifted from the post. Repeating the product copy
verbatim would trip the site-wide shingle check on the next precis run and reads
as padding to anyone who clicks through.

IDEMPOTENT: any existing card for this URL is removed (balanced-div aware)
before the new one is inserted, and the _slideTexts entry is replaced rather
than appended.
"""
import re, json, sys, os

URL   = "/drops/accessories-on-and-off-the-course"
KEY   = "accessories"
TITLE = "The Accessory Edit: 19 Small Things, On Course and Off"
TODAY = "2026-09-17"
IMG   = "/images/accessories/"

# (image, brand, product line, caption)
SLIDES = [
 (IMG + "bluegrass.jpg", "Bluegrass Fairway",
  "Horween Scorecard Holder &middot; $85",
  "Nineteen accessories from nineteen brands, sorted by where each one actually lives. Bluegrass Fairway "
  "cuts this one in Louisville from American full-grain leather, 6.75 by 8 inches opened, thin enough for a "
  "back pocket. They will heat-stamp initials inside it if you ask at checkout."),
 (IMG + "seamus.jpg", "Seamus Golf",
  "Hand Forged&reg; Greenskeeper Pitch Tool &middot; $76",
  "A three-eighths-inch aerification tyne at one end, a three-quarter-inch tip at the other, and a rounded "
  "face between them for tamping the surface flat. Seamus copied the shape from a tool greenkeepers in "
  "Monterey were using and had a second-generation blacksmith reproduce it."),
 (IMG + "ssc.jpg", "Sugarloaf Social Club",
  "Hidden Gem Crazy Creek Chair &middot; $75",
  "Crazy Creek has been making this folding ground chair for decades, mostly for trailheads and beaches. "
  "Sugarloaf put its Hidden Gem colourway on it. A pound and a half, sixteen and a half inches of seat "
  "height, rated to 250 pounds."),
 (IMG + "gamut.jpg", "Gamut Golf",
  "GG Alignment Sticks V5 &middot; $98",
  "Most alignment sticks are fibreglass driveway markers with a logo printed on them. Gamut turns these "
  "from American-grown hickory on a square profile, with waxed whipping at the collar &mdash; the thread "
  "wrap that held hickory shafts together before steel arrived."),
 (IMG + "huega.jpg", "Huega House",
  "Squeeze Water Bottle &middot; $15",
  "The cheap answer to the bottle question and a good one: 550ml of flexible food-grade plastic with an "
  "easy-flow spout, built to be squeezed one-handed while you keep walking. Nothing to insulate, nothing "
  "to regret leaving behind."),
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
              <img src="{img}" alt="{_alt(b, n)}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{b}</div><div class="gear-slide-name">{n}</div></div>
            </a>
          </div>
''' for img, b, n, _c in SLIDES) + f'''        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="{URL}" class="card-link">See all 19 &#8599;</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

# ------------------------------------------------------------------- guards
if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the gear-arrows lost their inline onclick and would do nothing")
if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")
for img, *_ in SLIDES:
    if not os.path.exists(img.lstrip("/")):
        raise SystemExit(f"slide image missing on disk: {img}")
if len({i for i, *_ in SLIDES}) != len(SLIDES):
    raise SystemExit("a slide image is used twice")
if len({b for _i, b, *_ in SLIDES}) != len(SLIDES):
    raise SystemExit("two slides carry the same brand — one per brand is the point")
if not os.path.exists("drops/accessories-on-and-off-the-course.html"):
    raise SystemExit("the post does not exist — run build-accessories.py first")
_copy = TITLE + " " + " ".join(s[3] for s in SLIDES)
if re.search(r"\bworth\b", re.sub(r"&[a-z]+;", " ", _copy), re.I):
    raise SystemExit("banned word 'worth' in the card copy")
# the card must agree with the page it links to
_post = open("drops/accessories-on-and-off-the-course.html", encoding="utf-8").read()
for _i, _b, _n, _c in SLIDES:
    _price = re.search(r"\$[\d.]+", _n).group(0)
    if _price not in _post:
        raise SystemExit(f"{_b}: card says {_price} but that price is not on the page")

# ---------------------------------------------------------------- homepage
h = open("index.html", encoding="utf-8").read()

i = h.find(URL)
while i != -1:
    s = h.rfind('<div class="card"', 0, i)
    if s == -1:
        break
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
        h = h[:s] + h[end:]
        notes.append("removed the legacy six-slide card (2 dead links, 2 stale prices)")
    else:
        break
    i = h.find(URL)

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
if h.find(anchor) == -1:
    raise SystemExit("canonical window._slideTexts map not found")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)

def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&times;", "×"), ("&rsquo;", "'"),
                 ("&amp;", "&"), ("&ndash;", "–"), ("&reg;", "®"), ("&egrave;", "è")]:
        t = t.replace(a, b)
    return t

k = h.find(anchor)
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(c), ensure_ascii=False) for _i, _b, _n, c in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]
notes.append(f"card rebuilt at the top of the feed with {len(SLIDES)} slides + captions")

# ----------------------------------------------------------------- sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
row = re.search(r"<url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>", sm, re.S)
if row:
    new = re.sub(r"<lastmod>[0-9-]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", row.group(0))
    sm = sm.replace(row.group(0), new)
    notes.append("sitemap: lastmod bumped")
else:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                    f'<changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    notes.append("sitemap: row added")

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)

# ------------------------------------------------------------- post-checks
if apply_:
    h2 = open("index.html", encoding="utf-8").read()
    if h2.count(f'data-carousel="{KEY}"') != 1:
        raise SystemExit("the card was inserted more than once")
    if h2.count(f'"{KEY}": [') != 1:
        raise SystemExit("the _slideTexts entry was inserted more than once")
    blk = re.search(r'"' + KEY + r'": \[(.*?)\n    \],', h2, re.S).group(1)
    if blk.count('"') // 2 != len(SLIDES):
        raise SystemExit("caption count does not match slide count")
    # SCOPE THIS TO OUR OWN CARD. First pass checked the whole file and fired on
    # two unrelated cards that legitimately carry the same strings: the Magazine
    # Edit links depeche-golf.com as a publisher homepage (correct there), and
    # the Water Bottle Edit still carries the dead Sentinel "Basecamp Water
    # Bottle $68" slug. That second one is a real bug, but it belongs to that
    # post, not this one — flagged to Lenny rather than fixed here.
    _s = h2.find(f'data-carousel="{KEY}"')
    _c = h2[h2.rfind('<div class="card"', 0, _s):h2.find('</div>', h2.find('class="card-link"', _s))]
    for dead in ("depeche-golf.com", "76zkc-nctfn-cx85f", "dimpledivot.com"):
        if dead in _c:
            raise SystemExit(f"a dead link from the old card survived: {dead}")
    if _c.count("<a href=\"" + URL) < len(SLIDES):
        raise SystemExit("slides are not all pointing at the post")

print(("wired" if apply_ else "DRY RUN") + f" {URL} into the homepage feed")
for n in notes:
    print("  ·", n)
print(f"  title: {TITLE}")
if not apply_:
    print("\npass --apply to write")
