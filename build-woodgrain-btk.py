#!/usr/bin/env python3
"""build-woodgrain-btk.py — Brand to Know: Woodgrain Golf. Cloned from build-no-dirt-golf-btk.py. 12 October 2026.
Lenny: "let's do a brand to know https://woodgrain.golf/", then "let's go with all 14".
FACTS: woodgrain.golf products JSON (research/woodgrain/products-2026-10-12.json), home, Brand, Contact and Shipping pages,
read October 12, 2026. Founders sign the Brand page "Christian & Em"; no surnames anywhere, none invented. Quotes verbatim
from the Brand page. One lookbook image on the site is AI-generated (file "ChatGPTImage...") and is not used.
PHOTOS: Woodgrain's own product and lookbook images (frames in research/woodgrain/frames.json). No tight crotch crops.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Woodgrain Golf: Double Pleats and the ’90s Golf Look"
DESC = ("Brand to Know: Woodgrain Golf, the New York label bringing back wide double pleated trousers, cable knits and "
        "old-school caps. All 14 pieces from Collection 4, from $49 hats to $180 trousers.")
H1 = "Brand to Know: Woodgrain Golf &mdash; How Golf Used to Look"
BC = "Woodgrain Golf"
SLUG = "brand-to-know-woodgrain-golf"
IMG = "/images/woodgrain"
SHOP = "https://woodgrain.golf/products/"
A = "Woodgrain Golf"
TR = "relaxed-double-pleated-trouser"
SH = "the-double-pleated-short-"
P = {
 # Trousers
 TR: (A, "Legacy Double Pleated Trouser, Cream", "$180", TR,
   "The reason to know the brand. A wide-leg trouser with two front pleats on each side, cut from 100% cotton and built to sit high and fall straight, the way golf trousers did in old tournament photos. Cream is the one we would buy first: it is the color of the brand&rsquo;s lookbook and it makes a navy knit or a striped polo look right. Only M and L were left when we checked."),
 TR+"-tan": (A, "Legacy Double Pleated Trouser, Tan", "$180", TR+"-tan",
   "The same Legacy trouser in tan, a khaki that suits a dry Austin fairway in October. Woodgrain shot it with a brown long-sleeve polo and an old leather bag, and the whole look could pass for 1992. Same 100% cotton, same deep pleats."),
 TR+"-chocolate-brown": (A, "Legacy Double Pleated Trouser, Chocolate Brown", "$180", TR+"-chocolate-brown",
   "Chocolate brown is the fall color here and the least expected one on a golf course. With a cream knit or a sand polo it looks like it came out of a thrift store in the best possible way. M and L in stock."),
 TR+"-black": (A, "Legacy Double Pleated Trouser, Black", "$180", TR+"-black",
   "Black is the version for dinner after the round. The wide leg and pleats keep it from looking like a suit trouser, and it works with the black mock neck below for a head-to-toe dark look."),
 # Shorts
 SH+"cream": (A, "Double Pleated Short, Cream", "$130", SH+"cream",
   "The warm-weather version of the trouser: 100% cotton, two front pleats and a relaxed leg that stops above the knee. Woodgrain says the cotton is meant to get better with wear. Every size from XS to 2XL was in stock, which makes the shorts the easiest way into the brand right now."),
 SH+"tan": (A, "Double Pleated Short, Tan", "$130", SH+"tan",
   "Tan with a cream polo is the most classic pairing on the page. These are the shorts for a summer muni round in Austin, where trousers are not an option from May to September."),
 SH+"cream-copy": (A, "Double Pleated Short, Chocolate Brown", "$130", SH+"cream-copy",
   "Chocolate brown, shot with a plaid short-sleeve shirt and white socks pulled up. It is the most confident of the four, and the one we would pick for a fall scramble."),
 SH+"black": (A, "Double Pleated Short, Black", "$130", SH+"black",
   "Black shorts with a black polo, belted, socks up. The pleats keep it relaxed. All six sizes in stock."),
 # Tops and hats
 "the-cable-knit-sweater-vest-black": (A, "Cable Knit Sweater Vest, Black", "$95", "the-cable-knit-sweater-vest-black",
   "A 100% cotton cable-knit sweater vest with a V-neck, a relaxed fit and a small WG embroidered on the chest. Over a white tee with cream trousers, it is the most &rsquo;90s piece in the collection. Only XL was left."),
 "the-cable-knit-sweater-vest-black-copy": (A, "Mock Neck, Black", "$85", "the-cable-knit-sweater-vest-black-copy",
   "A heavy 280 GSM mock neck in a cotton and Sorona blend, slightly oversized, with the Woodgrain crest label at the hem. It has the weight of a good sweatshirt and the shape of a tee. Down to 3XL when we checked."),
 "nylon-vest-tan": (A, "Nylon Vest, Tan", "$98", "nylon-vest-tan",
   "A down-filled vest with a recycled polyester shell, a stand collar, a two-way zip and angled zip pockets. The crest on the chest is tonal, so it reads as a plain tan vest from a few feet away. It is the layer for a cold first tee in January. L and XL in stock."),
 "script-hat": (A, "Script Hat", "$49", "script-hat",
   "A black cotton cap with Woodgrain in white script across the front and &ldquo;Est. in New York&rdquo; on the side. Structured, with a semi-curved brim and a leather strap with a metal buckle at the back."),
 "script-hat-copy": (A, "Crest Hat", "$49", "script-hat-copy",
   "The crest cap, shown in the brand&rsquo;s photos with a cream crown, a brown brim and the Woodgrain crest embroidered on the front. It is the hat from most of the lookbook, with a snapback closure."),
 "wool-hat": (A, "Wool Hat", "$49", "wool-hat",
   "A five-panel cap in brown plaid wool with a 3D WG on the front, woodgrain-style stitching on the side and a dark green lining printed with &ldquo;Swing smooth, Dress sharp.&rdquo; The best of the three hats, and the earliest piece still listed in the shop."),
}
SECTIONS = [
 ("The Legacy Double Pleated Trouser", "trousers", [TR, TR+"-tan", TR+"-chocolate-brown", TR+"-black"],
  "<strong>Four picks &middot; $180</strong>One trouser in four colors: 100% cotton, a wide leg and two deep pleats on each side. It is the piece the brand is built around."),
 ("The Double Pleated Short", "shorts", [SH+"cream", SH+"tan", SH+"cream-copy", SH+"black"],
  "<strong>Four picks &middot; $130</strong>The same idea, cut above the knee in 100% cotton. Every size from XS to 2XL was in stock in all four colors."),
 ("Tops and Hats", "tops", ["the-cable-knit-sweater-vest-black", "the-cable-knit-sweater-vest-black-copy", "nylon-vest-tan", "script-hat", "script-hat-copy", "wool-hat"],
  "<strong>Six picks &middot; $49&ndash;$98</strong>A cable-knit vest, a heavy mock neck, a down vest and three caps. Several tops are down to one or two sizes."),
]
N = 14
PQ = {
 "trousers": ("We wanted to make golf clothes that we actually wanted to wear.", "Christian &amp; Em, Woodgrain Golf"),
 "tops": ("Woodgrain is our take on where golf style should be going by looking back at where it came from.", "Christian &amp; Em, Woodgrain Golf"),
}
CAP = "Photography &middot; Woodgrain Golf&rsquo;s own"
BANDS = {
 "trousers": (CAP, "From the Woodgrain lookbook: wood paneling, an old leather bag and a lot of pleats.", [("band-1","A golfer in a striped polo and cream double pleated shorts hitting a chip shot from the rough","The chip"),("band-2","A golfer in a sand knit and chocolate brown trousers sitting in a wooden chair","The chair"),("band-3","A hand holding a cream and brown Woodgrain crest cap in a wood-paneled room","The cap")]),
 "tops": (CAP, "Out on the course in the vest and caps.", [("band-4","A golfer in the tan Woodgrain nylon vest on a fairway lined with pine trees","The vest"),("band-5","A golfer in a black Woodgrain script cap and tan vest mid-swing","The swing"),("band-6","A golfer in the brown plaid Woodgrain wool hat standing in a field","The wool hat")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Woodgrain Golf is two people in New York making the golf clothes from old photos: wide trousers with double pleats, cable-knit vests, heavy knits and caps with real hardware on the back. Their pitch is simple. Somewhere along the way golf clothes got tighter, brighter and more technical, and Woodgrain wants the older shapes back, cut to actually play in.</p>
    <p>The Legacy Double Pleated Trouser is the piece that makes the case. It is 100% cotton, cut wide, with two deep pleats on each side, and it hangs the way trousers did before every golf pant became a slim five-pocket. In cream with a navy knit, it is the best-looking thing on the page. The pleated shorts do the same job for an Austin summer, and at $130 in every size they are the easiest place to start. The hats are $49, and the brown plaid wool cap with &ldquo;Swing smooth, Dress sharp&rdquo; printed inside is the one we would wear first.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Woodgrain started in New York with two founders, who sign the brand&rsquo;s story &ldquo;Christian &amp; Em.&rdquo; They write that they both grew up around golf and wanted pieces with &ldquo;that older feel&rdquo; that still made sense to golf in: &ldquo;oversized polos, wider trousers, knitwear, old hats.&rdquo; The current release is Collection 4, and the brand sells in numbered drops with early access by text. Orders ship in seven to nine business days, and US shipping is free over $100. All 14 pieces below were in stock on woodgrain.golf on October 12, 2026, several of them in only one or two sizes.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>New York</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Christian &amp; Em</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Double pleated trousers</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>Collection 4</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$49&ndash;$180</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Legacy Trouser, Cream, $180</span></div>
      <a href="https://woodgrain.golf/" target="_blank" rel="noopener" class="sidebar-cta">Visit Woodgrain Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#WoodgrainGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#DoublePleats</span>
        <span class="hashtag">#VintageGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Woodgrain Golf from?", "New York. The brand says it started there with its two founders."),
 ("Who founded Woodgrain Golf?", "Two founders who sign the brand's story \"Christian & Em.\" The site does not give their surnames."),
 ("What is the Legacy Double Pleated Trouser?", "Woodgrain's main piece: a wide-leg, double pleated golf trouser in 100% cotton. It was $180 in cream, tan, chocolate brown and black on October 12, 2026, with only sizes M and L in stock."),
 ("How much does Woodgrain Golf cost?", "On October 12, 2026, hats were $49, the mock neck $85, the cable-knit vest $95, the nylon vest $98, the double pleated shorts $130 and the Legacy trousers $180. US shipping is free over $100."),
 ("How long does Woodgrain take to ship?", "The brand says orders are processed and shipped within seven to nine business days."),
]
FRN = json.loads((ROOT / "research/woodgrain/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-WG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-12", "dateModified": "2026-10-12",
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Vintage-inspired golf clothes &middot; New York</span><span class="dot"></span>
    <span>14 picks &middot; every piece in stock, checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Three Woodgrain Golf photos on a course lined with pines: a golfer in the black cable knit sweater vest, the tan nylon vest and the black mock neck" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
