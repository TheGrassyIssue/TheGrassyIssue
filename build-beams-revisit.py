#!/usr/bin/env python3
"""build-beams-revisit.py — Brand Revisited: BEAMS Golf. 30 October 2026. Cloned from build-angus-grace-btk.py.
Lenny: "let's do a beams golf revisited" -> options sheet (36) -> "add items from .../special/bb100/outdoor&sports/" (+11) -> "Let's build the post".
No picks given: built from every in-stock option (Trouper 3.0, Malbon anorak, check coach jacket and the UGG boot were sold out; Electric
reversible and the Pilgrim sacoche dropped to keep rows of 3; Harris Tweed cart bag added). 42 cards.
FACTS: beams.co.jp product pages (JPY, read in Chrome 30 Oct 2026; ~US$ at 156 yen); BEAMS Golf blog (FW26 "THE GREATEST HITS", Aug 17;
BRIEFING woodland camo, July); Fashionsnap Oct 8 2026 (SUN DAY RED partnership); Golf Digest Bruder Oct 28 (Malbon archive);
Senken Shimbun Oct 21 2025 (Nishiwaki now former director, BEAMS Creative, New Vintage Golf); Bunshun Nov 28 2019 + WWD Japan Aug 28 2024
(quotes, translated by TGI). WorldShopping international checkout banner seen live on beams.co.jp Oct 30. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "BEAMS Golf Revisited: Sun Day Red, the 50th and 42 New Picks"
DESC = ("Back to BEAMS Golf: Tiger Woods' Sun Day Red lands in Japan through BEAMS, a 50th-anniversary run of Jones, Lacoste and Baracuta specials, "
        "a Malbon archive drop and 42 picks, with yen prices.")
H1 = "Brand Revisited: BEAMS Golf at 15"
BC = "Brand Revisited: BEAMS Golf"
SLUG = "brand-revisited-beams-golf"
IMG = "/images/beams-golf-revisit"
SHOP = "https://www.beams.co.jp/item/"
BG = "BEAMS Golf"
def Y(y): return f"&yen;{y:,} (~${round(y / 156)})"
P = {
 "81610479334": ("Jones Sports x BEAMS Golf", "RIDER BLUE Caddie Bag", Y(99000), "81610479334/",
   "The 50th-anniversary bag. BEAMS asked Jones for a special Rider in off-white and blue as an homage to a famous sneaker, with metal hardware and an 8.5-inch top. It is the headline of BEAMS&rsquo; Jones &ldquo;Blue&rdquo; collection."),
 "82120067462": ("Lacoste x BEAMS Golf", "Long-Sleeve Knit Polo", Y(26400), "82120067462/",
   "Our pick. A classic 100% wool knit polo, fully special-ordered, with one detail that only exists this year: for BEAMS&rsquo; 50th, the logo inside the crocodile patch reads BEAMS. Several colors."),
 "82180255493": ("Baracuta x BEAMS Golf", "G4 Tree Camo Blouson", Y(39600), "82180255493/",
   "BEAMS&rsquo; first Baracuta special in several years, made for the 50th. A clean navy G4, the model without a ribbed hem so it sits right over a swing, with an original tree-camo print hidden in the lining and a dog-ear collar to keep the wind out."),
 "82130357411": ("Jones Sports x Champion x BEAMS Golf", "Reverse Weave Crew", Y(19800), "82130357411/",
   "A three-way special on Champion&rsquo;s Reverse Weave body, with a big collegiate Jones logo on the front in a different typeface for each color. Made for the 50th and as at home in town as on the range."),
 "82180263411": ("Champion x BEAMS Golf", "Warm-Up Piste Jacket", Y(24200), "82180263411/",
   "A fully special-ordered pullover &ldquo;piste,&rdquo; the warm-up jacket Champion and BEAMS Golf keep coming back to, with an updated version of its big back print. A side zip from hem to underarm opens for air and makes it easy to pull on and off."),
 "81041029467": ("Malbon x BEAMS Golf", "Archive Buckets Driver Cover", Y(33000), "81041029467/",
   "The Malbon piece in BEAMS&rsquo; 50th list: grained cowhide embroidered all over with every Buckets logo from their past special orders, plus a stars-and-stripes M on top. It doubles as a history of the collaboration."),
 "81411362467": ("Malbon x BEAMS Golf", "First Buckets Bucket Hat", Y(16500), "81411362467/",
   "From the October 28 archive drop: Malbon&rsquo;s Buckets mascot in a green hunting cap, the graphic from the pair&rsquo;s first collaboration, brought back for the anniversary. Packable, with the old script logo on the back."),
 "82020722467": ("Malbon x BEAMS Golf", "First Buckets Polo", Y(27500), "82020722467/",
   "The same revived Hunting Buckets graphic, in green, embroidered on a high-stretch nylon and polyurethane pique polo. Selling through; check sizes."),
 "82180281357": ("Quiet Golf x BEAMS Golf", "Half-Zip Pullover", Y(42900), "82180281357/",
   "A fully special-ordered half zip, cut from its own pattern, with a stand collar, side pockets and a back print that merges the Quiet Golf name with a globe. In burgundy and black."),
 "82230441060": ("Lee x BEAMS Golf", "Westerner Pants", Y(24200), "82230441060/",
   "Lee made the Westerner in 1959 as dress-up wear for cowboys, and Ivy League students made it a hit in the 1960s. BEAMS Golf brought back its own past special order with a straighter cut, closer to the original, and modern golf details."),
 "81510016221": ("Tomo &amp; Co. x BEAMS Golf", "Western Belt", Y(25300), "81510016221/",
   "The second special with designer Tomotaka Onozaki: a western belt modeled on the ones PGA Tour players wore in the 1990s, with &ldquo;Drive for show, Putt for dough&rdquo; stamped on the tip."),
 "81411390499": ("Yoshinori Kotake x BEAMS Golf", "Serge Cap", Y(12100), "81411390499/",
   "An Orange Label cap from the Tokyo hat designer, with a raised gothic B, a shield and globe embroidered on the side and a pile sweatband."),
 "81411417412": ("J.Press x Poten x BEAMS Golf", "Baseball Cap", Y(9900), "81411417412/",
   "Three Japanese names on one cap: a J.Press emblem, a classic six-panel shape, and construction by Poten, the workshop that makes caps for pro baseball players. Wear it with a blazer."),
 "82230453585": ("Gramicci x BEAMS Golf", "Corduroy Pants", Y(19800), "82230453585/",
   "Last year&rsquo;s popular special order, back in this season&rsquo;s colors, with Gramicci&rsquo;s one-hand webbing belt and a new glove holder."),
 "82180265402": ("Marmot x BEAMS Golf", "Fleece Blouson", Y(29700), "82180265402/",
   "Marmot&rsquo;s outdoor fleece reworked for golf, with military-style patches on the shoulders and elbows, contrast piping and enough room to swing."),
 "84150122529": ("BEAMS Golf Purple Label", "Return British Mock-Neck Knit", Y(24200), "84150122529/",
   "Purple Label&rsquo;s fall theme is Return British. This is the base layer: a polyester knit with a clean, cut-and-sew look, in this season&rsquo;s crayon colors and burgundy."),
 "84150123529": ("BEAMS Golf Purple Label", "Return British Knit", Y(27500), "84150123529/",
   "A sweatshirt-shaped knit with a jacquard Return British crest, in a warm wool-blend double jacquard. BEAMS suggests it with knickerbockers for what it calls a &ldquo;strange classic&rdquo; look."),
 "84180120529": ("BEAMS Golf Purple Label", "Combination Knit Blouson", Y(30800), "84180120529/",
   "British-trad blouson in TUMUGITO, a fabric with the feel of wool that you can wash at home, with ribbed collar, cuffs and hem."),
 "84230254803": ("BEAMS Golf Purple Label", "Windproof Knickerbockers", Y(28600), "84230254803/",
   "The most Purple Label thing in the line: windproof plus fours with tucks at the waist, made to be worn with high socks."),
 "84230256803": ("BEAMS Golf Purple Label", "6-Pocket Corduroy Pants", Y(25300), "84230256803/",
   "Corduroy woven with a zigzag pattern, with six pockets so the scorecard and tees have a place to go."),
 "81411371863": ("BEAMS Golf Purple Label", "Hunting Cap", Y(11000), "81411371863/",
   "A traditional flat cap in a cleaner shape, with a small embroidered logo on the side and an adjuster at the back. It finishes the Return British look."),
 "82150159647": ("BEAMS Golf Orange Label", "Varsity Knit Blouson", Y(29700), "82150159647/",
   "U.S. Traditional, the late-fall theme, in one piece: a windproof knit cut like a stadium jacket, with chain-stitched letter patches, a pennant and striped ribs, on raglan sleeves for the swing."),
 "82180240336": ("BEAMS Golf Orange Label", "College Stadium Blouson", Y(39600), "82180240336/",
   "A padded stadium jacket with BEAMS GOLF across the chest in sewn-on fabric letters, not a print. Warm enough for a cold round and easy to wear in town."),
 "82120062444": ("BEAMS Golf Orange Label", "Long-Sleeve Twill Polo", Y(23100), "82120062444/",
   "A long-sleeve double-jacquard polo with a small chest logo and a compact collar. The simple one in a loud line."),
 "84180106803": ("BEAMS Golf B.G.THREE", "ALL-TIME Golfer&rsquo;s Jacket", Y(42900), "84180106803/",
   "The city-to-course label at its most useful: a boxy, unvented jacket in a water-repellent, wrinkle-resistant stretch fabric that packs into its own back pocket. BEAMS says it works for business, too."),
 "84150121120": ("BEAMS Golf B.G.THREE", "ALL-TIME Windproof Crew Knit", Y(28600), "84150121120/",
   "A plain black crewneck with a windproof lining behind the knit. No logo you can see from across the fairway."),
 "82150171705": ("The Golfer&rsquo;s Journal at BEAMS Golf", "Broken Tee Society Crew", Y(30250), "82150171705/",
   "A 14-gauge merino crewneck from The Golfer&rsquo;s Journal, inspired by the great players of the past, with jacquard stripes at the cuffs and hem and a metal logo rivet."),
 "81040988629": ("BEAMS Golf", "Harris Tweed Driver Cover", Y(13200), "81040988629/",
   "New on October 30: Harris Tweed with faux leather and a chenille BG patch. The back gathers so it stays on in the cart."),
 "81610485629": ("BEAMS Golf", "Harris Tweed Tote", Y(17600), "81610485629/",
   "A tall tote in Harris Tweed, in herringbone or check, with a pennant patch and a base that stands up on its own."),
 "81610486629": ("BEAMS Golf", "Harris Tweed Cart Bag", Y(14300), "81610486629/",
   "The cart bag version, with the BG patch on the front, a Harris Tweed orb tag on the back, a zip top and tougher fabric where it gets dirty."),
 "81610399833": ("BEAMS Golf", "Black Watch Stand Bag", Y(53900), "81610399833/",
   "One of BEAMS Golf&rsquo;s best-selling accessories: a 14-club stand bag in its own Black Watch tartan, with waterproof zips, seven pockets and custom hardware."),
 "81610402833": ("BEAMS Golf", "Black Watch Boston Bag", Y(24200), "81610402833/",
   "The matching weekender, with a separate shoe compartment built into the side."),
 "81320568221": ("Tomo &amp; Co. at BEAMS Golf", "Pull-Tab Bit Loafer", Y(69300), "81320568221/",
   "For the clubhouse: Dupuy box calf in black and white, with a soda-can pull tab standing in for the horsebit."),
 "36130314101": ("Pilgrim Surf+Supply", "Watkins Fleece Popover", Y(33000), "36130314101/",
   "From BEAMS&rsquo; outdoor shop. A wool and angora pile knit made in the Bishu region of Japan, with a jacquard pattern inspired by the raked sand of a Zen garden."),
 "36180962049": ("NANGA x Pilgrim Surf+Supply", "Expedition Down Hoodie", Y(68200), "36180962049/",
   "NANGA calls its down jackets &ldquo;wearable sleeping bags.&rdquo; This is the second version of a 1990s-inspired expedition hoodie, cut short, with a black zip. A pre-order."),
 "11180218403": ("Patagonia at BEAMS", "Houdini Jacket", Y(16500), "11180218403/",
   "The packable shell that disappears into its own chest pocket, in recycled nylon ripstop with a PFC-free water-repellent finish. The one to keep in the bag."),
 "36240568139": ("Pilgrim Surf+Supply", "Salathe Straight Pants", Y(28600), "36240568139/",
   "A full-length version of Pilgrim&rsquo;s climbing pants, wide and straight, with a webbing belt, a double belt loop for a carabiner and a PFC-free water-repellent finish."),
 "38240081120": ("BEAMS PLUS", "MIL 6-Pocket Ripstop Pants", Y(28600), "38240081120/",
   "Based on 1960s U.S. military ripstop trousers, with double side pockets and drawstring hems, in a three-ply yarn."),
 "38240077578": ("BEAMS PLUS", "Gym Pants", Y(16500), "38240077578/",
   "European military underwear turned into a slim, stretchy pant with a drawcord waist and ribbed hems. The post-round pair."),
 "36100106683": ("Pilgrim Surf+Supply", "Pennant Team Long-Sleeve Tee", Y(9900), "36100106683/",
   "A long-sleeve tee with Pilgrim logos front and back, in cotton grown by small farms in Zambia."),
 "36610302496": ("BLUE LUG x Pilgrim Surf+Supply", "The Day Pack", Y(27500), "36610302496/",
   "A navy day pack from the Tokyo bike shop and Pilgrim, with insulated side pockets for a drink. A pre-order."),
 "36480003259": ("G-SHOCK x Pilgrim Surf+Supply", "GLX-5600 Watch", Y(19800), "36480003259/",
   "Made for Pilgrim&rsquo;s tenth year in Japan: the slim tide-graph G-Shock in matte grey, with green markers inspired by New York subway signs."),
}
SECTIONS = [
 ("The 50th Anniversary Specials", "fiftieth", ["82120067462", "81610479334", "82180255493", "82130357411", "82180263411", "81041029467"],
  "<strong>Six pieces &middot; &yen;19,800&ndash;&yen;99,000</strong>BEAMS turned 50 this year. These are the golf pieces from its anniversary list."),
 ("The Malbon Archive and More Special Orders", "special", ["81411362467", "82020722467", "82180281357", "82230441060", "81510016221", "81411390499", "81411417412", "82230453585", "82180265402"],
  "<strong>Nine pieces &middot; &yen;9,900&ndash;&yen;42,900</strong>&ldquo;Bechu&rdquo; means special order, and it is what BEAMS does best: Malbon, Quiet Golf, Lee, Tomo &amp; Co., J.Press and more."),
 ("Purple Label: Return British", "purple", ["84150122529", "84150123529", "84180120529", "84230254803", "84230256803", "81411371863"],
  "<strong>Six pieces &middot; &yen;11,000&ndash;&yen;30,800</strong>Knickerbockers, crests and a flat cap. The most fun part of the fall line."),
 ("Orange Label, B.G.THREE and The Golfer&rsquo;s Journal", "orange", ["82150159647", "82180240336", "82120062444", "84180106803", "84150121120", "82150171705"],
  "<strong>Six pieces &middot; &yen;23,100&ndash;&yen;42,900</strong>Varsity Americana from Orange Label and quiet city-to-course pieces from B.G.THREE."),
 ("Harris Tweed, Black Watch and a Loafer", "bags", ["81040988629", "81610485629", "81610486629", "81610399833", "81610402833", "81320568221"],
  "<strong>Six pieces &middot; &yen;13,200&ndash;&yen;69,300</strong>New Harris Tweed from October 30 and the house Black Watch tartan."),
 ("Off the Course: From BEAMS Best 100", "off-course", ["36130314101", "36180962049", "11180218403", "36240568139", "38240081120", "38240077578", "36100106683", "36610302496", "36480003259"],
  "<strong>Nine pieces &middot; &yen;9,900&ndash;&yen;68,200</strong>Not BEAMS Golf: picks from BEAMS&rsquo; outdoor shop Pilgrim Surf+Supply, BEAMS and BEAMS PLUS, from the Outdoor &amp; Sports page of BEAMS Best 100."),
]
N = 42
PQ = {
 "purple": ("Ultimately, BEAMS GOLF isn&rsquo;t made for professional golfers.", "Satoshi Nishiwaki, to Bunshun, 2019 (translated)"),
}
CAP = ""
BANDS = {
 "fiftieth-after": ("Fall/Winter 2026", "From BEAMS Golf&rsquo;s &ldquo;The Greatest Hits&rdquo; lookbook.",
   [("band-1-1", "A man in a burgundy knit and a beanie checking a distance with a rangefinder on a fairway", "On the course"),
    ("band-1-2", "Two golfers talking on a tee, one in a green cardigan and bucket hat, one in a striped rugby knit and beanie", "Between shots"),
    ("band-1-3", "A golfer in a bucket hat and a green Champion jacket at dusk", "Last light")]),
 "purple-after": ("Return British and the 50th", "Purple Label&rsquo;s crest knit and the anniversary Baracuta.",
   [("band-2-1", "A bearded man in a Return British crest sweater adjusting a flat cap in a wood-paneled room", "Return British"),
    ("band-2-2", "A man in a brown zip blouson standing by a car", "The Baracuta"),
    ("band-2-3", "Two men talking by a vintage car on a city street, one in a navy BEAMS GOLF jacket", "Off to the course")]),
 "orange-after": ("The Greatest Hits", "More from the fall lookbook.",
   [("band-3-1", "A man in a tartan shirt and navy cap teeing up a ball", "The tartan shirt"),
    ("band-3-2", "A golfer on the tee at sunset with a cart behind him", "The back nine"),
    ("band-3-3", "The back of a green BEAMS GOLF jacket with a large yellow Champion C", "Champion x BEAMS Golf")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We wrote about BEAMS Golf in August, and a lot has happened since. BEAMS, the Harajuku shop that started as a 21.5-square-meter store in 1976, turned 50 this year, and BEAMS Golf turned 15. The brand marked it the way it marks everything: with special orders. There is a Lacoste knit polo with BEAMS inside the crocodile patch, available for one year only, a Baracuta jacket with a tree-camo lining, a blue-and-white Jones caddie bag, and on October 28 a Malbon archive drop that brought back the graphic from the two brands&rsquo; first collaboration.</p>
    <p><strong>Sun Day Red, through BEAMS.</strong> The bigger news is that BEAMS Golf is now the exclusive home in Japan of Sun Day Red, the brand Tiger Woods started with TaylorMade in 2024. It made its Japanese debut with a BEAMS Golf pop-up at the Baycurrent Classic, Japan&rsquo;s only PGA Tour event, at Yokohama Country Club from October 8 to 11, then went into the BEAMS Golf store in Yurakucho on October 16, alongside a special Icon Polo II in BEAMS Golf green at &yen;26,400.</p>
    <p><strong>The Greatest Hits.</strong> The fall/winter season is called &ldquo;The Greatest Hits,&rdquo; old favorites brought back like a band&rsquo;s best-of album: an &ldquo;On the Course&rdquo; chapter in late summer, then &ldquo;U.S. Traditional,&rdquo; with Purple Label running a British theme it calls Return British. In July, BRIEFING and BEAMS Golf made their first special caddie bag since 2018, in woodland camo, and on October 30 a run of Harris Tweed headcovers and bags arrived.</p>
    <p><strong>A correction.</strong> Our August post called Satoshi Nishiwaki the director of BEAMS Golf. According to Senken Shimbun, he moved to BEAMS Creative in March 2025 and now directs New Vintage Golf, a line that mixes vintage and new pieces. He set the tone for BEAMS Golf for most of its 15 years, and his line from 2019 still describes it: the clothes are for golfers who like them, not for the pros.</p>
    <p><strong>Buying it from the US.</strong> Everything here is priced in yen on beams.co.jp; we converted at about &yen;156 to the dollar. When we checked on October 30, the site was offering international checkout through WorldShopping. BEAMS&rsquo; US store, BEAMS America, does not carry BEAMS Golf.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">What&rsquo;s New</div>
      <div class="sidebar-detail"><span class="l">BEAMS</span><span>50 years</span></div>
      <div class="sidebar-detail"><span class="l">BEAMS Golf</span><span>15 years</span></div>
      <div class="sidebar-detail"><span class="l">FW26 theme</span><span>The Greatest Hits</span></div>
      <div class="sidebar-detail"><span class="l">New partner</span><span>Sun Day Red (Japan)</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&yen;9,900&ndash;&yen;99,000</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Lacoste 50th knit polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#BEAMSGolf</span>
        <span class="hashtag">#BEAMS50</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">Not Made for the Pros</h2>
  <div class="writeup-body">
    <p>BEAMS Golf launched in spring 2011 as Japan&rsquo;s first select-shop golf line, and for most of its life the man shaping it was Satoshi Nishiwaki, a BEAMS lifer who, by his own account, had never played the game. &ldquo;Until I got involved in launching BEAMS GOLF, I had never played golf at all. If anything I avoided it,&rdquo; he told Bunshun in 2019 (our translation).</p>
    <p>That outsider view became the brand&rsquo;s idea. &ldquo;BEAMS GOLF wants its clothes worn by players who like them and who they suit,&rdquo; he said in the same interview, after Hinako Shibuno won the 2019 Women&rsquo;s British Open in an Orange Label polo. &ldquo;Ultimately, BEAMS GOLF isn&rsquo;t made for professional golfers.&rdquo;</p>
    <p>He was also honest about the boom years. In 2024, returning as director for a season after time away, he told WWD Japan the brand had leaned too hard on reorders of best-sellers and staples instead of new ideas, and that it had to reflect on that. The answer since has been special orders and themes: New York, then Basic &amp; Future, and now The Greatest Hits.</p>
    <p>Nishiwaki has since moved on to BEAMS Creative and New Vintage Golf. BEAMS Golf, at 15, now has a Tiger Woods brand to sell, a Malbon archive to dig through and a parent company celebrating 50 years. The special orders keep coming.</p>
    <p>For the original story, read our <a href="/drops/brand-to-know-beams-golf">Brand to Know on BEAMS Golf</a> from August.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/beams-revisit/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-30", "dateModified": "2026-10-30",
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
    <span>Brand Revisited &middot; Tokyo &middot; Est. 2011</span><span class="dot"></span>
    <span>42 picks &middot; prices checked October 30, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golf cart parked on a sunny fairway lined with pines, from the BEAMS Golf FW26 lookbook" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
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
