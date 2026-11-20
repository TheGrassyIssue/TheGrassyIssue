#!/usr/bin/env python3
"""build-not-golf-first.py — Not Golf First: Brain Dead, Stone Island and Only NY. Cloned from build-fresh-three-2.py. 19 November 2026.
Lenny: "a post about three fashion brands that arent golf first but have the design, quality and style that makes them some of the first brands
I want to reach for when shopping" -> Brain Dead, Stone Island, Kith or Only NY; options sheet v1 (47); "no on 31, avoid button downs. Tees,
sweaters, hoodies, polos, pants"; "let's go with OnlyNY over Kith"; v2 sheet (51); "build it" -> all 51 from the v2 sheet.
FACTS: Brain Dead — founded 2014 by Kyle Ng (LA) and Ed Davis (Melbourne), who met online; Ng's quote to Complex. Stone Island — Moncler Group
history page (Massimo Osti, Tela Stella 1982, seven jackets, Carlo Rivetti 1983, Ghost 2011, Moncler 2021, Ravarino HQ) and Moncler brand page
(60,000+ dye formulas). Only NY — its About page (founded 2007, city/outdoors/arts, city licenses) plus NYC Tourism/Hypebeast (Micah Belamarich
and Julian Goldstein; LES flagship; city partner). Product facts from each product page. US prices: Brain Dead/Only NY USD Shopify JSON;
Stone Island US category pages (stoneisland.com/en-us). No FAQ. Not added to the golf brand index (not golf brands).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Not Golf First: Brain Dead, Stone Island and Only NY"
DESC = ("Three fashion brands we reach for before most golf brands: Brain Dead, Stone Island and Only NY. "
        "51 polos, tees, sweaters, hoodies and pants that work on the course and off, with prices.")
H1 = "Not Golf First: Brain Dead, Stone Island and Only NY"
BC = "Brain Dead, Stone Island, Only NY"
SLUG = "not-golf-first-brain-dead-stone-island-only-ny"
IMG = "/images/not-golf-first"
SHOP = ""
BD, SI, ON = "Brain Dead", "Stone Island", "Only NY"
BDU, ONU = "https://wearebraindead.com/products/", "https://onlyny.com/products/"
SIK = "https://www.stoneisland.com/en-us/collection/knitwear/"
SIP = "https://www.stoneisland.com/en-us/collection/polos-and-t-shirts"
def _o(a, b): return f'{a} <span style="opacity:.6">({b})</span>'
P = {
 # Brain Dead — polos & tees
 "pique-thermal-polo-shirt-washed-black": (BD, "Pique Thermal Polo, Washed Black", "$175", BDU+"pique-thermal-polo-shirt-washed-black",
   "Our pick from Brain Dead. Garment-dyed cotton pique thermal with a slubby texture and a boxy, structured fit. Washed black hides a long day and still looks right at dinner."),
 "brain-dead-x-a-p-c-striped-pique-polo-navy": (BD, "Brain Dead &times; A.P.C. Striped Pique Polo", "$220", BDU+"brain-dead-x-a-p-c-striped-pique-polo-navy",
   "A long-sleeve navy-and-cream stripe made with A.P.C., with silver snap buttons and saddle yokes across the shoulders. The cold-morning polo."),
 "pigment-dye-long-sleeve-polo-sweater-green": (BD, "Pigment Dye Long Sleeve Polo Sweater", "$112.50", BDU+"pigment-dye-long-sleeve-polo-sweater-green",
   "A light knit in soft pigment-dyed Pima cotton with a chest pocket. Green on green, made for a fall nine."),
 "stripe-dye-pique-t-shirt-brown": (BD, "Stripe Dye Pique T-Shirt", "$115", BDU+"stripe-dye-pique-t-shirt-brown",
   "Garment-dyed pique, hand dyed in horizontal tie-dye stripes, so no two are the same. Bound collar, railroad stitching, 3D logohead at the hem."),
 "pigment-pique-t-shirt-natural": (BD, "Pigment Pique T-Shirt, Natural", "$95", BDU+"pigment-pique-t-shirt-natural",
   "The same boxy pique tee in plain natural. Breathable, broken in from the first wear, and the closest thing to a polo without a collar."),
 "easy-t-shirt-cement": (BD, "Easy T-Shirt, Cement", "$75", BDU+"easy-t-shirt-cement",
   "Garment-dyed, peached cotton jersey washed for a lived-in feel, with a tonal embroidered logohead. The everyday tee."),
 "long-sleeve-hitting-shirt-dusk-green": (BD, "Long Sleeve Hitting Shirt", "$185", BDU+"long-sleeve-hitting-shirt-dusk-green",
   "Lightweight nylon ripstop with a two-way zip, mesh side vents and a zip chest pocket. Built for the batting cage; works on the range."),
 "broken-stripe-rugby-shirt-natural": (BD, "Broken Stripe Rugby Shirt", "$225", BDU+"broken-stripe-rugby-shirt-natural",
   "A long-sleeve rugby polo in slubby cotton pique, printed with wavy, washed-out stripes. Snap buttons, saddle shoulders."),
 # Brain Dead — sweaters
 "boxy-striped-knit-sweater-eggplant": (BD, "Boxy Striped Knit Sweater", "$295", BDU+"boxy-striped-knit-sweater-eggplant",
   "Oversized brushed alpaca in eggplant, green and blue stripes with yellow ribbing. The loudest sweater in the bag, in the best way."),
 "curved-zip-sweater-brown": (BD, "Curved Zip Sweater", "$250", BDU+"curved-zip-sweater-brown",
   "An asymmetric two-way zip, wide diagonal stripes, raglan sleeves and hand pockets. A full-zip with a point of view."),
 "wool-commuter-sweater-marled": (BD, "Wool Commuter Sweater", "$395", BDU+"wool-commuter-sweater-marled",
   "Marled merino quarter-zip with a chest pocket and three cycling pockets on the back. Room for balls, tees and a scorecard."),
 "waffle-pullover-sweater-charcoal": (BD, "Waffle Pullover Sweater", "$137.50", BDU+"waffle-pullover-sweater-charcoal",
   "A lightweight marled knit with a collar, a short button front, two pockets and a metal logohead on the lapel."),
 "brooks-brothers-california-pullover-sweater-charcoal": (BD, "Brooks Brothers California Pullover Sweater", "$375", BDU+"brooks-brothers-california-pullover-sweater-charcoal",
   "A fuzzy knit polo sweater from the Brooks Brothers California collab, with patch pockets and a metal logohead charm on the lapel."),
 "brooks-brothers-california-alpaca-cycling-jersey-brown": (BD, "Brooks Brothers California Cycling Jersey", "$375", BDU+"brooks-brothers-california-alpaca-cycling-jersey-brown",
   "A merino half-zip modeled on vintage wool cycling jerseys, with flocked Brooks Brothers lettering and striped ribbing. The best piece in the collab."),
 # Brain Dead — hoodies
 "reversed-terry-button-hoodie-olive": (BD, "Reversed Terry Button Hoodie", "$285", BDU+"reversed-terry-button-hoodie-olive",
   "Reversed French terry, garment dyed and heavily washed, with a high mock neck, real horn buttons and curved patch pockets."),
 "streak-dyed-hoodie-navy": (BD, "Streak Dyed Hoodie", "$285", BDU+"streak-dyed-hoodie-navy",
   "Heavyweight French terry with a hand-applied bleach streak, so each one is different. Tonal logohead on the chest."),
 "padded-elbow-zip-up-hoodie-sand": (BD, "Padded Elbow Zip-Up Hoodie", "$125", BDU+"padded-elbow-zip-up-hoodie-sand",
   "Light vintage-wash terry with padded elbows, a two-way zip and an oversized hood. Easy to swing in, easy to stuff in the bag."),
 # Brain Dead — pants
 "type-02-washed-canvas-pant-natural": (BD, "Type 02 Washed Canvas Pant", "$275", BDU+"type-02-washed-canvas-pant-natural",
   "A high-rise, wide-leg carpenter pant in washed canvas with double knees and a button fly. Natural canvas for a cream-and-green round."),
 "washed-ripstop-climber-pant-brown": (BD, "Washed Ripstop Climber Pant", "$187.50", BDU+"washed-ripstop-climber-pant-brown",
   "A baggy climber pant with Brain Dead belt webbing built in. No belt, no fuss, plenty of room to turn."),
 "brooks-brothers-california-climber-trouser-charcoal": (BD, "Brooks Brothers California Climber Trouser", "$395", BDU+"brooks-brothers-california-climber-trouser-charcoal",
   "Japanese recycled wool-blend flannel, pleated, with a jacquard belt and quick-release buckle built in. A climbing pant cut like a trouser."),
 "brooks-brothers-california-pleated-corduroy-trouser-midnight-blue": (BD, "Brooks Brothers California Pleated Corduroy Trouser", "$175", BDU+"brooks-brothers-california-pleated-corduroy-trouser-midnight-blue",
   "Midnight-blue corduroy with exaggerated pleats and the Brooks Brothers California logohead embroidered on the leg."),
 "type-00-hickory-stripe-denim-pant-green": (BD, "Type 00 Hickory Stripe Denim Pant", "$295", BDU+"type-00-hickory-stripe-denim-pant-green",
   "Wide-leg hickory stripe denim in green with scalloped front pockets and silver rivets. The workwear pant for the nineteenth hole."),
 # Stone Island
 "L2S152200002S0039V002E": (SI, "Organic Cotton Pique Polo, Slate Blue", "$285", SIP,
   "Our pick from Stone Island. A short-sleeve pique polo in slate blue with a small archival logo on the chest. It looks like a golf shirt."),
 "L2S152200004S00G9V0065": (SI, "Stellina Pique Polo, Charcoal Grey", "$285", SIP,
   "From the Stellina line, a pique polo in charcoal with a snap placket. Quiet, boxy and easy to wear all day."),
 "L2S152200005S0F11V0020": (SI, "Ghost Long-Sleeve Polo, Navy", "$465", SIP,
   "From Ghost, the line where the badge matches the garment. A long-sleeve polo in navy jersey crepe, tonal head to toe."),
 "L2S152100030S0500V005R": (SI, "Combed Organic Cotton Tee, Cactus", "$220", SIP,
   "A combed organic cotton tee in cactus green. Under a sweater on cold mornings, on its own by the back nine."),
 "L2S155100154S00D8V0093": (SI, "Ribbed Organic Cotton Crewneck, Ivory", "$550", SIK+"regular-fit-crewneck-sweater-5100154-ribbed-soft-organic-cotton-L2S155100154S00D8V0093.html",
   "Soft ribbed organic cotton in ivory with the compass badge on the sleeve. The cream sweater every golf brand tries to make."),
 "L2S155100124S00D8V0049": (SI, "Ribbed Organic Cotton Half-Zip, Ash Gray", "$575", SIK+"regular-fit-half-zipper-sweater-5100124-ribbed-soft-organic-cotton-L2S155100124S00D8V0049.html",
   "The same rib as a half-zip in ash gray. Also navy and black. The most golf-ready piece in the Stone Island line."),
 "L2S155100058S00HCV002A": (SI, "Casentino-Effect Wool Nylon Crewneck, Navy", "$575", SIK+"loose-fit-crewneck-sweater-5100058-casentino-effect-wool-nylon-L2S155100058S00HCV002A.html",
   "A loose crew in wool and nylon finished to look like Casentino cloth, the brushed Tuscan wool. Navy or pearl gray."),
 "L2S155100052S00C2V005G": (SI, "Full-Rib Wool Turtleneck, Military Green", "$625", SIK+"regular-fit-turtleneck-sweater-with-fine-ribbed-trims-5100052-full-rib-rws-wool-L2S155100052S00C2V005G.html",
   "Full-rib RWS wool in military green with fine-ribbed trims. For the round where the frost delay never quite lifts."),
 "L2S155100028S00GDV0M6D": (SI, "Stellina Brushed Wool Crewneck, Storm Gray", "$655", SIK+"loose-fit-crewneck-sweater-with-contrast-trims-5100028-brushed-wool_s.i.-stellina-L2S155100028S00GDV0M6D.html",
   "Brushed wool from the Stellina line in storm gray, with contrast trims. Loose, soft and very easy to wear."),
 "L2S155100047S00A3V0M60": (SI, "Lambswool Zip Sweater, Gray Melange", "$755", SIK+"regular-fit-zip-up-sweater-with-button-placket-5100047-lambswool-L2S155100047S00A3V0M60.html",
   "A lambswool zip-up with a button placket over the zip. Also navy, black and sand. The splurge, and the one that will last the longest."),
 # Only NY — sweaters & polos
 "sron1500": (ON, "Speckled Knit Polo Sweater", "$148", ONU+"sron1500",
   "Our pick from Only NY. A rib-knit polo sweater with a multicolor nep speckle and faux mother-of-pearl buttons. The golf sweater Only NY didn&rsquo;t call a golf sweater."),
 "sron1499": (ON, "Brook Trout Crewneck Sweater", "$168", ONU+"sron1499",
   "Cream cotton with an intarsia brook trout across the chest. For the golfer who also owns a fly rod."),
 "nyc-parks-rec-sweater": (ON, "NYC Parks &amp; Rec Varsity Sweater", "$168", ONU+"nyc-parks-rec-sweater",
   "A cotton V-neck with an intarsia NYC Parks &amp; Rec graphic and striped trim. Licensed by the city; proceeds go back to it."),
 "srsd1254": (ON, "Only NY &times; J. Press NY Crewneck Sweater", "$99", ONU+"srsd1254",
   "Chunky 5-gauge navy cotton with an intarsia NY, made with J. Press, the old Ivy League tailor. Under $100."),
 "sron1498": (ON, "Hero Crewneck Sweater", "$168", ONU+"sron1498",
   "Navy cotton with an intarsia hero sandwich on the chest. The halfway-house order, knitted."),
 "track-field-sweater": (ON, "Track &amp; Field Crewneck Sweater", "$64", ONU+"track-field-sweater",
   "Navy cotton with an intarsia runner breaking the tape on the front and back. Fully fashioned."),
 "retriever-sweater": (ON, "Retriever Crewneck Sweater", "$53", ONU+"retriever-sweater",
   "A red cotton crew with an intarsia retriever. The cheapest sweater here, and maybe the most fun."),
 # Only NY — tees & rugbies
 "long-island-golf-long-sleeve-t-shirt": (ON, "Long Island Golf Long Sleeve T-Shirt", "$32", ONU+"long-island-golf-long-sleeve-t-shirt",
   "The one golf piece in the line: a Long Island Golf &ldquo;2026 U.S. Classic&rdquo; graphic on midweight cotton. Made in Peru. $32."),
 "nyc-department-of-parks-vintage-ringer-t-shirt": (ON, "NYC Department of Parks Vintage Ringer T-Shirt", "$58", ONU+"nyc-department-of-parks-vintage-ringer-t-shirt",
   "A light jersey ringer with green trim and the City of New York Department of Parks seal. Licensed by the city."),
 "freshwater-fishes-pocket-t-shirt": (ON, "Freshwater Fishes Pocket T-Shirt", "$54", ONU+"freshwater-fishes-pocket-t-shirt",
   "A pocket tee with the freshwater fishes of New York State printed on the back. Made in Peru."),
 "only-ny-x-paragon-sports-equipment-servicing-pocket-t-shirt": (ON, "Only NY &times; Paragon Sports Pocket T-Shirt", "$58", ONU+"only-ny-x-paragon-sports-equipment-servicing-pocket-t-shirt",
   "Made with Paragon Sports, the Union Square sporting goods store, with an equipment-servicing graphic on the back."),
 "loon-rugby-stripe-shirt": (ON, "Loon Rugby Stripe Shirt", "$108", ONU+"loon-rugby-stripe-shirt",
   "A boxy brown cotton rugby with yarn-dyed green and gold stripes, a woven collar and an embroidered loon."),
 "only-ny-x-j-press-rugby-stripe-shirt": (ON, "Only NY &times; J. Press Rugby Stripe Shirt", "$195", ONU+"only-ny-x-j-press-rugby-stripe-shirt",
   "Heavyweight cotton jersey in navy with an orange chest stripe and rubber buttons. Made in the USA. Runs large."),
 # Only NY — hoodies
 "premium-heavyweight-hoodie-1": (ON, "Premium Basics Hoodie", _o("$118", "some colors $148"), ONU+"premium-heavyweight-hoodie-1",
   "10&ndash;11oz brushed-back French terry, pigment dyed so each one comes out a little different. The plain hoodie done properly."),
 "nyc-parks-logo-hoodie": (ON, "NYC Parks Logo Hoodie", "$108", ONU+"nyc-parks-logo-hoodie",
   "The NYC Parks leaf logo on midweight fleece, in white, green, gray or black. Proceeds go back to the city."),
 "nyc-parks-rec-hoodie": (ON, "NYC Parks &amp; Rec Hoodie", "$108", ONU+"nyc-parks-rec-hoodie",
   "Gray fleece with an orange collegiate NYC Parks &amp; Rec graphic. Licensed by the city."),
 # Only NY — pants
 "bton1508": (ON, "Crosstown Carpenter Pants", "$128", ONU+"bton1508",
   "Heavyweight 12oz canvas, garment-dyed and enzyme-washed, with a hammer loop and utility pockets. In black."),
 "crosswind-active-pant": (ON, "Crosswind Active Pant", "$148", ONU+"crosswind-active-pant",
   "Nylon, cotton and spandex with an elastic bungee waist, pleats, knee darts and a zip pocket. The most golf-ready pant here."),
 "ny-senior-cord-sweatpants": (ON, "NY Senior Cord Sweatpants", "$104", ONU+"ny-senior-cord-sweatpants",
   "Fleece sweatpants printed with artwork by Caroline Mills: trout and walking figures. For the drive home."),
}
SECTIONS = [
 ("Brain Dead", "brain-dead", list(P)[:22],
  "<strong>Los Angeles &middot; 22 picks &middot; $75&ndash;$395</strong>Polos and tees, knits, hoodies and pants, plus pieces from the Brooks Brothers California collab and a polo made with A.P.C."),
 ("Stone Island", "stone-island", list(P)[22:32],
  "<strong>Ravarino, Italy &middot; ten picks &middot; $220&ndash;$755</strong>Polos and a tee, then the knitwear: ribbed cotton, wool and lambswool, from the main line, Ghost and Stellina. US prices from stoneisland.com."),
 ("Only NY", "only-ny", list(P)[32:],
  "<strong>New York City &middot; 19 picks &middot; $32&ndash;$195</strong>Intarsia sweaters, a knit polo, tees and rugbies, hoodies and pants, including the Long Island Golf long-sleeve and two J. Press pieces."),
]
N = 51
PQ = {
 "brain-dead": ("We decided to start a brand inspired by the stuff that we loved.", "Kyle Ng, Brain Dead co-founder, to Complex"),
 "stone-island": ("Stone Island was born from a fabric.", "Moncler Group, on Stone Island&rsquo;s history"),
 "only-ny": ("Driven by the city, outdoors, and arts.", "Only NY, on its About page"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "stone-island": ("Brain Dead, in the studio", "From Brain Dead&rsquo;s own photos.", [("band-1-1","A man playing guitar in the Brain Dead x A.P.C. striped polo","A.P.C. polo"),("band-1-2","A man in the natural Brain Dead pique tee in a studio full of monitors","Pique tee"),("band-1-3","A man in the Brooks Brothers California cycling jersey at night","Cycling jersey")]),
 "only-ny": ("Stone Island, the knitwear", "From Stone Island&rsquo;s own photos.", [("band-2-1","A man in the Stone Island navy Casentino-effect crewneck","Casentino crew"),("band-2-2","A man in the Stone Island ivory ribbed cotton crewneck","Ribbed crew"),("band-2-3","A man in the Stone Island slate blue pique polo","Pique polo")]),
 "end": ("Only NY, around the city", "From Only NY&rsquo;s own photos.", [("band-3-1","A man on a bike in the Only NY speckled knit polo sweater","Polo sweater"),("band-3-2","A man in the Only NY brook trout sweater outside a cabin","Brook Trout"),("band-3-3","A man holding a basketball in the Only NY x Paragon tee","Paragon tee")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most of what we cover here starts on the golf course. These three don&rsquo;t. Brain Dead, Stone Island and Only NY are fashion brands first, and none of them is a golf brand. They are still the first places we look when we want something new to wear, on the course or anywhere else, because the design is better, the fabrics are better and the clothes have a point of view.</p>
    <p>We kept it to what you can actually play in: polos, tees, sweaters, hoodies and pants. No button-downs, no jackets, no hats. Fifty-one pieces, all men&rsquo;s, all in stock when we checked.</p>
    <p><strong>Brain Dead</strong> was started in 2014 by Kyle Ng in Los Angeles and Ed Davis, a graphic designer in Melbourne. The two met online and still work mostly online. It began with graphics drawn from post-punk, comics and skate culture and has grown into one of the best-made labels in streetwear: garment-dyed pique, hand-dyed stripes, alpaca knits and wide-leg pants, plus collaborations that range from A.P.C. to Brooks Brothers.</p>
    <p><strong>Stone Island</strong> was founded in 1982 by Massimo Osti in Ravarino, near Modena, around a single fabric: Tela Stella, a heavy, washed military canvas he used for a first capsule of seven jackets. Carlo Rivetti joined a year later and led the brand for decades. It is known for material research and dyeing, with more than 60,000 dye formulas, and for the compass badge on the left sleeve. Ghost, the line where the badge matches the garment, arrived in 2011. Stone Island has been part of the Moncler Group since 2021.</p>
    <p><strong>Only NY</strong> was founded in New York in 2007 by Micah Belamarich and Julian Goldstein. It describes itself as an independent brand driven by the city, the outdoors and the arts, and it holds official licenses with the City of New York, NYC Parks and the MTA. Its knitwear is the reason it is here: intarsia trout, retrievers and hero sandwiches, and a speckled polo sweater that would look right on any first tee. It also made a Long Island Golf long-sleeve this year.</p>
    <h2 class="products-hdr" style="margin-top:32px">How to Wear Them on the Course</h2>
    <p><strong>Start with a polo.</strong> The Stone Island slate blue pique ($285) and the Brain Dead pique thermal ($175) are golf shirts in everything but the name. For colder rounds, the A.P.C. striped polo ($220) or the Only NY speckled knit polo ($148).</p>
    <p><strong>Then a sweater with room to turn.</strong> The Stone Island ribbed half-zip ($575) is the most golf-ready piece here. The Brain Dead wool commuter ($395) has back pockets for balls and tees. The Only NY intarsia crews are the fun ones, and most are under $170.</p>
    <p><strong>Pants that move.</strong> The Only NY Crosswind Active Pant ($148) has stretch and a bungee waist. The Brain Dead climber pants have the belt built in.</p>
    <p><strong>If you only buy one thing from each:</strong> the Brain Dead pique thermal polo, the Stone Island slate blue polo and the Only NY speckled knit polo sweater. Three polos, three cities, no golf logo in sight.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brain Dead</span><span>Los Angeles, since 2014</span></div>
      <div class="sidebar-detail"><span class="l">Stone Island</span><span>Ravarino, Italy, since 1982</span></div>
      <div class="sidebar-detail"><span class="l">Only NY</span><span>New York City, since 2007</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>51</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$32&ndash;$755</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Brain Dead Pique Thermal Polo, Stone Island Pique Polo, Only NY Speckled Knit Polo Sweater</span></div>
      <div class="hashtags">
        <span class="hashtag">#NotGolfFirst</span>
        <span class="hashtag">#BrainDead</span>
        <span class="hashtag">#StoneIsland</span>
        <span class="hashtag">#OnlyNY</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Dress Like You, Then Go Play</h2>
    <p>Golf clothes have come a long way, but the best-designed clothes still mostly come from outside golf. Brain Dead brings the graphics and the fabrics, Stone Island brings decades of dyeing and material research, and Only NY brings New York and a sense of humor. A polo from one, a sweater from another and pants from the third will get you around eighteen holes and through dinner after.</p>
    <p>For more in this vein, read <a href="/drops/best-golf-streetwear-brands-2026">our streetwear golf brands list</a> and <a href="/drops/apc-golf-cph-golf-collab">the A.P.C. Golf collab</a>. Prices were checked on November 19, 2026; Stone Island prices are from its US store. If you know a brand we should look at next, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/not-golf-first/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-PQ*/.pull-quote-inner{font-size:clamp(34px,4.6vw,58px);line-height:1.15;text-align:center;padding:44px 0}.pull-quote-attr{font-size:11px;margin-top:18px}@media(max-width:720px){.pull-quote-inner{font-size:30px;padding:32px 0}}</style>\n<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-19", "dateModified": "2026-11-19",
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <figure style="margin:0 0 28px"><img src="{IMG}/banner-{anchor}.jpg" alt="{H.escape(H.unescape(h2))}, from the brand&rsquo;s own photos" loading="lazy" style="width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:#e8e2d6" /></figure>\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}" style="font-size:clamp(44px,7vw,84px);line-height:1;margin:14px 0 16px;letter-spacing:-.01em">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
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
    <span>The Edit</span><span class="dot"></span>
    <span>{N} picks &middot; prices checked November 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a man in a Brain Dead striped alpaca sweater, a man in a Stone Island wool turtleneck, and a golfer on a putting green in the Only NY Long Island Golf long-sleeve" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Heathlander", "Reinland", "Matize", "Kith", "Kadet"):
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
