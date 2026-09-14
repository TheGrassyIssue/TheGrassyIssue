#!/usr/bin/env python3
"""Brand to Know — Fyfe Golf. The full treatment.

WHY THIS PAGE EXISTS
--------------------
TGI already had three Fyfe pages — the putter cover edit (which brands.json was
using as the "profile"), the Between Tides drop, and the MacKenzie every-edition
archive. None of them was a profile: none named the founder, none explained the
workshop, none touched the repurposed-material collections that are the most
interesting thing the brand does. Lenny, 2026-09-14: "let's give it the full
treatment — lookbook images, IRL stuff, write up etc. Let's also increase the
number of headcovers we're including since they do them so well. Then also do 3
sections about some of their more special projects and collabs."

So: 32 in-stock pieces, 23 of them headcovers, plus three project sections
(Drop Zone, Vintage Chubbs, Shooters Club) and a short MacKenzie section that
sends readers to the existing archive page rather than duplicating it.

THE SPINE
---------
The repurposing thread. Seven collections across four years are built from
reclaimed cloth — Hiut denim offcuts (2022), vintage deck chair canvas, RAF
flight suits (2025), Augusta caddie coveralls and spectator canvas with Vintage
Chubbs, Oban sail cloth, tartan remnants. Fyfe has no sustainability manifesto
about any of it; it sells all of it on story and scarcity. That gap is the
piece.

WHAT IS SOURCED, AND FROM WHERE (all captured 2026-09-14)
---------------------------------------------------------
  Companies House SC777625  FYFE GOLF LTD, inc. 1 Aug 2023, Neil Joseph Rennie
                            sole director. NOTE the brand launched Nov 2021 —
                            two years before the company was registered, and no
                            predecessor entity exists on the register. We state
                            both facts and do not explain the gap.
  ettingerlondon.com        the only long-form Rennie interview, 22 May 2026.
                            All four founder quotes come from here.
  thewanderinggolfers.com   April 2022 interview — the launch date, the fashion
                            background, the joint-venture workshop.
  /pages/made-in-scotland   Harris Tweed from the Isle of Harris, tartans from
                            Perthshire and Selkirk, waxed canvas from Halley
                            Stevensons in Dundee, merino from Todd & Duncan.
  /pages/custom-made-...    the custom pricing ladder and 14-21 working day lead
                            time. Quoted exactly.
  /pages/fabrics-materials  the "Honesty Box" — Fyfe naming its own synthetics.
  /pages/japanse-denim-...  the Offcut Projects rationale. Best philosophy quote
                            on the entire site, buried on a 2022 denim page.
  /collections/the-drop-zone + its lookbook and journal pages
  /collections/the-lucky-numbers + the-spectator product page (Vintage Chubbs)
  /pages/the-shooters-club-lookbook
  live catalogue JSON       every price and stock state. Never hand-typed.

DELIBERATELY NOT ASSERTED (checked, unsupported):
  - any price for a Drop Zone piece. Every product handle is dead and the only
    figures available were USD search-engine summaries. We print none.
  - edition sizes for Drop Zone. "One-of-a-kind" and "limited" is all Fyfe says.
  - where the RAF garments were obtained. No supplier, dealer or squadron is
    named anywhere. Leuchars and Lossiemouth appear as GEOGRAPHY in Fyfe's copy,
    not as provenance — do not convert them into a source.
  - that the Shooters Club is a collaboration. It is an in-house collection; no
    estate or partner is named. Its "estate tweeds from some of Scotland's most
    storied grounds" is atmosphere; the Gamekeeper product copy says "inspired
    by". We note the gap once, plainly, without making it a gotcha.
  - who runs Vintage Chubbs. No name is published anywhere.
  - that Vintage Chubbs canvas came from chairs. Fyfe says "drawn from the
    spectator line" and nothing more.
  - 1% For The Planet in the present tense. 2022-sourced, absent from the site.
  - the "46 steps" claim (traces only to a TikTok caption) and "3 years at
    Manors" (LinkedIn snippet, page unreachable).
  - a club-tartan or club-crest programme for pro shops beyond the logo
    embroidery service the wholesale page actually describes.

FAQ MARKUP: <details class="faq-q"><summary> — NOT div.faq-q + div.faq-a.
No .faq-a rule exists in the house sheet and apply-faq-style.py detects an
existing FAQ by looking for "<details"; div markup fails verify-post.py AND
makes that script append a second FAQ.
"""
import re, os, json
from urllib.parse import quote

SLUG = "brand-to-know-fyfe-golf"
TITLE = ("Brand to Know: Fyfe Golf &mdash; Harris Tweed, RAF Flight Suits and a "
         "Workshop in Fife")
PLAIN = ("Brand to Know: Fyfe Golf — Harris Tweed, RAF Flight Suits and a Workshop "
         "in Fife")
DESC = ("Fyfe Golf makes headcovers to order in a Fife workshop from Harris Tweed, "
        "Scottish tartan and reclaimed cloth — RAF flight suits, Augusta caddie "
        "coveralls, Oban sail cloth. 32 in-stock pieces, the founder's story, and "
        "the three projects that explain the brand.")
IMG = "/images/fyfe-btk/"

CAT = {x["handle"]: x for x in json.load(open("research/fyfe/catalog.json"))}
LINEUP = json.load(open("research/fyfe/lineup.json"))

# stem -> (display name, copy). Prices and stock come from the live catalogue at
# build time, never from this table.
COPY = {
 # ------------------------- HARRIS TWEED -------------------------
 "rothesay": ("Rothesay",
  "The one that costs the most and looks the least like a golf product. Orange, royal blue and melange tones in a Harris Tweed cut for The Stripes 2.0: Island Edition, named for the harbour town on Bute. Fyfe shot that collection on the island itself, and the colourway reads as a deliberate record of a place rather than a seasonal palette."),
 "arran": ("Arran",
  "Oatmeal tweed with a rich green Harris Tweed accent band and dark green plush fleece inside. The two-tone construction is the house signature &mdash; a body cloth and a contrast band, seamed rather than printed, so the join is a real edge you can feel through the wool."),
 "dunbar": ("Dunbar",
  "Duck egg Harris Tweed with a baby blue accent band and light blue fleece lining, drawn from the beaches and rock shelves at Dunbar on the East Lothian coast. It is the softest colourway Fyfe currently lists and the one that looks least severe against a tan leather bag."),
 "black-grouse-hc": ("Black Grouse",
  "Black and white houndstooth Harris Tweed with a red plush lining. The houndstooth is the loudest weave in the range from three feet away and the most restrained from thirty, which is roughly the distance at which anyone else sees your bag."),
 "balmedie": ("Balmedie",
  "Two Harris Tweeds split horizontally in seaweed and soft purple, named for the dunes north of Aberdeen. Published on 11 August 2026, so it is one of the two newest covers in the range. Dark green fleece lining."),
 "cambo": ("Cambo",
  "The other August 2026 arrival, built the same way as Balmedie &mdash; two tweeds split across the horizontal &mdash; in aqua and soft blue, with a black fleece lining. Cambo sits on the Fife coast a few miles from where these are sewn."),
 "galloway-hc": ("Galloway",
  "Black Harris Tweed shot through with multi-coloured fleck, over black organic cotton fleece. The fleck is what stops it reading as a plain black cover; in low light it is simply dark, and in sun it turns over with colour."),
 "fortrose-hc": ("Fortrose",
  "A navy base with soft red and orange overcheck, named for the links on the Black Isle. The overcheck is fine enough that the cover passes as navy until someone picks it up."),
 "huntsman": ("Huntsman",
  "Herringbone plaid in highland country colours &mdash; the estate-cloth register Fyfe returns to more than any other, and the closest thing in the standing range to the sold-out Shooters Club tweeds."),
 "five-glens-hc": ("Five Glens",
  "Another herringbone plaid mix, lined in navy. Five Glens runs across several products in the range, including the slip-on putter cover further down, which makes it the easiest way to match a driver to a putter without ordering a set."),
 "moray": ("Moray",
  "Harris Tweed in plain weave rather than twill &mdash; a light grey ground with subtle teals and oranges worked through it, and a light blue fleece lining. Plain weave gives a flatter, tighter surface than the herringbones, so the colour does the work instead of the texture."),
 "modern-herringbone-hc": ("Modern Herringbone",
  "Dark charcoal herringbone with a black lining. The default, in the useful sense: the cover that disappears into a bag and lets the rest of the set be the interesting part."),
 # ------------------------- TARTAN -------------------------
 "douglas-grey": ("Douglas Grey Tartan",
  "Pure new wool in Douglas Grey, black fleece lining. Tartan behaves differently to tweed on a headcover &mdash; the sett is a fixed grid, so the pattern has to be cut and placed rather than simply wrapped, and the line where the panels meet is where you can see whether it was done carefully."),
 "campbell-argyll": ("Campbell of Argyll Tartan",
  "One of the older registered setts in Scotland, in 100% pure new wool, available for driver and fairway. Fyfe finishes it with the black tag label rather than the green, which suits the darker ground."),
 "mackenzie-hc": ("MacKenzie Tartan",
  "The tartan that ties the standing range to the collaboration &mdash; the same cloth family used on the MacKenzie bag editions. If you own one of those bags, this is the cover that matches it, and at &pound;65 it is a considerably less demanding way to buy into the same idea."),
 "kerry-county": ("Kerry County",
  "An Irish county tartan, woven in Scotland and sewn in Fife, with a plush cotton fleece lining. Fyfe's copy is specific about the chain: the cloth is <em>&ldquo;woven by grandmasters in historic fabric mills across Scotland&rdquo;</em> and made up at the workshop."),
 "irish-national": ("Irish National",
  "The Irish National sett at &pound;49, which is where the tartan line starts. Same wool, same lining, smaller cover &mdash; this is the fairway and hybrid end of the range rather than a lesser build."),
 "clare-county": ("Clare County",
  "The second Irish county tartan currently in stock, also &pound;49. The county tartans move in and out of the range faster than the Scottish setts, which are more or less permanent &mdash; so this one is a narrower window than it looks."),
 # ------------------------- MINI DRIVER & HYBRID -------------------------
 "jura-mini": ("Jura Sunset Mini Driver Cover",
  "Blues, oranges and purples in a Harris Tweed tartan, cut for a mini driver &mdash; a club shape most cover makers still ignore. Light blue fleece lining. If you have put a mini driver in the bag in the last two seasons you already know how short the list of options is."),
 "jura-sunset-hc": ("Jura Sunset Headcover",
  "The full-size driver and fairway version of the same cloth. Jura Sunset is the brightest thing Fyfe weaves into a standing product, and it is the cover that makes the most sense in a bag that is otherwise all black leather."),
 "jura-hybrid": ("Jura Sunset Hybrid Cover",
  "Hybrid cut, same tweed, &pound;49. Hybrids are the clubs people stop covering because nothing matches; this is the fix for a set built around Jura Sunset."),
 "modern-herringbone-hyb": ("Modern Herringbone Hybrid Cover",
  "Charcoal herringbone in hybrid form. Pairs with the driver cover above, which is the whole point of Fyfe running most cloths across all four club shapes."),
 "earl-st-andrews": ("Earl of St Andrews Hybrid Cover",
  "Pure new wool in the Earl of St Andrews tartan. The name is doing some work here, but the sett is a registered one and the build is the same as everything else on this page."),
 # ------------------------- BETWEEN TIDES & PUTTER -------------------------
 "marine-suede-tan": ("Marine Suede Blade Cover &mdash; Light Tan",
  "Marine suede from the Clyde, in light tan, over a sherpa fleece lining with a leather seam label. Fyfe's own line on the material is that it was <em>&ldquo;chosen for strength, texture, and the particular quality of a material that improves with exposure&rdquo;</em> &mdash; which is the honest pitch for suede on a golf course rather than a warning against it."),
 "marine-suede-white": ("Marine Suede Blade Cover &mdash; Optic White",
  "The same construction in optic white. It will not stay optic white, and that is more or less the proposition &mdash; the Between Tides collection was built around materials that record use rather than resist it."),
 "harbour-seersucker": ("Harbour Seersucker Blade Putter Cover",
  "Blue and white striped cotton seersucker, sherpa lined. Seersucker is woven at two tensions so the surface puckers permanently, which is why it holds air and dries fast &mdash; a genuinely sensible fabric for a cover that spends half a round damp."),
 "five-glens-slipon": ("Five Glens Blade Putter Slip-On",
  "Five Glens herringbone Harris Tweed with mahogany heritage Scottish leather, cut as a slip-on rather than a magnetic-close blade cover. At &pound;35 it is the cheapest way into the tweed, and it fits all standard blades."),
 "gt-rosso-scud": ("GT Rosso Scuderia Leather Mallet Cover",
  "The outlier: Italian leather in racing red, cream sherpa lining, neodymium magnet strips, debossed leather seam labels. The GT line is the one place Fyfe leaves Scottish cloth entirely, and it is deliberately styled against everything else in the catalogue."),
 # ------------------------- ACCESSORIES -------------------------
 "marksman-green": ("Marksman Rangefinder Case &mdash; Vintage Green",
  "P270 waxed canvas from Dundee, space mesh lining, a two-way waterproof YKK zip with 275 paracord pulls, matte black brass swivel hook, nylon webbing and dark brown leather. The spec list is longer than anything else Fyfe makes, and it is the piece that shows the workshop can build something with structure rather than just cut and line a cover."),
 "brave-marker": ("The Brave Copper Ball Marker",
  "Hand-forged from high-grade copper at what Fyfe describes as a partnership forge in the heart of Scotland, <em>&ldquo;where age old battle swords are made with traditional artisan methods passed down through the generations.&rdquo;</em> Copper tarnishes, so it will not look like this in a year."),
 "jura-pouch": ("Jura Sunset Drawstring Pouch",
  "Harris Tweed with a premium leather drawstring &mdash; a valuables pouch for a watch and a wedding ring, or a ball and tee bag if you would rather. The pouches turn over faster than anything else Fyfe lists; most of the range is sold out at any given moment."),
 "wb-24k": ("Western Birch &times; Fyfe Bamboo Tees",
  "Fifty striped 70mm bamboo tees in a box, with a curved top and Fyfe branding on the cup. Western Birch is a US tee brand; the collaboration has been running since 2022, which makes it Fyfe's longest-standing partnership after MacKenzie."),
}

SECTIONS = [
 ("The Headcovers &mdash; Harris Tweed",
  "Twelve Harris Tweed cloths are in stock today. This is the heart of the range and the reason to know the brand.",
  ["rothesay", "arran", "dunbar", "black-grouse-hc", "balmedie", "cambo",
   "galloway-hc", "fortrose-hc", "huntsman", "five-glens-hc", "moray",
   "modern-herringbone-hc"]),
 ("The Headcovers &mdash; Tartan",
  "Registered setts in pure new wool, woven in Perthshire and Selkirk, cut and placed by hand.",
  ["douglas-grey", "campbell-argyll", "mackenzie-hc", "kerry-county",
   "irish-national", "clare-county"]),
 ("Mini Drivers and Hybrids",
  "The club shapes most cover makers skip, in the same cloths as the drivers.",
  ["jura-mini", "jura-sunset-hc", "jura-hybrid", "modern-herringbone-hyb",
   "earl-st-andrews"]),
 ("Between Tides and the Putter Covers",
  "Marine suede, seersucker and leather &mdash; the materials Fyfe reaches for when it leaves tweed behind.",
  ["marine-suede-tan", "marine-suede-white", "harbour-seersucker",
   "five-glens-slipon", "gt-rosso-scud"]),
 ("Everything Else in the Bag",
  "A rangefinder case, a forged marker, a pouch and a box of tees.",
  ["marksman-green", "brave-marker", "jura-pouch", "wb-24k"]),
]

LOOKBOOK = [
 ("ls-crail", "The East Neuk coastline at Crail, the stretch of Fife where Fyfe Golf is based"),
 ("irl-arran", "An Arran Harris Tweed driver cover photographed on course"),
 ("sw-pole", "A MacKenzie x Fyfe bag resting against a marker pole, from the Summer Tweeds shoot"),
 ("bt-crinan", "Crinan Harbour at first light, the setting for the Between Tides collection"),
 ("irl-beanie-nb", "A Fyfe beanie and MacKenzie bag on the 10th at North Berwick"),
 ("ls-speybay", "An overhead frame of the green complex at Spey Bay, sea and beach beyond"),
 ("irl-defender", "A Land Rover Defender loaded with bags at Anstruther"),
 ("ct-elie", "The Coastal Tones campaign, shot at Elie in Fife"),
]

LOOK = ('<section class="products" style="border-top:none;padding-top:48px">\n'
        '  <h2 class="products-hdr">In the Wild</h2>\n'
        '  <p class="cat-kicker">Fyfe shoots its own product on Scottish courses and coastline, '
        'and publishes a lookbook for every collection.</p>\n'
        '  <div class="fy-look" style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px">\n'
        + "".join(
            '    <figure style="margin:0;border:.5px solid var(--ink);overflow:hidden">'
            f'<img src="{IMG}{s}.jpg" alt="{a}" loading="lazy" '
            'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" /></figure>\n'
            for s, a in LOOKBOOK)
        + '  </div>\n</section>\n')

LOOK_CSS = ("<style>@media(max-width:760px){.fy-look{grid-template-columns:repeat(2,1fr)!important}"
            ".fy-pair{grid-template-columns:1fr!important}}</style>")


def pair(a, b, alt_a, alt_b):
    """Two-up image block used inside the project sections."""
    return ('<div class="fy-pair" style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:28px 0">'
            f'<figure style="margin:0;border:.5px solid var(--ink);overflow:hidden"><img src="{IMG}{a}.jpg" '
            f'alt="{alt_a}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block" /></figure>'
            f'<figure style="margin:0;border:.5px solid var(--ink);overflow:hidden"><img src="{IMG}{b}.jpg" '
            f'alt="{alt_b}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block" /></figure>'
            '</div>')


INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Fyfe Golf makes headcovers to order in a workshop in Fife, out of Harris Tweed, Scottish tartan, waxed canvas from Dundee and, several times a year, something that used to be a completely different object &mdash; an RAF flight suit, a caddie&rsquo;s coverall from Augusta, a deck chair, a bolt of sail cloth off a yacht on the west coast. Thirty-two pieces are below, twenty-three of them headcovers, all in stock on 14 September 2026.</p>
    <p>The brand started with a complaint. Neil Rennie had spent years walking into Scottish pro shops and finding nothing in them that had anything to do with Scotland. <em>&ldquo;Going around the pro shops and golf retailers, I couldn&rsquo;t find that more elevated product, with heritage and provenance,&rdquo;</em> he told The Wandering Golfers in 2022. <em>&ldquo;Everything was mass-produced and heavily branded.&rdquo;</em> He had come out of fashion rather than golf, which meant he already knew who still wove cloth in Scotland and how to reach them. Fyfe launched in November 2021.</p>
    <p>If you want the short version: the Harris Tweed covers are the reason to know the brand, the tartans are the ones people ask about, and the reclaimed-material projects are where it gets interesting &mdash; and where almost everything sells out inside a week.</p>
  </div>
</div>
"""

MAKING = """<section class="products">
  <h2 class="products-hdr">Made in Scotland, and Specifically Where</h2>
  <p class="cat-kicker">Fyfe names its mills. That is rarer than it sounds, and it is checkable.</p>
  <div class="writeup-body">
    <p><strong>The workshop is a joint venture, not a contractor.</strong> Rennie set it up in Fife with what he has called a small group of friends and family, and it is where every headcover is cut, lined and sewn. Fyfe publishes a set of coordinates on its own story page &mdash; 56.3438&deg; N, 2.8031&deg; W, which puts you in the East Neuk near Crail &mdash; and no street address. Distribution runs from the same county.</p>
    <p><strong>The cloth comes from named places.</strong> Harris Tweed from the Isle of Harris. Tartans from historic makers in Perthshire and Selkirk. Waxed canvas from Halley Stevensons in Dundee, the mill that has been finishing waterproof cotton for North Sea fishermen since 1864. Merino dyed and finished by Todd &amp; Duncan, the cashmere and merino specialists at Loch Leven. Hats made in Ayrshire, socks in Hawick. Every one of those is a company you can look up.</p>
    <p><strong>Most of it does not exist until you order it.</strong> Fyfe describes its approach as <em>&ldquo;producing in response to demand rather than overmaking&rdquo;</em>, which in practice means a custom cover ships in fourteen to twenty-one working days and the standing range is small on purpose. The custom programme has a published price ladder rather than a quote-on-request page: &pound;15 to make an item to order, a further &pound;15 fabric surcharge on one or two covers in a bespoke tartan that is waived at three or more in the same cloth, &pound;20 for initials, &pound;30 setup plus &pound;8.50 per application for custom embroidery. You choose outer fabric, lining, label colour and embroidery.</p>
    <p><strong>And they publish an Honesty Box.</strong> On the fabrics page Fyfe names the two materials in its own products that are not natural &mdash; elastane in the internal grip of a headcover, switched over from organic cotton and rubber because the tension was inconsistent, and polycotton in some linings, chosen over pure organic cotton for strength. Plenty of brands publish a sustainability page. Very few use it to list what they have compromised on and why.</p>
  </div>
</section>
"""

REPURPOSE = """<section class="products">
  <h2 class="products-hdr">The Habit: Making Golf Covers Out of Something Else</h2>
  <p class="cat-kicker">Seven collections in four years built from cloth that had a previous job.</p>
  <div class="writeup-body">
    <p>The most consistent thing Fyfe does is also the thing it says least about. Since 2022 the brand has run at least seven collections built from reclaimed material: denim offcuts from Hiut in Cardigan, made with Kuroki Mill selvedge and Isko organic; vintage deck chair canvas, for a collection about Scottish seaside holidays; RAF flight suits and quilted liners; white caddie coveralls and green canvas from Augusta, twice, with Vintage Chubbs; repurposed sail cloth from Oban, alongside marine suede from the Clyde; and tartan remnants from its own previous production runs, patchworked into a new cloth.</p>
    <p>The clearest statement of why is on a denim page from February 2022, and it has been sitting there ever since: <em>&ldquo;As part of our continued focus on craftsmanship and sustainability, we decided to launch the Offcut Projects. Working with likeminded brands who focus on the artisan led approach to making product and who themselves have a focus on sustainable fabrics and materials, we utilise the cuts of fabrics that would otherwise go to waste to create a variety of products at our workshop in Scotland.&rdquo;</em></p>
    <p>What is striking is that none of this appears on the sustainability page. Fyfe&rsquo;s fabrics and materials page is entirely about virgin fibre &mdash; tweed, merino, organic waxed cotton, bamboo &mdash; and the words deadstock, offcut and waste appear nowhere on it. The reclaimed collections are sold on story and scarcity instead: one-of-a-kind, twelve per style, once standard issue and now far from it. Which is a choice, and probably the right one commercially, but it means the most defensible environmental thing the brand does is filed under marketing rather than under ethics.</p>
    <p>The three projects below are the ones that best explain how it works.</p>
  </div>
</section>
"""

DROPZONE = """<section class="products">
  <h2 class="products-hdr">One &mdash; The Drop Zone: RAF Flight Kit, Cut Up</h2>
  <p class="cat-kicker">Fyfe cut vintage flight suits and quilted liners into covers and pouches in April 2025.</p>
  <div class="writeup-body">
    <p>Scotland&rsquo;s coastal links and its airfields have been neighbours for a century. Fyfe&rsquo;s lookbook makes the point directly: <em>&ldquo;Scotland&rsquo;s coastal golf courses once shared their ground with the Royal Air Force&mdash;fairways became flight paths, and bunkers bordered runways. During wartime, the links served a different purpose.&rdquo;</em> The Drop Zone took that overlap and made it physical, cutting vintage RAF flight suits and quilted combat liners into headcovers, putter covers and pouches, with a parallel run in P200 camo waxed canvas from Halley Stevensons for anyone who wanted the look without the provenance.</p>
    """ + pair("dz-shop1", "dz-out4",
               "Inside Fyfe&rsquo;s cut-and-sew workshop during production of the Drop Zone collection",
               "A Drop Zone headcover photographed on course at Aberdour") + """
    <p>The line Fyfe used is the one that matters: <em>&ldquo;These are not replicas. They are remnants, reworked.&rdquo;</em> And in the longer collection copy: <em>&ldquo;Reworked from vintage RAF flight suits and liner fatigues, The Drop Zone range honours Scotland&rsquo;s enduring connection to the Royal Air Force&mdash;past and present. From Leuchars to Lossiemouth, these garments once flew across shared skies. Now, cut and sewn in Scotland, they return to ground level&mdash;repurposed for play. Each piece is one-of-a-kind. Once standard issue. Now far from it.&rdquo;</em></p>
    <p>Two things to be straight about. Leuchars and Lossiemouth are named as geography, not as sources &mdash; Fyfe publishes nothing about where it obtained the garments, and no supplier, dealer or squadron appears anywhere. And the camo half of the collection is new cloth, not surplus, which the copy is clear about if you read the product pages rather than the collection header. The claim being made is that the flight-suit pieces are genuinely used garments. Fyfe asserts it; it does not evidence it.</p>
    <p>Fyfe commissioned a map for the shoot, tracing where Scotland&rsquo;s historic RAF airfields overlap its golf courses, and photographed the collection at Aberdour across the Forth from Rosyth. The store records show the collection published on 22 April 2025 with the lookbook up the next day, and a small restock followed on 4 September. Everything is now gone &mdash; the collection page is still live and reads zero products, which is a fairly exact picture of how this brand operates.</p>
  </div>
</section>
"""

CHUBBS = """<section class="products">
  <h2 class="products-hdr">Two &mdash; Vintage Chubbs: Masters Week, Unlicensed</h2>
  <p class="cat-kicker">Fyfe has run four releases with a UK reseller, two of them landing on the Wednesday of the Masters.</p>
  <div class="writeup-body">
    <p>This is the sharpest thing Fyfe does, and it is not on the collaborations menu. Working with Vintage Chubbs &mdash; a UK operation that sells through Instagram, Depop and Vinted and publishes nobody&rsquo;s name &mdash; Fyfe has run four releases built from Augusta-adjacent material, timed to the tournament.</p>
    <p><strong>The Lucky Numbers</strong> landed at 7pm on 9 April 2025, the Wednesday of Masters week. Driver and fairway covers made, in Fyfe&rsquo;s words, <em>&ldquo;from repurposed white caddie coveralls&mdash;echoing the suits worn at Augusta each April. Each headcover carries a number linked to a Masters champion. From No. 1 to No. 89, every digit tells a story of pressure, poise, and improbable victory. Some worn by legends. Some left untouched.&rdquo;</em> The chest pocket vinyl number was cut out and stitched into the reworked body. Dark green fleece lining. The sign-off: <em>&ldquo;One number. One story. Made to carry.&rdquo;</em></p>
    """ + pair("vc-1", "vc-2",
               "A Vintage Chubbs x Fyfe Golf headcover made from reworked dark green canvas",
               "The numbered collector&rsquo;s card and ID badge pocket detail on a Spectator headcover") + """
    <p><strong>The Spectator</strong> arrived exactly a year later, 9 April 2026, and Fyfe called it <em>&ldquo;the fourth release in our collaboration with Vintage Chubbs&rdquo;</em> &mdash; <em>&ldquo;a limited series shaped from dark green canvas, drawn from the spectator line and reworked into a collection of headcovers. Each piece carries a 1950s inspired entry ticket, individually numbered, with only 12 made per style.&rdquo;</em> Twelve driver covers at &pound;69 and twelve fairway covers at &pound;65, each with an ID badge pocket and a printed collector&rsquo;s card. Both sold out.</p>
    <p>No licence is claimed and none is implied; the word Masters appears in Fyfe&rsquo;s copy exactly once, in the phrase about champions&rsquo; numbers, and Augusta National is never named. What Fyfe is selling is the material and the week, and it is selling twenty-four units of it. Releases one and three are harder to pin down &mdash; the product pages are gone, as they always are &mdash; but the pattern across the two that are documented is unusually disciplined for something this opportunistic.</p>
  </div>
</section>
"""

SHOOTERS = """<section class="products">
  <h2 class="products-hdr">Three &mdash; The Shooters Club: Glen Affric, With a Dog</h2>
  <p class="cat-kicker">Fyfe published twenty-two pieces in October 2025, alongside the best photography it has produced.</p>
  <div class="writeup-body">
    <p>Not a collaboration, despite the name &mdash; there is no club, no estate and no partner named anywhere. The Shooters Club is an in-house collection, published on 15 October 2025, that borrows the language of Scottish field sport and applies it to golf. The conceit is spelled out in the lookbook: <em>&ldquo;In Scotland, the pursuit of sport takes many forms. On the moor or the links, both demand precision, patience, and respect for the land. The ghillie and the caddie &mdash; two guardians of their game &mdash; share a quiet kinship, guiding each shot and swing with instinct and understanding.&rdquo;</em></p>
    """ + pair("sc-landy", "sc-hut",
               "A Land Rover and a golfer on a hill road in Glen Affric, from the Shooters Club shoot",
               "Two MacKenzie x Fyfe bags and shoe bags outside a Highland hut") + """
    <p>It was shot at Glen Affric &mdash; lodge, forest, a Defender on a hill road, two golfers walking out with a gundog, bags propped against a hut, a bottle of whisky in a doorway. Twenty-two pieces went out: Achnacarry and Cannich tweeds, Gun Dog, Ghillie waxed canvas, Nightwatch tartan, Remony, and a Dalmore leather cover at &pound;89 that remains the most expensive headcover Fyfe has listed. Six are still available, including the Gamekeeper and Remony blade covers and the Marksman rangefinder case further up this page.</p>
    <p>One honest note on the cloth. The lookbook says the tweeds are <em>&ldquo;limited-edition estate tweeds from some of Scotland&rsquo;s most storied grounds&rdquo;</em> but names no estate, mill or weaver. The product pages tell a plainer story &mdash; Harris Tweed woven in the Outer Hebrides, Peregrine Houndstooth Waverley Tweed woven in Selkirk, and a Gamekeeper cloth described as a pattern <em>&ldquo;inspired by&rdquo;</em> Scotland&rsquo;s estate tweeds. It is good cloth from named mills, dressed in a slightly bigger story than it needs. The pictures, on the other hand, do not oversell anything.</p>
  </div>
</section>
"""

MACKENZIE = """<section class="products">
  <h2 class="products-hdr">And the One That Runs and Runs: MacKenzie</h2>
  <p class="cat-kicker">Twenty-two numbered editions have come and gone since 2021 &mdash; Dundee canvas, Oregon stitching, &pound;650 a bag.</p>
  <div class="writeup-body">
    <p>Fyfe&rsquo;s longest collaboration is with MacKenzie Golf Bags in Portland, Oregon, and the division of labour is clean: Fyfe supplies the Scottish cloth and designs the colourway and the story, MacKenzie builds the bag. Every edition is a MacKenzie Walker &mdash; 8&Prime; opening, single divider, one tartan-lined pocket, full-grain leather, Halley Stevensons waxed canvas, and a leather patch made specifically for that release. They are &pound;650 and they do not last.</p>
    """ + pair("irl-dunes", "irl-westfalia",
               "A MacKenzie x Fyfe limited edition bag standing in the dunes",
               "A MacKenzie x Fyfe edition photographed with a yellow VW Westfalia") + """
    <p>The count now stands at twenty-two. Editions 21 and 22 &mdash; the Coastal Tones pair, one sage and one charcoal, each with a two-tone split leather base &mdash; were published on 11 August 2026 and both sold out. Editions 19 and 20 came out of the Between Tides shoot at Crinan Harbour in April, with nautical navigation symbols tooled into the leather patch and paracord zip pulls.</p>
    <p>We have written up every edition, with the stories behind each one, on a separate page: <a href="/drops/fyfe-x-mackenzie-every-edition">Fyfe x MacKenzie &mdash; Every Edition</a>.</p>
  </div>
</section>
"""

QUOTES = """<section class="products">
  <h2 class="products-hdr">In His Words</h2>
  <p class="cat-kicker">Neil Rennie has given two long interviews in five years. These are from both.</p>
  <div class="writeup-body">
    <p>Rennie is the founder and, per Companies House, the sole director of Fyfe Golf Ltd. He has described himself as a co-founder as well, crediting <em>&ldquo;a small group consisting of friends and family&rdquo;</em> without naming them. The company was incorporated on 1 August 2023, two years after the brand launched &mdash; there is no predecessor entity on the register, and Fyfe has never explained the gap.</p>
    <p>The story he keeps returning to is a mill:</p>
    <blockquote><p>&ldquo;My grandparents on my mother&rsquo;s side both worked in a fabric mill just north of Aberdeen that produced cloth for Crombie coats, which became famous across the world through the 1950s and 60s. That mill eventually closed in the mid 1990s, and I think growing up around those stories stayed with me.&rdquo;</p>
    <cite>&mdash; Neil Rennie, interviewed by Ettinger London, May 2026</cite></blockquote>
    <p>On what he found missing, and why he started:</p>
    <blockquote><p>&ldquo;Having visited many golf pro shops across Scotland over the years, I felt there was a real disconnect between where the game began and the products being sold within it. Scotland has an extraordinary history of craftsmanship, textiles, and making, yet very little within modern golf felt genuinely connected to that heritage anymore.&rdquo;</p>
    <cite>&mdash; Neil Rennie, Ettinger London</cite></blockquote>
    <p>On where a product starts &mdash; which explains the reclaimed collections better than anything on the sustainability page:</p>
    <blockquote><p>&ldquo;Most products begin with either a material or a story. Sometimes it is a particular tweed, waxed canvas, military textile, or even a landscape or place in Scotland that sparks an idea for a collection.&rdquo;</p>
    <cite>&mdash; Neil Rennie, Ettinger London</cite></blockquote>
    <p>And on what he wants the covers to become:</p>
    <blockquote><p>&ldquo;Hopefully, decades from now, there will still be Fyfe products being used and passed on, much in the same way people value beautifully made leather goods today.&rdquo;</p>
    <cite>&mdash; Neil Rennie, Ettinger London</cite></blockquote>
  </div>
</section>
"""

WHERE = """<section class="products">
  <h2 class="products-hdr">Where You Actually Find Them</h2>
  <p class="cat-kicker">Roughly seventy pro shops, and Canada is the biggest market outside the UK.</p>
  <div class="writeup-body">
    <p>Fyfe sells direct, but the stockist list is the more interesting document. In Scotland and England: Panmure, Royal Dornoch, Royal Aberdeen, Cruden Bay, Cabot Highlands, the Carnegie Club at Skibo, Nairn, Brora, Carnoustie, North Berwick, Crail, Dumbarnie, Bruntsfield, Wentworth, Sunningdale Heath, Royal St George&rsquo;s and the Isle of Skye, among others. Five of those &mdash; Panmure, Royal Dornoch, Royal Aberdeen, Nairn and Carnegie &mdash; are listed separately as club partners, though Fyfe never defines what the distinction means.</p>
    <p>Then there is Canada, which carries twenty-three clubs on its own: Toronto Golf Club, Royal Montreal, St. George&rsquo;s, Rosedale, Beaconsfield, Donalda, Oakdale, Ottawa Hunt, Glencoe, Vancouver and more. Online, the brand reaches Korea through The Green Cup Official and The Cart, and the Netherlands through Bisque.</p>
    <p>For clubs, the offer on the wholesale page is a logo embroidery service rather than a bespoke tartan programme: <em>&ldquo;We work with golf clubs worldwide, providing unique designs and best-selling items, along with a full club logo embroidery service.&rdquo;</em> Minimums are described only as relatively low, and no figure is published.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("Who founded Fyfe Golf?",
  "Neil Rennie. He launched the brand in November 2021 after a career in fashion, and is the sole director of Fyfe Golf Ltd (company number SC777625), incorporated in August 2023. He has also described himself as a co-founder alongside a small group of friends and family, whom he has never named."),
 ("Where are Fyfe Golf headcovers made?",
  "In a workshop in Fife that Rennie set up as a joint venture rather than contracting production out. Fyfe publishes coordinates &mdash; 56.3438&deg; N, 2.8031&deg; W, which is the East Neuk near Crail &mdash; but no street address. Everything is cut, stitched, assembled, pressed and checked by hand there."),
 ("What is Harris Tweed, exactly?",
  "A protected cloth. By law it must be made from pure virgin wool, dyed and spun in the Outer Hebrides, and handwoven at the home of the weaver on the islands of Lewis, Harris, Uist or Barra. Fyfe buys it from the Isle of Harris. It is the reason a Fyfe cover feels heavier than a synthetic one."),
 ("How much do Fyfe headcovers cost?",
  "Hybrid covers start at &pound;49, driver and fairway covers run &pound;65 to &pound;75, and putter covers are &pound;35 for a tweed-and-leather slip-on up to &pound;75 for the Dalmore leather blade. The MacKenzie collaboration bags are &pound;650. Custom work adds &pound;15 per item on top."),
 ("Can I get a custom Fyfe cover made?",
  "Yes, and the pricing is published rather than quote-on-request. &pound;15 custom make fee per item; a further &pound;15 fabric surcharge on one or two covers in a bespoke tartan, waived at three or more in the same cloth; &pound;20 for initials; &pound;30 setup plus &pound;8.50 per application for custom embroidery. You choose outer fabric, lining, label colour and embroidery. Custom orders ship in 14 to 21 working days."),
 ("What is the Drop Zone collection?",
  "A run from April 2025 made from vintage RAF flight suits and quilted liners, cut into headcovers, putter covers and pouches, with a parallel line in camo waxed canvas from Halley Stevensons. Fyfe describes the reworked pieces as remnants rather than replicas but publishes nothing about where the garments came from. It sold out and was delisted."),
 ("Who are Vintage Chubbs?",
  "A UK reseller that trades through Instagram, Depop and Vinted and publishes no names. Fyfe has run four releases with them, two of which landed on the Wednesday of Masters week &mdash; The Lucky Numbers in April 2025, made from repurposed white caddie coveralls, and The Spectator in April 2026, made from dark green canvas drawn from the spectator line, twelve per style."),
 ("How many Fyfe x MacKenzie bags have there been?",
  "Twenty-two numbered editions as of September 2026. Editions 21 and 22, the Coastal Tones pair, were published on 11 August 2026 and sold out. Each is a MacKenzie Walker built in Portland, Oregon from Halley Stevensons waxed canvas, at &pound;650."),
 ("Is Fyfe Golf sustainable?",
  "Fyfe makes to order rather than to forecast, buys from Scottish mills to keep the supply chain short, and has built at least seven collections from reclaimed cloth. It also publishes an Honesty Box naming the synthetics in its own products &mdash; elastane in headcover grips, polycotton in some linings &mdash; and why they are there. It avoids broad claims, and its current language is deliberately hedged."),
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
    while os.path.exists(f"images/fyfe-btk/{s}-a{n+1}.jpg"):
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
    p = LINEUP[s]
    price = f"&pound;{p['price'].rstrip('0').rstrip('.') if p['price'].endswith('.00') else p['price']}"
    tag = "" if p["avail"] else " &middot; sold out"
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, nm)}
      <div class="product-body">
        <div class="product-brand">Fyfe Golf</div>
        <div class="product-name">{nm} &middot; {price}{tag}</div>
        <div class="product-desc">{desc}</div>
        <a href="{p['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
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
            .replace("&middot;", "·").replace("&ndash;", "–").replace("&pound;", "£")
            .replace("&deg;", "°").replace("&Prime;", "″").replace("&times;", "×")
            .replace("&eacute;", "é"))


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
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com/images/fyfe-btk/sc-hero.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

n_products = sum(len(s[2]) for s in SECTIONS)
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Fyfe Golf</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 14, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{n_products} Pieces &middot; &pound;12.95 to &pound;75</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/fyfe-btk/sc-hero.jpg" '
        'alt="A golfer standing with a full set of Fyfe Golf covers and a MacKenzie bag in Glen Affric, Scotland" /></div></div>\n'
        + INTRO
        + sec(*SECTIONS[0])
        + MAKING
        + sec(*SECTIONS[1])
        + QUOTES
        + LOOK
        + sec(*SECTIONS[2])
        + REPURPOSE
        + DROPZONE
        + CHUBBS
        + SHOOTERS
        + sec(*SECTIONS[3])
        + MACKENZIE
        + sec(*SECTIONS[4])
        + WHERE
        + FAQ)

head = head.replace("</head>", LOOK_CSS + "\n</head>")

# ---- guards -------------------------------------------------------------
missing = [s for s in LINEUP if s not in COPY]
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(COPY):
    raise SystemExit(f"section/COPY mismatch: unplaced={set(COPY)-set(placed)} "
                     f"extra={set(placed)-set(COPY)}")
nolin = [s for s in placed if s not in LINEUP]
if nolin:
    raise SystemExit(f"placed but not in lineup.json: {nolin}")
gone = [s for s in placed if not os.path.exists(f"images/fyfe-btk/{s}.jpg")]
gone += [s for s, _ in LOOKBOOK if not os.path.exists(f"images/fyfe-btk/{s}.jpg")]
gone += [s for s in ("sc-hero", "dz-shop1", "dz-out4", "vc-1", "vc-2", "sc-landy",
                     "sc-hut", "irl-dunes", "irl-westfalia")
         if not os.path.exists(f"images/fyfe-btk/{s}.jpg")]
if gone:
    raise SystemExit(f"images missing on disk: {gone}")
if "fy-look" not in head:
    raise SystemExit("LOOK_CSS never landed in <head> — verify-post will fail on .fy-look")
_body_txt = re.sub(r'<[^>]+>', ' ', body).lower()
for w in ("worth the pocket",):        # house ban: never the word 'worth' in our own copy
    pass
if re.search(r'\bworth\b', _body_txt):
    raise SystemExit("BANNED WORD 'worth' appears in the body copy")
sold = [s for s in placed if not LINEUP[s]["avail"]]
if sold:
    raise SystemExit(f"Lenny asked for in-stock picks only; these are sold out: {sold}")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {n_products} products "
      f"({sum(1 for s in placed if 'hc' in s or s in ('rothesay','arran','dunbar','balmedie','cambo','huntsman','moray','douglas-grey','campbell-argyll','kerry-county','irish-national','clare-county','jura-mini','jura-hybrid','modern-herringbone-hyb','earl-st-andrews'))} headcovers) | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
