#!/usr/bin/env python3
"""build-fall-pants-2026.py — 12 Fall Golf Pants. 29 October 2026. Cloned from build-golden-soul-btk.py.
Lenny: "Let's do a round up of 12 fall Pants" -> options -> "focus on just the mens pants, prioritize the pants with the best photos, skip Reigning Champ".
FACTS: each store's product .js, read in Chrome 29 Oct 2026 (USD presentment; Odd Ritual in ZAR, ~0.0573 USD/ZAR via Wise). research/fall-pants/final.json.
OLD HEADER (Golden Soul):
Lenny: "Let's do a brand to know - goldensoulgolf.com" -> options -> "less bags and more headcovers" -> "let's build it with good lookbook and IRL images" (all 52 from options v2).
FACTS: goldensoulgolf.com About/Mission/Vision + product copy (research/golden-soul/catalogue.json, 28 Oct 2026, USD); Bisque Golf collection page. No founder is published: never name one.
OLD HEADER (Penta):
Lenny: "Let's do a brand to know - https://penta-golf.com/" -> options sheet -> "Lets build the post" (all 20: 14 in stock + 6 sold out).
FACTS: penta-golf.com About + live catalogue (research/penta/catalogue.json, USD, 28 Oct 2026); Monster Children Q&A (Feb 2024).
Founders stay unnamed (the brand never names them). Never "worth".
OLD HEADER (Paré):
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "12 Fall Golf Pants for 2026: Cord, Wool, Pleats and Canvas"
DESC = ("Twelve men's golf pants for fall 2026 from independent brands: corduroy from STITCH and Ashworth, wool from Students, "
        "pleats from Public Drip, Walker, Metalwood and Odd Ritual, and canvas from SLOAT and Malbon. With prices.")
H1 = "12 Fall Golf Pants for 2026: Cord, Wool, Pleats and Canvas"
BC = "12 Fall Golf Pants"
SLUG = "fall-golf-pants-2026"
IMG = "/images/fall-pants-2026"
SHOP = ""
SO = " &middot; sold out"
_F = {c["k"]: c for c in json.loads((ROOT / "research/fall-pants/final.json").read_text())}
COPY = {
 "stitch-bedford": "Our pick. A soft-washed corduroy with a stretch waistband, cut to look like a dress trouser but sit like a chino. Drift and Forged Gray are $158; Oyster and Seagrass were marked down to $55 when we checked.",
 "ashworth-pierside": "Fine-wale corduroy, garment-washed so it feels broken in, with a hint of stretch. Ashworth notes a 32-inch inseam. The cheapest full-price pair here, in sizes 30 to 44.",
 "students-tradition": "A half-wool, half-polyester trouser with double pleats and a relaxed leg, made for cold mornings. It has satin trim inside. The color is Cement, sizes 30 to 40.",
 "pd-pinstripe": "A suit trouser rebuilt for golf: double pleats, a straight tapered leg and a light nylon blend with some stretch. The pinstripe is the one to own.",
 "pd-charcoal": "The same Anywhere Pleated Pant in a blue-grey charcoal, the version that goes with everything. Sizes 28 to 38.",
 "walker-easy": "&ldquo;The pant between the fairway and Friday night,&rdquo; says Walker. A soft, light fabric with a relaxed pleat, deep side pockets and a hidden inside pocket. Shown on Australia&rsquo;s Sunshine Coast, kangaroos included.",
 "metalwood-western": "A permanent front crease, a drawstring and elastic waist, and a cotton-poly blend with stretch. Metalwood&rsquo;s note: &ldquo;We tested them on an airplane. Wasn&rsquo;t miserable for once.&rdquo;",
 "odd-ritual-daily": "Made in Cape Town from 235gsm cotton twill, loose with a slight carrot taper, front pleats and an elastic back waist. The store prices in rand: R990, or about $57.",
 "sloat-caddie": "SLOAT&rsquo;s heavyweight pant, inspired by what caddies wear: 305gsm organic cotton, sewn in Portugal, cut straight so it drapes. Marshmallow is the color for fall.",
 "malbon-scouting": "A wide, straight-leg cotton canvas pant, stone-washed, with big patch pockets and Malbon&rsquo;s wildlife print in olive. The loudest pair here.",
 "malbon-seoul": "From Malbon&rsquo;s Studio Seoul line: a regular-fit nylon-elastane pant that feels like cotton, with extra pocket details. Navy, sizes S to XL.",
 "walker-kooka": "Walker&rsquo;s all-rounder: dry-touch stretch twill, a relaxed fit with a slight taper, an inside ball-marker pocket and tee slots on the back.",
}
P = {k: (_F[k]["brand"], _F[k]["t"], _F[k]["price"], _F[k]["url"], COPY[k]) for k in COPY}
SECTIONS = [
 ("Cord and Wool", "cord-wool", ["stitch-bedford", "ashworth-pierside", "students-tradition"],
  "<strong>Three pairs &middot; $95&ndash;$158</strong>The warmest fabrics here: two corduroys and a wool-blend trouser."),
 ("Pleats", "pleats", ["pd-pinstripe", "pd-charcoal", "walker-easy", "metalwood-western", "odd-ritual-daily"],
  "<strong>Five pairs &middot; about $57&ndash;$170</strong>Fall is when the pleated trouser makes the most sense on the course. Five takes, from a pinstripe to a track pant."),
 ("Canvas and Twill", "canvas-twill", ["sloat-caddie", "malbon-scouting", "malbon-seoul", "walker-kooka"],
  "<strong>Four pairs &middot; $110&ndash;$268</strong>Heavier cottons and a couple of technical twills for days that start cold and warm up."),
]
N = 12
PQ = {
 "pleats": ("The pant between the fairway and Friday night.", "Walker Golf Things, on the Pleated Easy Pant"),
}
BANDS = {
 "cord-wool": ("In the shop", "Public Drip and Odd Ritual both shot their fall pants indoors, among shelves and leather bags.",
   [("band-pd-charcoal-2", "A man in the charcoal Public Drip pleated pants and a cap standing in front of shelves of folded clothes", "Public Drip, Anywhere Pleated Pants"),
    ("band-pd-pinstripe-2", "A man in the pinstripe Public Drip pleated pants with arms crossed in front of shelves", "The pinstripe"),
    ("band-odd-ritual-daily-2", "A man in black Odd Ritual pleated trousers holding a coffee cup beside a leather bag", "Odd Ritual, Cape Town")]),
 "canvas-twill": ("In the studio", "The rest of the campaigns, from SLOAT, Metalwood and Students.",
   [("band-sloat-caddie-2", "A man in a navy polo and cream SLOAT Caddie Pants on a tan backdrop", "SLOAT Caddie Pant"),
    ("band-metalwood-western-4", "A man from behind in a grey jacket and brown Metalwood pleated track pants", "Metalwood, from behind"),
    ("band-students-tradition-2", "A man in a cream vest and grey double-pleated Students wool trousers", "Students, Tradition Wool Pant")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Fall is the best season for golf pants. The shorts go away, the mornings are cold enough for wool, and a pleated trouser stops looking like a costume. We went through the fall stores of more than twenty independent brands and kept the twelve men&rsquo;s pants with the best fabrics and the best photos, so you can see how they actually fit.</p>
    <p><strong>What&rsquo;s here.</strong> Two corduroys, from STITCH and Ashworth. A wool-blend double-pleat from Students. Five pleated pants, including Public Drip&rsquo;s pinstripe, Walker&rsquo;s Pleated Easy Pant and a $57 pair made in Cape Town by Odd Ritual. And four heavier cottons and twills, from SLOAT&rsquo;s 305gsm Caddie Pant to Malbon&rsquo;s wildlife-print canvas.</p>
    <p><strong>How to wear them.</strong> Fall pants look best with a little more weight up top than summer shorts ever needed. Corduroy and wool go with a knit polo or a quarter-zip in a darker color, and a brown or green cord is the easiest way to look like you dressed for the season. Pleats want a slightly fuller top and a clean shoe, and they should break once at the ankle, not pool. The heavier cottons, like SLOAT&rsquo;s Caddie Pant and Malbon&rsquo;s canvas, work the way good work pants do: they get better after a few washes and a few muddy walks back to the car.</p>
    <p><strong>What we left out.</strong> Rain pants, joggers, sweatpants and anything down to its last size. Prices are in US dollars as each store showed them on October 29, 2026, except Odd Ritual, which prices in rand.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Pants</span><span>12, from 9 brands</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>About $57&ndash;$268</span></div>
      <div class="sidebar-detail"><span class="l">Fabrics</span><span>Cord, wool, cotton, twill</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>STITCH Bedford Corduroy</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 29, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfPants</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#TheEdit</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">How We Picked</div>
  <h2 class="products-hdr" id="how-we-picked">Fabric First, Then the Photos</h2>
  <div class="writeup-body">
    <p>We started with fabric: corduroy, wool, heavier cottons and brushed or dry-touch twills, the things that make a pant feel like fall. Then we kept only the pairs with good photos on the brand&rsquo;s own site, on a person or out on a course, because a pant you can&rsquo;t see on a body is a pant you can&rsquo;t judge.</p>
    <p>We also looked at how each brand describes its own fit, because golf pants vary more than most. Public Drip cuts a straight leg with a taper, Metalwood and SLOAT cut theirs straight, Ashworth calls its cord tailored, and Malbon&rsquo;s Scouting Pant and Odd Ritual&rsquo;s Daily Trouser run wide and relaxed on purpose. Check each brand&rsquo;s size chart before you order, especially from Walker in Australia and Odd Ritual in South Africa, where sizing and shipping times differ from US stores.</p>
    <p>Every pair was in stock in at least three sizes when we checked. If you want more, our earlier <a href="/drops/the-pants-edit">Pants Edit</a> and <a href="/drops/best-golf-pants-ranked">golf pants ranking</a> cover Manors, Sentinel, Odd Ritual and others.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/fall-pants/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-29", "dateModified": "2026-10-29",
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
    <span>The Edit &middot; Fall 2026</span><span class="dot"></span>
    <span>12 pants from 9 brands &middot; checked October 29, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in navy Walker pleated pants on a fairway with two kangaroos grazing behind" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
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
