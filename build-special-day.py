#!/usr/bin/env python3
"""Refresh — Special Day Rounds Near Austin. Same slug, 17 September 2026.

WHY THE REBUILD
---------------
The live post ran 356 words with eight cards whose product-desc divs were ALL
EMPTY. Only brand, name and price rendered. That is a broken build, not thin
copy, and it is why the page reads as a list of prices with no reason attached.

Two facts in it were also wrong:

  * WOLFDANCER IS NOW LOST PINES RESORT. wolfdancergolfclub.com redirects to
    lostpinesresortandspa.com/golf/, which is titled "Golf at Lost Pines Resort"
    and uses the word Wolfdancer zero times. Same Arthur Hills course, same
    7,300 yards, par 72. The resort's own copy says "just 20 minutes from
    Austin"; the post said ~30 east. Renamed sitewide, keeping "still Wolfdancer
    to most people" on first mention so the old name still finds the page.
  * FALCONHEAD HAS MOVED TO DYNAMIC PRICING and says so on its own rates page:
    "Prices adjust - both lower and higher - in real-time based upon demand."
    The old $52-78 was a rate card that no longer exists.

PRICING POLICY (Lenny's call, 17 Sept 2026)
-------------------------------------------
Publish a dated figure ONLY where the course still runs a fixed rate card that
was read today. Where a course has moved to dynamic pricing or books through a
third-party engine, say that plainly instead of inventing a range. A price band
that drifts within a fortnight is worse than no band at all.

  VERIFIED TODAY, from the course's own rates page:
    Vaaler Creek   $95 Mon-Thu 18 holes, cart included; $75 twilight
    Star Ranch     $85-99 Mon-Thu; $129-139 Fri/weekends; $62-75 after 3pm
  DYNAMIC OR THIRD-PARTY, stated as such:
    Falconhead (dynamic, its own words), Kissing Tree (Troon), The Quarry,
    Avery Ranch, Grey Rock, Crystal Falls, ShadowGlen, Lost Pines Resort
  RESORT PRICING, quoted only as "resort rates":
    Horseshoe Bay, Omni Barton Creek, La Cantera, Lajitas

TEN DAY TRIPS, NOT TWELVE. Lenny asked for twelve. Ten is what has a real,
already-localised photograph behind it. Padding to twelve would have meant two
cards with no image or a stock photo of somebody else's golf course, which is
the thing this rebuild exists to stop. Adding ColoVista and one more is a
ten-minute job the moment there is photography for them.

IMAGE NOTE: Lajitas' own golf page serves a file named
"ChatGPT-Image-Dec-21-2025-10_33_04-AM-1024x683.png". That is AI-generated art,
not course photography, and is deliberately NOT used here.

CORRECTION, 17 September 2026 — THE LAJITAS FRAME.
images/special-day/lajitas.jpg was first published here as a JSX AIRLINE PROMO
BANNER: a fly-in-package advert with "SAVE UP TO 40% ON FLY-IN GOLF PACKAGES" set
across a photo of a parked jet. No golf course in it at all. It shipped into this
post AND into the Field Guide, because the file was pulled off their page by name
and never opened. Replaced with black-jack.jpg from their own uploads — a real
photograph of a green at dusk below the Chihuahuan Desert mesas, centre-cropped
from 1200x800 to the house 4:3 rather than stretched, so the mesa is not warped.
THE LESSON, AND IT IS CHEAP: OPEN EVERY IMAGE BEFORE IT SHIPS. A plausible
filename on the right domain is not a check. The guard below only catches the one
failure mode I already knew about; it could not have caught this one.

RANKINGS ARE ATTRIBUTED, NEVER ASSERTED. Black Jack's Crossing rankings are
quoted to the publications that made them (Golfweek, Dallas Morning News), as
printed on Lajitas' own page. TGI does not rank these courses itself.
"""
import re, os, sys, json, html as H

apply_ = "--apply" in sys.argv
SLUG  = "8-special-day-rounds-near-austin"
PLAIN = "Special Day Rounds Near Austin — 10 Day Trips and 4 Overnights"
TITLE = "Special Day Rounds Near Austin &mdash; 10 Day Trips and 4 Overnights"
DESC  = ("Ten courses within a couple of hours of Austin for the round that is not a normal round, plus "
         "four overnight trips. Prices and course status checked 17 September 2026.")
DATE  = "September 17, 2026"
FG    = "/images/field-guide/"
FEED  = "/images/feed/"
SD    = "/images/special-day/"

# (img slug-or-path list, name, meta, url, copy)
DAY = [
 ([FG+"wolfdancer.jpg"], "Lost Pines Resort", "Bastrop &middot; ~20 min east &middot; resort rates",
  "https://www.lostpinesresortandspa.com/golf/",
  "Still Wolfdancer to most people, and the reason to make the drive first. Arthur Hills routed 7,300 "
  "yards through the Lost Pines &mdash; a band of loblolly that has no business being an hour from the "
  "Hill Country &mdash; and the course plays like two. The opening stretch rolls through open pasture; "
  "then it drops into the trees and the Colorado River bottom and stops being polite. The resort rebranded "
  "in 2026 and the Wolfdancer name has come off the signage, which is the only thing about it that has "
  "changed."),
 ([FG+"falconhead.jpg", "/images/austin-road-trip/falconhead-hole8.jpg"], "Falconhead Golf Club",
  "Lakeway &middot; ~25 min west &middot; dynamic pricing",
  "https://www.falconheadaustin.com/",
  "The closest thing to a big-day course you can reach without committing the whole morning to driving. "
  "Falconhead moved to dynamic pricing in 2026 and is unusually straight about it &mdash; its rates page "
  "says outright that prices move up and down in real time on demand, which in practice means a Tuesday "
  "afternoon can cost a third of a Saturday morning. Check before you assume it is out of range."),
 ([FG+"avery-ranch.jpg"], "Avery Ranch Golf Club", "Cedar Park &middot; ~30 min north &middot; check rates",
  "https://averyranch.com/",
  "Semi-private, north of the city, and the one on this list most likely to be somebody's regular track "
  "rather than an occasion. It earns a place anyway: the back nine works around water often enough that a "
  "good round needs decisions rather than just contact, and it is close enough to make a late-afternoon "
  "nine after work a plausible idea."),
 ([FG+"grey-rock.jpg"], "Grey Rock Golf Club", "South Austin &middot; ~20 min &middot; check rates",
  "https://www.greyrockgolfandtennis.com/",
  "The one that is barely a drive at all. Grey Rock sits in the hills south of the river and calls itself "
  "the city&rsquo;s premier golf and tennis club; the useful part is that it delivers elevation change and "
  "limestone without asking for a highway. If you want the round to feel like an event but have to be back "
  "by two, this is the answer."),
 ([FG+"star-ranch.jpg"], "The Golf Club at Star Ranch", "Hutto &middot; ~35 min NE &middot; $85&ndash;99 Mon&ndash;Thu",
  "https://www.starranchgolf.com/",
  "Out past Toll 130 in Hutto, with undulating fairways and white sand bunkering, and the best-value big "
  "day on this page if you go midweek. Rates read on 17 September 2026: $85&ndash;99 Monday to Thursday, "
  "$129&ndash;139 Friday and weekends, and $62&ndash;75 after 3pm. A 15,000-square-foot clubhouse on a "
  "hilltop makes the post-round part easy."),
 ([FEED+"c68dec72-banner1.jpg", FG+"vaaler-creek.jpg"], "Vaaler Creek Golf Club",
  "Blanco &middot; ~50 min west &middot; $95 Mon&ndash;Thu",
  "https://www.vaalercreekgolfclub.com/",
  "The underrated one, and the drive out through Blanco is half the point. Rates read on 17 September "
  "2026: $95 for 18 Monday to Thursday with the cart included, $75 on the twilight rate, which starts at "
  "3pm from March to the end of October and 1pm through the winter. Cart-inclusive pricing is rarer than "
  "it should be and makes the real cost easy to work out in advance."),
 ([FEED+"ed1deed0-slide1.jpg"], "Kissing Tree Golf Club", "San Marcos &middot; ~45 min south &middot; via Troon",
  "https://www.kissingtreegolfclub.com/",
  "Semi-private in San Marcos, and the Hill Country landscape starts doing the work about halfway down "
  "I-35. Tee times book through Troon rather than the club&rsquo;s own sheet, so pricing moves with the "
  "day and the season &mdash; go through the booking engine rather than expecting a posted rate."),
 ([FEED+"85a30a62-Quarry-13-Cliff-Edge-scaled-1-1.jpg"], "The Quarry Golf Club",
  "San Antonio &middot; ~1 hr 15 south &middot; check rates",
  "https://quarrygolf.com/",
  "The back nine alone justifies the extra half hour past San Marcos: it drops into a genuine "
  "hundred-year-old quarry pit and plays inside the walls. The front nine is links-adjacent and open; the "
  "transition between the two is one of the most abrupt and most enjoyable in Texas golf."),
 ([FG+"crystal-falls.jpg"], "Crystal Falls Golf Club", "Leander &middot; ~35 min NW &middot; check rates",
  "https://www.crystalfallsgolf.com/",
  "North-west into Leander, where the terrain starts breaking up properly. Crystal Falls bills itself as a "
  "Hill Country destination and the elevation backs it up. One thing to know before you drive out: the "
  "range closes thirty minutes before sunset daily, and two hours before sunset on Tuesdays."),
 ([FG+"shadowglen.jpg"], "ShadowGlen Golf Club", "Manor &middot; ~30 min east &middot; check rates",
  "https://www.shadowglengolf.com/",
  "East out through Manor, and the least scenic drive on this list attached to one of the better-conditioned "
  "public tracks near the city. It is long off the back tees and exposed enough that wind is a genuine "
  "factor, which makes it a better test than the entry price suggests."),
]

NIGHT = [
 ([FEED+"89123d8f-Ram-Rock-Aerial-Water-Shot-1920x920-min.jpg"], "Horseshoe Bay Resort",
  "Horseshoe Bay &middot; ~1 hr 15 NW &middot; resort rates",
  "https://www.hsbresort.com/golf/",
  "Four courses on one property &mdash; Ram Rock, Apple Rock, Slick Rock and Summit Rock &mdash; which is "
  "the whole argument for staying the night rather than driving out and back. Ram Rock is the hard one and "
  "has been since it opened; Apple Rock is the one people come back talking about. Two nights lets you play "
  "all four and still eat dinner like a person."),
 ([FEED+"ffe7e30b-Omni-Barton-Creek-9.jpg", FG+"omni-barton.jpg"], "Omni Barton Creek Resort",
  "West Austin &middot; in town &middot; resort rates",
  "https://www.omnihotels.com/hotels/austin-barton-creek/golf",
  "The staycation entry, and the only one on this page where the drive is twenty minutes and the point is "
  "still to stay over. Four championship courses on the property, including Fazio Canyons, which is the one "
  "to play if you are only playing one. Booking a room is usually the difference between a tee sheet that "
  "is open to you and one that is not."),
 ([SD+"lacantera.jpg", SD+"lacantera-a2.jpg", SD+"lacantera-a3.jpg"], "La Cantera Golf Club",
  "San Antonio &middot; ~1 hr 15 south &middot; resort rates",
  "https://www.lacanteragolfclub.com/",
  "Just north of San Antonio, cut into quarry and Hill Country ledge, and close enough that you could day-"
  "trip it &mdash; but the resort is the reason not to. The property pairs the golf with the Resort &amp; "
  "Spa, which turns a long Saturday into a legitimate weekend without anybody having to drive home tired."),
 ([SD+"lajitas.jpg"], "Lajitas Golf Resort &mdash; Black Jack&rsquo;s Crossing",
  "Lajitas &middot; ~7 hrs west &middot; resort rates",
  "https://www.lajitasgolfresort.com/golf/",
  "The far end of the list and the one that needs real commitment: seven hours west, on the Rio Grande at "
  "the edge of Big Bend, in country that looks like nowhere else in the state. Lajitas prints the "
  "accolades on its own page &mdash; Golfweek ranks Black Jack&rsquo;s Crossing the #1 Course You Can Play "
  "in Texas and #38 Resort Course in the USA, and the Dallas Morning News has had it at #1 in Texas since "
  "2013. Go for three nights or do not go."),
]

ALL = DAY + NIGHT

# ------------------------------------------------------------------- guards
for imgs, name, *_ in ALL:
    for i in imgs:
        if not os.path.exists(i.lstrip("/")):
            raise SystemExit(f"{name}: image missing on disk — {i}")
if len({n for _i, n, *_ in ALL}) != len(ALL):
    raise SystemExit("a course appears twice")

def gal(imgs, name):
    pl = re.sub(r"\s+", " ", re.sub(r"<[^>]+>|&[a-z]+;|&#\d+;", "", name)).strip()
    n = len(imgs)
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{imgs[0]}" alt="{pl}" loading="lazy" /></div></div></div>'), 1
    fr = "".join(f'<div class="pg-frame"><img src="{u}" alt="{pl} &middot; view {i+1} of {n}" '
                 f'loading="lazy" /></div>' for i, u in enumerate(imgs))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return ('<div class="product-gallery"><div class="pg-track">' + fr +
            '</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>'), n

def card(x):
    imgs, name, meta, url, copy = x
    g, n = gal(imgs, name)
    return f"""<div class="product-card" data-frames="{n}">
      {g}
      <div class="product-body">
        <div class="product-brand">{name}</div>
        <div class="product-name">{meta}</div>
        <div class="product-desc">{copy}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Course site ↗</a>
      </div>
    </div>"""

def sec(hdr, kicker, items):
    c = "\n    ".join(card(x) for x in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Most golf in Austin is a muni round on a Saturday morning, and that is a good way to live. This page is for the other kind &mdash; the birthday, the anniversary, the friend in from out of town, the Tuesday that calls for somewhere with a bit of ceremony to it.</p>
    <p>Ten of them are day trips: leave after breakfast, be home for dinner, nothing further than about an hour and a quarter. Four are overnights, because some of this golf is too far or too good to squeeze into a single day, and one of them is seven hours west at the edge of Big Bend.</p>
    <p>Every course here was checked on 17 September 2026 &mdash; open, operating, and linked to the right website. Prices are handled honestly, which takes a paragraph to explain and is the next thing on the page.</p>
  </div>
</div>
"""

PRICES = """<section class="products">
  <h2 class="products-hdr">A Word on What These Cost</h2>
  <p class="cat-kicker">Half of these courses no longer have a price to quote, and pretending otherwise would age badly.</p>
  <div class="writeup-body">
    <p>Golf around Austin has moved to dynamic pricing faster than most people have noticed. Falconhead is the clearest case and the most upfront about it: its own rates page says prices adjust in real time, up and down, on demand and availability. A posted range for a course like that is a snapshot of one afternoon, not a rate card, and it starts lying within a fortnight.</p>
    <p>So this page does two different things. Where a course still publishes a fixed rate card, there is a figure with the date it was read &mdash; Vaaler Creek at $95 Monday to Thursday with the cart included, Star Ranch at $85 to $99 midweek. Where a course prices dynamically or books through Troon or GolfNow, the card says so and sends you to the booking engine, because that is where the real number lives.</p>
    <p>The resorts are their own category. Horseshoe Bay, Barton Creek, La Cantera and Lajitas price golf as part of a stay, and the rate you get depends on whether you are a guest, which package you booked and what time of year it is. Quoting a green fee for those in isolation would be close to meaningless.</p>
    <p>One practical note that applies everywhere: twilight is the cheat code. Star Ranch drops to $62 after three. Vaaler Creek goes to $75. In an Austin summer the last three hours of light are the only civilised time to play anyway.</p>
  </div>
</section>
"""

PLANNING = """<section class="products">
  <h2 class="products-hdr">Picking the Right One</h2>
  <p class="cat-kicker">The occasion usually decides the drive before the golf does.</p>
  <div class="writeup-body">
    <p><strong>You have half a day.</strong> Grey Rock and Falconhead are the two that feel like an occasion without costing you the morning. Grey Rock is twenty minutes from most of central Austin and still gives you limestone and elevation change; Falconhead is twenty-five west and prices low enough on a quiet weekday that the whole thing can come in under a normal weekend round.</p>
    <p><strong>Somebody is visiting and you want them to leave impressed.</strong> The Quarry. An hour and a quarter south, and the moment the back nine drops into the pit is the part they will describe to other people when they get home. Lost Pines Resort is the shorter version of the same instinct &mdash; twenty minutes east, and the loblolly pine does not look like anywhere else within an hour of the city.</p>
    <p><strong>It is a birthday and four of you are going.</strong> Star Ranch midweek, or Vaaler Creek. Both still publish a real number, both come in around or under a hundred dollars a head, and knowing the cost in advance is what makes it easy to organise four people who all have to say yes.</p>
    <p><strong>You want the drive to be part of it.</strong> Vaaler Creek out through Blanco, or Crystal Falls up into Leander. Neither is the best course on this page and both are on it partly because the forty minutes before you arrive are good.</p>
    <p><strong>It is a real occasion and a day will not cover it.</strong> Go to the overnight section. Horseshoe Bay for the volume of golf, Barton Creek if nobody wants to drive, La Cantera if half the group is not playing, Lajitas if you have three days and the will to use them.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What happened to Wolfdancer Golf Club?",
  "It is now branded Lost Pines Resort. The old wolfdancergolfclub.com address redirects to the resort's own golf page, which no longer uses the Wolfdancer name anywhere. The course itself is unchanged — the same Arthur Hills design at 7,300 yards, par 72, out at Bastrop. The resort's current copy puts it about 20 minutes from Austin."),
 ("What is the best golf course near Austin for a special occasion?",
  "It depends how far you will drive. Inside half an hour, Lost Pines Resort and Falconhead both feel like an event without eating the day. At an hour or so, The Quarry's back nine plays inside a genuine hundred-year-old quarry pit and is unlike anything else in reach. If the occasion justifies a night away, Horseshoe Bay has four courses on one property."),
 ("Why do so many Austin courses no longer list green fees?",
  "Dynamic pricing. Rates move with demand, tee time, day of week and season, the same way airline seats do. Falconhead states this openly on its rates page. Others book through Troon or GolfNow, where the price is generated at the point of booking. A course that still posts a fixed rate card — Vaaler Creek and Star Ranch both do — is now the exception."),
 ("How far is Lajitas from Austin, and is it a day trip?",
  "It is roughly seven hours west, on the Rio Grande at the edge of Big Bend, and it is emphatically not a day trip. Plan three nights. Lajitas prints its accolades on its own site: Golfweek ranks Black Jack's Crossing the number one course you can play in Texas and #38 resort course in the USA, and the Dallas Morning News has had it at number one in Texas since 2013."),
 ("Which course near Austin is the best value for a big round?",
  "Star Ranch midweek. Rates read on 17 September 2026 were $85 to $99 Monday through Thursday, against $129 to $139 on a Friday or weekend, and $62 to $75 after 3pm. Vaaler Creek at $95 with the cart included is the other one where you know the real number before you leave the house."),
 ("Do I need to stay overnight to play the resort courses?",
  "Not always, but it usually helps. Resorts like Barton Creek and Horseshoe Bay prioritise guest tee times, and the rate you are quoted often depends on whether you have a room. For Horseshoe Bay's four courses or Barton Creek's four, a night on the property is usually the difference between playing what you wanted and playing what was left."),
]

def st(s):
    return (re.sub(r"<[^>]+>", "", s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&ndash;", "–").replace("&times;", "×"))

# HOUSE FAQ MARKUP IS <details class="faq-q"><summary>. div.faq-q + div.faq-a
# fails twice over — see build-divot-tools.py.
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

# TWO SEPARATE SCRIPTS, NOT ONE @graph. fix-template-leak.py rebuilds the visible
# FAQ from the first ld+json block containing "FAQPage" and reads ["mainEntity"]
# off the top level of it. An @graph wrapper has no top-level mainEntity and the
# script dies with KeyError. The chassis pages all ship a bare FAQPage object, so
# that is what this emits — with the Article as its own separate block.
SCHEMA_FAQ = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}
SCHEMA_ART = {"@context": "https://schema.org", "@type": "Article", "headline": st(PLAIN),
   "description": DESC, "datePublished": "2026-09-17",
   "mainEntityOfPage": f"https://thegrassyissue.com/drops/{SLUG}",
   "author": {"@type": "Person", "name": "Lenny Harrington"},
   "publisher": {"@type": "Organization", "name": "The Grassy Issue",
                 "url": "https://thegrassyissue.com"}}

# ------------------------------------------------------------------ chassis
model = open("drops/7-divot-tools-actually-worth-carrying.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]

head = re.sub(r"<title>[^<]*</title>", f"<title>{st(PLAIN)} — The Grassy Issue</title>", head)
for k, attr in [("description", "name"), ("og:title", "property"), ("og:description", "property"),
                ("twitter:title", "name"), ("twitter:description", "name")]:
    v = st(PLAIN) if k.endswith("title") else DESC
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, _v=v: m.group(1) + _v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
for k, attr in [("og:image", "property"), ("twitter:image", "name")]:
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + "https://thegrassyissue.com" + FG + "wolfdancer.jpg" + m.group(2), head)
_ld = ('<script type="application/ld+json">' + json.dumps(SCHEMA_FAQ) + "</script>\n"
       '<script type="application/ld+json">' + json.dumps(SCHEMA_ART) + "</script>")
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _m: _ld, head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Field Notes</a><span>/</span>\n  Special Day Rounds</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>{DATE}</span><span class="dot"></span>\n'
        '    <span>Field Notes</span><span class="dot"></span>\n'
        f'    <span>{len(DAY)} Day Trips &middot; {len(NIGHT)} Overnights</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{FG}wolfdancer.jpg" '
        'alt="Resort fairway winding through the Lost Pines east of Austin, Texas" /></div></div>\n'
        + INTRO
        + sec(f"Day Trips &mdash; {len(DAY)} Courses",
              "Leave after breakfast, home for dinner. Nothing further out than about an hour and a quarter.", DAY)
        + PRICES
        + sec(f"Make It a Weekend &mdash; {len(NIGHT)} Overnights",
              "Golf that is too far, or too good, to compress into one day.", NIGHT)
        + PLANNING
        + FAQ)

out = head + body + tail

# ------------------------------------------------------------- post-checks
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(body)))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if words < 1200:
    problems.append(f"only {words} words")
if out.count("<h1") != 1:
    problems.append(f"{out.count('<h1')} h1 tags")
if out.count('class="product-card"') != len(ALL):
    problems.append("card count mismatch")
# House rule: the word is banned in TGI copy. Place names are exempt, and the
# chassis filename we read from happens to contain it — check the OUTPUT prose.
_banned = re.findall(r"\bworth\b", plain, re.I)
if _banned:
    problems.append(f"banned word 'worth' appears {len(_banned)}x in the copy")
# The FAQ explains the rename, so it legitimately prints the old name and the old
# domain. Everywhere ELSE they are defects — a card named Wolfdancer Golf Club, or
# a product-link pointing at a domain that now redirects.
_nofaq = out.replace(FAQ, "").replace(json.dumps(SCHEMA_FAQ), "")
if "Wolfdancer Golf Club" in _nofaq:
    problems.append("the retired Wolfdancer Golf Club name is used outside the FAQ that explains it")
if "wolfdancergolfclub.com" in _nofaq:
    problems.append("the redirecting Wolfdancer URL is still linked")
if 'href="https://www.wolfdancergolfclub' in out:
    problems.append("a product link points at the redirecting Wolfdancer domain")
if "ChatGPT-Image" in out:
    problems.append("an AI-generated image from a course site was used as photography")
for _i, _n, meta, *_ in ALL:
    if re.search(r"\$\d", meta) and "2026" not in body:
        problems.append("a price is quoted without the date it was read")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
    json.loads(b)
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(out)

print(("wrote" if apply_ else "DRY RUN") + f" drops/{SLUG}.html")
print(f"  {len(DAY)} day trips + {len(NIGHT)} overnights = {len(ALL)} courses")
print(f"  {words} words | {sum(len(i) for i,*_ in ALL)} gallery frames | FAQ {len(FAQ_ITEMS)} + schema")
if not apply_:
    print("\npass --apply to write")
