#!/usr/bin/env python3
"""build-color-combos.py — "Seven Golf Color Combos to Mix and Match" 13 October 2026.
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

TITLE = "7 Golf Color Combos to Mix and Match: Clothes, Headcovers, Grips"
DESC = ("Seven two-color pairings, from Royal Blue and Chalk to Forest and Leaf, each built from 7+ pieces you can buy now: "
        "polos, headcovers, grips, hats and towels. Plus a lookbook gallery.")
H1 = "Seven Golf Color Combos to Mix and Match, from Royal Blue + Chalk to Forest + Leaf"
BC = "Golf Color Combos"
SLUG = "golf-color-combos-mix-and-match"
IMG = "/images/color-combos"
SHOP = ""
C = "Colorway in the pairing: "
P = {
 # Royal Blue + Chalk
 "lof": ("Left of Field Golf", "Sorrento Polo, Royal Blue", "A$150 &middot; US $110", "https://lofgolf.com/en-us/products/sorento-polo-royal-blue",
   "The brand&rsquo;s own lookbook puts the whole pairing on one person: a royal blue polo over off-white trousers. Start here and build out. Every size from S to XXL was in stock."),
 "slice": ("SLICE TOWN", "Golf Track Jacket, Cobalt", "1,750 kr &middot; US $190", "https://slice-town.com/products/track-jacket-cobalt",
   "SLICE TOWN cuts this track jacket in nylon with a full zip and a high collar, an ST. print on the chest and a golf ball on the back. The loud half of the combo; put chalk-colored trousers under it and let it do the work. M, L and XL in stock."),
 "cwporcelain": ("Cloud &amp; Wind Golf", "The Blossom: Porcelain", "$18", "https://www.cloudandwindgolf.com/products/p/2tnb4kjsjbcmduukev9p569k309okz-26t8d",
   "Cloud &amp; Wind paints blue blossoms on a white grip, so it looks like old china. It is this pairing turned upside down: mostly chalk, a little royal blue, on every club in the bag." + " More in <a href=\"/drops/niche-grip-report-vol-2\">Niche Grip Report Vol. 2</a>."),
 "cadblue": ("Cadero", "2x2 Pentagon, White x Blue", "&euro;21.90 (~$25)", "https://cadero.shop/products/2x2-pentagon",
   "CADERO runs down this white pentagon-profile grip in bright blue. The round White x Blue was in stock; the ribbed version was not."),
 "iomicblue": ("IOMIC", "Sticky 2.3, Blue", "$14.50", "https://iomicusa.com/products/sticky-2-3",
   "IOMIC makes this solid blue grip for the player who wants the color without the pattern. The cheapest piece in this section, and singles were in stock."),
 "jonesglove": ("Jones Sports Co.", "Flying J Golf Glove, Cobalt Blue", "$30", "https://www.jonessportsco.com/products/flying-j-golf-glove-cobalt-blue",
   "Jones puts a cobalt Flying J on the back of an off-white glove: chalk with a royal blue accent, which is exactly the ratio this pairing wants. Men&rsquo;s left hand, S to XL in stock."),
 "tarraing": ("Tarraing Golf", "Gray, White and Blue Highland Cow Hat", "$40", "https://tarrainggolf.com/products/red-white-blue-highland-cow-copy",
   "Tarraing puts a royal blue Highland cow on the front of a pale gray cap. The store marked it low inventory when we checked."),
 # Red Wine + Light Sand
 "latenine": ("Late Nine", "Cable Knit Polo, Burgundy", "2,950 SEK &middot; US $388", "https://late-nine.com/products/cable-knit-polo-burgundy",
   "Late Nine cable-knits this long-sleeved polo in deep burgundy merino. Wear it over sand-colored trousers and you have the pairing at its most expensive. S and M in stock." + " More in <a href=\"/drops/golf-brands-clothes-they-wanted-to-wear\">The Clothes They Wanted to Wear</a>."),
 "walkerpolo": ("Walker Golf Things", "Members Polo, Maroon", "A$120 &middot; US $100", "https://www.walkergolfthings.com/en-us/products/members-polo-3",
   "Walker tips this maroon polo in cream on the collar and sleeves, so the second color is already built in. M to XXL in stock."),
 "nodirtburg": ("No Dirt Golf", "Ultimate Caddy Towel, Burgundy + Silver Stripes", "$29.99", "https://nodirtgolf.com/products/the-ultimate-caddy-towel-burgundry-silver-stripes",
   "No Dirt makes this caddy towel in burgundy with pale stripes at the ends. The easiest way to put red wine on the bag without changing anything else."),
 "hiroki": ("Hiroki Golf", "Oriental Stand Bag, Maroon Red", "NZ$550 &middot; US $350", "https://hirokigolf.com/products/hiroki-oriental-stand-bag-red",
   "Hiroki weaves a pattern through the body of this deep maroon stand bag. It is the biggest single block of color on the page, so keep everything else light sand."),
 "hypegolf": ("RIPIT Grips", "RIPIT x HYPEGOLF, Merlot", "US $18.50", "https://ripitgrips.com/products/hypegolf-x-ripit-grips",
   "RIPIT runs pale pinstripes down a merlot cord-and-rubber grip and tops it with a RIPIT x HYPEGOLF cap. Merlot and Moss were in stock; Hype Black was sold out."),
 "wgshort": ("Woodgrain Golf", "Double Pleated Short, Tan", "$130", "https://woodgrain.golf/products/the-double-pleated-short-tan",
   "Warm days get the light sand half as a tan short with two pleats a side. Every size from XS to 2XL in stock." + " More in <a href=\"/drops/brand-to-know-woodgrain-golf\">our Woodgrain Brand to Know</a>."),
 "wgtan": ("Woodgrain Golf", "Legacy Double Pleated Trouser, Tan", "$180", "https://woodgrain.golf/products/relaxed-double-pleated-trouser-tan",
   "Woodgrain makes the same color full length, as a wide tan trouser with deep double pleats. Put the Late Nine knit or the Walker polo on top. Only M and L left."),
 # Orange + Linen
 "jonescirca": ("Jones Sports Co.", "Circa &rsquo;71 Headcover, Orange", "$55", "https://www.jonessportsco.com/products/circa-71-headcover-orange",
   "Jones makes this bright orange headcover with a woven label. Driver $55, fairway $45, or both for $90, all in stock. Pair it with a cream or white cover on the next club."),
 "palm": ("Palm Golf Co.", "Night Moves Orange Driver Headcover", "$89.99", "https://palmgolfco.com/products/night-moves-orange-driver-headcover",
   "Black palm trees cover an orange headcover, made to order in seven to ten business days. The loudest orange here."),
 "mogshade": ("Mogshade", "Tiles Olive &amp; Orange Headcover", "&euro;78 &middot; US $115", "https://www.mogshadegolf.com/products/tile-olive-orange-headcover",
   "Mogshade weaves a geometric tile pattern in burnt orange and olive brown. The quiet way to do orange. Driver only; the wood and hybrid covers were sold out."),
 "devereux": ("Devereux Golf", "High Noon Polo, Clay", "$74", "https://devereuxgolf.com/products/high-noon-polo-clay",
   "Devereux gives this clay-orange polo a black collar and a small all-over print. Wear it with linen-colored shorts and white shoes. S to XL in stock."),
 "iomicorange": ("IOMIC", "Sticky 1.8, Orange/Blue", "$14.50", "https://iomicusa.com/products/sticky-1-8",
   "IOMIC makes this undersize grip in solid orange with a thin blue cap. One grip, in the putter or a wedge, is enough."),
 "flowerclay": ("RIPIT Grips", "Flower of Life, Clay and Cream", "US $18.50", "https://ripitgrips.com/products/flower-of-life",
   "Cream cord sits on top and clay rubber below, split on a diagonal. It is the whole pairing on one grip. Standard+, undersize and jumbo all in stock."),
 "seamuscopper": ("Seamus Golf", "Hand Forged &ldquo;Mark It 8&rdquo; Marker, Copper", "$36", "https://www.seamusgolf.com/products/hand-forged-mark-it-8-dude-copper",
   "Seamus hand-forges this copper ball marker and stamps it. Copper is orange that has been in your pocket for a few seasons."),
 "ashworth": ("Ashworth Golf", "The O.G. Polo", "$98", "https://www.ashworth-golf.com/products/the-o-g-polo-white-denim",
   "Ashworth has the linen half covered: a white cotton polo with thin tipping. Under an orange headcover or next to a clay grip it does the job off-white is for. M to XL in stock." + " More in <a href=\"/drops/brand-to-know-ashworth\">our Ashworth Brand to Know</a>."),
 # Plum + Cream
 "eastside": ("Eastside Golf", "Tip Pique Polo, Wild Grape", "$78", "https://eastsidegolf.com/products/ec2041101-517-wild-grape-tip-pique-polo",
   "Eastside trims a purple pique polo with white tipping and puts its golfer logo on the chest. The brightest plum here; every size from S to 3XL in stock."),
 "cwmoonshade": ("Cloud &amp; Wind Golf", "The Blossom: Moonshade", "$18", "https://www.cloudandwindgolf.com/products/p/blossom-zrs7n",
   "Purple blossoms cover a purple grip and turn darker at the branches. A plum grip goes with more than you would expect."),
 "fyfe09": ("Fyfe Golf", "Second Round Remake 09", "&pound;69 (~$91)", "https://www.fyfegolf.com/products/second-round-remake-09-headcover",
   "Fyfe cut this cover from a vintage Sunderland golf jacket in a blue and purple print, and only two drivers and two fairways were made. Driver &pound;69, fairway &pound;65, both in stock when we checked." + " More in <a href=\"/drops/fyfe-golf-second-round-headcovers-from-vintage-golf-jackets\">our Fyfe Second Round post</a>."),
 "kraken": ("Kraken Golf", "Transfusion Satin Purple Crayon Divot Tool", "$79", "https://www.krakengolf.com/products/transfusion-satin-purple-crayon-divot-tool",
   "Kraken makes this divot tool look like a purple crayon, label and all. Plum for your pocket."),
 "swag": ("SWAG Golf", "Tito&rsquo;s Splash of Grape Ball Marker", "$66.66", "https://swag.golf/products/titos-splash-of-grape-ball-marker",
   "SWAG puts a grape-colored drink, lime included, on a ball marker. Final sale."),
 "apres": ("Apr&egrave;s Golf", "@HallyLead x Apr&egrave;s-Golf Grapeness Wins", "$98", "https://apresgolf.com/products/hallylead-x-apres-golf-grapeness-wins-sherpa-fleece-headcover",
   "These purple sherpa fleece headcovers were designed by Hally Leadbetter and hand-sewn in California. The driver cover costs $98, the fairway and hybrid $88 and the putters $108; an alignment stick cover is $38."),
 "iomiclav": ("IOMIC", "Sticky 1.8, Lavender/White", "$14.50", "https://iomicusa.com/products/sticky-1-8",
   "IOMIC covers the soft end of plum with a lavender undersize grip and a white cap. In stock as a single."),
 "oddritual": ("Odd Ritual Golf", "1990s Heritage Polo", "R 950 (~$52)", "https://oddritualgolf.com/products/1990s-heritage-polo",
   "Odd Ritual has the cream half, a pique polo with a dark contrast collar and cuffs, cut oversized. Under a plum headcover or next to a purple grip it is the off-white you need. L, XL and 2XL left." + " More in <a href=\"/drops/brand-to-know-odd-ritual\">our Odd Ritual Brand to Know</a>."),
 # Midnight Indigo + Vanilla
 "criquet": ("Criquet", "Throwback Players Shirt, Navy", "$104", "https://criquetshirts.com/products/throwback-players-shirt-navy",
   "Criquet cuts this players shirt in navy pima cotton with pale contrast piping. S, M and L in stock." + " More in <a href=\"/drops/brand-to-know-criquet\">our Criquet Brand to Know</a>."),
 "seamusnavy": ("Seamus Golf", "Navy Harris Tweed Blade Putter Cover", "$130", "https://www.seamusgolf.com/products/navy-harris-tweed-magnet-putter-cover",
   "Seamus cuts navy herringbone Harris Tweed and finishes it with a pale trim and a magnetic closure. Midnight indigo in wool."),
 "jancraig": ("Jan Craig Headcovers", "Driver Headcover, Navy &amp; White", "$79", "https://www.jancraigheadcovers.com/driver-460-headcover-8-in-pom-1-stripe-navy-white/",
   "Jan Craig hand-knits this navy wool cover with a white stripe and a big navy and white pom. The pairing in its oldest form."),
 "fella": ("Fella Golf", "Boris Quarter-Zip Sweater", "&euro;150 (~$168)", "https://fellagolf.com/products/boris-quarter-zip-sweater-navy",
   "Fella runs one wide navy stripe across the chest of a cream sweater. Vanilla first, indigo second. S, M and XL in stock."),
 "walkerhedge": ("Walker Golf Things", "Hedge Mid Cap, Navy", "A$60 &middot; US $50", "https://www.walkergolfthings.com/en-us/products/hedge-mid-cap",
   "Walker stitches its script in a contrast thread on a navy cap. One size, in stock."),
 "lofduck": ("Left of Field Golf", "Duckbill Birds Cap, Navy/Cream", "A$69 &middot; US $50", "https://lofgolf.com/en-us/products/duckbill-birds-cap-navy-cream",
   "Left of Field splits the pairing across one hat, with a navy crown and a cream brim. One size, in stock."),
 "wgcream": ("Woodgrain Golf", "Legacy Double Pleated Trouser, Cream", "$180", "https://woodgrain.golf/products/relaxed-double-pleated-trouser",
   "Woodgrain&rsquo;s lookbook shows the vanilla half under a navy polo: a wide cream cotton trouser with deep double pleats. Only M and L left."),
 # Cherry + Alabaster
 "cwpalace": ("Cloud &amp; Wind Golf", "The Blossom: Palace Wall", "$18", "https://www.cloudandwindgolf.com/products/p/2tnb4kjsjbcmduukev9p569k309okz",
   "Pale blossoms run up a deep red grip. The red half and the light half on every club."),
 "students": ("Students Golf", "Society 5-Panel Wool Hat, Red", "$52", "https://studentsgolf.com/products/society-structured-5-panel-acrylic-wool-hat",
   "Students puts a white Old English S on a deep red five-panel. One size, in stock."),
 "lofplaid": ("Left of Field Golf", "Heritage Plaid Cap, Red", "US $50", "https://lofgolf.com/en-us/products/heritage-plaid-cap-red",
   "Left of Field puts a cream script on the front of a red tartan cap. Cherry for the player who likes a pattern."),
 "localgc": ("Local GC", "Nantucket Red Canvas Headcover", "NZ$89 (~$51)", "https://www.localgc.co.nz/product/nantucket-red-canvas-head-cover",
   "Local GC makes this faded red canvas cover in a one-man workshop in New Zealand, made to order in seven to ten days. Driver, mini driver, wood and hybrid." + " More in <a href=\"/drops/brand-to-know-local-gc\">our Local GC Brand to Know</a>."),
 "parmorered": ("Parmore Golf", "Paneled Tee, Red", "&pound;45 &middot; US $70", "https://parmoregolf.com/products/red-paneled-tee-rebrand",
   "Parmore cuts this red cotton jersey tee with white side panels: cherry and alabaster cut into one shirt. S to XL in stock." + " More in <a href=\"/drops/brand-to-know-parmore-golf\">our Parmore Brand to Know</a>."),
 "sugarloaf": ("Sugarloaf Social Club", "&ldquo;Nantucket Red&rdquo; Needlepoint Bottle Opener", "$35", "https://sugarloafsocialclub.com/products/nantucket-red-needlepoint-bottle-opener",
   "Sugarloaf stitches this needlepoint bottle opener in red, pale pink and navy, for after the round."),
 "both": ("B.O.T.H.", "Berry Hills Cap, Red", "$80", "https://betonthehorses.co/products/berry-hills-cap-red",
   "This red trucker cap has BERRY HILLS across the front in white. The loudest red in this section."),
 # Forest + Leaf
 "lazywood": ("Lazyface", "The Wood Cover", "$118", "https://lazyface.com/products/the-wood-cover",
   "Lazyface puts a white LF on dark green leather and adds yellow and white stripes at the neck." + " More in <a href=\"/drops/brand-to-know-lazyface\">our Lazyface Brand to Know</a>."),
 "parmoregreen": ("Parmore Golf", "Varsity Quarter-Zip", "&pound;90 &middot; US $140", "https://parmoregolf.com/products/green-1-4-zip-rebrand",
   "Parmore makes this weatherproof pullover in forest green with striped cuffs and hem. S to XL in stock."),
 "cwmist": ("Cloud &amp; Wind Golf", "Mountain &amp; Mist", "$18", "https://www.cloudandwindgolf.com/products/p/wave-gygps",
   "This grip puts dark green and pale leaf green in a wave pattern. Forest + Leaf, exactly, on a grip."),
 "nodirtgreen": ("No Dirt Golf", "The Classic, Forest Green", "$25.99", "https://nodirtgolf.com/products/the-classic-forest-green",
   "No Dirt makes this green waffle towel at 16 by 39 inches. The brightest green in this section, closer to leaf than forest." + " More in <a href=\"/drops/brand-to-know-no-dirt-golf\">our No Dirt Brand to Know</a>."),
 "puttwell": ("Puttwell", "Wordmark L/S Tee, Deep Green", "$30", "https://puttwellgolfclub.com/products/puttwell-wordmark-l-s-tee",
   "Puttwell prints a small wordmark on a deep green long-sleeve tee, half price at $30 when we checked. S, M and L in stock."),
 "lazycap": ("Lazyface", "The Chenille Sun Cap", "$48", "https://lazyface.com/products/the-chenille-sun-cap",
   "Lazyface sews a chenille sun on the front of a soft green cap. The leaf half."),
 "cadgreen": ("Cadero", "2x2 Pentagon, White x Green", "&euro;21.90 (~$25)", "https://cadero.shop/products/2x2-pentagon",
   "CADERO runs down this white grip in bright leaf green. The round version was in stock."),
}
PAIRS = {
 "royal": ("Royal Blue", "#014BAA", "Chalk", "#F8F3F0"),
 "red-wine": ("Red Wine", "#7F011F", "Light Sand", "#F5EBD0"),
 "orange": ("Orange", "#EC5E27", "Linen", "#FDFDF1"),
 "plum": ("Plum", "#381932", "Cream", "#FFF3E6"),
 "indigo": ("Midnight Indigo", "#282B4A", "Vanilla", "#EEEBDA"),
 "cherry": ("Cherry", "#890149", "Alabaster", "#F3F3E7"),
 "forest": ("Forest", "#064734", "Leaf", "#E0FFC2"),
}
SECTIONS = [
 ("Royal Blue + Chalk", "royal", ["lof", "slice", "jonesglove", "tarraing", "cwporcelain", "cadblue", "iomicblue"],
  "The brightest pairing here, and the easiest to wear: one royal blue piece, everything else chalk. A blue polo with off-white trousers, or a white glove and grip with blue on them."),
 ("Red Wine + Light Sand", "red-wine", ["latenine", "walkerpolo", "wgtan", "wgshort", "hiroki", "nodirtburg", "hypegolf"],
  "The fall pairing. Burgundy on top, sand below, and the bag or towel picks up the red."),
 ("Orange + Linen", "orange", ["devereux", "ashworth", "jonescirca", "palm", "mogshade", "flowerclay", "iomicorange", "seamuscopper"],
  "Orange is loud, so let one piece carry it, a headcover or a polo, and keep the rest linen and off-white."),
 ("Plum + Cream", "plum", ["eastside", "oddritual", "fyfe09", "apres", "cwmoonshade", "iomiclav", "kraken", "swag"],
  "The pairing nobody else in your group will have. Plum headcovers and grips against a cream polo."),
 ("Midnight Indigo + Vanilla", "indigo", ["criquet", "fella", "wgcream", "lofduck", "walkerhedge", "jancraig", "seamusnavy"],
  "Navy and cream is the oldest pairing in golf. These are the pieces that make it look deliberate."),
 ("Cherry + Alabaster", "cherry", ["parmorered", "lofplaid", "students", "both", "localgc", "cwpalace", "sugarloaf"],
  "Cherry pairs a deep red with a soft off-white, and hats do most of the work here."),
 ("Forest + Leaf", "forest", ["parmoregreen", "puttwell", "lazycap", "lazywood", "cwmist", "nodirtgreen", "cadgreen"],
  "Green on a golf course should be obvious, but the trick is two greens: one dark, one pale."),
]
N = 51
LIFE = [  # (n, alt, caption)
 (1, "A model in Left of Field's royal blue Sorrento Polo and off-white trousers", "Left of Field &middot; Royal Blue + Chalk"),
 (2, "A model in SLICE TOWN's cobalt golf track jacket", "SLICE TOWN &middot; Royal Blue"),
 (3, "A golfer in Walker Golf Things' maroon Members Polo on a range", "Walker Golf Things &middot; Red Wine"),
 (4, "A model in Late Nine's burgundy cable knit polo and grey slacks", "Late Nine &middot; Red Wine"),
 (5, "A model in Woodgrain's tan double pleated shorts and a cream polo", "Woodgrain &middot; Light Sand"),
 (6, "A model in Woodgrain's tan Legacy trousers and a brown knit, leaning on a club", "Woodgrain &middot; Light Sand"),
 (7, "A hand holding a cream Woodgrain cap in a wood-paneled room", "Woodgrain &middot; Light Sand"),
 (8, "A close crop of Devereux's clay High Noon Polo", "Devereux &middot; Orange"),
 (9, "A golfer's hands on RIPIT's Clay and Cream Flower of Life grip", "RIPIT &middot; Orange + Linen"),
 (10, "A model in Odd Ritual's cream 1990s Heritage Polo and a cream cap", "Odd Ritual &middot; Cream"),
 (11, "A model in a navy polo and Woodgrain's cream Legacy trousers", "Woodgrain &middot; Midnight Indigo + Vanilla"),
 (12, "A model in Fella's cream Boris Quarter-Zip with a navy chest stripe", "Fella &middot; Vanilla + Midnight Indigo"),
 (13, "A model in Odd Ritual's navy Caddie Jacket and a white cap", "Odd Ritual &middot; Midnight Indigo"),
 (14, "A man in Criquet's navy Throwback Players Shirt and olive shorts", "Criquet &middot; Midnight Indigo"),
 (15, "A man in Walker's navy Hedge Mid Cap at a bar", "Walker Golf Things &middot; Midnight Indigo"),
 (16, "A model in Left of Field's navy and cream Duckbill Birds Cap", "Left of Field &middot; Midnight Indigo + Vanilla"),
 (17, "A golfer in a striped polo and Woodgrain's cream trousers at night", "Woodgrain &middot; Vanilla"),
 (18, "A golfer in Parmore's red Paneled Tee teeing up a ball", "Parmore &middot; Cherry + Alabaster"),
 (19, "A model in Left of Field's red Heritage Plaid Cap", "Left of Field &middot; Cherry"),
 (20, "A golfer gripping a club fitted with Cloud & Wind's red Palace Wall grip", "Cloud &amp; Wind &middot; Cherry"),
 (21, "A man in Parmore's forest green Varsity Quarter-Zip on a city street", "Parmore &middot; Forest"),
 (22, "A golfer in Puttwell's deep green Wordmark long-sleeve tee", "Puttwell &middot; Forest"),
 (23, "A golfer in a green Puttwell cap and long-sleeve tee", "Puttwell &middot; Forest + Leaf"),
 (24, "A hand holding Lazyface's green Facescreen on a green background", "Lazyface &middot; Forest + Leaf"),
]
SWATCHES = "".join(f'<span style="display:inline-block;width:22px;height:22px;background:{a[1]};border:1px solid rgba(20,20,20,.25)"></span><span style="display:inline-block;width:22px;height:22px;background:{a[3]};border:1px solid rgba(20,20,20,.25);margin-right:10px"></span>' for a in PAIRS.values())
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>It started with a palette carousel we saved from a design account: seven two-color pairings, each one a dark color next to a soft off-white, each with its hex codes. Royal blue and chalk. Red wine and light sand. Orange and linen. It was made for graphic designers, but it kept reminding us of a golf bag.</p>
    <p>That is because golf already dresses in pairs. A polo and trousers. A driver cover and a putter cover. A grip and a glove. The combos that look good on a first tee are almost never three or four colors; they are one strong color and one quiet one, used more than once. So we took the seven pairings and built each one out of things you can buy from independent brands right now: clothes, headcovers, grips and the small things that hang off a bag.</p>
    <p>Below, each pairing gets its own swatch with the hex codes, then at least seven pieces: some carry the strong color, some carry the off-white, and a few, like Left of Field&rsquo;s duckbill cap or RIPIT&rsquo;s Clay and Cream grip, carry both. At the bottom is a gallery of the brands&rsquo; own photos, from the lookbooks and in the wild, so you can see the pairings on people instead of on a screen.</p>
    <h2 class="products-hdr btk-story-hdr">How to Use a Two-Color Combo</h2>
    <p>Pick one pairing and give the strong color to one or two pieces only, a polo and a headcover, or a hat and a grip. Everything else gets the off-white or a neutral. The second time the strong color shows up, on a towel, a putter cover or a cap, is what makes it look planned instead of accidental. Three times is plenty.</p>
    <p>A few names have changed from the original carousel. The two colors it called milk are linen and cream here, and royal blue&rsquo;s partner is chalk so that cream only appears once. The hex codes are the carousel&rsquo;s. All 51 pieces were in stock on each brand&rsquo;s own store on October 13, 2026. Prices are in each store&rsquo;s currency, with an approximate dollar figure; where a brand charges US customers a set dollar price, that is shown second instead.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pairings</span><span>Seven</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>51</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$14.50&ndash;US $388</span></div>
      <div class="sidebar-detail"><span class="l">Easiest</span><span>Midnight Indigo + Vanilla</span></div>
      <div class="sidebar-detail"><span class="l">Boldest</span><span>Orange + Linen</span></div>
      <div class="sidebar-detail"><span class="l">Rarest</span><span>Plum + Cream</span></div>
      <div class="sidebar-detail"><span class="l">Palette</span><span>""" + SWATCHES + """</span></div>
      <a href="#lookbooks" class="sidebar-cta">See the lookbooks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#ColorCombos</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#Headcovers</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What are good color combinations for golf outfits?", "Two-color pairings with one strong color and one soft off-white are the easiest to wear: royal blue and chalk, red wine and light sand, orange and linen, plum and cream, midnight indigo and vanilla, cherry and alabaster, or forest and leaf green."),
 ("How do I match my headcovers to my outfit?", "Pick the strong color from your pairing and use it on one or two headcovers, then let the rest of the bag stay neutral. A grip, towel or cap in the same color ties it together without matching everything."),
 ("What is the easiest golf color combo to start with?", "Navy and cream. Most golfers already own a navy polo or cap, and cream trousers or an off-white cover finish it. Criquet, Fella, Left of Field and Woodgrain all have pieces for it here."),
 ("Where do the hex codes come from?", "From a palette carousel of seven two-color pairings by a graphic design account. We kept its hex codes and renamed the two colors it called milk as linen and cream, and called royal blue's partner chalk."),
 ("How much do these pieces cost?", "On October 13, 2026 they ran from $14.50 (IOMIC grips) to US $388 (Late Nine's cable knit polo), with most between $18 and $130."),
]
HERO_ALT = "A model in a Students Golf dark green jacket over a cream cable-knit polo, against a pale sage background"
FRN = json.loads((ROOT / "research/color-combos/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-CC-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = SHOP + handle
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
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-13", "dateModified": "2026-10-13",
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
    assert len(LIFE) >= 20 and all((ROOT / f"{IMG.lstrip('/')}/life-{n}.jpg").is_file() for n, _, _ in LIFE)
    for s in SECTIONS: assert len(s[2]) >= 7, s[0]
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Seven pairings, hex codes included</span><span class="dot"></span>
    <span>51 picks &middot; in stock, checked October 13, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += lookbooks()
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Lehi", "Rookline", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram", "Wine Red", "Milk"):
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
