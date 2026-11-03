#!/usr/bin/env python3
"""build-around-the-greens.py — Around the Greens roundup, 3 November 2026. Cloned from build-vest-edit.py.
Lenny: "Around the Greens - Ball markers, divot tools, putter head covers and wedges" (9 each, options sheet first), then
"ballmarkers we havent done before, but include Swell golf. Include Totem, no on Seamus or students putter covers".
Sweep: ~155 indexed brand stores via browser products.json, Nov 3 2026. Prices as presented to a US visitor (Fyfe, Mackem,
Walker, Totem show USD); Sinking Birdies in GBP (x1.34). Markers chosen from products never linked on TGI before.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Around the Greens: 36 Ball Markers, Divot Tools, Putter Covers and Wedges"
DESC = ("Nine each of the best independent ball markers, divot tools, putter covers and wedges for 2026: Swell Marks, TOTEM, Walker, "
        "Fyfe, Mackem, Dormie, hand-stamped Piretti and torched Haywood wedges and more, all in stock.")
H1 = "Around the Greens: The Short-Game Kit"
BC = "Around the Greens"
SLUG = "around-the-greens-short-game-kit"
IMG = "/images/around-the-greens"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "m1": ("Swell Marks", "Rise &amp; Grind Red Sun Ball Marker", "$65", U("swellmarks.com","red-sun"),
   "Laser-colored, hand-finished stainless steel with a breaking wave and red sun on one side and RISE AND GRIND on the other. From Coronado."),
 "m2": ("Evnroll", "Get Even Mighty Marker", "$20", U("evnroll.com","ball-marker-get-even"),
   "A large hard-enamel marker with GET EVEN and &ldquo;Sweetest Face in Golf&rdquo; around the border, sold with a leather pouch. From the Carlsbad putter maker."),
 "m3": ("TOTEM", "Tag.01 Magnetic Ball Mark Tag, Raw Brass", "$90", U("totem.golf","tag-01-magnetic-ball-mark-tag"),
   "A precision-machined brass bag tag that holds a magnetic ball mark. Hangs off the bag, carries your name or a word of your choosing, and the mark comes off when you reach the green."),
 "m4": ("Walker Golf Things", "Ball Marker 3-Pack, The Australian Pack", "$40", U("walkergolfthings.com","ball-marker-3-pack-the-australian-pack"),
   "Three enamel and embossed markers: a classic kookaburra in sky blue, a brushed gold bottle cap and a Walker-green map of Australia. One for every mood on the green."),
 "m5": ("ANTi Country Club Tokyo", "Camacho Ball Marker", "$25.80", U("anticountryclubtokyo.com","anti-country-club-tokyo-camacho-green-marker"),
   "The Camacho monster, a symbol of 1970s anarchism, updated for golf in green. It is the Tokyo label&rsquo;s first green marker."),
 "m6": ("Provision Machining &amp; Design", "Brass Detour Sign Ball Marker", "$29.99", U("provisionmachiningdesign.com","brass-detour-sign-ball-marker"),
   "Machined from solid brass with an engraved, filled detour sign. For the player whose ball rarely takes the direct route."),
 "m7": ("Pluto Golf", "Evil Twin Floater Ball Marker, Platinum", "$29", U("pluto.golf","evil-twin-floater-ball-marker-silver-copy"),
   "Pluto&rsquo;s new floater marker, in black and platinum with the Evil Twin character. From Indianapolis."),
 "m8": ("Smathers &amp; Branson", "Crossed Clubs Needlepoint Ball Marker, Classic Navy", "$22.50", U("smathersandbranson.com","crossed-clubs-golf-ball-marker"),
   "Hand-stitched needlepoint crossed clubs on navy, set in a leather-rimmed marker. The preppy one."),
 "m9": ("Hazy Golf", "Hazy Golf x Luxury Ball Marker", "$40", U("hazygolf.com","untitled-oct31_14-23-32"),
   "316 stainless steel with the HG script on the face and HAZY GOLF around the edge. Thick and heavy enough to stay put on a windy green."),
 "d1": ("TOTEM", "1PCS Divot Tool, Titanium", "$90", U("totem.golf","1pcs-divot-tool-brass-copy"),
   "A one-piece titanium tool machined and balanced by hand, in a sand-blasted or stonewash finish. Built like an industrial object, not a giveaway."),
 "d2": ("Piretti Putters", "Workshop &ldquo;Augusta on my Mind&rdquo; Mini Divot Tool", "$99", U("pirettigolf.com","new-workshop-fruit-loop-mini-divot-tool-copy"),
   "A one-of-a-kind milled 303 stainless mini tool with Piretti&rsquo;s classic logo engraving, small enough to live in a pocket. From the Texas putter maker."),
 "d3": ("Provision Machining &amp; Design", "Copper Divot Tool", "$35.99", U("provisionmachiningdesign.com","custom-milled-golf-divot-tool"),
   "CNC-machined from solid copper, about three inches long and a quarter-inch thick. It will darken with every round."),
 "d4": ("Haywood Golf", "Arc Multi Tool", "$20", U("haywoodgolf.com","arc-multi-tool"),
   "A divot tool, magnetic ball marker and bottle opener in one pocket-friendly piece, in silver or black. Made for the round and everything after it."),
 "d5": ("Evnroll", "The Pitch Fork Divot Tool", "$25", U("evnroll.com","golf-divot-tool"),
   "Three forks cut from a single piece of metal, from the Carlsbad putter brand. Three prongs make quick work of a deep pitch mark."),
 "d6": ("VESSEL", "VESSEL x Birdicorn Divot Tool", "$29", U("vesselgolf.com","vessel-x-birdicorn-divot-tool"),
   "A limited six-in-one tool with a removable ball marker, from the Carlsbad bag maker. Thin and light enough to forget it is there."),
 "d7": ("Bettinardi Golf", "Wordmark Black Ox Divot Tool", "$120", U("bettinardi.com","bettinardi-wordmark-divot-tool"),
   "A single-prong Black Ox tool with the Hex B above the thumb contour and the Bettinardi wordmark in black paintfill on the reverse."),
 "d8": ("Sinking Birdies", "Bogey Machine Divot Tool", "&pound;14 (~$19)", U("sinkingbirdies.co.uk","bogey-machine-divot-tool"),
   "Solid metal with an enamel mystery-van graphic and a substantial feel for about the price of a sleeve of balls. From Hampshire, England."),
 "d9": ("Eastside Golf", "Swingman Divot Tool", "$25", U("eastsidegolf.com","multi-multi-color-swingman-divot-tool"),
   "Shaped like Eastside&rsquo;s Swingman logo, with Eastside Golf in script down the shaft. The most recognizable silhouette on the green."),
 "p1": ("Fyfe Golf", "Brechin Waxed Canvas Mallet Cover", "$95", U("fyfegolf.com","brechin-waxed-canvas-mallet-putter-cover"),
   "Charcoal Scottish waxed canvas made in Dundee by Halley Stevensons, with a semi-dry finish and a fleece lining. Built to weather well."),
 "p2": ("Bluegrass Fairway", "Redan Mallet Cover, Harris Tweed", "$80", U("bluegrassfairway.com","redan-mallet-putter-cover-in-harris-tweed-wool-suede-leather"),
   "Navy herringbone Harris Tweed on the front and roughout suede cowhide on the back, made in Louisville. It is meant to look better beat up."),
 "p3": ("Mackem Golf", "Fawcett Mallet Putter Cover", "$102", U("mackemgolf.com","fawcett-mallet-putter-cover"),
   "Deadstock wool-blend plaid in deep red, burnt orange and brown, cut in standard, center-shaft and Spider shapes. The most fall cover here."),
 "p4": ("Metalwood Studio", "World Class Waxed Canvas Mallet Cover, Black", "$108", U("metalwood.studio","world-class-waxed-canvas-mallet-putter-headcover-black"),
   "Black-on-black cotton waxed canvas from Metalwood&rsquo;s World Class line. Clean enough for any bag."),
 "p5": ("Lazyface", "The Mallet Cover", "$108", U("lazyface.com","the-mallet-cover"),
   "Deep green leather with Lazyface&rsquo;s yellow sun. Their reasoning: the truly lazy golfer would pick the more forgiving mallet."),
 "p6": ("Dormie Workshop", "Chevron Tobacco Center-Shafted Mallet Cover", "$160", U("dormieworkshop.com","dormie-chevron-tobacco-center-shafted-mallet"),
   "Rugged tobacco leather from the Halifax workshop, cut for center-shafted mallets. Dormie suggests measuring your putter against its size chart first."),
 "p7": ("Sugarloaf Social Club", "Classic SSC Mallet Putter Cover", "$85", U("sugarloafsocialclub.com","classic-ssc-mallet-putter-cover"),
   "Made in the USA for Sugarloaf by EP, with a magnetic closure, in five colors from white to yellow. Sugarloaf jokes it might make you switch to a mallet."),
 "p8": ("Walker Golf Things", "Dancing Kooka Leather Blade Cover", "$90", U("walkergolfthings.com","dancing-kooka-leather-blade-cover"),
   "Cream leather with embroidered dancing kookaburras and a velvet lining, from the Gold Coast brand&rsquo;s Dancing Kooka capsule."),
 "p9": ("Lamb Crafted", "Circle Texas Putter Cover, Navy/Lime", "$200", U("lambcrafted.com","circle-texas-putter-cover-navy-lime-green"),
   "Genuine leather, designed and stitched in Plano, with a heavy-duty magnetic closure and lime green interior. Fits blades and small half mallets. The Texas pick."),
 "w1": ("Edison Golf", "Edison 2.0 Wedge, Graphite", "$179", U("edisonwedges.com","2026-edison-2-0-wedges-graphite-shafts"),
   "Lofts from 49 degrees up, with KBS PGI graphite shafts, Lamkin grips and custom length and lie at no extra charge. From Rockport, Texas."),
 "w2": ("Avoda Golf", "W1 Wedge, DLC Black", "$186.30", U("avodagolf.com","w1-wedges-black"),
   "An extremely low-bounce wedge in DLC black, built for firm, tight lies and players who open the face wide and hit it high. Not for everyone, which is the point."),
 "w3": ("Piretti Putters", "Custom Handstamped 60&deg; Forged Wedge", "$299", U("pirettigolf.com","piretti-handstamped-60-forged-wedge"),
   "Forged by Fujimoto, then stamped by hand with a field of colorful icons around Piretti&rsquo;s script. The most fun wedge in the post."),
 "w4": ("Bettinardi Golf", "HLX 6.0 Molten Copper Wedge", "$250", U("bettinardi.com","hlx-6-0-molten-copper-pvd-wedges"),
   "Soft carbon steel with a molten copper PVD finish in C and RJ grinds, from 50 to 60 degrees. It will turn heads in the bunker."),
 "w5": ("Haywood Golf", "Copper-Torched Wedge, Head Only", "$230", U("haywoodgolf.com","haywood-copper-torched-wedges-heads-only"),
   "Haywood&rsquo;s tour wedge head with a raw copper layer, hand-torched until it blooms into purples, blues and sunset golds. No two match."),
 "w6": ("STIX", "Compete 56&deg; Wedge", "$119", U("stix.golf","compete-56-wedge"),
   "The same 56-degree sand wedge from the Compete set, sold on its own in right or left hand. The one you reach for most around the green."),
 "w7": ("Vice Golf", "VGW01 Wedge, Lime", "$99", U("vicegolf.com","vicegolf-vgw01-lime"),
   "A triple-forged head hand-built in Germany with lime paintfill. Under $100 for a forged wedge is hard to beat."),
 "w8": ("Piretti Putters", "Custom Handstamped USA Forged Wedge", "$299", U("pirettigolf.com","piretti-handstamped-usa-forged-wedge"),
   "Red, white and blue stars and stamps across the back of Piretti&rsquo;s forged head, in 52, 56 or 60 degrees."),
 "w9": ("Haywood Golf", "&ldquo;Stars &amp; Stripes&rdquo; Limited Wedge", "$150", U("haywoodgolf.com","haywood-stars-stripes-wedges-56-60-rh-limited-edition"),
   "A micro-batch of right-hand 56 and 60 degree wedges, each laser-engraved with a USA flag and finished in satin chrome."),
}
SECTIONS = [
 ("Ball Markers", "markers", ["m1","m2","m3","m4","m5","m6","m7","m8","m9"],
  "<strong>Nothing we have featured before</strong>Surf-town steel, a Tokyo monster, a kookaburra and needlepoint. A marker is the cheapest way to carry a little personality in your pocket, and the one thing everyone in your group sees on every green."),
 ("Divot Tools", "divot-tools", ["d1","d2","d3","d4","d5","d6","d7","d8","d9"],
  "<strong>Fix your mark, and one more</strong>From a $20 multi-tool to hand-balanced titanium. Every pick here has two or three solid prongs, which matter more than any logo on top."),
 ("Putter Covers", "putter-covers", ["p1","p2","p3","p4","p5","p6","p7","p8","p9"],
  "<strong>The cover you see most</strong>Your putter comes out on every hole, so its cover gets more looks than anything else in the bag. Waxed canvas, Harris Tweed, wool plaid and leather. Check blade or mallet before you buy."),
 ("Wedges", "wedges", ["w1","w2","w3","w8","w4","w5","w9","w6","w7"],
  "<strong>Where scores get made</strong>Hand-stamped, laser-engraved, torched and painted, from $99 to $299. Most of these makers offer custom loft, bounce and shaft, so the right wedge is the one fitted to your swing."),
]
N = 36
PAIRS = {}
BANDS = {
 "putter-covers": ("On the green", "Pitch marks fixed, from Sinking Birdies, TOTEM and Provision.",
   [("band-1-1","A Sinking Birdies Bogey Machine divot tool stuck in the grass","Sinking Birdies"),
    ("band-1-2","A TOTEM titanium divot tool on a golf bag","TOTEM"),
    ("band-1-3","A Provision Machining copper divot tool on a wooden table","Provision Machining &amp; Design")]),
 "wedges": ("In the bag", "A wool cover on a mallet, then copper and chrome, from Mackem, Haywood and Piretti.",
   [("band-2-1","A Mackem Fawcett plaid putter cover beside a mallet putter","Mackem Golf"),
    ("band-2-2","A hand holding a Haywood copper-torched wedge head over grass","Haywood Golf"),
    ("band-2-3","The face of a Piretti forged wedge resting on turf","Piretti Putters")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most of your strokes happen within fifty yards of the hole, and so do most of the small things you carry. A ball marker, a divot tool, a putter cover and a wedge: none of them cost much next to a driver, and all of them get used on every hole that matters.</p>
    <p><strong>How we picked.</strong> We went through the stores of the brands in our index, around 155 of them, and found over a thousand markers, tools, covers and wedges in stock. We kept nine of each, with no more than two from any one brand. Every ball marker here is one we have never featured before.</p>
    <p><strong>Ball markers.</strong> This is the place to have fun. A $22 needlepoint marker and a $90 machined brass tag do the same job, so pick the one you like looking at. Surf-town steel from Swell Marks, TOTEM&rsquo;s machined brass bag tag and ANTi Country Club Tokyo&rsquo;s Camacho monster lead the section.</p>
    <p><strong>Divot tools.</strong> Look at the prongs before the logo. Two solid prongs with a little taper fix a pitch mark cleanly; flimsy ones tear the turf. Everything here passes that test, from Haywood&rsquo;s $20 multi-tool to TOTEM&rsquo;s hand-balanced titanium.</p>
    <p><strong>Putter covers.</strong> Measure first. Blade, mallet and center-shaft covers are cut differently, and a few makers here offer several shapes of the same cover. After that, it comes down to material: waxed canvas and leather age well, wool plaid and Harris Tweed bring color.</p>
    <p><strong>Wedges.</strong> Get your wedges fitted if you can; most of the makers here will build to your loft, bounce, shaft and length. We went looking for the unusual ones: Piretti stamps its forged heads by hand, Haywood laser-engraves a flag or torches raw copper, and Avoda makes a black wedge with almost no bounce. If you buy one, buy the sand wedge you hit from 80 yards and in.</p>
    <p><strong>What is in here.</strong> 36 pieces from @@NB@@ brands, all in stock when we checked on November 3, 2026. Prices are what each store shows a US visitor; Sinking Birdies is listed in pounds with a rough dollar figure beside it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>@@NB@@</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>4</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$19&ndash;$299</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Swell Marks Rise &amp; Grind Red Sun Ball Marker</span></div>
      <div class="hashtags">
        <span class="hashtag">#ShortGame</span>
        <span class="hashtag">#BallMarker</span>
        <span class="hashtag">#GolfGear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Spend Where You Score</h2>
    <p>If you are going to upgrade one thing in this post, make it the wedge. A fitted sand wedge saves more strokes than any marker, tool or cover ever will.</p>
    <p>Then have fun with the rest. A marker you like looking at, a tool that fixes a mark properly and a cover that makes you smile when you pull the putter out are small things, but you will touch them on every green.</p>
    <p>For more small upgrades, see our <a href="/drops/small-golf-accessories-small-things-big-impact">small golf accessories</a> and <a href="/drops/swell-marks-hinotori-studio-grain-indie-golf-brands">Swell Marks, Hinotori and Studio Grain</a>.</p>
  </div>
</section>
"""
HERO_ALT = "Three photos side by side: Swell Marks ball markers on grass, Piretti forged wedges in a golf bag, and a Mackem plaid putter cover beside a mallet putter"
FRN = json.loads((ROOT / "research/around-greens/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-AG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-03", "dateModified": "2026-11-03",
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


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for s in SECTIONS: assert len(s[2]) == 9, s[0]
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
    <span>The Kit &middot; Markers, tools, covers, wedges</span><span class="dot"></span>
    <span>36 picks &middot; in stock, checked November 3, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Seamus", "Students", "vest", "Kraken", "Clint Orms", "Winston", "PXG", "Show Out"):
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
