"""build-gift-guide-3b.py — 2026 Holiday Gift Guide, Part 3 of 3, brand-by-brand format (9 November 2026).
Categories 7-9: Will Last a Lifetime, Made by a Handful of People, For the Off-Season. Brand map approved by Lenny.
FACTS: product pages read November 9, 2026; prices as shown to a US visitor (Chrome). Brand facts from TGI brand index + product pages.
"""
import html as H, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gift_guide_series as GS
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "The 2026 Golf Gift Guide, Part 3: Heirlooms, Tiny Makers and Off-Season Gifts, Brand by Brand"
DESC = ("30 independent golf brands and the gifts each one does best: things built to be handed down, pieces from makers small enough "
        "to fit in a golf cart, and layers for the months when the course is cold.")
H1 = "The 2026 Golf Gift Guide, Part 3: Heirlooms, Tiny Makers and Off-Season Gifts"
BC = "Gift Guide 2026, Part 3"
SLUG = "golf-gift-guide-2026-heirlooms-tiny-makers-off-season"
IMG = "/images/gift-guide-3b"
D = json.loads((ROOT / "research/gift-guide-2026/p3b-data.json").read_text())
FRN = json.loads((ROOT / "research/gift-guide-2026/frames3b.json").read_text())
BH = json.loads((ROOT / "research/gift-guide-2026/brandhero3.json").read_text())
CUR = {"late-nine.com": ("", " kr", 0.106), "oddritualgolf.com": ("R", "", 0.057), "localgc.co.nz": ("NZ$", "", 0.59), "northernballmarkers.co.uk": ("&pound;", "", 1.33)}
FROM = {"cmdgolfco.com|custom-putter"}
DEPOSIT = {"artisangolftx.com|custom-putter", "artisangolftx.com|iron-deposit"}
NAME_FIX = {"8-airliner-style-golf-bag-premium-leather": "8&Prime; Airliner Golf Bag, Premium Leather", "slate-bison-9-x-8-leather-valuables-pouch": "Slate Bison Leather Valuables Pouch",
            "modern-driver-cover-maclaren-modern-tartan-with-natural-leather": "Maclaren Tartan Driver Cover",
            "haywood-blue-steel-signature-blade-putter-rh": "&ldquo;Blue Steel&rdquo; Signature Blade Putter", "haywood-stars-stripes-wedges-56-60-rh-limited-edition": "&ldquo;Stars &amp; Stripes&rdquo; Wedge, 56&deg; or 60&deg;",
            "piretti-handstamped-60-forged-wedge": "Handstamped 60&deg; Forged Wedge", "the-field-saddle-tan-leather-golf-headcover-handmade": "The Field Leather Headcover, Saddle Tan",
            "premium-italian-buttero-leather-golf-yardage-book-scorecard-holder": "Italian Buttero Leather Scorecard Holder", "bluegrass-fairway-shoe-bag-in-blackwatch-waxed-canvas": "Blackwatch Waxed Canvas Shoe Bag",
            "redan-putter-cover-in-black-napa-leather": "Redan Putter Cover, Black Napa", "bogey-boy-tee": "Bogey Boy Tee", "red-lobster-hoodie": "Red Lobster Hoodie", "og-knit-jumper": "OG Knit Jumper", "waffle-polo": "Waffle Polo",
            "the-diamond-trusty-driver-golf-headcover-in-genuine-leather": "Diamond TRUSTY Leather Driver Cover", "dancing-trusty-fairway-wood-headcover": "Dancing TRUSTY Fairway Cover",
            "old-faithful-trusty-caddy-golf-towel-copy-1": "TRUSTY Caddy Towel", "trusty-ball-marker-pouch-full-grain-leather": "TRUSTY Ball Marker Coin Tote",
            "harris-tweed-barrel-cover-3": "Shamrock Harris Tweed Barrel Cover", "homestead-blade-cover-copy": "Homestead Leather Mallet Cover", "large-hammered-edge-big-dog®-golf-co-ball-marker": "Hammered Edge Ball Marker",
            "italian-calfskin-leather-belt-cognac": "Italian Calfskin Belt, Cognac", "electric-lamb-putter-cover-black-blue": "Electric Lamb Putter Cover",
            "cable-knit-polo-burgundy": "Cable Knit Merino Polo, Burgundy", "instructors-jacket-cotton-navy": "Instructors Jacket, Navy", "5-pocket-cords-olive": "5-Pocket Cords, Olive", "ribbed-vest-dark-brown": "Ribbed Merino Vest, Brown",
            "the-douglas": "The Douglas Puffer Vest", "the-gordo-copy": "The Ry Quarter-Zip", "scottish-thistle-quarter-zip-pullover-copy": "The Steve D Thistle Quarter-Zip", "white-tarraing-highland-cow-hat-copy": "Highland Cow Hat, Stone &amp; Green",
            "eden-base-layer-with-pointelle-star-dark-navy": "Eden Cotton-Cashmere Knit", "good-look-crew-in-deep-orange-cotton": "Good Look Crew, Deep Orange", "sounder-ribbed-bobble-hat-green": "Ribbed Bobble Hat",
            "original-jones-bag-navy-red-white": "Original Jones Bag, Navy/Red/White", "trouper-4-0-ecru": "Trouper Stand Bag, Ecru", "rider-bag-navy-white": "Rider Bag, Navy/White", "players-series-deep-green-kodiak": "Players Series Bag, Deep Green", "mackenzie-bag": "MacKenzie Original Walker Bag, Leather", "mackenzie-original-walker-bag-canvas": "MacKenzie Original Walker Bag, Waxed Canvas",
            "custom-putter": None, "iron-deposit": "Custom Iron Set, Fitting Deposit", "organic-ventile-jacket": "Organic Ventile Jacket", "mens-organic-ventile-jacket": "Organic Ventile Jacket"}
def nm(k):
    v = D[k]; h = k.split("|")[1]
    t = NAME_FIX.get(h) or v["title"]
    if k == "artisangolftx.com|custom-putter": t = "Custom Putter, Fitting Deposit"
    t = re.sub(r"\s*[-–|]\s*(Pre-Order|Preorder)\b.*", "", t)
    t = t.replace("™", "").replace(" - ", ", ").replace(" | ", ", ").replace(" · ", ", ").replace(" – ", ", ")
    t = re.sub(r"\s*\[([^\]]+)\}?\]?$", r", \1", t)
    t = re.sub(r"\s*\(([^)]+)\)$", r", \1", t)
    if t.isupper(): t = t.title()
    return t
def pr(k):
    v = D[k]; p = v["price"]
    s = f"{p:,.2f}".replace(".00", "")
    if v["d"] in CUR:
        a, b, r = CUR[v["d"]]; return f"{a}{s}{b} (~${round(p*r)})"
    if k in FROM: return f"from ${s}"
    if k in DEPOSIT: return f"${s} deposit"
    return f"${s}"
def K(d, h):
    k = f"{d}|{h}"; assert k in D and "err" not in D[k], k; return k
NAME_FIX.update({"8-airliner-style-leather": "8&Prime; Airliner Golf Bag, Premium Leather", "weather-golf-bag-covers": "Waxed Canvas Rain &amp; Storage Hood",
 "modern-driver-cover-maclaren-modern-tartan-with-natural-leather-trim": "Maclaren Tartan Driver Cover", "dallas-mural-headcovers": "Dallas Mural Leather Headcover",
 "the-field-saddle-tan-leather-golf-headcover-handmade-driver-fairway-hybrid-cover-copy": "The Field Leather Headcover, Saddle Tan",
 "premium-italian-buttero-leather-golf-scorecard-holder-yardage-book-cover-black": "Italian Buttero Leather Scorecard Holder", "redan-putter-cover-in-black-leather": "Redan Putter Cover, Black Napa",
 "mens-ventile-windbreaker": "Organic Ventile Jacket", "mens-golf-quarter-zip": "Organic Cotton Fleece Quarter-Zip", "mens-merino-wool-golf-polo": "Merino Polo", "mens-ventile-vest": "Organic Ventile Vest",
 "grid-fleece-windbreaker-carbon-blue": "Grid Fleece Windbreaker", "cashmere-watch-cap-oatmeal-heather": "Cashmere Watch Cap", "grid-fleece-golf-carbon-blue": "Grid Fleece Pant",
 "two-golf-club-head-covers-retro-vintage-blue-white-with-tassels-for-fairway-woods-copy": "Hand-Knit Fairway Covers, Blue &amp; White (Pair)",
 "three-golf-club-head-covers-retro-vintage-light-pink-green-white-with-tassels-for-drivers-woods": "Hand-Knit Covers, Pink, Green &amp; White",
 "hand-knit-golf-club-head-covers-retro-vintage-blue-yellow-gray-with-tassels-for-fairway-woods": "Hand-Knit Fairway Covers, Blue &amp; Yellow",
 "diamondback-stencil-lab-edition": "Desert Diamondback Wedge Engraving", "desert-roadrunner-ball-marker": "Desert Roadrunner Copper Marker", "custom-ball-marker": "Custom Portrait Ball Marker",
 "lamb-crafted-scout-bag-lamb-script": "Lamb Crafted x Jones Scout Duffle", "contrast-quarter-zip-butter": "Contrast Quarter-Zip, Butter", "golfs-hard-crew": "Golf&rsquo;s Hard Crew",
 "the-caddie-jacket-navy": "The Caddie Jacket, Navy", "orgc-sweater-blue": "ORGC Sweater, Blue", "orgc-traditions-crewneck-burgundy": "ORGC Traditions Crewneck, Burgundy", "pleated-daily-trouser-black": "Pleated Daily Trouser, Black",
 "pac-mach-jacket-deep-navy-ripstop": "Pac Mach Packable Jacket", "clubglider3-tour": "ClubGlider3 Tour Travel Bag", "ezpz": "EZPZ Putter", "gravity-grip-gg1-black": "Gravity Grip GG1",
 "bogey-boy-tee": "Bogey Boy Tee"})
CATS = [
 ("lifetime", "Will Last a Lifetime", "Built to be handed down",
  "Some gifts get replaced every season. These get handed down. Full leather bags, forged irons, milled putters, waxed canvas and Crazy Horse leather that looks better with every round. None of it is cheap, and all of it is built to outlast the clubs it carries.",
  [("Sun Mountain", "Missoula, Montana", "Sun Mountain invented the modern stand bag in 1986 and still assembles bags in Montana. The Legacy is the full-leather version of the stand bag it made famous. The striped Boston bag handles the overnight trip, and the ClubGlider3 Tour is the ripstop travel bag built bigger for tour pros.",
    [K("sunmountain.com","legacy-leather-stand-bag"),K("sunmountain.com","mid-stripe-boston-bag"),K("sunmountain.com","clubglider3-tour")]),
   ("Steurer &amp; Jacoby", "", "The Airliner is a full leather carry bag cut from American-tanned hides with American-made brass hardware, big enough for a modern set. The waxed canvas weather hood, a slate bison pouch and a Scottish tartan driver cover round it out. Handmade pieces can take four to six weeks.",
    [K("steurerjacoby.com","8-airliner-style-leather"),K("steurerjacoby.com","weather-golf-bag-covers"),K("steurerjacoby.com","slate-bison-9-x-8-leather-valuables-pouch"),K("steurerjacoby.com","modern-driver-cover-maclaren-modern-tartan-with-natural-leather-trim")]),
   ("Winston Collection", "Rochester Hills, Michigan", "Custom leather goods made largely in the USA since 2006. Crazy Horse leather is waxed to age as it&rsquo;s used, which is the whole point of the Hermosa weekender and the Reef pouch. The Torino drawstring pouch is Italian pebble-grain, and the Dallas cover is embroidered with the city.",
    [K("winstoncollection.com","hermosa-weekender-bag-crazy-horse-leather"),K("winstoncollection.com","reef-zip-pouch-crazy-horse-leather"),K("winstoncollection.com","drawstring-players-pouch-in-torino-leather"),K("winstoncollection.com","dallas-mural-headcovers")]),
   ("Artisan Golf", "Fort Worth, Texas", "Two ex-Nike craftsmen in Nike&rsquo;s old Fort Worth building, grinding wedges by hand. Custom putters and iron sets start with a fitting and a $300 deposit. The Energy Drop wedges are ready to order in Tour Satin or Texas Crude.",
    [K("artisangolftx.com","custom-putter"),K("artisangolftx.com","energy-drop-tour-satin"),K("artisangolftx.com","energy-drop-texas-crude"),K("artisangolftx.com","iron-deposit")]),
   ("Haywood Golf", "Vancouver, Canada", "Vancouver, 2018: forged irons built in-house and sold direct at near off-the-rack prices. The CB2 + MB2 combo is the set we&rsquo;d pick. The Blue Steel blade is Cerakoted deep blue down a matching shaft, and the Stars &amp; Stripes wedges are a limited micro-batch.",
    [K("haywoodgolf.com","cb2-mb2-forged-combo-irons"),K("haywoodgolf.com","haywood-blue-steel-signature-blade-putter-rh"),K("haywoodgolf.com","haywood-stars-stripes-wedges-56-60-rh-limited-edition"),K("haywoodgolf.com","magnetic-golf-towel")]),
   ("Piretti", "Spring, Texas", "Putters milled from solid billets since 2008, and never a cast one. The Potenza LN and Savona Elite are milled from 303 stainless, the Paragon Matera is the newest series, and the handstamped 60&deg; wedge comes from Fujimoto Forgings.",
    [K("pirettigolf.com","elite-series-potenza-ln"),K("pirettigolf.com","savona-elite"),K("pirettigolf.com","paragon-series-matera-db"),K("pirettigolf.com","piretti-handstamped-60-forged-wedge")]),
   ("Golden Soul", "Colombia", "Handmade leather and wool from Colombia, and most pieces are one of a kind. The Beaumont is woven leather cut to fit LAB&rsquo;s OZ.1 putter, the Wren driver cover is woven from hand-cut strips, and the Belmont is an all-leather Sunday bag made in-house.",
    [K("goldensoulgolf.com","beaumont-1"),K("goldensoulgolf.com","wren-driver"),K("goldensoulgolf.com","the-belmont-sunday"),K("goldensoulgolf.com","rivelle-scorecard")]),
   ("Evnroll", "Carlsbad, California", "Milled putters and grips built in Carlsbad since 2016. The ORIGIN ER2cs is a center-shafted take on Evnroll&rsquo;s most-awarded design, the EZPZ is its reverse-torque putter, and the V5.1 is a players mallet. The Gravity Grip is the stocking-sized way in.",
    [K("evnroll.com","origin-er2cs-satin"),K("evnroll.com","ezpz"),K("evnroll.com","v-series-v5-1-midlock-mallet-putter"),K("evnroll.com","gravity-grip-gg1-black")]),
   ("Bluegrass Fairway", "Louisville, Kentucky", "Leather, Harris Tweed and waxed canvas made in Louisville since 2015. The Field headcover is full-grain leather built to earn a patina, the scorecard holder is Italian Buttero leather, and the shoe bag pairs British Millerain canvas with Milwaukee leather.",
    [K("bluegrassfairway.com","the-field-saddle-tan-leather-golf-headcover-handmade-driver-fairway-hybrid-cover-copy"),K("bluegrassfairway.com","premium-italian-buttero-leather-golf-scorecard-holder-yardage-book-cover-black"),K("bluegrassfairway.com","bluegrass-fairway-shoe-bag-in-blackwatch-waxed-canvas"),K("bluegrassfairway.com","redan-putter-cover-in-black-leather")]),
   ("MacKenzie", "Portland, Oregon", "MacKenzie has made carry bags by hand in Oregon since 1985, and some of its best work lives in its collaborations. The Original Walker comes in sage waxed canvas or full-grain leather through Miura, the Miura x Sentinel edition is the newest, and Sugarloaf Social Club&rsquo;s canvas bag wears a chenille patch. Every one is handmade in Portland.",
    [K("miuragolf.com","miura-x-sentinel-mackenzie-walker-bag-2026"),K("miuragolf.com","mackenzie-original-walker-bag-canvas"),K("miuragolf.com","mackenzie-bag"),K("www.sugarloafsocialclub.com","ssc-x-mackenzie-golf-bag")])]),
 ("handful", "Made by a Handful of People", "Small enough to fit in a golf cart",
  "Some of the best things in golf are made by people you could fit in a golf cart. One person screen-printing in Perth, one machinist in Massachusetts, a copper stamper on Long Island, a knitter in Austin. Buy from them and the money goes straight to the person who made it.",
  [("Okka Golf", "Perth, Australia", "One person in Perth screen-prints everything and refuses wholesale on principle. The Bogey Boy tee was designed by Papa Prosciutto and printed by hand, the Red Lobster hoodie is printed front and back on heavy fleece, and the OG knit is the dressed-up option.",
    [K("okkagolf.com","bogey-boy-tee"),K("okkagolf.com","red-lobster-hoodie"),K("okkagolf.com","og-knit-jumper"),K("okkagolf.com","waffle-polo")]),
   ("Coggin Machine &amp; Design", "Massachusetts", "Jayme Coggin machines CMD&rsquo;s tools and putters himself. The threaded single-prong tool is stainless, and bespoke putters start at $1,500 with a deposit and take as long as they take. The Garsen grip and cocktail tees are the small way in.",
    [K("cmdgolfco.com","custom-putter"),K("cmdgolfco.com","threaded-single-prong-tool"),K("cmdgolfco.com","garsen-cmd-quad-tour-non-taper"),K("cmdgolfco.com","cocktail-themed-bamboo-tees-50-count")]),
   ("Golf Life Metals", "Long Island, New York", "Jon Millman hand-stamps copper ball markers on Long Island. Pick a moment, like the Shinnecock US Open or a Ryder Cup warning, or have a name or initials stamped instead.",
    [K("glmgolf.com","us-open-shinnecock"),K("glmgolf.com","ryder-cup-warning"),K("glmgolf.com","name-initials")]),
   ("Northern Ball Markers", "Newcastle, England", "A one-man business in Newcastle making markers and divot tools in brass and copper. The screw-ferrule divot tool takes a colored ferrule, and the combo pairs a custom marker with a single-prong tool. Prices are in pounds.",
    [K("northernballmarkers.co.uk","screw-ferrule-divot-tool-brass"),K("northernballmarkers.co.uk","two-prong-divot-tool-copper"),K("northernballmarkers.co.uk","custom-ball-marker-single-prong-divot-tool-combo-copper"),K("northernballmarkers.co.uk","jammie-d-bite-multi-metal-ball-marker")]),
   ("Old Faithful Golf Co.", "Canada", "A small Canadian brand built around Trusty, a dog with a club in its mouth. Leather covers with Trusty front and center, a striped caddy towel, and a leather coin tote for the marker that means something.",
    [K("oldfaithfulgolf.com","the-diamond-trusty-driver-golf-headcover-in-genuine-leather"),K("oldfaithfulgolf.com","dancing-trusty-fairway-wood-headcover"),K("oldfaithfulgolf.com","old-faithful-trusty-caddy-golf-towel-copy-1"),K("oldfaithfulgolf.com","trusty-ball-marker-pouch-full-grain-leather")]),
   ("Local GC", "Orewa, New Zealand", "Handmade headcovers and Sunday bags from an Orewa workshop: mallards, beach birds and a sense of humor. The Daybreak Sunday bag is the big one, and the Mallard and Beached covers and the shag bag make up the rest. Prices are in New Zealand dollars.",
    [K("localgc.co.nz","daybreak-local-gc-sunday-bag"),K("localgc.co.nz","mallard-canvas-head-cover"),K("localgc.co.nz","beached-head-cover"),K("localgc.co.nz","local-gc-shag-bag")]),
   ("Show Out Engraving", "Gilbert, Arizona", "Copper markers laser-engraved and finished by hand, led by a desert roadrunner in sunglasses. Stencil Lab designs like the Desert Diamondback are engraved on your own wedge, and the portrait marker turns a photo into brass.",
    [K("showoutengraving.com","diamondback-stencil-lab-edition"),K("showoutengraving.com","desert-roadrunner-ball-marker"),K("showoutengraving.com","custom-ball-marker")]),
   ("AustinKnittyLimits", "Austin, Texas", "Hand-knit retro headcovers from Austin, made one at a time by a maker who learned from their mother. Tassels, stripes, and custom colors on request.",
    [K("austinknittylimits.com","two-golf-club-head-covers-retro-vintage-blue-white-with-tassels-for-fairway-woods-copy"),K("austinknittylimits.com","three-golf-club-head-covers-retro-vintage-light-pink-green-white-with-tassels-for-drivers-woods"),K("austinknittylimits.com","hand-knit-golf-club-head-covers-retro-vintage-blue-yellow-gray-with-tassels-for-fairway-woods")]),
   ("Big Dog Golf Co.", "Wodonga, Australia", "Leather and Harris Tweed covers stocked in the pro shops at Royal Melbourne, Barnbougle and Cape Wickham. The Shamrock barrel is genuine Harris Tweed, the Cowboy scorecard holder is hair-on hide, and the Homestead mallet cover is diamond-stitched full-grain leather.",
    [K("bigdoggolfco.com","harris-tweed-barrel-cover-3"),K("bigdoggolfco.com","cowboy-scorecard-holder"),K("bigdoggolfco.com","homestead-blade-cover-copy"),K("bigdoggolfco.com","large-hammered-edge-big-dog®-golf-co-ball-marker")]),
   ("Lamb Crafted", "Plano, Texas", "A six-person Texas machine shop working from Tyson Lamb&rsquo;s bench: engraved putters, markers and leather. The Electric Lamb putter cover and the cognac calfskin belt are stitched in the USA, and the Scout duffle is a collaboration with Jones Sports Co.",
    [K("lambcrafted.com","electric-lamb-putter-cover-black-blue"),K("lambcrafted.com","italian-calfskin-leather-belt-cognac"),K("lambcrafted.com","lamb-crafted-scout-bag-lamb-script"),K("lambcrafted.com","texas-embroidered-belt")])]),
 ("off-season", "For the Off-Season", "For the months the course is cold",
  "Somewhere between November and March most golfers play less and think about golf more. These ten brands make the layers for the cold rounds that still happen and for the months in between: merino, cashmere, waxed cotton, fleece and a few good jackets.",
  [("Metalwood Studio", "Los Angeles, California", "Cole Young&rsquo;s LA studio mines Y2K tour style. A brown western-yoke track jacket, a tan raglan blouson, a navy contrast-stitch mock neck and the black Alien crew.",
    [K("metalwood.studio","western-yolk-track-jacket-brown"),K("metalwood.studio","raglan-sleeve-blouson-tan"),K("metalwood.studio","contrast-stitch-mock-neck-sweatshirt-navy"),K("metalwood.studio","alien-crewneck-sweatshirt-black")]),
   ("Casualist", "London, England", "Elie Reboul&rsquo;s West London label makes quiet clothes for golf and after. The Grazer vest is 100% merino, the Cart Path jacket is ripstop with a vented back, and the wool tartan cap is the vintage touch.",
    [K("casualist.com","grazer-cardigan-vest-grey"),K("casualist.com","cart-path-ripstop-jacket"),K("casualist.com","all-the-gear-sweatshirt"),K("casualist.com","legacy-wool-5-panel-cap")]),
   ("Late Nine", "Stockholm, Sweden", "Maxim Lundh&rsquo;s label is built on late-&rsquo;90s tour golf, with no elastane anywhere. First-shearing merino in the cable knit polo and ribbed vest, an Instructors jacket modeled on the blousons &rsquo;90s teaching pros wore, and baby-cord trousers. Prices are in Swedish kronor.",
    [K("late-nine.com","cable-knit-polo-burgundy"),K("late-nine.com","instructors-jacket-cotton-navy"),K("late-nine.com","5-pocket-cords-olive"),K("late-nine.com","ribbed-vest-dark-brown")]),
   ("Left of Field", "Sydney, Australia", "Surf and skate shapes for the course, with every collection named for a stretch of Australian coast. The Bridgewater quarter-zip, Portsea jacket, pleated pant and striped Mornington polo are all marked down right now.",
    [K("lofgolf.com","bridgewater-1-4-zip"),K("lofgolf.com","portsea-jacket"),K("lofgolf.com","pleated-lite-pant-slate"),K("lofgolf.com","mornington-polo-blue-white-stripe")]),
   ("Radry Golf", "Sheboygan, Wisconsin", "A Wisconsin artist whose logo is a bird in a bucket hat, est. 2018, and every design is drawn before it&rsquo;s stitched. A butter-yellow contrast quarter-zip, the heavyweight Staple hoodie and the Golf&rsquo;s Hard crew.",
    [K("radrygolf.com","contrast-quarter-zip-butter"),K("radrygolf.com","staple-hoodie"),K("radrygolf.com","golfs-hard-crew"),K("radrygolf.com","belly-up-hat")]),
   ("Odd Ritual", "Cape Town, South Africa", "Born in Cape Town and named for the small habits before every shot. The navy Caddie jacket is cotton twill, the ORGC sweater and pigment-washed crew are the heavy layers, and the pleated trouser finishes it. Prices are in South African rand.",
    [K("oddritualgolf.com","the-caddie-jacket-navy"),K("oddritualgolf.com","orgc-sweater-blue"),K("oddritualgolf.com","orgc-traditions-crewneck-burgundy"),K("oddritualgolf.com","pleated-daily-trouser-black")]),
   ("Tarraing Golf", "United States", "Inspired by the golf of Ireland and Scotland, with pieces named after people and a highland cow on the hat. The Douglas puffer vest, the Ry and Steve D quarter-zips, and the cow hat.",
    [K("tarrainggolf.com","the-douglas"),K("tarrainggolf.com","the-gordo-copy"),K("tarrainggolf.com","scottish-thistle-quarter-zip-pullover-copy"),K("tarrainggolf.com","white-tarraing-highland-cow-hat-copy")]),
   ("Sounder", "London, England", "British golf clothing from the founders of Folk and Urban Golf, named for Seve&rsquo;s first clubs. A packable Japanese ripstop jacket, a cotton-cashmere knit, a deep orange cotton crew and a bobble hat for the coldest tee times.",
    [K("soundergolf.com","pac-mach-jacket-deep-navy-ripstop"),K("soundergolf.com","eden-base-layer-with-pointelle-star-dark-navy"),K("soundergolf.com","good-look-crew-in-deep-orange-cotton"),K("soundergolf.com","sounder-ribbed-bobble-hat-green")]),
   ("Rookline", "New York", "Long Island natives making golf clothes from the round. The windbreaker and pant are Japanese Stormfleece with a wool interior, and the hoodie and watch cap are 100% cashmere.",
    [K("rookline.com","grid-fleece-windbreaker-carbon-blue"),K("rookline.com","ottoman-rib-cashmere-hoodie"),K("rookline.com","cashmere-watch-cap-oatmeal-heather"),K("rookline.com","grid-fleece-golf-carbon-blue")]),
   ("SLOAT", "San Francisco, California", "Named for Sloat Boulevard, natural fibers only, sewn in Portugal. An organic Ventile jacket and vest, a 480gsm organic cotton fleece quarter-zip and an RWS merino polo.",
    [K("sloat.cc","mens-ventile-windbreaker"),K("sloat.cc","mens-golf-quarter-zip"),K("sloat.cc","mens-merino-wool-golf-polo"),K("sloat.cc","mens-ventile-vest")])]),
]
GIFTED = set()
SECTIONS = [(c[1], c[0], [k for b in c[4] for k in b[3]], c[2]) for c in CATS]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
CSS = ('<style>/*TGI-GG-BRAND*/.gg-brand{max-width:1180px;margin:0 auto;padding:44px 0 8px;border-top:1px solid rgba(20,20,20,.12)}'
 '.gg-bhero{margin:0 0 18px;aspect-ratio:2000/860;overflow:hidden}.gg-bhero img{width:100%;height:100%;object-fit:cover;display:block}.gg-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.gg-bhead{max-width:760px;margin:0 auto 22px;text-align:center}.gg-cat{margin-top:72px;padding-top:56px;border-top:3px solid #2d4a2b}.gg-cat .products-hdr{font-size:clamp(40px,6.2vw,72px);line-height:1.02;letter-spacing:-.01em;margin:10px 0 10px}.gg-bname{font-size:30px;margin:8px 0 10px;line-height:1.15}'
 '.gg-bwhy{font-size:17px;line-height:1.6;margin:0}.gg-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
 '.gg-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr));max-width:900px;margin:0 auto}'
 '.gg-grid .product-name{font-size:15px}.gg-grid .product-body{padding:12px 12px 14px}'
 '@media(max-width:900px){.gg-grid,.gg-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
 '.gg-nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px auto 0;max-width:900px}.gg-nav a{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid rgba(20,20,20,.25);padding:4px 8px}</style>\n')
ML = json.loads((ROOT / "research/gift-guide-2026/model-lead.json").read_text()).get("3", {})  # on-model frame leads (Lenny, 9 Nov 2026)
def card(k, idx):
    v = D[k]; fr = FRN[k]
    if k in ML: fr = [fr[ML[k]]] + [x for i, x in enumerate(fr) if i != ML[k]]
    brand = v.get("brand", "")
    label = H.unescape(nm(k)).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-name">{nm(k)} &middot; {pr(k)}</div>'
            f'<a href="{v["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')
def bslug(n): return re.sub(r"[^a-z0-9]+", "-", H.unescape(n).lower()).strip("-")
def category(c, n0, num):
    anchor, title, kicker, intro, brands = c
    nav = "".join(f'<a href="#b-{bslug(b[0])}">{b[0]}</a>' for b in brands)
    o = (f'\n<section class="products gg-cat">\n  <div class="drop-tag grass">{num:02d} &middot; {len(brands)} brands</div>\n'
         f'  <h2 class="products-hdr" id="{anchor}">{title}</h2>\n  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
         f'  <div class="writeup-body" style="max-width:760px;margin:0 auto 10px;"><p>{intro}</p></div>\n  <div class="gg-nav">{nav}</div>\n')
    for name, loc, why, keys in brands:
        cards = "".join(card(k, n0 + j) for j, k in enumerate(keys)); n0 += len(keys)
        lc = f'<div class="drop-tag grass" style="display:inline-block">{loc}</div>' if loc else ""
        hero = BH[H.unescape(name)]
        o += (f'  <div class="gg-brand" id="b-{bslug(name)}"><figure class="gg-bhero"><img src="{hero}" alt="{H.escape(H.unescape(name))}" loading="lazy" /><h3 class="gg-sr">{name}</h3></figure>'
              f'<div class="gg-bhead">{lc}<p class="gg-bwhy">{why}</p></div>'
              f'<div class="products-grid gg-grid" data-n="{len(keys)}">{cards}</div></div>\n')
    return o + "</section>\n", n0
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Part 3 closes the guide with the gifts that take the longest view. Things built to outlast the person who opens them, things made by one or two people at a bench, and the layers that get a golfer through the months when the course is cold. Same format as <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">Parts 1</a> and <a href="/drops/golf-gift-guide-2026-statement-pieces-colorways-splurges">2</a>: each brand gets its own block, and none of the ninety brands across the guide appears twice.</p>
    <p>Thirty brands, from an $11 hammered ball marker out of Wodonga to a $2,700 all-leather Sunday bag from Colombia. Several of these makers work to order, so the earlier you buy, the better.</p>
    <p><strong>Where to start.</strong> For something to hand down, Sun Mountain&rsquo;s Legacy leather stand bag. For a tiny maker, a hand-knit set from AustinKnittyLimits. For the off-season, SLOAT&rsquo;s organic Ventile jacket.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Gifts</span><span>@@N@@</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$11&ndash;$2,700</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>3 of 9</span></div>
      <div class="hashtags"><span class="hashtag">#GolfGiftGuide</span><span class="hashtag">#GolfGifts</span><span class="hashtag">#IndieGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Order Early, Then Wait</h2>
    <p>The gifts in this part reward patience. Leather gets better with use, small makers work through a queue, and a good winter layer earns its place in February, not on Christmas morning.</p>
    <p><strong>Check the timing.</strong> Artisan&rsquo;s putters and irons and CMD&rsquo;s bespoke putters start with a deposit and a build. Steurer &amp; Jacoby asks four to six weeks for handmade pieces. Left of Field is on sale now, and MacKenzie collaborations are limited runs, so neither will wait long.</p>
    <p>Prices are as each store shows them to a US visitor. Late Nine, Odd Ritual, Local GC and Northern Ball Markers show their own currencies, so those dollar figures are approximate. Everything was available to order on November 9, 2026. <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">Part 1</a> and <a href="/drops/golf-gift-guide-2026-statement-pieces-colorways-splurges">Part 2</a> cover the other six categories.</p>
  </div>
</section>
"""
HERO_ALT = "Three gifts: a brown leather Sun Mountain stand bag and duffle on the grass, three hand-knit striped headcovers from AustinKnittyLimits, and a golfer in silhouette at sunset in Sounder"
def head_top(n):
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": D[k]["url"], "name": H.unescape(nm(k))} for i, k in enumerate(k for c in CATS for b in c[4] for k in b[3])]
    blocks = [{"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
               "datePublished": "2026-11-09", "dateModified": "2026-11-09",
               "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
               "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
              {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
                  {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
                  {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]}]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            f'<title>{t} | The Grassy Issue</title>\n<meta name="description" content="{d}" />\n<link rel="icon" href="/favicon.ico" />\n<link rel="apple-touch-icon" href="/apple-touch-icon.png" />\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com" />\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
            f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />\n'
            f'<meta property="og:type" content="article" />\n<meta property="og:url" content="{URL}" />\n<meta property="og:title" content="{t}" />\n<meta property="og:description" content="{d}" />\n'
            f'<meta property="og:image" content="{og}" />\n<meta property="og:site_name" content="The Grassy Issue" />\n<meta name="twitter:card" content="summary_large_image" />\n'
            f'<meta name="twitter:title" content="{t}" />\n<meta name="twitter:description" content="{d}" />\n<link rel="canonical" href="{URL}" />\n<link rel="preload" as="image" href="{IMG}/hero.jpg" />\n{ld}')
def main(apply_):
    keys = [k for c in CATS for b in c[4] for k in b[3]]
    assert len(keys) == len(set(keys))
    for k in keys: assert FRN.get(k), k
    n = len(keys)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = (f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  {BC}</div>\n\n'
            f'<header class="drop-header">\n  <h1>{H1}</h1>\n  <div class="drop-meta">\n    <span>The Guide &middot; Holiday Gift Guide 2026, Part 3 of 3</span><span class="dot"></span>\n'
            f'    <span>30 brands &middot; {n} gifts &middot; in stock, checked November 9, 2026</span>\n  </div>\n</header>\n\n'
            f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>\n')
    body += GS.nav(3)
    body += TAKE.replace("@@N@@", str(n))
    i = 1
    for num, c in enumerate(CATS, 7):
        o, i = category(c, i, num); body += o
    body += CLOSE
    body += GS.nav(3, "Keep going: the rest of the 2026 Gift Guide")
    out = head_top(n) + head_rest.replace("</head>", CSS + GS.CSS + "</head>", 1) + body + tail
    print(f"  {n} cards, {sum(len(c[4]) for c in CATS)} brands")
    if not apply_: return
    OUT.write_text(out, encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", out[:out.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if "Mackem" in above: bad.append("leak")
    txt = re.sub(r"<[^>]+>", " ", above).replace("Fort Worth", "")
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', out)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! " + "; ".join(bad))
    print("  wrote", OUT.relative_to(ROOT))
if __name__ == "__main__": main("--apply" in sys.argv)
