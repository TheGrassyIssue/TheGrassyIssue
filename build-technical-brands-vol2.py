#!/usr/bin/env python3
"""build-technical-brands-vol2.py — "The Technical Brands Roundup, Vol. 2" 15 October 2026.
Lenny: "lets do a The Technical Brands Roundup vol 2", then "Think more windy and a little rainy and then also muggy and kinda
hot", then "we're a little thin and also need to push more brands from the universe", then "let's build it" (all 27). Then swapped Redvanly's Varick short for a Malbon athletic short at Lenny's request (Malbon appears twice).
FACTS: every piece in stock in a medium Oct 15 2026 at the price each store shows a US shopper (Shopify products.json / .js in a
US browser). Local Rule and Abacus price in SEK (1 SEK = 0.10028 USD). Devereux's quarter-zip is final sale. Copy paraphrases each
brand's own product description; quoted phrases are verbatim. 21 brands from the TGI universe + 6 outside specialists.
PHOTOS: brands' own (research/technical-vol2/frame.py). Hero: Casualist's water-resistant coach jackets on the course.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Technical Brands Roundup, Vol. 2: Golf Layers for Wind, Rain and Muggy Fall Days"
DESC = ("Twenty-seven technical golf pieces from 26 brands for a Texas fall: packable windshirts, vests, rain shells that "
        "breathe, and polos and shorts for when it turns muggy again.")
H1 = "The Technical Brands Roundup, Vol. 2: Wind, a Little Rain and Muggy Afternoons"
BC = "The Technical Brands Roundup, Vol. 2"
SLUG = "the-technical-brands-roundup-vol-2"
IMG = "/images/technical-vol2"
SHOP = ""
P = {
 # Wind
 "malbon": ("Malbon Golf", "Studio Seoul Detachable Sleeve Anorak", "$278", "https://malbon.com/products/studio-seoul-detachable-sleeve-anorak-navy",
   "Malbon made the two-in-one of the bunch. It cuts this pullover from an imported Japanese fabric with a cotton-like hand that wicks and dries fast, and the sleeves zip off, so the anorak you teed off in becomes a vest by the turn."),
 "macade": ("Macade", "Storm Wind Shirt, Dark Blue", "$195", "https://macadegolf.com/products/storm-wind-shirt-dark-blue",
   "A windshirt with short sleeves and a hood, which is about as Texas as a technical layer gets. Water-repellent, smooth stretch fabric and a half zip; it blocks a gusty front without cooking you. Macade was in Vol. 1 with a summer polo."),
 "devereux": ("Devereux Golf", "Nylon Short Sleeve Quarter Zip, Acid Yellow", "$88", "https://devereuxgolf.com/products/nylon-short-sleeve-quarter-zip-acid-yellow",
   "Devereux built this 100% nylon short-sleeve pullover to handle wind and light rain, with an oversized fit that layers over a polo. It comes in the loudest color here, costs less than any other shell, and is final sale."),
 "sugarloaf": ("Sugarloaf Social Club", "SSC Windshirt", "$125", "https://www.sugarloafsocialclub.com/products/windshirt",
   "Sugarloaf made it stretchy and breathable to repel wind and water, then lined it in mesh and vents the back so it doesn&rsquo;t trap heat. Their product page admits: &ldquo;I do not know what the space-time continuum is.&rdquo; Size up if you&rsquo;re between."),
 "sounder": ("Sounder", "Pac Mach Jacket, Deep Navy Ripstop", "$197", "https://soundergolf.com/en-us/products/pac-mach-jacket-deep-navy-ripstop",
   "Ultra-lightweight Japanese ripstop made from recycled polyester, with its own matching stuff bag. This is the jacket that lives in the bag pocket until the wind picks up. Sounder was in Vol. 1; this is new for fall. XS to M."),
 "parmore": ("Parmore Golf", "Capsule Windbreaker, Long Sleeve Pullover", "$115", "https://parmoregolf.com/products/long-sleeved-windbreaker-rebrand",
   "Parmore calls it &ldquo;the wind layer for when style still matters&rdquo;: a khaki pullover with cream ribbed collar, cuffs and hem. If you want water resistance too, their Varsity Quarter-Zip is $140."),
 "publicdrip": ("Public Drip", "Swing Shirt, Green", "$120", "https://publicdrip.com/products/swing-shirt-green",
   "A nylon micro-ripstop outer layer that Public Drip designed to pack away, so it can always ride in the bag. Short sleeves, a boxy cut and hunter green. M to XL."),
 "casualist": ("Casualist", "Windbreaker Coach Jacket, Archive", "$120", "https://casualist.com/products/winbreaker-1",
   "Water resistant, light enough to forget you have it on, and cut for the course. Casualist made it for British weather: &ldquo;more of a suggestion than a forecast.&rdquo; Our hero photo, in navy."),
 "rebolf": ("Rebolf", "Crosswind Windbreaker", "$145", "https://rebolf.com/products/crosswind-windbreaker",
   "Spain&rsquo;s Rebolf made this a summer windbreaker: stretch nylon, a relaxed fit, a collared zip and elasticated details. Breathable, wind-resistant and easy to move in."),
 "latenine": ("Late Nine", "Quarter Zip Windbreaker, Navy", "$502", "https://late-nine.com/products/quarter-zip-windbreaker-navy",
   "Late Nine charges the most for a wind layer here, and tailors it the most: a full collar, a zip with a buttoned placket, dark metal hardware and Late Nine&rsquo;s boxy fit with a drawstring hem. Down to S and M."),
 "readthegreen": ("Read The Green", "The Swisher Zip", "$118", "https://readthegreen.com/products/the-swisher-zip",
   "A &rsquo;90s New York windbreaker in navy and heather gray, with &ldquo;Gotta Be You&rdquo; printed along the back neckline. Throwback shape, modern use."),
 "ghost": ("Ghost Golf", "Fairway Windshirt V2", "$150", "https://ghostgolf.com/products/fairway-windshirt-v2",
   "Wind- and water-resistant, made for &ldquo;dewy mornings, breezy fairways, and light rain,&rdquo; with a high ribbed V-neck collar that looks more like a sweater than a shell."),
 "walker": ("Walker Golf Things", "All Weather Pullover, Navy", "$110", "https://www.walkergolfthings.com/en-us/products/all-weather-pullover-2",
   "Walker&rsquo;s technical, weather-ready pullover, built to protect without restricting your swing. The US-store price; M to XXL."),
 "siegelman": ("Siegelman Stable", "Siegelman Stable &times; Maxfli Pullover Jacket", "$298", "https://siegelmanstable.com/products/retro-track-jacket-2",
   "Siegelman made this track jacket from tech poplin lined in athletic mesh, with Maxfli embroidery and hidden zip pockets. You can actually play in it."),
 # Vests
 "jones": ("Jones Sports Co", "Windblocker Vest, Wheat", "$168", "https://jonessportsco.com/products/windblocker-vest-wheat",
   "Jones builds it from lightweight crinkle nylon with 4-way stretch and a DWR finish, lined in brushed mesh. It protects your core and leaves your arms alone."),
 "localrule": ("Local Rule", "Tech Vest, Light Green", "1,499 SEK (~$150)", "https://local-rule.com/products/tech-vest-light-green",
   "Sweden&rsquo;s Local Rule built this for changing conditions: lightweight, breathable and stretchy, with a sharp Scandinavian cut. Priced in Swedish kronor; S and M left."),
 "stitch": ("Stitch Golf", "GT Vest Heritage", "$148", "https://stitchgolf.com/products/gt-vest-heritage",
   "Part of Stitch&rsquo;s Weather System: lightweight, water repellent and breathable, named after Gran Turismo. Made for exactly the in-between months we&rsquo;re in."),
 "holderness": ("Holderness &amp; Bourne", "The Boyd Vest, Black", "$185", "https://holdernessandbourne.com/products/the-boyd-vest-black",
   "Holderness &amp; Bourne made it ultra-lightweight, windproof and water-resistant with 4-way stretch. It is the cleanest-looking vest here, and one of our outside picks."),
 # Rain
 "goodgood": ("Good Good Golf", "Elite Rain Jacket", "$124.99", "https://goodgoodgolf.com/products/elite-rain-jacket",
   "Good Good gives you a waterproof shell with bonded seams, a three-panel hood and elastic inner cuffs, for less than any other rain jacket here."),
 "fella": ("Fella Golf", "Panel Tech Jacket, Water Repellent", "$275", "https://fellagolf.com/products/water-repellent-tech-jacket",
   "Fella made this water-repellent shell in two-tone green and off-white panels. It handles a shower that blows through, not a washout."),
 "zerorestriction": ("Zero Restriction", "Power Torque Waterproof Quarter Zip", "$203", "https://zerorestriction.com/products/power-torque-waterproof-quarter-zip",
   "Waterproof, windproof and built on Zero Restriction&rsquo;s Power Torque stretch system. Marked down from $290; black, S and M left. An outside specialist."),
 "abacus": ("Abacus Sportswear", "Mens Links Stretch Rainjacket", "1,599 SEK (~$160)", "https://abacussportswear.com/products/mens-links-stretch-rainjacket-navy",
   "Two-way stretch waterproof fabric that Abacus calls very breathable, with every seam sealed and a PFC-free water repellency. From Sweden, priced in kronor."),
 "linksoul": ("Linksoul", "Maverick Waterproof Full-Zip Jacket", "$248", "https://linksoul.com/products/ls5007-navy",
   "Built lighter and more breathable on purpose, with fully seam-sealed protection and targeted ventilation, so you stay dry without overheating."),
 # Muggy
 "students": ("Students Golf", "Recess Tech S/S Polo", "$98", "https://studentsgolf.com/products/recess-tech-s-s-polo",
   "A soft nylon and spandex polo that Students calls its &ldquo;coolest-to-the-touch&rdquo; one. For when the front passes and it&rsquo;s 82 and sticky again."),
 "eastside": ("Eastside Golf", "Crossover Short", "$115", "https://eastsidegolf.com/products/midnight-navy-eastside-golf-mens-mesh-lined-short",
   "Eastside pairs a light nylon outer with a mesh liner, 4-way stretch and water resistance. Wear it to the range, the course or the gym."),
 "dunning": ("Dunning Golf", "Freedman Ventilated Performance Quarter Zip", "$128", "https://dunninggolf.com/products/freedman-ventilated-performance-quarter-zip",
   "Printed mesh with COOLMAX for airflow: a quarter-zip for a cool start that won&rsquo;t turn into a sauna by the back nine."),
 "malbonshort": ("Malbon Golf", "Performance Poly Tech Short, Tan", "$128", "https://malbon.com/products/performance-poly-tech-short-tan",
   "Malbon made its most athletic short from nylon and spandex, with an elastic waist and internal drawcord, zip pockets front and back, perforation accents for airflow and a 5-inch inseam. Malbon is the only brand that shows up twice here."),
}
SECTIONS = [
 ("Wind: Light Layers for a Gusty Front Nine", "wind", ["malbon", "macade", "devereux", "sugarloaf", "sounder", "parmore", "publicdrip", "casualist", "rebolf", "latenine", "readthegreen", "ghost", "walker", "siegelman"],
  "<strong>Fourteen pieces</strong>These windshirts, anoraks and pullovers are light enough to stuff in a bag pocket. Several have short sleeves, which is the most Texas idea in the post."),
 ("Vests: Block the Wind, Keep the Arms Free", "vests", ["jones", "localrule", "stitch", "holderness"],
  "<strong>Four pieces</strong>A vest stops the wind on your chest and lets your arms breathe, which is exactly the trade a 70-degree windy day asks for."),
 ("A Little Rain: Shells That Breathe", "rain", ["goodgood", "fella", "zerorestriction", "abacus", "linksoul"],
  "<strong>Five pieces</strong>Waterproof or water-repellent, and built light enough that you don&rsquo;t sweat through them before the shower passes."),
 ("Muggy &amp; Kinda Hot", "muggy", ["students", "eastside", "dunning", "malbonshort"],
  "<strong>Four pieces</strong>For the other half of a Texas fall day: wicking, mesh and stretch nylon for when it turns sticky."),
]
N = 27
PAIRS = {}
LIFE = []
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Vol. 1 in August was about fabric stories for summer. Vol. 2 is about the weather we actually get in Austin in October and November: a front blows through, the wind picks up, it spits rain for ten minutes, and then it&rsquo;s 82 and muggy by the back nine.</p>
    <p><strong>Texas fall doesn&rsquo;t want a parka.</strong> It wants a wind layer you can stuff in a pocket, a rain shell that breathes, and something that moves sweat once the sun comes back out. So there is no down and no fleece here. Everything is light, and most of it packs.</p>
    <p><strong>The best pieces do two jobs.</strong> Malbon made an anorak that loses its sleeves when it warms up. Macade and Devereux made windshirts with short sleeves. Sounder and Public Drip pack into nothing. Linksoul vents its rain jacket so you don&rsquo;t overheat in it. And the vests from Jones and Local Rule block wind on your chest and leave your arms alone.</p>
    <p>The 27 pieces come from 26 brands, 21 of them from the TGI brand universe and five from outside specialists in weather gear. Every piece was in stock in a medium on October 15, 2026, at the price each store shows a US shopper. If you buy one thing: a packable windshirt, from Sounder ($197) or Sugarloaf ($125).</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>26</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$88&ndash;$502</span></div>
      <div class="sidebar-detail"><span class="l">Most versatile</span><span>Malbon zip-off anorak</span></div>
      <div class="sidebar-detail"><span class="l">Most packable</span><span>Sounder Pac Mach</span></div>
      <div class="sidebar-detail"><span class="l">Best value shell</span><span>Good Good, $124.99</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Devereux, $88</span></div>
      <a href="#wind" class="sidebar-cta">Start with wind &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#TechnicalGolf</span>
        <span class="hashtag">#GolfLayers</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#Windshirt</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">Read <a href="/drops/the-technical-brands-roundup">The Technical Brands Roundup, Vol. 1</a> for the summer fabrics, and <a href="/drops/the-fall-hoodie-edit-2026">The Fall Hoodie Edit</a> for when it finally gets cold.</p>
</section>
"""
FAQ = [
 ("What should I wear to play golf in windy weather?", "A light wind layer over a polo: a windshirt or pullover like Sugarloaf's SSC Windshirt or Sounder's packable Pac Mach, or a vest like Jones' Windblocker if you want your arms free. In a warm climate, short-sleeve windshirts from Macade or Devereux block the wind without overheating."),
 ("What is a golf windshirt?", "A thin, often stretchy pullover or half-zip that blocks wind and sheds light rain. It is lighter than a rain jacket, usually packs small, and is worn over a polo on breezy days."),
 ("What is the difference between water-resistant and waterproof golf jackets?", "Water-resistant or water-repellent jackets, like Casualist's coach jacket or Fella's Panel Tech, shed a passing shower. Waterproof jackets, like Good Good's Elite Rain Jacket or Abacus's Links, use waterproof fabric with sealed or bonded seams to keep out steady rain."),
 ("What golf clothes work in hot, humid weather?", "Nylon and spandex polos like Students' Recess Tech, mesh quarter-zips like Dunning's Freedman, and lightweight stretch shorts from Eastside and Malbon. Look for wicking, mesh and quick-dry fabrics."),
 ("Are these golf jackets in stock?", "Every piece here was in stock in a medium on its brand's own store on October 15, 2026. Late Nine and Local Rule are down to S and M, and Devereux's quarter-zip is final sale."),
]
HERO_ALT = "Two golfers seen from behind on a fairway wearing navy Casualist windbreaker coach jackets with CASUAL PRO printed on the back"
FRN = json.loads((ROOT / "research/technical-vol2/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-FF-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-15", "dateModified": "2026-10-15",
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
    <span>26 brands, wind to muggy</span><span class="dot"></span>
    <span>27 picks &middot; in stock, checked October 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
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
    for leak in ("Mackem", "Kalamunda", "Lehi", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram"):
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
