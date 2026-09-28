#!/usr/bin/env python3
"""build-sugarloaf-autumn.py — Sugarloaf Social Club's Autumn Layers, 12 picks.
27 September 2026.

Lenny: "let's do a post about sugarloafs new drop" (collections/autumn-layers).
He saw the 22-option grid (sugarloaf-autumn-options-2026-09-27.html), picked
the hero ("top right but don't cut off their heads", then "lower the crop
slightly split the difference") and said "looks good let's build it" — my
suggested 12.

DATA: research/sugarloaf-autumn/catalog.json. Store serves USD (/cart.js).
Prices and stock read 27 Sep 2026. Only four products are new on 22 Sep (Tech
Jacket, Windcrew, the two Hidden Gem putter covers); the post says so rather
than calling everything new.

COPY: from Sugarloaf's own product descriptions. Brand copy is quoted as brand
copy. The shoot location is given only as Ireland, because that is all the
brand says ("We took these to Ireland with us"); no course is named.

PHOTOS: Sugarloaf's own, localised to images/sugarloaf-autumn/; sources in
research/sugarloaf-autumn/frames.json and hero-pick.json. No quotes. Normal
template. No feed card; that waits for Lenny. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "sugarloaf-autumn-layers-2026"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/sugarloaf-autumn"
FR = json.loads((ROOT / "research/sugarloaf-autumn/frames.json").read_text())
SHOP = "https://www.sugarloafsocialclub.com/products/"

TITLE = "Sugarloaf Social Club's Autumn Layers: 12 Picks From the Fall Drop"
DESC = ("Sugarloaf Social Club's Autumn Layers collection: the new Tech Jacket and Windcrew, "
        "Hidden Gem putter covers and the layers to go with them. Twelve picks from $28 to $165, "
        "prices checked 27 September 2026.")
H1 = "Sugarloaf Social Club&rsquo;s Autumn Layers &mdash; 12 Picks From the Fall Drop"

# key -> (product, colour/detail, price, stock line, copy, handle, new?)
P = {
 "jacket-green": ("Tech Jacket", "Glow Green", 165, "S&ndash;XXL in stock",
   "This is a stretch-nylon full zip made from the same fabric as Sugarloaf&rsquo;s tech vests. The brand took it to Ireland and calls it &ldquo;weather resistant&rdquo;: good in a light sprinkle, not fully waterproof. It fits true to size.",
   "ssc-tech-jacket", True),
 "jacket-navy": ("Tech Jacket", "Navy", 165, "S&ndash;XXL in stock",
   "The same jacket in navy, which is the one most of the Ireland photographs show on the course. It is the piece we would pack for a wet round.",
   "ssc-tech-jacket", True),
 "windcrew-stone": ("Windcrew", "Stone", 150, "S&ndash;XXL in stock",
   "Sugarloaf describes this as its dream 90s windshirt: a thin retro silhouette, stretchy, a little roomy, with a waistband that is flat at the front and elastic at the back. The brand calls it &ldquo;one of the coolest things we have ever made.&rdquo;",
   "windcrew", True),
 "windcrew-navy": ("Windcrew", "Navy", 150, "S&ndash;XXL in stock",
   "The navy has purple panels down the sleeves and the small SSC arrows on the chest. It fits true to size.",
   "windcrew", True),
 "vest-red": ("Tech Vest", "Dark Red", 115, "S&ndash;XXL in stock",
   "This is the vest the Tech Jacket was built from, with zip pockets and the SSC arrow on the back. Sugarloaf calls it perhaps its favourite piece, and the dark red is the fall colour of the six.",
   "tech-vest-2026", False),
 "vest-navy": ("Tech Vest", "Navy", 115, "S&ndash;XXL in stock",
   "This is the same vest in navy, and it works over a long-sleeve polo or under the Windcrew. The brand&rsquo;s line is that it works on the course and walking down Wall Street.",
   "tech-vest-2026", False),
 "windshirt": ("Windshirt", "Stone/Navy", 125, "S&ndash;XXL in stock",
   "This short-sleeve half-zip came in late summer. It is stretchy and breathable, with a mesh lining and a vented back. It repels wind and water. If you are between sizes, Sugarloaf says size up.",
   "windshirt", False),
 "mallet": ("Hidden Gem Mallet Putter Cover", "Nylon", 95, "In stock",
   "This is a nylon mallet cover in bright blue with the Hidden Gem artwork, made in the USA for Sugarloaf by EP. Hidden Gem is a recurring Sugarloaf collection, with its own map page on the brand&rsquo;s site.",
   "hidden-gem-mallet-putter-cover", True),
 "blade": ("Hidden Gem Blade Putter Cover", "Nylon", 95, "In stock",
   "This is the blade version of the same cover, also nylon and made in the USA. Buy the one that matches your putter; they are the two newest things in the collection.",
   "hidden-gem-blade-putter-cover", True),
 "bigarrow": ("Big Arrow Cover", "Driver", 135, "Driver in stock; fairway sold out",
   "This is a plush leather driver cover with a big red arrow, made in the USA. Sugarloaf compares it to an oven mitt for your driver, and says it might double as a boxing glove.",
   "big-arrow-cover", False),
 "polo-spruce": ("The Club Stripe Polo", "Spruce Green", 95, "S&ndash;XL in stock",
   "This pique polo is 94% polyester and 6% spandex, with a softer shoulder for 2026. It is true to size: not slim, not boxy. The spruce green stripe is the one to wear under a vest this fall.",
   "the-club-stripe-polo", False),
 "socks": ("Sleeve Socks, 3-Pack", "Grey, Navy &amp; White", 28, "S/M and M/L in stock",
   "You get three pairs of mid-ankle socks, each with a different coloured sole so you can tell which ones go together, and the SSC arrow on the back.",
   "sock-3-pack", False),
}

SECTIONS = [
    ("layers", "The Layers", "the-layers", ["jacket-green", "jacket-navy", "windcrew-stone", "windcrew-navy", "vest-red", "vest-navy", "windshirt"],
     "<strong>Seven pieces &middot; the reason for the drop</strong>The Tech Jacket and Windcrew are new this month. The vest and windshirt came in over the summer and belong in the same stack."),
    ("covers", "The Covers", "the-covers", ["mallet", "blade", "bigarrow"],
     "<strong>Three covers &middot; made in the USA</strong>Two new nylon Hidden Gem putter covers and the leather Big Arrow for the driver."),
    ("under", "Under It All", "under-it-all", ["polo-spruce", "socks"],
     "<strong>Two pieces &middot; the base layer</strong>A striped polo for under the vest, and the socks Sugarloaf named after a sleeve of balls."),
]

BANDS = {
    "covers": ("Photography &middot; Sugarloaf in Ireland",
               "Sugarloaf shot the jackets on a links course in Ireland, in exactly the weather they are made for.",
               [("band-b1", "A golfer in a navy Windcrew walking past a black-and-white Tudor clubhouse", "Past the clubhouse"),
                ("band-b2", "A golfer in a stone Windcrew playing out of a pot bunker with the sea behind", "Out of the pot bunker"),
                ("band-b3", "A smiling golfer in a navy Tech Jacket and yellow beanie carrying his bag by the car park", "Car park, first tee")]),
    "under": ("Photography &middot; Sugarloaf&rsquo;s summer shoots",
              "The vest, windshirt and polo came in earlier; this is how the brand shot them.",
              [("band-b4", "A man in a yellow Tech Vest sitting in the back of a car full of golf gear", "Tech Vest, road trip"),
               ("band-b5", "A man in a Windshirt riding a bicycle with a golf bag through a city street", "Windshirt, in the city"),
               ("band-b6", "A man in a navy striped polo sitting on a dock bench with a duffel bag", "Club Stripe Polo")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>There is no studio and no swing sequence. Sugarloaf took the new jackets to an Irish links and shot two friends in red and yellow beanies carrying pencil bags under a grey sky, with a rainbow nobody planned. It looks like a trip, not a campaign, and that is the point.</p>
    <p>The Windcrew is the news. It is a roomy 90s pullover, and the navy one puts purple panels down the sleeves where most brands would play it safe. The Tech Jacket is the vest fabric with sleeves added, and its Glow Green, a pale mint with a blue zip, is the colour we did not expect in a fall drop. The rest stays quiet: small SSC arrows, clean zips.</p>
    <p>The joke is the covers. The Hidden Gem putter covers are bright blue nylon with the brand&rsquo;s illustration, loud next to the muted jackets, and very Sugarloaf. Our pick is the Windcrew at $150. Prices were read from Sugarloaf&rsquo;s store on 27 September 2026, in US dollars. More in our <a href="/drops/brand-to-know-sugarloaf-social-club">Sugarloaf Brand to Know</a> and its <a href="/drops/sugarloaf-ss26">spring collection</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Drop</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Sugarloaf Social Club</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>Autumn Layers</span></div>
      <div class="sidebar-detail"><span class="l">New</span><span>Tech Jacket &amp; Windcrew</span></div>
      <div class="sidebar-detail"><span class="l">Also new</span><span>Two putter covers</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>12</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$28&ndash;$165</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Windcrew, $150</span></div>
      <a href="#the-layers" class="sidebar-cta">Start with the layers &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#SugarloafSocialClub</span>
        <span class="hashtag">#AutumnLayers</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is in Sugarloaf Social Club's Autumn Layers collection?",
     "Ten products as of 27 September 2026. New on 22 September: the SSC Tech Jacket ($165), the SSC Windcrew ($150) and the Hidden Gem mallet and blade putter covers ($95 each). The collection also gathers the Tech Vest, Windshirt, Big Arrow Cover, Club Stripe Polo, Sleeve socks and a pair of milk glass mugs."),
    ("Is the Sugarloaf Tech Jacket waterproof?",
     "No. Sugarloaf calls it weather resistant: it handled a light sprinkle when the brand wore it in Ireland, but the brand says it is not fully waterproof."),
    ("What is the difference between the Windcrew and the Windshirt?",
     "The Windcrew ($150) is a new long-sleeve pullover with a 90s shape, roomy and stretchy. The Windshirt ($125) is a short-sleeve half-zip from late summer with a mesh lining and a vented back."),
    ("How does Sugarloaf clothing fit?",
     "Sugarloaf says the Tech Jacket, Windcrew and Club Stripe Polo fit true to size. For the Windshirt it recommends sizing up if you are between sizes."),
    ("Who is behind Sugarloaf Social Club?",
     "Ian Gilley. It began as a group of friends in 2011 and became a golf brand known for its collaborations and its recurring Hidden Gems collection."),
]


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(k, idx):
    name, colour, price, stock, copy, handle, new = P[k]
    fr = [f["local"] for f in FR[k]]
    label = H.unescape(f"Sugarloaf {name} {colour}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    tag = " &middot; New" if new else ""
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">Sugarloaf &middot; {colour}{tag}</div>'
            f'<div class="product-name">{name} &middot; ${price}</div>'
            f'<div class="product-desc">{copy} {stock} on 27 September.</div>'
            f'<a href="{SHOP}{handle}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} Pieces</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for _, _, _, ids, _ in SECTIONS:
        for k in ids:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[k][5],
                          "name": H.unescape(f"Sugarloaf Social Club {P[k][0]}, {P[k][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-27", "dateModified": "2026-09-27",
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
            {"@type": "ListItem", "position": 3, "name": "Sugarloaf Autumn Layers", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[3]]
    assert len(ids) == 12 == len(set(ids)) and set(ids) == set(P)
    for k in ids:
        assert FR.get(k), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Sugarloaf Autumn Layers</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 27, 2026</span><span class="dot"></span>
    <span>Sugarloaf Social Club &middot; Fall 2026</span><span class="dot"></span>
    <span>12 picks &middot; $28&ndash;$165</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Two golfers in red and yellow beanies carrying bags across a links course in Ireland under a rainbow" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for sec in SECTIONS:
        if sec[0] in BANDS:
            body += band(sec[0])
        s, n = section(sec, n)
        body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited"):
        if leak in above:
            bad.append(f"donor leak {leak}")
    if fin.count('class="product-card"') != 12:
        bad.append("card count")
    if 'class="pull-quote"' in above:
        bad.append("pull-quote")
    if above.count('class="ig-grid"') != 2:
        bad.append("band count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
