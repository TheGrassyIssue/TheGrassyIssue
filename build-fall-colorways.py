#!/usr/bin/env python3
"""build-fall-colorways.py — Fall golf colorways, 2 November 2026. Cloned from build-color-combos.py.
Lenny: "post about Fall golf colorways- 4-6 on trend + timeless options... Camo and also Hunter vibrant Orange in the mix", then "let's build the post- you pick the options".
Picks: 8 pairings x 6, live Shopify products.json via the browser Nov 2 2026 (US stores, USD). Trend sourcing: FW26 runway/retail coverage (The Impression, Hypebeast, Lyst, Harrods).
ORIGINAL DOCSTRING: — "Seven Golf Color Combos to Mix and Match" 13 October 2026.
Lenny: "using this post as a base of an idea of color combos let's do a post about mixing and matching colors with headcovers,
clothes, etc." (a design account's palette carousel, not named or linked), then "minimum 7 options in each category and then a
whole bunch of lifestyle IRL images at the bottom and call it from the look books and in the wild", "it would be Red Wine not
Wine red", "I like Linen & Cream as names", "build the post".
FACTS: hex codes from the palette carousel. Products and prices read live on each brand's store October 13, 2026 (Shopify .js /
Squarespace JSON). Dropped at build: Fyfe Jura Sunset (sold out), Jones "Original Bag, Burnt Clay" (not sold in that colour),
Mantra/Merrill "Clay" (read as stone/grey, not orange), RIPIT lilac and Parmore bone tee (off-palette), Woodgrain cream trouser
duplicate in Royal. Conversions: EUR x1.12, GBP x1.3234, AUD x0.70, NZD x0.57, ZAR x0.055; set US prices shown second.
PHOTOS: hero is Students Golf's own (homepage, Fall 2026). Others each brand's own, reused from earlier TGI posts (research/color-combos/frame.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Fall Golf Colorways for 2026: Sage, Hunter Orange, Chocolate and 5 More Pairings"
DESC = ("Nine pieces in each of eight fall golf color pairings, six on trend and two that never miss: sage and ecru, hunter orange and charcoal, chocolate and cream, "
        "racing green and butter, burgundy and stone, olive and tan, navy and heather gray, camel and charcoal. 72 pieces in stock.")
H1 = "Fall Golf Colorways: Six on Trend, Two That Never Miss"
BC = "Fall Golf Colorways"
SLUG = "fall-golf-colorways-2026"
IMG = "/images/fall-colorways"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 # Sage + Ecru
 "s1": ("Eastside Golf", "Sage Snap Placket Polo, Houndstooth", "$88", U("eastsidegolf.com","ep2040339-330-sage-snap-placket-polo-houndstooth"),
   "A sage polo in a big-scale houndstooth print with a snap placket and a small swingman on the hem. The easiest sage on the list."),
 "s3": ("52 Sundays", "Hermosa Sage Polo", "$60", U("52sundays.co","hermosa-sage-polo"),
   "A sage polo with a vertical pattern and a cream collar, named for Hermosa Avenue. S to XXXL."),
 "s2": ("Bad Birdie", "Golf Pant, Washed Sage", "$110", U("badbirdiegolf.com","golf-pant-washed-sage"),
   "Sage golf trousers in a washed finish. Wear them with an ecru sweater and nothing else needs to match."),
 "s6": ("Devereux", "Waffle Hoodie, Bone", "$84", U("devereuxgolf.com","waffle-hoodie-bone"),
   "The ecru half: a waffle-knit hoodie in bone. Over a sage polo, or with the sage pants."),
 "s5": ("Kingfisher Golf", "Sage Green DAL Cap", "$36", U("kingfisher-golf.com","sage-green-dal-cap"),
   "A cream cap with a sage brim and a green DAL on the front. Sage and ecru on one hat."),
 "s7": ("Jones Sports Co", "Trouper 4.0, Ecru", "$395", U("jonessportsco.com","trouper-4-0-ecru"),
   "An ecru stand bag with leather trim, the cleanest color Jones makes. It goes with everything in this section."),
 "s4": ("Sunday Golf", "Ranger Premium Stand Bag, Sage", "$400", U("sundaygolf.com","ranger-sage-premium-stand-bag"),
   "A sage stand bag with darker green panels, from San Diego&rsquo;s Sunday Golf."),
 "s9": ("52 Sundays", "Fairway Hat, Eucalyptus", "$35", U("52sundays.co","fairway-hat-eucalyptus"),
   "A pale eucalyptus cap with a script F. The softest sage here."),
 "s8": ("ITL Golf", "ITL 2.0 Signature Glove, Mint", "$30", "https://itlgolf.com/products/mens-itl-2-0-signature-glove-seasonal-colors",
   "A mint Cabretta leather glove from Calgary&rsquo;s ITL. Also in Sage, Olive and Augusta Green."),
 "t1": ("Three Putt Golf Clothing", "Dogleg Cotton Golf Polo, Brown with Cream", "$48", "https://threeputtgolfclothing.co.uk/products/dogleg-golf-polo",
   "A chocolate cotton polo with cream panels curving over the shoulders, from West Yorkshire&rsquo;s Three Putt. Chocolate and cream on one shirt. Also in Off-White with Tan, and every size from S to 3XL was in stock."),
 "6": ("Jones Sports Co", "Script Jones Golf Glove, Orange", "$30", U("jonessportsco.com","script-jones-golf-glove"),
   "A white leather glove with a hunter orange tab. The cheapest hunter orange in the post."),
 "7": ("Jones Sports Co", "Circa &rsquo;71 Headcover, Orange", "$55", U("jonessportsco.com","circa-71-headcover-orange"),
   "A knit-look headcover in safety orange for the driver or fairway wood, with the Jones label on the side. Easy to spot in a bag full of black."),
 "8": ("Palm Golf Co.", "Night Moves Orange Driver Headcover", "$89.99", U("palmgolfco.com","night-moves-orange-driver-headcover"),
   "A bright orange driver cover printed with palm trees. The loudest piece in this section, so let it be the only loud thing."),
 "9": ("Dicey Golf", "Dicey Country Club Hat", "$40", U("diceygolf.com","dicey-cc-hat"),
   "A blaze orange mesh trucker with &ldquo;Dicey Country Club&rdquo; across the front in black. The hat you can find in the woods."),
 "11": ("Eastside Golf", "Eastside Tee, Charcoal Grey", "$55", U("eastsidegolf.com","char-charcoal-grey-eastside-tee"),
   "A heavyweight charcoal tee with the Eastside Golf arch on the chest. The quiet base under an orange hat or vest."),
 "46": ("Palm Golf Co.", "Lager Beanie, Charcoal", "$34.99", U("palmgolfco.com","lager-beanie-1"),
   "A charcoal pom beanie with a small Palm patch. Wear it with an orange headcover on the bag and nothing else bright."),
 # Chocolate + Cream
 "12": ("Jones Sports Co", "Fleece Vest, Timber Brown/Jet Black", "$178", U("jonessportsco.com","fleece-vest-timber-brown-jet-black"),
   "A pile fleece vest in timber brown with black trim, from Jones&rsquo;s Forresters Outerwear line. Over a cream polo, it is the look of the season."),
 "13": ("Parmore", "Ripstop Cotton 5 Panel, Brown", "$55", U("parmoregolf.com","parmore-ripstop-cotton-5-panel-copy"),
   "A chocolate brown five-panel cap in ripstop cotton with the Parmore wordmark in cream. The pairing on one hat."),
 "14": ("Devereux", "El Classico Pant, Brown", "$88", U("devereuxgolf.com","el-classico-pant-brown"),
   "Brown golf trousers with a clean front and a little stretch. Brown pants are the easiest way to look like you know what is happening this fall."),
 "15": ("Sugarloaf Social Club", "SSC Work Jacket, Brown", "$165", U("sugarloafsocialclub.com","ssc-work-jacket"),
   "A brown work jacket with a corduroy collar. Also in Slate."),
 "16": ("Masterpiece Sports Club", "Semi-Private Performance Polo, Cream", "$118", U("masterpiecegolf.com","pique-poly-golf-polo-ss-cream"),
   "A cream performance polo with a small crest on the chest. The cream half of the pairing; wear it with the brown pants above."),
 # Racing Green + Butter
 "18": ("Quiet Golf", "Mesa Cashmere Sweater, Pine", "$348", U("quietgolf.com","mesa-cashmere-sweater"),
   "A pine green cashmere sweater with thin cream stripes. The best version of racing green here, and the most expensive."),
 "19": ("Bad Birdie", "Performance Mock Neck, Deep Forest", "$68", U("badbirdiegolf.com","performance-mock-neck-deep-forest"),
   "A deep forest mock neck for the range on a cold day. The easy entry into dark green."),
 "20": ("Grind City Golf", "The Unofficial Cardigan, Pine Green", "$103", U("grindcitygolf.com","the-unofficial-cardigan-copy"),
   "A pine green cardigan with a crest on the chest, made in Memphis. Buttoned over a polo, it looks like an old club sweater."),
 "22": ("Sugarloaf Social Club", "SSC Tech Vest, Hidden Gem Yellow", "$115", U("sugarloafsocialclub.com","tech-vest-2026"),
   "The yellow half of the pairing, and the brightest piece in the post. It also comes in Teal, Dark Red, Stone, White and Navy."),
 "23": ("Winslow", "Washed Yellow Cap", "$60", U("winslowla.com","washed-yellow-cap"),
   "A washed butter yellow cap with an embroidered W. The softer yellow, and the one that goes with a green sweater."),
 # Burgundy + Stone
 "24": ("Quiet Golf", "Montecito Cashmere Hoodie, Wine", "$348", U("quietgolf.com","montecito-cashmere-hoodie-wine"),
   "A cashmere hoodie in wine. Clubhouse burgundy, not loud burgundy."),
 "25": ("Grind City Golf", "Sphere Study Crew Knit, Burgundy", "$100", U("grindcitygolf.com","sphere-study-crew-knit"),
   "A burgundy crew knit with a big cream golf ball on the chest. Burgundy and stone, both on the sweater."),
 "26": ("52 Sundays", "Fairway Hat, Burgundy", "$35", U("52sundays.co","fairway-hat-burgundy"),
   "A clean burgundy cap with a script F. The cheapest burgundy here."),
 "27": ("Students Golf", "Future S/S Jersey Polo, Maroon", "$92", U("studentsgolf.com","future-s-s-jersey-polo-shirt-4"),
   "A maroon jersey polo with a relaxed fit. Put it with stone trousers."),
 "28": ("Old Faithful Golf", "The Diamond TRUSTY Leather Driver Headcover", "$90", U("oldfaithfulgolf.com","the-diamond-trusty-driver-golf-headcover-in-genuine-leather"),
   "A quilted leather driver cover in wine red with a stitched 1. Also in black."),
 "29": ("Devereux", "Scorpion Icon Polo, Stone", "$74", U("devereuxgolf.com","scorpion-icon-polo-stone"),
   "The stone half: a pale polo with a small scorpion on the chest. Wear it under any burgundy layer above."),
 # Olive + Tan
 "30": ("Aberdeen West", "CORDURA Track Jacket, Olive", "$235", U("aberdeenwest.com","cordura-track-jacket-copy"),
   "An olive half-zip track jacket in tough CORDURA nylon with Aberdeen West across the back."),
 "31": ("Students Golf", "Riverview Knit LS Polo Sweater, Moss", "$158", U("studentsgolf.com","riverview-knit-ls-polo-sweater"),
   "A moss green knit polo with long sleeves. The softest olive here."),
 "32": ("Parmore", "Stripe Polo, Olive and Cream", "$80", U("parmoregolf.com","green-stripes-polo-rebrand"),
   "An olive and cream striped polo with a solid collar. Pair it with tan trousers."),
 "33": ("Jones Sports Co", "Utility Beanie, Olive Night", "$36", U("jonessportsco.com","utility-beanie-olive-night"),
   "A dark olive watch-cap beanie with a leather patch. For the cart path in November."),
 "34": ("Dimple &amp; Divot", "D&amp;D Icon Dad Hat, Olive", "$35", U("dimpledivot.com","d-d-icon-dad-hat-olive"),
   "A washed olive dad hat with an orange label on the side, shot in the brand&rsquo;s In the Woods collection."),
 "35": ("Winston Collection", "Drawstring Player&rsquo;s Pouch, Tan", "$99.99", U("winstoncollection.com","drawstring-players-pouch-in-torino-leather-copy"),
   "The tan half: a quilted leather pouch for tees, balls and keys. Also in Forest Green, Black, Bone and Gray."),
 # Navy + Heather Gray
 "37": ("Grind City Golf", "The Switch Sweat, Navy Blue", "$69", U("grindcitygolf.com","unisex-boxy-collared-detachable-sweatshirt-1"),
   "A boxy navy sweatshirt with a detachable collar, so it works as a polo or a crew."),
 "38": ("Bad Birdie", "Ringers Rule Core Polo, Dark Navy", "$88", U("badbirdiegolf.com","core-polo-ringers-rule-dark-navy"),
   "A navy performance polo with a small all-over print. The busiest piece here, and still easy to wear."),
 "39": ("Sugarloaf Social Club", "Classic Quarter-Zip, Heather Grey", "$110", U("sugarloafsocialclub.com","classic-quarter-zip"),
   "The heather gray half: a classic quarter-zip with a pink zip pull inside. Also in Heather Navy."),
 "40": ("Eastside Golf", "Core Fleece Hoodie, Heather Grey", "$145", U("eastsidegolf.com","ec2070201-039-heather-grey-core-fleece-hoodie"),
   "A heather gray fleece hoodie with the Eastside Golf swingman on the chest."),
 "43": ("Devereux", "Back9 Checker Polo, Black/Tobacco", "$78", U("devereuxgolf.com","back9-checker-polo-black-tobacco"),
   "A long sleeve polo in a black and tobacco checkerboard. Camel and charcoal in one shirt."),
 "44": ("Vessel", "Sun Day Red x Vessel Icon Leather Driver Headcover, Camel", "$200", U("vesselgolf.com","sun-day-red-x-vessel-icon-leather-driver-headcover-camel"),
   "A camel leather driver cover from Vessel&rsquo;s collaboration with Sun Day Red. Also on the fairway wood for $150."),
 "wallet": ("ITL Golf", "Player&rsquo;s Wallet, Cognac", "$170", "https://itlgolf.com/products/itl-leather-glove-wallet",
   "A cognac leather zip case for a glove, tees, a marker and a pencil. From our <a href=\"/drops/itl-golf-masterpiece-sports-club-52-sundays\">Feel, Look, Habit</a> post."),
 "45": ("Rookline", "Grid Fleece Pant, Charcoal", "$295", U("rookline.com","grid-fleece-pant-charcoal"),
   "The charcoal half: a grid fleece trouser that is warm enough for a frosty tee time and smart enough for the clubhouse."),
}
P.update({
 "n5": ("Rookline", "Signature Blend Polo, Charcoal Heather", "$165", U("rookline.com","signature-blend-cotton-cashmere-polo-charcoal-heather"),
   "A cotton-cashmere polo in charcoal heather from New York&rsquo;s Rookline. The grown-up base for an orange accent."),
 "n6": ("Palm Golf Co.", "OC Towel, Orange", "$19.99", U("palmgolfco.com","oc-towel"),
   "An orange printed golf towel. The cheapest way to put hunter orange on the bag."),
 "n7": ("Dimple &amp; Divot", "Hickory Golf Brush Lite, Orange", "$45", U("dimpledivot.com","hickory-golf-brush-mini-woods"),
   "A hickory wood groove brush with an orange cord. A small dose of orange that clips to the bag."),
 "n8": ("Kingfisher Golf", "Cream Polo", "$45", U("kingfisher-golf.com","cream-polo"),
   "A cream polo with blue trim from Dallas&rsquo;s Kingfisher. Wear it with brown trousers."),
 "n9": ("Local Rule", "Pleated Trousers, Off-White", "1,499 kr (~$150)", U("local-rule.com","pleated-trousers-off-white"),
   "Off-white pleated trousers that turn a brown sweater or vest into an outfit."),
 "w4": ("Walker Golf Things", "Flecked Quarter Zip, Espresso", "$55", "https://www.walkergolfthings.com/en-us/products/flecked-quarter-zip",
   "A flecked knit quarter-zip in espresso brown from the Gold Coast brand. Over a cream polo, it is the whole look."),
 "m1": ("Manors", "Ranger Golf Jacket, Pine Green", "$189", "https://manorsgolf.com/products/track-jacket",
   "A pine green golf jacket from London&rsquo;s Manors with a stand collar and a stripe down the sleeve."),
 "n10": ("Local Rule", "Cotton Cap, Green", "499 kr (~$50)", U("local-rule.com","lr-cotton-cap-green"),
   "A dark green cotton cap with a small serif logo. Simple, and it goes with everything in this section."),
 "n11": ("Penta Golf", "Penta x Barnaby&rsquo;s Grid Polo, Lemon Sorbet", "$99", U("penta-golf.com","penta-x-barnabys-grid-polo-lemon-sorbet"),
   "A pale lemon grid polo from Penta&rsquo;s collaboration with Barnaby&rsquo;s. The butter half of the pairing."),
 "w1": ("Walker Golf Things", "Kooka Knit Polo, Pine / Cream", "$93", "https://www.walkergolfthings.com/en-us/products/kooka-knit-polo-1",
   "A pine green knit polo with a cream collar and Walker&rsquo;s kookaburra on the chest."),
 "m2": ("Manors", "GOAT Pique Polo, Burgundy", "$115", "https://manorsgolf.com/products/goat-pique-polo-stripe",
   "A striped pique polo in burgundy. Wear it with stone trousers."),
 "w2": ("Walker Golf Things", "Members Polo, Maroon", "$86", "https://www.walkergolfthings.com/en-us/products/members-polo-4",
   "A maroon polo with a contrast collar, shot on course by the brand."),
 "n12": ("Devereux", "Golden State Country Club Hat, Stone", "$38", U("devereuxgolf.com","golden-state-country-club-hat-stone-1"),
   "A stone cap with a red patch. The stone half of the pairing, on your head."),
 "n13": ("Kingfisher Golf", "Olive Patterned Polo", "$65", U("kingfisher-golf.com","olive-patterned-polo"),
   "An olive polo with a small all-over pattern. Pair it with tan trousers."),
 "m3": ("Manors", "Crewneck Polartec Fleece, Dark Olive", "$175", "https://manorsgolf.com/products/crewneck-polartec%C2%AE-fleece",
   "A dark olive Polartec fleece crewneck for cold mornings, from Manors&rsquo; winter line."),
 "n14": ("Local Rule", "Lightweight Tech Pants, Dusty Olive", "1,299 kr (~$130)", U("local-rule.com","lightweight-tech-pants-new-dusty-olive"),
   "Dusty olive tech trousers. Olive below, tan above, and you are done."),
 "m4": ("Manors", "Stableford Trousers, Vintage Indigo", "$188", "https://manorsgolf.com/products/work-trousers",
   "Workwear-style golf trousers in a faded vintage indigo. The navy half from the waist down."),
 "n15": ("Rookline", "Cashmere Watch Cap, Grey Heather", "$75", U("rookline.com","cashmere-watch-cap-grey-heather"),
   "A heather gray cashmere watch cap. The softest thing in this post."),
 "n16": ("Kingfisher Golf", "Navy Everyman Polo", "$65", U("kingfisher-golf.com","navy-everyman-polo"),
   "A navy polo cut plain, from Dallas&rsquo;s Kingfisher."),
 "n17": ("Penta Golf", "Footwork Tee, Navy", "$54", U("penta-golf.com","footwork-tee-navy"),
   "A navy tee with a graphic on the back. For the range under a gray quarter-zip."),
 "n18": ("Rookline", "Brushed Twill Pivot Pant, Navy Blazer", "$175", U("rookline.com","brushed-twill-pivot-pant-navy-blazer"),
   "Brushed twill golf trousers in navy. Wear them with anything heather gray."),
 "m5": ("Manors", "Merino Tech Crewneck, Dune", "$242", "https://manorsgolf.com/products/merino-wool-crewneck",
   "A merino crewneck in Dune, a warm camel. Over charcoal trousers, it is the timeless look."),
 "n19": ("Rookline", "Grid Fleece Windbreaker, Charcoal", "$355", U("rookline.com","grid-fleece-windbreaker-charcoal"),
   "A charcoal grid fleece windbreaker that matches Rookline&rsquo;s Grid Fleece Pant."),
 "n20": ("Devereux", "Goodnight Jacket, Tan", "$98", U("devereuxgolf.com","goodnight-jacket-tan"),
   "A tan work-style jacket with chest pockets. Camel on top, charcoal below."),
 "w3": ("Walker Golf Things", "Members Pant, Tan", "$110", "https://www.walkergolfthings.com/en-us/products/members-pant-1",
   "Tan golf trousers from Walker&rsquo;s Members line. The lighter way to wear camel."),
 "n21": ("Devereux", "Checkered Shoe Bag, Tan", "$88", U("devereuxgolf.com","checkered-shoe-bag-tan"),
   "A tan checkered leather shoe bag. Camel for the trunk of the car."),
})
PAIRS = {
 "sage": ("Sage", "#9CAF88", "Ecru", "#EDE4D0"),
 "orange": ("Hunter Orange", "#FF6A13", "Charcoal", "#3A3D40"),
 "chocolate": ("Chocolate", "#4A2F22", "Cream", "#EFE6D2"),
 "green": ("Racing Green", "#1F4D3A", "Butter", "#F2DC8F"),
 "burgundy": ("Burgundy", "#6B1F2A", "Stone", "#D9CFBD"),
 "olive": ("Olive", "#5C5F3A", "Tan", "#C8A97E"),
 "navy": ("Navy", "#1C2A44", "Heather Gray", "#A7A9AC"),
 "camel": ("Camel", "#C19A6B", "Charcoal", "#36383B"),
}
SECTIONS = [
 ("Sage + Ecru", "sage", ["s1","s3","s2","s6","s5","s7","s4","s9","s8"],
  "<strong>On trend</strong>The light color of the season, and the one we kept seeing in new drops across our brand index. Sage is calmer than mint and warmer than gray, so it sits well against fall grass and a low sun. Wear it on top or below, put ecru or bone next to it, and keep everything else quiet. The Kingfisher cap does the whole pairing on one hat."),
 ("Hunter Orange + Charcoal", "orange", ["9","6","7","8","n6","n7","n5","11","46"],
  "<strong>On trend</strong>The safety-vest orange from the hunting world. It is the loudest color in the post, so keep it to one piece: a hat, a glove, a headcover or a towel on the bag. Charcoal is the right partner because it is darker than gray and softer than black, which lets the orange do the talking without looking like a costume."),
 ("Chocolate + Cream", "chocolate", ["12","w4","14","13","15","16","n8","n9","t1"],
  "<strong>On trend</strong>Brown is the color of the season, and it is replacing navy as the base for everything else. A brown vest, quarter-zip or pair of trousers looks warmer and more relaxed than the navy you would usually reach for. Cream keeps it from looking heavy; a cream polo under a brown layer is the simplest outfit in this post."),
 ("Racing Green + Butter", "green", ["18","m1","20","w1","19","n10","22","n11","23"],
  "<strong>On trend</strong>Deep green with a soft yellow accent. Racing green is the most traditional color on this list, close to the old club sweaters your grandfather wore, and it looks right on a golf course in any season. The green does the work; the yellow is a cap, a vest or a polo, kept pale so it reads as butter, not highlighter."),
 ("Burgundy + Stone", "burgundy", ["24","m2","25","w2","27","28","26","29","n12"],
  "<strong>On trend</strong>Deep red against a pale neutral. Burgundy reads clubhouse, not loud, and it hides a long day better than a bright red. Wear it as the polo or the sweater and keep the trousers and cap in stone, or flip it and put the burgundy on your head and your driver."),
 ("Olive + Tan", "olive", ["30","m3","31","n13","32","n14","33","34","35"],
  "<strong>On trend</strong>Two earth colors that sit together without trying, and the easiest pairing here to wear. Olive works as a fleece, a polo or a pair of trousers, and tan softens it. If you only buy one new pairing this fall and you already own khakis, this is it."),
 ("Navy + Heather Gray", "navy", ["m4","39","n16","38","37","40","n18","n17","n15"],
  "<strong>Timeless</strong>The default fall golf outfit, and it is the default for a reason. Navy is dark enough to look sharp and heather gray is soft enough to look relaxed, and together they work at a muni, a private club or a dinner after the round. Navy on top, heather gray underneath, or the other way around."),
 ("Camel + Charcoal", "camel", ["m5","43","n20","n19","45","w3","44","n21","wallet"],
  "<strong>Timeless</strong>A camel layer over charcoal looks expensive at any price. It is the pairing from old cold-weather tailoring, a camel coat over gray flannel, moved onto the course. Camel works as a jacket, a knit or leather on the bag; charcoal is the trousers or the fleece underneath."),
]
N = 72
BANDS = {
 "chocolate": ("In the field", "Hunter orange, olive and a beanie for the cold, from Jones Sports Co and Dimple &amp; Divot.",
   [("band-1-1","Jones Sports Co Circa '71 orange headcovers on clubs in a bag","Jones Sports Co"),
    ("band-1-2","A golfer in a Jones Sports Co olive Utility Beanie","Jones Sports Co"),
    ("band-1-3","A Dimple & Divot olive dad hat with an orange label","Dimple &amp; Divot")]),
 "navy": ("Into the cold", "Olive, navy and checkerboard, from Manors, Kingfisher and Devereux.",
   [("band-2-1","A golfer in a Manors dark olive Polartec fleece on the course","Manors"),
    ("band-2-2","A man in a Kingfisher navy polo","Kingfisher Golf"),
    ("band-2-3","A golfer in a Devereux black and tobacco checker polo","Devereux")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Fall is the best season to dress for golf. It is cold enough for layers, the light is low and warm, and the colors that look wrong in July suddenly look right. We picked eight pairings: six that are on trend for fall 2026 and two that have worked for fifty years.</p>
    <p><strong>What is on trend.</strong> The fall and winter 2026 runway and retail coverage keeps landing on earthy browns and olives, with a few strong accents: a deep racing green, burgundy, a soft butter yellow. Across the 200-plus brands in our index, the softer color we kept seeing in fall drops was sage, usually next to ecru or bone. Golf&rsquo;s loud one is hunter orange, borrowed from the hunting world and showing up on everything from headcovers to blaze orange trucker hats.</p>
    <p><strong>How to wear a pairing.</strong> Pick the main color for the biggest piece, a jacket, a sweater or trousers, and use the second color for one or two smaller things: a cap, a glove, a headcover. With hunter orange, one piece is plenty.</p>
    <p><strong>Light against dark.</strong> Every pairing here is one darker color and one lighter one: racing green and butter, burgundy and stone, navy and heather gray. That contrast is what makes two colors look planned instead of random. If both pieces are dark, the outfit goes flat; if both are light, it washes out on a gray November morning.</p>
    <p><strong>Where the money goes.</strong> Spend on the big piece you will wear every round, a jacket, a sweater or a pair of trousers, and save on the accent. Most of the second colors in this post come in caps, gloves and towels under $60, so you can try a new pairing for the price of a range bucket and a beer before you buy the sweater.</p>
    <p><strong>Start with what you own.</strong> You probably already have navy, gray and something khaki. Pick the pairing closest to your closet, add one new piece in the second color, and wear it for a month. Chocolate and cream and camel and charcoal work with almost any golf trousers you have now; sage and hunter orange are the ones to add if you want something that feels new this year.</p>
    <p><strong>What is in here.</strong> Nine pieces per pairing, 72 in all, from @@NB@@ independent brands. Every piece was in stock in the color shown when we checked on November 2, 2026, and every price is in US dollars.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pairings</span><span>8</span></div>
      <div class="sidebar-detail"><span class="l">On trend</span><span>6</span></div>
      <div class="sidebar-detail"><span class="l">Timeless</span><span>2</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>72</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$19.99&ndash;$398</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Kingfisher Sage Green DAL Cap</span></div>
      <div class="hashtags">
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#Colorways</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Two Colors Are Enough</h2>
    <p>The easiest way to look put together on the course is to stop at two colors. Pick a pairing, buy the big piece in the main color, and let a cap or a headcover carry the second one. Sage and hunter orange are the new ones this year; navy and gray will still be right when they are gone.</p>
    <p>For more color ideas, see our <a href="/drops/golf-color-combos-mix-and-match">seven color combos to mix and match</a>.</p>
  </div>
</section>
"""
HERO_ALT = "Three photos side by side: a man in a Devereux bone waffle hoodie, a golfer in a Jones timber brown fleece vest by the water, and a golfer in a Walker maroon polo on the course"
FRN = json.loads((ROOT / "research/fall-colorways/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-CC-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
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
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-02", "dateModified": "2026-11-02",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
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


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' + swatch(anchor) +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for s in SECTIONS: assert len(s[2]) == 9, s[0]
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Eight pairings, hex codes included</span><span class="dot"></span>
    <span>72 picks &middot; in stock, checked November 2, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Criquet", "Malbon", "Royal Blue", "Plum", "Cherry"):
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
