#!/usr/bin/env python3
"""Wire the late-season putter switch: homepage feed card, sitemap, search index.

NO 301 HERE, deliberately. Two putter pages are already live and stay live:
/drops/5-zero-torque-putters-worth-your-attention and
/drops/the-2026-putter-drop-8-worth-the-cash. Depth over consolidation is the
house rule; the new post links to both rather than absorbing them.

CARD TYPE is data-type="drops" with the [Drops &amp; Brands] tag, matching every
other product roundup in the feed (the divot tools, the towels, the wedges).
Field Notes is for place-and-time reporting, which this is not.

FIVE SLIDES, one per putter, and each caption carries a fact that stands on its
own — a reader who only sees slide three should still learn something. Captions
go in the canonical window._slideTexts literal; the arrows need their inline
onclick or they do nothing.
"""
import re, json, sys, os

SLUG = "late-season-putter-switch"
URL = f"/drops/{SLUG}"
KEY = "putterswitch"
TITLE = "Twenty Putters for the Late-Season Switch, From $170 to $799"
IMG = "/images/putter-switch/"
TODAY = "2026-09-17"

SLIDES = [
 ("piretti", "Piretti", "No-Torque Savona 2.5 &middot; $549",
  "Eighteen putters you can buy today and two on presale, every price read off the brand&rsquo;s own page on 9/16/26 — and four of the eighteen are marked down right now because the new model year lands in October."),
 ("macgregor", "MacGregor", "MT Milled 002 &middot; $169.99",
  "The cheapest milled putter here by a distance, down from $199.99. One billet of carbon steel, CNC milled, weight pushed out into the wings, and a 360-gram head that is centre-shafted and face balanced."),
 ("bettinardi-bb28", "Bettinardi", "BB28 Armlock &middot; $495",
  "Armlock putters carry loft that looks wrong on paper — the BB28 runs 5 degrees — and it is there for one reason: to cancel out the forward press the setup demands."),
 ("sub70-001z", "Sub 70", "Sycamore 001Z &middot; $199",
  "Almost every zero-torque putter arrives as a mallet, because the geometry is easier there. Sub 70 built one as a blade and kept the compact profile better players ask for."),
 ("scotty", "Scotty Cameron", "Phantom 9.5R &middot; Presale",
  "Two of the twenty are not in shops yet. Scotty's Phantom 9.5R lands 9/30 and Mizuno's zero-torque Z necks on 10/30 — which is exactly why the outgoing model year is cheap this month."),
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
      <a href="{URL}" class="card-link">See all 20 &#8599;</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the new card's gear-arrows are missing their inline onclick")
if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")
for s, _b, _n, _t in SLIDES:
    if not os.path.exists(f"images/putter-switch/{s}.jpg"):
        raise SystemExit(f"slide image missing on disk: {s}.jpg")
if len({s for s, *_ in SLIDES}) != len(SLIDES):
    raise SystemExit("a slide image is used twice")
if not os.path.exists(f"drops/{SLUG}.html"):
    raise SystemExit(f"drops/{SLUG}.html does not exist — run build-putter-switch.py first")

# ---------------------------------------------------------------- 1. homepage
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
k = h.find(anchor)
def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&times;", "×"),
                 ("&rsquo;", "'"), ("&amp;", "&"), ("&ndash;", "–")]:
        t = t.replace(a, b)
    return t
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]
notes.append(f"card inserted with {len(SLIDES)} slides + captions")

# ----------------------------------------------------------------- 2. sitemap
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

# ------------------------------- 3. the two existing putter pages link BACK here
# A new page nobody links to is a new page nobody finds. Both existing putter
# posts get one contextual link, inserted once, never duplicated.
BACKLINK = ('<p>Shopping a switch rather than a category? We put twenty putters — eighteen in '
            f'stock and two on presale — side by side in <a href="{URL}">the Late-Season Putter '
            'Switch</a>.</p>')
linked = []
for p in ("drops/5-zero-torque-putters-worth-your-attention.html",
          "drops/the-2026-putter-drop-8-worth-the-cash.html"):
    if not os.path.exists(p):
        notes.append(f"!! {p} not found — backlink skipped")
        continue
    t = open(p, encoding="utf-8").read()
    if URL in t:
        continue
    anchor_faq = t.find('<h2 class="products-hdr">Questions</h2>')
    at = anchor_faq if anchor_faq != -1 else t.find('<section class="more"')
    if at == -1:
        notes.append(f"!! no insertion point in {p} — backlink skipped")
        continue
    t = t[:at] + '<div class="writeup">\n  ' + BACKLINK + "\n</div>\n\n" + t[at:]
    if apply_:
        open(p, "w", encoding="utf-8").write(t)
    linked.append(p)
if linked:
    notes.append("backlinks added on: " + ", ".join(os.path.basename(x) for x in linked))

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"wired {URL} | card + {len(SLIDES)} captions | no 301 (nothing replaced)")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print("  ·", n)
