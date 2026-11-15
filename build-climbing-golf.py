#!/usr/bin/env python3
"""build-climbing-golf.py — Climbing x Golf crossover gear. 14 November 2026. Cloned from build-lucky-rituals.py.
Lenny: "Let's do a Climbing / Golf crossover" -> crossover gear -> sheet v1-v4 (chalk bags out, trail shoes in, more brands, indie labels) -> "build the post" (all 98; Hitorii Barrel Pants dropped: only women-modelled photos).
FACTS: prices/products read from each store 14 Nov 2026 (Shopify JSON; Danner/Salomon pages in browser). Looking For Wild sells in EUR. Lifestyle bands from brands' own campaign images (Instagram images could not be downloaded). Men only. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Climbing x Golf: 37 Pieces of Climbing and Trail Gear That Work on the Course"
DESC = ("The climbing pant is a very good golf pant. 37 crossover picks: South2 West8, four indie climbing labels, "
        "trail shoes from Danner, Salomon, Altra and Scarpa, carabiners, boulder brushes and totes, with US prices.")
H1 = "Climbing &times; Golf"
BC = "Climbing &times; Golf"
SLUG = "climbing-golf-crossover-gear"
IMG = "/images/climbing-golf"
SHOP = ""
P = {
 "g000": ('South2 West8', 'Trek Pant, Olive Herringbone', '$365', 'https://nepenthesamerica.com/products/south2-west8-trek-pant-olive-cotton-herringbone-fall-winter-2026',
   'Our pick. Made in Japan from cotton herringbone, with a relaxed fit, a drawstring waist and drawcord hems you can pull in above a spikeless shoe. The pant that started this post.'),
 "g003": ('South2 West8', 'Climbing Pant, Natural Canvas', '$290', 'https://nepenthesamerica.com/products/south2-west8-climbing-pant-natural-cotton-canvas-fall-winter-2026',
   'New on November 1. Cotton canvas with double knees, a reinforced seat that doubles as the back pockets, a webbing belt and drawcord hems.'),
 "g057": ('Rungne', 'Highballer Utility Pants Soft Stretch', '$159', 'https://rungne.com/products/highballer-utility-pants-new-color',
   'Rungne&rsquo;s boulder pant in soft stretch with utility pockets.'),
 "g060": ('Rungne', 'Approach Quarter Zip, 180g', '$99', 'https://rungne.com/products/athletic-unisex-zip-pullover',
   'A light grid-fleece quarter zip with contrast stitching.'),
 "g013": ('Gramicci', 'Corduroy Loose Tapered Ridge Pant', '$138', 'https://www.gramicci.com/products/corduroy-loose-tapered-ridge-pant-1',
   '100% cotton 10-wale cord with Gramicci&rsquo;s elastic waist and integrated belt, cut loose with a taper. New for fall.'),
 "g061": ('Hitorii', 'Bouldering Pants, Pastel Sage, Ginkgo', '$120', 'https://hitorii.com/products/bouldering-pants-mint-green-gingko',
   'Hitorii&rsquo;s baggy bouldering pant with a ginkgo leaf embroidered at the knee.'),
 "g066": ('g2g', 'Double Knee Pants', '$120', 'https://g2g.co/products/double-knee-pants',
   'g2g&rsquo;s double-knee work pant with contrast stitching, from Seattle.'),
 "g068": ('g2g', 'High Pile Fleece Jacket, Forest', '$120', 'https://g2g.co/products/high-pile-zip-fleece-forest',
   'High-pile fleece with a shell yoke and hood.'),
 "g071": ('Looking For Wild', 'Fitz Roy Cargo Climbing Pant, Mayfly', '&euro;99 (about $110)', 'https://lookingforwild.com/products/pantalon-descalade-fitz-roy-cargo-mayfly-1',
   'Looking For Wild&rsquo;s cargo climbing pant, new in September. From the French climbing label.'),
 "g079": ('Altra', 'Lone Peak 9+ x and wander', '$185', 'https://www.altrarunning.com/en-us/products/mens-lone-peak-9-and-wander-al0a85uk',
   'The Lone Peak, reworked by and wander.'),
 "g082": ('Scarpa', 'Mescalito Approach Shoe', '$219.95', 'https://www.scarpa.com/products/mescalito-shoe-for-technical-approach-and-via-ferrata-72103-350-8',
   'Scarpa&rsquo;s approach shoe, made for the walk to the rock, with a sticky climbing-rubber toe. Steady on a slope.'),
 "g077": ('Altra', 'Experience Wild 3+ GTX', '$185', 'https://www.altrarunning.com/en-us/products/mens-experience-wild-3-gtx-al0a85se',
   'A cushioned trail shoe with a GORE-TEX lining. New in September; the one for dew.'),
 "g084": ('Salomon', 'XT-4 OG', '$200', 'https://www.salomon.com/en-us/product/xt-4-og-li3335/L49217200',
   'The reissued Salomon trail runner that turned into a fashion shoe.'),
 "g087": ('Salomon', 'XT-Quest GTX x BEAMS', '$240', 'https://www.salomon.com/en-us/product/xt-quest-gtx-beams-li9703/L45459900',
   'Salomon&rsquo;s XT-Quest GORE-TEX made with BEAMS, the Tokyo store we know from BEAMS Golf.'),
 "g091": ('Danner', 'Trail 2650', '$190', 'https://www.danner.com/trail-2650-3-brown-red.html',
   'Named for the 2,650-mile Pacific Crest Trail. A light, grippy hiking sneaker that looks at home on a golf course.'),
 "g095": ('Danner', 'Danner x Osprey N45 MAX', '$220', 'https://www.danner.com/men-s-n45-max-low-osprey-sandy-grey.html',
   'A limited N45 made with the backpack maker Osprey.'),
 "g005": ('South2 West8', 'Long-Sleeve Polo, Green Pique', '$165', 'https://nepenthesamerica.com/products/south2-west8-l-s-polo-shirt-green-cotton-pique-fall-winter-2026',
   'Cotton pique in a long-sleeve polo shape with the label&rsquo;s deer embroidered on the chest. Passes a dress code and still looks like South2 West8.'),
 "g015": ('Outdoor Research', 'Astroman Long Sleeve Sun Shirt', '$120', 'https://www.outdoorresearch.com/products/mens-astroman-long-sleeve-sun-shirt-322670',
   'Named for the Yosemite climb and built for climbing in the sun. A light button-up that works as a golf sun shirt.'),
 "g047": ('Snow Peak', 'Lindis Sun Hoodie', '$99.95', 'https://snowpeak.com/products/lindis-sun-hoodie',
   'A light sun hoodie in a water print. For the bright days.'),
 "g050": ('Battenwear', 'Warm-Up Fleece, Tan', '$250', 'https://battenwear.com/products/20426fw-warm-up-fleece-tan',
   'Battenwear&rsquo;s zip fleece with a flap pocket and ribbed cuffs.'),
 "g021": ('Metolius', 'FS Mini II Carabiner', '$7.95', 'https://www.metoliusclimbing.com/products/fs-mini-ii-carabiner',
   'A small, light, full-strength climbing carabiner. Clip a towel, a brush or your keys to the bag.'),
 "g022": ('Metolius', 'Bravo II Wiregate Carabiner', '$9.95', 'https://www.metoliusclimbing.com/products/bravo-ii-wiregate-carabiner',
   'A wiregate climbing carabiner in bright anodized colors. The cheapest climbing gear in the post.'),
 "g023": ('Topo Designs', 'Crux Key Clip', '$18', 'https://topodesigns.com/products/crux-key-clip-black-white',
   'Climbing rope that loops around your wrist with a Topo aluminum carabiner. For the cart key.'),
 "g024": ('Topo Designs', 'Carabiner Shoulder Strap', '$17', 'https://topodesigns.com/products/carabiner-shoulder-strap-desert-palm-goldenrod',
   'Paracord with Topo carabiners on each end. Turns a small Topo bag into a shoulder carry for the range.'),
 "g025": ('Black Diamond', 'BD Stretch Belt', '$39', 'https://www.blackdiamondequipment.com/products/bd-stretch-belt',
   'A stretch webbing belt with an aluminum buckle, made to stay put through any activity. A good belt for a full turn.'),
 "g026": ('Topo Designs', 'Slim Web Belt', '$42', 'https://topodesigns.com/products/slim-web-belt-desert-palm-goldenrod',
   'One-inch nylon webbing with a Topo jacquard pattern and an anodized aluminum buckle.'),
 "g027": ('Gramicci', 'Boulder Brush', '$25', 'https://www.gramicci.com/products/boulder-brush',
   'A wood-handled climbing brush with dense synthetic bristles and a paracord loop. It cleans clubface grooves as well as holds.'),
 "g028": ('Metolius', 'Razorback Boar&rsquo;s Hair Brush', '$9.95', 'https://www.metoliusclimbing.com/products/razorback-boars-hair-brush',
   'Densely packed boar&rsquo;s hair with an ergonomic handle, for $9.95. The best club brush on this page might be a climbing brush.'),
 "g029": ('Metalwood Studio', 'Luminous Carabiner', '$10', 'https://metalwood.studio/products/metal-logo-luminous-carabiner-green',
   'The one golf-brand piece: Metalwood&rsquo;s glow-in-the-dark plastic carabiner, for keys or a towel.'),
 "g030": ('Gramicci', 'Running Man Key Chain', '$35', 'https://www.gramicci.com/products/running-man-climbing-key-chain',
   'Gramicci&rsquo;s running-man climber mascot in resin, on a mini carabiner.'),
 "g031": ('Gramicci', 'Climbing Tote', '$98', 'https://www.gramicci.com/products/climbing-tote-1',
   'Cordura nylon with daisy-chain webbing on the sides and an interior zip pocket. A range bag in disguise.'),
 "g032": ('Black Diamond', 'Stonehauler Athlete Tote', '$120', 'https://www.blackdiamondequipment.com/products/stonehauler-athlete-tote',
   'A 20-liter overbuilt daily tote for gear and everything else.'),
 "g033": ('Metolius', 'Climbers Tote', '$64.95', 'https://www.metoliusclimbing.com/products/climbers-tote',
   'Sized for a rope, shoes and harness, so it fits shoes, balls and a jacket easily.'),
 "g034": ('Organic Climbing', 'Quiver Tote', '$56', 'https://www.organicclimbing.com/products/quiver-tote',
   'Organic Climbing&rsquo;s refined take on its market tote. Handmade in Pennsylvania.'),
 "g035": ('Black Diamond', 'Capsule 20 Bouldering Bag', '$59.95', 'https://www.blackdiamondequipment.com/products/capsule-20-bouldering-bag',
   'A 20-liter organizer bag with zip compartments, made to ride inside a crash pad. Also good inside a golf bag.'),
 "g036": ('Tension Climbing', 'Figures Tote', '$35', 'https://www.tensionclimbing.com/products/figures-tote',
   'A denim tote printed with Tension&rsquo;s Figures graphic on one side and its logo on the other.'),
 "g070": ('g2g', 'Rope Tote', '$70', 'https://g2g.co/products/rope-tote',
   'A big black tote sized for a climbing rope, or a pair of shoes and a jacket.'),
}
SECTIONS = [
 ('The Pants', 'pants', ['g000', 'g003', 'g013', 'g061', 'g066', 'g071', 'g057'],
  '<strong>Seven pairs &middot; $110&ndash;$365</strong>Stretch, room in the knee and a belt you can cinch: everything a climbing pant needs, a golf swing needs too. Our pick, Gramicci, then four small climbing labels.'),
 ('Shirts and Layers', 'tops', ['g005', 'g015', 'g047', 'g060', 'g068', 'g050'],
  '<strong>Six pieces &middot; $99&ndash;$250</strong>A polo, two sun layers and three fleeces, all made for long days outside.'),
 ('Trail and Approach Shoes', 'shoes', ['g091', 'g087', 'g077', 'g079', 'g082', 'g095', 'g084'],
  '<strong>Seven pairs &middot; $185&ndash;$240</strong>Grippy, light and built for wet ground: the trail shoe as a spikeless golf shoe, plus an approach shoe made for the walk to the rock.'),
 ('Hardware: Carabiners, Belts and Brushes', 'hardware', ['g021', 'g022', 'g023', 'g024', 'g025', 'g026', 'g027', 'g028', 'g029', 'g030'],
  '<strong>10 pieces &middot; $7.95&ndash;$42</strong>Carabiners for towels and keys, web belts, and boar&rsquo;s-hair boulder brushes that clean grooves as well as holds.'),
 ('Totes and Bags', 'bags', ['g031', 'g032', 'g033', 'g034', 'g035', 'g036', 'g070'],
  '<strong>7 bags &middot; $35&ndash;$120</strong>Gear haulers that double as range or shoe bags.'),
]
N = 37
PQ = {}
BANDS = {
 "pants-after": ("In Motion", "Climbing pants doing what they were made for, from the brands&rsquo; own photography.",
   [("band-4", "A climber in a Gramicci sweatshirt and pants belaying from a rock ledge with a red rope", "Gramicci"),
    ("band-5", "A climber in a yellow shirt jamming up a dark crack", "Black Diamond"),
    ("band-6", "A man in a green g2g fleece sitting on grass while a friend leaps over him", "g2g")]),
 "tops-after": ("Layers at Work", "Fleeces, sun hoodies and shells on the wall and at the crag.",
   [("band-10", "A climber in a yellow fleece coiling a rope in a pine forest", "Metolius"),
    ("band-11", "A climber in a blue shirt on a streaked limestone wall", "Metolius"),
    ("band-12", "A climber in a red helmet high on a granite face", "Black Diamond")]),
 "shoes-after": ("On the Approach", "Approach and trail shoes on the ground they were built for.",
   [("band-7", "A man in an olive vest and pants striding across rocks in Scarpa approach shoes", "Scarpa"),
    ("band-8", "Two hikers with poles heading into a mountain valley", "Scarpa"),
    ("band-9", "A boulderer on a tall grey boulder on a heather moor", "Organic Climbing")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The pant that started this post was made for climbing. South2 West8&rsquo;s Trek Pant has the things a climber wants: a relaxed cut that lets you high-step onto a hold, a belt you can cinch with one hand, cuffs you can pull in. Those are also the things you want on a golf course, where you spend four hours walking, squatting to read putts and making a full turn.</p>
    <p><strong>Why climbing gear.</strong> Climbing clothes are built for movement and wear: stretch, gussets, reinforced knees and seats, quick-drying fabric. Golf clothes have spent years getting slimmer and shinier. The climbing version is roomier, tougher and, to us, better looking.</p>
    <p><strong>What is here.</strong> The most interesting pants, shirts and shoes we found, plus the small stuff. The pants come from South2 West8, Gramicci and four small climbing labels we had never covered: Hitorii from Los Angeles, g2g from Seattle, Looking For Wild from France and Rungne. The shirts are sun layers and fleeces, and the shoes are trail and approach shoes that grip wet grass like a spikeless golf shoe. Then come carabiners, belts and boar&rsquo;s-hair boulder brushes that clean a clubface as well as a hold, and totes built to haul ropes, which carry shoes and balls just as well.</p>
    <p>Golf brands have barely touched this yet. The only climbing piece we found from one was Metalwood Studio&rsquo;s $10 glow-in-the-dark carabiner.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>37</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>19</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$7.95&ndash;$390</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>S2W8 Trek Pant, $365</span></div>
      <div class="sidebar-detail"><span class="l">Best value</span><span>Metolius brush, $9.95</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>Checked Nov 14, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#ClimbingStyle</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#TrailShoes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
IDEA = ""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">Keep Going</div>
  <h2 class="products-hdr" id="more">More From the Outdoors</h2>
  <div class="writeup-body">
    <p>For golf gear for climbers, anglers and surfers, read <a href="/drops/golf-gear-for-climbers-anglers-techies-surfers">Golf Gear for Climbers, Anglers, Techies, Surfers and More</a>. For winter layers from Arc&rsquo;teryx, Goldwin and Salomon, see <a href="/drops/outdoor-brands-for-golf">Winter Golf Clothes From Outdoor Brands</a>, and for the brand that made its name on the climbing pant, our <a href="/drops/brand-to-know-gramicci">Brand to Know on Gramicci</a>.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/climbing-golf/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}.product-card[data-frames="1"] .pg-arw,.product-card[data-frames="1"] .pg-count,.product-card[data-frames="1"] .pg-dots{display:none!important}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle if handle.startswith("http") else SHOP + handle
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
            items.append({"@type": "ListItem", "position": pos, "url": (P[h][3] if P[h][3].startswith("http") else SHOP + P[h][3]), "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-14", "dateModified": "2026-11-14",
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
    <span>Drops &amp; Brands &middot; Climbing &middot; Trail</span><span class="dot"></span>
    <span>37 picks &middot; 19 brands &middot; prices checked November 14, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three action shots: a climber in a sun hoodie clipping a quickdraw on a crack, a man striding across rocks in Scarpa approach shoes, and a man stepping between boulders against the sun" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
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
