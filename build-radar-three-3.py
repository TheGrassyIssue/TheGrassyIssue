#!/usr/bin/env python3
"""build-radar-three-3.py — On Our Radar Vol. 3: Aberdeen West, We Hit Fairways, Grind City Golf. Cloned from build-hat-makers.py. 27 October 2026.
Lenny: "three small brands on our radar" (Apex swapped for Aberdeen West), then "I like the A4 colorway, add A13, add G12 then build the post".
FACTS: research/radar-three-3/*.json (live catalogues Oct 27, US-market prices via ?country=US) and pages/ (About pages).
No founder is named on Aberdeen West's or Grind City's sites; don't add one. We Hit Fairways names its four founders on its About page.
We Hit Fairways' home base isn't stated anywhere we could find; the store prices in NZD. Grind City's store prices in GBP and says it's print on demand.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "3 Small Golf Brands: Aberdeen West, We Hit Fairways, Grind City"
DESC = ("On our radar: Aberdeen West's satin jackets and golf shoes, We Hit Fairways' knit polos and Grind City's golf streetwear. "
        "Where each brand is heading, the trend they share and 27 picks with US prices.")
H1 = "On Our Radar: Three Small Golf Brands Bringing Back the Clubhouse Look"
BC = "Aberdeen West, We Hit Fairways, Grind City"
SLUG = "aberdeen-west-we-hit-fairways-grind-city"
IMG = "/images/radar-three-3"
SHOP = ""
AW, WH, GC = "Aberdeen West", "We Hit Fairways", "Grind City Golf"
AWU, WHU, GCU = "https://aberdeenwest.com/products/", "https://wehitfairways.com/products/", "https://grindcitygolf.com/products/"
P = {
 # Aberdeen West
 "aw-beige": (AW, "Satin Trucker Jacket, Beige", "$348", AWU+"beige-satin-trucker-jacket",
   "Our pick from Aberdeen West. Japanese satin in beige with green trim, two flap pockets on the chest and a huge embroidered flower spread across the back above the Aberdeen West name. The piece that tells you what the brand is about."),
 "aw-blacksatin": (AW, "Satin Trucker Jacket, Black", "$348", AWU+"black-satin-trucker-jacket",
   "The same jacket in black, which makes the white flowers on the back stand out even more. Relaxed fit, zip front, elastic hem."),
 "aw-nylon": (AW, "Nylon Pullover Jacket, Black", "$278", AWU+"black-nylon-pullover-jacket",
   "A V-neck pullover in a Japanese cotton-poly shell, with side zips to let air in, green-striped rib cuffs and a mesh lining. The old-school wind shirt, made sharper."),
 "aw-cardigan": (AW, "Cashmere Checker Cardigan", "$438", AWU+"100-cashmere-checker-cardigan",
   "100% cashmere in a navy and blue checkerboard, heavyweight, with custom buttons and a small embroidered A on the chest. The most expensive thing in the post, and the one that looks it."),
 "aw-polo": (AW, "Striped Knit Long Sleeve Polo, Brown", "$188", AWU+"brown-striped-knit-long-sleeve-polo",
   "Cotton knit in brown and cream stripes with a pink collar and rib cuffs. A long-sleeve polo that looks like it came out of a 1970s pro shop."),
 "aw-plaid": (AW, "Classic Plaid Pant", "$168", AWU+"classic-plaid-pant",
   "Brown plaid in a Japanese poly-rayon blend, single pleat, elastic waist and zip side pockets. The pant to wear with the satin jacket."),
 "aw-pine": (AW, "AW Wing Tip, Pine", "$288", AWU+"pine-aw-wing-tip",
   "A box calf golf wingtip in dark green with brogue detailing, a waterproofed leather lining and a studded AW outsole. Comes with a perforated carrying case and a shoehorn."),
 "aw-oxblood": (AW, "Ghost, Oxblood", "$300", AWU+"oxblood-ghost",
   "A patent oxblood penny loafer built as a golf shoe, on the same studded AW outsole with a star-pattern tread. The shoe most likely to get a comment on the first tee."),
 "aw-harmony": (AW, "Harmony, White", "$248", AWU+"harmony-white",
   "The modern option: a white mesh and synthetic leather golf sneaker with a stability shank and a multi-direction tread. Every size was in stock when we checked."),
 "aw-bag": (AW, "AW Golf Stand Bag", "$378", AWU+"aw-golf-stand-bag",
   "A brown and tan stand bag in a coated fabric the brand says looks like leather but weighs less, with zip pockets, a cross-back strap and a hood. 35 inches tall, just under six pounds."),
 # We Hit Fairways
 "wh-qzip": (WH, "Checkered Q-Zip, Mint Blue", "$115", WHU+"checkered-q-zip-mint-blue",
   "Our pick from We Hit Fairways. A brushed quarter-zip in pale mint with a checkered graphic across the chest. Warm without the bulk, and the checkerboard is the brand&rsquo;s signature."),
 "wh-cardigan": (WH, "Champion&rsquo;s Cardigan", "$129.50", WHU+"champions-cardigan-off-white",
   "Off-white with green trim, fine stripes and custom WHF buttons. The varsity-cardigan look, done in colors that suit a golf course."),
 "wh-sweater": (WH, "Tour Knit Sweater", "$105", WHU+"champions-knit-sweater-ivory",
   "An ivory crew with a green band and checkered detail across the chest, cut to sit closer to the body without getting in the way of a swing."),
 "wh-zip": (WH, "Signature Knit Zip Sweater, Oat", "$165", WHU+"signature-knit-zip-sweater-oat",
   "A full-zip knit in oat with a contrast zip and a subtle fairway pattern across the back. The quietest piece in the brand&rsquo;s range."),
 "wh-vneck": (WH, "Tour V-Neck Polo, Mustard", "$95", WHU+"tour-v-neck-polo-mustard",
   "A mustard polo with a V-neck and a piqu&eacute; collar tipped in burgundy. The color is the reason to buy it."),
 "wh-waffle": (WH, "Waffle Knit Polo, Clay Red", "$105", WHU+"waffle-knit-polo-clay-red",
   "Waffle-textured knit in clay red with a contrast placket, cut to be worn untucked. Three sizes left when we checked."),
 "wh-medalist": (WH, "Medalist Knit Polo, Sky Blue", "$110", WHU+"medalist-knit-polo-sky-blue",
   "Sky blue with a navy and white stripe across the chest. The brand calls it its take on a traditional course polo, made to be worn untucked."),
 "wh-lion": (WH, "Lion Cap, Green", "$40", WHU+"lion-cap-green",
   "A soft, unstructured cotton cap in green with a small embroidered lion on the front. The cheapest way into the brand."),
 # Grind City Golf
 "gc-cardigan": (GC, "The Unofficial Cardigan", "$102", GCU+"the-unofficial-cardigan-copy",
   "Our pick from Grind City. A pine green cardigan with a GC crest on the chest and script on the cuff. The brand&rsquo;s line on it: &ldquo;Golf doesn&rsquo;t always have to look like golf.&rdquo;"),
 "gc-sphere": (GC, "Sphere Study Crew Knit", "$100", GCU+"sphere-study-crew-knit",
   "A burgundy crew with half a giant golf ball knitted into the side and GC script on the sleeve. Relaxed fit, lightweight cotton blend."),
 "gc-floral": (GC, "Misfit In Bloom Knit Vest", "$87", GCU+"v-neck-copy",
   "A black sweater vest covered in big tan flowers, with GrindCity script knitted into the chest. The loudest piece in the post."),
 "gc-clubs": (GC, "Lost Property Knit Vest", "$87", GCU+"v-vest-1",
   "A taupe V-neck vest with two crossed clubs knitted on the front. Vintage-looking in the best way, and easy to wear over a white polo."),
 "gc-varsity": (GC, "Players Club Jacket", "$75", GCU+"two-tone-fleeced-varsity-jacket-1",
   "A coffee and cream varsity jacket with striped rib trims, a G on the chest and Grind City Golf across the back."),
 "gc-pinstripe": (GC, "Pinstripe Protocol Polo", "$52", GCU+"pinstripe-protocol-polo",
   "A relaxed pinstripe polo with a white collar, in navy, black or red. A baseball-jersey feel on a golf shirt."),
 "gc-track": (GC, "Club Check Jacket", "$71", GCU+"unisex-plaid-full-zip-track-jacket",
   "A light check jacket in apricot plaid, cut loose in woven cotton. A layer for a cool morning that works at the bar after."),
 "gc-barrel": (GC, "No.18 Barrel Leg Trousers", "$71", GCU+"men-s-barrel-leg-pants",
   "Barrel-leg golf trousers, roomy through the leg and tapering at the ankle, in coffee, gray green or black. The fit-forward pant the brand is built around."),
 "gc-lowfade": (GC, "Low Fade Polo", "$51", GCU+"low-fade-polo",
   "A boxy short-sleeve polo in navy or black with a small script logo. The easy one to start with."),
}
SECTIONS = [
 ("Aberdeen West", "aberdeen-west", ["aw-beige","aw-blacksatin","aw-nylon","aw-cardigan","aw-polo","aw-plaid","aw-pine","aw-oxblood","aw-harmony","aw-bag"],
  "<strong>Scotland meets Los Angeles &middot; ten picks &middot; $168&ndash;$438</strong>A small, premium range built around golf shoes, with satin jackets, knits and plaid pants around them. Prices in US dollars, as listed on the brand&rsquo;s store."),
 ("We Hit Fairways", "we-hit-fairways", ["wh-qzip","wh-cardigan","wh-sweater","wh-zip","wh-vneck","wh-waffle","wh-medalist","wh-lion"],
  "<strong>Four friends &middot; eight picks &middot; $40&ndash;$165</strong>Knit polos, sweaters and caps, many with a checkerboard or lion. The store prices in New Zealand dollars but sets its own US prices, which are the ones shown here."),
 ("Grind City Golf", "grind-city-golf", ["gc-cardigan","gc-sphere","gc-floral","gc-clubs","gc-varsity","gc-pinstripe","gc-track","gc-barrel","gc-lowfade"],
  "<strong>UK &middot; nine picks &middot; $51&ndash;$102</strong>Golf streetwear: boxy polos, knit vests, a varsity jacket and barrel-leg trousers. The store prices in pounds and sets its own US prices, shown here. Every piece is made to order."),
]
N = 27
PQ = {
 "aberdeen-west": ("Inspired by the storied fairways of Aberdeen, Scotland, and the dynamic energy of Los Angeles.", "Aberdeen West, on its About page"),
 "we-hit-fairways": ("Built by people who love golf and know it doesn&rsquo;t always love them back.", "We Hit Fairways, on its About page"),
 "grind-city-golf": ("Golf doesn&rsquo;t always have to look like golf.", "Grind City Golf, on The Unofficial Cardigan"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "aberdeen-west": ("From Aberdeen West", "The jackets at golden hour and the shoes on the course.", [("band-1","A man from behind at sunset in a cream Aberdeen West jacket with West across the back","Golden hour"),("band-2","Black Aberdeen West Ghost loafers on a cobblestone path","The Ghost"),("band-3","Aberdeen West Harmony golf sneakers in white and black lying on a putting green","On the green")]),
 "we-hit-fairways": ("From We Hit Fairways", "The founders on the course, the vest and the caps.", [("band-4","Four golfers in We Hit Fairways caps and knits crouched together on a green, laughing","The crew"),("band-5","A golfer in a black puffer vest with a green stripe over a light blue shirt, carrying a bag on a course","The vest"),("band-6","Three We Hit Fairways caps in white and green lying in the grass","The caps")]),
 "grind-city-golf": ("From Grind City Golf", "The knits, the quarter-zip and the dress.", [("band-7","A young man in a cream Grind City quarter-zip, green trousers and a brown cap sitting on a wooden bench","The bench"),("band-8","A woman in a green Grind City collared tennis dress","The dress"),("band-9","A man in the burgundy Sphere Study crew knit and a navy GC cap","The knit")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three small brands, three very different price points, and the same idea running through all of them. Look at what each one is putting at the front of its store this fall: satin and varsity jackets, cardigans with crests, striped knit polos, sweater vests and checkerboards. This is the clubhouse look of the 1970s, &rsquo;80s and &rsquo;90s coming back, and it is coming back through small brands first.</p>
    <p><strong>Aberdeen West</strong> is the dressiest of the three. It describes itself as born from the traditions of golf, inspired by Aberdeen in Scotland and by Los Angeles, at &ldquo;the intersection of luxury, athleisure, and vintage aesthetics.&rdquo; What stands out is that it starts with shoes. Wingtips, a patent penny loafer called the Ghost and a mesh sneaker all sit on the same studded golf outsole, and the dress shoes come with a carrying case and a shoehorn. Around them is a short, tight range: embroidered satin jackets, a cashmere cardigan, plaid pants and a leather-look stand bag. Thirty-two products in all, every one in stock when we checked. It also lists authorized distributors on its site, which tells you it is selling to shops as well as directly. The brand doesn&rsquo;t name its founders, so we won&rsquo;t either.</p>
    <p><strong>We Hit Fairways</strong> is the most golf of the three, and the most personal. Its About page names the four friends who run it, Tae &ldquo;Taco&rdquo; Koh, Harry &ldquo;Dimchae&rdquo; Na, Sam Heung Min and Luke &ldquo;Tooms&rdquo; Toomey, and says they wanted to build &ldquo;something they&rsquo;d actually want to wear.&rdquo; The clothes are knit polos, a checkered quarter-zip and a Champions collection with a cardigan and sweater in cream and green. The store prices in New Zealand dollars but sets separate, rounder prices for US shoppers: a cap that is NZ$65 at home is $40 here. That is a small brand deciding the US is a market, not an afterthought.</p>
    <p><strong>Grind City Golf</strong> is the streetwear end. It calls itself &ldquo;modern golf streetwear that belongs on the course and beyond it,&rdquo; and the range is big for a small brand: 176 products in stock, from boxy polos and barrel-leg trousers to a women&rsquo;s line of polos, skirts and tennis dresses. Its About page also says every product is &ldquo;custom and printed on demand&rdquo; and made to order. That keeps prices low, between about $50 and $100 for our picks, and means the range can be huge. It also means we would buy one piece first and check the fit and quality before going further. Our picks lean on the knits, which are where the brand&rsquo;s designs are strongest.</p>
    <h2 class="products-hdr" style="margin-top:32px">The Trend They Share</h2>
    <p><strong>The clubhouse look is back.</strong> Varsity jackets, crests, cardigans and sweater vests are in all three ranges. The reference point is the old pro shop, not the skate park.</p>
    <p><strong>Outfits, not single pieces.</strong> Aberdeen West sells the jacket, the pant and the shoe. We Hit Fairways builds its Champions pieces in one cream and green palette, made to be worn together. Grind City shoots most of its pieces on a model in a full look. All three are selling a way to dress for the round and the drink after it.</p>
    <p><strong>Small brands are courting US buyers.</strong> Two of the three are not priced in dollars at home, and both set their own US prices rather than leaving it to a currency converter.</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>Aberdeen West is for the golfer who dresses up for the round.</strong> Start with the shoes, then the satin jacket if you want people to ask where it&rsquo;s from.</p>
    <p><strong>We Hit Fairways is for the golfer who wants clean, classic knits at a fair price.</strong> The quarter-zip and the knit polos are the place to start.</p>
    <p><strong>Grind City is for the golfer who wants something louder for less.</strong> Buy one knit or vest first and see how it fits.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Aberdeen West</span><span>Scotland meets LA</span></div>
      <div class="sidebar-detail"><span class="l">We Hit Fairways</span><span>Run by four friends</span></div>
      <div class="sidebar-detail"><span class="l">Grind City Golf</span><span>UK, made to order</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$40&ndash;$438</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Satin Trucker Jacket, Checkered Q-Zip, The Unofficial Cardigan</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#AberdeenWest</span>
        <span class="hashtag">#WeHitFairways</span>
        <span class="hashtag">#GrindCityGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is Aberdeen West?", "A golf brand inspired by Aberdeen, Scotland and Los Angeles that makes golf shoes, satin jackets, knits, pants and bags. On October 27, 2026 its golf shoes were $248 to $300 and its jackets $278 to $348."),
 ("Who is behind We Hit Fairways?", "Four friends named on its About page: Tae Koh (CEO), Harry Na (operations), Sam Heung Min (launches and shoots) and Luke Toomey (brand and content). Its store prices in New Zealand dollars and sets separate US prices."),
 ("Does We Hit Fairways ship to the US?", "Its store sets US-dollar prices for US shoppers, for example $40 for a cap and $115 for the Checkered Q-Zip on October 27, 2026. Check shipping costs and times at checkout."),
 ("Is Grind City Golf print on demand?", "Yes. Its About page says all of its products are custom and printed on demand, made to order. The store prices in pounds and shows US prices, about $50 to $100 for most polos, knits and trousers."),
 ("Which of the three should I buy first?", "Aberdeen West's golf shoes if you want to dress up, We Hit Fairways' Checkered Q-Zip or a knit polo for classic golf clothes, and one Grind City knit or vest if you want something louder for less."),
]
FRN = json.loads((ROOT / "research/radar-three-3/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-27", "dateModified": "2026-10-27",
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
    <span>On Our Radar</span><span class="dot"></span>
    <span>27 picks &middot; prices checked October 27, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: Aberdeen West golf sneakers on a putting green, four We Hit Fairways founders crouched on a green, and a man in a cream Grind City quarter-zip on a bench" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Three Putt", "Tarraing", "Rebolf", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
