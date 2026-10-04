#!/usr/bin/env python3
"""build-which-golfer.py — Which Golfer Are You? (cloned from build-ashworth-btk.py). 4 October 2026.\nLenny: archetype post, one post with seven types (G07 swapped for a bird headcover, Golf Traveler replaced by Former Skater, Cowboy renamed), TGI-featured brands only, five picks each chosen by Claude from the approved options; "good job, let's put it all together". Prices from research/archetypes/verified.json (4 Oct 2026).\n\nLenny: "Let's do a brand to know- https://www.ashworth-golf.com/", then "drop a7,a8,9,a10,a11,a23, then build the post and make sure we have multiple images for each product". 31 picks from research/ashworth/picks.json; catalogue read 3 Oct 2026. Quotes verbatim from FashionUnited (16 Dec 2024), Global Golf Post (7 Mar 2025), Golf Today (14 Dec 2022). Photos: Ashworth's own store images.\n

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

TITLE = "Which Golfer Are You? 7 Types and What to Buy"
DESC = ("Nature Lover, Muni Rat, Minimalist, Purist, Quiet Luxury, Cowboy or Former Skater: seven golfer types and "
        "five pieces for each, all from independent brands TGI has featured, with prices.")
H1 = "Which Golfer Are You? Seven Types and the Gear That Fits"
BC = "Which Golfer Are You?"
SLUG = "which-golfer-are-you"
IMG = "/images/golfer-archetypes"
SHOP = ""
def S(post, label="Our story"):
    return f' <a href="/drops/{post}" style="border-bottom:1px solid currentColor;">{label} &rarr;</a>'
P = {
 "g01": ("Gramicci", "Taos Canvas Jacket", "$127.50 (was $170)", "https://gramicci.com/products/taos-canvas-jacket",
   "A sturdy canvas chore-style jacket from the California climbing brand, on sale right now. Built for a cold dawn tee time or a trailhead."+S("brand-to-know-gramicci")),
 "g03": ("Palm Golf Co.", "Out of Bounds Towel", "$39.99", "https://palmgolfco.com/products/out-of-bounds-towel",
   "Rugged suede printed with a topo map, big enough for golf and made to roll up for camping."+S("brand-to-know-palm-golf-co")),
 "g04": ("Jones Sports Co.", "Rover Stand Bag, High Desert", "$295", "https://www.jonessportsco.com/products/rover-stand-bag-high-desert",
   "The Portland bag maker&rsquo;s stand bag in a sandy desert colour that looks at home on a hiking trail."+S("brand-revisited-jones-sports-co")),
 "g05": ("Sugarloaf Social Club", "Hidden Gem Scoutfitters Nalgene", "$32", "https://sugarloafsocialclub.com/products/hidden-gem-scoutfitters-32-oz-nalgene",
   "A 32oz Nalgene from Sugarloaf&rsquo;s Hidden Gem collection. The bottle that has been to every campsite, now in the golf bag."+S("ssc-hidden-gem-collection")),
 "g07": ("Magpie Supply x RossCo", "The Magpie x RossCo Headcover", "$100", "https://magpie-supply.com/on-the-course/p/the-magpie-tweed-headcover",
   "A magpie stitched on an aqua crown, made in Bandon, Oregon by RossCo Golf for the Denver leather shop. Named for the birds that gather on Denver&rsquo;s courses."+S("brand-to-know-magpie-supply")),
 "g08": ("Criquet", "Slub Graphic Tee, Lions Badge", "$58", "https://criquetshirts.com/products/slub-graphic-t-shirt-lions-badge-vintage-indigo",
   "Austin&rsquo;s Criquet made a Lions Municipal badge tee in vintage indigo. The uniform of the city&rsquo;s most famous muni."+S("brand-to-know-criquet")),
 "g09": ("Palm Golf Co.", "Divot Repair Tool (Bottle Opener)", "$11.99", "https://palmgolfco.com/products/divot-repair-tool-bottle-opener-silver",
   "Fixes your pitch marks and opens the tallboy on the 10th tee. The muni&rsquo;s two most important jobs, one tool."+S("brand-to-know-palm-golf-co")),
 "g10": ("Puttwell", "Putting Discs", "$30", "https://puttwellgolfclub.com/products/putting-disks",
   "A three-pack of practice discs with a carabiner, for the twenty minutes on the practice green before your twilight time."+S("brand-to-know-puttwell")),
 "g11": ("Jones Sports Co.", "Original Jones Bag, Navy/White", "$185", "https://www.jonessportsco.com/products/original-jones-bag-navy-white",
   "The simple carry bag that has walked more public courses than anyone. Light, cheap to love and built to last."+S("brand-revisited-jones-sports-co")),
 "g12": ("Hudson Sutler", "Small Heritage Range Bucket", "$125", "https://www.hudsonsutler.com/products/small-heritage-range-bucket",
   "A canvas range bucket made in New Jersey, for the muni rat who practises more than he plays."+S("brand-to-know-hudson-sutler")),
 "g14": ("Quiet Golf", "Vintage Supima Cotton Polo", "$118", "https://quietgolf.com/products/vintage-supima-cotton-polo",
   "A plain Supima cotton polo from the brand that named itself after saying less. No logo shouting, just a good collar."+S("brand-to-know-quiet-golf")),
 "g15": ("Magpie Supply", "Scorecard Holder", "$75", "https://magpie-supply.com/on-the-course/p/scorecard-holder",
   "Black full-grain leather made in Denver, for keeping score in pencil instead of an app."+S("brand-to-know-magpie-supply")),
 "g16": ("Quiet Golf", "Monogram Cotton Dad Hat", "$50", "https://quietgolf.com/products/qg-cotton-dad-hat",
   "A soft cotton cap with a small monogram. The only logo the Minimalist allows."+S("brand-to-know-quiet-golf")),
 "g17": ("Jones Sports Co.", "Short Course Bag, Navy", "$215", "https://www.jonessportsco.com/products/short-course-bag-navy",
   "A slimmer Jones built for a half set. Seven clubs, two balls, done."+S("brand-revisited-jones-sports-co")),
 "g20": ("St Andr&eacute;", "Classic Ball Marker", "$10", "https://standre.golf/products/st-andre-classic-ball-marker",
   "A clean, simple marker for ten dollars. Nothing more needed."+S("brand-to-know-st-andre")),
 "g21": ("Ashworth", "The O.G. Polo", "$98", "https://www.ashworth-golf.com/products/the-o-g-polo-white-denim",
   "A modern version of the roomy cotton polo Ashworth launched in 1987, now in a Pima cotton blend with contrast tipping."+S("brand-to-know-ashworth")),
 "g22": ("Seamus Golf", "Hand Forged Mesh Dimple Ball Marker, Steel", "$36", "https://seamusgolf.com/products/hand-forged-square-dimple-balata-ball-mark-steel",
   "Hammered by hand in Oregon with the square mesh dimples of an old-style ball."+S("brand-to-know-seamus")),
 "g23": ("Sentinel Golf x MacKenzie", "S&oslash;rensen Walker, Charcoal Nubuck", "$1,750", "https://www.sentinelgolf.us/shop/p/ultracomp-walker-mf43f-9nnps-8y9n3-aj82l-y9w5f",
   "A MacKenzie Walker made for Sentinel in charcoal nubuck from S&oslash;rensen, the family-owned Danish tannery. An 8-inch opening, one pocket, one strap, full-grain leather trim and stainless hardware, all in four pounds. Made in the USA to order and ships in about eight weeks."+S("brand-to-know-sentinel-golf")),
 "g25": ("Quiet Golf", "Harris Tweed Driver Head Cover", "$132", "https://quietgolf.com/products/harris-tweed-driver-head-cover",
   "A driver cover in Harris Tweed, the hand-woven Scottish cloth. About as traditional as a headcover gets."+S("brand-to-know-quiet-golf")),
 "g26": ("Hudson Sutler", "Heritage Golf Shoe Bag", "$149", "https://www.hudsonsutler.com/products/heritage-golf-shoe-bag",
   "Waxed canvas made in New Jersey, for carrying your shoes to the course the old way."+S("brand-to-know-hudson-sutler")),
 "g27": ("Quiet Golf", "San Marino Pant", "$178", "https://quietgolf.com/products/san-merino-pant",
   "A tailored trouser from Quiet Golf that wears like it cost more than it did. Which, at $178, is saying something."+S("brand-to-know-quiet-golf")),
 "g28": ("Ashworth", "Walt 1/4 Zip", "$265", "https://www.ashworth-golf.com/products/walt-1-4-zip-golfman-taupe",
   "A textured cotton jacquard quarter-zip with contrast trim, the best layer in Ashworth&rsquo;s fall drop."+S("brand-to-know-ashworth")),
 "g29": ("Hudson Sutler", "Heritage All Leather Weekender", "$399", "https://www.hudsonsutler.com/products/heritage-leather-weekender-bag",
   "A full-leather weekender in chestnut or espresso, made in New Jersey. For the member-guest weekend."+S("brand-to-know-hudson-sutler")),
 "g30": ("Ashworth", "Fully Fashioned Polo", "$225", "https://www.ashworth-golf.com/products/fully-fashioned-polo-charcoal",
   "A knitted polo in 12-gauge superwash wool. It looks like a sweater and plays like a polo."+S("brand-to-know-ashworth")),
 "g31": ("Sun Mountain", "Legacy Leather Stand Bag", "$1,199.99", "https://www.sunmountain.com/products/legacy-leather-stand-bag",
   "A full-leather stand bag from the Montana bag maker. The most expensive thing on this page, and it shows."+S("brand-to-know-sun-mountain")),
 "g33": ("Clint Orms", "Ball Marker 1801, Sterling Silver Texas Flag", "$300", "https://clintorms.com/products/sterling-silver-texas-flag-ball-marker",
   "A sterling marker with an engraved Texas flag, made and engraved by hand in Kerrville by the Hill Country silversmith."+S("austin-golf-weekend","Our Austin golf weekend")),
 "g34": ("Sierra Madre Golf", "Golf Cowgirl Trucker Hat", "$38", "https://sierramadregolf.com/products/golf-cowgirl-trucker-hat",
   "A cowgirl-on-a-golf-cart trucker from the Austin brand."+S("texas-golf-brands-and-makers","Our Texas makers guide")),
 "g35": ("Criquet", "Short Sleeve Corduroy Pearl Snap", "$128", "https://criquetshirts.com/products/short-sleeve-corduroy-pearl-snap-burnt-orange",
   "A burnt-orange corduroy pearl snap from Austin&rsquo;s Criquet. Wear it to the course and straight to the dance hall."+S("brand-to-know-criquet")),
 "g36": ("Ashworth", "Aztec Stitched Sicily Jean Belt", "$225", "https://www.ashworth-golf.com/products/aztec-stitched-sicily-jean-belt-cognac-brown",
   "A leather jean belt with Aztec stitching in cognac, chocolate or black. The closest thing to a rodeo belt in golf."+S("brand-to-know-ashworth")),
 "g38": ("Seamus Golf", "Hand Forged Lucky Horseshoe Ball Marker, Steel", "$48", "https://seamusgolf.com/products/hand-forged-mild-steel-lucky-horshoe-ball-mark",
   "A hand-forged horseshoe for the putt that has to drop."+S("brand-to-know-seamus")),
 "g39": ("Clamp Golf Company", "Supreme Reworked Mallet Headcover", "&pound;150 (~$202)", "https://www.clampgolfcompany.co.uk/products/supreme-reworked-mallet-headcover",
   "A one-of-one mallet cover sewn from an old Supreme piece in Clamp&rsquo;s Yorkshire workshop."+S("brand-to-know-clamp-golf-company")),
 "g40": ("Clamp Golf Company", "Palace Reworked Headcover Set", "&pound;300 (~$403)", "https://www.clampgolfcompany.co.uk/products/palace-reworked-headcovers",
   "A full set reworked from Palace, the London skate brand. One of one, so once it&rsquo;s gone it&rsquo;s gone."+S("brand-to-know-clamp-golf-company")),
 "g41": ("No Return Club", "Skull Ball Marker, Collectors Edition", "&pound;25.99 (~$35)", "https://noreturnclub.co.uk/products/ball-marker-brass-skull",
   "A brass skull from the UK club with a punk streak. The marker your playing partners will ask about."+S("brand-to-know-no-return-club")),
 "g42": ("Students Golf", "Calculus Baggy Pleated Pants", "$138", "https://studentsgolf.com/products/calculus-baggy-pleated-pants",
   "Wide, pleated and baggy, from the LA brand that made it fine to play in skate pants."+S("students-golf-our-15-favorites")),
 "g44": ("Public Drip", "&ldquo;P&rdquo; Script Denim Snapback", "$60", "https://publicdrip.com/products/p-script-denim-snapback-indigo",
   "An indigo denim snapback from the Brooklyn muni label. Flat brim optional."+S("public-drip-brooklyns-muni-born-golf-label")),
}
SECTIONS = [
 ("Nature Lover", "nature", ["g01","g03","g04","g05","g07"],
  "<strong>Five picks &middot; $32&ndash;$295</strong>The golfer who notices the course before the card. Canvas and topo maps, a towel you could take camping, a Nalgene instead of a plastic bottle, and a magpie on the driver. The round is an excuse to be outside for four hours."),
 ("The Muni Rat", "muni", ["g08","g09","g10","g11","g12"],
  "<strong>Five picks &middot; $11.99&ndash;$185</strong>Plays twilight, walks and carries, and knows the starter by first name. The kit is cheap, tough and a little sentimental: a Lions Muni tee, a divot tool that opens a beer, a range bucket and a Jones bag that has seen every public course in town."),
 ("The Minimalist", "minimalist", ["g14","g15","g16","g17","g20"],
  "<strong>Five picks &middot; $10&ndash;$215</strong>One logo, if any. Navy, bone and white, a slim bag with nothing in it that doesn&rsquo;t need to be there, and a scorecard holder instead of an app. The goal is to look like you&rsquo;ve been playing for twenty years without saying so."),
 ("The Purist", "purist", ["g21","g22","g23","g25","g26"],
  "<strong>Five picks &middot; $36&ndash;$1,750</strong>Believes golf peaked somewhere between persimmon and balata. Cotton polos, a carry bag, a hand-forged marker and a Harris Tweed headcover. The Purist would rather walk nine holes than ride eighteen."),
 ("The Quiet Luxury Golfer", "quiet-luxury", ["g27","g28","g29","g30","g31"],
  "<strong>Five picks &middot; $178&ndash;$1,199.99</strong>Expensive, never loud. Wool, leather and a jacquard quarter-zip, a leather weekender and a leather bag. Nothing has a big logo, and everything costs more than you&rsquo;d guess."),
 ("The Cowboy", "cowboy", ["g33","g34","g35","g36","g38"],
  "<strong>Five picks &middot; $38&ndash;$300</strong>Texas golf with a belt-buckle attitude. A sterling Texas-flag marker made in Kerrville, a pearl snap, a lucky horseshoe and a cowgirl trucker from Austin. Plays fast and tips the cart girl well."),
 ("The Former Skater", "skater", ["g39","g40","g41","g42","g44"],
  "<strong>Five picks &middot; about $35&ndash;$403</strong>Grew up on a board, found golf later and brought the wardrobe. Baggy pleats, a denim snapback, a skull ball marker and headcovers sewn from old Supreme and Palace pieces. Still treats every round like a session."),
]
N = 35
PQ = {}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Every golfer is a type. You know them from the first tee: the guy in a waxed-canvas jacket who stops to look at a hawk, the one walking 18 at the muni with a bag older than his car, the one whose whole kit is navy and white. Golf has always been a game you dress for, and what you carry says as much about you as your handicap.</p>
    <p>So we sorted the brands we&rsquo;ve featured on TGI into seven types and picked five pieces for each, from a $10 ball marker to a $1,200 leather bag. Every item comes from an independent brand we&rsquo;ve already written about, and each one links back to our full story on it. Find yourself, find your partner, or find the gift for the golfer who has everything. Prices were checked on each brand&rsquo;s own store on 4 October 2026; UK prices are shown in pounds with an approximate dollar figure.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Types</div>
      <div class="sidebar-detail"><span class="l">01</span><span><a href="#nature">Nature Lover</a></span></div>
      <div class="sidebar-detail"><span class="l">02</span><span><a href="#muni">The Muni Rat</a></span></div>
      <div class="sidebar-detail"><span class="l">03</span><span><a href="#minimalist">The Minimalist</a></span></div>
      <div class="sidebar-detail"><span class="l">04</span><span><a href="#purist">The Purist</a></span></div>
      <div class="sidebar-detail"><span class="l">05</span><span><a href="#quiet-luxury">The Quiet Luxury Golfer</a></span></div>
      <div class="sidebar-detail"><span class="l">06</span><span><a href="#cowboy">The Cowboy</a></span></div>
      <div class="sidebar-detail"><span class="l">07</span><span><a href="#skater">The Former Skater</a></span></div>
      <a href="/brands" class="sidebar-cta">The Brand Index &#8594;</a>
      <div class="hashtags">
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#WhichGolferAreYou</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What kind of golfer am I?", "Start with what you already reach for. If you walk and carry at public courses, you are probably a Muni Rat; if your kit is all navy and white, a Minimalist; if you want cotton, tweed and a carry bag, a Purist. Most golfers are two types at once."),
 ("What is a good gift for a golfer?", "Something they will use every round. A ball marker ($10 to $48), a towel ($39.99) or a scorecard holder ($75) works for almost anyone; a pearl snap, a Harris Tweed headcover or a reworked Supreme cover suits a specific type."),
 ("Are these all independent golf brands?", "Yes. Every item comes from an independent brand TGI has already featured, and each card links back to our full story on that brand."),
 ("When were these prices checked?", "On each brand's own store on 4 October 2026. Clamp Golf Company and No Return Club are UK brands, so their prices are shown in pounds with an approximate dollar figure."),
]
FRN = json.loads((ROOT / "research/archetypes/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-04", "dateModified": "2026-10-04",
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
    <span>Seven types</span><span class="dot"></span>
    <span>35 picks &middot; checked 4 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three golfer types: a magpie headcover on a bag, a golfer walking above the bay, and a golfer in a streetwear tee on a city street at night" fetchpriority="high" /></div></div>
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
