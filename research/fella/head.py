#!/usr/bin/env python3
"""build-fella-golf.py — Fella Golf, refreshed on its original URL (/drops/fella-golf).
1 October 2026. Lenny: "this brand page needs a refresh- https://thegrassyissue.com/drops/fella-golf",
then (after the 49-item options sheet) "add F35 adn F46, F14,F20" to my 25 stars = 29 pieces.

FACTS: Fella's own store, About us page, FAQ and shipping policy, read 1 Oct 2026. Founder Behdad
Rahnamai per his LinkedIn and The Devil's Back founder interview (search summary). Prices are the store's
own US-dollar prices (US orders are charged without Dutch VAT), read 1 Oct 2026 via ?currency=USD.
Nine items not sold to the US (Performance Polos, Fella x Jones bags, Fred vest, etc.) are left out.
QUOTES: verbatim from fellagolf.com/pages/about-us. PHOTOS: Fella's own (product + About/home campaign).
Product frames on soft gradient backgrounds via soften-product-frames.py (Lenny, 1 Oct 2026).
Original July post kept its datePublished; dateModified moves to today.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "fella-golf"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/fella-golf-2026"
FR = json.loads((ROOT / "research/fella/frames.json").read_text())
CAT = {o["slug"]: o for o in json.loads((ROOT / "research/fella/options.json").read_text())}
SHOP = "https://fellagolf.com/products/"
BRAND = "Fella Golf"

TITLE = "Fella Golf — Amsterdam Golf Clothes for the Ones Too Far Gone"
DESC = ("Fella Golf, from Amsterdam, makes golf-cart knits, pizza headcovers and sandbagger tees. "
        "Our 2026 refresh: 29 pieces in US dollars, from $15 to $275.")
H1 = "Fella Golf, Revisited &mdash; Amsterdam Golf Clothes for the Ones Already Too Far Gone"


def usd(h):
    p = CAT[h]["usd"]
    return f"${p:g}"


# slug -> (name, detail, copy)
P = {
 # Outerwear and layers
 "reversible-bodywarmer-fleece-golfcart-pattern": ("Reversible Golf Cart Bodywarmer", "New &middot; dropped 29 September",
   "One side is sherpa fleece printed all over with golf carts; flip it and it is a water-resistant forest green shell with a stand collar and zip pockets. It is the newest thing Fella makes, and the right weight for a 50-degree first tee."),
 "wyatt-reflective-windshirt": ("Wyatt Reflective Windshirt", "New for fall",
   "This is a light nylon shell with a mesh lining, back venting and reflective Fella logos that catch the light after dark. Inside the neck tape it reads &ldquo;It Only Takes One Good Shot.&rdquo;"),
 "tech-ripstop-anorak-jacket": ("Tech Ripstop Anorak", "Half zip",
   "This half-zip anorak is ripstop nylon with mesh under the arms, YKK zips and hidden cinch cords at the hem. It layers over a polo and packs small."),
 "liam-windshirt": ("Liam Windshirt", "Short sleeve",
   "The Liam is an oversized short-sleeve windshirt in water-repellent Taslan nylon, green with cream sleeves and orange overlock stitching. The pockets close with hidden magnets."),
 "water-repellent-tech-jacket": ("Panel Tech Jacket", "Green and off-white",
   "This is Fella&rsquo;s most serious jacket: a water-repellent shell in green and off-white panels, with a removable hood and a mesh vent across the back. At $275 it is also the most expensive thing here."),
 # Knitwear and sweaters
 "graham-cotton-cashmere-crewneck-knit": ("Graham Golf Cart Knit", "Cotton-cashmere",
   "This heavyweight cotton-cashmere crewneck has a jacquard golf cart across the chest. It was on our first Fella page and it is still the piece that sums the brand up best."),
 "boris-quarter-zip-sweater-navy": ("Boris Quarter-Zip", "Cream with navy stripe",
   "This is a heavyweight knit quarter-zip in cream with a navy stripe across the chest, salmon piping and a gold zip on a polo-style collar. It is built for winter layering."),
 "gavan-oversized-sweater-heather-grey": ("Gavan Oversized Sweater", "Heather grey &middot; new",
   "The Gavan is heavyweight cotton with a terry inside and a fuzzy chenille Fella patch on the chest. It is the off-course pick, and it pairs with the corduroy cap below."),
 # Polos, shirts and pants
 "jake-toffee-brown-intarsia-knit-polo": ("Jake Intarsia Knit Polo", "Toffee stripe",
   "This knitted polo is 100% combed cotton in a toffee stripe with an easy, relaxed drape. It looks like something from a 1970s European club."),
 "lionel-contrast-rib-knit-polo": ("Lionel Contrast Rib Polo", "Cream and navy",
   "This is a soft cotton knit with contrast rib detailing in cream and navy, made for the hot days when a regular polo feels like too much."),
 "navy-crochet-knitted-polo": ("Lionel Knitted Polo", "Navy",
   "The open-knit Lionel comes boxy and relaxed, with a tonal logo embroidered on the back of the collar. It is the dressier way to wear Fella."),
 "bruno-camp-shirt-tropical-golf-cart": ("Bruno Camp Shirt", "Tropical golf cart print",
   "This camp-collar shirt is a cotton-linen blend in a print of palm trees and golf carts. It is the one for an August round, or the bar after it."),
 "fella-long-sleeve-mockneck-shirt-black": ("Long Sleeve Mockneck", "Black &middot; new",
   "This light cotton-poly mockneck dries quickly and works as a base layer under a knit or on its own, with a big Fella script across the back."),
 "technical-mockneck": ("Technical Performance Mockneck", "Rayon",
   "This mockneck is soft rayon with slightly oversized sleeves and a longer cut that stays tucked through the swing. The logo is tonal, at the collar."),
 "fella-ripstop-cargo-pant": ("Ripstop Cargo Pant", "New &middot; 34/32 sold out",
   "This lightweight ripstop pant has magnetic cargo pockets, a rope tee holder at the left pocket and a velcro belt loop to hold your glove while you putt. The cuffs cinch."),
 # Graphic tees
 "butter-bistro-graphic-t-shirt": ("Butter Bistro Tee", "Chez Fella",
   "Chez Fella&rsquo;s special tonight is butter cuts, a nod to the blade purists who flush it. The back graphic is in butter yellow."),
 "cheesy-slice-graphic-tee": ("Cheesy Slice Tee", "Hunter green",
   "This one has a melting pizza slice on the back of a 240gsm carbon-finished cotton tee with a velvet feel. The fit is oversized."),
 "sandbagger-t-shirt": ("Sandbagger Tee", "Washed cognac",
   "Fella made this for the guy who &ldquo;can&rsquo;t find his swing&rdquo; until there is money on the line. It is a vintage-style graphic on washed cognac, 240gsm cotton."),
 "double-bogey-boxer-t-shirt": ("Double Bogey Boxer Tee", "Deep navy",
   "On the back, a bird boxes a golf bag in gloves that read Double and Bogey. It is heavyweight 220gsm cotton with a small embroidered logo on the front."),
 "papa-fella-t-shirt": ("Papa Fella Pizza Tee", "Butter",
   "Fella calls this the hero piece of its pizza collection: the Papa Fella character serving a cheesy slice, screen printed on the back of a butter-coloured tee."),
 "fella-golf-t-shirt": ("The Fella T-Shirt", "Black",
   "This is the plain one, a slightly oversized black tee with a small logo on the chest and a big one on the back. It is the cheapest tee here at $55."),
 # Headwear
 "cozy-corduroy-cap-teddy-brown": ("Cozy Corduroy Cap", "Teddy brown",
   "This soft corduroy cap has a raised chenille logo patch and a PU leather strap. It is the fall cap."),
 "contrast-sticht-dad-cap": ("All Gear No Game Dad Cap", "Blue-green",
   "This one says it for you in chunky 3D embroidery: &ldquo;ALL GEAR NO GAME.&rdquo; It is blue-green with white contrast stitching and a gold-tone buckle."),
 "fella-performance-cap-white-copy": ("Performance Cap", "Cognac",
   "This is Fella&rsquo;s light, breathable nylon cap in cognac, with a velcro strap. It is the one to wear with the Jake polo."),
 "cha-cheng-tee-buckethat": ("Cha-Cheng Bucket Hat", "Six tee holders",
   "The bucket hat hides six tee holders in its side loops, so you never dig through your pockets. It has a structured crown, a wide brim and a removable cinch cord."),
 # Accessories
 "dice-mallet-headcover-copy": ("Papa Fella Pizza Slice Driver Headcover", "White PU leather",
   "This driver cover is white PU leather with green diamond quilting and an embroidered slice of cheesy pizza. It was on our first page too, and it still makes the bag."),
 "dice-mallet-headcover": ("Double Bogey Dice Mallet Headcover", "White PU leather",
   "The matching mallet cover has two embroidered dice landing on double bogey. Fella sells the pair as a set of inside jokes."),
 "fella-golf-tees": ("Matchbox Golf Tees", "50 wooden tees",
   "These are 50 wooden tees with two green stripes, packed in a custom matchbox. At $20 it is an easy gift."),
 "pizza-slice-double-ball-marker": ("Pizza Slice Ball Marker", "3cm",
   "This 3cm marker has a golden pizza slice with &ldquo;It only takes one good shot&rdquo; around it, and the Fella logo on the back. At $15 it is the cheapest way into the brand."),
}

SECTIONS = [
    ("outer", "Outerwear and Layers", "outerwear",
     ["reversible-bodywarmer-fleece-golfcart-pattern", "wyatt-reflective-windshirt", "tech-ripstop-anorak-jacket", "liam-windshirt", "water-repellent-tech-jacket"],
     "<strong>Five pieces &middot; $160&ndash;$275</strong>Fella designs for Dutch weather, which changes three times before the turn, and that makes its layers good for an Austin fall. The new reversible bodywarmer is golf-cart sherpa on one side and a water-resistant green shell on the other. The Wyatt windshirt has reflective logos for the late finishes, and the Liam and the anorak are the lighter layers for the days that start cold and end warm."),
    ("knit", "Knitwear and Sweaters", "knitwear",
     ["graham-cotton-cashmere-crewneck-knit", "boris-quarter-zip-sweater-navy", "gavan-oversized-sweater-heather-grey"],
     "<strong>Three pieces &middot; $135&ndash;$220</strong>The knitwear is where Fella looks most like a European club from another decade. The Graham golf cart knit is still the signature, the Boris is a heavyweight quarter-zip with a stripe and a gold zip, and the new Gavan is the oversized sweater you wear after the round."),
    ("polo", "Polos, Shirts and a Pant", "polos-and-shirts",
     ["jake-toffee-brown-intarsia-knit-polo", "lionel-contrast-rib-knit-polo", "navy-crochet-knitted-polo", "bruno-camp-shirt-tropical-golf-cart",
      "fella-long-sleeve-mockneck-shirt-black", "technical-mockneck", "fella-ripstop-cargo-pant"],
     "<strong>Seven pieces &middot; $65&ndash;$145</strong>Fella barely makes a standard golf polo. Its polos are knitted, in intarsia stripes, contrast ribs and open crochet, so they read as much at dinner as on the tee. There is a golf-cart camp shirt for the hot months, two mocknecks for the cool ones, and a new ripstop cargo pant with a rope tee holder and a glove loop built in."),
    ("tees", "Graphic Tees", "graphic-tees",
     ["butter-bistro-graphic-t-shirt", "cheesy-slice-graphic-tee", "sandbagger-t-shirt", "double-bogey-boxer-t-shirt", "papa-fella-t-shirt", "fella-golf-t-shirt"],
     "<strong>Six tees &middot; $55&ndash;$65</strong>This is where the jokes live. Pizza runs through the whole brand, from the Papa Fella character to a melting slice, and the rest are inside jokes about the people you play with: the sandbagger, the double bogey and the blade purist. Most are heavyweight 220&ndash;240gsm cotton with a carbon finish, and the graphics sit on the back."),
    ("hats", "Headwear", "headwear",
     ["cozy-corduroy-cap-teddy-brown", "contrast-sticht-dad-cap", "fella-performance-cap-white-copy", "cha-cheng-tee-buckethat"],
     "<strong>Four hats &middot; $39&ndash;$60</strong>The caps run from a teddy-brown corduroy for fall to a light nylon performance cap. The All Gear No Game cap is the funniest thing Fella sells, and the Cha-Cheng bucket hat has six tee holders hidden in the side loops."),
    ("acc", "Headcovers and Small Goods", "accessories",
     ["dice-mallet-headcover-copy", "dice-mallet-headcover", "fella-golf-tees", "pizza-slice-double-ball-marker"],
     "<strong>Four pieces &middot; $15&ndash;$60</strong>The headcovers are quilted white PU leather with a pizza slice on the driver cover and double-bogey dice on the mallet. Add a matchbox of tees and a golden pizza ball marker and you have the cheapest Fella gift there is."),
]
N = 29

PQ = {
    "love": ("We love golf. Probably a little too much.", "Fella Golf, About us"),
    "serious": ("You don&rsquo;t need to take yourself too seriously.", "Fella Golf, About us"),
    "fellas": ("Golf is better with your Fella&rsquo;s.", "Fella Golf, About us"),
}

BANDS = {
    "fall": ("Photography &middot; Fella Golf&rsquo;s own", "The fall campaign: the reversible bodywarmer and the cargo pant out on the course.",
             [("band-a1", "A golfer seen from behind wearing Fella's golf-cart print sherpa bodywarmer on a green", "Golf-cart sherpa"),
              ("band-a2", "A golfer mid-swing in Fella's ripstop cargo pant on a fairway", "The cargo pant"),
              ("band-a3", "A golfer carrying a stand bag in Fella's green bodywarmer beside a flag", "The green side")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we first wrote about Fella in July, it was a fun Amsterdam label you had to buy in euros. Two things have changed. Fella now sells to the US in dollars, without the 21% Dutch VAT that is built into its euro prices, and it ships by DHL Express in two to three business days. And it has a fall collection: a reversible golf-cart bodywarmer that dropped this week, a reflective windshirt, a heavyweight grey sweater and a ripstop cargo pant.</p>
    <p>That makes it an easier brand to recommend from Austin. Fella is for the golfer who plays for the group chat as much as the scorecard: the guy who buys the Sandbagger tee for his regular foursome, wears the All Gear No Game cap without irony, and wants a knit polo that works at the bar afterwards. The jokes are good, and they sit on clothes that are better made than joke clothes usually are, in heavyweight cotton, cotton-cashmere and proper knits.</p>
    <p>On price, the tees are the easy call at $55 to $65 for 240gsm cotton, and the knit polos at $135 are fair for what they are. The new bodywarmer at $162 is the piece to buy this fall, two jackets for the price of one. The $220 Graham knit and the $275 Panel Tech Jacket are harder to justify unless you already love the brand. Budget for import duties on bigger orders, which Fella says are the buyer&rsquo;s to pay, and know that returns are at your own cost.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Fella Golf is an Amsterdam company, Fella Golf B.V., founded by Behdad Rahnamai. Its About page explains it best: the founders love golf, but &ldquo;never really saw ourselves in the overly serious side of golf,&rdquo; so they started a brand about &ldquo;everything that happens between the first tee and the last drink.&rdquo; The motto on the ball marker says the rest: it only takes one good shot.</p>
    <p>Since our first post, Fella has done a run of bags with Portland&rsquo;s <a href="/drops/brand-revisited-jones-sports-co">Jones Sports Co.</a>, most of which has sold out and none of which ships to the US, and added a pizza-themed collection, a fall line and a stockist list. Nine of its current pieces are not sold to the US at all, including the new Performance Polos and the cashmere vest, so we have left them out.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Amsterdam, Netherlands</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Behdad Rahnamai</span></div>
      <div class="sidebar-detail"><span class="l">US shipping</span><span>DHL Express, 2&ndash;3 business days; duties paid by buyer</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$15&ndash;$275</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Reversible Golf Cart Bodywarmer, $162</span></div>
      <div class="sidebar-detail"><span class="l">Updated</span><span>1 October 2026 (first published July 2026)</span></div>
      <a href="https://fellagolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Fella Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#FellaGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#Amsterdam</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Where is Fella Golf based?",
     "Amsterdam, in the Netherlands. The company is Fella Golf B.V., founded by Behdad Rahnamai."),
    ("Does Fella Golf ship to the US?",
     "Yes. US orders ship by DHL Express in two to three business days, are charged without Dutch VAT, and are shown in US dollars. Import duties or local taxes, if any, are paid by the buyer. A few products, including the Performance Polos and the Fella x Jones bags, are not sold to the US."),
    ("How much does Fella Golf cost in dollars?",
     "As of 1 October 2026: graphic tees $55 to $65, caps $39 to $60, knit polos $135 to $145, the reversible bodywarmer $162, the Graham golf cart knit $220 and the Panel Tech Jacket $275."),
    ("What is Fella Golf's return policy?",
     "Returns are accepted within 30 days if the items are unused and in their original condition. Return shipping is at your own cost unless the item is faulty or wrong."),
    ("What does Fella Golf's slogan mean?",
     "Fella's motto, printed on its ball marker and inside its windshirt, is \"It only takes one good shot\": the one shot that keeps you coming back after a bad round."),
]


