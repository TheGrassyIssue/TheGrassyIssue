#!/usr/bin/env python3
"""build-radmor-btk.py — Brand to Know: Radmor. 3 November 2026. Cloned from build-vest-edit.py.
Lenny: "Let's do a brand to know - Radmor" -> options sheet (44) -> "looks great, let's add some accessories they have a nice collection".
54 cards: 33 apparel from the sheet (Ellis short dropped for rows of 3), 9 headcovers, 12 caps and accessories.
FACTS: radmorgolf.com products.json (USD, Nov 3 2026); founders/story from Colorado AvidGolfer (Tony Dear, May 2022),
SI (Alex Miceli, Nov 2022, Morrison quote), Wikipedia (Scott Morrison: Paper Denim & Cloth 1999, Ernest Sewn).
Cardigan's AI-generated product image excluded. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Radmor, the Seattle Golf Brand With No Virgin Polyester"
DESC = ("Radmor is a Seattle golf brand from two former University of Washington teammates: knit polos, merino and cashmere sweaters, "
        "a new rain suit and leather BobRad headcovers. 54 picks in stock, in US dollars.")
H1 = "Brand to Know: Radmor"
BC = "Brand to Know: Radmor"
SLUG = "brand-to-know-radmor"
IMG = "/images/radmor"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "2": ("Radmor", "Taylor Recycled RG Micro Dot Polo", "$115", U("radmorgolf.com","products-taylor-radcycled-micro-dot-polo"),
   "A white polo with a navy micro dot and contrast collar, which Radmor calls its most technical take on performance. Recycled fibers, lightweight and quick to dry."),
 "13": ("Radmor", "Hudson Recycled Script Polo", "$115", U("radmorgolf.com","hudson-recycled-script-polo"),
   "One of Radmor&rsquo;s most versatile performance polos, with a small script detail that is easy to miss and nice when you notice it."),
 "14": ("Radmor", "Taylor Trellis Polo", "$115", U("radmorgolf.com","taylor-radcycled-trellis-polo"),
   "A refined geometric trellis pattern borrowed from classic menswear, on the recycled Taylor body."),
 "22": ("Radmor", "Taylor Recycled Arc Polo", "$115", U("radmorgolf.com","taylor-recycled-arc-polo"),
   "A plum polo with a graphic arc pattern. Radmor&rsquo;s line on it: designed to stand out without trying too hard."),
 "23": ("Radmor", "Taylor Recycled Gatsby Polo", "$115", U("radmorgolf.com","taylor-recycled-gatsby-polo"),
   "A deco-inspired print in slate blue on the recycled Taylor polo. Pair it with the Ellis shorts in spring or the Five-O pant now."),
 "42": ("Radmor", "Hudson Heritage Stripe 2.0 Polo", "$115", U("radmorgolf.com","hudson-recycled-heritage-stripe-2-0-polo"),
   "A vintage stripe in claret and dark navy. The quietest polo in the post, and maybe the best one."),
 "41": ("Radmor", "Charles Long Sleeve Pique", "$135", U("radmorgolf.com","charles-long-sleeve-pique"),
   "A long-sleeve pique for the days a short sleeve is not enough and a sweater is too much. Simple on purpose."),
 "27": ("Radmor", "Bauhaus x RADMOR &lsquo;Two Sleeves&rsquo; Stretch Tee", "$62", U("radmorgolf.com","bauhaus-x-radmor-two-sleeves-stretch-tee"),
   "A limited tee made with Bauhaus on Radmor&rsquo;s Peruvian Pima stretch body. Soft enough to sleep in, sharp enough to wear to the course."),
 "28": ("Radmor", "Bauhaus x RADMOR &lsquo;Target Golf&rsquo; Stretch Tee", "$62", U("radmorgolf.com","bauhaus-x-radmor-target-golf-stretch-tee"),
   "The second Bauhaus tee, with a target-and-hole graphic on the front. Same Pima stretch, same limited run."),
 "6": ("Radmor", "Whitman Long Sleeve Knit Polo", "$225", U("radmorgolf.com","radmerino-long-sleeve-polo"),
   "A long-sleeve pocket polo in fine knit, made with natural fibers. The piece that makes the whole post look expensive."),
 "11": ("Radmor", "Langley Jacquard Knit Polo", "$155", U("radmorgolf.com","langley-jacquard-knit-polo"),
   "A textured jacquard knit polo in soft blue. Radmor built it around texture, and it shows up even in photos."),
 "12": ("Radmor", "Whitman Knit Polo", "$165", U("radmorgolf.com","whitman-knit-polo"),
   "A snow white knit polo with fine stripes and a dark collar tip. Made for a late tee time and drinks after."),
 "37": ("Radmor", "Inness Knit Polo", "$145", U("radmorgolf.com","inness-knit-polo"),
   "Radmor&rsquo;s nod to the 3D knit sweaters of the 1990s, which it calls &ldquo;pixelated opulence.&rdquo; The boldest knit here."),
 "65": ("Radmor", "Ethan Johnny Collar Knit Polo", "$145", U("radmorgolf.com","ethan-knit-polo"),
   "A lightweight sweater polo with a modern Johnny collar in sky blue. Clean, simple and easy to dress up."),
 "142": ("Radmor", "RADMerino Ribbed Knit Polo", "$165", U("radmorgolf.com","radmerino-cashemere-blend-short-sleeve-ribbed-sweater-knit-polo-1"),
   "A short-sleeve ribbed sweater polo in Radmor&rsquo;s merino and cashmere blend. Light enough for fall rounds in Austin."),
 "146": ("Radmor", "Union Recycled Rib Knit Polo", "$135", U("radmorgolf.com","union-recycled-rib-knit-polo"),
   "A rib knit polo with tipping at the collar and sleeves. Athletic, clean and built to wear well past the 18th."),
 "64": ("Radmor", "Luca Rib Knit Camp Shirt", "$145", U("radmorgolf.com","luca-rib-camp-shirt"),
   "Half lightweight sweater, half camp shirt, in a cream rib knit with fine stripes. The most different shirt in the collection."),
 "96": ("Radmor", "RADMerino Cashmere Blend Cardigan", "$225", U("radmorgolf.com","radmerino-cashmere-blend-button-cardigan-sweater-dark-chateau"),
   "A button cardigan cut like a sweater polo, in Radmor&rsquo;s merino and cashmere blend. Light, soft and made to move."),
 "5": ("Radmor", "RADMerino Cashmere Blend Turtleneck", "$225", U("radmorgolf.com","radmerino-cashmere-blend-turtleneck"),
   "A fine-knit turtleneck in the merino and cashmere blend. Radmor calls it a study in quiet confidence; we call it the winter round uniform."),
 "136": ("Radmor", "RADMerino Cashmere Blend Crew", "$225", U("radmorgolf.com","radmerino-cashmere-blend-sweater-crew"),
   "A navy crew sweater in the same blend, built on the idea that a golf sweater should work at dinner too."),
 "61": ("Radmor", "Enzo Knit Zip Bomber", "$225", U("radmorgolf.com","enzo-knit-zip-bomber"),
   "A classic bomber rebuilt in knit, in a soft sage. Warmer than it looks, and it does not rustle at the top of your backswing."),
 "3": ("Radmor", "Hudson Performance Hoodie", "$135", U("radmorgolf.com","hudson-performance-hoodie"),
   "The Hudson polo fabric cut into a hoodie, in navy or slate blue. A range-session layer that still looks put together."),
 "15": ("Radmor", "Colton Interlock Rib Quarter-Zip", "$135", U("radmorgolf.com","colton-interlock-rib-quarter-1-4-zip"),
   "A clean interlock rib quarter-zip in olive. Radmor&rsquo;s everyday performance layer."),
 "63": ("Radmor", "Dylan Quarter-Zip", "$145", U("radmorgolf.com","dylan-quarter-zip"),
   "The cool-weather follow-up to the Colton, with more warmth for fall and winter rounds."),
 "128": ("Radmor", "Perkins 2.0 Crew Sweatshirt", "$125", U("radmorgolf.com","perkins-2-0-crew"),
   "A lightweight everyday crew in claret, made for the course and well beyond it."),
 "121": ("Radmor", "Anderson Hybrid Performance Vest", "$175", U("radmorgolf.com","anderson-hybrid-performance-vest"),
   "A three-season vest in recycled nylon and elastane with recycled bottle insulation. Quilted front, stretch back."),
 "127": ("Radmor", "Anderson Hybrid Performance Jacket", "$225", U("radmorgolf.com","anderson-hybrid-performance-jacket"),
   "The sleeved version of the Anderson: light recycled insulation, stretch where you swing."),
 "0": ("Radmor", "TINDALL 2.0 Rain Jacket", "$395", U("radmorgolf.com","tindall-2-0-jacket"),
   "Radmor&rsquo;s new rain jacket, written by people who learned golf in Seattle: rain is part of the game. The top of the line here."),
 "1": ("Radmor", "TINDALL 2.0 Rain Pant", "$295", U("radmorgolf.com","tindall-2-0-pant"),
   "The matching rain pant, cut to pull on over trousers when the weather turns mid-round."),
 "44": ("Radmor", "Team Varsity Jacket", "$295", U("radmorgolf.com","pro-team-varsity-jacket"),
   "Radmor&rsquo;s take on the American letterman, in black with cream sleeves. Not for the course, and that is fine."),
 "129": ("Radmor", "Moscrip Jacket", "$225", U("radmorgolf.com","moscrip-jacket"),
   "A lightweight, weather-resistant jacket in recycled nylon and elastane with four-way stretch. The everyday shell."),
 "67": ("Radmor", "Ellis Recycled Performance Pant", "$142", U("radmorgolf.com","ellis-performance-pant"),
   "A fuller-leg performance pant with a relaxed, clean line, in chateau, navy or alloy."),
 "115": ("Radmor", "Five-O Knit Pant", "$142", U("radmorgolf.com","five-o-knit-pant"),
   "A five-pocket pant in a soft performance knit. Looks like chinos, feels like joggers."),
 "72": ("Radmor", "Golf Needle + 12th Man Driver Headcover", "$95", U("radmorgolf.com","radmor-golf-needle-12th-man-hawks-edition-leather-headcover-driver-white-navy-electric-green"),
   "A leather driver cover made with Golf Needle in navy and electric green, a nod to Seattle football&rsquo;s 12th Man."),
 "139": ("Radmor", "Dancing BobRad Barrel Hybrid Headcover", "$95", U("radmorgolf.com","dancing-bobrad-barrel-headcover-hybrid"),
   "A 1990s-style barrel cover in natural leather, with BobRad, the brand&rsquo;s dancing mascot, in black or white."),
 "143": ("Radmor", "Dancing BobRad Leather Blade Putter Cover", "$90", U("radmorgolf.com","dancing-bobrad-leather-blade-plutter-headcover"),
   "The blade putter version, with BobRad dancing across white or black leather."),
 "140": ("Radmor", "Tour Edition Leather Blade Putter Cover", "$95", U("radmorgolf.com","tour-edition-bobrad-leather-blade-headcover-putter"),
   "Hand-crafted natural leather, treated for water and stains, in black with white or white with black."),
 "77": ("Radmor", "&lsquo;Pop-Art&rsquo; Leather Blade Putter Cover", "$78.50 (sale; $95)", U("radmorgolf.com","dancing-bobrad-leather-blade-headcover-putter-black-copy"),
   "A comic-book Pop-Art print on vegan leather. The loudest thing Radmor makes."),
 "98": ("Radmor", "&lsquo;Pop-Art&rsquo; Leather Driver Headcover", "$78.50 (sale; $95)", U("radmorgolf.com","radmor-script-leather-headcover-driver-black-yellow-copy"),
   "The same Pop-Art panels on a driver cover. Buy both if you are going to commit."),
 "86": ("Radmor", "&lsquo;Patriot DC&rsquo; Leather Driver Headcover", "$95", U("radmorgolf.com","patriot-dc-leather-headcover-driver-white-red-navy"),
   "White leather in red and navy with the DC, Radmor&rsquo;s &ldquo;Dead Center&rdquo; logo."),
 "97": ("Radmor", "RADMOR Script Bethpage Driver Headcover", "$78.50 (sale; $95)", U("radmorgolf.com","radmor-script-bethpage-leather-headcover-driver-white-red-navy"),
   "Red script on white leather with navy trim, a Bethpage-style colorway."),
 "144": ("Radmor", "RADMOR Script Leather Driver Headcover", "$78.50 (sale; $95)", U("radmorgolf.com","radmor-script-leather-headcover-driver"),
   "The script cover in white, navy, black or yellow. Natural leather, handcrafted."),
 "24": ("Radmor", "Corduroy Office Cap", "$40", U("radmorgolf.com","corduroy-script-cap-copy"),
   "Corduroy, a six-panel cap and simple type on the front, in black, white, green or navy."),
 "45": ("Radmor", "Meridian Tech RadCap", "$38", U("radmorgolf.com","meridian-tech-radcap"),
   "Radmor&rsquo;s lightest hat, with micro perforations for airflow. The one for hot days."),
 "123": ("Radmor", "B-Rad Multicam RADCap", "$40", U("radmorgolf.com","b-rad-multicam-radcap"),
   "A limited cap in Multicam or Multicam Black, for the golfer who spends as much time outdoors off the course."),
 "90": ("Radmor", "RAD Patch 5 Panel Roper", "$40", U("radmorgolf.com","copy-of-attack-mode-snap-back-snow-white-blue-graphite"),
   "A cotton twill five-panel snapback with a rope across the front and a round RAD patch."),
 "135": ("Radmor", "RADMerino Cashmere Blend Beanie", "$68", U("radmorgolf.com","radmerino-cashmere-blend-knit-beanie"),
   "A light rib knit in 90 percent merino and 10 percent cashmere, the same yarns as the sweaters. Navy or gray."),
 "71": ("Radmor", "Blaine Leather Belt", "$75", U("radmorgolf.com","blaine-b-rad-leather-belt-1"),
   "Vegetable-tanned leather in black, cognac or navy. Simple, and it will age well."),
 "113": ("Radmor", "Harrison Reversible Belt", "$75", U("radmorgolf.com","harrison-reversible-belt"),
   "A reversible vegetable-tanned leather belt: two belts for the price of one."),
 "43": ("Radmor", "RADMOR x Weatherman 66in Golf Umbrella", "$85", U("radmorgolf.com","radmor-x-weatherman-golf-umbrella"),
   "A 66-inch Weatherman umbrella in black or white with the DC logo. Seattle golfers know when you need one."),
 "82": ("Radmor", "Leather Mini-Blade Putter Cover Keychain", "$30", U("radmorgolf.com","leather-bobrad-keychain"),
   "A tiny leather blade putter cover on a keyring, with BobRad stitched across the top."),
 "103": ("Radmor", "Stainless Enamel BobRad Keychain", "$22", U("radmorgolf.com","stainless-enamel-bobrad-keychain-white-black"),
   "Stainless steel and enamel, in a recycled velvet pouch. A stocking stuffer for your golf group."),
 "99": ("Radmor", "RADSOCK Crew Socks, Clay/Multi (2-Pack)", "$28 (sale; $38)", U("radmorgolf.com","radsock-clay-multi-2-pack"),
   "Crew socks in cellulose, recycled nylon and elastane: one white Radmor pair and one in clay and multi."),
 "91": ("Radmor", "RAD-Mat Limited Edition Slipmat, BobRad", "$18", U("radmorgolf.com","rad-mat-limited-edition-logo-slipmat-bobrad-large-pixel"),
   "A felt record slipmat with a pixelated BobRad, for the turntable at home. Proof Radmor is about more than golf."),
}
SECTIONS = [
 ("Polos &amp; Tees", "polos", ["2","13","14","22","23","42","41","27","28"],
  "<strong>Recycled performance, Pima stretch</strong>The Taylor and Hudson polos are Radmor&rsquo;s core: recycled fibers, clean patterns and a fit that works on and off the course. The Bauhaus tees are the fun part."),
 ("Knit Polos", "knits", ["6","11","12","37","65","142","146","64","96"],
  "<strong>Where Radmor is different</strong>Fine knits, jacquards and a merino and cashmere blend. Few golf brands make this many knit polos, and they are the reason to know this one."),
 ("Sweaters &amp; Layers", "layers", ["5","136","61","3","15","63","128","121","127"],
  "<strong>For the Pacific Northwest, and everywhere else in November</strong>RADMerino sweaters, knit bombers, quarter-zips and hybrid insulation."),
 ("Outerwear &amp; Pants", "outerwear", ["0","1","129","44","67","115"],
  "<strong>Built for rain</strong>The new TINDALL 2.0 rain suit leads, written by golfers who learned the game in Seattle weather."),
 ("Headcovers", "headcovers", ["72","139","143","140","77","98","86","97","144"],
  "<strong>Leather, BobRad and Pop-Art</strong>Handcrafted leather covers with the brand&rsquo;s dancing mascot, a comic-book print and a Golf Needle collab for Seattle."),
 ("Caps &amp; Accessories", "accessories", ["24","45","123","90","135","71","113","43","82","103","99","91"],
  "<strong>The small stuff</strong>Caps, a cashmere beanie, vegetable-tanned belts, a Weatherman umbrella, keychains, socks and a record slipmat."),
]
N = 54
PAIRS = {}
BANDS = {
 "layers": ("On the course", "Knits worn the way Radmor shoots them, from the coast to the desert.",
   [("band-1-1","A man in a Radmor Luca rib knit camp shirt","Radmor"),
    ("band-1-2","A man in a Radmor Ethan knit polo","Radmor"),
    ("band-1-3","A golfer in a Radmor Dylan quarter-zip","Radmor")]),
 "headcovers": ("Off the rack", "Pop-Art covers, a Meridian cap and a patch roper.",
   [("band-2-1","Radmor Pop-Art leather headcovers on clubs","Radmor"),
    ("band-2-2","A man in a navy Radmor Meridian tech cap","Radmor"),
    ("band-2-3","A young golfer in a Radmor RAD patch roper cap","Radmor")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Radmor is a Seattle golf brand started by Scott Morrison and Bob Conrad, who played on the University of Washington golf team together. The name is half of each of their last names. Morrison came from denim: he founded Paper Denim &amp; Cloth in 1999 and later Ernest Sewn, so he knew how clothes are made long before he made golf clothes.</p>
    <p><strong>The idea.</strong> Most golf clothing is polyester, which Conrad calls an oil-based plastic. Radmor set out to make performance golf clothes without virgin polyester: Peruvian Pima cotton, Tencel and other plant-based fibers, with only a small amount of recycled polyester or nylon where it is needed.</p>
    <p><strong>Why it stands out now.</strong> Look past the polos and Radmor has quietly become one of the best knitwear brands in golf. The Whitman, Langley and Inness knit polos, the RADMerino cashmere-blend sweaters and the Enzo knit bomber look like they belong in a menswear store, and they still move like golf clothes. Morrison put it simply: fall is right in Radmor&rsquo;s wheelhouse.</p>
    <p><strong>The fun side.</strong> Then there is BobRad, a dancing mascot that turns up on leather headcovers, keychains and a record slipmat, plus a comic-book Pop-Art headcover set, a Golf Needle collab for Seattle&rsquo;s 12th Man and two Bauhaus tees. The clothes are serious; the accessories are not.</p>
    <p><strong>Where to start.</strong> A Taylor polo is the easy entry at $115. If you want to see what Radmor does best, buy a knit polo. If you just want a little of the brand in your bag, the BobRad headcovers and the $22 keychain do the job.</p>
    <p><strong>What is in here.</strong> 54 pieces, all in stock on radmorgolf.com when we checked on November 3, 2026, in US dollars. A few headcovers and the socks were on sale; we list both prices.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>Seattle, early 2020s</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Scott Morrison, Bob Conrad</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>No virgin polyester; knit polos</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>54</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$18&ndash;$395</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Inness Knit Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#Radmor</span>
        <span class="hashtag">#SeattleGolf</span>
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
    <h2 class="products-hdr" id="last-word">Seattle, in Knit</h2>
    <p>Plenty of brands talk about sustainability. Radmor built its whole line around one rule, no virgin polyester, and then made the clothes good enough that you would buy them anyway. The knits are the proof.</p>
    <p>Radmor has turned up on TGI before, in our <a href="/drops/the-technical-brands-roundup">technical brands roundup</a> and <a href="/drops/the-summer-tee-edit">summer tee edit</a>. This is the first time we have given it the full page.</p>
  </div>
</section>
"""
HERO_ALT = "A golfer in a Radmor olive quarter-zip and navy pants standing on a green with the flag and sandy dunes behind him"
FRN = json.loads((ROOT / "research/radmor/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-RAD-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    for s in SECTIONS: assert len(s[2]) % 3 == 0, s[0]
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
    <span>Brand to Know &middot; Seattle, WA</span><span class="dot"></span>
    <span>54 picks &middot; in stock, checked November 3, 2026</span>
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
    for leak in ("Mackem", "Vest Edit"):
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
