#!/usr/bin/env python3
"""build-bag-hang.py — What Hangs Off the Bag: 27 golf bag accessories.
5 October 2026. Lenny: "Let's do a round up style post of best things to hang from your bag, gloves, towels,
accessories, ranger finder holders and some personalized items like any cool key chains etc." (~24 picks,
Brand Index first, then fill). From the options sheet: "no on 1T, use T2, add R4, H1", then "Make sure each box
has multiple images and add some lifestyle/IRL images".

FACTS: research/bag-hang/picks.json (each read on the brand's own store, 5 Oct 2026). Non-USD prices shown in
store currency with an approximate dollar figure (AUD 0.66, EUR 1.17, SEK 0.105).
PHOTOS: brands' own store and site images, localised to /images/bag-hang (research/bag-hang/frames.json for
cards; band-*.jpg from research/bag-hang/life.json; hero from Ghost Golf's own site).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "golf-bag-accessories-what-to-hang-from-your-bag"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/bag-hang"
FRN = json.loads((ROOT / "research/bag-hang/frames.json").read_text())

TITLE = "Golf Bag Accessories: 27 Things to Hang From Your Bag"
DESC = ("Golf bag accessories to clip on: gloves, towels, rangefinder holders, brushes, personalised bag tags and keychains from 27 independent makers, with prices.")
H1 = "What Hangs Off the Bag: 27 Gloves, Towels, Rangefinder Holders, Tags and Keychains"

# code -> (brand, item, price, url, copy)
P = {
 "G04": ("Jones Sports Co.", "Flying J Golf Glove, Cobalt Blue", "$30",
   "https://jonessportsco.com/products/flying-j-golf-glove-cobalt-blue",
   'Jones put its Flying J on a glove and kept everything else simple. It is all Cabretta leather, made for Jones by North Coast Golf Co., with the J in cobalt blue on the strap so it matches a Jones bag from across the range. The full size run is in stock. More in our <a href="/drops/brand-revisited-jones-sports-co">Jones revisit</a>.'),
 "G05": ("Walker Golf Things", "Par-Tec Kooka Glove, White", "A$35 (~$23)",
   "https://walkergolfthings.com/products/par-tec-kooka-glove",
   'The Australian brand cut this one from select Cabretta with flush-sewn seams and engineered perforations, and printed its new kookaburra across the back. It comes in left and right hand, and it is the cheapest glove here once the dollar conversion is done. It launched with the <a href="/drops/walker-golf-the-par-tec-drop">Par-Tec drop</a>.'),
 "G06": ("Students Golf", "Lesson 2 Cabretta Glove, White", "$24",
   "https://studentsgolf.com/products/lesson-2-cabretta-gloves",
   'Students does the plain white glove well. The Lesson 2 is all Cabretta leather with a hot-melt Students logo and an adjustable velcro closure, and at $24 it is the one to buy three of. Sizes M to XL are in stock. See <a href="/drops/students-golf-our-15-favorites">our 15 Students favourites</a>.'),
 "G08": ("Modest Vintage Player", "PRO Houndstooth Cabretta Gloves, Brown (2-Pack)", "$65",
   "https://www.modestvintageplayer.com/products/pro-houndstooth-cabretta-leather-golf-gloves-brown-2-pack",
   "Modest Vintage Player makes its gloves look like they came out of a 1950s pro shop, and the houndstooth is the best of them. You get two lightweight Cabretta gloves in a limited brown houndstooth print, boxed in the brand&rsquo;s vintage packaging. Men&rsquo;s M to XL left hand are in stock."),
 "T02": ("Mogshade", "Contour Golf Towel", "&euro;39 (~$45)",
   "https://mogshadegolf.com/products/contour-golf-towel",
   'Mogshade makes the Contour in Portugal from combed cotton, pre-washed and double-stitched, with a striped texture and a single embroidered mark. It hangs from the bag like a scarf rather than a rag. Nude is the colour in stock; Mint has sold out. Read our <a href="/drops/brand-to-know-mogshade">Mogshade Brand to Know</a>.'),
 "T05": ("Dormie Workshop", "Multi Coloured Towel", "$30",
   "https://dormieworkshop.com/products/multi-coloured-towel-1",
   "Dormie is a leather and headcover workshop in Halifax, Nova Scotia, and its towel has the same quiet taste as its covers. It is a full 22 by 44 inch terry towel in bands of cream, sky blue, rust and brown, cotton with a little polyester so it dries quickly."),
 "T07": ("Local Rule", "Gym Towel, White", "449 kr (~$47)",
   "https://local-rule.com/products/gym-towel-white",
   'Local Rule, from Sweden, made its towel oversized on purpose. The ribbed terry is long enough to fold so one half stays wet for cleaning the ball and the other stays dry for your hands and grips, which is how caddies use one. Ours in <a href="/drops/brand-to-know-local-rule">the Local Rule Brand to Know</a>.'),
 "T09": ("Puttwell", "Know Your Roll Mini Towel, Black/White", "$30",
   "https://puttwellgolfclub.com/products/know-your-roll-mini-towel",
   'Puttwell, from Hawaii, puts its &ldquo;Know your roll&rdquo; tagline on one side of this mini towel and its wordmark on the other. It is a microfibre waffle knit that dries quickly and pulls dirt out of grooves, with a woven loop to hang it from the bag. Ours in <a href="/drops/brand-to-know-puttwell">the Puttwell Brand to Know</a>.'),
 "T10": ("Hidden Links Society", "Bud Chenille Caddie Towel, Black", "$38",
   "https://hiddenlinkssociety.com/products/bud-chenille-caddie-towel-black",
   'Hidden Links Society makes the old-school caddie towel, in heavy ringspun cotton with stripes down the long edges and the brand&rsquo;s Bud character stitched in the corner in chenille. Black is the one that hides a season of dirt. Ours in <a href="/drops/brand-to-know-hidden-links-society">the Hidden Links Society Brand to Know</a>.'),
 "R01": ("Mackem Golf", "Kielder Rangefinder Pouch", "A$125 (~$82)",
   "https://mackemgolf.com/products/kielder-rangefinder-pouch",
   "Mackem makes headcovers out of old tweed and wool, and the Kielder pouch is the same idea for the laser. It is olive waxed canvas on the front with checked wool on the back and inside, padded, with a magnetic closure that opens with one hand and a metal clip for the bag."),
 "R02": ("Winston Collection", "Range Finder Case in Colombian Leather", "$89.99",
   "https://winstoncollection.com/products/range-finder-case-in-colombian-leather",
   'Winston&rsquo;s Colombian leather is softer than the Crazy Horse case in <a href="/drops/rangefinder-cases-and-pouches">our rangefinder case guide</a>, and it creases in nicely. It is lined in polar fleece and hangs from a carabiner. Cafe and Black are in stock; Tan has sold out.'),
 "R03": ("Pins &amp; Aces", "Magnet Caddie", "$25",
   "https://pinsandaces.com/products/magnet-caddie",
   "Most new rangefinders have a magnet built in, and the Magnet Caddie gives it somewhere to stick when you walk. It is a small metal plate that clips onto a bag strap or handle and holds a magnetic rangefinder, towel or speaker. At $25 it is the cheapest fix here."),
 "R04": ("North Coast Golf Co.", "Bogey Black Bear Rangefinder Case", "$60",
   "https://northcoastgolfco.com/products/bogey-black-bear-rangefinder-case",
   "North Coast is a Michigan brand, and the Bogey Black Bear is its all-black case in a recycled shell. It has a waterproof double zip with paracord pulls, a magnetic flap, three pockets and a metal carabiner, so the laser, a few tees and a marker all live in one place."),
 "R06": ("BRIEFING", "Scope Box Pouch Mag Air", "$125",
   "https://www.briefing-us.com/products/brg261g28",
   "BRIEFING started out making bags to military spec in Japan, and the Scope Box shows it. The front panel tilts open on a magnet so the rangefinder comes out with one hand and drops back in, and the hollow-yarn fabric keeps it light. A hook on the back hangs it from the bag."),
 "H01": ("Dimple &amp; Divot", "Carved Hickory Golf Brush", "$78",
   "https://dimpledivot.com/products/carved-hickory-golf-brush",
   'Dimple &amp; Divot carves the handle by hand from American hickory, the wood old clubs were made from, and fits it with firm nylon bristles. It hangs from a layered green and orange paracord tether on an aluminium carabiner, and it is made in the USA. Ours in <a href="/drops/brand-to-know-dimple-divot">the Dimple &amp; Divot Brand to Know</a>.'),
 "H02": ("Gamut Golf", "Wilcox 10K Caddy Brush", "$68",
   "https://gamutgolf.com/products/wilcox",
   'Gamut worked with a tour caddie on the Wilcox and makes it in solid ebony or green sandalwood. It hangs from a heavy magnetic connector on a steel swivel clasp, so it pulls off the bag with one hand and snaps back on. See our <a href="/drops/brand-to-know-gamut-golf">Gamut Brand to Know</a>.'),
 "H04": ("Steurer &amp; Jacoby", "8&Prime; x 6&Prime; Golf Tee Bag, Premium Leather", "$55",
   "https://sj.golf/products/leather-golf-tee-bag",
   "Steurer &amp; Jacoby is known for its leather and plaid carry bags, and the tee bag is the small version of that look. It is American cowhide, handmade in the USA, with a zip top and a solid brass trigger snap that clips to the bag. Tees, balls and a marker fit inside."),
 "H05": ("Ghost Golf", "Utility Pouch, Valor", "$40",
   "https://ghostgolf.com/products/utility-pouch-valor",
   "Ghost&rsquo;s Utility Pouch is 7.25 by 6 inches, water-resistant and lined in velour so a phone or rangefinder goes in without scratching. The Valor colourway is navy, white and red, and it clips on with a carabiner."),
 "H06": ("STITCH", "Roadster Leather Valuables Pouch", "$78",
   "https://stitchgolf.com/products/roadster-leather-valuables-pouch",
   "STITCH built the Roadster to hold the watch, wallet and keys, in a two-tone leather treated to shed water and stains, with a magnetic closure and a leather loop that hangs it off the bag. Five colours are in stock."),
 "B01": ("Seamus Golf", "Hand Forged America Country Club Bag Tag, Copper", "$80",
   "https://www.seamusgolf.com/products/copy-of-hand-forged-old-glory-bag-tag-copper",
   'Seamus has a second-generation blacksmith in Portland hammer and finish each of these by hand from copper. It is a map of the US cut from a disc, about 2.75 inches across, on a leather tie, and Seamus will hand-stamp the back at no charge. Read our <a href="/drops/brand-to-know-seamus">Seamus Brand to Know</a>.'),
 "B02": ("iliac Golf", "Leather Bag Tag", "$50",
   "https://iliacgolf.com/products/leather-bag-tag",
   "iliac cuts and stitches its tags by hand from full-grain leather in its American workshop, with the shield on the front and a swivel snap clip. It comes in Pitch Black or Olive, initials are free, and each one is made to order in 14 days or less."),
 "B03": ("Billykirk", "No. 575 Golf Bag Tag, Navy", "$65",
   "https://billykirk.com/products/no-575-golf-bag-tag-navy",
   "Billykirk has been making leather goods in the US since 1999, and its golf tag is built like its belts. It is vegetable-tanned full-grain leather with hand-burnished edges, matte nickel hardware and a custom ID card. Up to three embossed initials are available; Billykirk lists monogramming at $15. Also in Black and Green."),
 "B07": ("Asher Riley", "Golf Tee Needlepoint Luggage Tag", "$45",
   "https://asherriley.com/products/bouy-needlepoint-luggage-tag",
   "Needlepoint is the classic country-club accessory, and Asher Riley&rsquo;s golf tee tag is a good one. The front is hand-stitched in striped tees on navy, the back is English leather with a window for your card, and it buckles on with a leather strap at 4.75 by 2.75 inches."),
 "K01": ("Aim&eacute; Leon Dore", "Leather Traveler Charm", "$150",
   "https://www.aimeleondore.com/products/leather-traveler-charm",
   "Aim&eacute; Leon Dore made this for luggage, and it looks better on a golf bag. It is three small calf leather tags printed with vintage postage stamps on a 9.5 inch leather strap, made in Italy. At $150 it is the most expensive small thing here."),
 "K03": ("Craighill", "Coachwhip Carabiner", "$44",
   "https://craighill.co/products/coachwhip-carabiner",
   "Craighill, a design studio in Brooklyn, makes the best-looking carabiner you can buy. The Coachwhip is CNC-milled stainless steel bent into an S-curve, with springy wire gates at each end, so the keys hang on one side and the bag on the other. Stainless, Vapor Brass or Vapor Black."),
 "K04": ("Corter Leather", "Bottlehook", "$36.50",
   "https://corterleather.com/products/bottlehook",
   "Corter, in Boston, makes the Bottlehook from solid brass. It hooks the keys to a belt loop or a bag D-ring and opens a beer at the turn, and it comes with a brass split ring and a lifetime warranty against breaking. The copper and stainless versions have sold out."),
 "K06": ("Smathers &amp; Branson", "Monogrammed Azalea Key Fob, Dark Navy", "$50",
   "https://smathersandbranson.com/products/monogrammed-azalea-key-fob-dark-navy",
   "Smathers &amp; Branson stitches a pink azalea on dark navy needlepoint, then stitches your three initials into the design. It has a leather tab and a split ring. The plain fobs are $35; the monogram is what makes this one yours."),
}

SECTIONS = [
    ("Gloves", "gloves", ["G04", "G05", "G06", "G08"],
     "<strong>Four gloves &middot; ~$23&ndash;$65</strong>The glove is the one thing on the bag you touch every shot, and it hangs off the strap between holes. All four here are Cabretta leather, the thin sheepskin most good gloves use, so the difference is in the details. Jones and Walker put their logos on the strap and the back, Students keeps it white and cheap enough to buy in threes, and Modest Vintage Player sells two houndstooth gloves in a box that looks like it came from a 1950s pro shop.",
     "gloves"),
    ("Towels", "towels", ["T02", "T05", "T07", "T09", "T10"],
     '<strong>Five towels &middot; $30&ndash;$47</strong>A towel is the biggest thing you can hang on a bag and the cheapest way to change how the bag looks. Three are cotton and quiet: Mogshade&rsquo;s combed cotton from Portugal, Dormie&rsquo;s striped terry from Halifax, and Local Rule&rsquo;s oversized ribbed towel that folds into a wet half and a dry half. Hidden Links Society&rsquo;s black chenille caddie towel is the heavy one, and Puttwell&rsquo;s mini waffle towel is the one for the grooves. For fifty more, see our <a href="/drops/fall-golf-towel-roundup-2026">fall towel roundup</a>.',
     "towels"),
    ("Rangefinder Holders", "rangefinder-holders", ["R01", "R02", "R03", "R04", "R06"],
     '<strong>Five holders &middot; $25&ndash;$125</strong>If you walk, the rangefinder needs to live on the outside of the bag where your hand finds it without looking. A magnetic closure is the thing to look for, and four of these have one: Mackem, North Coast and BRIEFING build it into the flap, and the Pins &amp; Aces Magnet Caddie skips the case and gives a magnetic laser a plate to stick to. Winston&rsquo;s soft leather case is the dressy one. We went deeper in <a href="/drops/rangefinder-cases-and-pouches">our rangefinder case guide</a>.',
     "rangefinder"),
    ("Brushes and Pouches", "brushes-and-pouches", ["H01", "H02", "H04", "H05", "H06"],
     "<strong>Five clip-ons &middot; $40&ndash;$78</strong>The small things that keep the pockets empty. Two of these are groove brushes, and both are made of wood: Dimple &amp; Divot carves its handle from hickory and Gamut uses ebony or sandalwood on a magnetic clip. The other three are pouches for tees, balls, a phone or your wallet, in leather from Steurer &amp; Jacoby and STITCH and in water-resistant nylon from Ghost.",
     "hangers"),
    ("Personalised Bag Tags", "bag-tags", ["B01", "B02", "B03", "B07"],
     "<strong>Four tags &middot; $45&ndash;$80</strong>A bag tag says whose bag it is, and a good one does it with your initials. Seamus has a blacksmith in Portland hammer its tags out of copper and will hand-stamp the back for free. iliac and Billykirk make theirs from full-grain leather in American workshops and will add your initials, free at iliac. Asher Riley&rsquo;s is hand-stitched needlepoint with a leather back and a window for your card.",
     "tags"),
    ("Keychains and Charms", "keychains", ["K01", "K03", "K04", "K06"],
     "<strong>Four pieces &middot; $36.50&ndash;$150</strong>The car keys have to go somewhere, and a hook on the bag is better than a pocket. Craighill&rsquo;s steel carabiner and Corter&rsquo;s solid brass Bottlehook clip the keys to a D-ring, and the Bottlehook opens a beer at the turn. Smathers &amp; Branson will stitch your initials into a needlepoint fob, and Aim&eacute; Leon Dore&rsquo;s stamp charms are the dressy option.",
     "keys"),
]

BANDS = {
    "gloves": ("Photography &middot; the brands&rsquo; own", "Walker, Modest Vintage Player and Students take their gloves out on the course.",
               [("band-gloves-1", "A Walker Golf Things bag and shoes on a turf mat at sunset by the water", "Walker Golf Things"),
                ("band-gloves-2", "A hand pulling on a brown houndstooth Modest Vintage Player glove", "Modest Vintage Player"),
                ("band-gloves-3", "Two golfers carrying their bags past a pine tree on a links course", "Students Golf")]),
    "towels": ("Photography &middot; the brands&rsquo; own", "Mogshade, Dormie and Local Rule show their towels on the bag and on the course.",
               [("band-towels-1", "A Mogshade Contour towel hanging from a golf bag beside a plaid headcover", "Mogshade"),
                ("band-towels-2", "Two golfers talking beside a golf bag under a wooden shelter", "Dormie Workshop"),
                ("band-towels-3", "A golfer walking with his bag across a misty marsh", "Local Rule")]),
    "rangefinder": ("Photography &middot; the brands&rsquo; own", "Mackem, Pins &amp; Aces and Jones show where the laser rides.",
                    [("band-rangefinder-1", "Plaid wool Mackem headcovers on the grass", "Mackem Golf"),
                     ("band-rangefinder-2", "A cart bag on the back of a golf cart with a magnetic rangefinder", "Pins &amp; Aces"),
                     ("band-rangefinder-3", "A golfer swinging beside a stand bag in long grass", "Jones Sports Co.")]),
    "hangers": ("Photography &middot; the brands&rsquo; own", "Dimple &amp; Divot, Steurer &amp; Jacoby and Gamut shoot their gear out on the course.",
                [("band-hangers-1", "A golfer checking a scorecard beside a stand bag with a checked headcover", "Dimple &amp; Divot"),
                 ("band-hangers-2", "A waxed canvas and leather Steurer &amp; Jacoby carry bag", "Steurer &amp; Jacoby"),
                 ("band-hangers-3", "Two golfers on a green framed by trees", "Gamut Golf")]),
    "tags": ("Photography &middot; the brands&rsquo; own", "Seamus, iliac and Billykirk photograph their leather on the bag and on the way to the course.",
             [("band-tags-1", "A black carry bag with a leather patch and a patterned headcover lying in tall grass", "Seamus Golf"),
              ("band-tags-2", "Two leather iliac bags in the boot of a car", "iliac Golf"),
              ("band-tags-3", "Two men walking down a street with a Billykirk leather bag", "Billykirk")]),
    "keys": ("Photography &middot; the brands&rsquo; own", "Craighill and Asher Riley show off the small stuff.",
             [("band-keys-1", "Keys clipped to the belt loop of a pair of jeans with a Craighill carabiner", "Craighill"),
              ("band-keys-2", "Two needlepoint Asher Riley luggage tags on a canvas tote", "Asher Riley"),
              ("band-keys-3", "Two needlepoint can holders, one with the Texas flag, on a planter", "Asher Riley")]),
}

N = 27
GRID_CSS = '<style>/*TGI-BAGHANG-GRID*/.products-grid[data-n=\"4\"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.products-grid[data-n=\"5\"]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n=\"5\"]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:1024px){.products-grid[data-n=\"4\"]{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:820px){.products-grid[data-n=\"5\"]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n=\"4\"]{grid-template-columns:1fr}.products-grid[data-n=\"5\"]>.product-card{flex-basis:100%}}</style>\n'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The clubs are the same for most of us. What changes from bag to bag is everything clipped to the outside of it: the glove drying on the strap, the towel, the brush, the case for the laser, the tag with your name on it and the car keys. That is where a bag gets its personality, and it is where a lot of the best independent makers are doing their most interesting work.</p>
    <p>So this is a roundup of the small things, twenty-seven of them from twenty-seven brands, sorted by what they do. Some are practical, like Pins &amp; Aces&rsquo; $25 Magnet Caddie, which gives a magnetic rangefinder somewhere to stick when you walk. Some are just good objects, like a copper tag hammered by a blacksmith in Portland or a brass hook from Boston that opens a beer.</p>
    <h2 class="products-hdr btk-story-hdr">Make It Yours</h2>
    <p>Four of these can carry your name or initials. Seamus hand-stamps the back of its copper tags for free, iliac adds initials to its leather tags at no charge, and Billykirk will emboss up to three. Smathers &amp; Branson stitches your initials into a needlepoint key fob. They are the best presents on the list, because nobody else has one.</p>
    <p>If you only buy one thing, buy the Seamus tag. It costs $80, it will outlast the bag, and the stamp on the back makes it yours. Prices were read on each brand&rsquo;s own store on 5 October 2026; non-US prices show an approximate dollar figure.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>27 from 27 brands</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>~$23&ndash;$150</span></div>
      <div class="sidebar-detail"><span class="l">Personalised</span><span>4 picks</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Seamus copper bag tag, $80</span></div>
      <div class="sidebar-detail"><span class="l">Under $30</span><span>Pins &amp; Aces Magnet Caddie, $25</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>5 October 2026</span></div>
      <a href="#gloves" class="sidebar-cta">See the picks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfBag</span>
        <span class="hashtag">#GolfAccessories</span>
        <span class="hashtag">#BagTag</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What should you hang on a golf bag?",
     "Most golfers hang a towel, a glove and a groove brush, and walkers add a rangefinder case or a magnetic mount. A bag tag with your name, a pouch for your phone and wallet, and a hook for your car keys finish the set. This roundup has 27 picks across those six groups."),
    ("What is the best personalised golf bag tag?",
     "In this guide, Seamus Golf's hand-forged copper tag ($80) comes with free hand-stamped personalisation on the back, iliac's leather tag ($50) adds initials at no charge, and Billykirk's No. 575 ($65) takes up to three embossed initials. Asher Riley's needlepoint tag ($45) is the classic country-club option."),
    ("How do you attach a rangefinder to a golf bag?",
     "Clip it on in a case with a carabiner or snap hook, like the Mackem Kielder or Winston leather case, or use a magnetic mount. The Pins & Aces Magnet Caddie ($25) clips to a bag strap and gives a rangefinder with a built-in magnet a metal plate to stick to."),
    ("Where should I keep my keys and wallet on the course?",
     "A valuables pouch that hangs off the bag, like STITCH's Roadster leather pouch ($78) or Ghost Golf's Utility Pouch ($40), keeps them in one place. For keys alone, a carabiner such as Craighill's Coachwhip ($44) or Corter's brass Bottlehook ($36.50) clips them to a D-ring."),
    ("How much do golf bag accessories cost?",
     "In this roundup, from about $23 for Walker Golf Things' Kooka glove and $25 for the Pins & Aces Magnet Caddie, up to $150 for Aime Leon Dore's leather charm. Most picks are between $40 and $80. Prices were read on each brand's own store on 5 October 2026."),
]


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


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker, bkey = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n' + band(bkey)), n0 + len(ids)


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
         "url": URL, "image": og, "datePublished": "2026-10-05", "dateModified": "2026-10-05",
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
            {"@type": "ListItem", "position": 3, "name": "Golf Bag Accessories", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    brands = [H.unescape(P[k][0]) for k in ids]
    assert len(brands) == len(set(brands)), "brand repeated"
    for k in ids:
        assert len(FRN.get(k, [])) >= 2, k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Golf Bag Accessories</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Seamus, Jones, Mackem, Dimple &amp; Divot, Billykirk and more</span><span class="dot"></span>
    <span>27 picks &middot; in stock 5 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Four Ghost Golf towels in orange, white, black and grey hanging from a golf bag on the course" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace('</head>', GRID_CSS + '</head>', 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
