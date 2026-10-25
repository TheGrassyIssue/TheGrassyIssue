#!/usr/bin/env python3
"""build-mount-tee-btk.py — Brand to Know: Mount Tee Golf. Cloned from build-lazyface-btk.py. 14 October 2026.
Lenny: "Let's do a brand to know- https://mountteegolf.com.au/", then "let's finish up the mount tee post" (all 39 in stock).
FACTS: mountteegolf.com.au About page (verbatim quotes), product pages and Summer '24 "Perfect Playing Partner" collection page,
read Oct 14, 2026. Founder first names (Jeremy, Joel, Tom) come only from one third-party newsletter, so the post says
"three friends" and does not print names. No founding year is published (earliest products date from late 2022), no
stockists, no collaborations; "Partners" is the brand's own collection. Prices in AUD with ~USD at x0.70.
PHOTOS: Mount Tee's own, from its Shopify CDN (research/mount-tee/frame.py). Hero: Woodlands Knit Polo, Pine Green.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Mount Tee Golf: Knit Polos, Pleats and Plush Headcovers From Melbourne"
DESC = ("Brand to Know: Mount Tee Golf, three friends in Melbourne who think golf should celebrate individuality. "
        "Waffle and knit polos, pleated shorts, plush and tartan headcovers. All 39 pieces in stock, A$12 to A$130.")
H1 = "Brand to Know: Mount Tee Golf &mdash; Not Everybody Has to Look the Same"
BC = "Mount Tee Golf"
SLUG = "brand-to-know-mount-tee-golf"
IMG = "/images/mount-tee"
SHOP = "https://mountteegolf.com.au/products/"
A = "Mount Tee Golf"
PK = {x["h"]: x for x in json.loads((ROOT / "research/mount-tee/picks.json").read_text())}
def price(h):
    a = PK[h]["aud"]
    return f"A${a} (~${round(a * 0.70)})"
def sizes(h):
    av = PK[h]["av"]
    if not av: return ""
    if len(av) == 1: return f" Only {av[0]} left."
    if len(av) >= 4: return f" Sizes {av[0]} to {av[-1]} in stock."
    return f" {', '.join(av[:-1])} and {av[-1]} in stock."
COPY = {
 "parklands-waffle-polo-wattle-stripe": "This is the new Parklands colorway, a 220gsm mid-weight waffle in yellow with a trailing vine stripe. Wattle is Australia&rsquo;s national flower, and the brand works a wattle wreath into its logo too. The heavier collar is new this season.",
 "parklands-waffle-polo-eucalyptus-stripe": "The same waffle polo comes in pale green with a eucalyptus-leaf stripe. Our favorite piece in the shop: it looks like a 1970s clubhouse photo and wears like a modern polo.",
 "parklands-waffle-polo-sky-blue": "The original Parklands launched in spring 2025, and this one is plain sky blue with a white-tipped collar.",
 "woodlands-knit-polo-short-sleeve-sand-copy": "Mount Tee calls Woodlands its best-selling polo. This is the lighter, summer knit from the Partners collection, in navy with an embroidered script logo.",
 "woodlands-knit-polo-long-sleeve-sand": "The Woodlands knit with long sleeves in the brand&rsquo;s best-selling sand. Mount Tee pitches it as a layer for the whole year.",
 "woodlands-knit-polo": "The original short-sleeve Woodlands in 100% cotton knit, with a three-button placket and ribbed sleeves and hem.",
 "copy-of-woodlands-knit-polo-pine": "This is the original Woodlands in pine green, the polo in our hero photo.",
 "mountaineering-hoody": "Mount Tee added this brushed cotton jersey hoodie this season, with raglan sleeves and a big mountain graphic on the back, and made it for cool, casual morning rounds at your local track.",
 "pullover-black": "A 380gsm French terry half-zip with a YKK zip and an embroidered chest logo, made to keep you covered and still look sharp.",
 "nylon-quarter-zip": "The Links quarter-zip comes in sand ripstop nylon with green piping, side zip pockets and a mesh lining, for wind and drizzle.",
 "pleated-shorts": "Double pleats, a partly elasticated waist and the clever part: a set of eyelets at the back right hip that hold your tees.",
 "pleated-shorts-black": "The same Peninsula short also comes in black, tee eyelets and all.",
 "partners-t-shirt-white-green": "A boxy 280gsm cotton tee from the Partners collection, with a golfer-and-dog print on the back. It comes in two colors so you can match your playing partner, &ldquo;whoever it may be.&rdquo;",
 "partners-t-shirt-white-navy": "The Partners tee with the print in navy.",
 "cream-t-shirt": "Mount Tee makes its staple 230gsm cotton tee in sand, with the logo front and back.",
 "navy-tshirt": "The staple tee also comes in slate.",
 "mountain-range-hat": "A ripstop nylon five-panel with the new MTG mountain logo, built for winter and wet weather.",
 "untitled-feb11_07-58": "This light nylon five-panel comes in evergreen with the wattle wreath monoscript on the front and a brass buckle at the back.",
 "monoball-5-panel-cap-cream-chocolate-brown": "The brand&rsquo;s most popular five-panel, in cotton twill with a felt Monoball patch that nods to 1960s and 70s baseball logos and a brown leather strap.",
 "monoball-5-panel-cap-navy": "The Monoball five-panel also comes in navy.",
 "partners-corduroy-cap-white-green": "Mount Tee made this corduroy cap for the Partners collection, cream with a green brim.",
 "partners-corduroy-cap-white-navy": "The Partners corduroy cap also comes with a navy brim.",
 "mtg-ball-cap": "A classic brown six-panel with MTG in felt letters and an antique brass buckle.",
 "wool-5-panel-cap-slate": "This wool five-panel in slate blue has a leather strap. It is the cap in our hero photo.",
 "headcover-plush-grey-checkered-driver": "The headline of the new &ldquo;This Could Get Ugly&rdquo; drop: a grey and white faux-fur checkerboard. The brand says it is &ldquo;like a warm hug for your golf bag.&rdquo;",
 "headcover-plush-grey-checkered-3-wood": "The plush checkerboard fits a 3 wood and has a big 3 on the side.",
 "headcover-plush-grey-checkered-hybrid": "The plush checkerboard also comes for a hybrid.",
 "headcover-plush-grey-checkered-putter": "The plush checkerboard also covers your putter, in blade or mallet.",
 "headcover-plush-grey-checkered-tee-bag": "Mount Tee made a matching plush tee bag to finish the set.",
 "putter-headcovers-mustard-checkered": "A mustard and cream checkered cotton putter cover with a plush lining. Blade or mallet.",
 "putter-headcovers-green-tartan": "Green tartan for the putter: Mount Tee&rsquo;s nod to the land the game was born in. Mallet only.",
 "driver-headcover-sky-blue": "Mount Tee cut this one in sky blue corduroy. The brand&rsquo;s copy: &ldquo;Your Father will tell you he had some trousers just like it in the 60s.&rdquo;",
 "3-wood-headcover-sky-blue": "The sky blue corduroy also comes for a 3 wood.",
 "driver-headcover-indigo-waxed-canvas": "From Mount Tee&rsquo;s first collection: waxed cotton canvas, water resistant, with a faint tie-dye look from the wax.",
 "driver-headcover-houndstooth-green-and-white": "Classic houndstooth, turned bright green.",
 "3-wood-houndstooth-headcover-green-and-white": "The green houndstooth also comes for a 3 wood.",
 "brown-suede-driver-headcover": "Mount Tee made this one in genuine suede as a nod to old leather headcovers, for &ldquo;the vintage lover in all of us.&rdquo;",
 "ball-markers-3-pack": "Three steel markers: the Monoball, the monoscript, and a tiny version of the waxed canvas cover from the first collection.",
 "bamboo-tees-50-pk-sky-blue": "Fifty 80mm bamboo tees in sky blue with the logo printed on. The cheapest thing in the shop.",
}
NAME = {h: PK[h]["t"] for h in PK}
P = {PK[h]["key"]: (A, NAME[h], price(h), h, COPY[h] + sizes(h)) for h in PK}
K = {h: PK[h]["key"] for h in PK}
SECTIONS = [
 ("The Polos", "polos", [K[h] for h in ["parklands-waffle-polo-eucalyptus-stripe", "parklands-waffle-polo-wattle-stripe", "parklands-waffle-polo-sky-blue", "woodlands-knit-polo-short-sleeve-sand-copy", "woodlands-knit-polo-long-sleeve-sand", "woodlands-knit-polo", "copy-of-woodlands-knit-polo-pine"]],
  "<strong>Seven polos</strong>Two families: Parklands, a mid-weight waffle with stripes named after Australian plants, and Woodlands, the knit the brand calls its best seller."),
 ("Layers and Shorts", "layers", [K[h] for h in ["mountaineering-hoody", "pullover-black", "nylon-quarter-zip", "pleated-shorts", "pleated-shorts-black"]],
  "<strong>Five pieces</strong>A new hoodie, a French terry half-zip, a ripstop quarter-zip and pleated shorts that hold your tees."),
 ("The Tees", "tees", [K[h] for h in ["partners-t-shirt-white-green", "partners-t-shirt-white-navy", "cream-t-shirt", "navy-tshirt"]],
  "<strong>Four tees</strong>Two come from the Summer &rsquo;24 Partners collection and two are staples."),
 ("The Hats", "hats", [K[h] for h in ["monoball-5-panel-cap-cream-chocolate-brown", "monoball-5-panel-cap-navy", "untitled-feb11_07-58", "wool-5-panel-cap-slate", "mountain-range-hat", "mtg-ball-cap", "partners-corduroy-cap-white-green", "partners-corduroy-cap-white-navy"]],
  "<strong>Eight caps</strong>Mostly five-panels, with felt patches and leather and brass straps."),
 ("This Could Get Ugly", "ugly", [K[h] for h in ["headcover-plush-grey-checkered-driver", "headcover-plush-grey-checkered-3-wood", "headcover-plush-grey-checkered-hybrid", "headcover-plush-grey-checkered-putter", "headcover-plush-grey-checkered-tee-bag"]],
  "<strong>The new drop</strong>The brand made a full plush checkerboard set, driver to tee bag. The name is the brand&rsquo;s, not ours."),
 ("More Headcovers and Small Things", "covers", [K[h] for h in ["driver-headcover-indigo-waxed-canvas", "driver-headcover-sky-blue", "3-wood-headcover-sky-blue", "driver-headcover-houndstooth-green-and-white", "3-wood-houndstooth-headcover-green-and-white", "brown-suede-driver-headcover", "putter-headcovers-mustard-checkered", "putter-headcovers-green-tartan", "ball-markers-3-pack", "bamboo-tees-50-pk-sky-blue"]],
  "<strong>Ten pieces</strong>The older covers come in waxed canvas, corduroy, houndstooth, suede, tartan and checks; the markers and tees finish the shop."),
]
N = 39
PQ = {
 "layers": ("We felt that there are so many ways to be an individual off the course, but struggled to do the same when playing the game that we love.", "Mount Tee Golf, on why it started"),
 "ugly": ("We think that the game should celebrate individuality &mdash; from your clothes and your headcovers, down to your swing.", "Mount Tee Golf"),
}
CAP = ""
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Mount Tee Golf makes the kind of golf clothes you would find in a good vintage shop, then makes them better. Waffle polos with leafy stripes, knit polos with script logos, pleated shorts with a place to keep your tees, and a wall of headcovers in corduroy, waxed canvas, suede, tartan and, new this Melbourne winter, a grey plush checkerboard the brand itself named &ldquo;This Could Get Ugly.&rdquo;</p>
    <h2 class="products-hdr btk-story-hdr">Three Friends in Melbourne</h2>
    <p>The brand&rsquo;s own story is short. Mount Tee Golf &ldquo;was created by 3 friends in Melbourne who believe golf is changing and want to see more expression on the course,&rdquo; and it was built &ldquo;on the ethos that not everybody has to look the same.&rdquo; The products have been on sale since late 2022, and they read like a love letter to Australian golf: polos named Parklands and Woodlands, shorts named Peninsula, stripes named after wattle and eucalyptus.</p>
    <p>It is a small shop, and some of the oldest pieces are down to one size. All 39 below were in stock on mountteegolf.com.au on October 14, 2026. Prices are in Australian dollars with an approximate US figure; the store shows US prices at checkout but does not publish a US shipping rate.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Melbourne, Australia</span></div>
      <div class="sidebar-detail"><span class="l">Founded by</span><span>Three friends</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Knit polos, headcovers</span></div>
      <div class="sidebar-detail"><span class="l">New drop</span><span>This Could Get Ugly</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>A$12&ndash;A$130</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Parklands, Eucalyptus Stripe</span></div>
      <a href="https://mountteegolf.com.au/" target="_blank" rel="noopener" class="sidebar-cta">Visit Mount Tee Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MountTeeGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#AustralianGolf</span>
        <span class="hashtag">#Headcovers</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">There is more from Australia in our <a href="/drops/australian-golf-brands-and-trips">Australian golf brands and trips</a> guide.</p>
</section>
"""
FAQ = [
 ("Where is Mount Tee Golf from?", "Melbourne, Australia. The brand says it was created by three friends in Melbourne who want to see more expression on the golf course."),
 ("What does Mount Tee Golf make?", "Knit and waffle golf polos, pleated shorts with built-in tee storage, tees, layers, five-panel caps, and headcovers in plush, corduroy, waxed canvas, houndstooth, suede and tartan."),
 ("What is the Mount Tee Golf This Could Get Ugly collection?", "The brand's newest drop, from June 2026: a grey and white plush checkerboard headcover set for driver, 3 wood, hybrid and putter, plus a matching tee bag, a Mountaineering Hoody and a Mountain Range cap."),
 ("How much does Mount Tee Golf cost?", "On October 14, 2026, prices ran from A$12 for bamboo tees to A$130 for the Links Nylon Quarter Zip; polos are A$90 to A$110 and headcovers A$45 to A$80."),
 ("Does Mount Tee Golf ship to the US?", "Its store shows prices in US dollars and other currencies, but the shipping policy only lists Australian rates, so check the total at checkout."),
]
FRN = json.loads((ROOT / "research/mount-tee/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-MT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-14", "dateModified": "2026-10-14",
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
    <span>Polos, pleats and headcovers &middot; Melbourne</span><span class="dot"></span>
    <span>39 picks &middot; all in stock, checked October 14, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A man in Mount Tee Golf's pine green Woodlands knit polo and slate wool cap in a dark wood-paneled room with a gilt mirror and chandelier" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore", "Lazyface", "Jeremy", "Joel and Tom"):
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
