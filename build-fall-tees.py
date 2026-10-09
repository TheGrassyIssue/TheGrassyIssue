#!/usr/bin/env python3
"""build-fall-tees.py — 26 Tees for Cooler Fall Weather. 9 Oct 2026.
Lenny: "Let's do a fall tee round up- 24 Tees for cooler fall weather". From fall-tees-options.html he picked "My 24
(Recommended)", then "drop 6,14,29 add 7,8,9,13,18,20,44,54,58" and chose "Keep all 26" (Fella, Odd Ritual and
Puttwell each appear twice, by his call).

FACTS: research/fall-tees/batch1.json + batch2.json (each read on the brand's own store, 9 Oct 2026, in stock in M).
Non-USD prices in store currency with an approximate dollar figure (GBP 1.34, EUR 1.16, AUD 0.66, SEK 0.105, ZAR 0.057).
PHOTOS: the brands' own product images, framed 1000x1250 (research/fall-tees/frames.json), studio whites softened.
Hero: Criquet's own lifestyle photo of the Cotton Slub Long Sleeve.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "fall-golf-t-shirts-tees-for-cooler-weather"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/fall-tees"
FRN = {f"F{int(k):02d}": v for k, v in json.loads((ROOT / "research/fall-tees/frames.json").read_text()).items()}
DATE = "2026-10-09"

TITLE = "Fall Golf T-Shirts: 26 Tees for Cooler Weather"
DESC = ("Fall golf T-shirts from independent brands: long sleeves, heavyweight cotton and graphic tees in fall colors "
        "from Criquet, Malbon, Manors, Ghost, Sounder and more, with prices.")
H1 = "26 Tees for Cooler Fall Weather"

U = "?utm_source=thegrassyissue&amp;utm_medium=referral&amp;utm_campaign=editorial&amp;utm_content=" + SLUG

# key -> (brand, item, price, url, copy)
P = {
 # The Long Sleeves
 "F04": ("Criquet Shirts", "Cotton Slub Long Sleeve T-Shirt, Natural", "$98",
   "https://criquetshirts.com/products/slub-cotton-long-sleeve-t-shirt-natural",
   'Criquet took its vintage slub pocket tee and gave it sleeves, which is exactly what an Austin October calls for. The slub jersey has that worn-in texture from the first wear, the cuffs are ribbed, and the Grassy C is stitched onto the chest pocket. Designed here in Austin, made in Peru. Ours in <a href="/drops/brand-to-know-criquet">the Criquet Brand to Know</a>.'),
 "F09": ("Ghost Golf", "Clubhouse Rebels GGC Long Sleeve T-Shirt, Bone", "$70",
   "https://ghostgolf.com/products/clubhouse-rebels-ggc-ls-t-shirt",
   "Ghost cut this one heavy, 285gsm cotton in a boxy, drop-shoulder fit, so it hangs like a sweatshirt and wears like a tee. The front carries a layered GhostGolf Club crest from the Clubhouse Rebels drop, and the back stays clean. Bone is the fall pick; black is in stock too."),
 "F10": ("Gumtree Golf &amp; Nature Club", "How To Tie a Fly Reference L/S Tee, Vintage Black", "$65",
   "https://www.gumtreegolfandnature.com/shop/p/anatomy-of-a-fly-reference-tee-35s3d",
   'Gumtree prints a 1940 E.C. Gregg illustration across the back of this one, twelve steps to tying a fly, which makes it the most interesting back on the list. It is 6.5oz American cotton, sewn in the USA in an oversized, boxy cut, with the Nature Club logo up front. More in <a href="/drops/gumtree-nature-club-drop">our Gumtree Nature Club post</a>.'),
 "F15": ("Malbon Golf", "Gorse Heritage Tee, Heather Oatmeal", "$88",
   "https://malbongolf.com/products/gorse-heritage-tee-heather-oatmeal",
   'From Malbon&rsquo;s fall drop, a long-sleeve heritage tee in heather oatmeal with contrast ribbing at the collar and cuffs. There is a small chest crest and an oversized clubhouse-style graphic on the back, and the dropped shoulder keeps it relaxed. More Malbon in <a href="/drops/malbon-fall-2026-the-ironworks-collection">our Ironworks Collection post</a>.'),
 "F17": ("Merrill Golf", "Golf Company LS Tee, Clay", "$65",
   "https://merrillgolf.com/products/golf-company-ls-tee-clay",
   'Merrill makes this in the USA from heavyweight cotton and garment-dyes it, so the clay color has the faded depth of a shirt you have owned for years. Golf Company prints sit front and back, and it fits true to size. Ours in <a href="/drops/brand-to-know-merrill-golf">the Merrill Brand to Know</a>.'),
 "F19": ("No Laying Up", "10 Years of Tourist Sauce Long Sleeve T-Shirt, Midnight", "$50",
   "https://store.nolayingup.com/products/no-laying-up-10-years-of-tourist-sauce-long-sleeve-tour-t-shirt-midnight",
   "A limited concert-style long sleeve marking ten years of Tourist Sauce, dropped this week. The back lists every destination on an airplane graphic, like a tour shirt, and it is printed on a pigment-dyed heavyweight Comfort Colors blank in a washed midnight navy."),
 "F26": ("Puttwell", "Wordmark L/S Tee, Deep Green", "$30",
   "https://puttwellgolfclub.com/products/puttwell-wordmark-l-s-tee",
   'Puttwell&rsquo;s wordmark tee is the easiest buy on the list: a mid-weight cotton long sleeve in deep green with the Puttwell wordmark across the chest, marked down from $60 to $30. Crew neck, cuffed sleeves, nothing extra. Ours in <a href="/drops/brand-to-know-puttwell">the Puttwell Brand to Know</a>.'),
 "F58": ("Puttwell", "Waikahalulu Country Club Longsleeve, Black", "$65",
   "https://puttwellgolfclub.com/products/waikahalulu-country-club-longsleeve-3",
   "Puttwell&rsquo;s second pick comes from its Honolulu capsule. The back carries hand-cut map art of Chinatown, and the black long sleeve gives it room to stand out. Medium is the last size in black; Off White is also in stock in M."),
 "F30": ("SLICE TOWN", "Long Sleeve Tee, Dusty Cobalt", "SEK 600 (~$63)",
   "https://slice-town.com/products/long-sleeve-tee-cobalt",
   'SLICE TOWN works in details, and here it is the contrast coverlock topstitching that crosses the chest and runs down the sides. The cotton is a heavy 253gsm in a relaxed cut, and dusty cobalt is a blue that sits well under a fall vest. Ours in <a href="/drops/brand-to-know-slice-town">the SLICE TOWN Brand to Know</a>.'),
 "F32": ("Sounder", "Fuzzy Pocket Long Sleeve T-Shirt, Gold and Slate", "&pound;90 (~$121)",
   "https://soundergolf.com/products/fuzzy-ls-pocket-t-shirt-in-gold-and-slate",
   'Sounder makes the most textured shirt here. It knits its own slub stripe from organic cotton in gold and slate, adds deep ribbed cuffs and a contrasting slate chest pocket, and has it made in Portugal. It reads like a vintage rugby stripe without the collar. Ours in <a href="/drops/brand-to-know-sounder">the Sounder Brand to Know</a>.'),
 "F34": ("Students Golf", "Laurence L/S Layered T-Shirt, Camo", "$70",
   "https://studentsgolf.com/products/laurence-l-s-layered-t-shirt",
   'Students fakes the layered look so you do not have to: a boxy 280gsm jersey body printed in wood camo with waffle-thermal long sleeves sewn in. It is the most fall-looking tee on the list and the easiest outfit. See <a href="/drops/students-golf-our-15-favorites">our 15 Students favorites</a>.'),
 # Heavyweights and Blanks
 "F01": ("B.O.T.H. Bet On The Horses", "Malibu Slub Tee, Vintage Black", "$80",
   "https://betonthehorses.co/products/berry-hills-t-shirt-1",
   "B.O.T.H. keeps this one a clean blank, with no golf graphic at all. It makes the tee in Los Angeles from slub cotton and distresses it lightly, so the vintage black looks like a shirt you found, not one you bought. It sits under an open flannel or a quarter-zip as well as it does on its own."),
 "F16": ("Manors Golf", "Manors Logo T-Shirt, Dark Olive", "&pound;45 (~$60)",
   "https://manorsgolf.com/products/manors-logo-t-shirt",
   'Manors cuts its everyday tee from 240gsm cotton in a relaxed fit and keeps the branding to a small logo. Dark olive is the fall color of the three in stock, and it is the plain tee you will reach for most. Ours in <a href="/drops/brand-to-know-manors">the Manors Brand to Know</a>.'),
 "F18": ("Metalwood Studio", "Heavyweight Mini Metal Logo T-Shirt, Green Tea", "$72",
   "https://metalwood.studio/products/heavyweight-mini-metal-logo-t-shirt-green-tea",
   'Heavyweight cotton in an oversized, boxy, cropped cut, with nothing on it but a small embroidered Metal patch. Green tea is a muted sage that works with every pair of fall pants. Small and medium are the last sizes. Ours in <a href="/drops/brand-to-know-metalwood-studio">the Metalwood Brand to Know</a>.'),
 "F13": ("Local Rule", "T-Shirt, Dark Green", "SEK 599 (~$63)",
   "https://local-rule.com/products/t-shirt-dark-green",
   'Local Rule, from Stockholm, makes its tee in Portugal from premium cotton in a relaxed fit and adds only an italic logo in embroidery. The dark green is deep enough for October and plain enough for every day. Ours in <a href="/drops/brand-to-know-local-rule">the Local Rule Brand to Know</a>.'),
 "F24": ("Pins &amp; Aces", "Embossed Spade Tee Shirt, Forrest", "$49.95",
   "https://pinsandaces.com/products/embossed-spade-tee-shirt-forrest",
   "Pins &amp; Aces skips the print and embosses its spade logo into the chest instead, tone on tone, so you only see it up close. It is a relaxed cotton-poly blend in a forest green that looks right next to a fall course."),
 "F20": ("Odd Ritual", "OR Monogram T-Shirt, Black", "R1,000 (~$57)",
   "https://oddritualgolf.com/products/or-monogram-t-shirt-black",
   'From Stellenbosch, South Africa, a drop-shoulder tee in black with tonal Odd Ritual embroidery on the arm and a distressed OR monogram stamped on the back in charcoal and gold. Quiet from the front, a little louder walking away. Ours in <a href="/drops/brand-to-know-odd-ritual">the Odd Ritual Brand to Know</a>.'),
 # The Graphic Tees
 "F03": ("Casualist", "No Idea Heavy Tee, Ecru", "&pound;65 (~$87)",
   "https://casualist.com/products/heavy-tee-agni",
   'The best joke on the list, printed in rust across the back: Casualist, all the gear, no idea. The tee itself is serious, heavyweight organic cotton in a relaxed oversized cut, made in Portugal. Ours in <a href="/drops/brand-to-know-casualist">the Casualist Brand to Know</a>.'),
 "F05": ("Devereux Golf", "Grand Canyon Country Club Tee, Brindle", "$38",
   "https://devereuxgolf.com/products/grand-canyon-country-club-tee-brindle",
   'Part of Devereux&rsquo;s State Pack, landed in late September: an Arizona state outline full of desert graphics on a brindle brown tee. Brown is the fall color most brands forget, and Devereux, out of Tempe, gets it right. Ours in <a href="/drops/brand-to-know-devereux-golf">the Devereux Brand to Know</a>.'),
 "F07": ("Fella Golf", "Sandbagger T-Shirt, Washed Cognac", "&euro;70 (~$81)",
   "https://fellagolf.com/products/sandbagger-t-shirt",
   'Fella, out of Amsterdam, washes this one in cognac, a rust that looks like October, and cuts it from 240gsm carbon-finished cotton with a soft, velvety hand. A vintage-style sandbagger graphic covers the back, and a Fella script is embroidered at the chest. More in <a href="/drops/fella-golf">our Fella post</a>.'),
 "F44": ("Fella Golf", "Double Bogey Boxer T-Shirt, Deep Navy", "&euro;70 (~$81)",
   "https://fellagolf.com/products/double-bogey-boxer-t-shirt",
   "Fella gets a second slot because the back graphic earns it: a bird squaring up to a golf bag in boxing gloves marked Double and Bogey. Deep navy, 220gsm carbon-finished cotton, embroidered logo up front."),
 "F12": ("Kingfisher Golf", "Kingfisher Athletics Tee, Heather Navy", "$40",
   "https://kingfisher-golf.com/products/kingfisher-athletics-tee",
   'Dallas brand Kingfisher prints a retro Kingfisher Athletics graphic on heather navy cotton, and it looks like a gym-class shirt from a better decade. At $40 it is one of the easiest buys here. Ours in <a href="/drops/brand-to-know-kingfisher-golf">the Kingfisher Brand to Know</a>.'),
 "F54": ("Odd Ritual", "ORGC Traditions T-Shirt, Navy", "R1,000 (~$57)",
   "https://oddritualgolf.com/products/ccc-traditions-t-shirt-navy",
   "Odd Ritual&rsquo;s second tee leans into the clubhouse: an Odd Ritual script across the front, an embroidered OR monogram and small icons on the chest, and a screen-printed emblem on the back, all on navy. Medium is the last size."),
 "F35": ("Sugarloaf Social Club", "Golf Technologies T-Shirt, Blue Spruce", "$44",
   "https://sugarloafsocialclub.com/products/golf-technologies-t-shirt",
   'Sugarloaf puts an oversized Golf Technologies graphic on the back of a blue spruce pocket tee, part spec sheet and part travel poster. Blue spruce is a muted green that suits the season. Ours in <a href="/drops/sugarloaf-autumn-layers-2026">Sugarloaf&rsquo;s Autumn Layers</a>.'),
 "F36": ("Walker Golf Things", "Cursive T-Shirt, Forest", "A$60 (~$40)",
   "https://www.walkergolfthings.com/products/cursive-t-shirt",
   'From Walker&rsquo;s fourth-quarter drop, which landed this week: an everyday 200gsm cotton tee in forest green with a small chest print and a 28cm gold Walker Golf Things script across the back. More in <a href="/drops/walker-golf-the-par-tec-drop">our Walker Par-Tec post</a>.'),
 "F08": ("Freddy Tyler Paul", "&lsquo;Spooky Arbys&rsquo; Tee, Faded Grey", "$36",
   "https://freddytylerpaul.com/products/lexapro-laced-iced-coffee-tee-copy",
   "Freddy Tyler Paul supplies the wild card and the only Halloween shirt here, made with Spooky Foodie: an &ldquo;I Miss The Meats&rdquo; memorial graphic for a Hollywood Arby&rsquo;s, printed on a soft-washed, garment-dyed faded grey tee. Wear it to the October scramble."),
}

SECTIONS = [
    ("The Long Sleeves", "long-sleeves", ["F04", "F09", "F10", "F15", "F17", "F19", "F26", "F58", "F30", "F32", "F34"],
     "<strong>Eleven long sleeves &middot; $30&ndash;~$121</strong>The fall shirt. A long-sleeve tee covers the cool first nine and the warm back nine without a layer to carry. Here they run from Criquet&rsquo;s slub pocket tee to Sounder&rsquo;s knitted stripe, with a heavy boxy Ghost, a garment-dyed Merrill and a Students tee with thermal sleeves sewn in."),
    ("Heavyweights and Blanks", "heavyweights", ["F01", "F16", "F18", "F13", "F24", "F20"],
     "<strong>Six tees &middot; $49.95&ndash;$80</strong>The quiet ones: heavy cotton, fall colors and branding kept to a small logo, an embossed spade or an embroidered patch. These go under a quarter-zip or a vest all season."),
    ("The Graphic Tees", "graphic-tees", ["F03", "F05", "F07", "F44", "F12", "F54", "F35", "F36", "F08"],
     "<strong>Nine tees &middot; $36&ndash;~$87</strong>Fall colors with something to say on the back: a desert state pack, a boxing bird, a sandbagger, a spec-sheet graphic and one Halloween wild card. Most of the art is on the back, so they read best walking off the tee."),
]

N = 26
GRID_CSS = ('<style>/*TGI-FALLTEES-GRID*/'
            '.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
            '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Book the tee time early enough and you might actually start in the sixties, but you will be finishing in the seventies and eighties. That is fall golf in Austin, and the shirt that handles both is a good tee, heavier cotton or a long sleeve, worn on its own or under a vest you can peel off at the turn.</p>
    <p>So this is twenty-six of them from independent golf brands, sorted three ways. The long sleeves cover the cool mornings. The heavyweights and blanks are the quiet tees that go under everything. The graphic tees carry the jokes, the art and one Halloween shirt. Most come in the browns, greens, navies and oatmeals that look right when the course starts to turn.</p>
    <h2 class="products-hdr btk-story-hdr">Start Here</h2>
    <p>If you buy one, make it Criquet&rsquo;s slub long sleeve. It is made by an Austin brand, it has the texture of a shirt you have owned for years, and it works from the first tee to dinner. Prices were read on each brand&rsquo;s own store on October 9, 2026, and everything was in stock in a medium.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Tees</span><span>26 from 23 brands</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$30&ndash;~$121</span></div>
      <div class="sidebar-detail"><span class="l">Long sleeves</span><span>11</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Criquet Slub Long Sleeve, $98</span></div>
      <div class="sidebar-detail"><span class="l">Best value</span><span>Puttwell Wordmark L/S, $30</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>October 9, 2026</span></div>
      <a href="#long-sleeves" class="sidebar-cta">See the tees &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#GolfTees</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What should I wear to play golf in the fall?",
     "A heavier cotton tee or a long-sleeve tee on its own, with a vest or quarter-zip for cold mornings. This guide has 26 fall tees from independent golf brands: eleven long sleeves, six heavyweights and blanks, and nine graphic tees."),
    ("Can you wear a T-shirt on a golf course?",
     "Many public and municipal courses allow T-shirts, while private clubs usually require a collar. Check the course's dress code before you go."),
    ("What are the best long-sleeve golf T-shirts?",
     "In this guide: Criquet's Cotton Slub Long Sleeve ($98) is our pick, Ghost Golf's 285gsm Clubhouse Rebels ($70) is the heaviest, Students' Laurence tee ($70) has waffle-thermal sleeves, and Puttwell's Wordmark L/S is the best value at $30."),
    ("What is a heavyweight T-shirt?",
     "A tee cut from thicker cotton, usually 220gsm and up, so it holds its shape and hangs more like a sweatshirt. In this guide, Students (280gsm), Ghost (285gsm), SLICE TOWN (253gsm), Manors and Fella (240gsm) are all heavyweight."),
    ("How much do fall golf tees cost?",
     "In this roundup, from $30 for Puttwell's Wordmark long sleeve to about $121 for Sounder's Fuzzy Pocket long sleeve. Most are between $40 and $80. Prices were read on October 9, 2026."),
]


def card(k, idx):
    brand, item, price, url, copy = P[k]
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
            f'<a href="{url}{U}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
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
            {"@type": "ListItem", "position": 3, "name": "Fall Golf T-Shirts", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    # Three brands appear twice by Lenny's call ("Keep all 26"); nothing else may repeat.
    brands = [H.unescape(P[k][0]) for k in ids]
    dup = {b for b in brands if brands.count(b) > 1}
    assert dup <= {"Fella Golf", "Odd Ritual", "Puttwell"}, dup
    for k in ids:
        assert len(FRN.get(k, [])) >= 1, k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Fall Golf T-Shirts</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Criquet, Malbon, Manors, Ghost, Sounder, Fella and more</span><span class="dot"></span>
    <span>26 tees &middot; in stock October 9, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A man in Criquet&rsquo;s natural slub long-sleeve pocket tee leaning on a green rail in front of cypress trees" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace('</head>', GRID_CSS + '</head>', 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
