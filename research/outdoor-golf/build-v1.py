#!/usr/bin/env python3
"""build-outdoor-golf.py — Outdoor brands that pair with golf. 22 October 2026. Cloned from build-dogs-golf.py.
Lenny: "Outdoor brands that pair perfectly with golf - Arc'teryx, Salomon, Gramicci, Purple Mountain Observatory ... I like my golf gear
durable, stain resistant, weather resistant and I wanna know it will last more than just one season. If it can survive the mountain, it
will be fine for my local muni especially in January." Pull 6-8 per brand + lookbook bands + a 5th brand (Goldwin; and wander has no US store).
"let's build the post" -> the starred 7 per brand from outdoor-golf-options.html.
FACTS + PRICES: research/outdoor-golf/<brand>.json (each brand's own US store, USD, 22 Oct 2026; sources inside).
Images: research/outdoor-golf/frame.py (brands' own product + lookbook photos). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Outdoor Brands That Pair With Golf: 35 Picks for Winter"
DESC = ("Arc'teryx, Salomon, Gramicci, Purple Mountain Observatory and Goldwin: 35 durable, "
        "weather-ready pieces that work on a golf course in January.")
H1 = "If It Can Survive the Mountain, It Can Survive the Muni"
BC = "Outdoor Brands for Golf"
SLUG = "outdoor-brands-for-golf"
IMG = "/images/outdoor-golf"
SHOP = ""
A = "Arc&rsquo;teryx"
P = {
 # Arc'teryx
 "o1": (A, "Gamma Pant", "$200", "https://arcteryx.com/us/en/shop/mens/gamma-pant-0481",
   "Fortius 2.0 softshell, 88% nylon and 12% elastane, with a gusseted crotch. The full turn and the crouch to read a putt are no fight, it blocks a January wind and sheds dew off a wet fairway, and the regular fit reads as a trouser."),
 "o2": (A, "Atom Vest", "$200", "https://arcteryx.com/us/en/shop/mens/atom-vest-9559",
   "Coreloft Stretch synthetic insulation with stretch fleece side panels, 195 g. Warmth at the core, nothing on the arms, and the synthetic fill keeps working if the drizzle starts on the back nine."),
 "o3": (A, "Delta 1/2 Zip Neck", "$180", "https://arcteryx.com/us/en/shop/mens/delta-1-2-zip-neck-0550",
   "A thin polyester fleece with a smooth, hard-wearing face and articulated patterning. It looks right on a first tee, and the deep zip dumps heat as the morning warms up."),
 "o4": (A, "Kyanite Jacket", "$180", "https://arcteryx.com/us/en/shop/mens/kyanite-jacket-8447",
   "Polartec Power Stretch Pro: four-way stretch with a tough nylon face. It swings like a sweater and shrugs off bag straps and the odd pine branch."),
 "o5": (A, "Squamish Hoody", "$200", "https://arcteryx.com/us/en/shop/mens/squamish-hoody-0276",
   "A 150 g stretch nylon windshell with a DWR finish that packs into its own chest pocket. Pull it over a polo when the north wind picks up; the swing feels the same."),
 "o6": (A, "Kopec 2 Low GTX Shoe", "$190", "https://arcteryx.com/us/en/shop/mens/kopec-2-low-gtx-shoe-0831",
   "A light, low Gore-Tex hiker on a Vibram Megagrip sole with 5 mm lugs. Dry socks on soaked morning grass; check your course&rsquo;s shoe rules, because lugs are not a golf sole."),
 "o7": (A, "Small Bird Cap", "$50", "https://arcteryx.com/us/en/shop/small-bird-cap-9782",
   "Four-way stretch polyester with a DWR finish and a mesh sweatband, 59 g. A small bird logo and nothing loud. Black only."),
 # Salomon
 "o8": ("Salomon", "XT-6 GORE-TEX", "$200", "https://www.salomon.com/en-us/product/xt-6-gore-tex-lg9333/L49306800",
   "The trail racer that became a street shoe, here with a Gore-Tex membrane and a Mud Contagrip outsole built for soft ground, which is exactly what a January fairway is at 8 a.m."),
 "o9": ("Salomon", "XA PRO 3D V9 GORE-TEX", "$170", "https://www.salomon.com/en-us/product/xa-pro-3d-v9-gore-tex-li3151/L49199100",
   "The most stable shoe here: a 3D chassis, a protective toecap and 3.5 mm lugs. It keeps you planted on sidehill lies and shrugs off cart-path scuffs. A few sizes are gone."),
 "o10": ("Salomon", "XT-WHISPER GORE-TEX", "$165", "https://www.salomon.com/en-us/product/xt-whisper-gore-tex-li9305/L45397400",
   "The lightest Gore-Tex shoe in the set at 290 g, with a ripstop upper and a lower, sneaker-like profile. For walkers who want dry feet without a hiker&rsquo;s bulk."),
 "o11": ("Salomon", "OUTWIND Jacket", "$90", "https://www.salomon.com/en-us/product/outwind-lc14428/LC2761400",
   "A light, packable windproof shell in a regular fit. It lives in a bag pocket and comes out on the exposed holes."),
 "o12": ("Salomon", "ESSENTIAL LIGHTWARM Half Zip", "$70", "https://www.salomon.com/en-us/product/essential-lightwarm-lc13574/LC2767400",
   "Grid fleece, 93% polyester and 7% elastane, in a slim fit. The classic quarter-zip shape with enough stretch to swing under a shell, and the cheapest top here."),
 "o13": ("Salomon", "THERNOVA Half Zip", "$130", "https://www.salomon.com/en-us/product/thernova-lc14960/LC2967500",
   "PrimaLoft fleece in a relaxed fit, roomy enough to layer and to swing in. The warm one for a frosty tee time; Coffee Bean is the course color. 2XL is sold out."),
 "o14": ("Salomon", "BONATTI PRO Waterproof Cap", "$50", "https://www.salomon.com/en-us/product/bonatti-pro-wp-lc14552/LC2930700",
   "A waterproof, packable five-panel at 60 g, for drizzle days. Burnt Umber is in stock in L/XL only."),
 # Gramicci
 "o15": ("Gramicci", "WR Anorak", "$190", "https://gramicci.com/products/wr-anorak",
   "Water-repellent polyester-cotton with a front zip pouch, elastic cuffs and a drawcord waist. A soft hand that won&rsquo;t rustle at address, and the pouch holds balls, tees and a glove."),
 "o16": ("Gramicci", "Mini Check Nylon Jacket", "$150", "https://gramicci.com/products/mini-check-nylon-jacket",
   "A dense nylon-cotton blend with water-repellent and UV finishes, in a short blouson cut that stays clear of your hands at the bottom of the swing."),
 "o17": ("Gramicci", "Thermal Fleece Pullover", "$130", "https://gramicci.com/products/thermal-fleece-pullover",
   "Recycled polyester thermal fleece in a quarter-zip with a drawcord hem. Low-profile, so it doesn&rsquo;t bunch at the top of the backswing."),
 "o18": ("Gramicci", "Thermal Fleece Vest", "$140", "https://gramicci.com/products/thermal-fleece-vest",
   "A slim fleece vest with nylon on the collar and shoulders, so a carry-bag strap won&rsquo;t wear it down. Bark Camo or black."),
 "o19": ("Gramicci", "Nylon Gramicci Pant", "$110", "https://gramicci.com/products/nylon-gramicci-pant",
   "The G-Pant idea in recycled nylon, described as durable and water-repellent: dew beads off and it dries fast. A relaxed, slightly tapered leg on an elastic waist."),
 "o20": ("Gramicci", "Mini Check Nylon Pant", "$130", "https://gramicci.com/products/mini-check-nylon-pant",
   "Water-resistant nylon-cotton with a shock-cord hem cinch to keep cuffs off wet grass, and velcro back pockets so the yardage book stays put."),
 "o21": ("Gramicci", "Mini Check Nylon Cap", "$55", "https://gramicci.com/products/mini-check-nylon-cap",
   "The same water- and UV-resistant check fabric in a short-billed cap that keeps the brim out of your sightline at address."),
 # Purple Mountain Observatory
 "o22": ("Purple Mountain Observatory", "Mogul Pant", "$215", "https://purplemountainobservatory.co.uk/products/mogul-pant",
   "A hard-wearing cotton-nylon blend in a wider, movement-first fit with plenty of pockets. Room through the leg for a full turn, and it shrugs off a muddy knee."),
 "o23": ("Purple Mountain Observatory", "City Pant", "$305", "https://purplemountainobservatory.co.uk/products/city-pant",
   "Japanese double-weave with stretch, water resistance and UV protection, plus zip pockets. The cleanest-looking pant here, tailored enough for the clubhouse."),
 "o24": ("Purple Mountain Observatory", "Deluge Pant", "$178", "https://purplemountainobservatory.co.uk/products/deluge-pant",
   "A real waterproof over-trouser with welded, taped seams, gusseted zip openings and front pockets you can reach without unzipping a layer."),
 "o25": ("Purple Mountain Observatory", "Stinger Jacket", "$305", "https://purplemountainobservatory.co.uk/products/stinger-jacket",
   "A 165 g two-layer ripstop shell with taped seams and a pack-away bag. The lightest shell in the post, so it swings like a windshirt but keeps out the rain."),
 "o26": ("Purple Mountain Observatory", "PrimaLoft Ursa Pullover", "$170", "https://purplemountainobservatory.co.uk/products/primaloft%C2%AE-ursa-pullover",
   "PrimaLoft Active Evolve for warmth while moving, with articulated seams and thumb loops. Warm on the first tee, not overheating by the turn."),
 "o27": ("Purple Mountain Observatory", "Polartec Alpha Direct 90 Pullover", "$170", "https://purplemountainobservatory.co.uk/products/polartec%C2%AE-alpha%E2%84%A2-direct-90-pullover",
   "Insulation built for stop-and-go, which is golf exactly: warm while you wait on the group ahead, venting heat on the walk. Thin enough to go under a shell."),
 "o28": ("Purple Mountain Observatory", "Tech Ripstop Air Cap", "$77", "https://purplemountainobservatory.co.uk/products/tech-ripstop-air-cap",
   "Light ripstop with ventilated side panels and a quick-release puller at the back. Dries fast after a drizzle."),
 # Goldwin
 "o29": ("Goldwin", "Floating Wind Shell Half Zip Pullover", "$189", "https://us.goldwin.global/products/gm15102",
   "Light, water-repellent polyester that balances wind resistance and breathability, cut slightly wider through the body and sleeves. It stuffs into its own sack once the wind drops."),
 "o30": ("Goldwin", "PERTEX UNLIMITED 2L Jacket", "$385", "https://us.goldwin.global/products/gl25142",
   "Water-resistant, windproof and breathable, with a loose cut for layering and a two-way zip. It looks like a normal jacket in the clubhouse and handles a January drizzle."),
 "o31": ("Goldwin", "Kel Mid Jacket", "$290", "https://us.goldwin.global/products/gm36335",
   "Polartec Alpha Direct with flatlock seams and thumbhole cuffs, made to be worn on the move. It breathes on the walk between shots; add a wind shell and a cold dawn round is covered."),
 "o32": ("Goldwin", "Mesh Pile Crew", "$175", "https://us.goldwin.global/products/gm35301",
   "A seamless WHOLEGARMENT pile knit, warm and quick-drying. A technical sweater that looks like a sweater, with nothing binding across the shoulders."),
 "o33": ("Goldwin", "Nimble Tech Tapered Pants", "$270", "https://us.goldwin.global/products/gm75155",
   "Windproof, water-repellent double-weave stretch with a large inseam gusset and a slacks-like taper. A zip pocket for the car key. Our pick of the pants for golf."),
 "o34": ("Goldwin", "One Tuck Light Stretch Shorts", "$147", "https://us.goldwin.global/products/gl76181",
   "High-stretch, wrinkle-resistant SOLOTEX with light water repellency and belt loops. For the warm January afternoons Austin throws in."),
 "o35": ("Goldwin", "All Direction Light Cap", "$90", "https://us.goldwin.global/products/gm95192",
   "Thin double-weave stretch that breathes and releases sweat on the inside, water-repellent for light rain. Black only right now."),
}
SECTIONS = [
 ("Arc&rsquo;teryx", "arcteryx", ["o1","o2","o3","o4","o5","o6","o7"],
  "<strong>Pants, layers, a shell, a shoe &middot; $50&ndash;$200</strong>The Gamma Pant and a Kyanite are the place to start."),
 ("Salomon", "salomon", ["o8","o9","o10","o11","o12","o13","o14"],
  "<strong>Three Gore-Tex shoes and the layers &middot; $50&ndash;$200</strong>Dry feet on wet grass is the whole case for Salomon at the muni."),
 ("Gramicci", "gramicci", ["o15","o16","o17","o18","o19","o20","o21"],
  "<strong>Nylon pants, fleece and shells &middot; $55&ndash;$190</strong>Water-repellent versions of the climbing pant, plus the layers to go with them."),
 ("Purple Mountain Observatory", "pmo", ["o22","o23","o24","o25","o26","o27","o28"],
  "<strong>Pants, a shell and active fleece &middot; $77&ndash;$305</strong>Sold in US dollars from London; ships worldwide, and US orders ship duties unpaid."),
 ("Goldwin", "goldwin", ["o29","o30","o31","o32","o33","o34","o35"],
  "<strong>Shells, layers, pants and a short &middot; $90&ndash;$385</strong>The one brand here that has made golf clothes, too."),
]
N = 35
PQ = {
 "arcteryx": ("Every piece we make serves a purpose and solves a problem for mountain athletes, delivering functionality, simplicity, and durability in a timeless design.", "Arc&rsquo;teryx"),
 "salomon": ("What fascinates me the most is what I&rsquo;m going to invent tomorrow.", "Georges Salomon"),
 "gramicci": ("For me, building clothing is like architecture and engineering.", "Mike Graham, Gramicci founder"),
 "pmo": ("There&rsquo;s no such thing as bad weather, just bad clothing.", "Matt Braun&rsquo;s father, as told to Basement Approved"),
 "goldwin": ("The resulting apparel can withstand the toughest outdoor conditions while still looking great in urban environments.", "Goldwin"),
}
BANDS = {
 "arcteryx": ("Arc&rsquo;teryx &middot; North Vancouver, 1989. ",
   "Started by Vancouver climbers in a basement making harnesses and packs, named for the Archaeopteryx fossil, and still designing and testing in the Coast Mountains of British Columbia. Gore-Tex apparel came in 1996; its ReBIRD program repairs and resells used gear.",
   [("band-arcteryx-1","Designers fitting a red shell on a model inside the Arc&rsquo;teryx design centre","Inside the design centre &middot; Arc&rsquo;teryx"),
    ("band-arcteryx-2","An ice climber on frozen falls at Helmcken Falls, British Columbia","Helmcken Falls, B.C. &middot; Arc&rsquo;teryx"),
    ("band-arcteryx-3","The view out of a tent door at sunset over snowy peaks","Footwear campaign &middot; Arc&rsquo;teryx")]),
 "salomon": ("Salomon &middot; Annecy, 1947. ",
   "Born in the French Alps making ski edges and bindings, then ski boots, then trail shoes: the XA Pro in 2002 and the XT-6 in 2013, a racing shoe that later crossed over to the street. Owned by Amer Sports, which also owns Arc&rsquo;teryx.",
   [("band-salomon-1","Two runners climbing a grey rock gully, shot from above","XA Pro &middot; Salomon"),
    ("band-salomon-2","XT-6 shoes worn with wide olive trousers on concrete steps","XT-6 &middot; Salomon"),
    ("band-salomon-3","Two hikers in shells on a dark ridge under heavy cloud","Hiking &middot; Salomon")]),
 "gramicci": ("Gramicci &middot; Ventura, California, 1982. ",
   "Founded in a garage by Mike Graham, one of Yosemite&rsquo;s Stonemasters, around a climbing short with a diamond gusset borrowed from kung-fu trousers and a built-in webbing belt. The G-Pant followed; the brand now calls Japan home.",
   [("band-gramicci-1","A magnifying glass held over the Gramicci label on a snowy mountain slope","FW26 &middot; Gramicci"),
    ("band-gramicci-2","El Capitan above the trees in Yosemite","Yosemite &middot; Gramicci Journal"),
    ("band-gramicci-3","Someone bouldering an overhanging mossy rock in orange pants","FW26 Journal &middot; Gramicci")]),
 "pmo": ("Purple Mountain Observatory &middot; London, 2021. ",
   "Founded by Matt Braun and Georgia Smith and named for Purple Mountain above Nanjing, near where the clothes are made. Unisex outerwear for trail and town, built on PrimaLoft, Polartec and other named technical fabrics.",
   [("band-purple-mountain-observatory-1","Two hikers roped up on a snowy alpine ridge","AW26 &middot; Purple Mountain Observatory"),
    ("band-purple-mountain-observatory-2","A man in a grey Purple Mountain Observatory shell on a park bench in London","Stories &middot; Purple Mountain Observatory"),
    ("band-purple-mountain-observatory-3","A hiker in a lime fleece on a mountain at dusk","AW26 &middot; Purple Mountain Observatory")]),
 "goldwin": ("Goldwin &middot; Toyama, Japan, 1950. ",
   "A ski-wear maker that also runs The North Face in Japan, and the bridge between the two worlds: Goldwin has made golf clothes since a U.S. Open Golf line in 1981, opened Goldwin Golf Club USA in California in 1994 and was an official supplier to the U.S. Open from 1997.",
   [("band-goldwin-1","A model in a stone-colored down jacket and pleated trousers","FW26 &middot; Goldwin"),
    ("band-goldwin-2","A model in a hooded down jacket walking along a wall","FW26 &middot; Goldwin"),
    ("band-goldwin-3","A model in a hooded shell and track pants walking past a window","FW26 &middot; Goldwin")]),
}
KIT_CSS = """<style>
.og-kit{max-width:1000px;margin:8px auto 0;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;text-align:left}
.og-kit div{border-top:1px solid #141414;padding-top:12px}
.og-kit b{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
.og-kit p{font-size:14px;line-height:1.6;margin:0}
@media(max-width:820px){.og-kit{grid-template-columns:1fr 1fr}}@media(max-width:480px){.og-kit{grid-template-columns:1fr}}
</style>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>We like our golf gear the way mountain people like theirs: durable, stain resistant, weather resistant, and still going next winter, not just this one. The thinking is simple. If it can survive the mountain, it will be fine at the local muni, especially in January.</p>
    <p><strong>January is when it matters.</strong> An Austin winter round is a cold, windy first tee, fairways soaked with dew, maybe a drizzle, and an afternoon that can turn warm by the back nine. That is a layering problem, and outdoor brands have been solving layering problems for a long time. Golf brands mostly make polos.</p>
    <p><strong>What we looked for.</strong> Stretch or gussets so the turn is free; wind blocking and water repellency that stays quiet at address; fabric that shrugs off grass stains and mud; pockets that zip; and shoes that keep socks dry on wet grass. We skipped harnesses, ski kit and heavy down, and anything that looks like you got lost on the way to the summit.</p>
    <p><strong>Five brands.</strong> Arc&rsquo;teryx, started by Vancouver climbers in 1989. Salomon, from the French Alps since 1947. Gramicci, a Yosemite climber&rsquo;s pant brand from 1982. Purple Mountain Observatory, a London label from 2021. And Goldwin, a Japanese ski maker from 1950 that has made golf clothes since 1981, which makes it the bridge between the two worlds.</p>
    <p>A note on shoes: trail and hiking soles grip wet grass well, but they aren&rsquo;t golf soles. Check your course&rsquo;s footwear rules before you walk one onto a green.</p>
    <p>Below: seven pieces from each brand, 35 in all, from a $50 cap to a $385 rain jacket, and one January kit built from them. Everything was in stock on each brand&rsquo;s US store when we checked on October 22, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Short Version</div>
      <div class="sidebar-detail"><span class="l">The thesis</span><span>Survive the mountain</span></div>
      <div class="sidebar-detail"><span class="l">The test</span><span>January at the muni</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Five</span></div>
      <div class="sidebar-detail"><span class="l">Gear</span><span>35 picks, $50&ndash;$385</span></div>
      <div class="hashtags">
        <span class="hashtag">#Gorpcore</span>
        <span class="hashtag">#WinterGolf</span>
        <span class="hashtag">#MuniGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
KIT = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">One January Kit</div>
  <h2 class="products-hdr" id="kit">A Cold Muni Morning, Head to Toe</h2>
  <p class="cat-kicker">One way to put it together from the picks above, for a 7:30 tee time with wind. Swap any piece for its neighbor.</p>
  <div class="og-kit">
    <div><b>Feet</b><p>Salomon XA PRO 3D V9 GORE-TEX for dry socks on wet fairways ($170).</p></div>
    <div><b>Legs</b><p>Goldwin Nimble Tech Tapered Pants: windproof, a big gusset, slacks look ($270).</p></div>
    <div><b>Layers</b><p>Arc&rsquo;teryx Delta 1/2 Zip under a Gramicci Thermal Fleece Vest ($180 + $140).</p></div>
    <div><b>Shell &amp; cap</b><p>Arc&rsquo;teryx Squamish Hoody in the bag, Salomon Bonatti Pro cap on the head ($200 + $50).</p></div>
  </div>
</section>
"""
FAQ = [
 ("Can you wear hiking or trail shoes to play golf?", "Many public courses allow soft-soled athletic shoes, but rules vary and some ask for golf-specific soles. Low trail shoes with Gore-Tex keep your feet dry on wet grass; check the course's footwear policy before you play."),
 ("What should I wear to play golf in cold weather?", "Layers: a thin quarter-zip or fleece, an insulated vest that leaves the arms free, a packable wind or rain shell, wind-blocking pants and waterproof shoes. Shed layers as the day warms up."),
 ("Is Arc'teryx good for golf?", "Several Arc'teryx pieces work well on a course, especially the stretch Gamma Pant, the Atom Vest, Kyanite and Delta fleeces and the packable Squamish windshell. They are built for movement and weather."),
 ("Does Goldwin make golf clothes?", "Yes. Goldwin, the Japanese outdoor and ski-wear company, has made golf apparel since a U.S. Open Golf line in 1981 and was an official supplier to the U.S. Open from 1997. Its current US line is outdoor and lifestyle clothing."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
FRN = {k: [f"{IMG}/p-{k[1:]}.jpg"] for k in P}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-22", "dateModified": "2026-10-22",
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Grassy Issue &middot; Outdoor brands for golf</span><span class="dot"></span>
    <span>35 picks &middot; prices checked October 22, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A hiker in a Purple Mountain Observatory fleece standing above a sea of cloud, from the brand&rsquo;s AW26 campaign" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += KIT
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + KIT_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
