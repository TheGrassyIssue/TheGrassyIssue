#!/usr/bin/env python3
"""build-austin-work-spots.py — Where to Get a Little Work Done in Austin (then sneak in nine). 31 Oct 2026.
Lenny: "a post about the best places to get a little work done in Austin" (atx-bites guide as a start) -> options sheet (21)
-> "add Radio Coffee + beer, add Leona then build the post". Picks: 13 from the sheet + Radio South + Leona = 15.
Cloned from build-golf-video-games.py (wide 16:9 cards). FACTS: research/work-spots-atx/candidates.json (venue sites, Visit Austin,
Infatuation, atx-bites Sept 2026, KVUE Oct 28 2026; all confirmed open 31 Oct 2026; drive distances free-flow estimates);
Radio South hours from radiocoffeeandbeer.com/radio-south; Radio + Leona background from build-coffee-v2.py. Images: venue sites only.
No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Where to Get a Little Work Done in Austin, Then Sneak in Nine"
DESC = ("15 laptop-friendly spots in Austin, from the Central Library and the Carpenter Hotel to Radio, Leona and Flightpath, "
        "each paired with the nearest course, range or simulator for after you log off.")
H1 = "Where to Get a Little Work Done in Austin"
BC = "Where to Get a Little Work Done in Austin"
SLUG = "where-to-work-remotely-austin"
IMG = "/images/austin-work-spots"
SHOP = ""
P = {
 "library": ("Downtown &middot; 710 W Cesar Chavez St", "Austin Central Library + Caf&eacute; Cr&egrave;me", "Butler Pitch &amp; Putt, about a mile", "https://library.austintexas.gov/central-library",
   "The best free office in town. Six floors, free city Wi-Fi, a rooftop deck and bookable rooms for a call, with Caf&eacute; Cr&egrave;me downstairs for crepes, breakfast tacos and a cr&egrave;me br&ucirc;l&eacute;e latte (daily 7am to 9pm). The library runs Monday through Thursday 9am to 8pm and shorter hours the rest of the week. Park in the garage under the building: the first hour is free, then $5 for two. Butler Pitch &amp; Putt is across the lake."),
 "carpenter": ("Zilker &middot; 400 Josephine St", "Carpenter Hotel Coffee Bar", "Butler Pitch &amp; Putt, a walk away", "https://www.bunkhousehotels.com/carpenter-hotel/eat-drink/",
   "The closest pairing on the list: Butler is about 400 yards away. Visit Austin calls the coffee bar laptop-friendly whether you&rsquo;re a guest or not, and it has the living-room setup to back it up, with leather couches, a big communal table, plenty of outlets and a record player. Coffee and breakfast tacos from 7am, then happy hour from 3 to 5pm, which is about when you should be walking over to the first tee."),
 "alfred": ("Downtown &middot; 111 E Cesar Chavez St", "Alfred Coffee at the LINE", "Butler Pitch &amp; Putt, about a mile", "https://www.thelinehotel.com/austin/restaurants-bars/alfred/",
   "The LINE says it outright: stay and catch up on emails, with free Wi-Fi and plenty of spaced-out lobby seating facing the lake. Alfred&rsquo;s iced vanilla latte and matcha, daily 7am to 5pm, with $3 pastries from 3 to 5pm. Parking is the catch: coffee customers get 30 minutes free, so plan on the street or the garage for a longer session."),
 "brewbrew": ("East Downtown &middot; 500 San Marcos St", "The Brew &amp; Brew", "Butler Pitch &amp; Putt, about two miles", "https://www.thebrewandbrew.com/",
   "Coffee in the morning and around 40 beer taps by the afternoon, in one room near Rainey Street. Breakfast sandwiches and grits bowls, open 7am to 8pm every day, with happy hour from 4 to 6pm. A long-time favorite for a working morning that turns into a long lunch."),
 "radio": ("South Austin &middot; 4204 Menchaca Rd", "Radio Coffee &amp; Beer (South)", "Butler Pitch &amp; Putt, a short drive up Lamar", "https://radiocoffeeandbeer.com/radio-south",
   "The original, opened in 2014 in a 1940s house off Menchaca. Radio South opens at 7am every day and stays open until midnight Monday through Saturday, so you can work through the afternoon, step out for nine and come back for a beer and whatever band is on. Food trucks out back, including Veracruz All Natural, and coffee roasted under its own RCB label."),
 "leona": ("Sunset Valley &middot; 6405 Brodie Ln", "Leona Botanical Caf&eacute; &amp; Bar", "Butler Pitch &amp; Putt, about 15 minutes north", "https://www.instagram.com/leonacafebar/",
   "The prettiest office on the list: a garden and pavilion on five acres in Sunset Valley, from the teams behind DEE DEE and Veracruz All Natural. The kitchen opens at 7:30am, which is when to come for a working session; it turns into a bar later in the day. Bring headphones and claim a table in the garden."),
 "spokesman": ("St. Elmo &middot; 440 E St Elmo Rd", "Spokesman Coffee (South)", "Roy Kizer and Jimmy Clay, about 4.5 miles", "https://www.spokesmancoffee.com/south",
   "Plenty of seating, plenty of parking and Glacier Freeze Gatorade on tap, which tells you something. House-roasted coffee, weekday hours of 7am to 9pm and happy hour from 4 to 7pm. When you log off, Roy Kizer and Jimmy Clay are about 11 minutes away, with a range and the Joe Balander short course for a quick loop."),
 "saten": ("East Austin &middot; 916 Springdale Rd", "Sa-T&eacute;n Coffee &amp; Eats", "Morris Williams, under three miles", "https://www.sa-ten.com/",
   "The Infatuation describes it as a room usually packed with people typing at laptops, and the Wi-Fi rarely kicks you off. Japanese coffee and food at The Canopy: thick-cut toast, katsu curry, rice bowls and a brown sugar cappuccino, plus beer and wine. Open 7am to 9pm daily, so you can play first and work after."),
 "medici": ("East Austin &middot; 1023 Springdale Rd", "Medici Roasting (Springdale General)", "Morris Williams, about 2.4 miles", "https://mediciroasting.com/pages/springdale-general",
   "Medici&rsquo;s roastery room at Springdale General is huge and full of natural light, with a covered, dog-friendly patio and a shared common area with Uroko and The Front Page for lunch. Open 7am to 7pm daily, with plenty of parking in the lot."),
 "spread": ("Cherrywood &middot; 2406 Manor Rd", "Spread &amp; Co. (Cherrywood)", "Morris Williams, 1.5 miles down Manor Rd", "https://www.spreadandco.com/cherrywood",
   "A cheese shop and caf&eacute; that works for a half day: espresso and a sandwich, then a happy-hour charcuterie board when the laptop closes. Weekdays 7am to 7pm. Morris Williams is a straight shot down Manor Road."),
 "palomino": ("East Austin &middot; 2023 Airport Blvd", "Palomino Coffee (Airport Blvd)", "Back Nine Golf, same address", "https://palominocoffee.com/",
   "The best golf pairing on the list: Back Nine Golf&rsquo;s East Austin simulator lounge shares the address, at about $50 an hour. The Infatuation calls the roastery a great place to spend a morning working, with a buzzy front half and a calmer back half. Open 7am to 4pm, so it&rsquo;s a morning office."),
 "createscape": ("East Austin &middot; 701 Tillery St", "Createscape Coworking", "Morris Williams, under three miles", "https://www.createscapework.co/coworking-day-passes",
   "For when you need a proper desk and a booth for the 3pm call. A locally owned coworking space with day passes from $25 (an open desk) or $35 for a reserved desk with a monitor, weekdays 9am to 8pm, with fast Wi-Fi, printing, free coffee and tea, and free parking."),
 "strangelove": ("East Austin &middot; 2614 E Cesar Chavez St", "Strangelove Coffee &amp; Wine", "Riverside Golf Course, about 3.5 miles", "https://strangelove.wine/",
   "A 1930s bungalow with a courtyard, from the Figure 8 coffee people and the Small Victory team: coffee and house-made syrups by day, wine and cheese plates by night. Open from 7:30am. Work the afternoon, play Riverside, come back for a glass."),
 "flightpath": ("Hyde Park &middot; 5011 Duval St", "Flightpath Coffeehouse", "Hancock, about 1.6 miles", "https://flightpathcoffeehouse.com/",
   "Built for it since 1992. Flightpath pitches itself to people who need to study or get work done: fast internet, plenty of outlets, big tables, low music and a big dog-friendly patio. The Infatuation notes the unwritten rule is to step outside for calls. East Side Pies slices and Tacodeli tacos, open 7am to 7pm. Hancock&rsquo;s walking nine is four minutes away."),
 "hanks": ("Windsor Park &middot; 5811 Berkman Dr", "Hank&rsquo;s", "Morris Williams, about two miles", "https://www.hanksaustin.com/",
   "The caf&eacute; side of a full restaurant, with plenty of room inside, a covered deck, a big parking lot and a full menu for a working lunch, including new East Coast-style pizzas. Open from 8am daily. Lunch meeting at Hank&rsquo;s, range bucket at Morris Williams."),
}
SECTIONS = [
 ("Downtown, Close to Butler", "downtown", ["library", "carpenter", "alfred", "brewbrew"],
  "<strong>Four spots &middot; all within two miles of Butler Pitch &amp; Putt</strong>Butler is first come, first served, open until 8pm, and $14 on weekdays."),
 ("South Austin", "south", ["radio", "leona", "spokesman"],
  "<strong>Three spots</strong>Late hours, big patios and Roy Kizer and Jimmy Clay to the south."),
 ("East Austin", "east", ["saten", "medici", "spread", "palomino", "createscape", "strangelove"],
  "<strong>Six spots</strong>Most of them are within three miles of Morris Williams."),
 ("North and Central", "north", ["flightpath", "hanks"],
  "<strong>Two spots</strong>Hancock and its $16 sunset rate are close by."),
]
N = 15
PQ = {}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>Some days the best tee time is the one you can steal at 4pm. Working from a coffee shop near a course is the cheapest way to make that happen: close the laptop, drive five minutes and you&rsquo;re on the first tee with daylight to spare.</p>
    <p>With the clocks falling back on November 1, the window gets shorter. Sunsets in November come around 5:30 to 5:45pm, which means packing up by about 3:30 or 4 if you want a full nine. So this list is built backwards from the golf: 15 places in Austin where you can get a few hours of work done, each paired with the nearest course, range or simulator.</p>
    <p><strong>A note on laptops.</strong> Not every caf&eacute; wants you camping. KVUE reported on October 28 that Better Half now bans laptops in its booths, and plenty of places quietly feel the same. Every spot here either welcomes laptops or has a reputation for it, and all were open when we checked on October 31. Buy something every couple of hours, take calls outside, and don&rsquo;t spread out over a four-top at lunch.</p>
    <p>We&rsquo;ve covered Austin coffee before, in <a href="/drops/austin-coffee-guide">our pre-round pour guide</a> and <a href="/drops/fourteen-independent-austin-coffee-shops">the fourteen independents we keep going back to</a>. This one is about the work, and the nine after it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Spots</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Free option</span><span>Central Library</span></div>
      <div class="sidebar-detail"><span class="l">Closest to golf</span><span>Carpenter Hotel (Butler)</span></div>
      <div class="sidebar-detail"><span class="l">Open latest</span><span>Radio South, midnight</span></div>
      <div class="sidebar-detail"><span class="l">Pack up by</span><span>About 3:30pm in November</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Flightpath</span></div>
      <div class="hashtags">
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#WorkThenPlay</span>
        <span class="hashtag">#TwilightNine</span>
      </div>
    </div>
  </aside>
</section>
"""
ROWS = [("Austin Central Library", "Butler Pitch &amp; Putt", "~1 mi"), ("Carpenter Hotel Coffee Bar", "Butler Pitch &amp; Putt", "~0.4 mi"),
 ("Alfred at the LINE", "Butler Pitch &amp; Putt", "~1.3 mi"), ("The Brew &amp; Brew", "Butler Pitch &amp; Putt", "~2 mi"),
 ("Radio South", "Butler Pitch &amp; Putt", "short drive"), ("Leona", "Butler Pitch &amp; Putt", "~15 min"),
 ("Spokesman South", "Roy Kizer / Jimmy Clay", "~4.5 mi"), ("Sa-T&eacute;n", "Morris Williams", "~2.7 mi"),
 ("Medici Springdale", "Morris Williams", "~2.4 mi"), ("Spread &amp; Co. Cherrywood", "Morris Williams", "~1.5 mi"),
 ("Palomino Airport Blvd", "Back Nine Golf (sims)", "same address"), ("Createscape", "Morris Williams", "~2.8 mi"),
 ("Strangelove", "Riverside", "~3.5 mi"), ("Flightpath", "Hancock", "~1.6 mi"), ("Hank&rsquo;s", "Morris Williams", "~2 mi")]
TABLE = ('\n<section id="gg-table">\n<style>#gg-table{padding:40px 20px 8px;border-top:1px solid var(--ink,#141414)}#gg-table .t-in{max-width:960px;margin:0 auto}'
 '#gg-table h2{font-family:var(--serif,Georgia,serif);font-size:clamp(22px,3vw,30px);text-align:center;margin:0 0 6px;font-weight:400}'
 '#gg-table .t-sub{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-align:center;opacity:.6;margin-bottom:18px}'
 '#gg-table .t-wrap{overflow-x:auto}#gg-table table{width:100%;border-collapse:collapse;font-size:14px}#gg-table th{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;padding:8px 10px;border-bottom:1px solid var(--ink,#141414)}'
 '#gg-table td{padding:9px 10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top}#gg-table td:first-child{font-weight:500}</style>\n'
 '<div class="t-in"><h2 id="log-off">Log Off, Then Play</h2><div class="t-sub">Nearest golf to each spot &middot; free-flow drive estimates, add traffic</div><div class="t-wrap"><table>\n'
 '<thead><tr><th>Work</th><th>Then play</th><th>Distance</th></tr></thead><tbody>\n'
 + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in ROWS) + '\n</tbody></table></div></div>\n</section>\n')
STORY = TABLE
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/work-spots-atx/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GG-WIDE*/.products-grid[data-wide]>.product-card{flex:0 0 100%!important;display:grid;grid-template-columns:3fr 2fr}.products-grid[data-wide] .product-gallery{aspect-ratio:16/9}.products-grid[data-wide] .product-body{display:flex;flex-direction:column;justify-content:center;text-align:left!important;padding:22px 26px}@media(max-width:820px){.products-grid[data-wide]>.product-card{grid-template-columns:1fr}}</style>'
            '<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item}</div><div class="product-brand">Then play: {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Visit &#8599;</a></div></div>')


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(P[h][1])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-31", "dateModified": "2026-10-31",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"spot" if len(ids)==1 else "spots"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}" data-wide="1">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
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
    <span>Austin, Texas</span><span class="dot"></span>
    <span>15 spots &middot; checked October 31, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="People working on laptops at big tables inside Flightpath Coffeehouse in Hyde Park" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
