#!/usr/bin/env python3
"""build-bag-upgrade-v2.py — "Upgrading Your Golf Bag", rebuilt on the same URL. 1 November 2026. Cloned from build-pgg-btk.py.
Lenny: "let's beef up this post, it's very thin, we need more makers and more pictures and details" / "it's also missing parts of the format" /
"for the Mackenzies, use IRL photos from Instagram or the collab images. Add more stitch golf and add Sunday golf, also find more IRL photos
for the bags and get rid of the stark white backgrounds."
Seven makers, 21 bags, rows of 3. Replaces build-bag-upgrade.py (Sept 22, 3 makers, FAQ). No FAQ.
FACTS: each brand's own storefront (Shopify products.json/.js, USD) read Nov 1, 2026. MacKenzie prices from its bag builder.
Instagram was not used (not reachable from here); MacKenzie cards show its ACL Golf and Jain Golf collab editions, band shows Fyfe x MacKenzie.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-paris-golf-gallery.html"

TITLE = "Upgrading Your Golf Bag: 21 Carry and Stand Bags From Seven Makers"
DESC = ("Seven bag makers a step above the pro shop rack: Shapland, Shoal, Jones, MacKenzie, Vessel, Stitch and Sunday Golf. "
        "21 carry and stand bags from $130 to $999, in US dollars, with what is in stock and what is preorder.")
H1 = "Upgrading Your Golf Bag"
BC = "Upgrading Your Golf Bag"
SLUG = "upgrading-your-golf-bag"
IMG = "/images/bag-upgrade"
SH = "https://shaplandbags.com/products/"
SO = "https://shoalgolfco.com/products/"
JO = "https://www.jonessportsco.com/products/"
MK = "https://www.mackenziegolfbags.com/shop/golf-bags/"
VE = "https://vesselgolf.com/products/"
ST = "https://stitchgolf.com/products/"
SG = "https://sundaygolf.com/products/"
P = {
 "rye": ("Shapland", "Rye 4.0", "$535 &middot; sold out", SH + "custom-rye-4-0",
   "The flagship, named for Rye Golf Club, the first course Harry Colt designed. A stand bag with oiled leather trim, hickory-wrapped legs and a quilted canvas body, in Navy, Black, Burgundy, Red, Heathered Blue and Rosemary. Every color is sold out as of November 1. Shapland says the next 4.0 run arrives in late November."),
 "kantle": ("Shapland", "Kantle 4.0", "$535 &middot; sold out", SH + "custom-kantle-4-0",
   "The Kantle carries two separate straps so it works as a single or a double carry, over a wider top than the Rye. Red, Burgundy, Honey, Navy, Black and Rosemary, all sold out for now."),
 "shsun": ("Shapland", "Sunday 4.0", "$475 &middot; sold out", SH + "custom-sunday-4-0",
   "The lightest way into Shapland and the cheapest, with the same leather trim and stand legs in a slimmer body. Navy, Black, Rosemary, Honey and Granite. Sold out, like the rest of the line."),
 "standard": ("Shoal Golf Co.", "The Shoal Standard Bag", "$450 &middot; preorder", SO + "preorder-for-december-15-ship-date-shoal-standard-black-golf-bag",
   "Shoal&rsquo;s one core bag: waxed canvas, leather trim and a four-way top on a light stand. The current preorder ships December 15 in Black, Salmon, Slate Grey, Charcoal and Sage. Tobacco is sold out."),
 "reserve": ("Shoal Golf Co.", "The Shoal Reserve Bag, Navy", "$450 &middot; preorder", SO + "the-shoal-reserve-bag-preorder-navy-december-15-ship-date",
   "The Reserve takes the Standard&rsquo;s shape into navy with brown leather, and it also ships December 15. Of the three Shoal bags here, it looks most at home at an old club."),
 "simple": ("Shoal Golf Co.", "The Simple Sunday Bag", "$250", SO + "the-shoal-simple-sunday-bag",
   "A 2.65-pound Sunday bag with one strap and no internal rod, in olive canvas with a leather base stamped with Shoal&rsquo;s dog. For a nine-hole evening or a quick range session."),
 "trouper": ("Jones Sports Co", "Trouper 4.0", "$340&ndash;$395", JO + "trouper-4-0-evergreen-kodiak",
   "The Jones stand bag, with a four-way top and the old narrow profile. The leather-trimmed versions (Ecru, Onyx/Kodiak, Evergreen/Kodiak) are $395. Black, Moon Gray/Seacrest, Cedar and Navy are $340, and Olive Gray is on sale at $245."),
 "rover": ("Jones Sports Co", "Rover Stand Bag", "$235&ndash;$295", JO + "rover-stand-bag-high-desert",
   "The Rover is Jones&rsquo;s lighter, more modern stand bag, with a shaped top and a double strap. High Desert and Cedar are $295, and the Ecola and F.C. Durham colorways are $235."),
 "original": ("Jones Sports Co", "Original Jones Bag, Navy/White", "$185", JO + "original-jones-bag-navy-white",
   "The 1971 bag, still unstructured: water-resistant nylon, one strap, three pockets and no legs. The cheapest bag in this post that is not a par 3 sling, and the one that has changed least."),
 "mkwax": ("MacKenzie", "Waxed Canvas Bag, made to order", "$685&ndash;$760", MK,
   "MacKenzie has hand-built carry bags in Pennsylvania since 1985, and every ready-made bag is sold out right now, so the way in is the builder: pick the canvas, the leather and the trim. Shown here: the MacKenzie x ACL Golf waxed canvas editions."),
 "mknylon": ("MacKenzie", "Nylon Bag, made to order", "$405&ndash;$455", MK,
   "The lightest and least expensive MacKenzie, in nylon with the same leather spine, strap and stitched details. Shown here: the navy MacKenzie x ACL Golf nylon carry bag."),
 "mktreated": ("MacKenzie", "Treated Canvas Bag, made to order", "$695&ndash;$785", MK,
   "Treated canvas sits between nylon and waxed canvas and takes color well. Shown here: the Jain Golf 1st Edition in Colonial Blue. Leather builds run $1,005 to $1,105."),
 "vsunday": ("Vessel", "Sunday IV Leather Stand", "$999", VE + "sunday-iv-leather-stand-crimson",
   "The most expensive bag here: a full leather Sunday stand bag in Crimson, Croc Black or Cognac. Vessel has made bags in Carlsbad, California since 2013, and this is the one that shows it."),
 "vlux": ("Vessel", "Lux Stand", "$399", VE + "lux-stand-crosshatch-navy",
   "A stand bag in a crosshatch-textured synthetic, with a matching cart strap sleeve included. Navy, Black, Grey, Green, White and DXR Black."),
 "vcarry": ("Vessel", "Sunday Carry", "$199", VE + "sunday-carry-olive",
   "A slim Sunday bag with a round top, a single strap and a shoe pouch-size pocket. Olive or Black."),
 "sl2": ("Stitch Golf", "SL2 Gen 2", "$398", ST + "sl2-gen-2",
   "Stitch has made golf bags and travel gear since 2012, and the SL2 is its signature stand bag: a clean coated body, a four-way top and piping down the side. Midnight, Fernwood, Glacier White, Morning Fog, Onyx, Orange and Stitch Blue."),
 "air": ("Stitch Golf", "SL2 Air Walker", "$298", ST + "sl2-air-walker-golf-bag",
   "The lighter walking version of the SL2, with a mesh back panel and a cooler pocket. Midnight, Morning Fog and Onyx."),
 "slsun": ("Stitch Golf", "SL Sunday Bag", "$198", ST + "stitch-sl-sunday-golf-bag",
   "A Sunday bag with a padded strap and a zip pocket that runs most of its length. Onyx is $198, and Midnight was on sale for $68 when we checked."),
 "ryder": ("Sunday Golf", "Ryder 14", "$270", SG + "ryder-14-midnight-green-full-size-stand-bag",
   "Sunday Golf&rsquo;s full-size stand bag, with a 14-way top and a cooler pocket. Matte Black, Midnight Green and Toasted Almond."),
 "elcamino": ("Sunday Golf", "El Camino", "$200", SG + "el-camino-seafoam-mid-size-stand-bag",
   "A mid-size stand bag for a half set or a light full one. Seafoam, Heather Gray, Cool Gray and Black &amp; Yellow."),
 "loma": ("Sunday Golf", "Loma", "$130", SG + "loma-friars-brown-par-3-bag",
   "The par 3 bag that started the brand: two pounds, room for about six clubs and a pocket for one cold can. Friars Brown and gold."),
}
SECTIONS = [
 ("Shapland", "shapland", ["rye", "kantle", "shsun"],
  "<strong>Three bags &middot; $475&ndash;$535 &middot; all sold out</strong>Leather, brass and hickory-wrapped legs. The line is sold out, so this is the bag to get on the list for."),
 ("Shoal Golf Co.", "shoal", ["standard", "reserve", "simple"],
  "<strong>Three bags &middot; $250&ndash;$450</strong>Waxed canvas made for walking, sold in preorder windows."),
 ("Jones Sports Co", "jones", ["trouper", "rover", "original"],
  "<strong>Three bags &middot; $185&ndash;$395 &middot; in stock</strong>Portland, since 1971. The only maker here you can order from today in every color."),
 ("MacKenzie", "mackenzie", ["mkwax", "mknylon", "mktreated"],
  "<strong>Three builds &middot; $405&ndash;$785</strong>Handmade carry bags, built to order. Photos from MacKenzie&rsquo;s collaborations."),
 ("Vessel", "vessel", ["vsunday", "vlux", "vcarry"],
  "<strong>Three bags &middot; $199&ndash;$999</strong>Carlsbad, since 2013. The most polished bags in the post."),
 ("Stitch Golf", "stitch", ["sl2", "air", "slsun"],
  "<strong>Three bags &middot; $198&ndash;$398</strong>Clean, coated bags that look like travel gear."),
 ("Sunday Golf", "sunday-golf", ["ryder", "elcamino", "loma"],
  "<strong>Three bags &middot; $130&ndash;$270</strong>San Diego. The cheapest way to upgrade, and the most fun."),
]
N = 21
PQ = {
 "shoal": ("crafted not to distract, but to complement the traditions of golf", "Shoal Golf Co.&rsquo;s mission"),
 "sunday-golf": ("I saw player after player lug around their full set when you really only use four or five clubs to play the course.", "Ronan Galvin, Sunday Golf co-founder, 2022"),
}
BANDS = {
 "jones-after": ("On the Course", "From Jones Sports Co&rsquo;s own photos.",
   [("band-1-1", "A golfer with a Jones Rover stand bag in cedar on a wooden porch", "Rover, Cedar"),
    ("band-1-2", "A Jones Trouper bag in cedar carried on the shoulder", "Trouper, Cedar"),
    ("band-1-3", "A Jones Rover stand bag in High Desert carried by its strap", "Rover, High Desert")]),
 "mackenzie-after": ("In the Wild", "From the Fyfe x MacKenzie lookbooks in Scotland.",
   [("band-2-1", "A MacKenzie carry bag leaning on a wooden hut in the Highlands", "Glen Affric"),
    ("band-2-2", "A MacKenzie carry bag standing in the dunes and fescue", "The dunes"),
    ("band-2-3", "A MacKenzie carry bag leaning against a yellow camper van", "7th Edition")]),
 "sunday-golf-after": ("Out Walking", "From Sunday Golf and Stitch Golf&rsquo;s own photos.",
   [("band-3-1", "A golfer carrying a black Sunday Golf Ryder bag on a coastal course", "Sunday Golf Ryder 14"),
    ("band-3-2", "A golfer carrying a navy Stitch SL2 bag on a terrace", "Stitch SL2"),
    ("band-3-3", "A golfer walking with a seafoam Sunday Golf El Camino bag", "Sunday Golf El Camino")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most golfers end up with a bag rather than choosing one. It came from a brother-in-law, a clearance rack or a full set bought in a box, and it works. But it is the piece of gear you carry for four hours and never swing, and at some point that is the argument for picking one on purpose.</p>
    <p><strong>What the money buys.</strong> Mainstream stand bags are printed polyester over a molded frame. The bags here go another way: waxed canvas that creases and darkens (Shoal, MacKenzie), oiled leather and brass (Shapland), full leather (Vessel&rsquo;s Sunday IV), or a single strap on a bag that has barely changed since 1971 (Jones). A bag should be quiet, light, and built to still look like itself in ten years.</p>
    <p><strong>Seven makers, three tiers.</strong> Sunday Golf and Stitch are the easy step up, from $130 to $398, and both are in stock. Jones, Shoal and Vessel sit in the middle at roughly $185 to $450. Shapland, MacKenzie and Vessel&rsquo;s leather Sunday are the top shelf, from $475 to $999.</p>
    <p><strong>Before you click.</strong> Shapland is sold out across every bag, with the next Rye, Kantle and Sunday 4.0 runs due in late November. Shoal sells in preorder windows and the current run ships December 15. MacKenzie&rsquo;s ready-made bags are sold out, but the builder takes orders. Jones, Vessel, Stitch and Sunday Golf ship now. Prices were checked on each brand&rsquo;s own site on November 1, 2026, in US dollars.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Makers</span><span>7</span></div>
      <div class="sidebar-detail"><span class="l">Bags</span><span>21</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$130&ndash;$999</span></div>
      <div class="sidebar-detail"><span class="l">Ships now</span><span>Jones, Vessel, Stitch, Sunday Golf</span></div>
      <div class="sidebar-detail"><span class="l">Preorder</span><span>Shoal, ships Dec 15</span></div>
      <div class="sidebar-detail"><span class="l">Sold out</span><span>Shapland</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Shoal Standard Bag</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfBags</span>
        <span class="hashtag">#CarryBag</span>
        <span class="hashtag">#WalkTheCourse</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">Built for the Walk</h2>
  <div class="writeup-body">
    <p>Every maker here started with walking. George Jones sewed the first Jones bags in his basement in Portland in 1971 and sold them out of the trunk of his taxi. Shoal says its bag was &ldquo;inspired by four years of collegiate play.&rdquo; Shapland borrows its names from Harry Colt&rsquo;s courses. Ronan Galvin built the first Sunday Golf bag after watching players at a nine-hole par 3 in San Diego carry fourteen clubs to use five.</p>
    <p>MacKenzie is the oldest name in the handmade end of the market, building carry bags by hand in Pennsylvania since 1985, and its collaborations with clubs and brands, from Fyfe in Scotland to ACL Golf, are some of the best photographed bags in golf.</p>
    <p>What they share is restraint: one or two straps, a light frame, materials that age well and nothing on the bag that dates it to a season. For more, read our <a href="/drops/brand-to-know-shoal-golf">Brand to Know on Shoal</a>, our <a href="/drops/brand-to-know-sunday-golf">Brand to Know on Sunday Golf</a>, <a href="/drops/brand-revisited-jones-sports-co">Jones Sports Co Revisited</a> and <a href="/drops/fyfe-x-mackenzie-every-edition">every Fyfe x MacKenzie edition</a>.</p>
  </div>
</section>
"""
META = "The Kit &middot; Seven makers &middot; Carry and stand bags"
HERO_ALT = "MacKenzie carry bags propped on a harbor wall with sailboats moored behind"
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/bag-upgrade-v2/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-22", "dateModified": "2026-11-01",
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
    <span>{META}</span><span class="dot"></span>
    <span>21 bags &middot; prices checked November 1, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
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
