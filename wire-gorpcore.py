#!/usr/bin/env python3
"""Put the Gorpcore page into the homepage feed as a fresh post.

/brands/tag/gorpcore is a taxonomy page rather than a /drops post, but it now
carries 2,700 words, ten brand carousels and its own FAQ schema, so it behaves
like a post and belongs in the feed like one. The card type is "drops" with the
[Drops & Brands] chip, matching every other multi-brand product roundup in the
feed (the wedges, the divot tools, the putter switch).

FIVE SLIDES, ONE BRAND EACH, chosen to span the whole argument of the page: a
mountain-grade waterproof, a Dyneema carry bag, a 1982 climbing pant, a bag that
behaves like a backpack, and a cotton work shirt with no membrane in it at all.
Each caption carries a fact that stands on its own, because a reader who only
sees slide three should still come away knowing something.

The captions here are deliberately NOT lifted from the page they link to. The
homepage and the page are not competing for the same query, but repeating the
copy verbatim would trip the site-wide shingle check on the next precis run and
would read as padding to anyone who clicks through.

IDEMPOTENT: an existing card for this URL is removed before the new one is
inserted, and the _slideTexts entry is replaced rather than appended.
"""
import re, json, sys, os

URL = "/brands/tag/gorpcore"
KEY = "gorpcore"
TITLE = "Gorpcore Golf: Ten Brands Borrowing From the Trail"
TODAY = "2026-09-17"

# (image, brand, product line, caption)
SLIDES = [
 ("/images/gorpcore/sounder-protsp-1.jpg", "Sounder",
  "&times; Protected Species &middot; &pound;275",
  "Ten brands where the outdoor borrowing is structural rather than decorative. Sounder&rsquo;s "
  "collaboration with Protected Species holds back a 15,000mm column of water, with seams that are "
  "laser-cut and welded instead of stitched, and a guarantee on the waterproofing that runs two years."),
 ("/images/sentinel-golf/basecamp-walker-black-dyneema-1.jpg", "Sentinel Golf",
  "Basecamp Walker &middot; $890",
  "Dyneema composite is not woven &mdash; it is a laminate, polyethylene fibre pressed in sheets "
  "between films, and it feels closer to paper than to nylon. Sentinel builds this one to order in "
  "Minneapolis on six to eight weeks, with no leather at any point on it."),
 ("/images/gramicci/gramicci-pant.jpg", "Gramicci",
  "Gramicci Pant &middot; $100",
  "The oldest thing on the list and the one that never aimed at golf at all. Two details carried "
  "over from the 1982 original do the work: a diamond panel set into the crotch, and a belt you can "
  "tighten with one hand. Climbers needed both. So, it turns out, does a backswing."),
 ("/images/gorpcore/ghost-kovert-1.jpg", "Ghost Golf",
  "Anyday &middot; Kovert Ops &middot; $415",
  "Read the spec sheet without the word golf on it and this is a pack: a magnetic pocket sized for "
  "a rangefinder, insulated bottle sleeves on either side, waterproof valuables pockets, legs in "
  "carbon fibre. Seven colourways, all the same price."),
 ("/images/gorpcore/agronomy-ss-shirt-1.jpg", "Agronomy Workshop",
  "S/S Heavyweight Work Shirt &middot; $136",
  "Not every answer here involves a membrane. Agronomy Workshop runs to four products total, hand-"
  "dyed and hand-sewn in Los Angeles, and the whole brand started from one mock-neck cotton shirt "
  "with space in the chest pocket for three tees."),
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
      <a href="{URL}" class="card-link">See all 10 &#8599;</a>
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
if not os.path.exists("brands/tag/gorpcore.html"):
    raise SystemExit("brands/tag/gorpcore.html does not exist — run build-brand-taxonomy.py first")
if re.search(r"\bworth\b", re.sub(r"&[a-z]+;", " ", TITLE + " " + " ".join(s[3] for s in SLIDES)), re.I):
    raise SystemExit("banned word 'worth' in the card copy")

# ---------------------------------------------------------------- homepage
h = open("index.html", encoding="utf-8").read()

# remove any existing card for this URL, balanced-div aware
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
        notes.append(f"removed an existing card for {URL}")
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
                 ("&amp;", "&"), ("&ndash;", "–"), ("&pound;", "£")]:
        t = t.replace(a, b)
    return t

k = h.find(anchor)
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(c), ensure_ascii=False) for _i, _b, _n, c in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]
notes.append(f"card inserted at the top of the feed with {len(SLIDES)} slides + captions")

# ----------------------------------------------------------------- sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
row = re.search(r"<url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>", sm, re.S)
if row:
    new = re.sub(r"<lastmod>[0-9-]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", row.group(0))
    sm = sm.replace(row.group(0), new)
    notes.append("sitemap: lastmod bumped")
else:
    raise SystemExit("gorpcore is not in the sitemap — wire-brand-taxonomy.py should have added it")

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

print(("wired" if apply_ else "DRY RUN") + f" {URL} into the homepage feed")
for n in notes:
    print("  ·", n)
print(f"  title: {TITLE}")
if not apply_:
    print("\npass --apply to write")
