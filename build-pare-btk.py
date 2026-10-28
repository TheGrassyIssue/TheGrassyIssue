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
        "triangle that will remind you of Prada. 36 picks, including the colorful pieces that sold out.")
H1 = "Brand to Know: Paré Golf, Golf Through a Filipino-American Lens"  # Lenny 27 Oct: "selling out" reads negative
BC = "Brand to Know: Paré Golf"
SLUG = "brand-to-know-pare-golf"
IMG = "/images/pare-golf"
SHOP = "https://pare.golf/products/"
C = "Paré Golf"
SO = " &middot; sold out"
P = {
 # The Manila line
 "imp-walnut": (C, "Paré &times; Imperial Manila Hat, Walnut", "$55", "pare-x-imperial-manila-hat-walnut",
   "Our pick. Paré says it&rsquo;s the first Filipino-American company to partner with Imperial, and for the first release it put the Manila triangle on Imperial&rsquo;s performance cap: lightweight, moisture-wicking and UPF 50+. Released for the brand&rsquo;s third anniversary and Filipino American History Month. Walnut is the one we&rsquo;d buy."),
 "imp-white": (C, "Paré &times; Imperial Manila Hat, White", "$55", "pare-x-imperial-manila-hat-white",
   "The same Imperial cap in white, where the black-and-white triangle looks most like the plaque it&rsquo;s riffing on. The summer option."),
 "imp-black": (C, "Paré &times; Imperial Manila Hat, Black", "$55", "pare-x-imperial-manila-hat-black",
   "All black with the white triangle. It matches the black Manila mocknecks and the Bluetross covers, if you want the whole set."),
 "imp-olive": (C, "Paré &times; Imperial Manila Hat, Olive", "$55", "pare-x-imperial-manila-hat-olive",
   "Olive, the quietest of the four, and the one that goes with the most golf clothes."),
 "manila-mock": (C, "Manila Mockneck Shirt", "$70", "pare-manila-mockneck-shirt",
   "A black oversized mockneck with the Manila triangle on the chest, made in the USA. The product copy is four words long and gives the game away: &ldquo;The Devil Wears Paré.&rdquo;"),
 "manila-ls": (C, "Manila Long Sleeve Shirt", "$80", "pare-manila-long-sleeve-shirt",
   "The heavier 8oz long sleeve, boxy with a high neck, made in the USA from USA-grown cotton, with the Manila triangle on the chest. Same four-word description: &ldquo;The Devil Wears Paré.&rdquo;"),
 "bt-driver": (C, "Paré &times; Bluetross Driver Headcover", "$170", "pare-x-bluetross-driver-headcover",
   "Bluetross is known for leather headcovers made in the USA. For Paré it worked in waxed canvas for the first time, with the Manila triangle on the front."),
 "bt-putter": (C, "Paré &times; Bluetross Blade Putter Headcover", "$150", "pare-x-bluetross-blade-putter-headcover",
   "The blade cover from the same collaboration, in black waxed canvas with the triangle patch. The pair is the most grown-up thing Paré makes."),
 "manila-nylon": (C, "&ldquo;Manila&rdquo; Nylon Hat", "$45" + SO, "pare-manila-nylon-hat",
   "Where the triangle first went on a hat: a black nylon six-panel made and embroidered in New Jersey by Panther. The copy reads &ldquo;The Devil Wears Paré. Straight From Greenhills,&rdquo; the Manila shopping district."),
 "manila-visor": (C, "Manila Tour Visor (HYPEGOLF Exclusive)", "$55" + SO, "hypegolf-exclusive-pare-manila-tour-visor",
   "A visor made with Tour Visor for Paré&rsquo;s HYPEGOLF drop in August 2026, with the triangle on the front and a sweatband inside. Made in the USA, and gone fast."),
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
 ("The Manila Line", "manila", ["imp-walnut", "imp-white", "imp-black", "imp-olive", "manila-mock", "manila-ls", "bt-driver", "bt-putter", "manila-nylon", "manila-visor"],
  "<strong>Ten pieces &middot; $55&ndash;$170</strong>The triangle logo: four Imperial caps, two shirts, two Bluetross covers and two pieces that already sold out."),
 ("The Paré Boy", "pare-boy", ["paretex", "maganda", "sock"],
  "<strong>Three pieces in stock &middot; $20&ndash;$70</strong>The drawing of the kid putting: the founder as a boy, on the green in his Girbaud jean shorts."),
 ("The Clothes", "clothes", ["club", "wind", "plisse2", "plisse", "adobo", "forgood", "eldrick", "gulay", "logotee"],
  "<strong>Nine pieces &middot; $55&ndash;$160</strong>Oversized mocknecks, pleated pants, a wind shirt and the first collared shirt. Most are made in the USA."),
 ("Sold Out: The Colorful Stuff", "sold-out", ["am94", "azalea", "eggsalad", "magnolia", "faces", "maasim", "pakwan", "pink", "barnabys", "mogshade", "toddler", "sunflower", "pgg", "camphat"],
  "<strong>Fourteen pieces you can&rsquo;t buy right now</strong>86 of Paré&rsquo;s 112 products were sold out when we checked, and the loudest ones went first. Prices are what they sold for. Paré does restock some pieces, so watch the drops."),
]
N = 36
PQ = {
 "pare-boy": ("Golf, growing up was so stuffy, and I stood out.", "Matt Sakdalan, to MyGolfSpy, 2025"),
 "sold-out": ("I&rsquo;m here to just kind of change your perspective on what golf could look like, especially from a Filipino lens.", "Matt Sakdalan, to MyGolfSpy, 2025"),
}
BANDS = {
 "manila-after": ("The fall campaign", "From Paré&rsquo;s fall 2026 shoot: the Manila caps, the Bluetross covers, the Gulay hoodies and the Plissé pants.",
   [("lb-duo-bluetross", "Two people in black Manila tees and grey Plissé pants on stools holding the Bluetross driver and putter covers", "The Bluetross covers, fall 2026"),
    ("lb-walnut", "A man in a brown tee pulling down the walnut Imperial Manila cap", "The walnut Imperial cap"),
    ("lb-putter", "A man in a black Manila tee holding the Bluetross putter cover up to the camera", "The blade putter cover"),
    ("lb-hoodies", "Two people in forest green Gulay hoodies and green trousers standing together", "Two Gulay hoodies"),
    ("lb-crouch", "A woman in a black Manila long sleeve, grey Plissé pants and a black cap crouching", "The Manila long sleeve and Plissé pants"),
    ("lb-gulay", "A woman in the green Gulay hoodie and grey Plissé pants crouching with a hand on her chin", "The Gulay hoodie")]),
 "sold-out-before": ("Out in the world", "Two of the sold-out collaborations, as the brands shot them: the Little Sundays toddler bag on a course, and the Paris Golf Gallery hat in Paris.",
   [("irl-ls-bag", "A small child in pink trousers standing on a fairway with the pastel Little Sundays x Paré toddler bag", "Little Sundays &times; Paré, on the course"),
    ("irl-ls-walk", "A child from behind carrying the pastel toddler bag across a fairway toward trees", "The toddler bag, carried properly"),
    ("irl-ls-green", "A child walking across a green past a bunker carrying the toddler bag", "Past the bunker"),
    ("irl-pgg-1", "A man in a pink long sleeve and the cream Paris Golf Gallery x Paré cap looking down", "Paris Golf Gallery &times; Paré, Paris"),
    ("irl-pgg-2", "A man in a pink long sleeve and the cream Paris Golf Gallery x Paré cap smiling at the camera", "The Paris Fashion Week cap"),
    ("irl-pgg-3", "A man in a pink long sleeve and shorts adjusting his cap against a pale blue wall", "Photos: Paris Golf Gallery")]),
 "pare-boy": ("The name", "From Paré&rsquo;s About page: what the colors mean, and the hats that wear them.",
   [("band-flag", "Yellow card reading Yellow equals the sun, Pink plus blue equals the flag, with PARÉ in pink and blue", "Yellow is the sun; pink and blue are the flag"),
    ("band-hats", "A row of Paré nylon hats in orange, black, neon yellow and pink on a wooden shelf", "The hats, in the flag&rsquo;s colors and then some"),
    ("band-walk", "A golfer in the pink-and-white striped 94 AM Sensation mockneck walking across a fairway in evening light", "The 94 AM Sensation, out on the course")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Paré is golf seen through Filipino-American eyes, and it doesn&rsquo;t hide it. The word is Tagalog slang for buddy, and founder Matt Sakdalan likes that it also reads as par plus an E, for even. The colors are the pastels of the Philippine flag. The products are named after food and slang: Ube, Adobo, Gulay, Pakwan, Kanin. The brand calls itself &ldquo;an on-going creative outlet paying homage to the love of golf, streetwear, and Filipino culture,&rdquo; and that is exactly what the store looks like.</p>
    <p><strong>The kid putting.</strong> The best thing Paré has is its Paré Boy logo, a line drawing of a small golfer leaning over a putt. It&rsquo;s the founder himself as a kid; the product copy says it shows him putting &ldquo;in my Girbaud Jean Shorts.&rdquo; It turns up on mocknecks, socks, a towel, a tote and the new waterproof hat, and it&rsquo;s the reason we kept clicking.</p>
    <p><strong>About that triangle.</strong> The other logo, the Manila triangle on the Imperial caps, the Bluetross covers and the black mocknecks, looks a lot like Prada&rsquo;s triangle plaque. We don&rsquo;t think that&rsquo;s an accident, and neither, it seems, does Paré: the Manila mockneck&rsquo;s whole product description is &ldquo;The Devil Wears Paré.&rdquo;</p>
    <p><strong>Limited drops.</strong> Sakdalan played college golf at Gordon College, put the first hat up for sale in November 2023 and has run the brand in limited drops ever since. When we checked, 86 of its 112 products were sold out, including most of the colorful pieces, which is why they get their own section below. The hats are made and embroidered in New Jersey, and the tees, long sleeves and hoodies are made in the USA. The collaborations are strong for a brand this young: Imperial, Bluetross, Mogshade, Barnaby&rsquo;s, Little Sundays and Paris Golf Gallery, which brought Paré to Paris Fashion Week in 2025.</p>
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
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">From a Fortune Cookie to Paris</h2>
  <div class="writeup-body">
    <p>Sakdalan carried the idea for more than ten years before he did anything with it. He worked at pharma media agencies and then in the sneaker industry, and when that company folded and let him go with severance, he told his old college, Gordon, that a Panda Express fortune cookie he opened with his wife read like an instruction. He took it as one. The PARE GOLF trademark was filed in October 2023, and the first product went up that November.</p>
    <p>That first product was the 5-Panel Camp Hat, which the brand calls &ldquo;my first baby&rdquo; and traces back to Sakdalan&rsquo;s early obsession with Supreme. The first piece of clothing came next: the &ldquo;94 AM Sensation&rdquo; mockneck, a pink-and-white stripe borrowed from Tiger&rsquo;s 1994 U.S. Amateur, cut oversized and cropped from samples he bought in Japan. Both are long sold out, and both are in the section at the bottom of this page.</p>
    <p>The drawings are by Nith, whom Sakdalan calls his partner in crime. Nith drew the Paré Boy, and the brand&rsquo;s About page says the logo and the wordmark tip their hat to PING and Karsten Solheim, whose own logo is a little man putting. Nith also designed the &ldquo;Faces&rdquo; rope hat, printed so randomly that no two of the 100 match.</p>
    <p>The Paris chapter started on Instagram. Pierre Greilsamer of Paris Golf Gallery followed Paré, in Sakdalan&rsquo;s words, &ldquo;before I even had a product,&rdquo; and later connected him with Gwop, a golf swap meet. That led to a Paré showing during Paris Fashion Week 2025 in the Cadillac building beside the Paris Opera, and to the Paris Golf Gallery hat. &ldquo;Generating some sort of Filipino representation out there was always part of our mission,&rdquo; he told Gordon College afterward.</p>
    <p>Paré also runs a members tier it calls Kapamilya, Tagalog for family, with some pieces sold only to members and at lower prices. We&rsquo;ve left those out because you can&rsquo;t buy them without joining. As recently as July 2024 Sakdalan was still calling Paré his side gig, and his one regret, he told Kollective Hustle, is not starting earlier: &ldquo;Only thing I would&rsquo;ve done differently is start sooner.&rdquo;</p>
  </div>
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
FRN = json.loads((ROOT / "research/pare/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-27", "dateModified": "2026-10-27",
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
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Brand to Know &middot; First drop November 2023</span><span class="dot"></span>
    <span>36 picks, 16 of them sold out &middot; checked October 27, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer in the pink-striped 94 AM Sensation mockneck on a fairway, the striped shirt with a Paré glove, and a lilac mockneck on a hanger with the Paré Boy putting logo" fetchpriority="high" /></div></div>
"""
    body += TAKE + STORY
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
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
