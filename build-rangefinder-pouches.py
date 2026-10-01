#!/usr/bin/env python3
"""build-rangefinder-pouches.py — Keep the Laser Reachable: 16 rangefinder cases and pouches, plus 6 rangefinders.
1 October 2026. Lenny: "Let's do a post about rangefinder pouches- lots of cool options for keeping the laser
reachable- then also include some rangefinders", then "add some options from Quiet Golf & Sentinel", then
"no on P23, p22, p15,p14,p11 / yes on p18,p5".

FACTS: research/rangefinder/options.json (each read on the brand's own store, 1 Oct 2026). Garmin Z30 price read
on garmin.com in Chrome, 1 Oct 2026. Non-USD prices shown in store currency with approximate USD at
frankfurter.dev rates for 1 Oct 2026 (GBP 1.3234, EUR 1.1298, AUD 0.6951).
PHOTOS: brands' own store images, localised to /images/rangefinder-pouches (research/rangefinder/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "rangefinder-cases-and-pouches"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/rangefinder-pouches"
FRN = json.loads((ROOT / "research/rangefinder/frames.json").read_text())

TITLE = "Rangefinder Cases and Pouches: 16 Picks, Plus 6 Rangefinders"
DESC = ("Rangefinder cases and pouches from Sentinel, Quiet Golf, Fyfe, Winston, Jones, Mogshade and more, "
        "in waxed canvas, wool, leather and X-Pac, plus six rangefinders from $149.99. With prices.")
H1 = "Keep the Laser Reachable: 16 Rangefinder Cases and Pouches, Plus 6 Rangefinders"
OLD = '<a href="/drops/10-rangefinders-from-90-to-600">10 Rangefinders from $90 to $600</a>'

# key -> (brand, item, price, url, copy)
P = {
 "fyfe-marksman": ("Fyfe Golf", "Marksman Range Finder Case", "&pound;69 (~$91)",
   "https://www.fyfegolf.com/products/marksman-vintage-green",
   'Fyfe makes the Marksman in Scotland from P270 waxed canvas, with a dark brown leather pocket on the front, a mesh lining and a two-way waterproof YKK zip. It hangs from a matte black brass swivel hook on nylon webbing, and it comes in five colours, Vintage Green and Burnt Orange among them. More on the brand in our <a href="/drops/brand-to-know-fyfe-golf">Fyfe Brand to Know</a>.'),
 "bluegrass-recon": ("Bluegrass Fairway", "The Recon, Blackwatch", "$80",
   "https://www.bluegrassfairway.com/products/golf-rangefinder-case-in-blackwatch-waxed-canvas",
   "The Recon is Blackwatch tartan in heavyweight Scottish waxed canvas, trimmed in cigar leather and handmade in the USA. It clips on with a D-ring snap hook. Blackwatch is the only Recon left; the olive, camo, Pendleton wool and Harris Tweed versions have sold out."),
 "walker-canvas": ("Walker Golf Things", "Canvas Rangefinder Bag, Forest", "A$70 (~$49)",
   "https://walkergolfthings.com/products/canvas-rangefinder-bag-forest",
   "Walker Golf Things is an Australian brand, and this is the only case here that doubles as a crossbody bag. It comes with a detachable rope sling as well as a carabiner and webbing. The shell is heavyweight cotton canvas, padded inside, with the embroidered Kooka logo and a snap flap."),
 "lopar-canvas": ("Lopar Golf", "Canvas Rangefinder Case", "$75",
   "https://lopargolf.com/products/rangefinder-case-waxed-canvas",
   "Lopar&rsquo;s canvas case has a waxed look, a leakproof zip and a magnetic flap the brand calls EZYGrab, so the laser comes out with one hand. It comes in Washed Olive or Merlot Red."),
 "mogshade-course-case": ("Mogshade", "Course Case", "&euro;96 (~$108)",
   "https://mogshadegolf.com/products/grape-course-case",
   "Mogshade, from Portugal, sews the Course Case by hand from rescued wool fabric woven in the Serra da Estrela. It is round, with a pocket for a ball marker, loops for tees and an open compartment that holds the rangefinder. Four patterns are in stock, Grape included."),
 "winston-crazy-horse": ("Winston Collection", "Range Finder Case, Crazy Horse Leather", "$99.99",
   "https://winstoncollection.com/products/range-finder-case-in-crazy-horse-leather",
   "Winston cuts this one from full-grain waxed Crazy Horse leather and lines it in black polar fleece. It fits rangefinders up to six inches long and clips on with a carabiner. The leather darkens and scuffs the more you carry it."),
 "winston-tradition": ("Winston Collection", "Range Finder Case, Tradition Leather", "$119.99",
   "https://winstoncollection.com/products/tradition-leather-range-finder-case",
   "The Tradition is plain leather on the outside and McKenzie plaid fleece inside, so the tartan only shows when you open the flap. It comes in white, pink, red, navy and dark green; the open photo shows a light blue that has sold out."),
 "winston-aberdeen": ("Winston Collection", "Range Finder Case, Aberdeen Diamond Leather", "$129.99",
   "https://winstoncollection.com/products/aberdeen-diamond-range-finder-case",
   "The Aberdeen has an antique worn finish and a diamond deboss, with the same plaid fleece lining. Bone is the only colour in stock; the open photo shows the saddle version."),
 "jones-heritage-pouch": ("Jones Sports Co.", "Rangefinder Pouch, Heritage Collection", "$45",
   "https://jonessportsco.com/products/rangefinder-pouch-kodiak",
   'The Heritage pouch is Jones&rsquo;s cinch-top shape in deluxe vegan leather, in Kodiak brown and four other colours, with a YKK carabiner. Jones also sells collegiate versions, Texas included, for $70 to $80. See our <a href="/drops/brand-revisited-jones-sports-co">Jones revisit</a>.'),
 "qg-sentinel-scout": ("Quiet Golf x Sentinel", "Scout Bag", "$140",
   "https://quietgolf.com/products/qg-x-sentinel-golf-scout-bag-1",
   'Sentinel&rsquo;s Scout is the rangefinder case the others get compared to, and every colour on Sentinel&rsquo;s own store is sold out. <a href="/drops/brand-to-know-quiet-golf">Quiet Golf</a> still has its version in Navy and Olive. It is waterproof X-Pac lined in neoprene, with a Fidlock magnetic closure over a two-way waterproof YKK zip and a brass swivel hook. It is made in the USA.'),
 "sentinel-stash": ("Sentinel Golf", "Stash Pouch", "$62",
   "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-srmy2-h7w7l-39l7x-bsgfm-ywarl-9cpaj",
   'The Stash is <a href="/drops/brand-to-know-sentinel-golf">Sentinel&rsquo;s</a> valuables pouch, but at 9.5 by 6 inches it holds a rangefinder and a phone. It has an X-Pac shell, an AquaGuard zip, a snap panel on the back for two gloves and a carabiner loop, and it is cut and sewn in New York. Only a handful are left in black, cayenne and white.'),
 "north-coast-rf-case": ("North Coast Golf Co.", "Rangefinder Case", "$70",
   "https://northcoastgolfco.com/products/rangefinder-case",
   "North Coast&rsquo;s case has a waterproof double zip with paracord pulls, a magnetic flap, two inner pockets and a slit pocket on the back. It comes in five two-tone colourways, from sea green with a navy flap to light blue with teal."),
 "malbon-tour-divot": ("Malbon Golf", "Tour Divot Camo Rangefinder Case", "$128",
   "https://malbongolf.com/products/tour-divot-camo-rangefinder-case-bark-camo",
   "Malbon&rsquo;s case is ripstop nylon in bark camo, with a zip and bungee cords across the front. $128 is a lot for nylon, and most of it pays for the Tour Divot label."),
 "jones-rf-pouch": ("Jones Sports Co.", "Rangefinder Pouch", "$38",
   "https://jonessportsco.com/products/rangefinder-pouch-cedar",
   "The original Jones pouch is nylon with a cinch top and a YKK carabiner, made to match the colours of Jones bags. There are twelve colourways in stock."),
 "palm-utility-bag": ("Palm Golf Co.", "Utility Bag", "$35",
   "https://palmgolfco.com/products/utility-bag-range-finder-case-yosemite",
   "Palm&rsquo;s Utility Bag is padded, fleece-lined 900D Oxford with a zip rangefinder pocket on the front, a phone pocket on the back, a velcro pouch and four colourways to choose from."),
 "stickit-strap": ("STICKIT Magnetic Gear", "Magnetic Rangefinder Strap, Gen3", "$26.95",
   "https://stickitmagneticgear.com/products/stickit-magnetic-rangefinder-strap-2",
   "STICKIT is not a case at all. It is a slim elastic band with a large bar magnet that wraps the rangefinder and sticks it to the cart bar. It fits more than 50 models and comes in camo, skull, tiki and paisley prints."),
 "vc-el3": ("Voice Caddie", "EL3", "$149.99",
   "https://voicecaddie.com/products/el3-laser-rangefinder",
   "The EL3 is the smallest rangefinder here at 117 grams. It has 6x magnification, slope you can switch off, a built-in magnet and USB-C charging."),
 "bushnell-a1-slope": ("Bushnell Golf", "A1-Slope", "$299.99",
   "https://www.bushnellgolf.com/products/a1-slope",
   "Bushnell says the A1-Slope is the smallest rangefinder it has made. It weighs 5.1 ounces, reads to 1,300 yards, is rated IPX6 and charges over USB-C for 50-plus rounds. It ships with a BITE magnetic skin."),
 "nikon-50i-gii": ("Nikon", "Coolshot 50i GII", "$299.95",
   "https://www.nikonusa.com/p/coolshot-50i-gii/16789/overview",
   "The Coolshot 50i GII reads from 6 to 1,200 yards at 6x, with an incline/decline mode, a built-in magnet and a CR2 battery. Nikon gives it a five-year warranty."),
 "vc-tl1": ("Voice Caddie", "TL1", "$349.99",
   "https://voicecaddie.com/products/tl1-laser-rangefinder-with-slope",
   "The TL1 is the best-looking laser here, white and yellow, with a two-colour OLED display, auto slope, an integrated magnet and IP54 water resistance."),
 "garmin-z30": ("Garmin", "Approach Z30", "$449.99",
   "https://www.garmin.com/en-US/p/1411809/",
   "The Z30 reads pins to 400 yards and sends each distance to a Garmin watch or the Garmin app with Range Relay. It has PlaysLike distance, a magnetic mount and an IPX7 rating."),
 "bushnell-pro-x3-link": ("Bushnell Golf", "Pro X3+LINK", "$599.99",
   "https://www.bushnellgolf.com/products/pro-x3-link",
   "On top of slope, the Pro X3+LINK reads wind speed and direction, temperature and altitude. It has a 7x lens, an integrated BITE magnet and a locking slope switch, and it links to Foresight launch monitors over Bluetooth."),
}

SECTIONS = [
    ("Waxed Canvas and Wool", "canvas-and-wool", ["fyfe-marksman", "bluegrass-recon", "walker-canvas", "lopar-canvas", "mogshade-course-case"],
     "<strong>Five cases &middot; ~$49&ndash;$108</strong>These look like they came off an old shooting bag, and they get better with a season of dirt on them. Waxed canvas sheds a light rain and picks up creases and scuffs as you carry it, the way a good field jacket does. Fyfe and Bluegrass both use Scottish waxed canvas and trim it in leather, Lopar adds a magnetic flap, and Walker&rsquo;s comes with a rope sling so you can wear it. Mogshade is the odd one out: a round case sewn by hand from rescued Portuguese wool, with room for tees and a ball marker as well as the laser."),
    ("Leather", "leather", ["winston-crazy-horse", "winston-tradition", "winston-aberdeen", "jones-heritage-pouch"],
     "<strong>Four cases &middot; $45&ndash;$129.99</strong>Leather is the dressiest way to carry a rangefinder, and it ages the most. Three of these come from Winston Collection, which lines every case in fleece; two of them hide a McKenzie plaid lining that only shows when the flap is open. The Crazy Horse case is waxed full-grain leather that darkens with use, and the Aberdeen has a worn finish and a diamond deboss. The fourth is Jones&rsquo;s Heritage pouch in vegan leather, the cheapest way into the look at $45."),
    ("Built for Weather", "built-for-weather", ["qg-sentinel-scout", "sentinel-stash", "north-coast-rf-case", "malbon-tour-divot"],
     "<strong>Four cases &middot; $62&ndash;$140</strong>These are for the rounds that start in a drizzle, or the ones where the laser rides on the outside of the bag all day. Sentinel builds with X-Pac, a fabric laminated from nylon, polyester mesh and a waterproof film that is hard to tear, and seals it with waterproof YKK zips; its Scout case, sold here through Quiet Golf, adds a Fidlock magnet so the flap snaps shut on its own. North Coast pairs a waterproof double zip with a magnetic flap and extra pockets, and Malbon&rsquo;s ripstop camo case is the streetwear pick."),
    ("Under $40, and a Magnet", "under-40", ["jones-rf-pouch", "palm-utility-bag", "stickit-strap"],
     "<strong>Three picks &middot; $26.95&ndash;$38</strong>You do not need to spend $100 to get the laser out of the cupholder. Jones&rsquo;s original pouch is a nylon cinch-top in twelve colours to match its bags, and Palm&rsquo;s padded Utility Bag fits a phone as well as the rangefinder. STICKIT is not a case at all: it is a magnetic strap that wraps an older rangefinder and gives it the cart-bar magnet newer models have built in."),
    ("The Rangefinders", "rangefinders", ["vc-el3", "bushnell-a1-slope", "nikon-50i-gii", "vc-tl1", "garmin-z30", "bushnell-pro-x3-link"],
     f"<strong>Six lasers &middot; $149.99&ndash;$599.99</strong>Something to put in the case. Rangefinders have been getting smaller, and the Voice Caddie EL3 and Bushnell A1-Slope are both small enough to fit almost any pouch above. All six come with a magnet for the cart bar, and all six measure slope, with a way to switch it off for tournament play. Moving up the price range gets you a watch connection on the Garmin, then wind and temperature readings and launch-monitor pairing on the Bushnell Pro X3+LINK. None of these six were in {OLD}, so read the two together."),
]
N_POUCH = 16
N_RF = 6

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most rangefinders spend the round in the wrong place: zipped into a side pocket, rattling in a cupholder, or stuck to a cart bar that is thirty yards away when you need it. The built-in magnet only helps if you ride. Walk nine at <a href="/drops/lions-municipal-golf-course-austin">Muny</a> or <a href="/guides/roy-kizer-15">Roy Kizer</a> and the laser needs somewhere to live on the bag, where your hand finds it without looking.</p>
    <p>That is the job of a rangefinder case, and it has turned into one of the more interesting small things in golf. The case is the first thing anyone sees on your bag, so brands now treat it the way they treat headcovers. Fyfe uses Scottish waxed canvas and brass hardware, Mogshade sews it from old Portuguese wool, and Winston hides a tartan lining under plain leather.</p>
    <h2 class="products-hdr btk-story-hdr">What to Look For</h2>
    <p><strong>How it opens.</strong> A magnetic flap, such as Sentinel&rsquo;s Fidlock, Lopar&rsquo;s EZYGrab or North Coast&rsquo;s, opens with one hand. A zip is more secure, and a cinch top is the simplest of all. The best cases have a magnet over a zip, so you can use whichever the hole needs.</p>
    <p><strong>How it hangs.</strong> A swivel hook lets the case turn with the bag, and webbing keeps it from swinging into your hip. Walker&rsquo;s rope sling is for players who want the laser on them rather than on the bag.</p>
    <p><strong>Whether it fits.</strong> It is easy to buy one too small, so check the inside measurements against your rangefinder. Sentinel&rsquo;s Scout fits 3.5 by 5 by 2 inches; Winston&rsquo;s leather cases take lasers up to six inches long. Newer rangefinders like the Bushnell A1-Slope and Voice Caddie EL3 are small enough for almost any of these.</p>
    <p>If you buy one, buy the Quiet Golf x Sentinel Scout at $140. It is the best-made case here, and it is the only Scout you can still buy. Prices were read on each brand&rsquo;s own store on 1 October 2026; non-US prices show an approximate dollar figure.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Cases</span><span>16 cases, pouches and straps</span></div>
      <div class="sidebar-detail"><span class="l">Lasers</span><span>6 rangefinders</span></div>
      <div class="sidebar-detail"><span class="l">Cases from</span><span>$26.95&ndash;$140</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Quiet Golf x Sentinel Scout, $140</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>1 October 2026</span></div>
      <a href="#canvas-and-wool" class="sidebar-cta">See the cases &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#Rangefinder</span>
        <span class="hashtag">#GolfAccessories</span>
        <span class="hashtag">#GolfBag</span>
        <span class="hashtag">#GolfGear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is the best way to carry a rangefinder on a golf bag?",
     "Clip it to the bag in a case with a swivel hook or webbing, so it hangs where your hand finds it. A magnetic flap, like Sentinel's Fidlock closure, lets you open it with one hand. If you ride, a magnet on the rangefinder or a strap like STICKIT will hold it to the cart bar."),
    ("Do I need a case if my rangefinder has a magnet?",
     "If you always ride in a cart, maybe not. If you walk, the magnet has nothing to stick to, and a case keeps the laser on the bag and the lens out of the rain."),
    ("How do I know a rangefinder case will fit?",
     "Compare the case's inside measurements with your rangefinder. Sentinel's Scout fits 3.5 by 5 by 2 inches, and Winston's leather cases take rangefinders up to six inches long. STICKIT's strap fits more than 50 models."),
    ("How much does a rangefinder case cost?",
     "In this guide, from $26.95 for the STICKIT strap and $35 to $45 for pouches from Palm and Jones, up to $140 for the Quiet Golf x Sentinel Scout. Most waxed canvas and leather cases are $70 to $130."),
    ("Where can I buy a Sentinel Scout rangefinder case?",
     "As of 1 October 2026, every Scout on Sentinel's own store is sold out. Quiet Golf sells a QG x Sentinel Scout for $140 in Navy and Olive."),
]


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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    noun = "rangefinders" if anchor == "rangefinders" else "picks"
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {noun}</div>\n'
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
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-01", "dateModified": "2026-10-01",
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
            {"@type": "ListItem", "position": 3, "name": "Rangefinder Cases and Pouches", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N_POUCH + N_RF == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN.get(k), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Rangefinder Cases and Pouches</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Sentinel, Quiet Golf, Fyfe, Winston, Jones and more</span><span class="dot"></span>
    <span>22 picks &middot; in stock 1 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three rangefinder cases: a North Coast case held in a forest, a round Mogshade wool case hanging from a signpost, and a Walker canvas bag worn crossbody" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
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
    if fin.count('class="product-card"') != N_POUCH + N_RF: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
