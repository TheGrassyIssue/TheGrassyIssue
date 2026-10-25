#!/usr/bin/env python3
"""build-pnw-trip.py — Field Note: a five-day Pacific Northwest golf trip for 2027. Cloned from build-austin-weekend.py. 12 October 2026.
Lenny: "Setting my intention for 2027 a golf trip to the PNW ... Wildwood golf course, Chambers Bay, Gamble Sands, The Home Course.
Research cool restaurants, sites to see and if there's any public must-play courses for a 5 day trip", then picked "Reverse it"
(start at Gamble Sands, finish in Portland), Gold Mountain as the bonus course and Bandon Dunes as a footnote, and asked to plug
the TGI Social Club at the end.
FACTS: research/pnw-trip-2027/research-2026-10-12.md (official course, restaurant and agency sites read 12 Oct 2026).
Wildwood's listed domain (golfingwildwood.com) now redirects to a gambling site and is NOT linked; the OGA page is.
PHOTOS: each course's and venue's own; USFS for Multnomah Falls; OGA for Wildwood.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "My 2027 PNW Golf Trip: Gamble Sands, Chambers Bay and Five Days to Remember"
DESC = ("The five-day Pacific Northwest golf trip I am planning for 2027: Gamble Sands and Scarecrow, Chambers Bay, The Home Course, "
        "Wildwood in Portland and a bonus round at Gold Mountain, with where to eat, what to see and when to book.")
H1 = "Field Note: My 2027 Golf Trip to the Pacific Northwest"
BC = "My PNW Golf Trip"
SLUG = "pnw-golf-trip-gamble-sands-chambers-bay"
IMG = "/images/pnw-trip-2027"
FR = json.loads((ROOT / "research/pnw-trip-2027/frames.json").read_text())
P = {
 # key: (kicker, name, price-or-area, url, copy, frames, link label)
 "inn": ("Day 1 &middot; Brewster, Washington", "The Inn at Gamble Sands", "From $475 a night, May&ndash;Oct 2027",
   "https://www.gamblesands.com/rates",
   "The plan is to fly Seattle to Wenatchee on Alaska, about 90 minutes from the resort, though a four-hour drive from Sea-Tac is the backup. We want to stay on site: every room has a fireplace, the 40 Golf View rooms look over Scarecrow, and overnight guests can already book tee times for every 2027 date, while day visitors only get 120 days out. That alone makes the case.",
   FR["inn"], "Rates and booking"),
 "quicksands": ("Day 1, late afternoon", "QuickSands", "$80 in 2027",
   "https://www.gamblesands.com/quicksands/",
   "Fourteen short holes on the bluff with a pull cart and a couple of wedges. After a travel day, this is the round we have in mind first: no pressure, big views over the Columbia River, and a chance to get our eyes in before the big courses. Ideally as the light drops.",
   FR["quicksands"], "Book QuickSands"),
 "cascades": ("Day 1, after dark", "The Cascades Putting Course", "At the resort",
   "https://www.gamblesands.com/cascades/",
   "A 100,000-square-foot putting course, 175 yards end to end, that the resort calls an homage to the Himalayas at St Andrews. There are fire pits, and after dark they hand out glow balls. This is where we figure the first bet of the trip gets settled.",
   FR["cascades"], "Visit"),
 "barn": ("Day 1 dinner &middot; on site", "The Barn", "All day",
   "https://www.gamblesands.com/food-and-drink/",
   "The casual one: pizzas, sliders and a canning machine that seals cocktails to go. A patio dinner, the sun going down over the river and an early night is the idea. The next day is 36 holes.",
   FR["barn"], "Visit"),
 "sands": ("Day 2 morning", "Gamble Sands", "$315 May&ndash;Sep 2027, cart included",
   "https://www.gamblesands.com/rates",
   "David McLay Kidd's course on a sandy bluff above the Columbia, with fairways so wide and greens so receptive that the whole design is about fun rather than punishment. We are thinking a morning tee time, while the wind is down. If the dates slide, April and October are shoulder season at $235.",
   FR["sands"], "Tee times"),
 "scarecrow": ("Day 2 afternoon", "Scarecrow", "$210 as a second 18",
   "https://www.gamblesands.com/rates",
   "The second course, designed by McLay Kidd with Nick Schaan and opened slightly more than a decade after the first. It is wilder than the original, and the second-18 rate would make an afternoon round the best value of the trip. If we only have legs for one more 18 all week, this is the one.",
   FR["scarecrow"], "Tee times"),
 "dannyboy": ("Day 2 dinner &middot; on site", "Danny Boy", "Dinner only",
   "https://www.gamblesands.com/food-and-drink/",
   "The resort's steakhouse: prime rib, ribeye and the Tower of Tots, with a sommelier on site. After 36 holes in the desert it feels earned. We will try to book the table when we book the room.",
   FR["dannyboy"], "Visit"),
 "tsillan": ("Day 3 morning &middot; Lake Chelan", "Tsillan Cellars and Sorrento&rsquo;s Ristorante", "South Shore",
   "https://tsillancellars.com",
   "The drive west passes the south shore of Lake Chelan, 35 miles from the resort. Tsillan is an estate winery with an Italian restaurant on the same property, under new local owners as of July 2026. It is on our list as a stop for the view and a bottle for the car.",
   FR["tsillan"], "Visit"),
 "munchen": ("Day 3 lunch &middot; Leavenworth", "M&uuml;nchen Haus", "No reservations",
   "https://www.munchenhaus.com",
   "Halfway over Stevens Pass is Leavenworth, a whole town built to look Bavarian. M&uuml;nchen Haus is its sausage grill and beer garden, with Icicle Brewing beers on tap. A good place to eat outside and stretch our legs before getting back on US-2.",
   FR["munchen"], "Visit"),
 "homecourse": ("Day 3 twilight &middot; DuPont", "The Home Course", "$64&ndash;$70, twilight $54&ndash;$56",
   "https://www.thehomecourse.com",
   "Owned and run by the Pacific Northwest Golf Association and Washington Golf, and laid out for walking with views of Puget Sound, the Olympics and Mount Rainier. It would be the cheapest great round of the week and is about 20 minutes from Chambers Bay. The idea is to roll in off the pass and catch a twilight time. Rates read in October 2026; the association rate applies to Oregon Golf Association members.",
   FR["homecourse"], "Rates and tee times"),
 "copper": ("Day 3 dinner &middot; Point Ruston", "Copper &amp; Salt Northwest Kitchen", "Ruston waterfront",
   "https://www.copperandsaltnw.com",
   "Italian-leaning Northwest cooking on the Ruston waterfront, recommended by Chambers Bay itself, with Point Defiance Park next door. It books on OpenTable. Staying nearby would put us about 15 minutes from the first tee in the morning.",
   FR["copper"], "Visit"),
 "chambers": ("Day 4 morning &middot; University Place", "Chambers Bay", "$279 non-resident in Sep 2026, plus 15.2% tax",
   "https://chambersbaygolf.com/golf/",
   "The reason for the trip. Robert Trent Jones II built it on an old sand and gravel mine above Puget Sound, and it hosted the 2015 U.S. Open. It is walking only, and we plan to take caddies ($100 a bag plus tip) and budget five hours. Non-resident advance times for April to October 2026 opened on January 1; if 2027 works the same way, that is the alarm to set.",
   FR["chambers"], "Rates and booking"),
 "gold": ("Day 4 afternoon &middot; the bonus round", "Gold Mountain Golf Club, Olympic Course", "Dynamic pricing",
   "https://goldmountaingolf.com/green-fees/",
   "If our legs survive Chambers, the idea is to drive 40 minutes across the Narrows to Bremerton. The Olympic is a city-owned course through tall firs that hosted the 2006 U.S. Amateur Public Links, and Chambers Bay bundles it into its own package with The Home Course. Rates move with demand, so this one gets decided closer to the day.",
   FR["gold"], "Green fees"),
 "tides": ("Day 4 dinner &middot; Gig Harbor", "Tides Tavern", "21 and over",
   "https://tidestavern.com",
   "On the way back from Bremerton, a waterfront tavern in a 1910 building that has been pouring beer since 1973, with Mount Rainier across the harbor on a clear night. It is now part of the Anthony's family, it is 21 and over, and its own site lists two sets of hours, so we will call ahead.",
   FR["tides"], "Visit"),
 "pinestate": ("Day 5 brunch &middot; Portland", "Pine State Biscuits", "Daily 8am&ndash;2pm",
   "https://pinestatebiscuits.com",
   "Two hours and change down I-5 would put us in Portland in time for the Reggie Deluxe: fried chicken, bacon, cheddar and an egg on a biscuit, covered in gravy. There are four locations, so we will hit whichever is on the way to the course.",
   FR["pinestate"], "Visit"),
 "wildwood": ("Day 5 afternoon &middot; NW St. Helens Rd", "Wildwood Golf Course", "Call for rates",
   "https://exploreoregongolf.oga.org/wildwood-golf-course",
   "The plan is to finish small. Wildwood is a hilly public course from 1990, 15 miles north of downtown off Highway 30, with creeks running through it and the Cascade volcanoes on the skyline. It is short, around 5,850 yards, and the right last round to play for pride. It does not have a working website, so it is a phone call to (503) 621-3402 to book.",
   FR["wildwood"], "Course listing"),
 "lepigeon": ("Day 5 dinner &middot; 738 E Burnside", "Le Pigeon", "Tasting menus",
   "https://www.lepigeon.com",
   "The last night gets the big dinner. Le Pigeon is a Portland institution that now serves tasting menus only, omnivore or vegetarian. It is the one reservation we will make well ahead.",
   FR["lepigeon"], "Reserve"),
 "multnomah": ("Next morning &middot; before the flight", "Multnomah Falls", "Columbia River Gorge",
   "https://www.fs.usda.gov/r06/columbiarivergorge/recreation/multnomah-falls",
   "Thirty minutes east of PDX on I-84, a 620-foot waterfall right off the highway. In 2026 the Forest Service required timed permits from May 22 to September 7, so going after Labor Day should mean no permit, but we will check Recreation.gov first. Then home.",
   FR["multnomah"], "Plan a visit"),
}
SECTIONS = [
 ("Day 1: Arrive at Gamble Sands", "day-1", ["inn","quicksands","cascades","barn"],
  "<strong>Brewster, Washington</strong>The idea: fly into Wenatchee, check in, play the short course at sunset and putt by firelight."),
 ("Day 2: Thirty-Six Holes Above the Columbia", "day-2", ["sands","scarecrow","dannyboy"],
  "<strong>The two big courses</strong>Gamble Sands in the morning, Scarecrow in the afternoon at the second-18 rate, then steak."),
 ("Day 3: Over the Cascades", "day-3", ["tsillan","munchen","homecourse","copper"],
  "<strong>Lake Chelan, Leavenworth, Stevens Pass</strong>Four and a half hours of driving with the best stops in the state, then a twilight round in DuPont."),
 ("Day 4: Chambers Bay", "day-4", ["chambers","gold","tides"],
  "<strong>The U.S. Open course, then the bonus</strong>Chambers Bay with caddies in the morning. If we still have it in us, Gold Mountain after lunch, then dinner on the harbor."),
 ("Day 5: Portland", "day-5", ["pinestate","wildwood","lepigeon","multnomah"],
  "<strong>Biscuits, a hilly muni and the big dinner</strong>Down I-5 to Oregon for one last round, then a waterfall on the way to the airport."),
]
N = 18
PQ = {
 "day-5": ("Mount Hood, Saint Helens and Adams dominate the skyline, while the Columbia River and Downtown Portland paint the backdrop as golfers navigate the terrain.", "Oregon Golf Association, on Wildwood"),
}
BANDS = {
 "day-2": ("Gamble Sands", "Photos courtesy of Gamble Sands: Scarecrow at sunset, the Sands course from above, and the Inn on the bluff.", [("band-1","Scarecrow at sunset above a bend in the Columbia River","Scarecrow"),("band-2","Black and white aerial of bunkers and fairways at Gamble Sands","From above"),("band-3","The Inn at Gamble Sands on the bluff with the Cascades behind","The Inn")]),
 "day-4": ("Chambers Bay", "Photos courtesy of Chambers Bay: the lone fir, the clubhouse above the Sound, and the course in the evening.", [("band-4","The lone fir tree at Chambers Bay at sunset over Puget Sound","The lone fir"),("band-5","The Chambers Bay clubhouse above a green with Puget Sound behind","The clubhouse"),("band-6","Golfers walking past a tall fir on the edge of Puget Sound at Chambers Bay","The walk")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>I am setting my intention for 2027: a golf trip to the Pacific Northwest. Chambers Bay and Gamble Sands have been on my list for years, and I am writing the plan down so it actually happens. Nothing is booked yet and all of it is flexible, but here is what is on our radar: five days, two states and six rounds, from the sand dunes of eastern Washington to a hilly muni outside Portland.</p>
    <p>The rough shape: start at Gamble Sands, David McLay Kidd&rsquo;s resort on a bluff above the Columbia River, for 36 holes and a night on the putting course. Cross the Cascades past Lake Chelan and Leavenworth to Tacoma for The Home Course and Chambers Bay, with Gold Mountain as a bonus round if our legs allow. Finish in Portland at Wildwood, with one big dinner and a waterfall on the way to the airport.</p>
    <p>We are leaning toward September. Gamble Sands is still at its peak, Chambers Bay is cheaper than in high summer, the rain usually has not arrived west of the mountains, and after Labor Day the Multnomah Falls permit season is over. The thinking is to fly into Wenatchee and out of Portland.</p>
    <p><strong>How we would book it.</strong> The Inn at Gamble Sands first: overnight guests can already book every 2027 date, room and tee times together. Then Chambers Bay, where non-resident advance times opened on January 1 in 2026. Then Le Pigeon and everything else. Green fees for the six rounds come to roughly $1,200 to $1,400 a person before lodging, using 2027 rates at Gamble Sands and 2026 rates elsewhere. Stops will move around, and I will update this as the plan firms up.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Plan So Far</div>
      <div class="sidebar-detail"><span class="l">When</span><span>Thinking September 2027</span></div>
      <div class="sidebar-detail"><span class="l">Rounds</span><span>6, plus a putting course</span></div>
      <div class="sidebar-detail"><span class="l">Courses</span><span>Gamble Sands, Scarecrow, QuickSands, The Home Course, Chambers Bay, Wildwood</span></div>
      <div class="sidebar-detail"><span class="l">Bonus</span><span>Gold Mountain, Olympic</span></div>
      <div class="sidebar-detail"><span class="l">Fly</span><span>In to Wenatchee or Seattle, out of Portland</span></div>
      <div class="sidebar-detail"><span class="l">Green fees</span><span>~$1,200&ndash;$1,400</span></div>
      <div class="sidebar-detail"><span class="l">Book first</span><span>The Inn at Gamble Sands</span></div>
      <a href="/events/social-club" class="sidebar-cta">Join the TGI Social Club &#8594;</a>
      <div class="hashtags">
        <span class="hashtag">#PNWGolf</span>
        <span class="hashtag">#GambleSands</span>
        <span class="hashtag">#ChambersBay</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
MORE = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="more-time">If We Have More Time</h2>
  <p class="cat-kicker"><strong>Mount Rainier</strong>If we can steal a day, it is a day trip from Tacoma. In 2026 the park needed no timed-entry reservation, just the entrance fee.</p>
  <p class="cat-kicker"><strong>Seattle</strong>With a night to spare, we would eat at <a href="https://canlis.com" target="_blank" rel="noopener" style="border-bottom:1px solid currentColor;">Canlis</a>, the family-run fine dining room that has been open since 1950, then a late burger at <a href="https://ddir.com" target="_blank" rel="noopener" style="border-bottom:1px solid currentColor;">Dick&rsquo;s Drive-In</a>.</p>
  <p class="cat-kicker"><strong>Bandon Dunes</strong>The obvious question. It is about four and a half hours south of Portland, too far for five days, and a whole trip of its own. Call it 2028.</p>
</section>
"""
CLUB = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Come play</div>
  <h2 class="products-hdr" id="social-club">The TGI Social Club</h2>
  <p class="cat-kicker"><strong>Find your foursome before 2027</strong>A trip like this is only as good as the people in the car, and I am still filling seats. The Grassy Issue Social Club is how I find them: small groups of eight to twelve people playing good courses in and around Austin, no dues, everyone pays their own green fee. Join the interest list, come play a few rounds with me, and maybe I will see you on the first tee at Gamble Sands. <a href="/events/social-club" style="border-bottom:1px solid currentColor;">Join the Social Club &#8594;</a></p>
</section>
"""
FAQ = [
 ("When is the best time for a Pacific Northwest golf trip?", "September. Gamble Sands is still in its peak season, Chambers Bay's non-resident rate drops from $325 in July and August to $279 in September (2026 rates), it is usually drier west of the Cascades, and the Multnomah Falls timed-permit season ended on September 7 in 2026."),
 ("How far is Gamble Sands from Seattle?", "About 221 miles and four hours by car, according to the resort. Wenatchee airport, with Alaska flights from Seattle, is 77 miles and about 90 minutes away."),
 ("How much does it cost to play Chambers Bay?", "Non-resident rates in 2026 started at $220 in April, $299 in June, $325 in July and August, $279 in September and $229 in October, plus 15.2% tax. Caddies are $100 a bag plus tip. 2027 rates had not been published on October 12, 2026."),
 ("Is Chambers Bay walking only?", "Yes. Push carts are free and caddies are available; motorized carts are only for golfers with a medical need."),
 ("How much does Gamble Sands cost in 2027?", "Gamble Sands or Scarecrow is $315 from May to September 2027 and $235 in April and October, with a second 18 the same day at $210 in peak season. QuickSands is $80. Cart included; taxes extra."),
 ("Who owns The Home Course?", "It is cooperatively owned and operated by the Pacific Northwest Golf Association and Washington Golf. Rates in October 2026 were $64 Monday to Thursday and $70 Friday to Sunday for 18 holes."),
]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
def card(k, idx):
    kick, item, price, url, copy, fr, lab = P[k]
    ext = url.startswith("http")
    label = H.unescape(item).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    arrow = " &#8599;" if ext else " &#8594;"
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{kick}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}"{tgt} class="product-link">{lab}{arrow}</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": (P[h][3] if P[h][3].startswith("http") else "https://thegrassyissue.com" + P[h][3]), "name": H.unescape(P[h][1])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-12", "dateModified": "2026-10-12",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]},
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



def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG + "/" + f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"stop" + ("" if len(ids)==1 else "s")}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert all((ROOT / f.lstrip("/")).is_file() for f in P[k][5]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Washington and Oregon</span><span class="dot"></span>
    <span>5 days &middot; 6 rounds &middot; checked 12 October 2026</span><span class="dot"></span>
    <span>Hero photo courtesy of Gamble Sands</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Sunset over the Columbia River from the high bluff at Gamble Sands in Brewster, Washington" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += MORE
    body += CLUB
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Lost Pines", "Barton Springs", "Kizer"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
