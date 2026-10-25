#!/usr/bin/env python3
"""build-wwd-revisit.py — Brand Revisited: water when dry. 24 October 2026. Cloned from build-publicdrip-revisit.py.
Lenny: "let's do a brand revisited - Water when Dry" -> options sheet (29 in stock, Garden Club removed) -> "build the post with all the good images, the story about the brand with the full treatment".
Every in-stock pick from the sheet, colorways grouped: 21 cards, 80 frames. Size charts, mannequin composites and AI-looking model shots left out.
FACTS: waterwhendry.com products.json (USD, Oct 24 2026); research/water-when-dry/brand.md (About page, Garden Club page golf days,
Discord invite API 2,029 members, Trustpilot 4.7/106). No founder named anywhere, so none is named here. Paid club left out (Lenny removed it). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "water when dry Revisited: Fall/Winter 2026 and 21 Picks"
DESC = ("Four months after our first look at water when dry, the Orlando label built on a garden metaphor: the fall/winter 2026 utility pants "
        "and made-to-order pullovers, golf days, a 2,000-member Discord and 21 picks from $15 to $128.")
H1 = "Brand Revisited: water when dry, Tending the Garden Through Winter"
BC = "Brand Revisited: water when dry"
SLUG = "brand-revisited-water-when-dry"
IMG = "/images/water-when-dry-revisit"
SHOP = "https://waterwhendry.com/products/"
C = "water when dry"
P = {
 "pants": (C, "Utility Pants", "$108", "black-utility-pants",
   "The lead piece of fall/winter 2026, in black, brown or green crinkle nylon with two zip cargo pockets, toggle hems and the script logo at the knee. The brand&rsquo;s line: &ldquo;Light enough to forget you have it on.&rdquo; Our pick for a cold walking nine. S to 2XL in all three."),
 "cap": (C, "Utility Cap", "$48", "utility-cap-black",
   "A five-panel, unstructured cap with the stacked logo on the front and the icon on the left side. The product copy names golf outright: &ldquo;running, golfing, or nothing in particular.&rdquo; Black is $48; the burgundy with a green brim is made to order at $42 and ships November 20&ndash;30."),
 "univ": (C, "Blue University T-Shirt", "$58", "blue-university-t-shirt",
   "A washed blue tee with a new collegiate WWD graphic, distressed, with flowers growing out of the letters. Screen printed. The brand calls it &ldquo;the tee everybody asked for.&rdquo; XS to 2XL."),
 "socks": (C, "Cream Quarter Socks", "$15", "cream-quarter-socks",
   "One pair, cream, with the stacked logo and an embroidered icon on a cushioned sole. The cheapest way into the brand, and new this season."),
 "fw26po": (C, "Pullover, Fall/Winter 2026", "$128 (was $148)", "brown-pullover",
   "The brand&rsquo;s signature collared pullover in two new seasonal colorways, brown with a cream script or pink with a white one. 450gsm cotton, with the brand&rsquo;s description: &ldquo;Feels like a crewneck, wears like a rugby polo.&rdquo; Made to order, shipping November 20&ndash;30. XS to 2XL."),
 "wwdpo": (C, "WWD Pullover, V1 and V2", "$103 (was $148)", "internets-favorite-pullover-v2",
   "The original black pullover from fall 2024 and the green V2 from last November, both on sale. Same 450gsm cotton and white collar, with the oversized script across the front. Sizes are down to XS in black and XS or M in green, so move quickly."),
 "hoodie": (C, "Canopy Zip Hoodie", "$68 (was $98)", "black-zip-up-hoodie",
   "In our June post at $98, now $68. A 380gsm garment-dyed, stone-washed cotton zip hoodie with metal hardware and tonal embroidery, including &ldquo;Every flower&rdquo; at the hem. Charcoal or leaf, S to 2XL."),
 "fleece": (C, "Canopy Fleece, Riverbank", "$64 (was $128)", "sherpa-fleece-riverbank",
   "Heavyweight brown sherpa with blue contrast panels at the elbows and underarms, a half zip, a mesh liner and a kangaroo pocket. Half price, but only XS is left. Boxy, so size down for a closer fit."),
 "sweats": (C, "Charcoal Sweats", "$54 (was $108)", "charcoal-sweats",
   "The matching bottom for the Canopy hoodie: 380gsm garment-dyed cotton, straight leg and toggle hems. Half price, XS only."),
 "iconls": (C, "Icon Long Sleeve Tee, Black", "$34 (was $68)", "icon-ls-tee-plum",
   "A stone-washed 220gsm long sleeve with the icon on the chest and a big oval logo on the back. Half price, XS only."),
 "juniper": (C, "Logo Long Sleeve Tee, Juniper", "$34 (was $68)", "logo-ls-tee-juniper",
   "Deep green, stone-washed, with a small logo on the chest and the stacked wordmark across the back. Half price, XS only."),
 "camper": (C, "Camper Short, River", "$61 (was $88)", "camper-short-dusk",
   "The short that led our June post, now $61 in River: nylon with a mesh lining, eight pockets and a 7-inch inseam. The brand shot it on a golf course in the rain. True to size; only S and 2XL are left."),
 "tree": (C, "Treehugger Short, Green", "$48 (was $68)", "treehugger-short-green",
   "A cream lined mesh short printed with a green pine forest, a 6-inch inseam and an elastic waist. Every size from XS to 2XL."),
 "swim": (C, "Utility Swim Short", "$54 (was $78)", "utility-swim-short-black",
   "Quick-dry four-way stretch with a wave panel, 3M reflective piping and a hidden zip pocket. Black with teal, or terracotta. A 6-inch inseam, and a better summer golf short than most golf shorts. Low stock in both."),
 "tote": (C, "Carry-All Bag", "$18", "grocery-tote",
   "A teal woven tote that holds what four single-use plastic bags would, and carries up to 50 lbs. It&rsquo;s 24 by 15 by 6 inches, which is also about the size of a shoe-and-towel bag for the trunk."),
 "raglan": (C, "Uniform Raglan Tee", "$47 (was $68)", "raglan-tee",
   "A 280gsm French terry tee with black body, sage raglan sleeves and contrast flatlock stitching. The brand calls it the &ldquo;Everyday Uniform.&rdquo; S to 2XL."),
 "seeds": (C, "SEEDS Pocket Tee", "$30 (was $44)", "seeds-pocket-tee-blue",
   "The lighter base layer, in cobalt or maroon with a pocket and a bright green SEEDS tab. The brand&rsquo;s line: &ldquo;nothing extra. just right.&rdquo; S to 2XL in both."),
 "hands": (C, "Garden Hands Tee", "$29 (was $58)", "garden-hands-tee",
   "Black, with a big green gardening glove printed on the back. Half price in XS to M."),
 "grass": (C, "Greener Grass Tee, Soil", "$40 (was $58)", "greener-grass-tee-soil",
   "The back reads &ldquo;The grass is always greener where you water it.&rdquo; A brown stone-washed 220gsm tee, and the closest thing the brand has to a golf motto. XS, S or 2XL."),
 "rose": (C, "Logo Tee, Rose Clay", "$40 (was $58)", "logo-tee-rose-clay",
   "A dusty rose stone-washed tee with the wordmark on the back. XS, S, L or 2XL."),
 "greenhouse": (C, "Greenhouse Tee", "$29 (was $58)", "greenhouse-tee",
   "An off-white tee with an illustrated greenhouse in the woods across the front. Half price, XS only."),
}
SECTIONS = [
 ("New for Fall/Winter 2026", "fw26", ["pants","cap","univ","socks"],
  "<strong>Four pieces &middot; $15&ndash;$108</strong>The cold-weather drop that landed in early October. The brand&rsquo;s line for it: &ldquo;The garden goes quiet. The colors don&rsquo;t.&rdquo;"),
 ("The Pullover", "pullover", ["fw26po","wwdpo"],
  "<strong>Two cards, four colorways &middot; $103&ndash;$128</strong>The product the brand is known for, which its own copy calls &ldquo;the internet&rsquo;s favorite pullover.&rdquo;"),
 ("Layers", "layers", ["hoodie","fleece","sweats","iconls","juniper"],
  "<strong>Five pieces &middot; $34&ndash;$68</strong>Heavy cotton and sherpa from past seasons, most of it half price, some of it down to one size."),
 ("Shorts &amp; the Bag", "shorts", ["camper","tree","swim","tote"],
  "<strong>Four pieces &middot; $18&ndash;$61</strong>Three shorts for Texas, where shorts season runs into November, and an $18 tote."),
 ("Tees", "tees", ["raglan","seeds","hands","grass","rose","greenhouse"],
  "<strong>Six tees &middot; $29&ndash;$47</strong>Stone-washed heavy cotton, all on sale, with the garden on the back."),
]
N = 21
PQ = {
 "fw26": ("Water what matters. Tend to it often. Grow wherever you&rsquo;re planted.", "water when dry, on its homepage"),
 "pullover": ("Feels like a crewneck, wears like a rugby polo.", "water when dry, on the pullover"),
 "shorts": ("A round in Orlando, and whoever wants in. No handicap required and none checked.", "water when dry, on its golf days"),
}
CAP = "Photography &middot; water when dry"
BANDS = {
 "fw26": ("Fall/Winter 2026", "From the brand&rsquo;s own photos of the new drop.",
   [("lb-field","A man in a green puffer vest and black utility pants standing in a field at sunset","The Utility Pants, in a field"),
    ("lb-pantsdetail","Close-up of black utility pants with the script logo at the knee on a dirt path","The script at the knee"),
    ("lb-pantpane","Green utility pants laid flat on concrete","Green, on concrete")]),
 "pullover": ("The pullover, out in the world", "From the brand&rsquo;s shoots for the original and the new colorways.",
   [("lb-pullovers","The brown and pink fall/winter 2026 pullovers folded on concrete","Brown and pink, made to order"),
    ("lb-stairs","A man in the black pullover and grey shorts walking down concrete steps","The original, in black"),
    ("lb-walk","A man in the black pullover seen from behind, with the script across the back","From the back")]),
 "shorts": ("On the course", "The brand shot the Camper Short on a golf course in the rain.",
   [("lb-pond","A golfer in a teal cap and the Camper Short waving a towel on a club by a pond","The Camper Short, by the pond"),
    ("lb-putt","A golfer in the Camper Short bending to tee up a ball under palm trees","Teeing it up"),
    ("lb-feet","Looking down at grey running shoes and shorts on a putting green next to the hole","On the green")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we first wrote about <a href="/drops/water-when-dry-the-garden-metaphor-that-actually-works" style="border-bottom:1px solid var(--ink)">water when dry</a> in June, we called it the garden metaphor that actually works: colorways named River, Leaf, Soil and Blackberry, a brand voice that should tip into self-help and somehow doesn&rsquo;t, and eight pieces from $15 to $128. Four months on, the metaphor is still doing all the work, and there&rsquo;s more garden than ever.</p>
    <p><strong>Who they are.</strong> water when dry is a small label out of Orlando, Florida. Its website shows a live Orlando clock in the header, and its golf days are rounds in Orlando. It doesn&rsquo;t put a founder&rsquo;s name on anything. Its oldest products date to early 2023, and the whole idea fits on one line from its About page: &ldquo;Like any garden, what you tend to will grow.&rdquo; The brand writes its name in lowercase, and so do we.</p>
    <p><strong>The new drop is built for cold weather.</strong> Fall/winter 2026 arrived in early October with a homepage line we liked: &ldquo;The garden goes quiet. The colors don&rsquo;t.&rdquo; The lead piece is a crinkle-nylon Utility Pant in black, brown and green with zip cargo pockets and toggle hems, and the brand shot it in a field at sunset with a puffer vest, which is exactly how we&rsquo;d wear it for a November nine. A five-panel Utility Cap, a blue collegiate tee with flowers growing out of the letters, and $15 socks round it out.</p>
    <p><strong>The pullover is the product everybody knows.</strong> The collared pullover, 450gsm cotton with a white collar and an oversized script across the front, first came out in fall 2024. Its own product copy calls it &ldquo;the internet&rsquo;s favorite pullover,&rdquo; and one Trustpilot reviewer says he&rsquo;s seen it on celebrities, influencers and sneakerheads. This fall it comes in brown and pink, made to order and shipping November 20&ndash;30. The black original and the green V2 are on sale, but only in a couple of sizes.</p>
    <p><strong>There&rsquo;s more golf than you&rsquo;d guess.</strong> water when dry isn&rsquo;t a golf brand, but it keeps ending up on the course. The Camper Short, which led our June post, was shot on a golf course in the rain, towel on a club by the pond. The Utility Cap copy names golfing outright. And the brand runs golf days in Orlando, open to anyone: &ldquo;No handicap required and none checked.&rdquo; That&rsquo;s the most TGI sentence any brand has written this year.</p>
    <p><strong>The community is the brand.</strong> Its Discord server, The Garden, has grown past 2,000 members. Members post what landed in the mail, what&rsquo;s on their feet, their dogs and their records, and get early access to drops. The brand&rsquo;s homepage runs a live feed from it. Customers on Trustpilot give the brand 4.7 out of 5 across more than 100 reviews.</p>
    <p><strong>What hasn&rsquo;t changed:</strong> nothing costs more than $128, the colors still come from a garden, and the voice is still wholesome without being corny. Half the store is on sale right now, mostly the sizes at the ends of the run. If you&rsquo;re buying one thing, get the Utility Pants. If you&rsquo;re buying two, add a pullover before the made-to-order window closes.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Since June</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Orlando, FL</span></div>
      <div class="sidebar-detail"><span class="l">Oldest pieces</span><span>Early 2023</span></div>
      <div class="sidebar-detail"><span class="l">New drop</span><span>Fall/Winter 2026, Oct</span></div>
      <div class="sidebar-detail"><span class="l">Made to order</span><span>Ships Nov 20&ndash;30</span></div>
      <div class="sidebar-detail"><span class="l">The Garden</span><span>2,000+ on Discord</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$15&ndash;$128</span></div>
      <div class="sidebar-detail"><span class="l">In the post</span><span>21 picks</span></div>
      <div class="hashtags">
        <span class="hashtag">#WaterWhenDry</span>
        <span class="hashtag">#Orlando</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">How It Fits</div>
  <h2 class="products-hdr" id="fit">Sizing, Fabrics and Where to Start</h2>
  <p class="cat-kicker">Most of the tees and layers are a boxy fit, and the brand suggests sizing down on the Canopy Fleece if you want it closer. The tees are 220gsm stone-washed cotton (the SEEDS pocket tee is lighter, the Raglan is a heavier 280gsm French terry), and the hoodie and sweats are 380gsm. The Camper Short fits true to size with a 7-inch inseam; the swim and Treehugger shorts are 6 inches. The made-to-order pullovers and burgundy cap ship November 20&ndash;30, and in-stock orders take one to two weeks to process. If you&rsquo;ve never worn the brand, start with the $15 socks or a $30 SEEDS tee.</p>
</section>
"""
FAQ = [
 ("Where is water when dry based?", "Orlando, Florida. Its website header shows an Orlando clock, and the brand runs its golf days in Orlando."),
 ("What is new from water when dry for fall/winter 2026?", "Utility Pants in black, brown and green ($108), a Utility Cap ($48, or $42 for the made-to-order burgundy), a Blue University T-Shirt ($58), Cream Quarter Socks ($15), and the collared pullover in brown and pink, made to order at $128 and shipping November 20 to 30, 2026."),
 ("What is the water when dry pullover?", "A 450gsm cotton collared pullover with a white collar and an oversized script logo, first released in fall 2024. The brand describes it as feeling like a crewneck and wearing like a rugby polo."),
 ("Does water when dry run golf events?", "Yes. It runs golf days in Orlando that are open to anyone, with no handicap required."),
 ("Does water when dry run true to size?", "The Camper Short fits true to size. Most tees, hoodies and the Canopy Fleece are a boxy fit, and the brand suggests sizing down on the fleece for a closer fit."),
]
_LB = [("lb-cart","Looking over a golfer&rsquo;s shoulder in a black Utility Cap toward a golf cart","The Utility Cap, at the cart"),
 ("lb-seated","A man in the black pullover sitting on a concrete ledge in front of a wall of vines","The original pullover"),
 ("lb-sock","A cream logo sock and a green-and-cream running shoe on a tree root","The socks"),
 ("lb-fleecefig","Close-up of brown sherpa fleece with a blue contrast panel","The Canopy Fleece, up close"),
 ("lb-soil","A man in a cap buried to his face in soil, from the brand&rsquo;s About page","From the About page"),
 ("lb-everyflower","Close-up of &ldquo;Every flower&rdquo; embroidered tone on tone on the black Canopy Zip Hoodie","&ldquo;Every flower,&rdquo; on the hoodie")]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _LB)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">Since June, in Photos</h2>
  <p class="cat-kicker"><strong>From water when dry&rsquo;s site &middot; six photos</strong>The new drop, the pullover and the brand on a golf course.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/water-when-dry/frames.json").read_text())
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
    <span>Brand Revisited &middot; Orlando &middot; First covered June 15, 2026</span><span class="dot"></span>
    <span>21 picks &middot; prices checked October 24, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three water when dry photos: a golfer in the Camper Short by a pond, a golfer in the Utility Cap at a golf cart, and a man in the black collared pullover" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Sounder", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
