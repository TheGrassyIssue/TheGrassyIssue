#!/usr/bin/env python3
"""build-local-gc-btk.py — Brand to Know: Local GC.
1 October 2026.

Lenny: "Let's do a brand to know - https://www.localgc.co.nz/", then "do a deeper dive, add more
headcovers and group them by style", "In the TGI take- who is inspiring this brand, they are obviously
pulling inspo from Mackenzie and Gumtree", "remove '*MORE COLOURS IN DROP DOWN*' from all items",
"Add P46, P49, and P51 (I wish more brands did flags) add the few clothing options", then "show me the
post preview" (built from my 48 stars plus his 7).

FACTS: Local GC's own About, FAQ, Course Notes (blog), Find Us In Stores, Upcycled Customs and product
pages, read 1 Oct 2026. Founder surname from the company's Dun & Bradstreet record (Local GC Limited,
key principal Myles Leon Brock). MacKenzie / Fyfe details from TGI's own earlier posts. Gumtree not named in copy (Lenny: "let's not name Gumtree directly, its more of a trend").
QUOTES: verbatim from Local GC's Course Notes and product pages.
PHOTOS: Local GC's own (product pages, Course Notes, Upcycled Customs, homepage). No press photos.
Prices NZD read 1 Oct 2026; ~USD at 0.5645 (frankfurter.dev, 30 Sep 2026).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-local-gc"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/local-gc"
FR = json.loads((ROOT / "research/localgc/frames.json").read_text())
CAT = {o["slug"]: o for o in json.loads((ROOT / "research/localgc/options.json").read_text())}
BRAND = "Local GC"
RATE = 0.5645

TITLE = "Local GC — Handmade Golf Headcovers From Orewa, New Zealand"
DESC = ("Local GC sews headcovers, Sunday bags, putter covers and flags by hand in Orewa, New Zealand. "
        "Where the ideas come from, and 55 picks from NZ$18 to NZ$850.")
H1 = "Brand to Know: Local GC &mdash; Handmade Headcovers From a One-Man Workshop in New Zealand"


def nz(slug):
    p = CAT[slug]["price"]
    return f"NZ${p:g} (~${round(p * RATE)})"


# slug -> (name, detail, copy)
P = {
 # Sunday bags
 "camo-local-gc-sunday-bag-2": ("Camo Sunday Bag #2", "One of one",
   "This is 18oz camo poly-cotton canvas with waxed brown leather, solid brass hardware and a tube lined in black sailcloth. The opening is a 200mm (8-inch) stainless steel hoop with a leather divider, both pockets have YKK waterproof zips, and the Time of Leisure bird is embroidered inside. The bag in the photos is the one you get."),
 "daybreak-local-gc-sunday-bag": ("Daybreak Sunday Bag", "One of one",
   "This one is 14.9oz poly-cotton canvas with black cow leather and solid brass, with dancing swallows embroidered across the body and pocket. Local GC compares the way it wears in to raw denim: firm at first, then creased to the way you carry it. It is also a one-off."),
 # Birds, bugs and the field
 "mallard-canvas-head-cover": ("Mallard Canvas", "Driver to hybrid",
   "This is 14.9oz sand canvas with a single embroidered mallard. It starts stiff and softens with rounds and weather, the way a work jacket does."),
 "mallard-wool-head-cover": ("Mallard Wool", "Driver to hybrid",
   "The same mallard sits on a forest green wool outer, which gives the cover a warmer, quieter look in the bag. It pairs with the Mallard putter cover further down."),
 "flusher-head-cover": ("The Flusher", "Driver to hybrid",
   "The Flusher is 15oz army green canvas with one pheasant embroidered in early flight, the moment it breaks cover. Local GC calls it a tribute to the traditions of the field."),
 "beached-head-cover": ("Beached", "Driver to hybrid",
   "Beach birds are scattered across 10oz silk grey canvas. The design comes from slow morning walks on the beach in Orewa, the brand&rsquo;s hometown."),
 "swallow-navy-canvas-head-cover": ("Swallow Navy Canvas", "Driver to hybrid",
   "This is heavy 14.9oz navy canvas with one embroidered swallow. Local GC uses the swallow for resilience and finding your way home, and it turns up on the Daybreak bag, the stick cover and the &frac14; zip too."),
 "canvas-tol-head-cover": ("Time of Leisure Mitt", "Slip-on, driver to hybrid",
   "This slip-on mitt in proofed 14.9oz canvas carries the Time of Leisure dove, the brand&rsquo;s emblem for unhurried days and the long way back to the clubhouse. At NZ$79 it is one of the cheapest embroidered covers in the range."),
 "lure-canvas-head-cover": ("Lure", "Driver, mini driver, hybrid",
   "A fly-fishing lure is embroidered on top of the barrel, on heavy sand canvas. The product page sums it up as slow mornings, steady hands and learning the conditions."),
 "fly-head-cover": ("Fly", "Driver to hybrid",
   "House flies are scattered at random across 11oz dark grey Gridlock canvas, so no two covers are the same. Local GC admits there is no reason for the design. Like a fly, it just exists."),
 # Aotearoa and personal
 "manuka-navy-canvas-head-cover": ("M&#257;nuka Navy Canvas", "Driver to hybrid",
   "This one has m&#257;nuka, the native New Zealand tea tree, embroidered at random over navy canvas, so every cover is a one-off."),
 "manuka-cream-wool-head-cover": ("M&#257;nuka Cream Wool", "Mini driver or hybrid",
   "Black m&#257;nuka and working honey bees are embroidered over cream wool, again placed at random. Only the mini driver and hybrid sizes are available."),
 "local-gc-crest-head-cover": ("Local GC Crest Mitt", "Slip-on, driver to hybrid",
   "This heavy canvas mitt carries the Local GC crest, the monogram framed by silver ferns. At NZ$79 it is the easiest way to put the brand in your bag."),
 "dead-rats-canvas-head-cover": ("Dead Rats", "Driver to hybrid",
   "A row of dead rats is embroidered across soft 10oz artist canvas, with a rising hand at the crown. Local GC calls it unapologetically unconventional, and it is."),
 "candy-heart-head-cover": ("Heart Candy", "Driver to hybrid",
   "This 11oz canvas cover is scattered with candy hearts, placed differently on every one. Myles says the design came from time spent with his daughters."),
 "milton-head-cover": ("Milton", "Driver only",
   "This cover is silk grey canvas with a red Swingline stapler and one of Milton&rsquo;s lines from Office Space on top. It only comes in a driver size."),
 # Wool, tweed and tartan
 "vintage-harris-tweed-head-cover": ("Vintage Harris Tweed", "Wood only &middot; limited",
   "This barrel cover is cut from authentic vintage Harris Tweed, woven from pure new wool in the Outer Hebrides. The run was three drivers and three woods, the drivers have gone, and it will not be repeated."),
 "scottish-windowpane-wool-headcover": ("Scottish Windowpane Wool", "Mini driver or wood &middot; limited",
   "This is a limited run in traditional Scottish windowpane wool, with a plush lining and a hidden elastic insert. The mini driver and wood sizes are left."),
 "classic-check-and-branded-leather-headcover": ("Classic Check and Branded Leather", "Hybrid only &middot; no restocks",
   "This is heavyweight check wool with a full-grain leather top that has been fire-branded with the Local GC monogram. Only the hybrid size is left, and there will be no restock."),
 "vintage-peach-wool-head-cover": ("Vintage Peach Wool", "Driver to hybrid",
   "This barrel cover is made in small quantities from a vintage wool in a soft peach, one of the few warm colours in a bag of greens and navies."),
 "boucle-head-cover": ("GJM Pro Model Boucl&eacute;", "Driver to hybrid",
   "This is a white boucl&eacute; outer named for someone Local GC calls GJM, with a line about his style and elegance. It is the most fashion-forward cover in the shop."),
 "serape-head-cover": ("Serape", "Driver only &middot; limited",
   "This is handwoven serape fabric, cut to show off the stripes, so every cover looks different. It is a limited run in driver only."),
 # Leather and suede
 "cabretta-leather-tol-head-cover": ("Cabretta Leather Time of Leisure", "Slip-on, driver to hybrid",
   "This mitt is Italian waxed cabretta leather with the Time of Leisure dove embroidered in brown. The tanning gives it a lived-in patina from the first day."),
 "tan-suede-leather-covers": ("Tan Suede", "Driver to hybrid",
   "This is tan jersey cow suede with a smooth black lining. At NZ$180 it is the most expensive headcover in the shop, and the suede darkens and softens as you use it."),
 "sand-pig-suede": ("Sand Pigskin Suede", "Driver to hybrid",
   "This is genuine pigskin suede in sand, part of a premium range that also comes in navy, brown and black. Expect natural markings in the leather."),
 "whisky-brown-leather-covers": ("Whiskey Brown Leather", "Woods and putters",
   "This is full-grain whiskey brown leather, made for drivers and woods as well as blade, mallet and LAB DF3 putters, which close with a magnet. It is the cover to buy as a matching set."),
 # Sailcloth, oilskin and camo
 "coyote-brown-eplx400-head-cover": ("Coyote Brown EPLX400", "Driver, mini driver, wood",
   "This is EcoPak EPLX400, a technical laminate, in coyote brown, with a bungee cord across the front borrowed from a backpack. You can tuck a glove or a snack under it."),
 "cdx6-pro-head-cover": ("CDX6 Pro Sailcloth", "Driver, mini driver, wood",
   "CDX6 Pro is a laminate made for offshore sails. It starts stiff, stays weatherproof, and has nothing on it but the fabric."),
 "yellow-sail-cloth-head-cover": ("Yellow Sailcloth", "Driver to hybrid",
   "This is the brand&rsquo;s all-weather sailcloth barrel in bright yellow. Black, graphite, stone, oyster and red versions cost the same NZ$79."),
 "camo-oilskin-head-cover": ("Camo Oilskin", "Orange or black lining",
   "This is a camo oilskin outer with a choice of orange or black lining. Oilskin sheds rain and picks up a patina over time."),
 "brown-oilskin-head-cover": ("Brown Oilskin", "Driver to hybrid",
   "This is the classic brown oilskin version, which Local GC recommends for wet days. It is the closest thing in the range to an old waxed jacket."),
 "tiger-camo-canvas-head-cover": ("Tiger Camo", "Driver, mini driver, hybrid",
   "This one is 1000D polyester in tiger stripe camo, which feels different from the cotton covers. At NZ$79 it is one of the cheapest in the shop."),
 "floral-head-cover": ("Floral Coated Cotton", "Driver to hybrid",
   "This is acrylic-coated cotton in a floral print that Local GC says is like vintage camp tea towels. The coating makes it weather-resistant."),
 # Colour
 "Daybreak-Canvas-Head-Cover": ("Daybreak Canvas", "Eight colours",
   "This is heavy 14.9oz canvas with two dancing swallows, in a choice of eight colours from antelope to maroon. It is the headcover version of the Daybreak bag."),
 "nantucket-red-canvas-head-cover": ("Nantucket Red Canvas", "Driver to hybrid",
   "Local GC dyes this canvas in house to a faded Nantucket red and puts the monogram on top. Nothing else is on it."),
 "masters-green-canvas-head-cover": ("Masters Green Canvas", "Driver or wood",
   "This is a plain Masters-green canvas barrel with a black lining. It is NZ$79 and does not pretend to be anything more."),
 "hessian-head-cover": ("Hessian", "Driver to hybrid",
   "This barrel is natural hessian, the burlap of a coffee sack, with a raw texture that wears in. There is a black version too."),
 # Putter covers
 "waxed-cabretta-leather-putter-cover": ("Waxed Cabretta Leather Putter Cover", "Blade or mid mallet",
   "This is waxed brown cabretta leather that softens and darkens as you use it, with a magnetic closure. Each hide is a slightly different brown."),
 "ponga-wool-and-leather-mallet-putter-cover": ("Ponga Wool and Leather Mallet", "Mallet, centre shaft, LAB DF3",
   "This wool and leather mallet cover has an embroidered ponga, the silver fern. It comes cut for standard, centre-shaft and zero-torque LAB putters, and Local GC will adjust the pattern for the new Scotty Cameron Phantom 5."),
 "wool-and-whiskey-leather-crane-mallet-putter-cover": ("Crane Wool and Whiskey Leather Mallet", "Mallet, centre shaft, LAB DF3",
   "This is wool with whiskey leather and an embroidered crane, which Local GC uses as a symbol of luck and longevity. It comes in the same shapes as the Ponga, LAB DF3 included."),
 "Mallard-Putter": ("Mallard Putter Cover", "Blade or mid mallet &middot; eight colours",
   "This is 14.9oz canvas over 20mm of open-cell foam, with the mallard on one side. Pick the colour and the head shape from the dropdown."),
 "camo-oilskin-x-leather-mallet-and-df3-putter-cover": ("Camo Oilskin and Leather Mallet", "Mallet, centre shaft, LAB DF3",
   "Camo oilskin and black leather wrap padded foam here, and hidden magnets close it. Local GC says it is one of the few makers cutting covers for LAB&rsquo;s DF3 and OZ1, and every mallet cover here has a torque-putter option."),
 # Bags, pouches and practice
 "local-gc-shield-shag-bag": ("Shield Shag Bag", "Eight colours",
   "This is proofed 14.9oz canvas that holds 70 balls to the cuff and 100 with the drawstring out. The handle is off-centre so the bag leans as you pick up balls, and a brass eyelet in the base lets you hose it out."),
 "Localgc-Shoebag": ("Shoe Bag", "Eight colours, two linings",
   "This shoe bag is cut from a single panel of 14.9oz canvas, lined in tiger camo or black sailcloth. You can add initials, a name or a club crest."),
 "players-pouch": ("Premium Players Pouch", "Eight colours",
   "This 18 x 28cm canvas pouch has a soft liner and a waterproof zip, sized for a phone, keys and wallet in the bag."),
 "wool-essentials-pouch": ("Wool Essentials Pouch", "Charcoal",
   "This drawstring pouch is made from charcoal wool with a soft lining, for tees and markers on the course or keys off it."),
 "camo-range-finder-pouch": ("Camo Rangefinder Pouch", "Black lining",
   "This is the brand&rsquo;s heaviest canvas, in the Australian forces camo print, with a magnetic closure and a swivel snap. The black lining is in stock; the orange is not. See our <a href=\"/drops/rangefinder-cases-and-pouches\">rangefinder case roundup</a> for more."),
 "great-outdoors-range-finder-pouch": ("Great Outdoors Rangefinder Pouch", "Maroon, navy, copper green",
   "This is 14.9oz canvas of the kind Local GC says your childhood summer tent was made of, with panels of maroon, navy and copper green and a magnetic flap."),
 "merbau-alignment-sticks-harbour": ("Merbau Alignment Sticks, Harbour", "New Zealand shipping only",
   "These are 10mm merbau hardwood sticks, about 1.1 metres long, laser-engraved and painted with royal blue and grey bands. They only ship within New Zealand, so they are for the Kiwi readers."),
 "swallow-alignment-stick-cover": ("Swallow Alignment Stick Cover", "Black or navy",
   "This 8oz canvas sleeve keeps your alignment sticks together in the bag, finished with the swallow. Local GC calls it a small symbol of commitment to the long game."),
 # Flags and clothing
 "local-gc-golf-flag": ("19th Hole Flag", "Red and oyster",
   "This is a regulation-size flag in red and oyster with a 19, made with eyelets for a wall or a PVC spine for a pin. Local GC also makes custom 18-hole sets for clubs, embroidered in-house, and very few brands sell a flag at all."),
 "swallow-1-4-zip": ("Swallow &frac14; Zip", "Black, S&ndash;2XL",
   "This mid-heavyweight cotton-blend fleece has a mock neck and the swallow on the chest. Local GC is honest that it is a blank it embroiders while it works out stock levels."),
 "local-gc-monogram-beanie": ("Monogram Beanie", "Olive",
   "This is a classic olive acrylic beanie with the monogram on the front. At NZ$18 it is the cheapest thing in the shop."),
 "greenside-childrens-bucket-hat": ("Greenside Bucket Hat", "Kids and adult sizes",
   "This cotton bucket hat carries the Greenside Collection embroidery and comes in children&rsquo;s and adult sizes. Local GC will add a name on the back."),
 "greenside-childrens-t-shirt": ("Greenside Kids&rsquo; Tee", "Sizes 2&ndash;10",
   "This is a relaxed cotton tee with the same Greenside embroidery, for the junior golfer."),
}

SECTIONS = [
    ("bags", "The Sunday Bags", "sunday-bags",
     ["camo-local-gc-sunday-bag-2", "daybreak-local-gc-sunday-bag"],
     "<strong>Two bags &middot; NZ$850 (~$480) each</strong>Local GC finished its first Sunday bag prototype in October 2025, and every bag since has been a one-off or a tiny drop. The build is the same each time: heavy canvas, real leather, solid brass, a leather divider and an 8-inch stainless steel hoop, with the Time of Leisure bird or the swallow stitched somewhere you find later. These two are the only ones in the shop, and the photos show the exact bag you would get."),
    ("birds", "Headcovers: Birds, Bugs and the Field", "birds-and-the-field",
     ["mallard-canvas-head-cover", "mallard-wool-head-cover", "flusher-head-cover", "beached-head-cover",
      "swallow-navy-canvas-head-cover", "canvas-tol-head-cover", "lure-canvas-head-cover", "fly-head-cover"],
     "<strong>Eight covers &middot; NZ$79&ndash;$110 (~$45&ndash;$62)</strong>This is the heart of the brand. Most of Local GC&rsquo;s embroidery comes from the sporting field and the shoreline: a mallard, a flushing pheasant, a swallow, the dove it calls Time of Leisure, the birds on the beach at Orewa, and a fly-fishing lure. Some sit alone on the canvas; others are scattered at random, so no two covers match. The flies are there for no reason at all, which Local GC happily admits."),
    ("aotearoa", "Headcovers: Aotearoa and Personal", "aotearoa-and-personal",
     ["manuka-navy-canvas-head-cover", "manuka-cream-wool-head-cover", "local-gc-crest-head-cover",
      "dead-rats-canvas-head-cover", "candy-heart-head-cover", "milton-head-cover"],
     "<strong>Six covers &middot; NZ$79&ndash;$110 (~$45&ndash;$62)</strong>These are the covers that could only come from this workshop. M&#257;nuka and the silver fern are New Zealand&rsquo;s own plants, and the crest puts the monogram inside a ring of ferns. The rest are personal: candy hearts for his daughters, Milton&rsquo;s stapler from Office Space, and a row of dead rats that started as a joke in the workshop and stayed."),
    ("wool", "Headcovers: Wool, Tweed and Tartan", "wool-tweed-and-tartan",
     ["vintage-harris-tweed-head-cover", "scottish-windowpane-wool-headcover", "classic-check-and-branded-leather-headcover",
      "vintage-peach-wool-head-cover", "boucle-head-cover", "serape-head-cover"],
     "<strong>Six covers &middot; NZ$99&ndash;$120 (~$56&ndash;$68)</strong>This is the Scottish side of the shop, and the closest Local GC gets to Fyfe. There is vintage Harris Tweed, Scottish windowpane and a heavyweight check with a branded leather top, plus two wildcards in white boucl&eacute; and handwoven serape. Several are limited runs with only one or two sizes left, so check the dropdown before you fall for one."),
    ("leather", "Headcovers: Leather and Suede", "leather-and-suede",
     ["cabretta-leather-tol-head-cover", "tan-suede-leather-covers", "sand-pig-suede", "whisky-brown-leather-covers"],
     "<strong>Four covers &middot; NZ$160&ndash;$180 (~$90&ndash;$102)</strong>Local GC&rsquo;s premium range is waxed Italian cabretta, cow suede, pigskin suede and full-grain whiskey leather. They cost about twice the canvas covers and they age the most, darkening and softening with every round. The whiskey brown comes in every shape from driver to LAB putter, so you can build a matching set."),
    ("weather", "Headcovers: Sailcloth, Oilskin and Camo", "sailcloth-oilskin-and-camo",
     ["coyote-brown-eplx400-head-cover", "cdx6-pro-head-cover", "yellow-sail-cloth-head-cover", "camo-oilskin-head-cover",
      "brown-oilskin-head-cover", "tiger-camo-canvas-head-cover", "floral-head-cover"],
     "<strong>Seven covers &middot; NZ$79&ndash;$99 (~$45&ndash;$56)</strong>These are built for New Zealand weather: coastal wind, cold mornings and rain. Local GC uses offshore sailcloth and technical laminates, oilskin that sheds water, and the camo print issued to Australian forces. The Coyote Brown cover even has a bungee on the front for a glove, and the floral one is coated cotton that looks like a camp tea towel."),
    ("colour", "Headcovers: Colour", "colour",
     ["Daybreak-Canvas-Head-Cover", "nantucket-red-canvas-head-cover", "masters-green-canvas-head-cover", "hessian-head-cover"],
     "<strong>Four covers &middot; NZ$79&ndash;$89 (~$45&ndash;$50)</strong>Sometimes you just want a colour. These are plain heavy canvas, picked by shade, with a small tag or monogram. The Daybreak comes in eight colours, the Nantucket red is dyed in the workshop, and the hessian is the texture of a coffee sack."),
    ("putters", "Putter Covers", "putter-covers",
     ["waxed-cabretta-leather-putter-cover", "ponga-wool-and-leather-mallet-putter-cover",
      "wool-and-whiskey-leather-crane-mallet-putter-cover", "Mallard-Putter", "camo-oilskin-x-leather-mallet-and-df3-putter-cover"],
     "<strong>Five covers &middot; NZ$99&ndash;$160 (~$56&ndash;$90)</strong>Local GC is one of the few makers cutting mallet covers to fit LAB&rsquo;s torque-balanced putters, the DF3, Mezz and OZ1, and every mallet cover here has that option in the dropdown. The closures are magnetic, not velcro. The mallard and silver fern from the headcovers carry over, so the putter can match the woods."),
    ("bagsplus", "Bags, Pouches and Practice", "bags-pouches-and-practice",
     ["local-gc-shield-shag-bag", "Localgc-Shoebag", "players-pouch", "wool-essentials-pouch",
      "camo-range-finder-pouch", "great-outdoors-range-finder-pouch", "merbau-alignment-sticks-harbour", "swallow-alignment-stick-cover"],
     "<strong>Eight pieces &middot; NZ$50&ndash;$150 (~$28&ndash;$85)</strong>The practice gear is as thought through as the covers. The shag bag was field-tested in New Zealand before it went on sale, with an off-centre handle and a brass eyelet so you can hose the sand out. There are pouches in canvas and wool, two rangefinder cases and a shoe bag you can monogram. The merbau alignment sticks are beautiful, but they only ship within New Zealand."),
    ("flags", "Flags and Clothing", "flags-and-clothing",
     ["local-gc-golf-flag", "swallow-1-4-zip", "local-gc-monogram-beanie", "greenside-childrens-bucket-hat", "greenside-childrens-t-shirt"],
     "<strong>Five pieces &middot; NZ$18&ndash;$110 (~$10&ndash;$62)</strong>Very few small golf brands make flags, and Local GC makes them properly: regulation size, in outdoor fabric, with eyelets for a wall or a spine for a pin, and full 18-hole sets for clubs. The clothing is a short list: a swallow &frac14; zip, a monogram beanie, and the Greenside bucket hat and tee for kids."),
]
N = 55

PQ = {
    "small": ("Small runs. No shortcuts. Just good gear for walking golf.", "Local GC, Course Notes"),
    "hold": ("If it doesn&rsquo;t hold up here, it doesn&rsquo;t make the cut.", "Local GC, on testing in New Zealand conditions"),
    "rats": ("In our workshop, creativity and ridiculous ideas spend a lot of time together, and every now and then one refuses to leave.", "Local GC, on the Dead Rats cover"),
}

BANDS = {
    "bags": ("Photography &middot; Local GC&rsquo;s own", "Local GC shoots the Sunday bags on the Orewa coast and in the workshop.",
             [("band-a1", "A camo canvas Local GC Sunday bag with brown leather straps", "Camo Sunday bag"),
              ("band-a2", "The leather-wrapped stainless steel hoop at the top of a Local GC Sunday bag", "The 8-inch hoop"),
              ("band-a3", "An olive Local GC Sunday bag standing in an empty concrete garage", "The original olive")]),
    "covers": ("Photography &middot; Local GC&rsquo;s own", "Local GC shoots its covers in real golf bags, out on the course.",
             [("band-b1", "Two navy canvas headcovers with scattered manuka embroidery in a golf bag", "M&#257;nuka navy"),
              ("band-b2", "A tan leather headcover on a driver in a golf bag beside a fence", "Leather on the range"),
              ("band-b3", "Navy manuka headcovers in a grey golf bag against a wall", "Every cover different")]),
    "birds": ("Photography &middot; Local GC&rsquo;s own", "Local GC shoots its mallards and oilskins on the bag, against brick and turf.",
             [("band-d1", "Mallard canvas and wool headcovers on clubs against a brick wall", "Mallards on brick"),
              ("band-d2", "Mallard wool and canvas headcovers up close in a carry bag", "Wool and canvas"),
              ("band-d3", "Tartan and oilskin headcovers in a golf bag on artificial turf", "On the turf")]),
    "wool": ("Photography &middot; Local GC&rsquo;s own", "The wool covers live in a carry bag, at the office as often as on the course.",
             [("band-e1", "Navy and tartan wool headcovers in a green carry bag against a white wall", "Wool in the bag"),
              ("band-e2", "Check wool headcovers in a carry bag next to an office printer", "Office hours"),
              ("band-e3", "Tartan and check wool headcovers on clubs against a blue sky", "Check and tartan")]),
    "out": ("Photography &middot; Local GC&rsquo;s own", "Myles shoots the bags wherever he finds a good wall or a picnic table.",
             [("band-f1", "A navy carry bag with matching covers leaning on a schoolyard picnic table", "Picnic table"),
              ("band-f2", "An olive carry bag standing in a schoolyard", "Schoolyard"),
              ("band-f3", "The swallow embroidery and tag on the Daybreak Sunday bag", "The Daybreak")]),
    "camo": ("Photography &middot; Local GC&rsquo;s own", "The Australian-forces camo shows up on iron covers, pouches and the Sunday bags.",
             [("band-g1", "A camo canvas iron cover on a club on artificial turf", "Camo on the iron"),
              ("band-g2", "The camo Sunday bag in sunlight on a timber floor", "Camo Sunday bag"),
              ("band-g3", "The leather-trimmed top of the camo Sunday bag", "Leather trim")]),
    "colour": ("Photography &middot; Local GC&rsquo;s own", "Local GC took the camo Sunday bag down to the beach at Orewa, and shot the Daybreak in the street.",
             [("band-h1", "The camo Sunday bag standing on a tidal beach in Orewa beside a flagstick", "Orewa"),
              ("band-h2", "The Daybreak Sunday bag in blue-grey canvas with a tan strap", "Daybreak"),
              ("band-h3", "A black sailcloth headcover on a club on turf", "Sailcloth")]),
    "putter": ("Photography &middot; Local GC&rsquo;s own", "Local GC shoots its putter covers on the club, on grass and turf.",
             [("band-i1", "A camo putter cover on a putter lying on grass", "Camo putter"),
              ("band-i2", "A black sailcloth putter cover on a putter on turf", "Sailcloth putter"),
              ("band-i3", "The zip pocket on a canvas Sunday bag", "Zip detail")]),
    "kit": ("Photography &middot; Local GC&rsquo;s own", "Local GC photographs the shoe bag where you would actually use it: in the locker room.",
             [("band-j1", "An olive Local GC shoe bag with saddle shoes on a locker room bench", "Locker room"),
              ("band-j2", "The olive shoe bag unzipped on the bench", "Shoe bag"),
              ("band-j3", "A camo pouch clipped to a canvas carry bag on grass", "On the bag")]),
    "upcycled": ("Photography &middot; Local GC&rsquo;s Upcycled Customs", "Send Local GC your own clothes and it will rework them: here, a New Balance running jacket became a set of wood covers.",
             [("band-c1", "A navy New Balance fleece running jacket laid on grass", "The jacket"),
              ("band-c2", "Black headcovers made from the jacket on clubs in a carry bag", "The covers"),
              ("band-c3", "Navy pinstripe headcovers made from suit trousers on a bench", "From suit trousers")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>You can tell who Myles has been looking at. The Sunday bags follow the <a href="/drops/the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site">MacKenzie</a> recipe almost line for line: an 8-inch top, a single leather divider, waxed leather, brass and heavy canvas, sold in small drops. The Harris Tweed and tartan covers are pure <a href="/drops/brand-to-know-fyfe-golf">Fyfe</a>.</p>
    <p>The headcovers ride the trend we keep seeing this year: birds are in. Small makers are stitching ducks, pheasants and songbirds onto canvas and wool, usually the species from their own backyard (more in <a href="/drops/the-bird-edit">The Bird Edit</a>). That is what makes Local GC fun from Austin. A mallard from a New Zealand workshop, the beach birds Myles sees on his morning walks in Orewa or a swallow stitched on the other side of the world is a better story in the bag than another logo. He adds New Zealand&rsquo;s own plants, m&#257;nuka and the silver fern, the camo print issued to Australian forces, and a sense of humour most brands would not touch: dead rats, house flies and Milton&rsquo;s stapler.</p>
    <p>For an Austin golfer, the covers are the easy part. A handmade canvas cover with custom embroidery is NZ$89, about $50, which is a low price for something cut and embroidered by hand. The catch is shipping. Local GC charges NZ$35 (about $20) per item to the US and sends each one separately to stay under the tariff thresholds, so one cover lands around $70 and three cost three lots of postage. Buy the one you like most.</p>
    <p>The Sunday bags are the bigger call. At about $480, a one-off canvas bag with a stainless hoop and brass hardware costs well under a Fyfe x MacKenzie at &pound;650, and it is only one of one. If you walk Muny with a half set, the Camo #2 is the most interesting carry bag we have seen this year at that price.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Local GC is Myles Brock, working out of a workshop in Orewa on the Hibiscus Coast, north of Auckland. His About page says he started because he &ldquo;found a hole in the market when it came to locally made, quality headcovers,&rdquo; then spent months in the workshop getting the templates right. Everything is cut, sewn and embroidered in-house, and most covers are made to order in 7 to 10 days.</p>
    <p>The range has grown since: mini driver covers sized for 250&ndash;320cc heads, torque putter covers for LAB, shag bags, merbau alignment sticks, flags, and full 18-hole flag sets in sailcloth for New Zealand clubs. He also reworks customers&rsquo; own clothes into headcovers, from a running jacket to a pair of suit trousers. You can find Local GC in pro shops at Muriwai, Wainui, Pupuke, Napier and Russley, at Golf HQ, and in Sydney at NSW Golf Club and Playfair.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Orewa, New Zealand</span></div>
      <div class="sidebar-detail"><span class="l">Maker</span><span>Myles Brock</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>By hand, in-house; covers made to order in 7&ndash;10 days</span></div>
      <div class="sidebar-detail"><span class="l">US shipping</span><span>NZ$35 per item, sent separately</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>NZ$18&ndash;$850</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Beached headcover, NZ$89 (~$50)</span></div>
      <a href="https://www.localgc.co.nz/" target="_blank" rel="noopener" class="sidebar-cta">Visit Local GC &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#LocalGC</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#MadeInNZ</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Where are Local GC headcovers made?",
     "By hand in Local GC's own workshop in Orewa, north of Auckland, New Zealand. Everything is cut, sewn and embroidered in-house."),
    ("Does Local GC ship to the US?",
     "Yes. US orders are charged NZ$35 per item and each item is sent separately to stay under the tariff thresholds. Customs, duty or tax charges are the buyer's responsibility. International delivery takes 3 to 10 working days once dispatched."),
    ("How long do Local GC headcovers take to make?",
     "Most headcovers and pouches are made to order, with a lead time of 7 to 10 days before dispatch."),
    ("Does Local GC make covers for LAB putters and mini drivers?",
     "Yes. Its mallet putter covers come cut for LAB's DF3 and other zero-torque putters, and its barrel covers come in a mini driver size for 250 to 320cc heads."),
    ("Can Local GC make a custom headcover or flag?",
     "Yes. It offers in-house embroidery for monograms and logos, custom golf flags and 18-hole flag sets, and it will rework your own clothing into headcovers through its Upcycled Customs service."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-LGC-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-LGC-PQ-{key} -->\n')


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(h, idx):
    name, detail, copy = P[h]
    fr = FR[h]
    label = H.unescape(f"Local GC {name} {detail}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{BRAND} &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; {nz(h)}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{CAT[h]["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"Piece" if len(ids) == 1 else "Pieces"}</div>\n'
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
    items, pos = [], 1
    for _, _, _, ids, _ in SECTIONS:
        for h in ids:
            items.append({"@type": "ListItem", "position": pos, "url": CAT[h]["url"], "name": H.unescape(f"Local GC {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-01", "dateModified": "2026-10-01",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Local GC", "item": URL}]},
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
    ids = [h for s in SECTIONS for h in s[3]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for h in ids:
        assert FR.get(h), h
        assert CAT[h]["name"] and "*" not in P[h][0], h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Local GC</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Orewa, New Zealand &middot; handmade</span><span class="dot"></span>
    <span>{N} pieces &middot; NZ$18&ndash;$850</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A tan leather Local GC headcover on a driver in a golf bag beside a chain-link fence at the range" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    # IRL bands between every category (Lenny, 1 Oct 2026: "add IRL/Lifestyle images between catagories")
    s, n = section(SECTIONS[0], n); body += s + band("bags") + pq("small")
    s, n = section(SECTIONS[1], n); body += s + band("birds")
    s, n = section(SECTIONS[2], n); body += s + pq("rats") + band("covers")
    s, n = section(SECTIONS[3], n); body += s + band("wool")
    s, n = section(SECTIONS[4], n); body += s + band("out")
    s, n = section(SECTIONS[5], n); body += s + pq("hold") + band("camo")
    s, n = section(SECTIONS[6], n); body += s + band("colour")
    s, n = section(SECTIONS[7], n); body += s + band("putter")
    s, n = section(SECTIONS[8], n); body += s + band("kit")
    s, n = section(SECTIONS[9], n); body += s + band("upcycled")
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Manors Revisited", "Nicklaus", "Hudson Sutler", "Macade", "MORE COLOURS", "LIMITED RUN"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != N:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:40]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != len(BANDS):
        bad.append("band count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file():
            bad.append("dead link " + href)
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
