#!/usr/bin/env python3
"""build-hat-makers.py — Three Hat Makers With Momentum: Communal, Duke + Dexter, Winslow. Cloned from build-radar-three-2.py. 25 October 2026.
Lenny: "we're gonna do a post that's three hat makers with motion" -> "Brands with momentum", 6 hats per brand; "build it" on the starred picks.
FACTS: research/hat-makers/brief.md and catalogue.json, read live October 25, 2026 (USD). Winslow names no founder; don't add one.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "3 Hat Makers With Momentum: Communal, Duke + Dexter, Winslow"
DESC = ("Three hat makers on the rise: Communal from Austin, Duke + Dexter from London and Winslow from LA. "
        "Their stories, what's driving each one right now and 18 hats with prices.")
H1 = "Three Hat Makers With Momentum"
BC = "Three Hat Makers With Momentum"
SLUG = "hat-makers-with-momentum"
IMG = "/images/hat-makers"
SHOP = ""
CM, DD, WN = "Communal", "Duke + Dexter", "Winslow"
CMU, DDU, WNU = "https://communalmfg.com/products/", "https://dukeanddexter.com/products/", "https://winslowla.com/products/"
P = {
 # Communal
 "dang": (CM, "Dang Hat", "$60", CMU+"dang-hat",
   "Our pick from Communal. The original: one word in 3D embroidery on cotton twill, with a mesh flap behind the front panel so it keeps its shape. In camo, brown, navy and red. When we checked it had 86 reviews, 97% of them five stars."),
 "anchor": (CM, "C Anchor Hat", "$60", CMU+"c-anchor-hat",
   "From the nautical drop Communal released on September 24: a C wrapped around an anchor, in navy cotton canvas or bone white and kelly green twill."),
 "trading": (CM, "Trading Co. Hat", "$60", CMU+"trading-co-hat",
   "An oval Communal Trading Co. logo on the front, in camel with a vintage white crown, blue or vintage red. Also from the September drop."),
 "captain": (CM, "The Captain Hat", "$60", CMU+"the-captain-hat",
   "Navy twill with the Communal script across the crown and a striped band underneath. The third hat from the nautical drop, and the most Lake Austin of the lot."),
 "martini": (CM, "Cowboy Martini Short Brim Hat", "$60", CMU+"cowboy-martini-short-brim-hat",
   "Communal calls this navy one &ldquo;one of our first ever short brimmed truckers.&rdquo; The short brim now has its own section of the store."),
 "eagle": (CM, "Communal Eagle Hat", "$60", CMU+"communal-eagle-hat",
   "A gold embroidered eagle over the Communal wordmark, in bone white, red, black or camo. The loudest hat in the post."),
 # Duke + Dexter
 "eatdirt": (DD, "Eat Dirt Washed Red Cap", "$90", DDU+"eat-dirt-washed-red-cap",
   "Our pick from Duke + Dexter. Distressed washed-red cotton with &ldquo;Eat Dirt&rdquo; across the crown and Duke lettering on the side. D+D made it &ldquo;for the trash talkers,&rdquo; which makes it a golf hat whether they meant it or not."),
 "chateau": (DD, "Midnight Chateau Washed Purple Cap", "$90", DDU+"midnight-chateau-washed-purple-cap",
   "Distressed cotton canvas from the new Midnight Chateau collection, with the name embroidered across the crown and screen-printed artwork drawn by D+D&rsquo;s in-house artists, Jess and Valentino."),
 "pitstop": (DD, "DR2 Pit Stop Cream Cap", "$90", DDU+"finish-line-cap",
   "Off-white canvas with a black peak, a pit stop graphic on the front, D+D&rsquo;s wing logo on one side and, in the brand&rsquo;s words, &ldquo;trash-talking to the back.&rdquo;"),
 "dukeblack": (DD, "Duke Black Cap", "$90", DDU+"duke-black-cap",
   "All-black satin with DUKE in raised embroidery, a padded headband and World Championship detailing on the side. D+D calls it a first for the brand."),
 "trucker": (DD, "Duke Cream Trucker Cap", "$90", DDU+"duke-cream-trucker-cap",
   "DUKE across a cream front panel with black mesh behind it, a padded headband and a snapback. The easiest of the D+D caps to wear with anything."),
 "dukegreen": (DD, "DR2 Duke Green Cap", "$90", DDU+"duke-green-cap",
   "The satin DUKE cap in green, with the same raised lettering and World Championship detailing as the black one."),
 # Winslow
 "cord": (WN, "Corduroy Hat", "$60", WNU+"corduroy-hat",
   "Our pick from Winslow. The brand&rsquo;s best-selling hat redone in soft navy cotton corduroy with the Winslow script embroidered on the front. The one to reach for once it turns cold."),
 "whitney": (WN, "Mt. Whitney Cap", "$60", WNU+"mt-whitney-cap",
   "Washed grape cotton, stone washed and distressed by hand, with a leather strap. Made in the USA, and made to look like it has had a few summers already."),
 "yellow": (WN, "Washed Yellow Cap", "$60", WNU+"washed-yellow-cap",
   "The same hand-distressed, stone-washed five-panel in yellow, with a W on the front. Made in the USA with a leather strap closure."),
 "mesh": (WN, "Mesh Cap", "$60", WNU+"american-trucker-copy",
   "A white mesh upper, a green brim and a green W on the front. Soft structured, snapback, made in the USA."),
 "amtrucker": (WN, "American Trucker", "$60", WNU+"camo-hat-copy",
   "A cotton twill front with puff-printed lettering and a brown mesh back. Soft structured, snapback, made in the USA."),
 "weathered": (WN, "Weathered Hat", "$55 &middot; sold out", WNU+"weathered-hat",
   "A six-panel washed and distressed by hand. Winslow wrote that it&rsquo;s perfect &ldquo;for hanging by the lake or going low on the golf course.&rdquo; Sold out when we checked, but that line earns it a spot."),
}
SECTIONS = [
 ("Communal", "communal", ["dang","anchor","trading","captain","martini","eagle"],
  "<strong>Austin, TX &middot; six picks &middot; all $60</strong>A hat company that started as the clothing side of a hemp brand. Every hat is cotton twill, in a standard brim with a mesh flap or a short brim, and every one comes with a limited lifetime warranty."),
 ("Duke + Dexter", "duke-dexter", ["eatdirt","chateau","pitstop","dukeblack","trucker","dukegreen"],
  "<strong>London &middot; six picks &middot; all $90</strong>A loafer brand founded in 2015 that has started making caps, with satin crowns, washed cotton and motorsport graphics. US prices, as shown on the brand&rsquo;s US store."),
 ("Winslow", "winslow", ["cord","whitney","yellow","mesh","amtrucker","weathered"],
  "<strong>Los Angeles &middot; six picks &middot; $55&ndash;$60</strong>Washed, worn-in caps made in the USA, from a brand that started with hats and is now building out a full line of clothes. Five hats were in stock when we checked; the sixth is the sold-out one that mentions golf."),
]
N = 18
PQ = {
 "communal": ("Closer to a design studio mining archives than a novelty hat brand chasing a moment.", "Communal, on its About page"),
 "duke-dexter": ("Our first beanie. We made it a good one.", "Duke + Dexter, on its new beanies"),
 "winslow": ("Our hats are the entry point.", "Winslow"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "communal": ("From Communal", "Hats on the rocks, on the porch and by the water.", [("band-1","A stack of Communal hats in navy, cream and red on a rock by the water","The stack"),("band-2","Two people in Communal hats sitting on the front steps of a white clapboard house","The porch"),("band-3","A woman in a navy Communal anchor hat leaning on a railing over a harbor","The harbor")]),
 "duke-dexter": ("From Duke + Dexter", "The Eat Dirt cap in a motorcycle garage, and the new beanies.", [("band-4","An older man with a white beard in a washed red Eat Dirt cap and a patched racing jacket, beside a motorcycle wheel","The garage"),("band-5","A man in an Eat Dirt cap and denim shirt standing in a garage doorway covered in old oil signs","The doorway"),("band-6","A man in a red ribbed Duke beanie and a black Midnight Chateau jacket","The beanie")]),
 "winslow": ("From Winslow", "A California hillside, a studio chair and the corduroy hat.", [("band-7","Two people in Winslow sweatshirts in a green field below California hills","The hills"),("band-8","A man in an orange top and dark cap slouched in a chair in a bright studio","The studio"),("band-9","A man in a navy Winslow corduroy hat and a grey tank top","The corduroy")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The hat is the cheapest way into a brand and the one piece of clothing every golfer wears on every round. So it says something that three brands from three very different places are all putting their energy into hats right now. One is an Austin company that got here by accident, one is a London shoe brand trying something new, and one is an LA label that started with hats on purpose and is now building everything else around them.</p>
    <p><strong>Communal</strong> is the local one, and it has the best origin story of the three. It started in 2019 as Communal Cowboy, a hemp brand with a shop on Austin&rsquo;s East Side that was nearly ready to open when COVID closed it for good. Hemp companies couldn&rsquo;t run social media ads, so the team made clothes they could advertise, to &ldquo;leave breadcrumbs&rdquo; back to the hemp. In a December 2023 post, Justin Dumbeck wrote that it worked &ldquo;better than we could have ever imagined,&rdquo; and the company dropped hemp to focus on clothes. Today it calls itself a headwear company focused on American iconography. The momentum shows in the rebrand to Communal MFG, a nautical drop in September and a review count most hat brands would envy: 4.93 stars from 215 reviews on its site. Every hat is $60 and comes with a limited lifetime warranty.</p>
    <p><strong>Duke + Dexter</strong> is the outlier. Archie Hewlett started it in London in 2015, selling slippers out of his bedroom on a &pound;9,000 loan, and it became a loafer brand, with every pair handmade at its factory in England. Hats are new territory. The product copy calls the satin DUKE caps &ldquo;a first for D+D,&rdquo; and the beanies are &ldquo;our first beanie.&rdquo; The momentum comes from everything around them: a collaboration with the Alpine Formula One team, another with Cole Buxton and the new Midnight Chateau collection. The caps borrow from all of it, with racing graphics, satin crowns and an Eat Dirt cap the brand made &ldquo;for the trash talkers.&rdquo;</p>
    <p><strong>Winslow</strong> is the newest and quietest of the three. It is a Los Angeles brand that says plainly that its &ldquo;hats are the entry point,&rdquo; with full collections of clothes coming next, and you can see that happening: the store now carries hoodies, sweaters, jackets and pants alongside the caps. The washed caps are made in the USA, stone washed and distressed by hand, so they look a few years old on day one. Its own copy even mentions golf: the Weathered Hat, sold out when we checked, is for &ldquo;going low on the golf course.&rdquo;</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>Communal is for the golfer who likes a hat with a joke or a story on it.</strong> Its hats carry Dang, an eagle or a cowboy with a martini. If you play Lions or Roy Kizer and want something from down the road, start here.</p>
    <p><strong>Duke + Dexter is for the golfer who dresses up the rest of the outfit.</strong> These are $90 caps with satin crowns and motorsport details, made for pairing with a good knit and loafers at the clubhouse afterward.</p>
    <p><strong>Winslow is for the golfer who wants a hat that looks like they found it.</strong> The colors are washed, the straps are leather and nothing on them is loud, which makes these the easiest of the three to wear every day.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Communal</span><span>Austin, TX</span></div>
      <div class="sidebar-detail"><span class="l">Duke + Dexter</span><span>London, since 2015</span></div>
      <div class="sidebar-detail"><span class="l">Winslow</span><span>Los Angeles</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>18 hats</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$55&ndash;$90</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Dang Hat, Eat Dirt Cap, Corduroy Hat</span></div>
      <div class="hashtags">
        <span class="hashtag">#HatMakers</span>
        <span class="hashtag">#CommunalMFG</span>
        <span class="hashtag">#DukeDexter</span>
        <span class="hashtag">#WinslowLA</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Communal based?", "Austin, Texas. It started in 2019 as Communal Cowboy, a hemp brand, began making clothes in 2020 and dropped hemp in December 2023 to focus on headwear. On October 25, 2026 every hat on its site was $60."),
 ("Is Communal the same as Communal Cowboy?", "Yes. Communal Cowboy rebranded as Communal MFG; the Dang Hat and the rest of the hats carried over."),
 ("Does Duke + Dexter make hats?", "Yes. The London loafer brand, founded in 2015, now sells caps at $90 and wool beanies at $110 on its US store. It describes several of the caps, and the beanies, as firsts for the brand."),
 ("Where are Winslow hats made?", "Winslow, a Los Angeles brand, says its washed caps are made in the USA from 100% cotton, stone washed and distressed by hand. Its caps were $60 on October 25, 2026."),
 ("Which of the three should I buy?", "Communal for a hat with a story or a joke on it, Duke + Dexter for a dressier satin or motorsport cap, and Winslow for a washed, worn-in cap you can wear every day."),
]
FRN = json.loads((ROOT / "research/hat-makers/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-25", "dateModified": "2026-10-25",
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
    <span>Austin &middot; London &middot; Los Angeles</span><span class="dot"></span>
    <span>18 hats &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a stack of Communal hats on a rock by the water, a bearded man in a Duke + Dexter Eat Dirt cap in a motorcycle garage, and two people in Winslow sweatshirts in a green California field" fetchpriority="high" /></div></div>
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
