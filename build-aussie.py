#!/usr/bin/env python3
"""Rebuild the Aussie golf post as a brands + courses + trips guide.

Replaces the thin legacy /drops/3-aussie-golf-brands-you-should-know (1,092 words,
no sections, no FAQ, legacy card markup). Old slug gets a 301 -> new slug.

SOURCING RULES (all research verified 2026-08-24, dossier at /tmp/au/courses.md):
  * Every green fee is either [OFFICIAL from the club] or explicitly marked unpublished.
    Only ONE Sandbelt club (Woodlands) publishes a fee. Do not invent the others.
  * Rankings are Golf Digest World's 100 Greatest 2026-27 unless stated.
  * MacKenzie routed exactly ONE Sandbelt course (Royal Melbourne West). Do not
    repeat the American myth that he designed the whole Sandbelt.
  * Ellerston's price is 8AM Travel's published figure, not the club's. Attribute it.
  * No course photography — nothing rights-clean was available. Courses run as a
    designed text treatment using the .trip* classes defined in EXTRA_CSS.
  * All brand prices are AUD base currency, verified via Shopify.currency.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open("/tmp/au/man.json"))
TRIPIMG = json.load(open("/tmp/au/tripimgs.json"))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-left-of-field-golf.html")
OUT  = os.path.join(ROOT, "drops", "australian-golf-brands-and-trips.html")
SLUG = "australian-golf-brands-and-trips"
TITLE = "Golf in Australia &mdash; Ten Brands to Know, and Twelve Trips You Can Actually Book"
TITLE_TXT = "Golf in Australia — Ten Brands to Know, and Twelve Trips You Can Actually Book"
DESC = ("Ten independent Australian golf brands, and twelve organised trips you can book \u2014 from "
        "Random Golf Club's Australia Major to a charter plane that lands at the course.")
AUD = 0.717
def usd(a): return int(round(float(a) * AUD))

# ---------------------------------------------------------------- brands
BRANDS = {
"lof": dict(name="Left of Field Golf", city="Sydney, NSW", dom="lofgolf.com",
  meta="Est. 2022", imgdir="left-of-field", frames=[
    "xelements-polo-0-0.jpg","xbass-polo-black-1-0.jpg","xelements-polo-0-2.jpg",
    "xbass-polo-black-1-2.jpg","xelements-polo-0-3.jpg"],
  desc="The one that opened the door for most of the others. Nick Ilias started it in his brother&rsquo;s old "
       "bedroom in 2022, and the brief was never golf clothing: it was surf and skate silhouettes that happened "
       "to work on a course. In his words, &ldquo;our mission isn&rsquo;t to create products that scream "
       "&lsquo;golf&rsquo;.&rdquo; Every collection is named for a stretch of Australian coast &mdash; Elements "
       "for Barnbougle in Tasmania, SOUTH for the Mornington Peninsula, RNP for Royal National Park below Sydney. "
       "They also publish a sustainability page committing to recycled-PET yarn, which almost nobody at this size does."),
"walker": dict(name="Walker Golf Things", city="Gold Coast, QLD", dom="walkergolfthings.com",
  meta="First drop July 2022", imgdir="walker-blooming-grounds", frames=[
    "blooming-grounds-knit-polo-1-0.jpg","gardener-ss-shirt-5-0.jpg","hedge-hood-4-0.jpg",
    "blooming-grounds-t-shirt-3-0.jpg"],
  desc="Founded by Jack Fardell, a professional skateboarder whose father named him after Jack Nicklaus &mdash; "
       "&ldquo;I didn&rsquo;t really have a choice but to play golf.&rdquo; He has ridden for adidas Skateboarding "
       "since 2015, which is how a small Gold Coast label ended up with an adidas Golf capsule in 2024, built "
       "around a co-designed MC-Z Traxion shoe. The most prolific brand here by a distance, and the most "
       "collaborative &mdash; Evan Mock&rsquo;s Wahine, Coopers the brewery, and Shortees, the floodlit Sydney par-three."),
"penta": dict(name="Penta Golf", city="Northern Beaches, Sydney", dom="penta-golf.com",
  meta="Founders not published", imgdir="aussie", frames=None,
  desc="Three friends who met working at a creative print magazine and a youth-culture agency, and who have never "
       "put their names on the site. It shows in the product &mdash; the Etiquette Pants and the PXB line with "
       "Barnaby&rsquo;s read like a magazine art department made golf clothes. Asked where they play, the answer "
       "was refreshingly specific: &ldquo;anywhere on the Northern Beaches&hellip; but Warringah Golf Club is our "
       "local. Shout out to Rob and Greg at the Pro Shop.&rdquo; One flag: their last drop was December 2025, so "
       "the range is stocked but static."),
"midiron": dict(name="Midiron", city="Australia", dom="midiron.shop",
  meta="First product Dec 2025", imgdir="midiron", frames=[
    "detour-stripe-polo-5.jpg","results-cap-black-1.jpg","tour-spec-polo-tree-camo-0.jpg",
    "the-big-stick-headcover-4.jpg","tour-spec-cap-black-1.jpg"],
  desc="The newest and smallest, and the one that names nobody at all. Nine products in eight months, most of it "
       "shot at night under a hard flash on a floodlit par-three. Every second product page signs off &ldquo;Golf "
       "Apparel Research approved,&rdquo; which reads like an endorsement until you realise Golf Apparel Research "
       "is their own house name. The best thing they have made is a reworked vintage Titleist cap, sold as three "
       "one-offs, with an unsigned story about a grandad&rsquo;s hand-me-down underneath it."),
"birds": dict(name="Birds of Condor", city="Byron Bay, NSW", dom="birdsofcondor.com",
  meta="Founded by Frankie &amp; Zoe Kimpton", imgdir="aussie", frames=None,
  desc="The most established brand on this list and the one you have probably already seen. Frankie Kimpton was a "
       "booking agent at Mushroom Records, sneaking out at lunch to hit balls at Albert Park &mdash; &ldquo;I think "
       "it was 20 bucks for a bucket of balls and a beer&rdquo; &mdash; in black jeans and a Guns N&rsquo; Roses "
       "shirt. The first drop was ten hats. It is now several hundred products, a Culture Kings stockist list, and "
       "a Byron Bay flagship containing a restored 1980s buggy from Sanctuary Cove."),
"okka": dict(name="Okka Golf", city="Perth, WA", dom="okkagolf.com",
  meta="Founder: Kalani", imgdir="aussie", frames=None,
  desc="Screen-printed by one person in Perth, and militantly kept that way. Asked about wholesale, the answer on "
       "their own site is &ldquo;no bueno amigo. not something i do. i&rsquo;m extremely protective of the "
       "relationship i have with frens of OKKA.&rdquo; The stated aim is the opposite of a pitch deck: not "
       "&ldquo;changing the game,&rdquo; not a vanity project. The photography is the giveaway &mdash; every piece "
       "shot the same way on the same backdrop, like a lookbook made by someone who only owns one light."),
"grayhaast": dict(name="Gray + Haast", city="Burleigh Heads, QLD", dom="grayandhaast.com",
  meta="Founder surname only", imgdir="aussie", frames=None,
  desc="The most conventionally handsome clothing here, and the best name. Gray is the founder&rsquo;s surname; "
       "Haast is for the Haast&rsquo;s eagle, the largest eagle known to have existed and a decent joke about the "
       "score every golfer is chasing and never makes. The Peninsula long-sleeve polo and the Performance Shell are "
       "the pieces to start with. Stocked at Noosa Golf Co, and dropping regularly &mdash; there was new product "
       "on the site the day we wrote this."),
"found": dict(name="Found Golf", city="Melbourne, VIC", dom="found.golf",
  meta="Est. 2022", imgdir="aussie", frames=None,
  desc="Barely a clothing brand. Lance Peach and Ellen Keillar have been running it since 2022, and thirty-five of "
       "their fifty-eight products are art rather than apparel &mdash; paintings, sculpture, a bench listed at "
       "nearly six thousand dollars. The clothing that does exist is made, where possible, with boutique ateliers "
       "in Cape Town. Ex-AFL player Dale Thomas is their creative partner. They also sell golf tees in a reusable "
       "cigarette box, which tells you the register."),
"mackem": dict(name="Mackem Golf", city="Kalamunda, WA", dom="mackemgolf.com",
  meta="Adam Brown &amp; Paige Harding", imgdir="aussie", frames=None,
  desc="Wool-blend headcovers and waxed-canvas pouches, all sewn in-house in the Perth hills, with a real shop on "
       "Haynes Street you can walk into. Their bespoke work has turned football shirts, wedding suits and "
       "boardshorts into covers. The one Adam tells is a set made from a family tartan and embroidered with the "
       "initials of a customer&rsquo;s late father: &ldquo;he wished they had spent more time together on the golf "
       "course. That really got me.&rdquo; On scaling up, he is blunt &mdash; &ldquo;we&rsquo;re not Amazon Prime "
       "and never want to be.&rdquo;"),
"bigdog": dict(name="Big Dog Golf Co.", city="Wodonga, VIC", dom="bigdoggolfco.com",
  meta="Est. 2019", imgdir="aussie", frames=None,
  desc="Mark Calder started this on a dining table in a Brunswick apartment in 2019 after noticing something "
       "nobody had bothered to do. In his words: &ldquo;I couldn&rsquo;t believe &mdash; The Big Dog&reg; &mdash; is "
       "commonly used when referring to the driver, so I thought, why not trademark it and see what we can "
       "do?&rdquo; The leather "
       "covers are now in the pro shops at Royal Melbourne, Barnbougle, Royal Adelaide, NSW, Victoria, Peninsula "
       "Kingswood and Cape Wickham, plus Tara Iti and Te Arai Links across the Tasman. If you are building an "
       "Australian trip, this is the souvenir."),
}
LABELS = ["lof","walker","penta","midiron","birds","okka","grayhaast","found"]
MAKERS = ["mackem","bigdog"]

# ---------------------------------------------------------------- trips
# price=None -> not published. NEVER guess. Status verified 2026-08-24.
TRIPS = [
 ("Random Golf Club &mdash; The Long Way Round", "Australia Major 2026", "Bookable",
  "US$6,195 shared &middot; US$7,395 single", "31 Oct &ndash; 7 Nov 2026 &middot; 8 rounds + a 9-hole scramble &middot; 14 players",
  "The one trip on this page built for the people who read this site, and the only community-led Australia trip "
  "that exists. Fourteen players, eight rounds plus an opening nine-hole scramble, and an itinerary that opens at Royal Park &mdash; the Melbourne "
  "public course where the first Random Golf Club meetup happened &mdash; before getting into Kingston Heath, "
  "Victoria, Peninsula Kingswood North, both Nationals and St Andrews Beach. Al and Erik Anders Lang drive the "
  "vans themselves, which is the whole pitch: &ldquo;a smaller group and no fixed leash, so if someone fancies a "
  "dip in the sea after golf&hellip; we go and have one.&rdquo; Golf, lodging, transport and breakfast are in; "
  "airfare, caddies and trolleys are not. Australians can buy a stripped-back local ticket at US$4,995. It closes "
  "with 36 holes of matchplay for the Random Cup, and if you are not ready to go home it runs straight into their "
  "Japan Major."),
 ("Outpost Overseas", "Edinburgh, for the Outpost Club", "Bespoke, no fixed dates",
  None, "11&ndash;12 days &middot; minimum 4 players &middot; quoted in GBP",
  "The most ambitious routing anyone offers. Their &ldquo;Best of Australia&rdquo; promises all seven Australian "
  "courses currently in the world top hundred, plus Royal Adelaide, Lost Farm and Seven Mile Beach, which they "
  "describe as a likely future entrant. The only way twelve days absorbs that is the bit that makes it "
  "interesting: they move you Melbourne to King Island to Barnbougle to Hobart by private flight. No published "
  "price, quoted in pounds, with a fifty per cent non-refundable deposit. Outpost Overseas was set up by the "
  "US-based Outpost Club, which publishes almost nothing about itself."),
 ("Jet Set Golf &mdash; The Big 5", "Victoria, flying Air Adventure&rsquo;s aircraft", "On request",
  "From A$4,977 per person", "5 days &middot; 5 courses &middot; group of 8, twin share",
  "A Pilatus PC-12 that lands at the golf course. Air Adventure Australia has been flying out of regional Victoria "
  "since 1977 and their own pitch is &ldquo;as little as 90 minutes from take-off to tee-off&rdquo; &mdash; which "
  "is the only clean answer to the King Island problem, because there is no passenger ferry across Bass Strait and "
  "the commercial flights are small. Five days covers Barnbougle Dunes, Lost Farm, Seven Mile Beach, Cape Wickham "
  "and Ocean Dunes, with a night on site at Cape Wickham. Two footnotes to read: there is a A$285 green fee and "
  "accommodation surcharge across the five courses for international players, and the advertised rate is flagged "
  "as expiring at the end of August 2026, so treat the number as indicative."),
 ("Luxury Golf &amp; Scenic Tours", "Tasmania", "Bookable online",
  "A$3,599 &middot; A$5,169 for seven days", "4 days &middot; 4 rounds &middot; minimum 4 players",
  "Small, Tasmanian, and the only operator here that publishes every price and takes a booking online without a "
  "phone call. The four-day Barnbougle and King Island package includes the Launceston and Melbourne flights and "
  "shared carts on the island. The reason to look at them, though, is a one-day product nobody else packages: "
  "Ratho Farm, a course laid out on an 1822 sheep farm and the oldest in Australia, for A$350."),
 ("Moran Golf Tours", "Toronto, New South Wales", "Register interest",
  "A$4,850 per person twin share", "12&ndash;19 Oct 2026 &middot; 6 rounds &middot; 12&ndash;16 players",
  "A Tasmania week led by a PGA professional who runs a clinic before each Barnbougle round and coaches inside the "
  "rounds themselves. Seven Mile Beach, Royal Hobart, Tasmania Golf Club, Barnbougle Dunes and Lost Farm twice, "
  "because playing a great course once is a waste of a flight. Transfers, breakfast daily and meals on golf days "
  "included; the flights to Tasmania are not stated as included, so ask."),
 ("Signature Golf Tours &mdash; Sandbelt Trophy", "Gold Coast", "Entries open",
  "A$3,499 twin &middot; A$4,299 single", "11&ndash;17 Oct 2026 &middot; 4 rounds &middot; a tournament",
  "Not a tour but a competition, which is a different and better proposition if you want a card in your hand. "
  "Three rounds of single Stableford and a fourball, open to anyone with an official handicap, over Peninsula "
  "Kingswood South, Woodlands, Victoria and Huntingdale &mdash; all walking, six nights at Crown Promenade, and "
  "more than fifteen thousand dollars in prizes. Returning after a three-year gap. Priced and pitched at "
  "Australians, so flights are on you and no non-resident surcharge is stated."),
 ("PerryGolf", "Wilmington, North Carolina", "Escorted trip sold out &middot; custom available",
  "From US$9,415 custom &middot; US$20,995 escorted", "8&ndash;12 nights &middot; 6&ndash;7 rounds",
  "The most transparently priced American operator selling Australia, and the most honest about the limits. Their "
  "November 2026 escorted departure is sold out with a waitlist; custom itineraries start around US$9,415 double "
  "occupancy. What earns them a place here is the disclosure: &ldquo;Australian golf culture is deeply rooted in "
  "walking. While electric carts will be available at Peninsula Kingswood, all other rounds will be walking-only,&rdquo; "
  "and on caddies, &ldquo;they cannot be guaranteed.&rdquo; Everybody else sells certainty."),
 ("Pioneer Golf", "Austin, Texas", "Custom, no fixed departures",
  "From US$4,250 Tasmania &middot; US$8,350 Sandbelt", "8 nights &middot; group of 8, double occupancy",
  "A hometown call for anyone reading this in Austin, and the only operator in the world we found who publishes "
  "the exchange rate their quote is built on, with the date attached. Three products: the Sandbelt from US$8,350, "
  "Sydney and the Sandbelt from US$9,100, and a Tasmania-only trip from US$4,250 that takes in both Barnbougles, "
  "Bougle Run, Tasmania Golf Club and two rounds at Seven Mile Beach. That last one is the cheapest credible "
  "package we found anywhere."),
 ("Kalos Golf", "Chapel Hill, North Carolina", "Two departures live",
  None, "1&ndash;12 Nov 2026 &middot; also Oct&ndash;Nov 2027",
  "The only operator flying clients privately to Cape Wickham as part of a mainland itinerary rather than a "
  "Tasmania add-on. Sydney, then a chartered flight to Adelaide, then Melbourne &mdash; The Australian, New South "
  "Wales, Royal Adelaide, Cape Wickham, Royal Melbourne West, Kingston Heath and Victoria, with optional Great "
  "Barrier Reef and Tasmania extensions. No price published anywhere on the site; you have to request the brochure."),
 ("Voyages.golf", "Merricks North, Victoria", "Sold out &mdash; waitlist",
  None, "18 Jan &ndash; 1 Feb 2027 &middot; 8 rounds &middot; 12&ndash;24 players",
  "Listed because of what they disclose rather than what they sell. The 2027 departure is gone and the pricing tab "
  "has been replaced with a sold-out notice, but they publish the one number every other operator buries: "
  "&ldquo;caddies are required for overseas guests at Royal Melbourne Golf Club. Caddies are AUD 200 in cash per "
  "person, plus expected tips.&rdquo; The free day offers a helicopter to The National, three guests per aircraft."),
 ("Premier Golf", "Alpharetta, Georgia", "Bookable",
  "From US$4,975 double &middot; US$6,195 single", "10 days &middot; but only 4 rounds",
  "The cheapest headline number on this page and the one that needs reading properly: it assumes four people "
  "sharing transfers, travel in October or May, and it buys four rounds across ten days rather than the seven you "
  "get elsewhere. Not comparable like-for-like with PerryGolf or Pioneer, and the low headline is doing a lot of "
  "work &mdash; read the occupancy and the season before you compare it to anything else on this page."),
 ("AUSGOLF", "Victoria", "Enquiry only &mdash; read the footnote",
  "A$2,525 &mdash; but not at that price for you", "5 days &middot; 4 rounds incl. Royal Melbourne",
  "Included as a warning rather than a recommendation, because that A$2,525 is the single most misleading number "
  "in Australian golf travel. Their own conditions: access to some Sandbelt clubs requires proof of membership at "
  "a recognised interstate club, and &ldquo;rates are for GolfLink Australia members and overseas golfer "
  "surcharges apply.&rdquo; The surcharge is never quantified. If you are American, this is a rate card, not a price."),
]

FAQS = [
 ("What are the best Australian golf brands?",
  "For clothing: Left of Field Golf out of Sydney, Walker Golf Things on the Gold Coast, Penta on Sydney&rsquo;s "
  "Northern Beaches, Gray + Haast in Burleigh Heads, Okka in Perth, Found Golf in Melbourne, Birds of Condor in "
  "Byron Bay, and Midiron, which will not tell you where it is based. For leather and wool goods: Mackem Golf in "
  "the Perth hills and Big Dog Golf Co. in Victoria, whose covers are stocked in the pro shops at Royal Melbourne, "
  "Barnbougle, Royal Adelaide and Cape Wickham. Most price in Australian dollars, though Left of Field and Birds "
  "of Condor both run overseas storefronts that will show you a converted price."),
 ("Does Random Golf Club run a trip to Australia?",
  "Yes. Their Australia Major runs 31 October to 7 November 2026 and is limited to fourteen players. "
  "It is US$6,195 per person on shared occupancy or US$7,395 for a private room, "
  "covering eight rounds plus an opening nine-hole scramble, lodging, ground transport and breakfast &mdash; "
  "but not airfare, caddies or trolleys. "
  "deposit, with the balance due 1 October 2026. Australians can buy a local ticket at US$4,995 that strips out "
  "the hotels, breakfasts and transport."),
 ("Is Random Golf Club the only brand running an Australia trip?",
  "As far as we can establish, yes, and it is not close. We checked No Laying Up, Fried Egg Golf, The Golfer&rsquo;s "
  "Journal, Bob Does Sports, Good Good and Skratch, plus a dozen apparel labels including Manors, Malbon, Eastside "
  "and Sugarloaf. None of them run an Australia trip. Fried Egg publishes its calendar through September 2027 with "
  "a deposit system already built, and its entire international slate is Britain and Ireland."),
 ("How much does a golf trip to Australia cost?",
  "The honest range for an organised trip is roughly US$4,250 to US$21,000 per person, and the spread is mostly "
  "about how many rounds you get. Pioneer Golf&rsquo;s Tasmania-only package starts around US$4,250 and is the "
  "cheapest credible option we found. Random Golf Club is US$6,195 for eight rounds and a scramble. PerryGolf&rsquo;s custom trips "
  "start near US$9,415 and their escorted departure runs US$20,995. Watch the round count &mdash; Premier "
  "Golf&rsquo;s US$4,975 headline buys four rounds across ten days, not the seven you get elsewhere. Airfare from "
  "the US is almost never included."),
 ("Do you need a tour operator to play the Melbourne Sandbelt?",
  "No, and this surprises people. Every major Sandbelt club publishes an unaccompanied-visitor pathway and none "
  "requires a member host. What you do need is membership of a home club and, at most of them, a registered "
  "handicap &mdash; for an American, an active GHIN, printed and brought with you, because Golf Australia runs no "
  "reciprocal scheme and no shared database. Kingston Heath and Commonwealth want a letter of "
  "introduction; Yarra Yarra explicitly does not. What an operator actually buys you is the introductions and the "
  "booking windows, not access nobody else can get."),
 ("Do international visitors pay more to play in Australia?",
  "Often, and the good news is that the better courses print it rather than hiding it. Barnbougle charges A$199 to "
  "an Australian and A$285 to an international visitor for the same eighteen holes. Cape Wickham is A$235 against "
  "A$315. Kooyonga in Adelaide publishes A$425 for local and interstate visitors against A$625 international. Woodlands, the only "
  "Sandbelt club that publishes a fee at all, is A$350 domestic and A$450 international. Budget for the premium; "
  "just do not be surprised by it."),
 ("When is the best time for a golf trip to Australia?",
  "Spring, meaning October to mid-December, or autumn, mid-February through April. Avoid the Australian school "
  "summer holidays from around 19 December to 26 January, when domestic demand spikes and access tightens. Two "
  "counterintuitive points: Melbourne&rsquo;s rainfall is almost dead flat year-round, between 47 and 66mm every "
  "single month, so there is no dry season to chase; and Tasmania is windiest in summer, not winter &mdash; Hobart "
  "averages 19km/h at 3pm in January against 12km/h in June."),
 ("How do you get to King Island and Barnbougle?",
  "Barnbougle is about ninety minutes from Launceston airport, which is an hour from Melbourne. King Island has no "
  "passenger ferry &mdash; the Bass Strait vessels carry freight and vehicles only &mdash; so you fly, or you book "
  "a trip that flies you. If you are travelling independently with clubs, the airline choice matters: Sharp "
  "Airlines gives you 21kg all in, with excess charged by the kilo above that, while King Island Airlines carries "
  "clubs as freight at a published A$5 a kilo &mdash; roughly A$140 return for a typical travel bag on top of the "
  "fare. Ring whichever one you book and confirm how they will handle the clubs."),
 ("Do Americans need a visa for Australia?",
  "Yes. US citizens need an Electronic Travel Authority, subclass 601. There is no visa application charge but "
  "there is an A$20 service fee, and it is app-only &mdash; the Australian government does not run a web form, so "
  "any website charging you for one is not official. It is valid twelve months with unlimited entries and a "
  "three-month maximum per visit."),
 ("What should you know before you play &mdash; carts, caddies, dress code?",
  "Three things that catch Americans out. First, most of these courses are walking courses and a cart genuinely "
  "requires a medical certificate; Barnbougle is walking-only with a A$150 exemption. Second, caddies are thinner "
  "on the ground than at a US destination resort and need booking with the tee time &mdash; Kingston Heath charges "
  "A$220 plus gratuity in cash, and Royal Melbourne A$200 in cash for overseas guests. "
  "Australia has no tipping culture anywhere else, but you do tip the caddie, in cash. Third, the old long-socks "
  "rule has been replaced by its opposite. Kingston Heath asks for short socks, predominantly white; Royal "
  "Melbourne for short socks that are either predominantly white or complement the rest of your clothing. Neither "
  "allows denim of any colour."),
]

# ---------------------------------------------------------------- css
EXTRA_CSS = """
<style>
.trip{border-top:1px solid var(--rule,#e2dfd6);padding:22px 0 6px;}
.trip:first-child{border-top:none;}
.trip-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-bottom:4px;}
.trip-name{font-size:20px;font-weight:700;letter-spacing:-0.01em;}
.trip-rank{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:#3a5c36;border:1px solid #3a5c36;border-radius:2px;padding:2px 6px;}
.trip-arch{font-size:13px;color:#6e736c;font-style:italic;}
.trip-facts{display:flex;flex-wrap:wrap;gap:6px 18px;margin:8px 0 10px;}
.trip-fact{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.04em;color:#4a4f48;}
.trip-fact b{color:#16180f;font-weight:700;}
.ttable{margin:6px 0 4px;border-top:1px solid var(--rule,#e2dfd6);}
.trow{display:grid;grid-template-columns:1.5fr 1.1fr 1.7fr 1.7fr 1fr;gap:12px;padding:11px 0;border-bottom:1px solid #ece9e0;font-size:13.5px;line-height:1.45;color:#42463f;}
.trow.thead{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#6e736c;border-bottom:1px solid #d8d5cc;}
.tc-op{font-weight:700;color:#16180f;}
.tc-base{color:#6e736c;}
.tc-price{color:#16180f;}
.tc-spec{color:#5a5f57;}
.tc-status{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;color:#3a5c36;}
@media(max-width:760px){.trow{grid-template-columns:1fr 1fr;}.trow.thead{display:none;}}
.trip-note{font-size:15px;line-height:1.62;color:#42463f;margin:0;}
</style>
"""

# ---------------------------------------------------------------- build
h = open(TPL, encoding="utf-8").read()
head = h[:h.index('<div class="faq">')]
_i = h.index('<div class="faq">'); _d = 0
for _m in re.finditer(r'<div\b|</div>', h[_i:]):
    _d += 1 if _m.group(0) != "</div>" else -1
    if _d == 0:
        TAIL = h[_i + _m.end():]; break
else:
    raise SystemExit("could not find close of faq div")

def gallery(frames, imgdir, alt):
    n = len(frames)
    t = "".join('<div class="pg-frame"><img src="/images/%s/%s" loading="lazy" alt="%s"></div>'
                % (imgdir, f, alt) for f in frames)
    g = '<div class="product-gallery"><div class="pg-track">%s</div>' % t
    if n >= 2:
        g += ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>'
              % (n, "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                            % (" on" if i == 0 else "", i, i + 1) for i in range(n))))
    return g + "</div>", n

def brand_card(key):
    b = BRANDS[key]
    frames = b["frames"] or MAN[key]["frames"]
    imgdir = b["imgdir"]
    for f in frames:
        assert os.path.exists(os.path.join(ROOT, "images", imgdir, f)), "missing %s/%s" % (imgdir, f)
    g, n = gallery(frames, imgdir, "%s Australian golf brand" % b["name"])
    prices = [int(i["pr"]) for i in MAN.get(key, {}).get("items", []) if i.get("pr", "").isdigit()]
    rng = ("A$%d&ndash;A$%d <span style=\"opacity:.6\">(about US$%d&ndash;%d)</span>"
           % (min(prices), max(prices), usd(min(prices)), usd(max(prices)))) if prices else b["meta"]
    return ('  <div class="product-card" data-frames="%d">\n    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">%s</div>\n'
            '        <div class="product-name">%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="https://%s" target="_blank" rel="noopener" class="product-link">Visit &#8599;</a>\n'
            '      </div>\n  </div>\n' % (n, g, b["city"], b["name"], b["desc"], b["dom"]))

FEATURED = {
"rgc": dict(name="Random Golf Club &mdash; The Long Way Round", base="Australia Major 2026",
  price="US$6,195 shared &middot; US$7,395 single",
  spec="31 Oct &ndash; 7 Nov 2026 &middot; 8 rounds + a 9-hole scramble &middot; 14 players",
  url="https://randomgolfclub.com/pages/australia-major-2026",
  desc="The one trip on this page built for the people who read this site, and the only community-led Australia "
       "trip that exists. Fourteen players, and an itinerary that opens at Royal Park &mdash; the Melbourne public "
       "course where the first Random Golf Club meetup happened &mdash; before getting into Kingston Heath, "
       "Victoria, Peninsula Kingswood North, both Nationals and St Andrews Beach. Al and Erik Anders Lang drive the "
       "vans themselves, which is the whole pitch: &ldquo;a smaller group and no fixed leash, so if someone fancies "
       "a dip in the sea after golf&hellip; we go and have one.&rdquo; Golf, lodging, transport and breakfast are "
       "in; airfare, caddies and trolleys are not. Australians can buy a stripped-back local ticket at US$4,995. It "
       "closes with 36 holes of matchplay for the Random Cup, and if you are not ready to go home it runs straight "
       "into their Japan Major."),
"jetset": dict(name="Jet Set Golf &mdash; The Big 5", base="Flying Air Adventure&rsquo;s aircraft",
  price="From A$4,977 per person",
  spec="5 days &middot; 5 courses &middot; group of 8, twin share",
  url="https://www.jetsetgolf.com.au/st_tour/the-big-5-barnbougle-7-mile-beach-king-island/",
  desc="A Pilatus PC-12 that lands at the golf course. Air Adventure Australia has been flying out of regional "
       "Victoria since 1977 and their own pitch is &ldquo;as little as 90 minutes from take-off to tee-off&rdquo; "
       "&mdash; which is the only clean answer to the King Island problem, because there is no passenger ferry "
       "across Bass Strait and the commercial flights are small. Five days covers Barnbougle Dunes, Lost Farm, "
       "Seven Mile Beach, Cape Wickham and Ocean Dunes, with a night on site at Cape Wickham. Two footnotes: there "
       "is a A$285 green fee and accommodation surcharge across the five courses for international players, and the "
       "advertised rate is flagged as expiring at the end of August 2026, so treat the number as indicative."),
}

# The other ten: no rights-clean imagery exists, so they run as a comparison table.
TABLE = [
 ("Outpost Overseas","Edinburgh","Not published","11&ndash;12 days, min 4 players","Bespoke"),
 ("Luxury Golf &amp; Scenic Tours","Tasmania","A$3,599 &ndash; A$5,169","4&ndash;7 days, min 4 players","Bookable online"),
 ("Moran Golf Tours","Toronto, NSW","A$4,850 twin share","12&ndash;19 Oct 2026, 6 rounds","Register interest"),
 ("Signature Golf Tours","Gold Coast","A$3,499 twin &middot; A$4,299 single","11&ndash;17 Oct 2026, 4 rounds","Entries open"),
 ("PerryGolf","Wilmington, NC","From US$9,415 &middot; US$20,995 escorted","8&ndash;12 nights, 6&ndash;7 rounds","Escorted sold out"),
 ("Pioneer Golf","Austin, TX","From US$4,250 &middot; US$8,350 Sandbelt","8 nights, group of 8","Custom"),
 ("Kalos Golf","Chapel Hill, NC","Not published","1&ndash;12 Nov 2026","Two departures live"),
 ("Voyages.golf","Merricks North, VIC","Not published","18 Jan &ndash; 1 Feb 2027, 8 rounds","Sold out"),
 ("Premier Golf","Alpharetta, GA","From US$4,975 double","10 days, but only 4 rounds","Bookable"),
 ("AUSGOLF","Victoria","A$2,525 &mdash; not at that price for you","5 days, 4 rounds","Enquiry only"),
]

def featured_card(key):
    c = FEATURED[key]; frames = TRIPIMG[key]
    for f in frames:
        assert os.path.exists(os.path.join(ROOT, "images", "aussie-trips", f)), "missing " + f
    g, n = gallery(frames, "aussie-trips", "%s Australia golf trip" % c["name"].replace("&mdash;", ""))
    return ('  <div class="product-card" data-frames="%d">\n    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">%s</div>\n'
            '        <div class="product-name">%s</div>\n'
            '        <div class="trip-facts"><span class="trip-fact"><b>Price</b> %s</span>'
            '<span class="trip-fact"><b>Details</b> %s</span></div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Details &#8599;</a>\n'
            '      </div>\n  </div>\n'
            % (n, g, c["base"], c["name"], c["price"], c["spec"], c["desc"], c["url"]))

def trip_table(rows):
    head = ('<div class="ttable"><div class="trow thead">'
            '<span class="tc-op">Operator</span><span class="tc-base">Based</span>'
            '<span class="tc-price">Price</span><span class="tc-spec">Details</span>'
            '<span class="tc-status">Status</span></div>')
    body = "".join(
      '<div class="trow"><span class="tc-op">%s</span><span class="tc-base">%s</span>'
      '<span class="tc-price">%s</span><span class="tc-spec">%s</span>'
      '<span class="tc-status">%s</span></div>' % r for r in rows)
    return head + body + "</div>"

def sec(sid, h2, kick_lead, kick_body, inner):
    return ('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s</strong>%s</p>\n%s'
            % (sid, h2, kick_lead, kick_body, inner))

body = []
body.append(sec("labels", "The Labels", "Apparel &middot; eight brands",
  "Australia&rsquo;s independent golf scene got good fast, and it got good in a specific way &mdash; surf and skate "
  "silhouettes, coastal names, and almost no interest in looking like a pro shop. Most price in Australian "
  "dollars, which is quietly good news for an American &mdash; though note that Left of Field runs a US "
  "storefront in dollars and Birds of Condor a New Zealand one, so what you see may already be converted. All "
  "eight ship internationally.",
  '<div class="products-grid">\n' + "".join(brand_card(k) for k in LABELS) + '</div>'))
body.append(sec("makers", "The Makers", "Leather and wool &middot; two workshops",
  "The other half of the Australian scene is two small workshops sewing things by hand, and their work has quietly "
  "ended up in the best pro shops in the country. Big Dog&rsquo;s covers are in the shops at Royal Melbourne, "
  "Barnbougle, Royal Adelaide and Cape Wickham. If you are going and want to bring something home, start here "
  "rather than with a logoed cap.",
  '<div class="products-grid">\n' + "".join(brand_card(k) for k in MAKERS) + '</div>'))
body.append(sec("trips", "The Trips", "Two featured &middot; ten more compared",
  "Here is the finding that shaped this section. Random Golf Club runs an Australia trip. No other golf-media or "
  "apparel brand in the world does &mdash; not No Laying Up, not Fried Egg, not The Golfer&rsquo;s Journal, none "
  "of the clothing labels. Fried Egg has the deposit-and-calendar machinery built and points its whole "
  "international programme at Britain and Ireland. Two trips get the full treatment below because they are the two "
  "genuinely distinctive things you can book; the other ten are compared underneath on the numbers that actually "
  "differ. One thing to carry through all of it: across roughly twenty operators, not one described a private "
  "Sandbelt tee time as guaranteed. Access is sold as capability, never as contract.",
  '<div class="products-grid">\n' + "".join(featured_card(k) for k in ["rgc","jetset"]) + '</div>\n'
  + '<p class="cat-kicker"><strong>The other ten</strong>Competent, mostly quote-only, and best compared on price '
    'and round count rather than on marketing. Read the AUSGOLF line carefully &mdash; that A$2,525 is a rate for '
    'Golf Australia members, and overseas surcharges apply without being quantified. Premier&rsquo;s low headline '
    'buys four rounds across ten days, not the seven you get elsewhere.</p>\n'
  + trip_table(TABLE)))
BODY = "\n".join(body)

FAQ_HTML = ('<div class="faq">\n' + "\n".join(
    '    <details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)
    + "\n  </div>" + TAIL)

page = head + FAQ_HTML
mark = '<section class="products">'
page = page[:page.index(mark) + len(mark)] + "\n" + BODY + "\n" + page[page.index('<div class="faq">'):]

def sub1(pat, rep, s, label):
    s2, n = re.subn(pat, rep, s, count=1, flags=re.S)
    assert n == 1, "head surgery failed: " + label
    return s2

page = sub1(r'<title>.*?</title>', '<title>%s | The Grassy Issue</title>' % TITLE_TXT, page, "title")
page = sub1(r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="%s"' % DESC, page, "description")
for k in ["og:title", "twitter:title"]:
    page = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % k, r'\g<1>%s\g<2>' % TITLE_TXT, page)
for k in ["og:description", "twitter:description"]:
    page = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % k, r'\g<1>%s\g<2>' % DESC, page)
page = re.sub(r'(https://thegrassyissue\.com/drops/)brand-to-know-left-of-field-golf', r'\g<1>%s' % SLUG, page)
page = sub1(r'</head>', EXTRA_CSS + '</head>', page, "extra css")
page = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % TITLE, page, "h1")
page = sub1(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(\s*</div>)',
            r'\g<1>' + TITLE_TXT + r'\g<2>', page, "breadcrumb")
page = sub1(r'<div class="drop-meta">.*?</div>',
            '<div class="drop-meta">\n    <span>10 Brands &middot; 12 Trips</span>\n  </div>', page, "drop-meta")
page = sub1(r'<div class="drop-hero">.*?</div></div>',
            '<div class="drop-hero"><div class="drop-hero-img">'
            '<img src="/images/aussie/hero-australia.jpg" '
            'alt="Two golfers on the Tasmanian coast, from Left of Field Golf\'s Barnbougle campaign" />'
            '</div></div>', page, "hero")
page = sub1(r'<div class="sidebar-detail"><span class="l">Pieces</span>.*?<span class="l">Range</span><span>[^<]*</span></div>',
  '<div class="sidebar-detail"><span class="l">Brands</span><span>10</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Trips</span><span>12</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">From</span><span>US$4,250</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Currency</span><span>AUD</span></div>', page, "sidebar")
page = sub1(r'<span class="hashtag">#LeftOfFieldGolf</span>',
            '<span class="hashtag">#AustralianGolf</span>', page, "hashtag")
page = page.replace('<span class="hashtag">#GearEdit</span>', '<span class="hashtag">#Sandbelt</span>')

INTRO = """
    <p>Australia is the best golf destination almost no American has been to, and the reason is not distance. It is
    that the information is bad. Half of what gets written about the Melbourne Sandbelt in the US repeats a myth
    about Alister MacKenzie designing all of it; almost none of it tells you what a trip costs or how you get on
    one.</p>
    <p>So this is two lists. The first is the independent brands, which have got very good very fast and which
    nobody outside Australia is covering properly. The second is every organised trip we could find that an
    American can actually book, with prices exactly as published and a clear note where they are not.</p>
    <p>The finding that surprised us most is in the second list. <em>Random Golf Club runs an Australia trip. No
    other golf media or apparel brand does.</em> We checked No Laying Up, Fried Egg, The Golfer&rsquo;s Journal, Bob Does
    Sports, Good Good, Skratch, and a dozen clothing labels from Manors to Malbon to Eastside. Nothing. Fried Egg
    has a deposit system and a calendar published a year ahead, and points its entire international programme
    at Britain and Ireland. There is a genuine hole in this market, and for now one fourteen-person van tour is
    filling it.</p>
    <p>One note on money running through everything below. Brand prices are in Australian dollars, because that is
    what these businesses charge; at late-August 2026 rates an Australian dollar is about seventy-two US cents, so
    knock off a bit under a third. Trip prices are quoted in whatever currency the operator publishes, and we have
    said which. Where an operator does not publish a price, we have said that too, rather than guessing.</p>
"""
page = sub1(r'(<div class="writeup-body">).*?(\s*</div>)', lambda m: m.group(1) + INTRO + m.group(2),
            page, "intro")

def strip(s):
    s = re.sub(r'<[^>]+>', '', s)
    for a, b in [("&mdash;","—"),("&ndash;","–"),("&rsquo;","’"),("&ldquo;","“"),("&rdquo;","”"),
                 ("&lsquo;","‘"),("&amp;","&"),("&middot;","·"),("&pound;","£"),("&hellip;","…"),
                 ("&reg;","®"),("&eacute;","é")]:
        s = s.replace(a, b)
    return s

art = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
  "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
  "publisher":{"@type":"Organization","name":"The Grassy Issue"},
  "datePublished":"2026-08-24","dateModified":"2026-08-24",
  "mainEntityOfPage":"https://thegrassyissue.com/drops/%s" % SLUG}, ensure_ascii=False)
faq = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":
  [{"@type":"Question","name":strip(q),
    "acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q, a in FAQS]}, ensure_ascii=False)
page = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">%s</script>' % art, page, count=1, flags=re.S)
last = page.rfind('<script type="application/ld+json">')
end = page.index('</script>', last) + len('</script>')
page = page[:last] + '<script type="application/ld+json">%s</script>' % faq + page[end:]

open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, len(page), "bytes")
print("brand cards:", page.count('<div class="product-card'),
      " grids:", page.count('<div class="products-grid">'),
      " trips:", page.count('<div class="trip">'))
