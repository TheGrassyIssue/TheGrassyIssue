#!/usr/bin/env python3
"""
wire-takomo-card.py — swap the old Takomo feed card for a [Brand Revisited] card.

Playbook step 7: remove the old feed card, insert a Brand Revisited card at the
top of the feed pointing at the EXISTING ranking URL (/drops/brand-to-know-takomo-golf),
not a new page. 10 of the 11 existing Revisited cards do exactly this; only Jones
has a separate page, and that is the outlier.

The old Takomo card used the legacy id="dots-x"/id="counter-x" markup. This one is
built on the current data-carousel / data-slidetext / data-dots / data-counter
pattern that the recent cards use.

Idempotent via data-carousel="takomorevisit". Dry-run default; --apply writes.
"""
import re, sys

KEY = "takomorevisit"
SLIDES = [
 ("skyforger-002-wedges", "sf002", "Skyforger 002 &middot; $99",
  "Takomo Skyforger 002 full-face wedge played from a fairway lie"),
 ("ignis-d2-fairway-wood", "ignis-d2", "Ignis D2 Fairway Wood &middot; $269",
  "Takomo Ignis D2 fairway wood behind a golf ball on close-mown turf"),
 ("stand-bag-02", "standbag02", "Stand Bag 02 &middot; $279",
  "Takomo Stand Bag 02 in off-white laid on fairway grass beside clubs and golf balls"),
 ("iron-301-mb", "iron301mb", "Iron 301 MB &middot; $649",
  "Takomo Iron 301 MB forged muscle back iron"),
 ("ignis-d1-driver", "ignis-d1", "Ignis D1 Driver &middot; $319 &middot; sold out",
  "A golfer walking with the Takomo Ignis D1 driver over one shoulder"),
]

TITLE = "Brand Revisited &mdash; Takomo Went Past Irons"
TEXT  = ("The Finnish direct-to-consumer brand built its name on forged irons at half the going rate. "
         "The catalog now runs to full-face wedges, a fairway wood, a stand bag and a driver, and the "
         "Skyforger has gone from $89 to $99 since we first wrote it up.")
SOURCE = "Takomo Golf &middot; Turku, Finland &middot; since 2021 &middot; $99 to $679"
HREF = "/drops/brand-to-know-takomo-golf"

def slide(handle, img, name, alt):
    return f'''          <div class="gear-slide">
            <a href="https://takomogolf.com/products/{handle}" target="_blank" rel="noopener">
              <img src="/images/takomo-golf/{img}.jpg" alt="{alt}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">Takomo Golf</div><div class="gear-slide-name">{name}</div></div>
            </a>
          </div>'''

CARD = f'''<div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{chr(10).join(slide(*s) for s in SLIDES)}
        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{HREF}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{TEXT}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <div class="card-source">{SOURCE}</div>
      <a href="{HREF}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>
    </div>
  </div>'''

def span(h, start):
    d=0; j=start
    while True:
        t=re.compile(r'<div\b|</div>').search(h,j)
        if not t: return None
        d += 1 if t.group(0)=='<div' else -1; j=t.end()
        if d==0: return j

APPLY = "--apply" in sys.argv
p="index.html"; h=open(p,encoding="utf-8").read(); orig=h
if f'data-carousel="{KEY}"' in h:
    print("already applied"); sys.exit(0)

opens=[m.start() for m in re.finditer(r'<div class="card"[^>]*data-type=', h)]

# 1) remove the OLD Takomo card (legacy markup, data-carousel="takomogolf")
m = re.search(r'data-carousel="takomogolf"', h)
removed = 0
if m:
    st = max(o for o in opens if o < m.start()); en = span(h, st)
    pos = sum(1 for o in opens if o < st)
    h = h[:st] + h[en:].lstrip('\n')
    removed = 1
    print(f"removed old Takomo card (was feed position {pos})")
else:
    print("no old Takomo card found")

# 2) insert the new card at the top of the feed
opens=[mm.start() for mm in re.finditer(r'<div class="card"[^>]*data-type=', h)]
h = h[:opens[0]] + CARD + "\n\n  " + h[opens[0]:]

if APPLY and h != orig:
    open(p,"w",encoding="utf-8").write(h)
print(f"inserted [Brand Revisited] card at feed position 0 | slides: {len(SLIDES)} | removed old: {removed}")
print("applied" if APPLY else "DRY RUN — pass --apply")
