#!/usr/bin/env python3
"""build-atx-reservations.py — Austin's Hardest Reservations, 23 November 2026 (Field Notes).
Lenny: "Austins hardest reservations and how to book them. also add on Sammies italian" + his list:
Big Slick, Red Ash Italia, Aba, Este, Suerte, Tsuke Edomae, Toshokan, Paperboy, Uchi, Sammie's Italian.
FACTS: each restaurant's own site + live booking page, checked Nov 23, 2026 (research/atx-reservations/). Where the restaurant
doesn't publish its window or drop time we attribute The Infatuation's tracking by name (no link). No prices that can go stale
except published tasting/deposit figures. Images: restaurants' own sites; photo-less three get typographic cards. No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
SLUG = "austin-hardest-reservations-how-to-book"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/atx-reservations"
TITLE = "Austin's Hardest Reservations, and How to Actually Get In"
DESC = ("How to book Austin's ten hardest tables, from Tsuke Edomae and Toshokan to Big Slick, Red Ash, Sammie's Italian and Uchi: "
        "which app, when the window opens, and the walk-in backdoor at each. Checked November 23, 2026.")
H1 = "Austin&rsquo;s Hardest Reservations"
DEK = "Ten tables everyone wants, which app to use, when the window opens, and the backdoor at each one."

# key, name, area, platform, book_url, site, [imgs], what, (quote, who) or None, window, backdoor, good
E = [
 ("tsuke", "Tsuke Edomae", "Mueller", "Tock", "https://www.exploretock.com/tsukeedomae/", None,
  [("tsuke-1.jpg", "The Tsuke Edomae storefront in Mueller: a black panel with gold kanji and the unit number 1035"), ("tsuke-2.jpg", "A single piece of scored tuna nigiri on a dark board at Tsuke Edomae"), "Photos: Nicolai McCrary for The Infatuation"],
  "Edomae-style sushi omakase from Chef Mike, who trained in Ginza at Hakkoku under Hiroyuki Sato. 4600 Mueller Blvd. The Infatuation calls it easily the toughest table in town.",
  None,
  "Tock, in batches. Tsuke doesn&rsquo;t publish a schedule; The Infatuation tracks the drops at roughly twice a year, usually a Sunday at 9am, announced on Instagram at @tsuke_edomae.",
  "There isn&rsquo;t one. Follow the Instagram, set an alarm, and be logged into Tock with a card saved before the drop. When we checked, every date read &ldquo;All reservations sold out.&rdquo;",
  "Parties of two. Tock takes a $145-per-person deposit, plus fees, at booking."),
 ("toshokan", "Toshokan", "East Austin", "Tock", "https://www.exploretock.com/toshokan/", "https://www.toshokanatx.com/",
  [("toshokan-1.jpg", "Toshokan&rsquo;s dark brick room with a long live-edge counter and candles on the shelves"), ("toshokan-2.jpg", "Salmon nigiri being finished with tweezers at Toshokan"), "Photos: Toshokan"],
  "A 14-course omakase for six diners at a time from Chef Saine Wong, at 807 E 4th St. The Michelin Guide recommends it and places it inside Holey Moley, the mini golf bar, hidden behind a wall lined with books. Dinner, then nine holes.",
  None,
  "Tock. Toshokan announces drops on Instagram (@toshokanatx) and to its newsletter, which promises &ldquo;priority announcements, reservation drops.&rdquo; The Infatuation reports seats open on the 1st of the month, usually at midnight.",
  "Refresh. The Infatuation says stray seats come back about ten minutes after a drop, when unpaid carts expire.",
  "Two seatings, 6:00 and 8:30pm, for parties of one to six. A card hold is required; cancel inside 48 hours and Toshokan charges $180 per person plus a 20% service charge unless the seat is refilled. Tock lists it at $170&ndash;$180 per person."),
 ("bigslick", "Big Slick", "East 6th", "SevenRooms", "https://www.sevenrooms.com/explore/bigslick/reservations/create/search/?party_size=2", "https://www.scratchrestaurants.com/bigslick",
  [("bigslick-1.jpg", "A carved tomahawk steak on a silver platter at Big Slick"), ("bigslick-2.jpg", "A corner of Big Slick&rsquo;s dining room with a wall of wine, grey chairs and a red curtain"), "Photos: Richard Casteel for The Infatuation (steak); Jasmin Porter for CultureMap Austin (room)"],
  "A 22-seat steakhouse and bar from Michelin-starred chefs Phillip Frankland Lee and Margarita Kallas-Lee, open since the end of August. Fire-cooked and &agrave; la carte.",
  ("Guests enter through an unmarked door on East 6th Street, ringing a bell before being welcomed into a candlelit bar.", "Big Slick"),
  "SevenRooms. Big Slick doesn&rsquo;t publish its window; The Infatuation reports reservations open 60 days out and disappear in about five minutes.",
  "The bar. Big Slick&rsquo;s own site: &ldquo;Walk-ins accepted at the bar on a first come, first served basis.&rdquo; The Infatuation says the bar serves the full menu and suggests lining up 20 to 30 minutes before the 5pm open.",
  "Wednesday to Sunday only. Dining room 5:30&ndash;10pm; the bar runs to midnight, and 1am on Fridays and Saturdays."),
 ("redash", "Red Ash Italia", "Downtown", "OpenTable", "https://www.opentable.com/r/red-ash-italia-reservations-austin?restref=214576", "https://www.redashgrill.com/",
  [("redash-1.jpg", "Red Ash agnolotti with crisp sage and shaved cheese"), ("redash-2.jpg", "Red Ash grilled octopus in a white bowl with a glass of ros&eacute;")],
  "Wood-fired Italian from owner and executive chef John Carver, on the second floor of Colorado Tower. It reopened in 2024 after a fire, and has been hard to get into ever since.",
  None,
  "OpenTable. Red Ash doesn&rsquo;t publish its window; The Infatuation reports booking opens six months out, with prime times gone about four months ahead.",
  "Pick up the phone. Red Ash&rsquo;s own site: &ldquo;Please call us if you do not see the reservation time that you would like.&rdquo; Hosts call back within 24 hours.",
  "Dinner nightly, 5&ndash;10pm. Call for parties of eight or more. The house asks for &ldquo;Proper Attire, please&rdquo; &mdash; no athletic wear."),
 ("sammies", "Sammie&rsquo;s Italian", "West 6th", "Sammie&rsquo;s own site", "https://sammiesitalian.com", "https://sammiesitalian.com",
  [("sammies-1w.jpg", "Sammie's spaghetti and meatballs on a white plate against a dark red banquette")],
  "Old-school red-sauce Italian from MML Hospitality at 807 W 6th St, with a long bar, a back room called Mildred&rsquo;s Room and a patio.",
  None,
  "Only through Sammie&rsquo;s own website; OpenTable lists it as not bookable there. Sammie&rsquo;s doesn&rsquo;t publish how far ahead tables open, so check the site often.",
  "Friday lunch. It is the only daytime service Sammie&rsquo;s runs, noon on Fridays.",
  "Tue&ndash;Wed 5&ndash;11pm; Thu and Sat 5pm&ndash;midnight; Fri noon&ndash;midnight; Sun&ndash;Mon 5&ndash;10pm. Valet out front. The online book takes parties up to 20."),
 ("uchi", "Uchi", "South Lamar", "SevenRooms", "https://www.sevenrooms.com/explore/uchiaustin/reservations/create/search?venues=uchikoaustin,uchiaustin,uchibaaustin", "https://uchi.uchirestaurants.com/location/sushi-austin/",
  [("uchi-1.jpg", "Uchi's hama chili: yellowtail with ponzu, chili and orange"), ("uchi-2.jpg", "The original Uchi, a converted house on South Lamar, lit up at dusk")],
  "Tyson Cole&rsquo;s James Beard-winning original, in a converted house on South Lamar for more than 20 years.",
  ("We accept reservations and welcome walk-ins. Patio seating is available weather permitting.", "Uchi Austin"),
  "SevenRooms, in a shared book with Uchiko and Uchiba. Uchi doesn&rsquo;t publish its window; The Infatuation says one month out.",
  "Happy hour, every day 4&ndash;6pm, with a walk-in welcome. It includes a nine-course happy-hour omakase for two at $120. The Infatuation says showing up at open often lands a bar seat.",
  "Sun&ndash;Thu 4&ndash;10pm; Fri&ndash;Sat 4&ndash;11pm. Large parties call 512-916-4808."),
 ("suerte", "Suerte", "East 6th", "Resy", "https://www.suerteatx.com/reserve-table/", "https://www.suerteatx.com/",
  [("suerte-1.jpg", "Suerte's dining room: white chairs, wooden tables and a long banquette"), ("suerte-2.jpg", "A shelf at Suerte with a framed agave print, a weathered round plate and a jar of dried chiles")],
  "Masa-first Mexican from chef Ferm&iacute;n N&uacute;&ntilde;ez at 1800 E 6th St.",
  ("Our booking window opens up 30 days in advance at midnight via Resy.", "Suerte&rsquo;s FAQ"),
  "Resy, 30 days out at midnight. It is the only restaurant on this list that publishes its exact drop time, so use it.",
  "Suerte says it always saves &ldquo;a portion of our seating for walk-in guests at our bar, in our dining room, and outdoors.&rdquo; Peak waits run 15 minutes to an hour and a half, and they text you when the table is ready.",
  "Lucky Hour Mon&ndash;Fri 5&ndash;6pm and Sat&ndash;Sun 3&ndash;5pm. Online bookings take parties of eight or nine depending on the page; ten or more book the semi-private room."),
 ("este", "Este", "Manor Road", "OpenTable", "https://www.opentable.com/r/este-austin", "https://www.esteatx.com/",
  [("este-1.jpg", "Este's ceviche with avocado and herbs on a white plate"), ("este-2.jpg", "Este's dining room under a white wooden ceiling")],
  "Mexican seafood from Ferm&iacute;n N&uacute;&ntilde;ez and Sam Hellman-Mass, the Suerte team, at 2113 Manor Rd.",
  None,
  "OpenTable, up to 30 days in advance for the dining room and covered patio, per Este&rsquo;s own reservations page. The release time isn&rsquo;t published.",
  "Este says it always saves &ldquo;a portion of our seating for walk-in guests including our bar, chef&rsquo;s counter, and lounge.&rdquo; Check in with the host in person. Or go to lunch, Friday to Sunday, noon to 4.",
  "Dinner daily 5&ndash;10pm; happy hour Mon&ndash;Thu 5&ndash;6pm and Fri&ndash;Sun noon&ndash;5pm. Free valet. Up to eight online; ten or more is a private event. Tables are held for 15 minutes."),
 ("aba", "Aba", "South Congress", "OpenTable", "https://www.opentable.com/r/aba-austin-reservations-austin?restref=1280941", "https://www.abarestaurants.com/austin",
  [("aba-1.jpg", "An overhead spread of Aba's Mediterranean dishes: hummus, falafel and salads"), ("aba-2.jpg", "Aba's tree-shaded patio on South Congress")],
  "Mediterranean with a California accent from chef CJ Jacobson, on South Congress, with one of the best patios in town.",
  ("All three of our bars offer full-service dining and walk-up diners&hellip; just snag an open chair.", "Aba Austin"),
  "OpenTable, 60 days in advance for groups up to eight, per Aba&rsquo;s own reserve page. Regular reservations are indoor only.",
  "The patio and the bars. Outdoor tables are first come, first served, and all three bars serve the full menu. You have to check in at the host stand in person; they won&rsquo;t take your name over the phone.",
  "Weekday lunch 11am&ndash;4pm; weekend brunch 10am&ndash;3pm; dinner nightly. Closed Thanksgiving Day."),
 ("paperboy", "Paperboy", "East 11th &amp; South Lamar", "OpenTable", "https://www.opentable.com/r/paperboy-austin", "https://www.eatpaperboy.com/",
  [("paperboy-1.jpg", "A Paperboy brunch spread: pancakes with blueberries, bacon, toast and a cocktail"), ("paperboy-2.jpg", "An overhead Paperboy table with toast, kale salad and coffee")],
  "All-day brunch from Daybreak Hospitality Group that started as a food truck in 2015, now on East 11th and South Lamar. The only breakfast on the list.",
  ("Reservations can be made via OpenTable for groups of up to 10 guests. We also hold plenty of walk-in space for walk-in guests every day!", "Paperboy"),
  "OpenTable. The Infatuation reports bookings open on the 1st of the month, on a rolling two-month basis.",
  "Walk in, and go late. The Infatuation puts weekend waits at one to two hours and says a 2pm table is much easier than a 10am one.",
  "Mon&ndash;Thu 8am&ndash;2pm; Fri&ndash;Sun 8am&ndash;3pm."),
]

CSS = ('<style>/*TGI-RESERVATIONS v1*/'
       '.rs-tbl{width:100%;border-collapse:collapse;margin:8px 0 0;font-size:15px}.rs-tbl th{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;opacity:.65;padding:10px 12px;border-bottom:.5px solid var(--ink)}'
       '.rs-tbl td{padding:12px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top;line-height:1.45}.rs-tbl td:first-child{font-family:var(--serif);font-size:18px;white-space:nowrap}.rs-tbl a{border-bottom:none;text-decoration:none;color:inherit}'
       '.em{padding-top:0!important;padding-bottom:0!important}.em-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;padding:56px 0;border-top:.5px solid rgba(20,20,20,.25)}'
       '.em-row.flip .em-imgs{order:2}.em-imgs{display:grid;grid-template-columns:1fr 1fr;gap:8px}.em-imgs.one{grid-template-columns:1fr}.em-imgs img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#E8E2D6}.em-imgs.one img{aspect-ratio:4/3}'
       '.em-who{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:10px}'
       'section.products.em .em-txt h2{font-family:var(--serif);font-weight:400;font-size:clamp(34px,4vw,50px);line-height:1;letter-spacing:-.01em;margin:0 0 16px!important;text-align:left!important}'
       '.em-txt p{font-size:17px;line-height:1.62;margin:0 0 14px}.em-txt a{border-bottom:1px solid currentColor}'
       '.em-q{font-family:var(--serif);font-size:22px;line-height:1.35;color:#2D4A2B;margin:6px 0 18px;padding:2px 0 2px 18px;border-left:2px solid #2D4A2B}.em-q cite{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2D4A2B;opacity:.75;margin-top:10px}'
       '.rs-dl{margin:4px 0 14px;border-top:.5px solid rgba(20,20,20,.2)}.rs-dl div{display:grid;grid-template-columns:110px 1fr;gap:14px;padding:11px 0;border-bottom:.5px solid rgba(20,20,20,.2)}'
       '.rs-dl dt{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2D4A2B;padding-top:4px}.rs-dl dd{margin:0;font-size:15.5px;line-height:1.55}'
       '.rs-cred{grid-column:1/-1;font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin:4px 0 0}.em-links{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;display:flex;gap:18px;flex-wrap:wrap}'
       '.em-pq{font-size:clamp(24px,2.6vw,30px)!important;margin:22px 0!important;padding:4px 0 4px 22px!important}'
       '.drop-tag.grass{background:none!important;color:#2D4A2B!important;border:0!important;padding:0!important;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.75}'
       '.rs-cap{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:clamp(26px,3.6vw,40px);line-height:1.05;text-align:center!important;color:#2D4A2B}'
       '@media(max-width:820px){.em-row{grid-template-columns:1fr;gap:20px;padding:40px 0}.em-row.flip .em-imgs{order:0}.rs-dl div{grid-template-columns:1fr;gap:4px}.rs-tbl td:first-child{white-space:normal}.rs-tbl .hide-m{display:none}}'
       '</style>\n')


def entry(i, e):
    k, name, area, plat, book, site, imgs, what, quote, window, back, good = e
    cred = imgs[-1] if isinstance(imgs[-1], str) else ""
    imgs = [x for x in imgs if not isinstance(x, str)]
    im = "".join(f'<img src="{IMG}/{f}" alt="{a}" loading="lazy" />' for f, a in imgs)
    if cred: im += f'<p class="rs-cred">{cred}</p>'
    q = f'<blockquote class="em-q">&ldquo;{quote[0]}&rdquo;<cite>{quote[1]}</cite></blockquote>' if quote else ""
    links = f'<a href="{book}" target="_blank" rel="noopener">Book on {plat} &#8599;</a>' if not book.startswith("https://sammies") else f'<a href="{book}" target="_blank" rel="noopener">Book on Sammie&rsquo;s site &#8599;</a>'
    if site and site != book:
        links += f'<a href="{site}" target="_blank" rel="noopener">Website &#8599;</a>'
    dl = (f'<dl class="rs-dl"><div><dt>How to book</dt><dd>{window}</dd></div><div><dt>The backdoor</dt><dd>{back}</dd></div>'
          f'<div><dt>Good to know</dt><dd>{good}</dd></div></dl>')
    flip = " flip" if i % 2 == 0 else ""
    return (f'\n<section class="products em" id="{k}">\n'
            f'  <div class="em-row{flip}"><div class="em-imgs{" one" if len(imgs) == 1 else ""}">{im}</div>'
            f'<div class="em-txt"><div class="em-who">{area}</div><h2>{name}</h2><p>{what}</p>{q}{dl}<div class="em-links">{links}</div></div></div>\n</section>\n')


CHEAT = {  # short cells for the cheat sheet; every cell restates something in the entry below
 "tsuke": ("Tock", "Twice a year, Sunday 9am*", "None. Watch Instagram"),
 "toshokan": ("Tock", "1st of the month, midnight*", "Refresh ~10 min after the drop"),
 "bigslick": ("SevenRooms", "60 days*", "Bar is walk-in"),
 "redash": ("OpenTable", "6 months*", "Call the host stand"),
 "sammies": ("Own site", "Not published", "Friday lunch"),
 "uchi": ("SevenRooms", "1 month*", "Happy hour, 4&ndash;6pm daily"),
 "suerte": ("Resy", "30 days, midnight", "Bar, dining room and patio walk-ins"),
 "este": ("OpenTable", "30 days", "Bar, chef&rsquo;s counter, lounge; weekend lunch"),
 "aba": ("OpenTable", "60 days", "Patio and all three bars"),
 "paperboy": ("OpenTable", "1st of the month, 2 months out*", "Walk in, and go late"),
}


def cheat():
    rows = "".join(f'<tr><td><a href="#{e[0]}">{e[1]}</a></td><td>{CHEAT[e[0]][0]}</td><td>{CHEAT[e[0]][1]}</td><td class="hide-m">{CHEAT[e[0]][2]}</td></tr>' for e in E)
    return ('\n<section class="products" id="cheat-sheet" style="padding-top:36px">\n  <div class="drop-tag grass" style="text-align:center">The Cheat Sheet</div>\n'
            '  <h2 class="products-hdr rs-cap">Who Books Where</h2>\n'
            f'  <table class="rs-tbl"><thead><tr><th>Restaurant</th><th>Books on</th><th>Window opens</th><th class="hide-m">The backdoor</th></tr></thead><tbody>{rows}</tbody></table>\n'
            '  <p style="font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:10px">* Not published by the restaurant; reported by The Infatuation. Everything else is from the restaurant&rsquo;s own site or booking page, checked November 23, 2026.</p>\n</section>\n')


RELATED = [
 ("/drops/the-lottery-round-austin-private-clubs", "The Lottery Round", "The other hard booking in Austin: how to get on a private course."),
 ("/drops/date-night-vol-2-austin-restaurants-for-reconnecting", "Date Night, Vol. 2", "Austin restaurants for actually talking to each other."),
 ("/drops/best-steakhouses-in-austin", "Austin&rsquo;s Best Steakhouses", "For when Big Slick is full."),
 ("/drops/the-morning-round-austin-cafes-and-lunch", "The Morning Round", "Cafés before the tee, lunch after. No reservations needed."),
]


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-23", "dateModified": "2026-11-23",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": [
            {"@type": "ListItem", "position": i, "name": H.unescape(e[1]), "url": f"{URL}#{e[0]}"} for i, e in enumerate(E, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Austin's Hardest Reservations", "item": URL}]},
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
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""




def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    side = "\n".join(f'      <div class="sidebar-detail"><span class="l">{e[2]}</span><span><a href="#{e[0]}" style="border-bottom:none">{e[1]}</a></span></div>' for e in E)
    rel = "".join(f'<li style="padding:10px 0;border-bottom:.5px solid rgba(20,20,20,.2)"><a href="{u}">{t}</a> &mdash; {d_}</li>' for u, t, d_ in RELATED)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Austin&rsquo;s Hardest Reservations</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 23, 2026</p><!--/TGI-BY-->
  <p style="font-size:20px;font-style:italic;max-width:680px;margin:10px auto 0">{DEK}</p>
  <div class="drop-meta">
    <span>Field Note</span><span class="dot"></span>
    <span>10 restaurants &middot; booking rules checked November 23, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The long bar at Sammie's Italian on West 6th, lit low under a painted mural" fetchpriority="high" /></div></div>

<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Golfers already know how this works. The good tee times go the minute the sheet opens, the people who get them set alarms, and everyone else learns where the walk-on slots are. <strong>Austin&rsquo;s best restaurants now run on exactly the same logic.</strong> We have written before about <a href="/drops/the-lottery-round-austin-private-clubs">getting onto the courses you can&rsquo;t book</a>; this is the dinner version.</p>
    <p><strong>Every one of these places has a system, and most of them tell you what it is.</strong> Some open 30 days out, some 60, one six months. One drops its seats twice a year on Instagram. And several hold back part of the room for whoever walks in: the bar, the patio, a chef&rsquo;s counter. They say so on their own websites, but the booking apps don&rsquo;t mention it.</p>
    <blockquote class="em-q em-pq">Six of these ten restaurants keep seats open for people who just walk in. The app never tells you that.</blockquote>
    <p><strong>So for each of the ten, we read it.</strong> Which app it books on, how far ahead the window opens and at what time, what the deposit and cancellation rules are, and the backdoor: the bar, the patio, the lunch service or the phone call that gets you in when the app says no.</p>
    <p>Everything below comes from each restaurant&rsquo;s own site or live booking page, checked on November 23, 2026. Where a restaurant doesn&rsquo;t publish its window or drop time, we say whose number it is: usually The Infatuation, which tracks these drops closely. Rules change, so check before you set the alarm.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Ten &middot; hardest first</div>
{side}
    </div>
  </aside>
</section>
"""
    body += ('\n<section class="products" id="the-ten" style="padding-top:48px;padding-bottom:8px">\n'
             '  <div class="drop-tag grass" style="text-align:center">The Ten</div>\n'
             '  <h2 class="products-hdr rs-cap">Hardest First</h2>\n'
             '  <p style="max-width:720px;margin:12px auto 0;text-align:center;font-size:18px;line-height:1.6">We start with the two omakase counters that only open a few seats at a time and work down to Paperboy, where a little patience usually gets you a table. Each one has the same three notes: <strong>how to book</strong>, <strong>the backdoor</strong> for when the app says no, and the <strong>good to know</strong> details like deposits, party sizes and hours.</p>\n'
             '</section>\n')
    for i, e in enumerate(E, 1):
        body += entry(i, e)
    body += f"""
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr rs-cap" id="last-word">Show Up</h2>
    <p>The apps reward speed, but almost every room on this list still saves seats for the people who walk through the door. Go early, go on a weeknight, sit at the bar, and be nice to the host. That gets you into more of these than any alarm will.</p>
    <p>If we got a rule wrong or a restaurant changes how it books, <a href="/work-with-us">tell us</a>.</p>
    <div class="drop-tag grass" style="margin-top:34px">More Austin</div>
    <ul style="list-style:none;padding:0;margin:10px 0 0;font-size:17px">{rel}</ul>
  </div>
</section>
"""
    if apply_:
        pass
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Mackem"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html · {len(E)} restaurants")


if __name__ == "__main__":
    main("--apply" in sys.argv)
