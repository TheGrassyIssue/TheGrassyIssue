#!/usr/bin/env python3
"""build-practice-facilities.py — full rewrite of /drops/8-best-practice-facilities-around-austin.
28 September 2026. Lenny: "this post needs a full update", then "let's update the post and images".
Went to ten spots (my recommendation); URL kept for its ranking, datePublished kept.

Every fact and price re-read on first-party pages on 28 Sep 2026: research/practice-2026/notes.md.
Corrections vs the June page: Harvey Penick is First Tee-owned (not city-owned) and has mats;
Lions is 18 holes with an irons-only range (moved to a mention); Topgolf is near, not in, the Domain;
Dripping Springs CC is a standalone range; every price updated. Photos are the facilities' own
(research/practice-2026/img/log.json); two carried over from the June page.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "8-best-practice-facilities-around-austin"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/practice-2026"
FR = json.loads((ROOT / "research/practice-2026/frames.json").read_text())

TITLE = "Best Practice Facilities in Austin: 10 Driving Ranges and Short-Game Spots"
DESC = ("The best driving ranges and practice facilities in Austin, re-checked for 2026: lit all-grass ranges, "
        "$7 muni buckets, Toptracer bays and short-game courses, with current prices and hours.")
H1 = "Best Practice Facilities in Austin: 10 Ranges and Short-Game Spots"

# key -> (name, where, price line, url, copy, address)
F = {
 "drr": ("The Driving Range", "Round Rock &middot; standalone, lit", "Buckets $10&ndash;$19.75", "https://drivingrangerr.com/",
   "This is the only true practice complex in the metro: 35 acres with no course attached. The long range has a 75,000-square-foot all-grass tee and targets from 40 to 300 yards, the wedge range has its own grass tee, and there is a chipping green with a bunker and a free putting green. The whole site is lit, and it is open until 10:30pm every night. Add $2 a basket on weekends and after 5pm.",
   "3533 Greenlawn Blvd, Round Rock"),
 "dscc": ("Dripping Springs Country Club", "Dripping Springs &middot; standalone, Toptracer", "Buckets $10&ndash;$25; Toptracer from $28/hr", "https://drippingspringscountryclub.com/",
   "It is not a country club. It is a family-run driving range on Highway 290, with Toptracer on the range, a clubhouse bar and food, and hours until 9pm (8pm after the clocks change). Weekday buckets start at $10 for about 50 balls, and a Toptracer bay is $28 an hour on weekdays for up to four people.",
   "3000 W Hwy 290, Dripping Springs"),
 "clay": ("Jimmy Clay &amp; Roy Kizer", "Southeast Austin &middot; muni", "Buckets $7 / $11; short course $5", "https://www.austintexas.gov/golfatx/jimmy-clay-course",
   "This is the best-value serious range in town. The shared city range was enlarged in the 2015 renovation, with bigger targets and an elevated hitting area, and it stays open until 9pm most nights. Next door, the Joe Balander Short Course has four par 3s, a practice bunker and a putting green for $5.",
   "5400 Jimmy Clay Dr, Austin"),
 "penick": ("Harvey Penick Golf Campus", "East Austin &middot; First Tee", "Buckets $8 / $12", "https://www.harveypenickgc.com/",
   "This is the home of First Tee Greater Austin, on land leased from the East Communities YMCA. It has a grass-and-mat range, a putting green, a chipping green, two practice bunkers and a 3-hole short course, which is included with a large bucket when space allows. The range is irons only Monday to Thursday.",
   "5501 Ed Bluestein Blvd, Austin"),
 "forest": ("Forest Creek Golf Club", "Round Rock &middot; lit range", "Buckets $10 / $15", "https://forestcreek.com/practice-facilities/",
   "It is the other late-night option in the north. The range stays open until 10pm daily, opens at 6:30am most days, and a large bucket of about 70 balls is $15. It is a strong choice if you want grass and lights without the drive to Round Rock&rsquo;s standalone range.",
   "99 Twin Ridge Pkwy, Round Rock"),
 "plum": ("Plum Creek Golf Course", "Kyle &middot; Toptracer, short game", "Range price not posted", "https://www.plumcreekgolf.com/golf/toptracer-range",
   "This is the south-side answer. Plum Creek has a Toptracer range and three acres of short-game areas from its 2012 renovation: multiple chipping greens, bunkers, uneven lies and target greens. It is the practice home of Texas State&rsquo;s golf teams. The site does not post a range price, so call ahead.",
   "4301 Benner Rd, Kyle"),
 "tera": ("Teravista Golf Club", "Round Rock &middot; covered Toptracer", "Buckets $10&ndash;$25", "https://teravistagolf.com/practice-facility/",
   "It has covered Toptracer bays and Power Tee, which sets the ball on the tee for you, and the club says it is one of only three in the Austin area with both. The range runs sunrise to 5pm, shorter on Tuesdays and later-starting on Wednesdays.",
   "4333 Teravista Club Dr, Round Rock"),
 "grey": ("Grey Rock Golf Club", "Southwest Austin &middot; mats and grass", "Buckets $14&ndash;$19", "https://www.greyrockgolfandtennis.com/golf/rates",
   "This is the city&rsquo;s upscale course on SH 45. The range is mats Monday to Thursday and grass Friday to Sunday, weather permitting, and the Elite Motion Golf studio beside the tee has Full Swing and FlightScope for lessons and open-bay practice.",
   "7401 Hwy 45, Austin"),
 "butler": ("Butler Pitch &amp; Putt", "Butler Park &middot; 9-hole par 3", "$14 weekdays, $16 weekends", "https://butlerpitchandputt.com/",
   "This is the short-game classic, on the edge of Lady Bird Lake since 1950. It has nine par 3s on real grass greens, a large practice green, clinics and coaching, and no tee times. It is open 8am to 8pm, sells beer and wine, and has Gimme Burger on site. Clubs and a ball rent for $1.",
   "201 Lee Barton Dr, Austin"),
 "topgolf": ("Topgolf Austin", "North Austin &middot; entertainment", "Bays $38&ndash;$64/hr", "https://topgolf.com/us/austin/",
   "This is the entertainment pick, not a traditional range, but the Toptracer numbers in every bay are useful and it is open until midnight or later. Bays hold six and run $38 to $64 an hour, and the online half-off deal cuts that to $19&ndash;$32 Monday to Thursday.",
   "2700 Esperanza Crossing, Austin"),
}

SECTIONS = [
    ("Standalone Ranges", "standalone", ["drr", "dscc"],
     "<strong>Two ranges &middot; no course attached</strong>These exist only for practice, and both stay open after dark."),
    ("Muni and Value Ranges", "value", ["clay", "penick", "forest"],
     "<strong>Three ranges &middot; from $7 a bucket</strong>These are the cheapest serious sessions in the metro, two of them lit late."),
    ("Tech Ranges", "tech", ["plum", "tera", "grey"],
     "<strong>Three ranges &middot; Toptracer, Power Tee and launch monitors</strong>Choose these when you want numbers with your practice."),
    ("Short Game and Social", "short-game", ["butler", "topgolf"],
     "<strong>Two spots &middot; wedges, putting and a crowd</strong>One is the city&rsquo;s best short-game course, the other is Topgolf."),
]

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Austin has more good places to practice than most people use. The guide now covers ten, up from eight, with four new spots, two dropped and every price updated.</p>
    <p>If you only go to one, go to The Driving Range in Round Rock. It is 35 acres of all-grass practice with no course in the way, and it is lit until 10:30pm. For value, the Jimmy Clay and Roy Kizer range is $7 for a small bucket and open until 9pm. For numbers, Plum Creek and Teravista have Toptracer.</p>
    <p>Prices and hours were read on 28 September 2026 and change often, so check before you drive. Summer heat and aeration close ranges more than people expect.</p>
    <h2 class="products-hdr btk-story-hdr">How We Picked</h2>
    <p>We only included outdoor facilities that are open to the public, with a real range or a real short-game area. Indoor simulators have their own guide. Avery Ranch drops off this year, because its buckets now run $10 to $25 and its Toptracer is the app-based version, and Lions moves to a mention: it is 18 holes, not nine, and its range is irons only.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Spots</span><span>Ten</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest bucket</span><span>$7, Jimmy Clay &amp; Roy Kizer</span></div>
      <div class="sidebar-detail"><span class="l">Open latest</span><span>10:30pm, The Driving Range</span></div>
      <div class="sidebar-detail"><span class="l">Toptracer</span><span>Plum Creek, Teravista, Dripping Springs, Topgolf</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Driving Range, Round Rock</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>28 September 2026</span></div>
      <a href="#standalone" class="sidebar-cta">See the list &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#DrivingRange</span>
        <span class="hashtag">#GolfPractice</span>
        <span class="hashtag">#FieldGuide</span>
      </div>
    </div>
  </aside>
</section>
"""

TIPS = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="good-to-know">Good to Know</h2>
  <div {PROSE}>
    <p style="margin:0 0 16px;"><strong>Hit the munis a lot?</strong> Golf ATX&rsquo;s RangeGrinder membership is $95 a month for Austin residents and $110 for non-residents, and it covers three large buckets a day at Jimmy Clay, Roy Kizer, Morris Williams and Lions.</p>
    <p style="margin:0 0 16px;"><strong>Also on the map.</strong> Lions Municipal has an irons-only range and putting greens by downtown. Morris Williams has a range at the same $7 and $11 muni prices. Crystal Falls in Leander has the cheapest buckets we found, from $5, and Blackhawk in Pflugerville sells buckets for $5 on a 15-acre practice facility.</p>
    <p style="margin:0 0 16px;"><strong>Check the calendar.</strong> The city&rsquo;s courses close for aeration and overseeding in late September and October, and ranges close early one day a week for picking and mowing. Every facility here lists its closures on its own site.</p>
  </div>
</section>
"""

FAQ = [
    ("What is the best driving range in Austin?",
     "The Driving Range in Round Rock is the best dedicated practice facility: 35 acres, an all-grass tee, a separate wedge range, chipping and putting greens, and lights until 10:30pm. Inside the city, the Jimmy Clay and Roy Kizer range is the best value."),
    ("What is the cheapest driving range in Austin?",
     "The city's muni ranges at Jimmy Clay, Roy Kizer, Morris Williams and Lions charge $7 for a small bucket and $11 for a large one. Crystal Falls in Leander starts at $5."),
    ("Which Austin driving ranges are open at night?",
     "The Driving Range in Round Rock is lit until 10:30pm and Forest Creek's range is open until 10pm. The Jimmy Clay and Roy Kizer range and Dripping Springs Country Club are open until 9pm."),
    ("Which Austin ranges have Toptracer?",
     "Plum Creek in Kyle, Teravista in Round Rock, Dripping Springs Country Club and Topgolf Austin all use Toptracer. Teravista's bays are covered and also have Power Tee."),
    ("Where can I practice my short game in Austin?",
     "Butler Pitch & Putt has nine par 3s and a large practice green by Lady Bird Lake. Plum Creek has three acres of short-game areas, and the Joe Balander Short Course at Jimmy Clay has four par 3s for $5."),
]


def card(k, idx):
    name, where, price, url, copy, addr = F[k]
    fr = [f["local"] for f in FR[k]]
    label = H.unescape(name).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{where}</div>'
            f'<div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<div class="product-desc" style="font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.7;margin-top:8px;">{addr}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Visit site &#8599;</a></div></div>')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} spots</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = []
    for i, k in enumerate([k for s in SECTIONS for k in s[2]], 1):
        name, _, _, url, _, addr = F[k]
        items.append({"@type": "ListItem", "position": i, "item": {"@type": "SportsActivityLocation", "name": H.unescape(name),
                      "url": url, "address": H.unescape(addr)}})
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-06-15", "dateModified": "2026-09-28",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Guide", "item": "https://thegrassyissue.com/field-guide/"},
            {"@type": "ListItem", "position": 3, "name": "Practice Facilities", "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t} | The Grassy Issue</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    keys = [k for s in SECTIONS for k in s[2]]
    assert len(keys) == 10 == len(set(keys)) and set(keys) == set(F)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/field-guide/">Field Guide</a><span>/</span>
  Practice Facilities</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Austin metro &middot; outdoor practice</span><span class="dot"></span>
    <span>10 spots &middot; re-checked September 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The Driving Range in Round Rock lit up at dusk, seen from above" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        out, n = section(s, n)
        body += out
    body += TIPS + faq_html()
    body += '\n<p style="text-align:center;margin:0 0 40px;"><a href="/field-guide/#practice">&larr; Part of the Austin Golf Field Guide</a></p>\n'
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for leak in ("Manors Revisited", "Burnt Orange", "Nicklaus", "city-owned", "Shop &#8599;"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 10: bad.append("card count")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad:
        sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
