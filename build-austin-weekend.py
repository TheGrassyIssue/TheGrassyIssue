#!/usr/bin/env python3
"""build-austin-weekend.py — Field Note: The Austin Golf Weekend (cloned from build-magpie-btk.py). 2 October 2026.\n\nLenny: "Let's create a new field note about a fantastic Austin Golf weekend- Where to play, eat, hang out after the round, and suggest a few cool items", then "lets build the post". Revised 2 Oct per Lenny ("no on Hancock, let's do Lion, Kizer then a extra nice round like wild springs"; no AustinKnittyLimits; add a ball marker; hero from Wild Spring Dunes; then "not wild springs- Lost Pines Golf Club"). Venues re-verified on their own sites 2 Oct 2026 (LeRoy and Lewis truck closed; using the Emerald Forest Dr restaurant). Course fees from the Field Guide (City of Austin, read 17 Sep 2026).\n

Lenny: "Let's also do a brand to know - https://magpie-supply.com/", approved the TGI Take ("looks good, let's build it").
All 10 products run (the whole store). FACTS: catalogue, prices and stock read from the Squarespace JSON on 2 Oct 2026
(research/magpie/items.json); story from magpie-supply.com/our-story (quoted verbatim). Founder not named on the site.
PHOTOS: Magpie's own store and site images, localised to /images/magpie-supply.

--- original Palm docstring follows ---

Lenny: "Let's do a brand to know - https://palmgolfco.com/", then "looks good" on the 38-option sheet
(research/palm/options.json), so all 38 run. FACTS: catalogue read from palmgolfco.com/products.json on 2 Oct 2026;
story and founder quotes from MyGolfSpy, "Palm Golf Swings And Smiles Its Way To Cult Following" (Sean Fairholm,
21 Mar 2025, a brand-story feature); the MyGolfSpy comfort line is quoted on Palm's own homepage. Product copy written
from each listing and its photos. PHOTOS: Palm's own store images, localised to /images/palm-golf.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "The Austin Golf Weekend: Where to Play, Eat and Drink"
DESC = ("An Austin golf weekend: Lions Muni on Friday, Roy Kizer on Saturday and Lost Pines Golf Club on Sunday, "
        "with breakfast tacos, barbecue, Barton Springs, a vinyl bar and six things to pack.")
H1 = "The Austin Golf Weekend: Lions, Kizer and a Sunday at Lost Pines"
BC = "Austin Golf Weekend"
SLUG = "austin-golf-weekend"
IMG = "/images/austin-weekend"
W = IMG
P = {
 # key: (kicker, name, price-or-area, url, copy, frames, link label)
 "lions": ("Friday afternoon &middot; Enfield Rd", "Lions Municipal Golf Course", "$41 Fridays",
   "/drops/lions-municipal-golf-course-austin",
   "Start where Austin golf started. Lions opened in 1924, Ben Crenshaw and Tom Kite learned here, and it was one of the first courses in the South to desegregate. It is short at 6,001 yards, par 71, but the tree-lined fairways are narrow, so leave the driver in the bag more than you think. Walk it. The Friday rate is $41, or $28 after the sunset cutoff.",
   [f"{W}/lions.jpg", f"{W}/lions-3.jpg", f"{W}/lions-2.jpg", f"{W}/lions-4.jpg"], "Our guide"),
 "barton": ("Friday, after the round &middot; Zilker Park", "Barton Springs Pool", "$9 visitors, $5 residents",
   "https://www.austintexas.gov/services/visit-barton-springs-pool",
   "Ten minutes from Lions: three acres of spring-fed water that holds at 68 to 70 degrees all year. After 18 holes in the Texas sun there is nothing better. Adult admission is $9 for visitors and $5 for Austin residents, paid at the kiosk or the cash window. No coolers, glass or alcohol. It is closed Thursdays from 9am to 7pm for cleaning, which does not touch a weekend.",
   [f"{W}/barton.jpg", f"{W}/barton-2.jpg", f"{W}/barton-3.jpg"], "Visit"),
 "loro": ("Friday dinner &middot; 2115 S Lamar Blvd", "Loro", "South Lamar",
   "https://www.loroeats.com/locations/austin/south-lamar/",
   "Five minutes from the springs: Aaron Franklin and Tyson Cole's Asian smokehouse, with brisket, smoked turkey and a big patio that suits a group still damp from the pool. It is open until 11pm on Fridays and Saturdays.",
   [f"{W}/loro-2.jpg", f"{W}/loro.jpg", f"{W}/loro-3.jpg", f"{W}/loro-4.jpg"], "Visit"),
 "equipment": ("Friday night &middot; 1101 Music Ln", "Equipment Room", "Under Hotel Magdalena",
   "https://equipmentroom.com/",
   "A listening bar in the old equipment room beneath Hotel Magdalena, built on the Japanese jazz kissa: records played on vintage hi-fi, proper cocktails and small plates. It opens at 5pm on Fridays and stays open until 2am. Book on Resy or try for one of the walk-in tables.",
   [f"{W}/equip-3.jpg", f"{W}/equipment-room.jpg", f"{W}/equip-2.jpg", f"{W}/equip-4.jpg"], "Visit"),
 "veracruz": ("Saturday, 7am &middot; 3504 Montopolis Dr", "Veracruz All Natural, East Radio", "Southeast Austin",
   "https://www.veracruzallnatural.com/locations",
   "The East Radio truck opens at 7am and sits about ten minutes from Kizer. Get the migas taco. Breakfast tacos before a Saturday round is the most Austin start there is.",
   [f"{W}/veracruz-2.jpg", f"{W}/veracruz-3.jpg", f"{W}/veracruz-4.jpg", f"{W}/veracruz.jpg"], "Visit"),
 "kizer": ("Saturday morning &middot; Southeast Austin", "Roy Kizer Golf Course", "$44 weekends",
   "/drops/roy-kizer-from-sewage-plant-to-links-style-gem",
   "After a tight Lions, Kizer lets you swing. It is a Randolph Russell links-style course from 1994, built on an old wastewater plant, with wide flat fairways and lakes and wetlands running through them. 6,819 yards, par 71. Wind is the real hazard. The weekend rate is $44. Saturday tee times open online at 8pm Central the Monday before, one tee time per Golf ATX account.",
   [f"{W}/kizer.jpg", f"{W}/kizer-2.jpg", f"{W}/kizer-3.jpg"], "Our guide"),
 "leroy": ("Saturday lunch &middot; 5621 Emerald Forest Dr", "LeRoy and Lewis Barbecue", "South Austin",
   "https://leroyandlewisbbq.com/",
   "The new-school barbecue crew has closed its Pickle Road truck to focus on this restaurant in South Austin, which is in the Michelin Guide. It opens at 11am, so you can come straight from Kizer.",
   [f"{W}/leroy-2.jpg", f"{W}/leroy-3.jpg", f"{W}/leroy-4.jpg", f"{W}/leroy.jpg"], "Visit"),
 "meanwhile": ("Saturday afternoon &middot; 3901 Promontory Point Dr", "Meanwhile Brewing", "Southeast Austin",
   "https://www.meanwhilebeer.com",
   "Back near Kizer: a brewery with a huge lawn, food trucks, a soccer field and its own lagers. Spend the afternoon outside and watch the games. Sunday is the nice round, so do not stay too late.",
   [f"{W}/meanwhile.jpg", f"{W}/meanwhile-2.jpg", f"{W}/meanwhile-3.jpg"], "Visit"),
 "lostpines": ("Sunday &middot; 575 Hyatt Lost Pines Rd", "Lost Pines Golf Club", "Rates vary by day",
   "https://www.lostpinesresortandspa.com/golf/",
   "Finish the weekend at the resort course out by Bastrop. It is an Arthur Hills design, 7,300 yards and par 72, laid along the natural contours of the Lost Pines woodland, and The Dallas Morning News has named it one of the best courses in Texas. The signature holes are the 603-yard par-5 3rd and the 155-yard downhill par-3 12th. There is a 13-acre range with eight target greens if you want to warm up properly. Green fees change by day, so check the resort's tee sheet when you book, then stay for a drink at Maude's Bar &amp; Terrace on the property.",
   [f"{W}/lostpines-4.jpg", f"{W}/lostpines-0.jpg", f"{W}/lostpines-2.jpg", f"{W}/lostpines-1.jpg"], "Course and tee times"),
 "criquet": ("Criquet Shirts &middot; Austin", "Slub Graphic Tee, Lions Badge", "$58",
   "https://criquetshirts.com/products/slub-graphic-t-shirt-lions-badge-vintage-indigo",
   "Austin's own shirt brand made a Lions Municipal badge tee in vintage indigo. Wear it to Friday's round and then all year at home.",
   [f"{W}/criquet-0.jpg", f"{W}/criquet-1.jpg", f"{W}/criquet-2.jpg"], "Shop"),
 "duffle": ("Criquet x Jones &middot; Austin", "Letterman Duffle, Criquet Patch", "$150",
   "https://criquetshirts.com/products/criquet-x-jones-letterman-duffle-criquet-patch-black",
   "A black duffle from Criquet and Jones with the Criquet patch, for three days of golf clothes and a pair of shoes. It is the bag that carries the whole weekend.",
   ["/images/criquet/jones-duffle-0.jpg", "/images/criquet/jones-duffle-1.jpg", "/images/criquet/jones-duffle-2.jpg"], "Shop"),
 "orms": ("Clint Orms &middot; Kerrville, Texas", "Ball Marker 1801, Sterling Silver Texas Flag", "$300",
   "https://clintorms.com/products/sterling-silver-texas-flag-ball-marker",
   "A sterling silver marker with an engraved Texas flag on one side and scrollwork on the other, made and engraved by hand in the Hill Country. It is a splurge, and one you will keep for decades. The engraved State of Texas marker is $220.",
   [f"{W}/orms-0.jpg", f"{W}/orms-1.jpg", f"{W}/orms-3.jpg", f"{W}/orms-2.jpg"], "Shop"),
 "magpie": ("Magpie Supply &middot; Denver", "Scorecard Holder", "$75",
   "https://magpie-supply.com/on-the-course/p/scorecard-holder",
   "Keep all three cards. This one is black full-grain leather made in Denver, holds a standard scorecard and fits a back pocket. Only a few were left when we checked.",
   ["/images/magpie-supply/m01-0.jpg", "/images/magpie-supply/m01-1.jpg", "/images/magpie-supply/m01-2.jpg"], "Shop"),
 "sierra": ("Sierra Madre Golf &middot; Austin", "Sierra Madre Golf Towel", "$22",
   "https://sierramadregolf.com/products/sierra-madre-towel",
   "A waffle-weave towel with a carabiner from the Austin brand, in chartreuse, burgundy or desert orange. Clip it on Friday and it will remind you of the trip every time you clean a club.",
   [f"{W}/smg-0.jpg", f"{W}/smg-1.jpg", f"{W}/smg-3.jpg"], "Shop"),
 "palm": ("Palm Golf Co. &middot; Huntington Beach", "Divot Repair Tool (Bottle Opener)", "$11.99",
   "https://palmgolfco.com/products/divot-repair-tool-bottle-opener-silver",
   "Fix your pitch marks at Kizer, then open a Lone Star at Meanwhile. A divot tool with a bottle opener built in, for the price of a beer.",
   ["/images/palm-golf/p34-0.jpg", "/images/palm-golf/p34-1.jpg", "/images/palm-golf/band-p34-3.jpg"], "Shop"),
}
SECTIONS = [
 ("Friday: Lions, Then the Springs", "friday", ["lions","barton","loro","equipment"],
  "<strong>The historic muni and a cold swim</strong>Play Lions in the afternoon, jump in Barton Springs, then smoked brisket on South Lamar and records under Hotel Magdalena."),
 ("Saturday: Kizer and a Long Lunch", "saturday", ["veracruz","kizer","leroy","meanwhile"],
  "<strong>Open fairways, then barbecue</strong>Tacos at 7am, the links-style muni in southeast Austin, a barbecue lunch and a brewery lawn. Make it an early night."),
 ("Sunday: Lost Pines Golf Club", "sunday", ["lostpines"],
  "<strong>The nice one</strong>An Arthur Hills resort course in the pines east of the city, the treat after two days of munis."),
 ("Pack These", "pack", ["criquet","duffle","orms","magpie","sierra","palm"],
  "<strong>Six things that make the trip</strong>Four from Texas makers and two small things you will use all weekend. Prices read on each brand's own store on 2 October 2026."),
]
N = 15
PQ = {}
BANDS = {
 "saturday": ("Friday at Lions", "The course where Crenshaw and Kite learned the game.", [("band-dusk","Dusk over the fairways at Lions Municipal Golf Course","Dusk at Lions"),("band-hole16","The 16th hole at Lions Municipal","The 16th"),("band-hist-fairway","A historic photo of golfers on a Lions Municipal green","Lions, years ago")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>The best Austin golf weekend is two days of munis and one round that feels like a treat. Play Lions on Friday, where Austin golf began, and Roy Kizer on Saturday, the links-style muni that lets you swing. Then on Sunday head east to Lost Pines Golf Club, the Arthur Hills course at the resort near Bastrop, which the Dallas Morning News has named one of the best in Texas.</p>
    <p>Between rounds: a swim in Barton Springs, smoked brisket on South Lamar, breakfast tacos at 7am, a barbecue lunch from the Michelin Guide and records under Hotel Magdalena. Friday stays central, and Saturday stays in southeast Austin near Kizer, which also puts you on the right side of town for Sunday. Heads up: Saturday and Sunday tee times at the city munis open online at 8pm Central on the Monday before, and they go fast, so set an alarm for Kizer. You need a Golf ATX account, and each account can book one tee time for up to four players. Friday at Lions books on the normal weekday window.</p>
    <p>The two munis come to $85: $41 at Lions on a Friday and $44 at Kizer on the weekend. Lost Pines prices by the day, so check its tee sheet. We also picked six things to pack, four of them from Texas makers. The muni fees are the City of Austin's rates, read on 17 September 2026. Venue hours, pool prices and product prices were read on each one's own site on 2 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Weekend</div>
      <div class="sidebar-detail"><span class="l">Rounds</span><span>3 &middot; 54 holes</span></div>
      <div class="sidebar-detail"><span class="l">Courses</span><span>Lions Muni, Roy Kizer, Lost Pines Golf Club</span></div>
      <div class="sidebar-detail"><span class="l">Muni fees</span><span>$85 for two rounds</span></div>
      <div class="sidebar-detail"><span class="l">Lost Pines</span><span>Rates vary by day</span></div>
      <div class="sidebar-detail"><span class="l">Book Kizer</span><span>Monday, 8pm CT</span></div>
      <div class="sidebar-detail"><span class="l">Walk</span><span>Lions and Kizer</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Lions on Friday afternoon</span></div>
      <a href="/field-guide" class="sidebar-cta">The Austin Golf Field Guide &#8594;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#GolfWeekend</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
MORE = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="more-austin">Staying Longer?</h2>
  <p class="cat-kicker">Swap any stop for one from our other Austin guides: <a href="/drops/austin-food-truck-field-guide" style="border-bottom:1px solid currentColor;">15 food trucks</a>, <a href="/drops/austin-bbq-field-guide" style="border-bottom:1px solid currentColor;">the barbecue field guide</a>, <a href="/drops/the-morning-round-austin-cafes-and-lunch" style="border-bottom:1px solid currentColor;">caf&eacute;s before an early tee time</a>, <a href="/drops/date-night-after-36" style="border-bottom:1px solid currentColor;">date night after 36</a>, <a href="/drops/8-special-day-rounds-near-austin" style="border-bottom:1px solid currentColor;">special-day rounds near Austin</a> and, for a five-round version of this trip, <a href="/drops/austin-golf-road-trip" style="border-bottom:1px solid currentColor;">the Austin golf road trip</a>.</p>
</section>
"""
FAQ = [
 ("How much does this Austin golf weekend cost in green fees?", "The two munis come to $85: $41 for a Friday round at Lions Municipal and $44 for a weekend round at Roy Kizer, the City of Austin rates read on 17 September 2026. Lost Pines Golf Club prices by the day, so check its tee sheet when you book."),
 ("What is the best public golf course in Austin for a visitor?", "Lions Municipal. It opened in 1924, Ben Crenshaw and Tom Kite learned there, and it is central, walkable and scorable."),
 ("When do weekend tee times open at Austin's municipal golf courses?", "At 8pm Central on the Monday before, online only, for that Saturday and Sunday. You need a Golf ATX account, and each account can book one tee time for up to four players. Weekday tee times book on the usual schedule."),
 ("Where is Lost Pines Golf Club?", "At Lost Pines Resort, 575 Hyatt Lost Pines Road, near Bastrop, east of Austin. The resort puts it about 20 minutes from Austin."),
 ("Who designed Lost Pines Golf Club?", "Arthur Hills. It is a 7,300-yard, par-72 course, and the signature holes are the 603-yard par-5 3rd and the 155-yard downhill par-3 12th."),
 ("Can you swim at Barton Springs after golf?", "Yes. Barton Springs Pool is about ten minutes from Lions and is open 5am to 10pm every day except Thursday daytime. Adult admission was $9 for visitors and $5 for Austin residents on 2 October 2026."),
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
         "url": URL, "image": og, "datePublished": "2026-10-02", "dateModified": "2026-10-02",
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
            f'  <div class="drop-tag grass">{len(ids)} {("pick" if anchor=="pack" else "stop") + ("" if len(ids)==1 else "s")}</div>\n'
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Austin, Texas</span><span class="dot"></span>
    <span>3 rounds &middot; checked 2 October 2026</span><span class="dot"></span>
    <span>Hero photo courtesy of Lost Pines Resort</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A creek running through the oaks beside a fairway at Lost Pines Golf Club" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += MORE
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
