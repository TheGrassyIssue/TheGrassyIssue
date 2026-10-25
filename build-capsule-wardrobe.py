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

FRN = json.loads((ROOT / "research/capsules/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
EXTRA_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
             '/*TGI-CAPSULE*/.swatches{display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin:6px 0 22px}.swatch{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase}.swatch i{display:inline-block;width:22px;height:22px;border-radius:50%;border:.5px solid var(--ink)}'
             '.looks{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:8px 0 34px}.looks figure{margin:0}.looks img{width:100%;aspect-ratio:4/5;object-fit:cover;border:.5px solid var(--ink);display:block;background:#e8e2d6}.looks figcaption{font-size:13px;line-height:1.5;margin-top:10px;text-align:center}.looks figcaption b{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:500;margin-bottom:4px}@media(max-width:900px){.looks{grid-template-columns:repeat(2,1fr)}}'
             '.capsule-toc{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:0 auto 10px;max-width:900px}.capsule-toc a{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;border:.5px solid var(--ink);padding:7px 12px}</style>\n')


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


INTRO = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The Idea</div>
    <p>A capsule wardrobe is a small set of pieces that all go together: about ten staples in one palette, so anything you pull out of the closet works with anything else. Nobody has to think at 6:40 a.m. before a muni tee time, and nobody has to buy a new outfit for the one round a year at a course with a dress code.</p>
    <p>Golf is a good fit for the idea because golf clothes repeat. You need a polo, something for your legs, a layer and a hat, and the only thing that changes is how dressed up the day is. So we built five capsules for five different tastes, each from the independent brands we cover. Each has ten or eleven pieces in a tight palette, and each comes with four outfits made only from those pieces: the muni round, the special-day course, dinner after, and a cold morning.</p>
    <p><strong>How we built them.</strong> Every capsule follows the same rules. Three neutrals and one accent colour. At least three tops, two bottoms and one real layer. One piece that dresses the whole thing up (a pleated trouser, a cashmere crew, a vest). One hat that goes with everything. And no piece that only works with one other piece.</p>
    <p>Every price and size was checked on the brands&rsquo; own stores on October 25, 2026. Prices from UK, Australian, Swedish and South African stores are converted to US dollars, with the original price shown. Some sizes are already thin, and we&rsquo;ve said so on the card.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Capsules</div>
      <div class="sidebar-detail"><span class="l">Capsules</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>52</span></div>
      <div class="sidebar-detail"><span class="l">Outfits</span><span>20</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>28 independents</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$25&ndash;$295</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 25, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#CapsuleWardrobe</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#TheEdit</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Build Your Own</div>
  <h2 class="products-hdr" id="build-your-own">How to Build a Golf Capsule Wardrobe</h2>
  <p class="cat-kicker">Start with the palette, not the pieces: pick three neutrals you already wear and one accent you like. Buy the bottoms first, because a good trouser and a good short carry more outfits than any shirt. Then add three tops that each work with both bottoms, one layer that goes over all three, and a hat in one of the neutrals. Leave the loud piece for last and make it the accent. If a new piece only goes with one thing you own, it isn&rsquo;t a capsule piece.</p>
</section>
"""
FAQ = [
 ("What is a golf capsule wardrobe?", "A small set of about ten golf clothes in one palette, usually three neutrals and one accent, where every top works with every bottom so you can dress for any round without thinking about it."),
 ("How many pieces should a golf capsule wardrobe have?", "About ten: three or four tops, two or three bottoms, one or two layers, a hat and socks. That gives you well over a dozen combinations."),
 ("What colours work best for a golf capsule wardrobe?", "Pick three neutrals, such as navy, cream and stone, or black, olive and grey, then one accent colour like forest green, cobalt or terracotta."),
 ("Can a capsule wardrobe work for a course with a dress code?", "Yes. Include one collared polo and one tailored trouser, such as a pleated or chino-cut pant, and the same capsule covers a muni round and a private course."),
 ("Which brands are in TGI's capsule wardrobes?", "Twenty-eight independent brands, including Criquet, Rookline, Woodgrain, Public Drip, Hidden Links Society, Odd Ritual, Sentinel, Late Nine, Metalwood, Read The Green, Sounder, Manors, Gramicci, Mount Tee, Howie Benson and Juniper & James."),
]


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for cap in CAPS:
        for k in [x for x in P if re.fullmatch(cap[0] + r"\d+", x)]:
            items.append({"@type": "ListItem", "position": pos, "url": P[k][3], "name": H.unescape(f"{P[k][0]} {P[k][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-25", "dateModified": "2026-10-25",
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


def capsule(i, cap, n0):
    key, name, anchor, sw, intro, brands, rng = cap
    ids = sorted([x for x in P if re.fullmatch(key + r"\d+", x)], key=lambda x: int(x[2:]))
    sws = "".join(f'<span class="swatch"><i style="background:{c}"></i>{lab}</span>' for lab, c in sw)
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    looks = "\n".join(
        f'  <figure><img src="{IMG}/look-{key}-{m}.jpg" alt="{H.escape(name_)} outfit from the {H.unescape(name)} capsule: {H.escape(cap_)}" loading="lazy" />'
        f'<figcaption><b>{H.escape(name_)}</b>{H.escape(cap_)}</figcaption></figure>'
        for m, (name_, _, cap_) in enumerate(LOOKS[key], 1))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Capsule {i} &middot; {len(ids)} pieces</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <div class="swatches">{sws}</div>\n'
            f'  <p class="cat-kicker"><strong>{brands} &middot; {rng}</strong>{intro}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n'
            f'  <h3 class="products-hdr" style="font-size:26px;margin-top:44px" id="{anchor}-outfits">Four Outfits From the {name}</h3>\n'
            f'  <div class="looks">\n{looks}\n  </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [x for c in CAPS for x in sorted([x for x in P if re.fullmatch(c[0] + r"\d+", x)], key=lambda x: int(x[2:]))]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), set(P) ^ set(ids)
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    for key, looks in LOOKS.items():
        for _, keys, _ in looks:
            assert all(x in P and x.startswith(key) for x in keys), keys
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    toc = "".join(f'<a href="#{c[2]}">{c[1]}</a>' for c in CAPS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Five capsules &middot; Twenty outfits</span><span class="dot"></span>
    <span>52 picks &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Five golf looks side by side, one from each capsule: tan pleated trousers in a wood-panelled clubroom, a slate waffle polo, a pleated short and knit polo, a merino crew on the course, and a waffle polo with a green cap" fetchpriority="high" /></div></div>
"""
    body += INTRO
    body += f'\n<div class="capsule-toc">{toc}</div>\n'
    n = 1
    for i, c in enumerate(CAPS, 1):
        o, n = capsule(i, c, n); body += o
    body += CLOSE
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", EXTRA_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards, {sum(len(v) for v in LOOKS.values())} looks")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
