#!/usr/bin/env python3
"""Re-wire the refreshed Divot Tool Edit card and move it to the top of the feed.

Replaces the June 2026 legacy card, which had three problems:
  1. `card-tag ink` — off-palette. House chip colour is GREEN (grass).
  2. Legacy carousel markup (`gear-dots`/`gear-counter` with data-dots/
     data-counter) and a static `card-text` with no data-slidetext, so the
     caption never tracked the image.
  3. Copy naming products that are now dead links or sold out.

slideTexts go in the CANONICAL `window._slideTexts = {` object literal — NOT a
per-card registration block. Registration blocks write `window.__slideTexts`
(two underscores) which goTo() never reads, and a wholesale assignment later in
the file overwrites anything added to the one-underscore map at runtime.
See reference_gear_arrow_handlers.

Both gear arrows carry the inline onclick. Without it the carousel is silently
dead — no error, nothing in the console.
"""
import re, json

SLUG = "7-divot-tools-actually-worth-carrying"
KEY = "divottools"
TITLE = "The Divot Tool Edit &mdash; Machined, Forged and Milled, From $20 to $130"
IMG = "/images/divot-tools/"

SLIDES = [
 ("kraken-0", "Kraken Golf", "Gimme Green Crayon &middot; $79",
  "Twenty-five green repair tools from sixteen makers, from a $19.99 Frogger to a $130 Sugarloaf collab. Kraken's Crayon is CNC-milled into the exact silhouette of a Crayola, down to the wrapper ridges — and it runs in twenty colourways."),
 ("seamus", "Seamus Golf", "Greenskeeper Pitch Tool &middot; $76",
  "Single prong, forged steel, hammer-finished in Portland so no two faces match. The single-prong shape is the point: one prong pushes turf inward from the edge of the mark, which is the repair a two-prong fork encourages you to get wrong."),
 ("sentinel", "Sentinel Golf", "Jimmy Bar &mdash; Titanium &middot; $68",
  "A bar rather than a fork. Machined titanium, shaped to be pushed in at an angle and levered rather than pronged and twisted — which is the method most superintendents actually ask for."),
 ("kraken-9", "Kraken Golf", "The Tentacle &mdash; Copper &middot; $99",
  "Solid copper, cast as a curled tentacle with raised suckers along the underside that double as grip. Copper darkens with handling, so it looks like a different object in a year."),
 ("edel", "Edel Golf", "Fine Milled Repair Tool &middot; $45",
  "Milled rather than stamped, which is the meaningful line in this category — a milled tool starts as solid billet and holds an edge on the prongs instead of rolling over at the tip."),
]

_ENT = re.compile(r'&[a-z]+;|&#\d+;')
def _alt(b, n):
    """Plain-text alt: strip entities, collapse whitespace."""
    return re.sub(r'\s+', ' ', _ENT.sub('', f"{b} {n}")).strip()

CARD = f'''      <div class="card" data-type="drops">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
''' + "".join(
f'''          <div class="gear-slide">
            <a href="/drops/{SLUG}">
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
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="/drops/{SLUG}" class="card-link">See all 25 ↗</a>
    </div>
  </div>
'''

h = open("index.html", encoding="utf-8").read()

# --- 1. excise the old card by brace-matching from its opening <div class="card" ---
i = h.find(f"/drops/{SLUG}")
if i == -1:
    raise SystemExit("no existing divot card found")
s = h.rfind('<div class="card"', 0, i)
depth = 0; j = s; end = None
while j < len(h):
    m = re.compile(r'<div\b|</div>').search(h, j)
    if not m: break
    if m.group(0).startswith("<div"): depth += 1
    else:
        depth -= 1
        if depth == 0: end = m.end(); break
    j = m.end()
if end is None:
    raise SystemExit("could not brace-match the old card")
old = h[s:end]
if f"/drops/{SLUG}" not in old:
    raise SystemExit("brace-match captured the wrong card — refusing to write")
h = h[:s] + h[end:]
print(f"removed legacy card ({len(old)} chars)")

# --- 2. insert the new card as the first card in the feed ---
m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

# --- 3. slideTexts into the CANONICAL map ---
anchor = "  window._slideTexts = {\n"
k = h.find(anchor)
if k == -1:
    raise SystemExit("canonical window._slideTexts map not found")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)   # drop any stale entry
k = h.find(anchor)
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(re.sub(r'&mdash;', '—', re.sub(r'&middot;', '·', t)), ensure_ascii=False)
    for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

open("index.html", "w", encoding="utf-8").write(h)
print(f"inserted refreshed card at top of feed + {len(SLIDES)} slide captions")

# --- 4. sitemap lastmod ---
sm = open("sitemap.xml", encoding="utf-8").read()
url = f"https://thegrassyissue.com/drops/{SLUG}"
if url in sm:
    sm = re.sub(r'(<loc>' + re.escape(url) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                lambda m: m.group(1) + "2026-09-09" + m.group(2), sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("sitemap lastmod -> 2026-09-09")
else:
    print("!! slug not in sitemap")
