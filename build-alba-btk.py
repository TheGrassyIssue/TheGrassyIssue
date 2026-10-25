#!/usr/bin/env python3
"""build-alba-btk.py — Brand to Know: Alba Golf. 25 October 2026. Cloned from build-wwd-revisit.py.
Lenny: "let's do a brand to know - https://albagolf.it/" -> options sheet (24, all in stock) -> "whats the TGI take? Why should
someone spend almost 600 with them?" -> verdict agreed in chat -> "build the alba post with all picks".
All 24 products, colourways grouped: 16 cards. FACTS: research/alba/catalogue.json (albagolf.it products.json + .js, 25 Oct 2026,
EUR at 1.1201), research/alba/brand.md (About page, shipping policy, terms). No founder, founding year or made-in claim
published, so none is made here. Comparison prices from TGI's own 25 Oct capsule sweep (research/capsules/*.json). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Alba Golf, Milan's New Technical Golfwear"
DESC = ("Alba Golf launched in Milan in October 2026: REDA merino polos, PrimaLoft vests and taped waterproof jackets from $56 to $616. "
        "All 24 pieces, and our honest take on the price.")
H1 = "Brand to Know: Alba Golf, Milan&rsquo;s New Technical Golfwear"
BC = "Brand to Know: Alba Golf"
SLUG = "brand-to-know-alba-golf"
IMG = "/images/alba-golf"
SHOP = "https://albagolf.it/products/"
C = "Alba Golf"
P = {
 "crest": (C, "Crest Jacket", "$616 (&euro;550)", "crest-jacket",
   "The most expensive thing Alba makes. A three-layer waterproof shell with fully taped seams, a laser-cut ergonomic pattern, shaped sleeves, Ultra-Suede at the cuffs and collar, and the brand&rsquo;s signature metal zip and low stand collar. Black. Read our take before you buy it."),
 "shire": (C, "Shire Quarter Zip Jacket", "$482 (&euro;430)", "shire-quarter-zip-jacket",
   "The same three-layer waterproof fabric as the Crest in a pullover cut: a three-quarter metal zip, a big kangaroo pocket, a drawcord hem and a ventilation yoke across the back of the shoulders. In mud, with a salmon contrast at the collar."),
 "glen": (C, "Glen Padded Vest", "$437 (&euro;390)", "glen-padded-vest-in-salmon",
   "A microfiber vest with an internal coating against wind and light rain, insulated with PrimaLoft Active Evolve. Metal zip, Ultra-Suede trim and two zip pockets. Salmon, chocolate brown or ivory, and the salmon is the best colour in the collection."),
 "haar": (C, "Haar Reversible Vest", "$392 (&euro;350)", "haar-reversible-vest-in-navy-blue",
   "Two vests in one: soft technical wool on one side, wind-resistant microfiber on the other, with the monogram on the wool and the wordmark on the microfiber. Navy or black, sized S/M to L/XL."),
 "grianls": (C, "Grian Long Sleeve Quarter Zip Polo", "$291 (&euro;260)", "grian-ls-quarter-zip-polo",
   "Our pick. An exclusive REDA 1865 merino and lyocell fabric in a pique structure. Zipped, the collar stands up; open, it folds into a polo collar. Machine washable, in grey melange."),
 "grianss": (C, "Grian Short Sleeve Quarter Zip Polo", "$269 (&euro;240)", "grian-ss-quarter-zip-polo",
   "The same REDA merino and lyocell fabric and two-way collar with short sleeves. Navy. Alba calls the fabric year-round, and it&rsquo;s the piece we&rsquo;d wear most."),
 "cheviot": (C, "Cheviot Mockneck", "$269 (&euro;240)", "cheviot-mockneck-in-melange-beige",
   "A 100% technical wool knit with shaped sleeves, a slightly raised collar and small ventilation perforations along the sides and sleeves. Melange beige or black. It goes under the vests and over nothing at dinner."),
 "voarls": (C, "Voar Long Sleeve Polo", "$196 (&euro;175)", "voar-ls-polo-in-mauve",
   "Cotton pique with three small metal snaps at the collar, tonal exposed seams and a stretch cuff. Mauve or ivory (ivory is out in L). The cheapest way into the clothing."),
 "voarss": (C, "Voar Short Sleeve Polo", "$174 (&euro;155)", "voar-ss-polo",
   "The short-sleeve Voar in ivory cotton pique. The lowest-priced shirt Alba makes."),
 "rime": (C, "Rime Thermal Layer", "$202 (&euro;180)", "rime-thermal-layer",
   "A high-collared base layer Alba says was developed from professional skiing, with grey melange panels and a big logo across the back. Black, sized S/M or L/XL. The bottom of what Alba calls its Layering System."),
 "nevis": (C, "Nevis Tech Trouser", "$437 (&euro;390)", "nevis-tech-trouser-in-mud",
   "A cotton trouser blended with nylon and elastane, with a bonded waistband, a metal snap front and a side pocket built into the right leg. Mud, ivory or black."),
 "roy": (C, "Roy Tech Shorts", "$347 (&euro;310)", "roy-tech-shorts-in-mud",
   "The Nevis fabric and details as a short, which Alba says reinterprets cotton as a technical material. Mud or black."),
 "driver": (C, "Barrel Driver Wood Cover", "$146 (&euro;130)", "alba-barrel-driver-wood-cover-in-black",
   "A black barrel-style driver cover with the Alba monogram on the top and the wordmark down the side."),
 "fairway": (C, "Barrel Fairway Wood Cover", "$146 (&euro;130)", "alba-barrel-fairway-wood-cover-in-black",
   "The matching fairway-wood cover, in black."),
 "pouch": (C, "Pouch", "$56 (&euro;50)", "alba-pouch-in-black",
   "A black drawstring pouch printed with the monogram and wordmark, for balls, tees and the things in your pockets."),
 "towel": (C, "Caddie Towel", "$56 (&euro;50)", "alba-caddie-towel-in-off-white-black",
   "An off-white towel with black stripes and the monogram. The cheapest Alba piece, along with the pouch."),
}
SECTIONS = [
 ("Outerwear", "outerwear", ["crest", "shire", "glen", "haar"],
  "<strong>Four pieces, seven colourways &middot; $392&ndash;$616</strong>Two waterproof shells with taped seams, a PrimaLoft vest and a reversible wool vest."),
 ("Polos, Knits &amp; Layers", "polos", ["grianls", "grianss", "cheviot", "voarls", "voarss", "rime"],
  "<strong>Six pieces &middot; $174&ndash;$291</strong>The REDA merino polos, a wool mock neck, cotton polos and a base layer."),
 ("Trousers &amp; Shorts", "trousers", ["nevis", "roy"],
  "<strong>Two pieces, five colourways &middot; $347&ndash;$437</strong>A tech trouser and short in a cotton, nylon and elastane blend."),
 ("For the Bag", "bag", ["driver", "fairway", "pouch", "towel"],
  "<strong>Four pieces &middot; $56&ndash;$146</strong>Headcovers, a pouch and a towel, all in black and off-white."),
]
N = 16
PQ = {
 "outerwear": ("Performance is integrated rather than displayed.", "Alba Golf, on its About page"),
 "polos": ("Technical by nature. Refined by design.", "Alba Golf, on its homepage"),
}
BANDS = {
 "outerwear": ("The campaign", "From Alba&rsquo;s launch shoot: dark layers and white gloves.",
   [("lb-3", "Alba Golf campaign: a line of models walking in dark layers with white golf gloves", "The launch, in a line"),
    ("lb-4", "Alba Golf campaign: the companion walking shot, dark layers and white gloves", "Dark layers, white gloves"),
    ("lb-8", "The black Crest Jacket with black trousers, full length", "The Crest Jacket")]),
 "polos": ("On model", "The pieces as Alba styles them.",
   [("lb-7", "The salmon Glen Padded Vest over an ivory long-sleeve polo", "Glen vest over the Voar"),
    ("lb-10", "The mauve Voar long-sleeve polo tucked into mud trousers with a black belt", "Voar polo, Nevis trouser"),
    ("lb-9", "An ivory and navy Haar vest from the reversible vest gallery", "The Haar vest")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TABLE = """
<div style="max-width:760px;margin:18px auto 6px;overflow-x:auto">
<table style="width:100%;border-collapse:collapse;table-layout:fixed;font-size:14px;line-height:1.45"><colgroup><col style="width:22%"><col style="width:22%"><col style="width:56%"></colgroup>
<thead><tr style="border-bottom:.5px solid var(--ink);text-align:left;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase">
<th style="padding:8px 10px;text-align:left !important;vertical-align:top">The job</th><th style="padding:8px 10px;text-align:left !important;vertical-align:top">Alba</th><th style="padding:8px 10px;text-align:left !important;vertical-align:top">Who else does it</th></tr></thead>
<tbody>
<tr style="border-bottom:.5px solid rgba(20,20,20,.25)"><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Waterproof jacket</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Crest, $616</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Galvin Green Akron, $399 &middot; SLOAT Organic Ventile, $595</td></tr>
<tr style="border-bottom:.5px solid rgba(20,20,20,.25)"><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Merino polo</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Grian, $269&ndash;$291</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Olydoe Merino Aire, $125 &middot; SLOAT Merino Polo, $215</td></tr>
<tr style="border-bottom:.5px solid rgba(20,20,20,.25)"><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Tech trouser</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Nevis, $437</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Manors Ripstop Tech Trouser, $201</td></tr>
<tr><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Wool mid layer</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Cheviot, $269</td><td style="padding:9px 10px;text-align:left !important;vertical-align:top">Macade Bridge Merino Quarter Zip, $195 &middot; Manors Merino Tech Crewneck, $241</td></tr>
</tbody></table>
<p style="font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:8px">Comparison prices from our <a href="/drops/golf-capsule-wardrobe" style="border-bottom:1px solid currentColor">capsule wardrobe</a> sweep, checked October 25, 2026</p>
</div>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Alba Golf went live in the middle of October with one collection and 24 pieces. It is a Milan label, and it describes itself as &ldquo;a contemporary golfwear brand born in Milan, exploring the intersection of engineering, material research and modern performance.&rdquo; Its one-line pitch is that the range was &ldquo;born from Scotland&rsquo;s wild skies and shaped in Milan,&rdquo; and the product names read like a map of Scotland: Glen, Haar, Cheviot, Nevis. (Alba is also the Gaelic name for Scotland. The brand doesn&rsquo;t say that&rsquo;s why, so take it as our reading.)</p>
    <p><strong>The fabric is the story.</strong> The Grian polos use an exclusive merino and lyocell fabric from REDA 1865, an Italian wool maker that has been weaving since the nineteenth century, and the collar zips into a stand collar or folds open into a polo. The Glen vest is insulated with PrimaLoft, the Cheviot is 100% technical wool with ventilation holes along the sides, and both jackets are three-layer waterproof with taped seams. Every piece shares the same metal zip, low stand collar and Ultra-Suede trim. Alba&rsquo;s line for all of it: &ldquo;Performance is integrated rather than displayed.&rdquo;</p>
    <p><strong>It looks like nothing else we cover.</strong> Quiet colours (black, mud, ivory, a salmon that steals the collection), no big logos, and a cut that sits closer to Italian tailoring than to golf. The launch campaign is a single swing shot as a multiple-exposure sequence, which is the best image any brand has launched with this year.</p>
    <p><strong>So why would anyone spend almost $600?</strong> Most people shouldn&rsquo;t, at least not on the jacket. The $616 Crest is a well-made shell, but Galvin Green has built rain gear for golf for more than thirty years and its Akron is $399, and the Nevis trouser costs twice what Manors charges for its ripstop. US orders also add a &euro;35 shipping charge and import duties on delivery, and returns are at your cost within 14 days. Alba hasn&rsquo;t published who founded it or where the clothes are made (its site says &ldquo;engineered in Italy,&rdquo; which isn&rsquo;t the same thing), and every product photo is a studio shot, so we haven&rsquo;t seen it on a course yet.</p>
    <p><strong>Where it earns the price is the polo.</strong> Nobody else we cover uses REDA fabric, the two-way collar is a real idea, and at $269 to $291 the Grian sits in the same territory as the merino polos from SLOAT and the better clubhouse brands. That is where we&rsquo;d start: one Grian, maybe the Cheviot to go under a vest, and then wait a season to see how the collection holds up before buying the shell.</p>
    <p><strong>The verdict:</strong> buy one piece, not the outfit. Get the Grian. Watch Alba for the rest.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Milan, Italy</span></div>
      <div class="sidebar-detail"><span class="l">Launched</span><span>October 2026</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>FW26, 24 pieces</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$56&ndash;$616</span></div>
      <div class="sidebar-detail"><span class="l">Fabric</span><span>REDA 1865, PrimaLoft</span></div>
      <div class="sidebar-detail"><span class="l">Ships to US</span><span>&euro;35 + duties</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Grian polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#AlbaGolf</span>
        <span class="hashtag">#Milano</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">The Price Check</div>
  <h2 class="products-hdr" id="price">What Alba Costs Next to Brands We Know</h2>
  <p class="cat-kicker">Alba is priced like a luxury label. Here is what the same jobs cost from brands we&rsquo;ve already covered.</p>
""" + TABLE + """
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">How It Fits</div>
  <h2 class="products-hdr" id="fit">Sizing, Shipping and Where to Start</h2>
  <p class="cat-kicker">Most pieces run S to XXL; the Haar vest and Rime base layer come in paired sizes (S/M, M/L, L/XL). Alba doesn&rsquo;t publish a size chart we could read, so check the chart on each product page before you order, because returns from the US are at your own cost. Prices show in dollars for US visitors and may differ slightly from the euro conversions here. Orders ship by courier from Italy for &euro;35, with duties paid on delivery. If you want to try the brand, start with the $174 Voar polo or the $269 Grian.</p>
</section>
"""
FAQ = [
 ("Where is Alba Golf from?", "Milan, Italy. Alba describes itself as a contemporary golfwear brand born in Milan, and its collection as born from Scotland's wild skies and shaped in Milan."),
 ("When did Alba Golf launch?", "Its first collection, FW26, went live on its store in October 2026 with 24 pieces."),
 ("How much does Alba Golf cost?", "From about $56 for the pouch and caddie towel to about $616 for the Crest Jacket. Polos run about $174 to $291."),
 ("Does Alba Golf ship to the US?", "Yes. Orders ship by courier from Italy for a flat 35 euros, and US customers pay import duties on delivery. Returns are accepted within 14 days at the customer's cost."),
 ("What is the best Alba Golf piece?", "The Grian quarter-zip polo, in an exclusive REDA 1865 merino and lyocell fabric with a collar that zips into a stand collar or opens into a polo collar."),
]
_LB = [("lb-0", "Alba Golf campaign: one golfer in a salmon cap shot as a multiple-exposure swing sequence", "One swing, start to finish"),
 ("lb-5", "A grassy links dune under a grey sky, from Alba&rsquo;s site", "Scotland&rsquo;s wild skies")]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _LB)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">The Launch, in Photos</h2>
  <p class="cat-kicker"><strong>From Alba&rsquo;s site &middot; two photos</strong>The full swing and the landscape the brand says it came from.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/alba/frames.json").read_text())
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
    <span>Brand to Know &middot; Milan &middot; Launched October 2026</span><span class="dot"></span>
    <span>All 24 pieces in 16 cards &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Alba Golf launch campaign: one golfer in a salmon cap and dark jacket, shot as a multiple-exposure swing sequence" fetchpriority="high" /></div></div>
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
