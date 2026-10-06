#!/usr/bin/env python3
"""build-slice-town-btk.py — Brand to Know: SLICE TOWN (cloned from build-golden-hour-btk.py). 6 October 2026.
Lenny: "let's do a brand to know; https://slice-town.com/". Options sheet: recommended 18, hero H (the yellow
balaclava), then "add S20, 22 and 23 in the same box, 24,26" — 22 cards, the two Nalgene bottles sharing one.
FACTS: catalogue, SEK prices, stock and the store's own USD prices from slice-town.com on 6 Oct 2026
(research/slice-town/options.json). Story from the brand's own About, FAQ, Stockists and events pages; quotes verbatim.
PHOTOS: SLICE TOWN's own store and site images, localised to /images/slice-town (research/slice-town/make_frames.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "SLICE TOWN: Scandinavian Golf Streetwear Made for the Rough"
DESC = ("Brand to Know: SLICE TOWN, golf streetwear started in 2024 by a Dane and a Swede. Nylon track suits, boxy "
        "polos, tech pants, caps and a yellow balaclava, with prices.")
H1 = "Brand to Know: SLICE TOWN &mdash; Golf Streetwear Made for the Rough"
BC = "SLICE TOWN"
SLUG = "brand-to-know-slice-town"
IMG = "/images/slice-town"
SHOP = "https://slice-town.com/products/"
A = "SLICE TOWN"
P = {
 "S05": (A, "Golf Track Jacket, Cobalt", "1,750 kr (~$190)", "track-jacket-cobalt",
   "This is a wide-fit nylon track jacket with a high collar, a double front zip and white piping across the chest and down the sleeves. ST. is stitched on the chest with the brand mascot sitting in the full stop, and a big golf ball is printed across the back. M to XL in stock."),
 "S06": (A, "Golf Track Jacket, Slate", "1,750 kr (~$190)", "track-jacket-slate",
   "The same jacket in slate grey with yellow piping, which is the colour we would pick. It has zip side pockets and an airflow opening across the back yoke, so it breathes on a warm range session. M to XL in stock."),
 "S03": (A, "Golf Track Pants, Cobalt", "1,500 kr (~$160)", "track-pants-cobalt",
   "These are wide-leg nylon track pants with an elastic waist, an inner lining and white piping down the sides. The brand says they run extra wide and suggests sizing down for a closer fit. S to XL in stock."),
 "S04": (A, "Golf Track Pants, Slate", "1,500 kr (~$160)", "track-pants-slate",
   "The slate pants with yellow piping, to go with the slate jacket. There are side pockets and hidden zips on the back pockets, and the ST. logo is printed on the right leg. M to XL in stock."),
 "S08": (A, "Short Sleeve Windbreaker, Charcoal", "1,250 kr (~$135)", "short-sleeve-windbreaker-charcoal",
   "This is a boxy short-sleeve windbreaker in nylon and spandex, with a quarter zip, two stripes over the shoulders and a reflective SLICE TOWN logo on the chest and back. It is cut big enough to wear over a long-sleeve tee and matches the Retro Sports Shorts. S to L in stock."),
 "S09": (A, "Quarter Zip Polo, Brown", "850 kr (~$95)", "quarter-zip-polo-brown",
   "This is a cropped, boxy short-sleeve polo in a wool blend with a steel quarter zip, a spread collar and a welted chest pocket with the SLICE TOWN emblem. It matches the Wide Pleated Pants for a brown set. M to XL in stock."),
 "S11": (A, "Button Down Shirt, Charcoal", "1,250 kr (~$135)", "cropped-button-down-shirt-charcoal",
   "This is a boxy short-sleeve shirt in cotton satin with black buttons and a yellow label at the hem. The back carries a big ST. outlined in reflective silver, which lights up in a car&rsquo;s headlights on the walk back to the lot. S to XL in stock."),
 "S02": (A, "Long Sleeve Tee, Dusty Cobalt", "600 kr (~$65)", "long-sleeve-tee-cobalt",
   "This is a heavy 253gsm cotton long-sleeve in a washed blue, with contrast topstitching that crosses the chest and runs down the sides. It is the layer to wear under the short-sleeve windbreaker. S to XL in stock."),
 "S27": (A, "Relaxed Fit Tee, Black", "600 kr (~$65)", "black-slice-tee",
   "This is a boxy black tee in midweight cotton with the brand&rsquo;s sliced logo screenprinted big down the back. It is the shirt in most of SLICE TOWN&rsquo;s photos, including the one on the fairway. S to XL in stock."),
 "S20": (A, "Regular Fit Tee, Black", "500 kr (~$55)", "regular-fit-tee-black",
   "The regular-fit tee is the plain one, closer to the body than the relaxed cut, in midweight cotton with a small SLICE TOWN logo printed on the chest and nothing on the back. S to XL in stock."),
 "S21": (A, "Regular Fit Tee, White", "500 kr (~$55)", "regular-fit-tee-white",
   "This is the same regular-fit tee in white, with the small chest logo. The brand shoots it with the dark navy tech pants. S to XL in stock."),
 "S26": (A, "Relaxed Fit Tee, White", "600 kr (~$65)", "white-slice-tee",
   "This is the relaxed tee in white, with the logo on the front and the sliced SLICE TOWN logo across the back. Only a medium was left when we checked."),
 "S10": (A, "Wide Pleated Pants, Brown", "1,700 kr (~$185)", "wide-pleated-pants-brown",
   "These wide-leg trousers come in the same wool blend as the brown polo, with single front pleats, a high waist and belt loops. The brand says they run long and wide in the waist and suggests sizing down. S to XL in stock."),
 "S07": (A, "Retro Sports Shorts, Charcoal", "750 kr (~$85)", "retro-sports-shorts-charcoal",
   "These are nylon and spandex shorts with an elastic waist, reflective stripes down the sides, zip pockets and a yellow flag label at the hem. They are made to go with the short-sleeve windbreaker. S to XL in stock."),
 "S25": (A, "Straight Fit Tech Pants, Charcoal", "900 kr (~$98)", "tech-pants",
   "These are straight-fit stretch pants in nylon and spandex with zipped back pockets, zips at the ankles and front pockets the brand describes as deep enough for &ldquo;2 cans or a tall boy in each.&rdquo; Only S and M were left."),
 "S24": (A, "Straight Fit Tech Pants, Dark Navy", "900 kr (~$98)", "straight-fit-tech-pants-dark-navy",
   "These are the same tech pants in dark navy, shot by the brand on the course with a cap and a black tee. Also down to S and M."),
 "S14": (A, "Reflective Logo Sports Cap", "600 kr (~$65)", "reflective-logo-sports-cap",
   "This is a light charcoal five-panel cap from the &ldquo;Autumn is coming&rdquo; drop, with the SLICE TOWN logo stitched across the front in reflective thread and an orange label. Adjustable strap."),
 "S13": (A, "Trucker Cap", "650 kr (~$70)", "trucker-cap",
   "This is a charcoal five-panel trucker from the same drop, with SLICE TOWN stitched over a line of Spanish text and orange contrast stitching. Cotton, with a velcro strap."),
 "S15": (A, "Canvas Logo Cap, Brown", "385 kr (~$42)", "canvas-logo-cap-brown",
   "This is a brown cotton canvas six-panel with SLICE TOWN stitched across the front and a curved brim. At 385 kr it is the cheapest way into the brand&rsquo;s headwear."),
 "S28": (A, "Black Leather Golf Glove", "300 kr (~$35)", "black-golf-glove",
   "This is a black cabretta leather glove for right-handed golfers, with the SLICE TOWN emblem on the velcro tab. The brand&rsquo;s pitch is simple: &ldquo;Don&rsquo;t be a normie.&rdquo; S to XL, including M/L."),
 "S12": (A, "Butterfly Pitch Repair Tool", "300 kr (~$35)", "butterfly-divot-tool",
   "This is a stainless steel divot tool that folds open like a butterfly knife, with a gunmetal finish. A new batch was on pre-order when we checked."),
 "NAL": (A, "Nalgene Bottle, 1L, Bordeaux or Denim", "275 kr (~$30)", "bordeaux-nalgene-bottle-1l",
   "This is a litre Nalgene, BPA and BPS free, with a big SLICE TOWN swirl printed on it, in bordeaux with a yellow cap or in denim blue. Swipe for both; the Shop link opens the bordeaux, and the denim is <a href=\"https://slice-town.com/products/blue-nalgene-bottle-1l\" target=\"_blank\" rel=\"noopener\">here</a>."),
 "S01": (A, "Knitted Golf Balaclava, Yellow", "2,200 kr (~$240)", "knitted-golf-balaclava",
   "The most expensive thing on the store and the best joke in golf this year: a yellow knitted balaclava with a SLICE TOWN flag label on the chin. The brand&rsquo;s description: &ldquo;For when your game&rsquo;s so bad, you need full anonymity.&rdquo;"),
}
SECTIONS = [
 ("Track Suits", "track-suits", ["S05","S06","S03","S04"],
  "<strong>Four picks &middot; ~$160&ndash;$190</strong>The track suit is the centre of the range: light 135gsm nylon, a wide cut, piping down the arms and legs, and a golf ball printed across the back of the jacket. It comes in cobalt with white piping or slate with yellow. Wear the set to the range, or split it and wear the jacket over a tee."),
 ("Shirts and Layers", "shirts-and-layers", ["S08","S09","S11","S02"],
  "<strong>Four picks &middot; ~$65&ndash;$135</strong>Everything here is cut short and boxy. The short-sleeve windbreaker and the cotton satin button-down both have reflective logos, the brown polo is a wool blend that matches the pleated pants, and the cobalt long-sleeve goes under all of them."),
 ("Tees", "tees", ["S27","S20","S26","S21"],
  "<strong>Four picks &middot; ~$55&ndash;$65</strong>Every tee SLICE TOWN makes, all in midweight cotton. The relaxed fit is boxy, with the sliced logo printed big down the back; the regular fit is closer cut, with just a small logo on the chest. Both come in black and white."),
 ("Pants and Shorts", "pants-and-shorts", ["S10","S07","S25","S24"],
  "<strong>Four picks &middot; ~$85&ndash;$185</strong>There are no chinos here. The brown pleated trousers are the dressy pair, the tech pants are the everyday pair with pockets for a beer each, and the nylon shorts finish the windbreaker set. Several of these run long or wide, so read the brand&rsquo;s size notes."),
 ("Caps", "caps", ["S14","S13","S15"],
  "<strong>Three picks &middot; ~$42&ndash;$70</strong>Two charcoal caps from the &ldquo;Autumn is coming&rdquo; drop with orange details, one with reflective stitching and one a trucker, plus the brown canvas logo cap."),
 ("On the Bag", "on-the-bag", ["S28","S12","NAL","S01"],
  "<strong>Four picks &middot; ~$30&ndash;$240</strong>A black leather glove, a divot tool that flips open like a butterfly knife, a Nalgene in two colours, and the yellow balaclava."),
]
N = 23
PQ = {
 "tees": ("Our purpose is to challenge tradition, and make it possible for golfers to wear whatever they want on the course.", "SLICE TOWN"),
}
CAP = "Photography &middot; SLICE TOWN&rsquo;s own"
BANDS = {
 "shirts-and-layers": (CAP, "SLICE TOWN takes its photos in the city as much as on the course.", [("band-1","A man from behind in a white SLICE TOWN tee with the sliced logo on the back, between tall buildings","The back print"),("band-2","A man in a white tee and black trousers leaning on a brick wall with a pint","After the round"),("band-3","A man in a black SLICE TOWN tee in front of a tower block","The black tee")]),
 "pants-and-shorts": (CAP, "The brand shoots in the studio and on the green.", [("band-4","A man in a black tee and black tech pants in a white studio","The tech pants"),("band-5","A man in the slate track jacket and pants in a white studio","The slate set"),("band-6","A man in sunglasses lying flat on a green, lining up a putt","Reading the putt")]),
 "on-the-bag": (CAP, "SLICE TOWN photographs the details, the car and the swing.", [("band-7","White SLICE TOWN socks with grey trainers, shot from above","The socks"),("band-8","An old silver Volvo saloon with its headlights on","The car"),("band-9","A golfer in wraparound sunglasses and a black tee mid-swing","The swing")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>SLICE TOWN makes golf clothes for people who came to the game through simulators and late-night range sessions rather than a country club. A Dane and a Swede started it at the end of 2024, the company is registered in Sweden, and the clothes are designed in Copenhagen. The first collection came out in 2025. The brand&rsquo;s line on its own About page is: &ldquo;Our purpose is to challenge tradition, and make it possible for golfers to wear whatever they want on the course.&rdquo;</p>
    <p>That means nylon track suits, boxy short-sleeve windbreakers, wide wool trousers, tech pants and a lot of reflective logos. The range is small and the jokes are good: there is a divot tool that opens like a butterfly knife and a yellow knitted balaclava sold &ldquo;for when your game&rsquo;s so bad, you need full anonymity.&rdquo; In Austin heat, the light nylon and short sleeves make more sense than most Scandinavian golf clothes.</p>
    <h2 class="products-hdr btk-story-hdr">More Than Clothes</h2>
    <p>SLICE TOWN puts as much into events as product. It has run a late-night simulator tournament in Copenhagen with a DJ, a bar, a pop-up shop and a free bleach and haircut station, thrown an after-party for the Östersjö Open at its outpost in Svängsta in southern Sweden, and set up at pop-ups in Paris and Lisbon. In shops, it is stocked at GOLV. in Zürich and The Agora in Bangkok.</p>
    <p>Everything is made in small batches, and the brand says plainly that sold-out pieces are not guaranteed to come back. Prices are in Swedish kronor; the dollar figures here are the store&rsquo;s own US prices. Start with the slate track jacket at 1,750 kr (~$190), or the charcoal tech pants at 900 kr (~$98) if your size is still there. Prices and stock were read on slice-town.com on 6 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Sweden and Copenhagen</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>A Dane and a Swede</span></div>
      <div class="sidebar-detail"><span class="l">Started</span><span>Late 2024</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Nylon track suits, tech pants and reflective logos</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>275&ndash;2,200 kr (~$30&ndash;$240)</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Golf Track Jacket, Slate, 1,750 kr</span></div>
      <a href="https://slice-town.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit SLICE TOWN &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#SliceTown</span>
        <span class="hashtag">#GolfStreetwear</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#ScandiGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who started SLICE TOWN?", "A Dane and a Swede founded the company, Slice-Town AB, at the end of 2024. Its first collection came out in 2025. The brand does not name the founders on its site."),
 ("Where is SLICE TOWN based?", "The company is registered in Sweden and its clothes are designed in Copenhagen, Denmark. It ships worldwide, and it is stocked at GOLV. in Zurich and The Agora in Bangkok."),
 ("How much does SLICE TOWN cost?", "On 6 October 2026, from 275 kr (about $30) for a Nalgene bottle and 300 kr for the glove or divot tool, through 1,750 kr (about $190) for a track jacket, up to 2,200 kr (about $240) for the knitted balaclava."),
 ("Does SLICE TOWN restock?", "Not always. The brand makes everything in small batches and says on its FAQ that a sold-out product is not guaranteed to be restocked."),
 ("How does SLICE TOWN fit?", "Big. The track pants and pleated trousers run wide and the brand suggests sizing down, and the polos, windbreaker and shirt are cut short and boxy. Most product pages note that the model is 186cm and wears a large."),
]
FRN = json.loads((ROOT / "research/slice-town/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-ST-GRID*/.products-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}.products-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
            '@media(max-width:1024px){.products-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:820px){.products-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:480px){.products-grid[data-n="3"],.products-grid[data-n="4"]{grid-template-columns:1fr}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-06", "dateModified": "2026-10-06",
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Golf streetwear from Sweden and Copenhagen</span><span class="dot"></span>
    <span>23 picks &middot; checked 6 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A golfer in a yellow knitted SLICE TOWN balaclava, blurred in motion, beside a friend in sunglasses and a SLICE TOWN cap" fetchpriority="high" /></div></div>
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
