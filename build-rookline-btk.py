#!/usr/bin/env python3
"""build-rookline-btk.py — Brand to Know: Rookline. Cloned from build-quiet-golf-revisit.py. 7 October 2026.
Lenny: "Let's do a brand to know - https://rookline.com/", then "looks good, muted colors are nice for fall. don't
include any of the not yet in stock options for now" (the 18 recommended styles; Grid Fleece left out), hero A.
FACTS: catalogue, prices and stock from rookline.com products JSON on 7 Oct 2026 (research/rookline/catalog.json).
Story: Rookline's About page and journal (Bethpage in our Backyard, Introducing: Hand & Heritage), quoted verbatim.
Founder name and launch date from launch coverage (not named here, per house rule on other publications).
PHOTOS: Rookline's own store, journal and site images, localised to /images/rookline.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Rookline Golf: New York Golf Apparel Built to Be Played In"
DESC = ("Brand to Know: Rookline, the New York golf label from Long Island natives. The Hudson brrr° polo, "
        "Hand & Heritage cashmere and 18 fall picks, with prices.")
H1 = "Brand to Know: Rookline &mdash; Golf Clothes From Players Who Walk 36"
BC = "Rookline"
SLUG = "brand-to-know-rookline"
IMG = "/images/rookline"
SHOP = "https://rookline.com/products/"
A = "Rookline"
P = {
 "sigpolo": (A, "Signature Blend Polo", "$165", "signature-blend-cotton-cashmere-polo-oatmeal-heather",
   "A long-sleeve polo in a cotton and cashmere blend that Rookline says you wear more like a sweater: light enough for a cool morning round, smart enough for dinner after. It is the piece we would start with, in oatmeal heather, navy or charcoal."),
 "cashcrew": (A, "Ottoman Rib Cashmere Crew", "$295", "ottoman-rib-cashmere-crew-oatmeal-heather",
   "This crew is knit from 100% cashmere, with a fully fashioned saddle sleeve and Ottoman rib at the elbow, cuff and hem. The product copy makes the case for wearing it on an ordinary Sunday: &ldquo;Wear it more than you think you should.&rdquo; Oatmeal, stone blue and grey heather are shown."),
 "cashhood": (A, "Ottoman Rib Cashmere Hoodie", "$335", "ottoman-rib-cashmere-hoodie",
   "The same 100% cashmere and Ottoman rib detailing as the crew, cut as a hoodie. Rookline pictures it on the range at 6:40am and at the pub at 8:30pm, which is the honest pitch for a $335 hoodie. Grey heather and stone blue."),
 "pivot": (A, "Brushed Twill Pivot Pant", "$175", "brushed-twill-pivot-pant",
   "A golf trouser in Japanese cotton twill with 3% spandex, which the brand calls a modest compromise between slim and wide, and between performance and lifestyle. It comes in elephant grey and navy blazer, with 30 to 34 inch inseams."),
 "watchcap": (A, "Cashmere Watch Cap", "$75", "cashmere-watch-cap-oatmeal-heather",
   "A 100% cashmere beanie, knit from two ends of yarn twisted into one so it stays dense through a season of being pulled on and stuffed in a pocket. It is the cheapest way into the cashmere, for frosty mornings waiting to tee off."),
 "hudpolo": (A, "Hudson 3-Button Polo with brrr&deg;", "$110", "hudson-3-button-polo-with-brrr-bunker-light-grey",
   "The everyday shirt: quick-dry, four-way stretch fabric with brrr&deg; cooling, sew-in collar stays and a three-button placket. The prints look quiet from a distance and turn out to be golf: a dimple pattern, and a Bunker Print mapping all 78 bunkers on Bethpage Black. We picked dimple grey, steel grey and the bunker print in light grey."),
 "hudqz": (A, "Hudson Quarter Zip", "$155", "hudson-quarter-zip-lichen",
   "The Hudson Quarter Zip is a mid-weight layer with a micro-peached interior, moisture-wicking fabric, UV protection and a slightly tapered sleeve. Rookline calls it crucial for dewsweepers and easy to stow once the sun is up. Lichen, navy and steel grey."),
 "hudcrew": (A, "Hudson Crew", "$145", "hudson-crew-elephant",
   "A crewneck in a UPF 50+ interlock knit, two layers knitted together for more structure than a standard sweatshirt, with branded elastic at the cuffs to keep the sleeves still through the swing. Elephant and highrise."),
 "hudhood": (A, "Hudson Hoodie", "$170", "hudson-hoodie-elephant",
   "The same interlock knit as the crew, with a mesh-lined hood and a zip pocket at the back right for a scorecard, glove or ball marker. It reads as golf clothing, not gym clothing. Elephant and dark navy."),
 "sscrew": (A, "Southside Crew", "$155", "southside-crew-vintage-green",
   "The Southside line is Rookline&rsquo;s more relaxed side, made for the walk to the car as much as the round. The crew has a premium, easy feel and comes in a vintage green that fits fall, or a wet-sand neutral."),
 "circa": (A, "Circa Windbreaker", "$155", "circa-windbreaker-vintage-green",
   "The Circa is a &rsquo;90s-inspired pullover windbreaker with a water-resistant shell, a breathable mesh lining, a side zip and a single-button closure. It is the layer for a windy afternoon, in vintage green or steel grey."),
 "fivepocket": (A, "Hudson 5-Pocket Pant", "$155", "hudson-5-pocket-pant-dark-moss",
   "The Hudson five-pocket comes in water-repellent four-way stretch fabric with a bonded waistband and a discreet internal pocket for course essentials. It has a tapered fit that looks like a normal trouser off the course. Dark moss and wet sand."),
 "zephyr": (A, "Zephyr Pant", "$160", "zephyr-pant-regal-navy",
   "An elastic-waist pant in water-repellent four-way stretch with a brushed back for warmth, so it is the one for cold rounds. It has a slight taper and comes in regal navy and light grey."),
 "juneau": (A, "Juneau Lined Jogger 2.0", "$190", "juneau-lined-jogger-2-0-dark-moss",
   "The Juneau is a tapered jogger lined in soft jersey, with articulated knees, water-repellent stretch fabric and concealed zips at the ankle. Rookline compares it to your Sunday sweats, and it is the warmest bottom here. Dark moss and oil can."),
 "yeoman": (A, "Yeoman&rsquo;s Performance Short", "$135", "performance-golf-short-elephant",
   "A lightweight micro-dobby short with four-way stretch, an 8.5-inch inseam and an elastic waistband that keeps a polo tucked in. Rookline calls it a workhorse, and in Austin it will see plenty of fall rounds. Elephant and dark navy."),
 "pullon": (A, "Hudson Pull On Short", "$110", "hudson-pull-on-short-slate",
   "The Hudson short pulls on with an elastic waist and belt loops, a 7-inch inseam and a tailored, above-the-knee fit. It is the shorter, simpler partner to the Yeoman&rsquo;s. Slate and dark navy."),
 "oneunder": (A, "One Under Cap", "$45", "one-under-cap-chive",
   "A structured, low-profile, lightweight cap with the RKL crest, made to stay put from the first tee to the last green. Chive green and light grey."),
 "nopics": (A, "No Pictures T-Shirt", "$49", "no-pictures-t-shirt-vintage-green",
   "This washed tee carries a small golf graphic, in vintage green or stone. It is the joke that keeps the brand from taking itself too seriously, and the cheapest thing in the store."),
}
SECTIONS = [
 ("Hand &amp; Heritage", "hand-heritage", ["sigpolo","cashcrew","cashhood","pivot","watchcap"],
  "<strong>Five picks &middot; $75&ndash;$335</strong>The new fall capsule, built on cotton, cashmere and brushed twill in oatmeal, charcoal, navy and stone blue. Rookline describes it as an homage to what has always worked. Start with the Signature Blend Polo."),
 ("Polos and Layers", "polos-layers", ["hudpolo","hudqz","hudcrew","hudhood","sscrew","circa"],
  "<strong>Six picks &middot; $110&ndash;$170</strong>The Hudson line is the performance core: the brrr&deg; polo, a quarter zip and an interlock crew and hoodie. Southside adds a more relaxed crew, and the Circa is the windbreaker."),
 ("Pants and Shorts", "pants-shorts", ["fivepocket","zephyr","juneau","yeoman","pullon"],
  "<strong>Five picks &middot; $110&ndash;$190</strong>Three pants for three kinds of weather, from the five-pocket to the brushed Zephyr to the lined Juneau jogger, and two shorts for the warm days Austin still gets in October."),
 ("Extras", "extras", ["oneunder","nopics"],
  "<strong>Two picks &middot; $45&ndash;$49</strong>A cap and a tee make the easy way into the brand."),
]
N = 18
PQ = {
 "polos-layers": ("Can this fabric hold up walking 36 in August?", "Rookline, on its About page"),
 "pants-shorts": ("As Long Island natives, we&rsquo;ve had the privilege to play the Black Course dozens of times.", "Rookline, in its journal"),
 "extras": ("We know because we play.", "Rookline"),
}
CAP = "Photography &middot; Rookline&rsquo;s own"
BANDS = {
 "hand-heritage": (CAP, "Hand &amp; Heritage, the fall capsule, in cashmere and cotton.", [("band-1","A cashmere sleeve folded over a golf club","The cashmere"),("band-2","A golfer walking off with a carry bag over a black hoodie","The walk"),("band-3","A man in a grey cashmere hoodie in a clubhouse grill room","The grill room")]),
 "polos-layers": (CAP, "Rookline shoots on the course, mostly at either end of the day.", [("band-4","A bunker shot spraying sand on a seaside course","The bunker"),("band-5","A golfer in a navy quarter zip finishing his swing","Quarter zip"),("band-6","A golfer in a vintage green windbreaker leaning on a club","The Circa")]),
 "pants-shorts": (CAP, "Rookline likes late light and long shadows.", [("band-7","A golfer in a navy top and jogger standing on a green at dusk","Dusk"),("band-8","A golfer reading a putt in moss pants on a hillside course","The read"),("band-9","A golfer finishing a swing in navy pants and a green layer","Follow-through")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We like Rookline because it is made by people who clearly play a lot of golf, and play it the way we do. They are Long Island natives who have walked Bethpage Black dozens of times, and their About page reads like the questions you ask yourself in the parking lot: can this hold up walking 36 in August, and will this layer keep the cold out without the bulk? For an Austin muni player, the Hudson polo is the everyday shirt, quick-dry and stretchy, with prints that look plain from ten feet and turn out to be golf up close. One of them maps all 78 bunkers on Bethpage Black.</p>
    <p>Fall is where it gets good. The new Hand &amp; Heritage capsule is cotton, cashmere and brushed twill in oatmeal, charcoal and stone blue, the colors you want on a cold first tee in December. It is not cheap, and the cashmere crew is $295. But the Signature Blend Polo at $165 is the piece we would buy first, a long-sleeve polo you wear like a sweater, and the Hudson Quarter Zip at $155 is the layer that comes off on the fourth hole and goes back on at the turn.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Rookline launched in late 2024 and plays most of its golf in New York, where, in its own words, the season is shorter than they would like. Its founder, Matt Dowling, grew up in a family that has been in the women&rsquo;s apparel business for decades. The range runs in three lines: Hand &amp; Heritage for fall, Hudson for performance and Southside for relaxed crews and hoodies. Shipping is free on every order this fall, and all 18 pieces below were in stock on rookline.com on 7 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>New York</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2024, by Matt Dowling</span></div>
      <div class="sidebar-detail"><span class="l">Lines</span><span>Hand &amp; Heritage, Hudson, Southside</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>The Hudson brrr&deg; polo</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$45&ndash;$335</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Signature Blend Polo, $165</span></div>
      <a href="https://rookline.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Rookline &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Rookline</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#FallGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Rookline from?", "New York. The team are Long Island natives and play most of their golf in New York; the brand launched in late 2024."),
 ("Who founded Rookline?", "Matt Dowling, whose family has been in the women's apparel business for decades."),
 ("What is the Rookline Hudson polo?", "Rookline's everyday golf polo: quick-dry four-way stretch fabric with brrr° cooling, sew-in collar stays and a three-button placket, $110. Prints include a dimple pattern and a Bunker Print of all 78 bunkers on Bethpage Black."),
 ("How much does Rookline cost?", "On 7 October 2026 the Hudson polo was $110, the Signature Blend Polo $165, pants $155 to $190, the cashmere crew $295 and the cashmere hoodie $335. Caps are $45 and shipping is free on all fall orders."),
 ("What is Rookline Hand & Heritage?", "The fall 2026 capsule: cotton-cashmere polos, 100% cashmere Ottoman rib crews and hoodies, a brushed Japanese twill pant and a cashmere watch cap."),
]
_FR = json.loads((ROOT / "research/rookline/frames.json").read_text())["frames"]
FRN = {k: [x["f"] for x in v] for k, v in _FR.items()}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-RK-GRID*/.products-grid[data-n="5"],.products-grid[data-n="6"]{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.products-grid[data-n="2"]{grid-template-columns:repeat(2,minmax(0,1fr));max-width:820px;margin-left:auto;margin-right:auto}'
            '@media(max-width:820px){.products-grid[data-n="5"],.products-grid[data-n="6"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:480px){.products-grid[data-n="5"],.products-grid[data-n="6"],.products-grid[data-n="2"]{grid-template-columns:1fr}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-07", "dateModified": "2026-10-07",
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
    <span>New York golf apparel</span><span class="dot"></span>
    <span>18 picks &middot; all in stock, checked 7 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A golfer in an oatmeal sweater mid-swing on a tee at sunset" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Quiet Golf", "Costa Mesa", "LBB", "GolfPass", "Something Different"):
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
