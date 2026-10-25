#!/usr/bin/env python3
"""build-capsule-wardrobe.py — The Golf Capsule Wardrobe: five capsules, 50 pieces, 20 outfits. 25 October 2026. Cloned from build-publicdrip-revisit.py.
Lenny: "Post idea; capsule wardrobe – versatile, timeless and interchangeable staples in complementary colourways ... from a solid Muni round to special day course"
-> answered: 5 capsules for different tastes, pieces + outfit grid, brand index only -> "let's build this post".
FACTS: research/capsules/<capsule>.json, live store sweeps 25 Oct 2026 (USD; GBP 1.3375, AUD 0.7028, SEK 0.0955). Manors sizes are page-listed, stock not per-size confirmed.
Outfit boards from research/capsules/looks.py. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Golf Capsule Wardrobe: 5 Capsules, 52 Pieces, 20 Outfits"
DESC = ("Five golf capsule wardrobes from independent brands, ten or eleven interchangeable pieces each in one palette, with four outfits per capsule "
        "from a muni round to a special-day course. Prices checked October 25, 2026.")
H1 = "The Golf Capsule Wardrobe: Five Closets That Dress Themselves"
BC = "The Golf Capsule Wardrobe"
SLUG = "golf-capsule-wardrobe"
IMG = "/images/capsule-wardrobe"
# key: (brand, item, price, url, copy)
P = {
 # 1 Clubhouse Classic
 "cl1": ("Criquet", "Slim Fit Top-Shelf Range Polo, Navy", "$104", "https://criquetshirts.com/products/slim-fit-top-shelf-range-polo-navy-blue",
   "The anchor. Pima cotton with a touch of spandex, a slim fit and removable collar stays, designed in Austin and made in Peru. Navy goes with every other piece in this capsule."),
 "cl2": ("Criquet", "Performance Players Shirt, Golf Green", "$104", "https://criquetshirts.com/products/performance-players-shirt-golf-green",
   "The one accent. A tri-blend players shirt with stretch, a chest pocket and collar stays. Green against navy, tan and cream is as loud as this capsule gets."),
 "cl3": ("Casualist", "Weekend Pique Polo, Ecru", "$127 (&pound;95)", "https://casualist.com/products/weekend-pique-polo-ecru",
   "Organic cotton pique with raglan sleeves, a relaxed retro fit and an olive collar, made in Portugal. Casualist&rsquo;s line: &ldquo;The sort of polo your club captain would wear, if your club captain had better taste.&rdquo;"),
 "cl4": ("Rookline", "Ottoman Rib Cashmere Crew, Oatmeal", "$295", "https://rookline.com/products/ottoman-rib-cashmere-crew-oatmeal-heather",
   "The splurge. Pure cashmere with a saddle sleeve and an Ottoman rib at the elbow, cuff and hem. It sits over any polo here and takes you straight to dinner."),
 "cl5": ("Criquet", "Anytime Pants, Navy", "$148", "https://criquetshirts.com/products/anytime-pants-navy",
   "Cut like a chino, built like a performance pant, with stretch and a small embroidered C. The everyday trouser for rounds and the drive home."),
 "cl6": ("Woodgrain Golf", "Legacy Double Pleated Trouser, Tan", "$180", "https://woodgrain.golf/products/relaxed-double-pleated-trouser-tan",
   "Wide-leg, double-pleated, 100% cotton. The special-day trouser, and the piece that makes a navy polo look like it was planned."),
 "cl7": ("Olydoe", "The Walker Short, Navy", "$105", "https://olydoe.com/products/cotton-shorts",
   "A cotton, Tencel and linen blend with a wider leg and a matte texture Olydoe says holds up in humidity. For the eight months a year Austin wears shorts."),
 "cl8": ("Sounder", "Raglan Star Sweat, Dark Green", "$102 (was $156)", "https://soundergolf.com/en-us/products/raglan-star-sweat-dark-green",
   "Organic cotton, cut for a full swing, with a chenille star on the sleeve. Sounder&rsquo;s pitch: &ldquo;sometimes it&rsquo;s nice to layer up without breaking out the cashmere.&rdquo;"),
 "cl9": ("Sounder", "Logo Cap, Stone", "$55", "https://soundergolf.com/en-us/products/logo-cap-stone-copy",
   "A six-panel cotton cap with a small wordmark patch, restocked from Sounder&rsquo;s first collection. Stone works with all of it."),
 "cl10": ("Sounder", "Ivy Ellis Crew Sock, Cream", "$28", "https://soundergolf.com/en-us/products/ivy-ellis-x-sounder-lightweight-crew-sock-cream-with-green-trim",
   "A lightweight ribbed crew sock made with Ivy Ellis at a family-owned mill in the Scottish Highlands. The green trim ties back to the accent."),
 # 2 Muni Streetwear
 "st1": ("Public Drip", "Triborough Waffle Knit Polo, Dark Slate", "$110", "https://publicdrip.com/products/triborough-waffle-knit-polo-dark-slate",
   "A long-sleeve waffle-knit polo with four-way stretch and a spread collar. The one collared shirt this capsule needs."),
 "st2": ("Hidden Links Society", "The Society Tee, Light Grey", "$43", "https://hiddenlinkssociety.com/products/the-society-tee-light-grey",
   "A 230gsm garment-washed cotton tee with drop shoulders and a tonal patch. Its own copy: &ldquo;No loud graphics. No tech-fabric shine.&rdquo;"),
 "st3": ("Hidden Links Society", "The Society Long Sleeve Tee, Vintage Brown", "$62", "https://hiddenlinkssociety.com/products/the-society-long-sleeve-tee-vintage-brown",
   "Heavy 310gsm cotton with the Running Man on the front and back, and the warm accent in a capsule of greys. Made to order; allow two weeks."),
 "st4": ("Public Drip", "Anywhere Pleated Pants, Olive", "$170", "https://publicdrip.com/products/anywhere-pleated-pants",
   "Double-pleated stretch nylon modeled on a suit pant, with an elastic waist and side zip pockets. The trouser that takes this capsule to a special-day course."),
 "st5": ("water when dry", "Utility Pants, Black", "$108", "https://waterwhendry.com/products/black-utility-pants",
   "Crinkle nylon with two zip cargo pockets and toggle hems, from the fall/winter drop. Black goes under everything else here."),
 "st6": ("Public Drip", "Anywhere Tech Short, Olive", "$90", "https://publicdrip.com/products/anywhere-tech-short-olive",
   "Stretch nylon with a flat drawstring waist and belt loops, about a 6-inch inseam. Low stock: 28 and 32 only."),
 "st7": ("Malbon Golf", "Performance Raglan Quarter Zip, Dark Slate", "$148", "https://malbon.com/products/performance-raglan-quarter-zip-dark-slate",
   "A nylon and spandex mid layer with raglan sleeves and mesh side panels. Slate matches the waffle polo. XS to M left."),
 "st8": ("water when dry", "Canopy Zip Hoodie, Charcoal", "$68 (was $98)", "https://waterwhendry.com/products/black-zip-up-hoodie",
   "A 380gsm garment-dyed, stone-washed cotton zip hoodie with metal hardware. The after-round layer."),
 "st9": ("Hidden Links Society", "Hidden Links Soc. Hat, Olive", "$32", "https://hiddenlinkssociety.com/products/hidden-links-soc-hat-olive",
   "A lightweight cotton cap with 3D embroidery on the front and a snapback. Olive picks up the pleated pants and the short, and it&rsquo;s the cheapest piece in the capsule."),
 "st10": ("Malbon Golf", "Performance Tech Bucket Hat, Black", "$68", "https://malbon.com/products/performance-tech-bucket-hat-black",
   "An unstructured performance bucket with perforated panels and a bungee at the back. For cold mornings and hot afternoons."),
 "st11": ("Odd Ritual", "Classic Polo, Black", "$31 (R550, was R850)", "https://oddritualgolf.com/products/odd-ritual-classic-polo-black",
   "A lightweight performance polo with a modern collar, the wordmark on the chest and a crest on the back, from Cape Town. Ships to the US."),
 # 3 Tour '97
 "to1": ("Late Nine", "Ribbed Jersey Polo Long Sleeve, Brown Melange", "$191 (SEK 2,000)", "https://late-nine.com/products/ribbed-jersey-polo-long-sleeve-brown-melange",
   "A hefty cotton melange polo with a contrast-stripe ribbed collar, from the Stockholm label that Late Nine says is &ldquo;based on the iconic jersey golf polos of the late 90&rsquo;s and early &rsquo;00s.&rdquo;"),
 "to2": ("Devereux Golf", "Camelback Polo, Brown / White Stripe", "$68", "https://devereuxgolf.com/products/camelback-polo-brown-white-stripe",
   "A brushed pique stripe with a contrast ribbed collar, from the Scottsdale brothers. The cheapest polo in this capsule, and the most nineties."),
 "to3": ("Ashworth Golf Company", "2Bar Solid Polo, Core Red", "$89", "https://www.ashworth-golf.com/products/2bar-solid-polo-core-red",
   "A Pima cotton and performance blend from the relaunched 1987 California brand. A faded red straight out of the late nineties."),
 "to4": ("Metalwood Studio", "Pleated Western Track Pant, Brown", "$168", "https://metalwood.studio/products/pleated-western-track-pant-brown",
   "A straight leg with a permanent pleat and a drawstring waist. Metalwood calls it &ldquo;arguably the most comfortable pants ever made,&rdquo; and it works with every top here."),
 "to5": ("Late Nine", "Double Pleat Shorts, Beige", "$239 (SEK 2,500)", "https://late-nine.com/products/double-pleat-shorts-beige",
   "A double-pleated Bermuda in lightweight cotton twill with slanted side pockets. EU sizing, 48 to 54."),
 "to6": ("Read The Green", "The '97 Vintage Pullover, Navy", "$100", "https://readthegreen.com/products/the-97-vintage-pullover-navy",
   "The nylon pullover that went viral, with rib-knit cuffs and collar and &ldquo;Read The Green Golf Club 1997&rdquo; on the chest."),
 "to7": ("Late Nine", "Cable Knit Polo, Light Blue", "$282 (SEK 2,950)", "https://late-nine.com/products/cable-knit-polo-light-blue",
   "A lightly brushed cable knit in fine merino with an oversized seventies collar and mother-of-pearl buttons. The accent colour, and the piece to wear to dinner. S and M only."),
 "to8": ("Ashworth Golf Company", "Tech Stretch Vest, Bone", "$145", "https://www.ashworth-golf.com/products/tech-stretch-vest-bone",
   "A four-way-stretch full-zip vest, wind and water resistant, with the Golfman on the chest. Over a polo, it&rsquo;s the whole era in one layer."),
 "to9": ("Read The Green", "Founder's Cap, Sky", "$45", "https://readthegreen.com/products/founders-cap-sky-blue",
   "A cotton five-panel with a sky blue brim, the accent colour again."),
 "to10": ("Metalwood Studio", "Carlsbad Dad Hat, Tan", "$48", "https://metalwood.studio/products/carlsbad-dad-hat-tan",
   "A nylon mid-crown dad hat with the Metalwood wordmark. Tan goes with the shorts."),
 # 4 Outdoor Technical
 "ou1": ("Macade", "Bridge Merino Quarter Zip, Black", "$195", "https://macadegolf.com/products/bridge-black-mernio-quarter-zip",
   "A lightweight merino and cashmere quarter-zip with a tailored fit, from the Stockholm brand built for cold, wet rounds. The base layer."),
 "ou2": ("Manors Golf", "Merino Tech Crewneck, Dune", "$241", "https://manorsgolf.com/products/merino-wool-crewneck",
   "A 9-gauge merino crew with ripstop elbow patches. Manors&rsquo; line: &ldquo;Smart enough for the clubhouse, tough enough to live in your bag.&rdquo;"),
 "ou3": ("Sounder", "Clean Lie Polo, Smokey Olive", "$103", "https://soundergolf.com/en-us/products/clean-lie-polo-smokey-olive",
   "Organic cotton jersey with a ribbed hem and only a star tab for branding. Sounder: &ldquo;you never saw Arnie or Jack with a massive logo on their chest.&rdquo;"),
 "ou4": ("Galvin Green", "Marty TOUR Polo, Royal Blue", "$99", "https://www.galvingreen.com/products/marty-tour-breathable-short-sleeve-golf-shirt-royal-blue",
   "Galvin Green&rsquo;s breathable tour polo with stretch through the shoulders and UV protection. The cobalt accent."),
 "ou5": ("Manors Golf", "Ripstop Tech Trouser, Dune", "$201", "https://manorsgolf.com/products/ripstop-tech-trouser",
   "Recycled Toray stretch ripstop with a PFC-free water-repellent finish, a gusseted seat and scorecard pockets. Sizes as listed on the page."),
 "ou6": ("Gramicci", "Nylon Gramicci Pant, Carbon", "$110", "https://gramicci.com/products/nylon-gramicci-pant",
   "The climbing pant in recycled, water-repellent nylon with a colour-matched elastic waist. Also in burnt olive, black and stone."),
 "ou7": ("Gramicci", "Thermal Fleece Pullover, Black", "$130", "https://gramicci.com/products/thermal-fleece-pullover",
   "Low-profile recycled thermal fleece with a stand collar and drawcord hem. Gramicci says it keeps you warm &ldquo;without making you feel like a puffed-up marshmallow.&rdquo;"),
 "ou8": ("Macade", "Course Shell Jacket, Charcoal", "$210", "https://macadegolf.com/products/charcoal-course-shell-jacket",
   "A light, wind-resistant shell with contrast piping and zip pockets. Wind-resistant, not waterproof, so it goes over the merino rather than into a storm."),
 "ou9": ("SLOAT", "Organic Cotton Five Panel Hat, Oil Green", "$65", "https://sloat.cc/products/organic-cotton-five-panel-hat",
   "Organic cotton, made in the USA, with a leather strap that develops a patina. The San Francisco brand&rsquo;s take on a classic cap."),
 "ou10": ("Sounder", "Long Marl Sock, Olive", "$25", "https://soundergolf.com/en-us/products/long-marl-sock-olive",
   "A cushioned olive and grey marl sock, made in Portugal. Cotton rather than wool, and only US 7&ndash;9 is left."),
 "ou11": ("Sentinel Golf", "Basecamp Walker, Charcoal ULTRA", "$890", "https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-rsxwj-ykzhj-z89wk-5smxj",
   "The bag. A 2 lb carry bag in Challenge Sailcloth ULTRA with a stretch Dyneema interior pocket and a waterproof zip, made in the USA. Made to order, shipping in 8&ndash;10 weeks. The splurge, and the piece the rest of this capsule is built to walk with."),
 # 5 Coastal Resort
 "co1": ("Howie Benson", "Resort Camp Collar Polo, Off-White", "$108", "https://howiebenson.com/products/resort-camp-collar-polo-off-white",
   "A textured stretch knit with a camp collar and a relaxed fit. Howie Benson calls it &ldquo;a resort shirt made to play 18.&rdquo; Runs large."),
 "co2": ("Mount Tee Golf", "Parklands Waffle Polo, Eucalyptus Stripe", "$77 (A$110)", "https://mountteegolf.com.au/products/parklands-waffle-polo-eucalyptus-stripe",
   "A 220gsm waffle in sage with a brown vine stripe and a heavier collar, from three friends in Melbourne. Relaxed, oversized fit."),
 "co3": ("Juniper &amp; James", "Comfort Polo, Sea Foam / Slate", "$99", "https://juniperjamesgolf.com/products/comfort-polo-sea-storm-slate",
   "Micro modal with mother-of-pearl buttons and a spread collar with built-in stays, from New Braunfels. Built for Hill Country heat."),
 "co4": ("AXXA", "Golfer Knit, Cream", "$112 (A$159)", "https://www.axxa.com.au/products/golfer-knit",
   "A 730g heavyweight cotton crew with a jacquard golfer, from Sydney&rsquo;s Northern Beaches. For when the sea breeze turns."),
 "co5": ("Left of Field Golf", "Elements Weather Jacket, Sand / Moss", "$210 (A$299)", "https://lofgolf.com/products/xelements-weather-jacket-sand-moss",
   "A windproof, water-repellent shell with an insulated front panel and hidden pockets. Its tagline: &ldquo;Built for when the forecast turns.&rdquo;"),
 "co6": ("Mount Tee Golf", "Peninsula Pleated Shorts, Tan", "$70 (A$100)", "https://mountteegolf.com.au/products/pleated-shorts",
   "Double front pleats, a partial stretch waist and eyelets at the back right hip that hold your tees."),
 "co7": ("Birds of Condor", "Good Weather Walkshort, Rust", "$63 (A$90)", "https://birdsofcondor.com/products/brown-good-weather-golf-walk-short",
   "Recycled stretch nylon with felt-lined pockets and a velcro back pocket with a key loop. The terracotta accent, from Byron Bay."),
 "co8": ("Left of Field Golf", "Pleated Lite Pant, Beige", "$158 (A$225)", "https://lofgolf.com/products/pleated-lite-pant-beige",
   "Lightweight stretch nylon with a pleated front and a wider leg. Left of Field says it&rsquo;s sharp enough to wear straight off the course."),
 "co9": ("Howie Benson", "Five-Panel Patch Hat, White", "$50", "https://howiebenson.com/products/five-panel-patch-hat-white",
   "A moisture-wicking five-panel with a rubber oval patch, made for humid days."),
 "co10": ("AXXA", "Golf Bag Cap, Espresso", "$41 (A$59)", "https://www.axxa.com.au/products/expresso-golf-bag-cap",
   "A cream canvas crown with a brown corduroy brim and an embroidered golf bag. The cap that goes from the first tee to the pub."),
}
CAPS = [
 ("cl", "The Clubhouse Classic", "clubhouse", [("Navy", "#1f2a44"), ("Cream", "#efe8d6"), ("Stone", "#c9bca0"), ("Forest green", "#2f5a3c")],
  "Quiet, timeless and never wrong. Navy, cream and stone do the work, and forest green is the only colour that speaks up. Every top goes with every bottom, and the cashmere goes over all of it.",
  "Criquet, Casualist, Rookline, Woodgrain, Olydoe, Sounder", "$28&ndash;$295"),
 ("st", "The Muni Streetwear", "streetwear", [("Black", "#161616"), ("Olive", "#6b6b45"), ("Slate", "#4a5560"), ("Brown", "#7a5b45")],
  "For golfers who dress like they skate. Black, washed olive and slate grey, with one warm brown. Heavy cotton, stretch nylon and a five-panel, and nothing you&rsquo;d have to change out of to get a taco after.",
  "Public Drip, Hidden Links Society, water when dry, Malbon, Odd Ritual", "$31&ndash;$170"),
 ("to", "The Tour &rsquo;97", "tour97", [("Cream", "#ece2c8"), ("Chocolate", "#4b3326"), ("Faded red", "#b2322d"), ("Sky blue", "#a9c6dc")],
  "Late-nineties tour golf: pleats, piped collars, a nylon pullover and a vest over a polo. Cream and chocolate are the base, faded red and sky blue the accents. Three tops, one trouser, one short, and everything matches the brown pants.",
  "Late Nine, Metalwood, Read The Green, Ashworth, Devereux", "$45&ndash;$282"),
 ("ou", "The Outdoor Technical", "outdoor", [("Charcoal", "#33363a"), ("Sage", "#8c9273"), ("Sand", "#cfc2a5"), ("Cobalt", "#1f5fbf")],
  "For walkers and anyone who plays when the forecast says not to. Merino next to the skin, ripstop and climbing nylon on the legs, fleece and a shell on top, and one cobalt polo for the day it clears up.",
  "Macade, Manors, Sounder, Galvin Green, Gramicci, SLOAT, Sentinel", "$25&ndash;$890"),
 ("co", "The Coastal Resort", "coastal", [("Off-white", "#f1ece0"), ("Sand", "#d6c4a0"), ("Sea foam", "#a9cbb7"), ("Terracotta", "#b5653c")],
  "Warm-weather and travel golf. Off-white, sand and sea foam, with a terracotta short as the accent. Camp collars, waffle knits and pleated shorts that fold into a carry-on and still look right at the resort bar.",
  "Howie Benson, Mount Tee, Juniper &amp; James, AXXA, Left of Field, Birds of Condor", "$41&ndash;$210"),
]
N = 52
LOOKS = json.loads((ROOT / "research/capsules/looks.json").read_text())
