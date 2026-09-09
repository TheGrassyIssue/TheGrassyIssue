#!/usr/bin/env python3
"""Wire the Manors AW26 drop: homepage card, slideTexts, brand mentions, sitemap.

Card markup is copied verbatim from the Gamut card contract, INCLUDING the
inline onclick on both gear arrows. Three cards shipped 2026-09-08 without it
and their carousels were silently dead — see reference_gear_arrow_handlers.

slideTexts are injected into the page via el.textContent, so the strings here
must contain RAW characters (&, ', ") and NOT HTML entities, or the card
renders a literal "&amp;".
"""
import re, json, os

SLUG = "manors-golf-aw26-collection"
KEY = "manorsaw26"
TITLE = "Manors&rsquo; Honourable Company AW26 &mdash; Dressed for the Sub-Four-Hour Round"
IMG = "/images/manors-aw26/"

SLIDES = [
 ("merino-tech-hoodie",   "Merino Tech Hoodie",          "Dune &middot; $305",
  "Manors' AW26 Honourable Company collection runs on merino, Primaloft and Cordura ripstop. The Merino Tech Hoodie sits at the top of it at $305 — wool regulates across a wider temperature band than fleece, which is the whole argument for autumn golf."),
 ("crosswind-cordura-vneck","Crosswind Cordura® V-Neck",  "Black &middot; $265",
  "High-tenacity Cordura ripstop, a fabric originally developed for military use, with a PFC-free water-repellent finish and side vent zips. Manors' own copy signs off the spec sheet with the line that explains the brand: \"You will also look very good in a warm pub.\""),
 ("heritage-primaloft-cardigan","Heritage Primaloft® Cardigan","Burgundy &middot; $217",
  "A buttoned cardigan insulated with Primaloft, in burgundy and ivory. The silhouette is deliberately old-fashioned; the synthetic fill is the concession to actually playing in it, since it keeps insulating when a wool cardigan would give up."),
 ("ripstop-tech-vest",    "Ripstop Tech Vest",           "Dune &middot; $217",
  "Recycled ripstop with a water-resistant finish. The gilet solves the real autumn problem — a cold core and arms that still need to swing — and it is the piece here most likely to live in a bag year-round."),
 ("tour-shirt",           "Tour Shirt",                  "Powder &middot; $163",
  "A short-sleeved wind top at 148gsm, cut from four-way stretch and modelled on vintage wind proofs. Bonded YKK zip, adjustable hem with cord and toggle. Short sleeves on a wind layer reads odd until the first genuinely blustery warm day."),
]

CARD = f'''      <div class="card" data-type="drops">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
''' + "".join(
f'''          <div class="gear-slide">
            <a href="/drops/{SLUG}">
              <img src="{IMG}{s}.jpg" alt="Manors {re.sub(r'&[a-z]+;|®','',nm).strip()}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{nm}</div><div class="gear-slide-name">{sub}</div></div>
            </a>
          </div>
''' for s, nm, sub, _ in SLIDES) + f'''        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="/drops/{SLUG}" class="card-link">Read the collection ↗</a>
    </div>
  </div>
'''

h = open("index.html", encoding="utf-8").read()
if f'data-carousel="{KEY}"' in h:
    raise SystemExit("card already present — nothing to do")

# insert as the newest card: immediately before the first existing .card in the feed
m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

# slideTexts — RAW characters, never entities
block = "window.__slideTexts[\"%s\"] = [\n%s\n];" % (
    KEY, ",\n".join("  " + json.dumps(t) for _, _, _, t in SLIDES))
anchor = h.find("window.__slideTexts[")
if anchor == -1:
    raise SystemExit("no window.__slideTexts map found")
h = h[:anchor] + block + "\n" + h[anchor:]
open("index.html", "w", encoding="utf-8").write(h)
print(f"card inserted ({len(SLIDES)} slides) + slideTexts registered")

# --- brand mentions: no entry = no /brands coverage page ---
# TWO traps here, both hit on the first run 2026-09-08:
#   1. The index slug is "manors", NOT "manors-golf". Writing the wrong key
#      created a second, orphaned bucket with 1 entry while the real one sat
#      at 30 — and nothing errored.
#   2. The entry schema is {url, title, profile}, NOT {slug, title, date}.
#      All 30 existing entries use the former. Assert before writing.
MP = "data/brand-mentions.json"
mm = json.load(open(MP))
URL = f"/drops/{SLUG}"
ent = {"url": URL, "title": "Manors' Honourable Company AW26", "profile": False}
lst = mm.setdefault("manors", [])
if not any(e.get("url") == URL for e in lst):
    lst.insert(0, ent)
    bad = [e for e in lst if set(e) != {"url", "title", "profile"}]
    if bad:
        raise SystemExit(f"brand-mentions schema drift, refusing to write: {bad[:2]}")
    json.dump(mm, open(MP, "w"), indent=1, ensure_ascii=False)
    print(f"brand-mentions: manors now {len(lst)} entries")
else:
    print("brand-mentions: already listed")

# --- sitemap ---
SM = "sitemap.xml"
sm = open(SM, encoding="utf-8").read()
url = f"https://thegrassyissue.com/drops/{SLUG}"
if url not in sm:
    node = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-09-08</lastmod>\n  </url>\n"
    sm = sm.replace("</urlset>", node + "</urlset>")
    open(SM, "w", encoding="utf-8").write(sm)
    print("sitemap: added")
else:
    print("sitemap: already present")
