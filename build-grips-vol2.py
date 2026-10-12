#!/usr/bin/env python3
"""build-grips-vol2.py — Grips Vol. 2: RIPIT, 97golf, Gives Golf, Sweet Rollz and IOMIC. Cloned from build-radar-three.py. 12 October 2026.
Lenny: "new options from ripit and 97golf, gives golf and more", then "Make sure all images are High res and no stark white
backgrounds. at least 8 options from each maker and different colorways in the same box".
FACTS: each store's products.json (research/grips-vol2/), read October 12, 2026; in-stock colorways only. RIPIT in AUD (x0.6984).
Gives Golf sells five grips plus a divot tool, and 97golf has six in-stock grip lines, so neither reaches eight; all are shown.
Dropped: IOMIC X-Evolution Blackout (no photo over 900px) and Sticky Army 1.0 (ladies/junior sizing).
Frames: research/grips-vol2/frame.py (white packshots destarked; 97golf square artwork padded to 4:5).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Grips Vol. 2: 56 Golf Grips From RIPIT, Cloud & Wind, IOMIC, Cadero and More"
DESC = ("The Niche Grip Report, Vol. 2: seven small grip makers. RIPIT art grips, Cloud & Wind, 97golf, Gives Golf, "
        "Sweet Rollz putter grips, and IOMIC and Cadero from Japan. 56 boxes, every colorway together, with prices.")
H1 = "The Niche Grip Report, Vol. 2"
BC = "Grips Vol. 2"
SLUG = "niche-grip-report-vol-2"
IMG = "/images/grips-vol2"
SHOP = ""
RI, NS, GG, SR, IO = "RIPIT Grips", "97golf", "Gives Golf", "Sweet Rollz", "IOMIC"
RIU, NSU, GGU, SRU, IOU = ("https://ripitgrips.com/products/", "https://97golf.co/products/", "https://givesgolf.com/products/",
                           "https://sweetrollzgolf.com/products/", "https://iomicusa.com/products/")
CW, CD = "Cloud &amp; Wind Golf", "Cadero"
CWU, CDU = "https://www.cloudandwindgolf.com/products/p/", "https://cadero.shop/products/"
A17, A35 = "A$24.95 (~$17)", "A$49.95 (~$35)"
P = {
 # RIPIT
 "kenny": (RI, "Kenny &middot; 2026 Art Series", A17, RIU+"kenny",
   "Artwork by Kentaro Yoshida wrapped around the whole grip, mixing his Japanese heritage with Australian coast culture. Limited edition. In this box: <strong>Charcoal and Red Clay</strong>."),
 "coco": (RI, "Coco &middot; 2026 Art Series", A17, RIU+"coco",
   "Tattoo artist Coco Loberg&rsquo;s linework in orange and red on a royal blue grip. The boldest of the Art Series and the one we would put on a driver. Limited edition, one colorway: <strong>Royal Blue</strong>."),
 "brosmind": (RI, "Brosmind &middot; 2026 Art Series", A17, RIU+"brosmind",
   "Barcelona illustration duo Brosmind filled this one with characters and hidden details, the kind you find on the fifth hole. Limited edition. In this box: <strong>Neon Blue, Neon Pink, Neon White and Neon Yellow</strong>."),
 "chopper": (RI, "Ron Chopper Collab", A17, RIU+"ripit-x-chopper-striped",
   "Two RIPIT patterns in an exclusive Chopper colorway, for the Australian golf content creator: navy with a pink cap. In this box: <strong>Striped x Chopper and Flower of Life x Chopper</strong>, each sold separately."),
 "hypegolf": (RI, "RIPIT x HYPEGOLF", A17, RIU+"hypegolf-x-ripit-grips",
   "A collab with the streetwear-minded golf outlet HYPEGOLF: a clean, repeating athletic stripe in muted colors. Hype Black was sold out when we checked. In this box: <strong>Merlot and Moss</strong>."),
 "freshprince": (RI, "Fresh Prince", A17, RIU+"fresh-prince",
   "Early-1990s shapes and colors on a performance grip, as loud as anything here. Undersized is offered in Apricot only. In this box: <strong>Fresh Apricot, Fresh Blue and Fresh White</strong>."),
 "flower": (RI, "Flower of Life &middot; Dual Compound", A17, RIU+"flower-of-life",
   "Two zones: a firmer upper half for stability and a softer lower half for feel, with a two-tone finish to match. Undersized, Standard+ and Jumbo. In this box: <strong>Clay and Cream, Green and Raisin, Lilac and Rust</strong> and more."),
 "striped": (RI, "Striped", A17, RIU+"striped",
   "RIPIT&rsquo;s simplest grip: a repeating stripe in soft, grown-up colors. All 16 options were in stock, from Undersized to Jumbo. In this box: <strong>Azalea, Blue Striped, Camellia and Chocolate</strong> among others."),
 "geo": (RI, "Geo", A17, RIU+"geo",
   "A repeating geometric pattern that doubles as reference points for your hands. In this box: <strong>Geo Aqua, Augusta, Jester and Lemon</strong> among others, in Undersized and Standard+."),
 "squiggle": (RI, "The Squiggle", A17, RIU+"the-squiggle",
   "A loose, abstract squiggle over a textured surface. The most playful of RIPIT&rsquo;s everyday grips. In this box: <strong>Squiggle Aqua, Augusta, Burnt Olive, Lemon, Lilac and Peach</strong>."),
 "sqputter": (RI, "Square-Face Putter Grips", A35, RIU+"checkered-sq-face-putter-grip",
   "New this fall: four patterns on a square-face putter grip shaped to help you set up the same way every time. Slim or Standard. In this box: <strong>Checkered</strong> (Pink Lemonade, Creaming Soda, Vanilla Cola), <strong>Ripple</strong> (Chocolate, Navy, Raisin), <strong>Drip</strong> (Tide, Dune) and <strong>Camo</strong>."),
 # 97golf
 "j25links2": (NS, "J25 Hybrid &middot; Links II Collection", "$9.99", NSU+"j25-hybrid-grip-clay-links-ii-collection",
   "A corded upper half for traction and a softer rubber lower half for feel, in five earthy colors. Amber and Fairway were down to Standard size only. In this box: <strong>Clay, Harbor, Granite, Amber and Fairway</strong>."),
 "j25links": (NS, "J25 Hybrid &middot; Links Collection", "$9.99", NSU+"j25-hybrid-grips-clay-links-collection",
   "The same hybrid grip with the original Links artwork. Every color was in stock in Standard and Midsize +4. In this box: <strong>Clay, Harbor, Granite, Amber and Fairway</strong>."),
 "t01field": (NS, "T01 Tour &middot; Field Collection", "$7.99", NSU+"t01-tour-grip-tundra-field-collection",
   "97golf&rsquo;s upgrade to its TW97: a high-tack texture over a three-rubber compound. Standard or Midsize; Dune was Standard only. In this box: <strong>Tundra, Summit, Dune and Iron</strong>."),
 "t01sunday": (NS, "T01 Tour &middot; Sunday Green", "$7.99", NSU+"t01-tour-grip-sunday-green-tournament-collection",
   "The T01 in deep green with gold trim, from the Tournament Collection. If you only buy one grip on this page for a full set, this is the one we would pick at $7.99 each."),
 "t01cord": (NS, "T01 Cord &middot; Panda Collection", "$9.99", NSU+"t01-cord-grip-black-panda-cord-collection-copy",
   "The T01&rsquo;s compound with a full-length heavy cord, for rain and sweaty hands. The white version was sold out. In this box: <strong>Black</strong>."),
 "tw97": (NS, "TW97 Tour &middot; Edgewood Collection", "$3.99", NSU+"tw97-tour-grips-redwood-edgewood-collection",
   "The cheapest grip here by a distance: responsive rubber with a barbell texture, in woodland colors. Some colors were down to one size. In this box: <strong>Redwood, Evergreen, Overcast Blue and Sandstone</strong>."),
 # Gives Golf
 "tide": (GG, "The Tide", "$14", GGU+"the-tide",
   "A midsize rubber grip in navy with white waves. Gives says it is for when you &ldquo;let your swing do the talking.&rdquo;"),
 "orbit": (GG, "The Orbit", "$14", GGU+"the-orbit",
   "Olive with a column of white dots, and a cushioned feel Gives pitches at the short game."),
 "prism": (GG, "The Prism", "$14", GGU+"the-prism",
   "Mint with a teal cap: the brightest Gives grip, on the same smooth midsize shape."),
 "matrix": (GG, "The Matrix", "$14", GGU+"the-matrix",
   "Gray with a higher-traction texture than the rest of the range. The one for players who like to feel the grip bite."),
 "birdie": (GG, "The Birdie", "$14", GGU+"the-birdie",
   "Clean white and gray. The brand&rsquo;s joke is in the name; see the quote above."),
 "divot": (GG, "The Divot Tool", "$30 silver &middot; $40 bronze", GGU+"the-divot-tool",
   "Not a grip, but it rounds out the brand: a stainless steel divot tool shaped like a tee. In this box: <strong>Silver and Bronze</strong>."),
 # Sweet Rollz
 "lapina": (SR, "La Pi&ntilde;a", "$34.95", SRU+"la-pina",
   "Pineapples on cream, for anyone who likes pi&ntilde;a coladas and holing putts. Midsize only when we checked."),
 "sinatra": (SR, "Sinatra", "$34.95", SRU+"sinatra-midsize",
   "Colorful martini glasses on charcoal, a nod to Ol&rsquo; Blue Eyes. Midsize or Skinny."),
 "electric": (SR, "Electric Avenue", "$34.95", SRU+"electric-avenue-midsize",
   "Tropical flowers in neon pink and green. The loudest putter grip on the page. Midsize or Skinny."),
 "hula": (SR, "Hula Girl", "$34.95", SRU+"hula-girl-midsize",
   "Hula dancers on cream, island style for the flatstick. Midsize or Skinny."),
 "tuesday": (SR, "Tuesday", "$34.95", SRU+"tuesday-midsize-1",
   "Tacos on turquoise, for the best day of the week. Midsize or Skinny."),
 "muertos": (SR, "Muertos", "$34.95", SRU+"muertos",
   "Sugar skulls and marigolds, a festive Day of the Dead design that works year round. Midsize or Skinny."),
 "swash": (SR, "Swashbuckler", "$34.95", SRU+"swashbuckler-midsize-1",
   "Black-on-black skull and crossbones. The quiet one, until someone looks closely. Midsize or Skinny."),
 "bethpage": (SR, "Bethpage Black", "$34.95", SRU+"bethpage-black-midsize",
   "All black with a subtle texture, named after the famously tough public course. Midsize only when we checked."),
 "backcountry": (SR, "Backcountry", "$34.95", SRU+"backcountry",
   "A misty mountain scene in grays and greens, the most landscape-like of the range. Midsize only when we checked."),
 # IOMIC
 "sticky23": (IO, "Sticky 2.3", "$14.50", IOU+"sticky-2-3",
   "IOMIC&rsquo;s best-known grip: tacky, standard size, used by everyone from beginners to tour players. A 13-grip box set is $180. In this box: <strong>Black, Blue, Coral Red, Navy, White and Green</strong> among others."),
 "stickycamo": (IO, "Sticky Camo 2.3 / 1.8", "$16", IOU+"sticky-camo-2-3-1-8",
   "The same all-weather tack in camo, made in Japan. In this box: <strong>Green and Sand Canyon</strong> (2.3, standard) and <strong>Pink</strong> (1.8, undersize)."),
 "blackarmy": (IO, "Sticky Black Army 2.3", "$16", IOU+"sticky-black-army-2-3",
   "Black camo with a color running through it, molded in rather than printed so it lasts. In this box: <strong>Blue, Orange and Yellow</strong>."),
 "sticky18": (IO, "Sticky 1.8", "$14.50", IOU+"sticky-1-8",
   "An undersize grip, softer than the 2.3, with two-tone colors. In this box: <strong>Black/Sky Blue, Blue/Sky Blue, Orange/Blue, Red/Blue and White/Silver Grey</strong> among others."),
 "evose": (IO, "Sticky Evolution SE 2.3", "$14.50", IOU+"sticky-evolution-se-2-3",
   "A hybrid: X-Evolution texture on top, softer Sticky pattern below, with a ribbed option. In this box: <strong>Coral Red/Pink</strong> (ribbed or round) and <strong>Sky Blue/Autumn Blue</strong> (ribbed)."),
 "ix23": (IO, "iX 2.3", "$14.75", IOU+"ix-2-3",
   "IOMIC&rsquo;s answer to a cord grip: crosses and a pebbled grain, without the rough feel on your hands. In this box: <strong>Black, Coral Red and Light Blue</strong>."),
 "iclassic": (IO, "I-Classic Tour Putter &middot; Mid-Taper", "$35.50", IOU+"i-classic-tour-putter-74g-taper-midsize",
   "A traditional tour putter shape, 74g, precision-molded in Japan. In this box: <strong>Black, Coral Red, Light Blue, Platinum Grey and Turquoise Green</strong>."),
 "absolutex": (IO, "Absolute-X &middot; 65g", "$16.50", IOU+"absolute-x-65g-standard",
   "A textured grip built to lower grip pressure. Ten colors, all in stock. In this box: <strong>Black, Blue, Coral Red, Orange and Pink</strong> among others."),
 # Cloud & Wind (all single grips $18)
 "cwblossom": (CW, "The Blossom &middot; Classics", "$18", CWU+"blossom",
   "Cherry blossom branches painted the length of the grip, the design Cloud &amp; Wind started with. In this box: <strong>The Blossom, Palace Wall</strong> (red, for blooming branches against red walls), <strong>Porcelain</strong> (blue on white, after porcelain art) and <strong>Canvas</strong> (a vintage, painted look)."),
 "cwspring": (CW, "The Blossom &middot; Spring Colors", "$18", CWU+"2tnb4kjsjbcmduukev9p569k309okz-26t8d-n2tz3-cmnx3",
   "Three more Blossom colorways. <strong>Apricot</strong> is pale yellow with apricot flowers, <strong>First Light</strong> is a deep marigold for the first tee time of the day, and <strong>Moonshade</strong> is violet, for the range at nightfall."),
 "cwblossom26": (CW, "The Blossom &middot; 2026", "$18", CWU+"blossom-ax8dg",
   "This year&rsquo;s two. <strong>Beneath the Boughs</strong> is pink blossom on deep green, with the verse &ldquo;曲径通幽处，禅房花木深&rdquo; along the grip. <strong>After the Rain</strong> is white blossom on cobalt blue."),
 "cwwave": (CW, "Cloud &amp; Wave", "$18", CWU+"wave",
   "Rolling wave lines for the spot on the Pacific coast where the clouds meet the waves. In this box: <strong>Cloud &amp; Wave, Twilight, June Gloom</strong> (new) and <strong>Afterglow</strong> (new)."),
 "cwmist": (CW, "Mountain &amp; Mist", "$18", CWU+"wave-gygps",
   "Two greens, a mossy lower half under a pale sage top, for spring rounds in misty weather with mountains behind the green. One colorway."),
 "cwzen": (CW, "The Zen Grip", "$18", CWU+"zen",
   "No flowers, just a raked-sand wave texture, like a Zen garden or a freshly raked bunker. In this box: <strong>The Zen</strong> (white), <strong>Sand</strong> and <strong>Smoke</strong> (new)."),
 "cwpacific": (CW, "Pacific Summer &middot; 3-Grip Set", "$50", CWU+"tri-color-serenade-22jtc-rp77r-2f5zd",
   "June Gloom, Afterglow and Smoke in one set, inspired by the marine layer, clearing skies and haze of the California coast. Three new grips for $50 instead of $54."),
 "cwten": (CW, "10-Grip Sets", "$160", CWU+"tri-color-serenade-j8nbp-wly6b-tbmd6",
   "Enough for a full regrip, in two colorways five and five. In this box: <strong>Waiting for You</strong> (Porcelain and After the Rain), <strong>Blossom, Boughs, Beneath</strong> and <strong>A Midsummer Night&rsquo;s Dream</strong> (Moonshade and Afterglow)."),
 # Cadero (EUR x1.12)
 "cadduo": (CD, "2x2 Pentagon DUO SP", "&euro;22.90 (~$26)", CDU+"2x2-pentagon-duo",
   "Cadero&rsquo;s flagship: pentagon-shaped grooves for traction under a clear outer layer that keeps the color clean. Round or ribbed. In this box: <strong>White x Rainbow, White x Gold, Grey x Yellow, Carbon x Pink, Carbon x Red, Carbon x Silver, Grey x Orange and Tricolour</strong>, among others."),
 "cadpent": (CD, "2x2 Pentagon", "&euro;21.90 (~$25)", CDU+"2x2-pentagon",
   "The original: the Cadero logo printed under a translucent, tacky elastomer skin. In this box: <strong>White x Silver, Red, Green, Pink and Blue; Black x Red, Silver and Gold</strong>."),
 "cadmil": (CD, "Pentagon DUO LTD Military", "&euro;24.90 (~$28)", CDU+"2x2-pentagon-duo-military",
   "A stencil-style military Cadero logo on olive, white or navy. In this box: <strong>Olive x Black, Olive x Orange, White x Orange, White x Black, Navy x Pink and Navy x White</strong>."),
 "cadstars": (CD, "Pentagon DUO LTD Stars", "&euro;24.90 (~$28)", CDU+"2x2-pentagon-duo-ltd-stars",
   "Stars down the top of the grip and &ldquo;Have a nice day!&rdquo; underneath. In this box: <strong>Rainbow</strong> (on white) and <strong>Silver</strong> (on black)."),
 "cadmex": (CD, "Pentagon DUO LTD Mexico", "&euro;24.90 (~$28)", CDU+"2x2-pentagon-duo-ltd-mexico",
   "A Day of the Dead tribute: red-and-green logo up top, calacas (skulls) below. Only size S, ribbed, was left when we checked."),
 "cadputt": (CD, "2x2 Putter Grip", "&euro;34.90 (~$39)", CDU+"2x2-putter-grip",
   "The Pentagon construction on a putter grip. In this box: <strong>Gold x Silver, Red x Blue, Orange x Yellow and Pink x Pink</strong>."),
 "cadab": (CD, "AB Rubber 4 PRO", "&euro;13.90 (~$16)", CDU+"ab-rubber-4-pro",
   "The quiet one: 100% natural, renewable rubber with no artificial resins, and an antibacterial agent made from scallop shells. Only grey, size M, was in stock."),
 "cadbasic": (CD, "Basic Rubber", "&euro;10.90 (~$12)", CDU+"basic-rubber",
   "Plain black rubber with the logo vulcanized near the end. The cheapest Cadero, and it goes on with air. Round only when we checked."),
}
SECTIONS = [
 ("RIPIT Grips", "ripit", ["kenny","coco","brosmind","chopper","hypegolf","freshprince","flower","striped","geo","squiggle","sqputter"],
  "<strong>Australia &middot; 11 boxes &middot; A$24.95&ndash;A$49.95</strong>Back from Vol. 1 with a 2026 Art Series, two collabs and its first square-face putter grips. Prices in Australian dollars."),
 ("Cloud &amp; Wind Golf", "cloud-and-wind", ["cwblossom","cwspring","cwblossom26","cwwave","cwmist","cwzen","cwpacific","cwten"],
  "<strong>California &middot; eight boxes &middot; $18 a grip</strong>Eastern design on golf grips: blossom, waves and raked sand, some carrying a line of Chinese verse. Every single grip is $18; sets save a little. Our <a href=\"/drops/brand-to-know-cloud-and-wind-golf\">Brand to Know</a> has the full story."),
 ("97golf", "97golf", ["t01sunday","j25links2","j25links","t01field","t01cord","tw97"],
  "<strong>Six grip lines &middot; $3.99&ndash;$9.99</strong>Earthy colors at prices that make a full regrip cheap. Six lines were in stock, every color of each one in a single box."),
 ("Gives Golf", "gives-golf", ["tide","orbit","prism","matrix","birdie","divot"],
  "<strong>Five grips and a divot tool &middot; $14&ndash;$40</strong>A small brand with five midsize patterned grips at $14 each. That is the whole range, so all of it is here."),
 ("Sweet Rollz", "sweet-rollz", ["lapina","sinatra","electric","hula","tuesday","muertos","swash","bethpage","backcountry"],
  "<strong>Nine putter grips &middot; $34.95</strong>Designer putter grips with prints you notice from the next green."),
 ("IOMIC", "iomic", ["sticky23","stickycamo","blackarmy","sticky18","evose","ix23","iclassic","absolutex"],
  "<strong>Japan &middot; eight boxes &middot; $14.50&ndash;$35.50</strong>Tacky grips molded in Japan, in more colors than anyone else here. Prices from IOMIC&rsquo;s US store."),
 ("Cadero", "cadero", ["cadduo","cadpent","cadmil","cadstars","cadmex","cadputt","cadab","cadbasic"],
  "<strong>Tokyo &middot; eight boxes &middot; &euro;10.90&ndash;&euro;34.90</strong>Grips from a company that started out making car tires in Shibuya, with a clear outer layer over the color and a pentagon groove for traction. Most go on with air instead of solvent. Prices in euros."),
]
N = 56
PQ = {
 "gives-golf": ("We were going to call it The Eagle but let&rsquo;s be honest, you&rsquo;re not quite there yet.", "Gives Golf, on The Birdie"),
 "cloud-and-wind": ("Find inner peace on the course.", "Cloud &amp; Wind Golf"),
 "cadero": ("We believe golf grips should not only be functional. They should also be fun!", "Cadero, on its story"),
 "sweet-rollz": ("Nothing goes better with birdies than a tasty taco.", "Sweet Rollz, on Tuesday"),
}
CAP = ""
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>A new grip is the cheapest way to make an old set feel new. <a href="/drops/the-niche-grip-report">Vol. 1</a> covered five small grip makers in August. Vol. 2 brings back RIPIT with everything it has launched since, and adds six more: Cloud &amp; Wind, 97golf, Gives Golf, Sweet Rollz, IOMIC and Cadero. Every colorway of a model sits in one box, so swipe through each gallery to see them all.</p>
    <p><strong>RIPIT</strong> is the art-grip brand of the group, with a 2026 Art Series by three artists and its first putter grips. <strong>Cloud &amp; Wind</strong> paints blossom, waves and raked sand onto grips in a way nobody else does, all at $18. <strong>97golf</strong> is the value play, with grips from $3.99. <strong>Gives Golf</strong> keeps it small: five grips, one price. <strong>Sweet Rollz</strong> makes nothing but putter grips, all of them loud. <strong>IOMIC</strong> is the tacky Japanese grip you have probably seen in a tour bag, and <strong>Cadero</strong>, from Tokyo, puts the color under a clear skin and installs with air.</p>
    <p><strong>Where to start: your wedges.</strong> If you are nervous about a loud grip, put it on your wedges first. They are the clubs you look down at most around the green, a fun grip there never fights with a matching driver and irons, and wedges get swapped out more often anyway. If you like it, work up the bag from there.</p>
    <p><strong>Getting them installed.</strong> You do not need a club fitter. PGA TOUR Superstore lists grip installation from $0.99 a club, and it will put on grips you bring in yourself, not just ones bought in the store. It is often done while you shop, and always within 48 hours of drop-off. Prices vary by location, so call your local store first.</p>
    <p>Everything was in stock on October 12, 2026, and only colors you could buy that day are listed.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Makers</span><span>Seven</span></div>
      <div class="sidebar-detail"><span class="l">Boxes</span><span>56</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>97golf TW97, $3.99</span></div>
      <div class="sidebar-detail"><span class="l">Priciest</span><span>IOMIC I-Classic putter, $35.50</span></div>
      <div class="sidebar-detail"><span class="l">Start with</span><span>Your wedges</span></div>
      <div class="sidebar-detail"><span class="l">Regrip</span><span>From $0.99 a club at PGA TOUR Superstore</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>RIPIT Coco, A$24.95</span></div>
      <div class="sidebar-detail"><span class="l">Vol. 1</span><span><a href="/drops/the-niche-grip-report">The Niche Grip Report</a></span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfGrips</span>
        <span class="hashtag">#RIPITGrips</span>
        <span class="hashtag">#CloudAndWindGolf</span>
        <span class="hashtag">#Regrip</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("How much are RIPIT grips in US dollars?", "RIPIT sells in Australian dollars. On October 12, 2026 its full-swing grips were A$24.95 (about $17) and its square-face putter grips A$49.95 (about $35)."),
 ("What are the cheapest grips in this list?", "97golf's TW97 Tour grips at $3.99 each, followed by its T01 Tour at $7.99 and its J25 Hybrid and T01 Cord at $9.99 (October 12, 2026)."),
 ("Does Sweet Rollz make full-swing grips?", "No. Every Sweet Rollz grip in this list is a putter grip, at $34.95, most in Midsize or Skinny."),
 ("How much are Cloud & Wind grips?", "Every single Cloud & Wind grip was $18 on October 12, 2026. A 3-grip set was $54, a 7-grip set $126 and 10-grip sets $160."),
 ("Where can I get new grips installed cheaply?", "PGA TOUR Superstore lists grip installation from $0.99 a club (grips not included) on its regripping page, read October 12, 2026. It will install grips you bring in, often while you wait and always within 48 hours. Prices vary by location."),
 ("Which clubs should get a fun grip first?", "Your wedges. They are the clubs you look at most around the green, a loud grip there does not clash with the rest of the bag, and wedges get replaced more often anyway."),
 ("Where are IOMIC grips made?", "IOMIC grips are made in Japan. Prices here are from IOMIC's US store: $14.50 for the Sticky 2.3 on October 12, 2026."),
]
HERO_ALT = "Three golf grip photos side by side: hands on a RIPIT Flower of Life grip, a Cloud &amp; Wind Blossom grip held among pink flowers, and a golfer holding a Sweet Rollz Electric Avenue putter grip"
FRN = json.loads((ROOT / "research/grips-vol2/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GV2-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-12", "dateModified": "2026-10-12",
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} boxes</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
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
    <span>Seven grip makers &middot; Vol. 2</span><span class="dot"></span>
    <span>56 boxes &middot; all in stock, checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Woodgrain", "Rookline", "Hudson", "LBB", "GolfPass", "Tarraing"):
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
