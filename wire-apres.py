#!/usr/bin/env python3
"""Wire the Après Golf Brand to Know: homepage card, brand index, sitemap.

TRAPS THIS SCRIPT GUARDS AGAINST — all three have bitten before:

1. GEAR ARROWS NEED THE INLINE onclick.
   Homepage feed carousels are driven by onclick="gearSlide(this, ±1)", not by
   a delegated listener. A hand-wired card without it is silently dead: no
   console error, and the arrows are opacity:0 until hover, so it looks fine.

2. slideTexts GO IN THE CANONICAL `window._slideTexts = {` OBJECT LITERAL.
   goTo() reads window._slideTexts (ONE underscore). Per-card registration
   blocks write window.__slideTexts (TWO), which nothing reads, and a wholesale
   `window._slideTexts = {...}` assignment far down index.html runs afterwards
   and wipes anything added at runtime. Splicing into that literal is the only
   thing that survives.

3. brand-mentions.json IS KEYED BY BRAND SLUG WITH SCHEMA {url,title,profile}.
   Not {slug,title,date}. Guessing the schema silently corrupts the coverage
   page. This script asserts on drift before writing.

Idempotent: re-running replaces the card and the caption entry rather than
stacking duplicates.
"""
import re, json, sys, os

SLUG  = "brand-to-know-apres-golf"
URL   = f"/drops/{SLUG}"
KEY   = "apresgolf"
BRAND = "apres-golf"
TITLE = "Brand to Know: Apr&egrave;s Golf &mdash; Ski Patches, Tie-Dye Fleece and a Rack of Dancing Bears"
PLAIN = "Brand to Know: Après Golf — Ski Patches, Tie-Dye Fleece and a Rack of Dancing Bears"
IMG   = "/images/apres-golf/"
TODAY = "2026-09-09"

SLIDES = [
 ("fruit-looper", "Apr&egrave;s Golf", "The Fruit Looper&trade; &middot; $88",
  "Forty-five pieces from an Ohio-of-the-fleece-world outlier: Après sews vintage ski-resort and country-club patches onto hi-loft sherpa headcovers, hand-sewn in California. The Fruit Looper is the print the brand is built around, and it behaves like real dye rather than a repeat pattern."),
 ("steal-clubface", "Apr&egrave;s Golf", "Steal Your Clubface Patch &middot; $88",
  "The lightning-bolt skull in red, white and blue on a cream cover, under a name that puns the artwork into golf. It anchors a rack of eight bear-and-bolt pieces running from $88 to $128."),
 ("chamonix", "Apr&egrave;s Golf", "Chamonix Vintage Patch &middot; $108",
  "Where the name stops being a pun. Genuine resort patches — Chamonix, St. Moritz, Alta, Mad River Glen — cut into golf headcovers, and each one exists in whatever quantity Après managed to buy."),
 ("sweater-payne", "Apr&egrave;s Golf", "Sunday Sweater: The Payne &middot; $98",
  "A navy 1980s intarsia sweater with a full golf scene knitted across the chest. Après buys these secondhand and resells them one at a time, which makes the rail a different shop every week."),
 ("send-your-patch", "Apr&egrave;s Golf", "Send Us Your Patch! Custom &middot; $118",
  "You mail them a patch and they build a headcover around it. This is the service the rest of the catalogue is a showroom for, and it is why the vintage rack never settles."),
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
      <a href="{URL}" class="card-link">See all 50 ↗</a>
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
        print("removed existing Après card")

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
                          re.sub(r'&trade;', '™', t)))), ensure_ascii=False)
    for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]

# ------------------------------------------------------------- 2. brand index
brands = json.load(open("data/brands.json"))
ENTRY = {
 "slug": BRAND,
 "name": "Après Golf",
 "loc": "California",
 "regions": ["usa"],
 "cats": ["headcovers", "accessories", "apparel"],
 "line": "Hi-loft sherpa fleece headcovers hand-sewn in California, with vintage ski-resort and country-club patches sewn on top.",
 "url": URL,
 "img": f"{IMG}fruit-looper.jpg",
 "tags": ["loud-on-purpose", "made-by-hand", "design-nerd"],
 "added": TODAY,
 "attrs": ["new-to-index"],
}
# Schema guard: every key we write must already exist SOMEWHERE in the file.
# Comparing against brands[0] alone was wrong — the first entry (3-putt-round)
# carries no "img", which is optional and present on ~half the roster, so the
# guard rejected a perfectly valid entry. Union across all entries is the right
# reference; required keys are checked separately.
known = set().union(*(set(b) for b in brands))
drift = set(ENTRY) - known
if drift:
    raise SystemExit(f"brands.json schema drift, refusing to write: {drift}")
required = {"slug", "name", "loc", "regions", "cats", "line", "url", "tags", "added"}
missing = required - set(ENTRY)
if missing:
    raise SystemExit(f"brands.json entry missing required keys: {missing}")
brands = [b for b in brands if b["slug"] != BRAND]
brands.append(ENTRY)
brands.sort(key=lambda b: b["slug"])

# ---------------------------------------------------------- 3. brand mentions
mm = json.load(open("data/brand-mentions.json"))
ent = {"url": URL, "title": PLAIN, "profile": True}
lst = mm.setdefault(BRAND, [])
lst = [e for e in lst if e.get("url") != URL]
lst.insert(0, ent)
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
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"card inserted at top of feed + {len(SLIDES)} captions in the canonical map")
    print(f"brands.json: {len(brands)} entries (Après added)")
    print(f"brand-mentions.json: {BRAND} -> {len(mm[BRAND])} entry/entries")
    print(sitemap_note)
else:
    print("DRY RUN — pass --apply")
    print(f"  would insert card ({len(CARD)} chars) + {len(SLIDES)} captions")
    print(f"  would add brands.json entry {BRAND}")
    print(f"  would add brand-mentions {BRAND} ({len(mm[BRAND])} total)")
    print(f"  {sitemap_note}")
