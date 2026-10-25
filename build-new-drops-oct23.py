#!/usr/bin/env python3
"""build-new-drops-oct23.py — three new drops in one post (23 October 2026). Cloned from build-cph-jones.py.
Lenny: "Let's do one post that combines the Malbon, Gumtree and Mogshade new releases".
FACTS + PRICES (all checked October 23, 2026, brands' own stores):
 Malbon x Grateful Dead "Long Vacation": malbon.com products.json, 18 listings tagged "10.23.26 Grateful Dead", published Oct 23 (research/new-drops-oct23/malbon.json). USD.
   Six-part collab for the band's 60th anniversary; Drop 1 Dec 2025, Drop 2 July 2026 (drops/malbon-x-grateful-dead.html). No drop number given for this one.
 Gumtree Golf & Nature Club x Wynn: gumtreegolfandnature.com/shop/ggnc-x-wynn (Squarespace JSON, research/new-drops-oct23/gumtree.json). USD.
 Mogshade Re.Weave autumn headcovers: mogshadegolf.com products.json, 15 created Oct 19-23, published Oct 23 (research/new-drops-oct23/mogshade.json).
   Store currency EUR (meta.json). USD at 1.12167 USD/EUR (open.er-api.com, 23 Oct 2026). Noor Brown sold out, left out.
Images: brands' own product + lookbook shots (research/new-drops-oct23/frame.py). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "New Golf Drops: Malbon x Grateful Dead, Gumtree x Wynn, Mogshade"
DESC = ("This week's new golf releases: Malbon's Long Vacation drop with the Grateful Dead, Gumtree's Wynn Golf Club "
        "collab and 14 new Mogshade headcovers, with prices.")
H1 = "Three Drops, One Week: Malbon, Gumtree and Mogshade"
BC = "New Drops: Malbon, Gumtree, Mogshade"
SLUG = "new-golf-drops-malbon-gumtree-mogshade"
IMG = "/images/new-drops-oct23"
SHOP = ""
MB = "Malbon &times; Grateful Dead"
GB = "Gumtree &times; Wynn"
SB = "Mogshade"
MS = "https://malbon.com/products/grateful-dead-"
GS = "https://www.gumtreegolfandnature.com/shop/p/wynn-golf-club-"
SS = "https://mogshadegolf.com/products/"
def eur(e): return f"&euro;{e} (~${round(e*1.12167)})"
SH = "Made from rescued fabric woven in Portugal&rsquo;s Serra da Estrela mountains, lined in fleece. "
P = {
 "m1": (MB, "Long Vacation Poncho", "$398", MS + "long-vacation-poncho-forest",
   "The loudest piece in the drop: an oversized hooded poncho in a cotton-wool jacquard, with the Stealie-on-a-golf-ball graphic front and back, a big front pocket and snap sides. One size, 67 inches long."),
 "m2": (MB, "Long Vacation Varsity Jacket", "$428", MS + "long-vacation-varsity-jacket-forest",
   "A forest-green wool-blend varsity with a quilted nylon lining, jacquard rib at the collar, cuffs and hem, &ldquo;Long Vacation&rdquo; script on the chest and a chenille dancing bear riding a golf ball across the back."),
 "m3": (MB, "Long Vacation Cardigan", "$278", MS + "long-vacation-cardigan-forest",
   "A relaxed V-neck in 95% wool and 5% cashmere, with the collection&rsquo;s blanket pattern across the body and sleeves. Forest or heather oatmeal; the one to wear over a polo in November."),
 "m4": (MB, "Long Vacation Quarter Zip", "$228", MS + "long-vacation-quarter-zip-heather-oatmeal",
   "A deep-pile fleece quarter-zip in heather oatmeal, with woven pattern tape down the placket and pockets, an antique-brass zip and a clear chest patch. Pairs with the sweatpant."),
 "m5": (MB, "Long Vacation Sweatpant", "$178", MS + "long-vacation-sweatpant-heather-oatmeal",
   "The matching deep-pile sweatpant: woven tape down the side seams, a drawcord waist, an embroidered back pocket and a 30-inch inseam. Clubhouse wear, not range wear."),
 "m6": (MB, "Fairway Dancing Buckets Polo", "$128", MS + "fairway-dancing-buckets-polo-ivory",
   "The golf piece: a clean-front polo with a brown flat-knit collar, a hidden two-snap placket, patterned side tape and the dancing bear on the back. Ivory or forest."),
 "m7": (MB, "Gorse Dancing Buckets Tee", "$98", MS + "gorse-dancing-buckets-tee-washed-black",
   "A long-sleeve tee in enzyme-washed cotton with artwork on the chest, both sleeves and the back. Washed black or white."),
 "m8": (MB, "Bermuda Riders Tee", "$68", MS + "bermuda-riders-tee-ivory",
   "The easy way in: a short-sleeve cotton crew with a small front hit and a bigger back graphic. Ivory or ash heather."),
 "m9": (MB, "Long Vacation Snapback", "$68", MS + "long-vacation-snapback-forest",
   "A five-panel snapback with a clear rubber Stealie patch, woven pattern tape at the sides and rear embroidery. Forest or brown, both with a black brim."),
 "m10": (MB, "Long Vacation Bucket Hat", "$98", MS + "long-vacation-bucket-hat-heather-oatmeal",
   "A deep-pile bucket in heather oatmeal, wrapped in the woven pattern band with a clear patch at the front. S/M and L/XL."),
 "m11": (MB, "Long Vacation Cart Bag", "$448", MS + "long-vacation-cart-bag-forest",
   "The most detailed piece: a full cart bag in textured green PU with woven wool panels, chenille artwork and a &ldquo;Long Vacation&rdquo; ball pocket. Preorder; Malbon says it ships by November 23."),
 "m12": (MB, "Tour M Golf Ball Pack", "$60", "https://malbon.com/products/grateful-dead-tour-m-golf-ball-pack-white",
   "A dozen Malbon Tour M balls with the Long Vacation character printed on four sides. Already sold out on Malbon&rsquo;s site."),
 "m13": (MB, "Long Vacation Sticker Pack", "$18", MS + "long-vacation-sticker-pack-multi",
   "Eleven vinyl stickers in green, white and black, for the cart, the cooler or the laptop."),
 "g1": (GB, "Unstructured 5-Panel Hat: Roadrunner", "$60", GS + "hat-roadrunner",
   "A soft brown five-panel with a roadrunner, a Mojave local, embroidered in off-white cotton and the GGNC x Wynn Explorers label inside. Embroidered in New York City."),
 "g2": (GB, "Unstructured 5-Panel Hat: Cactus Wren", "$60", GS + "hat-cactus-wren",
   "The navy version, with the cactus wren, one of the desert birds that live around Las Vegas."),
 "g3": (GB, "Unstructured 5-Panel Hat: Sidewinder", "$60", GS + "hat-sidewinder",
   "Black, with the sidewinder rattlesnake that moves sideways across the Mojave sand. Pick your animal."),
 "g4": (GB, "Ripstop Work Jacket", "$345", GS + "work-jacket",
   "A cropped, boxy chore coat cut and sewn in Manhattan from Japanese cotton ripstop, with an oversized collar, raglan shoulders and swirl buttons. The piece the whole shoot is built around."),
 "g5": (GB, "French Twill Long-Sleeve Shirt", "$185", GS + "ls-shirt",
   "A white button-down in mid-weight cotton French twill with shell buttons and the Wynn tree embroidered on the chest in brown. Cut and sewn in Manhattan."),
 "g6": (GB, "Ripstop Wide-Leg Pleated Pant", "$325", GS + "lightweight-pleated-pant",
   "The matching Japanese ripstop pant: front pleats into a wide leg that stops at the ankle, made for boots or loafers. Black, tan or navy."),
 "g7": (GB, "Dobby Short-Sleeve Polo", "$145", GS + "ss-polo",
   "A camp-collar polo woven from a textured cotton dobby check with a linen-like feel, Wynn Golf Club on the sleeve. Brown or off-white; made in New York."),
 "g8": (GB, "Headcover", "$125&ndash;$140", GS + "headcover",
   "Driver ($140) and fairway ($125) covers in the same dobby check, canvas-lined with a felt interior and the Wynn tree on top. Brown or off-white."),
 "g9": (GB, "Valuables Pouch", "$90", GS + "valuables-pouch",
   "A dobby zip pouch with a brass zip and brass clip, so the phone, keys and wallet have somewhere to live on the cart."),
 "g10": (GB, "Golf &amp; Nature Token", "$25", GS + "ball-marker",
   "A two-sided die-cast token that doubles as a ball marker, in gunmetal, antique gold or antique silver. All three sold out on drop day."),
 "s1": (SB, "Tartan Yellow Headcover", eur(78), SS + "tartan-yellow-headcover",
   SH + "The loudest of the batch: a yellow, black and red tartan. Driver &euro;78, wood &euro;74, hybrid &euro;71."),
 "s2": (SB, "Houndstooth Autumn Headcover", eur(78), SS + "dogtooth-autumn-headcover",
   SH + "A small purple-and-cream houndstooth that reads gray from the tee box."),
 "s3": (SB, "Azulejo Brown Headcover", eur(78), SS + "azulejo-brown-black-headcover",
   SH + "Brown and black in a pattern named for Portugal&rsquo;s painted tiles."),
 "s4": (SB, "Desert Orange &amp; Sea Headcover", eur(78), SS + "desert-orange-sea-headcover",
   SH + "A rust-orange weave with a pale sea-blue figure; the brightest of the autumn colors."),
 "s5": (SB, "Waffle Autumn Headcover", eur(71), SS + "waffle-autumn-headcover",
   SH + "Cream waffle with rust and blue checks. Only the hybrid size is left."),
 "s7": (SB, "Vintage Orange &amp; Gray Headcover", eur(78), SS + "vintage-orange-gray-headcover",
   SH + "An orange-and-gray geometric that looks lifted from a 70s sofa, in the best way."),
 "s8": (SB, "Vintage Berry Headcover", eur(78), SS + "vintage-berry-headcover",
   SH + "Berry and cream in a dense vintage pattern."),
 "s9": (SB, "Dot Red &amp; Gray Headcover", eur(78), SS + "dot-red-gray-headcover",
   SH + "Gray dots on red, like an old silk tie."),
 "s10": (SB, "Dot Gray &amp; Red Headcover", eur(78), SS + "dot-gray-red-headcover",
   SH + "The reverse: red dots on charcoal, the quietest of the dots."),
 "s11": (SB, "Vintage Algae Headcover", eur(78), SS + "vintage-algae-headcover",
   SH + "A mustard-and-gray geometric. Driver and hybrid only; the wood size has sold out."),
 "s12": (SB, "Tiles Orange Headcover", eur(78), SS + "tiles-orange-headcover",
   SH + "A tight orange basketweave that looks solid from a distance."),
 "s13": (SB, "Arrow Eucalypto Headcover", eur(78), SS + "arrow-eucalypto-headcover",
   SH + "A pale eucalyptus-green arrow weave; the calmest cover here."),
 "s14": (SB, "Houndstooth Lichen Headcover", eur(78), SS + "dogtooth-lychen-headcover",
   SH + "A big sage-and-cream houndstooth. Driver and hybrid; the wood size has sold out."),
 "s15": (SB, "Houndstooth Brown Headcover", eur(78), SS + "dogtooth-brown-headcover",
   SH + "Brown and black houndstooth for the tweed crowd. Driver and hybrid; no wood left."),
}
SECTIONS = [
 ("Malbon &times; Grateful Dead: Long Vacation", "malbon", ["m1","m2","m3","m4","m5","m6","m7","m8","m9","m10","m11","m12","m13"],
  "<strong>13 pieces &middot; $18&ndash;$448 &middot; released October 23</strong>Malbon&rsquo;s newest chapter of its six-part Grateful Dead collaboration for the band&rsquo;s 60th anniversary. Forest green, oatmeal and a blanket-style pattern, with the dancing bear riding a golf ball."),
 ("Gumtree Golf &amp; Nature Club &times; Wynn Golf Club", "gumtree", ["g1","g2","g3","g4","g5","g6","g7","g8","g9","g10"],
  "<strong>10 pieces &middot; $25&ndash;$345 &middot; released October 23</strong>Made for Wynn Golf Club in Las Vegas, with Mojave animals on the hats and most of it cut, sewn or embroidered in New York."),
 ("Mogshade: 14 New Autumn Headcovers", "mogshade", ["s1","s2","s3","s4","s5","s7","s8","s9","s10","s11","s12","s13","s14","s15"],
  "<strong>14 covers &middot; &euro;71&ndash;&euro;78 (~$80&ndash;$87) &middot; released October 23</strong>New patterns in Mogshade&rsquo;s Re.Weave line, handmade in Portugal. Prices by size: driver &euro;78, wood &euro;74, hybrid &euro;71. One more, Noor Brown, sold out on day one."),
]
N = 37
PQ = {}
BANDS = {
 "gumtree": ("Shot at Wynn Golf Club, Las Vegas. ",
   "Gumtree&rsquo;s lookbook goes camping, climbing and fishing on a course that sits on the Strip.",
   [("look-1","A model in the Gumtree x Wynn work jacket and pants on a fairway with the Wynn tower behind","On the Strip &middot; Gumtree Golf &amp; Nature Club"),
    ("look-2","A model in the Gumtree x Wynn polo standing in a rowboat on a course pond","Fishing &middot; Gumtree Golf &amp; Nature Club"),
    ("look-3","A model in the ripstop work jacket and pants under a tree","Under the trees &middot; Gumtree Golf &amp; Nature Club")]),
 "malbon": ("Long Vacation, shot on green canvas. ",
   "Malbon&rsquo;s campaign for the drop: blanket-pattern knits, deep-pile fleece and a golf club for a walking stick.",
   [("look-5","A model in the forest Long Vacation cardigan holding a golf club","The cardigan &middot; Malbon"),
    ("look-6","A model in the oatmeal Long Vacation cardigan","Oatmeal &middot; Malbon"),
    ("look-7","A model in the Long Vacation fleece quarter-zip","The fleece &middot; Malbon")]),
 "mogshade": ("Rescued wool from the Serra da Estrela. ",
   "Every Mogshade cover is photographed on the fabric it is made from.",
   [("look-9","A Mogshade tartan yellow headcover lying on matching tartan fabric","Tartan Yellow &middot; Mogshade"),
    ("look-10","A Mogshade waffle autumn headcover on matching fabric","Waffle Autumn &middot; Mogshade"),
    ("look-11","A Mogshade houndstooth lichen headcover on matching fabric","Houndstooth Lichen &middot; Mogshade")]),
}
KIT_CSS = ""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>Three brands we cover a lot put out new collections on the same day, October 23. They have almost nothing in common, which is the fun of putting them side by side: a Grateful Dead fever dream from Los Angeles, a quiet desert-nature capsule sewn in Manhattan for a Las Vegas golf club, and a stack of handmade wool headcovers from Portugal.</p>
    <p><strong>Malbon &times; Grateful Dead, Long Vacation.</strong> This is the latest chapter of Malbon&rsquo;s six-part collaboration with the Dead for the band&rsquo;s 60th anniversary; <a href="/drops/malbon-x-grateful-dead">Drop 2</a> landed in July. Long Vacation moves the story into cold weather: a jacquard poncho, a chenille varsity, wool-cashmere cardigans and a deep-pile fleece set, all in forest green and oatmeal, with the dancing bear riding a golf ball. The polo is the piece you would actually play in. The golf balls sold out the same day, and the cart bag is a preorder that ships by November 23.</p>
    <p><strong>Gumtree &times; Wynn.</strong> Karsten Jurkschat&rsquo;s Brooklyn label made this one for Wynn Golf Club, the course behind the Wynn on the Las Vegas Strip, which Gumtree describes as an oasis of birds, streams and trees nearly 80 years old. The hats carry Mojave locals (a roadrunner, a cactus wren, a sidewinder), and the clothes are cut and sewn in Manhattan: a Japanese ripstop chore coat and pleated pants, a dobby check polo and a white button-down. The ball-marker token sold out on drop day. Our <a href="/drops/brand-to-know-gumtree-golf-and-nature-club">Gumtree Brand to Know</a> has the backstory.</p>
    <p><strong>Mogshade&rsquo;s autumn headcovers.</strong> The Portuguese maker added 14 new patterns to its Re.Weave line, which uses rescued fabric from mills in the Serra da Estrela mountains. Tartan, houndstooth, dots, tiles and 70s-sofa geometrics, all at the same price by size. Mogshade makes to order, so expect a wait; our <a href="/drops/brand-to-know-mogshade">Mogshade Brand to Know</a> covers how it works.</p>
    <p><strong>If you buy one thing.</strong> From Malbon, the Fairway polo ($128); from Gumtree, a hat ($60) or, if you are going big, the work jacket; from Mogshade, the Tartan Yellow driver cover. Prices were checked on each brand&rsquo;s site on October 23, 2026; Mogshade sells in euros, converted at about $1.12 to the euro.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Drops</div>
      <div class="sidebar-detail"><span class="l">Malbon</span><span>Long Vacation &middot; $18&ndash;$448</span></div>
      <div class="sidebar-detail"><span class="l">Gumtree</span><span>&times; Wynn &middot; $25&ndash;$345</span></div>
      <div class="sidebar-detail"><span class="l">Mogshade</span><span>Re.Weave &middot; &euro;71&ndash;&euro;78</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>October 23, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>37</span></div>
      <div class="hashtags">
        <span class="hashtag">#Malbon</span>
        <span class="hashtag">#GratefulDead</span>
        <span class="hashtag">#GumtreeGolf</span>
        <span class="hashtag">#Mogshade</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
KIT = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">More Photos</div>
  <h2 class="products-hdr" id="lookbook">From the Campaigns</h2>
  <p class="cat-kicker">Photography &middot; Malbon and Gumtree Golf &amp; Nature Club.</p>
  <div class="ig-grid">
  <figure><img src="/images/new-drops-oct23/look-4.jpg" alt="A Gumtree x Wynn valuables pouch clipped to a climbing harness, from Gumtree's lookbook" loading="lazy" /></figure>
  <figure><img src="/images/new-drops-oct23/look-8.jpg" alt="The back of the Malbon x Grateful Dead varsity jacket with the dancing bear on a golf ball, from Malbon's campaign" loading="lazy" /></figure>
  <figure><img src="/images/new-drops-oct23/look-12.jpg" alt="The Malbon x Grateful Dead Long Vacation sweatpant and fleece, from Malbon's campaign" loading="lazy" /></figure>
  </div>
</section>
"""
FAQ = [
 ("When did the Malbon x Grateful Dead Long Vacation collection come out?", "October 23, 2026, on Malbon's website. It is the latest release in Malbon's six-part Grateful Dead collaboration for the band's 60th anniversary."),
 ("How much is the Malbon x Grateful Dead cart bag?", "$448. It is a preorder, and Malbon says it ships by November 23, 2026."),
 ("What is the Gumtree x Wynn collection?", "A collaboration between Brooklyn's Gumtree Golf & Nature Club and Wynn Golf Club in Las Vegas, released October 23, 2026: hats, a ripstop work jacket and pants, a polo, a shirt, headcovers, a pouch and a ball-marker token, from $25 to $345."),
 ("How much are Mogshade headcovers?", "In the new autumn Re.Weave patterns, 78 euros for a driver cover, 74 for a wood and 71 for a hybrid, roughly $80 to $87. Mogshade is in Portugal and ships to the US."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
_FR = json.loads((ROOT / "research/new-drops-oct23/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-23", "dateModified": "2026-10-23",
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
    <span>The Grassy Issue &middot; New drops</span><span class="dot"></span>
    <span>37 pieces &middot; prices checked October 23, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Malbon x Grateful Dead cardigan, the Gumtree x Wynn work jacket at Wynn Golf Club, and a Mogshade tartan headcover" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Parmore", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Climber", "Woodgrain", "Bethpage", "LBB", "GolfPass"):
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
