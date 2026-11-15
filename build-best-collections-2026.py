#!/usr/bin/env python3
"""build-best-collections-2026.py — Our Favorite Golf Collections of 2026 (12, unranked except Metalwood first) + honorable mentions. 15 November 2026.
Cloned from build-climbing-golf.py. Lenny: "a post about the best golf collections of 2026" -> ranked top 10,
indie and fashion brands (collabs count, OEMs only as collab partners) -> options sheet -> "bump up to 12 so we can
include sugarloaf and students".
FACTS: every collection has its own TGI post (linked). Prices and stock read from each store 15 Nov 2026
(Shopify .js / products.json; PUMA Europe in browser). ALD's SS26 golf pieces are gone from ALD's store: prices are
from our June coverage and marked sold out. Non-US prices in native currency with approximate USD
(EUR 0.90, GBP 0.752, CAD 0.73, JPY ~160, ZAR ~18 per USD). Men only. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Our Favorite Golf Collections of 2026"
DESC = ("Our 12 favorite golf collections of 2026, from Metalwood Studio FW26 and Malbon's Ironworks to Mantra and "
        "Walker: why each one mattered, 48 standout pieces, what is still in stock and six honorable mentions.")
H1 = "Our Favorite Golf Collections of 2026"
BC = "Favorite Golf Collections of 2026"
SLUG = "best-golf-collections-2026"
IMG = "/images/best-collections-2026"
DATE = "2026-11-15"

# (brand, item, price, url, copy)
P = {
 # 1 Metalwood Studio FW26
 "b01": ("Metalwood Studio", "Raglan Sleeve Blouson", "$298", "https://metalwood.studio/products/raglan-sleeve-blouson-tan",
   "Cotton-poly, raglan sleeves, a western back yoke and a hidden button placket over the zip. The piece we&rsquo;d buy first."),
 "b02": ("Metalwood Studio", "Oasis Parka", "$248", "https://metalwood.studio/products/oasis-parka-black",
   "The hooded shell from the lookbook, in black."),
 "b03": ("Metalwood Studio", "Goalie Jersey", "$168", "https://metalwood.studio/products/goalie-jersey-blue",
   "A padded hockey-style jersey with the Metalwood wordmark across the chest."),
 "b04": ("Metalwood Studio", "Trophy Pant", "$168", "https://metalwood.studio/products/trophy-pant-black",
   "A wide, easy pant that sits right with everything above it."),
 # 2 Malbon Ironworks
 "b05": ("Malbon", "Foreman Jacket", "$348", "https://malbon.com/products/foreman-jacket-blueberry",
   "Stone-washed denim with Ironworks Dvsn. across the back. The center of the collection."),
 "b06": ("Malbon &times; Red Wing", "Moc Oxford", "$400", "https://malbon.com/products/red-wing-moc-oxford-oro-legacy",
   "Red Wing&rsquo;s Shop Moc, made with Malbon, in Oro Legacy leather."),
 "b07": ("Malbon", "Hickory Windshirt", "$228", "https://malbon.com/products/hickory-windshirt-hickory-brown-stripe",
   "The hickory-stripe workwear fabric, cut as a golf windshirt."),
 "b08": ("Malbon &times; CLUCT", "Divot Tool", "$78 &middot; Sold out", "https://malbon.com/products/cluct-divot-tool-silver",
   "A silver divot tool made in Japan by CLUCT."),
 # 3 Manors AW26
 "b09": ("Manors Golf", "Merino Tech Hoodie", "&pound;225 (about $299)", "https://www.manorsgolf.com/products/merino-tech-hoodie",
   "Merino wool with a technical build. The mid-layer the collection is built around."),
 "b10": ("Manors Golf", "Heritage PrimaLoft&reg; Cardigan", "&pound;160 (about $213)", "https://www.manorsgolf.com/products/heritage-primaloft%C2%AE-cardigan",
   "A cardigan with PrimaLoft insulation. Warm without the bulk."),
 "b11": ("Manors Golf", "Crosswind Cordura&reg; V-Neck", "&pound;195 (about $259)", "https://www.manorsgolf.com/products/crosswind-cordura-vneck",
   "A Cordura pullover in a sweater shape, made to stop the wind."),
 "b12": ("Manors Golf", "Ripstop Tech Trouser", "&pound;150 (about $199)", "https://www.manorsgolf.com/products/ripstop-tech-trouser",
   "Ripstop trousers for cold, wet rounds."),
 # 4 ALD SS26 Golf
 "b13": ("Aim&eacute; Leon Dore", "Lightweight Tips Windbreaker", "$495 &middot; Sold out", "https://www.aimeleondore.com/",
   "Printed woven mesh in Blackwatch plaid, and the most expensive piece in the capsule."),
 "b14": ("ALD &times; FootJoy", "Premiere Series Marquis", "$375 &middot; Sold out", "https://www.aimeleondore.com/",
   "Croc-embossed, waterproof leather with a co-branded insole. Sold out in both colorways."),
 "b15": ("Aim&eacute; Leon Dore", "Clubhouse Sweater", "$395 &middot; Sold out", "https://www.aimeleondore.com/",
   "Merino with an intarsia golfer on the front. The loudest piece in the capsule."),
 "b16": ("Aim&eacute; Leon Dore", "Golf Blackwatch Pullover", "$295 &middot; Sold out", "https://www.aimeleondore.com/",
   "A printed half-zip popover in Blackwatch plaid."),
 # 5 A.P.Cph/Golf
 "b17": ("A.P.Cph/Golf", "Zipper No Collar Jacket", "&yen;28,600 (about $179) &middot; Sold out", "https://captainshelmgolf.com/en/products/chg26-apcg-j01",
   "The collarless jacket with the merged A.P.Cph logo on the back."),
 "b18": ("A.P.Cph/Golf", "L/S Polo Pullover", "&yen;18,700 (about $117) &middot; Sold out", "https://captainshelmgolf.com/en/products/chg26-apcg-t04",
   "A long-sleeve polo pullover in black."),
 "b19": ("A.P.Cph/Golf", "Adjustable Pants", "&yen;19,800 (about $124)", "https://captainshelmgolf.com/en/products/chg26-apcg-p01",
   "Golf pants with an adjustable waist. Still in stock."),
 "b20": ("A.P.Cph/Golf", "Green Fork", "&yen;4,400 (about $28)", "https://captainshelmgolf.com/en/products/chg26-apcg-a01",
   "A divot tool with the A.P.Cph logo. The cheapest way into the collab."),
 # 6 Gumtree x PUMA
 "b21": ("PUMA &times; Gumtree", "Golf Polo", "&euro;36.95 (about $41), was &euro;89.95", "https://eu.puma.com/de/en/pd/puma-x-gumtree-golf--nature-club-golf-polo-men/635619",
   "A striped polo in Sandstone. On sale at PUMA Europe."),
 "b22": ("PUMA &times; Gumtree", "Pardoides Golf T-Shirt", "&euro;22.95 (about $26), was &euro;44.95", "https://eu.puma.com/de/en/pd/puma-x-gumtree-golf--nature-club-pardoides-golf-t-shirt-men/635618",
   "A golf tee with a nature print on the back."),
 "b23": ("PUMA &times; Gumtree", "Relaxed Golf Shorts", "&euro;28.95 (about $32), was &euro;74.95", "https://eu.puma.com/de/en/pd/puma-x-gumtree-golf--nature-club-relaxed-golf-shorts-men/635621",
   "Relaxed shorts in Warm White with a printed hem."),
 "b24": ("PUMA &times; Gumtree", "Golf Cap", "&euro;15.95 (about $18), was &euro;39.95", "https://eu.puma.com/de/en/pd/puma-x-gumtree-golf--nature-club-golf-cap/027047",
   "A Sandstone cap with conservation lettering across the front."),
 # 7 Students fall
 "b25": ("Students", "Denali Stadium Jacket", "$280", "https://studentsgolf.com/products/denali-stadium-jacket",
   "The headline piece from The Curriculum, Students&rsquo; September drop."),
 "b26": ("Students", "Obispo Nylon Jacket, Camo", "$268", "https://studentsgolf.com/products/obispo-nylon-jacket",
   "Camo nylon from Fall Drop 2 in October."),
 "b27": ("Students", "Tradition Double Pleated Wool Pants", "$158", "https://studentsgolf.com/products/tradition-double-pleated-wool-pants",
   "Double-pleated wool trousers in Cement."),
 "b28": ("Students", "Visalia Knit L/S Polo Sweater", "$158", "https://studentsgolf.com/products/visalia-knit-ls-polo-sweater",
   "A long-sleeve knit polo in Midnight."),
 # 8 SSC Hidden Gem
 "b29": ("Sugarloaf Social Club", "Hidden Gem MacKenzie Golf Bag", "$850 &middot; Sold out", "https://sugarloafsocialclub.com/products/hidden-gem-mackenzie-golf-bag",
   "A MacKenzie walking bag in the Hidden Gem colors. Gone fast."),
 "b30": ("Sugarloaf Social Club", "Hidden Gem Windshirt", "$125", "https://sugarloafsocialclub.com/products/hidden-gems-windshirt",
   "The collection&rsquo;s windshirt, still in stock."),
 "b31": ("Sugarloaf Social Club", "Hidden Gem Crazy Creek Chair", "$75", "https://sugarloafsocialclub.com/products/hidden-gem-crazy-creek-chair",
   "A Crazy Creek folding chair for the range, the beach or the parking lot."),
 "b32": ("Sugarloaf Social Club", "Hidden Gem Scoutfitters Nalgene", "$32 &middot; Sold out", "https://sugarloafsocialclub.com/products/hidden-gem-scoutfitters-32-oz-nalgene",
   "A 32 oz. Nalgene with the Hidden Gem graphic."),
 # 9 OVO Golf
 "b33": ("OVO Golf", "Stretch Nylon Polo, Deep Denim", "CA$158 (about $115)", "https://octobersveryown.com/collections/ovo-golf/products/ovo-golf-stretch-nylon-polo-deep-denim-m-0226-wt-6862-nyp",
   "Stretch nylon in deep blue."),
 "b34": ("OVO Golf", "Stretch Nylon Chino, Sandstone", "CA$168 (about $123)", "https://octobersveryown.com/collections/ovo-golf/products/ovo-golf-stretch-nylon-chino-sandstone-m-0226-wb-7182-fe",
   "A golf chino in the same stretch nylon."),
 "b35": ("OVO Golf", "Basketweave Sweater Vest, Cream", "CA$178 (about $130) &middot; Sold out", "https://octobersveryown.com/collections/ovo-golf/products/ovo-golf-basketweave-sweater-vest-cream-m-0226-kt-6678-whs",
   "The basketweave knit vest from the campaign."),
 "b36": ("Vessel &times; OVO", "Monogram Lux Stand Bag", "CA$698 (about $510) &middot; Sold out", "https://octobersveryown.com/collections/ovo-golf/products/vessel-monogram-lux-stand-bag-black-cust-lxstd25-sp-bk",
   "A black monogram stand bag made by Vessel."),
 # 10 Public Drip Nightshift
 "b37": ("Public Drip", "Triborough Waffle Knit Polo, Coffee", "$110", "https://publicdrip.com/products/triborough-waffle-knit-polo-coffee",
   "Waffle knit in the drop&rsquo;s coffee color."),
 "b38": ("Public Drip", "The Herringbone Half Zip, Coffee", "$140", "https://publicdrip.com/products/the-herringbone-half-zip-coffee",
   "A herringbone half zip for cold mornings."),
 "b39": ("Public Drip", "Anywhere Pleated Pants, Charcoal", "$170", "https://publicdrip.com/products/anywhere-pleated-pants-charcoal",
   "Double-pleated trousers in charcoal."),
 "b40": ("Public Drip", "&ldquo;P&rdquo; Script Denim Bucket, Indigo", "$65", "https://publicdrip.com/products/p-script-denim-bucket-indigo",
   "An indigo denim bucket hat with the script P."),
 # 11 Walker Blooming Grounds
 "b41": ("Walker Golf Things", "Blooming Grounds Knit Polo", "$84, was $120 &middot; Sold out", "https://www.walkergolfthings.com/en-us/products/blooming-grounds-knit-polo",
   "A full-jacquard knit of the hand-drawn course scene. The star of the drop."),
 "b42": ("Walker Golf Things", "Blooming Grounds T-Shirt", "$30, was $50", "https://www.walkergolfthings.com/en-us/products/blooming-grounds-t-shirt",
   "The same course scene printed on the back of a white tee."),
 "b43": ("Walker Golf Things", "Hedge Hood, Navy", "$77, was $110", "https://www.walkergolfthings.com/en-us/products/hedge-hood",
   "A 400gsm hood with the Walker script in green."),
 "b44": ("Walker Golf Things", "Hedge Mid Cap, Navy", "$35, was $50", "https://www.walkergolfthings.com/en-us/products/hedge-mid-cap",
   "A navy cap with contrast stitching."),
 # 12 Mantra Golf, Sonoran Desert
 "b45": ("Mantra Golf", "Legacy Crewneck Pullover, Birdie Embroidery", "$168", "https://mantragolf.com/products/mens-legacy-crewneck-pullover-birdie-embroidery",
   "Limited edition: cream heavyweight cotton fleece covered in hand-drawn embroidery of North American birds. The piece people will ask about."),
 "b46": ("Mantra Golf", "Legacy Quarter Zip, Sea Salt", "$118, was $158", "https://mantragolf.com/products/mens-legacy-quarter-zip-sea-salt",
   "The quarter-zip version of Mantra&rsquo;s first heavyweight fleece."),
 "b47": ("Mantra Golf", "Pique Polo L/S, Checkerboard", "$108", "https://mantragolf.com/products/mens-pique-polo-ls-checkerboard",
   "A long-sleeve pique polo in a checkerboard that looks borrowed from a 1970s pro shop."),
 "b48": ("Mantra Golf", "Signature Mock Neck L/S, Prickly Pear", "$98", "https://mantragolf.com/products/signature-mock-neck-ls-prickly-pear",
   "A long-sleeve Pima cotton mock in one of the collection&rsquo;s desert colors."),
}

# rank, anchor, collection name, kicker, why (html), links [(href, text)], campaign (file, alt, caption), ids
ENTRIES = [
 (12, "mantra", "Mantra Golf, The Sonoran Desert Collection", "San Francisco &middot; Released October 8",
  "<p>Every season Mantra builds a collection around a landscape, from the Scottish Highlands and the Norwegian fjords to the redwoods. This fall it went to the Sonoran Desert, shot in Arizona in late September, and it&rsquo;s the best collection the San Francisco brand has made, mostly because of the Legacy fleece, its first heavyweight layer.</p><p>The colors are clay, prickly pear, agave and sand. The standout is a cream Legacy crewneck covered in hand-drawn embroidery of North American birds, and there&rsquo;s a long-sleeve pique polo in a checkerboard straight out of a 1970s pro shop. Mantra is Climate Neutral certified and gives at least 1% of sales to conservation. Everything below is in stock, and the quarter zip is on sale.</p>",
  [("/drops/brand-to-know-mantra-golf", "Brand to Know: Mantra Golf")],
  ("c12", "A golfer in a brown Mantra knit holding a flagstick in the desert", "Mantra Golf"),
  ["b45", "b46", "b47", "b48"]),
 (11, "walker", "Walker Golf Things, Blooming Grounds", "Australia &middot; Released August 21",
  "<p>Walker Golf Things draw everything by hand, and Blooming Grounds is the fullest expression of that they have put out. The Australian brand released it on August 21 as an ode to spring and the flora along the fairways, which is exactly right in Melbourne and a forward buy in an Austin August.</p><p>One piece matters more than the rest. The knit polo has a whole landscape knitted into the body as a jacquard, so the picture is made from the yarn itself rather than printed on top. The same scene appears as a print on the tee, and seeing the two side by side makes the point better than any description. The polo sold out; the tee, the hood and the cap are now marked down.</p>",
  [("/drops/walker-golf-blooming-grounds-drop", "Walker&rsquo;s Blooming Grounds")],
  ("c11", "A man in the Walker Blooming Grounds knit polo standing in a bar", "Walker Golf Things"),
  ["b41", "b42", "b43", "b44"]),
 (10, "public-drip", "Public Drip, FW26 Nightshift", "Brooklyn &middot; Released August 21",
  "<p>Public Drip called its fall collection Nightshift, and the name does the describing: coffee, cream, charcoal, black, navy and raw indigo, cut for the round that starts after work and ends somewhere that isn&rsquo;t a golf course.</p><p>The Brooklyn label built its name making New York muni golf look like a scene, and this is its most tailored outing yet: a waffle-knit long-sleeve polo that reads as a sweater, a herringbone half zip with a gold YKK pull, and pleated trousers that would pass at a downtown office. Everything below is under $175, and all of it is still in stock at full price.</p>",
  [("/drops/public-drip-fw26-nightshift", "Public Drip FW26: Nightshift")],
  ("c10", "A golfer in a Public Drip polo and green P cap holding a club on the course at dusk", "Public Drip"),
  ["b37", "b38", "b39", "b40"]),
 (9, "ovo", "OVO Golf, The 2026 Collection", "Toronto &middot; Apparel, Callaway and Vessel",
  "<p>OVO Golf launched in July 2025 with a Callaway and Vessel equipment capsule that sold out within hours. 2026 is where it stopped being a capsule and became a brand: stretch nylon polos, vests and chinos in Midnight Green, Deep Denim and Sandstone, basketweave sweater vests that nod to old country club knits, and open-knit sweater polos with contrast tipping.</p><p>A second equipment drop in July added an Opus SP wedge, Chrome Tour Triple Diamond balls and the Monogram Lux stand bag, and most of it sold out inside 72 hours. The knits and the bag are gone. The nylon pieces, in four-way stretch that is water-repellent and UV-cut, are still in.</p>",
  [("/drops/ovo-golf-2026-collection", "OVO Golf: The 2026 Collection")],
  ("c09", "A golfer in an OVO tee and light blue shorts walking off with a club", "OVO"),
  ["b33", "b34", "b35", "b36"]),
 (8, "sugarloaf", "Sugarloaf Social Club, The Hidden Gem Collection", "McLean, Virginia &middot; Released August",
  "<p>Hidden Gem is a very Sugarloaf Social Club list: an $850 MacKenzie bag next to a $16 frisbee. The McLean, Virginia brand calls itself a beacon for golf nerds who like a mix of high and low, and this collection is that idea turned into product, with USA-made wool headcovers and a Portland-built leather bag at one end and a Nalgene and a Crazy Creek chair at the other.</p><p>It reads less like a golf collection than like packing for a weekend where golf happens to be involved, which is exactly why it made the list. Three pieces sold out on day one, and the MacKenzie and the Nalgene are gone now too. The windshirt and the chair are still there.</p>",
  [("/drops/ssc-hidden-gem-collection", "SSC: The Hidden Gem Collection")],
  ("c08", "A golfer splashing out of a deep links bunker beside the sea", "Sugarloaf Social Club"),
  ["b29", "b30", "b31", "b32"]),
 (7, "students", "Students, Fall 2026", "Los Angeles &middot; The Curriculum and Fall Drop 2",
  "<p>Students released fall in two parts. The Curriculum landed in September, led by the Denali Stadium Jacket, a heavy wool jacket that gets better with years, and double-pleated wool trousers. Fall Drop 2 followed on September 30 with two jackets in an oil-slick camo the brand says is based on a golf course pond, plus waffle-knit and diamond-knit sweater polos.</p><p>Together they make the fullest fall wardrobe any streetwear-golf label put out this year, and they hit every idea of the season: the knit polo as the shirt of fall, texture over shiny polyester, and a real jacket for the walk to the first tee. Every piece below is in stock.</p>",
  [("/drops/fall-drops-eastside-students-devereux", "Fall 2026 Golf Drops"), ("/drops/fresh-fall-drops-students-walker-sugarloaf", "Three Fresh Fall Drops")],
  ("c07", "A man in a dark green Students jacket and cap against a green wall", "Students"),
  ["b25", "b26", "b27", "b28"]),
 (6, "gumtree-puma", "Gumtree Golf &times; PUMA, Field Notes", "Collab &middot; Released April",
  "<p>A brand that hand-sews headcovers from vintage fishing waders, working with PUMA. Field Notes put Gumtree&rsquo;s nature-first ideas into polos, tees, shorts and a cap at PUMA&rsquo;s scale, and it was the indie-meets-big-brand collab of the year.</p><p>Gumtree puts two percent of every purchase toward pulling carbon out of the atmosphere, and the collection carries that through to the details, from the print along the hems of the shorts to the conservation lettering on the cap. It&rsquo;s sold out on PUMA&rsquo;s US site. PUMA Europe still has it, at outlet prices that make it the cheapest entry on this list.</p>",
  [("/drops/gumtree-golf-x-puma-the-field-notes-collection-lands", "Gumtree Golf &times; PUMA: Field Notes")],
  ("c06", "A golfer in shorts and a grey hoodie swinging on a hillside course", "Gumtree Golf &amp; Nature Club"),
  ["b21", "b22", "b23", "b24"]),
 (5, "apcph", "A.P.C. Golf &times; Cph/Golf", "Paris &times; Tokyo &middot; Released September 2",
  "<p>The two marks don&rsquo;t sit side by side on these 18 pieces. They were welded into one, A.P.Cph, on the chest of nearly everything A.P.C. Golf and Tokyo&rsquo;s Cph/Golf released on September 2. Several tops carry 39 RUE MADAME PARIS, A.P.C.&rsquo;s head office, across the back, and the half zip runs it against Cph/Golf&rsquo;s own house line, NOT A GOLF GENTLEMAN.</p><p>Everything sits in black, navy, white, cream and light gray. It was a Japan-only release on a Japan-only store, and six of the eighteen pieces sold out on day one, including the jacket and the polo below. The pants and the green fork are still on Captain&rsquo;s Helm&rsquo;s site.</p>",
  [("/drops/apc-golf-cph-golf-collab", "A.P.Cph/Golf: the 18-piece drop")],
  ("c05", "The back of a navy and black A.P.Cph/Golf jacket with the merged logo", "A.P.Cph/Golf"),
  ["b17", "b18", "b19", "b20"]),
 (4, "ald", "Aim&eacute; Leon Dore, SS26 Golf", "New York &middot; Released April 23",
  "<p>ALD&rsquo;s third golf capsule landed April 23 and ran 55 pieces: Blackwatch plaid windbreakers and popovers, double-pleated Cordura pants and shorts, merino intarsia knits, diamond jacquard quarter zips and croc-embossed FootJoy Premiere Series Marquis shoes. Performance fabrics throughout, and nothing that looks like it came from a pro shop.</p><p>The FootJoys were the headline, waterproof leather with a co-branded insole, and they sold out in both colorways. The knits were the quieter win: the kind you&rsquo;d wear to dinner after the round without anyone knowing they were golf clothes. Every piece below is sold out. It still set the look for the year.</p>",
  [("/drops/aim-leon-dore-ss26-golf-croc-embossed-footjoys-and-a-sweater", "ALD SS26 Golf"), ("/drops/ald-golf-ss26-new-releases", "ALD Golf SS26: 10 Picks")],
  ("c04", "A man in a Blackwatch plaid jacket and black trousers against a grey backdrop", "Aim&eacute; Leon Dore"),
  ["b13", "b14", "b15", "b16"]),
 (3, "manors", "Manors Golf, AW26 Honourable Company", "London &middot; 22 pieces",
  "<p>The Honourable Company is 22 pieces built around merino, PrimaLoft insulation and Cordura ripstop. The name points at the Honourable Company of Edinburgh Golfers, the club that wrote the first surviving rules of golf in 1744, and Manors has always borrowed that formal vocabulary (Stableford, Greenskeeper, Ranger) and then cut the trousers wide and pleated.</p><p>It&rsquo;s a layering collection, which is the right answer to a season where the first tee is cold and the ninth is not. Merino holds warmth when the temperature drops and sheds it when you walk uphill; PrimaLoft keeps insulating when it gets wet, where down would not. It&rsquo;s the most technical collection on this list, and all four pieces below are in stock.</p>",
  [("/drops/manors-golf-aw26-collection", "Manors&rsquo; Honourable Company AW26")],
  ("c03", "A man in the Manors Merino Tech Hoodie and olive trousers", "Manors Golf"),
  ["b09", "b10", "b11", "b12"]),
 (2, "malbon", "Malbon Golf, The Ironworks", "Los Angeles &middot; Fall 2026",
  "<p>Malbon&rsquo;s fall collection runs to 88 pieces, and about 27 of them matter. What holds them together is Ironworks Division, built from heavyweight stone-washed hickory-stripe denim, the striped cotton painters and railroad crews wore, and run across a jacket, a carpenter short, overalls, a sweatshirt, a snapback and a driver headcover. It&rsquo;s the least golf-looking thing Malbon has made.</p><p>Under that run a herringbone twill called Station, an all-over Inkwash print on two windshirts and a short, and two knits doing the quiet work logos usually do. Two collaborations close it out, and both are better than anything Malbon made on its own: a Red Wing Shop Moc oxford and a CLUCT divot tool made in Japan.</p>",
  [("/drops/malbon-fall-2026-the-ironworks-collection", "Malbon&rsquo;s Ironworks Collection")],
  ("c02", "The back of a Malbon denim Foreman jacket printed Malbon Ironworks Dvsn.", "Malbon Golf"),
  ["b05", "b06", "b07", "b08"]),
 (1, "metalwood", "Metalwood Studio, FW26", "Los Angeles &middot; 36 styles",
  "<p>When we profiled Metalwood in June, it ran on medieval heraldry and &rsquo;90s tour polos. FW26 shows founder Cole Young building something bigger than a golf brand: of 36 styles, one is a polo and seven are outerwear. There&rsquo;s a padded goalie jersey with a 94 on the back, a reversible tee, and western yokes on the track jacket and the blouson.</p><p>Golf still shows up in the graphics, like the iGolf hat, but the clothes are cut for the rest of the week, and the fits keep getting bigger. It&rsquo;s a fashion collection with a golf accent rather than golf clothing with a fashion edge, and it&rsquo;s the clearest picture of where independent golf clothing went this year. The &ldquo;Pt 1&rdquo; on the lookbook says more is coming. All four pieces below are in stock.</p>",
  [("/drops/metalwood-studio-fw26-collection", "Metalwood Studio FW26: The Full Collection")],
  ("c01", "A man pulling a blue Metalwood jersey over his head", "Metalwood Studio"),
  ["b01", "b02", "b03", "b04"]),
]
N = 48

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We covered dozens of golf collections this year. These are the twelve we kept coming back to.</p>
    <p><strong>How we picked them.</strong> Design first: did the collection have a point of view, and did every piece belong to it? Then depth, because a full wardrobe beats a single great polo. Then whether it works on a course and off it. We kept to independent golf labels and fashion brands doing golf. Big golf companies only count as collab partners, which is how FootJoy, PUMA, Callaway, Vessel and Red Wing got in.</p>
    <p><strong>What is still out there.</strong> Each entry has four standout pieces with prices we checked on November 15. Plenty of spring pieces have sold out; we kept them in with a sold-out tag rather than pretend the collection was something else. ALD&rsquo;s capsule is gone entirely, and Gumtree &times; PUMA now lives at PUMA Europe at outlet prices. Each entry links to our original coverage.</p>
    <p><strong>What 2026 looked like.</strong> Fashion brands stopped dabbling. ALD put out its third and biggest golf capsule, OVO went from equipment to a full clothing line, and A.P.C. teamed up with Tokyo&rsquo;s Cph/Golf. The independents moved past the polo: Metalwood&rsquo;s fall collection has seven pieces of outerwear and one polo, Malbon built its season around workwear denim, and Manors went deep on merino and insulation. The knit polo became the shirt of fall. And some of the best work came from well outside the usual places, like Australia&rsquo;s Walker and Cape Town&rsquo;s Odd Ritual.</p>
    <p><strong>The verdict.</strong> Metalwood Studio FW26 is our collection of the year: the most complete, the most confident, and the clearest look at where golf clothing is heading. It comes first below, with Malbon&rsquo;s Ironworks right behind it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Twelve</div>
      __LIST__
      <div class="sidebar-detail"><span class="l">Prices</span><span>Checked Nov 15, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#GolfFashion</span>
        <span class="hashtag">#2026</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">Keep Going</div>
  <h2 class="products-hdr" id="more">More From 2026</h2>
  <div class="writeup-body">
    <p>For the bigger picture, read <a href="/drops/golf-style-trends-2026">our 2026 golf style trends</a>. For the brands behind several of these collections, see <a href="/drops/best-golf-streetwear-brands-2026">the 10 best golf streetwear brands in 2026</a>, and for the smaller collabs we liked this fall, <a href="/drops/favorite-golf-collabs-november-2026">our favorite golf collabs this month</a>.</p>
  </div>
</section>
"""
CAMP = {int(k): v for k, v in json.loads((ROOT / "research/best-collections-2026/camp.json").read_text()).items()}
FRN = json.loads((ROOT / "research/best-collections-2026/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
 '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 72px)/4);min-width:0}'
 '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
 '.product-card[data-frames="1"] .pg-arw,.product-card[data-frames="1"] .pg-count,.product-card[data-frames="1"] .pg-dots{display:none!important}'
 '.bc-nums{max-width:1400px;margin:8px auto 0;padding:0 32px;display:grid;grid-template-columns:repeat(4,1fr);border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}'
 '.bc-nums div{padding:22px 18px;border-right:.5px solid rgba(20,20,20,.2);text-align:center}.bc-nums div:last-child{border-right:none}'
 '.bc-nums b{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(36px,5vw,64px);line-height:1;color:var(--grass)}'
 '.bc-nums span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}'
 '@media(max-width:820px){.bc-nums{grid-template-columns:repeat(2,1fr);padding-left:18px;padding-right:18px}.bc-nums div:nth-child(2){border-right:none}.bc-nums div:nth-child(n+3){border-top:.5px solid rgba(20,20,20,.2)}}'
 '.bc-top{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:center;margin:0 auto 36px}'
 '.bc-camp{margin:0}.bc-camp .product-gallery{border:.5px solid var(--ink)}'
 '.bc-rank{font-family:var(--serif);font-size:clamp(72px,10vw,140px);line-height:.85;color:var(--grass);margin-bottom:14px}'
 '.bc-rank small{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);opacity:.6;margin-bottom:10px}'
 '.bc-txt{text-align:center}.bc-txt p{margin:0 0 14px!important}.bc-txt .products-hdr{margin-top:6px!important}.bc-txt p{line-height:1.65}'
 '.bc-read{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-top:18px;line-height:2}'
 '.bc-read a{border-bottom:1px solid var(--ink)}'
 '.bc-list a{border-bottom:none}.bc-list .sidebar-detail span:last-child{text-align:right}'
 '.bc-q{margin:0 auto 22px;max-width:520px;font-family:var(--serif);font-style:italic;font-size:clamp(22px,2.2vw,30px);line-height:1.3;color:var(--grass)}'
 '.bc-q cite{display:block;margin-top:12px;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:.6}'
 '.bc-hm{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:24px}'
 '.bc-hm-card{display:block;text-align:center;border-bottom:none!important;color:inherit}'
 '.bc-hm-card img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;border:.5px solid var(--ink);margin-bottom:14px}'
 '.bc-hm-brand{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6}'
 '.bc-hm-name{display:block;font-family:var(--serif);font-style:italic;font-size:20px;margin:6px 0 8px}'
 '.bc-hm-txt{display:block;font-size:14px;line-height:1.55;max-width:340px;margin:0 auto}'
 '.bc-hm-go{display:inline-block;margin-top:12px;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--ink)}'
 '@media(max-width:820px){.bc-hm{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.bc-hm-txt{font-size:13px}}'
 '@media(max-width:820px){.bc-top{grid-template-columns:1fr;gap:22px}.bc-rank{font-size:84px}}'
 '</style>\n')


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


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": f"https://thegrassyissue.com{e[5][0][0]}",
              "name": H.unescape(re.sub(r"<[^>]+>", "", e[2]))} for i, e in enumerate(sorted(ENTRIES, key=lambda e: e[0]))]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
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


# verbatim quotes, sources: TGI coverage (brand pages / collection posts), malbon.com product copy, walkergolfthings.com product copy,
# aimeleondore.com/blogs/news/aime-leon-dore-golf-2, octobersveryown.com/pages/ovo-golf-collection-drop-02-2026
Q = {
 1: ("Golf is a contact sport. You&rsquo;re just not playing it correctly.", "Metalwood Studio, on the Goalie Jersey"),
 2: ("The Foreman Jacket reimagines classic workwear through the Malbon lens.", "Malbon Golf"),
 3: ("It&rsquo;s one of the only sports where you can actually choose what to look like and how to dress.", "Jojo Regan, Manors co-founder"),
 4: ("New styles thoughtfully designed for the modern game.", "Aim&eacute; Leon Dore, on its third golf capsule"),
 5: ("I don&rsquo;t like the way that amateur players try to dress like professional golfers. I just want them to be chic.", "Jean Touitou, founder of A.P.C."),
 6: ("I like to describe Gumtree to people as almost a slow-fashion golf brand.", "Karsten Jurkschat, Gumtree founder"),
 7: ("My past as a designer is rooted in streetwear, so it gets me excited to bring those principles to golf in ways that the sport hasn&rsquo;t had access to yet.", "Michael Huynh, Students founder"),
 8: ("All I&rsquo;ve ever wanted to do is make cool stuff with my friends.", "Ian Gilley, Sugarloaf Social Club founder"),
 9: ("Built for the course and everywhere after it.", "OVO, on OVO Golf Drop 2"),
 10: ("The city plays public.", "Public Drip"),
 11: ("A Walker Golf Things ode to the course itself.", "Walker Golf Things, on Blooming Grounds"),
 12: ("Our flagship product is the polo, and we call it the most versatile polo on the planet.", "Dom Natalizio, Mantra co-founder"),
}

HM = [
 ("hm-odd", "Odd Ritual", "Collection 03", "/drops/brand-to-know-odd-ritual",
  "Cape Town&rsquo;s golf culture brand grew into a full wardrobe: the Caddie Jacket, pleated trousers and a 1990s polo, all made in South Africa.",
  "A golfer in an Odd Ritual tee and white cap finishing his swing"),
 ("hm-jones", "Jones &times; Cph/Golf", "Round Two", "/drops/jones-cph-golf-collab",
  "Portland&rsquo;s bag maker and Tokyo&rsquo;s Cph/Golf reunited for a &rsquo;90s windbreaker, mock necks, pants, caps and a Trouper stand bag.",
  "A man in a black Jones Sports Co. windbreaker on a golf course"),
 ("hm-arsham", "Daniel Arsham &times; Malbon", "Chapter Three", "/drops/arsham-malbon-chapter-three",
  "Fifteen pieces in Arsham&rsquo;s oxidized green palette with his eroded Buckets logo, from $38 to $448.",
  "The white Arsham x Malbon Cloudburst rain jacket"),
 ("hm-gumtree", "Gumtree Golf &amp; Nature Club", "The Nature Club Drop", "/drops/gumtree-nature-club-drop",
  "Sixteen pieces sewn by hand in New York from deadstock lace, wetsuit neoprene, Angora mohair and reclaimed cotton.",
  "A cream deadstock lace camp shirt from Gumtree Golf and Nature Club"),
 ("hm-eastside", "Eastside Golf", "Fall 2026", "/drops/fall-drops-eastside-students-devereux",
  "The Course Camo print repeats a golf landscape until it reads as camouflage, and the Pitch Jersey borrows from football shirts.",
  "A man in an Eastside Golf Course Camo polo"),
 ("hm-devereux", "Devereux", "Pioneertown Golf Club", "/drops/fall-drops-eastside-students-devereux",
  "Devereux went to the high desert for fall, with western polos and pearl snaps from $74.",
  "A golfer in a Devereux shirt swinging on a desert road"),
]


def honorable():
    cards = "\n".join(
        f'  <a class="bc-hm-card" href="{u}"><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" />'
        f'<span class="bc-hm-brand">{b}</span><span class="bc-hm-name">{c}</span><span class="bc-hm-txt">{t}</span>'
        f'<span class="bc-hm-go">Our coverage &rarr;</span></a>'
        for f, b, c, u, t, a in HM)
    return ('\n<section class="products" id="honorable-mentions" style="margin-top:8px;">\n'
            '  <div class="drop-tag grass">Six More</div>\n'
            '  <h2 class="products-hdr">Honorable Mentions</h2>\n'
            '  <p class="cat-kicker">Six more collections from 2026 that nearly made the twelve.</p>\n'
            f'  <div class="bc-hm">\n{cards}\n  </div>\n</section>\n')


def gallery(imgs, rank):
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}/{f}.jpg" alt="{a}" loading="{"eager" if rank == 1 and j == 0 else "lazy"}" /></div>' for j, (f, a) in enumerate(imgs))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(imgs)))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(imgs)}</span><div class="pg-dots">{dots}</div></div>')


def entry(e, n0):
    rank, anchor, name, kicker, why, links, (cf, calt, ccap), ids = e
    reads = " &middot; ".join(f'<a href="{h}">{t}</a>' for h, t in links)
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" id="c-{anchor}" style="margin-top:8px;">\n'
            f'  <div class="bc-top">\n'
            f'    <figure class="bc-camp" data-frames="{len(CAMP[rank])}">{gallery(CAMP[rank], rank)}<figcaption class="ig-cap">{ccap}</figcaption></figure>\n'
            f'    <div class="bc-txt">\n'
            
            f'      <blockquote class="bc-q">&ldquo;{Q[rank][0]}&rdquo;<cite>&mdash; {Q[rank][1]}</cite></blockquote>\n'
            f'      <div class="drop-tag grass">{kicker}</div>\n'
            f'      <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'      {why}\n'
            f'      <div class="bc-read">Our coverage: {reads}</div>\n'
            f'    </div>\n  </div>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for e in ENTRIES for k in e[7]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    assert sorted(e[0] for e in ENTRIES) == list(range(1, 13))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    for e in ENTRIES:
        assert all((ROOT / IMG.lstrip("/") / f"{f}.jpg").is_file() for f, _ in CAMP[e[0]]), e[0]
    sold = sum("Sold out" in P[k][2] for k in ids)
    lst = "\n      ".join(
        f'<div class="sidebar-detail"><span class="l">{re.sub(r",.*", "", e[2])}</span><span><a href="#c-{e[1]}">{re.sub(r"^[^,]*, ", "", e[2])}</a></span></div>'
        for e in sorted(ENTRIES, key=lambda e: e[0]))
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
    <span>Drops &amp; Brands &middot; Year in Review</span><span class="dot"></span>
    <span>12 collections &middot; {N} pieces &middot; prices checked November 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a Manors cap lying flat on the green to read a putt while two friends wait behind him" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("__LIST__", '<div class="bc-list">' + lst + '</div>')
    n = 1
    for e in sorted(ENTRIES, key=lambda e: e[0]):
        o, n = entry(e, n); body += o
    body += honorable()
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards, {sold} sold out")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    text = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\b(worth|genuinely|honestly|straightforward|selling out)\b", text, re.I): bad.append("banned word")
    for f in set(re.findall(r'src="(/images/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
