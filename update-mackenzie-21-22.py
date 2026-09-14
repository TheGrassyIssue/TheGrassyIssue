#!/usr/bin/env python3
"""Bring /drops/fyfe-x-mackenzie-every-edition up to date: editions 21 & 22.

WHY: the page shipped claiming 20 editions and teasing a "21st Edition · July
2026" that has since landed. Editions 21 and 22 — the Coastal Tones pair — were
published 2026-08-11 and both sold out. wire-fyfe.py already flipped the header
count to 22; this adds the actual section so the count and the content agree.

Three other corrections while in here, all sourced from the live collection JSON
and the Shooters Club lookbook, captured 2026-09-14:
  - the 19th Edition card says "The only edition still in stock". Its variant now
    reads available:false. Both Between Tides bags are gone.
  - the 17th Edition card says the Shooters Club was "Shot at Dalmore". It was
    shot at GLEN AFFRIC; "Dalmore" is Fyfe's dark-brown leather SKU name, which
    appears in the image filenames as a product label, not a location.
  - the What's Next card is stale. Replaced with the standing state of play.

Idempotent: re-running detects the Coastal Tones marker and skips the insert.
"""
import re, sys, os

P = "drops/fyfe-x-mackenzie-every-edition.html"
MARK = "<!-- Coastal Tones — Editions 21 & 22 (2026) -->"
BTK = "/drops/brand-to-know-fyfe-golf"

COASTAL = '''  ''' + MARK + '''
  <div class="products-section">
    <h2 class="products-hdr">Coastal Tones &mdash; Editions 21 &amp; 22 (2026)</h2>
    <div class="products-grid">

      <a href="https://www.fyfegolf.com/products/mackenzie-golf-bag-x-fyfe-2" target="_blank" rel="noopener" class="product-card">
        <div class="product-img">
          <img src="/images/fyfe-mackenzie/21st.jpg" alt="21st Edition &mdash; Coastal Tones Sage" loading="lazy" />
        </div>
        <div class="product-body">
          <div class="product-brand">21st Edition</div>
          <div class="product-name">Coastal Tones &middot; Sage &middot; Sold Out</div>
          <div class="product-desc">Sage waxed canvas with black, dark green and white leather accents, and a limited-edition patch moved inside the bag rather than stitched above the pocket. Split base, white above dark green. Published 11 August 2026 and gone.</div>
          <span class="product-link">View &nearr;</span>
        </div>
      </a>

      <a href="https://www.fyfegolf.com/products/mackenzie-golf-bag-x-fyfe-1" target="_blank" rel="noopener" class="product-card">
        <div class="product-img">
          <img src="/images/fyfe-mackenzie/22nd.jpg" alt="22nd Edition &mdash; Coastal Tones Charcoal" loading="lazy" />
        </div>
        <div class="product-body">
          <div class="product-brand">22nd Edition</div>
          <div class="product-name">Coastal Tones &middot; Charcoal &middot; Sold Out</div>
          <div class="product-desc">Charcoal waxed canvas with black, agave and white leather. The same internal limited-edition patch as the 21st, and a split base in white over black. Released the same day as its sage counterpart, in the run of paired drops the series has kept to since the 8th.</div>
          <span class="product-link">View &nearr;</span>
        </div>
      </a>

      <a href="https://www.fyfegolf.com/collections/mackenzie-golf-bags" target="_blank" rel="noopener" class="product-card">
        <div class="product-img">
          <img src="/images/fyfe-mackenzie/coastal-duo.jpg" alt="Editions 21 and 22 photographed together at Elie" loading="lazy" />
        </div>
        <div class="product-body">
          <div class="product-brand">Editions 21 &amp; 22</div>
          <div class="product-name">Coastal Tones &middot; The Pair</div>
          <div class="product-desc">Shot together at Elie on the Fife coast, a few miles from the workshop that makes the covers. Coastal Tones is the quietest palette the collaboration has run &mdash; sage and charcoal against white, where Between Tides went to raw canvas and heaven blue.</div>
          <span class="product-link">Collection &nearr;</span>
        </div>
      </a>

    </div>
  </div>

'''

NEXT_OLD_DESC = ("The next chapter. Fyfe&rsquo;s site confirms a new MacKenzie collaboration "
                 "landing July 2026. Sign up for early access on their collection page. If "
                 "history is any guide, it won&rsquo;t last long.")
NEXT_NEW = (f'''<div class="product-desc">Twenty-two editions in, the pattern is fixed: two bags at a time, &pound;650 each, Halley Stevensons canvas from Dundee stitched by MacKenzie in Oregon, and sold out before most people hear about them. Coastal Tones landed 11 August 2026. Watch the collection page, or read our full profile of <a href="{BTK}">the workshop behind them</a>.</div>''')

apply_ = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
before = h
notes = []

if MARK in h:
    notes.append("Coastal Tones section already present — skipped")
else:
    anchor = "  <!-- Between Tides — Editions 19 & 20 (2026) -->"
    if anchor not in h:
        raise SystemExit("could not find the Between Tides section anchor")
    h = h.replace(anchor, COASTAL + anchor, 1)
    notes.append("inserted Coastal Tones (editions 21 & 22) above Between Tides")

# 19th is no longer in stock
old19 = "Split base in cream and tan. The only edition still in stock."
if old19 in h:
    h = h.replace(old19, "Split base in cream and tan. Sold out.", 1)
    h = h.replace("<div class=\"product-name\">Between Tides &middot; Raw Canvas &middot; &pound;650</div>",
                  "<div class=\"product-name\">Between Tides &middot; Raw Canvas &middot; Sold Out</div>", 1)
    notes.append("19th Edition: 'only edition still in stock' -> sold out")

# the Shooters Club was shot at Glen Affric, not Dalmore
if "Shot at Dalmore with a gundog." in h:
    h = h.replace("Shot at Dalmore with a gundog.",
                  "Shot at Glen Affric with a gundog.", 1)
    notes.append("17th Edition: shoot location corrected Dalmore -> Glen Affric")

# refresh the stale What's Next card
if NEXT_OLD_DESC in h:
    h = h.replace(f'<div class="product-desc">{NEXT_OLD_DESC}</div>', NEXT_NEW, 1)
    h = h.replace('<div class="product-name">21st Edition &middot; July 2026</div>',
                  '<div class="product-name">Editions 23 &amp; 24 &middot; Unannounced</div>', 1)
    h = h.replace('alt="21st Edition — Coming July 2026"',
                  'alt="The Fyfe x MacKenzie collaboration, twenty-two editions in"', 1)
    h = h.replace('<div class="product-brand">Next Drop</div>',
                  '<div class="product-brand">What Happens Next</div>', 1)
    notes.append("What's Next card refreshed")

# header count sanity — wire-fyfe.py should already have done this
if "<span>20 Editions</span>" in h:
    h = h.replace("<span>20 Editions</span>", "<span>22 Editions</span>")
    notes.append("header count 20 -> 22")

for s in ("21st", "22nd", "coastal-duo"):
    if not os.path.exists(f"images/fyfe-mackenzie/{s}.jpg"):
        raise SystemExit(f"missing image: images/fyfe-mackenzie/{s}.jpg")
if re.search(r'\bworth\b', re.sub(r'<[^>]+>', ' ', h[h.find("<body"):]), re.I):
    raise SystemExit("banned word 'worth' present in body")

if apply_:
    open(P, "w", encoding="utf-8").write(h)
    print(f"wrote {P} ({len(h)-len(before):+d} bytes)")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print("  ·", n)
