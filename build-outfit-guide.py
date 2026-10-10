#!/usr/bin/env python3
"""build-outfit-guide.py — How to Build a Golf Outfit: seven looks from Top 25 brands. 10 October 2026.
Lenny: "a post similar to curating-your-golf-bag-setup but for building an outfit, think of different combos like Pants with a
Tee, casual shorts with a jersey polo, color combos like pastels & earth tones. 5-7 different outfit choices. I want Manors,
Odd Rituals' pants featured and other brands from our top 25 list." -> "let's have a few options in each category".
Cloned in structure from build-bag-setup.py (palette swatches, two big photos, prose, then the pieces), with 2-3 options per slot.
FACTS/PRICES: each brand's own store, read October 10, 2026 (research/outfits/spec.json, prices.json). Store currency first;
Sounder and Walker figures in brackets are the stores' own US prices; other conversions are approximate.
Odd Ritual's Pleated Daily Trouser: khaki sold out, black in M and XL only, marked R990 from R1,300.
PHOTOS: each brand's own product photography (research/outfits/frames.json). Hero: Sounder's own coastal-course shoot
(Clean Lie Polo product page), per Lenny: "let's get a better hero shot, any good wide shots of golfers on the course?"
"""
import html as H
import json
import pathlib
import re
import sys
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "how-to-build-a-golf-outfit"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/outfits"
SPEC = json.loads((ROOT / "research/outfits/spec.json").read_text())
FR = json.loads((ROOT / "research/outfits/frames.json").read_text())
DATE = "2026-10-10"

TITLE = "How to Build a Golf Outfit: 7 Looks, From Pants and a Tee to Pastels"
DESC = ("How to put together a golf outfit, with seven complete looks from independent brands: pants and a tee, shorts and a "
        "jersey polo, pastels, earth tones and more, with two or three options for every piece.")
H1 = "How to Build a Golf Outfit: 7 Looks, From Pants and a Tee to Pastels"

BRAND = {"manors": "Manors", "odd-ritual": "Odd Ritual", "students": "Students Golf", "birds-of-condor": "Birds of Condor",
         "devereux": "Devereux", "walker": "Walker Golf Things", "radry": "Radry", "kingfisher": "Kingfisher Golf",
         "sounder": "Sounder", "left-of-field": "Left of Field", "fella": "Fella Golf", "casualist": "Casualist"}
SHOP = {"left-of-field": "https://lofgolf.com/en-us"}

def key(b, h, c):
    k = f"{b}--{re.sub(r'[^a-z0-9]+','-',h.lower()).strip('-')[:40]}"
    return k + (f"--{re.sub(r'[^a-z0-9]+','-',c.lower())}" if c else "")

# key -> (name, price, copy)
P = {
 # 1 Pants & a Tee
 "odd-ritual--pleated-daily-trouser-black": ("Pleated Daily Trouser, Black", "R990 (~$55)",
   "The pants this look is built around. A single-pleat trouser from Cape Town, cut wide and cropped just above the shoe, so it sits right over a sneaker or a golf shoe. The khaki is gone and the black is down to M and XL, marked down from R1,300."),
 "manors--club-trousers--black": ("Club Pant, Black", "$159",
   "Manors&rsquo; straight-leg club pant in black: a cleaner, slimmer take than the pleat if you want the tee to do the talking."),
 "students--curriculum-baggy-twill-pants-1--black": ("Curriculum Baggy Twill Pants, Black", "$135",
   "The skate-shop option. A baggy cotton twill pant that drapes over the shoe, and the most relaxed fit of the three."),
 "casualist--heavy-tee-agni": ("No Idea Heavy Tee, Organic Cotton", "&pound;95 (~$128)",
   "A heavyweight organic-cotton tee with a self-deprecating orange back print: all the gear, no idea. Heavy enough to hold its shape over a swing."),
 "fella--fella-logo-tee-white": ("Logo Tee, White", "&euro;55 (~$64)",
   "A boxy white tee with a small Fella script. The plainest tee here, which is the point."),
 "odd-ritual--minimal-wordmark-t-shirt-duck-grey": ("Minimal Wordmark Tee, Duck Grey", "R700 (~$39)",
   "Odd Ritual&rsquo;s own tee in a soft grey-blue, so the pants and the shirt come from the same Cape Town label."),
 "fella--gavan-oversized-sweater-heather-grey": ("Gavan Oversized Sweater, Heather Grey", "&euro;135 (~$157)",
   "An oversized heather-grey crew with a chenille script. Throw it over the tee on a cool first tee and tie it round your waist by the turn."),
 "manors--crewneck-polartec-fleece--black": ("Crewneck Polartec Fleece, Black", "$173",
   "The technical layer: a black Polartec crewneck that keeps the outfit black, white and gray."),
 # 2 Shorts & a Jersey Polo
 "sounder--monterey-stripe-polo-in-indigo-and-slate": ("Monterey Stripe Polo, Indigo / Slate", "&pound;45 ($61)",
   "A soft jersey polo in olive with blue stripes and a contrast collar. The stripe does the work, so keep the shorts plain."),
 "kingfisher--new-blue-polo": ("Vega Polo", "$65",
   "A light-blue jersey polo from Dallas with a fine texture. The easiest shirt here to wear with any short."),
 "walker--members-polo-3": ("Members Polo, Maroon", "A$120 ($100)",
   "A deep maroon polo with a tipped collar from the Gold Coast. Maroon with stone shorts is the most grown-up version of this look."),
 "manors--stableford-shorts--dune": ("Stableford Short, Dune", "$126",
   "A stone-colored golf short with a clean front and an above-the-knee cut. Dune goes with every polo in this section."),
 "students--calculus-standard-pleated-shorts-4--sand": ("Calculus Pleated Shorts, Sand", "$108",
   "A pleated sand short with a little more room through the leg, for a looser, more 1990s shape."),
 # 3 Pastels
 "sounder--capri-collar-polo-mint-natural": ("Capri Collar Polo, Mint / Natural", "&pound;85 ($115)",
   "A natural-colored knit polo with a mint open collar. A quiet way into pastels: the color is only at the neck."),
 "manors--tour-shirt--powder": ("Tour Shirt, Powder", "$159",
   "A powder-blue half-zip tour shirt. It works as the polo on a warm day and as a layer when it isn&rsquo;t."),
 "sounder--play-well-polo-in-jade": ("Play Well Polo, Jade", "&pound;40 ($55)",
   "A jade jersey polo, the boldest of the three. Pair it with pebble shorts and nothing else colorful."),
 "manors--greenskeeper-chino-short--pebble": ("Lightweight Pleated Short, Pebble", "$146",
   "A pleated short in a pale stone that lets any pastel sit on top of it. This is the base of the whole look."),
 "walker--pitch-cargo-short-1": ("Pitch Cargo Short, Sand", "A$120 ($100)",
   "A sand cargo short if you want pockets and a more relaxed shape."),
 "radry--contrast-quarter-zip-butter": ("Contrast Quarter Zip, Butter", "$120",
   "A butter-yellow quarter-zip with mustard pockets. The pastel layer for a cool morning, and the piece people will ask about."),
 "casualist--appropriate-dress-code-mockneck-tee-dust": ("Dress Code Mockneck Tee, Dusty Blue", "&pound;115 (~$155)",
   "A dusty-blue mock neck that replaces the polo entirely, for anyone who has had enough of collars."),
 # 4 Earth Tones
 "devereux--el-classico-pant-brown": ("El Classico Pant, Brown", "$88",
   "A chocolate-brown golf pant from Scottsdale with a leather patch at the back. Brown pants are the quickest way into earth tones."),
 "manors--club-trousers--earth": ("Club Pant, Earth", "$159",
   "The same Manors club pant as look one, in a muted earth brown."),
 "casualist--weekend-pique-polo-mocha": ("Weekend Pique Polo, Mocha", "&pound;129 (~$174)",
   "A mocha pique polo with a cream collar. Tonal with the pants, so the cream does the contrast."),
 "devereux--duke-polo-brindle": ("Duke Polo, Brindle", "$74",
   "A brown polo with an all-over medallion print and a dark collar. The pattern makes it the loudest earth tone here."),
 "fella--jake-toffee-brown-intarsia-knit-polo": ("Jake Intarsia Knit Polo, Toffee", "&euro;135 (~$157)",
   "A striped toffee-and-cream knit polo with a 1970s feel. The best shirt in this section for the walk to the bar afterward."),
 "manors--heritage-primaloft-cardigan--ivory": ("Heritage Primaloft Cardigan, Ivory", "$212",
   "An ivory cardigan with Primaloft insulation inside. It lightens the browns and makes the whole outfit look considered."),
 "odd-ritual--caddie-jacket-chocolate": ("Caddie Jacket, Chocolate", "R1,200 (~$66)",
   "A chocolate work jacket with an Odd Ritual Golf Club print on the back. Brown on brown, and it works."),
 # 5 Fall Knit & Pleats
 "manors--greenskeeper-chino-trousers--pebble": ("Lightweight Pleated Trouser, Pebble", "$173",
   "A pleated trouser in a pale stone, the base for a knit. Light pants under a darker knit is the fall version of the classic."),
 "left-of-field--pleated-lite-pant-beige": ("Pleated Lite Pant, Beige", "$150",
   "A lighter pleated pant from Sydney in beige, for warmer fall days."),
 "casualist--pleated-trousers": ("Pleated Golf Trousers, Organic Cotton", "&pound;199 (~$269)",
   "Organic-cotton pleated trousers from London with a wider leg. The most tailored of the three."),
 "students--riverview-knit-ls-polo-sweater--moss": ("Riverview Knit Polo Sweater, Moss", "$158",
   "A cable-knit polo sweater in moss green with an open collar. This is the piece that makes the look."),
 "students--knight-knitted-l-s-polo-sweater-1--coffee": ("Knight Knitted Polo Sweater, Coffee", "$130",
   "A dark coffee knit polo with a textured weave, if you want the earthier option."),
 "manors--reversible-polartec-fleece-vest--dark-olive": ("Reversible Polartec Fleece Vest, Dark Olive", "$199",
   "A dark-olive Polartec vest that reverses to a lighter side. A vest keeps your arms free for the swing."),
 "casualist--grazer-cardigan-vest-grey": ("Grazer Cardigan Vest, Grey", "&pound;185 (~$250)",
   "A gray knit cardigan vest, the softer and more vintage take on the layer."),
 # 6 Navy & Stripes
 "birds-of-condor--blue-navy-ranger-golf-chino-straight-leg": ("Ranger Pant, Navy", "$100",
   "A straight-leg navy chino from Byron Bay. Navy pants are the base that makes every stripe look good."),
 "manors--recycled-greenskeeper-trouser--navy": ("Recycled Greenskeeper Trouser, Navy", "$173",
   "Manors&rsquo; recycled-fabric trouser in navy, a little more technical and a little more relaxed."),
 "left-of-field--mornington-polo-blue-white-stripe": ("Mornington Polo, Blue / White Stripe", "$110",
   "A blue-and-white striped polo with a white collar. The classic stripe, and the easiest win in this guide."),
 "sounder--monterey-stripe-polo-in-deep-red-and-dee": ("Monterey Stripe Polo, Deep Red / Deep Navy", "&pound;40 ($55)",
   "Red and navy stripes with a navy collar, for a more collegiate, warmer version of the look."),
 "manors--goat-pique-polo-stripe--navy": ("GOAT Pique Polo, Navy Stripe", "$113",
   "A navy-striped pique polo from Manors, the tightest stripe of the three."),
 "fella--boris-quarter-zip-sweater-navy": ("Boris Quarter-Zip Sweater, Navy", "&euro;170 (~$198)",
   "A cream knit quarter-zip with a single navy band across the chest. It ties the navy pants and the stripe together."),
 "sounder--pac-mach-jacket-deep-navy-ripstop": ("Pac Mach Jacket, Deep Navy Ripstop", "&pound;145 ($196)",
   "A packable navy ripstop jacket for wind and drizzle that disappears into the bag."),
 # 7 One Loud Piece
 "fella--bruno-camp-shirt-tropical-golf-cart": ("Bruno Camp Shirt, Tropical Golf Cart", "&euro;135 (~$157)",
   "A camp-collar shirt printed with palm trees and golf carts. Wear it untucked and let it be the only thing anyone notices."),
 "walker--whitsundays-ss-shirt": ("Whitsundays Shirt, Sunrise", "A$140 ($120)",
   "A cream camp shirt with a sunrise tropical print from the Gold Coast. Softer than the Fella, just as loud."),
 "birds-of-condor--lawn-pawn-blue-green-plaid-golf-polo-shi": ("Lawn Pawn Polo, Blue / Green Plaid", "$80",
   "A blue-and-green plaid polo, the loud option for courses that want a collar."),
 "students--stockton-work-pants--dark-grey": ("Stockton Work Pants, Dark Grey", "$138",
   "A dark-grey work pant that sits back and lets the shirt do everything."),
}

LOOKS = [
 ("Pants &amp; a Tee", "pants-and-a-tee", ["#141414", "#f4f2ec", "#a8a8a6"], ["Black", "White", "Heather"],
  "The modern muni uniform: a good pair of pants, a heavy tee and one layer.",
  ["This is the outfit that changed what golf looks like on public courses. Wide or pleated pants, a heavyweight tee and a sneaker-style shoe. It only works if the pieces are good, so spend on the pants and keep the tee plain or nearly plain.",
   "Keep the palette to black, white and gray and you can swap any piece for any other. The pants should break just over the shoe, and the tee should be heavy enough to hold its shape over a swing. Check the dress code first; most munis are fine with it, and most private clubs are not.",
   "<strong>Our pick</strong> is the Odd Ritual Pleated Daily Trouser in black. One pleat, a wide, cropped leg, and it makes any tee look intentional. It&rsquo;s down to two sizes, so buy it now or go with the Manors Club Pant."],
  ["odd-ritual--pleated-daily-trouser-black--1", "fella--fella-logo-tee-white--4"]),
 ("Shorts &amp; a Jersey Polo", "shorts-and-a-jersey-polo", ["#6b6b4e", "#d6ccb6", "#8fb7d9"], ["Stripe", "Stone", "Sky"],
  "The summer default: a soft jersey polo, stone shorts, done.",
  ["Jersey polos are softer and drapier than pique, which makes them look less like a uniform. Put one over stone or sand shorts and you have the easiest outfit in golf, the one you can wear from the first tee to a patio.",
   "The rule is one interesting thing. If the polo has stripes or a strong color, keep the shorts plain. Shorts should end just above the knee. Add white socks and a white shoe and stop there.",
   "<strong>Our pick</strong> is the Manors Stableford Short in Dune. Every polo in this section works with it, and so does almost every polo you already own."],
  ["sounder--monterey-stripe-polo-in-indigo-and-slate--4", "walker--members-polo-3--2"]),
 ("Pastels", "pastels", ["#c4e6d4", "#f1df9b", "#e6e1d6"], ["Mint", "Butter", "Pebble"],
  "Soft color on a pale base. Two pastels at most.",
  ["Pastels look best on a pale base, so start with pebble or sand shorts and add one or two soft colors on top: mint, powder blue, butter. They read as summer and they photograph well on a green course.",
   "The rule is two pastels at most, and never the same intensity. A mint collar and a butter layer work; a mint shirt, pink shorts and a yellow hat start to look like an Easter basket. Keep the shoes white.",
   "<strong>Our pick</strong> is the Radry Contrast Quarter Zip in butter. It&rsquo;s the one piece of color you need, and it goes over every polo here."],
  ["radry--contrast-quarter-zip-butter--2", "sounder--capri-collar-polo-mint-natural--3"]),
 ("Earth Tones", "earth-tones", ["#5b3b28", "#9a7656", "#efe8da"], ["Brown", "Mocha", "Ivory"],
  "Brown, mocha and cream: the fall look that never looks like trying.",
  ["Earth tones are the most forgiving palette in golf. Brown pants, a mocha or toffee polo and a cream layer go together in almost any combination, and they look right on a dry Texas fairway in October.",
   "Go tonal, with browns on browns, and let a cream or ivory piece do the contrast. One pattern is plenty: the Devereux medallion print or the Fella stripe, not both.",
   "<strong>Our pick</strong> is the Devereux El Classico Pant in brown, at $88 the best value on the page. It goes with every top in this section."],
  ["casualist--weekend-pique-polo-mocha--2", "odd-ritual--caddie-jacket-chocolate--2"]),
 ("Fall Knit &amp; Pleats", "fall-knit-and-pleats", ["#7d8a5a", "#e6e1d6", "#4f5337"], ["Moss", "Pebble", "Olive"],
  "A knit polo, pleated pants and a vest for the first cold round.",
  ["When it drops below 60, swap the polo for a knit polo sweater. It looks better than a quarter-zip over a polo, and it&rsquo;s warm enough on its own. Put it over pale pleated trousers so the knit stands out.",
   "If you need more warmth, add a vest rather than a jacket; it keeps your arms free for the swing. Greens and stone work best here: moss, olive and pebble.",
   "<strong>Our pick</strong> is the Students Riverview Knit Polo Sweater in moss. A cable knit with an open collar is the single best fall golf piece we&rsquo;ve seen this year."],
  ["manors--reversible-polartec-fleece-vest--dark-olive--0", "students--knight-knitted-l-s-polo-sweater-1--coffee--1"]),
 ("Navy &amp; Stripes", "navy-and-stripes", ["#1d2a44", "#7fa3d8", "#f5f5f2"], ["Navy", "Stripe", "White"],
  "Navy pants and a striped polo: the classic that always works.",
  ["Navy pants and a striped polo is the outfit you can wear to any course in the world. Navy makes every stripe look sharp, and a white collar ties it together.",
   "Keep the stripe on top only, and pick one stripe color besides white. For a layer, use something that repeats the navy: a band of it on a cream knit, or a plain navy shell.",
   "<strong>Our pick</strong> is the Left of Field Mornington Polo in blue and white stripe. It&rsquo;s the stripe in its simplest form, and it looks good with all three pants."],
  ["left-of-field--mornington-polo-blue-white-stripe--1", "sounder--monterey-stripe-polo-in-deep-red-and-dee--4"]),
 ("One Loud Piece", "one-loud-piece", ["#141414", "#4f9ec7", "#3c3c3c"], ["Black", "Print", "Charcoal"],
  "One shirt that shouts. Everything else stays quiet.",
  ["The rule is the same as with a bag: only one. A camp shirt covered in golf carts or a sunrise print looks great when the pants are black or charcoal and the shoes are plain. Add a second loud piece and it stops looking chosen.",
   "Camp shirts are casual, so check the dress code. For courses that want a collar, the plaid polo gets you most of the way there.",
   "<strong>Our pick</strong> is the Fella Bruno Camp Shirt. Palm trees and golf carts, and it&rsquo;s exactly as fun as it sounds."],
  ["walker--whitsundays-ss-shirt--2", "fella--bruno-camp-shirt-tropical-golf-cart--3"]),
]
PICKS = {"odd-ritual--pleated-daily-trouser-black", "manors--stableford-shorts--dune", "radry--contrast-quarter-zip-butter",
         "devereux--el-classico-pant-brown--brown", "students--riverview-knit-ls-polo-sweater--moss",
         "left-of-field--mornington-polo-blue-white-stripe", "fella--bruno-camp-shirt-tropical-golf-cart"}
P["devereux--el-classico-pant-brown--brown"] = P.pop("devereux--el-classico-pant-brown")

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 30px;"'
IMGSTY = 'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5;"'
GRID_CSS = ('<style>/*TGI-OUTFIT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
            '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.slot-hdr{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;text-align:center;margin:34px 0 14px;opacity:.75}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>A good golf outfit isn&rsquo;t a collection of nice pieces. It&rsquo;s a few pieces that agree with each other. The golfers you notice on the first tee have usually picked one idea, like pants and a tee, all earth tones or one loud shirt, and kept everything else out of its way.</p>
    <p>This guide has seven of those ideas, every one built from brands on our <a href="/brands/best-independent-golf-brands" style="border-bottom:1px solid currentColor">25 best independent golf brands</a>. Each look opens with photographs and a palette, then gives you two or three options for every piece, so you can build it at your price and in your size.</p>
    <h2 class="products-hdr btk-story-hdr">Three Rules</h2>
    <p><strong>One idea per outfit.</strong> Decide what the outfit is about first: a color, a fit or one piece. Everything else supports it.</p>
    <p><strong>Three colors, one pattern.</strong> The same rule as a golf bag. Pick a palette of three, and if one piece has a pattern, keep the rest plain.</p>
    <p><strong>Fit before logos.</strong> Pants that break just over the shoe and shorts that end just above the knee do more than any brand name. Buy the fit first.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Looks</span><span>Seven</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>45, from 12 brands</span></div>
      <div class="sidebar-detail"><span class="l">The rule</span><span>One idea per outfit</span></div>
      <div class="sidebar-detail"><span class="l">Easiest start</span><span>Shorts &amp; a jersey polo</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>October 10, 2026</span></div>
      <a href="#pants-and-a-tee" class="sidebar-cta">See the looks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#GolfOutfit</span>
        <span class="hashtag">#WhatToWear</span>
        <span class="hashtag">#TheGrassyIssue</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

NOTE = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="how-we-picked">How We Picked</h2>
  <div %s>
    <p style="margin:0 0 16px;">Every piece comes from a brand on our 25 best independent golf brands list, and every one was in stock in at least some sizes when we checked on October 10, 2026. A few were down to their last sizes, which we&rsquo;ve noted. Photographs are the brands&rsquo; own.</p>
    <p style="margin:0 0 16px;">Prices are in each store&rsquo;s own currency. Where Sounder and Walker Golf Things publish a US price, it&rsquo;s in brackets; other dollar figures are approximate. For the same approach applied to your bag, see <a href="/drops/curating-your-golf-bag-setup">Golf Bag Setup Ideas</a>.</p>
  </div>
</section>
""" % PROSE

FAQ = [
    ("How do I put together a golf outfit?",
     "Pick one idea for the outfit, such as pants and a tee, a color palette or one loud piece, then choose three colors and at most one pattern. Get the fit right: pants that break just over the shoe and shorts that end just above the knee."),
    ("Can you wear a t-shirt to play golf?",
     "At most public courses and munis, yes, and a heavyweight tee with good pants is now a common look. Many private clubs still require a collar, so check the dress code before you go."),
    ("What colors look good on a golf course?",
     "Navy, stone, brown and green look right on a course because they sit alongside the grass rather than fighting it. Pastels like mint, butter and powder blue work well in summer on a pale base."),
    ("What should I wear golfing when it's cold?",
     "Swap the polo for a knit polo sweater and add a vest instead of a jacket, so your arms stay free for the swing. Pleated trousers in a pale color keep the outfit from going too dark."),
    ("What length should golf shorts be?",
     "Just above the knee for most people. Longer, looser shorts are a deliberate 1990s look, and they work best with a pleat."),
]


def items():
    for o in SPEC["outfits"]:
        for slot, its in o["slots"]:
            for b, h, c in its:
                yield o["key"], slot, b, h, c


def card(b, h, c, idx):
    k = key(b, h, c)
    name, price, copy = P[k]
    fr = FR[k]
    label = H.unescape(f"{BRAND[b]} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    url = f'{SHOP.get(b, SPEC["domains"][b])}/products/{quote(h)}'
    star = "&#9733; Our pick &middot; " if k in PICKS else ""
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{star}{BRAND[b]}</div>'
            f'<div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def swatches(cols, names):
    s = "".join(f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:6px;margin:0 8px;">'
                f'<span style="display:block;width:44px;height:44px;border-radius:50%;background:{c};border:1px solid rgba(0,0,0,.12);"></span>'
                f'<span style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;">{n}</span></span>'
                for c, n in zip(cols, names))
    return f'<div style="display:flex;justify-content:center;margin:6px 0 22px;">{s}</div>'


def band(frames):
    figs = []
    for f in frames:
        b = f.split("--")[0]
        base, n = f.rsplit("--", 1)
        f = f"{base}-{int(n) + 1}"  # frames named by raw index (0-based) -> file -N (1-based)
        figs.append(f'<figure style="margin:0;"><img src="{IMG}/{f}.jpg" alt="{H.escape(BRAND[b])} photograph" loading="lazy" {IMGSTY} />'
                    f'<figcaption class="ig-cap">{BRAND[b]}</figcaption></figure>')
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px;max-width:1180px;margin:0 auto 26px;">'
            + "".join(figs) + '</div>')


def look(i, lk, n0):
    name, anchor, cols, names, kicker, paras, frames = lk
    o = [x for x in SPEC["outfits"] if x["key"] == anchor][0]
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in paras)
    body, n = "", n0
    for slot, its in o["slots"]:
        cards = "\n".join(card(b, h, c, n + j) for j, (b, h, c) in enumerate(its))
        n += len(its)
        body += (f'  <p class="slot-hdr">{slot} &middot; {len(its)} options</p>\n'
                 f'    <div class="products-grid" data-n="{len(its)}">\n{cards}\n    </div>\n')
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Look {i}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <p class="cat-kicker"><strong>{" &middot; ".join(names)}</strong>{kicker}</p>\n'
            f'  {band(frames)}\n  {swatches(cols, names)}\n'
            f'  <div {PROSE}>\n{prose}\n  </div>\n{body}</section>\n'), n


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    lst, pos = [], 1
    for _, _, b, h, c in items():
        lst.append({"@type": "ListItem", "position": pos, "url": f'{SHOP.get(b, SPEC["domains"][b])}/products/{quote(h)}',
                    "name": H.unescape(f"{BRAND[b]} {P[key(b, h, c)][0]}")}); pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": DATE, "dateModified": DATE,
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": lst},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "How to Build a Golf Outfit", "item": URL}]},
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
    ks = [key(b, h, c) for _, _, b, h, c in items()]
    missing = [k for k in ks if k not in P or not FR.get(k)]
    assert not missing, missing
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  How to Build a Golf Outfit</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Manors, Odd Ritual, Students, Devereux, Sounder and more</span><span class="dot"></span>
    <span>7 looks &middot; {len(set(ks))} pieces &middot; prices read October 10, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Two golfers on a clifftop links course above the sea, one crouching to read a putt, from Sounder&rsquo;s own shoot" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for i, lk in enumerate(LOOKS, 1):
        o, n = look(i, lk, n); body += o
    body += NOTE + faq_html()
    out = head_top() + head_rest.replace('</head>', GRID_CSS + '</head>', 1) + body + tail
    print(f"  {n-1} cards, {len(set(ks))} unique pieces")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus"):
        if leak in above: bad.append("leak " + leak)
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
