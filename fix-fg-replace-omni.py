#!/usr/bin/env python3
"""fix-fg-replace-omni.py — remove Omni Barton Creek from the Field Guide and put Forest Creek in its card slot.
12 October 2026. Lenny: "remove the OMNI, and replace with a different course like Grey Rock or Star Ranch".
Grey Rock and Star Ranch already have full cards, so Forest Creek (public, city-owned, KemperSports-run) is promoted
from the short list into the empty slot; its short-list entry is removed so it is not listed twice.
Why Omni goes: Omni's own rates page says golf is for Barton Creek members and registered resort guests only.
FACTS for the Forest Creek card: forestcreek.com (home, rates, FAQ) read 12 Oct 2026 — 99 Twin Ridge Parkway, Round Rock
TX 78664, 512-388-2874, tee sheet opens 30 days out, dynamic pricing, walking permitted; Dick Phelps 1990, owned by the City
of Round Rock, 7,147 yards from the Gold tees, 139 slope (as already printed in the guide's short list).
PHOTO: Forest Creek's own aerial (research/field-guide-src/forest-creek-aerial.webp). Idempotent. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "field-guide/index.html"

CARD = """  <div class="special-course">
    <img class="special-course-img" src="/images/field-guide/forest-creek.jpg" alt="Aerial view of Forest Creek Golf Club in Round Rock, fairways and a pond among oak woodland at golden hour" loading="lazy" />
    <div>
      <div class="special-course-name">Forest Creek Golf Club.</div>
      <div class="special-course-meta">Public &middot; Round Rock &middot; under 30 min north</div>
      <div class="special-course-body">The hardest public test near Austin, and a muni in all but management. Dick Phelps designed it in 1990; the City of Round Rock owns it and KemperSports runs it. From the Gold tees it plays 7,147 yards with a 139 slope, longer and harder than anything else in this guide, munis included. There is no rate card: pricing moves with demand and the tee sheet opens 30 days out, so booking early genuinely costs less, from about $40 on a twilight weekday to around $100 on a weekend morning. Walking is allowed. Bring every club and a few extra balls.</div>
      <div class="special-course-stats">
        <div class="special-course-stat"><span class="label">Designer</span><span class="value">Dick Phelps &middot; 1990</span></div>
        <div class="special-course-stat"><span class="label">Yards / slope</span><span class="value">7,147 &middot; 139</span></div>
        <div class="special-course-stat"><span class="label">Walking</span><span class="value">Allowed</span></div>
        <div class="special-course-stat"><span class="label">Best for</span><span class="value">A real test at public prices</span></div>
      </div>
      <a href="https://forestcreek.com/?utm_source=thegrassyissue&amp;utm_medium=referral&amp;utm_campaign=field-guide&amp;utm_content=field-guide" target="_blank" rel="noopener" class="special-course-link">Book a tee time &#8599;</a>
    </div>
  </div>
"""

SCHEMA = """   "item": {
    "@type": "GolfCourse",
    "name": "Forest Creek Golf Club",
    "url": "https://forestcreek.com/",
    "subjectOf": {
     "@type": "WebPage",
     "url": "https://thegrassyissue.com/field-guide/#special-day"
    },
    "address": {
     "@type": "PostalAddress",
     "streetAddress": "99 Twin Ridge Parkway",
     "addressLocality": "Round Rock",
     "addressRegion": "TX",
     "postalCode": "78664",
     "addressCountry": "US"
    },
    "telephone": "+1-512-388-2874",
    "publicAccess": true
   }"""

RESORT_OLD = [
 "For the full resort experience, Omni Barton Creek has four championship courses by Fazio, Crenshaw, and Palmer.",
 "For the full resort experience, Omni Barton Creek has four Tom Fazio, Crenshaw, and Palmer courses at one property.",
]
RESORT_NEW = "For the full resort experience, Lost Pines Resort at the Hyatt Regency has an Arthur Hills course that finishes in a river valley."

def main(apply_):
    t = F.read_text(encoding="utf-8"); o = t
    # 1. card swap
    m = re.search(r'  <div class="special-course">\s*<img class="special-course-img" src="/images/field-guide/omni-barton\.jpg".*?\n  </div>\n', t, re.S)
    if m:
        t = t[:m.start()] + CARD + t[m.end():]
    # 2. drop Forest Creek from the short list (now a full card)
    if 'src="/images/field-guide/forest-creek.jpg"' in t:
        t = re.sub(r'  <div class="hon-item">\s*<div>\s*<div class="hon-name">Forest Creek Golf Club\.</div>.*?</p>\s*</div>\s*</div>\n', '', t, count=1, flags=re.S)
    # 3. schema
    t = re.sub(r'   "item": \{\s*"@type": "GolfCourse",\s*"name": "Omni Barton Creek Resort & Spa Golf".*?"publicAccess": false\s*\}', SCHEMA, t, count=1, flags=re.S)
    # 4. FAQ / answer copy
    for s in RESORT_OLD:
        t = t.replace(s, RESORT_NEW)
    # 5. quick reference
    t = t.replace('<li><span>Full resort experience</span><span class="ref">Omni Barton Creek</span></li>',
                  '<li><span>Full resort experience</span><span class="ref">Lost Pines Resort</span></li>')
    left = [x for x in re.findall(r'.{0,60}Omni.{0,60}', re.sub(r"<!--.*?-->", "", t)) ]
    print(f"  field-guide: {'changed' if t != o else 'unchanged'}; Omni mentions left: {len(left)}")
    for x in left: print("   ", x)
    if apply_ and t != o:
        F.write_text(t, encoding="utf-8"); print("  wrote field-guide/index.html")

if __name__ == "__main__":
    main("--apply" in sys.argv)
