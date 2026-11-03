#!/usr/bin/env python3
"""build-collabs-nov.py — "Our Favorite Golf Collabs This Month", 3 November 2026. Cloned from build-vest-edit.py; large-image layout
(two big photos per collab, then the write-up and the pieces), after build-bag-setup.py.
Lenny: "post about our favorite collabs this month. Manors did a great one with Sun Mountain, let's find at least 6 others and do the large
image format". Picks: Manors x Sun Mountain + his selections (Pare x Minted Greens, Pare x Bluetross, Sherwood x Dormie, Nike x Eastside,
Sun Day Red x VESSEL, Tremont x Apres-Golf). Sweep: ~107 indexed stores' products.json for collab titles created since mid-Sept (Nov 3 2026).
FACTS: each product's own page copy (USD stores). Photos: each brand's own.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Our Favorite Golf Collabs This Month: Manors x Sun Mountain, Sherwood x Dormie and More"
DESC = ("The best golf collaborations of the month: Manors x Sun Mountain bags, a Par\u00e9 x Minted Greens mahjong set, Sherwood hockey socks "
        "turned Dormie headcovers, Nike x Eastside Golf, Sun Day Red x VESSEL, Walker x Hiroki and more.")
H1 = "Our Favorite Golf Collabs This Month"
BC = "Favorite Collabs: November"
SLUG = "favorite-golf-collabs-november-2026"
IMG = "/images/collabs-nov"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "e25": ("Sun Mountain x Manors", "E-2.5 Stand Bag", "$325", U("sunmountain.com","sun-mountain-x-manors-e-2-5-stand-bag"),
   "Sun Mountain&rsquo;s light E-2.5 stand bag in stone, wrapped in Manors&rsquo; wave monogram. Limited edition; Sun Mountain lists it as shipping November 9."),
 "cg3": ("Sun Mountain x Manors", "ClubGlider3 Travel Bag", "$500", U("sunmountain.com","sun-mountain-x-manors-clubglider3-travel-bag"),
   "The travel bag with the fold-out legs, in the same monogram, with a TSA lock. Made for the bucket-list trip. Also shipping November 9."),
 "mahj": ("Par&eacute; x Minted Greens", "Mahjong Set", "$350", U("pare.golf","pare-x-minted-greens-mahjong-set"),
   "144 tiles, a custom green table mat and a green leather briefcase. Dice and other accessories are not included."),
 "blade": ("Par&eacute; x Bluetross", "Blade Putter Headcover", "$150", U("pare.golf","pare-x-bluetross-blade-putter-headcover"),
   "Bluetross&rsquo;s first piece in waxed canvas instead of leather, with Par&eacute;&rsquo;s Manila logo and a magnetic snap."),
 "drv": ("Par&eacute; x Bluetross", "Driver Headcover", "$170", U("pare.golf","pare-x-bluetross-driver-headcover"),
   "The matching driver cover. Waxed canvas creases and darkens with every round, so no two will age the same way."),
 "sock": ("Sherwood x Dormie", "Hockey Sock Fairway Headcover, Red", "$230", U("dormieworkshop.com","sherwood-x-dormie-hockey-sock-fairway-headcover-red"),
   "Real red Sherwood hockey socks rebuilt as a fairway barrel, with leather stripes and a strip of clear patent leather stitched on like sock tape."),
 "sdrv": ("Sherwood x Dormie", "Driver Headcover", "$210", U("dormieworkshop.com","sherwood-x-dormie-headcover"),
   "Black full-grain leather with the Sherwood script running the length, its final d turning into Dormie&rsquo;s tap-in icon."),
 "rbag": ("Sherwood x Dormie", "Range Ball Bag", "$300", U("dormieworkshop.com","sherwood-x-dormie-range-ball-bag"),
   "A leather range bag inspired by the puck bag dumped at the blue line before warmups. Same ritual, different ice."),
 "am90": ("Nike x Eastside Golf", "Air Max 90 G", "$170", U("eastsidegolf.com","nike-air-max-90-g-x-eastside-golf"),
   "A cosmic edition in black and smoke gray with midnight accents and metallic details, on the spikeless Air Max 90 G."),
 "next": ("Nike x Eastside Golf", "NEXT% Tour 3", "$200", U("eastsidegolf.com","nike-next-tour-3-x-eastside-golf"),
   "The same cosmic story on Nike&rsquo;s spiked tour shoe, in black and obsidian with an iridescent swoosh."),
 "pv": ("Sun Day Red x VESSEL", "Player V Stand Bag, Venom XV", "$548", U("vesselgolf.com","sun-day-red-x-vessel-player-v-stand-venom-black"),
   "VESSEL&rsquo;s 6-way Player V in custom iridescent black eco leather with an embossed tiger logo. It shifts color in the sun."),
 "hset": ("Sun Day Red x VESSEL", "Venom XV Headcover Set", "$248", U("vesselgolf.com","sun-day-red-x-vessel-venom-xv-headcover-set"),
   "Driver, fairway and utility covers in the same pearlized black finish, each with the embossed tiger."),
 "vblade": ("Sun Day Red x VESSEL", "Blade Cover, Venom XV", "$90", U("vesselgolf.com","sun-day-red-x-vessel-blade-cover-venom-black"),
   "A tour-shaped blade cover with a padded interior and black hardware. The easiest way into the collection."),
 "diam": ("Tremont x Apr&egrave;s-Golf", "Diamond Stitch Leather Headcovers", "$138", U("apresgolf.com","diamond-stitch-leather-tremont-x-apres-golf"),
   "Diamond-stitched full-grain brown leather lined in Apr&egrave;s&rsquo;s Fruit Looper fleece. Driver, fairway, hybrid and putter."),
 "mossy": ("Tremont x Apr&egrave;s-Golf", "Mossy Waxed Canvas Headcovers", "$128", U("apresgolf.com","mossy-waxed-canvas-tremont-x-apres-golf"),
   "Mossy green waxed canvas with Apr&egrave;s-Golf puffed up in Nantucket Red. Center-shafted putter covers are new for this run."),
 "iwn": ("Tremont x Apr&egrave;s-Golf", "&ldquo;I Will Not&rdquo; Headcovers", "$128", U("apresgolf.com","i-will-not-tremont-x-apres-golf"),
   "The &ldquo;I will not Apr&egrave;s-Golf&rdquo; slogan printed all over leather, with the Fruit Looper fleece inside."),
 "rvwb": ("Old Rip Van Winkle x Bettinardi", "Barrels Blade Putter Headcover", "$150", U("bettinardi.com","old-rip-van-winkle-x-bettinardi-barrels-blade-putter-headcover"),
   "A weathered cream cover printed with the Old Rip Van Winkle distillery barrels, with a plush lining and a magnetic closure."),
 "rvwm": ("Old Rip Van Winkle x Bettinardi", "Barrels Mallet Putter Headcover", "$150", U("bettinardi.com","old-rip-van-winkle-x-bettinardi-barrels-mallet-putter-headcover"),
   "The mallet version, with the B hex and the Van Winkle W on the back. It is a pre-order, shipping in three to four weeks."),
 "hiroki": ("Walker x Hiroki", "Leather Sunday Bag, Almond", "$400", U("walkergolfthings.com","walker-x-hiroki-leather-sunday-bag"),
   "Full leather panels, a waterproof lining, an 8-inch opening with one divider and two big pockets embossed with the &ldquo;Dancing Kooka.&rdquo; It collapses flat."),
 "ftmal": ("Sugarloaf x First Tee", "Camille&rsquo;s Mallet Headcover", "$100", U("sugarloafsocialclub.com","ssc-x-first-tee-mallet-cover"),
   "Camille drew a golfer putting on top of a club sandwich, her favorite. Every dollar goes to the First Tee."),
 "ftbrl": ("Sugarloaf x First Tee", "Julien&rsquo;s Driver Headcover", "$105", U("sugarloafsocialclub.com","ssc-x-first-tee-barrel-driver-cover"),
   "A navy barrel cover with the New York skyline and &ldquo;The Future of the Game,&rdquo; designed by Julien for his Metro New York chapter."),
 "ftbld": ("Sugarloaf x First Tee", "Riya&rsquo;s Blade Putter Cover", "$100", U("sugarloafsocialclub.com","ssc-x-first-tee-blade-cover"),
   "Periwinkle with flowers, inspired by what Riya sees on the course and her favorite colors. Green fleece inside."),
 "f23": ("MacKenzie x Fyfe", "23rd Edition Carry Bag", "$888", U("fyfegolf.com","mackenzie-golf-bag-x-fyfe-23rd-edtion"),
   "Midnight black waxed canvas with tan leather, a cream suede strap, a tartan-lined pocket and a cream badge for the edition."),
 "f24": ("MacKenzie x Fyfe", "24th Edition Carry Bag", "$1,161", U("fyfegolf.com","mackenzie-golf-bag-x-fyfe-24th-edition"),
   "Green leather with mahogany trim and a pocket lined in Harris Tweed. The first run sold out; this is a pre-order for January 2027."),
}
COLLABS = [
 ("manors", "Manors x Sun Mountain", "Released October 21", ["e25","cg3"],
  ["Manors, the London brand, and Sun Mountain, the bag maker from Missoula, Montana, put the same idea on two bags: golf should take you places. Sun Mountain&rsquo;s copy says the best golf is &ldquo;still out there waiting to be found.&rdquo;",
   "The result is Sun Mountain&rsquo;s E-2.5 stand bag and ClubGlider3 travel bag in stone and charcoal, covered in Manors&rsquo; wave monogram. It is the most wearable collab here: quiet colors, serious bags, and a pattern you notice only up close.",
   "Both are limited and listed as shipping November 9. If you have a golf trip planned for 2027, the ClubGlider3 is the one to get."]),
 ("pare", "Par&eacute; x Minted Greens and Bluetross", "Released October 14 and 26", ["mahj","blade","drv"],
  ["Par&eacute;, the Filipino-American golf brand, had the busiest month of anyone, with two collabs two weeks apart.",
   "The first, with Bluetross, is a driver cover and a blade putter cover with Par&eacute;&rsquo;s Manila logo. Bluetross is known for leather headcovers made in the USA, and this is its first time working in waxed canvas. That is the right call: waxed canvas creases, darkens and picks up a patina, so the cover gets better the more you play.",
   "The second marks Par&eacute;&rsquo;s third anniversary and Filipino American History Month: a mahjong set made with Minted Greens, dedicated to a late uncle who taught the family to play. It comes in a green leather briefcase with 144 tiles and a custom green mat. It is the least golf thing in this post, which is exactly why we like it. Golf trips end at a table, and this is a better table game than cards."]),
 ("dormie", "Sherwood x Dormie", "Released September 21 to October 7", ["sock","sdrv","rbag"],
  ["Two Canadian shops: Sherwood has made hockey sticks since 1949, and Dormie Workshop has made leather headcovers since 2014. They call the collection North of Par, for everyone who plays hockey all winter and golf all summer.",
   "The standout is the fairway cover made from real red Sherwood hockey socks, with leather stripes and a strip of patent leather stitched on like sock tape. The driver cover runs the Sherwood script into Dormie&rsquo;s tap-in icon, and the range bag is modeled on the puck bag at practice. Some pieces have already sold out."]),
 ("eastside", "Nike x Eastside Golf", "Released October 6", ["am90","next"],
  ["Eastside Golf, from Atlanta, has a long-running partnership with Nike, and this edition looks to the sky. The Air Max 90 G and NEXT% Tour 3 come in black and smoke gray with midnight accents and metallic details.",
   "The Air Max 90 G is the one we would wear: spikeless, comfortable and good off the course. The NEXT% Tour 3 is for players who want spikes and a little more grip."]),
 ("vessel", "Sun Day Red x VESSEL", "Released September 28", ["pv","hset","vblade"],
  ["VESSEL keeps working with Sun Day Red, Tiger Woods&rsquo;s brand, and the Venom XV set is the best-looking one yet: custom iridescent black eco leather with an embossed tiger logo and black hardware.",
   "It looks plain black in the shade and shifts color in the sun. The Player V stand bag is the centerpiece; the blade cover is the easy entry at $90. A duffel and backpack match if you want the full set."]),
 ("apres", "Tremont x Apr&egrave;s-Golf", "Released September 26 to 29", ["diam","mossy","iwn"],
  ["Apr&egrave;s-Golf, the brand for the round after the round, teamed up with Tremont Sporting Co. on headcovers: diamond-stitched brown leather, mossy green waxed canvas and the &ldquo;I will not Apr&egrave;s-Golf&rdquo; slogan in leather.",
   "Every cover is lined in Apr&egrave;s&rsquo;s Fruit Looper fleece, and this run adds center-shafted putter covers for the first time. Matching Tremont trucker hats came out in the same drop."]),
 ("rvw", "Old Rip Van Winkle x Bettinardi", "Released October 20", ["rvwb","rvwm"],
  ["Bettinardi, the putter maker from Tinley Park, Illinois, and Old Rip Van Winkle, the bourbon that people line up for, released a Pappy collection on October 20. The one-of-one putters with barrel-wood inlays were gone within a day.",
   "The headcovers are still here. Both are a weathered cream with the old distillery barrels printed on the front, which is about as close as most of us will get to a bottle. The blade cover ships now; the mallet is a pre-order."]),
 ("hiroki", "Walker x Hiroki", "Released September 17", ["hiroki"],
  ["Walker, the Gold Coast brand, went across the ditch to Hiroki in Auckland, which makes some of the best Sunday bags around. Walker calls it &ldquo;a handshake with our mates from across the ditch.&rdquo;",
   "The bag is almond leather from top to bottom, with a waterproof lining, a leather base and two big pockets embossed with the &ldquo;Dancing Kooka,&rdquo; a kookaburra mid-step. It is the most beautiful bag in this post and the one we would carry on a quick nine."]),
 ("firsttee", "Sugarloaf Social Club x First Tee", "Released September 13", ["ftmal","ftbrl","ftbld"],
  ["This is the one with the best story. Sugarloaf Social Club handed the design work to kids from the First Tee, and every cover is named for the junior who drew it.",
   "Camille put a golfer on top of a club sandwich. Julien drew the New York skyline for his Metro New York chapter and wrote &ldquo;The Future of the Game&rdquo; on it. Riya went with flowers and her favorite colors. Tiago&rsquo;s driver cover and Aadya&rsquo;s visor round out the set.",
   "All proceeds go to the First Tee. That makes it the easiest thing in this post to justify buying."]),
 ("fyfe", "MacKenzie x Fyfe", "Released October 29", ["f23","f24"],
  ["MacKenzie has made carry bags in Oregon since 1985, and Fyfe, from Fife in Scotland, is known for tweed and tartan headcovers. Their bags come in numbered editions, and the two newest landed this month.",
   "The 23rd is black waxed canvas with tan leather and a tartan-lined pocket. The 24th is green leather and mahogany with Harris Tweed inside the pocket. It is the most expensive collab in this post and the one that will look best in 20 years."]),
]
SECTIONS = [(c[1], c[0], c[3], c[2]) for c in COLLABS]
N = 24
PAIRS = {}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The best collabs in golf right now are not logo swaps. They take something one brand does well and put it somewhere new: a London clothing brand&rsquo;s pattern on a Montana bag maker&rsquo;s travel bag, a hockey sock turned into a headcover, a mahjong set from a golf brand.</p>
    <p><strong>How we picked.</strong> We went through the stores of the brands in our index and pulled every collaboration released since mid-September that was still in stock on November 3, 2026. These are the eleven we liked most, led by Manors x Sun Mountain.</p>
    <p><strong>What makes a good one.</strong> Each brand has to bring something real. Sun Mountain brings the bag, Manors the look. Sherwood brings real hockey socks, Dormie the leather work. Bluetross tries waxed canvas for the first time. When the collab teaches one of the brands a new trick, you get something neither would have made on its own.</p>
    <p><strong>What to buy first.</strong> If you only get one thing here, make it the Sherwood x Dormie hockey sock cover. It is the most original piece in the post, and some of the collection has already sold out. If you are planning a trip, the Manors ClubGlider3 is the practical pick.</p>
    <p><strong>What is in here.</strong> Eleven collabs and 24 pieces, all in stock when we checked, with prices in US dollars. The two Sun Mountain x Manors bags are listed as shipping November 9.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Collabs</span><span>11</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>24</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>Sept 13&ndash;Oct 29, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$90&ndash;$1,161</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Sherwood x Dormie Hockey Sock Fairway Cover</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfCollabs</span>
        <span class="hashtag">#NewDrops</span>
        <span class="hashtag">#GolfStyle</span>
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
    <h2 class="products-hdr" id="last-word">More on the Way</h2>
    <p>A few more collabs from the last few weeks did not make the eleven. Sun Mountain also made a Western stand bag with Marucci, the baseball bat company, and Jones and Cph/Golf released a full collection that we covered in <a href="/drops/jones-cph-golf-collab">its own post</a>.</p>
    <p>Collabs move fast and most are limited. If one of these is the one, do not wait for the restock.</p>
  </div>
</section>
"""
HERO_ALT = "Hands opening the green leather briefcase of the Paré x Minted Greens mahjong set, with the PARÉ logo inside the lid"
FRN = json.loads((ROOT / "research/collabs-nov/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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


BIGSTY = 'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5;"'
CBY = {c[0]: c for c in COLLABS}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    c = CBY[anchor]
    num = [x[0] for x in COLLABS].index(anchor) + 1
    figs = "".join(f'<figure style="margin:0;"><img src="{IMG}/big-{anchor}-{i}.jpg" alt="{H.escape(H.unescape(h2))} photograph {i}" loading="lazy" {BIGSTY} /></figure>' for i in (1, 2))
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in c[4])
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Collab {num}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
            f'  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:1180px;margin:0 auto 26px;">{figs}</div>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;">\n{prose}\n  </div>\n'
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
    <span>The Edit &middot; Eleven collabs</span><span class="dot"></span>
    <span>24 picks &middot; in stock, checked November 3, 2026</span>
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
