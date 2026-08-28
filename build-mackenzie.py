#!/usr/bin/env python3
"""Rebuild The MacKenzie Collab Archive at the existing slug.

Lenny's brief (2026-08-27/28): rebuild the old 6-bag post AT THE SAME SLUG, expand to
every partner with 2-4 standout editions each, include sold-out product, note what
isn't published rather than guessing, add quotes and IRL photography.

FOUNDING FACT, verified 2026-08-28 and previously wrong everywhere: MacKenzie was
founded in 1985 by PGA Tour pro Peter Jacobsen and his brother David. It is named for
RICK MacKENZIE, the St Andrews caddie who carried double for them and swapped their
staff bags into one leather pencil bag. The original logo came off his business card.
Todd Rohrer revived the company in 2006. Sources: mackenziegolfbags.com/about/the-mackenzie-story,
golfclubatlas.com feature interview with Rohrer (Nov 2015), scotlandshop.com Mulflur Q&A (Aug 2020).

NOT INCLUDED, and why:
  - PowerBilt ($699, sold out, published 2026-03-13). Real Shopify record but the copy
    describes a stand bag with integrated legs and dual straps, which MacKenzie does not
    make; image filenames disagree with the variant names; lead SKU is "Hireko Ignore".
    Reads as templated boilerplate. Left out rather than printed as fact.
  - Sentinel Golf's own four Walkers - Squarespace, no fetchable imagery. Covered in prose.
    The Miura x Sentinel bag carries Sentinel visually.
  - BEAMS Golf Japan digital camo (Y143,000, 2026-01-17) - beams.co.jp returns
    ERR_HTTP2_PROTOCOL_ERROR to Playwright. Covered in prose.
  - Broken Tee Society Vol. 1 (10 bags, dispatched 2024-03-07) - page returns empty.
    Covered in prose. Do NOT print "Vol. 2"; later drops exist but were never numbered.

FYFE NUMBERING: 22 editions exist. Only 19-22 are still listed. Editions 4, 14, 15 and
16 have no public product record at all, though a lookbook for 14-16 survives. Cached
prices for the 12th/13th/18th were rejected as unreliable - the cache visibly blended
copy between adjacent editions.

NOTE the template nests <aside class="sidebar"> INSIDE <div class="writeup">. Do not
close .writeup before the aside; the final </div> closes it. Getting this wrong makes
the sidebar overlap the first section.
"""
import re, os, glob, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(ROOT, "drops", "the-niche-grip-report.html")
OUT  = os.path.join(ROOT, "drops", "the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site.html")
IMGD = "/images/mackenzie/"

TITLE = "The MacKenzie Collab Archive"
DESC  = ("Every MacKenzie Golf Bags collaboration we can document - Fyfe's 22 Scottish editions, "
         "Sugarloaf's house account, Miura, Bandon Dunes and more. Prices, dates and what nobody published.")
SLUG  = "the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site"

def frames(prefix):
    fs = sorted(glob.glob(os.path.join(ROOT, "images", "mackenzie", prefix + "-*")))
    fs = [f for f in fs if re.search(r"-\d+\.(jpg|jpeg|png|webp)$", f, re.I)]
    return [IMGD + os.path.basename(f) for f in fs][:6]

def single(name):
    p = os.path.join(ROOT, "images", "mackenzie", name)
    return [IMGD + name] if os.path.exists(p) else []

def card(cid, brand, name, desc, imgs, alt):
    imgs = [i for i in imgs if os.path.exists(os.path.join(ROOT, i.lstrip("/")))]
    if not imgs:
        raise SystemExit("NO IMAGES for card: " + cid)
    n = len(imgs)
    fr = "".join(
        f'<div class="pg-frame"><img src="{u}" loading="lazy" '
        f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, u in enumerate(imgs))
    dots = "".join(
        f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
        f'aria-label="View image {i+1}"></button>' for i in range(n))
    arrows = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              f'<span class="pg-count">1/{n}</span>') if n > 1 else ""
    return (f'<div class="product-card" id="{cid}" data-frames="{n}">\n'
            f'    <div class="product-gallery"><div class="pg-track">{fr}</div>{arrows}'
            f'<div class="pg-dots">{dots}</div></div>\n'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{brand}</div>\n'
            f'        <div class="product-name">{name}</div>\n'
            f'        <div class="product-desc">{desc}</div>\n'
            f'      </div>\n    </div>')

# ----------------------------------------------------------------- the lineup
SECTIONS = []

# 1 --------------------------------------------------------------- FYFE
SECTIONS.append(("scotland", "The Scottish Line", "FYFE GOLF &middot; 22 EDITIONS AND COUNTING",
  "Fyfe Golf has run the longest MacKenzie collaboration of anyone, and it is the one that closes the "
  "circle: an Oregon workshop named after a St Andrews caddie, making bags again in Scottish cloth. The "
  "canvas is organic cotton from the Halley Stevenson mill in Dundee, finishing fabric since the 1800s. "
  "Twenty-two numbered editions have shipped. Four are still listed. Editions 4, 14, 15 and 16 have no "
  "surviving product record at all - a lookbook for 14 to 16 is the only proof they existed.", [
  card("fyfe-19", "Scotland &middot; Sold out", "19th Edition, Between Tides &middot; &pound;650",
    "Fyfe shoots its campaigns where the game actually gets played in Scotland - the Isle of Seil, a boat "
    "crossing, Crinan harbour at first light - and the bags are built to match that weather. Raw duck canvas "
    "with brown tan, cream and red leather, a nautical navigation patch above the pocket and paracord zip "
    "pulls. The base is split cream over tan. Released 23 April 2026 alongside the 20th.", frames("fyfe-mackenzie-golf-bag-x-fyfe-19th-edition"),
    "Fyfe Golf 19th Edition MacKenzie bag in raw duck canvas"),
  card("fyfe-20", "Scotland &middot; Sold out", "20th Edition, Between Tides &middot; &pound;650",
    "Between Tides shipped as a pair, and this is the louder half of it. Heaven blue waxed canvas trimmed in "
    "colonial blue, cream and salmon leather, with the same nautical patch and paracord pulls as its twin "
    "and a split base of cream over heaven blue. Fyfe does not publish how many it makes of anything, and "
    "this sold out like the rest.", frames("fyfe-mackenzie-golf-bag-x-fyfe-20th-edition"),
    "Fyfe Golf 20th Edition MacKenzie bag in heaven blue waxed canvas"),
  card("fyfe-21", "Scotland &middot; Sold out", "21st Edition, Coastal Tones &middot; &pound;650",
    "Fyfe cut the 21st in sage waxed canvas with black, dark green and white leather, and hid a patch "
    "where only the owner sees it. Shot at Elie, on the Fife coast. Fyfe had promised this collaboration "
    "for July 2026 and the sign-up block still says so; the bags were actually cut in late July and put on "
    "sale 11 August.", frames("fyfe-mackenzie-golf-bag-x-fyfe-2"),
    "Fyfe Golf 21st Edition MacKenzie bag in sage waxed canvas"),
  card("fyfe-22", "Scotland &middot; Sold out", "22nd Edition, Coastal Tones &middot; &pound;650",
    "Fyfe cut the 22nd in charcoal waxed canvas against black, agave and white leather, over a white-and-black split base. It "
    "is the most restrained bag Fyfe has made and the one that will age best, because waxed canvas darkens "
    "unevenly and charcoal hides the argument. The current end of the line - no 23rd edition has been "
    "announced.", frames("fyfe-mackenzie-golf-bag-x-fyfe-1"),
    "Fyfe Golf 22nd Edition MacKenzie bag in charcoal waxed canvas"),
]))

# 2 --------------------------------------------------------------- SSC
SECTIONS.append(("sugarloaf", "Sugarloaf's House Account", "SUGARLOAF SOCIAL CLUB &middot; SEVEN BAGS",
  "No brand has used MacKenzie harder than Sugarloaf Social Club. Seventeen MacKenzie-made items sit in "
  "their catalogue, and the bags run from $850 canvas up to a $1,400 white leather piece that reads more "
  "like furniture than luggage. What makes the account interesting is that Ian Gilley keeps changing the "
  "brief - sailcloth one season, all-white leather the next - and MacKenzie keeps saying yes.", [
  card("ssc-white", "Portland, OR &middot; Sold out", "White Leather Double Seve 8&quot; &middot; $1,400",
    "The most expensive thing in this archive and the least sensible, which is the point. SSC's entire "
    "product description runs to fourteen words - made in Portland by MacKenzie, eight inch, white leather, "
    "so good. White leather on a golf bag is a decision you have to keep defending every time you set it "
    "down on wet grass.", frames("ssc-ssc-x-mackenzie-white-leather-double-seve-8"),
    "SSC x MacKenzie white leather Double Seve golf bag"),
  card("ssc-sail-1492", "Portland, OR &middot; Sold out", "Sail Bag &quot;1492&quot; &middot; $975",
    "Three bags cut from recycled Laser dinghy sails, each named for the sail number it was made from, each "
    "therefore a one-off. The battens run down the spine the way they do on a standard Mac. This is the "
    "cleverest thing anyone has done with the Walker pattern - the material arrives already weathered, "
    "already numbered, already having had a life.", frames("ssc-ssc-x-mackenzie-sail-bag"),
    "SSC x MacKenzie Sail Bag 1492 made from recycled Laser sailcloth"),
  card("ssc-sail-8185", "Portland, OR &middot; Sold out", "Sail Bag &quot;8185&quot; &middot; $975",
    "The second of the three sail bags, and proof the idea holds up across different cloth. Because each "
    "sail carries its own creasing, sun-fade and numbering, no two of these are the same bag, and SSC sold "
    "them as individual units rather than a colourway. Part of the Summer Sailing drop, July 2026.",
    frames("ssc-ssc-x-mackenzie-sail-bag-8185"),
    "SSC x MacKenzie Sail Bag 8185 made from recycled Laser sailcloth"),
  card("ssc-mac", "Portland, OR &middot; Sold out", "SSC x MacKenzie Golf Bag &middot; $875",
    "The one that started the account. Plain canvas in navy or Nantucket with the SSC chenille arrow patch "
    "on the flank, eight-inch top, no cleverness anywhere. It is the bag the others are variations on, and "
    "the reason to start here is that the chenille patch against waxed canvas is a texture combination "
    "nobody else in golf is doing.", frames("ssc-ssc-x-mackenzie-golf-bag"),
    "SSC x MacKenzie golf bag in canvas with chenille arrow patch"),
  card("ssc-seve", "Portland, OR &middot; Sold out", "Double Seve 8&quot; &middot; $850",
    "Black waxed canvas or Sunday blue treated canvas, with two leather SSC arrow labels stacked on the "
    "pocket side and the club motto - Play or Perish - printed inside the pocket where you find it later. "
    "There is a D-ring on the spine, an SSC x Mac badge and a Velcro glove square. The details are all "
    "interior, which is very much the house style.", frames("ssc-ssc-x-mackenzie-double-seve-8-golf-bag"),
    "SSC x MacKenzie Double Seve golf bag in black waxed canvas"),
  card("ssc-hidden", "Portland, OR &middot; Sold out", "Hidden Gem &middot; $850",
    "Sand, brown or navy, eight-inch, and the only SSC MacKenzie carrying a water bottle holder - which "
    "their own copy calls a rare offering in the SSC universe, since the house position is generally that "
    "pockets are a character flaw. Released 11 August 2026 as part of the Hidden Gem collection.",
    frames("ssc-hidden-gem-mackenzie-golf-bag"),
    "Hidden Gem MacKenzie golf bag by Sugarloaf Social Club"),
  card("ssc-students", "Portland, OR &middot; Sold out", "Students x Sugarloaf x MacKenzie &middot; $875",
    "A three-way that landed February 2026 and sat at the top of a seventeen-piece collection starting at "
    "$60 for a T-shirt. Eight-inch MacKenzie in 500D Cordura camo nylon with custom merit patches, leather "
    "detailing and terry cloth padding on the strap. Camo on a handmade bag should not work; the merit "
    "patches are what save it.", frames("students-ssc-x-students-x-mackenzie-golf-bag"),
    "Students Golf x Sugarloaf Social Club x MacKenzie golf bag in Cordura camo"),
]))

# 3 --------------------------------------------------------------- MIURA
SECTIONS.append(("clubmakers", "The Clubmakers", "MIURA &middot; FORGED-IRON MONEY",
  "Miura has sold MacKenzie-built Walkers since August 2020, which makes it the longest equipment "
  "relationship on the list - though Miura's own collaborations page does not list MacKenzie at all, "
  "treating them as the maker rather than the partner. The three original Walkers still sit on the site "
  "in leather, waxed canvas and ballistic nylon, and two newer editions have joined them.", [
  card("miura-sentinel", "Japan / USA &middot; Made to order", "Miura x Sentinel Walker &middot; $1,360",
    "A three-way between a Japanese forging house, a Minneapolis design lab and an Oregon bag maker, and "
    "the most technical thing MacKenzie puts its name on. The shell is 1680D CORDURA ballistic nylon woven "
    "in Japan and finished with a heavy polyurethane reverse coating, which makes it weatherproof rather "
    "than merely weather-resistant. It comes in coyote, olive or black and weighs three pounds.", frames("miura-miura-x-sentinel-mackenzie-walker-bag-2026"),
    "Miura x Sentinel MacKenzie Walker bag in 1680D CORDURA ballistic nylon"),
  card("miura-kaicho", "Japan / USA &middot; Made to order", "Kaicho Original Walker &middot; $1,250",
    "Kaicho means chairman, and this is the bag from Miura's Chairman Collection: black premium leather, "
    "minimalist pocket layout, a leather base with a cinch top, and the red Miura hanko stamp - the "
    "personal seal that functions as a signature in Japan. Seven to eight weeks to build. Miura publishes "
    "no release date for it.", frames("miura-kaicho-mackenzie-original-walker-bag"),
    "Kaicho MacKenzie Original Walker bag in black leather with Miura hanko stamp"),
  card("miura-leather", "Japan / USA &middot; In stock", "Original Walker, Leather &middot; $1,250",
    "Miura has sold this arrangement since August 2020 in three materials. The buckskin and cream "
    "leather version is the one that shows what MacKenzie actually does - full grain leather "
    "in an upholstery weight around a millimetre thick, cut and folded and stitched by hand rather than "
    "moulded.", frames("miura-leatherwalker"),
    "Miura MacKenzie Original Walker bag in buckskin and cream leather"),
  card("miura-canvas", "Japan / USA &middot; In stock", "Original Walker, Waxed Canvas &middot; $850",
    "This is the sensible one of the three, cut in sage waxed canvas from one of the oldest "
    "fabric finishers in the country. Waxed canvas is the original outdoor waterproof cloth and it earns "
    "its keep here: it marks, it darkens, it takes on the shape of wherever you lean it, and it does all "
    "that on purpose.", frames("miura-mackenzie-original-walker-bag-canvas"),
    "Miura MacKenzie Original Walker bag in sage waxed canvas"),
]))

# 3b -------------------------------------------------------------- SENTINEL
SECTIONS.append(("sentinel", "The Technical Wing", "SENTINEL GOLF &middot; MINNEAPOLIS",
  "Sentinel is the most interesting thing happening to the MacKenzie pattern, because it treats a 1985 "
  "leather bag as a chassis and swaps the material for laminates borrowed from sailing and alpine packs. "
  "The Minneapolis design lab calls these Sentinel-sourced iterations of the timeless MacKenzie Walker, "
  "and sells them nowhere else. Four models, all made to order in the USA, all built in Oregon, none with "
  "a published edition size. Founder John Mooty has described the sourcing brief as finding the people who "
  "care most about what they make and who do things the right way at all phases of the process.", [
  card("sen-sorensen", "Minneapolis &middot; Made to order", "S&oslash;rensen Walker &middot; $1,750",
    "The most expensive bag in this entire archive, and the least technical thing Sentinel makes - which is "
    "the joke. Where the rest of the range chases laminates, this one goes the other way into Sorensen "
    "Leather, from a Danish tannery established in 1973. Four pounds, which is heavy for a carry bag, in "
    "charcoal, dark or light nubuck.", frames("sentinel-sorensen"),
    "Sentinel Golf Sorensen Walker MacKenzie bag in Danish nubuck leather"),
  card("sen-ultracomp", "Minneapolis &middot; Made to order", "Ultracomp Walker 2.0 &middot; $890",
    "The first project Sentinel and MacKenzie did together, now on its second version. ULTRAcomp is a "
    "polymer laminate bonded to a Cordura face fabric, so it behaves like a technical shell rather than "
    "cloth. YKK reverse-coil waterproof zipper, 550 paracord pulls, full grain leather trim and stainless "
    "hardware. Black, coyote or olive, three pounds.", frames("sentinel-ultracomp"),
    "Sentinel Golf Ultracomp Walker 2.0 MacKenzie bag in ULTRAcomp laminate"),
  card("sen-x50", "Minneapolis &middot; Made to order", "X50 Walker &middot; $810",
    "This is their second project together, and the one that borrows hardest from sailing. X-Pac is a 9.3oz "
    "American-made textile with a 500 denier Cordura face bonded to a polyester X-ply mesh reverse - the "
    "grid you can see through the surface is structural. A stretch Dyneema interior pocket, and a Multicam "
    "colourway alongside navy, stealth gray and black.", frames("sentinel-x50"),
    "Sentinel Golf X50 Walker MacKenzie bag in X-Pac laminate"),
  card("sen-basecamp", "Minneapolis &middot; Made to order", "Basecamp Walker &middot; $890",
    "Bio-based Dyneema composite, which is the fibre alpine climbers use when weight is the enemy, and it "
    "does the obvious thing here: the Basecamp weighs two pounds, a third less than the S&oslash;rensen. Eight-inch "
    "opening, one pocket, full grain leather trim. The only Sentinel Walker offered with no customisation "
    "at all.", frames("sentinel-basecamp"),
    "Sentinel Golf Basecamp Walker MacKenzie bag in Dyneema composite"),
]))

# 4 --------------------------------------------------------------- standing accounts
SECTIONS.append(("accounts", "The Standing Accounts", "DONALD ROSS, ACL AND JAIN &middot; RUNNING SERIES",
  "Below the headline collaborations sits a quieter tier: brands that have made MacKenzie a permanent line "
  "rather than a one-off. Donald Ross Sportswear runs a numbered series that has reached five. ACL Golf's "
  "vendor field on its own storefront reads, literally, MacKenzie x ACL GOLF. These are the accounts that "
  "tell you the workshop has repeat customers, not just admirers.", [
  card("dr-i", "USA &middot; In stock", "DR x MacKenzie Carry Bag &middot; $795",
    "Donald Ross Sportswear trades on a name with more architectural weight than almost any in golf, and "
    "the bags stay respectful of it. Hand-crafted waxed canvas in red with full grain tan leather straps "
    "and navy detailing, eight-inch opening, two pockets, single strap, DR logo embroidered. The first of "
    "the series, listed November 2025.", frames("donaldross-dr-x-mackenzie-carry-bag-red"),
    "Donald Ross x MacKenzie carry bag in red waxed canvas"),
  card("dr-ii", "USA &middot; In stock", "DR x MacKenzie Carry Bag II &middot; $795",
    "The series is at its best on the second edition: navy canvas against a blue and white "
    "crest. Donald Ross released II through V together in July 2026 under a Scottish Traditions banner, "
    "which is a reasonable thing to call a range named for a man from Dornoch who redrew American golf.",
    frames("donaldross-dr-x-mackenzie-bag-blue"),
    "Donald Ross x MacKenzie carry bag II in navy canvas"),
  card("dr-iv", "USA &middot; In stock", "DR x MacKenzie Carry Bag IV &middot; $795",
    "Navy canvas with a red thistle and a Dornoch crest - the most explicitly Scottish bag in the DR run, "
    "and the one that earns the reference rather than borrowing it. Same eight-inch Clubmaker build as the "
    "rest of the series, same $795, no edition size published for any of the five.",
    frames("donaldross-dr-x-mackenzie-bag-navy"),
    "Donald Ross x MacKenzie carry bag IV with thistle and Dornoch crest"),
  card("acl-tan", "USA &middot; In stock", "MacKenzie x ACL, Tan &middot; $850",
    "ACL Golf has built the deepest non-apparel MacKenzie range going - eleven items covering bags, leather "
    "pouches and headcovers. The tan waxed canvas with green leather accents is the pick: warm cloth against "
    "cold trim, with the ACL monogram on the pocket. Eight-inch opening, one pocket, made by hand in Portland.",
    frames("acl-mackenzie-x-acl-golf-8-waxed-canvas-carry-ba"),
    "MacKenzie x ACL Golf carry bag in tan waxed canvas with green leather"),
  card("acl-green", "USA &middot; In stock", "MacKenzie x ACL, Dark Green &middot; $850",
    "The same build in dark green, which is the harder colour to get right on waxed canvas because the wax "
    "pushes green towards olive as it ages. ACL has been running these since 2023 and adding colourways "
    "steadily rather than dropping and vanishing, which makes them unusual among MacKenzie's partners.",
    frames("acl-mackenzie-x-acl-golf-8-green-waxed-canvas-ca"),
    "MacKenzie x ACL Golf carry bag in dark green waxed canvas"),
  card("acl-nylon", "USA &middot; In stock", "MacKenzie x ACL, Nylon &middot; $550",
    "The cheapest way into a MacKenzie here, and a useful reminder that the workshop is not only a "
    "luxury proposition. Ballistic nylon rather than canvas or leather, eight-inch adult carry. ACL also "
    "makes a $450 Mini Mac in the same nylon for kids, the only youth bag MacKenzie builds for anyone.",
    frames("acl-mackenzie-x-acl-golf-8-nylon-adult-carry-bag"),
    "MacKenzie x ACL Golf adult carry bag in ballistic nylon"),
  card("jain", "Los Angeles &middot; Sold out", "Jain &amp; MacKenzie 1st Edition &middot; $720",
    "Jain builds its identity on not being explicable, and the bag commits: Colonial Blue treated canvas "
    "trimmed in Tennessee Orange, white and green leather, with Jain Is Not To Be Defined embroidered "
    "inside the pocket and four enamel pins in the box. Published March 2023, called a first edition, and "
    "no second edition ever followed.", frames("jain-jain-mackenzie-canvas-bag"),
    "Jain and MacKenzie 1st Edition canvas bag in Colonial Blue"),
]))

# 5 --------------------------------------------------------------- course editions
SECTIONS.append(("courses", "The Course Editions", "BANDON DUNES &middot; A STANDING PROGRAMME",
  "Bandon Dunes is not a collaboration so much as a permanent arrangement, and it is the largest single "
  "MacKenzie programme anywhere - twelve bags, one per course, made to order on a nine to ten week lead "
  "time. MacKenzie links to the Bandon shop twice from its own homepage. The 2021 generation embroiders "
  "the architect and opening date inside the pocket; the 2023 generation moved the course logo to the base.", [
  card("bandon-ghost", "Bandon, OR &middot; In stock", "Custom Ghost Tree &middot; $735",
    "Bandon listed this one on 26 August 2026, which makes it the newest course edition anywhere in the "
    "archive. Ghost Tree is the resort's newest course and the bag arrived alongside it. Premium waxed "
    "canvas and full grain leather, an eight-inch opening and two pockets, with embroidered initials "
    "included in the price.", single("bandon-waxed-canvas-golf-bag-custom-ghost-tree-1.png"),
    "MacKenzie Custom Ghost Tree waxed canvas golf bag from Bandon Dunes"),
  card("bandon-pacific", "Bandon, OR &middot; In stock", "Pacific Dunes &middot; $735",
    "Grey waxed canvas for the course most people would name if you made them pick one at Bandon. This is "
    "the 2023 generation, with the course logo embroidered large on the base rather than tucked inside the "
    "pocket - a change that reads as confidence. Free embroidered initials, nine to ten weeks.",
    frames("bandon-new-waxed-canvas-golf-bag-pacific-dunes"),
    "MacKenzie Pacific Dunes waxed canvas golf bag in grey"),
  card("bandon-sheep", "Bandon, OR &middot; In stock", "Sheep Ranch &middot; $735",
    "Sheep Ranch has no bunkers and thirteen greens on the cliff edge, and gets forest green canvas. The "
    "interesting thing about the Bandon programme is the price: $735 runs a hundred dollars under most of "
    "the collaboration bags here, for the same build out of the same workshop.",
    frames("bandon-new-waxed-canvas-golf-bag-sheep-ranch"),
    "MacKenzie Sheep Ranch waxed canvas golf bag in forest green"),
  card("bandon-trails", "Bandon, OR &middot; In stock", "Bandon Trails &middot; $735",
    "Tan canvas for the one course at the resort that leaves the dunes and goes into the trees. Bandon runs "
    "both generations of most courses simultaneously, so the 2021 version of this bag - grey, with David "
    "McLay Kidd and the opening date stitched inside the pocket - is still orderable alongside it.",
    frames("bandon-new-waxed-canvas-golf-bag-bandon-trails"),
    "MacKenzie Bandon Trails waxed canvas golf bag in tan"),
  card("bandon-preserve", "Bandon, OR &middot; In stock", "Bandon Preserve &middot; $685",
    "The odd one out and the cheapest bag at the resort, because it is built differently: a seven-inch "
    "opening rather than eight, single divider, one pocket. Preserve is the thirteen-hole par-three course, "
    "so a smaller bag is the right answer. Listed February 2022 and never revised.",
    single("bandon-waxed-canvas-golf-bag-bandon-preserve-1.jpg"),
    "MacKenzie Bandon Preserve waxed canvas golf bag with seven-inch opening"),
]))

# 6 --------------------------------------------------------------- members only
SECTIONS.append(("members", "Members Only", "THE ONES THAT NEEDED A PASSWORD",
  "The last tier is the hardest to see: bags sold behind a membership, a passcode or an anniversary, and "
  "in some cases never listed publicly at all. This is where MacKenzie does a lot of its actual business - "
  "the wholesale page mentions private label and tournament gifting without publishing a single example.", [
  card("top100", "United Kingdom &middot; Sold out", "Top 100 Exclusive Edition &middot; &pound;795",
    "Top 100 Golf Courses sells one bag and put some thought into it. Charcoal waxed canvas from one of "
    "America's oldest fabric finishers, coated in Martexin original wax, trimmed in full-grain semi-aniline "
    "leather in forest green, crimson and cream. It carries embroidery on both the body and the base, and "
    "takes six to eight weeks to build.", single("top100-mackenzie-navy-waxed-canvas-golf-bag-copy-1.jpg"),
    "Top 100 Golf Courses Exclusive Edition MacKenzie bag in charcoal waxed canvas"),
  card("lockhart", "United Kingdom &middot; Sold out", "Lockhart Travel Club Edition &middot; &pound;795",
    "The sister bag to the Top 100 edition, made for its travel club and sold behind a purchase passcode - "
    "you cannot buy it without being told how. Olive waxed canvas with mahogany trim and buckskin accents, "
    "eight-inch opening, two pockets, the same Martexin wax and the same Beaverton workshop.",
    frames("top100-mackenzie-lockhart-olive-waxed-canvas-golf-b"),
    "MacKenzie Lockhart Travel Club Edition bag in olive waxed canvas"),
  card("hb", "USA &middot; Archived", "H&amp;B x MacKenzie &middot; Price not published",
    "Holderness &amp; Bourne marked its tenth anniversary with navy ballistic nylon and white leather, the "
    "H&amp;B diamond stitched into the handle, brand milestones embroidered on the base and the pocket lined "
    "in house stripe over a leather patch reading Make It Look Easy. No price was ever published and the "
    "product page now redirects to the bag collection.", frames("hb"),
    "Holderness and Bourne x MacKenzie golf bag in navy ballistic nylon"),
]))

# ----------------------------------------------------------------- prose
HERO = IMGD + "life-affric-set.jpg"

WRITEUP = """<p>MacKenzie is a golf brand whose name is a tribute rather than a founder, and the story is
better than most origin myths: in 1985 the Oregon PGA Tour pro <strong>Peter Jacobsen</strong> and his brother
<strong>David</strong> started building bags and named the company after <strong>Rick MacKenzie</strong>, the St
Andrews caddie who used to carry double for them and who solved the problem by tipping both their staff bags into
a single leather pencil bag. The first logo was a drawing lifted off his business card. Forty years later the
workshop still makes one thing, still makes it by hand in Oregon, and has quietly become the maker other brands go
to when they want an object rather than a product.</p>

<p>That is what this page is about. MacKenzie itself publishes almost nothing &mdash; no collaborations page, no
archive, a blog that went dark between July 2020 and November 2025 &mdash; so the record of who it has built for
lives scattered across two dozen partner storefronts, most of them sold out. We went and collected it. What comes
back is a picture of a very small company with a very long order book: <strong>ten employees, seven of whom
actually make bags</strong>, supplying Scotland, Japan, Bandon Dunes and the Walker Cup at the same time.</p>

<p>The house style is unusually consistent for something made in this many colourways. An eight-inch top, a single
strap, one pocket if you are lucky, full grain leather in an upholstery weight around a millimetre thick, and
waxed canvas from a finisher that has been treating cloth since the 1800s. Todd Rohrer, who revived the company in
2006 with what he described as one stitcher and a cell phone, put the brief plainly:
<em>&ldquo;the MacKenzie mantra has always been simple, beautiful, useful.&rdquo;</em> On the question of everything
else the industry bolts onto a bag, he was blunter: <em>&ldquo;In essence, most of what isn&rsquo;t a sack on a
sling in unnecessary.&rdquo;</em></p>

<p>Current chief executive <strong>Nic Mulflur</strong> is clear that the simplicity is the hard part.
<em>&ldquo;There are north of 40 pieces involved in our bags,&rdquo;</em> he told LINKS.
<em>&ldquo;It looks simple, but there are a lot of steps to make a bag to the exacting specifications of our
customers.&rdquo;</em> He is also fairly relaxed about who this is and is not for:
<em>&ldquo;It&rsquo;s not for everybody. But for some of us, there&rsquo;s an emotional attachment to our bags.
It&rsquo;s like a romantic relationship.&rdquo;</em></p>

<p>A word on what is missing, because the gaps are part of the story. <strong>Fyfe Golf has made 22 numbered
editions</strong> and only four are still listed; editions 4, 14, 15 and 16 have no surviving product record
anywhere, though a lookbook for 14 to 16 survives to prove they shipped. Almost nobody publishes edition sizes &mdash;
the one hard number in the entire archive is <strong>ten</strong>, the Broken Tee Society bags The Golfer&rsquo;s
Journal dispatched on 7 March 2024. Two further Broken Tee drops followed and neither was ever numbered, so anyone
selling you a &ldquo;Vol. 2&rdquo; is inventing it. And a <strong>PowerBilt</strong> listing that looks like a
MacKenzie collaboration describes a stand bag with legs and dual straps, which MacKenzie does not make; its lead
SKU is literally <code>Hireko Ignore</code>. We left it out.</p>

<p>Two more are real but could not be photographed. <strong>BEAMS Golf</strong> in Japan released a digital
camouflage caddie bag on 17 January 2026 at &yen;143,000, a genuine Japanese exclusive that ships with its own
wooden stand and sold alongside a matching &yen;16,500 pouch. And the <strong>Broken Tee Society</strong> bags are
gone entirely &mdash; the page is dead, and the drops after the first were never numbered.</p>"""

SIDEBAR = [("Maker", "MacKenzie Golf Bags, Oregon"), ("Founded", "1985, by Peter &amp; David Jacobsen"),
           ("Named for", "Rick MacKenzie, St Andrews caddie"), ("In this archive", "34 bags, 15 partners"),
           ("Range", "$450 &ndash; $1,750")]

FAQ = [
 ("Who founded MacKenzie Golf Bags?",
  "PGA Tour professional Peter Jacobsen and his brother David Jacobsen, both Oregonians, founded the company in "
  "1985. It is named for Rick MacKenzie, the St Andrews caddie who carried double for the brothers and combined "
  "their two staff bags into a single leather pencil bag. The original company logo was taken from a drawing on "
  "his business card. Todd Rohrer revived the company in 2006."),
 ("Where are MacKenzie bags made?",
  "By hand in Oregon &mdash; the company has been based in Portland and Beaverton, and partner listings name both. "
  "In a November 2025 update, chief executive Nic Mulflur wrote: &ldquo;I&rsquo;m not sure folks realize how small "
  "our team is sometimes. We have 10 employees, 7 of which are the insanely talented crew that actually make golf "
  "bags.&rdquo;"),
 ("Which brand has done the most MacKenzie collaborations?",
  "Fyfe Golf in Scotland, by a distance. Fyfe has released 22 numbered limited editions using organic cotton canvas "
  "from the Halley Stevenson mill in Dundee. Sugarloaf Social Club has the deepest US account, with seventeen "
  "MacKenzie-made items in its catalogue including seven bags."),
 ("How many MacKenzie collaboration bags are made of each edition?",
  "Almost never published. Across every collaboration we documented, only one hard edition size exists: the Broken "
  "Tee Society x MacKenzie Vol. 1, of which The Golfer&rsquo;s Journal made ten physical bags, dispatched 7 March "
  "2024. Every other &ldquo;limited edition&rdquo; here is unnumbered."),
 ("What is the most expensive MacKenzie collaboration bag?",
  "Of the bags documented here, the Sugarloaf Social Club x MacKenzie White Leather Double Seve at $1,400. Sentinel "
  "Golf&rsquo;s S&oslash;rensen Walker, in Danish leather from a tannery established in 1973, is listed higher at "
  "$1,750, and the Miura x Sentinel Walker sits at $1,360."),
 ("Can you still buy a MacKenzie collaboration bag?",
  "Some. The Bandon Dunes course editions ($685&ndash;$735), the Miura Walkers ($550&ndash;$1,360), the ACL Golf "
  "range ($450&ndash;$850) and most of the Donald Ross series ($795) are made to order. The Fyfe editions, every "
  "Sugarloaf bag and both Top 100 editions have sold out."),
 ("Does MacKenzie make bags for golf clubs and tournaments?",
  "Yes, though it publishes none of it. In November 2025 Nic Mulflur listed the order book: &ldquo;a 60 golf bag "
  "order for Golf Pride, a couple of Sugarloaf projects, a large stock order for the new Doak course in Baja called "
  "Punta Brava... 30 drop ship Walker Cup bags that were ordered at Cypress in September, a batch of Sentinel x "
  "Miura bags, a batch of bags for the R&amp;A.&rdquo;"),
 ("What is the difference between MacKenzie and Alister MacKenzie?",
  "They are unrelated. MacKenzie Golf Bags is named after Rick MacKenzie, a St Andrews caddie. Alister MacKenzie "
  "was the golf course architect behind Augusta National, Cypress Point and Royal Melbourne. Products referencing "
  "&ldquo;MacKenzie bunkers&rdquo; are referring to the architect, not the bag maker."),
]

# ----------------------------------------------------------------- assemble
tpl = open(TPL, encoding="utf-8").read()
head, tail = tpl.split('<section class="products">', 1)

head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>", head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+TITLE+m.group(2), head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
head = re.sub(r'(<meta property="og:image" content="https://thegrassyissue\.com)[^"]*(")',
              lambda m: m.group(1)+HERO+m.group(2), head)
head = re.sub(r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")',
              lambda m: m.group(1)+SLUG+m.group(2), head)
head = re.sub(r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")',
              lambda m: m.group(1)+SLUG+m.group(2), head)
head = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1)+TITLE+m.group(2), head, flags=re.S)
head = re.sub(r'(<div class="breadcrumb">).*?(</div>)',
              lambda m: m.group(1)+'<a href="/">The Feed</a> &rsaquo; <a href="/drops/">Drops</a> &rsaquo; '
              'The MacKenzie Collab Archive'+m.group(2), head, flags=re.S)
head = re.sub(r'(<div class="drop-meta">).*?(</div>)',
              lambda m: m.group(1)+'Drops &amp; Brands &middot; 28 August 2026 &middot; 34 bags, 15 partners'+m.group(2),
              head, flags=re.S)
head = re.sub(r'(<div class="drop-hero-img">)\s*<img[^>]*>',
              lambda m: m.group(1)+f'<img src="{HERO}" alt="A golfer carrying a Fyfe x MacKenzie bag in Glen Affric, Scotland">',
              head, flags=re.S)
head = re.sub(r'(<div class="writeup-body"[^>]*>).*?(</div>)',
              lambda m: m.group(1)+WRITEUP+m.group(2), head, flags=re.S)
sb = "".join(f'<div class="sidebar-detail"><strong>{k}</strong>{v}</div>' for k, v in SIDEBAR)
head = re.sub(r'(<div class="sidebar-card">).*?(</div>\s*</aside>)',
              lambda m: m.group(1)+'<div class="sidebar-label">The Archive</div>'+sb+m.group(2), head, flags=re.S)

# JSON-LD: article + FAQ
head = re.sub(r'("headline"\s*:\s*")[^"]*(")', lambda m: m.group(1)+TITLE+m.group(2), head)
head = re.sub(r'("datePublished"\s*:\s*")[^"]*(")', lambda m: m.group(1)+"2026-08-28"+m.group(2), head)
head = re.sub(r'("dateModified"\s*:\s*")[^"]*(")', lambda m: m.group(1)+"2026-08-28"+m.group(2), head)
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r"&[a-z]+;|&#\d+;"," ",a)}}
    for q,a in FAQ]}
head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
              '<script type="application/ld+json">'+json.dumps(faq_ld)+'</script>', head, flags=re.S)

body = []
for anchor, hdr, kicker, lede, cards in [(s[0], s[1], s[2], s[3], s[4]) for s in SECTIONS]:
    body.append(f'<h2 id="{anchor}">{hdr}</h2>')
    body.append(f'<p class="cat-kicker"><strong>{kicker}</strong>{lede}</p>')
    body.append('<div class="products-grid">\n' + "\n".join(cards) + '\n</div>')

faq_html = ('<div class="faq">\n<h2 id="faq">Questions</h2>\n' + "\n".join(
    f'<details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '\n</div>')

# keep everything from the FAQ block onward in the template (more-from-feed, footer, scripts)
rest = tail[tail.find('<div class="faq">'):] if '<div class="faq">' in tail else tail
rest = re.sub(r'<div class="faq">.*?</div>\s*(?=<section|<div class="more")', faq_html, rest, count=1, flags=re.S)

out = head + '<section class="products">\n' + "\n".join(body) + "\n" + rest
open(OUT, "w", encoding="utf-8").write(out)

n_cards = sum(len(s[4]) for s in SECTIONS)
words = len(re.sub(r"<[^>]+>", " ", out).split())
print(f"wrote {OUT}")
print(f"sections={len(SECTIONS)} cards={n_cards} words~{words}")

# house voice guard
os.system(f'cd {ROOT} && python3 copy-deck.py apply 2>/dev/null | tail -1')
