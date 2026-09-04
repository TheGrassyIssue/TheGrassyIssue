#!/usr/bin/env python3
"""
takomo-lookbook.py — add the editorial section + IRL lookbook the first pass missed.

Lenny, 2026-09-04: "Did we include a solid write up and also IRL pics?" Answer was
no on both — the refresh added product cards and FAQs but zero new prose, and the
imagery skewed packshot. This fixes that.

All 6 lookbook frames are TRUE IRL (a person visibly playing/walking), verified by
rendering each image, not by trusting alt text — most Takomo product-page alt text
is just the product name. Captions describe only what was confirmed in frame; no
one is named, because the site does not identify these players.

Facts in the prose are from National Club Golfer (Jun 2026) + Takomo product pages.
No invented quotes.

Idempotent via the marker. Dry-run default; --apply writes.
"""
import re, sys

MARK = "<!--TGI-TAKOMO-LOOKBOOK-V1-->"
P = "drops/brand-to-know-takomo-golf.html"

CSS = """/*TGI-IGGRID-V1*/
.ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 8px}
.ig-grid figure{margin:0}
.ig-grid .ig-ph{aspect-ratio:1/1;overflow:hidden;border:.5px solid var(--ink);background:#e8e5dc}
.ig-grid .ig-ph img{width:100%;height:100%;object-fit:cover}
.ig-grid figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.5;margin-top:8px;line-height:1.5}
@media(max-width:760px){.ig-grid{grid-template-columns:1fr 1fr;gap:10px}}
"""

SHOTS = [
 ("irl-swing",   "At the top of the backswing",       "A golfer at the top of the backswing, shot from below against open sky"),
 ("irl-carry",   "Walking with the Stand Bag 02",     "A golfer in a cap and hooded top walking a fairway with the black Stand Bag 02 on one shoulder"),
 ("irl-green",   "On the green with the SF002",       "A bearded golfer in a navy jacket standing on a green holding the Skyforger 002 wedge, flagstick behind"),
 ("irl-iron",    "Sizing up the 101 MKII","A golfer in a cap and dark polo holding a Takomo 101 MKII iron, open course behind"),
 ("irl-close",   "A Takomo cap and a 6-iron",               "A golfer in a Takomo cap and white outerwear holding an iron across frame, green course behind"),
 ("irl-address", "Addressing it on the fairway",      "A golfer addressing a ball on the fairway with a Takomo iron, tree line behind"),
]

PROSE = '''<h2 class="products-hdr">Past the Irons</h2>
<div class="writeup" style="grid-template-columns:1fr;">
  <div class="writeup-body" style="max-width:760px">
    <p>Takomo spent its first years as an irons company. The 101, the 201 and the 301 covered game improvement through to blades, all forged, all sold direct out of Turku at prices that undercut the houses making comparable heads. That remains the centre of the business.</p>

    <p>The catalog around those irons has filled in since. Wedges arrived in the Skyforger, developed with George and Wesley Bryan, and the SF002 added a full-face version at $99. A hollow-body utility iron followed at $119. The Ignis D1 driver marked what National Club Golfer described as the company&rsquo;s first major move into metalwoods, and the Ignis D2 fairway wood arrived for 2026 in 3, 5 and 7. With the Stand Bag 02 at $279, a golfer can now assemble most of a bag without leaving the site.</p>

    <p>Growth has run through YouTube rather than tour bags. Grant Horvat, who has more than a million and a half subscribers, took an ownership stake and plays the irons and wedges on camera. That reaches a different golfer than a rack in a pro shop reaches, and it explains how a five-year-old company from a city of two hundred thousand people ended up in this many bags.</p>
  </div>
</div>
'''

def fig(img, cap, alt):
    return f'''      <figure>
        <div class="ig-ph"><img src="/images/takomo-golf/{img}.jpg" alt="{alt}" loading="lazy" /></div>
        <figcaption>{cap}</figcaption>
      </figure>'''

LOOKBOOK = f'''<section class="products">
  <h2 class="products-hdr">On Course</h2>
  <div class="ig-grid">
{chr(10).join(fig(*s) for s in SHOTS)}
  </div>
</section>
'''

APPLY = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
if MARK in h:
    print("already applied"); sys.exit(0)

k = h.rfind("</style>")
h = h[:k] + CSS + h[k:]

anchor = h.find('<section class="products">')
h = h[:anchor] + MARK + "\n" + PROSE + "\n" + LOOKBOOK + "\n" + h[anchor:]

if APPLY:
    open(P, "w", encoding="utf-8").write(h)
words = len(re.sub(r'<[^>]+>', ' ', PROSE).split())
print(f"prose added: {words} words in 3 paragraphs | lookbook: {len(SHOTS)} IRL frames | ig-grid CSS injected")
print("applied" if APPLY else "DRY RUN — pass --apply")
