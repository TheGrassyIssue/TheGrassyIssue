#!/usr/bin/env python3
"""build-pullovers.py — The Pullover Edit: 20 new + 5 vintage. Cloned from build-hat-makers.py. 27 October 2026.
Lenny: "let's do a post of Pullovers, the perfect layer for fall. Let's add a few vintage options from resellers"; half/quarter-zips,
wind pullovers and V-necks; 20 new + 5 vintage; "Nothing with Hoods, make sure all images look crisp and clean. swap out v15 with v14".
FACTS: each store's own product JSON (research/pullovers/new.json) and live resale listings (vintage.json), read 27 Oct 2026.
Skips brands from this week's posts and the seven held for the quiet luxury post.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Pullover Edit: 25 Quarter-Zips, Windshirts and V-Necks for Fall Golf"
DESC = ("The best golf pullovers for fall: 20 new quarter-zips, windshirts and V-necks from independent brands, "
        "plus 5 vintage finds from resellers, Tiger-era Nike to the Masters. All with prices.")
H1 = "The Pullover Edit: The Perfect Layer for Fall"
BC = "The Pullover Edit"
SLUG = "golf-pullovers-fall-layer"
IMG = "/images/pullovers"
SHOP = ""
P = {
 # quarter-zips and half-zips
 "n1": ("Students", "Giovant Knit Q-Zip Sweater", "$145", "https://studentsgolf.com/products/giovant-knit-q-zip-sweater",
   "A thin-gauge, fully fashioned knit in 100% cotton with a felt Students appliqu&eacute; across the front. A sweater cut close enough to swing in."),
 "n10": ("Eastside Golf", "Retro Quarter Zip Sweatshirt", "$88", "https://eastsidegolf.com/products/el2070601-036-smoke-grey-retro-quarter-zip-sweatshirt",
   "Soft French terry with a vintage-style wash, a relaxed fit and a small Swingman on the chest. The one to throw over anything."),
 "n15": ("Sugarloaf Social Club", "Grid Quarter-Zip", "$110", "https://www.sugarloafsocialclub.com/products/grid-quarter-zip",
   "Sugarloaf&rsquo;s classic quarter-zip in a stretchy micro-grid fleece. The brand compares it to a mountaineering base layer, warm but breathable."),
 "n18": ("Devereux", "Sandy Lane Pullover", "$128", "https://devereuxgolf.com/products/sandy-lane-pullover-red",
   "A fleece pullover inspired by yacht-club styling, in red with Devereux&rsquo;s checker pattern across the chest. The loudest layer in the post."),
 "n22": ("Criquet", "Waffle Stretch Pullover", "$168", "https://criquetshirts.com/products/waffle-stretch-pullover-teak",
   "Criquet&rsquo;s newest quarter-zip, in a light waffle stretch. Over a polo for the round, over a tee for the weekend."),
 "n32": ("Dual Sport", "Shiver Quarter Zip", "$78", "https://dualsportbrand.com/products/shiver-quarter-zip-mist",
   "Stretch performance nylon with a contrast forearm and a relaxed, true-to-size fit. The cheapest new piece here."),
 "n34": ("Public Drip", "Herringbone Half Zip", "$140", "https://publicdrip.com/products/the-herringbone-half-zip-coffee",
   "A soft cotton-blend knit in a herringbone weave, in coffee. Textured enough to look good on its own."),
 "n35": ("Birds of Condor", "Rage Cord Quarter Zip", "$120", "https://us.birdsofcondor.com/products/black-birds-rage-corduroy-quarter-zip-golf-jacket",
   "Black 100% cotton corduroy with a tonal zip, side pockets and the Birds script on the chest."),
 "n42": ("Macade", "Bridge Merino Quarter Zip", "$195", "https://macadegolf.com/products/bridge-brown-merino-quarter-zip",
   "A merino wool and cashmere blend, light and soft, with a clean, tailored fit and a little stretch. Our pick of the knits."),
 "n49": ("Bunker Mentality", "Augusta Organic Cotton Quarter Zip", "$113", "https://bunker-mentality.com/products/augusta-organic-cotton-1-4-zip-green",
   "Organic cotton fleece, soft and warm, with enough structure to hold its shape. In Augusta green, naturally."),
 "n53": ("Fella", "Boris Quarter-Zip Sweater", "$170", "https://fellagolf.com/products/boris-quarter-zip-sweater-navy",
   "A heavyweight knit with a cream body and a navy chest stripe, re-cut this season with an improved fit."),
 "n58": ("Juniper &amp; James", "Quiver Quarter Zip", "$149", "https://juniperjamesgolf.com/products/quiver-quarter-zip-pullover-gulf-stream-blue",
   "A silky Tencel Lyocell blend from Lenzing, made to go from the course to dinner or the office."),
 # wind pullovers
 "n5": ("Malbon", "Links Windshirt", "$168", "https://malbon.com/products/links-windshirt-forest",
   "A lightweight short-sleeve windshirt with an elastic waist and Malbon embroidery, built to wear year round. Throw it over a long-sleeve polo."),
 "n23": ("Parmore", "Capsule Windbreaker", "$120", "https://parmoregolf.com/products/long-sleeved-windbreaker-rebrand",
   "A khaki-stone wind layer with cream ribbed collar, cuffs and hem and a small white cross on the chest."),
 "n31": ("Mount Tee", "Links Nylon Quarter Zip", "A$130", "https://mountteegolf.com.au/products/nylon-quarter-zip",
   "100% nylon ripstop with a mesh lining, side-seam zip pockets and elasticated cuffs and waist. Priced in Australian dollars."),
 "n38": ("Walker", "All Weather Pullover", "$110", "https://www.walkergolfthings.com/products/all-weather-pullover-1",
   "A technical, weather-ready pullover in a midnight check, cut to move. The most interesting pattern here."),
 "n46": ("Read the Green", "&rsquo;97 Vintage Pullover", "$100", "https://readthegreen.com/products/the-97-vintage-pullover",
   "100% nylon with rib-knit collar and cuffs, a drawstring hem and &ldquo;Read The Green Golf Club 1997&rdquo; on the chest. New, made to look old."),
 "n57": ("Siegelman Stable", "x Maxfli Pull Over Jacket", "$298", "https://siegelmanstable.com/products/retro-track-jacket-2",
   "Charcoal and green tech poplin lined in athletic mesh, with Maxfli and Siegelman embroidery. The most expensive piece here."),
 # V-necks
 "n26": ("Ashworth", "Aeroflex V-Neck Pullover", "$165", "https://www.ashworth-golf.com/products/aeroflex-v-neck-golfman-pullover-ag-khaki",
   "Ashworth&rsquo;s classic V-neck redone in a four-way-stretch soft shell with a water-repellent finish."),
 "n27": ("Ashworth", "Fully Fashioned V-Neck Sweater", "$265", "https://www.ashworth-golf.com/products/fully-fashioned-v-neck-sweater-golfman-velvet",
   "12-gauge superwash wool with a ribbed V and contrast-trimmed cuffs. The proper golf sweater."),
 # vintage
 "v8": ("Augusta National Golf Shop", "90s V-Neck Sweater", "$40 + shipping &middot; eBay &middot; L", "https://www.ebay.com/itm/327404102171",
   "A cream acrylic V-neck from the Augusta National golf shop, with the Masters logo on the chest. Pre-owned, in good condition."),
 "v4": ("Ashworth", "2002 U.S. Open Quarter-Zip", "$35 + shipping &middot; eBay &middot; L", "https://www.ebay.com/itm/407212076836",
   "A green quarter-zip windbreaker from the 2002 U.S. Open at Bethpage Black, new without tags. The best deal in the post."),
 "v2": ("Nike Golf", "Tiger Woods 90s Quarter-Zip", "$69 + shipping &middot; eBay &middot; L", "https://www.ebay.com/itm/318660835011",
   "A blue Nike FIT quarter-zip from the Tiger Woods collection, with the white chest panel that dates it."),
 "v12": ("ProQuip", "1997 Ryder Cup Windshirt", "$40 + shipping &middot; eBay &middot; XL", "https://www.ebay.com/itm/128086680290",
   "A plaid windshirt from the 1997 Ryder Cup at Valderrama, the first one played in continental Europe. Size XL."),
 "v14": ("Masters Collection", "90s Microfiber Pullover", "$240 &middot; Etsy &middot; XL", "https://www.etsy.com/listing/4595016160/nwt-90s00s-vintage-masters-collection",
   "A green microfiber pullover from Augusta National&rsquo;s Masters Collection, still new with tags. Size XL."),
}
SECTIONS = [
 ("Quarter-Zips &amp; Half-Zips", "quarter-zips", ["n42","n1","n53","n34","n22","n15","n18","n35","n58","n49","n10","n32"],
  "<strong>Twelve picks &middot; $78&ndash;$195</strong>The workhorse of fall golf. Knits, fleece, cord and terry, all with a short zip so you can open it up on the back nine when the sun comes out."),
 ("Wind Pullovers", "wind-pullovers", ["n57","n23","n46","n38","n31","n5"],
  "<strong>Six picks &middot; $100&ndash;$298</strong>The &rsquo;90s tour layer is back. Light, packable shells for wind and drizzle, most with a rib-knit or elastic hem."),
 ("V-Necks", "v-necks", ["n27","n26"],
  "<strong>Two picks from Ashworth</strong>The original golf sweater, from the brand that defined the &rsquo;90s version of it."),
 ("Vintage, From Resellers", "vintage", ["v8","v4","v2","v12","v14"],
  "<strong>Five finds &middot; $35&ndash;$240</strong>One-off pieces live on eBay and Etsy when we checked on October 27. They will not last, so check the listing before you fall for one."),
]
N = 25
PQ = {}
BANDS = {
 "quarter-zips": ("The Lookbook", "Quarter-zips at golden hour, by the clubhouse and in the woods.", [
   ("look-juniper-james-1", "A golfer in a light-blue Juniper &amp; James performance quarter-zip on a course at golden hour", "Juniper &amp; James"),
   ("look-macade-3", "A golfer in a grey Macade cable-knit quarter-zip holding an iron in front of a stone clubhouse", "Macade"),
   ("look-criquet-1", "A man in a teal Criquet fleece half-zip in a forest", "Criquet")]),
 "wind-pullovers": ("The Lookbook", "Windshirts on links greens and parkland fairways.", [
   ("look-read-the-green-2", "A golfer in a green Read the Green quarter-zip windshirt at the finish of a swing", "Read the Green"),
   ("look-sugarloaf-social-club-1", "A golfer in a mint Sugarloaf windshirt lining up a putt on a links green beside dunes", "Sugarloaf Social Club"),
   ("look-mount-tee-golf-1", "A golfer in a cream Mount Tee nylon pullover walking off a green with a carry bag", "Mount Tee")]),
 "v-necks": ("The Lookbook", "Plaid, tipped trim and a full swing.", [
   ("look-walker-golf-things-1", "A golfer in a plaid Walker windshirt on a sunlit course", "Walker"),
   ("look-macade-1", "A golfer in a heather-tan Macade quarter-zip with varsity trim, iron in hand", "Macade"),
   ("look-juniper-james-3", "A golfer in a pale-blue Juniper &amp; James quarter-zip at the finish of an iron swing", "Juniper &amp; James")]),
 "vintage": ("More From the Lookbook", "Parkland, pubs, desert courses and fairways.", [
   ("look-mount-tee-golf-2", "A golfer in a black Mount Tee tipped-collar quarter-zip on a parkland course beside a green bag", "Mount Tee"),
   ("look-juniper-james-2", "A golfer in a maroon Juniper &amp; James quarter-zip addressing the ball", "Juniper &amp; James"),
   ("look-walker-golf-things-3", "A man in a brown space-dye Walker knit quarter-zip in a pub", "Walker"),
   ("look-devereux-golf-1", "A man in a brown checkerboard Devereux knit on a desert golf course", "Devereux"),
   ("look-read-the-green-3", "A golfer in a navy piped Read the Green half-zip windshirt on a fairway", "Read the Green"),
   ("look-sugarloaf-social-club-3", "A man in an oatmeal Sugarloaf waffle-knit quarter-zip indoors", "Sugarloaf Social Club")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Fall golf starts cold and ends warm. The first tee is 48 degrees, the turn is 70, and whatever you put on at 8am has to make sense at noon. That is why the pullover is the most useful thing in a golf closet from October to December: it goes over a polo, comes off in one move, and a short zip lets you vent it without stopping to take it off.</p>
    <p>It is also the one layer that has stayed honest to golf. A full-zip jacket flaps, a hoodie fights your backswing, and a puffer belongs in the cart. A good pullover sits flat across the shoulders, stays put at the waist and looks right walking into the clubhouse afterward. None of the 25 picks here has a hood, on purpose.</p>
    <h2 class="products-hdr btk-story-hdr">The Three Families</h2>
    <p><strong>Quarter-zips and half-zips</strong> are the everyday layer, and they come in every weight. A thin cotton knit, like the Students Giovant or Fella&rsquo;s Boris, is a sweater you can swing in. Fleece, like Bunker Mentality&rsquo;s organic cotton Augusta or Sugarloaf&rsquo;s micro-grid, is for the cold first hour. Merino and cashmere, in Macade&rsquo;s Bridge, is the warmest for its weight and the one that looks best at dinner. Cord and terry, from Birds of Condor and Eastside, are the casual end.</p>
    <p><strong>Wind pullovers</strong> are the &rsquo;90s tour look that independent brands have brought back: light woven shells, usually nylon, with rib-knit or elastic hems that keep the wind out. They pack into a bag pocket and come out when the breeze picks up on the back nine. Read the Green&rsquo;s &rsquo;97 Pullover and Parmore&rsquo;s Capsule Windbreaker are the cleanest versions; Siegelman Stable&rsquo;s Maxfli collab is the most technical.</p>
    <p><strong>V-necks</strong> are the original golf sweater, and still the neatest thing you can wear over a collared shirt. Ashworth, the brand that defined golf clothes in the &rsquo;90s, makes both of ours: a fully fashioned wool one and a modern stretch shell that shrugs off light rain.</p>
    <h2 class="products-hdr btk-story-hdr">What to Look For</h2>
    <p>Room through the shoulders and upper back, so the pullover moves with your turn instead of pulling. A hem that sits at or just below the belt, so it doesn&rsquo;t ride up at the top of the swing. A zip long enough to vent properly, and cuffs that stay pushed up. And a weight that matches your mornings: knit or windshirt for a mild fall, fleece or merino when the frost delays start.</p>
    <h2 class="products-hdr btk-story-hdr">How to Wear It</h2>
    <p>Over a polo with the collar out, with pleated trousers or cords. Keep the pullover the boldest thing you&rsquo;re wearing, or the quietest, but not somewhere in between. A plain knit lets a loud polo work; Devereux&rsquo;s checker or Walker&rsquo;s check wants a plain shirt and trousers underneath.</p>
    <h2 class="products-hdr btk-story-hdr">Why Vintage</h2>
    <p>Some of the best golf pullovers were made 25 years ago, and they turn up on eBay and Etsy for less than a new one. Tournament pieces are the ones to look for: a 2002 U.S. Open quarter-zip from Bethpage, a 1997 Ryder Cup windshirt from Valderrama, an Augusta National V-neck. Vintage sizing runs big, so check the measurements before you buy, and move quickly, because each one is a one-off.</p>
    <h2 class="products-hdr btk-story-hdr">How We Picked</h2>
    <p>Every new piece was in stock on the brand&rsquo;s own store when we checked on October 27, 2026, one per brand except Ashworth, which gets two for the V-necks. The vintage listings were live and buyable the same day.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">New</span><span>20 pieces, 19 brands</span></div>
      <div class="sidebar-detail"><span class="l">Vintage</span><span>5 resale finds</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$35&ndash;$298</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Macade Bridge Merino, Ashworth V-Neck, 2002 U.S. Open Quarter-Zip</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>27 October 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfPullover</span>
        <span class="hashtag">#QuarterZip</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#VintageGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is the best golf pullover for fall?", "A quarter-zip in a knit or light fleece is the most versatile: it layers over a polo, vents with the zip and comes off easily. Our pick is the Macade Bridge Merino Quarter Zip, a merino and cashmere blend, at $195 when we checked."),
 ("What is the difference between a quarter-zip and a windshirt?", "A quarter-zip is usually a knit or fleece mid-layer for warmth. A windshirt, or wind pullover, is a light woven shell, often nylon, that blocks wind and light rain and packs small."),
 ("Can you wear a hoodie to play golf?", "Plenty of courses allow it, but a hood gets in the way of a full swing and many clubs' dress codes rule it out. None of the pullovers in this post has a hood."),
 ("Where can I buy vintage golf pullovers?", "eBay, Etsy, Grailed and Depop all carry them. Search for tournament or club names, like the U.S. Open or Augusta National, or for older brand names such as Ashworth, Nike Golf and Polo Golf, and check measurements before you buy."),
 ("How much does a good golf quarter-zip cost?", "The new pullovers in this post ran from $78 to $298 on October 27, 2026, with most between $110 and $170. Vintage pieces started at $35."),
]
FRN = json.loads((ROOT / "research/pullovers/frames.json").read_text())
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
    <span>20 new &middot; 5 vintage</span><span class="dot"></span>
    <span>Prices checked October 27, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer in a red Devereux Sandy Lane pullover on coastal rocks, a man in a cream Fella Boris quarter-zip with a navy stripe, and a golfer mid-swing in a blue Juniper &amp; James quarter-zip" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
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
    for leak in ("Mackem", "Kalamunda", "Three Putt", "Tarraing", "Rebolf", "Woodgrain", "LBB", "GolfPass"):
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
