#!/usr/bin/env python3
"""build-fresh-three.py — Three fresh golf brands: Pierre, Pluto Golf, Bordé Golf. Cloned from build-radar-three-5.py. 16 November 2026.
Lenny: "three fresh brand round up" (pierre.golf, pluto.golf, studiograin.store). Studio Grain was covered on Oct 29 (swell-marks post), so Lenny
chose Bordé Golf as the substitute. Options sheet (44) approved: "looks great, let's build it" (picks ours: Pierre all 7 listings, Pluto 12, Bordé all 11 (Lenny: more Pierre, more variety from Bordé — split colors into their own cards)).
FACTS: Pierre — Stupid Dope (Nov 14, 2026) and Hypebeast: artistic director Vincent Tsang (Dime's artistic director); designed in Montreal, made in
Japan; "true luxury is felt before it is seen". No founder named: don't add one. US prices from Pierre's own US storefront (polo $293, trousers $408,
jacket $480, cap $97 — read on the US shop page in Chrome).
Pluto — its About Us page (quotes below); Stupid Dope (Mar 2025): Indianapolis, launched March 18, 2024, self-funded, P1 sold out six times.
Co-founders Quentin Purtee and Leen Dhillon per LinkedIn. The $28M raise is unverified: leave it out. LIV Golf capsule left out.
Bordé — its own "The Brand" page; Three Putt Golf's new-brands guide: St Albans, selling since early 2025, founders Euan and Bec (first names only).
Prices in GBP with approximate USD (0.752). No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Three Fresh Golf Brands: Pierre, Pluto Golf and Bord\u00e9 Golf"
DESC = ("Three new golf brands to know: Pierre's silk golf clothes from Montreal, Pluto Golf's sneakers and streetwear from Indianapolis, "
        "and Bord\u00e9 Golf's tailored polos from St Albans. 30 picks with prices.")
H1 = "Three Fresh Golf Brands: Pierre, Pluto Golf and Bord\u00e9 Golf"
BC = "Pierre, Pluto Golf, Bord\u00e9 Golf"
SLUG = "pierre-pluto-borde-golf-brands"
IMG = "/images/fresh-three"
SHOP = ""
PI, PL, BO = "Pierre", "Pluto Golf", "Bord&eacute; Golf"
PIU, PLU, BOU = "https://pierre.golf/products/", "https://www.pluto.golf/products/", "https://bordegolf.co.uk/products/"
P = {
 # Pierre
 "pi-jacket-b": (PI, "Nylon Silk Quarter Zip Jacket, Brown", "$480", PIU+"asd3",
   "Our pick from Pierre. A loose quarter-zip in a nylon and silk blend, with elastic at the hem and cuffs. The brown is the one from the campaign, worn by the water, and the clearest version of what Pierre is doing."),
 "pi-jacket-g": (PI, "Nylon Silk Quarter Zip Jacket, Gray", "$480", PIU+"asd3-gray",
   "The same quarter-zip in gray, with a slight sheen from the silk. It is the cooler, quieter of the two."),
 "pi-pants-g": (PI, "Nylon Silk Pleated Trousers, Gray", "$408", PIU+"pants",
   "Pleated trousers in the same nylon and silk, with an elastic waist and a tapered leg. The campaign pairs the gray with the cream polo."),
 "pi-pants-b": (PI, "Nylon Silk Pleated Trousers, Brown", "$408", PIU+"pants-brown",
   "The trousers in brown. Wear them with the brown jacket and it is a suit you can play in."),
 "pi-polo-c": (PI, "Cotton Silk S/S Polo, Cream", "$293", PIU+"short-sleeve-knit-polo-copy",
   "A short-sleeve knit polo in cotton and silk, with a ribbed hem and a green woven label at the collar. The cream is the softest thing in the shop."),
 "pi-polo-b": (PI, "Cotton Silk S/S Polo, Brown", "$293", PIU+"short-sleeve-knit-polo-brown",
   "The same knit polo in a deep brown. It matches the jacket, the trousers and the cap."),
 "pi-cap": (PI, "Nylon Silk Cap", "$97", PIU+"silk-nylon-baseball-cap",
   "A soft six-panel cap in brown nylon and silk with the white Pierre P on the front. The easiest way into the brand."),
 # Pluto
 "pl-moss": (PL, "Pluto 1 Sneaker, Moss", "$159", PLU+"pluto-1-moss",
   "Our pick from Pluto. The spikeless golf sneaker the brand was built on, in leather and suede, moss green on a brown sole. Pluto calls it the most comfortable shoe in golf, and suggests going up half a size."),
 "pl-camo": (PL, "Pluto 1 Sneaker, OG Camo", "$159", PLU+"pluto-1-og-camo",
   "The same Pluto 1 in cream with camo panels. There are more than a dozen colors; this and the Moss are our two favorites."),
 "pl-target": (PL, "PlutoDry Target Jacket, Olive", "$179", PLU+"plutodry-generals-jacket-olive",
   "A hooded rain jacket from PlutoDry, the brand&rsquo;s own waterproof line, which it says is &ldquo;priced for the people.&rdquo; Olive with curved green panels."),
 "pl-block": (PL, "PlutoDry Block Jacket, Green", "$159", PLU+"plutodry-block-jacket-green",
   "A green PlutoDry track-style shell with a big chevron across the chest. It looks more like a sideline jacket than a rain jacket, which is the point."),
 "pl-church": (PL, "Church Polo, Fish-Scale", "$84", PLU+"church-polo-fish-scale",
   "The loudest thing in this post: a rainbow fish-scale print with hidden shamrock buttons, cut and sewn from scratch. As Pluto puts it, &ldquo;this ain&rsquo;t no printed blank.&rdquo;"),
 "pl-sunday": (PL, "Sunday Polo, Tiffany", "$84", PLU+"sunday-polo-tiffany",
   "A slightly boxy cotton-blend polo in pale blue with a tan collar and shamrock buttons. The easiest Pluto piece to wear on a normal Sunday."),
 "pl-vest": (PL, "Tri-Tone Vest, Bermuda", "$99", PLU+"tri-tone-vest-bermuda",
   "Three greens stacked: a puffer middle with smooth panels top and bottom, and hidden zip pockets. Layer it over a polo or a hoodie."),
 "pl-candle": (PL, "Candle Quarter-Zip, Aqua", "$114", PLU+"candle-quarter-zip-turquoise",
   "A slim stretch quarter-zip with mesh side panels and white piping that curves across the chest. Bright, light and made to play in."),
 "pl-road": (PL, "Road Pants, Olive", "$144", PLU+"road-pants-olive",
   "Straight-leg, button-fly pants with snap cargo pockets and a hidden zip pocket for tees and balls. Neither baggy nor skinny."),
 "pl-diamond": (PL, "Leather Diamond Cap, Emerald", "$54", PLU+"leather-diamond-cap-emerald",
   "A six-panel cap with a quilted leather crown and a suede brim, made, Pluto says, with the same attention as its shoes."),
 "pl-astro": (PL, "Astro Canvas Cap, Ice Blue", "$44", PLU+"astro-canvas-cap-ice-blue",
   "An unstructured cotton strapback with the P logo on the front and small hits of blue and red."),
 "pl-floater": (PL, "Boy Pluto Floater Ball Marker", "$29", PLU+"boy-pluto-floater-ball-barker-silver",
   "Boy Pluto, the brand&rsquo;s mascot, as a black and platinum ball marker. &ldquo;You asked, we delivered,&rdquo; says the listing."),
 # Bordé
 "bo-edge-b": (BO, "Edge Polo, Black", "&pound;80 (about $106)", BOU+"edge-polo-quarter-zip",
   "Our pick from Bord&eacute;. A zip-neck polo with white tipping on the collar and sleeves and a small crest on the back. Minimal branding, a fitted cut and a lot of quiet confidence."),
 "bo-edge-w": (BO, "Edge Polo, Pure White", "&pound;80 (about $106)", BOU+"borde-golf-edge-polo-pure-white",
   "The same Edge Polo in white with black tipping. The cleanest polo in this post."),
 "bo-contour-t": (BO, "Contour Polo, Tea Green", "&pound;80 (about $106)", BOU+"contour-polo-tea-green",
   "A zipped polo in soft pique with a little stretch, in a pale green. Made for spring or a warm-weather trip."),
 "bo-contour-b": (BO, "Contour Polo, Dusty Blue", "&pound;80 (about $106)", BOU+"contour-polo",
   "The Contour in a pale blue. With white trousers it is the brand&rsquo;s summer look."),
 "bo-verge-g": (BO, "Verge Midlayer, Mist Grey", "&pound;90 (about $120)", BOU+"verge-half-zip-cool-grey",
   "A fitted half-zip in soft-touch Portuguese fabric, in a pale gray. The layer you leave on all round."),
 "bo-verge-b": (BO, "Verge Midlayer, Serene Blue", "&pound;90 (about $120)", BOU+"verge-half-zip",
   "The Verge in navy blue, with a small crest on the back. Pairs with the Vantage Cap in either color."),
 "bo-brisa": (BO, "Brisa Windbreaker", "&pound;110 (about $146)", BOU+"brisa-windbreaker",
   "A short-sleeve windbreaker in navy with white piping. Wear it over a long-sleeve layer on a cold, windy morning and your arms stay free to swing."),
 "bo-crest-g": (BO, "Crest Cap, Cool Grey", "&pound;40 (about $53)", BOU+"borde-golf-crest-cap-soft-grey",
   "A structured cap with a tone-on-tone crest, in an off-white gray. Bord&eacute; says each cap is a limited run that will not come back."),
 "bo-crest-b": (BO, "Crest Cap, Serene Blue", "&pound;40 (about $53)", BOU+"everyday-cap",
   "The Crest Cap in navy, with the crest stitched in the same color."),
 "bo-vantage-b": (BO, "Vantage Cap, Black", "&pound;40 (about $53)", BOU+"vantage-cap-black",
   "A brushed twill cap with a small side badge. Pair it with the black Edge Polo."),
 "bo-vantage-w": (BO, "Vantage Cap, Pure White", "&pound;40 (about $53)", BOU+"vantage-cap-pure-white",
   "The Vantage in white, for the navy Verge or the black Edge."),
}
SECTIONS = [
 ("Pierre", "pierre", ["pi-jacket-b","pi-jacket-g","pi-pants-g","pi-pants-b","pi-polo-c","pi-polo-b","pi-cap"],
  "<strong>Montreal &middot; seven picks &middot; $97&ndash;$480</strong>The whole shop: a jacket, trousers and a polo in silk blends, each in two colors, plus a cap. Made in Japan. Prices from Pierre&rsquo;s US store."),
 ("Pluto Golf", "pluto-golf", ["pl-moss","pl-camo","pl-target","pl-block","pl-church","pl-sunday","pl-vest","pl-candle","pl-road","pl-diamond","pl-astro","pl-floater"],
  "<strong>Indianapolis &middot; 12 picks &middot; $29&ndash;$179</strong>Sneakers first, then everything around them: rain jackets, polos, layers, caps and a ball marker."),
 ("Bord&eacute; Golf", "borde-golf", ["bo-edge-b","bo-edge-w","bo-contour-t","bo-contour-b","bo-verge-g","bo-verge-b","bo-brisa","bo-crest-g","bo-crest-b","bo-vantage-b","bo-vantage-w"],
  "<strong>St Albans, UK &middot; 11 picks &middot; &pound;40&ndash;&pound;110</strong>The whole line-up, every color: two polos, a midlayer, a windbreaker and two caps, each in a short run. Prices in pounds."),
]
N = 30
PQ = {
 "pierre": ("True luxury is felt before it is seen.", "Pierre&rsquo;s philosophy, as reported by Stupid Dope"),
 "pluto-golf": ("Rap music is the culture, skating is the culture, basketball is the culture, and we&rsquo;ll get golf there too.", "Pluto Golf, on its About Us page"),
 "borde-golf": ("Clean designs, tailored silhouettes and subtle branding; key features derived from the game we love.", "Bord&eacute; Golf, on its brand page"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "pluto-golf": ("Pierre, Fall/Winter 2026", "From Pierre&rsquo;s own campaign.", [("band-1-1","A man in the brown Pierre quarter-zip jacket by the water","Quarter Zip Jacket"),("band-1-2","A man in the cream Pierre polo and gray trousers holding an umbrella","Polo and trousers"),("band-1-3","A man in a brown Pierre jacket in a car","Off the course")]),
 "borde-golf": ("Pluto on the course", "From Pluto Golf&rsquo;s own photos.", [("band-2-1","A golfer in the Pluto Sunday Polo mid-swing","Sunday Polo"),("band-2-2","A man in the olive PlutoDry jacket in the rain","PlutoDry"),("band-2-3","A golfer in the Pluto Church Polo on the course","Church Polo")]),
 "end": ("Bord&eacute; on the course", "From Bord&eacute; Golf&rsquo;s own photos.", [("band-3-1","A golfer in the Bord&eacute; Contour Polo walking past a tree","Contour Polo"),("band-3-2","A golfer in the Bord&eacute; Verge Midlayer swinging","Verge Midlayer"),("band-3-3","A golfer in the Bord&eacute; Brisa Windbreaker on the course","Brisa Windbreaker")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three golf brands we hadn&rsquo;t covered before, and three very different ideas of how a golfer should dress. One makes four pieces in silk. One makes sneakers and loud polos and wants golf to be as cool as skating. One makes tailored polos for golfers who want to look sharp without saying much.</p>
    <p><strong>Pierre</strong> launched this month. It is designed in Montreal and made in Japan, and its artistic director is Vincent Tsang, who holds the same role at the Montreal skate brand Dime. The whole shop is four things: a quarter-zip jacket and pleated trousers in a nylon and silk blend, a cotton and silk polo, and a cap. There are no big logos. As Stupid Dope put it, Pierre&rsquo;s belief is that &ldquo;true luxury is felt before it is seen.&rdquo;</p>
    <p><strong>Pluto Golf</strong> is the opposite. It launched in Indianapolis in March 2024, self-funded, as a sneaker company first; its Pluto 1 sold out six times in the first year, according to Stupid Dope. The name, its About Us page says, is both the planet past the edge of the map and the Greek god of the underworld. The page also takes aim at golf brands &ldquo;run by guys that look like they got dressed in the dark.&rdquo; Its clothes are loud, funny and cheaper than you would expect.</p>
    <p><strong>Bord&eacute; Golf</strong> is from St Albans, outside London, and has been selling since early 2025. Its brand page says the founder, an avid golfer, couldn&rsquo;t find golf clothes that combined performance with style, so he made them, in fabric from Portugal. It launched with a small core range on purpose, and every cap is a limited run.</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>Pierre is for the golfer who buys fewer, better things.</strong> If you would rather own one perfect jacket than five fine ones, start with the Nylon Silk Quarter Zip ($480). The trousers make it a suit you can play in.</p>
    <p><strong>Pluto is for the golfer who dresses for the group chat.</strong> Start with the Pluto 1 ($159), the shoe the brand was built on, then add a polo. The Church Polo is the loud one and the Sunday Polo is the safe one, and both are $84.</p>
    <p><strong>Bord&eacute; is for the golfer who wants to look put together.</strong> The Edge Polo (&pound;80, about $106) is the place to start. Bord&eacute; ships to the US, and UK buyers can ask for free fabric samples before they order.</p>
    <p><strong>If you only buy one thing from each:</strong> the Pierre cap ($97), the Pluto 1 and the Bord&eacute; Edge Polo. That covers your head, your feet and the rest of you, from three brands most people at your club have never heard of.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pierre</span><span>Montreal, made in Japan</span></div>
      <div class="sidebar-detail"><span class="l">Pluto Golf</span><span>Indianapolis, since 2024</span></div>
      <div class="sidebar-detail"><span class="l">Bord&eacute; Golf</span><span>St Albans, since 2025</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$29&ndash;$480</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Pierre Quarter Zip, Pluto 1 Moss, Bord&eacute; Edge Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#PierreGolf</span>
        <span class="hashtag">#PlutoGolf</span>
        <span class="hashtag">#BordeGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Quiet, Loud and Somewhere in Between</h2>
    <p>Put these three next to each other and you get most of what is happening in golf clothes right now. Pierre is the quiet end: no logos, rare fabrics and a price to match. Pluto is the loud end: sneakers, prints and a brand that wants golf to feel like skating. Bord&eacute; sits in the middle, a small British brand doing the basics carefully.</p>
    <p>All three are young, and all three sell direct. Prices were checked on November 16, 2026. If you know a brand we should look at next, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/fresh-three/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-16", "dateModified": "2026-11-16",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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
    <span>On Our Radar</span><span class="dot"></span>
    <span>{N} picks &middot; prices checked November 16, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a man in a brown Pierre jacket by the water, a golfer in the Pluto Sunday Polo mid-swing, and a golfer in a black Bord&eacute; Edge Polo" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "ITL", "Masterpiece", "52 Sundays", "Studio Grain", "LIV"):
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
