#!/usr/bin/env python3
"""build-small-things.py — Small Things, Big Impact: 25 palm-sized golf pieces.
8 October 2026. Lenny: "Let's do a small things with a big impact round up, use those items on the watch list and
then give me a solid list of options that fit in your palm but catch your friends eye." Picked "My 20 (Recommended)"
from small-things-options.html, then "use the totem divot tool" (1PCS Brass replaces Tag.01) and "Add some small
pouches for keeping the bag organized" (five pouches, brands not otherwise in the post).

FACTS: research/small-things/candidates.json + each product's own store page (.js), read 8 Oct 2026, all in stock.
Non-USD prices in store currency with an approximate dollar figure (CAD 0.72, GBP 1.34, EUR 1.16, AUD 0.66).
PHOTOS: brands' own store images, framed 1000x1250 by research/small-things/frame.py (frames.json), white studio
backgrounds softened by soften-product-frames.py. Hero: Provision Machining & Design's own photo.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "small-golf-accessories-small-things-big-impact"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/small-things"
FRN = {f"S{int(k):02d}": v for k, v in json.loads((ROOT / "research/small-things/frames.json").read_text()).items()}
DATE = "2026-10-08"

TITLE = "Small Golf Accessories: 25 Pocket Pieces That Get Noticed"
DESC = ("Small golf accessories that fit in your palm: ball markers, divot tools, brushes, tees, pouches and pocket "
        "pieces from 25 independent makers, with prices.")
H1 = "Small Things, Big Impact: 25 Golf Pieces That Fit in Your Palm"

# code -> (brand, item, price, url, copy)
P = {
 # Ball markers
 "S02": ("Birdie Balm", "The Original", "CA$22.99 (~$17)",
   "https://birdiebalm.co/products/birdie-balm",
   "A lip balm with a ball marker built into the lid. The marker says &ldquo;Make This Putt&rdquo; and sits on a strong magnet, the balm is an all-natural formula, and the whole thing is the size of a big coin. It is one of the cheapest things here and the one your playing partners will ask about first."),
 "S04": ("Fyfe Golf", "The Brave Copper Hand Forged Ball Marker", "&pound;25 (~$34)",
   "https://fyfegolf.com/products/the-brave-copper-hand-forged-ball-marker",
   'Fyfe has this one made by a swordsmith at a forge in Scotland, from the same shop that still makes battle swords by hand. It is copper, with the Lion Rampant and the Saltire on the front, and initials can be hand-stamped on the back. Ours in <a href="/drops/brand-to-know-fyfe-golf">the Fyfe Brand to Know</a>.'),
 "S06": ("Show Out Engraving", "Desert Roadrunner 30mm Copper Ball Marker", "$50",
   "https://showoutengraving.com/products/desert-roadrunner-ball-marker",
   "Show Out is an engraving shop in Gilbert, Arizona, and its roadrunner wears sunglasses. The marker is solid copper, 30mm across and 21 grams, laser-engraved and finished by hand, with a Southwestern pattern around the bird. Heavy enough to stay put on a windy green."),
 "S05": ("Clint Orms Engravers &amp; Silversmiths", "Ball Marker 1803, Engraved State of Texas", "$220",
   "https://clintorms.com/products/sterling-silver-custom-state-of-texas-ball-marker",
   'Clint Orms makes buckles in Kerrville, and this is the same hand engraving at coin size. It is sterling silver, with the State of Texas on one side and full scrollwork on the other, and because it is cut by hand no two are quite the same. The splurge on the list. More in <a href="/drops/texas-golf-brands-and-makers">our Texas makers guide</a>.'),
 "S10": ("Malbon Golf", "Nimbus Buckets Ball Marker", "$38",
   "https://malbon.com/products/nimbus-buckets-ball-marker-multi",
   'Malbon cut this one in the shape of its Nimbus cloud, in red and gold, with the Formula 1 Chinese Grand Prix mark on the back. It is stainless steel with the artwork debossed and filled with soft enamel on both sides, so it reads from across the green and the finish stands up to a season in your pocket. More Malbon in <a href="/drops/malbon-fall-2026-the-ironworks-collection">our Ironworks Collection post</a>.'),
 "S33": ("Smathers &amp; Branson", "Crossed Clubs Golf Ball Marker", "$22.50",
   "https://smathersandbranson.com/products/crossed-clubs-golf-ball-marker",
   "Smathers &amp; Branson is the needlepoint house, and this is its smallest golf piece: two crossed clubs stitched on Classic Navy. It is the marker that matches a needlepoint belt, and it reads as preppy from ten feet away."),
 # Divot and pitch tools
 "S01": ("TOTEM", "1PCS Divot Tool, Brass", "$80",
   "https://totem.golf/products/divot-repair-tool-1pcs",
   "TOTEM is a new name making what it calls high-end golf accessories, and this is its core piece. The tool is machined from one piece and balanced by hand, it hangs on a paracord loop, and it comes in an EDC case. Pick raw brass or black PVD and black, teal, red or sage cord. The brass will age with you."),
 "S07": ("Kraken Golf", "The Signet Stainless Steel Pitch Tool", "$109",
   "https://krakengolf.com/products/the-signet-stainless-steel-pitch-tool",
   "Kraken shaped this pitch tool like a signet ring. You slide it onto a finger to fix the mark, and the KRAKEN name is cut under the band in solid 303 stainless. It is the oddest object here and the one most likely to get passed around the group."),
 "S15": ("Edel Golf", "Fine Milled Repair Tool", "$45",
   "https://edelgolf.com/products/fine-milled-repair-tool",
   'Edel machines this from 303 stainless in Texas, fine-mills the face and finishes it by hand, then stamps it for free. It is 3.25 inches long and comes in a felt pouch. It was our pick in <a href="/drops/7-divot-tools-actually-worth-carrying">our divot tool guide</a>, and it still is.'),
 "S16": ("Provision Machining &amp; Design", "Copper Golf Divot Tool with Spade", "$39.99",
   "https://www.provisionmachiningdesign.com/products/copper-spade-golf-divot-tool",
   "Provision cuts this from solid copper on a CNC machine and fills an engraved spade with enamel. It is just over three inches long and weighs about two ounces, so it feels like a real object in the pocket, and the copper will patina the longer you carry it."),
 "S31": ("Hidden Links Society", "Single Prong Pitch Mark Tool, Aged Brass", "$47",
   "https://hiddenlinkssociety.com/products/single-prong-pitch-mark-tool-aged-brass",
   'Hidden Links makes this from a quarter-inch square brass bar, three and a half inches long, with a single prong, an aged finish and a small stamp. The product page sums it up as &ldquo;Fix your damn pitch marks!&rdquo; Ours in <a href="/drops/brand-to-know-hidden-links-society">the Hidden Links Society Brand to Know</a>.'),
 # Brushes and tees
 "S22": ("Gamut Golf", "WILCOX 10K Pocket Brush", "$48",
   "https://gamutgolf.com/products/wilcox-10k-pocket-brush",
   'Gamut asked a tour caddie what he wanted during a round, and the answer was a small brush that does its job. The 10K is solid ebony or green sandalwood with firm bristles cut short enough to reach into the grooves. Ours in <a href="/drops/brand-to-know-gamut-golf">the Gamut Brand to Know</a>.'),
 "S23": ("Dimple &amp; Divot", "Hickory Golf Brush Lite, Keeper", "$45",
   "https://dimpledivot.com/products/hickory-golf-brush-mini-grass",
   'The smallest, lightest brush Dimple &amp; Divot makes: a short American hickory handle, firm nylon bristles and a four-inch tether on a carabiner, handmade in the USA. The yellow, green and blue cord is what people notice. Ours in <a href="/drops/brand-to-know-dimple-divot">the Dimple &amp; Divot Brand to Know</a>.'),
 "S11": ("Fella Golf", "Fella Matchbox Golftees", "&euro;25 (~$29)",
   "https://fellagolf.com/products/fella-golf-tees",
   'Fifty wooden tees with two retro green stripes, packed in a matchbox Fella designed itself. &ldquo;Strike and send them away,&rdquo; says the box. It is the best-looking way to carry tees we have found. More in <a href="/drops/fella-golf">our Fella post</a>.'),
 "S27": ("Students Golf", "Highly Educated Golf Tees, Box of 50", "$15",
   "https://studentsgolf.com/products/highly-educated-golf-tees-box-of-51",
   'Fifty 2.75-inch tees made from recycled bamboo, with contrast stripes and the Students logo in the middle, and they conform to the rules. The joke on the box is that they are highly educated, even if you are not sure you can get off the tee. See <a href="/drops/students-golf-our-15-favorites">our 15 Students favorites</a>.'),
 "S36": ("Western Birch", "&ldquo;Redan&rdquo; Striped Golf Tee, Box of 50", "$9.99",
   "https://westernbirch.com/products/redan-striped-golf-tee",
   "Western Birch makes its tees from white birch with a thicker shank, so they last longer than the ones in the pro shop bowl. The Redan box is fifty 2.75-inch tees striped in white, dark blue and green. Under ten dollars, and they look like they cost more."),
 # Pocket pieces
 "S03": ("Seamus Golf", "Hand Forged Seamus Goat Money Clip, Bronze", "$80",
   "https://www.seamusgolf.com/products/hand-forged-seamus-goat-money-clip",
   'A second-generation blacksmith in Portland heats the bronze and hammers this clip by hand, then stamps it with the Seamus goat. There are no magnets, springs or carbon, just one forged piece. It carries the cash for the skins game. Ours in <a href="/drops/brand-to-know-seamus">the Seamus Brand to Know</a>.'),
 "S19": ("Craighill", "Swingtop Lighter", "$78",
   "https://craighill.co/products/swingtop-lighter",
   "Craighill is a design studio in Brooklyn, and the Swingtop is a refillable flint lighter. Press the arm and the top swings open and sparks; let go and it snaps shut. It is for the post-round cigar, and nothing else here is as satisfying to fidget with. Stainless or black."),
 "S20": ("Corter Leather", "Bottlehook", "$36.50",
   "https://corterleather.com/products/bottlehook",
   'Corter&rsquo;s patented hook clips your keys to a belt loop or a bag D-ring and opens a beer at the turn. It is solid brass, about three inches long, with a lifetime warranty against breaking. It was in <a href="/drops/golf-bag-accessories-what-to-hang-from-your-bag">our bag accessories roundup</a> too, because it earns its place.'),
 "S28": ("Sugarloaf Social Club", "&ldquo;Nantucket Red&rdquo; Needlepoint Bottle Opener", "$35",
   "https://sugarloafsocialclub.com/products/nantucket-red-needlepoint-bottle-opener",
   'Hand-stitched needlepoint set into solid wood, with a magnet hidden inside so it sticks to the cart or the fridge. It is 4.25 inches long, in Nantucket red with the SSC mark. Ours in <a href="/drops/brand-to-know-sugarloaf-social-club">the Sugarloaf Brand to Know</a>.'),
 # Pouches
 "S41": ("Jones Sports Co.", "Zipper Pouch, Black", "$30",
   "https://jonessportsco.com/products/zipper-pouch-black",
   'An 8 by 7 inch pouch with a YKK carabiner, built to clip to the bag and hold the small stuff from the list above. It is the plainest pouch here and the cheapest, and Jones will embroider it if you want. More in <a href="/drops/brand-revisited-jones-sports-co">our Jones revisit</a>.'),
 "S42": ("Ghost Golf", "Utility Pouch, Kovert Ops", "$40",
   "https://ghostgolf.com/products/utility-pouch-kovertops",
   "Ghost&rsquo;s pouch is 7.25 by 6 inches and water-resistant, with a velour lining so a phone or a brass tool goes in without scratching. It has one zip pocket and one snap pocket, so tees and markers stay apart from keys. Kovert Ops is the gray and black colorway."),
 "S43": ("Steurer &amp; Jacoby", "9&Prime; x 8&Prime; Valuables Pouch, Waxed Canvas", "$50",
   "https://sj.golf/products/waxed-canvas-and-leather-valuables-pouch",
   "Steurer &amp; Jacoby makes this by hand from waxed cotton duck and leather, with a solid brass trigger snap that clips to the bag. Phone, wallet and keys go in one place for the round, and the waxed canvas looks better the more it gets beaten up."),
 "S44": ("Mackem Golf", "Copley Valuables Pouch", "A$55 (~$36)",
   "https://mackemgolf.com/products/copley-valuables-pouch",
   'Mackem turns old suiting into golf goods, and the Copley is a deep blue cloth with pink and gold running through it. It is a 20cm drawstring bag that holds a watch, wallet and phone, or a dozen balls. Ours in <a href="/drops/brand-to-know-mackem-golf">the Mackem Brand to Know</a>.'),
 "S45": ("Hudson Sutler", "Canvas Club Pouch", "$50",
   "https://hudsonsutler.com/products/canvas-club-pouch",
   'Hudson Sutler makes this pouch in the USA from 18-ounce water-repellent canvas, with a nylon base, a YKK zip and a leather pull. At 10 by 5.5 inches it takes balls, tees and markers, and it can be monogrammed. Navy, natural with hunter green, or Nantucket red. Ours in <a href="/drops/brand-to-know-hudson-sutler">the Hudson Sutler Brand to Know</a>.'),
}

SECTIONS = [
    ("Ball Markers", "ball-markers", ["S02", "S04", "S06", "S05", "S10", "S33"],
     "<strong>Six markers &middot; ~$17&ndash;$220</strong>The ball marker is the smallest thing you own that everybody sees, because it sits on the green while three people wait for you to putt. These run from a lip balm with a magnet in the lid to a sterling silver piece engraved by hand in Kerrville. In between: Scottish copper from a sword forge, an Arizona roadrunner in sunglasses, Malbon&rsquo;s enameled cloud, and needlepoint. For more, see <a href=\"/drops/the-ball-marker-atlas\">The Ball Marker Atlas</a>."),
    ("Divot and Pitch Tools", "divot-tools", ["S01", "S07", "S15", "S16", "S31"],
     "<strong>Five tools &middot; $39.99&ndash;$109</strong>You fix a pitch mark on almost every green, so the tool comes out of your pocket more than anything else you carry. Four of these are metal you can feel: TOTEM&rsquo;s brass on a paracord loop, Provision&rsquo;s solid copper, Edel&rsquo;s fine-milled steel and Hidden Links&rsquo; single brass prong. Kraken&rsquo;s goes on your finger like a ring."),
    ("Brushes and Tees", "brushes-and-tees", ["S22", "S23", "S11", "S27", "S36"],
     "<strong>Five pieces &middot; $9.99&ndash;$48</strong>Two small groove brushes in good wood, and three boxes of tees that look better than the free ones. Gamut&rsquo;s ebony brush lives in a pocket and Dimple &amp; Divot&rsquo;s hickory one clips to the bag. Fella packs its tees in a matchbox, Students makes them from recycled bamboo, and Western Birch stripes birch hardwood in white, blue and green."),
    ("Pocket Pieces", "pocket-pieces", ["S03", "S19", "S20", "S28"],
     "<strong>Four pieces &middot; $35&ndash;$80</strong>Not strictly golf, but they come out on the course and in the parking lot after. A hand-forged bronze money clip for the cash game, a flint lighter for the cigar, a brass hook that opens a beer and a needlepoint opener with a magnet in it."),
    ("Pouches for an Organized Bag", "pouches", ["S41", "S42", "S43", "S44", "S45"],
     "<strong>Five pouches &middot; $30&ndash;$50</strong>Everything above has to live somewhere, and the bottom of a bag pocket is where markers and tees go to disappear. A small pouch keeps the round&rsquo;s kit in one place and the phone and keys in another. Jones and Ghost clip on with a carabiner, Steurer &amp; Jacoby with a brass snap, Hudson Sutler zips up like a dopp kit, and Mackem&rsquo;s is a drawstring bag cut from old suiting."),
]

N = 25
GRID_CSS = ('<style>/*TGI-SMALLTHINGS-GRID*/.products-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
            '.products-grid[data-n="6"]{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}'
            '.products-grid[data-n="5"]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
            '.products-grid[data-n="5"]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:1024px){.products-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:820px){.products-grid[data-n="6"]{grid-template-columns:repeat(2,minmax(0,1fr))}.products-grid[data-n="5"]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n="4"],.products-grid[data-n="6"]{grid-template-columns:1fr}.products-grid[data-n="5"]>.product-card{flex-basis:100%}}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>I carried a plastic divot tool for years and never once thought about it. It snapped, I grabbed another from the bowl in the pro shop, and that one snapped too. The brass one I carry now is heavier and cost more, and it&rsquo;s still the same tool a season later. The edges have gone soft and the shine has dulled to something warmer. My hand finds it in my pocket without looking, and fixing a pitch mark has become part of how I walk onto a green.</p>
    <p>Every pick here is a small thing made well enough to stay with you: twenty-five of them, each from a different independent maker, in brass, copper, bronze, hickory, leather and waxed canvas, materials that look better with use instead of worse. A copper marker darkens, a leather pouch creases, a hickory brush handle smooths out in your grip. None of it is disposable, and most of it costs less than a dozen balls.</p>
    <h2 class="products-hdr btk-story-hdr">Buy It Once</h2>
    <p>If you start with one thing, make it TOTEM&rsquo;s brass divot tool. It comes out on every green, it ages the way brass should, and it&rsquo;s the kind of tool that slowly becomes yours. From there, add a marker you like looking at and a pouch to keep it all in one place, and you won&rsquo;t be digging through the bottom of the bag for tees again.</p>
    <p>Prices were read on each brand&rsquo;s own store on October 8, 2026, and everything was in stock that day. Non-US prices show an approximate dollar figure.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>25 from 25 brands</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$9.99&ndash;$220</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>TOTEM brass divot tool, $80</span></div>
      <div class="sidebar-detail"><span class="l">Materials</span><span>Brass, copper, bronze, hickory, leather</span></div>
      <div class="sidebar-detail"><span class="l">The splurge</span><span>Clint Orms Texas marker, $220</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>October 8, 2026</span></div>
      <a href="#ball-markers" class="sidebar-cta">See the picks &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#BallMarker</span>
        <span class="hashtag">#DivotTool</span>
        <span class="hashtag">#GolfAccessories</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best small golf accessories?",
     "This roundup has 25 from independent makers in five groups: ball markers, divot and pitch tools, brushes and tees, pocket pieces like money clips and bottle openers, and small pouches to keep them organized. Our pick is TOTEM's brass divot tool ($80)."),
    ("What is a good golf gift under $50?",
     "Most of this list is under $50. Birdie Balm's lip balm with a built-in ball marker (about $17), Malbon's Nimbus Buckets marker ($38), Fella's matchbox tees (about $29), Edel's Fine Milled Repair Tool ($45) and Corter's brass Bottlehook ($36.50) all qualify."),
    ("What is the best divot tool?",
     "In this guide, TOTEM's 1PCS brass tool ($80) is our pick, Edel's Fine Milled Repair Tool ($45) is the best value, and Kraken's Signet ($109) is the most unusual, a pitch tool that slides onto your finger like a ring."),
    ("How do you keep a golf bag organized?",
     "Use a small pouch for the round's kit so markers, tees and tools don't sink to the bottom of a pocket. Jones' Zipper Pouch ($30), Ghost Golf's Utility Pouch ($40), Steurer & Jacoby's waxed canvas pouch ($50), Mackem's Copley drawstring pouch and Hudson Sutler's Canvas Club Pouch ($50) all clip on or drop in."),
    ("What is the most expensive pick here?",
     "Clint Orms' sterling silver State of Texas ball marker at $220, engraved by hand in Kerrville, Texas. Prices were read on each brand's own store on October 8, 2026."),
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
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
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
            {"@type": "ListItem", "position": 3, "name": "Small Golf Accessories", "item": URL}]},
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
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    brands = [H.unescape(P[k][0]) for k in ids]
    assert len(brands) == len(set(brands)), "brand repeated"
    for k in ids:
        assert len(FRN.get(k, [])) >= 1, k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Small Golf Accessories</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>TOTEM, Birdie Balm, Seamus, Fyfe, Edel, Craighill and more</span><span class="dot"></span>
    <span>25 picks &middot; in stock October 8, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A copper Provision divot tool and a white tee lying on the green beside a golf ball" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace('</head>', GRID_CSS + '</head>', 1) + body + tail
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
