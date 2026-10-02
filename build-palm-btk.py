#!/usr/bin/env python3
"""build-palm-btk.py — Brand to Know: Palm Golf Co. (cloned from build-break80.py). 2 October 2026.

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

TITLE = "Palm Golf Co.: The Huntington Beach Glove Brand"
DESC = ("Brand to Know: Palm Golf Co., the Huntington Beach glove brand started by three friends from a muni. "
        "Gloves, USA-made headcovers, caps, hoodies and the REEF shoe collab, with prices.")
H1 = "Brand to Know: Palm Golf Co., the Glove Brand That Grew Up at the Muni"
BC = "Palm Golf Co."
SLUG = "brand-to-know-palm-golf-co"
IMG = "/images/palm-golf"

G = "$27.99 (3 for $69)"
P = {
 "p01": ("Palm Golf Co.", "Barrels and Birdies Glove", G, "mens-barrels-and-birdies-glove",
   "The glove Palm launched with in 2017 and still its signature: white AAA cabretta leather, Lycra between the fingers and a tropical tab with the palm logo. Every Palm glove is USGA conforming and sells three for $69."),
 "p02": ("Palm Golf Co.", "Ball Marker Glove", G, "mens-mag-glove",
   "New this week. The tab hides a magnet that holds a Palm ball marker, so the marker rides on your hand rather than in a pocket. Swap in the skull, the golf cart or the hula girl."),
 "p03": ("Palm Golf Co.", "Rhythm Glove", G, "mens-rhythm-glove",
   "An orange palm on a dark tropical tab, from the summer Rhythm collection that also gave us the hoodie and the headcovers."),
 "p04": ("Palm Golf Co.", "Hula Glove", G, "mens-hula-glove",
   "A hula-print tab from the summer Hula collection, which also covers caps, a tee and headcovers."),
 "p05": ("Palm Golf Co.", "Sea Isle Glove", G, "mens-sea-isle-glove",
   "A gold palm on a yellow tab, in the range since 2023."),
 "p06": ("Palm Golf Co.", "Canvas Glove", G, "mens-canvas-glove-white",
   "The plainest Palm glove: white leather with a green palm badge. For the golfer who wants the fit without the print."),
 "p07": ("Palm Golf Co.", "Wanderer Glove", G, "mens-wanderer-glove",
   "A teal palm badge on white, part of the outdoorsy Wanderer collection with the caddie towel."),
 "p08": ("Palm Golf Co.", "Night Moves Driver Headcover", "$89.99", "night-moves-driver-headcover-1",
   "Every Palm headcover is made in the USA with a DRYTEX shell that shrugs off rain and a sherpa lining. Night Moves is the dark one, charcoal with palm-tree silhouettes and a leather Palm tab."),
 "p09": ("Palm Golf Co.", "Night Moves Orange Driver Headcover", "$89.99", "night-moves-orange-driver-headcover",
   "The same Night Moves pattern in safety orange, from the fall drop on 30 September. The loudest cover Palm makes."),
 "p10": ("Palm Golf Co.", "Tropics Driver Headcover", "$89.99", "tropics-driver-headcover",
   "A cream cover in a tropical floral print, new for fall. It looks like a vintage aloha shirt."),
 "p11": ("Palm Golf Co.", "Olas Driver Headcover", "$89.99", "olas-driver-headcover",
   "Olas means waves, and this one is serape stripes in turquoise, red and cream. New on 30 September."),
 "p12": ("Palm Golf Co.", "Halloween Driver Headcover", "$89.99", "halloween-black-driver-headcover",
   "Black with skulls, for October. A seasonal cover, so it will not be around long."),
 "p13": ("Palm Golf Co.", "Beachin' Driver Headcover", "$89.99", "beachin-driver-headcover",
   "A beach-day print from the August Beachin' drop, also sold as a fairway and hybrid cover."),
 "p14": ("Palm Golf Co.", "Reef Dangerous Rips Red Driver Headcover", "$89.99", "reef-dangerous-rips-red-driver-headcover",
   "From the REEF collaboration: deep red with a &ldquo;Warning: Dangerous Rips&rdquo; sign, a beach joke that works on a driver."),
 "p15": ("Palm Golf Co.", "Hula Black &amp; White Driver Headcover", "$89.99", "hula-black-white-driver-headcover",
   "The hula print in black and white, made to order in 7 to 10 days. Palm sells it in driver, fairway and hybrid."),
 "p16": ("Palm Golf Co.", "Rhythm Tan Driver Headcover", "$89.99", "rhythm-tan-driver-headcover",
   "Tan with the Rhythm palm-and-flowers crest and &ldquo;find your rhythm&rdquo; around it. Made to order."),
 "p17": ("Palm Golf Co.", "Cart Cruisin' Yellow Driver Headcover", "$89.99", "cart-cruisin-yellow-driver-headcover",
   "From the Cart Cruisin' collection, made to order. Pairs with the Cart Cruisin' cap and tee."),
 "p18": ("Palm Golf Co.", "Harbor Barrel Fairway Headcover", "$89.99", "harbor-bucket-wood-headcover",
   "A barrel-shaped fairway cover in Harbor blue with &ldquo;swing and smile&rdquo; in script, made to order."),
 "p19": ("Palm Golf Co.", "Lazy Palm Strapback", "$34.99", "lazy-palm-strapback-yellow",
   "An unstructured dad hat with a curved bill and a round palm patch, designed with women in mind but cut to fit anyone. It comes in seven colours."),
 "p20": ("Palm Golf Co.", "Local Performance Snapback", "$44.99", "local-performance-snapback",
   "A water-resistant performance snapback with the palm in a circle, in several colourways."),
 "p21": ("Palm Golf Co.", "OB Snapback", "$44.99", "ob-snapback-black",
   "A black performance snapback with an OB patch, new in late September."),
 "p22": ("Palm Golf Co.", "Paradise Golf Club", "$44.99", "paradise-golf-club",
   "A rope snapback with a Paradise Golf Club badge, the clubhouse cap for a club that does not exist."),
 "p23": ("Palm Golf Co.", "Cart Cruisin' Snapback", "$44.99", "cart-cruisin-snapback",
   "A white performance snapback from the Cart Cruisin' collection, built for hot rounds."),
 "p24": ("Palm Golf Co.", "Rhythm Hoodie", "$79.99", "rhythm-hoodie-bone",
   "A soft fleece hood with the &ldquo;find your rhythm&rdquo; palm crest on the back. Palm writes that you can have all the speed in the world, but without tempo you are just swinging blindly."),
 "p25": ("Palm Golf Co.", "Local Hoodie", "$71.99", "local-hoodie-navy",
   "A navy fleece hoodie with the palm patch sewn over the heart. The plain one, for after the round."),
 "p26": ("Palm Golf Co.", "Uptown Polo", "$74.99", "uptown-polo",
   "A white performance polo in a fine stripe with the palm script on the chest. Light, stretchy and wearable off the course."),
 "p27": ("Palm Golf Co.", "Coasty Polo", "$39.99", "coasty-polo-heather-red",
   "A heathered red polo in a stretch blend, sold as office-to-tee-box-to-dinner. At $39.99 it is the cheapest Palm polo."),
 "p28": ("Palm Golf Co.", "Make it a Double Tee", "$39.99", "make-it-a-double",
   "A tee for the double bogey or the double at the 19th hole, in Palm's brushed premium blend."),
 "p29": ("Palm Golf Co.", "Cart Cruisin' T-Shirt", "$39.99", "cart-cruisin-t-shirt-tan",
   "Tan, brushed for a flannel-soft feel, with the golf cart on the back."),
 "p30": ("Palm Golf Co.", "Coast to Coast T-Shirt", "$39.99", "coast-to-coast-t-shirt-cream",
   "Named, in Palm's words, for the founders' trip from East to West. Palm suggests wearing it to your favourite muni without a dress code."),
 "p31": ("Palm Golf Co.", "Wanderer Caddie Towel", "$39.99", "wanderer-caddie-towel",
   "An oversized ribbed cotton caddie towel in sage with the palm script, for golfers who still clean their grooves."),
 "p32": ("Palm Golf Co.", "Out of Bounds Towel", "$39.99", "out-of-bounds-towel",
   "Rugged suede printed with a topo map, big enough for golf but made to roll up for camping too."),
 "p33": ("Palm Golf Co. x Surfside", "Golf Towel", "$29.99", "surfside-x-palm-golf-towel",
   "A waffle-knit towel with a carabiner from the collaboration with Surfside, the canned-cocktail brand."),
 "p34": ("Palm Golf Co.", "Divot Repair Tool (Bottle Opener)", "$11.99", "divot-repair-tool-bottle-opener-silver",
   "A hand-drawn U-shape that rests your club off the wet grass, with a bottle opener built in."),
 "p35": ("Palm Golf Co.", "2-Pack Coasters", "$24.99", "2-pack-coasters",
   "American-made leather coasters with the debossed Palm logo, in brown or black."),
 "p36": ("Palm Golf Co.", "Ball Marker, Skull", "$2.99", "glove-magnet-skull",
   "The magnetic marker that clips into the Ball Marker Glove. At $2.99, buy a few."),
 "p37": ("REEF x Palm Golf Co.", "Dangerous Rips G-Papi", "$130", "palm-x-g-papi",
   "REEF's spikeless G-Papi golf shoe with &ldquo;Swing at your own risk&rdquo; on the sole and nitro-infused cushioning. It comes with a limited REEF x Palm keychain float."),
 "p38": ("Palm Golf Co. x Precision Pro", "Titan Elite Rangefinder", "$399.99", "titan-elite-rangefinder",
   "Precision Pro's Titan Elite in Palm colours: slope, GPS front-centre-back numbers in the viewfinder, a magnetic mount and 6x magnification to 400 yards."),
}
SECTIONS = [
 ("The Gloves", "gloves", ["p01","p02","p03","p04","p05","p06","p07"],
  "<strong>Seven gloves &middot; $27.99, or three for $69</strong>Gloves are where Palm started and still the reason most people find it. Every one is white AAA cabretta leather with a patterned tab, which is the whole idea: a premium player's glove with a bit of character that goes with whatever you are wearing. MyGolfSpy called it among the most comfortable gloves it tested."),
 ("The Headcovers", "headcovers", ["p08","p09","p10","p11","p12","p13","p14","p15","p16","p17","p18"],
  "<strong>Eleven covers &middot; $89.99</strong>Headcovers are now the deepest part of the range, with more than forty in stock. They are made in the USA with a weather-resistant DRYTEX shell and a sherpa lining, and the newest batch dropped on 30 September."),
 ("The Caps", "caps", ["p19","p20","p21","p22","p23"],
  "<strong>Five caps &middot; $34.99&ndash;$44.99</strong>Ghaul's test for Palm headwear is that it does not scream golf. The Lazy Palm is the dad hat, the rest are performance snapbacks built for a hot round."),
 ("Apparel", "apparel", ["p24","p25","p26","p27","p28","p29","p30"],
  "<strong>Seven pieces &middot; $39.99&ndash;$79.99</strong>Hoodies, two polos and the brushed graphic tees, with the inside jokes on the back: the double bogey, the golf cart and the trip from New Jersey to California."),
 ("Towels and Small Things", "accessories", ["p31","p32","p33","p34","p35","p36"],
  "<strong>Six pieces &middot; $2.99&ndash;$39.99</strong>Towels for the bag and the campsite, a divot tool that opens a beer, leather coasters and the $2.99 magnetic markers."),
 ("The Collabs", "collabs", ["p37","p38"],
  "<strong>Two collaborations &middot; $130&ndash;$399.99</strong>Palm's two biggest partnerships this year: a REEF golf shoe that matches the Dangerous Rips covers, and a Precision Pro rangefinder in Palm colours."),
]
N = 38
PQ = {
 "gloves": ("Well, we both suck at golf. So what is something that&rsquo;s neglected?", "Dustin Ghaul, Palm co-founder, to MyGolfSpy, 2025"),
 "caps": ("If you look at something like our headwear, it doesn&rsquo;t scream golf, which is unique.", "Dustin Ghaul, to MyGolfSpy, 2025"),
 "apparel": ("We&rsquo;re not tucked-in country club guys and we&rsquo;re also not out there with inappropriate course attire.", "Joe Ciafardoni, Palm co-founder, to MyGolfSpy, 2025"),
}
BANDS = {
 "headcovers": ("Swing and smile", "Palm's own shots, from the glove that started it.", [("band-p01-3","A Palm Barrels and Birdies glove on a golfer's hand at the course","The original glove"),("band-p05-1","A golfer in a Palm cap and Sea Isle glove","Sea Isle"),("band-p04-3","A Palm Hula glove gripping a club","Hula")]),
 "apparel": ("Built for the course, worn everywhere", "", [("band-p19-3","A woman in a Palm Lazy Palm cap and sunglasses","Lazy Palm"),("band-p21-3","A golfer in a Palm snapback at his bag","On the bag"),("band-p23-1","Palm caps on the sand at the beach","From the sand")]),
 "accessories": ("Huntington Beach, by way of the muni", "", [("band-p29-2","A golfer in the Palm Cart Cruisin' tee walking with his bag","Cart Cruisin'"),("band-p33-1","A golfer carrying the Surfside x Palm towel","The Surfside towel"),("band-p34-3","Opening a bottle with the Palm divot tool","Divot tool, bottle opener")]),
 "collabs": ("Swing at your own risk", "The REEF x Palm G-Papi.", [("band-p37-2","The REEF x Palm G-Papi sole reading Swing at your own risk","The sole"),("band-p37-4","A golfer in the REEF x Palm G-Papi on the green","On the green"),("band-p37-3","The REEF x Palm G-Papi at address","At address")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Palm makes the best-looking glove you can buy for under $30, and it has quietly turned that glove into one of the most likeable brands in golf. The idea is simple and still rare: a proper AAA cabretta player's glove with a patterned tab, so the one piece of kit every golfer touches on every shot finally has some character.</p>
    <p>Three friends from New Jersey started it. Dustin Ghaul, Justin Junior and Joe Ciafardoni moved to Southern California after college and met playing Costa Mesa Country Club, a muni near Huntington Beach. Around 2015 those rounds turned into plans for a golf company, a Kickstarter funded in under three days, and the first gloves shipped in 2017. The three of them still run it, with family and friends helping out.</p>
    <p>Since then Palm has grown into USA-made headcovers, caps, hoodies and towels, plus collaborations with REEF, Surfside and Precision Pro, all under the same motto: swing and smile. It is surf-town golf without the attitude, the brand for the player who shows up to the muni in a good hoodie and laughs off the double. Prices were read on Palm's own store on 2 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Huntington Beach, California</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Dustin Ghaul, Justin Junior, Joe Ciafardoni</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>First gloves shipped 2017</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Patterned-tab cabretta gloves</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$2.99&ndash;$399.99</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Barrels and Birdies Glove, $27.99</span></div>
      <a href="https://palmgolfco.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Palm Golf Co. &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#PalmGolf</span>
        <span class="hashtag">#SwingAndSmile</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfGloves</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Palm Golf Co. from?", "Huntington Beach, California. The three founders are from New Jersey and met playing Costa Mesa Country Club, a municipal course in Orange County."),
 ("Are Palm golf gloves good?", "Yes. They are AAA cabretta leather and USGA conforming, and MyGolfSpy called the Palm glove among the most comfortable it tested. They cost $27.99 each or three for $69 as of 2 October 2026."),
 ("Where are Palm headcovers made?", "In the USA. They have a weather-resistant DRYTEX shell and a sherpa lining, and several styles are made to order in 7 to 10 business days."),
 ("What does swing and smile mean?", "It is Palm's motto: golf is meant to be fun, whether you make a birdie or a double bogey."),
 ("Who makes the Palm golf shoe?", "REEF. The Dangerous Rips G-Papi is a REEF x Palm collaboration, a spikeless golf shoe that sells for $130."),
]
FRN = json.loads((ROOT / "research/palm/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = f"https://palmgolfco.com/products/{handle}"
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
            items.append({"@type": "ListItem", "position": pos, "url": f"https://palmgolfco.com/products/{P[h][3]}", "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-02", "dateModified": "2026-10-02",
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
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
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
    <span>Huntington Beach, California</span><span class="dot"></span>
    <span>38 picks &middot; in stock 2 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Palm Golf Co.: a golfer in a Palm glove on the tee, a woman in a Lazy Palm cap, and the REEF x Palm G-Papi shoe on the grass" fetchpriority="high" /></div></div>
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
