#!/usr/bin/env python3
"""build-ashworth-btk.py — Brand to Know: Ashworth Golf Company (cloned from build-magpie-btk.py). 3 October 2026.\nLenny: "Let's do a brand to know- https://www.ashworth-golf.com/", then "drop a7,a8,9,a10,a11,a23, then build the post and make sure we have multiple images for each product". 31 picks from research/ashworth/picks.json; catalogue read 3 Oct 2026. Quotes verbatim from FashionUnited (16 Dec 2024), Global Golf Post (7 Mar 2025), Golf Today (14 Dec 2022). Photos: Ashworth's own store images.\n

Lenny: "Let's also do a brand to know - https://magpie-supply.com/", approved the TGI Take ("looks good, let's build it").
All 10 products run (the whole store). FACTS: catalogue, prices and stock read from the Squarespace JSON on 2 Oct 2026
(research/magpie/items.json); story from magpie-supply.com/our-story (quoted verbatim). Founder not named on the site.
PHOTOS: Magpie's own store and site images, localised to /images/magpie-supply.

--- original Palm docstring follows ---

Lenny: "Let's do a brand to know - https://palmgolfco.com/", then "looks good" on the 38-option sheet
(research/palm/options.json), so all 38 run. FACTS: catalogue read from palmgolfco.com/products.json on 2 Oct 2026;
story and founder quotes from MyGolfSpy, "Palm Golf Swings And Smiles Its Way To Cult Following" (Sean Fairholm,
21 Mar 2025, a brand-story feature); the MyGolfSpy comfort line is quoted on Palm's own homepage. Product copy written
from each listing and its photos. PHOTOS: Palm's own store images, localised to /images/palm-golf.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Ashworth Golf: The 1987 Polo Brand Is Back"
DESC = ("Brand to Know: Ashworth Golf Company, the 1987 cotton-polo brand, relaunched with founder John Ashworth back as "
        "creative director. Polos, fall layers, Golfman belts, Jones bags and shoes, with prices.")
H1 = "Brand to Know: Ashworth Golf Company, the Polo Brand That Came Home"
BC = "Ashworth Golf Company"
SLUG = "brand-to-know-ashworth"
IMG = "/images/ashworth"
SHOP = "https://www.ashworth-golf.com/products/"
A = "Ashworth"
P = {
 "a01": (A, "The O.G. Polo", "$98", "the-o-g-polo-white-denim",
   "The one that started it, rebuilt. Ashworth's original roomy cotton polo, now in CT Tech, a blend of fine Pima cotton and polyester that wicks and carries UPF 50+, with contrast tipping on the collar. Eight colourways."),
 "a02": (A, "Fairway Polo", "$89", "fairway-polo-golfman-velvet-white",
   "A crisp fine stripe in AG Tech, Ashworth's lightest performance knit, with stretch and a soft matte finish. It comes in eleven colourways, the widest run of anything in the store."),
 "a03": (A, "LS Newport Supima Polo", "$115", "ls-newport-supima-polo-kalamata",
   "A long-sleeve polo in Supima cotton interlock with a tailored collar, two-button placket and a tonal Golfman. The cool-morning polo, new for fall."),
 "a04": (A, "Fully Fashioned Polo", "$225", "fully-fashioned-polo-charcoal",
   "A knitted polo in 12-gauge superwash wool with a fully fashioned collar and ribbed cuffs. The most expensive polo in the store and the one that looks like it."),
 "a05": (A, "Houndstooth Polo", "$89", "houndstooth-polo-peyote-asphalt",
   "A small houndstooth in AG Tech, so it reads classic from ten feet and performs like a tech polo up close."),
 "a06": (A, "Starburst Polo", "$110", "starburst-polo-golfman-velvet-multi",
   "The loud one: an all-over starburst print on soft stretch cotton jersey, with a three-button placket. One colourway, new this month."),
 "a24": (A, "Golfman Walking Tee", "$45", "golfman-walking-tee-heather-columbia-blue-navy",
   "The Golfman, Ashworth's walking-golfer logo, drawn big across the chest of a soft cotton tee. Eight colourways, and the cheapest way into the brand."),
 "a12": (A, "Fully Fashioned V-Neck Sweater", "$265", "fully-fashioned-v-neck-sweater-golfman-velvet",
   "A 12-gauge superwash wool V-neck with contrast-trimmed cuffs. The sweater your grandfather wore to the club, cut for now."),
 "a13": (A, "Walt 1/4 Zip", "$265", "walt-1-4-zip-golfman-taupe",
   "A textured cotton jacquard quarter-zip with contrast trim at the zip, cuffs and hem. New on 21 September and the best-looking layer in the fall drop."),
 "a14": (A, "Aeroflex V-Neck Pullover", "$165", "aeroflex-v-neck-golfman-pullover-ag-khaki",
   "Ashworth's take on its own classic V-neck, in a four-way-stretch soft shell with a water-repellent finish. It shrugs off a light shower without restricting the swing."),
 "a15": (A, "Aeroflex Vest", "$145", "aeroflex-vest-golfman-asphalt",
   "The same stretch soft shell as a vest, with the Golfman on the back yoke. Four colourways."),
 "a16": (A, "Ace Raglan 1/4 Zip", "$110", "ace-raglan-1-4-zip-golfman-asphalt",
   "A smooth, stretchy performance quarter-zip with raglan sleeves and a relaxed athletic fit, for early tee times and travel days. Ten colourways."),
 "a17": (A, "Newport Supima Hoodie", "$125", "newport-supima-hoodie-kalamata",
   "A hoodie in 100% Supima cotton interlock with banded cuffs and hem and a tonal Golfman. Soft enough to wear off the course all winter."),
 "a18": (A, "1987 Golfman Hoodie", "$115", "1987-golfman-hoodie-grey-heather",
   "A heather-grey hoodie with the Golfman over the pocket. Ashworth's own listing recommends buying two, because one will get borrowed."),
 "a19": (A, "Golfman Satin Stitch Crew", "$125", "golfman-satin-stitch-crew-grey-heather",
   "A substantial crewneck with the Golfman in satin stitch, in grey heather, navy or black. Collected rather than casual."),
 "a20": (A, "Terry Twillback 1/4 Zip", "$125", "terry-twillback-1-4-zip-driver-navy",
   "A structured quarter-zip with a contrast zipper and a soft, stretchy CT Tech feel. Five colourways."),
 "a21": (A, "Pierside Cord Pant", "$125", "pierside-cord-pant-taupe",
   "Fine-wale corduroy, garment-washed, with a hint of stretch. New for fall in taupe and charcoal, with a 32-inch inseam."),
 "a22": (A, "GM Classic Pant", "$135", "gm-classic-pant-asphalt",
   "A traditional golf pant in AG Tech, cut in a classic golf fit. Ashworth suggests a size down if you like it trim."),
 "a25": (A, "Wide Wale Cord Woven Label Patch Cap", "$45", "wide-wale-cord-woven-label-patch-cap-charcoal",
   "An unstructured, low-profile wide-wale cord cap with a shield-shaped &ldquo;Since 1987&rdquo; patch and a leather buckle strap. New this fall."),
 "a26": (A, "Micro Cord Vintage Woven Patch Cap", "$45", "micro-cord-vintage-woven-patch-cap-steel-navy",
   "A lightweight perforated poly cap with a vintage woven Golfman patch. The one to actually play in."),
 "a27": (A, "Embossed Croc Golfman Belt", "$195", "embossed-croc-golfman-belt-indigo",
   "Embossed croc leather with a Golfman plaque buckle, in indigo, cognac, black, grey and chocolate. A heritage belt with some swagger."),
 "a28": (A, "Cloth Weave Belts", "$145", "cloth-weave-with-embossed-croc-tabs-olive-multi",
   "A textured cloth weave with embossed croc-leather tabs, new on 22 September in olive. The plain Cloth Weave Belt, also $145, comes in brown or grey."),
 "a29": (f"{A} x Jones", "Trouper Stand Bag", "$345", "trouper-stand-bag-cedar",
   "From the Ashworth x Jones bag line: a stand bag with a single or double strap, a five-way divider, seven pockets and an insulated cooler pocket that holds four cans."),
 "a30": (A, "Heritage Players Series Golf Bag", "$245", "heritage-players-series-golf-bag-kodiak",
   "A classic carry bag in Kodiak brown: a three-way divider, three pockets, a reinforced liner and a mesh sleeve for a big water bottle. Built for walking."),
 "a31": (A, "Heritage Clubhouse Duffle", "$175", "heritage-clubhouse-duffle-kodiak",
   "The matching Kodiak duffle, 20 by 11 by 11 inches, with one main compartment, a side pocket and a shoulder strap."),
 "a32": (A, "Heritage Classic Shoe Bag", "$95", "heritage-classic-shoe-bag-kodiak",
   "A ventilated shoe bag in vegan leather to match the duffle and carry bag."),
 "a33": (f"{A} x Jones", "The Ranger Shag Bag / Cooler", "$60", "the-ranger-shag-bag-cooler-charcoal",
   "A shag bag that doubles as a cooler, with a cinch top. Bring it to the range with balls, or to the course with drinks. Three colourways."),
 "a34": (A, "Reserve Classic Tour RS", "$180", "reserve-classic-tour-rs-white",
   "A spiked tour shoe with a Clarino microfiber upper, a waterproof membrane, PMX foam and Fast Twist spikes, in white or black."),
 "a35": (A, "X Tour Proto RS", "$200", "x-tour-proto-rs-white-black-pale-neon",
   "A spiked shoe Ashworth says was designed with tour-player input, in white and black with a pale neon accent."),
 "a36": ("Ashworth x Payntr", "Payntr X 002 F", "$200", "payntr-x-002-f-grey-black-white",
   "Made with Payntr: a full-grain leather upper treated to shed water and stains, a dual-density PMX foam midsole and a graphite plate for stability."),
 "a37": (A, "Match Day SC", "$200", "match-day-sc-black-black-gold",
   "A spikeless shoe Ashworth bills as the counterpart to Jason Day's tour model, with a waterproof bootie, PMXNitro+ cushioning and a Carbitex plate. Black and gold or white."),
}
SECTIONS = [
 ("The Polos", "polos", ["a01","a02","a03","a04","a05","a06","a24"],
  "<strong>Seven picks &middot; $45&ndash;$225</strong>The polo is the whole story. Ashworth built the brand on a roomier cotton polo in 1987, and the relaunch starts with the O.G., a modern version of the original. The rest run from tech stripes to a wool knit."),
 ("Fall Layers", "layers", ["a12","a13","a14","a15","a16","a17","a18","a19","a20"],
  "<strong>Nine picks &middot; $110&ndash;$265</strong>Most of these landed between 17 and 21 September: fully fashioned wool, a jacquard quarter-zip, stretch soft shells and Supima cotton hoodies, with the Golfman on nearly all of it."),
 ("Pants and Caps", "pants", ["a21","a22","a25","a26"],
  "<strong>Four picks &middot; $45&ndash;$135</strong>Cord was the theme of the fall drop: a cord pant and two cord caps, plus the classic golf pant."),
 ("Belts", "belts", ["a27","a28"],
  "<strong>Two picks &middot; $145&ndash;$195</strong>Ashworth sells ten belts, more than most apparel brands carry. These are the two we would wear."),
 ("The Bags", "bags", ["a29","a30","a31","a32","a33"],
  "<strong>Five picks &middot; $60&ndash;$345</strong>A stand bag from the Ashworth x Jones line, the Heritage set in Kodiak brown, and a shag bag that doubles as a cooler."),
 ("The Shoes", "shoes", ["a34","a35","a36","a37"],
  "<strong>Four picks &middot; $180&ndash;$200</strong>Ashworth's shoe line runs on PMX foam, and the X 002 F is made with <a href=\"/drops/the-payntr-collab-edit\" style=\"border-bottom:1px solid currentColor;\">Payntr</a>, golf's busiest collaborator."),
]
N = 31
PQ = {
 "polos": ("I always had a feeling that at some point, when the timing was right, I&rsquo;d be back, and now here we go.", "John Ashworth, founder, on returning as creative director, to FashionUnited, December 2024"),
 "pants": ("It feels natural, where I&rsquo;m supposed to be at this point in the journey.", "John Ashworth, March 2025"),
 "shoes": ("We continue to bump into golfers who have the Golfman tattoo &ndash; what other golf brand can say that?", "Eddie Fadel, Ashworth president, December 2022"),
}
BANDS = {
 "polos": ("Since 1987", "Ashworth's own photos.", [("band-10","A golfer in a pale green Ashworth polo","The polo"),("band-4","A golfer in a striped Ashworth polo carrying his bag","On the walk"),("band-11","A golfer in a white Ashworth polo and green shorts among palms","Desert golf")]),
 "layers": ("Honor the walk", "", [("band-1","A golfer in an olive Ashworth layer swinging on a hillside course","Fall layers"),("band-2","A golfer in an Ashworth sweater vest over a striped polo","The vest"),("band-3","A golfer in a white Ashworth sweater chipping","The V-neck")]),
 "bags": ("Rooted in the game", "", [("band-7","An Ashworth carry bag lying on the grass under trees","The Heritage bag"),("band-8","A golfer walking with his bag above the bay","On the coast"),("band-12","A golfer in Ashworth walking down a fairway","Down the middle")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Ashworth is the brand that made golf clothes California-casual, and after twenty-odd years of being passed around it is back in the hands of people who care about it. John Ashworth co-founded the company in 1987 as a relaxed alternative to the polyester that golf wore then: a roomier cotton polo, a walking-golfer logo called the Golfman, and Fred Couples wearing it. It was everywhere in the &rsquo;90s.</p>
    <p>Then it drifted. John Ashworth stepped down in 1997 and later started Linksoul. TaylorMade-adidas bought the brand in 2008, it went to the investment firm KPS with TaylorMade in 2016, and it now belongs to Hong Kong&rsquo;s YGM Group. The US relaunch came for 2023 under president Eddie Fadel, who worked at Ashworth in its early years, with Couples back on staff alongside Tom Hoge. In December 2024 John Ashworth returned as creative director.</p>
    <p>Nothing here is radical, and that is the point. There are no loud prints chasing the streetwear crowd, no reinvented silhouettes and no hype drops. The relaunch takes Ashworth&rsquo;s own back catalogue &mdash; the roomy polo, the Golfman, the stripes &mdash; and remakes it in better fabric: CT Tech cotton blends, AG Tech knits, fully fashioned wool and cord for fall. The Starburst polo is about as wild as it gets. It is for the golfer who wants classic clothes that still work in the heat.</p>
    <p>On quality, the one independent review of the relaunched range we found, from December 2024, is positive: sizing true to label, polos cut an inch longer in the back so they stay tucked, and soft, slick fabrics, with one striped polo rougher than the rest. Customer reviews are still thin. Prices were read on Ashworth&rsquo;s own store on 3 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1987, California</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>John Ashworth, back as creative director</span></div>
      <div class="sidebar-detail"><span class="l">President</span><span>Eddie Fadel</span></div>
      <div class="sidebar-detail"><span class="l">Owner</span><span>YGM Group, Hong Kong</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$45&ndash;$345</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The O.G. Polo, $98</span></div>
      <a href="https://www.ashworth-golf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Ashworth &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Ashworth</span>
        <span class="hashtag">#Golfman</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfPolos</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who owns Ashworth Golf now?", "YGM Group, a Hong Kong company. TaylorMade-adidas bought Ashworth in 2008, it moved to KPS with TaylorMade in 2016, and YGM now owns it and licenses it in the US, UK and South Korea."),
 ("Is John Ashworth back at Ashworth?", "Yes. The founder, who started the company in 1987 and stepped down in 1997, returned as creative director in December 2024."),
 ("What is the Ashworth Golfman?", "Ashworth's logo, a walking golfer carrying his bag. It is on most of the current range, from polos and hoodies to the belt buckle."),
 ("How much is an Ashworth polo?", "From $89 to $225 at full price on Ashworth's own store on 3 October 2026. The O.G. Polo, a modern version of the original, is $98."),
 ("Is Ashworth good quality?", "The one independent review of the relaunched range we found, from December 2024, found the sizing true to label, the polos cut an inch longer in the back to stay tucked, and the fabrics soft, with one striped polo rougher than the rest. Customer reviews are still sparse."),
 ("Does Ashworth make golf shoes and bags?", "Yes. It sells spiked and spikeless shoes from $180 to $200, including the X 002 F made with Payntr, and bags including the Trouper stand bag from the Ashworth x Jones line."),
]
FRN = json.loads((ROOT / "research/ashworth/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
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
         "url": URL, "image": og, "datePublished": "2026-10-03", "dateModified": "2026-10-03",
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
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>California, since 1987</span><span class="dot"></span>
    <span>31 picks &middot; in stock 3 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer carrying his bag under a big oak on a hillside course, from Ashworth" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
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
