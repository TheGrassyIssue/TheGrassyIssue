#!/usr/bin/env python3
"""build-radar-three.py — On Our Radar: three small golf brands, three directions. Cloned from build-woodgrain-btk.py. 12 October 2026.
Lenny: "Let's do a post about three small new brands to keep on your radar" (Three Putt, Tarraing, Rebolf), "6 items from each",
then picked 1, 8, 9, 10, 11, 17, 24 / 25, 29, 31, 32, 36, 45, 46 / 66, 67, 70, 74, 80, 92, 95 from the options sheet (seven each).
FACTS: each store's products JSON (research/radar-three/), About pages read October 12, 2026. Prices in store currency first:
Three Putt GBP (x1.3234), Rebolf EUR (x1.1203, its own euro prices, not its higher US-market prices), Tarraing USD.
Three Putt galleries use flat and back-print shots only; several of its on-model photos look AI-generated.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Three Small Golf Brands to Keep on Your Radar"
DESC = ("Three Putt, Tarraing and Rebolf: three new, small-batch golf brands from England, the US and Spain, "
        "taking golf clothing in three directions. Seven picks from each, with prices.")
H1 = "On Our Radar: Three Small Golf Brands, Three Directions"
BC = "Three Brands on Our Radar"
SLUG = "three-small-golf-brands-on-our-radar"
IMG = "/images/radar-three"
SHOP = ""
TP, TG, RB = "Three Putt Golf Clothing", "Tarraing Golf", "Rebolf"
TPU, TGU, RBU = "https://threeputtgolfclothing.co.uk/products/", "https://tarrainggolf.com/products/", "https://rebolf.com/products/"
P = {
 # Three Putt
 "1": (TP, "Three on the Green Sweatshirt", "&pound;37.99 (~$50)", TPU+"three-on-the-green-golf-sweatshirt",
   "The quiet one. A 400gsm, 100% cotton crewneck with nothing on it but the small TPG flag on the left chest. It comes in cream, off-white, black, gray marl and navy, and it is the cheapest of the brand&rsquo;s heavyweight layers."),
 "8": (TP, "Contours Hoodie", "&pound;54.99 (~$73)", TPU+"contours-golf-hoodie",
   "The back print is a topographic map of a single green, every ring and run-off drawn in one continuous line, with the brand saying a three-putt is hidden in it. A 430gsm, oversized cotton-blend hood in forest green, sand, navy or oatmeal. It is the heaviest piece in the range."),
 "9": (TP, "Contours Sweatshirt", "&pound;47.99 (~$64)", TPU+"contours-golf-sweatshirt",
   "The same green contour map on a 400gsm cotton crewneck. Three Putt points out that a crew sidesteps the no-hood rule at stricter clubs, which is the kind of detail you only think about if you play at one."),
 "10": (TP, "Happy Place Long-Sleeve Tee", "&pound;34.99 (~$46)", TPU+"happy-place-golf-long-sleeve-tee",
   "A hand-drawn golf bag, a few irons and a basket of range balls across the back, with Happy Place in script. A loose 280gsm long sleeve in black, white, gray, bean or brown. The brand calls it the layer for cold-handed range sessions."),
 "11": (TP, "Tee Time T-Shirt", "&pound;29.99 (~$40)", TPU+"tee-time-golf-t-shirt",
   "Our favorite design in the range. A dairy cow sits on a chair with a cup of tea, clubs leaning beside it, under a Tee Time sign. The cow is a nod to the founder&rsquo;s grandad&rsquo;s farm field, where he learned the game. An oversized 260gsm cotton tee, with a small teacup on the chest."),
 "17": (TP, "The Scenic Route Hoodie", "&pound;54.99 (~$73)", TPU+"the-scenic-route-golf-hoodie",
   "A whole course drawn across the back: a golfer mid-swing, the clubhouse on the hill, pines, a cart and birds overhead. Up front, the cow carries a golf bag. The forest green version is the one we would buy."),
 "24": (TP, "Reckless Driving T-Shirt", "&pound;29.99 (~$40)", TPU+"reckless-driving-golf-t-shirt",
   "The cow again, this time flat out behind the wheel of a golf cart with clubs flying out the back. A small chest print on a 260gsm cotton tee, in five colors. Daft, and that is the point."),
 # Tarraing
 "25": (TG, "The Ry Quarter-Zip", "$130", TGU+"the-gordo-copy",
   "The newest piece from Tarraing. A nylon and spandex quarter-zip with real stretch and the highland cow logo on the left sleeve, light enough to layer all year. Only M and L were in stock when we checked."),
 "29": (TG, "The Russell Polo", "$85", TGU+"white-red-navy-polo",
   "White with thin red and navy stripes, a small cow logo on the chest, and the brand&rsquo;s standard lightweight polyester-spandex fabric. Every Tarraing polo is named after a person, and this is the most traditional of them."),
 "31": (TG, "The Flan Polo", "$85", TGU+"lime-seablue-polo",
   "Lime and sea blue, a soft stripe that reads teal from a few feet away. Same moisture-wicking, wrinkle-resistant fabric and athletic fit as the rest of the polos. All four sizes in stock."),
 "32": (TG, "Gray, White and Blue Highland Cow Hat", "$40", TGU+"red-white-blue-highland-cow-copy",
   "A gray, unstructured summer hat with the blue highland cow on the front, a wicking sweatband and UPF 35+. Tarraing listed it as low inventory."),
 "36": (TG, "The VA Quarter-Zip", "$125", TGU+"periwinkle-quarter-zip-pullover",
   "A periwinkle quarter-zip in a Tencel modal and spandex blend with four-way stretch, made in Boston. Tarraing calls it the most comfortable thing you will own. L and XL left."),
 "45": (TG, "The Jiffa Polo", "$85", TGU+"navy-white-specs-polo",
   "Navy with a fine white speckle, the polo here that will hide a long day best. The specks give it texture without a loud pattern."),
 "46": (TG, "White Highland Cow Rope Hat", "$40", TGU+"white-tarraing-highland-cow-hat",
   "A white six-panel rope hat with Douglas, Tarraing&rsquo;s highland cow, embroidered in navy, and the rope across the brim. Snapback, one size, and listed as low inventory."),
 # Rebolf
 "66": (RB, "Harbour Polo", "&euro;70 (~$78)", RBU+"harbour-polo",
   "A white polo with navy sleeves and a navy collar, the summer piece of the latest collection. Rebolf describes it simply: blue for the ocean, white for the light."),
 "67": (RB, "Riviera Beige Pleated Shorts", "&euro;80 (~$90)", RBU+"riviera-beige-shorts",
   "Double pleated shorts in a cotton blend with a relaxed summer fit, a nod to golf heritage from a brand that otherwise leans to the street. Beige is the color that goes with everything else on this page."),
 "70": (RB, "Joga Navy Polo", "&euro;75 (~$84)", RBU+"joga-navy-polo",
   "A football-inspired polo: navy with white raglan panels, a short zip at the neck and a relaxed fit. It looks like a 1990s club training top, which is the idea."),
 "74": (RB, "Crosswind Windbreaker", "&euro;110 (~$123)", RBU+"crosswind-windbreaker",
   "Stretch nylon color-blocked in navy, orange and cream, with a collared zip, side pockets and a relaxed fit. Lightweight, wind-resistant and the loudest piece in the post. Rebolf styled it with matching orange shorts."),
 "80": (RB, "Iconic Black Pleated Pants", "&euro;110 (~$123)", RBU+"iconic-black-pleated-pants",
   "Black pleated trousers with yellow accents and a straight, functional cut. Rebolf calls the attitude &ldquo;strong course,&rdquo; and they work just as well off it."),
 "92": (RB, "Pleated Navy Pants", "&euro;70 (~$78)", RBU+"pleated-flex-navy-pants",
   "Classic pleated trousers in a stretch fabric, navy with a contrast stripe down the side seam. Only XL was in stock when we checked."),
 "95": (RB, "Sportive Citric Polo", "&euro;70 (~$78)", RBU+"sportive-citric-polo",
   "A bright yellow polo with a white collar that Rebolf calls its most technical, &ldquo;with a touch of vintage essence.&rdquo; L and XL left."),
}
SECTIONS = [
 ("Three Putt Golf Clothing", "three-putt", ["1","8","9","10","11","17","24"],
  "<strong>West Yorkshire &middot; seven picks &middot; &pound;29.99&ndash;&pound;54.99</strong>Golf streetwear in heavy cotton, with hand-drawn back prints and a dairy cow that turns up everywhere. Prices in pounds; free UK delivery."),
 ("Tarraing Golf", "tarraing", ["25","29","31","32","36","45","46"],
  "<strong>United States &middot; seven picks &middot; $40&ndash;$130</strong>Classic polos and quarter-zips inspired by the golf of Ireland and Scotland, each named after a person, plus highland cow hats."),
 ("Rebolf", "rebolf", ["66","67","70","74","80","92","95"],
  "<strong>Barcelona &middot; seven picks &middot; &euro;70&ndash;&euro;110</strong>A golf professional&rsquo;s take on streetwear, made in a local studio: football polos, pleats and color blocking. Prices in euros."),
]
N = 21
PQ = {
 "three-putt": ("No ego. No pretense. No elitism.", "Three Putt Golf Clothing, on where it started"),
 "tarraing": ("Our experiences traveling and playing on these renowned courses serve as the foundation of our identity.", "Tarraing Golf, on Ireland and Scotland"),
 "rebolf": ("We bridge the gap between the fairway and the street.", "Rebolf"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "three-putt": ("From Three Putt", "Rounds from the brand&rsquo;s own About page, and the Tee Time cow up close.", [("band-1","Two golfers waiting on a tee box on a green, rolling course","The tee"),("band-2","A smiling golfer in a beanie carrying his bag across a fairway at sunset","The walk"),("band-3","The Tee Time print on the back of a cream Three Putt tee: a cow on a chair with a cup of tea beside a golf bag","The cow")]),
 "tarraing": ("From Tarraing", "On the course, the coast that inspired it, and the polo up close.", [("band-4","A golfer seen from behind in a navy vest with the blue highland cow on the back, a mesh cap and a striped polo, looking out over a course","On the course"),("band-5","The Tarraing highland cow badge over a coastal links hole above a beach","The coast"),("band-6","A folded white and blue striped Tarraing polo with the highland cow logo","The polo")]),
 "rebolf": ("From Rebolf", "Campaign photos: polos, a buggy in a bunker, caps and a snowy mountain set.", [("band-7","A model in a green Rebolf polo holding a club over his shoulder in front of a snowy mountain backdrop","The green polo"),("band-8","A golfer in a navy Rebolf polo and shorts holding a club on a studio set","The studio"),("band-9","A Rebolf golf buggy tipped over on its side in a sand bunker","The bunker"),("band-10","A model in a yellow Rebolf polo adjusting a green Caddie&rsquo;s Grace cap","The polo"),("band-11","A model in a blue and yellow Rebolf cap and orange sunglasses","The shades"),("band-12","A model in a black and white Rebolf sweater in front of a snowy mountain backdrop","The mountain")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>There is no single way a new golf brand has to look. Here are three small ones, all a few years old or younger, each making a small amount of clothing and each pulling golf style in a different direction. Three Putt makes heavyweight streetwear with hand-drawn back prints. Tarraing makes clean, traditional polos with a Celtic streak. Rebolf mixes football training tops, pleats and loud color blocking. Seven pieces from each, all in stock when we checked.</p>
    <p><strong>Three Putt</strong> launched in 2025 in West Yorkshire. Founder Graeme Whiles learned the game in his grandad&rsquo;s field with charity-shop clubs, which is why a dairy cow turns up on half the range. Everything is heavy cotton, from 260gsm tees to a 430gsm hoodie, and built for the pub after the round as much as the round.</p>
    <p><strong>Tarraing</strong> takes its cue from the courses of Ireland and Scotland. The polos are named after people, the highland cow on the hats is called Douglas, and the VA quarter-zip is made in Boston.</p>
    <p><strong>Rebolf</strong> is from Barcelona, founded by a golf professional who, in the brand&rsquo;s words, &ldquo;felt he needed a change.&rdquo; Its clothes are made at a local studio, in small runs, and look more like a football kit than a pro shop.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Three Putt</span><span>West Yorkshire, UK</span></div>
      <div class="sidebar-detail"><span class="l">Tarraing</span><span>United States</span></div>
      <div class="sidebar-detail"><span class="l">Rebolf</span><span>Barcelona, Spain</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>Seven from each, 21 in all</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>~$40&ndash;$130</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Three Putt Tee Time Tee, &pound;29.99</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#ThreePuttGolf</span>
        <span class="hashtag">#Tarraing</span>
        <span class="hashtag">#Rebolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Three Putt Golf Clothing from?", "West Yorkshire, England. It launched in 2025 and was founded by Graeme Whiles. Prices are in pounds, from £29.99 for a tee to £54.99 for a hoodie on October 12, 2026."),
 ("Where is Tarraing Golf from?", "Tarraing draws on the golf of Ireland and Scotland, and its VA quarter-zip is made in Boston, Massachusetts. Polos were $85 and quarter-zips $125 to $130 on October 12, 2026."),
 ("Where is Rebolf from?", "Barcelona, Spain. Rebolf was founded by a golf professional and makes its collections at a local Barcelona studio. Prices are in euros; on October 12, 2026 polos were €70 to €75 and pleated trousers €70 to €110."),
 ("What makes these three brands different?", "Three Putt makes heavyweight cotton streetwear with hand-drawn prints, Tarraing makes traditional performance polos and quarter-zips, and Rebolf mixes football-style polos, pleats and color blocking."),
]
FRN = json.loads((ROOT / "research/radar-three/frames.json").read_text())
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
    <span>Three small golf brands &middot; England, the US and Spain</span><span class="dot"></span>
    <span>21 picks &middot; all in stock, checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three golf course photos side by side: the Happy Place range-basket print on the chest of a gray Three Putt sweatshirt, a golfer from behind in a navy Tarraing vest with the highland cow on the back, and a golfer in a white robe walking off a green by the flag" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Woodgrain", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
