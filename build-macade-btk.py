#!/usr/bin/env python3
"""build-macade-btk.py — Brand to Know: Macade.
30 September 2026.

Lenny: "let's do a brand to know - https://macadegolf.com/", then "start building
the post" after the 26-option grid with my starred 18. Two swaps for stock: the
ArcWeave Trouser (down to one size) and the TX Links Windbreaker (small only) are
out; the Padded Core Tech Jacket is in.

FACTS: Macade's own pages (the-brand, macade-worldwide, the Clubhouse page,
hydrocore, knit-capsule, fall-26, ambassadors) and product copy, read 30 Sep 2026.
Stockholm, founded 2019. No founder is named on the brand's site, so none here.
Launch dates are the US store's publish dates (Fall 26: 14 Aug; Knit Capsule:
26 Aug; HydroCore: 23 Sep).

QUOTES: verbatim from Macade's own launch pages. PHOTOS: Macade's own (launch
pages and product images), localised to images/macade/. No press photos.
Prices and stock read 30 Sep 2026 from the US store, USD. No feed card yet.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-macade"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/macade"
FR = json.loads((ROOT / "research/macade/frames.json").read_text())
SHOP = "https://macadegolf.com/products/"
BRAND = "Macade"
BRAND_T = "Macade"

TITLE = "Macade Golf — The Swedish Brand Built for Bad Weather"
DESC = ("Macade is the Stockholm golf brand behind the HydroCore rain jacket and a merino Knit Capsule. "
        "The story, the Clubhouse HQ and 19 picks from $50 to $350.")
H1 = "Brand to Know: Macade &mdash; Swedish Golf Clothes for Bad Weather"

P = {
 "hydrocore-rain-jacket-green": ("HydroCore Rain Jacket", "Green &middot; new 23 September", "350",
   "Macade calls this its most technical piece to date. It is a three-layer shell with a bonded waterproof membrane rated to 20,000mm, a PFAS-free ZEALAN DWR finish, taped seams and YKK AquaGuard two-way zips, cut in a regular fit. There is a women&rsquo;s version at the same price."),
 "hydrocore-rain-trousers-green": ("HydroCore Rain Trousers", "Green", "250",
   "The matching trousers use the same three-layer shell, with long side-leg zips so they go on over your shoes between holes. Wear them with the jacket for the full HydroCore rain suit."),
 "black-padded-core-tech-jacket": ("Padded Core Tech Jacket", "Black", "320",
   "Macade built this for golfers who stretch the season as far as it goes. It is a padded thermal jacket with zip pockets at the chest and waist, and the full-length zip has a pull you can use with gloves on."),
 "therma-hoodie-zip-taupe": ("Therma Zip Hoodie", "Taupe &middot; Fall &rsquo;26", "160",
   "This is an insulated hoodie with a high neck, a generous hood and a half zip, warm without the bulk of a jacket. It is the layer for the Austin mornings that start cold and dry, which is most of them from November to March."),
 "storm-wind-shirt-dark-blue": ("Storm Wind Shirt", "Dark Blue", "195",
   "This is a water-repellent windbreaker in smooth stretch fabric, with a half zip, short sleeves, a slim hood and zip pockets. It is the layer for a gusty morning when a full jacket is too much."),
 "arcweave-gilet-ashwood": ("ArcWeave Gilet", "Ashwood", "195",
   "The vest is cut from ArcWeave, Macade&rsquo;s textured cotton-wool blend and the fabric story of Fall &rsquo;26. It adds warmth through the chest without getting in the way of the swing."),
 "flow-light-knit-hoodie-pine": ("Flow Light Knit Hoodie", "Pine &middot; Knit Capsule", "245",
   "This is the hero of the Knit Capsule. The new blend is 45% extrafine merino and 55% ThermoCool, with a hollow core that pulls moisture off the skin and holds warmth. It has a low hood, four-way stretch and a regular fit, and it goes in the washing machine."),
 "flow-light-bomber-neck-camel": ("Flow Light Bomber Neck", "Camel &middot; Knit Capsule", "225",
   "The same merino and ThermoCool knit comes with a bomber collar and a close cut for layering. Macade built the capsule for the edges of the season, and this is the one for a cold first tee that turns warm by the back nine."),
 "theo-knit-polo-sweater-grey-melange": ("Club Knit Polo", "Striped Grey Melange", "180",
   "Macade knits this polo sweater in a cotton-cashmere blend with four-way stretch yarn and a relaxed fit, heavy enough to wear as a layer on its own. The grey, white and green stripe is the most classic thing in the collection."),
 "club-knit-polo-rust": ("Club Knit Polo", "Rust", "180",
   "This is the same knit polo in rust, the colour of Macade&rsquo;s fall. Medium, large and XL were in stock when we checked."),
 "airlite-henley-sweater-navy": ("Airlite Henley Sweater", "Navy", "180",
   "This midweight henley is cut from Macade&rsquo;s Airlite fabric, relaxed but structured, and designed to go over a polo. A small red crest sits on the chest."),
 "tx-intarsia-knit-crewneck-rust": ("TX Intarsia Knit Crewneck", "Rust", "160",
   "Macade knits its line, Stay on Course, across the chest of this cotton-cashmere crew in script. It is meant for the clubhouse as much as the course, and it is the one piece here that says the brand name out loud."),
 "clayton-core-shirt-green": ("Clayton Core Shirt", "Green", "130",
   "This polo is cut from a dense waffle fabric with a structured drape that holds its shape through a round. Macade pitches it for mild days, which in Austin means most of the winter."),
 "brooks-wayline-shirt-dark-green": ("Brooks Wayline Shirt", "Dark Green", "120",
   "This lightweight stretch polo has a smooth technical face, a sharp collar and a subtle tonal pattern. It is the warm-day shirt of the fall range."),
 "flight-green-palm-shirt": ("Flight Shirt", "Green Palm", "85",
   "The Flight is a featherweight polo with four-way stretch and a pale all-over palm print, and at $85 it is the least expensive shirt here. It has been in the range since February."),
 "lightweight-tapered-trouser-stone-blue": ("Lightweight Tapered Trouser", "Stone Blue", "130",
   "The core trouser is now cut with ROICA, a Japanese stretch elastane that recovers well and keeps its shape. It is tapered and made for hot rounds, in six colours with inseams from 30 to 36."),
 "green-cashmere-blend-course-beanie": ("Cashmere Blend Course Beanie", "Green", "60",
   "This is a cashmere-blend pom beanie with a cream stripe and the script logo, made for cold-weather rounds."),
 "dark-green-tour-belt": ("Men&rsquo;s Tour Belt", "Dark Green", "65",
   "The belt has a leather front, a woven elastic strap and a metal logo on the buckle. The dark green matches the rest of the fall palette."),
 "black-rope-course-snapback": ("Rope Course Snapback", "Black", "50",
   "This structured A-frame cap is made in a cotton-elastane blend, with a rope across the brim and Stay on Course embroidered in script."),
}

SECTIONS = [
    ("rain", "Built for the Weather", "built-for-the-weather",
     ["hydrocore-rain-jacket-green", "hydrocore-rain-trousers-green", "black-padded-core-tech-jacket", "storm-wind-shirt-dark-blue", "therma-hoodie-zip-taupe", "arcweave-gilet-ashwood"],
     "<strong>Six layers &middot; $160&ndash;$350</strong>The new HydroCore rain suit, a padded jacket for the coldest rounds, a wind shirt, an insulated zip hoodie and an ArcWeave vest."),
    ("knits", "The Knits", "the-knits",
     ["flow-light-knit-hoodie-pine", "flow-light-bomber-neck-camel", "theo-knit-polo-sweater-grey-melange", "club-knit-polo-rust", "airlite-henley-sweater-navy", "tx-intarsia-knit-crewneck-rust"],
     "<strong>Six knits &middot; $160&ndash;$245</strong>Two pieces from the merino Knit Capsule, two cotton-cashmere knit polos, a henley and the Stay on Course crew."),
    ("shirts", "Shirts &amp; Trousers", "shirts-and-trousers",
     ["clayton-core-shirt-green", "brooks-wayline-shirt-dark-green", "flight-green-palm-shirt", "lightweight-tapered-trouser-stone-blue"],
     "<strong>Four pieces &middot; $85&ndash;$130</strong>Macade makes three polos for milder days, and the core tapered trouser comes in six colours."),
    ("details", "The Details", "the-details",
     ["green-cashmere-blend-course-beanie", "dark-green-tour-belt", "black-rope-course-snapback"],
     "<strong>Three pieces &middot; $50&ndash;$65</strong>The beanie is a cashmere blend, the belt matches the fall green, and the snapback carries the brand line."),
]

PQ = {
    "tool": ("This is not apparel. This is a tool.", "Macade, on the HydroCore launch page"),
    "announce": ("Golf clothing shouldn&rsquo;t announce itself from across the room; it should feel just as right leaning over a putt as it does settling in at the clubhouse.",
                 "Macade, on the Knit Capsule launch page"),
    "clubhouse": ("Every team member&rsquo;s golf clubs line the walls. Putters are out to share. Drinks are always one degree above freezing.",
                  "Macade, on its Stockholm Clubhouse"),
}

BANDS = {
    "rain": ("Photography &middot; Macade&rsquo;s own", "This is the HydroCore campaign: green rain suits, grey skies and a bag on the shoulder.",
             [("band-a1", "A golfer kneeling on the fairway in green Macade HydroCore rain trousers and jacket", "HydroCore"),
              ("band-a2", "A golfer in a green Macade HydroCore rain suit beside a stand bag on the course", "The rain suit"),
              ("band-a3", "A woman in the green Macade HydroCore rain jacket and trousers beside her golf bag", "Women&rsquo;s HydroCore")]),
    "knit": ("Photography &middot; Macade&rsquo;s own", "The Knit Capsule was shot in wood-panelled rooms, the clubhouse after the round.",
             [("band-b1", "A man in a dark green Macade knit polo and cream trousers in a wood-panelled room", "Knit Capsule"),
              ("band-b2", "A man and a woman in Macade knitwear in an old library", "The capsule"),
              ("band-b3", "A man in a camel Macade Flow Light bomber-neck knit with arms crossed", "Flow Light")]),
    "fall": ("Photography &middot; Macade&rsquo;s own", "Fall &rsquo;26 on the course, the Clubhouse in Stockholm, and Ewen Ferguson.",
             [("band-c1", "A golfer in a navy Macade layer and brown trousers beside his bag near a bunker", "Fall &rsquo;26"),
              ("band-c2", "The Macade Clubhouse in Stockholm with a putting green, racks of clothes and a shop wall", "The Clubhouse, Stockholm"),
              ("band-c3", "Ewen Ferguson swinging in a dark Macade polo", "Ewen Ferguson")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Why Macade, and why in Austin? Because our season never really stops, and the hard part of it is not the rain. It is a 7:40 tee time at Lions in January, in the low 40s on the first tee and 65 by the turn, with a north wind across the back nine. Macade, a Stockholm brand founded in 2019, builds for exactly that swing in temperature. Three collections landed on its US store in six weeks this fall, Fall &rsquo;26, the Knit Capsule and HydroCore rainwear, and all three are about layers that keep working when the round changes on you.</p>
    <p>It is for the year-round player who walks, carries and goes somewhere after the round. The look is clean and quiet: deep green, rust, camel and navy, script logos and nothing loud. It suits the golfer who wants to look put together at Muny and at dinner on South Congress in the same clothes, not the one who wants a big print on the first tee.</p>
    <p>Is it good value? It is expensive, and some of it earns the price more than the rest. The Flow Light Knit Hoodie is $245, and it is the piece we would pay for: a merino and ThermoCool blend that handles a 25-degree swing, goes in the washing machine and passes for a normal sweater off the course. The Lightweight Tapered Trouser at $130 and the $85 Flight Shirt are the sensible way in, and they will carry you through an Austin summer. The HydroCore rain suit is the best-built thing here, but at $600 for the jacket and trousers it is for the golfer who travels to play in Scotland or the Pacific Northwest. In Austin, when it pours, we go to the range.</p>
    <p>Prices were read from Macade&rsquo;s US store on 30 September 2026, in US dollars. It ships from the US with free shipping and returns, so you can try the fit before you commit.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Macade says it started in 2019 to reimagine golf apparel for a new generation, with a handful of technical, sharply tailored pieces, and that it has now dressed more than 150,000 golfers. The brief is performance built on Scandinavian design principles, and the company says every piece is tested against what professional golfers need.</p>
    <p>Home is the Macade Clubhouse on Torsgatan in central Stockholm. It is the company&rsquo;s global headquarters, with a golf simulator, a shop and the staff&rsquo;s own clubs on the walls. The tour team includes Scotland&rsquo;s Ewen Ferguson on the DP World Tour, Dylan Naidoo, who won the 2025 South African Open, the LPGA&rsquo;s Gabriella Then and the LET&rsquo;s Harang Lee. In the US, the brand is stocked in the shops at TPC Scottsdale and Big Cedar Lodge in Missouri.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Stockholm, Sweden</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>2019</span></div>
      <div class="sidebar-detail"><span class="l">HQ</span><span>The Macade Clubhouse, Torsgatan</span></div>
      <div class="sidebar-detail"><span class="l">Tour team</span><span>Ewen Ferguson, Dylan Naidoo, Gabriella Then</span></div>
      <div class="sidebar-detail"><span class="l">US shipping</span><span>From the US, free returns</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$50&ndash;$350</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Flow Light Knit Hoodie, $245</span></div>
      <a href="https://macadegolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Macade &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MacadeGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#StayOnCourse</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Where is Macade Golf from?",
     "Stockholm, Sweden. Macade was founded in 2019, and its global headquarters is the Macade Clubhouse on Torsgatan in central Stockholm."),
    ("Does Macade ship to the US?",
     "Yes. Macade's US store ships from the United States, prices in US dollars, and offers free shipping and returns."),
    ("Is the Macade HydroCore rain jacket waterproof?",
     "Yes. It is a three-layer shell with a waterproof membrane rated to 20,000mm, a PFAS-free DWR finish, taped seams and YKK AquaGuard zips. It costs $350, and the matching trousers are $250."),
    ("What is the Macade Knit Capsule?",
     "A fall 2026 collection of knitwear in a new blend of 45% extrafine merino wool and 55% ThermoCool fibre, which wicks moisture, holds warmth and is machine washable. The Flow Light Knit Hoodie ($245) is the hero piece."),
    ("Is Macade good for golf in Austin?",
     "For fall and winter, yes. Its knits and light layers are built for rounds that start cold and warm up, which is most Austin mornings from November to March. The Lightweight Tapered Trouser ($130) and Flight Shirt ($85) work in summer. The $350 HydroCore rain jacket is more than most Austin golfers need."),
    ("Which tour players wear Macade?",
     "Macade's tour team includes Ewen Ferguson (DP World Tour), Dylan Naidoo (2025 South African Open winner), Gabriella Then (LPGA) and Harang Lee (LET)."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-MAC-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-MAC-PQ-{key} -->\n')

def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(h, idx):
    name, detail, price, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"Macade {name} {detail}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{BRAND} &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; ${price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{SHOP}{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"Piece" if len(ids) == 1 else "Pieces"}</div>\n'
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
        for h in ids:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"Macade {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-30", "dateModified": "2026-09-30",
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
            {"@type": "ListItem", "position": 3, "name": "Macade", "item": URL}]},
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
    ids = [h for s in SECTIONS for h in s[3]]
    assert len(ids) == 19 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Macade</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Stockholm, Sweden &middot; since 2019</span><span class="dot"></span>
    <span>19 pieces &middot; $50&ndash;$350</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a green Macade rain suit walking over a rise with his bag under a heavy grey sky" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("rain") + pq("tool")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + band("knit") + pq("announce")
    s, n = section(SECTIONS[1], n); body += s + band("fall")
    s, n = section(SECTIONS[2], n); body += s + pq("clubhouse")
    s, n = section(SECTIONS[3], n); body += s
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
    for leak in ("Manors Revisited", "Nicklaus", "Chewning", "Australian"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 19:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != 3:
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
