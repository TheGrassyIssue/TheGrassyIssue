"""build-gift-guide-1.py — 2026 Holiday Gift Guide, Part 1 of 3 (9 November 2026). Cloned from build-hidden-details.py.
Lenny: 12 gifts per category, a good write-up for each category, no brand repeated in the post, prioritize brands that sent us product.
Categories: The Everyday Item as Well Done as Possible / For the Range Rat / Small Enough for a Stocking. Lenny swapped C12 (Chipp dryer) for
Puttwell disks and C4 (Odd Ritual) for Sentinel socks. FACTS: product pages, read November 9, 2026. Prices as shown to a US visitor in Chrome.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "The 2026 Golf Gift Guide, Part 1: Everyday Upgrades, Range Rat Gifts and Stocking Stuffers"
DESC = ("36 golf gifts from 36 independent brands: everyday kit made as well as it can be, gifts for the golfer who lives at the range, "
        "and small things for a stocking, from $9 to $300.")
H1 = "The 2026 Golf Gift Guide, Part 1: Everyday Upgrades, Range Rat Gifts and Stocking Stuffers"
BC = "Gift Guide 2026, Part 1"
SLUG = "golf-gift-guide-2026-everyday-range-rat-stocking-stuffers"
IMG = "/images/gift-guide-1"
U = lambda d, h: f"https://{d}/products/{h}"
GIFTED = {"tt","dv","aw","bl","ab","lz","sh","fe","tp","hb","cm","ta","bb","ap","hl"}
P = {
 "tt": ("TOTEM", "Divot Tool, Brass", "$80", U("totem.golf","divot-repair-tool-1pcs"),
   "Machined, balanced by hand and finished in brass that takes on a patina the more it gets used. It comes on a paracord loop with its own carry case. We named TOTEM our top pick in <a href=\"/drops/7-divot-tools-actually-worth-carrying\">our divot tool roundup</a>, and nothing since has changed our mind."),
 "dv": ("DRVN Golf Co.", "MM-722 Ball Marker", "$75 (was $85)", U("drvngolfco.com","mm-722-ball-marker"),
   "Milled from 303 stainless steel in the shape of the multi-spoke wheel from the McLaren SLR 722. A marker for the friend who knows his supercars as well as his putting line. One left at this price when we checked."),
 "aw": ("Agronomy Workshop", "Spiritual Approach Towel, Aura", "$56", "https://agronomywork.shop/store/spiritual-approach-towel-copy",
   "Woven terry cotton, extra absorbent, printed like a late-night TV ad for &ldquo;alignment consultations&rdquo; that, the towel admits, do not guarantee success. The best joke in the bag, and a very good towel."),
 "bl": ("BLURRD", "Heritage Collection Glove, Churchill 2-Pack", "$65", U("blurrdgoods.com","the-heritage-collection-churchill-2-pack"),
   "Two gloves in AAA Cabretta leather, one in each colorway: tan with burgundy, burgundy with tan. Ultra-thin, with a two-row elastic cuff and a reinforced thumb. The glove is the thing everyone wears out; this is the one to wear out."),
 "ab": ("Aberdeen West", "Checker Crew Sock, Navy", "$28", U("aberdeenwest.com","navy-checker-crew-sock"),
   "A navy checkerboard crew with embroidered artwork, one size fits most. Socks are the most-worn gift on this list, so they may as well be good ones."),
 "lz": ("Lazyface", "Facescreen", "$35", U("lazyface.com","facescreen"),
   "Mineral sunscreen from Dr. Steven Kent, who wanted something he would recommend to a patient without the department-store price. Streak-free and no white cast, which means it actually gets used before a round."),
 "se": ("Seamus Golf", "Navy Harris Tweed Scorecard Holder", "$93", U("www.seamusgolf.com","navy-harris-tweed-scorecard-holder"),
   "Harris Tweed outside, toffee leather inside, made in Beaverton, Oregon. Folds to 4.5 x 6.5 inches for a back pocket, takes a standard 5.75-inch card and now has a pencil holder built in."),
 "co": ("Clint Orms", "Ball Marker 1802, Sterling Silver", "$300", U("clintorms.com","ball-marker-1802"),
   "Made and engraved by hand in Texas by Clint Orms Engravers &amp; Silversmiths: an American flag on one side, scroll engraving on the other. Because each one is cut by hand, no two patterns match. The one gift here that gets handed down."),
 "wg": ("Woodgrain Golf", "The Signature Belt", "$130", U("woodgrain.golf","the-signature-belt"),
   "Genuine leather in a black crocodile-embossed finish with polished hardware. Classic enough for tailored trousers off the course, which is where a belt like this earns its keep."),
 "wk": ("Walker Golf Things", "Canvas Rangefinder Bag, Forest", "$49 (was $70)", U("walkergolfthings.com","canvas-rangefinder-bag-forest"),
   "Heavyweight cotton canvas with a padded, embossed lining, a fold-over flap with a metal snap, a detachable rope sling and a carabiner. Wear it across your body or clip it to the bag."),
 "hs": ("Hudson Sutler", "Heritage Waxed Canvas Pouch", "$72", U("hudsonsutler.com","heritage-waxed-canvas-pouch"),
   "Handmade from 18-oz water-repellent waxed canvas with a full-grain leather bottom and an interior divider. Keys, wallet, phone and markers go in; the pouch goes in the bag. It also works on a plane."),
 "cb": ("Charleston Belt", "Golf Cart Needlepoint Key Fob, Red", "$35", "https://charlestonbelt.com/products/key-fob-golf-cart-red-hand-stitched-needlepoint",
   "Top-grain leather with hand-stitched needlepoint golf carts and a solid D ring. Something golf-related they will carry every day of the year, not just on Saturdays."),
 "sh": ("SAHA", "Clip Towel", "$45", U("saha.golf","saha-clip-towel"),
   "A clean towel with a metal eyelet and a carabiner, so it clips onto the bag and stays there. Navy or green, with a small Saha.Golf logo."),
 "fe": ("Fella Golf", "Stretch-Fit Golf Glove", "$29", U("fellagolf.com","fella-stretch-fit-golf-glove"),
   "Soft PU leather with green lycra gussets between the fingers for stretch and airflow. One size, M/L, built to fit most hands. A range rat goes through gloves; give him a few."),
 "tp": ("Three Putt Golf Clothing", "Yardage Golf Cargo Trousers", "$69", U("threeputtgolfclothing.co.uk","yardage-golf-cargo-trousers"),
   "A relaxed 300gsm cotton cargo with front pleats, a straight leg and a pocket on each leg for the yardage book, the tees, the pitch-mark tool and the ball found in the rough. The store shows US prices."),
 "hb": ("Howie Benson", "Single Button Polo Pullover, Brown", "$118", U("howiebenson.com","single-button-pullover-brown"),
   "A midweight, textured stretch pullover with a single-button collar. Enough give to swing in, and it doesn&rsquo;t look like golf outerwear when he heads to dinner after the last bucket."),
 "cm": ("Communal", "C Patch Hat", "$60", U("communalmfg.com","c-patch-hat"),
   "Cotton twill with a big felt C on the front, in navy or cream. A range hat should be one you don&rsquo;t mind sweating through; this is the one he&rsquo;ll keep wearing after."),
 "ta": ("Tarraing", "The Douglas Puffer Vest, Navy", "$150", U("tarrainggolf.com","the-douglas"),
   "A quilted front for warmth, smooth stretch side and back panels so the swing isn&rsquo;t restricted, a stand collar and zippered hand pockets. The Highland Cow logo sits on the chest. Made for the first cold bucket of the year."),
 "cl": ("Clutch Golf Co.", "The Range Set: Hickory Alignment Sticks and Leather Cover", "$79.99 (was $94.98)", U("clutchgolfcompany.com","range-set-alignment-sticks-leather-cover"),
   "Two 42-inch hickory alignment sticks in one of 11 colorways, with a hand-cut, hand-stitched leather cover that has a window to show off the stripes. Handmade to order in the USA and ships in two to three business days."),
 "ed": ("Edel Golf", "Array Alignment Plates", "$45", U("edelgolf.com","array-alignment-plates"),
   "Interchangeable sight plates (blank, one line, two lines, three lines, three dots or a T-bar) for Edel&rsquo;s Array putters, so he can find the line that fits his eye. Only for the Array F-1, F-2 and F-3, so check his putter first."),
 "dd": ("Dimple &amp; Divot", "Hickory Golf Brush PRO Plus, Blue", "$65", U("dimpledivot.com","hickory-golf-brush-pro-hybrid-blue"),
   "An American hickory handle with nylon and metal bristles, a retractable tether that reaches up to 20 inches and a nickel trigger snap. Handcrafted in the USA, and the only brush they make with both bristle types."),
 "so": ("Shoal Golf Co.", "The Shoal Shag Bag", "$70", U("shoalgolfco.com","the-shoal-shag-bag"),
   "Waxed canvas with a drawstring top and a carry handle, holding around 60 to 65 balls. For the short-game area and the back of the cart, without the look of a mesh range bag."),
 "su": ("Sunday Golf", "Loma Par 3 Bag, Toasted Almond", "$130 (was $145)", U("sundaygolf.com","loma-toasted-almond-par-3-golf-bag"),
   "A single-strap stand bag for up to six clubs, with a two-way top divider, an insulated two-can cooler pocket and a velour-lined valuables pocket. Made for a range session, a par 3 or a quick nine."),
 "jo": ("Jones Sports Co.", "Original Jones Bag, Navy/White", "$111 (was $185)", "https://www.jonessportsco.com/products/original-jones-bag-navy-white",
   "The bag that started Jones in 1971, built for the walking golfer: water-resistant nylon, a single strap and an unstructured body with three pockets. On sale when we checked."),
 "bb": ("Birdie Balm", "The Original", "$18", U("birdiebalm.co","birdie-balm"),
   "Lip balm with a magnetic ball marker in the lid, so it is always in your pocket. Beeswax, coconut oil, cocoa butter and sweet almond oil, with a little tea tree and peppermint. Every marker reads &ldquo;Make This Putt.&rdquo;"),
 "ap": ("Apr&egrave;s-Golf", "WARNING: Habit-Forming Premium Golf Tees", "$9", U("apresgolf.com","warning-habit-forming-premium-golf-tees"),
   "Twenty tees in a pack that looks like a pack of smokes, with a warning that side effects may include enjoying your round. Under ten dollars and guaranteed to get a laugh on the first tee."),
 "hl": ("Hidden Links Society", "Stencil Series Ball Marker, Aged Brass", "$20", U("hiddenlinkssociety.com","stencil-collection-ball-marker-aged-brass"),
   "Aged brass, 1.25 inches across and an eighth of an inch thick, with double-sided raised engraving and knurled edges. Heavy enough to feel like something."),
 "sn": ("Sentinel Golf", "Cotton/Hemp Field Sock", "From $30", "https://www.sentinelgolf.us/shop/p/mwqw2hk7jsxug69d9fa1t1gk7kdu6e-jg7sw-kz2dg-ftpet-ajk8r-myp3l-hzctp-arh9m",
   "Made with KNITWIN, a Japanese mill founded in 1950 with a single hand-operated knitting machine. A 50/50 cotton-hemp yarn with a cushioned pile sole, in three colors or a three-pack. Fits men&rsquo;s 9 to 13."),
 "sb": ("Sinking Birdies", "Bogey Machine Divot Tool", "&pound;14 (~$19)", U("sinkingbirdies.co.uk","bogey-machine-divot-tool"),
   "A solid metal pitch-mark repairer from the UK, about 85 by 50 millimeters, shaped like a hippie van with &ldquo;Bogey Machine&rdquo; down the side. An upgrade on the plastic one that has been in the bag for years."),
 "pa": ("Pins &amp; Aces", "Ice Cubes Ball Marker", "$14.95", U("pinsandaces.com","ice-cubes-ball-marker"),
   "Cast stainless steel with oven-cured enamel: two ice cubes, for the golfer who orders a drink at the turn. Sticks to any magnetic hat clip or divot tool."),
 "ss": ("Scotch &amp; Skins", "Chestnut Leather Ball Marker", "$15", U("scotchandskins.com","ball-marker-1"),
   "North American leather from Wickett &amp; Craig, a tannery founded in 1867, with a metal insert for weight and gold-embossed alignment lines. Handcrafted in the USA."),
 "tr": ("3 Putt Round", "The Eucalyptus Scented Tee Pack", "&euro;12.90 (~$15)", U("3puttround.com","the-eucalyptus-scented-blue-tee-pack"),
   "Twenty-one bamboo tees, lightly scented with eucalyptus, in a pocket-sized pack. The brand pitches eucalyptus as the scent to reset after a bad shot. We can&rsquo;t promise that, but the tees smell great."),
 "sg": ("Sugarloaf Social Club", "SSC x Grooveit Mini Brush", "$30", U("sugarloafsocialclub.com","groove-it-brush"),
   "A smaller, water-free version of the Grooveit brush with the same heavy-duty nylon bristles and a magnetic clip. Small enough to live on the bag without anyone noticing."),
 "pg": ("Palm Golf Co.", "Men&rsquo;s Ball Marker Glove", "$27.99", U("palmgolfco.com","mens-mag-glove"),
   "An AAA Cabretta leather glove with a spot on the back that holds a ball marker. The markers are sold separately, from $3.99, so pair it with one of Palm&rsquo;s skulls or palm trees."),
 "vs": ("Vessel", "Magnetic Golf Towel, 5 x 5 in.", "$19", U("vesselgolf.com","magnetic-golf-towel-5-x-5"),
   "A pocket-size waffle microfiber towel that holds up to 400% of its weight in water, with a strap and magnet to clip it to a D ring or a club head. For the grooves, the ball and the sunglasses."),
 "pw": ("Puttwell Golf Club", "Putting Disks, 3-Pack", "$30", U("puttwellgolfclub.com","putting-disks"),
   "Three disks with light alignment markings to roll putts to on the practice green, plus a carabiner to clip them to the bag. A small, cheap way to work on pace, which is where most three-putts start."),
}
SECS = [
 ("everyday", "The Everyday Item as Well Done as Possible", "Kit they already use every round, made by someone who cared", ["tt","dv","aw","bl","ab","lz","se","co","wg","wk","hs","cb"],
  "The best gift is the thing they already use every round, made by someone who cared more than they had to. Nobody needs a new divot tool. Everybody notices when the one in their pocket is solid brass from TOTEM, or when the marker on the green is DRVN&rsquo;s MM-722 instead of a logo coin from a charity scramble. This category is the upgrade on autopilot: a Seamus scorecard holder in Harris Tweed, a Woodgrain belt in croc-embossed leather, an Agronomy Workshop towel in woven terry cotton, a needlepoint key fob from Charleston Belt. Nothing here changes how they play. All of it changes how the bag feels when they unzip it on the first tee."),
 ("range-rat", "For the Range Rat", "For the golfer who hits two buckets before a casual nine", ["cl","ed","dd","so","su","jo","ta","hb","tp","fe","sh","cm"],
  "Every group has one: the guy who hits two buckets before a casual nine and has opinions about mats versus grass. He does not want another sleeve of balls. He wants the range to feel less like a chore. That starts with Clutch&rsquo;s hickory alignment sticks in a leather cover, made to order, and Edel&rsquo;s alignment plates for the putting green. It continues with a Dimple &amp; Divot brush and a Shoal shag bag for the short-game area, then a Sunday Loma or the Original Jones for walking down to the far end with six clubs. The rest is about being out there in November: a Tarraing puffer vest, a Howie Benson pullover, Three Putt&rsquo;s cargo trousers, a fresh Fella glove, a SAHA towel and a Communal hat."),
 ("stocking", "Small Enough for a Stocking", "Small things people keep, from $9 to $30", ["bb","ap","hl","sn","sb","pa","ss","tr","sg","pg","vs","pw"],
  "Stocking stuffers are where golf gifts go to die, mostly as novelty tees and logo balls nobody plays. These are small things people keep. Birdie Balm, with a ball marker in the lid, for the back nine in December wind. Apr&egrave;s-Golf tees with a warning label and 3 Putt Round tees that smell like eucalyptus. Ball markers in aged brass from Hidden Links Society, leather from Scotch &amp; Skins and enamel from Pins &amp; Aces, plus a solid metal divot tool from Sinking Birdies in the UK. Sentinel&rsquo;s field socks are knit with KNITWIN, a Japanese mill founded in 1950. Rounding it out: a Sugarloaf mini brush, a Palm Golf glove with a spot for a marker, a pocket-size Vessel towel and a three-pack of Puttwell putting disks for pace work on the practice green."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 36
PAIRS = {}
BANDS = {
 "stocking": ("On the course", "The small stuff, in use", [("life-a-1","DRVN MM-722 ball markers lined up on a stone ledge","DRVN Golf Co."),("life-a-2","A brass TOTEM divot tool resting on dark foam","TOTEM"),("life-a-3","A leather Scotch &amp; Skins ball marker behind a ball near the hole","Scotch &amp; Skins"),("life-a-4","A van-shaped Sinking Birdies divot tool stuck in the grass","Sinking Birdies"),("life-a-5","A small brush cleaning the grooves of an iron","Sugarloaf Social Club"),("life-a-6","A canvas rangefinder bag lying on the grass","Walker Golf Things")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>This is the first of three gift guides we are publishing together this year, nine categories in all, twelve gifts in each. Part 1 covers the gifts that get used the most: everyday kit made as well as it can be, gifts for the golfer who lives at the range, and small things for a stocking. Every brand is independent, and no brand appears twice in this post, so the 36 gifts below come from 36 different makers.</p>
    <p>We kept the rule simple. If we wouldn&rsquo;t want it in our own bag, it isn&rsquo;t here. That ruled out most of what usually fills a golf gift guide: logo balls, gadget tees and anything that ends up in a drawer by February. What is left are things golfers keep: a brass divot tool, a sterling marker, a scorecard holder, a waxed canvas pouch, a hickory brush.</p>
    <p><strong>Where to start.</strong> For the everyday upgrade, the TOTEM brass divot tool, $80. For the range rat, Clutch&rsquo;s Range Set, $79.99. For the stocking, Birdie Balm, $18, which puts a ball marker in the lid of a lip balm and is the cleverest small gift we found this year.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Gifts</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$9&ndash;$300</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>TOTEM Brass Divot Tool</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfGiftGuide</span>
        <span class="hashtag">#GolfGifts</span>
        <span class="hashtag">#IndieGolf</span>
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
    <h2 class="products-hdr" id="last-word">Buy the Thing They Already Use</h2>
    <p>The golf gifts that last are almost never the clever ones. They are the ordinary things a golfer touches every round, made better than they had to be. A divot tool, a marker, a towel, a glove. Upgrade one of those and the person thinks of you every time they reach for it, which is eighteen times a round.</p>
    <p><strong>Know what they play.</strong> A few gifts here depend on the person. Edel&rsquo;s plates only fit Edel&rsquo;s Array putters. The Palm glove comes without its marker. Clutch makes the Range Set to order, so allow a few days on top of shipping. If you are not sure, the towels, socks, markers and tees fit everyone.</p>
    <p><strong>Order early.</strong> Small brands make small runs, and stock moves fast in December. DRVN&rsquo;s marker was down to one when we checked. If something here is the one, don&rsquo;t wait for the week before Christmas.</p>
    <p>Prices are as each store shows them to a US visitor. Sinking Birdies shows pounds and 3 Putt Round shows euros, so those dollar figures are approximate. Everything was in stock on November 9, 2026. Parts 2 and 3 cover the other six categories.</p>
  </div>
</section>
"""
HERO_ALT = "Three gifts: a brass TOTEM divot tool hanging on a wooden chair, a Jones carry bag lying on a links fairway, and a hand holding a tin of Birdie Balm on the course"
FRN = json.loads((ROOT / "research/gift-guide-2026/frames1.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
GTAG = ' <span style="font-family:var(--mono,monospace);font-size:9px;letter-spacing:.1em;text-transform:uppercase;border:1px solid currentColor;padding:1px 5px;margin-left:6px;opacity:.7">Gifted</span>'
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
         "url": URL, "image": og, "datePublished": "2026-11-09", "dateModified": "2026-11-09",
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


CBY = {s[0]: s for s in SECS}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    s = CBY[anchor]
    num = [x[0] for x in SECS].index(anchor) + 1
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} gifts</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;"><p style="margin:0 0 16px;">{s[4]}</p></div>\n'
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
    <span>The Guide &middot; Holiday Gift Guide 2026, Part 1 of 3</span><span class="dot"></span>
    <span>36 gifts from 36 brands &middot; in stock, checked November 9, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    if "end" in BANDS: body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Vest Edit", "Collab "):
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
