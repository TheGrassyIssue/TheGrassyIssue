#!/usr/bin/env python3
"""build-pare-btk.py — Brand to Know: Paré Golf. 27 October 2026. Cloned from build-whim-btk.py.
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Paré Golf, Filipino Pastels and the Kid Putting in Jorts"
DESC = ("Paré Golf mixes golf, streetwear and Filipino culture: Philippine-flag pastels, the Paré Boy putting logo and a Manila "
        "triangle that will remind you of Prada. 30 picks, including the colorful pieces that sold out.")
H1 = "Brand to Know: Paré Golf, the Filipino-American Brand That Keeps Selling Out"
BC = "Brand to Know: Paré Golf"
SLUG = "brand-to-know-pare-golf"
IMG = "/images/pare-golf"
SHOP = "https://pare.golf/products/"
C = "Paré Golf"
SO = " &middot; sold out"
P = {
 # The Manila line
 "imperial": (C, "Paré &times; Imperial Manila Hat", "$55", "pare-x-imperial-manila-hat-walnut",
   "Our pick. Paré says it&rsquo;s the first Filipino-American company to partner with Imperial, and for the first release it put the Manila triangle on Imperial&rsquo;s performance cap: lightweight, moisture-wicking and UPF 50+. Walnut, white, black or olive, released for the brand&rsquo;s third anniversary and Filipino American History Month."),
 "manila-mock": (C, "Manila Mockneck Shirt", "$70", "pare-manila-mockneck-shirt",
   "A black oversized mockneck with the Manila triangle on the chest, made in the USA. The product copy is four words long and gives the game away: &ldquo;The Devil Wears Paré.&rdquo;"),
 "bt-driver": (C, "Paré &times; Bluetross Driver Headcover", "$170", "pare-x-bluetross-driver-headcover",
   "Bluetross is known for leather headcovers made in the USA. For Paré it worked in waxed canvas for the first time, with the Manila triangle on the front."),
 "bt-putter": (C, "Paré &times; Bluetross Blade Putter Headcover", "$150", "pare-x-bluetross-blade-putter-headcover",
   "The blade cover from the same collaboration, in black waxed canvas with the triangle patch. The pair is the most grown-up thing Paré makes."),
 # Paré Boy
 "paretex": (C, "PARÉ-TEX Waterproof 5-Panel Long Bill Hat", "$70", "pare-tex-waterproof-5-panel-long-bill-hat",
   "The brand&rsquo;s first technical piece: a waterproof five-panel with a long bill, built for bad weather. Black, with the Paré Boy drawn on the front."),
 "maganda": (C, "Maganda Ang Buhay Mockneck Shirt", "$70", "pare-maganda-ang-buhay-mockneck-shirt",
   "&ldquo;Golf is life. And life is good,&rdquo; says the copy, which is roughly what maganda ang buhay means. A white oversized mockneck with a big Paré Boy on the chest, made in the USA."),
 "sock": (C, "White Crew Sock", "$20", "pare-logo-crew-sock-v2",
   "Cotton crew socks, made in the USA, with the Paré Boy on the sides. Version two, and the brand says it&rsquo;s &ldquo;way better.&rdquo; The cheapest way to wear the logo."),
 # Clothes
 "club": (C, "Club Shirt", "$120", "pare-club-shirt",
   "&ldquo;We finally made a collared shirt. Don&rsquo;t worry, we&rsquo;re not getting too serious.&rdquo; Tan olive with a striped ribbed collar and curved seams, in a relaxed cut. The newest thing in the store."),
 "wind": (C, "&ldquo;Cool Grey&rdquo; Short Sleeve Wind Shirt", "$130", "pare-cool-grey-short-sleeve-wind-shirt",
   "A grey half-zip wind shirt in lightweight polyester with snaps and zip side pockets. The founder&rsquo;s note recommends it for Ballyowen and says the tariffs &ldquo;were no joke on this bad boy.&rdquo; Only a small was left when we checked."),
 "plisse2": (C, "Plissé Pants 2.0", "$150", "pare-plisse-pants-2-0",
   "The pleated pant again, with deeper pleats, belt loops, bigger pockets and a tapered leg. Light grey, and the easiest way into the brand if you already own enough hats."),
 "plisse": (C, "Plissé Pants", "$100", "pare-plisse-pants",
   "The original: pleated, elastic-waisted, drawstring, and in the founder&rsquo;s words &ldquo;MEANT FOR ALL.&rdquo; Off-white, down to an XL when we checked."),
 "adobo": (C, "Adobo Mockneck Shirt", "$70", "pare-adobo-mockneck-shirt",
   "A brown oversized mockneck named after the Filipino dish. The whole description: &ldquo;Chicken or pork?&rdquo; Made in the USA."),
 "forgood": (C, "For Good Long Sleeve Shirt", "$60", "pare-for-good-long-sleeve-shirt",
   "A forest green long sleeve with &ldquo;Paré goes good with green&rdquo; printed on it, made in the USA. The copy just says &ldquo;WICKED SEASON!!! THANK GOODNESS!!!&rdquo;"),
 "eldrick": (C, "Blonde Eldrick Long Sleeve Shirt", "$75", "pare-blonde-eldrick-long-sleeve-shirt",
   "A grey long-sleeve mockneck with a small box graphic on the chest. Eldrick is Tiger&rsquo;s first name; the copy says only &ldquo;IYKYK.&rdquo;"),
 "gulay": (C, "Gulay Hooded Pullover Sweatshirt", "$160", "pare-gulay-hooded-pullover-sweatshirt",
   "A 16oz forest green hoodie made in the USA, named for the Tagalog word for vegetables. The kangaroo pocket, per the copy, is for your baon or pasalubong."),
 "logotee": (C, "Golf Logo T-Shirt", "$55", "pare-classic-new-york-logo-t-shirt",
   "An 8oz white tee with a mock neck and the lowercase paré wordmark, made in the USA from USA-grown cotton. &ldquo;Recognize the font? IYKYK.&rdquo;"),
 # Sold out, the colorful stuff
 "am94": (C, "&ldquo;94 AM Sensation&rdquo; Mockneck", "$80" + SO, "pare-94-am-sensation-mockneck",
   "Paré&rsquo;s first cut-and-sew piece: a pink-and-white striped mockneck, oversized and cropped, inspired by the striped polo Tiger wore at the 1994 U.S. Amateur. The neck is cut wider than usual, &ldquo;for them thicc necks like me.&rdquo;"),
 "azalea": (C, "Azalea Mockneck", "$80" + SO, "pare-azalea-mockneck",
   "Bright azalea pink, released ahead of Masters week with the Paré Boy on the chest. The founder&rsquo;s note: &ldquo;We look forward to this time of year. Except pollen.&rdquo;"),
 "eggsalad": (C, "Egg Salad Mockneck", "$80" + SO, "pare-egg-salad-mockneck",
   "The same spring mockneck in pale yellow, with the kid putting on the chest."),
 "magnolia": (C, "Magnolia Mockneck", "$80" + SO, "pare-magnolia-mockneck",
   "The third spring colorway, a bright green. Paré also sold all three together as a bundle."),
 "faces": (C, "&ldquo;Faces&rdquo; Rope Hat", "$60" + SO, "pare-faces-rope-hat",
   "Designed by Nith, the brand&rsquo;s designer, to show people from the founder&rsquo;s life and people who inspire him. The print came out randomized on every panel, so each of the 100 hats is one of a kind."),
 "maasim": (C, "&ldquo;MAASIM&rdquo; Nylon Hat", "$36" + SO, "pare-maasim-nylon-hat",
   "Neon lime nylon with the PARÉ letters in pink and blue. Maasim means sour; the copy just says &ldquo;Calamansheeeeeesh!&rdquo; Every one came out a little different in the wash."),
 "pakwan": (C, "&ldquo;PAKWAN&rdquo; Snapback Hat", "$42" + SO, "pare-pakwan-snapback-hat",
   "Watermelon green with pink lettering, from Paré&rsquo;s first snapback series, made in the USA. Pakwan is watermelon; the copy is a watermelon joke."),
 "pink": (C, "Pink Nylon Hat", "$40" + SO, "pare-pink-nylon-hat",
   "From the &ldquo;This Is My Jumpman&rdquo; collection, a pink nylon six-panel designed and embroidered in New Jersey. The founder&rsquo;s note calls it his personal favorite."),
 "barnabys": (C, "Barnaby&rsquo;s &times; Paré Driver Headcover", "$55" + SO, "barnabys-x-pare-driver-headcover",
   "Butter yellow with PARÉ scribbled across it in pink and blue. It was Paré&rsquo;s first headcover and, per the brand, Barnaby&rsquo;s first public release that wasn&rsquo;t a glove."),
 "mogshade": (C, "Paré &times; Mogshade Driver Headcover", "$135" + SO, "pare-x-mogshade-driver-headcover",
   "Made in Portugal from rescued wool with a deadstock fleece lining, in a pattern built from the flag&rsquo;s pastels and a hint of ube. Two years in the making, and gone this month."),
 "toddler": (C, "Little Sundays &times; Paré Toddler Golf Bag", "$100" + SO, "little-sundays-x-pare-toddler-golf-bag",
   "A golf bag for kids up to five, in the pastel colors of the Philippines, with both brands embroidered on it. Probably the most colorful thing on this page."),
 "sunflower": (C, "Sunflower Mockneck Long Sleeve Shirt", "$75" + SO, "sunflower-mockneck-long-sleeve-shirt",
   "From the one-year anniversary collection: a cream long-sleeve mockneck with a sunflower graphic, made in honor of the founder&rsquo;s mother-in-law."),
 "pgg": (C, "Paré &times; Paris Golf Gallery Snapback Hat", "$50" + SO, "pare-x-paris-golf-gallery-snapback-hat",
   "Designed with Paris Golf Gallery for Paré&rsquo;s showing at Paris Fashion Week 2025. Nylon, moisture-wicking, and in the copy&rsquo;s words, &ldquo;just absolutely money.&rdquo;"),
 "camphat": (C, "5-Panel Camp Hat", "$45" + SO, "5-panel-camp-hat",
   "Where it started, in November 2023. The founder calls it &ldquo;my first baby&rdquo;, and his friend Jose promised &ldquo;You will not look like a train conductor.&rdquo;"),
}
SECTIONS = [
 ("The Manila Line", "manila", ["imperial", "manila-mock", "bt-driver", "bt-putter"],
  "<strong>Four pieces &middot; $55&ndash;$170</strong>The triangle logo, on an Imperial cap, a mockneck and two Bluetross covers."),
 ("The Paré Boy", "pare-boy", ["paretex", "maganda", "sock"],
  "<strong>Three pieces in stock &middot; $20&ndash;$70</strong>The drawing of the kid putting: the founder as a boy, on the green in his Girbaud jean shorts."),
 ("The Clothes", "clothes", ["club", "wind", "plisse2", "plisse", "adobo", "forgood", "eldrick", "gulay", "logotee"],
  "<strong>Nine pieces &middot; $55&ndash;$160</strong>Oversized mocknecks, pleated pants, a wind shirt and the first collared shirt. Most are made in the USA."),
 ("Sold Out: The Colorful Stuff", "sold-out", ["am94", "azalea", "eggsalad", "magnolia", "faces", "maasim", "pakwan", "pink", "barnabys", "mogshade", "toddler", "sunflower", "pgg", "camphat"],
  "<strong>Fourteen pieces you can&rsquo;t buy right now</strong>86 of Paré&rsquo;s 112 products were sold out when we checked, and the loudest ones went first. Prices are what they sold for. Paré does restock some pieces, so watch the drops."),
]
N = 30
PQ = {
 "pare-boy": ("Golf, growing up was so stuffy, and I stood out.", "Matt Sakdalan, to MyGolfSpy, 2025"),
 "sold-out": ("I&rsquo;m here to just kind of change your perspective on what golf could look like, especially from a Filipino lens.", "Matt Sakdalan, to MyGolfSpy, 2025"),
}
BANDS = {
 "pare-boy": ("The name", "From Paré&rsquo;s About page: what the colors mean, and why the E has an accent.",
   [("band-flag", "Yellow card reading Yellow equals the sun, Pink plus blue equals the flag, with PARÉ in pink and blue", "Yellow is the sun; pink and blue are the flag"),
    ("band-e", "Yellow card with a large pale blue É and the words So you don't say", "The accent, so you say it right"),
    ("band-walk", "A golfer in the pink-and-white striped 94 AM Sensation mockneck walking across a fairway in evening light", "The 94 AM Sensation, out on the course")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Paré is golf seen through Filipino-American eyes, and it doesn&rsquo;t hide it. The word is Tagalog slang for buddy, and founder Matt Sakdalan likes that it also reads as par plus an E, for even. The colors are the pastels of the Philippine flag. The products are named after food and slang: Ube, Adobo, Gulay, Pakwan, Kanin. The brand calls itself &ldquo;an on-going creative outlet paying homage to the love of golf, streetwear, and Filipino culture,&rdquo; and that is exactly what the store looks like.</p>
    <p><strong>The kid putting.</strong> The best thing Paré has is its Paré Boy logo, a line drawing of a small golfer leaning over a putt. It&rsquo;s the founder himself as a kid; the product copy says it shows him putting &ldquo;in my Girbaud Jean Shorts.&rdquo; It turns up on mocknecks, socks, a towel, a tote and the new waterproof hat, and it&rsquo;s the reason we kept clicking.</p>
    <p><strong>About that triangle.</strong> The other logo, the Manila triangle on the Imperial caps, the Bluetross covers and the black mocknecks, looks a lot like Prada&rsquo;s triangle plaque. We don&rsquo;t think that&rsquo;s an accident, and neither, it seems, does Paré: the Manila mockneck&rsquo;s whole product description is &ldquo;The Devil Wears Paré.&rdquo;</p>
    <p><strong>It sells out.</strong> Sakdalan played college golf at Gordon College, put the first hat up for sale in November 2023 and has run the brand in limited drops ever since. When we checked, 86 of its 112 products were sold out, including most of the colorful pieces, which is why they get their own section below. The hats are made and embroidered in New Jersey, and the tees, long sleeves and hoodies are made in the USA. The collaborations are strong for a brand this young: Imperial, Bluetross, Mogshade, Barnaby&rsquo;s, Little Sundays and Paris Golf Gallery, which brought Paré to Paris Fashion Week in 2025.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Matt Sakdalan</span></div>
      <div class="sidebar-detail"><span class="l">First drop</span><span>November 2023</span></div>
      <div class="sidebar-detail"><span class="l">Name</span><span>Tagalog for buddy</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>USA (hats in New Jersey)</span></div>
      <div class="sidebar-detail"><span class="l">In stock</span><span>26 of 112 products</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$20&ndash;$170</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Imperial Manila Hat</span></div>
      <div class="hashtags">
        <span class="hashtag">#PareGolf</span>
        <span class="hashtag">#PareBoy</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What does Paré mean?", "It's Tagalog slang for buddy or friend. Founder Matt Sakdalan also points out that it reads as par plus E, for even."),
 ("Who founded Paré Golf?", "Matt Sakdalan, a Filipino-American golfer who played college golf at Gordon College. The first Paré product, the 5-Panel Camp Hat, went on sale in November 2023."),
 ("Who is the Paré Boy?", "The line drawing of a kid putting is the founder himself as a boy. Paré's product copy describes it as him putting in his Girbaud jean shorts."),
 ("Is the Paré Manila logo based on Prada?", "Paré hasn't said so, but the Manila triangle looks a lot like Prada's triangle plaque, and the Manila mockneck's product description is simply \"The Devil Wears Paré.\""),
 ("Where is Paré Golf made?", "Its snapbacks and nylon hats are made and embroidered in New Jersey, and its tees, long sleeves, hoodies and socks are made in the USA. The Mogshade headcovers were made in Portugal."),
 ("Why is so much of Paré sold out?", "The brand works in limited drops. On October 27, 2026, 86 of its 112 products were sold out, including most of the colorful hats, mocknecks and headcovers."),
]
LOOKBOOK = ""
