#!/usr/bin/env python3
"""build-fresh-fall-drops.py — "Three Fresh Fall Drops: Students, Walker Golf Things and Sugarloaf Social Club" 13 October 2026.
Lenny: "students just did a fresh drop, let's do a post about 3 recent fresh fall releases", then "Let's use all three brands
12 items each but make sure they are from the new fall drops".
FACTS: every pick was created/published on the brand's store in the last two weeks (Shopify products.json, read Oct 13, 2026):
Students Fall Drop 2 (created Sept 30, live Sept 30 - Oct 1); Walker's October "Kooka" drop (created Sept 8, live Oct 8 and Oct 13);
Sugarloaf's October drop (live Oct 6 and Oct 12). Nothing here appeared in TGI's Sept 24 fall-drops post or the Sept 27
Sugarloaf Autumn Layers post. Sugarloaf's October drop is nine products (two sold out), so its 12 cards count colorways of
the work jacket, rugby and grid fleece separately. Walker prices are its US-store prices. Copy paraphrases each brand's own
product description; short quoted phrases are brand copy.
PHOTOS: each brand's own, from the product pages (research/fresh-fall/frame.py). Hero: one lifestyle frame per brand.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Three Fresh Fall Golf Drops: Students, Walker and Sugarloaf"
DESC = ("Thirty-six new pieces from three fall drops that landed in the last two weeks: Students' Fall Drop 2, "
        "Walker Golf Things' Kooka drop and Sugarloaf Social Club's October release.")
H1 = "Three Fresh Fall Drops: Students, Walker Golf Things and Sugarloaf Social Club"
BC = "Three Fresh Fall Drops"
SLUG = "fresh-fall-drops-students-walker-sugarloaf"
IMG = "/images/fresh-fall"
SHOP = ""
STU = "https://studentsgolf.com/products/"
WLK = "https://www.walkergolfthings.com/en-us/products/"
SSC = "https://www.sugarloafsocialclub.com/products/"
P = {
 # Students — Fall Drop 2
 "obisponylonjacket": ("Students", "Obispo Nylon Jacket, Camo", "$268", STU + "obispo-nylon-jacket",
   "The statement piece of the drop. Students says the green camo is based on an oil spill on the surface of a murky golf course lake, and cuts it as a long, structured mack. S to XXL in stock."),
 "perrisnyloncoat": ("Students", "Perris Nylon Coat, Camo", "$178", STU + "perris-nylon-coat",
   "The same oil-slick camo in a shorter, boxier coat that sits at the hip. Easier to wear over a hoodie, and $90 less than the Obispo. S to XL."),
 "osonylonjacket1": ("Students", "Oso Nylon Jacket, Peapod", "$158", STU + "oso-nylon-jacket-1",
   "Students cuts this one in crinkled nylon in a pale peapod green, with chest pockets and a snap front. A light utility layer for a round that starts cold and ends warm."),
 "lockecardigansweater1": ("Students", "Locke Cardigan Sweater, Pine", "$158", STU + "locke-cardigan-sweater-1",
   "This collegiate cardigan comes in deep pine with STUDENTS arched across the back. It also comes in brown. S to XXL."),
 "visaliaknitlspolosweater": ("Students", "Visalia Knit LS Polo Sweater, Midnight", "$158", STU + "visalia-knit-ls-polo-sweater",
   "Wide navy and tan stripes, a zip collar and a script logo: Students calls it a rugby-style sweater polo. 100% cotton, every size in stock."),
 "carlsbadknitlspolosweate": ("Students", "Carlsbad Knit L/S Polo Sweater, Khaki", "$148", STU + "carlsbad-knit-l-s-polo-sweater-1",
   "A cream sweater polo knit in a diamond hex texture, worn in the lookbook with brown shorts. M, L and XL left."),
 "palmdalestripeknitcrewsw": ("Students", "Palmdale Stripe Knit Crew Sweater, Khaki", "$158", STU + "palmdale-stripe-knit-crew-sweater",
   "Black and cream stripes run across a full-fashioned cotton crew with a small SG crest. Only L, XL and XXL left already."),
 "irvinewaffleknitcrewswea": ("Students", "Irvine Waffle Knit Crew Sweater, Tan", "$118", STU + "irvine-waffle-knit-crew-sweater-1",
   "A light waffle-knit crew that breathes on a warm November afternoon. The cheapest knit in the drop, and every size is in stock."),
 "viejoflannellsshirt": ("Students", "Viejo Flannel LS Shirt, Brown", "$118", STU + "viejo-flannel-ls-shirt",
   "A brushed brown and rust check flannel with a slightly cropped body, so it sits right over shorts. S to XL."),
 "newportsspoloshirt1": ("Students", "Newport S/S Polo Shirt, Khaki", "$118", STU + "newport-s-s-polo-shirt-1",
   "A retro polo with navy and sky panels cut into the sides, contoured to move through the swing. Students suggests wearing it with slacks. L and XL left."),
 "orovillesspoloshirt": ("Students", "Oroville S/S Polo Shirt, Midnight", "$108", STU + "oroville-s-s-polo-shirt",
   "Students puts an all-over pinstripe on a navy cotton polo and a big star logo on the back. Every size in stock."),
 "sandiegotrackpants2": ("Students", "San Diego Track Pants, Pine", "$128", STU + "san-diego-track-pants-2",
   "These pine green track pants have cream side panels, made for the drive there and the range before. S to XXL."),
 # Walker — Kooka drop
 "outbackknitpolo": ("Walker Golf Things", "Outback Knit Polo, Dust / Blue", "$120", WLK + "outback-knit-polo",
   "Walker calls it the statement piece of the drop: an acrylic knit with a six-color jacquard of stockmen, a windmill and a mountain across the body. The polo you notice from across the parking lot. S to XXXL."),
 "kookatwotonepolo1": ("Walker Golf Things", "Kooka Two-Tone Polo, Navy / White", "$90", WLK + "kooka-two-tone-polo-1",
   "Walker calls this its color-block classic: a navy pique body with a white ribbed collar and placket, tortoiseshell buttons and the Kooka patch. Every size in stock."),
 "kookatwotonepolo": ("Walker Golf Things", "Kooka Two-Tone Polo, Lemon / Green", "$90", WLK + "kooka-two-tone-polo",
   "The same polo comes in pale lemon with a green collar. The brighter of the two. M to XXL."),
 "kookaloomknitpolo": ("Walker Golf Things", "Kooka Loom Knit Polo, Oat / Cream", "$110", WLK + "kooka-loom-knit-polo",
   "A speckled oat knit with a cream rib collar and no buttons at all: the look of a knit polo without the weight. M to XXL."),
 "kookawindbreaker": ("Walker Golf Things", "Kooka Windbreaker, Sand / Navy", "$130", WLK + "kooka-windbreaker",
   "A nylon pullover printed in a sand and navy check, cut loose enough to go over a polo and light enough to live in the bag. M to XXL."),
 "featherlitekookapolo7": ("Walker Golf Things", "Featherlite Kooka Polo, Pine", "$100", WLK + "featherlite-kooka-polo-7",
   "Walker makes its everyday pique polo in pine green, with a striped collar and pearl buttons. Shot by a pond on the course. M to XXL."),
 "vacationterrypolo": ("Walker Golf Things", "Vacation Terry Polo, Cream / Choc", "$100", WLK + "vacation-terry-polo",
   "Walker knits this one in cotton terry with vertical jacquard stripes and a chocolate collar. Walker pitches it for a slow start on the first tee and a long lunch after. S to XXXL."),
 "whitsundaysssshirt": ("Walker Golf Things", "Whitsundays SS Shirt, Sunrise", "$120", WLK + "whitsundays-ss-shirt",
   "A rayon camp-collar shirt with an all-over print of palms and coastline. It is from Walker&rsquo;s Vacation Collection, part of the same October release. M to XXL."),
 "pitchcargoshort1": ("Walker Golf Things", "Pitch Cargo Short, Sand", "$100", WLK + "pitch-cargo-short-1",
   "Walker&rsquo;s new ripstop utility short has an elastic waist, zipped pockets, cargo pockets and two tee slots at the back. Every size from 30 to 38."),
 "scorecardtshirt": ("Walker Golf Things", "Scorecard T-Shirt, Navy", "$50", WLK + "scorecard-t-shirt",
   "A navy cotton tee with a six-color scorecard print on the chest. The cheapest way into the drop. M to XXL."),
 "rodeocap": ("Walker Golf Things", "Rodeo Cap, Ecru / Choc", "$50", WLK + "rodeo-cap",
   "This ecru cotton cap has a chocolate brim and a kookaburra riding a kangaroo, embroidered in seven colors."),
 "cursivenyloncap": ("Walker Golf Things", "Cursive Nylon Cap, Forest", "$50", WLK + "cursive-nylon-cap",
   "This light forest green nylon cap carries a gold Walker script and a braided rope across the brim."),
 # Sugarloaf — October drop
 "sscworkjacketslts": ("Sugarloaf Social Club", "SSC Work Jacket, Slate", "$165", SSC + "ssc-work-jacket",
   "Sugarloaf&rsquo;s take on the work jacket everyone is wearing right now: vintage-washed cotton, unlined, with a little stretch. The brand calls it &ldquo;Tour-Tuff.&rdquo; S to XXL."),
 "sscworkjacketbrwns": ("Sugarloaf Social Club", "SSC Work Jacket, Brown", "$165", SSC + "ssc-work-jacket",
   "The same jacket in brown, which looks more like a classic work jacket. S to XXL."),
 "sscrugbyshirtnvys": ("Sugarloaf Social Club", "SSC Rugby Shirt, Navy", "$115", SSC + "ssc-rugby-shirt",
   "Sugarloaf made its new rugby in sweatshirt French terry, softer than its old ones, with a white collar. S to XXL."),
 "sscrugbyshirtgrys": ("Sugarloaf Social Club", "SSC Rugby Shirt, Grey", "$115", SSC + "ssc-rugby-shirt",
   "The lookbook shows the grey version with an orange cap. S to XXL."),
 "gridtzipfleecenant": ("Sugarloaf Social Club", "Grid Quarter-Zip, Nantucket Red", "$110", SSC + "grid-t-zip-fleece",
   "Sugarloaf put its classic quarter-zip into a new micro-grid performance fleece. The brand describes it as a mountaineering base layer turned into a golf piece. This is the faded-red colorway."),
 "gridtzipfleecenvy": ("Sugarloaf Social Club", "Grid Quarter-Zip, Heather Blue", "$110", SSC + "grid-t-zip-fleece",
   "The same grid fleece also comes in heather blue. Sugarloaf suggests sizing down if you are between sizes."),
 "gridtzipfleeceoat": ("Sugarloaf Social Club", "Grid Quarter-Zip, Oatmeal", "$110", SSC + "grid-t-zip-fleece",
   "The oatmeal colorway is the quietest of the three, shot over a striped polo."),
 "gridfleecehoodyoat": ("Sugarloaf Social Club", "Grid Tech Hoody, Oatmeal", "$120", SSC + "grid-fleece-hoody",
   "Sugarloaf cut its Tech Hoody shape in the new grid fleece, which is stretchy, warm and breathable. S to XXL in all three colors."),
 "gridfleecehoodynant": ("Sugarloaf Social Club", "Grid Tech Hoody, Nantucket Red", "$120", SSC + "grid-fleece-hoody",
   "The hoody in Nantucket red, the loudest piece in the drop."),
 "bigschevroncardwallet": ("Sugarloaf Social Club", "Big S Chevron Card Wallet", "$65", SSC + "big-s-chevron-card-wallet",
   "Hand-stitched needlepoint in the club&rsquo;s red, purple and blue chevron, made for Sugarloaf by Smathers &amp; Branson, with Italian leather. Three card slots."),
 "nantucketredneedlepointc": ("Sugarloaf Social Club", "&ldquo;Nantucket Red&rdquo; Needlepoint Can Cooler", "$40", SSC + "nantucket-red-needlepoint-can-cooler",
   "Smathers &amp; Branson stitches the needlepoint onto full-grain Italian leather, with a neoprene liner. For the beer on the walk to the 10th tee."),
 "nantucketredneedlepointb": ("Sugarloaf Social Club", "&ldquo;Nantucket Red&rdquo; Needlepoint Bottle Opener", "$35", SSC + "nantucket-red-needlepoint-bottle-opener",
   "A wooden opener with a needlepoint inlay and a hidden magnet, which the brand says makes it 100% more useful."),
}
SECTIONS = [
 ("Students: Fall Drop 2", "students", ["obisponylonjacket", "perrisnyloncoat", "osonylonjacket1", "lockecardigansweater1", "visaliaknitlspolosweater", "carlsbadknitlspolosweate", "palmdalestripeknitcrewsw", "irvinewaffleknitcrewswea", "viejoflannellsshirt", "newportsspoloshirt1", "orovillesspoloshirt", "sandiegotrackpants2"],
  "<strong>Twelve picks &middot; live September 30 &ndash; October 1</strong>The second fall delivery from the Southern California brand: an oil-slick camo, a run of knit sweater polos and cardigans, and colors pulled from a golf course in late October: pine, peapod, khaki and brown."),
 ("Walker Golf Things: The Kooka Drop", "walker", ["outbackknitpolo", "kookatwotonepolo1", "kookatwotonepolo", "kookaloomknitpolo", "kookawindbreaker", "featherlitekookapolo7", "vacationterrypolo", "whitsundaysssshirt", "pitchcargoshort1", "scorecardtshirt", "rodeocap", "cursivenyloncap"],
  "<strong>Twelve picks &middot; live October 8 and October 13</strong>Walker is Australian, so its October drop is spring gear back home. Over here it is the knit polo and windbreaker weather Austin gets in fall. The Kooka is the kookaburra patch on almost every piece."),
 ("Sugarloaf Social Club: The October Drop", "sugarloaf", ["sscworkjacketslts", "sscworkjacketbrwns", "sscrugbyshirtnvys", "sscrugbyshirtgrys", "gridtzipfleecenant", "gridtzipfleecenvy", "gridtzipfleeceoat", "gridfleecehoodyoat", "gridfleecehoodynant", "bigschevroncardwallet", "nantucketredneedlepointc", "nantucketredneedlepointb"],
  "<strong>Twelve picks &middot; live October 6 and October 12</strong>A work jacket, a softer rugby, a new grid fleece and needlepoint made with Smathers &amp; Branson. The drop is nine products, so the jackets, rugbys and fleece appear here in more than one color."),
]
N = 36
PAIRS = {}
LIFE = []
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The second wave of fall is here. Students put up Fall Drop 2 on September 30, Sugarloaf Social Club added a work jacket, a rugby and a new fleece over the past week, and Walker Golf Things released its Kooka drop last Thursday and today. Three brands, three very different looks, and the same four ideas keep showing up in all of them.</p>
    <h2 class="products-hdr btk-story-hdr">What Fall Golf Looks Like in 2026</h2>
    <p><strong>The knit polo is the shirt of the season.</strong> Every drop is built around a collared knit: Students&rsquo; Visalia and Carlsbad sweater polos, Walker&rsquo;s Outback jacquard and Loom Knit, and Sugarloaf&rsquo;s rugby, the same idea in sweatshirt terry. It sits between a polo and a sweater, which is exactly what a 60-degree morning in Austin asks for.</p>
    <p><strong>Texture beats tech.</strong> Almost none of it is shiny polyester. Students went with waffle knit, a diamond hex knit and crinkled nylon; Walker with speckled marl and cotton terry; Sugarloaf with a micro-grid fleece and French terry. The fabric does the work a big chest logo used to do.</p>
    <p><strong>Everyone made a jacket.</strong> Students made two in an oil-slick camo it says is based on a golf course pond, Walker made a check windbreaker, and Sugarloaf made a work jacket it admits was &ldquo;inspired by the ones we&rsquo;re seeing everywhere these days.&rdquo; Workwear and light nylon shells have taken over the walk from the car to the first tee.</p>
    <p><strong>Pine and oatmeal, with a contrast collar.</strong> Deep green runs through Students&rsquo; cardigan, track pants and Oso jacket and Walker&rsquo;s Featherlite polo and cap. Oat and cream turn up in Walker&rsquo;s Loom Knit, Sugarloaf&rsquo;s grid fleece and Students&rsquo; Carlsbad. And the collars keep coming in a second color: the Two-Tone polos, the rugby, the Vacation Terry.</p>
    <p>Below are twelve pieces from each brand, all added to the brand&rsquo;s own store in the last two weeks and in stock on October 13, 2026. Prices are in US dollars; Walker&rsquo;s are from its US store. If you only buy one from each: the Perris camo coat ($178), the Outback Knit Polo ($120) and the Grid Quarter-Zip in Nantucket red ($110).</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Three</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$35&ndash;$268</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>Walker Kooka, October 13</span></div>
      <div class="sidebar-detail"><span class="l">Loudest</span><span>Walker Outback Knit Polo</span></div>
      <div class="sidebar-detail"><span class="l">Warmest</span><span>Sugarloaf Grid Tech Hoody</span></div>
      <div class="sidebar-detail"><span class="l">Most expensive</span><span>Students Obispo, $268</span></div>
      <a href="#students" class="sidebar-cta">Start with Students &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#FallDrops</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#NewArrivals</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">The first wave: <a href="/drops/fall-drops-eastside-students-devereux">Three Fall Drops We Dig</a>. More from these brands: <a href="/drops/sugarloaf-autumn-layers-2026">Sugarloaf Autumn Layers</a> and <a href="/drops/walker-golf-the-par-tec-drop">Walker&rsquo;s Par-Tec drop</a>.</p>
</section>
"""
FAQ = [
 ("What are the golf fashion trends for fall 2026?", "Across Students, Walker Golf Things and Sugarloaf Social Club's fall 2026 drops: knit sweater polos, textured fabrics like waffle knit, terry and grid fleece instead of shiny polyester, light jackets and workwear, and a palette of pine green and oatmeal with contrast collars."),
 ("What is in Students Golf's Fall Drop 2?", "Students' second fall 2026 delivery went up September 30 to October 1. It includes the Obispo and Perris jackets in an oil-slick camo, knit sweater polos like the Visalia and Carlsbad, the Locke cardigan, the Viejo flannel and San Diego track pants, from $108 to $268."),
 ("What is Walker Golf Things' Kooka drop?", "Walker's October 2026 release, named for the kookaburra patch on most pieces. It includes the Outback jacquard knit polo, Kooka Two-Tone and Loom Knit polos, a check windbreaker, caps and tees, mostly $50 to $130 on Walker's US store."),
 ("What did Sugarloaf Social Club release in October 2026?", "A stretch work jacket, a French terry rugby, a grid-fleece quarter-zip and hoody in three colors, and needlepoint pieces made with Smathers & Branson, from $35 to $165."),
 ("Are these golf clothes in stock?", "Every piece here was in stock on its brand's own store on October 13, 2026, though some sizes are already gone, including several of Students' knits."),
]
HERO_ALT = "Three lookbook photos side by side: a model in Students' green camo Obispo jacket, a golfer in Walker's Outback knit polo with a stockmen and windmill jacquard, and a model in Sugarloaf's slate work jacket"
FRN = json.loads((ROOT / "research/fresh-fall/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-13", "dateModified": "2026-10-13",
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
    for s in SECTIONS: assert len(s[2]) == 12, s[0]
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
    <span>Three brands, twelve pieces each</span><span class="dot"></span>
    <span>36 picks &middot; in stock, checked October 13, 2026</span>
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
    for leak in ("Mackem", "Kalamunda", "Lehi", "Rookline", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram"):
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
