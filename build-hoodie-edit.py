#!/usr/bin/env python3
"""build-hoodie-edit.py — "The Fall Hoodie Edit: 28 Golf Hoodies for 2026" 14 October 2026.
Lenny: "let's pivot to Hoodies- apres golf makes a good one", then picked from a 74-hoodie options sheet:
the 26 TGI picks + 20, 22, 24, 39, 63, 72, minus 33, 53, 55, 59.
FACTS: every hoodie in stock in a medium on the brand's own store, Oct 14 2026 (Shopify products.json / .js).
Prices are store currency: J.Lindeberg EUR (store showed EUR), Mount Tee AUD, Walker Canvas Hood AUD (not on Walker's
US store; Hedge Hood is $110 on the US store). Rates Oct 14 2026: EUR 1.1195 USD, AUD 0.701 USD.
Malbon Fesque Department of Game is a preorder shipping by Nov 4. Copy paraphrases brand descriptions; quoted phrases verbatim.
PHOTOS: brands' own (research/hoodie-edit/frame.py). Sunset Twirl's only images are 540px (flagged to Lenny).
Hero: single shot, Jones Sports Co. Range Hoodie on a dune path (Lenny: needs a single hero shot).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Best Golf Hoodies for Men: 28 Picks for Fall 2026"
DESC = ("The 28 best golf hoodies for men this fall from Après Golf, Malbon, Devereux and Macade: graphic, "
        "heavyweight, knit and performance hoodies, all in stock.")
H1 = "The Fall Hoodie Edit: The 28 Best Golf Hoodies for Men in 2026"
BC = "The Fall Hoodie Edit"
SLUG = "the-fall-hoodie-edit-2026"
IMG = "/images/hoodie-edit"
SHOP = ""
P = {
 # Clubhouse & graphic
 "i-will-not-apres-golf-hoodie": ("Après Golf", "Find Your Line Après-Golf&reg; Hoodie", "$98", "https://apresgolf.com/products/i-will-not-apres-golf%C2%AE-hoodie",
   "Après Golf started this whole edit. It makes a cream midweight with a gondola over the mountains and &ldquo;Find Your Line&rdquo; under it, in Après Golf&rsquo;s own private-label blank: 9.4 oz, 80% cotton. Their pitch: &ldquo;Gondola? How about golfdola.&rdquo; Relaxed fit, M to XXL."),
 "sunset-twirl-original-blue-log": ("Après Golf", "Sunset Twirl Original Blue Logo Hoodie", "$88", "https://apresgolf.com/products/sunset-twirl-original-blue-logo-hoodie",
   "Hand tie-dyed in pink, mint and blue, with the round blue Après Golf logo on the chest. Every one is dyed by hand, so no two match. The loudest thing you can wear to the 19th hole. S to L."),
 "olive-tree-hoodie": ("Aimé Leon Dore", "Olive Tree Hoodie", "$200", "https://aimeleondore.com/products/olive-tree-hoodie",
   "Heather grey, 530 gsm pigment-washed loopback terry, and a navy olive tree printed on the chest. Raglan sleeves and flat braided drawstrings. No cotton hoodie here is heavier. XS to XXL."),
 "lonestar-country-club-hoodie-n": ("Devereux Golf", "Lonestar Country Club Hoodie, Navy", "$84", "https://devereuxgolf.com/products/lonestar-country-club-hoodie-navy",
   "Devereux made the Texas one: a navy fleece hoodie with Devereux&rsquo;s Lone Star State Country Club graphic on the back: a Texas outline, a golf shop sign and a sun. S to XXL."),
 "clubhouse-hoodie": ("Ghost Golf", "Clubhouse Hoodie, Burgundy", "$160", "https://ghostgolf.com/products/clubhouse-hoodie",
   "Ghost Golf keeps it quiet: 420 gsm French terry, a tonal chest logo, a classic fit and a ribbed waist. Shown in burgundy, with five more colors."),
 "fesque-department-of-game-hood": ("Malbon Golf", "Fesque Department of Game Hoodie, Sunfaded Olive", "$168", "https://malbon.com/products/fesque-department-of-game-hoodie-sunfaded-olive",
   "Malbon&rsquo;s new field-club graphics on a heavyweight cotton hoodie, sun-faded so it looks lived in, with art on the chest, sleeve and back. A preorder: Malbon says it ships by November 4. XS to XXL."),
 "go-for-broke-hoodie-olive": ("Merrill Golf", "Go For Broke Hoodie, Olive", "$150", "https://merrillgolf.com/products/go-for-broke-hoodie-olive",
   "A garment-dyed olive hoodie in 14 oz cotton fleece, made in the USA, with a &ldquo;Go For Broke!&rdquo; print front and back. S to XL."),
 "parm-049": ("Parmore Golf", "Graphic Hoodie, Motorsport Print", "$100", "https://parmoregolf.com/products/parm-049",
   "Parmore puts a red italic wordmark on black 350 gsm fleece. It built this one for &ldquo;when it&rsquo;s too cold for a quarter-zip but you&rsquo;re not done for the day.&rdquo; Boxy, S to 3XL."),
 "racing-stable-hoodie-2": ("Siegelman Stable", "Racing Stable Hoodie, Cobalt", "$248", "https://siegelmanstable.com/products/racing-stable-hoodie-2",
   "Siegelman makes it in organic cotton fleece, washes it in a bright cobalt and puts the Racing Stable horse and sulky on the back. It fits boxy and cropped. XS to XXL."),
 "fesque-tour-divot-camo-hoodie-": ("Malbon Golf", "Fesque Tour Divot Camo Hoodie, Flame", "$168", "https://malbon.com/products/fesque-tour-divot-camo-hoodie-flame-bark-camo",
   "Malbon cuts this one in blaze orange cotton fleece with a bark-camo hood lining, an embroidered M script on the chest and a Tour Divot graphic across the back. It brings hunting-season colors to the course. XS to M left."),
 "mountaineering-hoody": ("Mount Tee Golf", "Mountaineering Hoody, Black", "A$79 (~$55)", "https://mountteegolf.com.au/products/mountaineering-hoody",
   "Mount Tee made this for &ldquo;cooler, casual morning rounds at your local track&rdquo;: brushed cotton jersey, raglan sleeves and the big Mount Tee Mountaineering Golf print on the back. M to XL."),
 "rhythm-hoodie-bone": ("Palm Golf Co.", "Rhythm Hoodie, Bone", "$79.99", "https://palmgolfco.com/products/rhythm-hoodie-bone",
   "A bone hoodie with a palm tree, roses and &ldquo;Find Your Rhythm&rdquo; across the back, a reminder about tempo. The cheapest graphic hoodie here. M to 2XL; also black and navy."),
 # Heavyweight & fleece
 "union-made-hoodie-heather-oatm": ("Malbon Golf", "Union Made Hoodie, Heather Oatmeal", "$168", "https://malbon.com/products/union-made-hoodie-heather-oatmeal",
   "A heavyweight cotton sweatshirt with a workwear finish: sun-faded oatmeal, a V-notch at the neck, a rope drawcord and a Union Made handshake graphic. S to XXL; also dusty navy ($178)."),
 "hedge-hood": ("Walker Golf Things", "Hedge Hood, Navy", "$110", "https://www.walkergolfthings.com/en-us/products/hedge-hood",
   "The heavy layer of Walker&rsquo;s Blooming Grounds drop: 400 gsm brushed fleece with a green Walker script on the chest and a kangaroo pocket Walker says fits a scorecard. M to XXXL on the US store."),
 "canvas-hood-olive": ("Walker Golf Things", "Canvas Hood, Olive", "A$160 (~$112)", "https://www.walkergolfthings.com/products/canvas-hood-olive",
   "Not a sweatshirt at all: heavyweight cotton canvas cut like an anorak, with a zip that runs up and around the hood, a fleece-lined hood and a vintage wash. Only a medium left, on Walker&rsquo;s Australian store."),
 "warm-up-hoodie-black": ("Huega House", "Warm Up Hoodie, Black", "$66", "https://huegahouse.com/products/warm-up-hoodie-black",
   "Heavyweight fleece, a relaxed fit, an embroidered icon on the chest and a track-club print on the back. The cheapest hoodie in the edit. S to XXL."),
 # Knit, wool & cashmere
 "wool-ribbed-knit-hoodie": ("Aimé Leon Dore", "Wool Ribbed Knit Hoodie, Jet Black", "$495", "https://aimeleondore.com/products/wool-ribbed-knit-hoodie",
   "Aimé Leon Dore charges the most here for a ribbed wool and nylon knit with double zips at the front and a bungee cord at the hood. It looks like a sweater from across the room. XS to XXL."),
 "chill-knit-hoodie-stone": ("Criquet", "Chill-Knit Hoodie, Stone", "$178", "https://criquetshirts.com/products/chill-knit-hoodie-stone",
   "Austin&rsquo;s own Criquet put the fabric from its best-selling Chill-Knit Pearl Snap into a hoodie: soft, textured and sharp enough to wear to dinner. Criquet suggests it under a shacket when the temperature really drops. S to XXL; also navy."),
 "plki-merino-wool-hooded-sweate": ("Eastside Golf", "Luxe Soft Hoodie", "$148", "https://eastsidegolf.com/products/plki-merino-wool-hooded-sweater",
   "A merino-blend knit in oatmeal with a big Eastside Golf script knitted into the front. Light enough to wear from October into spring. S to 3XL."),
 "kolton-wool-hoodie-kelp": ("J.Lindeberg", "Kolton Wool Hoodie, Kelp", "&euro;240 (~$269)", "https://jlindeberg.com/products/kolton-wool-hoodie-kelp",
   "A full-zip wool-blend knit in a chunky 7-gauge half-cardigan stitch, with a knitted hood and a two-way zip. New on J.Lindeberg&rsquo;s store this week. S to XXL; also seal brown."),
 "flow-light-knit-hoodie-pine": ("Macade Golf", "Flow Light Knit Hoodie, Pine", "$245", "https://macadegolf.com/products/flow-light-knit-hoodie-pine",
   "Macade&rsquo;s most technical knit: a merino blend with a low-profile hood, four-way stretch and a hollow core that moves sweat away and holds warmth. Made for rounds where the weather changes. S to XXL; also navy."),
 "merino-tencel-hoodie": ("Olydoe", "Merino Aire Hoodie", "$145", "https://olydoe.com/products/merino-tencel-hoodie",
   "Olydoe spins merino and Tencel around recycled nylon, so it breathes, resists odor and has a near-silk feel. A thin hoodie for under a vest or on its own. S to XXL, four colors."),
 "pine-green-tech-knit-hoodie": ("Macade Golf", "Cashmere Tech Knit Hoodie, Pine Green", "$150", "https://macadegolf.com/products/pine-green-tech-knit-hoodie",
   "A thin cotton and cashmere knit with an athletic fit and almost no details. The easy way into a knit hoodie at $95 less than the Flow. S to XXL; also cream, white and dark grey."),
 "tx-range-hoodie-sand": ("Macade Golf", "TX Range Hoodie, Sand", "$180", "https://macadegolf.com/products/tx-range-hoodie-sand",
   "A structured cotton jacquard knit in sand with a single oversized hand pocket at the waist. Heavy, relaxed and made for range sessions. S to XXL."),
 # Tech & smooth
 "range-hoodie-loden-green": ("Jones Sports Co.", "Range Hoodie, Loden Green", "$148", "https://jonessportsco.com/products/range-hoodie-loden-green",
   "Double-knit performance fleece with a DWR finish, so it works like a mid-layer and sheds a little rain like a shell. A zip stash pocket keeps a glove or phone dry. Jones&rsquo; own note: &ldquo;Worn 3x a week.&rdquo; S to XXL."),
 "monterey-hoodie": ("Quiet Golf", "Monterey Hoodie, Blue", "$148", "https://quietgolf.com/products/monterey-hoodie",
   "Cotton, modal and nylon, milled in Portugal, with a tonal logo and a smooth, drapey hand. It is the cleanest hoodie here. Blue comes in M, L and XXL, and four other colors are in stock."),
 "camargo-nylon-hoodie": ("Students Golf", "Camargo Nylon Hoodie, Black", "$178", "https://studentsgolf.com/products/camargo-nylon-hoodie",
   "Students made a stretch-nylon zip hoodie with technical paneling, a mesh lining, hidden pockets and the Students logo embroidered on the hood. It works as a shell on windy fall afternoons. S to XXL."),
 "grid-fleece-hoody": ("Sugarloaf Social Club", "Grid Tech Hoody, Oatmeal", "$120", "https://www.sugarloafsocialclub.com/products/grid-fleece-hoody",
   "Sugarloaf&rsquo;s Tech Hoody in a new micro-grid fleece, &ldquo;like a mountaineering base layer that we turned into a golf piece.&rdquo; Sugarloaf says to size down if you&rsquo;re between sizes. S to XXL; also heather blue and Nantucket red."),
}
SECTIONS = [
 ("Graphic Golf Hoodies", "clubhouse", ["i-will-not-apres-golf-hoodie", "sunset-twirl-original-blue-log", "lonestar-country-club-hoodie-n", "fesque-department-of-game-hood", "fesque-tour-divot-camo-hoodie-", "olive-tree-hoodie", "go-for-broke-hoodie-olive", "parm-049", "racing-stable-hoodie-2", "mountaineering-hoody", "rhythm-hoodie-bone", "clubhouse-hoodie"],
  "<strong>Twelve picks</strong>The hoodie for after the round: big back prints, a Texas country club, two from Malbon and Après Golf&rsquo;s own."),
 ("Heavyweight Golf Hoodies", "heavyweight", ["union-made-hoodie-heather-oatm", "hedge-hood", "canvas-hood-olive", "warm-up-hoodie-black"],
  "<strong>Four picks</strong>These are for the coldest tee times: 400 gsm brushed fleece, sun-faded cotton and a canvas anorak."),
 ("Knit Golf Hoodies: Wool &amp; Cashmere", "knit", ["chill-knit-hoodie-stone", "flow-light-knit-hoodie-pine", "pine-green-tech-knit-hoodie", "tx-range-hoodie-sand", "plki-merino-wool-hooded-sweate", "kolton-wool-hoodie-kelp", "merino-tencel-hoodie", "wool-ribbed-knit-hoodie"],
  "<strong>Eight picks</strong>These hoodies pass for sweaters, and they are the biggest change from our summer hoodie edits: three from Macade, Austin&rsquo;s own Criquet, and wool from Aimé Leon Dore and J.Lindeberg."),
 ("Performance Golf Hoodies", "tech", ["range-hoodie-loden-green", "camargo-nylon-hoodie", "grid-fleece-hoody", "monterey-hoodie"],
  "<strong>Four picks</strong>For playing in, not just after: water-shedding fleece, stretch nylon, grid fleece and a smooth modal blend."),
]
N = 28
PAIRS = {}
LIFE = []
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Late October is when Austin starts to get hoodie weather: a cold first tee and a warm back nine. We started with <a href="#clubhouse">Après Golf</a>, whose whole brand is the part after the round, then swept more than 80 stores in the TGI index for the best golf hoodies for men this fall. Three trends stood out, along with a color palette that is hard to miss.</p>
    <h2 class="products-hdr btk-story-hdr">Golf Hoodie Trends for Fall 2026</h2>
    <p><strong>The hoodie went knit.</strong> Our hoodie edits in June and July were mostly cotton fleece. This fall eight of our 28 are knits that pass for sweaters: Macade made three, Austin&rsquo;s own Criquet put its Chill-Knit into a hood, Eastside knitted its script into merino, and Aimé Leon Dore and J.Lindeberg went to wool. You can wear these to dinner.</p>
    <p><strong>Everything comes pre-worn.</strong> Malbon sun-fades its Union Made and Department of Game hoodies, Merrill garment-dyes its olive, Siegelman washes its cobalt and Aimé Leon Dore pigment-washes its terry. Brands want a hoodie to look like you have owned it for ten years on the first day.</p>
    <p><strong>The detail moved to the back and the hood.</strong> The graphic hoodies keep the front to a small logo and put the art on the back: Devereux&rsquo;s Lone Star country club, Siegelman&rsquo;s racing stable, Mount Tee&rsquo;s mountaineering badge. And hoods got attention: a camo lining on Malbon&rsquo;s Tour Divot, a zip that runs around the hood on Walker&rsquo;s Canvas Hood, a bungee cord on Aimé Leon Dore&rsquo;s knit.</p>
    <h2 class="products-hdr btk-story-hdr">What&rsquo;s Freshest</h2>
    <p>Six of these went up in the last week. J.Lindeberg&rsquo;s Kolton wool zip hoodie landed today, Sugarloaf&rsquo;s Grid Tech Hoody on October 12, Aimé Leon Dore&rsquo;s Olive Tree and wool knit hoodies and Criquet&rsquo;s Chill-Knit on October 9, and Malbon&rsquo;s Department of Game on October 8, as a preorder that ships by November 4.</p>
    <h2 class="products-hdr btk-story-hdr">The Colors of Fall: Olive, Oatmeal and Navy</h2>
    <p><strong>Green is the color of the season.</strong> Seven of the 28 are green, and none of them is kelly green: sun-faded olive from Malbon and Merrill, Walker&rsquo;s olive canvas, Jones&rsquo; loden, Macade&rsquo;s pine twice and J.Lindeberg&rsquo;s kelp. The greens look like a course in late fall, not in June.</p>
    <p><strong>Oatmeal is the new white.</strong> Another seven sit in the cream family: Après Golf&rsquo;s cream, Malbon and Sugarloaf&rsquo;s oatmeal, Macade&rsquo;s sand, Palm&rsquo;s bone, Criquet&rsquo;s stone and Eastside&rsquo;s oat knit. Nobody made a stark white hoodie we liked.</p>
    <p><strong>Navy holds, and one bright is enough.</strong> Devereux, Walker and Olydoe keep navy as the dark option, with Ghost&rsquo;s burgundy for a change. The brights are single statements: Siegelman&rsquo;s cobalt, Malbon&rsquo;s blaze orange and Après Golf&rsquo;s hand-dyed tie-dye.</p>
    <p>Every hoodie here was in stock in a medium on the brand&rsquo;s own store on October 14, 2026. Prices are in the store&rsquo;s currency, with US dollars in brackets for the others. If you only buy three: the Après Golf Find Your Line ($98), Criquet&rsquo;s Chill-Knit in stone ($178) and Macade&rsquo;s Cashmere Tech Knit in pine ($150).</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Hoodies</span><span>28</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>21</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$66&ndash;$495</span></div>
      <div class="sidebar-detail"><span class="l">Lead pick</span><span>Après Golf Find Your Line</span></div>
      <div class="sidebar-detail"><span class="l">Color of the season</span><span>Olive and pine</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>J.Lindeberg Kolton, Oct 14</span></div>
      <div class="sidebar-detail"><span class="l">Heaviest</span><span>Aimé Leon Dore, 530 gsm</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Huega House, $66</span></div>
      <a href="#clubhouse" class="sidebar-cta">Start with Après Golf &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfHoodie</span>
        <span class="hashtag">#ApresGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">You can find more hoodies in <a href="/drops/14-hoodies-that-caught-my-eye">14 Hoodies That Caught My Eye</a> (June) and <a href="/drops/the-hoodie-and-shorts-edit">Hoodie and Shorts</a> (July). For more fall layers, see <a href="/drops/fresh-fall-drops-students-walker-sugarloaf">Three Fresh Fall Drops</a>.</p>
</section>
"""
FAQ = [
 ("What colors are in for fall 2026 golf?", "Across the 28 hoodies we picked: muted greens (olive, loden, pine and kelp) and the cream family (oatmeal, sand, bone and stone), with navy as the dark option and single brights like cobalt and blaze orange."),
 ("What are the best golf hoodies for fall 2026?", "Our 28 picks run from Après Golf's Find Your Line hoodie ($98) and Devereux's Lonestar Country Club hoodie ($84) to knit hoodies from Criquet, Macade, Aimé Leon Dore and J.Lindeberg, plus tech hoodies from Jones Sports Co., Students and Sugarloaf Social Club."),
 ("Can you wear a hoodie on the golf course?", "At most public courses and munis, yes. Some private clubs still ban them, so check the dress code. A knit or tech hoodie like Macade's Flow Light Knit or Jones' Range Hoodie reads as a sweater or mid-layer and is the safer bet."),
 ("Does Après Golf make a good hoodie?", "Après Golf's Find Your Line and I Will Not hoodies are its own private-label blank: a 9.4 oz, 80% cotton midweight fleece in a relaxed fit, $98. Its tie-dyed Sunset Twirl hoodies are $88 and dyed by hand."),
 ("What is a knit golf hoodie?", "A hoodie knitted like a sweater instead of cut from sweatshirt fleece, usually in merino, cashmere blends or cotton. It is lighter, drapes better and can be worn to dinner. Examples here: Criquet Chill-Knit, Macade Flow Light Knit and Cashmere Tech Knit, Eastside Luxe Soft and J.Lindeberg Kolton."),
 ("What is the best performance golf hoodie?", "For playing in, look for stretch, a water-resistant finish and a pocket that closes. Jones Sports Co.'s Range Hoodie ($148) is double-knit fleece with a DWR finish and a zip stash pocket; Students' Camargo Nylon Hoodie ($178) is a stretch-nylon shell; Macade's Flow Light Knit ($245) is a merino blend with four-way stretch."),
 ("How should a golf hoodie fit?", "Loose enough to swing in without pulling across the shoulders, but not so long it catches on your belt at the top of the backswing. Raglan sleeves, like Aimé Leon Dore's Olive Tree and Mount Tee's Mountaineering Hoody, give the most room. Boxy, cropped cuts like Siegelman's and Parmore's are for after the round."),
 ("Are these hoodies in stock?", "Every hoodie here was in stock in a medium on its brand's own store on October 14, 2026. Malbon's Department of Game hoodie is a preorder shipping by November 4, and Walker's Canvas Hood is down to one size."),
]
HERO_ALT = "A golfer in Jones Sports Co.'s loden green Range Hoodie standing on a path through tall dune grass"
FRN = json.loads((ROOT / "research/hoodie-edit/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-FF-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-14", "dateModified": "2026-10-14",
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


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


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
    <span>21 brands, four kinds of hoodie</span><span class="dot"></span>
    <span>28 picks &middot; in stock, checked October 14, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Lehi", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram"):
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
