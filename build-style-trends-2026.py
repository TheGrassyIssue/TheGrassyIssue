"""build-style-trends-2026.py — The Year in Golf 2026, Part 1: Style & Design (12 November 2026).
Lenny: "an in-depth post about the golf trends of 2026, what we saw, who made waves and what we think might be trends in 2027"
-> scope: style & design, manufacturing, courses; "Let's start with Style and Design". Parts 2 (manufacturing) and 3 (courses) to follow.
FACTS: trend evidence is TGI's own 2026 coverage (linked). Prices/stock read live in Chrome on 12 Nov 2026 as shown to a US visitor.
Frames reuse each product's existing TGI frames (research/style-trends-frames.json); white sweeps re-toned to stone.
"""
import html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/hidden-details-golf-gear.html"
SLUG = "golf-style-trends-2026"
TITLE = "Golf Style Trends of 2026: 7 Trends, the Brands Behind Them and What Comes Next in 2027"
DESC = ("The golf style trends that defined 2026, from pleated trousers and natural fibers to needlepoint, remade headcovers and global indie brands, "
        "with the brands that made waves and our calls for 2027.")
H1 = "Golf Style Trends of 2026: What We Saw, Who Made Waves and What Comes Next"
BC = "Golf Style Trends 2026"
IMG = "/images/style-trends-2026"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
FR = json.loads((ROOT / "research/style-trends-frames.json").read_text())
def L(slug, text): return f'<a href="/drops/{slug}">{text}</a>'

# (handle, brand, product name, price shown to a US visitor 12 Nov 2026, url)
P = {
 "baggy-trousers-black": ("Merrill Golf", "Baggy Pleated Trousers, Black", "$125", "https://merrillgolf.com/products/baggy-trousers-black"),
 "clubhouse-pants-olive": ("Twentyfour Golf", "Clubhouse Pants, Olive", "$58 (was $115)", "https://twentyfourgolf.com/products/clubhouse-pants-olive"),
 "renato-golf-trousers-iaj-psanz-h08055": ("A.P.C. Golf", "Renato Golf Trousers, Navy", "&euro;260 (~$289)", "https://apcstore.com/products/renato-golf-trousers-iaj-psanz-h08055"),
 "pare-plisse-pants-2-0": ("Par&eacute;", "Plisse Pants 2.0", "$150", "https://pare.golf/products/pare-plisse-pants-2-0"),
 "mens-ventile-wind-shirt": ("SLOAT", "Organic Ventile Wind Shirt", "$295", "https://sloat.cc/products/mens-ventile-wind-shirt"),
 "whitman-knit-polo": ("Radmor", "Whitman Knit Polo", "$115.50 (was $165)", "https://radmorgolf.com/products/whitman-knit-polo"),
 "linen-trouser": ("Rowena Golf Club", "Laurel Linen Trouser, Navy Pinstripe", "$108", "https://rowenagolf.com/products/linen-trouser"),
 "big-wale-carpenter-pant": ("Gramicci", "Big Wale Carpenter Pant", "$140", "https://gramicci.com/products/big-wale-carpenter-pant"),
 "golf-flags-needlepoint-belt-green": ("Good Threads", "Golf Flags Needlepoint Belt, Green", "$125", "https://goodthreadsneedlepoint.com/products/golf-flags-needlepoint-belt-green"),
 "mallard-wool-head-cover": ("Local GC", "Mallard Wool Headcover", "NZ$110 (~$62)", "https://www.localgc.co.nz/product/mallard-wool-head-cover"),
 "emerald-putter": ("Golden Soul Golf", "Emerald Blade Putter Cover", "$160", "https://www.goldensoulgolf.com/blade-putter-covers/emerald-putter"),
 "red-sun": ("Swell Marks", "Red Sun Ball Marker", "$65", "https://swellmarks.com/products/red-sun"),
 "tree-frog-green-camp-tent-headcover": ("Gumtree Golf &amp; Nature Club", "Tree Frog Green Camp Tent Headcover", "$140", "https://www.gumtreegolfandnature.com/shop/p/tree-frog-green-camp-tent-headcover"),
 "custom-football-headcovers": ("Clamp Golf Company", "Custom Slots: Headcovers Made From Your Shirt", "From $35", "https://www.clampgolfcompany.co.uk/products/custom-football-headcovers"),
 "u-s-soccer-upcycled-headcover-driver": ("Matchstick Golf", "U.S. Soccer Upcycled Driver Headcover", "$155", "https://matchstickgolf.com/products/u-s-soccer-upcycled-headcover-driver"),
 "deadstock-russel-hat-beige": ("Radry Golf", "Deadstock Russell Hat", "$35 (was $45)", "https://radry.com/products/deadstock-russel-hat-beige"),
 "old-rip-van-winkle-x-bettinardi-barrels-blade-putter-headcover": ("Old Rip Van Winkle &times; Bettinardi", "Barrels Blade Putter Headcover", "$150", "https://bettinardi.com/products/old-rip-van-winkle-x-bettinardi-barrels-blade-putter-headcover"),
 "realtree-camo-golf-polo-aw26": ("PUMA Golf &times; Realtree", "Realtree Camo Golf Polo", "$90", "https://www.pumagolf.com/products/realtree-camo-golf-polo-aw26"),
 "sherwood-x-dormie-hockey-sock-fairway-headcover-red": ("Sherwood &times; Dormie", "Hockey Sock Fairway Headcover, Red", "$230", "https://dormieworkshop.com/products/sherwood-x-dormie-hockey-sock-fairway-headcover-red"),
 "82180255493": ("Baracuta &times; BEAMS Golf", "G4 Tree Camo Blouson", "&yen;39,600 (~$248)", "https://www.beams.co.jp/item/beamsgolf/blouson/82180255493/"),
 "detour-stripe-polo": ("Midiron &middot; Sydney", "Detour Stripe Polo", "$119", "https://midiron.shop/products/detour-stripe-polo"),
 "wind-shirt-purple-haze": ("No Return Club &middot; Manchester", "Purple Haze Wind Shirt", "$102", "https://noreturnclub.co.uk/products/wind-shirt-purple-haze"),
 "chg26-aw-p02": ("Cph/Golf &middot; Tokyo", "Belted Adjustable Wide Pants", "$120", "https://captainshelmgolf.com/en/products/chg26-aw-p02"),
 "green-1-4-zip-rebrand": ("Parmore Golf &middot; Bournemouth", "Varsity Quarter-Zip", "$160", "https://parmoregolf.com/products/green-1-4-zip-rebrand"),
 "pique-poly-golf-polo-ss-cream": ("Masterpiece Sports Club", "Semi-Private Performance Polo", "$118", "https://masterpiecegolf.com/products/pique-poly-golf-polo-ss-cream"),
 "heavyweight-work-shirt-ss-earth": ("Agronomy Workshop", "S/S Heavyweight Work Shirt, Earth", "$136", "https://agronomywork.shop/store/heavyweight-work-shirt-ss-earth"),
 "forest-green-unstructured-corduroy-cap": ("Draw", "Forest Green Unstructured Corduroy Cap", "$57", "https://drawgolf.co/products/forest-green-unstructured-corduroy-cap"),
 "the-tee-case": ("3 Putt Round", "The iPhone Tee Case", "$40", "https://3puttround.com/products/the-tee-case"),
}

DESCS = {
 "baggy-trousers-black": "Pleated, deliberately baggy and cut in a light stretch fabric, this is the loose trouser at its most direct. Merrill sells by waist and tells you to let a tailor set the length, the way trousers used to be bought.",
 "clubhouse-pants-olive": "A relaxed, straight leg in a stretch nylon blend: the loose look for golfers who still want a performance fabric. Half price when we checked.",
 "renato-golf-trousers-iaj-psanz-h08055": "When a Paris fashion house cuts its golf trouser wide, the trend has left the indie corner. A.P.C. made the Renato in a water-repellent fabric with a little stretch.",
 "pare-plisse-pants-2-0": "Par&eacute; takes the pleat further than anyone, with pleated texture running the full length of the leg. Loose, light and easy to swing in.",
 "mens-ventile-wind-shirt": "The clearest case for natural fibers on the course: a quarter-zip in organic Ventile cotton, woven so tightly it blocks wind and showers without a synthetic membrane.",
 "whitman-knit-polo": "A knit polo in organic cotton and organic silk with a little recycled nylon, from a brand that uses no virgin polyester. It sells on hand-feel, not wicking. On sale from $165.",
 "linen-trouser": "Linen is the oldest answer to a hot round, and Rowena cut it into a relaxed golf trouser with a single pleat and a tee pocket. It also sits neatly in the loose-trouser trend.",
 "big-wale-carpenter-pant": "All-cotton wide-wale corduroy from a climbing brand. Natural fiber, a roomy cut and real warmth for winter golf, without a stitch of polyester.",
 "golf-flags-needlepoint-belt-green": "Needlepoint at its most traditional: pin flags hand-stitched in pearl cotton on 18-count canvas, then finished in full-grain leather. A small maker doing the trend of the year by hand.",
 "mallard-wool-head-cover": "Made to order, one at a time, in Orewa, New Zealand. A hand-sewn wool cover is the opposite of a molded logo cover, and that is the whole appeal.",
 "emerald-putter": "Golden Soul&rsquo;s covers are made by hand in Colombia, and this green and white woven blade cover shows why handmade has become the upgrade golfers notice.",
 "red-sun": "Stainless steel, laser colored and finished by hand in Coronado by a maker who names his markers after surf breaks. Small-batch and personal, which is the whole point of the handmade trend.",
 "tree-frog-green-camp-tent-headcover": "Cut from a 1970s Coleman tent found in Vermont, with 50 years of patina on the waxed canvas. The source material decides how many exist, and no two match.",
 "custom-football-headcovers": "Remade taken personally: send Clamp a football shirt or jersey and it becomes a set of covers. Slots open in small batches, and prices vary by cover.",
 "u-s-soccer-upcycled-headcover-driver": "Built from a reclaimed U.S. men&rsquo;s national team jacket, with USA wrapping around the back and the original neck ribbing kept at the top. One of one, by definition.",
 "deadstock-russel-hat-beige": "Remade does not always mean cut up. Radry took unworn &rsquo;90s Russell Athletic blanks and finished them with its own embroidery, and once the run is gone, it is gone.",
 "old-rip-van-winkle-x-bettinardi-barrels-blade-putter-headcover": "A putter maker and a bourbon distillery with nothing in common but a following. The barrel print and weathered cream finish make something neither would make alone.",
 "realtree-camo-golf-polo-aw26": "PUMA put Realtree&rsquo;s hunting camo, all bark and branches, on a standard golf polo. It is the boldest collab of the year: two worlds with almost no overlap, worn on the first tee.",
 "sherwood-x-dormie-hockey-sock-fairway-headcover-red": "The best kind of collab: real Sherwood hockey socks rebuilt into a fairway cover, with patent leather stitched on like sock tape. Specific, a little funny and impossible to fake.",
 "82180255493": "BEAMS Golf had Baracuta make its classic G4 for the course, minus the ribbed hem so it sits right over a swing, with a tree-camo lining. A collab that changes how the product works.",
 "detour-stripe-polo": "Sydney&rsquo;s take on a &rsquo;90s polo, in wide black and white stripes on a boxy fit. Proof that the indie look now comes from everywhere, not just LA and New York.",
 "wind-shirt-purple-haze": "Manchester weather made this one: a waterproof nylon three-quarter zip with a mesh lining. It is the jacket in nearly every No Return Club photo.",
 "chg26-aw-p02": "Tokyo&rsquo;s version of the wide-leg trend, with a roomy stretch silhouette and a built-in belt. Cph/Golf comes out of the CAPTAINS HELM shop and its city&rsquo;s streetwear scene.",
 "green-1-4-zip-rebrand": "A wind- and water-resistant quarter-zip in bottle green with cream varsity stripes, from an English brand whose whole pitch is No Membership Required. Golf clothes built like streetwear, and proof that UK golf style now travels.",
 "pique-poly-golf-polo-ss-cream": "It looks like a plain cream polo until you find the tee holder built into it. Exactly the kind of detail you only notice by playing in it.",
 "heavyweight-work-shirt-ss-earth": "A 17.5-ounce cotton mock neck, hand-dyed and hand-sewn in Los Angeles, with a tee holder hidden inside the chest pocket that takes three tees.",
 "forest-green-unstructured-corduroy-cap": "A corduroy cap with a small side pouch that holds a tee. It reads as a design detail until the moment you need it.",
 "the-tee-case": "The hidden-details idea applied to the thing you carry most: a phone case with a tee holder molded into the back.",
}

TRENDS = [
 ("loose", "Trousers Got Loose", "Pleats, wide legs and room to turn",
  [f"The shape of 2026 was the double-pleated trouser. We ran {L('the-pants-edit','Pleated Golf Pants Are Back')} in September with 18 pairs, then {L('baggy-golf-pants-edit','Loose Golf Pants')} in November with 18 more, from barrel legs to wide pleats, and neither list was hard to fill.",
   f"{L('brand-to-know-woodgrain-golf','Woodgrain')} built a whole brand on the way the game dressed in the &rsquo;80s and &rsquo;90s, and {L('brand-to-know-ashworth','Ashworth came back')} with its 1987 polo. But the cut spread well past the brands we wrote about most. {L('brand-to-know-merrill-golf','Merrill')} makes a baggy pleated trouser in light stretch fabric, Twentyfour Golf cut its Clubhouse Pants to look as right in the bar as on the tee, A.P.C. Golf sent its Renato trouser out in a wide fit, and Par&eacute;&rsquo;s Plisse Pants are pleated all the way down. Part of it is nostalgia, but part of it is practical: a wide leg breathes on a 100-degree Austin afternoon, and it does not pull when you make a full turn.",
   f"The color story moved with the cut. Our {L('fall-golf-colorways-2026','fall colorways')} post kept landing on chocolate, sage and hunter orange. If you buy one pair of pleated trousers this winter, make it chocolate brown."],
  ["baggy-trousers-black", "clubhouse-pants-olive", "renato-golf-trousers-iaj-psanz-h08055", "pare-plisse-pants-2-0"],
  "A golfer in wide khaki trousers lying on a green, reading a magazine"),
 ("natural", "Natural Fibers Became the Quiet-Luxury Tell", "Cotton, wool and silk back on the course",
  [f"When we ranked the {L('best-quiet-luxury-golf-brands','12 best quiet luxury golf brands')} in October, what the list had in common was not a logo size. It was fabric.",
   f"{L('brand-to-know-sloat','SLOAT')} in San Francisco uses natural fibers only, down to an organic Ventile cotton wind shirt where nearly everyone else uses polyester. {L('brand-to-know-radmor','Radmor')} in Seattle uses no virgin polyester at all. Radmor&rsquo;s Whitman polo is knitted from organic cotton and organic silk. {L('dim-sum-rowena-drvn-small-golf-brands','Rowena')} cut a golf trouser in lightweight linen, and Gramicci&rsquo;s wide-wale carpenter pant is all cotton corduroy. Whim works in American merino, and Ashworth relaunched on Supima cotton.",
   "Performance polyester is not going anywhere, and on a wet day it still wins. But at the top end of independent golf, the brands people talked about this year were the ones selling how a shirt feels, not what it wicks."],
  ["mens-ventile-wind-shirt", "whitman-knit-polo", "linen-trouser", "big-wale-carpenter-pant"],
  "A golfer in a Radmor quarter-zip on a links course"),
 ("handmade", "The Handmade Accessory Boom", "Needlepoint, hand-sewn covers and hand-finished markers",
  [f"Needlepoint was everywhere. We covered it twice: {L('the-needlepoint-belt-report','20 hand-stitched belts')} in August and the {L('golf-needlepoint-roundup','Needlepoint Roundup')} this week, with 36 belts, headcovers and small things. By fall the stitching had moved off the belt and onto driver covers, key fobs, card wallets and scorecard holders.",
   f"The smaller makers are where it got good. Good Threads stitches its belts in pearl cotton on 18-count canvas, a long way from the logo belts in the pro shop. Next to it sat headcovers sewn by hand: {L('brand-to-know-local-gc','Local GC')} makes its wool covers to order in Orewa, New Zealand, {L('brand-to-know-mackem-golf','Mackem')} sews in Perth, and {L('brand-to-know-golden-soul-golf','Golden Soul')} working in leather in Colombia. In Coronado, {L('swell-marks-hinotori-studio-grain-indie-golf-brands','Swell Marks')} finishes its stainless steel ball markers by hand and pours one-off resin pitch tools.",
   "The appeal is the same in every case. When everything in the pro shop is made by the thousand, the thing in your bag made by one person stands out."],
  ["golf-flags-needlepoint-belt-green", "mallard-wool-head-cover", "emerald-putter", "red-sun"],
  "Four needlepoint belts laid on the grass"),
 ("remade", "Remade, Not New", "Headcovers that started life as something else",
  [f"The most interesting headcovers of the year began as something else. {L('brand-to-know-gumtree-golf-and-nature-club','Gumtree Golf &amp; Nature Club')} cuts them from heirloom quilts and old camping tents. {L('brand-to-know-clamp-golf-company','Clamp')} in Yorkshire reworks old Carhartt, Nike and Patagonia pieces into one-off sets, and will make a full set of covers from a single football shirt you send in. Fyfe&rsquo;s {L('fyfe-golf-second-round-headcovers-from-vintage-golf-jackets','Second Round')} series did the same with vintage golf jackets. {L('brand-to-know-matchstick-golf','Matchstick')} upcycles old jerseys, {L('brand-to-know-gamut-golf','Gamut')} cuts covers from real course towels and vintage baseball jerseys, and {L('radry-hats-the-full-lineup','Radry')} takes unworn &rsquo;90s Russell Athletic blank caps and gives them its own treatment.",
   "Each run is limited by the source material, and that is the point. Once the tent is used up, that cover is gone. Clamp&rsquo;s reworked one-off sets and Gamut&rsquo;s covers were all sold out when we checked this week, which tells you how this kind of thing moves."],
  ["tree-frog-green-camp-tent-headcover", "custom-football-headcovers", "u-s-soccer-upcycled-headcover-driver", "deadstock-russel-hat-beige"],
  "Two golfers loading bags into a vintage Porsche by the beach, in Gumtree Golf & Nature Club"),
 ("collabs", "Collabs Everywhere, and the Small Ones Were Best", "Two brands making what neither would alone",
  [f"2026 was the year of the collab. The big names kept them coming all year; our {L('the-payntr-collab-edit','PAYNTR edit')} alone counted 33 pieces, and MacKenzie bags turned up in so many that we keep a running {L('the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site','archive')}.",
   f"Our favorites were the small, specific ones, and most came from outside the usual names. In {L('favorite-golf-collabs-november-2026','this month&rsquo;s collab roundup')}, Sherwood and Dormie turned a hockey sock into a fairway cover, and Bettinardi put Old Rip Van Winkle&rsquo;s barrels on a putter cover. The boldest pairing of the year was {L('puma-golf-x-realtree-precision-in-the-wild','PUMA Golf and Realtree')}, which put hunting camo on a golf polo. In Tokyo, {L('brand-revisited-beams-golf','BEAMS Golf')} had Baracuta make its G4 jacket in tree camo. A good collab makes something neither brand would have made alone. A bad one is a logo on a logo."],
  ["old-rip-van-winkle-x-bettinardi-barrels-blade-putter-headcover", "realtree-camo-golf-polo-aw26", "sherwood-x-dormie-hockey-sock-fairway-headcover-red", "82180255493"],
  "An Old Rip Van Winkle x Bettinardi putter cover, a PUMA Golf x Realtree camo polo and a Sherwood x Dormie headcover"),
 ("global", "Indie Golf Went Global", "Sydney, Manchester, Tokyo, Bournemouth and beyond",
  [f"For a long time, independent golf mostly meant Los Angeles and New York. This year we wrote about {L('brand-to-know-midiron','Midiron')} and {L('brand-to-know-angus-and-grace-go-golfing','Angus &amp; Grace')} in Sydney, {L('brand-to-know-no-return-club','No Return Club')} in Manchester, {L('brand-revisited-cph-golf','Cph/Golf')} in Tokyo, {L('brand-to-know-parmore-golf','Parmore')} in Bournemouth and {L('brand-to-know-alba-golf','Alba')} in Milan. {L('australian-golf-brands-and-trips','Golf in Australia')} alone took ten brands.",
   "What they share is not a look. It is the sense that golf clothes can come from the same place as a city&rsquo;s skate and music scenes. Several of them now show US shoppers their prices in dollars."],
  ["detour-stripe-polo", "wind-shirt-purple-haze", "chg26-aw-p02", "green-1-4-zip-rebrand"],
  "A Midiron camo cap, a No Return Club golfer with his bag, and a Cph/Golf jacket"),
 ("details", "Design You Only Notice by Using It", "Tee pockets, marker magnets and pencil holders",
  [f"One of our favorite posts of the year was {L('hidden-details-golf-gear','Hidden Details')}: 18 pieces with features you only find once you are wearing them. Agronomy Workshop sews a tee holder into the chest pocket of its work shirt. Masterpiece Sports Club built a tee holder into a polo. Draw&rsquo;s corduroy cap has a small side pouch that holds a tee, and 3 Putt Round molded a tee holder into the back of a phone case. Manors even hides a magnet for your ball marker in a trouser pocket.",
   "None of it shows up in a product photo, which is exactly why it matters. It is the clearest sign that the people designing these clothes are out playing in them."],
  ["heavyweight-work-shirt-ss-earth", "pique-poly-golf-polo-ss-cream", "forest-green-unstructured-corduroy-cap", "the-tee-case"],
  "Close-ups of tees in a shirt pocket, a glove clipped to a cargo pocket, and engraved divot tools"),
]

WAVES = [
 ("Radmor", "brand-to-know-radmor", "A Seattle brand with no virgin polyester in the line, and knitwear in organic cotton, silk and merino that does not look like it is trying."),
 ("Golden Soul Golf", "brand-to-know-golden-soul-golf", "Leather headcovers handmade in Colombia, with blade, mallet and mid-mallet putter covers in dozens of designs."),
 ("Clamp Golf Company", "brand-to-know-clamp-golf-company", "One-off sets reworked from Carhartt, Nike and Patagonia in Yorkshire. Every reworked set we covered has since sold."),
 ("Local GC", "brand-to-know-local-gc", "Canvas and wool covers made to order in Orewa, New Zealand, with names like The Flusher and Dead Rats."),
 ("Midiron", "brand-to-know-midiron", "The Sydney label that does not sign its own work, and camo caps that sold out fast."),
 ("No Return Club", "brand-to-know-no-return-club", "Manchester golf built for the hero shot: Harris Tweed covers, bamboo tees and wind shirts in Purple Haze."),
 ("Parmore Golf", "brand-to-know-parmore-golf", "Started in England in 2024 with three words printed on half the range: No Membership Required. Streetwear that happens to be about golf."),
 ("BEAMS Golf", "brand-revisited-beams-golf", "Japan&rsquo;s first select-shop golf line and a fall run of collabs with Baracuta, Lacoste, Gramicci and more."),
]

CALLS = [
 ("Natural fibers go mainstream.", "Merino and organic cotton move from the quiet-luxury tier into mid-priced lines. Expect more brands to put the fabric, not the tech, in the product name."),
 ("Needlepoint moves off the belt.", "The belt peaked this year. Next come needlepoint bag straps, scorecard holders and headcovers as the main event."),
 ("Fewer collabs, but better ones.", "Logo-on-logo drops are wearing thin. The ones that last will be two makers building one specific thing together."),
 ("Wide legs stay; shorts follow.", "Pleated shorts with a longer inseam and a fuller leg are the next step from the trousers of 2026."),
 ("More one-offs.", "Remade and limited-run pieces sold out faster than anything else we covered, and our Gone Already post listed 35 of them. Brands will chase that."),
 ("Brown is the new black.", "Chocolate and sage settle in as golf&rsquo;s neutrals, with black saved for the evening."),
]

CALL_ALTS = ["A golfer in a blue cotton quarter-zip holding his driver against a clear sky", "A golfer holding a needlepoint American flag piece at his belt", "A golfer carrying a canvas carry bag across a fairway at sunset", "A man in shorts and a knit shirt leaning on a vintage car", "Hands guiding fabric through a sewing machine in a headcover workshop", "A golfer in chocolate brown pleated trousers standing in a wood-paneled room"]
CSS = ('<style>/*TGI-TRENDS*/.tr-sec{max-width:1180px;margin:0 auto;padding:56px 0 8px;border-top:1px solid rgba(20,20,20,.12)}'
 '.tr-band{margin:0 0 26px;aspect-ratio:2000/857;overflow:hidden}.tr-band img{width:100%;height:100%;object-fit:cover;display:block}'
 '.tr-head{max-width:760px;margin:0 auto 24px}.tr-head p{font-size:17px;line-height:1.65;margin:0 0 14px}'
 '.tr-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.tr-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr));max-width:900px;margin:0 auto}'
 '.tr-grid .product-name{font-size:15px}.tr-grid .product-body{padding:12px 12px 14px}'
 '.products-grid.tr-grid[data-n]{grid-template-columns:repeat(4,minmax(0,1fr))}.products-grid.tr-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}'
 '@media(max-width:900px){.products-grid.tr-grid[data-n],.products-grid.tr-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
 '.products-grid.tr-grid[data-n]{display:grid}.products-grid.tr-grid[data-n]>.product-card{flex:none;min-width:0}'
 '.tr-head .writeup-body a,.tr-wave p a{border-bottom:1px solid var(--grass,#2D4A2B)}'
 '@media(max-width:480px){.products-grid.tr-grid[data-n] .product-name{font-size:13px}.products-grid.tr-grid[data-n]{gap:10px}}'
 '@media(max-width:820px){.tr-head,.tr-waves,.tr-calls{padding-left:20px;padding-right:20px}}'
 '.tr-nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:18px auto 0;max-width:900px}.tr-nav a{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid rgba(20,20,20,.25);padding:4px 8px}'
 '.tr-waves{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;max-width:1000px;margin:24px auto 0}'
 '.tr-wave{border:1px solid rgba(20,20,20,.16);padding:16px 18px}.tr-wave a{font-size:17px;font-weight:500;border-bottom:1px solid var(--grass,#2D4A2B)}.tr-wave p{font-size:15px;line-height:1.55;margin:8px 0 0}'
 '.tr-calls{max-width:1100px;margin:24px auto 0;counter-reset:c;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 22px}.tr-call{border-top:1px solid rgba(20,20,20,.12);padding-top:12px}.tr-call-img{margin:0 0 12px;aspect-ratio:4/5;overflow:hidden}.tr-call-img img{width:100%;height:100%;object-fit:cover;display:block}.tr-call p{margin:0;font-size:16px;line-height:1.6}@media(max-width:820px){.tr-calls{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 14px}.tr-call p{font-size:14px}}'
 '.tr-call strong:before{counter-increment:c;content:counter(c,decimal-leading-zero) "  ";font-family:var(--mono,monospace);font-size:11px;opacity:.6}'
 '@media(max-width:700px){.tr-waves{grid-template-columns:1fr}}</style>\n')

def card(h, idx):
    brand, name, price, url = P[h]; fr = FR[h]
    label = H.unescape(f"{brand} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div><div class="product-name">{name} &middot; {price}</div><div class="product-desc">{DESCS[h]}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')

def body_html(n):
    nav = "".join(f'<a href="#{a}">{t}</a>' for a, t, *_ in TRENDS) + '<a href="#made-waves">Who Made Waves</a><a href="#2027">2027</a>'
    o = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We published more than 300 posts this year, nearly all of them about independent golf brands and what they make. Read back through them in order and the year has a shape. Trousers got wider. Fabric got more natural. The best accessories were made by hand, or remade from something older. Brands teamed up constantly, and the scene stopped being an American one.</p>
    <p>This is Part 1 of our look back at 2026, covering style and design. For each of the seven trends we saw, we explain where it showed up in our coverage, link the posts where we first noticed it, and pick three or four pieces that sum it up. Then come the brands that made waves this year, and six calls for 2027. Parts 2 and 3 will cover how golf gear is made and the courses that defined the year.</p>
    <p><strong>The short version.</strong> If one piece sums up golf style in 2026, it is a pair of chocolate-brown, double-pleated trousers in a natural fabric, worn with a hand-stitched belt.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Trends</span><span>7</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>{n}</span></div>
      <div class="sidebar-detail"><span class="l">Brands that made waves</span><span>{len(WAVES)}</span></div>
      <div class="sidebar-detail"><span class="l">Calls for 2027</span><span>{len(CALLS)}</span></div>
      <div class="sidebar-detail"><span class="l">Series</span><span>Part 1 of 3</span></div>
      <div class="hashtags"><span class="hashtag">#GolfStyle</span><span class="hashtag">#GolfTrends</span><span class="hashtag">#IndieGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<div class="tr-nav">{nav}</div>
"""
    i = 1
    for num, (a, title, kicker, paras, keys, alt) in enumerate(TRENDS, 1):
        cards = "".join(card(h, i + j) for j, h in enumerate(keys)); i += len(keys)
        ps = "".join(f"<p>{p}</p>" for p in paras)
        o += (f'\n<section class="products tr-sec">\n  <figure class="tr-band"><img src="{IMG}/band-{a}.jpg" alt="{H.escape(alt)}" loading="lazy" /></figure>\n'
              f'  <div class="tr-head"><div class="drop-tag grass">Trend {num:02d} of 07</div>\n  <h2 class="products-hdr" id="{a}">{title}</h2>\n'
              f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n  <div class="writeup-body">{ps}</div></div>\n'
              f'  <div class="products-grid tr-grid" data-n="{len(keys)}">{cards}</div>\n</section>\n')
    waves = "".join(f'<div class="tr-wave"><a href="/drops/{s}">{nm}</a><p>{t}</p></div>' for nm, s, t in WAVES)
    o += (f'\n<section class="products tr-sec">\n  <div class="tr-head"><div class="drop-tag grass">2026</div>\n  <h2 class="products-hdr" id="made-waves">Who Made Waves</h2>\n'
          f'  <div class="writeup-body"><p>Eight brands that shaped the year without getting the most airtime. Not the biggest, and not a ranking: these are the smaller names whose new drops we were most eager to see.</p></div></div>\n'
          f'  <div class="tr-waves">{waves}</div>\n</section>\n')
    calls = "".join(f'<div class="tr-call"><figure class="tr-call-img"><img src="{IMG}/call-{i}.jpg" alt="{H.escape(CALL_ALTS[i-1])}" loading="lazy" /></figure><p><strong>{h}</strong> {t}</p></div>' for i, (h, t) in enumerate(CALLS, 1))
    o += (f'\n<section class="products tr-sec">\n  <div class="tr-head"><div class="drop-tag grass">2027</div>\n  <h2 class="products-hdr" id="2027">What Comes Next: Six Calls for 2027</h2>\n'
          f'  <div class="writeup-body"><p>These are our guesses, based on what sold out this year and where the brands we follow seem to be heading. We will check back on them this time next year.</p></div></div>\n'
          f'  <div class="tr-calls">{calls}</div>\n</section>\n')
    o += f"""
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">How We Made This</div>
    <p>Every trend here comes from our own coverage this year, and each one links back to the posts where we first noticed it. Prices are as each store showed them to a US visitor on November 12, 2026. A.P.C., Local GC and BEAMS price in euros, New Zealand dollars and yen, so those dollar figures are approximate. Everything listed was in stock that day except where we say otherwise.</p>
    <p>Part 2 looks at how golf gear was made in 2026, from small club makers to the zero-torque putter fight. Part 3 covers the courses, from new builds in Texas to the comeback of the muni.</p>
  </div>
</section>
"""
    return o

def head_top(n):
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    keys = [h for t in TRENDS for h in t[4]]
    items = [{"@type": "ListItem", "position": i + 1, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")} for i, h in enumerate(keys)]
    blocks = [{"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
               "datePublished": "2026-11-12", "dateModified": "2026-11-12",
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
    keys = [h for t in TRENDS for h in t[4]]
    assert len(keys) == len(set(keys)) and all(h in P and FR.get(h) and h in DESCS for h in keys)
    n = len(keys)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = (f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  {BC}</div>\n\n'
            f'<header class="drop-header">\n  <h1>{H1}</h1>\n  <div class="drop-meta">\n    <span>The Year in Golf 2026 &middot; Part 1 of 3: Style &amp; Design</span><span class="dot"></span>\n'
            f'    <span>7 trends &middot; {n} picks &middot; checked November 12, 2026</span>\n  </div>\n</header>\n\n'
            f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a knit sweater and wide trousers finishing his swing beneath a stand of Scots pines" fetchpriority="high" /></div></div>\n')
    body += body_html(n)
    out = head_top(n) + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    print(f"  {n} picks, {len(TRENDS)} trends")
    if not apply_: return
    (ROOT / f"drops/{SLUG}.html").write_text(out, encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", out[:out.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if "18 Pieces With Tee Pockets" in above: bad.append("donor leak")
    txt = re.sub(r"<[^>]+>", " ", above)
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned " + w)
    for f in set(re.findall(r'src="(/images/[^"]+)"', out)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for s in set(re.findall(r'href="/drops/([^"#]+)"', above)):
        if not (ROOT / f"drops/{s}.html").is_file(): bad.append("deadlink " + s)
    if bad: sys.exit("! " + "; ".join(bad))
    print("  wrote", f"drops/{SLUG}.html")
if __name__ == "__main__": main("--apply" in sys.argv)
