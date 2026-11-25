#!/usr/bin/env python3
"""build-golf-fishing.py — Golf & Fishing: Where the Overlap Lives, 24 November 2026 (Drops & Brands).
Lenny: "a post about Golf & Fishing and where the overlap exists" -> fresher brands, no country clubs,
munis only and cheap, more fishing headcovers. Picks from research/golf-fishing/items3.json (options v3).
FACTS: brand product pages (prices checked Nov 2026), TPWD stocking schedules, city course rate pages. No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"  # standard product-card template + gallery script
SLUG = "golf-and-fishing-where-they-overlap"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/golf-fishing"
TITLE = "Golf and Fishing: The Brands, Headcovers and Austin Munis Where They Overlap"
DESC = ("Golf and fishing share early mornings and the same patience. 32 pieces from fresh brands that do both, fish headcovers "
        "from Fins & Pins and Sunfish, and seven cheap Central Texas munis with fishing next door.")
H1 = "Play Nine, Fish Nine"
DEK = "Golf and fishing keep the same hours. Here are the brands that cover both, the fish headcovers, and seven cheap munis with water nearby."

ITEMS = json.loads((ROOT / "research/golf-fishing/items3.json").read_text(encoding="utf-8"))

GROUPS = [
 ("wear", "Wear It to Both", "Clothes That Work on Both",
  "Sun hoodies, fishing shirts and rope hats from brands that started on one side and kept wandering to the other. All of it is light, quick-drying and fine to wear on the first tee.",
  [0, 1, 2, 3, 6, 20, 8, 9, 10, 11, 13, 15, 16, 18, 19]),
 ("golf-brands", "Golf Brands, Gone Fishing", "Golf Labels With a Tackle Box",
  "Golf brands that made a fishing piece, and one fly shop that made a golf hat.",
  [21, 22, 24, 25, 26]),
 ("headcovers", "Headcovers", "Fish on the Driver",
  "Only a handful of makers do real fishing headcovers. Fins &amp; Pins prints actual fish skin patterns on leather; Sunfish hand-embroiders them; Daphne&rsquo;s makes the whole bass.",
  [27, 28, 29, 30, 32, 34, 35, 38, 39, 5]),
 ("cart", "For the Cart", "Two More Things",
  "Both go from the boat to the cart without a second thought.",
  [40, 41]),
]

# key, name, town, img, alt, headline, fee, fish, good, (label,url), tgi-link
PLACES = [
 ("hancock", "Hancock", "Austin", "pl42.jpg", "A striped fairway between live oaks at Hancock Golf Course in Austin",
  "Austin&rsquo;s oldest course is nine holes for $20, and Lady Bird Lake is a short drive south.",
  "$20 for nine holes, any day. Walking only.",
  "Largemouth bass in Lady Bird Lake, which Texas Parks and Wildlife rates as excellent. Free bank access at Festival Beach and Auditorium Shores.",
  "Year-round. Go early on a weekday for both.",
  ("Hancock rates", "https://www.austintexas.gov/golfatx/hancock-course"), "/drops/hancock-golf-course-austin"),
 ("lions", "Lions Municipal", "Austin", "pl43.jpg", "A pond guarding a green at Lions Municipal Golf Course with a cart path behind",
  "Muny, then the upper end of Lady Bird Lake.",
  "$35 on a weekday.",
  "Red Bud Isle, just below Tom Miller Dam, a few minutes from the course.",
  "Year-round.",
  ("Lions rates", "https://www.austintexas.gov/golfatx/lions-municipal-course"), "/drops/lions-municipal-golf-course-austin"),
 ("kizer", "Roy Kizer &amp; Jimmy Clay", "Austin", "pl44.jpg", "A green and bunker with a pond behind at Roy Kizer Golf Course",
  "Thirty-six city holes in southeast Austin, with winter trout down the road.",
  "$35 on a weekday.",
  "Texas Parks and Wildlife is scheduled to stock 2,600 rainbow trout in Onion Creek on January 10 and January 24, 2027. The ponds at Southeast Metro Park are TPWD community fishing lakes.",
  "January and February, while the trout last.",
  ("Roy Kizer rates", "https://www.austintexas.gov/golfatx/roy-kizer-course"), None),
 ("fredericksburg", "Lady Bird Johnson", "Fredericksburg", "pl46.jpg", "Live Oak Creek running through Lady Bird Johnson Park in Fredericksburg",
  "The city course and a stocked trout creek share the same park.",
  "$47 to walk on a weekday, Monday to Thursday, plus tax.",
  "Live Oak Creek runs through the park and past hole 6, which plays over it. TPWD is scheduled to stock 500 trout around January 10, 2027.",
  "Kid Fish Day is January 9, 2027, the day before the stocking.",
  ("Kid Fish Day", "https://fbgtx.org/972/Kid-Fish-Day"), None),
 ("landa", "Landa Park", "New Braunfels", "pl47.jpg", "Aerial view of Landa Park Golf Course in New Braunfels with ponds and a cart path",
  "A city course that runs along the Comal.",
  "$50 on a weekday with a cart (2024 rate card; check before you go).",
  "Landa Lake, inside the same park, is a TPWD community fishing lake.",
  "Year-round. The Comal stays cool even in August.",
  ("Landa Park rates", "https://www.landaparkgolfcourse.com/golf/rates/"), None),
 ("llano", "Llano River Golf Course", "Llano", "pl48.jpg", "The Llano River running clear over granite near Castell",
  "A small-town course on the Llano, with clear river fishing a short drive away.",
  "Rates aren&rsquo;t published online; call the pro shop.",
  "TPWD is scheduled to stock 1,909 trout at Castell Crossing on December 10, 2026, and the Llano holds Guadalupe and largemouth bass year-round. Llano City Lake is in town.",
  "December for trout; spring and fall for bass.",
  ("Castell trout info", "https://tpwd.texas.gov/fishboat/fish/recreational/rivers/lease_access/llano_castell.phtml"), None),
 ("burnet", "Delaware Springs", "Burnet", "pl50.jpg", "The clubhouse at Delaware Springs Golf Course in Burnet under Texas and US flags",
  "The priciest round on this list, cart included, an hour northwest of Austin.",
  "$60 on a weekday with a cart.",
  "Hamilton Creek Park in Burnet, with 1,000 trout scheduled for January 10, 2027.",
  "January.",
  ("Delaware Springs rates", "https://delawaresprings.com/rates/"), None),
]

CSS = ('<style>/*TGI-GOLFFISH v2 — standard product-card template*/'
       '.products-grid[data-n]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
       '.products-grid[data-n="5"],.products-grid[data-n="2"]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
       '.products-grid[data-n="5"]>.product-card,.products-grid[data-n="2"]>.product-card{flex:0 0 calc((100% - 54px)/4);min-width:0}'
       '.product-card.out .product-name{color:#8a3b2b}'
'.em{padding-top:0!important;padding-bottom:0!important}.em-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;padding:52px 0;border-top:.5px solid rgba(20,20,20,.25)}'
       '.em-row.flip .em-imgs{order:2}.em-imgs img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#E8E2D6}'
       '.em-who{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:10px}'
       'section.products.em .em-txt h2{font-family:var(--serif);font-weight:400;font-size:clamp(32px,3.8vw,46px);line-height:1;letter-spacing:-.01em;margin:0 0 14px!important;text-align:left!important}'
       '.em-txt p{font-size:17px;line-height:1.62;margin:0 0 14px}.em-txt a{border-bottom:1px solid currentColor}'
       '.em-q{font-family:var(--serif);font-size:22px;line-height:1.35;color:#2D4A2B;margin:6px 0 18px;padding:2px 0 2px 18px;border-left:2px solid #2D4A2B}'
       '.em-pq{font-size:clamp(24px,2.6vw,30px)!important;margin:22px 0!important;padding:4px 0 4px 22px!important}'
       '.rs-dl{margin:4px 0 14px;border-top:.5px solid rgba(20,20,20,.2)}.rs-dl div{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:11px 0;border-bottom:.5px solid rgba(20,20,20,.2)}'
       '.rs-dl dt{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2D4A2B;padding-top:4px}.rs-dl dd{margin:0;font-size:15.5px;line-height:1.55}'
       '.em-links{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;display:flex;gap:18px;flex-wrap:wrap}'
       '@media(max-width:1024px){.products-grid[data-n]{grid-template-columns:repeat(2,minmax(0,1fr))}.products-grid[data-n="5"]>.product-card,.products-grid[data-n="2"]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
       '@media(max-width:820px){.em-row{grid-template-columns:1fr;gap:20px;padding:40px 0}.em-row.flip .em-imgs{order:0}.rs-dl div{grid-template-columns:1fr;gap:4px}}'
       '</style>\n')


FRAMES = json.loads((ROOT / "research/golf-fishing/gal/frames.json").read_text(encoding="utf-8"))


def card(i):
    g, brand, name, price, why, url, *_ = ITEMS[i]
    out = "sold out" in price
    label = H.escape(H.unescape(f"{brand} {name}").replace('"', ""), quote=True)
    price = price.replace("sold out", "Sold out")
    fr = FRAMES.get(str(i), [f"p{i:02d}.jpg"])
    imgs = "".join(f'<div class="pg-frame"><img src="{IMG}/{f}" alt="{label}{f" &middot; view {j+1} of {len(fr)}" if len(fr) > 1 else ""}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    nav = ""
    if len(fr) > 1:
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        nav = (f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
               f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>')
    return (f'<div class="product-card{" out" if out else ""}" id="p-{i}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>{nav}</div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{why}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">{"See it" if out else "Shop"} &#8599;</a></div></div>')


BANDS = {
 "a": ("On the Water, On the Course", [
   ("band-a1.jpg", "A golfer by a river next to a Fins &amp; Pins stand bag", "Play 9, Fish 9 &middot; Fins &amp; Pins"),
   ("band-a2.jpg", "An angler in a sun hoodie and face buff casting a fly rod from a boat", "Bamboo Lightweight Hoodie &middot; Free Fly"),
   ("band-a3.jpg", "A white bass sock worn next to a landing net on grass", "Largemouth Bass Sock &middot; del campo")]),
 "b": ("Off the Clock", [
   ("band-b1.jpg", "A man in a blue hooded sun shirt kneeling on a dock", "Loggerhead Hoodie &middot; Howler Brothers"),
   ("band-b2.jpg", "A man on a beach with a golf bag", "On the beach &middot; Gumtree Golf &amp; Nature Club"),
   ("band-b3.jpg", "A tumbler stuck to a boat rail over the water", "SmartGrip Tumbler &middot; Toadfish")]),
 "c": ("Play 9, Fish 9", [
   ("band-c1.jpg", "A golfer carrying a Fins &amp; Pins bag down a fairway", "Carry bag &middot; Fins &amp; Pins"),
   ("band-c2.jpg", "Brown trout putter covers lying on a green", "Fall Brown Trout blades &middot; Fins &amp; Pins"),
   ("band-c3.jpg", "A golfer standing at the pin with a Fins &amp; Pins bag", "On the green &middot; Fins &amp; Pins")]),
 "d": ("Where the Water Is", [
   ("band-d1.jpg", "Aerial view of a winding river through marsh grass", "Home water &middot; Fins &amp; Pins"),
   ("band-d2.jpg", "An angler in a hooded sun shirt and face buff on a boat under a blue sky", "On the boat &middot; Free Fly"),
   ("band-d3.jpg", "A golf ball on the lip of the cup", "The other kind of hole &middot; Fins &amp; Pins")]),
}


def band(k):
    tag, figs = BANDS[k]
    f = "".join(f'<figure><img src="{IMG}/{src}" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for src, alt, cap in figs)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{tag}</div>\n'
            f'  <div class="ig-grid" style="margin-top:18px">{f}</div>\n</section>\n')


def pq(text, who):
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def group(k, tag, cap, intro, idx):
    cards = "\n".join(card(i) for i in idx)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(idx)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{k}">{cap}</h2>\n'
            f'  <p class="cat-kicker"><strong>{tag}</strong>{intro}</p>\n'
            f'    <div class="products-grid" data-n="{len(idx)}">\n{cards}\n    </div>\n</section>\n')


def place(i, p):
    k, name, town, img, alt, head, fee, fish, good, link, tgi = p
    links = f'<a href="{link[1]}" target="_blank" rel="noopener">{link[0]} &#8599;</a>'
    if tgi:
        links = f'<a href="{tgi}">Our {H.unescape(name)} guide</a>' + links
    flip = " flip" if i % 2 == 0 else ""
    return (f'\n<section class="products em" id="{k}">\n  <div class="em-row{flip}"><div class="em-imgs"><img src="{IMG}/{img}" alt="{alt}" loading="lazy" /></div>'
            f'<div class="em-txt"><div class="em-who">{town}</div><h2>{name}</h2><p>{head}</p>'
            f'<dl class="rs-dl"><div><dt>The round</dt><dd>{fee}</dd></div><div><dt>The fish</dt><dd>{fish}</dd></div><div><dt>When</dt><dd>{good}</dd></div></dl>'
            f'<div class="em-links">{links}</div></div></div>\n</section>\n')


RELATED = [
 ("/drops/climbing-golf-crossover-gear", "Climbing x Golf", "The other crossover: gear from the crag that works on the course."),
 ("/drops/outdoor-brands-for-golf", "Outdoor Brands for Golf", "Patagonia-school labels that play well on the course."),
 ("/drops/brand-to-know-gumtree-golf-and-nature-club", "Gumtree Golf &amp; Nature Club", "The Brooklyn brand that made a whole collection about fishing."),
 ("/drops/hancock-golf-course-austin", "Hancock Golf Course", "Our guide to Austin&rsquo;s $20 nine."),
]


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    allp = [i for g in GROUPS for i in g[4]]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-24", "dateModified": "2026-11-24",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": [
            {"@type": "ListItem", "position": n, "name": H.unescape(f"{ITEMS[i][1]} {ITEMS[i][2]}"), "url": ITEMS[i][5]} for n, i in enumerate(allp, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Golf and Fishing", "item": URL}]},
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
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    head_rest = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\s*', "", head_rest, flags=re.S)
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    _side = "\n".join(f'      <div class="sidebar-detail"><span class="l">{len(g[4])}</span><span><a href="#{g[0]}" style="border-bottom:none">{g[2]}</a></span></div>' for g in GROUPS)

    rel = "".join(f'<li style="padding:10px 0;border-bottom:.5px solid rgba(20,20,20,.2)"><a href="{u}">{t}</a> &mdash; {d_}</li>' for u, t, d_ in RELATED)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Golf and Fishing</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 24, 2026</p><!--/TGI-BY-->
  <div class="drop-meta">
    <span>Metalwood, Gumtree, Malbon, Duck Camp, Fins &amp; Pins, Sunfish and more</span><span class="dot"></span>
    <span>32 picks &middot; 7 munis &middot; prices checked November 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Aerial view of Landa Park Golf Course in New Braunfels, with ponds between the fairways" fetchpriority="high" /></div></div>

<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p><strong>Same hours, same people.</strong> Golfers and anglers both get up before the sun, spend hours mostly quiet, and drive home talking about the one that got away. Reading a green and reading a current are the same squint. Plenty of us do both, and the good days are the ones where you get to do both before lunch.</p>
    <p><strong>The fresh brands noticed first.</strong> Metalwood&rsquo;s fishing shirt promises &ldquo;a stroke off your score for every fish caught in-round.&rdquo; Gumtree gave its 2024 collection over to fishing. Malbon now runs a Golf and Tackle line, Swag made a Gone Fishing pattern, and Fins &amp; Pins built a whole headcover company on four words: Play 9, Fish 9.</p>
    <p><strong>None of it needs a membership.</strong> Both sports have a velvet-rope version, and that isn&rsquo;t us. Every course below is a city or public course, most under $50 on a weekday, and the fishing next to them is free from the bank. You&rsquo;ll need a Texas fishing license, and that&rsquo;s about it.</p>
    <h2 class="products-hdr btk-story-hdr">Play Nine, Fish Nine</h2>
    <p><strong>Winter is the window.</strong> Texas Parks and Wildlife stocks rainbow trout in creeks and park ponds from December through February, several of them a short drive from a muni. Play the morning nine, keep the waders in the trunk, and fish the afternoon.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>32 from 18 brands</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$16&ndash;$289</span></div>
      <div class="sidebar-detail"><span class="l">Headcovers</span><span>10, from 3 makers</span></div>
      <div class="sidebar-detail"><span class="l">Munis</span><span>7, from $20 for nine</span></div>
      <div class="sidebar-detail"><span class="l">Trout season</span><span>December&ndash;February</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>November 2026</span></div>
      <a href="#wear" class="sidebar-cta">See the picks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfAndFishing</span>
        <span class="hashtag">#FishingHeadcover</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<div class="pull-quote" style="margin:56px auto 24px">
  <div class="pull-quote-inner">&ldquo;In Fredericksburg, the city course and a stocked trout creek share the same park. Hole 6 plays right over the water.&rdquo;<span class="pull-quote-attr">&mdash; The Grassy Issue</span></div>
</div>
"""
    W, B, HC, C = GROUPS
    body += band("a") + group(*W)
    body += pq("If the silverking breaks your line, you can at least keep this silverking.", "Duck Camp, on its tarpon rope hat")
    body += band("b") + group(*B)
    body += pq("Dressed like they own a tackle shop and a dive bar simultaneously.", "Swag Golf, on the Gone Fishing pattern")
    body += band("c") + group(*HC) + group(*C)
    body += band("d")
    body += ('\n<section class="products" style="margin-top:8px;padding-bottom:0">\n'
             '  <div class="drop-tag grass">7 munis</div>\n'
             '  <h2 class="products-hdr" id="places">Munis With Water Nearby</h2>\n'
             '  <p class="cat-kicker"><strong>Places to Do Both</strong>Seven city and public courses in Austin and the Hill Country, cheapest first-ish, each with fishing close enough to do the same day. Fees are the courses&rsquo; own published weekday rates; stocking dates are from Texas Parks and Wildlife&rsquo;s 2026&ndash;27 schedule.</p>\n'
             '</section>\n')
    for i, p in enumerate(PLACES, 1):
        body += place(i, p)
    body += f"""
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Bring Both</h2>
    <p>Throw a rod in the trunk next to the clubs. The worst case is a round of golf, and the best case is a trout and a birdie on the same Tuesday. If you know a muni with good water nearby that we missed, <a href="/work-with-us">tell us</a>.</p>
    <div class="drop-tag grass" style="margin-top:34px">More Like This</div>
    <ul style="list-style:none;padding:0;margin:10px 0 0;font-size:17px">{rel}</ul>
  </div>
</section>
"""
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Mackem", "Manors", "country club"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html · {sum(len(g[4]) for g in GROUPS)} pieces · {len(PLACES)} places")


if __name__ == "__main__":
    main("--apply" in sys.argv)
