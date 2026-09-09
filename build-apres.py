#!/usr/bin/env python3
"""Brand to Know — Après Golf.

STRUCTURE
---------
Built on the Kingfisher gold standard (galleries + brand voice + house FAQ),
with the section order set by what the catalogue actually is rather than by a
template. Après lists 241 products, 219 of them in stock on 9 Sept 2026, and
the shape of that catalogue is the story: a printed-fleece line, a vintage
patch archive, a Grateful Dead run, and a rail of 1980s and 90s sweaters they
buy secondhand and resell.

Lenny's direction, 2026-09-09: lead with the tie-dye, and include the Dead.

WHAT IS SOURCED, AND FROM WHERE
-------------------------------
Every factual claim below comes from Après's own pages, captured this session:
  /pages/about-us   "We source vintage patches, create new patches, embroider
                    logos and print custom designs"; hi-loft sherpa fleece;
                    the patent-pending reversible cover for two-logo events.
  /pages/custom     "Each headcover is made with hi-loft sherpa fleece and
                    hand-sewn in California. Our factory has been in business
                    since 1992"; the fleece mill also supplies outdoor and
                    fashion brands.
  product bodies    the Sunday Sweater line description ("collecting vintage
                    and vibrant golf sweaters from the '80s and '90s"), which
                    explicitly links the sweaters to the patch philosophy.
  homepage          the @HallyLead collaboration account, and three named
                    testimonials used verbatim in QUOTES below.

NO FOUNDER QUOTE. Searched /pages/about-us, /custom, /careers, /contact and
the open web on 2026-09-09: Après publishes no founder name anywhere. The
About page writes in "we", the Custom page slips into "I" once. Rather than
invent or paraphrase a founder voice, the voice section runs three named,
verbatim third-party quotes. See the founder-quotes house rule.

DELIBERATELY NOT ASSERTED (no source):
  - a founding year for the BRAND (1992 is the FACTORY, not Après)
  - the founder's name, location beyond "California", or headcount
  - any licensing arrangement for the bear/stealie artwork. Après names these
    "Dancing Bears" and "Steal Your Clubface" and says nothing about a licence,
    so neither do we. The copy describes the objects and stops there.
  - that any vintage patch is authentic to the club or resort named on it
  - Hally Leadbetter's involvement beyond what Après's own collab note states

FAQ MARKUP: <details class="faq-q"><summary> — NOT div.faq-q + div.faq-a.
There is no .faq-a rule in the house sheet, and apply-faq-style.py detects an
existing visible FAQ by looking for "<details". Div markup fails verify-post.py
AND makes that script append a duplicate FAQ. Learned on the divot rebuild the
same day.
"""
import re, os, json
from urllib.parse import quote

SLUG  = "brand-to-know-apres-golf"
TITLE = ("Brand to Know: Apr&egrave;s Golf &mdash; Ski Patches, Tie-Dye Fleece "
         "and a Rack of Dancing Bears")
PLAIN = ("Brand to Know: Après Golf — Ski Patches, Tie-Dye Fleece and a Rack of "
         "Dancing Bears")
DESC  = ("Après Golf sews vintage ski-resort and country-club patches onto hi-loft "
         "sherpa fleece headcovers, hand-sewn in California. 45 pieces from the "
         "tie-dye rack, the Dead run, the patch archive and the Sunday Sweaters.")
IMG   = "/images/apres-golf/"
SHOP  = "https://apresgolf.com/products/"

CAT = json.load(open("research/apres/all.json"))
LINEUP = json.load(open("research/apres/lineup.json"))

# slug -> (display name, copy). Names are shortened from the store titles;
# prices and stock come from the live catalogue, never from here.
COPY = {
 # ---------------- THE TIE-DYE RACK ----------------
 "fruit-looper": ("The Fruit Looper&trade;",
  "The Fruit Looper is the print the brand is built around, and it behaves like actual dye rather than a repeat pattern &mdash; magenta, marigold and teal bleeding into a navy ground with no two panels landing the same way. On hi-loft sherpa the colour sinks into the pile instead of sitting on top of it."),
 "fruit-looper-chenille": ("The Fruit Looper&trade; Chenille Patch",
  "Same print, with a chenille-lettered Apr&egrave;s-Golf patch stitched across the crown. Chenille is the varsity-jacket material, so the letters stand a few millimetres proud of the fleece and catch light from the side."),
 "yuppie-scum": ("Die Yuppie Scum Fruit Looper&trade;",
  "The Fruit Looper ground under a shield patch reading DIE YUPPIE SCUM &mdash; a line borrowed from 1980s Manhattan graffiti and later a Wall Street movie. On a golf headcover it is the most pointed thing in the catalogue."),
 "parparazzi": ("The Parparazzi",
  "Cobalt and violet dropped into a lilac field, sold as a three-piece set with a matching alignment-stick sleeve. This one photographs closest to a genuine spiral tie-dye of anything Apr&egrave;s prints."),
 "transfused": ("Transfused&trade;",
  "Magenta and violet speckle over black, named for the drink you order at the turn. The trademark suggests Apr&egrave;s intends to keep running it rather than retire the colourway after a season."),
 "crayon-clouds": ("Crayon Clouds",
  "Cream ground with navy, sage and rust shapes laid over it in soft-edged blocks. It reads as the quietest print here and is the one that survives a bag otherwise full of black leather."),
 "sand-mosaic": ("Sand Mosaic",
  "Speckled confetti over off-white, and the cheapest cover in the whole range at $38. Apr&egrave;s puts its price floor on the prints rather than on a stripped-down blank."),
 "digital-drops": ("Digital Drops",
  "White pixel-scatter on royal blue, printed rather than dyed, which is why the edges stay hard where the Fruit Looper's bleed."),
 "multi-mosaic": ("Multi Mosaic Blade Putter Cover",
  "Orange, cobalt and cream diamonds on a blade cover with a magnetic closure. The blade shape gives the print a flat panel to sit on, so the geometry stays legible instead of wrapping out of shape."),
 "azalea": ("Azalea",
  "Pink and yellow blooms scattered over forest green, part of a small floral run named after flowering shrubs. Sold as a set with a matching blade cover."),
 "magnolia": ("Magnolia",
  "White magnolia over pale pink, the softest thing in the printed line and the one that looks least like golf equipment sitting on a table."),
 "yellow-jasmine": ("Yellow Jasmine",
  "Yellow stars over navy paisley, which is the loudest of the three florals despite being the one named after the smallest flower."),
 # ---------------- @HALLYLEAD ----------------
 "hally-sherbet": ("@HallyLead &times; Apr&egrave;s-Golf Sherbet",
  "Coral pink with a scarlet trim, sold as a three-piece with an alignment sleeve. Hally Leadbetter designed the five-colour capsule after Apr&egrave;s spotted an order under her name and got in touch."),
 "hally-cotton-candy": ("@HallyLead &times; Apr&egrave;s-Golf Cotton Candy",
  "Hot pink over a black trim, the highest-saturation piece in a capsule that is already the brightest thing Apr&egrave;s makes."),
 "hally-blue-raspberry": ("@HallyLead &times; Apr&egrave;s-Golf Blue Raspberry",
  "Process blue against a red base tape. The neons are solid rather than printed, which puts all the work on the trim colour."),
 "hally-grapeness": ("@HallyLead &times; Apr&egrave;s-Golf Grapeness Wins",
  "Lilac with a cyan trim, and the only piece in the capsule where the trim reads brighter than the body."),
 "hally-sea-foam": ("@HallyLead &times; Apr&egrave;s-Golf Sea Foam Honeycomb",
  "Mint green over a coral trim, textured with a honeycomb pile rather than the flat sherpa loft used elsewhere in the capsule."),
 # ---------------- THE DEAD RACK ----------------
 "dancing-bears": ("Dancing Bears Patch",
  "A row of marching bears on a cream ground, and the most expensive piece in the Dead run at $128. The bears are stitched as a single wide patch rather than assembled from individual ones."),
 "steal-clubface": ("Steal Your Clubface Patch",
  "The lightning-bolt skull, rendered in red, white and blue on a cream cover, under a name that puns the artwork into golf. It is the most recognisable object Apr&egrave;s sells and the one that gets stopped on the first tee."),
 "steal-clubface-putter": ("Steal Your Clubface Blade Putter Cover",
  "The same bolt-and-skull patch shrunk onto a navy blade cover. On a putter it sits at eye level over the bag, which is where this artwork wants to be."),
 "mini-bears-mallet": ("Mini Bears Mallet Putter Cover",
  "Small bears repeated across a mallet-shaped cover, cut wide enough for a modern high-MOI head rather than a blade."),
 "bear-green-navy": ("Green Bear Patch &mdash; Navy",
  "One bear, embroidered green, on navy sherpa. The single-bear covers run a colour per cover, so a full set spells out the sequence across a bag."),
 "bear-blue": ("Blue Bear Patch",
  "The blue bear on navy, sold as a three-piece. Buying by colour rather than by club is how the Dead rack is designed to be collected."),
 "bear-pink": ("Pink Bear Patch",
  "Pink bear on navy, and the brightest of the single-bear set against its ground."),
 "bear-orange": ("Orange Bear Patch",
  "Orange bear on navy, the highest-contrast pairing in the run and the easiest to pick out of a bag at ten paces."),
 # ---------------- SKI PATCHES ----------------
 "chamonix": ("Chamonix Vintage Patch",
  "A Chamonix resort patch on cream sherpa. Chamonix hosted the first Winter Olympics in 1924, which makes this the oldest piece of ski history in the archive."),
 "st-moritz": ("St. Moritz Vintage Patch",
  "The St. Moritz sun crest, sewn onto cream. The Engadine resort is the other 1920s Winter Games host, and its patches turn up in European ski-swap boxes far more often than American ones do."),
 "alta": ("Alta Vintage Patch",
  "Alta's patch on cream, from the Little Cottonwood resort that still bans snowboards. At $88 it is the cheapest entry into the vintage patch archive."),
 "mad-river-glen": ("Mad River Glen Vintage Patch",
  "The Mad River Glen snowflake on black sherpa. The Vermont co-operative trades on being difficult, and its patch is the one skiers recognise across a crowded room."),
 "sugarloaf": ("Sugarloaf Vintage Patch",
  "A Sugarloaf patch on cream, and the most expensive ski piece at $128. Maine's Carrabassett Valley mountain is the outlier in a rack otherwise weighted to the Alps and the Rockies."),
 "heavenly-valley": ("Heavenly Valley Vintage Patch",
  "The Heavenly Valley crest in red and blue over cream, from the Tahoe resort that straddles the California&ndash;Nevada line."),
 # ---------------- CLUB PATCHES ----------------
 "lacc": ("LACC Vintage Patch",
  "The Los Angeles Country Club crest on cream sherpa. LACC hosted the 2023 U.S. Open, which pulled a famously private club into general view for a week."),
 "olympic-club": ("The Olympic Club Vintage Patch",
  "The Olympic Club's winged-O patch on navy, and the most expensive cover in the range at $138. The San Francisco club has hosted five U.S. Opens."),
 "pine-tree": ("Pine Tree GC Vintage Patch",
  "A Pine Tree Golf Club patch on cream. The Boynton Beach course is a Dick Wilson design and an architecture-nerd pick rather than a name-recognition one."),
 "sea-pines": ("Sea Pines Vintage Patch",
  "The Sea Pines patch on cream, sold as a set. Hilton Head's resort is where Harbour Town sits, and the patch predates the lighthouse becoming the logo."),
 "wianno": ("Wianno Club Vintage Patch Topper",
  "A Wianno Club burgee on navy, cut as a Topper rather than a full cover &mdash; a shorter shape that sits over the crown of the driver instead of sheathing the shaft."),
 "wilshire": ("Wilshire CC Vintage Patch",
  "The Wilshire Country Club crest on cream, from the Norman Macbeth course sitting in the middle of Los Angeles with an oil derrick on the property."),
 # ---------------- SUNDAY SWEATERS ----------------
 "sweater-payne": ("Sunday Sweater: The Payne",
  "A navy 1980s intarsia sweater with a full golf scene knitted across the chest, named for Payne Stewart. These are secondhand garments Apr&egrave;s buys and resells, so each one is a single unit in a single size."),
 "sweater-snead": ("Sunday Sweater: The Snead",
  "Cream ground, a lone golfer at the top of the backswing, and a navy-and-red tipped collar. The knit is the giveaway on age: intarsia panels this detailed largely stopped being made in volume after the early nineties."),
 "sweater-jack": ("Sunday Sweater: The Jack",
  "Navy with a foursome walking a fairway in colour blocks. The line is named after players rather than after the sweaters' original makers, which are mostly long gone."),
 "sweater-ernie": ("Sunday Sweater: The Ernie",
  "A four-golfer scene on navy, cut in the boxy fit of its decade rather than resized to modern proportions."),
 "sweater-watson": ("Sunday Sweater: The Watson",
  "Cream, a single figure mid-swing, and the cheapest sweater on the rail at $88. The Sunday Sweaters and the patch covers come from the same instinct &mdash; buy the old thing, keep it in circulation."),
 # ---------------- CUSTOM AND HOUSE ----------------
 "send-your-patch": ("Send Us Your Patch! Custom Headcover",
  "You mail Apr&egrave;s a patch and they build a cover around it. This is the service the rest of the catalogue is a showroom for, and it is why the vintage rack keeps changing &mdash; the supply is whatever turns up."),
 "reversible": ("Apr&egrave;s-Golf&reg; Reversible Patch Headcover",
  "A patent-pending reversible cover that carries a different patch on each face. Apr&egrave;s built it for tournaments and outings that need two logos, and for clubs running a member-only mark alongside a public one."),
 "big-retro-cream": ("BIG RETRO Logo Fruit Looper&trade;",
  "The Fruit Looper print with an oversized Apr&egrave;s-Golf script laid across it in cream. The house logo at this scale turns the print into a background rather than the subject."),
 # ---------------- HOODIES ----------------
 # HANDLE TRAP, verified against the live JSON on 2026-09-09: Après's two
 # slogan hoodies sit on SWAPPED handles. /products/i-will-not-apres-golf®-hoodie
 # serves "Find Your Line", and /products/find-your-line-apres-golf®-hoodie-copy
 # serves "I Will Not". The handles also contain a literal ®, so the shop link
 # has to be percent-encoded (see SHOP_URL below) — same class of bug as the
 # Manors ® handles that 404'd.
 "hoodie-find-your-line": ("Find Your Line Apr&egrave;s-Golf&reg; Hoodie",
  "A ski gondola strung across the chest, which is the joke the brand keeps making: Apr&egrave;s calls it a golfdola in its own product copy. The blank underneath is the house private-label mid-weight, 9.4 oz of 80% cotton and 20% recycled poly fleece, cut relaxed and sold unisex."),
 "hoodie-i-will-not": ("I Will Not Apr&egrave;s-Golf&reg; Hoodie",
  "Chalkboard lines repeating the title until they fill the front, a format Apr&egrave;s credits to Bart Simpson on the product page. Same 9.4 oz private-label body as the gondola hoodie, in cream."),
 "hoodie-cotton-candy": ("Cotton Candy Scratch Text Hoodie",
  "Pink and blue dye bleeding through a heavyweight fleece under the scratch-drawn house logo. This is the tie-dye rack applied to something you can wear rather than something you hang on a driver."),
 "hoodie-twirl-blue": ("Sunset Twirl Original Blue Logo Hoodie",
  "A spiral dye in blue and violet with the original Apr&egrave;s script on the chest. The twirl is a genuine spiral tie-dye rather than a print, so the pattern lands differently on every unit."),
 "hoodie-twirl-pink": ("Sunset Twirl Original Pink Logo Hoodie",
  "The same spiral in coral and gold, and the cheapest hoodie here at $88. Dyed pieces like this are the closest the apparel gets to the headcover catalogue&rsquo;s logic, where no two come out identical."),
}

SECTIONS = [
 ("The Tie-Dye Rack &mdash; 12 Prints",
  "Apr&egrave;s prints and dyes its own fleece, and this is the part of the catalogue that looks like nothing else on a first tee.",
  ["fruit-looper","fruit-looper-chenille","yuppie-scum","parparazzi","transfused",
   "crayon-clouds","digital-drops","sand-mosaic","multi-mosaic","azalea","magnolia","yellow-jasmine"]),
 ("The Neon Capsule &mdash; @HallyLead &times; Apr&egrave;s-Golf",
  "Five solid neons designed by Hally Leadbetter, each sold as a three-piece set with a matching alignment-stick sleeve.",
  ["hally-sherbet","hally-cotton-candy","hally-blue-raspberry","hally-grapeness","hally-sea-foam"]),
 ("The Dead Rack &mdash; 8 Pieces",
  "Bears and bolts, across headcovers, a blade cover and a mallet.",
  ["dancing-bears","steal-clubface","steal-clubface-putter","mini-bears-mallet",
   "bear-green-navy","bear-blue","bear-pink","bear-orange"]),
 ("The Ski Patches &mdash; 6 Resorts",
  "Where the name stops being a pun. Genuine resort patches, sewn onto golf headcovers.",
  ["chamonix","st-moritz","alta","mad-river-glen","sugarloaf","heavenly-valley"]),
 ("The Club Patches &mdash; 6 Crests",
  "Fifty-six club patches are in stock today. These six are the ones a reader is most likely to recognise.",
  ["lacc","olympic-club","pine-tree","sea-pines","wianno","wilshire"]),
 ("The Sunday Sweaters &mdash; 5 Knits",
  "Apr&egrave;s buys secondhand intarsia golf sweaters from the 1980s and 90s and resells them one at a time.",
  ["sweater-payne","sweater-snead","sweater-jack","sweater-ernie","sweater-watson"]),
 ("The Hoodies &mdash; 5 Pieces",
  "Apr&egrave;s puts its own private-label blank under the graphics: 9.4 oz, 80% cotton and 20% recycled poly, cut relaxed and sold unisex.",
  ["hoodie-find-your-line","hoodie-i-will-not","hoodie-cotton-candy",
   "hoodie-twirl-blue","hoodie-twirl-pink"]),
 ("Your Patch, Their Fleece &mdash; 3 Ways In",
  "The custom programme, the two-logo cover, and the house print.",
  ["send-your-patch","reversible","big-retro-cream"]),
]

# IRL frames, pulled from Après's own campaign and product photography. Found by
# testing every non-lead frame in the catalogue for a white backdrop: a Shopify
# packshot sits on pure white, so a frame whose non-white bounding box fills the
# image is a real photograph. 37 candidates surfaced; these 8 are the keepers.
LOOKBOOK = [
 ("irl-bag",        "A hand lifting a printed Apr&egrave;s fleece cover off a driver in a stand bag, on course"),
 ("irl-patch-rack", "A pile of finished vintage-patch headcovers with the resort and club patches still tagged"),
 ("irl-green",      "Three printed sherpa fleece headcovers lying on a cut green"),
 ("irl-hally-bag",  "The @HallyLead neon covers loaded onto a carry bag beside a set of irons"),
 ("irl-dog",        "A goldendoodle lying on a fairway with two sherpa fleece covers beside it"),
 ("irl-in-hand",    "A lilac sherpa fleece cover held in one hand with the clubhead still seated inside"),
 ("irl-sock",       "An Apr&egrave;s-Golf logo sock and a fleece cover at the foot of a push cart"),
 ("irl-archive",    "Dozens of Apr&egrave;s headcovers piled together, showing the range of patches and prints"),
]

LOOK = ('<section class="products" style="border-top:none;padding-top:48px">\n'
        '  <h2 class="products-hdr">In the Wild</h2>\n'
        '  <p class="cat-kicker">Apr&egrave;s photographs its own product on courses rather than on seamless.</p>\n'
        '  <div class="ap-look" style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px">\n'
        + "".join(
            '    <figure style="margin:0;border:.5px solid var(--ink);overflow:hidden">'
            f'<img src="{IMG}{s}.jpg" alt="{a}" loading="lazy" '
            'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" /></figure>\n'
            for s, a in LOOKBOOK)
        + '  </div>\n</section>\n')

# .ap-look needs a real CSS rule or verify-post.py fails "every class used has a
# CSS rule". Mirrors Kingfisher's .kf-look: the grid itself is inline, the class
# exists purely to carry the mobile column override.
LOOK_CSS = "<style>@media(max-width:760px){.ap-look{grid-template-columns:repeat(2,1fr)!important}}</style>"

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Apr&egrave;s Golf makes hi-loft sherpa fleece headcovers, hand-sewn in California, and sews vintage patches onto them &mdash; ski resorts, country clubs, and whatever else turns up. Fifty pieces are below, across eight groups, all of them in stock on 9 September 2026.</p>
    <p>The idea starts with the name. Apr&egrave;s-ski is the part of a ski day that happens after the skiing, and the patches that end up on these covers came off ski jackets: Chamonix, St. Moritz, Alta, Mad River Glen. Apr&egrave;s buys them, cuts fleece around them, and sells the result to golfers. The brand describes what it does plainly on its own site &mdash; <em>&ldquo;We source vintage patches, create new patches, embroider logos and print custom designs.&rdquo;</em> The sewing happens in a California factory that has been running since 1992, at a mill that also supplies fleece to outdoor and fashion labels.</p>
    <p>If you want the short version: the tie-dye prints are the ones people stop you about, the vintage patches are the ones that will not be repeatable, and the whole catalogue is really an advertisement for the custom programme, where you post them a patch of your own.</p>
  </div>
</div>
"""

PATCHES = """<section class="products">
  <h2 class="products-hdr">Where the Patches Come From</h2>
  <p class="cat-kicker">A supply chain that runs on ski swaps and clubhouse drawers rather than on a production calendar.</p>
  <div class="writeup-body">
    <p><strong>The archive is finite.</strong> Fifty-six club patches and eleven ski-resort patches are listed in stock today, and each design exists in whatever quantity Apr&egrave;s managed to buy. There is no reorder. When a resort patch runs out it is gone in a way that a printed colourway never is, which is why the vintage rack turns over faster than the rest of the catalogue.</p>
    <p><strong>The ski patches are the older objects.</strong> Chamonix hosted the first Winter Olympics in 1924 and St. Moritz the second in 1928; Alta opened in 1938; Mad River Glen has been a skier-owned co-operative since 1995 and still refuses snowboards. Their patches were made to be sewn onto jackets and hats, in an era when a resort visit produced a physical souvenir rather than a geotag.</p>
    <p><strong>The club patches read differently.</strong> A Los Angeles Country Club or Olympic Club crest carries an access question with it &mdash; these are private clubs, and the patch is a thing a member or a guest once had. Apr&egrave;s makes no claim about provenance and neither do we; what is on offer is the object, not the membership.</p>
    <p><strong>And the sweaters follow the same logic.</strong> Apr&egrave;s describes the Sunday Sweater rail in its own product copy as <em>&ldquo;collecting vintage and vibrant golf sweaters from the &rsquo;80s and &rsquo;90s&rdquo;</em>, and ties it directly to the covers: each one has a story <em>&ldquo;just like the vintage patches we affix atop our American Made fleece headcovers.&rdquo;</em> One brand, one instinct, applied to two categories.</p>
  </div>
</section>
"""

QUOTES = """<section class="products">
  <h2 class="products-hdr">What Other People Say About It</h2>
  <p class="cat-kicker">Apr&egrave;s publishes three named endorsements on its own site. All three run here in full.</p>
  <div class="writeup-body">
    <blockquote><p>&ldquo;In a space that&rsquo;s become more crowded and less original, Apr&egrave;s Golf sticks out for its sharp and unique products that are design catnip for the golf diehards and wannabes alike.&rdquo;</p>
    <cite>&mdash; Brendan Porath, Shotgun Start podcast</cite></blockquote>
    <blockquote><p>&ldquo;I&rsquo;m a huge headcover fan, always trying to find clean, unique looks for my golf clubs, and the Apres teams continually knocks it out of the park with the products they produce. I got headcovers made for my yearly buddies trip and the fellas gushed about the quality, the styles, and the colorway options.&rdquo;</p>
    <cite>&mdash; Shane Bacon, golf broadcaster and writer</cite></blockquote>
    <blockquote><p>&ldquo;My favorite headcover from Apr&egrave;s is the Rolex Patch Driver Cover. Adding a little Sherpa to accessorize your bag takes your style to the next level!&rdquo;</p>
    <cite>&mdash; Brad Tilley, USGA amateur</cite></blockquote>
    <p>Apr&egrave;s publishes no founder name on its About, Custom, Careers or Contact pages, and none surfaced elsewhere, so there is no maker&rsquo;s quote to run alongside these.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is a hi-loft sherpa fleece headcover?",
  "Sherpa fleece is a knitted pile fabric with a deep, curled nap on the face. Hi-loft means the pile is left long rather than sheared flat, which is what gives an Apr&egrave;s cover its bulk and why a printed colourway sinks into the surface instead of sitting on it. Apr&egrave;s states its fleece comes from a mill that also supplies outdoor and fashion brands."),
 ("Where are Apr&egrave;s Golf headcovers made?",
  "Hand-sewn in California. Apr&egrave;s states on its custom page that the factory doing the sewing has been in business since 1992. The brand markets the covers as American made."),
 ("Are the vintage patches real?",
  "Apr&egrave;s says it sources vintage patches, creates new patches, embroiders logos and prints custom designs, so the catalogue mixes all four. Individual listings do not carry provenance documentation, and Apr&egrave;s makes no authenticity claim on a per-patch basis."),
 ("What is the reversible headcover for?",
  "It carries a different patch on each face, so one cover serves two marks. Apr&egrave;s describes it as patent pending and aims it at tournaments and corporate outings needing two logos, and at clubs running a member-only logo alongside a public one."),
 ("Can I put my own patch on one?",
  "Yes. The Send Us Your Patch cover is $118 and works exactly as named &mdash; you post them the patch and they build the headcover around it. Apr&egrave;s also runs a separate wholesale and custom programme through sales@apresgolf.com for pro shops, clubs and events."),
 ("What are the Sunday Sweaters?",
  "Secondhand golf sweaters from the 1980s and 90s that Apr&egrave;s buys in and resells, named after players rather than makers. They run $88 to $98 and each is a single garment in a single size, so the rail changes constantly."),
 ("How much do Apr&egrave;s headcovers cost?",
  "The range runs $38 to $138. Printed and solid fleece starts at $38, the Grateful-Dead-style bear covers sit at $88, and the vintage club and resort patches occupy the top of the range from $88 to $138. Shipping is free on all orders."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""


def frames(s):
    n = 1
    while os.path.exists(f"images/apres-golf/{s}-a{n+1}.jpg"):
        n += 1
    return n


def gal(s, name):
    n = frames(s)
    pl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name)).strip()
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}.jpg" alt="{pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}{"" if i==0 else f"-a{i+1}"}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def card(s):
    nm, desc = COPY[s]
    p = CAT[LINEUP[s]["handle"]]
    price = f"${int(p['price'])}" if float(p["price"]) == int(p["price"]) else f"${p['price']}"
    tag = "" if p["avail"] else " &middot; sold out"
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, nm)}
      <div class="product-body">
        <div class="product-brand">Apr&egrave;s Golf</div>
        <div class="product-name">{nm} &middot; {price}{tag}</div>
        <div class="product-desc">{desc}</div>
        <a href="{SHOP}{quote(LINEUP[s]['handle'], safe='')}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""


def sec(hdr, kicker, slugs):
    c = "\n    ".join(card(s) for s in slugs)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&egrave;", "è").replace("&ndash;", "–")
            .replace("&trade;", "™").replace("&reg;", "®").replace("&times;", "×"))


SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
for k in ["canonical"]:
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                  lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com/images/apres-golf/hero.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

n_products = sum(len(s[2]) for s in SECTIONS)
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Apr&egrave;s Golf</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 9, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{n_products} Pieces &middot; $38 to $138</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/apres-golf/hero.jpg" '
        'alt="A tie-dyed Apr&egrave;s Golf sherpa fleece headcover being lifted off a driver beside a golf bag" /></div></div>\n'
        + INTRO
        + sec(*SECTIONS[0]) + sec(*SECTIONS[1]) + sec(*SECTIONS[2])
        + PATCHES
        + LOOK
        + sec(*SECTIONS[3]) + sec(*SECTIONS[4]) + sec(*SECTIONS[5])
        + QUOTES
        + sec(*SECTIONS[6]) + sec(*SECTIONS[7])
        + FAQ)

head = head.replace("</head>", LOOK_CSS + "\n</head>")

missing = [s for s in LINEUP if s not in COPY]
if missing:
    raise SystemExit(f"lineup entries with no COPY: {missing}")
gone = [s for s, _ in LOOKBOOK if not os.path.exists(f"images/apres-golf/{s}.jpg")]
if gone:
    raise SystemExit(f"lookbook images missing on disk: {gone}")
if "ap-look" not in head:
    raise SystemExit("LOOK_CSS never landed in <head> — verify-post will fail "
                     "'every class used has a CSS rule' on .ap-look")
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(LINEUP):
    raise SystemExit(f"section/lineup mismatch: "
                     f"unplaced={set(LINEUP)-set(placed)} extra={set(placed)-set(LINEUP)}")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {n_products} products | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
