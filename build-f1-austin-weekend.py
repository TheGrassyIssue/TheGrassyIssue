#!/usr/bin/env python3
"""build-f1-austin-weekend.py — Field Note: the ultimate (no-budget) F1 weekend in Austin. 21 October 2026.
Lenny: "Let's do a field note- the ultimate F1 Austin weekend, golf, F1, events, Restaurants, UT football, No budget".
Cloned from build-austin-weekend.py (place cards with galleries). FACTS (all checked Oct 21, 2026, research briefs in research/f1-weekend/):
 F1 timetable (formula1.com) + COTA schedule; COTA ticket/hospitality/grandstand/parking/shuttle pages; F1 Experiences package pages;
 BLADE Austin race weekend page; Texas Athletics 2026 schedule + Ole Miss release (Ole Miss at Texas, Sat Oct 24, 6:30pm CT, ABC);
 Omni Barton Creek golf page (guests/members only); Hyatt Lost Pines golf page; Michelin Guide Texas 2026 release (Oct 2026);
 Barley Swine FAQ ($150 F1-weekend tasting); Kappo Kappo FAQ; Jeffrey's/OpenTable; KXAN (92-95% hotel occupancy); F1 extension release (quotes).
 Field Club seat price is a reseller listing (SuiteHop), labelled as such. Paddock Club price not published (waitlist) - we say so.
PHOTOS: COTA's own site imagery, F1 Experiences package imagery, Texas Athletics, Kappo Kappo's site, and TGI's existing Austin photo library.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "The Ultimate F1 Weekend in Austin: Golf, COTA, Texas Football"
DESC = ("A no-budget US Grand Prix weekend in Austin, Oct 22-25, 2026: Barton Creek and Lost Pines golf, Paddock Club and a helicopter to COTA, "
        "Texas vs Ole Miss, Michelin-starred dinners and the race, day by day.")
H1 = "The Ultimate F1 Weekend in Austin, No Budget"
BC = "F1 Weekend in Austin"
SLUG = "ultimate-f1-weekend-austin"
IMG = "/images/f1-weekend"
W = IMG
R = "/images/austin-road-trip"
LS = ' style="border-bottom:1px solid var(--ink)"'
P = {
 # key: (kicker, name, price-or-area, url, copy, frames, link label)
 "omni": ("Thursday &middot; Check in &middot; West Austin", "Omni Barton Creek Resort &amp; Spa", "Guests and members only",
   "https://www.omnihotels.com/hotels/austin-barton-creek/golf/rates",
   "Base camp. Barton Creek&rsquo;s four courses are open only to club members and registered resort guests, so if you want Fazio Foothills and the Coore Crenshaw course on the same trip, this is where you sleep. Guests can book tee times up to 120 days ahead through the resort&rsquo;s Experience Planners (512-329-4018). Green fees aren&rsquo;t published; call the pro shop. Nothing is closed for maintenance this month.",
   [f"{R}/barton-creek-resort-aerial.jpg", f"{R}/barton-creek-resort-exterior.jpg", "/images/field-guide/omni-barton.jpg"], "Book"),
 "foothills": ("Thursday, 7am &middot; Barton Creek", "Fazio Foothills", "Resort guests",
   "https://www.omnihotels.com/hotels/austin-barton-creek/golf",
   "Get the best round in Austin out of the way first. Foothills is the Tom Fazio course that local guides rank as the top public-access round in town. Go off early and you&rsquo;re done with time for lunch before the gates open at COTA.",
   [f"{R}/barton-creek-foothills.jpg", "/images/field-guide/omni-barton.jpg"], "Tee times"),
 "interstellar": ("Thursday, 11am &middot; Northwest Austin", "InterStellar BBQ", "Michelin star, 2026",
   "https://guide.michelin.com/us/en/texas/austin_2958315/restaurant/interstellar-bbq",
   "One of two Austin barbecue joints with a Michelin star in the 2026 Texas guide. It opens at 11am Wednesday through Sunday and closes at 4pm, or when the meat runs out. Lunch here, then head southeast to the track.",
   ["/images/austin-bbq/interstellar-bbq.jpg"], "Michelin Guide"),
 "thursday": ("Thursday, 2pm &middot; COTA", "Grand PrixView Thursday", "From $20",
   "https://circuitoftheamericas.com/ticket/grand-prixview-thursday/",
   "New for 2026: a fourth day at the track. Gates open at 11:30am, F1 Academy practices at 12:25, Pirelli hot laps run at 1:20, and the <strong>Pit Lane Walk is 2 to 4pm</strong>. It&rsquo;s the closest most people ever get to the garages, and Thursday tickets start at $20.",
   [f"{W}/cota-aerial.jpg", f"{W}/cota-academy.jpg"], "Tickets"),
 "kappo": ("Thursday dinner &middot; Austin Proper, downtown", "Kappo Kappo", "$195 omakase",
   "https://www.kappokappo.com/faq",
   "One of two new Austin Michelin stars in the 2026 Texas guide. A nine-course French-Japanese omakase for $195, plus a 20% service charge, inside the Austin Proper. It&rsquo;s open Tuesday to Saturday, and there&rsquo;s a 48-hour cancellation policy.",
   [f"{W}/kappo-2.jpg", f"{W}/kappo-1.jpg", f"{W}/kappo-3.jpg"], "Reserve"),
 "coore": ("Friday, 7am &middot; Barton Creek", "The Coore Crenshaw Course", "Resort guests",
   "https://www.omnihotels.com/hotels/austin-barton-creek/golf",
   "Round two at Barton Creek, on the course Ben Crenshaw built with Bill Coore. The same local rankings put it second in Austin, right behind Foothills, so you&rsquo;ve played the top two by Friday lunch.",
   [f"{R}/barton-creek-coore-crenshaw.jpg", f"{R}/barton-creek-resort-aerial.jpg"], "Tee times"),
 "blade": ("Friday, late morning &middot; Steiner Steakhouse helipad", "BLADE to COTA", "Charter from $5,140 one way",
   "https://www.blade.com/austin_race_weekend",
   "The official helicopter partner of COTA flies Friday through Sunday. A private charter from the Steiner Steakhouse helipad on the west side starts at $5,140 one way or $10,280 round trip. Seats from the Creedmoor heliport run $1,495 one way. On landing, COTA staff meet you with a Cadillac SUV to the Turn 1 VIP entrance. There&rsquo;s no parking at the heliports, so arrive by car service.",
   [f"{W}/cota-heli.jpg", f"{W}/cota-race.jpg"], "Book a flight"),
 "paddock": ("Friday to Sunday &middot; Above the team garages", "F1 Paddock Club", "Waitlist",
   "https://circuitoftheamericas.com/ticket/paddock-club/",
   "The top ticket in the sport. A three-day suite above the team garages, looking down on the main straight, the grid and pit lane, with food and an open bar. Every day includes a Paddock Club pit lane walk, plus a track tour and talks with F1 ambassadors. COTA sells it by email and doesn&rsquo;t publish a price, and race week means you&rsquo;re joining a waitlist. If that doesn&rsquo;t come through, see the other seats below.",
   [f"{W}/cota-paddock.jpg", f"{W}/cota-hosp.jpg"], "Join the waitlist"),
 "barley": ("Friday dinner &middot; Burnet Rd", "Barley Swine", "$150 F1 tasting menu",
   "https://www.barleyswine.com/faqs",
   "Bryce Gilmore&rsquo;s tasting room kept its Michelin star in 2026, and its general manager won the guide&rsquo;s Outstanding Service Award. The tasting menu is $150 for race weekend, October 22 to 25 ($125 the rest of the year), with wine pairings from $75. Book on Tock.",
   ["/images/date-night-2/barley-1.jpg", "/images/date-night-2/barley-2.jpg", "/images/date-night-2/barley-3.jpg"], "Reserve"),
 "lostpines": ("Saturday, 7:30am &middot; Near Bastrop", "Lost Pines Golf Club", "About $115&ndash;$176",
   "https://www.hyatt.com/hyatt-regency/en-US/auslp-hyatt-regency-lost-pines-resort-and-spa/golf",
   "The resort course formerly known as Wolfdancer: an Arthur Hills design, 7,200 yards and par 72, in the pines east of Austin. The first tee time is 7:30am, and you finish on the same side of town as COTA. October tee times ran $115 to $176 a player with a cart on GolfNow; call the shop at 512-308-4653.",
   ["/images/austin-weekend/lostpines-0.jpg", "/images/austin-weekend/lostpines-1.jpg", "/images/austin-weekend/lostpines-2.jpg", "/images/austin-weekend/lostpines-4.jpg"], "Tee times"),
 "quali": ("Saturday, 4pm &middot; COTA", "Qualifying", "Included",
   "https://circuitoftheamericas.com/event/f1/schedule/",
   "Final practice is at 12:30 and qualifying runs 4 to 5pm. That hour sets the grid, and in Austin, where the run into Turn 1 decides so much, it&rsquo;s the session to watch from your seat rather than a screen. Post Malone plays the Super Stage about 90 minutes after the track goes quiet.",
   [f"{W}/cota-t12.jpg", f"{W}/f1e-2025-cirtuit-atmosphere-15.jpg"], "Schedule"),
 "texas": ("Saturday, 6:30pm &middot; DKR, on campus", "Texas vs. Ole Miss", "From $4,768 a seat (resale)",
   "https://texaslonghorns.com/sports/football/schedule/text/2026",
   "Ole Miss comes to Darrell K Royal&ndash;Texas Memorial Stadium on Saturday at 6:30pm, live on ABC, and the home schedule has been reported sold out. The top seat is the UFCU Field Club in the south end zone, at field level by the team tunnel, with food included; one reseller had it at $4,768 a ticket. Be honest with yourself about the timing: qualifying ends at 5pm on the far side of town. Leave right after, by car service, or watch the game at the hotel.",
   [f"{W}/dkr-night.jpg", f"{W}/dkr-flag.jpg", f"{W}/dkr-day.jpg", f"{W}/dkr-food.jpg"], "Schedule"),
 "race": ("Sunday, 3pm &middot; COTA", "The United States Grand Prix", "56 laps",
   "https://circuitoftheamericas.com/event/f1/schedule/",
   "The drivers&rsquo; parade is at 1pm, the anthem at 2:44, and lights out at 3. Fifty-six laps up the hill into Turn 1 and back again. Alesso plays the amphitheater at 5:30 while the car parks empty, which is the right time to be in no hurry. If you flew in, the last BLADE departures run until 10:20pm.",
   [f"{W}/cota-race.jpg", f"{W}/cota-crowd.jpg", f"{W}/cota-aerial.jpg"], "Schedule"),
 "jeffreys": ("Sunday dinner &middot; Clarksville", "Jeffrey&rsquo;s", "Michelin recommended",
   "https://www.opentable.com/r/jeffreys-restaurant-austin",
   "End it with a steak. Jeffrey&rsquo;s in Clarksville does dry-aged prime steaks, made the 2026 Michelin guide as a recommendation, and serves dinner every night from 4:30 to 10pm, Sundays included.",
   ["/images/steakhouses-2026/jeffreys-1.jpg", "/images/date-night-2/jeffreys-1.jpg", "/images/date-night-2/jeffreys-2.jpg"], "Reserve"),
 "papaya": ("If Paddock Club is full &middot; Turn 20", "Papaya Club, hosted by McLaren", "$11,529",
   "https://f1experiences.com/2026-united-states-grand-prix/papaya-club",
   "Still available when we checked, through F1 Experiences: a two-day McLaren hospitality club at Turn 20 with all-inclusive food, a premium open bar, team appearances, car displays and a gift bag. It&rsquo;s $11,529 per person before the 2.95% card fee.",
   [f"{W}/f1e-2026-papaya-club-2.jpg", f"{W}/f1e-2026-papaya-club-4.jpg", f"{W}/f1e-2026-papaya-club-6.jpg", f"{W}/f1e-2026-papaya-club-apperances-3.jpg"], "Book"),
 "guesthouse": ("COTA&rsquo;s own &middot; Turns 17 to 20", "The Guest House at Turn 20", "Ticketmaster",
   "https://circuitoftheamericas.com/ticket/turn-20-hospitality/",
   "A two-story club over the back of the lap, the main straight and the climb to Turn 1, with food, an open bar, a rooftop terrace with 360-degree views and on-track concert access on Friday and Saturday. COTA sells it on Ticketmaster and doesn&rsquo;t list the price. All of COTA&rsquo;s premium hospitality includes the three concerts.",
   [f"{W}/f1e-2026-the-guest-house-at-turn-20-1.jpg", f"{W}/cota-aerial.jpg"], "Tickets"),
 "clubsi": ("With a pit lane walk &middot; Turns 12 to 15", "Club SI | F1 Experiences Live", "$7,576",
   "https://f1experiences.com/2026-united-states-grand-prix/club-si-f1-experiences-live",
   "Friday to Sunday in the two-story Club SI lounge over the stadium section, with food and drink, plus the Aramco F1 pit lane walk, a guided track tour and a photo with the championship trophy. $7,576 through F1 Experiences.",
   [f"{W}/clubsi-1.jpg", f"{W}/clubsi-2.jpg"], "Book"),
}
SECTIONS = [
 ("Thursday: Foothills, Barbecue, Pit Lane", "thursday", ["omni","foothills","interstellar","thursday","kappo"],
  "<strong>Check in, play, walk the pit lane</strong>The best round in Austin at dawn, a Michelin-starred barbecue lunch, the new Thursday at COTA, then a nine-course omakase downtown."),
 ("Friday: Coore Crenshaw, Then Fly In", "friday", ["coore","blade","paddock","barley"],
  "<strong>Golf, a helicopter and the paddock</strong>Practice starts at 12:30. Play early, take the helicopter from the west side and skip the traffic entirely. Maroon 5 plays after the track closes."),
 ("Saturday: Lost Pines, Qualifying, Texas Football", "saturday", ["lostpines","quali","texas"],
  "<strong>The longest day</strong>An early round east of town, qualifying at four, and the Longhorns under the lights at 6:30. You can do all three. It just won&rsquo;t be relaxing."),
 ("Sunday: The Race", "sunday", ["race","jeffreys"],
  "<strong>Lights out at 3pm</strong>Slow morning, a late helicopter, the Grand Prix, and a steak to finish."),
 ("Other Seats, Still on Sale", "seats", ["papaya","guesthouse","clubsi"],
  "<strong>If the Paddock Club waitlist doesn&rsquo;t move</strong>Three top-end packages that were still available on October 21. The Main Grandstand and general admission are sold out; Turn 1 grandstand seats were still on sale from $1,206.50 for three days."),
]
N = 17
PQ = {
 "friday": ("We&rsquo;re glad Formula 1 has found a home in Texas.", "Bobby Epstein, COTA chairman, on the deal that keeps the race here through 2034"),
 "sunday": ("Since 2012 the United States Grand Prix has continued to grow in strength and popularity.", "Stefano Domenicali, F1 president and CEO"),
}
BANDS = {}
TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>Once a year Austin&rsquo;s hotels hit record prices for four days, and the US Grand Prix is this weekend, October 22 to 25. This year it lands on top of a sold-out Texas home game against Ole Miss. If money really is no object, here&rsquo;s how we&rsquo;d spend it: three rounds, three days at the track, a Saturday night at DKR and the best tables in town.</p>
    <p><strong>Stay at Barton Creek, because that&rsquo;s the only way in.</strong> Austin&rsquo;s best golf is private, and the one place a visitor can reliably play it is Omni Barton Creek, where the resort&rsquo;s guests get the Fazio and Coore Crenshaw courses. Play Thursday and Friday mornings there, and Saturday at Lost Pines, east of town, on the same side as the track.</p>
    <p><strong>Never sit in race traffic.</strong> COTA sits out in southeast Travis County, and the roads in are the worst part of the weekend. BLADE, the track&rsquo;s official helicopter partner, flies from a helipad at Steiner Steakhouse on the west side of town and drops you at a car to the Turn 1 VIP gate. At this budget, that&rsquo;s the single best money you&rsquo;ll spend.</p>
    <p><strong>Saturday is a choice.</strong> Qualifying ends at 5pm and kickoff is 6:30 on campus. You can make both with a car waiting at the gate, but if you don&rsquo;t, the game is on ABC.</p>
    <p><strong>Book everything today.</strong> Visit Austin expects hotels to be 92 to 95% full. The Paddock Club is down to a waitlist, the Main Grandstand and general admission are gone, and Barley Swine has a race-weekend menu. Some of what&rsquo;s here will sell out before Friday; where it already has, we&rsquo;ve said so and given you the next best thing.</p>
    <p>Also on the table if you have room: Hestia&rsquo;s live-fire tasting menu ($215), Craft Omakase ($185, seats released in weekly drops on Tock), Fabrik on Friday night (its only race-weekend service), the SingleThread dinner series at 1 Hotel Austin October 22 to 24, the Mercedes fan hub at 400 Congress, the Smashing Pumpkins at Moody Center on Sunday at 8, and our <a href="/drops/austin-bbq-field-guide"{LS}>barbecue field guide</a> for the rest of Austin&rsquo;s smoke.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Weekend</div>
      <div class="sidebar-detail"><span class="l">Dates</span><span>Oct 22&ndash;25, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Qualifying</span><span>Sat, 4pm CT</span></div>
      <div class="sidebar-detail"><span class="l">Race</span><span>Sun, 3pm CT</span></div>
      <div class="sidebar-detail"><span class="l">Texas vs Ole Miss</span><span>Sat, 6:30pm, ABC</span></div>
      <div class="sidebar-detail"><span class="l">Concerts</span><span>Maroon 5, Post Malone, Alesso</span></div>
      <div class="sidebar-detail"><span class="l">Rounds</span><span>Three</span></div>
      <div class="sidebar-detail"><span class="l">Budget</span><span>None</span></div>
      <div class="hashtags">
        <span class="hashtag">#USGP</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
MORE = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="more-austin">On a Budget After All?</h2>
  <p class="cat-kicker">Turn 1 grandstand seats were still on sale from $1,206.50 for three days, Thursday tickets start at $20, every race ticket includes the concerts on the festival lawn, and COTA&rsquo;s shuttle from Waterloo Park downtown starts at $49. For the golf, our <a href="/drops/austin-golf-weekend"{LS}>Austin golf weekend</a> does Lions, Kizer and Lost Pines for a fraction of this, and <a href="/drops/best-steakhouses-in-austin"{LS}>our steakhouse guide</a> has dinner covered.</p>
</section>
"""
FAQ = [
 ("When is the 2026 United States Grand Prix?", "October 22 to 25, 2026, at Circuit of The Americas in Austin. Thursday is Grand PrixView day, with a pit lane walk from 2 to 4pm. Practice is Friday, qualifying is Saturday at 4pm, and the race starts Sunday at 3pm Central. There is no sprint race in Austin this year."),
 ("Can you take a helicopter to COTA?", "Yes. BLADE is COTA's official helicopter partner and flies October 23 to 25. On October 21, 2026, seats from the Creedmoor heliport were $1,495 one way and private charters from the Steiner Steakhouse helipad started at $5,140 one way."),
 ("Is there a Texas football game during F1 weekend?", "Yes. Texas hosts Ole Miss at Darrell K Royal-Texas Memorial Stadium on Saturday, October 24, 2026, at 6:30pm Central on ABC, about 90 minutes after F1 qualifying ends."),
 ("Are the F1 concerts included with a COTA ticket?", "Yes. Every race ticket includes festival-lawn access to Maroon 5 on Friday, Post Malone on Saturday and Alesso after the race on Sunday. Floor and reserved concert seats cost extra, and COTA's premium hospitality packages include all three."),
 ("Can a visitor play golf at Barton Creek in Austin?", "Only as a registered guest of Omni Barton Creek Resort & Spa or as a club member. Guests can book tee times up to 120 days ahead through the resort's Experience Planners."),
 ("Which Austin restaurants have a Michelin star in 2026?", "The 2026 Michelin Guide Texas gave one star to Barley Swine, Craft Omakase, Fabrik, Hestia, InterStellar BBQ, Kappo Kappo and LeRoy and Lewis."),
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
         "url": URL, "image": og, "datePublished": "2026-10-21", "dateModified": "2026-10-21",
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
    <span>Austin, Texas &middot; October 22&ndash;25, 2026</span><span class="dot"></span>
    <span>Prices and availability checked October 21, 2026</span><span class="dot"></span>
    <span>Track photos: Circuit of The Americas</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A Red Bull Formula 1 car through a corner at Circuit of The Americas in front of a packed grandstand" fetchpriority="high" /></div></div>
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
