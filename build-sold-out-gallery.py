#!/usr/bin/env python3
"""build-sold-out-gallery.py — "Gone Already": a gallery of sold-out collabs, one-offs and oddities from independent golf brands. 22 Oct 2026.
Lenny: "a post about cool stuff that has sold out ... these brands become a gallery of interesting products and out there items that the community snatched up fast.
Search our universe" -> "these just arent cool enough, I liked the palace / supreme clamp headcovers, anything from Sentinel, Gumtree and Malbon?" -> "unusual items or
stuff that are collabs, and one off projects" -> cuts 24,25,36,44,45,49 -> "anything else from our top 25 brands?" -> "show me how we'd organize" -> "okay, let's build it".
Cut to 35 (7 per section) as proposed. Blind Draw (#70, text-only image) swapped for Gumtree's NYC subway-token markers (#18); #32 swapped to Piretti's 1-of-1 GOAT putter;
#31 is the $25,000 801 Damascus 1 of 1 (not the $15,000 sibling).
FACTS: each store's own products.json / Squarespace JSON, read Oct 21-22 2026: every variant unavailable. Clamp reworks: delisted (404) from clampgolfcompany.co.uk;
title, contents and GBP price from our own capture in research/clamp/rework.json. Copy lines come from each product's own description. GBP shown with ~USD at x1.34;
EUR/AUD shown in the store's currency. Cards link to the brand's TGI page, since the product pages are sold out or gone.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Gone Already: 35 Sold-Out Pieces From Independent Golf"
DESC = ("A gallery of sold-out collabs, one-offs and oddities from independent golf brands: Clamp's Supreme and Louis Vuitton reworks, "
        "a $25,000 Damascus putter, Jimmy Choo x Malbon, Sentinel, Gumtree and more.")
H1 = "Gone Already: The Coolest Things Independent Golf Brands Sold Out"
BC = "Gone Already"
SLUG = "sold-out-independent-golf-gallery"
IMG = "/images/sold-out"
FR = json.loads((ROOT / "research/sold-out/frames.json").read_text())
def f(k): return FR[k]
def gbp(x): return f"&pound;{x:,} (~${round(x*1.34):,})"
P = {
 # key: (kicker, name, price, url, copy, frames, link label)
 "c1": ("Clamp Golf Company &middot; Yorkshire", "Supreme Reworked Headcovers", "Sold out at " + gbp(390), "/brands/clamp-golf-company",
   "One Supreme bag, cut into a whole kit: driver, wood and hybrid covers, an alignment-stick cover, a tee holder, a blade cover and a scope pouch. Clamp has since taken the listing down.", f("c1"), "The brand"),
 "c2": ("Clamp Golf Company", "Palace Reworked Headcovers", "Sold out at " + gbp(300), "/brands/clamp-golf-company",
   "Driver, wood, hybrid and blade covers made from a Palace bag in its Stella Artois&ndash;style &ldquo;Palace Artois&rdquo; print.", f("c2"), "The brand"),
 "c3": ("Clamp Golf Company", "Reworked Louis Vuitton Headcovers", "Sold out at " + gbp(1200), "/brands/clamp-golf-company",
   "The priciest rework Clamp listed: a Louis Vuitton monogram bag turned into driver, wood, hybrid and alignment-stick covers. A matching LV rangefinder pouch went too.", f("c3"), "The brand"),
 "c4": ("Dormie Workshop", "Sherwood x Dormie Hockey Glove Headcover", "Sold out at $1,000", "/brands/dormie-workshop",
   "Dormie pulled apart a Sherwood hockey glove in DeBrincat&rsquo;s red and rebuilt it as a driver cover. The padded fingers and the white SHERWOOD cuff lettering made the trip from the rink.", f("c4"), "The brand"),
 "c5": ("Matchstick Golf &middot; Portland", "USA Olympic Starter Jacket Headcover", "Sold out at $145", "/brands/matchstick-golf",
   "Handmade in a Portland workshop from a reclaimed USA Olympic Starter jacket, with marine-grade stitching and a Polartec fleece lining.", f("c5"), "The brand"),
 "c6": ("Bluegrass Fairway x Steurer &amp; Co", "The Barbour Carry Bag", "Sold out at $850", "/brands/bluegrass-fairway",
   "A one-of-a-kind Sunday carry bag made from a repurposed Steve McQueen Barbour jacket, with the jacket&rsquo;s own waist belt turned into the shoulder strap.", f("c6"), "The brand"),
 "c7": ("Midiron", "Upcycled Vintage Titleist Cap", "Sold out at A$69", "/brands/midiron",
   "Vintage Titleist caps tracked down by Midiron&rsquo;s founder, after the hand-me-down his grandad gave him when he was 10, then customized by Oxy Customs.", f("c7"), "The brand"),
 "o1": ("Piretti", "801 Damascus Steel Putter, 1 of 1", "Sold out at $25,000", "/brands/piretti",
   "The first of eight one-off 801D putters, milled from Damascus steel that&rsquo;s folded as many as 32 times. The most expensive thing on this page by a distance.", f("o1"), "The brand"),
 "o2": ("Piretti", "D&iacute;a de los Muertos GOAT, 1 of 1", "Sold out at $1,250", "/brands/piretti",
   "A one-of-one GOAT putter in 303 stainless steel with a plumber&rsquo;s neck and D&iacute;a de los Muertos engraving.", f("o2"), "The brand"),
 "o3": ("Bettinardi x Old Rip Van Winkle", "Oil Rubbed Bronze BB1, 1 of 1", "Sold out at $1,800", "/brands/bettinardi",
   "A 1-of-1 BB1 with a neck inlay made from Old Rip Van Winkle bourbon barrels. The Pappy collection went up on October 20 and this was gone when we checked the next day.", f("o3"), "The brand"),
 "o4": ("Bettinardi x Monopoly", "Take A Chance BB0, 1 of 1", "Sold out at $2,100", "/brands/bettinardi",
   "A Tour Blast BB0 with a gold flame neck and Mr. Monopoly CHANCE engravings, sold only through Bettinardi&rsquo;s HIVE.", f("o4"), "The brand"),
 "o5": ("Show Out Engraving", "Tropical Noir Ping s159 Wedge, 1 of 1", "Sold out at $500", "/brands/show-out-engraving",
   "A one-of-one 60&deg; wedge engraved with hibiscus, banana leaves, orchids and a watchful jaguar, designed for the Ping s159 cavity.", f("o5"), "The brand"),
 "o6": ("Mackem Golf", "Sample #04, Tapestry Headcover Set", "Sold out at A$260", "/brands/mackem-golf",
   "Mackem found some tapestry fabric and made one driver, fairway and hybrid set from it. It&rsquo;s labeled a sample, and they say they might make more.", f("o6"), "The brand"),
 "o7": ("Sounder", "The Golden Gun", "Sold out at " + gbp(475), "/brands/sounder",
   "A Sonartec SS07 five-wood reworked by hand: extra head weight, a flatter lie and a custom gold paint job. Sounder&rsquo;s restored clubs are one-offs by nature.", f("o7"), "The brand"),
 "u1": ("Malbon x Jimmy Choo", "Diamond Golf Shoe", "Sold out at $850", "/brands/malbon",
   "Jimmy Choo&rsquo;s Diamond trainer rebuilt for golf, with faceted Diamond cleats and Buckets, Malbon&rsquo;s mascot, on the heel.", f("u1"), "The brand"),
 "u2": ("Malbon x Futura", "Futura Walking Bag", "Sold out at $368", "/brands/malbon",
   "A rip-stop stand bag covered in a graphic taken from the artist Futura&rsquo;s abstract work.", f("u2"), "The brand"),
 "u3": ("Seamus x Pendleton", "Sugar Skulls Mallet Cover", "Sold out at $150", "/brands/seamus",
   "Pendleton wool in a D&iacute;a de los Muertos sugar-skull pattern, on a center-shafted mallet cover.", f("u3"), "The brand"),
 "u4": ("Manors x Reebok", "GOAT Pique Polo", "Sold out at $90", "/drops/reebok-x-manors-ii",
   "The striped cotton pique polo from Manors&rsquo; second Reebok collab.", f("u4"), "Our coverage"),
 "u5": ("Gumtree x Malbon", "Birds of Georgia Bird Calls", "Sold out at $128", "/brands/gumtree-golf",
   "Four wooden bird whistles, made by hand in France&rsquo;s Dr&ocirc;me region by Fran&ccedil;ois Morel, for Gumtree&rsquo;s Birds of Georgia collab with Malbon.", f("u5"), "The brand"),
 "u6": ("Mogshade x Depeche", "Depeche Magazine #5 + Headcover", "Sold out at &euro;99", "/brands/mogshade",
   "An issue of Depeche magazine sold with a special Re.Weave headcover made from rescued fabric woven in Portugal&rsquo;s Serra da Estrela.", f("u6"), "The brand"),
 "u7": ("VESSEL x Curry Brand", "Player Air Stand Bag", "Sold out at $389", "/brands/vessel",
   "VESSEL&rsquo;s lightweight Cordura Player Air stand bag, done with Stephen Curry&rsquo;s Curry Brand.", f("u7"), "The brand"),
 "m1": ("Sentinel Golf", "Kvadrat Headcovers", "Sold out at $108", "/brands/sentinel-golf",
   "Knit in Denmark from Kvadrat&rsquo;s textured 3D fabric, cut and sewn in New York, and lined in American Melton wool.", f("m1"), "The brand"),
 "m2": ("Sentinel Golf", "S&oslash;rensen Mallet Cover", "Sold out at $124", "/brands/sentinel-golf",
   "Made in Tokyo by FPS, a husband-and-wife label that started making headcovers as a hobby and now works mostly to order.", f("m2"), "The brand"),
 "m3": ("Sentinel Golf", "MajoTech Field Suit", "Sold out at $490", "/brands/sentinel-golf",
   "Sentinel calls it its most technical project yet: Italian MajoTech ripstop that&rsquo;s water repellent and windproof, a removable hood and a magnetic belt, cut and sewn in New York.", f("m3"), "The brand"),
 "m4": ("Gumtree Golf &amp; Nature Club", "Heirloom Quilt Headcover 11.0", "Sold out at $140", "/brands/gumtree-golf",
   "Cut from a single vintage American nine-patch quilt from around 1970 to 1990, so every one is one of a kind. This was the eleventh run.", f("m4"), "The brand"),
 "m5": ("Gumtree x Greens &amp; Streams", "Freshwater Fish Pitch Repair Tool", "Sold out at $85", "/brands/gumtree-golf",
   "Handmade in the shapes of four freshwater fish, with an engraved brass or steel insert.", f("m5"), "The brand"),
 "m6": ("Seamus Golf", "Hand Forged Sakura Ball Marker", "Sold out at $48", "/brands/seamus",
   "A copper cherry-blossom marker, forged in Portland, Oregon by a second-generation blacksmith.", f("m6"), "The brand"),
 "m7": ("Gumtree x Samuel Falzone", "Italian Leather Tote", "Sold out at $695", "/brands/gumtree-golf",
   "Tuscan leather, handmade in New Jersey by Samuel Falzone, with solid brass feet.", f("m7"), "The brand"),
 "w1": ("3 Putt Round x Lost Balls", "&ldquo;Addiction&rdquo; Tee Carton", "Sold out at &euro;75", "/brands/3-putt-round",
   "A cigarette-style carton of golf tees: eight packs of 21.", f("w1"), "The brand"),
 "w2": ("Dimple &amp; Divot", "Clay Pigeon Ball Marker", "Sold out at $88", "/brands/dimple-divot",
   "Matte orange brass, cut like a clay pigeon. Dimple &amp; Divot calls it the only target in your bag you actually want to find.", f("w2"), "The brand"),
 "w3": ("Radry Golf", "&ldquo;Radge&rdquo; Resin Figurine", "Sold out at $210", "/brands/radry-golf",
   "A 10-inch resin figure of Radry&rsquo;s mascot, numbered out of 35 with a signed certificate.", f("w3"), "The brand"),
 "w4": ("VESSEL", "24-Hour Automatic Watch", "Sold out at $295", "/brands/vessel",
   "A golf bag company&rsquo;s automatic watch, with a 24-hour subdial and a see-through caseback.", f("w4"), "The brand"),
 "w5": ("Seamus x SlackerTide", "&ldquo;Kramer&rdquo; Driver Cover", "Sold out at $155", "/brands/seamus",
   "Kramer and his famous golf scene embroidered on canvas, with &ldquo;Without Rules There&rsquo;s Chaos&rdquo; on the lid.", f("w5"), "The brand"),
 "w6": ("Gumtree Golf &amp; Nature Club", "NYC Subway Token Ball Markers", "Sold out at $35", "/brands/gumtree-golf",
   "Vintage New York City subway tokens, turned into a set of ball markers.", f("w6"), "The brand"),
 "w7": ("Ghost Golf", "KATANA Headcover Set", "Sold out at $297.50", "/brands/ghost-golf",
   "A full set, each cover named: HIT BOMBS on the driver, then FAIRWAY FINDER, PIN SEEKER and TRUSTY.", f("w7"), "The brand"),
}
SECTIONS = [
 ("Made From Something Else", "reworked", ["c1","c2","c3","c4","c5","c6","c7"],
  "<strong>Reworks and upcycles</strong>Streetwear and luxury bags, a hockey glove, an Olympic jacket and a Barbour, cut up and made into golf gear. Each one is limited by how much of the original there was."),
 ("One of One", "one-of-one", ["o1","o2","o3","o4","o5","o6","o7"],
  "<strong>One-offs and prototypes</strong>Putters, a wedge, a headcover set and a five-wood that only ever existed once."),
 ("Unlikely Partners", "collabs", ["u1","u2","u3","u4","u5","u6","u7"],
  "<strong>Collabs where the pairing is the story</strong>A luxury shoemaker, a graffiti artist, a wool mill, a sneaker giant, a French whistle maker, a magazine and an NBA star."),
 ("Made Properly", "craft", ["m1","m2","m3","m4","m5","m6","m7"],
  "<strong>Craft and materials</strong>Danish textiles, Tokyo handwork, Italian technical fabric, a vintage quilt, hand-forged copper and Tuscan leather."),
 ("The Weird Shelf", "weird", ["w1","w2","w3","w4","w5","w6","w7"],
  "<strong>The out-there stuff</strong>The things that make you ask who this is for, right before you find out it already sold."),
]
N = 35
PQ = {}
BANDS = {}
LS = ' style="border-bottom:1px solid var(--ink)"'
TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Independent golf brands don&rsquo;t make much of anything. A run is a few dozen pieces, sometimes a handful, sometimes one, and the best of it is gone in days. That&rsquo;s the business model, and it&rsquo;s why their sold-out pages are some of the most interesting places in golf. Big brands restock. Small ones move on, and what&rsquo;s left behind is a record of what the community actually grabbed.</p>
    <p>We went through the stores of every brand in our Brand Index, and more than 8,000 products were sold out in every size. Most of that is basics in last season&rsquo;s colors. The 35 here are the opposite: things that could only exist because the brand behind them is small.</p>
    <p><strong>Small means you can take the risk.</strong> No big company cuts a Louis Vuitton bag into headcovers, builds a driver cover out of a hockey glove, or makes one putter from Damascus steel and prices it at $25,000. A one-person workshop can, because it only has to find one buyer. Seven of these pieces are reworks of something else, and seven more existed exactly once.</p>
    <p><strong>The collabs are a map of who golf talks to now.</strong> A luxury shoemaker, a graffiti artist, a bourbon distillery, a wool mill, a magazine and an NBA star all turn up here, partnered with golf brands most people haven&rsquo;t heard of yet. The Pappy Van Winkle collection went up on Bettinardi&rsquo;s site on October 20, and its 1-of-1 putter was gone when we checked the next day.</p>
    <p><strong>It isn&rsquo;t all expensive.</strong> More than a third of this gallery sold for $150 or less: subway tokens turned into ball markers, a copper marker forged by a second-generation blacksmith, a cigarette carton full of tees. Getting in early mattered more than spending big.</p>
    <p>None of it is for sale right now. Prices are what each piece sold for, and a few may come back, but most won&rsquo;t. That&rsquo;s the point. Each card links to the brand&rsquo;s page on TGI, which is the best place to catch the next one.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Gallery</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>35, all sold out</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>23</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$35 to $25,000</span></div>
      <div class="sidebar-detail"><span class="l">Stores checked</span><span>Oct 21, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#SoldOut</span>
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#OneOfOne</span>
      </div>
    </div>
  </aside>
</section>
"""
MORE = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="next-one">How Not to Miss the Next One</h2>
  <p class="cat-kicker">Join the mailing lists, because most of these brands email before a drop goes live. Turn on Instagram post notifications for the few you care about most. Know your size before release day. And browse <a href="/brands"{LS}>our Brand Index</a>, where every brand here has a page with everything we&rsquo;ve written about them.</p>
</section>
"""
FAQ = [
 ("Why do independent golf brands sell out so fast?", "They make small batches, often a few dozen pieces and sometimes just one, so popular pieces can sell out within days of a drop."),
 ("What were Clamp Golf Company's reworked headcovers?", "Headcover sets the Yorkshire maker cut from other brands' bags, including Supreme, Palace and Louis Vuitton. The Louis Vuitton set listed at £1,200, and all of the reworks have since been removed from Clamp's store."),
 ("What is the most expensive sold-out piece in this gallery?", "Piretti's 801 Damascus Steel Putter, a 1-of-1 milled from folded Damascus steel, at $25,000."),
 ("Will these sold-out golf products come back?", "Some brands restock or remake popular pieces, but one-of-ones, prototypes and collabs usually don't return. Brand mailing lists are the best way to hear about the next drop."),
]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
def card(k, idx):
    kick, item, price, url, copy, fr, lab = P[k]
    ext = url.startswith("http")
    label = H.unescape(item).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    arrow = " &#8599;" if ext else " &#8594;"
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{kick}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}"{tgt} class="product-link">{lab}{arrow}</a></div></div>')


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
            items.append({"@type": "ListItem", "position": pos, "url": (P[h][3] if P[h][3].startswith("http") else "https://thegrassyissue.com" + P[h][3]), "name": H.unescape(P[h][1])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-21", "dateModified": "2026-10-21",
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
    figs = "\n".join(f'  <figure><img src="{IMG + "/" + f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {("piece" if anchor in ("reworked","one-of-one","collabs","craft","weird") else ("pick" if anchor=="pack" else "stop")) + ("" if len(ids)==1 else "s")}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert all((ROOT / f.lstrip("/")).is_file() for f in P[k][5]), k
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
    <span>35 pieces &middot; 23 brands</span><span class="dot"></span>
    <span>All sold out when we checked, October 21, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Four sold-out pieces side by side: Clamp&rsquo;s Supreme rework headcovers, a Gumtree headcover cut from a vintage quilt, Dormie&rsquo;s red Sherwood hockey glove headcover, and the copper Pappy Van Winkle x Bettinardi putter" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += MORE
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
