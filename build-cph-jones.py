#!/usr/bin/env python3
"""build-cph-jones.py — Jones x Cph/Golf, round two (October 2026). 23 October 2026. Cloned from build-outdoor-golf.py.
Lenny: "let's do a post about the CPH & Jones collab- https://captainshelmgolf.com/en/collections/new".
FACTS + PRICES: research/cph-jones/store-new.json (Cph/Golf's own store, /en/collections/new products.json, 23 Oct 2026; JPY).
USD at 158.10 JPY/USD (open.er-api.com, 22 Oct 2026). Store is Japan-only (shipping policy, countryCode JP). Jones background from
drops/brand-revisited-jones-sports-co.html (sourced there); Jones US Trouper prices from jonessportsco.com products.json, 23 Oct 2026.
Images: Cph/Golf's own product shots + Oct 16 2026 lookbook on its product pages (research/cph-jones/frame.py). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Jones x Cph/Golf Collab: The Full October 2026 Drop"
DESC = ("Jones Sports Co. and Tokyo's Cph/Golf reunite: a 90s wind breaker, mock necks, pants, caps and a "
        "Trouper stand bag, with yen and dollar prices.")
H1 = "Jones &times; Cph/Golf, Round Two: Portland&rsquo;s Bag Maker in Tokyo"
BC = "Jones &times; Cph/Golf"
SLUG = "jones-cph-golf-collab"
IMG = "/images/cph-jones"
SHOP = ""
B = "Jones &times; Cph/Golf"
S = "https://captainshelmgolf.com/en/products/"
P = {
 "j1": (B, "Stadium Wind Breaker Jacket", "&yen;26,400 (~$167)", S + "chg26-jn-j02",
   "The headline piece: a 90s-style jacket that crosses Jones&rsquo;s classic logo with Cph&rsquo;s, ribbed at the shoulders so it stays out of the swing, cut short and boxy. Navy/white is in M&ndash;XL; black is down to M."),
 "j2": (B, "Team LS Mock Neck Tee", "&yen;13,200 (~$83)", S + "chg26-jn-t03",
   "Cotton-based stretch jersey with both logos on the chest. Cph/Golf pitches it as the layer under a polo. White and navy in M&ndash;XL; black in XL only."),
 "j3": (B, "Polo Sweat Pullover", "&yen;15,400 (~$97)", S + "chg26-jn-t04",
   "A sweatshirt-style pullover polo in stretch cotton pique, colored as a nod to Jones&rsquo;s caddie bags. Wear it over the mock neck, the way the lookbook does."),
 "j4": (B, "Adjustable Pants The 1st", "&yen;18,700 (~$118)", S + "chg26-jn-p02",
   "Stretch tapered pants with a logo jacquard elastic band set into the waist like a belt, so the fit adjusts, and colored piping at the pockets. Navy or black, M and L."),
 "j5": (B, "Team Cap", "&yen;8,800 (~$56)", S + "chg26-jn-c02",
   "A hybrid jet cap in mixed materials, including the pants fabric, colored like a Jones bag, with &ldquo;1971&rdquo; on the side. Navy or black."),
 "j6": (B, "Team Corded Bucket Hat", "&yen;8,800 (~$56)", S + "chg26-jn-c03",
   "The same mixed-material build as a bucket hat, with a drawcord for windy rounds. Black, or white with a navy brim."),
 "j7": (B, "Trouper Stand Bag", "&yen;88,000 (~$557)", S + "chg26-jn-cb03_1",
   "Jones&rsquo;s Trouper in water-repellent, hard-wearing ripstop: seven pockets including an insulated cooler pocket and a fleece-lined valuables pocket, double straps that convert to single, a five-way top and 2.6 kg. Black or navy; on sale October 28."),
 "j8": (B, "Leather Cylinder Head Cover (Driver)", "&yen;8,800 (~$56)", S + "chg26-jn-a02",
   "A tube-shaped driver cover in faux leather, colored after Jones&rsquo;s bags. White or black; on sale October 28."),
 "j9": (B, "Cylinder Head Cover (Wood)", "&yen;7,700 (~$49)", S + "chg26-jn-a03",
   "The fairway-wood version in the same faux leather. Black or white; on sale October 28."),
 "j10": (B, "Leather Cylinder Head Cover (Utility)", "&yen;7,150 (~$45)", S + "chg26-jn-a04",
   "The hybrid size, to finish the set. White or black; on sale October 28."),
}
SECTIONS = [
 ("To Wear: Jacket, Mock Neck, Polo Sweat and Pants", "wear", ["j1","j2","j3","j4","j5","j6"],
  "<strong>Six pieces &middot; &yen;8,800&ndash;&yen;26,400 (~$56&ndash;$167)</strong>Navy, black and white, worn in layers. Women&rsquo;s versions of the jacket and polo sweat are in stock in S, with a matching stretch skirt."),
 ("In the Bag: The Trouper Stand Bag and Three Cylinder Covers", "bag", ["j7","j8","j9","j10"],
  "<strong>On sale October 28 &middot; &yen;7,150&ndash;&yen;88,000 (~$45&ndash;$557)</strong>The bag is the piece to watch. Jones&rsquo;s own <a href=\"https://jonessportsco.com\">Troupers</a> in licensed school colors run $375 to $430 in the US."),
]
N = 10
PQ = {
 "bag": ("Who could have known? George Jones, that&rsquo;s who.", "Jones Sports Co., on its founder"),
}
BANDS = {
 "wear": ("Shot on a Japanese course, October 16. ",
   "Cph/Golf&rsquo;s lookbook for the drop: three players in navy, black and white, Jones Sports Co. across the backs and 1971, the year Jones started, on the sleeves and caps.",
   [("look-1","Three players in the Jones and Cph/Golf collaboration sitting on a bench by the course","The team &middot; Cph/Golf"),
    ("look-2","Three players seen from behind with Jones Sports Co. across their jackets","Jones Sports Co. on the back &middot; Cph/Golf"),
    ("look-3","Players walking away with 1971 printed across their backs","1971 &middot; Cph/Golf")]),
}
LOOKBOOK_FIGS = [
 ("look-4","Two players sitting on a bench beside a fairway"),("look-5","A player in the navy jacket by the flagstick"),
 ("look-6","Three players in the collaboration pieces on a green"),("look-7","Two players in navy on a green with a Jones bag"),
 ("look-8","A player in a black mock neck holding a club"),("look-9","A player in the navy jacket seen from behind"),
 ("look-10","A player in a black outfit beside a pine tree"),("look-11","A player in a white mock neck seen from behind"),
 ("look-12","Two players on a fairway in the collaboration pieces"),
]
KIT_CSS = ""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>Jones Sports Co. and Cph/Golf are back together. The Portland bag maker and the Tokyo brand first worked together in February, when the drop included a pack of 50 co-branded wood tees. Round two landed on Cph/Golf&rsquo;s store on October 21 and goes further: outerwear, layers, pants, two hats, three headcovers and a stand bag.</p>
    <p><strong>The look is 90s.</strong> Cph/Golf describes the jacket as a 90s design that crosses Jones&rsquo;s classic logo with its own, and the clothes borrow their colors from Jones caddie bags: navy, black and white, with &ldquo;1971&rdquo;, the year Jones started, stitched on backs and caps. It reads like a team kit for a club that doesn&rsquo;t exist, and that is the appeal.</p>
    <p><strong>It is built for the swing, too.</strong> The wind breaker has rib at the shoulders so it stays out of the way at the top, the pants are stretch with a logo elastic waistband that adjusts like a belt, and the mock neck is meant to sit under the polo sweat. The pieces are designed to be worn together, and the cap and bucket hat use the pants fabric.</p>
    <p><strong>The bag is the one to watch.</strong> It is Jones&rsquo;s Trouper stand bag in water-repellent ripstop, with seven pockets including a cooler pocket, at &yen;88,000 (about $557). It goes on sale October 28 with the three cylinder headcovers.</p>
    <p><strong>Who it&rsquo;s for.</strong> Anyone who already carries a Jones and wants the clothes to match it, and anyone who likes Cph/Golf&rsquo;s habit of dressing golf like a sports team rather than a country club. If you only buy one thing, make it the jacket: it is the piece the whole shoot is built around, and it works off the course as a plain 90s windbreaker. The mock neck and cap are the easy, cheaper ways in.</p>
    <p><strong>The catch is geography.</strong> Cph/Golf&rsquo;s webstore is set up for Japan only and its shipping policy covers domestic delivery. From the US, the routes are a proxy service that buys for you or a forwarding service with a Japanese address, both at extra cost. Prices below are in yen with dollars at about &yen;158 to the dollar (October 22, 2026), before shipping, fees or duties.</p>
    <p>More on both brands: our <a href="/drops/brand-revisited-jones-sports-co">Jones Sports Co. Brand Revisited</a>, our <a href="/drops/brand-revisited-cph-golf">Cph/Golf Brand Revisited</a>, and the <a href="/drops/apc-golf-cph-golf-collab">A.P.Cph/Golf collab</a> from September.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Drop</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Jones &times; Cph/Golf</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>Oct 21; bag Oct 28</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>10 men&rsquo;s &amp; unisex</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>&yen;7,150&ndash;&yen;88,000</span></div>
      <div class="sidebar-detail"><span class="l">Ships</span><span>Japan only</span></div>
      <div class="hashtags">
        <span class="hashtag">#JonesSportsCo</span>
        <span class="hashtag">#CphGolf</span>
        <span class="hashtag">#GolfCollab</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
_lb = "\n".join(f'  <figure><img src="/images/cph-jones/{f}.jpg" alt="{a}, from Cph/Golf&rsquo;s lookbook for the Jones collaboration" loading="lazy" /></figure>' for f, a in LOOKBOOK_FIGS)
KIT = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">The Jones &times; Cph/Golf Lookbook</h2>
  <p class="cat-kicker">More from Cph/Golf&rsquo;s October 16 shoot. Photography &middot; Cph/Golf.</p>
  <div class="ig-grid">
{_lb}
  </div>
</section>
"""
FAQ = [
 ("Where can I buy the Jones x Cph/Golf collab?", "On Cph/Golf's own webstore (captainshelmgolf.com). The store is set up for Japan only, so buyers outside Japan need a proxy shopping service or a forwarding address."),
 ("When does the Jones x Cph/Golf Trouper stand bag come out?", "The Trouper Stand Bag and the three cylinder headcovers go on sale October 28, 2026. The clothing and hats were released October 21."),
 ("How much is the Jones x Cph/Golf stand bag?", "88,000 yen, about $557 at October 2026 exchange rates, before shipping, fees and duties."),
 ("Is this the first Jones and Cph/Golf collaboration?", "No. It is the second; the first came in February 2026 and included a pack of 50 co-branded wood tees."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
_FR = json.loads((ROOT / "research/cph-jones/frames.json").read_text())
FRN = {k: [f"{IMG}/{f}" for f in _FR[k[1:]]] for k in P}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
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
         "url": URL, "image": og, "datePublished": "2026-10-23", "dateModified": "2026-10-23",
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Grassy Issue &middot; Collab drop</span><span class="dot"></span>
    <span>10 pieces &middot; prices checked October 23, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Players in the Jones and Cph/Golf collaboration on a golf course, from Cph/Golf&rsquo;s lookbook" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += KIT
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + KIT_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
