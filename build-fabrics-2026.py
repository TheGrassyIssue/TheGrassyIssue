#!/usr/bin/env python3
"""build-fabrics-2026.py — Our Favorite Fabrics of 2026, 25 November 2026 (Drops & Brands).
Lenny: "a post about our favorite fabrics of this year — Cordura nylon ripstop, Dyneema, organic cotton and natural
fibers", plus "a mackenzie bag from Sentinel on the dyneema list", "a good dive into the fabrics themselves in the
TGI take, really nerdy and detailed", "also include Sloat".
FACTS: research/fabrics26/facts.md (each fact sourced; brand claims attributed as claims). Products and prices read on
each brand's own store Nov 25, 2026. No FAQ. Template: standard product-card (donor brand-to-know-manors).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "favorite-golf-fabrics-2026-cordura-dyneema-organic-cotton"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/fabrics26"
TITLE = "Our Favorite Fabrics of 2026: Cordura, Dyneema, Organic Cotton and Ventile, Explained"
DESC = ("A nerdy guide to the four fabrics we liked most in golf this year: what denier means, why Dyneema floats, "
        "what makes cotton organic, and the WWII cotton that closes itself in the rain. 34 picks from Sentinel, "
        "Briefing, SLOAT, Dimple Divot, Students and more.")
H1 = "Our Favorite Fabrics of 2026"
FRAMES = json.loads((ROOT / "research/fabrics26/frames.json").read_text(encoding="utf-8"))

# code: (brand, name, price, url, copy)
P = {
 "C1": ("Dimple Divot", "Essentials Pouch, Smoke", "$120", "https://dimpledivot.com/products/essentials-pouch-smoke",
        "1000D Cordura outside, military-grade mesh inside so you can see what&rsquo;s in it, and a Fidlock magnetic closure. Cut and sewn in New York."),
 "C2": ("Eastside Golf", "Eastside Golf Tote, Black", "$148", "https://eastsidegolf.com/products/egb1001-blk-black-eastside-golf-tote",
        "A Cordura nylon body with a reinforced base and woven nylon straps."),
 "C4": ("Gramicci", "Trail Day Pack 25L", "$150", "https://gramicci.com/products/trail-day-pack-25l",
        "210D Cordura, light enough for a daypack, with a laptop sleeve and side mesh pockets."),
 "C7": ("Gramicci", "Velcro Wallet", "$35", "https://gramicci.com/products/velcro-wallet-2",
        "The same 210D Cordura as the pack, folded into a wallet."),
 "C8": ("Students", "Mossy Oak Original Barrel Headcover", "$60", "https://studentsgolf.com/products/mossy-oak-original-cordura-nylon-barrel-headcover-1",
        "500D Cordura in Mossy Oak camo with a two-pass polyurethane coating, a water-repellent finish and a sherpa lining."),
 "C9": ("Students &times; Sugarloaf", "Patch Tote Bag", "$95", "https://studentsgolf.com/products/ssc-x-students-patch-tote-bag",
        "Heavy-duty 500D Cordura camo with hand-placed merit patches. Made in the USA."),
 "C10": ("Students &times; Sugarloaf &times; MacKenzie", "Driver Headcover", "$120", "https://studentsgolf.com/products/ssc-x-students-x-mackenzie-driver-headcover",
         "500D Cordura camo up top, navy leather below, sherpa inside. Handcrafted in Portland, Oregon."),
 "C13": ("Sun Mountain", "Eclipse E-1.5 Stand Bag", "$280", "https://www.sunmountain.com/products/eclipse-e-1-5-stand-bag",
         "A carry bag in Cordura ripstop, with two velour-lined pockets, one sized for a rangefinder."),
 "C14": ("VESSEL", "Player Air Stand", "$269 (reg. $379)", "https://vesselgolf.com/products/player-air-stand",
         "VESSEL rebuilt its Player bag in Cordura and says it cut the weight by nearly 30%."),
 "C15": ("Aberdeen West", "Cordura Track Jacket", "$235", "https://aberdeenwest.com/products/aberdeen-satin-trucker-jacket-copy-1",
         "Cordura nylon made with air-jet textured fibers, with a half-zip, hood and kangaroo pocket. Proof that Cordura isn&rsquo;t only for luggage."),
 "D11": ("Sentinel Golf &times; MacKenzie", "Basecamp Walker, Black Dyneema", "$890", "https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-rsxwj",
         "The MacKenzie Walker in Dyneema. Made to order, ships in 8&ndash;10 weeks, final sale. Also in <a href=\"https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-rsxwj-ykzhj\" target=\"_blank\" rel=\"noopener\">white</a>."),
 "D1": ("Briefing", "Driver Cover DL", "$330", "https://www.briefing-us.com/products/brg263g26",
        "A 500D Cordura ripstop body with a patch of ECCO leather layered with Dyneema. Two fabrics from this post in one cover."),
 "D3": ("Briefing", "Putter Cover DL", "$265", "https://www.briefing-us.com/products/brg263g30",
        "The same DL build in a blade cover."),
 "D4": ("Briefing", "Iron Cover DL", "$395", "https://www.briefing-us.com/products/brg263g29",
        "A full iron-set cover in the DL build, with a clip to hang it off the bag."),
 "D5": ("Briefing", "Cart Tote DL", "$655", "https://www.briefing-us.com/products/brg263t31",
        "Briefing&rsquo;s CR-9 tote, slimmed down to clear a tight trunk, with ECCO-and-Dyneema hybrid leather panels."),
 "D7": ("Briefing", "Transport Cover DL", "$1,200", "https://www.briefing-us.com/products/brg263g33",
        "A travel cover for a full caddy bag: Cordura ripstop body, Dyneema-backed leather panels."),
 "D13": ("Sentinel Golf &times; 1733", "Basecamp Duffle, Gray Dyneema", "$340", "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-kjjr6-6gc6d-ar5fg-ykh5a-dbfwy-mkdrf-ze83c-r74ja-styrm-7dwcx-9s95h",
         "A barrel duffle made with Chicago&rsquo;s 1733: triple-layer build, YKK AquaGuard zipper, hand-tied paracord pulls."),
 "D15": ("Sentinel Golf", "Dyneema Suit, Olive", "$540", "https://www.sentinelgolf.us/shop/p/8t95uvw1ec28h1za76ycshtzy2kvha-57hyk-8trkf-6g8w5-b2y36-ftww5-a4fjc-228g6-glf2t",
         "Jacket and pants in four-way-stretch Dyneema ripstop: water repellent, windproof and breathable. Cut and sewn in the USA."),
 "D9": ("Defy", "Project Dyneema Pouches, Black", "$90 (reg. $99)", "https://defybags.com/products/project-dyneema-set-of-three-pouches-black",
        "Small, medium and large pouches in 5 oz Dyneema, a quarter-pound for all three. Made for camera gear; it works just as well in a golf bag."),
 "D10": ("Goldwin", "Moon Trail Pack", "$320", "https://usshop.goldwin-global.com/products/gm95799",
         "A 100-mile trail-running vest with a Dyneema-reinforced three-layer waterproof shell. Overkill for a walking round, which is the point."),
 "N1": ("Casualist", "Pleated Golf Trousers, Beige", "$160", "https://casualist.com/products/pleated-golf-trousers-organic-cotton-copy",
        "Smooth organic cotton twill, a high waist with a hidden drawstring, and clean front pleats. Made in Portugal."),
 "N3": ("Radmor", "Ethan Knit Polo", "$101.50 (reg. $145)", "https://radmorgolf.com/products/ethan-knit-polo",
        "Organic cotton, organic silk and recycled nylon. The silk gives it a slight sheen and a softer drape."),
 "N5": ("Sounder", "Big Mach Long Sleeve Polo Sweat", "&pound;50 (~$64, reg. &pound;100)", "https://soundergolf.com/products/big-mach-long-sleeve-polo-sweat-sea-blue",
        "A 100% organic cotton rugby polo named for Machrihanish, with thumbhole cuffs. Made in Portugal."),
 "N9": ("Mogshade", "O.B. Oversized Sweat", "$91", "https://www.mogshadegolf.com/products/o-b-oversized-sweat",
        "100% organic cotton with screen-printed art by Fiumani. Made in Portugal."),
 "N10": ("Morning People Clothiers", "The Cotton Knit Sweater", "$95", "https://morningpeopleclothiers.com/products/the-cotton-knit-sweater",
         "100% organic cotton in a medium knit. The brand&rsquo;s pitch: warmth &ldquo;without plastic.&rdquo;"),
 "N13": ("Olydoe", "Pleated Walker Pant", "$115", "https://olydoe.com/products/pleated-walker-pant",
         "Cotton, Tencel and linen. The linen breathes; the Tencel is there to fight linen&rsquo;s wrinkles."),
 "N21": ("Olydoe", "Italian Cashmere Sweater", "$340", "https://olydoe.com/products/cashmere-sweater",
         "100% cashmere from a family mill in Northern Italy, in a tight micro-rib."),
 "N15": ("Siegelman Stable", "Knit Cardigan", "$456", "https://siegelmanstable.com/products/knit-cardigan-2",
         "Alpaca and RWS extrafine merino with recycled nylon, in seafoam green."),
 "N16": ("Criquet", "Alpaca Sweater Hoodie, Smoke", "$228", "https://criquetshirts.com/products/aplaca-sweater-hoodie-tbd-lt-gray",
         "60% baby alpaca in a waffle stitch. Criquet calls it &ldquo;the softest thing we&rsquo;ve ever made.&rdquo;"),
 "N20": ("Bluegrass Fairway", "Charcoal Beanie", "$32", "https://www.bluegrassfairway.com/products/bluegrass-fairway-charcoal-beanie",
         "55% ramie, 45% cotton. Ramie is another bast fiber, from the stem of a plant in the nettle family."),
 "S11": ("SLOAT", "Organic Ventile Jacket", "$595", "https://sloat.cc/products/mens-ventile-windbreaker",
         "Organic Ventile, sewn in Portugal. Wind- and rain-resistant without a coating."),
 "S13": ("SLOAT", "Organic Ventile Wind Shirt", "$295", "https://sloat.cc/products/mens-ventile-wind-shirt",
         "The lightest way into Ventile: a quarter-zip with raglan sleeves."),
 "S1": ("SLOAT", "Organic Cotton Caddie Short", "$145", "https://sloat.cc/products/organic-cotton-caddie-short",
        "305 gsm heavyweight organic cotton, flat front, tailored leg. Sewn in Portugal."),
 "S2": ("SLOAT", "Organic Cotton Caddie Pant", "$195", "https://sloat.cc/products/organic-cotton-caddie-pant",
        "The heavyweight version of SLOAT&rsquo;s Day Pant, inspired by what caddies wear."),
 "S9": ("SLOAT", "Organic Cotton Fleece Quarter Zip", "$225", "https://sloat.cc/products/mens-golf-quarter-zip",
        "480 gsm organic cotton fleece, a metal zip and concealed side pockets."),
 "S6": ("SLOAT", "Merino Polo", "$215", "https://sloat.cc/products/mens-merino-wool-golf-polo",
        "200 gsm RWS-certified merino jersey: temperature-regulating and odor-resistant."),
 "S10": ("SLOAT", "Organic Cotton Jersey Polo", "$155", "https://sloat.cc/products/mens-organic-cotton-golf-polo",
         "170 gsm organic cotton jersey, three-button placket, a slightly longer back hem."),
 "S3": ("SLOAT", "Organic Cotton Six Panel Hat", "$65", "https://sloat.cc/products/organic-cotton-six-panel-hat",
        "100% organic cotton, made in the USA, with a leather strap that patinas."),
}

GROUPS = [
 ("cordura", "Cordura", "The Workhorse: Cordura",
  "Pouches, totes, headcovers, two carry bags and a track jacket. Check the denier on each one: 210D, 500D and 1000D are very different fabrics.",
  ["C1", "C9", "C10", "C8", "C13", "C14", "C2", "C4", "C7", "C15"]),
 ("dyneema", "Dyneema", "The Fiber That Floats: Dyneema",
  "Sentinel&rsquo;s MacKenzie Walker leads, followed by Briefing&rsquo;s new DL series, which puts Dyneema and Cordura in the same piece.",
  ["D11", "D13", "D15", "D1", "D3", "D4", "D5", "D7", "D9", "D10"]),
 ("natural", "Organic Cotton, Ventile &amp; Natural Fibers", "The Farm Fibers: Organic Cotton &amp; Naturals",
  "Organic cotton is the same plant as regular cotton. The difference is how it&rsquo;s grown, without synthetic persistent pesticides, fertilizers or GMO seed, and certified from field to garment, not how it feels. For feel, look at staple length and weave: Ventile is regular-looking cotton made from extra-long fibers and woven tight enough to shed rain. Then merino, linen, cashmere, alpaca and ramie, which aren&rsquo;t cotton at all.",
  ["S11", "N1", "N3", "S1", "N5", "N9", "N10", "S6", "N13", "N21", "N15", "N16", "N20", "S13"]),
]

BANDS = {
 "cordura": [("band-c1.jpg", "Dimple Divot Essentials Pouches stacked in four colors", "1000D Cordura &middot; Dimple Divot"),
             ("band-c2.jpg", "A merit patch on Students and Sugarloaf camo Cordura", "500D Cordura camo &middot; Students &times; Sugarloaf"),
             ("band-c3.jpg", "Embroidery on a camo Cordura driver cover", "Driver cover detail &middot; Students &times; Sugarloaf &times; MacKenzie")],
 "dyneema": [("band-d1.jpg", "The grid of a Dyneema fabric close up on Sentinel's Basecamp Walker", "The grid &middot; Sentinel Basecamp Walker"),
             ("band-d2.jpg", "Gray Dyneema duffle fabric close up", "Basecamp Duffle &middot; Sentinel &times; 1733"),
             ("band-d3.jpg", "A translucent Dyneema pouch with a red zipper pull", "5 oz Dyneema &middot; Defy")],
 "natural": [("band-n1.jpg", "Close-up of a gray baby alpaca waffle knit", "Baby alpaca &middot; Criquet"),
             ("band-n2.jpg", "Close-up of navy organic cotton knit", "Organic cotton knit &middot; Morning People Clothiers"),
             ("band-s1.jpg", "Close-up of a black organic Ventile jacket", "Organic Ventile &middot; SLOAT")],
}

CSS = ('<style>/*TGI-FABRICS26*/'
       '.products-grid[data-n]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
       '@media(max-width:1024px){.products-grid[data-n]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '.fb-h{font-family:var(--serif);font-weight:600;font-size:clamp(22px,2.4vw,28px);margin:36px 0 12px}'
       '.fb-tbl{width:100%;border-collapse:collapse;margin:14px 0 22px;font-size:14.5px}.fb-tbl th{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;color:#2D4A2B;padding:8px 10px;border-bottom:.5px solid var(--ink)}'
       '.fb-tbl td{padding:10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top;line-height:1.45}.fb-tbl td:first-child{font-family:var(--serif);font-size:17px;white-space:nowrap}'
       '.fb-pq{font-family:var(--serif);font-size:clamp(22px,2.4vw,28px);line-height:1.35;color:#2D4A2B;margin:24px 0;padding:4px 0 4px 20px;border-left:2px solid #2D4A2B}'
       '.fb-src{font-family:var(--mono);font-size:10px;letter-spacing:.06em;opacity:.6;line-height:1.7;margin-top:22px}'
       '@media(max-width:820px){.fb-tbl .hm{display:none}.fb-tbl td:first-child{white-space:normal}}'
       '</style>\n')


def card(k):
    brand, name, price, url, copy = P[k]
    fr = FRAMES[k]
    label = H.escape(H.unescape(re.sub(r"<[^>]+>", "", f"{brand} {name}")).replace('"', ""), quote=True)
    imgs = "".join(f'<div class="pg-frame"><img src="{IMG}/{f}" alt="{label}{f" &middot; view {j+1} of {len(fr)}" if len(fr) > 1 else ""}" loading="lazy" /></div>' for j, f in enumerate(fr))
    nav = ""
    if len(fr) > 1:
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        nav = (f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>')
    return (f'<div class="product-card" id="p-{k.lower()}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>{nav}</div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div><div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div><a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def band(k):
    figs = "".join(f'<figure><img src="{IMG}/{s}" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for s, a, c in BANDS[k])
    return f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">Up Close</div>\n  <div class="ig-grid" style="margin-top:18px">{figs}</div>\n</section>\n'


def pq(text, who):
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def group(k, tag, cap, intro, ids):
    cards = "\n".join(card(i) for i in ids)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{k}">{cap}</h2>\n  <p class="cat-kicker"><strong>{tag}</strong>{intro}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n')


TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p><strong>We read a lot of product pages.</strong> After a year of it, the same few fabric names kept coming back, on bags, headcovers, polos and pants from the brands we like most. This is our list of favorites, and we&rsquo;re going deep: what each fabric actually is at the fiber level, what the numbers on the tag mean, and where the marketing ends and the chemistry starts. Brand claims are labeled as brand claims.</p>

    <table class="fb-tbl">
      <thead><tr><th>Fabric</th><th>What it is</th><th class="hm">The number to read</th><th>Watch out for</th></tr></thead>
      <tbody>
        <tr><td>Cordura</td><td>A brand of high-tenacity nylon 6,6</td><td class="hm">Denier (D): 210D light, 1000D heavy</td><td>Weight at high denier</td></tr>
        <tr><td>Dyneema</td><td>Ultra-high-molecular-weight polyethylene</td><td class="hm">Ounces per square yard on composites</td><td>Heat: melts at 144&ndash;152&deg;C</td></tr>
        <tr><td>Organic cotton</td><td>Cotton grown without synthetic pesticides, fertilizers or GMO seed</td><td class="hm">gsm, and the certification (GOTS / OCS)</td><td>Slow to dry</td></tr>
        <tr><td>Ventile</td><td>Long-staple cotton woven so tight it swells shut when wet</td><td class="hm">The name itself; it&rsquo;s a licensed brand</td><td>Price</td></tr>
      </tbody>
    </table>

    <h2 class="fb-h" id="take-cordura">Cordura: The Workhorse</h2>
    <p><strong>It started as a tire cord.</strong> DuPont registered the Cordura name in 1929 for a high-tenacity rayon used in WWII military tires, and moved it to nylon 6,6 in 1967. Koch Industries&rsquo; INVISTA has owned it since 2004.</p>
    <p><strong>Cordura doesn&rsquo;t weave the fabric.</strong> It makes the fiber and licenses the name to mills, and says there are &ldquo;more than 850 certified&rdquo; Cordura fabrics. So the name on a tag tells you less than you&rsquo;d think. The classic version is &ldquo;high-tenacity, air-jet textured nylon 6,6 filament yarns in weights ranging from 330D to 1,000D,&rdquo; and that D is the number that matters.</p>
    <p><strong>Denier is weight per length:</strong> grams per 9,000 meters of yarn. Higher means thicker and tougher. Here, Gramicci&rsquo;s wallet and pack are 210D, the Students headcovers and tote are 500D, and Dimple Divot&rsquo;s pouch is 1000D.</p>
    <blockquote class="fb-pq">A 210D Cordura wallet and a 1000D Cordura pouch have almost nothing in common but the label.</blockquote>
    <p><strong>Ripstop is a weave, not a fiber.</strong> Thicker yarns run through the cloth in a grid, usually 5 to 8 millimeters apart, so a tear stops at the next line. Sun Mountain&rsquo;s Eclipse and Briefing&rsquo;s DL covers use Cordura ripstop. Ballistic nylon is different again: a heavy basketweave DuPont made for WWII flak jackets.</p>

    <h2 class="fb-h" id="take-dyneema">Dyneema: The Fiber That Floats</h2>
    <p><strong>It&rsquo;s grocery-bag plastic, organized.</strong> Dyneema is ultra-high-molecular-weight polyethylene; the company says a typical chain holds about 100,000 carbon atoms, against about 10,000 in a plastic bag. Gel spinning dissolves the polymer and heats it in an extruder to untangle the chains, then draws the fiber so they line up. Albert Pennings found the strength in 1968, DSM&rsquo;s Smith and Lemstra patented the process in 1979, and commercial fiber came around 1990.</p>
    <p><strong>It floats, and it hates heat.</strong> Density is 0.97 g/cm&sup3;, just under water. Dyneema&rsquo;s own line is &ldquo;15 times stronger than steel, yet light enough to float on water,&rdquo; a company claim, not an independent test. It melts at 144&ndash;152&deg;C and is rated for use up to 70&deg;C, so keep it out of the dryer.</p>
    <p><strong>It shows up two ways.</strong> Woven, as in Sentinel&rsquo;s stretch Dyneema suit, or laminated into a composite once called Cuben Fiber, which sailed on America&sup3;, the 1992 America&rsquo;s Cup winner. Briefing&rsquo;s DL series layers it with ECCO leather, an idea ECCO Leather first showed in 2017 as Dyneema Bonded Leather: 0.5 mm split leather bonded to Dyneema, developed with designer Sruli Recht.</p>
    <blockquote class="fb-pq">&ldquo;If you threw it in the air it floated down, unlike leather which just thuds to the floor.&rdquo;<cite style="display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-top:10px;opacity:.75">Sruli Recht, on Dyneema Bonded Leather, Stylezeitgeist, 2017</cite></blockquote>
    <p>Avient bought the business from DSM in September 2022 for about $1.4 billion.</p>

    <h2 class="fb-h" id="take-natural">Organic Cotton, Ventile and the Natural Fibers</h2>
    <p><strong>&ldquo;Organic&rdquo; is about the farm, not the fiber.</strong> It&rsquo;s the same cotton plant, grown with no synthetic persistent pesticides or fertilizers and no genetically engineered seed. An organic tee won&rsquo;t necessarily feel different from a regular one; the case for it is how it&rsquo;s farmed and the paper trail that proves it. It&rsquo;s about 2.9% of the world&rsquo;s cotton (2023/24), and China grows roughly 46% of it. GOTS certifies the processing through the finished garment; OCS tracks the fiber.</p>
    <p><strong>Two numbers tell you the most.</strong> Staple length is how long each fiber is: upland cotton runs about 1 to 1-1/4 inches, extra-long-staple like Pima starts at 1-3/8, and longer fibers spin smoother, stronger yarn. And gsm, grams per square meter, tells you how heavy a piece will feel: a 170 gsm polo, a 305 gsm short and a 480 gsm fleece are three different garments.</p>
    <p><strong>Ventile is what long staple can do.</strong> Developed in 1943 for the Royal Air Force at the Shirley Institute in Manchester, it&rsquo;s extra-long-staple cotton &ldquo;woven to exceptionally high densities.&rdquo; Dry, it breathes; wet, the fibers swell and close the gaps, with no membrane or coating. Zurich&rsquo;s Stotz &amp; Co. has owned it since 2017, and most of it is now organic.</p>
    <blockquote class="fb-pq">&ldquo;A texture-forward golf sweater that adds warmth without plastic.&rdquo;<cite style="display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-top:10px;opacity:.75">Morning People Clothiers, on its organic cotton knit</cite></blockquote>
    <p><strong>The rest grow too.</strong> Linen (flax), hemp and ramie are bast fibers from plant stems. Cashmere legally averages 19 microns or finer, superfine merino is 18.5 or finer, and alpaca carries almost no lanolin.</p>
    <p class="fb-src">Sources: cordura.com; srulirecht.com (Stylezeitgeist interview, 2017); dyneema.com and the Dyneema SK75 technical sheet; Avient&rsquo;s 2022 10-K; Textile Exchange Materials Market Report 2025 via the Organic Trade Association; 16 CFR 300.19; Woolmark; Britannica; ventile.co.uk; textile-network.com. Products and prices read on each brand&rsquo;s own store, November 25, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>34</span></div>
      <div class="sidebar-detail"><span class="l">Fabrics</span><span>Cordura, Dyneema, organic cotton &amp; naturals, Ventile</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$32&ndash;$1,200</span></div>
      <div class="sidebar-detail"><span class="l">Lead pick</span><span>Sentinel &times; MacKenzie Basecamp Walker</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>November 25, 2026</span></div>
      <a href="#cordura" class="sidebar-cta">See the picks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#Cordura</span>
        <span class="hashtag">#Dyneema</span>
        <span class="hashtag">#OrganicCotton</span>
        <span class="hashtag">#Ventile</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

RELATED = [
 ("/drops/golf-fabrics-merino-ripstop-corduroy", "Ripstop vs Merino vs Corduroy", "Our October explainer on three more fabrics."),
 ("/drops/the-dyneema-edit", "The Dyneema Edit", "Everything we found in Dyneema this summer."),
 ("/drops/brand-to-know-sloat", "Brand to Know: SLOAT", "The brand behind the Ventile picks."),
 ("/drops/brand-to-know-sentinel-golf", "Brand to Know: Sentinel Golf", "The Minneapolis bag maker behind the Basecamp line."),
]


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    ids = [i for g in GROUPS for i in g[4]]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-25", "dateModified": "2026-11-25",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": [
            {"@type": "ListItem", "position": n, "name": H.unescape(re.sub(r"<[^>]+>", "", f"{P[i][0]} {P[i][1]}")), "url": P[i][3]} for n, i in enumerate(ids, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Favorite Fabrics of 2026", "item": URL}]},
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
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    ids = [i for g in GROUPS for i in g[4]]
    assert len(ids) == len(set(ids)) == 34, len(ids)
    for i in ids:
        assert i in P and i in FRAMES, i
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    head_rest = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\s*', "", head_rest, flags=re.S)
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    rel = "".join(f'<li style="padding:10px 0;border-bottom:.5px solid rgba(20,20,20,.2)"><a href="{u}">{t}</a> &mdash; {d_}</li>' for u, t, d_ in RELATED)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Favorite Fabrics of 2026</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 25, 2026</p><!--/TGI-BY-->
  <div class="drop-meta">
    <span>Sentinel, Briefing, Dimple Divot, Students, SLOAT, Criquet and more</span><span class="dot"></span>
    <span>34 picks &middot; 4 fabrics &middot; prices checked November 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Sentinel Basecamp Dyneema duffles stacked on a camp chair at the door of a tent" fetchpriority="high" /></div></div>
"""
    body += TAKE
    C, D, N = GROUPS
    body += band("cordura") + group(*C)
    body += pq("Since it started, the project has always been about bringing new ideas, materials, and people into the golf space, not only to make it more interesting but to make it more fun.", "John Mooty, Sentinel Golf founder")
    body += band("dyneema") + group(*D)
    body += pq("When exposed to moisture, the fibres naturally expand, reducing the spaces within the weave.", "Ventile")
    body += band("natural") + group(*N)
    body += f"""
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Read the Tag</h2>
    <p>The best thing a fabric name can do is tell you what you&rsquo;re buying, and these four mostly do. Look for the denier on Cordura, the gsm on cotton and the word &ldquo;composite&rdquo; on Dyneema, and you&rsquo;ll know more than most of the copy on the product page. If we got a number wrong, <a href="/work-with-us">tell us</a>.</p>
    <div class="drop-tag grass" style="margin-top:34px">More Like This</div>
    <ul style="list-style:none;padding:0;margin:10px 0 0;font-size:17px">{rel}</ul>
  </div>
</section>
"""
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Manors"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if fin.count('class="product-card"') != 34: bad.append("card count")
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html · 34 picks")


if __name__ == "__main__":
    main("--apply" in sys.argv)
