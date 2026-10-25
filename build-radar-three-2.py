#!/usr/bin/env python3
"""build-radar-three-2.py — On Our Radar Vol. 2: Dim Sum Golf Club, Rowena Golf Club, DRVN Golf Co. Cloned from build-radar-three.py. 19 October 2026.
Lenny: "Let's do a post about three small golf brands, three very different styles", then "8 options per brand", write-ups on each,
and a TGI Take on the differences, who might like which brand, and why independent golf is exciting.
FACTS: each store's product JSON and About pages (research/radar-three-2/), read October 19, 2026. Dim Sum prices in HKD (x0.128).
Rowena only sells six products, so all six are here; two were sold out. DRVN Golf Co. is not "DRVN Golf" (a coaching certification).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "3 Small Golf Brands: Dim Sum, Rowena and DRVN"
DESC = ("Dim Sum Golf Club, Rowena Golf Club and DRVN Golf Co.: three small golf brands with three very different styles, "
        "from Hong Kong street graphics to linen trousers to milled putters. 22 picks with prices.")
H1 = "On Our Radar: Three Small Golf Brands, Three Very Different Styles"
BC = "Dim Sum, Rowena and DRVN"
SLUG = "dim-sum-rowena-drvn-small-golf-brands"
IMG = "/images/radar-three-2"
SHOP = ""
DS, RW, DR = "Dim Sum Golf Club", "Rowena Golf Club", "DRVN Golf Co."
DSU, RWU, DRU = "https://www.dimsumgolfclub.com/store/p/", "https://rowenagolf.com/products/", "https://drvngolfco.com/products/"
P = {
 # Dim Sum Golf Club
 "13": (DS, "Breakfast Ball Headcover", "HK$385 (~$49)", DSU+"breakfast-ball-headcover",
   "Our pick from Dim Sum. A driver cover based on a Hong Kong cha chaan teng breakfast, with French toast, milk tea, macaroni and ham, an egg sandwich and spam stitched onto red faux leather. Fleece lined, driver only."),
 "14": (DS, "Minibus Sign Bag Tag", "HK$55 (~$7)", DSU+"minibus-sign-bag-tag",
   "The red lettering of a Hong Kong minibus destination sign, turned into a bag tag. The cheapest thing here and the easiest way to carry a bit of the city on your bag."),
 "17": (DS, "Sum-Day Golf Bag", "HK$1,175 (~$150)", DSU+"sum-day-golf-bag-black",
   "A light black canvas carry bag for the range or a few holes with your favorite nine clubs. Two zip pockets, one shoulder strap and an embroidered &ldquo;Dim Sum Golf Club &mdash; Hong Kong&rdquo; logo. A pre-order when we checked, shipping from November 6."),
 "19": (DS, "Good Morning Microfibre Towel", "HK$255 (~$33)", DSU+"dim-sum-hong-kong-t-shirt-gg5x7-gbrxc",
   "A take on the classic Asian washcloth, the white one with blue stripes and red lettering, at 40 by 60cm for clubs and hands. Designed and assembled in Hong Kong."),
 "30": (DS, "Chopstick T-Shirt", "HK$435 (~$56)", DSU+"chopstick-t-shirt",
   "A pair of chopsticks holding a golf ball, with the club name in Chinese and English underneath. The brand&rsquo;s best-known graphic, back in white and navy."),
 "32": (DS, "Hong Kong Masters T-Shirt", "HK$435 (~$56)", DSU+"dim-sum-masters-hong-kong-t-shir",
   "The Augusta map logo, redrawn as a yellow map of Hong Kong with a flag on it. Made from 100% cotton and designed and assembled in Hong Kong, in white or black."),
 "35": (DS, "Cart Path Only Taxi T-Shirt", "HK$435 (~$56)", DSU+"cart-path-only-taxi-t-shirt",
   "The &ldquo;Cart Path Only&rdquo; sign, with the cart swapped for one of Hong Kong&rsquo;s red taxis. A joke about two places where the rules about routes are taken seriously."),
 "40": (DS, "Temple Street Golf Market T-Shirt", "HK$435 (~$56)", DSU+"temple-street-golf-market-tshirt",
   "Kowloon&rsquo;s Temple Street Night Market reimagined as a golf market, with golf balls inside the red pendant lamps. A 250g, 100% cotton tee."),
 # Rowena Golf Club
 "44": (RW, "Griffith Linen Shorts", "$78", RWU+"griffith-linen-shorts",
   "Navy pinstripe shorts in a linen blend with double pleats, a relaxed straight leg and elastic sides at the waistband. There is a tee pocket, too. Made for hot summer rounds."),
 "45": (RW, "Finley Barrel Headcover", "$56 &middot; sold out", RWU+"finley-barrel-headcover",
   "Navy leather with a hand-stitched diamond pattern and a black velvet lining. Sold out when we checked, but it is the piece that shows the brand best, so it stays in."),
 "46": (RW, "The Rope Hat", "$38", RWU+"the-rope-hat",
   "A structured five-panel cotton twill cap with Rowena Golf in script, a small RGC flag on the side and a braided rope across the brim. Snapback, one size."),
 "47": (RW, "Sunset Polo", "$84", RWU+"sunset-polo",
   "Our pick from Rowena. A light 100% cotton knit polo with a boxy, slightly cropped fit inspired by golf&rsquo;s earlier eras, a tartan collar and lapel and an embroidered R. In green or white; size up for a traditional fit."),
 "48": (RW, "Laurel Linen Trouser", "$108", RWU+"linen-trouser",
   "Single-pleat linen trousers with a relaxed straight leg, elastic sides at the waist and a tee pocket. In navy pinstripe or cr&egrave;me, with long lengths in some sizes."),
 "49": (RW, "&ldquo;The R&rdquo; Hat", "$38 &middot; sold out", RWU+"the-r-canvas-hat",
   "An unstructured canvas five-panel with a felt R on the front and a leather strap with a metal clasp. Sold out when we checked; it is the hat in most of the brand&rsquo;s photos."),
 # DRVN Golf Co.
 "56": (DR, "Heritage One", "$1,250", DRU+"heritage-one",
   "Limited to 50 numbered pieces, with no second run. A blade in 303 stainless steel with a torched Champagne Gold finish, a zero-torque center shaft and the firmest insert in the range, the unmilled GT1-R, fitted as standard. DRVN based it on the AMG One."),
 "59": (DR, "Touring LT", "$650", DRU+"touring-lt",
   "A long mallet in Petrol Blue named after the Long Tail race cars of the late 1990s, with a swept rear and a sight line that runs the full length of the head. Machined from 6061 aluminum, zero-torque."),
 "60": (DR, "Touring Six Four", "$500", DRU+"touring-six-four",
   "Our pick from DRVN. A center-shafted, face-balanced putter in British Racing Green, modeled on the Porsche 964: rounded rear shoulders, engine-vent milling and a thin bar on the sole for the rear light. 6061 aluminum, and the least expensive putter in the range."),
 "68": (DR, "GT1 Face Insert", "$85", DRU+"gt1-face-insert-hard",
   "Every DRVN putter takes interchangeable face inserts. The GT1 is the firm one: 303 stainless steel with 45-degree milled grooves, for a sharper sound and more feedback. In silver or black."),
 "64": (DR, "MM-722 Ball Marker", "$85", DRU+"mm-722-ball-marker",
   "A ball marker shaped like the multi-spoke wheel on the Mercedes-Benz SLR McLaren 722. Milled from 303 stainless steel with a silver finish."),
 "73": (DR, "Piston Stroke Divot Tool", "$105", DRU+"dt-03-piston-stroke",
   "A divot tool shaped like the piston and connecting rod of a V12 engine, in 303 stainless steel. The most car-obsessed thing here, and that is saying something."),
 "52": (DR, "Snail Driver Headcover", "$65", DRU+"drvn-snail-head-cover-driver",
   "A black barrel driver cover with the turbo-snail, DRVN&rsquo;s emblem, on the face. Nothing else on it."),
 "67": (DR, "Performance Hat", "$45", DRU+"drvn-water-resistant-performance-hat",
   "A water-resistant hat with laser-perforated side panels, the DRVN script on the front and the turbo-snail on the side. In cream with a green brim and rope, or black."),
}
SECTIONS = [
 ("Dim Sum Golf Club", "dim-sum", ["13","14","17","19","30","32","35","40"],
  "<strong>Hong Kong &middot; eight picks &middot; HK$55&ndash;HK$1,175</strong>A golf community first and a brand second, started in 2023. The merch is Hong Kong food and street signs redrawn as golf jokes. Prices in Hong Kong dollars."),
 ("Rowena Golf Club", "rowena", ["44","45","46","47","48","49"],
  "<strong>All six pieces &middot; $38&ndash;$108</strong>Linen trousers, boxy cotton polos and canvas hats in navy, green and cream. The whole store is six products, so all six are here, two of them sold out."),
 ("DRVN Golf Co.", "drvn", ["56","59","60","68","64","73","52","67"],
  "<strong>Milled putters &middot; eight picks &middot; $45&ndash;$1,250</strong>Putters and small metal accessories designed around classic sports cars, with an interchangeable face insert system in every putter."),
]
N = 22
PQ = {
 "dim-sum": ("Flipping the script on traditional, stuffy golf culture.", "Dim Sum Golf Club, on its About page"),
 "rowena": ("Feel good for 18, look good for the 19th.", "Rowena Golf Club"),
 "drvn": ("True luxury is rarely loud.", "DRVN Golf Co."),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "dim-sum": ("From Dim Sum", "Out on the course, on the terrace and the ProTour polo.", [("band-1","A golfer walking down a wide fairway toward the sea","The course"),("band-2","Two Dim Sum Golf Club members in navy polos on a terrace above a golf course and lake, with hills behind","On the terrace"),("band-3","Dim Sum Golf Club's sage green ProTour polo","The polo")]),
 "rowena": ("From Rowena", "Golden hour, the R hat and the linen.", [("band-4","A navy Rowena R hat hanging on a rail at sunset over long grass","The hat"),("band-5","A young golfer in a navy R hat carrying a bag through long grass at dusk","The walk"),("band-6","Close-up of navy pinstripe Rowena linen trousers on a grassy hillside","The linen")]),
 "drvn": ("From DRVN", "Putters, sports cars and a marker on the green.", [("band-7","A golfer with a green DRVN bag standing beside a green Porsche","The car"),("band-8","A DRVN golf bag with snail headcovers leaning on the wheel of a green sports car","The bag"),("band-9","The MM-722 wheel-shaped ball marker sitting on a putting green","The marker")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Put these three brands side by side and they barely look like they belong to the same sport. One is a Hong Kong golf club that sells T-shirts about breakfast. One makes six pieces of quiet, old-fashioned clothing. One mills $1,250 putters and names them after supercars. That is exactly why we put them together.</p>
    <p><strong>Dim Sum Golf Club</strong> started in Hong Kong in the winter of 2023. Its founder, Luke, a UK expat, ran into how limited and exclusive golf access is in the city, so he started a club for people who just wanted to play more. Joining is free; a paid membership gets you 15% off the merch and first access to golf days, monthly simulator nights and trips around Asia. The clothes come second to the club, and you can tell: they are inside jokes about cha chaan tengs, minibuses, taxis and Temple Street, made for people who know the city.</p>
    <p><strong>Rowena Golf Club</strong> goes the other way. Its whole store is six products: linen shorts and trousers, a boxy cotton polo, two hats and a leather headcover, in navy, green and cream. The look is golf&rsquo;s earlier eras with a modern, relaxed fit, and the mission is one line long.</p>
    <p><strong>DRVN Golf Co.</strong> is the equipment brand of the three. Its putters are precision milled, finished by hand and made in small batches, and each one takes interchangeable face inserts, so you can change the feel and sound without changing the putter. Every model, marker and divot tool starts with a car: a Porsche 964, a Le Mans long tail, an AMG One, a V12.</p>
    <h2 class="products-hdr" style="margin-top:32px">Who Each Brand Is For</h2>
    <p><strong>Dim Sum is for the social golfer.</strong> If your best rounds are the ones with eight friends, a simulator booking and a group chat, or if you have ever lived in or visited Hong Kong, start here. It is also the cheapest way in, from a HK$55 bag tag.</p>
    <p><strong>Rowena is for the golfer who wants to look good without trying hard.</strong> If you would rather own one pair of linen trousers you wear everywhere than ten logo polos, and you like a clubhouse that feels like the 1960s, this is your brand. Buy it quickly, as two of the six pieces were already sold out.</p>
    <p><strong>DRVN is for the golfer who cares about objects.</strong> If you read about a putter&rsquo;s milling pattern and head weight before you buy, or you know what a 964 is, this is for you. The $45 hat or an $85 ball marker gets you the look without the $1,250 commitment.</p>
    <h2 class="products-hdr" style="margin-top:32px">Why This Is the Fun Part of Golf Right Now</h2>
    <p>None of these brands could exist the same way inside a big golf company. A community club in Hong Kong can make a headcover about milk tea because its members will get the joke. A brand with six products can make every one of them carefully. A small putter maker can build 50 numbered blades and stop. Small brands get to be specific, and that is what makes them interesting: they are made by people with a point of view, for people who share it. Golf used to come in one style. Now you can pick the one that sounds like you.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Dim Sum</span><span>Hong Kong, since 2023</span></div>
      <div class="sidebar-detail"><span class="l">Rowena</span><span>Six pieces, all here</span></div>
      <div class="sidebar-detail"><span class="l">DRVN</span><span>Milled putters</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>22 in all</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>~$7&ndash;$1,250</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Breakfast Ball Headcover, Sunset Polo, Touring Six Four</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#DimSumGolfClub</span>
        <span class="hashtag">#RowenaGolf</span>
        <span class="hashtag">#DRVNGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is Dim Sum Golf Club?", "A golf community and clothing brand from Hong Kong, started in the winter of 2023 by a UK expat named Luke. It runs golf days, monthly simulator nights and trips around Asia, and joining is free. Its merch uses Hong Kong food and street culture, priced from HK$55 to HK$1,175 on October 19, 2026."),
 ("What does Rowena Golf Club make?", "Golf clothing with a classic, relaxed look: linen shorts and trousers, a boxy cotton polo with a tartan collar, two hats and a leather headcover. On October 19, 2026 its store had six products from $38 to $108, two of them sold out."),
 ("What is DRVN Golf Co.?", "A putter and accessories brand whose designs are based on classic sports cars. Its putters are precision milled, made in small batches and take interchangeable face inserts. On October 19, 2026 putters cost $500 to $1,250 and the Heritage models were limited to 50 numbered pieces."),
 ("Is DRVN Golf Co. the same as DRVN Golf?", "No. DRVN Golf Co. (drvngolfco.com) makes putters and accessories. DRVN Golf is a separate golf coaching certification with no connection to it."),
 ("Which of the three brands should I buy from?", "Dim Sum Golf Club suits social golfers and anyone with a link to Hong Kong, Rowena suits golfers who want a few quiet, classic pieces, and DRVN suits golfers who care about equipment design and cars."),
]
FRN = json.loads((ROOT / "research/radar-three-2/frames.json").read_text())
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
    <span>Three small golf brands &middot; three very different styles</span><span class="dot"></span>
    <span>22 picks &middot; prices checked October 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a white Dim Sum Golf Club tee with a dim sum basket graphic, a navy Rowena R hat hanging on a rail at sunset, and a golfer with a green DRVN bag beside a green Porsche" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Three Putt", "Tarraing", "Rebolf", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
