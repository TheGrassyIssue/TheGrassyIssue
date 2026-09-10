#!/usr/bin/env python3
"""The Dyneema Edit — five picks Lenny chose from an 18-grid (2026-09-10), plus the
rest of Sentinel's Dyneema rack.

WHAT THE SWEEP FOUND (research/dyneema/candidates.json, 27 verified entries)
Golf-specific Dyneema is one shop: Sentinel Golf, whose Basecamp series runs
~12 Dyneema SKUs (Walkers built by MacKenzie, duffles/totes by 1733 Chicago, a
rain suit, a chair by Wildingout of Japan). Seamus's Golf on the Moon DCF bag,
Western Gales' Dyneema headcovers/pouches and Goldwin's Dyneema sacoche are all
sold out; Jones, Vessel, Stitch, Sunday, MNML, Ghost, Metalwood, Malbon,
Sugarloaf, Kingfisher and Quiet Golf carry none. Everything else is carry /
outdoor crossover. Lenny OK'd repeating Sentinel: "it's a niche product".

THE ETSY DITTY BAG (Lenny's add) IS NOT DYNEEMA-BRANDED. Ultralitesacks' listing
title says "Dyneema/ULTRA" but the fabrics offered are Ultra200X, UltraTX
(Challenge Sailcloth's UHMWPE laminates — same fibre family, different mill)
and UltraGrid (recycled nylon). The copy says so plainly. Sizes S/R/L/XL,
$17-28, 13-33 g, #3 waterproof YKK zip, made by Luke Nalley in Yellville AR.

FACTS come from research/dyneema/facts.md, every line sourced. Dates: dyneema.com
says "In 1969, we invented"; Heddels/Carryology put Pennings's discovery at 1963
and the fibre process at 1968 — the copy says "late 1960s" and names both. The
"15x steel" figure is strength-to-weight, and the copy says so. Bio-based
Dyneema is chemically identical to fossil UHMWPE and does not biodegrade — the
copy does not imply otherwise. No Mooty quote about Dyneema exists; the pull
quote is his general materials line from The Old Ghosts (9 Dec 2025), verbatim.

Deliberately NOT asserted: that Dyneema is "the material of 2026" as fact (it's
Lenny's editorial call — the intro frames it as where the material is showing
up, with the 2025-26 launches as evidence); any restock date; that MacKenzie
sells the Dyneema Walker itself (it doesn't — Sentinel-only build).

House FAQ markup is <details class="faq-q"><summary>Q</summary><p>A</p></details>.
"""
import re, os, json

SLUG  = "the-dyneema-edit"
TITLE = "The Dyneema Edit &mdash; A Golf Bag, a Pouch, a Wallet and a Sling in the Fiber That Floats"
PLAIN = "The Dyneema Edit — A Golf Bag, a Pouch, a Wallet and a Sling in the Fiber That Floats"
DESC  = ("Dyneema is fifteen times stronger than steel by weight and light enough to float. Twenty-eight pieces "
         "that use it, from Sentinel's $890 MacKenzie-built Walker to $15 laces, and what the material actually is.")
IMG = "/images/dyneema/"

# slug -> (brand, name, price, url, copy)
P = {
 "walker": ("Sentinel Golf &times; MacKenzie", "Basecamp Walker &mdash; Black Dyneema", "$890",
  "https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-rsxwj",
  "The MacKenzie Walker is the single-strap Sunday bag that has not changed shape since 1985, built in Beaverton, Oregon. Sentinel has it made in a bio-based Dyneema composite instead of leather or waxed canvas, which takes the whole bag to two pounds with the full-grain leather trim and stainless hardware still on it. One eight-inch pocket, a single divider, a stretch Dyneema interior pocket, a YKK reverse-coil waterproof zip. Made to order, six to eight weeks, and Sentinel notes the fabric is not stain-proof &mdash; the white version will show a season."),
 "pouch": ("Sentinel Golf", "Basecamp Pouch &mdash; Clay Dyneema", "$64",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-srmy2-h7w7l-8pcrj-ezbym-tynw6-t4tg3",
  "Nine and a half by six inches, which is tees, a glove, a marker and a phone. The front is the composite with its fibre grid showing through; the back is a reverse snap panel, and there is a webbing loop with a carabiner so it hangs off a bag ring rather than living at the bottom of a pocket. YKK AquaGuard zip, 550 paracord pull, cut and sewn in New York. Also in Silver."),
 "hawbuck": ("Hawbuck", "Lean Wallet H01 &mdash; Black", "$35",
  "https://hawbuck.com/products/lean%E2%84%A2-wallet-h01-black-dyneema-composite-fabric-hybrid",
  "Five grams and under a millimetre thick, which is the argument for a Dyneema wallet in one line. Hawbuck uses the Hybrid version of the composite &mdash; the fibre-and-film laminate with a woven polyester face bonded on for texture and abrasion resistance &mdash; so it reads as fabric rather than sailcloth. The material is made in Arizona, the wallet in the USA. It will not absorb moisture, which is the difference between this and the leather one after a rain delay."),
 "dsptch": ("DSPTCH", "Zero-1 Bag &mdash; RND Edition, Dyneema", "$248",
  "https://www.dsptch.com/products/zero-1-bag-rnd-edition-dyneema-black",
  "A six-litre sling in 5.0 oz Dyneema Composite Fabric bonded to perforated EVA foam, so the body has structure and padding without a lining. Thirteen by nine and a half by five inches, fourteen ounces, a front mesh gusset pocket and a fold-down magnetic buckle that doubles as a compression strap when the bag is half empty. It comes with DSPTCH&rsquo;s Fidlock sling strap. This is the piece for the nine holes after work when the bag stays in the car."),
 "ditty": ("Ultralitesacks", "Ultralight Zip Ditty Bag &mdash; Ultra", "$17&ndash;$28",
  "https://www.etsy.com/listing/4555443173/dyneemaultra-ultralight-zip-ditty-bag",
  "A note on the label first: the listing says Dyneema in the title, but the fabrics on offer are Ultra200X and UltraTX &mdash; Challenge Sailcloth&rsquo;s UHMWPE laminates, the same fibre family from a different mill &mdash; and UltraGrid, which is recycled nylon. Pick Ultra200X for structure. Four sizes from 8&times;4&times;1 to 13.5&times;5&times;4 inches, 13 to 33 grams, a #3 waterproof YKK zip, sewn by Luke Nalley in Yellville, Arkansas. At this weight and price it is the thing to organise the inside of a golf bag: balls in one, cables in another, the rain glove in a third."),
 # the rack
 "walker-white": ("Sentinel Golf &times; MacKenzie", "Basecamp Walker &mdash; White Dyneema", "$890",
  "https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-rsxwj-ykzhj",
  "The same bag in white composite, which shows the fibre grid more clearly than the black and is the one in Sentinel&rsquo;s Expedition One film. Made to order, all sales final, and the page says it plainly: not stain-proof."),
 "suit": ("Sentinel Golf", "Dyneema Suit &mdash; Olive", "$540",
  "https://www.sentinelgolf.us/shop/p/8t95uvw1ec28h1za76ycshtzy2kvha-57hyk-8trkf-6g8w5-b2y36-ftww5-a4fjc-228g6-glf2t",
  "Jacket and pant in a four-way-stretch Dyneema ripstop from Japan &mdash; woven fibre this time, not the laminate &mdash; water repellent, windproof, with hidden waist and pocket zips and shock-cord at the waist and ankle. Cut and sewn in the USA; the zips are YKK from Japan and Canada, the snaps Kane-M. Also in Navy."),
 "duffle": ("Sentinel Golf &times; 1733", "Basecamp Duffle &mdash; Gray Dyneema", "$340",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-kjjr6-6gc6d-ar5fg-ykh5a-dbfwy-mkdrf-ze83c-r74ja-styrm-7dwcx-9s95h",
  "A 28-litre barrel duffle, 21 by 10 by 10 inches, built by 1733 in Chicago with a triple-layer body, two exterior zip pockets, a removable shoulder strap and 400D packcloth lining. Sized for a long weekend of golf clothes. Also in Black."),
 "tote": ("Sentinel Golf &times; 1733", "Basecamp Tote &mdash; Olive Dyneema", "$340",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-kjjr6-6gc6d-ar5fg-ykh5a-dbfwy-mkdrf-ze83c-r74ja-amdsg-knj8p-d5r8d-d2w2w-6m378",
  "The zip tote from the same Chicago workshop: Dyneema shell, a cotton-batting mid layer, 400D packcloth inside, a laptop sleeve and a removable strap. Nineteen by 13.5 by 7 inches, 26 litres. Also in Gray."),
 "chair": ("Sentinel Golf &times; Wildingout", "Basecamp Chair &mdash; White Dyneema", "$480",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-bj2ct-xf4dn-x8w8x-3ddk7-mjerl",
  "Wildingout&rsquo;s Chair1987, made in Japan with a Japanese chestnut frame delivered unpainted and a white Dyneema seat. 3.2 kilos, packs to 13 by 13 by 65 centimetres, rated to 100 kilos, with its own bag. Made to order in a limited batch, eight to twelve weeks. Not for wet ground."),
 # off the course — nine more, all Dyneema-branded fibre
 "norda": ("norda", "001A &mdash; Abyss", "$295",
  "https://nordarun.com/products/001a-m-abyss",
  "The trail shoe with the seamless woven Dyneema upper &mdash; norda&rsquo;s own line is that it was the first &mdash; and the laces are Dyneema too. 268 grams in a men&rsquo;s 8.5, a Vibram soleplate, and an upper that does not stretch, scuff or hold water, which is most of what a golf shoe is asked to do on a wet morning. norda says to go up half a size."),
 "porter": ("Porter-Yoshida &amp; Co.", "Freestyle Dyneema Coin Case", "$172",
  "https://monohawaii.com/products/porter-yoshida-co-freestyle-dyneema-coin-case",
  "Porter was the first Japanese bag house to use Dyneema Bonded Leather, ECCO&rsquo;s process of fusing cowhide to a Dyneema backing so the leather can be skived paper-thin without tearing. A 110 by 65 millimetre coin case with a card pocket and a D-ring for a belt loop, made in Japan. The maker warns that water and sun will fade it, which is the leather talking, not the fibre."),
 "vollebak": ("Vollebak", "Indestructible Belt &mdash; Black", "$395",
  "https://vollebak.com/products/indestructible-belt-black-edition",
  "A belt strap with a Dyneema core that Vollebak says you could hang more than four tonnes from, closed with a COBRA buckle rated to 1.8 tonnes and finished with an engraved Riri tip. Twelve rows of bonded stitching. It ships in an anodised metal case with a 3D-printed latch, which tells you the price is partly theatre and partly the buckle."),
 "satisfy": ("Satisfy", "Justice&trade; Dyneema Trail Band", "&euro;160",
  "https://satisfyrunning.com/products/justice-dyneema-trail-band",
  "A running belt from the Paris brand with nine pockets, one zipped, and abrasion panels cut from Justice, an Italian knit that is 64 percent Dyneema with elastane and polyester. 75 grams in a medium. Worn under a polo it carries a phone, a scorecard and a sleeve of balls without a pocket to bounce, which is the argument for it on a walking course. Priced in euros on Satisfy&rsquo;s site; the US checkout converts."),
 "andwander": ("and wander", "UL Wallet with Dyneema &mdash; Dark Gray", "C$156",
  "https://outnaboutboutique.com/products/and-wander-ul-wallet-with-dyneema-dark-gray",
  "Eleven grams, 10.5 by 9.5 centimetres closed, three card slots, a coin slot, a note slot and a taped waterproof zip, from the Tokyo brand that has done more than anyone to make the material look considered rather than technical. Currently easiest to buy from Out n About in Canada, in Canadian dollars."),
 "hilltop": ("Hilltop Packs", "Ultralight Dyneema Wallet", "$22",
  "https://hilltoppacks.com/products/ultralight-dyneema-wallet",
  "The cheapest actual-Dyneema thing here: 7.9 grams, 5.25 by 3.25 inches, a weatherproof YKK zip and taped seams, cut from the same composite Hilltop uses for its packs and printed in-house in Waynesburg, Pennsylvania. Twenty-six variants, from plain grey to the full printed collage."),
 "laces": ("Windthrow", "Unbreakable Laces", "$15.75",
  "https://windthrow.co/products/unbreakable-laces",
  "Dyneema shoelaces with a waxed jacket and a loose core so the knot holds, load-tested past a thousand pounds. They do not absorb water, rot or freeze. For a golf shoe this means the laces outlast the shoe, and never go stiff after a wet round. Two lengths."),
 "drybag": ("Hammock Gear", "Dyneema Dry Bags", "$19&ndash;$45",
  "https://hammockgear.com/dyneema-dry-bags/",
  "Roll-top dry bags in 1.3 oz Dyneema Composite Fabric with fully taped seams, from Reynoldsburg, Ohio. The small is 2.2 litres and 18 grams; the large is 14 litres and 34 grams. Not rated for submersion, but for a rain glove, a spare polo or the electronics in a bag pocket on a Texas afternoon they are the right tool at the right weight."),
 "leash": ("Been Campin", "Ultralight Dog Leash &mdash; Black Amsteel", "$26.49",
  "https://beencampin.com/products/ultralight-dog-leash-black-amsteel",
  "The one for the dog who walks nine with you. The rope is 7/64-inch AmSteel, a spliced cord made of Dyneema fibre with a stated break strength of 1,600 pounds; the handle is Venom UHMWPE webbing rated to 1,800. Sixty-six inches long, 23 grams with the carabiner. Handmade, and the biner is your choice."),
 # used lightly — Dyneema as a detail
 "goldwin": ("Goldwin", "Moon Trail Pack", "$320",
  "https://usshop.goldwin-global.com/products/gm95799",
  "A 240-gram running vest-pack built for hundred-mile races, in a three-layer waterproof shell that Goldwin describes as Dyneema-reinforced; the body is polyester, and the fibre shows up in the back pocket cloth. Magnetic chest buckle, a vertical pole pocket, and a rounded pattern that carries the load high. Stock is thin: a handful of size 3 in black and quarry gray."),
 "acg": ("Nike ACG", "Ays&eacute;n Day Pack &mdash; 32L", "$200",
  "https://www.nike.com/t/acg-aysen-day-pack-32l-Fk4tzD",
  "A 26 by 11 by 7 inch roll-top in mostly recycled polyester, with Dyneema running through the roll-top so the fold survives being rolled every day. Aluminium trims, G-hooks with corded pulls, a laptop sleeve and an expandable bottle pocket. The one piece here from a brand everybody already owns something from."),
 "thrudark": ("ThruDark", "Strike Pants G2 &mdash; Khaki", "&pound;230",
  "https://www.thrudark.com/products/strike-pants-g2-khaki",
  "A tapered technical trouser from the British brand founded by former special-forces operators, in a bamboo-charcoal nylon with a Dyneema-and-Cordura composite blend on the lower legs and a Dyneema rear harness loop. Magnetised rear pockets, YKK zips, made in Vietnam. Priced in pounds; the US storefront converts."),
 "goruck": ("GORUCK", "MACV-2 Safety Boot &mdash; Mid Top", "$185",
  "https://www.goruck.com/products/macv-2-safety-boot-mid-top",
  "A composite-toe work boot in coyote brown with a Dyneema puncture-resistant sole plate, ASTM certified, and a perforated foam upper. Around 3.8 pounds a pair. Not a golf shoe, but for the guy who plays the muni after a jobsite it is the one boot on this list that does both."),
 # sold out — the golf pieces to watch for
 "seamus-moon": ("Seamus Golf", "Golf on the Moon &mdash; Dyneema Composite Fabric", "$95&ndash;$895 &middot; sold out",
  "https://www.seamusgolf.com/collections/golf-on-the-moon",
  "February 2021, for the fiftieth anniversary of Alan Shepard&rsquo;s six-iron: a Fescue carry bag in white Dyneema Composite Fabric, cut to echo the A7-L pressure suit, at 1.4 pounds and $695, numbered on the scorecard pocket; a limited run of fourteen kits at $895 with a reflective gold hood, a Fisher space pen and a moon marker; driver, fairway and blade covers from $95 with a removable hook-and-loop US flag on the lid. Most of it was marked sold out within ten days of launch, and the collection page now redirects. The one golf bag in the material anyone but Sentinel has shipped."),
 "wg-cover": ("Western Gales", "Dyneema Project Headcovers &mdash; NASA White", "$65&ndash;$75 &middot; sold out",
  "https://stateapparel.com/products/dyneema-project-dr-fw-hy",
  "Handcrafted triangular covers with a puffy fill, in white Dyneema composite with black stitch and binding and a black fleece lining; driver, fairway and hybrid, and the 2.0 version ran in Space Gray and Ice Blue. All variants sit at zero stock on State Apparel&rsquo;s site with no restock date, so this is a listing to check rather than a promise."),
 "wg-pouch": ("Western Gales", "Dyneema SP &mdash; NASA White", "$30 &middot; sold out",
  "https://stateapparel.com/products/dyneema-sp-nasa-white",
  "A triangular snap pouch, five and a half inches a side, two compartments, a heavy snap at the vertex and a regatta-rope loop for the bag. Out in both colourways. If it comes back it is the cheapest golf-specific Dyneema piece there has been."),
 "sen-scout": ("Sentinel Golf", "Basecamp Scout &mdash; Olive Dyneema", "$110 &middot; sold out",
  "https://www.sentinelgolf.us/shop/p/do-chua-ss2px-2ab6f-n44hy-wb8rn-mr5da",
  "Sentinel&rsquo;s rangefinder case, sized 3.5 by 5 by 2 inches, in a Dyneema body on a vinyl base with a 1.5 mm neoprene lining, a Fidlock magnet closure and a matte black brass swivel hook. Made in the USA. The ULTRA versions in charcoal and silver are also out, which suggests it sells through every run."),
 "sen-shoebag": ("Sentinel Golf &times; 1733", "Basecamp Shoe Bag &mdash; Olive Dyneema", "$148 &middot; sold out",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-kjjr6-6gc6d-ar5fg-ykh5a-dbfwy-mkdrf-ze83c-t6mze-njngz-bez54-kckwy",
  "The 1733 triple-layer build again &mdash; Dyneema shell, cotton batting, 400D packcloth &mdash; as an eight-litre shoe bag, 13.4 by 9 by 5.9 inches, with a paracord drawstring and a YKK AquaGuard zip. Out in olive, gray and black."),
 "sen-drybag": ("Sentinel Golf", "Basecamp Drybag &mdash; Olive Dyneema", "$82 &middot; sold out",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-nctfn-cx85f-wm89j-nrcwb-amgxm-7lchk",
  "An 18 by 13.5 by 4.5 inch flat drybag in a custom-printed Dyneema composite, every seam finished with waterproof heat tape inside and out, closed with a Fidlock magnet. The ULTRA versions in silver and charcoal are in stock at the same price if you need the function before the fabric returns."),
 "sen-sock": ("Sentinel Golf", "Basecamp Sock &mdash; Dyneema Heather", "$38 &middot; sold out",
  "https://www.sentinelgolf.us/shop/p/mwqw2hk7jsxug69d9fa1t1gk7kdu6e-jg7sw-kz2dg-ftpet-ajk8r-myp3l-hzctp-wtgnr-axb2y",
  "A merino-and-Dyneema blend sock &mdash; Suedwolle merino with the fibre knitted in for abrasion, the way it is used in cut-resistant workwear &mdash; one size for a men&rsquo;s 9 to 13, made in the USA. Sentinel notes it is not stain-proof. The only Dyneema golf sock we know of."),
}
FIVE = ["walker", "pouch", "hawbuck", "dsptch", "ditty"]
NINE = ["norda", "porter", "vollebak", "andwander", "hilltop", "laces", "drybag", "leash"]
LIGHT = ["acg", "thrudark", "goruck"]
GONE = ["seamus-moon", "wg-cover", "wg-pouch", "sen-scout", "sen-shoebag", "sen-drybag", "sen-sock"]
RACK = ["walker-white", "suit", "duffle", "tote", "chair"]

def frames(s):
    n = 0
    while os.path.exists(f"images/dyneema/{s}-{n+1}.jpg"): n += 1
    assert n, s
    return n

def gal(s, name):
    n = frames(s)
    pl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name)).strip()
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}-1.jpg" alt="{pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}-{i+1}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def card(s):
    brand, nm, price, url, desc = P[s]
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, nm)}
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{nm} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>"""

def sec(hdr, kicker, items):
    c = "\n    ".join(card(x) for x in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>This is twenty-eight pieces made with Dyneema, from a $15 pair of laces to an $890 golf bag: five picks first, then every golf-specific piece that has sold out and is one to watch for, the rest of the one golf shop that has built a whole rack out of the material, eight more from off the course, and three where the fibre is a detail rather than the body. Everything was in stock on 10 September 2026.</p>
    <p>The material is the story. Dyneema is a polyethylene fibre that its maker describes as fifteen times stronger than steel by weight and light enough to float on water, and it spent its first thirty years in mooring lines, body armour and America&rsquo;s Cup sails. Ultralight hikers found it next, in the crinkly white laminate that used to be called Cuben Fiber. In the last year it has moved again: a new woven composite launched in July 2025, a Dyneema-denim sneaker out of Northampton in March, Avient adding fibre capacity in February. In golf it has so far arrived through Sentinel, which has been building bags, a rain suit and a chair in it since its Basecamp series started.</p>
    <p>Who it is for: the walker who counts ounces, anyone whose bag lives in a wet trunk, and the person who wants the thing in their hands to look like nothing else on the first tee.</p>
  </div>
</div>
"""

WHAT = """<section class="products">
  <h2 class="products-hdr">What Dyneema Actually Is</h2>
  <p class="cat-kicker">A Dutch lab accident, a gel-spinning patent, and two very different fabrics that share the name.</p>
  <div class="writeup-body">
    <p><strong>The fibre.</strong> Dyneema is a brand of ultra-high-molecular-weight polyethylene, or UHMWPE &mdash; the same polymer as a milk jug, spun so that the molecular chains line up along the fibre. Its maker&rsquo;s figure of fifteen times the strength of steel is a strength-to-weight number, not an absolute one, which is why the same fibre floats. It does not absorb water, it shrugs off UV and abrasion, and it is very slippery to stitch, which is part of why finished goods cost what they do.</p>
    <p><strong>The history.</strong> The discovery is credited to Albert Pennings, a chemist at DSM in the Netherlands, who in the late 1960s noticed strong fibrous crystals forming around a stirrer in a polyethylene solution. DSM patented the gel-spinning process in the seventies, commercialised the fibre in the eighties and has run the plant at Heerlen since 1990. In September 2022 DSM sold the business to Avient of Ohio for an enterprise value of &euro;1.45 billion.</p>
    <p><strong>Two fabrics.</strong> Most of what golfers will meet is Dyneema Composite Fabric: fibres laid in a grid and laminated between thin polyester films, non-woven, waterproof, and visibly crinkly. That was Cuben Fiber until DSM bought its maker, Cubic Tech of Mesa, Arizona, in May 2015 &mdash; a company whose laminates began as 1992 America&rsquo;s Cup sails. The Hybrid version bonds a woven polyester face onto the laminate for hand and abrasion resistance, which is what Hawbuck uses. Separately there is woven Dyneema, a ripstop cloth with the fibre in the weave, which is what Sentinel&rsquo;s rain suit is cut from and what the new Woven Composites are built around.</p>
    <p><strong>Bio-based.</strong> Since 2020 the fibre can be made from renewable ethylene derived from wood-pulp residue, on a mass-balance basis. Sentinel&rsquo;s bags use the bio-based grade. It is chemically identical to the fossil version, so it does not biodegrade; the gain is in the footprint, which Dyneema puts at ninety percent lower than generic HMPE fibre.</p>
    <p><strong>Ultra.</strong> The cottage-gear world also uses Ultra, from Challenge Sailcloth &mdash; a UHMWPE laminate that is not Dyneema-branded fibre. It is what the Etsy ditty bag below is made of, and the copy says so.</p>
  </div>
</section>
"""

QUOTE = """<section class="products">
  <h2 class="products-hdr">The Golf End of It</h2>
  <p class="cat-kicker">Sentinel&rsquo;s founder, on why the brand keeps bringing outside materials into golf.</p>
  <div class="writeup-body">
    <p>Sentinel&rsquo;s Basecamp series is where golf&rsquo;s Dyneema lives: the Walker is manufactured with MacKenzie Golf Bags in Beaverton, the duffles and totes with 1733 in Chicago, the chair with Wildingout in Japan, and the second Basecamp capsule in December 2025 added rain gear, carry bags and tents. Speaking to Michael Williams of The Old Ghosts that month, founder John Mooty put the project this way:</p>
  </div>
<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;Since it started, the project has always been about bringing new ideas, materials, and people into the golf space, not only to make it more interesting but to make it more fun. That is still the best part for me, but in terms of evolution, the most enjoyable challenge is exploring the boundaries (or lack thereof) beyond golf and how that can be done in both product and brand the right way, balancing innovation and tradition.&rdquo;<span class="pull-quote-attr">&mdash; John Mooty, Sentinel Golf founder &middot; The Old Ghosts, December 2025</span></div>
</div>
  <div class="writeup-body">
    <p>MacKenzie&rsquo;s own site offers the Walker in leather, waxed canvas, treated canvas and nylon; the Dyneema version exists only through Sentinel. If you have read our <a href="/drops/brand-to-know-sentinel-golf">Sentinel profile</a> or the <a href="/drops/the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site">MacKenzie collab archive</a>, this is where the two meet.</p>
  </div>
</section>
"""

LIGHT_NOTE = """<section class="products">
  <h2 class="products-hdr">A Note on the Label</h2>
  <p class="cat-kicker">New materials arrive as trim before they arrive as bodies.</p>
  <div class="writeup-body">
    <p>A fibre this expensive and this awkward to sew shows up in most products the way carbon fibre did in the nineties: as one panel, one strap, one plate, with the rest of the piece in something cheaper and easier. That is not a trick, it is how a material gets adopted, and the three pieces below are honest about it &mdash; Nike says the fibre &ldquo;runs through the roll top,&rdquo; ThruDark puts it on the lower leg, GORUCK in the sole. Expect more of this before you see many whole bags in it.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is Dyneema?",
  "A brand of ultra-high-molecular-weight polyethylene fibre, made by gel-spinning so the polymer chains align along the fibre. Its maker, Avient, describes it as fifteen times stronger than steel by weight and light enough to float on water. It does not absorb moisture and resists UV and abrasion."),
 ("What is the difference between Dyneema and Dyneema Composite Fabric?",
  "Dyneema is the fibre. Dyneema Composite Fabric is a non-woven laminate of that fibre laid in a grid between thin polyester films &mdash; the crinkly white material formerly sold as Cuben Fiber. Woven Dyneema is a separate cloth with the fibre in the weave; Sentinel&rsquo;s rain suit uses it."),
 ("Is Dyneema waterproof?",
  "The composite fabric is waterproof as a material because the films are continuous; whether a finished bag is waterproof depends on seams and zips. Sentinel and DSPTCH use YKK AquaGuard or reverse-coil waterproof zips. The fibre itself does not absorb water at all."),
 ("Why is a Dyneema golf bag $890?",
  "The Basecamp Walker is a made-to-order MacKenzie bag, built in Beaverton, Oregon, with full-grain leather trim and stainless hardware; MacKenzie&rsquo;s standard Walkers sit in the same range. The composite is expensive per yard and slow to sew. Sentinel lists it at $890 in black or white with a six-to-eight-week lead time."),
 ("Does Dyneema stain or wear?",
  "Sentinel&rsquo;s product page says the fabric is not stain-proof, and the white composite shows marks. The laminate creases visibly with use, which owners of ultralight packs either love or don&rsquo;t. Abrasion resistance is high; the Hybrid version used by Hawbuck adds a woven face for more of it."),
 ("Is the Etsy ditty bag really Dyneema?",
  "Not by brand. Ultralitesacks lists it as Dyneema/Ultra, but the fabrics offered are Ultra200X and UltraTX, Challenge Sailcloth&rsquo;s UHMWPE laminates, plus UltraGrid, a recycled nylon. Same fibre family, different mill. At $17 to $28 and under 35 grams it does the job of organising a golf bag either way."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&reg;", "®").replace("&times;", "×")
            .replace("&euro;", "€").replace("&ndash;", "–"))

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
for k in ("canonical", "og:url"):
    pat = r'(<link rel="canonical" href=")[^"]*(")' if k == "canonical" else r'(<meta property="og:url" content=")[^"]*(")'
    head = re.sub(pat, lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com/images/dyneema/hero.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)
assert "sentinel" not in head.lower() or "brand-to-know-sentinel" not in head, "template leak check"

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  The Dyneema Edit</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 10, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        '    <span>10 Pieces &middot; 4 Makers</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/dyneema/hero.jpg" '
        'alt="Three Sentinel Basecamp Walker golf bags in white and black Dyneema standing against a green bench" /></div></div>\n'
        + INTRO + WHAT
        + sec("The Five", "The picks run from an $890 made-to-order golf bag to a $17 ditty bag that weighs less than a ball.", FIVE)
        + QUOTE
        + sec("Sold Out, Watch For It &mdash; The Golf Pieces",
              "Every golf-specific Dyneema product that has existed and is out today, from Seamus&rsquo;s 2021 moon bag to Sentinel&rsquo;s sock. None of these makers publishes a restock date.", GONE)
        + sec("The Rest of the Basecamp Rack &mdash; Sentinel Golf",
              "Everything else Sentinel currently sells in the material, in stock on 10 September 2026.", RACK)
        + sec("Off the Course &mdash; Eight More",
              "Shoes, wallets, a belt, dry bags and a dog leash, all cut from Dyneema-branded fibre. The makers run from Porter in Tokyo to a one-man shop in Waynesburg, Pennsylvania.", NINE)
        + LIGHT_NOTE
        + sec("Used Lightly &mdash; Dyneema as a Detail",
              "Three pieces where the fibre reinforces one part &mdash; a roll-top, a sole, a lower leg &mdash; and the rest is something else. The copy says which part.", LIGHT)
        + FAQ)

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(FIVE)+len(RACK)} products | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
