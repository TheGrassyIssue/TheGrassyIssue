#!/usr/bin/env python3
"""build-publicdrip-revisit.py — Brand Revisited: Public Drip. 22 October 2026. Cloned from build-sloat-btk.py.
Lenny: "Let's do a brand revisited- .../public-drip-brooklyns-muni-born-golf-label" -> options sheet -> "let's build it and bring the post to the 1st slot".
Picks: everything new since June (Akashi-Kama x3, Nightshift FW26) + the core pieces, 19 cards -> v2 (22 Oct): "hero grainy", "remove the LIV golf mentions", "a little thin... more of a write up and more options", "background color for the products isn't right" -> 33 cards, site hero, stone backgrounds, no LIV/Cleeks.
FACTS: publicdrip.com products.json (USD, Oct 22 2026); research/publicdrip-revisit/brief.md (LINKS Apr 23 2026, LIV/Cleeks pages,
Instagram @publicdripbrand, Golfweek Sep 15). Akashi-Kama collab releases Oct 23. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Public Drip Revisited: Nightshift, Akashi-Kama and 33 Picks"
DESC = ("Four months after our first look at Brooklyn's muni-born Public Drip: the Nightshift fall collection, a Japanese-textile swing vest "
        "with Akashi-Kama, new pro shops, and 33 picks from $40 to $170.")
H1 = "Brand Revisited: Public Drip, From the Muni to the Pro Shop"
BC = "Brand Revisited: Public Drip"
SLUG = "brand-revisited-public-drip"
IMG = "/images/publicdrip-revisit"
SHOP = "https://publicdrip.com/products/"
C = "Public Drip"
AK = "Public Drip x Akashi-Kama"
P = {
 "a2": (AK, "Patchwork Swing Vest", "$140", "swing-vest-patchwork",
   "Our pick of the whole post. A ribbed V-neck sleeveless vest cut from a 100% cotton patchwork fabric Akashi-Kama supplied, with hidden button waist pockets for your on-course goods. Public Drip&rsquo;s line: &ldquo;There may not be a bigger flex on the course this fall than the swing vest.&rdquo; Releases October 23."),
 "a3": (AK, "Sharkskin Swing Vest", "$140", "swing-vest-sharkskin",
   "The same swing vest in a quieter 100% cotton sharkskin from Akashi-Kama, with ribbed trim and the collab logo embroidered on the back. Layer it over a long-sleeve mock. Releases October 23."),
 "a1": (AK, "&ldquo;Golf Abroad&rdquo; Long Sleeve Mock", "$115", "pa-ls-mock-neck-akashi-kama-coffee",
   "The long-sleeve player&rsquo;s mock in soft cotton, printed with a &ldquo;Golf Abroad&rdquo; graphic that reads hole, yard, par in Japanese. Coffee, with Akashi-Kama&rsquo;s &ldquo;NY to CA&rdquo; label at the hem. Releases October 23."),
 "n2": (C, "The Herringbone Half Zip", "$140", "the-herringbone-half-zip-coffee",
   "The Nightshift lead piece: a soft cotton-blend herringbone knit with a gold YKK zip, a felt P appliqu&eacute; and the script logo. Coffee or cream."),
 "n1": (C, "Triborough Waffle Knit Polo", "$110", "triborough-waffle-knit-polo-coffee",
   "A long-sleeve polo in a textured, quick-dry waffle knit with four-way stretch and the silicone P. Dress it up or down. Coffee, dark slate, black or navy."),
 "n3": (C, "Public Athlete Long Sleeve Mock", "$110", "public-athlete-long-sleeve-mock-coffee",
   "The player&rsquo;s mock with long sleeves, in cotton with the script logo at the chest and a tonal P on the sleeve. Coffee or cream. It&rsquo;s the base layer under both swing vests."),
 "n4": (C, "Anywhere Pleated Pants", "$170", "anywhere-pleated-pants-pinstripe",
   "The double-pleated trouser that made the brand&rsquo;s name, built on a classic suit pant in lightweight stretch nylon with a straight, tapered leg. Fall added pinstripe and charcoal to sand, black and olive."),
 "n5": (C, "&ldquo;P&rdquo; Script Denim Snapback", "$60", "p-script-denim-snapback-indigo",
   "Indigo denim five-panel with a felt P script and a leather strap. Made to get better the more you wear it."),
 "n6": (C, "&ldquo;P&rdquo; Script Denim Bucket", "$65", "p-script-denim-bucket-indigo",
   "The denim version of the bucket, with the felt P and branded seam tape inside. It&rsquo;s the hat on the hero up top."),
 "n7": (C, "Script Drip 3-Pack Marker Set", "$45", "3-pack-drip-marker",
   "Three gold-metal markers in green, black and maroon, with a drip alignment line and a faux-suede pouch."),
 "c1": (C, "Public Athlete Polo", "$95", "public-athlete-polo-coffee",
   "The everyday polo, and one Martin Kaymer has worn on tour: knit spread collar, embossed P, four-way recycled-poly stretch. Eight colors, with white and storm back in stock after selling out."),
 "c2": (C, "Public Athlete Blade Polo", "$90", "public-athlete-blade-polo-cream",
   "Still our favorite place to start: knit collar, hidden two-button placket, recycled-poly stretch. Cream, slate or sage."),
 "c3": (C, "Public Athlete Striped Polo", "$95", "public-athlete-striped-polo-olive-cream",
   "A jacquard-knit stripe with a contrast collar, in olive and cream or storm and white."),
 "p2": (C, "Public Athlete Frequency Polo", "$100", "public-athlete-frequency-polo",
   "A jacquard knit with a subtle pattern Public Drip says is meant to put you in the right mindset. Lightweight and breathable."),
 "p1": (C, "Public Athlete Up &amp; Down Polo", "$100", "public-athlete-up-down-polo",
   "A jacquard pattern inspired by the highs and lows of a round. Low stock, so check your size."),
 "p3": (C, "Public Athlete Retro Polo", "$100", "public-athlete-retro-polo",
   "A jacquard knit that borrows from classic polo patterns, with a modern cut."),
 "p4": (C, "Public Athlete Drip Stripe Polo", "$100", "public-athlete-drip-stripe-polo",
   "The statement stripe, in jacquard knit with a knitted spread collar and the embossed P."),
 "p5": (C, "Public Athlete Camo Polo", "$100", "public-athlete-camo-polo",
   "Camo drawn from the shapes of bunkers and greens, in a recycled-poly jacquard with a spread collar."),
 "p6": (C, "Public Athlete Tonal Polo", "$95", "public-athlete-tonal-polo-black",
   "The core polo with a tonal collar, in black or navy. As quiet as Public Drip gets."),
 "p7": (C, "Public Athlete Knit Polo", "$66", "public-athlete-knit-polo-ochre",
   "A 100% cotton sweater-knit polo with cross-stitch embroidery and a three-button placket. Ochre, green or navy, and the cheapest polo in the line."),
 "c4": (C, "The Dinner Polo", "$115", "dinner-polo",
   "A long-sleeve heathered piqu&eacute; with a felt P, made for the dinner after the round. Smoke."),
 "l1": (C, "Public Athlete Mock Neck", "$85", "public-athlete-mock-neck-cream",
   "The short-sleeve player&rsquo;s mock in a stretch poly blend with a silicone P, in cream or pine grove. Public Drip&rsquo;s line: &ldquo;Pinky up.&rdquo;"),
 "l2": (C, "Public Athlete Rugby", "$130", "public-athlete-rugby-navy-gold",
   "A 100% cotton rugby with a sturdy structure that softens with age, a three-button placket and a sewn-on felt P. Navy with gold or red stripes."),
 "c5": (C, "Swing Shirt", "$120", "swing-shirt-green",
   "Japanese nylon ripstop that packs into its own pocket, printed &ldquo;Always in the Bag.&rdquo; Green, cream or black."),
 "l3": (C, "Elevated Tee", "$50", "elevated-tee-green",
   "A relaxed tee inspired by Japanese street style, made from 100% recycled nylon fishnets. Green, cream or black."),
 "c6": (C, "Anywhere Tech Short", "$90", "anywhere-tech-short-olive",
   "Stretch nylon with a flat drawstring waist and belt loops. Olive or black."),
 "b1": (C, "Anywhere Cord Shorts", "$50", "anywhere-p-script-cord-shorts-navy",
   "Thin-wale cotton corduroy with a 6-inch inseam and a drawstring waist, in navy. Low stock."),
 "h1": (C, "&ldquo;P&rdquo; Script Nylon Snapback", "$40", "p-script-nylon-snapback-sand",
   "The lightweight, quick-drying everyday hat. Sand, pine grove, white or black."),
 "h2": (C, "&ldquo;P&rdquo; Script Nylon Bucket Hat", "$50", "script-nylon-bucket-hat-black",
   "Unstructured nylon with the P appliqu&eacute; and drip-pattern seam tape. Black, pine grove, sand or white."),
 "h4": (C, "Public Drip Classic Baseball Cap", "$50", "public-drip-classic-baseball-cap-sand",
   "Lightweight wool with a felt P script, a green satin underbrim and a leather strap. Sand, navy, forest green or black."),
 "h6": (C, "Fore All Nylon Snapback", "$40", "fore-all-nylon-snapback-black",
   "A nylon snapback with &ldquo;Fore All&rdquo; across the front, which Public Drip calls a reminder that the game is for everyone."),
 "h7": (C, "&ldquo;P&rdquo; Script Appliqu&eacute; Bucket", "$50", "p-script-applique-bucketwhite",
   "The classic bucket with a woven felt P patch, in white or black."),
 "h3": (C, "Script Driver Cover", "$90", "script-driver-cover-whiskey",
   "Genuine leather with a white leather P, two white stripes and the Drip club seal. Whiskey, green or black."),
}
SECTIONS = [
 ("Public Drip x Akashi-Kama", "akashi-kama", ["a2","a3","a1"],
  "<strong>Three pieces &middot; $115&ndash;$140 &middot; out October 23</strong>Built with Akashi-Kama, a Japanese-American label founded by Alec Nakashima, from fabrics Akashi-Kama supplied."),
 ("Nightshift, FW26", "nightshift", ["n2","n1","n3","n4","n5","n6","n7"],
  "<strong>Seven pieces &middot; $45&ndash;$170</strong>The fall collection, launched August 28: knits, mocks, pinstripes and denim."),
 ("The Polos", "polos", ["c1","c2","c3","p2","p1","p3","p4","p5","p6","p7"],
  "<strong>Ten polos &middot; $66&ndash;$100</strong>The heart of the brand. Every colorway sits in one card, and nearly all of them fit true to size."),
 ("Layers, Mocks &amp; Tees", "layers", ["c4","l1","l2","c5","l3"],
  "<strong>Five pieces &middot; $50&ndash;$130</strong>A dinner polo, a mock, a rugby, a packable shell and a tee made from fishing nets."),
 ("Shorts, Hats &amp; the Bag", "accessories", ["c6","b1","h1","h2","h4","h6","h7","h3"],
  "<strong>Eight pieces &middot; $40&ndash;$90</strong>Five hats, two shorts and a driver cover, all carrying the script P."),
]
N = 33
PQ = {
 "akashi-kama": ("My handicap is embarrassing. My kids don&rsquo;t care.", "Neil Tan, Public Drip founder, on Father&rsquo;s Day"),
 "nightshift": ("I almost think of the subway as being this mood board where you can see what everyone&rsquo;s wearing.", "Neil Tan, to LINKS"),
 "polos": ("I love the way some of my favorite dress shirts look, but you can&rsquo;t wear a dress shirt every day.", "Neil Tan, to LINKS"),
 "accessories": ("The city plays public.", "Public Drip, on its night at Flushing Meadows Pitch &amp; Putt"),
}
CAP = "Photography &middot; Public Drip"
BANDS = {
 "akashi-kama": ("The collab", "From the Public Drip x Akashi-Kama shoot.",
   [("site-31","A man in the patchwork swing vest over a cream long-sleeve, from the Akashi-Kama shoot","The Patchwork Swing Vest"),
    ("site-30","A man in the brown sharkskin swing vest over a cream long-sleeve in a vintage shop","The Sharkskin Swing Vest"),
    ("site-16","Close portrait in the patchwork swing vest and a denim P script snapback","Patchwork, with the denim snapback")]),
 "nightshift": ("Nightshift, on set", "From Public Drip&rsquo;s fall campaign, shot in a vintage shop.",
   [("site-8","A man in a coffee knit and P script cap in front of shelves of vintage boots","Nightshift"),
    ("site-10","A man in a cream long-sleeve mock and denim P script snapback","The cream mock and the denim snapback"),
    ("site-15","A man in the dark slate Triborough Waffle Knit Polo","The Triborough, in dark slate")]),
 "polos": ("Out in the world", "The polos off the set.",
   [("site-26","A man in the navy tonal polo and sand pants leaning on a laundromat cart","The Tonal Polo, at the laundromat"),
    ("site-63","A golfer with a carry bag in a striped polo and navy shorts in a clubroom","Spring 2026, in the clubroom"),
    ("site-64","A golfer in a mint polo and olive shorts on a lawn","The polo and the tech short")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we first wrote about <a href="/drops/public-drip-brooklyns-muni-born-golf-label" style="border-bottom:1px solid var(--ink)">Public Drip</a> in June, it was the Brooklyn label Neil Tan started in 2020, the year he went back to golf at Van Cortlandt Park in the Bronx after a decade away. Script-P polos, pleated trousers, a few good collabs and nothing over $170. Four months on, almost everything about the business has grown, and almost nothing about the clothes has gone corporate.</p>
    <p><strong>The clothes got better.</strong> Nightshift, the fall collection that landed August 28, is the strongest thing they&rsquo;ve made. The Herringbone Half Zip, a waffle-knit long-sleeve polo called the Triborough and pinstripe pleated pants look like a suit you can actually swing in. It&rsquo;s a fall line for golfers who play in New York in November, and it reads that way: browns, coffee, slate, denim.</p>
    <p><strong>The collab is the best thing on the site.</strong> Public Drip x Akashi-Kama, out October 23, puts Japanese patchwork and sharkskin textiles on a swing vest. The sleeveless V-neck is an old player&rsquo;s staple, and over a long-sleeve mock it&rsquo;s the outfit we&rsquo;d most like to be wearing on a cold first tee this fall.</p>
    <p><strong>It&rsquo;s in pro shops now.</strong> Public Drip went wholesale through RepSpark in January, took its first booth at the PGA Buying Summit in July and pre-sold Spring 2027 there. Stockists now include the new pro shop at Corica Park, the public course in Alameda whose youth programs it backed in May, and Black Desert Resort in Utah. Its line on the Corica shop: &ldquo;It&rsquo;s more than a stop for a sleeve of balls before your tee time.&rdquo;</p>
    <p><strong>It still plays public.</strong> The events are still muni events: a night at Flushing Meadows Pitch &amp; Putt in Queens with Five Boroughs Golf Club, an outing at Sullivan County Golf Club upstate. Martin Kaymer, a two-time major champion, wears the polos, and the brand celebrated Jorge Villar winning the Mexico Match Play this month. A brand that started on a public course in the Bronx now turns up at both ends of the game.</p>
    <p><strong>What hasn&rsquo;t changed:</strong> almost nothing costs more than $170, the script P is on everything, the polos fit true to size, and the founder still says his handicap is embarrassing. If you&rsquo;re buying one thing, get the Patchwork Swing Vest before it goes. If you&rsquo;re buying two, add the Long Sleeve Mock to wear under it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Since June</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Brooklyn, NY</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2020, Neil Tan</span></div>
      <div class="sidebar-detail"><span class="l">Collab</span><span>Akashi-Kama, Oct 23</span></div>
      <div class="sidebar-detail"><span class="l">Fall line</span><span>Nightshift, Aug 28</span></div>
      <div class="sidebar-detail"><span class="l">Stockists</span><span>Corica Park, Black Desert</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$40&ndash;$170</span></div>
      <div class="sidebar-detail"><span class="l">In the post</span><span>33 picks</span></div>
      <div class="hashtags">
        <span class="hashtag">#PublicDrip</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">How It Fits</div>
  <h2 class="products-hdr" id="fit">Sizing, Fabrics and Where to Start</h2>
  <p class="cat-kicker">Public Drip lists almost everything as true to size. The polos are recycled polyester with elastane, so they stretch and dry fast; the knits, mocks and rugby are cotton and sit closer to a sweater. The Anywhere Pleated Pants have a straight, tapered leg and run in S to XL rather than waist sizes, so check the size chart. Buckets come in S/M and L/XL. If you&rsquo;ve never worn the brand, the $90 Blade Polo or the $66 Knit Polo is the cheapest way to find your size before you spend $140 on a vest.</p>
</section>
"""
FAQ = [
 ("Who founded Public Drip?", "Neil Tan, who started the brand in Brooklyn in 2020 after getting back into golf at Van Cortlandt Park Golf Course in the Bronx."),
 ("When does the Public Drip x Akashi-Kama collab release?", "October 23, 2026: a Patchwork Swing Vest and a Sharkskin Swing Vest at $140 each, and a Golf Abroad long-sleeve mock at $115."),
 ("What is Public Drip Nightshift?", "Public Drip's fall 2026 collection, launched August 28, 2026, with the Herringbone Half Zip, Triborough Waffle Knit Polo, long-sleeve mocks, pinstripe Anywhere Pleated Pants and denim script hats."),
 ("Where can you buy Public Drip?", "On publicdrip.com, and in a growing number of pro shops and golf stores, including Corica Park in Alameda, California and Black Desert Resort in Utah."),
 ("Does Public Drip run true to size?", "Public Drip lists most pieces as true to size. The Anywhere Pleated Pants come in S to XL rather than waist sizes, and the bucket hats in S/M and L/XL."),
]
_LB = [("site-11","A man in a cream knit standing in front of shelves of vintage denim and boots","Nightshift"),
 ("site-19","A man in a cream knit, grey trousers and a P script cap in a vintage shop","Nightshift"),
 ("site-20","Close-up of a coffee knit and a golf club in a vintage shop","The details"),
 ("site-25","A man in sunglasses and the black tonal polo against a plain backdrop","The Tonal Polo, in black"),
 ("site-97","Three golfers in Public Drip sitting on a bench by a stone building","From the archive"),
 ("life-5","A golfer on the sand at Coney Island carrying a leather golf bag","Coney Island: &ldquo;This one meant something.&rdquo;"),
 ("life-12","A golfer on a beach carrying a leather Public Drip carry bag","&ldquo;My handicap is embarrassing. My kids don&rsquo;t care.&rdquo;"),
 ("life-14","Behind the scenes of a Public Drip campaign shoot, adjusting a hat","Behind the Spring 2026 shoot"),
 ("life-7","Public Drip&rsquo;s booth at the PGA Buying Summit in Frisco, Texas","Its first PGA Buying Summit, July")]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _LB)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">Since June, in Photos</h2>
  <p class="cat-kicker"><strong>From Public Drip&rsquo;s site and feed &middot; nine photos</strong>Nightshift, the archive and four months of muni golf, with the brand&rsquo;s captions where it wrote them.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/publicdrip-revisit/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-22", "dateModified": "2026-10-22",
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
    <span>Brand Revisited &middot; Brooklyn &middot; First covered June 15, 2026</span><span class="dot"></span>
    <span>33 picks &middot; prices checked October 22, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A man in the denim P script bucket and a cream long-sleeve in a vintage clothing shop, from Public Drip&rsquo;s Nightshift campaign" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Parmore", "Sounder", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
