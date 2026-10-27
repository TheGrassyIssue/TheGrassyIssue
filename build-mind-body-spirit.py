#!/usr/bin/env python3
"""build-mind-body-spirit.py — Field Note: golf trips for the Mind, Body or Spirit. 27 October 2026.
Lenny: "a field note for golf trips focused on Mind Body or Spirit ... public courses that are destination worthy
of a special trip. Bonus points for taking the trip alone." Then: "Single hero image. Let's do a different format than
the usual cards. Lots of great images and interesting write ups."
New editorial layout (no product cards): full-bleed hero, chapter openers per pillar, one long-form spread per course
with a lead image, a facts panel and a three-image mosaic.
FACTS: research/mbs-trips/{mind,body,spirit}.md (course and resort sites read Oct 27, 2026; UNVERIFIED items left out).
IMAGES: each course's own site / media library (research/mbs-trips/img/*/manifest.json); picks in picked.json.
Not printed because unconfirmed: Whistling Straits and Kiawah green fees, Silvies fees, walking at Tobacco Road and Black Mesa.
Northwood: only the club's homepage banner is used (its gallery is visitor-submitted, rights unclear).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Golf Trips for the Mind, Body or Spirit: 15 Public Courses to Travel For"
DESC = ("Fifteen public golf courses built for a dedicated trip, sorted by what you need: courses that make you think, "
        "courses that test your body and courses that quiet everything down. With fees, walking rules and how to go alone.")
H1 = "Mind, Body, Spirit: 15 Public Golf Trips, and Why You Should Take Them Alone"
BC = "Mind, Body, Spirit Golf Trips"
SLUG = "golf-trips-mind-body-spirit"
IMG = "/images/mbs-trips"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
N = 15

# course: (pillar, name, place, designer line, url, lead alt, lead caption, paras[], facts{}, mosaic[(alt, caption)])
C = {}
C["tobacco-road"] = ("mind", "Tobacco Road", "Sanford, North Carolina", "Mike Strantz &middot; 1998", "https://tobaccoroadgolf.com/",
 "Low sun through pines onto the 11th green at Tobacco Road, sandy waste ground and wire grass in front",
 "The 11th, one of two mirror-image cape holes, carved out of an old sand quarry.",
 ["Tobacco Road looks like nothing else in North Carolina golf. The course is cut from the orange sand of a former quarry, and the club&rsquo;s own pitch is blunt: &ldquo;Some golf courses ask you to follow the rules. Tobacco Road asks you to think differently.&rdquo;",
  "It means it. There is no out of bounds anywhere on the property, and Local Rule No. 1 says every bunker is a waste area, so you can ground your club in all of it. The approach to the 9th is blind to a plateau green. The par-5 13th, the club&rsquo;s own Road hole, finishes at what it calls a &ldquo;blind bathtub green.&rdquo; The 4th and 11th are mirror-image cape holes, the 16th green has three tiers, and the 18th asks for a blind drive. You spend the whole round deciding what you are looking at before you decide what to hit.",
  "Make it a Strantz trip. Tot Hill Farm, about 50 minutes away, is the course he built on horseback, riding his horse Scout with his dogs following along. Between the two you get the purest dose of one architect&rsquo;s imagination available to the public."],
 {"Fee": "Dynamic pricing. $249.51 with cart for early-November 2026 tee times on the club&rsquo;s booking page",
  "Walking": "Cart included in the fee. Call the shop about walking",
  "Fly into": "Raleigh-Durham (RDU). The club says it&rsquo;s 30 minutes from Pinehurst and Raleigh",
  "Watch for": "Only 17 holes open Jan&ndash;Feb 2027; closed June 28&ndash;July 8, 2027. The 2027 tee sheet opens Nov 1",
  "Going alone": "The club&rsquo;s travel desk builds trips for singles. The on-site Stewart Cabin comes with after-hours access to the course"},
 [("The par-5 13th at Tobacco Road, a river of sand and grass islands leading toward the blind green", "No. 13, the Road hole, with its blind bathtub green."),
  ("Autumn drone view of Tobacco Road's 3rd green cut into a hillside of orange and gold hardwoods", "The par-3 3rd in October."),
  ("Tot Hill Farm's 2nd hole seen past a cluster of huge granite boulders", "Tot Hill Farm, the Strantz course built on horseback.")])

C["bethpage-black"] = ("mind", "Bethpage Black", "Farmingdale, New York", "A.W. Tillinghast &middot; 1930s", "https://parks.ny.gov/visit/golf-courses/bethpage-state-park-golf-courses",
 "A foursome walking up a broad Bethpage fairway lined with ragged bunkers toward the clubhouse",
 "On foot, the only way the Black is played.",
 ["Bethpage is the head game. It is a state park course that has hosted two U.S. Opens, a PGA Championship and the 2025 Ryder Cup, and before you hit a shot the state tells you, on a sign by the first tee, that you probably shouldn&rsquo;t: &ldquo;The Black Course Is An Extremely Difficult Course Which We Recommend Only For Highly Skilled Golfers.&rdquo;",
  "What makes it a Mind trip is managing yourself for four-plus hours on a major-championship course, on foot, with no cart to rest in and big bunkers waiting on every miss. Getting there is part of it too. Non-New Yorkers book five days out at 7 p.m., one Black round per 28 days, and the most dedicated still sleep in the parking lot for a walk-up time. GOLF.com&rsquo;s Josh Sens described golfers &ldquo;willing to spend the night in their cars.&rdquo;",
  "We wrote up our own trip in <a href=\"/drops/new-york-golf-trip-sedgewood-union-vale-bethpage-black\">our New York golf trip</a>. The short version: the green fee is the bargain of the list, and the course makes you earn every bit of it."],
 {"Fee": "$140 weekday / $160 weekend for non-New York residents, plus a $5 booking fee (state price list, April 2026)",
  "Walking": "Walking only. Pull carts $7; caddies booked through the pro shop",
  "Fly into": "LaGuardia, JFK or Long Island MacArthur",
  "Watch for": "Open April 15&ndash;Nov 15. Closed Mondays except holidays",
  "Going alone": "Easier than in a group. The first walk-up times each day go to whoever is in line, and a single can take one"},
 [("The warning sign on a railing by Bethpage Black's first tee", "The sign."),
  ("Drone view of a Bethpage green ringed by five big white-sand bunkers", "The island-in-sand greens."),
  ("Fog over a bunkered Bethpage fairway at blue hour with the clubhouse lit on the ridge", "Blue hour from the fairway.")])

C["old-macdonald"] = ("mind", "Old Macdonald", "Bandon Dunes, Oregon", "Tom Doak &amp; Jim Urbina &middot; 2010", "https://bandondunesgolf.com/golf/golf-courses/old-macdonald-golf-course/",
 "A green perched above the Pacific under big clouds at Old Macdonald, ragged bunker and dune grass in front",
 "Old Macdonald, above the Pacific.",
 ["If you want a course that teaches you golf architecture while you play it, this is the one. Old Macdonald is Tom Doak and Jim Urbina&rsquo;s tribute to C.B. Macdonald, and it is built from the template holes he brought to America: Sahara, Biarritz, Redan, Alps, Punchbowl and more, each one a classic idea about how to defend a green.",
  "The resort&rsquo;s hole guide names them all. The 3rd, Sahara, is a blind tee shot over a dune. The 8th, Biarritz, has a green split by a deep swale (&ldquo;A two-putt on this hole is a feat of its own&rdquo;). The 12th is a 237-yard Redan. At the 16th, Alps, you play blind over a hill and ring a bell when you&rsquo;ve putted out so the group behind knows it&rsquo;s clear. The greens are huge, so the thinking doesn&rsquo;t stop when you reach them.",
  "Bandon is walking only, with caddies who know every template by heart. We footnoted the resort in <a href=\"/drops/pnw-golf-trip-gamble-sands-chambers-bay\">our PNW trip</a>; Old Mac is the course we&rsquo;d build a whole Bandon trip around."],
 {"Fee": "Day guests $180 (winter) to $425 (June&ndash;Sept) in 2026; resort guests $130&ndash;$375",
  "Walking": "Walking only. Caddies $125 a bag plus gratuity",
  "Fly into": "North Bend (OTH), 35 minutes, with United nonstops from Denver and San Francisco",
  "Watch for": "Day guests booking more than 21 days out pay a premium and get tee times after 10 a.m.",
  "Going alone": "The resort sells single rooms, and its trip planner has a &ldquo;Golf Trip &ndash; Solo&rdquo; option"},
 [("View from a high dune over hazy, sunlit links ground at Old Macdonald", "Dune country."),
  ("Sunset behind a dune ridge and Old Macdonald's bleached ghost tree", "The ghost tree at sunset."),
  ("A huge sleeper-faced cross bunker across a wide rolling fairway with the Pacific beyond", "Width, and then a bunker you have to deal with.")])

C["sweetens-cove"] = ("mind", "Sweetens Cove", "South Pittsburg, Tennessee", "King-Collins &middot; nine holes", "https://sweetenscovegolfclub.com/pages/daily-rates",
 "October view across Sweetens Cove's 5th with oaks and the Cumberland Plateau behind",
 "The 5th, seen from the 4th, in October.",
 ["Nine holes in a Tennessee valley, a shed for a clubhouse, and some of the boldest green contours in American golf. Rob Collins and Tad King built Sweetens Cove on the site of an old course, and the ground does things you don&rsquo;t expect. Holes 3 and 6 share one huge green that rises about 20 feet from end to end.",
  "The 4th is called King, after the late local golfer King Oehmig (no relation to Tad), who suggested a Himalayas hole. It plays anywhere from 90 to more than 200 yards off two huge tees set sideways to the line of play, into a 20,000-square-foot green. Play the nine again and it&rsquo;s a different course, which is the point of the all-day pass.",
  "The house rules are the best on this list: &ldquo;Wear whatever you want and bring your dog if you want to.&rdquo; Ran Morrissett, quoted by the club, put it best: &ldquo;If you leave [Sweetens Cove] smiling, don&rsquo;t panic, golf is supposed to be fun.&rdquo;"],
 {"Fee": "Through Dec 30, 2026: Thu&ndash;Sun all-day pass $100 walking. From Jan 2027: $240 walking in peak season, including food and a $150 deposit",
  "Walking": "Walk or ride. Cart-path only Nov&ndash;April",
  "Fly into": "Chattanooga (CHA) or Nashville (BNA)",
  "Watch for": "No walk-ons and no waitlist. 2027 passes go on sale at 5 p.m. Central, Nov 18&ndash;29, 2026. Closed Mondays",
  "Going alone": "The best setup on this list. One pass is one person; everyone meets at the shed around 8:30 for course notes and a shot of whiskey, then gets a starting hole"},
 [("Golfers in Adirondack chairs around a fire pit under string lights at Sweetens Cove", "After the round."),
  ("Top-down drone shot of Sweetens Cove's 4th green", "The 20,000-square-foot green at King."),
  ("A shaggy-lipped bunker with a flag and green mountain ridges behind at Sweetens Cove", "Bunkers with the Cumberland Plateau behind.")])

C["landmand"] = ("mind", "Landmand", "Homer, Nebraska", "King-Collins &middot; 2022", "https://www.landmandgc.com/",
 "Golden-hour drone view over Landmand's rumpled fairways to the clubhouse on the ridge",
 "Loess Hills farmland that hadn&rsquo;t been farmed in more than 30 years.",
 ["Landmand is Danish for farmer, and the course sits on 588 acres of the Andersen family&rsquo;s Nebraska land in the Loess Hills. There are almost no trees and no water. What there is, is width: fairways more than 100 yards across and greens averaging more than 14,000 square feet, with windsocks instead of flags.",
  "That width is the puzzle. With that much room, nothing tells you where to aim, so every shot is a choice of angle into greens with enormous slopes. Rob Collins described the site as &ldquo;this very raw, natural, tumbling landscape,&rdquo; and from the 12th tee you can see eight to ten other holes at once.",
  "Getting on is its own test. The Wall Street Journal called it America&rsquo;s toughest tee time, and all 11,000 tee times for 2026 sold out in 45 minutes. It&rsquo;s also fully public, with no members and no corporate outings. Its FAQ has the best line on this list: &ldquo;Walk 18? We&rsquo;ll buy your first beer.&rdquo;"],
 {"Fee": "$175 for 2027, cart included (club FAQ). $150 in 2026",
  "Walking": "Walking allowed, and they&rsquo;ll buy your first beer",
  "Fly into": "Sioux City (SUX), or Omaha (OMA), about 90 miles south",
  "Watch for": "The whole season goes on sale at once. 2027 runs May 15&ndash;Sept 30. Cancellations go through the Whoosh app waitlist",
  "Going alone": "Formal policy: a single gets paired with another single. Cabins and the Farmer&rsquo;s Table restaurant on site"},
 [("A yellow windsock flag on a Landmand green at sunset", "Windsocks instead of flags."),
  ("Aerial of a huge bunker-studded green complex at Landmand", "Greens average more than 14,000 square feet."),
  ("Low pass over native rough toward Landmand's 14th green", "The 14th.")])

C["erin-hills"] = ("body", "Erin Hills", "Erin, Wisconsin", "Hurdzan, Fry &amp; Whitten &middot; 2006", "https://erinhills.com/",
 "Elevated view over a big Erin Hills green and bunker toward rolling fescue hills at sunset",
 "652 acres of glacial land in the Kettle Moraine.",
 ["Erin Hills is the strictest walk on this list. It is walking only, and there are no push carts or pull carts, so you either carry your own bag or take a caddie. From the back tees it runs 7,715 yards, and it sprawls across 652 acres of glacial land shaped by the Kettle Moraine.",
  "The course sells its range of holes as &ldquo;from a terrifying 140 yard hole to a brute of 620,&rdquo; and it hosted the 2017 U.S. Open and the 2025 U.S. Women&rsquo;s Open. The fescue is long and golden, the walks between holes are real, and the club tells you to plan on four hours and 55 minutes.",
  "It is also one of the few places on this list built for someone traveling alone. The Lodge has seven single rooms out of eleven, steps from the first tee, and dining is limited to people with a tee time or a room, so the bar is full of people who just walked the same course you did."],
 {"Fee": "2026: $495 peak, $395 shoulder. 2027: $435&ndash;$555",
  "Walking": "Walking only, no push or pull carts. Caddie $65 plus a suggested $75 gratuity",
  "Fly into": "Milwaukee (MKE), 50 minutes. O&rsquo;Hare is two hours",
  "Watch for": "Season runs early May to mid-October. No twilight rates",
  "Going alone": "Seven single rooms at the Lodge. Single rooms are $395&ndash;$445 in 2027"},
 [("A group of golfers and caddies walking down a sloping Erin Hills fairway in evening light", "Caddies and players on the walk."),
  ("A dirt walking path through waist-high golden fescue toward a bunkered green", "The paths between holes are part of the round."),
  ("Aerial of tees, fairways and paths across rolling glacial terrain", "Glacial terrain from above.")])

C["whistling-straits"] = ("body", "Whistling Straits", "Haven, Wisconsin", "Pete Dye &middot; The Straits course", "https://www.destinationkohler.com/golf/whistling-straits/the-straits",
 "Golfers putting on a green perched on a bluff above Lake Michigan at Whistling Straits",
 "Two miles of Lake Michigan shoreline.",
 ["The Straits course is the longest course on this list: 7,790 yards from the back tees, rated 77.2 with a slope of 152, along two miles of rugged Lake Michigan shoreline. It is walking only, and the wind off the lake decides how long it plays on any given day.",
  "Pete Dye filled it with roughly a thousand bunkers, by Golf Digest&rsquo;s count. The holes have names that tell you what&rsquo;s coming. The 7th, Shipwreck, goes down to the shoreline. The 13th, Cliff Hanger, has a green on the cliff edge. The 15th starts a four-hole closing stretch the resort calls among the toughest in championship golf, and the 18th is called Dyeabolical.",
  "Dye, asked about it, said: &ldquo;Naah, this course is popcorn! But, sometimes people choke on popcorn.&rdquo; It hosted three PGA Championships and the 2021 Ryder Cup."],
 {"Fee": "Not published; Kohler shows it only in its booking system. Expect one of the highest fees on this list",
  "Walking": "Walking only. Caddies $90 plus a suggested $70 tip, recommended but not required",
  "Fly into": "Milwaukee (MKE), 72 miles, or Green Bay (GRB), 58 miles",
  "Watch for": "Twilight is 30% off rack; super twilight 45% off",
  "Going alone": "No published singles policy. Lodging is at The American Club in Kohler, about 20 minutes away"},
 [("The par-3 17th green, Pinched Nerve, on a lakeside bluff at Whistling Straits", "No. 17, Pinched Nerve."),
  ("The par-3 3rd green on a bluff edge with mist over the Lake Michigan shoreline", "The 3rd, in the mist."),
  ("Fog rolling off Lake Michigan over the 8th hole at dawn", "Dawn fog on the 8th.")])

C["bandon-trails"] = ("body", "Bandon Trails", "Bandon Dunes, Oregon", "Coore &amp; Crenshaw &middot; 2005", "https://bandondunesgolf.com/golf/golf-courses/bandon-trails-golf-course/",
 "From an elevated tee, Bandon Trails' 14th fairway drops into a bowl ringed by tall coastal forest",
 "The 14th, deep in the forest.",
 ["Reviewers who have walked every course at Bandon keep naming Trails as the hardest walk, and it doesn&rsquo;t even sit on the ocean. In the resort&rsquo;s words, it &ldquo;begins atop a massive sand dune, then quickly opens into a sprawling meadow,&rdquo; then &ldquo;works higher into the coastal forest&rdquo; before coming back down to finish in the dunes.",
  "The climbing is in the hole notes. The 1st goes &ldquo;slightly uphill through a saddle of sand dunes.&rdquo; The 7th is a long uphill par 4 to an elevated green. The 16th is an uphill par 5 into the prevailing wind that &ldquo;will play longer than the yardage indicates.&rdquo; The resort put water refill stations after the 3rd, 6th and 15th for a reason.",
  "It is 6,788 yards from the tips, par 71, and it is the quietest round at the resort. Out in the forest you can go several holes without seeing the ocean."],
 {"Fee": "Day guests $180&ndash;$425 in 2026 (same rate as every Bandon 18); resort guests $130&ndash;$375",
  "Walking": "Walking only. Caddies $125 a bag plus gratuity",
  "Fly into": "North Bend (OTH), 35 minutes",
  "Watch for": "2028 lodging goes by lottery; booking a day-guest time more than 21 days out costs the premium rate",
  "Going alone": "Single rooms, pubs and a solo trip option in the planner. Pair it with Old Macdonald from our Mind list"},
 [("Sand dunes and marram grass in golden light beside a Bandon Trails fairway", "The opening dune holes."),
  ("Low sun through dark forest behind a green at Bandon Trails", "Into the trees."),
  ("A tee in coastal scrub with a sandy path toward a distant green", "The trail between holes.")])

C["cabot-cliffs"] = ("body", "Cabot Cliffs", "Inverness, Nova Scotia", "Coore &amp; Crenshaw &middot; 6,835 yards", "https://cabot.com/capebreton/golf/cabot-cliffs/",
 "Golfers walking and putting on greens atop a red-rock sea cliff at Cabot Cliffs in golden light",
 "Greens on the cliff edge, Cape Breton.",
 ["Cabot&rsquo;s rule is short: &ldquo;We do not offer golf carts.&rdquo; Everyone walks, over ground that climbs from the dunes up onto sea cliffs on Cape Breton&rsquo;s west coast. The design team&rsquo;s own hole guide admits &ldquo;the conundrum during the design phase of Cabot Cliffs was whether we could make it work given the elevations.&rdquo;",
  "They made it work. The 9th is a short hole shaped by the crosswind, with the green right against the cliffs. The 16th, the one you&rsquo;ve seen in photos, plays to a green the guide says &ldquo;looks like it is hanging out over the ocean.&rdquo; The 18th crosses a ravine to a narrow, serpentine green. The resort describes spring and fall as &ldquo;misty rain and wind off the ocean.&rdquo;",
  "It&rsquo;s the only course on this list that needs a passport, and getting there is part of the effort: a two-hour drive from Sydney or three and a half from Halifax."],
 {"Fee": "Day guests C$565 (about US$413) in peak season, C$275&ndash;C$335 early and late, plus 14% tax",
  "Walking": "No carts at all. Caddies C$60&ndash;C$90, optional, booked 48 hours ahead",
  "Fly into": "Sydney (YQY), two hours by car or 22 minutes by helicopter. Halifax (YHZ) is three and a half hours",
  "Watch for": "The 2026 season ran May 8&ndash;Oct 25. Day-guest times are prepaid and non-refundable",
  "Going alone": "Day guests can book 14 days ahead. Cabot Bar is walk-in only, and Whit&rsquo;s Public House is in town"},
 [("A golfer carrying his own bag up Cabot Cliffs' 14th fairway", "Carrying your own on the 14th."),
  ("Aerial of greens on top of tall red and white cliffs with a long beach beyond", "The cliffs from the air."),
  ("Golfers on the 16th green atop a sheer cliff above the sea", "The 16th.")])

C["kiawah-ocean-course"] = ("body", "Kiawah Ocean Course", "Kiawah Island, South Carolina", "Pete &amp; Alice Dye &middot; 7,385 yards", "https://kiawahresort.com/golf/the-ocean-course/",
 "Aerial of Kiawah Ocean Course's 14th green in sandy dunes right above the Atlantic beach",
 "The 14th, the most exposed green on the course.",
 ["The Ocean Course is flat, and the resort itself calls it its easiest walk. It is on this list for the wind. Ten holes run along the Atlantic and the other eight parallel it, and the resort says a player &ldquo;can experience up to an 8-club difference on holes&rdquo; depending on how hard and which way it blows.",
  "Alice Dye suggested raising the course up out from behind the dunes, which left it exposed to the wind. Because Kiawah has no prevailing wind, Pete Dye designed &ldquo;two courses in one,&rdquo; one for an easterly and one for a westerly. On the 194-yard 14th, the most exposed green on the course, Dye expected players to need &ldquo;between a 2- and 4-iron.&rdquo;",
  "It is a physical test of a different kind: four-plus hours of leaning into it, on foot, with the sea in your ear the whole way."],
 {"Fee": "Not published; the resort shows rates only in its booking system",
  "Walking": "Walking only, except June&ndash;Aug after 10 a.m. with a forecaddie. No caddie fee; suggested $120 gratuity",
  "Fly into": "Charleston (CHS), about an hour and 20 minutes",
  "Watch for": "Non-guests book no sooner than 60 days out",
  "Going alone": "The resort says it pairs players up, so a single gets a game"},
 [("Sunset aerial of fairways between salt-marsh creeks and the Atlantic beach at Kiawah", "Marsh on one side, ocean on the other."),
  ("Low aerial over the sandy waste area short of Kiawah's 18th green", "Sand short of the 18th."),
  ("Low sun over the ocean behind a lagoon wrapping a green at Kiawah", "Late light over the lagoon.")])

C["wekopa-saguaro"] = ("spirit", "We-Ko-Pa Saguaro", "Fort McDowell Yavapai Nation, Arizona", "Coore &amp; Crenshaw &middot; 2006", "https://wekopa.com/saguaro-course/",
 "Elevated view down a We-Ko-Pa Saguaro fairway in low golden light with saguaros and bare mountains behind",
 "The Sonoran Desert, mostly left as it was.",
 ["We-Ko-Pa is owned by the Fort McDowell Yavapai Nation, and the club puts its appeal plainly: &ldquo;with no homes, roads, businesses or development of any kind, at We-Ko-Pa, it&rsquo;s just you, your ball and the sights and sounds of nature.&rdquo; Around Scottsdale, that is rare.",
  "Bill Coore and Ben Crenshaw walked the land for two months before they settled on a routing, and the club says &ldquo;hardly any dirt was moved.&rdquo; Tees and greens sit close together, and the club calls it one of just a few courses in Scottsdale built for walking. You play among hundreds of saguaros, which grow to 40 or 50 feet and live 150 to 175 years, with views of four mountain ranges: the Superstitions, the McDowells, the Mazatzals and Four Peaks.",
  "Crenshaw&rsquo;s line about the site: &ldquo;This ol&rsquo; boney ground has some sting to it.&rdquo; Roadrunners cross the fairways, hawks circle overhead and, in the club&rsquo;s words, the occasional coyote shows up in the distance."],
 {"Fee": "$239 through Jan 7, 2027; $329&ndash;$359 in peak season; $109 in summer. Plus 9% tax",
  "Walking": "Built for walking. The club provides Speedcart push carts",
  "Fly into": "Phoenix (PHX), about 20 minutes to the adjoining resort",
  "Watch for": "Closes for overseeding each October. The adjoining resort is a casino",
  "Going alone": "Book online up to 90 days ahead. The club says it uses no dynamic pricing"},
 [("Saguaros silhouetted against a low sun with a cholla in front", "Saguaros at last light."),
  ("A We-Ko-Pa fairway and green under a big sky with mountains behind", "Four mountain ranges in view."),
  ("Drone view of narrow fairways threaded through open Sonoran desert", "Fairways threaded through the desert.")])

C["silvies-valley-ranch"] = ("spirit", "Silvies Valley Ranch", "Seneca, Oregon", "Dan Hixson &middot; 2017", "https://silvies.us/golf-at-silvies-valley-ranch/",
 "Sun setting over the valley behind a bunkered green framed by sagebrush and pines at Silvies Valley Ranch",
 "Craddock No. 4, about 5,000 feet up.",
 ["This is the most remote place on the list and the quietest. Silvies is a working cattle and goat ranch of more than 150,000 acres in eastern Oregon, at about 5,000 feet, which makes it what the ranch calls the highest course in Oregon. There is no cell service. The ranch&rsquo;s own advice to golfers: &ldquo;it is a long way to the hospital &ndash; please don&rsquo;t overdo it.&rdquo;",
  "Dan Hixson built two reversible 18s, Craddock and Hankins, which play the same ground in opposite directions. Then there is McVeigh&rsquo;s Gauntlet, seven holes on a ridge where the caddies are goats carrying your bag. The owners describe a long-running habitat restoration for wildlife and fish, and elk graze the valley.",
  "FORE Magazine put it best: &ldquo;But if you want to be alone and unbothered, Silvies Valley Ranch is pure gold.&rdquo;"],
 {"Fee": "Not published. Day guests pay a daily resort fee with a cart included; call the ranch at (541) 573-5150",
  "Walking": "&ldquo;Walking is permitted and encouraged,&rdquo; with free pull carts. No carts on McVeigh&rsquo;s Gauntlet",
  "Fly into": "Boise, Redmond or Portland, then drive. The ranch will pick up at Burns or John Day",
  "Watch for": "Season runs early May to the end of October. Day visits need a reservation and deposit",
  "Going alone": "The best solo stay on the list: single-king Rancher&rsquo;s Suites and, per a 2021 FORE Magazine visit, nightly communal dinners"},
 [("A golfer hits while a handler holds a goat carrying a leather golf bag at Silvies", "A goat caddie on McVeigh&rsquo;s Gauntlet."),
  ("A bull elk with a herd on open grassland below forested hills", "The neighbors."),
  ("Aerial of a creek meandering across a broad valley floor", "The valley from above.")])

C["black-mesa"] = ("spirit", "Black Mesa", "Santa Clara Pueblo, New Mexico", "Baxter Spann &middot; 2003", "https://golfblackmesa.com/",
 "Low golden light across a Black Mesa fairway with eroded badland ridges and a long mesa",
 "High desert north of Santa Fe.",
 ["Golf Digest&rsquo;s description of Black Mesa is hard to beat: &ldquo;there is no development on or near the vast, high-desert property.&rdquo; The course runs through buttes, sagebrush ridges and dry arroyos. It is owned by Santa Clara Pueblo, 25 miles north of Santa Fe, with the Sangre de Cristo Mountains in view.",
  "Arroyos come into play on ten of the eighteen holes. The 4th has one fourteen feet deep; on the 18th, one runs the whole length of the hole. Architect Baxter Spann called it &ldquo;the most interesting and spectacular site I have ever had the opportunity to work with.&rdquo; His note on the 1st hole gave this story its opening line.",
  "It is also the cheapest course in our Spirit section, at about $91 on a weekday with a cart."],
 {"Fee": "About $91 weekday, $110 weekend with cart (club booking page, Oct 2026)",
  "Walking": "Every online rate includes a cart; call the club about walking",
  "Fly into": "Santa Fe (SAF) or Albuquerque (ABQ)",
  "Watch for": "Open Thursday&ndash;Monday only",
  "Going alone": "The hard one here. Singles are paired into foursomes; to play alone you pay for all four spots"},
 [("A dark basalt-capped mesa rising over a Black Mesa fairway", "The 2nd, under the mesa."),
  ("Panorama of a green beside a reed-fringed pond below pale eroded cliffs", "Pond and cliffs."),
  ("A dirt cart path curling through a green valley between sage-covered hills", "Paths kept mostly out of sight.")])

C["northwood"] = ("spirit", "Northwood", "Monte Rio, California", "Alister MacKenzie &middot; 1928 &middot; nine holes", "https://www.northwoodgolf.com/",
 "Morning mist and light shafts among tall redwood trunks at the edge of a Northwood fairway",
 "MacKenzie in the redwoods.",
 ["Northwood is nine holes of Alister MacKenzie routing in a grove of redwoods on the Russian River. Jack Neville, a Bohemian Club member, came up with the idea of a course on 70 wooded acres across the river from the Bohemian Grove, and he brought in MacKenzie and Robert Hunter, who designed it in 1928.",
  "It is not remote, and it is not grand. It sits on a highway in a small river town, there are homes around it, and GOLF.com&rsquo;s Noel Freeman wrote that it &ldquo;could use some restorative touches.&rdquo; He also called it &ldquo;a period piece and a wonderful walk amid arboreal splendor,&rdquo; which is why it&rsquo;s here. Redwood trunks line the holes, and in the morning the light comes through them in shafts.",
  "Treat it as a day, not a week: walk 18 by going around twice, then spend the rest of the trip on the Sonoma coast."],
 {"Fee": "Walking 18 from $49 weekday, $57 weekend; nine from $33",
  "Walking": "Walking is the default rate. Pull carts $6",
  "Fly into": "Santa Rosa (STS), or San Francisco and drive north",
  "Watch for": "Nine holes only. Players must be off the course by 7:30 p.m.",
  "Going alone": "Cheap, short and easy to fit in. The club lists nearby inns, some with golf packages"},
 [])

C["sand-valley"] = ("spirit", "Sand Valley", "Nekoosa, Wisconsin", "Coore &amp; Crenshaw &middot; 2017", "https://sandvalley.com/golf-courses/sand-valley",
 "Soft evening light over Sand Valley's rolling fairways, sandy blowouts and scrubby dunes with woods behind",
 "Sand barrens in central Wisconsin.",
 ["Sand Valley sits in an ancient glacial lakebed in central Wisconsin, on ground that had been planted over as a red pine plantation. The resort&rsquo;s owners pulled the pines and started bringing the sand barrens back: a Field Museum guide counts 250 acres of sand barrens and prairie being restored, plus 200 acres of oak savanna and jack pine managed with fire, as habitat for creatures like the Karner blue butterfly.",
  "The original Coore &amp; Crenshaw course came out of that ground in 2017, and the resort sells it as &ldquo;The original course that&rsquo;s like golfing in a national park.&rdquo; Blowout bunkers, scrub and big open sky, on 12,000 acres in all. The Field Museum guide opens with Aldo Leopold, whose <em>A Sand County Almanac</em> was written about Wisconsin&rsquo;s sand country.",
  "It&rsquo;s a big resort now, with more courses and real estate for sale, so it isn&rsquo;t empty. But play the original late in the day and it gets very quiet. That&rsquo;s our hero photo up top."],
 {"Fee": "$325 May 21&ndash;Oct 4; $235 in late April&ndash;May and October (2026)",
  "Walking": "Walking only. Caddies usually carry two bags",
  "Fly into": "Central Wisconsin (CWA), 1 hour 5 minutes; Madison (MSN), 1 hour 40",
  "Watch for": "Seasonal. The Lido course is for resort guests only",
  "Going alone": "Golf-only tee times are bookable without a stay. Plenty of communal restaurants and bars"},
 [("A wide green with sand faces under a streaked orange sunset at Sand Valley", "Sunset on the original course."),
  ("Wooden Adirondack chairs looking over the course as sun rays break through cloud", "The view from the chairs."),
  ("A monarch butterfly on a purple blazing-star wildflower", "Restored prairie, and who lives there.")])

PILLARS = [
 ("mind", "Mind", "I", "Courses that make you think about the game differently.",
  "Blind shots, no out of bounds, template holes, fairways a hundred yards wide. These five courses are puzzles more than tests, and each one makes you decide what you&rsquo;re looking at before you decide what to hit.",
  "Drone view over Bethpage fairway bunkers toward the clubhouse", ["tobacco-road", "bethpage-black", "old-macdonald", "sweetens-cove", "landmand"]),
 ("body", "Body", "II", "Courses that test you physically.",
  "Long walks with no carts, climbs from dunes into forest, cliffs, bluffs and wind. You&rsquo;ll feel these five the next morning.",
  "Sunrise over the Cape Breton highlands and a forested valley above the shore", ["erin-hills", "whistling-straits", "bandon-trails", "cabot-cliffs", "kiawah-ocean-course"]),
 ("spirit", "Spirit", "III", "Courses that quiet everything down.",
  "Desert with no houses, a ranch with no cell service, Pueblo land, redwoods and restored sand barrens. These are the places where the landscape is the point and the golf follows it.",
  "Sunburst over a wide valley with a green among sagebrush and pines at Silvies", ["wekopa-saguaro", "silvies-valley-ranch", "black-mesa", "northwood", "sand-valley"]),
]

PQ = {
 "tobacco-road": ("Some courses start off with a handshake; Mike Strantz gives you a stiff upper-cut.", "Tobacco Road hole guide, on the 1st"),
 "cabot-cliffs": ("This is a hole that just cried out, &lsquo;Here I am.&rsquo;", "Cabot Cliffs hole guide, on the 18th"),
 "silvies-valley-ranch": ("Due to our rural location, there is no cell service on the ranch.", "Silvies Valley Ranch FAQ"),
}

INTRO = """
<section class="mbs-intro">
  <p class="mbs-epi">&ldquo;A great course tests both the mind and the body.&rdquo;<span>&mdash; Baxter Spann, architect of Black Mesa</span></p>
  <div class="mbs-lede">
    <p>Most golf trips get planned around a list: the famous courses, the rankings, the places your friends have been. This one is planned around what you need. Some trips are for your head, a course that makes you rethink how the game is supposed to be played. Some are for your body, a walk long and hard enough that the score stops mattering. And some are for something quieter, a place so beautiful and so empty that you forget to check your phone.</p>
    <p>Every course here is open to the public, either fully public or a resort that lets day guests book a tee time. Each one is good enough to build a trip around. We&rsquo;ve sorted fifteen of them into Mind, Body and Spirit, with the fee, the walking rules, the nearest airport and what to watch out for.</p>
    <p>We&rsquo;d also make the case for going alone. A solo trip means you set the pace, play when the light is best and get paired with strangers who often turn out to be the best part of the day. Several of these courses are built for it: Sweetens Cove sells passes one person at a time, Landmand pairs singles with singles, and Erin Hills and Silvies keep single rooms. For every course we&rsquo;ve noted how it works if you show up by yourself.</p>
  </div>
</section>
"""

SOLO = """
<section class="mbs-solo">
  <h2 class="mbs-h2" id="going-alone">Going Alone: What We&rsquo;d Tell a Friend</h2>
  <div class="mbs-solo-grid">
    <div><h3>Pick the right course</h3><p>Some courses are set up for a single. Sweetens Cove sells one pass per person and starts everyone together with a whiskey shot. Landmand pairs singles with singles, and Kiawah says it pairs players up. Black Mesa is the exception: there, playing alone means paying for the whole foursome.</p></div>
    <div><h3>Book the room first</h3><p>Erin Hills has seven single rooms in its Lodge. Bandon sells single rooms and has a solo option in its trip planner. Silvies has single-king suites. At a walking resort with a pub, you won&rsquo;t eat dinner alone unless you want to.</p></div>
    <div><h3>Take the caddie</h3><p>On a walking-only course, a caddie is company and local knowledge in one. Bandon ($125), Erin Hills ($65), Whistling Straits ($90) and Cabot (C$60&ndash;C$90) all have caddie programs, and Kiawah charges no caddie fee, just a gratuity.</p></div>
    <div><h3>Play the windows</h3><p>The hard tee times are easier for one. Bethpage hands out walk-up times to whoever is in line, and a single fits into gaps a foursome can&rsquo;t. And the last tee times of the day are the quietest golf anywhere.</p></div>
  </div>
</section>
"""

FAQ = [
 ("What is the best public golf course to play alone?", "Sweetens Cove in Tennessee is the most solo-friendly on our list: passes are sold one person at a time, everyone meets for course notes and a shot of whiskey, and each player is assigned a starting hole. Landmand in Nebraska formally pairs single golfers together, and Erin Hills and Silvies Valley Ranch have single rooms."),
 ("Which of these courses are walking only?", "Bethpage Black, Old Macdonald and Bandon Trails, Erin Hills (no push or pull carts either), Whistling Straits, Cabot Cliffs, Sand Valley and the Kiawah Ocean Course (except summer afternoons with a forecaddie)."),
 ("Can you play Bethpage Black if you don't live in New York?", "Yes. Non-residents book online five days ahead from 7 p.m., limited to one Black round every 28 days, and pay $140 on weekdays or $160 on weekends. Walk-up times go to whoever is in line in the morning."),
 ("What is the cheapest course on this list?", "Northwood in Monte Rio, California: walking 18 starts at $49 on weekdays. Black Mesa in New Mexico is about $91 on a weekday with a cart, and Sweetens Cove's Thursday-to-Sunday all-day pass is $100 walking through Dec 30, 2026."),
 ("Can non-guests play Bandon Dunes, Cabot and Sand Valley?", "Yes. Bandon day guests paid $180 to $425 in 2026, depending on the month. Cabot Cliffs day guests book up to 14 days ahead at C$565 in peak season. Sand Valley sells golf-only tee times at $235 to $325."),
 ("Why isn't Pinehurst No. 2 on the list?", "Pinehurst No. 2 is open only to members and resort guests, so it doesn't meet our rule that every course takes outside tee times. Non-guests can walk on to The Cradle short course year-round."),
]

CSS = """<style>/*TGI-MBS*/
.mbs-hero{position:relative;width:100%;max-width:1600px;margin:0 auto 8px;padding:0 32px}
.mbs-hero img{width:100%;aspect-ratio:16/8;object-fit:cover;object-position:50% 45%;display:block;border:.5px solid var(--ink)}
.mbs-cap{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-intro{max-width:1100px;margin:56px auto 24px;padding:0 32px;display:grid;grid-template-columns:1fr 2fr;gap:56px;align-items:start}
.mbs-epi{font-family:var(--serif);font-size:30px;line-height:1.2;color:var(--grass);border-top:.5px solid var(--ink);padding-top:18px}
.mbs-epi span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:14px}
.mbs-lede p{font-family:var(--serif);font-size:19px;line-height:1.6;margin-bottom:18px}
.mbs-lede p:first-child::first-letter{font-size:64px;float:left;line-height:.9;padding:6px 10px 0 0;color:var(--grass)}
.mbs-toc{max-width:1400px;margin:48px auto;padding:0 32px;display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}
.mbs-toc>div{padding:24px 28px;border-right:.5px solid rgba(20,20,20,.2)}.mbs-toc>div:last-child{border-right:none}
.mbs-toc h3{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.14em;font-size:22px;color:var(--grass);margin-bottom:6px}
.mbs-toc p{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.55;margin-bottom:14px}
.mbs-toc ol{list-style:none;padding:0;margin:0;counter-reset:t}.mbs-toc li{font-family:var(--serif);font-size:17px;padding:5px 0;border-bottom:.5px dotted rgba(20,20,20,.2)}
.mbs-toc li a{border-bottom:none}.mbs-toc li span{font-family:var(--mono);font-size:10px;opacity:.5;margin-right:10px}
.mbs-open{position:relative;max-width:1600px;margin:96px auto 0;padding:0 32px}
.mbs-open img{width:100%;aspect-ratio:21/9;object-fit:cover;display:block;filter:brightness(.72)}
.mbs-open .t{position:absolute;left:32px;right:32px;bottom:0;padding:0 48px 44px;color:#F4F1EA}
.mbs-open .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.85}
.mbs-open h2{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.16em;font-size:clamp(48px,9vw,128px);line-height:1;margin:8px 0 10px}
.mbs-open .d{font-family:var(--serif);font-size:22px;max-width:640px}
.mbs-pill{max-width:820px;margin:36px auto 0;padding:0 32px;font-family:var(--serif);font-size:20px;line-height:1.55;text-align:center;opacity:.85}
.mbs-c{max-width:1400px;margin:96px auto 0;padding:0 32px}
.mbs-c-hd{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:end;border-bottom:.5px solid var(--ink);padding-bottom:14px;margin-bottom:20px}
.mbs-c-hd .num{font-family:var(--serif);font-size:84px;line-height:.8;color:var(--grass)}
.mbs-c-hd h3{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,48px);line-height:1;letter-spacing:-.01em}
.mbs-c-hd .where{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.mbs-lead img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.mbs-body{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:56px;margin-top:32px}
.mbs-text p{font-family:var(--serif);font-size:18px;line-height:1.65;margin-bottom:18px}
.mbs-text a{border-bottom:1px solid currentColor}
.mbs-facts{border:.5px solid var(--ink);padding:22px 24px;align-self:start;background:rgba(45,74,43,.04)}
.mbs-facts .k{font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;opacity:.5;margin-top:14px}
.mbs-facts .k:first-child{margin-top:0}.mbs-facts .v{font-family:var(--serif);font-size:15px;line-height:1.45;margin-top:3px}
.mbs-facts .v.solo{color:var(--grass)}
.mbs-facts a.go{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px}
.mbs-mos{display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:1fr 1fr;gap:12px;margin-top:36px;height:min(64vw,760px)}
.mbs-mos.flip{grid-template-columns:1fr 1.25fr}
.mbs-mos figure{margin:0;position:relative;overflow:hidden;min-height:0}
.mbs-mos figure:first-child{grid-row:1/3}.mbs-mos.flip figure:first-child{grid-column:2}.mbs-mos.flip figure:nth-child(2){grid-column:1;grid-row:1}.mbs-mos.flip figure:nth-child(3){grid-column:1;grid-row:2}
.mbs-mos img{width:100%;height:100%;object-fit:cover;display:block}
.mbs-mos figcaption{position:absolute;left:0;bottom:0;right:0;padding:24px 14px 10px;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#F4F1EA;background:linear-gradient(transparent,rgba(0,0,0,.55))}
.mbs-lead figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-solo{max-width:1400px;margin:120px auto 0;padding:48px 32px 0;border-top:.5px solid var(--ink)}
.mbs-h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,44px);margin-bottom:28px}
.mbs-solo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.mbs-solo h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:10px}
.mbs-solo p{font-family:var(--serif);font-size:16px;line-height:1.55}
.mbs-table{max-width:1400px;margin:72px auto 0;padding:0 32px;overflow-x:auto}
.mbs-table table{width:100%;border-collapse:collapse;font-family:var(--serif);font-size:15px}
.mbs-table th{font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;text-align:left;padding:10px 12px;border-bottom:.5px solid var(--ink);opacity:.7}
.mbs-table td{padding:11px 12px;border-bottom:.5px solid rgba(20,20,20,.15);vertical-align:top}
.mbs-table td.p{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--grass)}
@media(max-width:900px){.mbs-intro{grid-template-columns:1fr;gap:28px}.mbs-toc{grid-template-columns:1fr}.mbs-toc>div{border-right:none;border-bottom:.5px solid rgba(20,20,20,.2)}
.mbs-body{grid-template-columns:1fr;gap:28px}.mbs-solo-grid{grid-template-columns:1fr 1fr}.mbs-open img{aspect-ratio:4/3}.mbs-open .t{padding:0 22px 26px}}
@media(max-width:600px){.mbs-hero,.mbs-intro,.mbs-toc,.mbs-open,.mbs-c,.mbs-solo,.mbs-table,.mbs-pill{padding-left:18px;padding-right:18px}
.mbs-open .t{left:18px;right:18px}.mbs-hero img{aspect-ratio:4/3}.mbs-c-hd .num{font-size:56px}.mbs-solo-grid{grid-template-columns:1fr}
.mbs-mos,.mbs-mos.flip{grid-template-columns:1fr 1fr;grid-template-rows:auto auto;height:auto}
.mbs-mos figure:first-child,.mbs-mos.flip figure:first-child{grid-column:1/3;grid-row:1;aspect-ratio:4/3}.mbs-mos figure:nth-child(2),.mbs-mos.flip figure:nth-child(2){grid-column:1;grid-row:2;aspect-ratio:1}.mbs-mos figure:nth-child(3),.mbs-mos.flip figure:nth-child(3){grid-column:2;grid-row:2;aspect-ratio:1}
.mbs-lede p{font-size:17px}.mbs-text p{font-size:17px}}
</style>
"""

ORDER = [k for p in PILLARS for k in p[6]]


def course_html(k, n, flip):
    pil, name, place, des, url, lalt, lcap, paras, facts, mos = C[k]
    fx = "".join(f'<div class="k">{H.escape(lbl)}</div><div class="v{" solo" if lbl == "Going alone" else ""}">{v}{"" if v.endswith(".") else "."}</div>' for lbl, v in facts.items())
    text = "".join(f"<p>{p}</p>" for p in paras)
    mosaic = ""
    if mos:
        figs = "".join(f'<figure><img src="{IMG}/{k}-{i+2}.jpg" alt="{H.escape(a, quote=True)}" loading="lazy" /><figcaption>{c}</figcaption></figure>' for i, (a, c) in enumerate(mos))
        mosaic = f'<div class="mbs-mos{" flip" if flip else ""}">{figs}</div>'
    q = ""
    if k in PQ:
        qq, who = PQ[k]
        q = (f'\n<div class="pull-quote" style="margin:72px auto 0"><div class="pull-quote-inner">&ldquo;{qq}&rdquo;'
             f'<span class="pull-quote-attr">&mdash; {who}</span></div></div>\n')
    return (f'\n<article class="mbs-c" id="{k}">\n  <div class="mbs-c-hd"><div class="num">{n:02d}</div><div><h3>{name}</h3>'
            f'<div class="where">{place} &middot; {des}</div></div></div>\n'
            f'  <figure class="mbs-lead"><img src="{IMG}/{k}-1.jpg" alt="{H.escape(lalt, quote=True)}" loading="lazy" /><figcaption>{lcap} Photo: {name}</figcaption></figure>\n'
            f'  <div class="mbs-body"><div class="mbs-text">{text}</div><aside class="mbs-facts">{fx}'
            f'<a class="go" href="{url}" target="_blank" rel="noopener">Book at {name} &#8599;</a></aside></div>\n  {mosaic}\n</article>\n{q}')


def toc_html():
    cols = []
    n = 1
    for key, name, roman, line, _, _, ids in PILLARS:
        lis = ""
        for k in ids:
            lis += f'<li><span>{n:02d}</span><a href="#{k}">{C[k][1]}</a></li>'
            n += 1
        cols.append(f'<div><h3><a href="#{key}" style="border-bottom:none">{name}</a></h3><p>{line}</p><ol>{lis}</ol></div>')
    return f'\n<nav class="mbs-toc" aria-label="The fifteen courses">{"".join(cols)}</nav>\n'


def table_html():
    rows = ""
    short = {
     "tobacco-road": ("NC", "~$250 (dynamic)", "Cart included", "Travel desk books singles"),
     "bethpage-black": ("NY", "$140&ndash;$160", "Walking only", "Walk-up line"),
     "old-macdonald": ("OR", "$180&ndash;$425", "Walking only", "Single rooms"),
     "sweetens-cove": ("TN", "$100&ndash;$240 day pass", "Walk or ride", "One pass, one person"),
     "landmand": ("NE", "$175 (2027)", "Walk or ride", "Singles paired"),
     "erin-hills": ("WI", "$395&ndash;$495", "Walking only, no carts", "7 single rooms"),
     "whistling-straits": ("WI", "Not published", "Walking only", "No policy published"),
     "bandon-trails": ("OR", "$180&ndash;$425", "Walking only", "Single rooms"),
     "cabot-cliffs": ("NS, Canada", "C$275&ndash;C$565", "No carts", "Walk-in bar"),
     "kiawah-ocean-course": ("SC", "Not published", "Walking only (most of the year)", "Resort pairs players"),
     "wekopa-saguaro": ("AZ", "$109&ndash;$359", "Built for walking", "Flat pricing"),
     "silvies-valley-ranch": ("OR", "Call the ranch", "Walking encouraged", "Single suites, communal dinners"),
     "black-mesa": ("NM", "~$91&ndash;$110", "Cart included", "Pay for 4 to play alone"),
     "northwood": ("CA", "From $49", "Walking", "Short and cheap"),
     "sand-valley": ("WI", "$235&ndash;$325", "Walking only", "Golf-only times"),
    }
    for p in PILLARS:
        for k in p[6]:
            st, fee, walk, solo = short[k]
            rows += f'<tr><td class="p">{p[1]}</td><td><a href="#{k}" style="border-bottom:none">{C[k][1]}</a></td><td>{st}</td><td>{fee}</td><td>{walk}</td><td>{solo}</td></tr>'
    return (f'\n<section class="mbs-table"><h2 class="mbs-h2" id="at-a-glance">All Fifteen at a Glance</h2><table><thead><tr>'
            f'<th>Pillar</th><th>Course</th><th>Where</th><th>Fee</th><th>Walking</th><th>Going alone</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<p class="mbs-cap" style="margin-top:12px">Fees are 2026 unless noted, checked October 27, 2026. Day-guest rates for resorts.</p></section>\n')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:72px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": C[k][4], "name": H.unescape(C[k][1])} for i, k in enumerate(ORDER)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-27", "dateModified": "2026-10-27",
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


def main(apply_):
    assert len(ORDER) == N == len(set(ORDER)) and set(ORDER) == set(C), set(C) ^ set(ORDER)
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
    <span>Field Note</span><span class="dot"></span>
    <span>15 public courses &middot; fees checked October 27, 2026</span>
  </div>
</header>

<div class="mbs-hero"><img src="{IMG}/hero.jpg" alt="A lone golfer mid-backswing on a crest of fairway at dusk at Sand Valley, Wisconsin, under a wide pale sky" fetchpriority="high" />
<div class="mbs-cap">A late round, alone, at Sand Valley in Wisconsin. Photo: Sand Valley</div></div>
"""
    body += INTRO + toc_html()
    n = 1
    for key, name, roman, line, para, alt, ids in PILLARS:
        body += (f'\n<section class="mbs-open" id="{key}"><img src="{IMG}/open-{key}.jpg" alt="{H.escape(alt, quote=True)}" loading="lazy" />'
                 f'<div class="t"><div class="n">Part {roman} &middot; {len(ids)} courses</div><h2>{name}</h2><div class="d">{line}</div></div></section>\n'
                 f'<p class="mbs-pill">{para}</p>\n')
        for j, k in enumerate(ids):
            body += course_html(k, n, j % 2 == 1)
            n += 1
    body += SOLO + table_html()  # Lenny 27 Oct: "let's remove the questions section at the bottom"
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    print(f"  {n-1} courses")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    if fin.count('class="mbs-c"') != N: bad.append("course count")
    for w in ("worth", "genuinely", "honestly", "straightforward"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
