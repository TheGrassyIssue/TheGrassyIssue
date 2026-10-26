#!/usr/bin/env python3
"""build-whim-btk.py — Brand to Know: Whim Golf. 25 October 2026. Cloned from build-alba-btk.py.
Lenny: "Let's do a brand to know Whim golf" -> options sheet (37 in stock) -> "BUild it" (built from the suggested
starting point plus the objects; colourways grouped, 16 cards).
FACTS: research/whim/brief.md (About, Sheep to Shirt and Free Golf pages; CNN 22 Aug 2024; StockX 14 Apr 2022; Camp Dudley),
research/whim/products.json (whimgolf.com live, 25 Oct 2026). Whim is NYC (83 Canal St). The golf short is nylon made in
China, cut and sewn in NYC, so the post never says "natural fibers only". Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Whim Golf, American Merino and Free Golf in NYC"
DESC = ("Whim Golf makes merino golf shirts from sheep to shirt in the USA and runs free putting greens in New York. "
        "16 picks from $33 to $8,800, checked Oct. 25, 2026.")
H1 = "Brand to Know: Whim Golf, From Sheep to Shirt to Free Golf"
BC = "Brand to Know: Whim Golf"
SLUG = "brand-to-know-whim-golf"
IMG = "/images/whim-golf"
SHOP = "https://whimgolf.com/products/"
C = "Whim Golf"
P = {
 "navy": (C, "Embroidered Navy Merino Long Sleeve Golf Shirt", "$320", "chartreuse-embroidered-navy-merino-long-sleeve-golf-shirt",
   "This is the shirt the brand is built on: 100% American merino in a mid-weight 6.5oz jersey, knit in a centuries-old Massachusetts mill and finished in New York with natural horn buttons and the Whim script. Navy with a chartreuse or a white script, in a standard fit, and no synthetics anywhere."),
 "slate": (C, "Embroidered Slate Merino Long Sleeve Golf Shirt", "$309", "sky-embroidered-slate-merino-long-sleeve-golf-shirt",
   "Whim knits this lighter 4.5oz version in South Carolina and makes it by hand in New York, from merino sourced in Wyoming, Colorado and Nevada. Slate grey with a sky blue or black script. It&rsquo;s the one we&rsquo;d reach for on a cool morning that turns warm by the back nine, and our pick of the range."),
 "black": (C, "Embroidered Black Merino Long Sleeve Golf Shirt", "$309", "embroidered-black-merino-long-sleeve-golf-shirt",
   "The lightest shirt Whim makes, in a 3.5oz merino jersey from the Massachusetts mill, with horn buttons and a red or black script on the left chest. Black with the red script is the one we&rsquo;d buy. Handmade and embroidered in New York."),
 "orange": (C, "Orange Merino Long Sleeve Golf Shirt, Light-weight", "$309", "orange-merino-long-sleeve-golf-shirt-light-weight",
   "The loudest thing Whim makes is a plain merino shirt in bright orange. It&rsquo;s the light-weight jersey knit in Massachusetts and made in New York, and Whim says it&rsquo;s for year-round wear. Only S and L are left."),
 "jacket": (C, "Woven Merino Swing Jacket", "$499", "mens-woven-merino-swing-jacket",
   "Whim weaves this jacket in Connecticut from RWS-certified American merino and leaves it undyed, so each one carries small dark flecks from the wool itself. It has a RiRi zip, two side pockets, a cinched hem and paneled shoulders cut for an easy swing, with no ribbing at the cuffs. The most expensive piece of clothing Whim makes."),
 "short": (C, "Golf Short, Blue Stretch Nylon", "$80", "golf-short-gray-stretch-nylon",
   "Whim cuts this short at a classic length and says it&rsquo;s &ldquo;not for the guys showing thigh.&rdquo; It&rsquo;s a water-resistant stretch nylon mesh with a snap and button closure and a YKK zip, cut and sewn in New York from fabric made in China. Only S and M are left."),
 "reebok": (C, "WHIM Reebok Classic", "$100", "whim-reebok-classic",
   "Whim&rsquo;s take on Reebok&rsquo;s &rsquo;80s Classic Leather has a premium leather upper and lining, suede at the toe and heel, an ice nylon tongue with a four-color Whim label, a powder blue embossed heel and grass-print sock liners. It ships in custom Whim x Reebok packaging with white and ice laces."),
 "sheephat": (C, "Sheep Hat in Woven Merino", "$89", "natural-woven-merino-golf-hat",
   "An adjustable cap in 100% woven American merino from American Woolens, with a brass closure and a small embroidered sheep on the front. It&rsquo;s the clearest summary of the Sheep to Shirt program you can wear."),
 "merinohat": (C, "Woven Merino Golf Hat", "$89", "eggplant-woven-merino-golf-hat",
   "The same idea without the sheep: woven merino from a Connecticut mill, yarn from RWS-certified ranches in California, Colorado, Idaho and Nevada, a brass closure and a leather strap. The brim comes flat and is meant to be curved. Eggplant or dark navy."),
 "oxford": (C, "Oxford Cotton Hat", "$89", "oxford-cotton-hat",
   "Japanese oxford cotton in a pale stripe, made in California and embroidered in New York, with the purple Whim script on the back and a brass closure."),
 "sock": (C, "Featherweight Merino Golf Sock", "$39", "featherweight-merino-golf-sock",
   "Whim makes this sock from the same American merino as its shirts, knit and processed in North Carolina. It has minimal padding, a flat toe seam, the logo woven into the toe and a Made in U.S.A graphic inside the cuff. Navy or natural."),
 "sheep": (C, "Merino Fleece Sheep Driver Headcover", "$99", "merino-fleece-sheep-driver-headcover",
   "A barrel driver cover in American merino fleece with black merino jersey ears and lining. Whim cuts the ears and lining from scrap left over from shirt production, so the cover wastes less and looks like a sheep."),
 "tool": (C, "Steel Ball Mark Repair Tool", "$33", "steel-ball-mark-repair-tool",
   "A vintage forged steel ball mark repair tool, hand-engraved in New York with the Whim script and a thumbprint-style outline. At $33 it&rsquo;s the cheapest way into the brand."),
 "bag": (C, "Big Bag", "$67", "big-bag-sky-blue-logo",
   "Whim first made this tote from scrap fabric to carry shirts from the garment district to its office on Canal Street. It&rsquo;s cut and sewn in New York from leftover Pennsylvania-made polyester mesh, packs into a pocket and measures 24 by 18 by 12 inches. Sky blue, yellow or white script."),
 "cupola": (C, "La Cupola Paperweight", "$149", "la-cupola-paperweight",
   "A hand-poured concrete and gypsum model of La Cupola, Whim&rsquo;s installation at Milan Design Week 2026. The dome weighs 7.5 pounds, sits on a leather bottom, has a removable concrete flag and comes in an edition of 10."),
 "whimowa": (C, "WHIMOWA Portable Putting Green", "$8,800", "whimowa-portable-putting-green",
   "A one-of-one vintage Rimowa aluminum trunk with a putting green built inside, four wheels, a locking latch, a magnetic flag pin and a putter holder through the top. Suitcase, putter, balls, flag and pin are all included. It&rsquo;s the clearest proof that Whim is a design studio as much as a clothing label."),
}
SECTIONS = [
 ("The Merino Shirts", "shirts", ["navy", "slate", "black", "orange"],
  "<strong>Four shirts, seven colorways &middot; $309&ndash;$320</strong>American merino in three weights, knit in Massachusetts or South Carolina and finished in New York."),
 ("Outerwear, Shorts &amp; Shoes", "outerwear", ["jacket", "short", "reebok"],
  "<strong>Three pieces &middot; $80&ndash;$499</strong>An undyed merino swing jacket, a nylon golf short and the Reebok collab."),
 ("Hats &amp; Socks", "hats", ["sheephat", "merinohat", "oxford", "sock"],
  "<strong>Four pieces &middot; $39&ndash;$89</strong>Woven merino and Japanese oxford caps, and a merino golf sock."),
 ("Objects", "objects", ["sheep", "tool", "bag", "cupola", "whimowa"],
  "<strong>Five pieces &middot; $33&ndash;$8,800</strong>A sheep headcover, a forged steel tool, a mesh tote, a concrete paperweight and a putting green in a suitcase."),
]
N = 16
PQ = {
 "shirts": ("We want to wear clothes that we feel will look good on us 10 years from now.", "Colin Heaberg, to StockX, 2022"),
 "objects": ("If you make it so someone can walk off the street, grab a putter and try, you&rsquo;re going to get more golfers.", "Colin Heaberg, to CNN, 2024"),
}
BANDS = {
 "shirts": ("Sheep to shirt", "From Whim&rsquo;s Sheep to Shirt program: the wool before it becomes a shirt.",
   [("sheep-scan", "A tuft of uncombed American merino wool on a white background", "American merino, before it&rsquo;s combed"),
    ("sheep-wool", "A bag of scoured wool from Whim&rsquo;s partner ranch", "Scoured wool from the partner ranch"),
    ("sheep-leather", "A handmade leather sheep wearing a merino coat", "A handmade leather sheep in a merino coat")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
_FG = [("free-chicago", "Whim's first pop-up shop with a putting green, on West Randolph Street in Chicago", "729 W. Randolph Street, Chicago, June 2019"),
 ("free-avea", "A green putting surface running through Whim's pop-up shop on Avenue A in New York", "66 Avenue A, New York, summer 2023"),
 ("free-wsp", "Whim's portable putting green set up in Washington Square Park, New York", "The portable green in Washington Square Park, 2024")]
_fgfigs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _FG)
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Whim Golf makes the most American golf shirt we&rsquo;ve found. Every step happens in the US: the merino comes from sheep raised on ranches in Idaho, Colorado, California and Nevada, the fabric is knit in Massachusetts or South Carolina, and the shirt is cut, sewn and embroidered in New York. And the clothes are only half of what Whim does. In CNN&rsquo;s 2024 profile, they&rsquo;re the &ldquo;carrot&rdquo; that gets people, especially in cities, to pick up a putter and try the game. Colin Heaberg and Will Gisel met at Camp Dudley in 2006 and made their first t-shirts together in the camp&rsquo;s silk-screening course. They launched Whim in 2019 with pop-up shops in Chicago and on Manhattan&rsquo;s Lower East Side, and every one had a free putting green inside. There have been nine since, open more than 600 days across Chicago, Los Angeles and New York, and a permanent one now sits at 129 Eldridge Street.</p>
    <p><strong>Sheep to shirt.</strong> Whim has made everything in the US from the start, and in late 2022 it began sourcing the raw wool here too. The ranches are RWS and Nativa Regenerative certified, one of the mills is centuries old, and Whim calls itself &ldquo;the only true Made in U.S.A shirt maker in golf.&rdquo; The design is plain on purpose: a standard fit, horn buttons, a small script where a chest logo would go. Gisel told StockX in 2022, &ldquo;I just don&rsquo;t like clothes with a lot of logos on them.&rdquo;</p>
    <p><strong>Free Golf.</strong> Heaberg&rsquo;s argument, as he put it to CNN, is that people skip golf the way they skip broccoli, because they assume they won&rsquo;t like it. Whim&rsquo;s answer is to put a putter in their hands. More than 15,000 people had tried the greens by 2024, and Heaberg calls the number of people touching clubs &ldquo;the only metric there is.&rdquo;</p>
    <p><strong>Who it&rsquo;s for.</strong> In Heaberg&rsquo;s words, golfers who &ldquo;might be into architecture, or watch a lot of basketball&rdquo; as well. Whim probably has the widest price spread of any brand we&rsquo;ve covered, from a $33 forged ball mark tool to the WHIMOWA trunk at $8,800, more than 260 times as much. The clothes sit in the middle, and they aren&rsquo;t cheap: the merino shirts run $309 to $320, and the swing jacket is $499. Start with the slate long sleeve, or the $99 sheep headcover if you want something smaller, and keep an eye on the objects, because the La Cupola paperweight and the $8,800 WHIMOWA trunk are where the design studio shows.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>New York, NY</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2019</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Colin Heaberg &amp; Will Gisel</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>USA, American merino</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$33&ndash;$8,800</span></div>
      <div class="sidebar-detail"><span class="l">Free Golf</span><span>9 putting greens</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Slate merino long sleeve</span></div>
      <div class="hashtags">
        <span class="hashtag">#WhimGolf</span>
        <span class="hashtag">#FreeGolf</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Free Golf</div>
  <h2 class="products-hdr" id="free-golf">Nine Putting Greens, Free to Play</h2>
  <p class="cat-kicker"><strong>From Whim&rsquo;s Free Golf page &middot; three photos</strong>Whim builds open-access putting greens in the densest parts of American cities, &ldquo;creating the conditions for underrepresented communities to fall in love with golf on their own terms.&rdquo; The permanent one is at 129 Eldridge Street, New York.</p>
  <div class="ig-grid">
""" + _fgfigs + """
  </div>
</section>
"""
FAQ = [
 ("Where is Whim Golf based?", "New York City. Whim Golf Inc. is at 83 Canal Street, and its permanent free putting green is at 129 Eldridge Street on the Lower East Side."),
 ("Who founded Whim Golf?", "Colin Heaberg and Will Gisel, who met at Camp Dudley in 2006 and launched Whim Golf in 2019."),
 ("Is Whim Golf made in the USA?", "Yes. Whim makes its clothing, footwear, objects and accessories in the USA, and its merino shirts use wool from American ranches, knit in Massachusetts or South Carolina and finished in New York."),
 ("How much does Whim Golf cost?", "The merino long-sleeve golf shirts are $299 to $320, hats are $39 to $99, and the range in this post runs from a $33 ball mark tool to the $8,800 one-of-one WHIMOWA putting green."),
 ("What is Whim's Free Golf initiative?", "Free, open-access putting greens in cities. Whim has built nine pop-up greens across Chicago, Los Angeles and New York and runs a permanent one at 129 Eldridge Street."),
]
_LB = [("about-founders", "Colin Heaberg and Will Gisel standing outside Whim's Free Golf shop in New York", "Colin and Will outside Free Golf NYC, 2022"),
 ("about-michigan", "A green fairway and tree line from Whim's founding golf camping trip in Michigan", "The founding golf camping trip, Michigan, 2019"),
 ("about-merino", "Two golfers walking under cypress trees on Whim's American merino trip in California", "The American merino trip, California, 2025")]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _LB)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">Whim, in Photos</h2>
  <p class="cat-kicker"><strong>From Whim&rsquo;s About page &middot; three photos</strong>The founders, the trip that started it and the trip to the merino.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/whim/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-25", "dateModified": "2026-10-25",
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
    <span>Brand to Know &middot; New York &middot; Founded 2019</span><span class="dot"></span>
    <span>16 picks &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Whim Golf's free putting green at 129 Eldridge Street, New York, with putters on the wall and quilted artwork" fetchpriority="high" /></div></div>
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
