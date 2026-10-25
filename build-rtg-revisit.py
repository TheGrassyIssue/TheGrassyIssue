#!/usr/bin/env python3
"""build-rtg-revisit.py — "Brand Revisited: Read The Green" (fall 2026). Cloned from build-blended-interests.py. 19 October 2026.
Lenny: "any brands that need to be revisited?" -> "Let's do a revisit - Read The Green" -> "build it" (picks ours, from the options sheet).
FACTS: readthegreen.com products.json (Oct 19, 2026; 26 products new since our Jun 15 Brand to Know) and product copy;
the Swish Collection is billed on RTG's own homepage banners as "a Collaboration with World Series Champion Nick Swisher".
Brand origin (four lifelong friends, mini-golf name, New York) is from our Jun 15 Brand to Know.
PHOTOS: brand's own. Homepage Swish banners carry burned-in text, so no Swish lifestyle shots are used; hero is the windbreaker group shot.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Read The Green Revisited: Swish, '90s Windbreakers, New Caps"
DESC = ("We revisit Read The Green: the Swish Collection with Nick Swisher, the Back '90s Windbreaker, the Fairway 1/4 Zip "
        "and the new caps. 15 fall picks from the New York brand, plus the pullover that started it, with prices.")
H1 = "Brand Revisited: Read The Green, Four Months Later"
BC = "Brand Revisited: Read The Green"
SLUG = "brand-revisited-read-the-green"
IMG = "/images/rtg-revisited"
SHOP = "https://readthegreen.com/products/"
RTG = "Read The Green"
P = {
 "w1": (RTG, "The Swisher Zip", "$118", "the-swisher-zip",
   "The center of the Swish Collection: a navy and heather-gray windbreaker with a relaxed, throwback &rsquo;90s New York cut. Swisher&rsquo;s motto, &ldquo;Gotta Be You,&rdquo; is printed small along the back of the neck."),
 "w2": (RTG, "Founder&rsquo;s Cap | Swish", "$50", "founders-cap-swish",
   "Classic New York navy cotton with a vintage-green underbrim carrying Swisher&rsquo;s embroidered signature, #33 and &rsquo;09, and a &ldquo;World Series Champion&rdquo; lining inside. RTG calls it a hat that feels like it&rsquo;s been around forever."),
 "w3": (RTG, "Fairway Performance Cap | Home", "$50", "fairway-performance-cap-home",
   "Their best-selling performance cap in white with a pinstripe-inspired rope, which RTG says is one of Swisher&rsquo;s favorite touches. Signature, #33 and &rsquo;09 under the brim and the World Series lining inside."),
 "w4": (RTG, "Fairway Performance Cap | Away", "$50", "fairway-performance-cap-away",
   "The road version in navy with the same pinstripe rope and custom interior. Buy the Home and Away pair, the zip and the Founder&rsquo;s Cap together and the Swish bundle is $239. Swish pieces are excluded from discount codes."),
 "l1": (RTG, "Back &rsquo;90s Windbreaker, Seven Colorways", "$108", "back-90s-windbreaker-tux",
   "The main fall piece: a two-tone, relaxed windbreaker inspired by the golf and sportswear of the &rsquo;90s, reimagined in New York. Seven colorways, from Tux (black and white) to Patriot (red, white and navy), Jazz (white and teal) and Mallard (navy and green), all in stock in every size."),
 "l2": (RTG, "Fairway 1/4 Zip, Five Colorways", "$98", "fairway-windbreaker-forest",
   "The quieter option: a classic quarter-zip windbreaker in light, wind- and water-resistant fabric with side pockets, elastic cuffs and a drawstring waist. Unisex fit, in forest, white, black, iron and atlantic."),
 "l3": (RTG, "The Grounds Crew Jacket | Green", "$150", "the-grounds-crew-jacket-green",
   "Back for a second fall: midweight cotton twill with a corduroy collar and cuffs, a full zip and the embroidered Grounds Crew patch. A workwear jacket for after the round. XL was sold out when we checked."),
 "l4": (RTG, "The Oversized Knit Sweater", "$100", "the-knit-sweater",
   "Heavyweight hand-knit cotton at 800 GSM with Read The Green embroidered across the chest. It runs big; RTG recommends sizing down a full size. Dry clean only."),
 "l5": (RTG, "The Varsity Crewneck, Green or Grey", "$100", "the-grey-crewneck",
   "A 500 GSM all-cotton crew with GREEN printed across the front and rib-knit trims. It was $75 when we first wrote about it in June; it is $100 now."),
 "m1": (RTG, "The &rsquo;97 Vintage Pullover, Green, Black or Navy", "$100", "the-97-vintage-pullover",
   "The original. Lightweight, weather-resistant nylon with a cream V collar trimmed in stripes, rib-knit cuffs, a drawstring waist and &lsquo;Read The Green Golf Club 1997&rsquo; embroidered on the chest. RTG calls it inspired by outerwear from a golden era of golf and streetwear. Navy was in stock in every size; green and black were short a size or two."),
 "m2": (RTG, "The &rsquo;97 Vintage Short Sleeve Pullover", "$89", "the-97-vintage-short-sleeve-pullover-green",
   "The same nylon, cut short-sleeved for warm days, which RTG introduced as its fall classic turned summer staple. For Austin, this is the version you will actually wear most of the year. Green, navy and black, each missing a size or two when we checked."),
 "h1": (RTG, "Fairway Performance Cap, Four New Colorways", "$45", "fairway-performance-cap-green-white",
   "New this fall: green, navy, black and sky underbrims on a white front, with a perforated performance back panel for hot rounds and a small &ldquo;4&rdquo; on the side."),
 "h2": (RTG, "Club Cap | Rust or Intrepid", "$45", "club-cap-orange",
   "The mid-profile Club Cap with &ldquo;Read The Green Golf Club, New York, New York&rdquo; embroidered on the front. Rust has an orange brim on a cream front; Intrepid is all navy."),
 "h3": (RTG, "Founder&rsquo;s Cap | Blacktop or Courtside", "$40", "founders-cap-knicks",
   "Two new versions of the original five-panel cotton Founder&rsquo;s Cap: Blacktop in black with orange embroidery, Courtside in cream with an orange and royal brim. The cheapest new pieces here."),
 "h4": (RTG, "Founder&rsquo;s Cap | Stars &amp; Stripes", "$45", "founders-cap-stars-stripes",
   "A white Founder&rsquo;s Cap with an American flag on the side and &ldquo;Home of The Brave&rdquo; and &ldquo;Land of The Free&rdquo; on the custom interior lining."),
}
SECTIONS = [
 ("The Piece That Put Them on the Map", "map", ["m1","m2"],
  "<strong>The &rsquo;97 Vintage Pullover &middot; $89&ndash;$100</strong>Before the windbreakers and the Swisher collab, there was one nylon pullover. The &rsquo;97 went viral and turned a New York hat brand into a clothing brand. It has been on their store since fall 2024, it has picked up a short-sleeve version since, and the newer windbreakers all borrow from it."),
 ("The Swish Collection", "swish", ["w1","w2","w3","w4"],
  "<strong>New Sep 27 &middot; four pieces &middot; $50&ndash;$118</strong>RTG&rsquo;s own banners call it a collaboration with World Series champion Nick Swisher: a windbreaker and three caps with his signature, his #33 and &rsquo;09 for the 2009 title, and &ldquo;World Series Champion&rdquo; printed inside."),
 ("Fall Layers", "layers", ["l1","l2","l3","l4","l5"],
  "<strong>Two new windbreakers, three returning layers &middot; $98&ndash;$150</strong>The Back &rsquo;90s Windbreaker (Sep 12) and Fairway 1/4 Zip (Aug 21) are new. The Grounds Crew Jacket, Oversized Knit and Varsity Crewneck are back from last fall and still the core of their cold-weather range."),
 ("New Caps", "hats", ["h1","h2","h3","h4"],
  "<strong>Ten new caps since June &middot; $40&ndash;$45</strong>Hats are still where RTG started and still the cheapest way in. New Fairway Performance colorways, two Club Caps, two Founder&rsquo;s Caps and a flag cap."),
]
N = 15
PQ = {"swish": ("Gotta Be You.", "Nick Swisher&rsquo;s motto, printed inside the Swisher Zip")}
CAP = "Photography &middot; Read The Green"
BANDS = {"map": ("The &rsquo;97 in the wild", "From Read The Green&rsquo;s own campaign shoots.", [("band-1","Two models in green &rsquo;97 Vintage Pullovers sitting in a wood-paneled room","The pair"),("band-4","A model in a green &rsquo;97 Vintage Pullover and a white Read The Green cap","The pullover"),("band-5","A model with arms crossed in a green &rsquo;97 Vintage Pullover, another hanging on the wall behind him","The original")])}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we first wrote about <a href="/drops/brand-to-know-read-the-green" style="border-bottom:1px solid var(--ink)">Read The Green</a> in June, it was a New York hat brand with a small apparel line that had earned its place, started by four lifelong friends and named after something shouted across a mini-golf course. Four months later, it has added 26 products, and every one of them was in stock when we checked.</p>
    <p>The headline is the Swish Collection, which RTG bills as a collaboration with World Series champion Nick Swisher. It&rsquo;s small and specific: a windbreaker and three caps carrying his signature, his #33 and &rsquo;09, the year he won the World Series with the Yankees. It&rsquo;s a smart fit for a brand that has always put New York first.</p>
    <p>The bigger change is outerwear. RTG made its name on one nylon pullover, the &rsquo;97, and it&rsquo;s still the first thing we&rsquo;d point a new customer to. Now it has a full rack around it. The Back &rsquo;90s Windbreaker comes in seven two-tone colorways, the Fairway 1/4 Zip in five, and both sit under $110. Add the returning Grounds Crew Jacket and the heavyweight knit, and it&rsquo;s the first season you could dress for a cold round entirely in RTG.</p>
    <p>If you buy one thing: the Back &rsquo;90s Windbreaker in Tux. If you just want a hat, a new Fairway Performance colorway is $45.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Read The Green</span></div>
      <div class="sidebar-detail"><span class="l">Based in</span><span>New York</span></div>
      <div class="sidebar-detail"><span class="l">First covered</span><span>June 15, 2026</span></div>
      <div class="sidebar-detail"><span class="l">New since</span><span>26 products</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$40&ndash;$150</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Back &rsquo;90s Windbreaker, $108</span></div>
      <div class="hashtags">
        <span class="hashtag">#ReadTheGreen</span>
        <span class="hashtag">#SwishCollection</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is the Read The Green Swish Collection?", "A capsule Read The Green bills as a collaboration with World Series champion Nick Swisher: the Swisher Zip windbreaker ($118) and three caps ($50 each) with his signature, #33 and '09, plus a 'World Series Champion' interior lining. All four come as a $239 bundle. Prices checked October 19, 2026."),
 ("What's new from Read The Green for fall 2026?", "The Back '90s Windbreaker in seven colorways ($108), the Fairway 1/4 Zip in five ($98), the Swish Collection and ten new caps, plus returning layers like the Grounds Crew Jacket ($150) and Oversized Knit Sweater ($100)."),
 ("What is the Read The Green '97 Vintage Pullover?", "The piece that put the brand on the map: a lightweight, weather-resistant nylon pullover with a striped V collar, rib-knit cuffs, a drawstring waist and 'Read The Green Golf Club 1997' on the chest. It was $100 long-sleeved and $89 short-sleeved on October 19, 2026."),
 ("Where is Read The Green from?", "New York. It was started by four lifelong friends, and the name comes from three words shouted at a buddy who missed the pin on a mini-golf course."),
 ("How does the Read The Green Oversized Knit fit?", "Big. Read The Green recommends sizing down a full size, and it is dry clean only."),
]
FRN = json.loads((ROOT / "research/rtg-revisit/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-19", "dateModified": "2026-10-19",
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
    <span>Brand Revisited &middot; New York &middot; first covered June 15, 2026</span><span class="dot"></span>
    <span>15 picks &middot; all in stock, checked October 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Eleven models in Read The Green Back \'90s Windbreakers and Fairway quarter-zips, posed together in two rows" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
