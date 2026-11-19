#!/usr/bin/env python3
"""build-fresh-three-2.py — Three fresh golf brands, Vol. 2: Heathlander, Reinland Golf Co. and Matize. Cloned from build-fresh-three.py. 19 November 2026.
Lenny: "find me 3 fresh brands that we haven't featured on the site yet" -> Heathlander, Reinland, Kadet; "I hate Kadet, garbage quality" -> Matize;
"looks good, let's do a round up post". Picks ours (no options sheet): 9 Heathlander (men's only), 10 Reinland, 12 Matize.
FACTS: Heathlander — its About Us page (co-founders Teddy Lynn and Mark Himmelsbach, New York ad agency Episode Four, Lynn grew up on the
southern English heathland courses, Himmelsbach in a golfing family in Michigan) and product pages. Reinland — product pages (made by hand in the
USA, made to order, fleece-lined, Drew Reinland's hand-painted designs, Pendleton and Harris Tweed wool) and its strap-cover copy; founder
Maxton Reinland of Muni Kids and a family-run workshop in Walla Walla, WA per published reviews (no link). Matize — its own site (made in
Portugal, drops, Fall in Love text, MATIZE x Mogshade); founded by three friends from northern Portugal per Portuguese press (no link).
US prices: Heathlander and Reinland in USD; Matize .js?currency=USD (the price a US visitor sees). No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Three Fresh Golf Brands, Vol. 2: Heathlander, Reinland Golf Co. and Matize"
DESC = ("Three golf brands we hadn't covered: Heathlander's heathland-inspired shoe and cashmere, Reinland Golf Co.'s handmade headcovers "
        "from Walla Walla, and Matize's made-in-Portugal drops. 31 picks with prices.")
H1 = "Three Fresh Golf Brands, Vol. 2: Heathlander, Reinland Golf Co. and Matize"
BC = "Heathlander, Reinland, Matize"
SLUG = "heathlander-reinland-matize-golf-brands"
IMG = "/images/fresh-three-2"
SHOP = ""
HL, RG, MZ = "Heathlander", "Reinland Golf Co.", "Matize"
HLU, RGU, MZU = "https://heathlander.com/products/", "https://reinlandgolfco.com/products/", "https://www.matizegolf.com/products/"
P = {
 # Heathlander
 "hl-shoe": (HL, "The Golf Shoe", "$225 <span style=\"opacity:.6\">(two colorways $146.25)</span>", HLU+"heathlander-spikeless-golf-shoe",
   "Our pick from Heathlander. White pebbled leather on a dark green midsole and a pink outsole, a nod to the heather on England&rsquo;s old courses. Built for walking, and it comes with two shoe bags and spare laces."),
 "hl-wind": (HL, "The Wind Sweater", "$320", HLU+"the-wind-sweater-green-green",
   "A fully lined full-zip in 100% merino, modeled on the wind sweaters you still see in northern Scotland and Scandinavia. Pink zip tape on the navy; teal is the other option."),
 "hl-crew": (HL, "The Cashmere Crewneck", "$320 <span style=\"opacity:.6\">(stripe $360)</span>", HLU+"the-cashmere-crewneck-for-men",
   "100% Italian cashmere in navy, olive, camel or cream with a green arm stripe. European sizing, so size up."),
 "hl-vneck": (HL, "The Cashmere V-Neck", "$320", HLU+"the-cashmere-v-neck-for-men",
   "The same cashmere as a V-neck, in dark green or dark gray. The shoulder-season sweater."),
 "hl-hood": (HL, "The Cashmere Hoodie", "$320", HLU+"the-cashmere-hoodie",
   "Cashmere with no zips, pockets or drawstrings to get in the way of a swing. Navy, olive or pale blue."),
 "hl-svest": (HL, "The Cashmere Vest", "$240", HLU+"the-cashmere-sweater-vest",
   "For a slight chill over a golf shirt, in burnt orange or dark green. The orange is the one we would buy."),
 "hl-qvest": (HL, "The Quilted Down Vest", "$99", HLU+"the-quilted-vest",
   "A down-lined quilted vest with pink trim, in navy or teal. Warm without bulk, and the best value in the line."),
 "hl-rope": (HL, "Rope Hat", "$38", HLU+"the-rope-hat",
   "A Richardson rope hat with the pink Heathlander flower on the front, in navy and white or green and gold."),
 "hl-socks": (HL, "Golf Socks", "$20", HLU+"heathlander-golf-socks-men",
   "Crew or ankle socks with pink and white stripes, in green, navy or white. Made for walking 18."),
 # Reinland
 "rg-marathon": (RG, "Marathon Headcover", "$95", RGU+"marathon-golf-headcover",
   "Our pick from Reinland, and its newest cover. Black-and-white checkerboard with a nod to racing, handmade in the USA. A limited edition."),
 "rg-oxide": (RG, "Oxide Headcover", "$80", RGU+"oxide-golf-headcover",
   "Patchwork denim in rusty reds and faded pinks with visible stitching. Made to order, fleece-lined, for golfers who like a little character."),
 "rg-figueroa": (RG, "Figueroa Headcover", "$85", RGU+"figueroa-golf-headcover",
   "A plaid in purple, gold and orange, hand-painted by artist Drew Reinland as a nod to Los Angeles."),
 "rg-seas": (RG, "Angry Seas Headcover", "$85", RGU+"angry-seas-golf-headcover",
   "Navy, electric blue and white swirls of a rough ocean. &ldquo;Kind of like golf,&rdquo; says the listing."),
 "rg-magic": (RG, "Ancient Magic Headcover", "$85", RGU+"ancient-magic-golf-headcover",
   "Hand-drawn symbols and hidden golf illustrations in orange, teal and green. Look closely; the game is in there."),
 "rg-garden": (RG, "The Garden Headcover", "$85", RGU+"the-garden-golf-headcover",
   "A classic golf plaid with the color turned all the way up: navy, electric blue, orange, red and yellow."),
 "rg-seeker": (RG, "Seeker Headcover", "$85", RGU+"the-seeker-golf-headcover",
   "Argyle in burgundy, gold and white, painted with loose brushstrokes so no two diamonds match."),
 "rg-paddy": (RG, "Paddy Headcover", "$80", RGU+"paddy-golf-headcover",
   "Genuine Pendleton wool in a soft, weathered green. The quiet one, in driver, fairway and hybrid sizes."),
 "rg-reggie": (RG, "Reggie Headcover", "$95", RGU+"reggie-golf-headcover",
   "Gray-and-white Harris Tweed woven in Scotland, with small flecks of color you only see up close."),
 "rg-putter": (RG, "Sonny Jr. Putter Cover", "$80 <span style=\"opacity:.6\">(shearling $90)</span>", RGU+"sonny-jr-putter-cover",
   "Sandy brown and cream wide herringbone wool, in blade, mid-mallet, oversize and &ldquo;monster&rdquo; sizes."),
 # Matize
 "mz-autumn": (MZ, "MATIZE &times; Mogshade Autumn Headcover", "$89", MZU+"autumn-headcover-brown",
   "Our pick from Matize. A brown check woven in the Serra da Estrela mountains, made with Mogshade, the Portuguese headcover maker we covered earlier this year."),
 "mz-winter": (MZ, "MATIZE &times; Mogshade Winter Headcover", "$89", MZU+"winter-headcover-oyster",
   "The same collab in an oyster windowpane, with the Matize script on the end. Driver, wood and hybrid."),
 "mz-stripe-c": (MZ, "Autumn Stripes Polo, Charcoal", "$90", MZU+"autumn-stripes-polo-charcoal",
   "A fine stripe in four-way stretch performance fabric, from the Out of Bounds: Fall in Love drop."),
 "mz-stripe-o": (MZ, "Autumn Stripes Polo, Oyster", "$90", MZU+"autumn-stripes-polo-oyster",
   "The same polo in a pale aqua stripe. Also in white."),
 "mz-fog": (MZ, "Fog Polo, Mineral Blue", "$90", MZU+"fog-polo-mineral-blue",
   "A mottled print inspired by the Atlantic mist over Porto, with a ribbed green collar."),
 "mz-storm": (MZ, "Storm Performance Polo", "$107", MZU+"storm-performance-polo",
   "Crisp &ldquo;paper-touch&rdquo; technical fabric with a hidden zip placket. Clean enough for dinner."),
 "mz-coast": (MZ, "Coast LS Shirt", "$147", MZU+"coast-ls-shirt",
   "A navy long-sleeve in a cotton blend with a light seersucker texture, drawing on Portugal&rsquo;s shirting tradition."),
 "mz-port": (MZ, "Port Vest", "$170", MZU+"port-vest",
   "A green sherpa full-zip vest with utility pockets. The photo with the golf balls tells you everything about the brand."),
 "mz-sunday": (MZ, "Sunday Overshirt", "$159", MZU+"sunday-overshirt",
   "Navy Portuguese corduroy cut like a workwear shirt, made to go over a polo from the first tee to the city."),
 "mz-scuba": (MZ, "Scuba Anorak", "$113", MZU+"scuba-anorak",
   "A soft green pullover hoodie with a half zip and a front pocket. The cold-morning layer."),
 "mz-fojo": (MZ, "Fojo Vest", "$136", MZU+"fojo-windbreaker",
   "Sold as the Fojo Windbreaker, but it is a vest: windproof, water-resistant and stretchy, in black with a tonal script."),
 "mz-lisbon": (MZ, "Lisbon Masters Polo, Olive", "$78", MZU+"lisbon-masters-polo-olive",
   "Made for the Lisbon Masters 2026 at Lisbon Sports Club, with the tournament wordmark on the chest."),
}
SECTIONS = [
 ("Heathlander", "heathlander", ["hl-shoe","hl-wind","hl-crew","hl-vneck","hl-hood","hl-svest","hl-qvest","hl-rope","hl-socks"],
  "<strong>New York, inspired by England&rsquo;s heathland &middot; nine picks &middot; $20&ndash;$320</strong>The shoe it started with, then the knitwear: cashmere, a merino wind sweater and a down vest. Men&rsquo;s pieces only here."),
 ("Reinland Golf Co.", "reinland-golf-co", ["rg-marathon","rg-oxide","rg-figueroa","rg-seas","rg-magic","rg-garden","rg-seeker","rg-paddy","rg-reggie","rg-putter"],
  "<strong>Walla Walla, Washington &middot; ten picks &middot; $80&ndash;$95</strong>Handmade, made-to-order headcovers: the two newest, Drew Reinland&rsquo;s painted fall drop, two wool classics and a putter cover."),
 ("Matize", "matize", ["mz-autumn","mz-winter","mz-stripe-c","mz-stripe-o","mz-fog","mz-storm","mz-coast","mz-port","mz-sunday","mz-scuba","mz-fojo","mz-lisbon"],
  "<strong>Portugal &middot; 12 picks &middot; $78&ndash;$170</strong>Mostly from the Out of Bounds: Fall in Love drop, plus the Mogshade collab and the Lisbon Masters polo. All made in Portugal."),
]
N = 31
PQ = {
 "heathlander": ("Proper golfers walk.", "Heathlander, on its homepage"),
 "reinland-golf-co": ("Some golfers like their gear shiny and spotless. We like a little character.", "Reinland Golf Co., on the Oxide headcover"),
 "matize": ("Designed for the course, worn everywhere.", "Matize, on its homepage"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "reinland-golf-co": ("Heathlander, Fall/Winter", "From Heathlander&rsquo;s own photos.", [("band-1-1","A golfer walking a heathland course at sunrise","On the heath"),("band-1-2","Heathlander cashmere and wind sweaters folded by a fireplace","The knitwear"),("band-1-3","A man in the navy Heathlander Wind Sweater with a pink zip","Wind Sweater")]),
 "matize": ("Reinland in the wild", "From Reinland Golf Co.&rsquo;s own photos.", [("band-2-1","Reinland Special Day floral headcovers in three sizes","Special Day"),("band-2-2","Reinland Egg Hunt argyle headcovers in three sizes","Egg Hunt"),("band-2-3","The Reinland Figueroa plaid headcover","Figueroa")]),
 "end": ("Matize, Out of Bounds", "From Matize&rsquo;s own photos.", [("band-3-1","Two men in Matize on a course by the water","On the course"),("band-3-2","A man in the Matize Port Vest holding golf balls over his eyes","Port Vest"),("band-3-3","A man with a golf bag and balls on a yellow set","Golfers of the sea")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three brands we hadn&rsquo;t covered before, and three good reasons to look past the pro shop this winter. One makes a shoe and cashmere for golfers who walk. One makes headcovers by hand in a small town in Washington. One makes clothes in Portugal and releases them in small drops with a story behind each one.</p>
    <p><strong>Heathlander</strong> is named for the heathland courses of southern England. Co-founder Teddy Lynn grew up playing them, at Sunningdale, The Berkshire and Woking; Mark Himmelsbach grew up in a golfing family in Michigan, one of the few US states with real heathland golf. The two run a New York ad agency, and Heathlander is their brand for &ldquo;proper golfers.&rdquo; It started with a white golf shoe on a pink sole, the color of the heather, and has grown into Italian cashmere, a fully lined merino wind sweater and a down vest.</p>
    <p><strong>Reinland Golf Co.</strong> makes headcovers by hand in Walla Walla, Washington. It is a family business, the sister label of Muni Kids, and most covers are made to order with a fleece lining and a hidden elastic. The range runs from Pendleton wool and Harris Tweed to Drew Reinland&rsquo;s hand-painted plaids, argyles and ocean swirls. It also brought back the furry bag strap covers from the 1980s and &rsquo;90s Sunday bag. A new cover lands every few weeks.</p>
    <p><strong>Matize</strong> was started by three friends from northern Portugal who wanted to make golf feel less stuffy at home. Everything is made in Portugal, and it releases its clothes in named drops, not seasons. The current one, Out of Bounds: Fall in Love, is about the quieter rounds and colder mornings of fall golf, and includes a headcover collab with Mogshade.</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>Heathlander is for the golfer who walks in any weather.</strong> Start with The Golf Shoe ($225), then the Wind Sweater ($320). On a budget, the Quilted Down Vest is $99.</p>
    <p><strong>Reinland is for the golfer who wants a bag nobody else has.</strong> Pick one loud cover for the driver, the Marathon or Figueroa, and a quiet wool for the rest. Everything is $80 to $95.</p>
    <p><strong>Matize is for the golfer who goes straight from the course to dinner.</strong> Start with the Sunday Overshirt ($159) over an Autumn Stripes Polo ($90). The Mogshade headcover ($89) is the gift.</p>
    <p><strong>If you only buy one thing from each:</strong> the Heathlander shoe, the Reinland Marathon and the Matize &times; Mogshade Autumn headcover. Your feet, your driver and your fairway wood, from three brands most people at your course have never heard of.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Heathlander</span><span>New York, heathland-inspired</span></div>
      <div class="sidebar-detail"><span class="l">Reinland</span><span>Walla Walla, WA, handmade</span></div>
      <div class="sidebar-detail"><span class="l">Matize</span><span>Made in Portugal</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>31</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$20&ndash;$320</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Heathlander Golf Shoe, Reinland Marathon, Matize &times; Mogshade Autumn</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#Heathlander</span>
        <span class="hashtag">#ReinlandGolf</span>
        <span class="hashtag">#MatizeGolf</span>
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
    <h2 class="products-hdr" id="last-word">Walk It, Cover It, Wear It Out</h2>
    <p>None of these three is trying to be everything. Heathlander makes a shoe and a sweater drawer for golfers who walk. Reinland makes the covers, one at a time. Matize makes the clothes, a drop at a time, in Portugal. Put them together and you have a whole winter kit from three small brands.</p>
    <p>If you liked Matize, read our <a href="/drops/brand-to-know-mogshade">Mogshade Brand to Know</a> for the other half of that headcover. Prices were checked on November 19, 2026. If you know a brand we should look at next, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/fresh-three-2/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-PQ*/.pull-quote-inner{font-size:clamp(34px,4.6vw,58px);line-height:1.15;text-align:center;padding:44px 0}.pull-quote-attr{font-size:11px;margin-top:18px}@media(max-width:720px){.pull-quote-inner{font-size:30px;padding:32px 0}}</style>\n<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-19", "dateModified": "2026-11-19",
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
            f'  <figure style="margin:0 0 28px"><img src="{IMG}/banner-{anchor}.jpg" alt="{H.escape(H.unescape(h2))}, from the brand&rsquo;s own photos" loading="lazy" style="width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:#e8e2d6" /></figure>\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}" style="font-size:clamp(44px,7vw,84px);line-height:1;margin:14px 0 16px;letter-spacing:-.01em">{h2}</h2>\n'
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
    <span>{N} picks &middot; prices checked November 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer walking a heathland course at sunrise, Reinland Garden plaid headcovers, and a man in the Matize Sunday Overshirt" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Pierre", "Pluto", "Bord", "Kadet", "GRIPIT"):
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
