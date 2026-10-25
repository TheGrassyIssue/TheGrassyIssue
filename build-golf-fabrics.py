#!/usr/bin/env python3
"""build-golf-fabrics.py — Merino, Ripstop and Corduroy: a fabric guide with picks (24 October 2026). Cloned from build-new-drops-oct23.py.
Lenny: "a post that's a collection of three different fabrics Merino Wool, Ripstop and a third that is becoming popular. Research options
from our brands to feature then also explain the differences between those fabrics and the benefits." Then "build the post" (no picks
given; TGI picked 8 per fabric from fabrics-options.html, favouring golf brands, US stock and range of categories).
THIRD FABRIC: corduroy — the sweep of ~60 apparel brands (research/fabrics/sweep-*.json) found it at 19 brands, the widest spread.
LIVE DATA: research/fabrics/live.json (each product's .js, 24 Oct 2026). Currencies: Sounder, Casualist, Fyfe, Parmore GBP; Fella EUR;
Walker, Mackem AUD; rest USD. USD at GBP 1.3375, EUR 1.1201, AUD 0.7028 (open.er-api.com, 24 Oct 2026).
FABRIC FACTS: REI / Decathlon (merino microns, odour: reduces not eliminates); Wikipedia + ISHN (ripstop grid, WWII parachute nylon);
Wikipedia / So Sew Easy (corduroy cut pile, wales: standard 10-12, wide 8 or fewer, pinwale 16+). No "30% of its weight" claim (unverified).
Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Ripstop vs Merino vs Corduroy: Golf Fabrics Explained"
DESC = ("Ripstop, merino wool and corduroy, explained for golfers: what each fabric is, how they compare on warmth and weather, "
        "and 24 picks from independent brands.")
H1 = "Ripstop, Merino and Corduroy: The Three Fabrics Taking Over Golf"
BC = "Golf Fabrics Explained"
SLUG = "golf-fabrics-merino-ripstop-corduroy"
IMG = "/images/fabrics"
SHOP = ""
def g(x): return f"&pound;{x} (~${round(x*1.3375)})"
def e(x): return f"&euro;{x} (~${round(x*1.1201)})"
def a(x): return f"A${x} (~${round(x*0.7028)})"
P = {
 "M20": ("Olydoe", "Merino Aire Polo", "$125", "https://olydoe.com/products/merino-wool-polo",
   "A merino and Tencel blend core-spun around recycled nylon for durability, so it behaves like a performance polo with wool&rsquo;s odor control and a silky feel. The Dallas brand&rsquo;s whole pitch is the anti-polyester polo."),
 "M41": ("Whim Golf", "Merino Short Sleeve Golf Shirt, Mid-Weight", "$299", "https://whimgolf.com/products/merino-short-sleeve-golf-shirt-mid-weight-navy",
   "100% merino jersey at 6.5 ounces per yard, from RWS-certified sheep raised in the American West and made in the USA, with horn buttons. The purist&rsquo;s merino polo; stock is down to a small in navy."),
 "M51": ("Whim Golf", "Woven Merino Swing Jacket", "$499", "https://whimgolf.com/products/mens-woven-merino-swing-jacket",
   "A 100% woven merino jacket made in Connecticut from undyed wool, so every one has small natural flecks. RiRi zip, cinch hem and no elastic at the cuffs; the most unusual piece here."),
 "M11": ("Criquet", "Dan Merino Long Sleeve Polo", "$138", "https://criquetshirts.com/products/dan-merino-long-sleeve-polo-sage",
   "Austin&rsquo;s own: 60% merino and 40% Tencel, light and soft enough to wear alone or under a layer, with removable collar stays. Sage, plus two other colors."),
 "M10": ("Casualist", "Grazer Cardigan Vest", g(185), "https://casualist.com/products/grazer-cardigan-vest-grey",
   "A throwback button-front vest in 100% merino with a soft, vintage feel, an embroidered mascot on the chest and a caption across the back for whoever is walking behind you. Made in Portugal."),
 "M31": ("Students Golf", "Medinah Crew Knit Sweater", "$158", "https://studentsgolf.com/products/medinah-crew-knit-sweater-2",
   "100% merino in a traditional crew, with ribbed collar, cuffs and hem and the &ldquo;Chippy&rdquo; patch on the chest. The easy one to wear over a polo in November."),
 "M14": ("Fyfe", "Links Beanie", g(45), "https://www.fyfegolf.com/products/links-beanie-bone",
   "Superfine merino, spun, colored and finished in Scotland on the banks of Loch Leven. Light, warm and not itchy, which is the whole point of merino on your head."),
 "M37": ("Whim Golf", "Featherweight Merino Golf Sock", "$39", "https://whimgolf.com/products/featherweight-merino-golf-sock-1",
   "A merino-blend golf sock made in the USA, with minimal padding, a flat toe seam and Lycra for fit. The cheapest way to find out why golfers love merino."),
 "R44": ("Sounder", "Pac Mach Jacket", g(145), "https://soundergolf.com/products/pac-mach-jacket-deep-navy-ripstop",
   "Ultra-light Japanese recycled polyester ripstop, shower-resistant, that packs into its own drawstring bag small enough for a Sunday bag pocket. Deep navy; down to XS&ndash;M."),
 "R39": ("Sounder", "Drawcord Good Walk Chino", g(75) + " <s>&pound;145</s>", "https://soundergolf.com/products/drawcord-good-walk-chino-in-tan-ripstop",
   "Organic cotton ripstop with a little stretch, garment-dyed, with an elastic drawcord waist and a relaxed, tapered, cropped leg. Half price right now."),
 "R13": ("Devereux", "1703 Ripstop Cargo Short", "$74", "https://devereuxgolf.com/products/1703-ripstop-cargo-short-navy",
   "A light cargo short inspired by sailing gear, with the 1703 number down the leg. Marked final sale, so no returns."),
 "R51": ("Walker Golf Things", "Pitch Cargo Short", a(120), "https://walkergolfthings.com/products/pitch-cargo-short",
   "Stretch ripstop nylon with an elastic waist and belt loops, zipped side pockets, snap cargo pockets and two tee slots at the back. Built for a hot round."),
 "R8": ("Casualist", "Cart Path Ripstop Jacket", g(240), "https://casualist.com/products/cart-path-ripstop-jacket",
   "A light ripstop jacket with a ventilated back and an adjustable waist cord, for the course, the car park and the pub. Olive green."),
 "R20": ("Fella Golf", "Fella Ripstop Cargo Pant", e(120), "https://fellagolf.com/products/fella-ripstop-cargo-pant",
   "Light ripstop in a relaxed fit, with magnetic cargo pockets, a rope tee holder, Velcro belt loops to hold your glove while you putt and adjustable cuffs."),
 "R37": ("Parmore", "Ripstop Cotton 5-Panel", g(35), "https://parmoregolf.com/products/parmore-embroidered-5-panel",
   "A ripstop cotton-blend crown with the raised 3D-embroidered &ldquo;+&rdquo; on the front. The easy, cheap way into ripstop."),
 "R33": ("Hidden Links Society", "Dimple Ripstop Driver Cover", "$40", "https://hiddenlinkssociety.com/products/dimple-ripstop-driver-cover-black",
   "A black ripstop driver cover with a lining and the red Dimple patch. The one place ripstop&rsquo;s toughness really earns its keep: it lives in a bag."),
 "C16": ("Criquet", "Comfort Corduroy Pant", "$154", "https://criquetshirts.com/products/comfort-corduroy-pant-khaki",
   "The classic Criquet pant in a soft cord of cotton, Tencel and a little stretch, so it moves for a swing. Khaki or a second color, for cooler months."),
 "C7": ("ANTi COUNTRY CLUB TOKYO", "Corduroy Cargo Pants", "&yen;22,000 (~$140)", "https://anticountryclubtokyo.com/products/anti-country-club-corduroy-pants",
   "Thick-ribbed 100% cotton corduroy cut like cargo pants, from the Tokyo label that dresses golf like streetwear. Dark brown is down to a large; khaki and beige are listed too."),
 "C46": ("Sounder", "Clubhouse Five Pocket Cord", g(75) + " <s>&pound;135</s>", "https://soundergolf.com/products/clubhouse-5-pocket-cord-in-deep-navy",
   "A straight-leg 100% cotton corduroy five-pocket, garment-dyed deep navy, with silver rivets. Made in Portugal; on sale."),
 "C51": ("Students Golf", "Keith Big Wale Corduroy Cadet Jacket", "$100.80", "https://studentsgolf.com/products/keith-big-wale-corduroy-cadet-jacket",
   "A navy big-wale corduroy zip jacket with a cadet collar. Big wale means fat ridges, the warmest and most 70s version of the fabric."),
 "C20": ("Devereux", "Corduroy Short", "$58", "https://devereuxgolf.com/products/corduroy-short-brindle",
   "100% cotton wide-wale corduroy in a brindle brown, soft with a bit of structure. Shorts for a warm November in Texas."),
 "C44": ("Read The Green", "Founder&rsquo;s Cap", "$45", "https://readthegreen.com/products/founders-cap-the-reserve",
   "A 100% corduroy five-panel with a seamless front and the embroidered Read The Green logo. Six colors in the range."),
 "C53": ("Walker Golf Things", "Kooka Mid Box Cap, Cream Corduroy", a(60), "https://walkergolfthings.com/products/kooka-mid-box-cap-cream-corduroy",
   "A mid-profile snapback in 9-wale cotton cord with contrast stitching on the peak and the Kooka on the front."),
 "C38": ("Mackem Golf", "Killhope Headcover", a(85) + "&ndash;" + a(100), "https://mackemgolf.com/products/killhope",
   "A rust-colored corduroy headcover in driver, mini driver, fairway and hybrid sizes. Corduroy&rsquo;s easiest entry point: the bag, not the body."),
}
SECTIONS = [
 ("Ripstop: 8 Picks", "ripstop", ["R44","R39","R13","R51","R8","R20","R37","R33"],
  "<strong>8 pieces &middot; $40&ndash;$321</strong>A grid-reinforced weave, in nylon, polyester or cotton. Shells, pants, shorts, a cap and a driver cover."),
 ("Merino Wool: 8 Picks", "merino", ["M20","M41","M51","M11","M10","M31","M14","M37"],
  "<strong>8 pieces &middot; $39&ndash;$499</strong>Fine wool from merino sheep. Polos, knits, a jacket, a beanie and socks; several are merino blends with Tencel or nylon."),
 ("Corduroy: 8 Picks", "corduroy", ["C16","C7","C46","C51","C20","C44","C53","C38"],
  "<strong>8 pieces &middot; $42&ndash;$154</strong>The trend fabric: cut-pile cotton cords. Pants, a jacket, shorts, two caps and a headcover."),
]
N = 24
PQ = {}
BANDS = {
 "merino": ("Merino on the course. ", "Merino polos and knits from Olydoe, Criquet and Fyfe.",
   [("look-M20-1","A golfer in an Olydoe merino polo sitting in a golf cart","Merino Aire Polo &middot; Olydoe"),
    ("look-M11-1","A golfer in a sage Criquet merino long-sleeve polo","Dan Merino Polo &middot; Criquet"),
    ("look-M14-2","Hands holding a Fyfe merino beanie","Links Beanie &middot; Fyfe")]),
 "ripstop": ("Ripstop in motion. ", "Shorts and shells built to take a beating, from Devereux, Walker and Casualist.",
   [("look-R13-1","A golfer in Devereux navy ripstop cargo shorts","1703 Cargo Short &middot; Devereux"),
    ("look-R51-4","A golfer swinging in Walker black ripstop cargo shorts","Pitch Cargo Short &middot; Walker Golf Things"),
    ("look-R8-4","The back of a Casualist olive ripstop jacket","Cart Path Jacket &middot; Casualist")]),
 "corduroy": ("Corduroy, back for good. ", "Cords from Sounder, Students and Mackem.",
   [("look-C46-2","A golfer in Sounder navy corduroy five-pocket pants on a course","Clubhouse Cord &middot; Sounder"),
    ("look-C51-4","A model in a Students Golf navy big-wale corduroy jacket","Keith Cadet Jacket &middot; Students Golf"),
    ("look-C38-1","Rust corduroy Mackem headcovers on a wooden bench","Killhope &middot; Mackem Golf")]),
}
KIT_CSS = ""
TABLE = """
<div style="overflow-x:auto;margin:22px 0 6px"><table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.4">
<thead><tr style="border-bottom:1.5px solid #141414;text-align:left"><th style="padding:8px 6px"></th><th style="padding:8px 6px">Ripstop</th><th style="padding:8px 6px">Merino wool</th><th style="padding:8px 6px">Corduroy</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>What it is</strong></td><td style="padding:8px 6px">A weave, with a thicker reinforcing thread in a grid</td><td style="padding:8px 6px">A natural fiber: fine wool from merino sheep</td><td style="padding:8px 6px">A texture: cut-pile ridges, usually cotton</td></tr>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>Best for</strong></td><td style="padding:8px 6px">Shells, pants, shorts, caps</td><td style="padding:8px 6px">Polos, base layers, knits, socks</td><td style="padding:8px 6px">Pants, jackets, caps, headcovers</td></tr>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>Warmth</strong></td><td style="padding:8px 6px">Low on its own; blocks wind</td><td style="padding:8px 6px">Warm for its weight; regulates in heat too</td><td style="padding:8px 6px">Warm, especially wide wale</td></tr>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>Weather</strong></td><td style="padding:8px 6px">Often wind- and shower-resistant</td><td style="padding:8px 6px">Handles sweat well; not waterproof</td><td style="padding:8px 6px">Dry days only; soaks up rain</td></tr>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>Durability</strong></td><td style="padding:8px 6px">The toughest: tears stop at the grid</td><td style="padding:8px 6px">Good in blends; pure merino needs care</td><td style="padding:8px 6px">Sturdy; ridges wear smooth over years</td></tr>
<tr style="border-bottom:1px solid rgba(20,20,20,.15)"><td style="padding:8px 6px"><strong>Odor</strong></td><td style="padding:8px 6px">Depends on the fiber; synthetics hold odor</td><td style="padding:8px 6px">Resists it; can go a few rounds between washes</td><td style="padding:8px 6px">Like any cotton: wash after a sweaty round</td></tr>
<tr><td style="padding:8px 6px"><strong>Care</strong></td><td style="padding:8px 6px">Machine wash, low or no heat</td><td style="padding:8px 6px">Cool wash, lay flat to dry</td><td style="padding:8px 6px">Wash inside out, cool</td></tr>
</tbody></table></div>
<p style="font-size:12px;opacity:.7">Care is general guidance; always follow the label on the piece.</p>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>Three fabrics keep showing up across the independent golf brands we cover. Ripstop, the grid-woven fabric from military gear, is in every cargo short and packable shell. Merino wool has gone from ski base layers to golf polos. And corduroy, which we expected to be a niche fall thing, turned up at 19 of the roughly 60 apparel brands in our index that sell clothing, more than any other fabric on the rise.</p>
    <p>They do very different jobs, so here is what each one actually is, what it is good at on a golf course, and eight picks for each from brands in our Brand Index. Prices were checked on each brand&rsquo;s own store on October 24, 2026.</p>
    <p><strong>Ripstop</strong> isn&rsquo;t a fiber at all; it is a way of weaving. Every so often a thicker reinforcing thread is woven in, in both directions, making a little grid you can see on the fabric. If something snags, the tear runs to the next line of the grid and stops. It took off during World War II, when nylon replaced silk for parachutes, and it is now made in nylon, polyester and cotton. On the course that means light pants and shorts that survive fence lines and bag straps, and shells that block wind and shrug off a shower.</p>
    <p><strong>Merino wool</strong> is fine wool from merino sheep. The fibers are much thinner than regular wool (typically under about 22 microns, versus 30-plus for standard wool), which is why it feels soft instead of scratchy. It is warm for its weight, breathes, and handles sweat well, and it resists odor: wool holds odor molecules until it is washed, so a merino polo can usually go another round before it hits the laundry. It reduces smell; it does not make it disappear. Many golf merino pieces are blends with Tencel or nylon for a smoother feel and more durability.</p>
    <p><strong>Corduroy</strong> is a texture: extra threads woven over a base fabric, then cut and brushed up into raised ridges called wales. The fewer wales per inch, the fatter the ridges. Standard corduroy is about 10 to 12 wales per inch, wide or &ldquo;big&rdquo; wale is 8 or fewer, and pinwale is finer, at 16 or more. It is warm, soft, and very 70s, which is a big part of why golf brands love it right now. The catch: it is a dry-day fabric, because cotton cord soaks up rain.</p>
    <h2 class="products-hdr" id="compare" style="margin-top:28px">How They Compare</h2>
""" + TABLE + """
    <p><strong>How to wear them together.</strong> They layer well: a merino polo underneath, corduroy pants or a cord cap for warmth and character on a cold, dry morning, and a packable ripstop shell in the bag in case the weather turns. If you only buy one piece, start with merino: it is the fabric you will feel the difference in on the very first round.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Short Version</div>
      <div class="sidebar-detail"><span class="l">Ripstop</span><span>Light, tough, sheds wind</span></div>
      <div class="sidebar-detail"><span class="l">Merino</span><span>Soft, warm, resists odor</span></div>
      <div class="sidebar-detail"><span class="l">Corduroy</span><span>Warm, soft, dry days</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>24 from 15 brands</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 24, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#Ripstop</span>
        <span class="hashtag">#Merino</span>
        <span class="hashtag">#Corduroy</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
KIT = ""
LOOKBOOK = ""
FAQ = [
 ("What is the difference between merino wool, ripstop and corduroy?", "Merino is a natural fiber (fine wool from merino sheep), ripstop is a weave with a reinforcing grid that stops tears, and corduroy is a texture of cut-pile ridges, usually in cotton. Merino is best for polos and knits, ripstop for shells, pants and shorts, and corduroy for pants, jackets and caps."),
 ("Is merino wool good for golf?", "Yes, for most golfers: it is soft, warm for its weight, breathable, handles sweat well and resists odor, so a merino polo can usually go more than one round between washes. Many golf pieces blend merino with Tencel or nylon for durability."),
 ("What is ripstop fabric?", "A fabric woven with thicker reinforcing threads at regular intervals in both directions, forming a grid. A tear stops when it reaches the next reinforcing thread. It is made in nylon, polyester and cotton and is common in golf shells, cargo shorts and pants."),
 ("What does wale mean in corduroy?", "Wale is the number of ridges per inch. Standard corduroy is about 10 to 12 wales per inch, wide or big wale is 8 or fewer, and pinwale is 16 or more. Fewer wales means wider, warmer ridges."),
 ("Can you play golf in corduroy?", "Yes, on dry days. Cotton corduroy is warm and comfortable, and stretch versions move well in a swing, but it absorbs water, so pack a ripstop shell if rain is possible."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
_FR = json.loads((ROOT / "research/fabrics/frames.json").read_text())
FRN = {k: [f"{IMG}/{f}" for f in _FR[k]] for k in P}
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
         "url": URL, "image": og, "datePublished": "2026-10-24", "dateModified": "2026-10-24",
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
    <span>The Grassy Issue &middot; The Guide</span><span class="dot"></span>
    <span>24 pieces &middot; prices checked October 24, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Golfers in ripstop shorts, a merino polo and corduroy pants, each with a fabric swatch" fetchpriority="high" /></div></div>
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
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Kalamunda", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Climber", "Woodgrain", "Bethpage", "LBB", "GolfPass"):
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
