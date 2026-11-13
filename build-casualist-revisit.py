#!/usr/bin/env python3
"""build-casualist-revisit.py — Brand Revisited: Casualist. 13 November 2026. Cloned from build-siegelman-revisit.py.
Lenny: "let's do the brand revisited -Casualist" -> options sheet (27) -> "build it" (no picks named: every in-stock piece, colors merged per product, plus the sold-out Mogshade headcover).
FACTS: casualist.com products.json/.js (USD shown to US visitors, read 13 Nov 2026); homepage (Black Friday bundles, 10% code CASUAL10, Round 1 copy);
wool headcovers = collab with Mogshade (product page). History from our May 28 Brand to Know. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Casualist Revisited: Black Friday Kits, the Story So Far and What to Wear With It"
DESC = ("Back to Casualist: three new outfit bundles for Black Friday, beige pleated trousers, wool headcovers made with Mogshade "
        "the idea and history behind the brand, and 25 picks including what to wear with it, with US prices.")
H1 = "Brand Revisited: Casualist"
BC = "Brand Revisited: Casualist"
SLUG = "brand-revisited-casualist"
IMG = "/images/casualist-revisit"
SHOP = "https://casualist.com/products/"
C = "Casualist"
S_ = '<s style="opacity:.5">'
P = {
 "k2": (C, "The Full Round", "$345 " + S_ + "$411</s>", "the-full-round",
   "Our pick. The whole uniform in one box: a Weekend Pique Polo, the pleated trousers in beige or taupe and a cap. Casualist says it has everything you need for 18 holes, minus the ability to actually play them well. $66 less than buying the three separately."),
 "k3": (C, "The Clubhouse Kit", "$297 " + S_ + "$370</s>", "the-club-house-kit",
   "The Grazer merino cardigan vest in yellow with the All The Gear, No Idea tee. The off-course version of the brand, for after the round. $73 off the two pieces bought separately."),
 "k4": (C, "The Weekend Kit", "$161 " + S_ + "$195</s>", "the-weekend-kit",
   "The Weekend Pique Polo with a Casualist cap. The easiest way in, and the one most likely to be worn twice a week."),
 "k1": (C, "Pleated Golf Trousers, Beige and Taupe", "$199&ndash;$216", "pleated-golf-trousers-organic-cotton-copy",
   "New in beige on November 4, alongside the taupe we have written about before. Organic cotton twill with a high waist, clean front pleats, a hidden drawstring and a straight leg. Made in Portugal. The beige lists at $216, the taupe at $199."),
 "k5": ("Casualist x Mogshade", "Wool Headcovers", "$112 &middot; sold out", "wool-headcovers",
   "Made with Mogshade from rescued Portuguese wool, woven at mills in the Serra da Estrela mountains, with a deadstock fleece lining. A driver and a 3-wood cover, released October 13 and already gone. Watch for a restock."),
 "k6": (C, "Grazer Cardigan Vest", "$250", "grazer-cardigan-vest",
   "A throwback layer in 100% merino with a button front, the logo and mascot embroidered on the chest and a caption on the back. We have shown the grey plenty of times; the yellow is the one from the fall campaign."),
 "k7": (C, "All The Gear Sweatshirt", "$140", "all-the-gear-sweatshirt",
   "A 380gsm cotton crewneck with an embroidered logo on the chest and ALL THE GEAR, NO IDEA printed across the back. Made in Portugal."),
 "k8": (C, "Cart Path Ripstop Jacket", "$339", "cart-path-ripstop-jacket",
   "A light ripstop jacket with a vented back and an adjustable waist cord. For the course, the car park and the pub, in that order."),
 "k9": (C, "Windbreaker Coach Jacket, Archive", "$120", "winbreaker-1",
   "From the Casual Pro days: a water-resistant navy coach jacket with CASUAL PRO across the back. Light enough to pack, and the cheapest jacket in the shop."),
 "k10": (C, "Trust the Swing Long-Sleeve Polo", "$140", "trust-the-swing-pique-polo-olive",
   "A long-sleeve pique polo with a rounded retro collar and a relaxed fit, in olive or dusty blue. Made in Portugal. The one to reach for on a cool morning."),
 "k11": (C, "Weekend Pique Polo", "$129", "weekend-pique-polo-ecru",
   "Organic cotton pique with raglan sleeves, a relaxed retro fit and a contrast collar. Ecru with olive, or mocha. The polo inside two of the three kits."),
 "k12": (C, "Dress Code Mockneck Tee", "$115", "appropriate-dress-code-mockneck-tee-ecru",
   "Smooth organic interlock cotton with a mock neck that gets past most dress codes, raglan sleeves and a printed logo. Ecru or dusty blue. Made in Portugal."),
 "k13": (C, "No Idea Heavy Tee", "$95", "heavy-tee-agni",
   "A heavyweight organic cotton tee with a relaxed fit and the swing motif on the label. The tee from the Clubhouse Kit."),
 "k14": (C, "Good Enough Tee", "$95", "good-enough-tee",
   "380gsm organic cotton, cut oversized, with the logo front and back and an illustrated print on the back. Made in Portugal."),
 "k15": (C, "Legacy Wool 5 Panel Cap", "$60", "legacy-wool-5-panel-cap",
   "Soft wool tartan with a rope across the front and the C logo. Taupe is in stock; the dark brown has sold out."),
 "k16": (C, "Legacy Velvet 5 Panel Cap", "$60", "legacy-velvet-5-panel-cap",
   "The same shape in royal blue cotton velvet, with a rope detail and the C logo. The cap in most of the campaign photos."),
 "k17": (C, "Casual 5 Panel Ripstop Cap", "$60", "casual-5-panels-ripstop-cap-olive",
   "Light ripstop with a buckle back and casual stitched across the front. Olive or yellow."),
 "k18": (C, "Two Tone Course Cap", "$60", "two-tone-course-cap",
   "A low-profile, flat-brim cap based on old baseball hats, with Leisure Goods, West London under the script. Cream with a green brim."),
 "k19": (C, "Casual Pro Snapback, Leisure Hats OG", "$45", "leisure-hats",
   "The best seller, still carrying the old name: CASUAL PRO, SINCE 2023, MELB &ndash; LDN &ndash; LA. Recycled quick-dry nylon, made to order, 10 to 14 days to arrive."),
}

# Wear it with: other brands, prices read 13 Nov 2026 on each brand's own site (USD shown to US visitors)
RA = "Royal Albartross"
P.update({
 "w1": (RA, "Sanderson, Chestnut Suede", "$180", "https://us.albartross.com/products/sanderson-chestnut-suede-mens-spikeless-golf-shoe",
   "London&rsquo;s golf shoe brand, and the easiest match for Casualist&rsquo;s browns and taupes: an Italian suede sneaker on a spikeless sole, made to go from the course to the pub without changing. Wear it with the taupe trousers and the mocha polo."),
 "w2": (RA, "Tailor Brogue, White", "$250", "https://us.albartross.com/products/tailor-white-mens-spikeless-brogue-golf-shoes",
   "A spikeless wingtip handcrafted in Portugal from Italian leather, like most of Casualist&rsquo;s clothes. The dressier option, for the beige trousers and a Weekend polo."),
 "w3": ("Mogshade", "Houndstooth Autumn Headcover", "$103", "https://www.mogshadegolf.com/products/dogtooth-autumn-headcover",
   "From Casualist&rsquo;s headcover partner, and in stock while the collab is not: the same rescued Serra da Estrela wool and fleece lining, in a brown and cream houndstooth from the October 23 drop."),
 "w4": ("Fyfe Golf", "Glamis Harris Tweed Headcover", "$89", "https://www.fyfegolf.com/products/glamis-harris-tweed-headcover",
   "A dark check Harris Tweed woven in the Outer Hebrides, lined in green fleece and made in Scotland. The British-heritage half of the look, for the Legacy wool cap and a grey Grazer vest."),
 "w5": ("Jones Sports Co.", "Original Jones Bag, Navy/White", "$111 " + S_ + "$185</s>", "https://www.jonessportsco.com/products/original-jones-bag-navy-white",
   "The single-strap carry bag Jones has made since 1971, in water-resistant nylon with three pockets. Unstructured and simple, the way Casualist wants golf to feel, and on sale right now."),
 "w6": ("Smathers &amp; Branson", "Golf Tee Pattern Belt", "$195", "https://smathersandbranson.com/products/golf-tee-pattern-belt",
   "A hand-stitched needlepoint belt in dark navy with white tees, on Italian leather with a brass buckle. Casualist&rsquo;s dry humor, in belt form, and it sits right on a high-waisted pleated trouser."),
})
SECTIONS = [
 ("New for Fall: The Kits", "kits", ["k2", "k3", "k4", "k1", "k5"],
  "<strong>Five pieces &middot; $112&ndash;$345</strong>Three outfit bundles priced below the pieces on their own, a new trouser color and a collab that sold out."),
 ("Layers and Jackets", "layers", ["k6", "k7", "k8", "k9"],
  "<strong>Four pieces &middot; $120&ndash;$339</strong>For a cold first tee and the drive home."),
 ("Polos and Tees", "tops", ["k10", "k11", "k12", "k13", "k14"],
  "<strong>Five pieces &middot; $95&ndash;$140</strong>Most made in Portugal from organic cotton."),
 ("Caps", "caps", ["k15", "k16", "k17", "k18", "k19"],
  "<strong>Five pieces &middot; $45&ndash;$60</strong>Wool, velvet, ripstop and the snapback that started it."),
 ("Wear It With", "pairs", ["w1", "w2", "w3", "w4", "w5", "w6"],
  "<strong>Six pieces from other brands &middot; $89&ndash;$250</strong>Casualist does not make shoes, bags, belts or headcovers you can buy right now. These are the ones we would put with it."),
]
N = 25
PQ = {
 "layers": ("Not much was planned. There was golf. There were good looks. A few pints and lots of laughter.", "Casualist, on the Round 1 collection"),
}
BANDS = {
 "kits-after": ("Round 1", "From Casualist&rsquo;s fall campaign by the sea.",
   [("band-1", "A golfer in a brown Casualist polo, cream pleated trousers and a blue cap walking off a green", "On the green"),
    ("band-2", "A man carrying a canvas golf bag along a seafront railing in a Casualist cap and cream trousers", "The walk"),
    ("band-3", "A gloved hand teeing up a ball with a Casual Pro logo", "Casual Pro, 2024")]),
 "layers-after": ("By the Sea", "More from Round 1.",
   [("band-4", "A man in a light blue Casualist tee and royal blue cap on a pebble beach, seen from behind", "The pebble beach"),
    ("band-5", "Two golfers in Casualist caps, one blue and one yellow, looking down at something together", "Between shots"),
    ("band-6", "A close-up of a light blue mockneck tee tucked into cream pleated trousers", "Tucked in")]),
 "tops-after": ("Around Town", "The other half of the brand: West London, after the round.",
   [("band-7", "A man in an ecru Weekend polo and cream cap adjusting his collar in front of an ivy wall", "The Weekend polo"),
    ("band-8", "A man in a green Casualist cap and pale tee in front of a green garage door", "The ripstop cap"),
    ("band-9", "A yellow casual cap resting on a green velvet chair", "Off duty")]),
 "caps-after": ("The Casual Pro Years", "From before the rename, when the brand was still Casual Pro.",
   [("band-10", "A man in an olive Casual Pro snapback and black Casual Pro polo on a golf course", "The original snapback"),
    ("band-11", "Five Casual Pro snapbacks hanging on a tennis net over a clay court", "Every color"),
    ("band-12", "A hand holding a stack of snapback straps in olive, white, navy and brown on a clay court", "Leisure Hats OG")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We wrote about Casualist in May: the West London label that started life in Melbourne as Casual Pro, makes most of its clothes in Portugal and still sells the old snapback with the old name on it. Six months on, the range has not grown much, but the way it is sold has.</p>
    <p><strong>The kits.</strong> On November 11, Casualist put its clothes together into three outfits and priced them under the pieces bought separately: The Full Round (polo, pleated trousers and cap) at $345, The Clubhouse Kit (cardigan vest and tee) at $297 and The Weekend Kit (polo and cap) at $161. They are the brand&rsquo;s Black Friday offer, and the shop is also taking 10% off with the code CASUAL10.</p>
    <p><strong>What else is new.</strong> The pleated trousers, the piece we have recommended most, now come in beige as well as taupe. In October, Casualist and Mogshade made wool headcovers from leftover Portuguese wool, and they sold out. The fall campaign, called Round 1, was shot by the English seaside, and it is where most of the photos below come from.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">What&rsquo;s New</div>
      <div class="sidebar-detail"><span class="l">Headcovers</span><span>Oct 13, with Mogshade</span></div>
      <div class="sidebar-detail"><span class="l">Beige trousers</span><span>Nov 4</span></div>
      <div class="sidebar-detail"><span class="l">Kits</span><span>Nov 11</span></div>
      <div class="sidebar-detail"><span class="l">Black Friday</span><span>10% off, CASUAL10</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$45&ndash;$345</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Full Round</span></div>
      <div class="hashtags">
        <span class="hashtag">#Casualist</span>
        <span class="hashtag">#WestLondon</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
IDEA = """
<section class="products" data-btk="idea" style="margin-top:8px;padding-bottom:24px">
  <div class="drop-tag grass">The Idea</div>
  <h2 class="products-hdr" id="idea">What Casualist Is Going For</h2>
  <div class="writeup-body">
    <p>Casualist&rsquo;s own account of how it started is short: there was golf, there were good looks, a few pints, a lot of laughter, and a sense that nothing on the market fit the way its people wanted to play. It names who it is not for, &ldquo;not the serious players, not the performance crowd,&rdquo; and who it is for: the golfer who cares how he looks without caring too much about the scorecard, and who shows up in a proper cardigan on a drizzly Tuesday morning and means it.</p>
    <p>The line the brand keeps coming back to is that elegance and irreverence are not opposites. You can see both in the clothes. The elegance is in the construction: organic cotton pique, 100% merino, pleated trousers with a high waist, most of it made in Portugal and chosen, the brand says, for how it feels after a full round rather than how it photographs. The irreverence is in the words: ALL THE GEAR, NO IDEA across the back of a sweatshirt, a tee called Good Enough, product copy promising a uniform for 18 holes &ldquo;minus the ability to actually play them well.&rdquo;</p>
    <p>Before anything is made, the team asks one question: would we wear this properly and repeatedly, not once and not for the photos? That is why the range is small, fewer than 30 products, and why so little of it changes from season to season. The kits are the clearest version of the idea: the same few pieces, worn together, every week.</p>
    <p><strong>Where it sits.</strong> Among the small British labels we follow, Manors is the heritage one, Sounder the technical one, Fyfe the Scottish accessory maker. Casualist is the one with the softest collar and the driest joke. It is closer in spirit to an American brand like Radmor or Sugarloaf Social Club than to anything with a crest, which makes sense for a label that started in Melbourne.</p>
  </div>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">From Casual Pro to Casualist</h2>
  <div class="writeup-body">
    <p><strong>Melbourne.</strong> The brand started in Australia as Casual Pro. The original snapback still says so: CASUAL PRO, SINCE 2023, LEISURE APPAREL, MELB &ndash; LDN &ndash; LA. The idea from the start was a label built on soft collars and jokes, for golfers who did not want to dress like a tour pro.</p>
    <p><strong>London, 2024.</strong> On April 2, 2024, the Casual Pro team announced the brand was moving &ldquo;from the sunny shores of Melbourne, Australia, to the historic streets of London, UK.&rdquo; They were open about the bet: Australian and American golf is relaxed about dress codes, and in Britain &ldquo;tradition still holds sway, and golfers tend to stick to more formal attire.&rdquo; A brand built on humor was moving to the strictest dress codes in the game, and its answer was to keep the jokes and add the things that get you through the clubhouse door: collars, merino, pleats.</p>
    <p><strong>Casualist.</strong> The rename came after the move. The founder, Elie Reboul, explains it on the about page in two sentences: the spirit was right, but the name needed to grow up a little, and Casualist is the next step, with sharper details, better quality and a clearer point of view. He kept the old snapback on sale anyway, and it is still the best seller. The navy coach jacket with CASUAL PRO across the back is still listed, under Archive.</p>
    <p><strong>Now.</strong> Everything is designed in West London and most of it is made in Portugal. This fall brought the Round 1 campaign by the sea, a headcover collab with Mogshade made from leftover Portuguese wool, a second color of the pleated trouser and, for Black Friday, the three kits. Elie signs off the about page with a welcome to &ldquo;the enthusiasts,&rdquo; the ones who play for the joy of it and know that nobody really needs to know your handicap.</p>
    <p>For the original profile, read our <a href="/drops/brand-to-know-casualist">Brand to Know on Casualist</a>. For more on the headcover partner, see our <a href="/brands/mogshade">Mogshade brand page</a>, and for the rest of the British independents, <a href="/drops/uk-independent-golf-brands">our UK brands post</a>.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/casualist-revisit/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-13", "dateModified": "2026-11-13",
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
    <span>Brand Revisited &middot; West London &middot; Made in Portugal</span><span class="dot"></span>
    <span>25 picks &middot; prices checked November 13, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a yellow Casualist cardigan vest and cream cap at the top of his swing against a pale evening sky" fetchpriority="high" /></div></div>
"""
    body += TAKE + IDEA  # Lenny 28 Oct: the story closes the post in place of The Questions
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
