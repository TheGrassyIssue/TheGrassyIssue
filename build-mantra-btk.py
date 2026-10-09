#!/usr/bin/env python3
"""build-mantra-btk.py — Brand to Know: Mantra Golf. Cloned from build-rookline-btk.py. 9 October 2026.
Lenny: "let's do a brand to know Mantra golf-https://mantragolf.com/ Do a good deep dive into their new collection and
then essentials." From mantra-options.html he picked "My 20 (Recommended)": 12 from the Sonoran Desert collection
(live 8-9 Oct 2026) and 8 essentials.
FACTS: mantragolf.com products JSON, Story and Sustainability pages, read 9 Oct 2026 (research/mantra/brand.json).
Founders and dates from the brand's own Story page and its 2019/2024 press releases. Quotes are verbatim from a Q&A
with Dom Natalizio on the Swap blog (a commerce-software company, not a golf publication). Mantra published no
story text for the Sonoran Desert collection, so nothing here claims an inspiration beyond the Arizona shoot itself.
Pique fabric is not listed on the new product pages, so the copy describes it without a fiber percentage.
PHOTOS: Mantra's own product and campaign images (Arizona shoot, 23-24 Sep 2026; Redwoods for the essentials).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Mantra Golf: The Sonoran Desert Collection and the Essentials"
DESC = ("Brand to Know: Mantra Golf, the San Francisco label behind the Mantra Collar polo. The new Sonoran Desert "
        "collection, heavyweight Legacy fleece and the everyday essentials, with prices.")
H1 = "Brand to Know: Mantra Golf &mdash; The Sonoran Desert Collection and the Essentials"
BC = "Mantra Golf"
SLUG = "brand-to-know-mantra-golf"
IMG = "/images/mantra"
SHOP = "https://mantragolf.com/products/"
A = "Mantra"
P = {
 # Sonoran Desert: the layers
 "m01": (A, "Legacy Crewneck Pullover, Birdie Embroidery", "$168", "mens-legacy-crewneck-pullover-birdie-embroidery",
   "The standout of the drop and a limited edition: a cream heavyweight cotton fleece crewneck covered in hand-drawn embroidery of North American birds. It is cut relaxed and oversized with cuffed sleeves and a Mantra script at the chest. Mantra shot it among the saguaros at dusk, and it is the piece people will ask about."),
 "m02": (A, "Legacy Crewneck Pullover, Woods", "$138", "mens-legacy-crewneck-pullover-woods",
   "This is the everyday version of Mantra&rsquo;s first heavyweight fleece: 85% cotton and 15% polyester, relaxed and a little long, with cuffed sleeves, the Mantra script on the chest and the Blue-Footed Booby on the sleeve. Woods is a deep brown that sits with every pair of khakis you own."),
 "m03": (A, "Legacy Quarter Zip, Sea Salt", "$158", "mens-legacy-quarter-zip-sea-salt",
   "The same heavyweight fleece with a zip point collar, so it works as the outer layer on a cold first tee and opens up by the turn. Sea salt is an off-white that looks sharp over a darker polo. Relaxed and oversized, cuffed sleeves, booby on the arm."),
 "m23": (A, "Signature Mock Neck L/S, Prickly Pear", "$98", "signature-mock-neck-ls-prickly-pear",
   "Mantra&rsquo;s Signature mock is cut from 100% Peruvian Pima cotton interlock, a structured, weighted knit with natural stretch. In long sleeves and prickly pear, a deep cactus-fruit red, it is the most fall color in the collection, with Mantra embroidered at the chest and the booby on the sleeve."),
 "m17": (A, "Signature T-Shirt, Sonoran Desert", "$68", "signature-t-shirt-sonoran-desert",
   "This tee is the souvenir of the collection. It uses the same Pima cotton interlock as the mock, with a small Mantra embroidery up front and a Sonoran Desert print across the back: saguaro, mesa, sun and the words Mantra Golf, Sonoran Desert. It is the easiest way into the drop."),
 # Sonoran Desert: the polos
 "m06": (A, "Pique Mock Neck, Sand Trap", "$98", "mens-pique-mock-neck-sand-trap",
   "Mantra&rsquo;s pique line arrived in May with its Heritage collection, and the Sonoran drop gives it desert prints. Sand Trap is a contour-line pattern in sandy tones, on a relaxed pique mock with a short placket. Mantra photographed it standing in a greenside bunker, which is the joke."),
 "m08": (A, "Pique Polo L/S, Clay", "$108", "mens-pique-polo-ls-clay",
   "Mantra cuts this long-sleeve pique polo with a classic point collar and a relaxed body, in clay, a warm earth tone lifted straight from the desert floor. It is the polo we would wear on a cool morning when a fleece is too much."),
 "m09": (A, "Pique Polo L/S, Checkerboard", "$108", "mens-pique-polo-ls-checkerboard",
   "The checkerboard version swaps the solid for a small brown check with a solid collar and placket. Mantra shot it mid-swing under a pink dusk sky, and it reads like something from a 1970s pro shop in the best way."),
 "m10": (A, "Pique Polo, Spectrum", "$98", "mens-pique-polo-spectrum",
   "This short-sleeve pique polo comes in Spectrum, a fine geometric pattern on a pale ground with a solid cream collar. It is the polo in the collection that still works in an Austin October afternoon."),
 "m25": (A, "Pique Polo, Agave", "$98", "pique-polo-agave",
   "Agave is the green of the collection, a muted cactus color on a relaxed short-sleeve pique polo with a point collar. It is the quietest pattern-free option in the drop and the one that goes with everything."),
 "m13": (A, "Catalyst Polo, Mantra Collar, Spectrum", "$88", "catalyst-polo-mantra-collar-spectrum",
   "The polo Mantra started with in 2019, in the new Spectrum print. The Mantra Collar is a short stand-up band with a short placket and no fold-down points, so it looks as clean at dinner as it does on the course. The Catalyst is a recycled-polyester stretch knit with UPF 50+ and a loop at the placket for sunglasses."),
 "m16": (A, "Catalyst Polo, Mantra Collar, Clay", "$88", "catalyst-polo-mantra-collar-clay",
   "The same performance Catalyst in a solid clay, for the golfer who wants the stand collar without a print. Four-way stretch, moisture wicking, a curved hem that works tucked or untucked, and the Mantra loop for sunglasses."),
 # The essentials
 "m27": (A, "Catalyst Polo, Mantra Collar, Woods", "$88", "catalyst-polo-mantra-collar-woods",
   "If you buy one Mantra piece, buy this. The flagship Catalyst in woods brown with the stand-up Mantra Collar: 89% recycled polyester and 11% spandex, UPF 50+, four-way stretch, an athletic fit and the sunglasses loop at the placket. It has thousands of reviews on Mantra&rsquo;s own site, and the collar is why."),
 "m30": (A, "Catalyst Polo, Point Collar, Topo III", "$88", "catalyst-polo-point-collar-topo-iii",
   "The same Catalyst body with a classic point collar, added in 2023 for the golfer who wants a traditional look. Topo III is a topographic contour print, a quiet nod to the landscapes Mantra builds its collections around."),
 "m31": (A, "Catalyst Polo L/S, Mantra Collar, Woods", "$98", "catalyst-polo-ls-mantra-collar-woods",
   "The long-sleeve Catalyst, which is the one we would actually wear from October to March. Same recycled stretch knit, same stand collar, same UPF 50+, in woods brown. It layers under a quarter zip without bunching."),
 "m34": (A, "Signature Mock Neck, Woods", "$88", "signature-mock-neck-woods",
   "Mantra cuts the short-sleeve Signature mock from 100% Peruvian Pima cotton interlock, structured and weighted with natural stretch. It sits between a polo and a tee, and in woods it pairs with the long-sleeve Catalyst as the core of a brown fall kit."),
 "m38": (A, "Essential Pullover, Ocean", "$118", "essential-pullover-ocean",
   "Mantra makes its mid-layer quarter zip in a midweight French terry of Peruvian Pima cotton and eucalyptus Tencel with a little stretch. It breathes, it has a curved hem and the sunglasses loop, and ocean is a deep navy that goes with every polo above."),
 "m40": (A, "Essential Hoodie, Obsidian", "$78", "essential-hoodie-obsidian",
   "The same Pima and Tencel French terry as a hoodie, with raglan sleeves, a cordless hood, a hidden kangaroo pouch and a small pocket Mantra calls the Mulligan, sized for a golf ball. It is marked down from $128 to $78 right now, which makes it the best value on the page."),
 "m42": (A, "Crossover Trouser, Sand", "$128", "crossover-pant-32-inseam-sand",
   "A golf trouser in cotton, recycled nylon and spandex with a flex waistband, silicone grippers that keep a polo tucked in, a zip security pocket and a loop for a tee. Classic fit, 32 and 34 inch inseams, in a sand that matches the whole Sonoran palette."),
 "m48": (A, "Rain Jacket, Black Sands", "$198", "mens-rain-jacket-black-sands",
   "The weather layer: a water-repelling nylon shell with micro-mesh insulation, a vented back flap, a hood that stows away and zip pockets, cut relaxed enough to swing in. Black Sands is the one color, and it is the piece that keeps a wet winter round on the calendar."),
}
SECTIONS = [
 ("Sonoran Desert: The Layers", "sonoran-layers", ["m01","m02","m03","m23","m17"],
  "<strong>Five picks &middot; $68&ndash;$168</strong>The Sonoran Desert collection went live on October 8 and 9, shot in Arizona in late September. Its headline is Mantra&rsquo;s first heavyweight fleece, the Legacy crewneck and quarter zip, plus long-sleeve Pima mocks and a desert graphic tee."),
 ("Sonoran Desert: The Polos", "sonoran-polos", ["m06","m08","m09","m10","m25","m13","m16"],
  "<strong>Seven picks &middot; $88&ndash;$108</strong>The prints carry the desert: Sand Trap contours, Spectrum geometry, a brown checkerboard, and solid clay and agave. Five are the relaxed pique polos Mantra introduced in May; two are the original Catalyst with the stand-up Mantra Collar."),
 ("The Essentials", "essentials", ["m27","m30","m31","m34","m38","m40","m42","m48"],
  "<strong>Eight picks &middot; $78&ndash;$198</strong>The pieces Mantra keeps in stock season after season. Start with the Catalyst polo, then add the long-sleeve version, the Pima mock, the Essential layers, the Crossover trouser and a rain shell."),
]
N = 20
PQ = {
 "sonoran-polos": ("Our flagship product is the polo, and we call it the most versatile polo on the planet.", "Dom Natalizio, Mantra co-founder, in a Q&amp;A with Swap"),
 "essentials": ("I wore an athletic polo to the office and would usually turn around and wear that same polo on the weekend.", "Dom Natalizio, on where Mantra started"),
}
CAP = "Photography &middot; Mantra&rsquo;s own"
BANDS = {
 "sonoran-layers": (CAP, "Mantra shot the Sonoran Desert collection in Arizona in late September.", [("band-1","A golfer in a brown long-sleeve mock neck holding the flagstick among saguaros","The flag"),("band-2","A golfer in the Birdie Embroidery crewneck leaning on an iron at dusk","Birdie crewneck"),("band-3","A golfer finishing his swing under a pink dusk sky","Dusk")]),
 "sonoran-polos": (CAP, "Desert prints, shot where they were drawn from.", [("band-4","A golfer in the Sand Trap pique mock standing in a greenside bunker","Sand Trap"),("band-6","Two golfers walking with carry bags below a red mesa","The walk"),("band-9","A golfer with a carry bag in a redwood forest clearing","The essentials")]),
 "essentials": (CAP, "The essentials come from Mantra&rsquo;s Redwoods shoot.", [("band-7","A golfer in a brown Signature mock in a redwood forest","Woods"),("band-8","A golfer in a green Catalyst polo finishing his swing","The Catalyst"),("band-10","A golfer on a sunlit fairway among redwoods","Redwoods")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We like Mantra because it makes golf clothes that do not look like golf clothes until you need them to. The whole brand started with one problem: co-founder Dom Natalizio wore an athletic polo to the office, then wore it again on the weekend, and it never looked right off the course. His answer was the Mantra Collar, a short stand-up band with no fold-down points, and it is still the reason to know the brand. For a muni player, the Catalyst is the shirt you wear to the course, through eighteen and on to dinner without changing.</p>
    <p>What keeps it interesting is the travel. Every season Mantra builds a collection around a landscape, from the Scottish Highlands and the Norwegian fjords to the redwoods, and the new one is the Sonoran Desert. It is the best fall drop the brand has made, mostly because of the Legacy fleece, its first heavyweight layer, and a long-sleeve pique polo in a checkerboard that looks borrowed from a 1970s pro shop. The colors are clay, prickly pear, agave and sand, which suit an Austin winter as well as they suit Arizona.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Mantra was founded in San Francisco in 2019 by Dom Natalizio and Ashley Revay, a former high school golfer who designs the women&rsquo;s line Mantra added in 2025. Its stated mission is to connect people to nature through golf: the brand is Climate Neutral certified, uses Bluesign dyes and gives at least 1% of sales to conservation through its Impact Fund. The Catalyst is made from recycled polyester in a WRAP Gold-certified factory in Vietnam, and the tees and mocks are Peruvian Pima cotton. All 20 pieces below were in stock in a medium on mantragolf.com on October 9, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>San Francisco</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2019, by Dom Natalizio and Ashley Revay</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>The Mantra Collar polo</span></div>
      <div class="sidebar-detail"><span class="l">New</span><span>Sonoran Desert collection</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$68&ndash;$198</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Catalyst Polo, Woods, $88</span></div>
      <a href="https://mantragolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Mantra &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MantraGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#FallGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Mantra Golf from?", "San Francisco. Mantra was founded there in 2019 by Dom Natalizio and Ashley Revay."),
 ("What is the Mantra Collar?", "The stand-up band collar on Mantra's Catalyst Polo: a short placket and no fold-down points, so the polo looks clean off the course. It has been the brand's signature since 2019; a point-collar Catalyst was added in 2023."),
 ("What is Mantra's Sonoran Desert collection?", "Mantra's fall 2026 collection, released October 8-9, 2026 and shot in Arizona. It includes the brand's first heavyweight fleece, the Legacy Crewneck ($138, $168 for the Birdie Embroidery edition) and Legacy Quarter Zip ($158), plus pique polos and mocks, Catalyst polos, Signature mocks and a Sonoran Desert graphic tee."),
 ("How much does Mantra Golf cost?", "On October 9, 2026 the Catalyst Polo was $88, pique polos $98 to $108, the Essential Pullover $118, the Crossover Trouser $128 and the Rain Jacket $198. The Essential Hoodie was marked down to $78."),
 ("Is Mantra Golf sustainable?", "Mantra is Climate Neutral certified, uses Bluesign dye methods, makes the Catalyst from recycled polyester and gives at least 1% of sales to conservation through its Impact Fund."),
]
FRN = {f"m{int(k):02d}": v for k, v in json.loads((ROOT / "research/mantra/frames.json").read_text()).items()}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-MANTRA-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-09", "dateModified": "2026-10-09",
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>San Francisco golf apparel</span><span class="dot"></span>
    <span>20 picks &middot; all in stock, checked October 9, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Mantra golfers walking through Sonoran Desert scrub below a saguaro and a rocky ridge" fetchpriority="high" /></div></div>
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
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
