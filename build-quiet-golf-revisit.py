#!/usr/bin/env python3
"""build-quiet-golf-revisit.py — Quiet Golf, Revisited (same URL). Cloned from build-mackem-btk.py. 7 October 2026.
Lenny: "Let's do the Quiet Golf refresh- full treatment and brought back to the 1st homepage slot", then
"go with all 20, also pull images but make sure you keep the quote that got us that forbes shout-out".
WHY: 20 of the 24 product links on the August page were dead; the store was cut back and rebuilt for fall.
FACTS: catalogue, prices and stock read from quietgolf.com products JSON on 7 Oct 2026
(research/quiet-golf-2026/catalog.json). Founder story as already verified for the August page; journal quotes
verbatim from Quiet Golf's own journal, The Adirondack (Diego Diaz, 11 Jul 2026; Christion Lennon, 3 Aug 2026).
The Christion Lennon "some people go on runs" pull-quote is kept word for word (Lenny: the Forbes shout-out).
Dropped from the old page: the "Retail for us..." line (flagged unverifiable), and every mention of another publication.
PHOTOS: Quiet Golf's own store, journal and site images, localised to /images/quiet-golf-2026.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Quiet Golf: The Costa Mesa Golf Brand, Revisited for Fall"
DESC = ("Quiet Golf, revisited: the Costa Mesa label from Christion Lennon and the Diaz brothers. Fall polos, a Sentinel Scout and Harris Tweed covers, with prices.")
H1 = "Quiet Golf, Revisited &mdash; Less Performance, More Presence"
BC = "Quiet Golf"
SLUG = "brand-to-know-quiet-golf"
IMG = "/images/quiet-golf-2026"
SHOP = "https://quietgolf.com/products/"
A = "Quiet Golf"
PO = "$114"
P = {
 "scout": (A + " x Sentinel Golf", "Scout", "$140", "qg-x-sentinel-golf-scout-bag-1",
   "Sentinel&rsquo;s small clip-on Scout, made in the USA, in a Quiet Golf version with the QG monogram. It fits a rangefinder or valuables in a 3.5 by 5 inch pocket, with a neoprene lining, a Fidlock magnetic closure, a waterproof YKK zip and a brass swivel hook. Navy is the color still in stock. See our <a href=\"/drops/brand-to-know-sentinel-golf\">Sentinel profile</a> for the rest of the Minneapolis range."),
 "htdriver": (A, "Harris Tweed Driver Cover", "$132", "harris-tweed-driver-head-cover",
   "Cut to order and sewn by hand in the USA with Ross Co. Golf, in certified Harris Tweed from the Outer Hebrides and Oregon wool. Blue Geometric and Tan Overcheck are in stock, both with the QG roundel on top."),
 "htfairway": (A, "Harris Tweed Fairway Cover", "$114", "harris-tweed-fairway-wood-head-cover",
   "The matching fairway cover, in the same handwoven tweed and Oregon wool. Blue Tartan and Tan Overcheck are in stock, so you can pair it with the driver or mix the two."),
 "incense": (A, "Quiet Please Incense Holder", "$25", "quiet-please-incense-holder",
   "This ten-inch acrylic incense holder carries QUIET PLEASE down its length, the same words as the tournament-style sign in the Costa Mesa store. It is the cheapest way into the brand, and the one piece here that is not for the course, but it says more about how the founders think about golf than most of the polos do."),
 "cardroom": (A, "Cardroom Corduroy Jacket", "$198", "cardroom-corduroy-jacket",
   "The Cardroom is a tan cotton corduroy jacket with a polyester lining, angled hand pockets and a small embroidered QG flag. It is the fall piece in the new range, the jacket you wear to the course and keep on at dinner. Every size is in stock."),
 "monterey": (A, "Monterey Hoodie", "$148", "monterey-hoodie",
   "Milled in Portugal from a cotton, modal and nylon blend, with what the brand calls a naturally soft hand feel, a tonal logo on the chest and ribbed cuffs. Five colors, fern to rose, all in stock."),
 "sanpant": (A, "San Marino Pant", "$178", "san-merino-pant",
   "The San Marino is a golf trouser in a cotton, nylon and spandex blend, with a snap front and a secondary button. Quiet Golf cuts it with extra length to allow for the high cotton content, and says to order your true size. It comes in navy and bone, and it pairs with every polo below."),
 "sanshort": (A, "San Marino Short", "$148", "san-merino-short",
   "The short uses the same fabric at a 7.5-inch inseam, so it stays lightweight, four-way stretch and quick-drying, with the same snap front. Navy and bone are both available, and waist sizes 28 to 36 were in stock when we checked."),
 "vintage": (A, "Vintage Supima Cotton Polo", "$118", "vintage-supima-cotton-polo",
   "The cotton polo in a mostly polyester range: 96% Supima cotton with a little stretch, a three-button placket and an embroidered logo, made in Portugal. Seven colors, all in stock, and the one we would buy first."),
 "hampton": (A, "Hampton Polo", PO, "hampton-polo-active-pique",
   "The Hampton is the plain one in the Active Pique line: a stretch polyester pique with Trocas shell buttons and a small embroidered logo. It comes in solid colors, navy and green among them, and it is the polo to buy if you want the fabric without a stripe."),
 "hamptonls": (A, "Hampton Polo, Long Sleeve", "$124", "hampton-polo-long-sleeve-active-pique",
   "The long-sleeve Hampton puts the same pique and shell buttons on a long sleeve, which makes it the polo for a cool first tee in November. Navy is the color in stock."),
 "claremont": (A, "Claremont Polo", PO, "claremont-polo-active-jersey",
   "The Claremont belongs to the new Active Jersey line, a smoother knit than pique, in a fine stripe with shell buttons. It comes in pine and wine, both in stock."),
 "lowell": (A, "Lowell Polo", PO, "lowell-polo-active-jersey",
   "The Lowell is the second Active Jersey polo, in a bolder stripe than the Claremont. It is the loudest polo Quiet Golf makes, which is still not very loud, and it has the same embroidered logo and shell buttons as the rest."),
 "sunny": (A, "Sunny Polo", PO, "sunny-polo-active-pique-1",
   "The Sunny is a pinstripe Active Pique polo with the QG flag embroidered on the chest. Pine and wine are in stock."),
 "remy": (A, "Remy Polo, Stripe", PO, "remy-polo-active-pique-1",
   "The Remy runs a narrow stripe through the Active Pique fabric, in wine or white, with shell buttons and the flag logo on the chest."),
 "randolph": (A, "Randolph Polo", PO, "randolph-polo-active-pique-brown",
   "The Randolph runs a heavier stripe through the Active Pique fabric and swaps the flag for the QG monogram on the chest. It comes in pine and navy, both in stock."),
 "remymono": (A, "Remy Polo, Monogram", PO, "remy-polo-active-pique-brown",
   "This version of the Remy takes the same stripe into brown or pine and uses the QG monogram instead of the flag. Both colors are in stock."),
 "flaghat": (A, "QG Flag Cotton Dad Hat", "$50", "flag-cotton-dad-hat-copy",
   "The flag cap is an unstructured six-panel in cotton twill, with the QG flag embroidered on the front and an adjustable strap. White and wine are in stock."),
 "monohat": (A, "Monogram Cotton Dad Hat", "$50", "qg-cotton-dad-hat",
   "This is the same unstructured cotton cap with the QG monogram embroidered on the front instead of the flag. It comes in navy and pine, with an adjustable strap."),
 "nylonhat": (A, "Monogram Nylon Dad Hat", "$50", "monogram-nylon-dad-hat",
   "The nylon version is lighter, with six unstructured panels and a velcro strap, which makes it the cap for a hot August round. It comes in white, navy and pine."),
}
SECTIONS = [
 ("On the Bag", "on-the-bag", ["scout","htdriver","htfairway","incense"],
  "<strong>Four picks &middot; $25&ndash;$140</strong>The two new collaborations lead the range: a Sentinel Scout made in the USA and Harris Tweed covers sewn by hand with Ross Co. Golf in Oregon. The incense holder is the one thing here for the house."),
 ("Outerwear and Bottoms", "outerwear", ["cardroom","monterey","sanpant","sanshort"],
  "<strong>Four picks &middot; $148&ndash;$198</strong>The fall additions: a corduroy jacket, a soft hoodie milled in Portugal, and the San Marino pant and short in a stretch cotton blend."),
 ("The Polos", "polos", ["vintage","hampton","hamptonls","claremont","lowell","sunny","remy","randolph","remymono"],
  "<strong>Nine polos &middot; $114&ndash;$124</strong>The polo is the core of the brand now. There is one cotton polo, the Vintage Supima, made in Portugal; the rest are stretch Active Pique or the new, smoother Active Jersey, all with Trocas shell buttons. They come in solids, pinstripes and wider stripes, with either the flag or the QG monogram on the chest."),
 ("Hats", "hats", ["flaghat","monohat","nylonhat"],
  "<strong>Three picks &middot; $50</strong>Unstructured dad hats in cotton or nylon, with the flag or the monogram. The flag five-panel and the visor are sold out for now."),
]
N = 20
PQ = {
 "outerwear": ("Some people go on runs, others go rock climbing or mountain biking. But for us golf is a way to get outside, get away from your phone and have some quiet time for yourself.", "Christion Lennon, Quiet Golf co-founder"),
 "polos": ("Golf has a way of doing that. It cuts through everything else.", "Diego Diaz, Quiet Golf co-founder, in the brand&rsquo;s journal"),
 "hats": ("Some rounds are memorable because of the golf. Others are memorable because of everything surrounding it.", "Christion Lennon, in the brand&rsquo;s journal"),
}
CAP = "Photography &middot; Quiet Golf&rsquo;s own"
BANDS = {
 "on-the-bag": (CAP, "The Costa Mesa flagship, and a nine-hole course built for a single homeowner in Sagaponack, from the brand&rsquo;s journal.", [("band-1","The headcover shadowbox and wood counter inside the Quiet Golf flagship in Costa Mesa","The flagship"),("band-2","A golfer in a striped polo hitting a tee shot on a private nine-hole course in Sagaponack","Sagaponack"),("band-3","The house above the private nine-hole course in Sagaponack","One member")]),
 "polos": (CAP, "Christion Lennon wrote up a spring day at Maidstone for the brand&rsquo;s journal.", [("band-4","Two golfers with carry bags on a fairway at Maidstone","Maidstone"),("band-5","A golfer carrying a bag down a sandy path through the dunes","The walk"),("band-6","The Maidstone clubhouse beyond a green under a blue sky","The clubhouse")]),
 "hats": (CAP, "The brand shoots its own clothes out on the course.", [("band-7","A yellow number eight flag lying on a green with a golfer's shadow","The eighth"),("band-8","A fairway running between dunes toward the sea","Links"),("band-9","Two golfers standing on a tee under a cloudy sky","On the tee")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We like Quiet Golf because nothing on it asks for attention, and for a muni player that makes it the upgrade, not the whole closet. You do not need head-to-toe anything to play Roy Kizer on a Saturday. You need one good polo that still looks right on the back nine in August, a pair of trousers you can wear to lunch afterwards, and a hat that does not shout. That is where Quiet Golf fits: the Vintage Supima polo with the shorts you already own, the San Marino pant when the mornings finally cool off, a flag cap that goes with anything in the bag.</p>
    <p>It also suits how muni golf feels at its best. The founders talk about golf as a way to get outside and away from your phone, and a five-hour Saturday round at a busy city course is exactly that, whether you planned it or not. Clothes built around restraint make sense for a game you play in a crowd. The catch is price. One $114 polo costs more than two weekend rounds at Kizer, so buy one great piece rather than a uniform.</p>
    <h2 class="products-hdr btk-story-hdr">What Changed</h2>
    <p>Since August, the Costa Mesa label has cut its range back and rebuilt it around the polo: nine of them, from the Supima cotton polo made in Portugal to a new, smoother Active Jersey line. The cashmere, the linen trousers and the adidas Samba collaboration have left the store. The best new things are the collaborations, a Scout with Sentinel and Harris Tweed covers sewn with Ross Co. Golf.</p>
    <p>The people are the same. Christion Lennon, who started the fashion label Museum of Peace &amp; Quiet in 2019, runs it with brothers Raul and Diego Diaz, and the flagship at 2949 Randolph Avenue in Costa Mesa is open Tuesday to Sunday. Old Tom Capital led a seed round in 2024, which keeps Quiet Golf off our independent list; the clothes have not got any louder for it. Start with the Vintage Supima Cotton Polo at $118. All 20 pieces below were in stock on quietgolf.com on 7 October 2026, and US shipping is free.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Costa Mesa, California</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Christion Lennon, Raul and Diego Diaz</span></div>
      <div class="sidebar-detail"><span class="l">Flagship</span><span>2949 Randolph Ave, Tue&ndash;Sun 11&ndash;7</span></div>
      <div class="sidebar-detail"><span class="l">New for fall</span><span>Polos, a Sentinel Scout, Harris Tweed covers</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$25&ndash;$198</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Vintage Supima Cotton Polo, $118</span></div>
      <a href="https://quietgolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Quiet Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#QuietGolf</span>
        <span class="hashtag">#BrandRevisited</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#CostaMesa</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who founded Quiet Golf?", "Christion Lennon, who launched the fashion label Museum of Peace & Quiet in 2019, co-founded Quiet Golf with brothers Raul and Diego Diaz."),
 ("Where is the Quiet Golf store?", "The flagship is at 2949 Randolph Avenue in Costa Mesa, California, open Tuesday to Sunday from 11am to 7pm."),
 ("How much does Quiet Golf cost?", "On 7 October 2026 the polos were $114 to $124, the Vintage Supima Cotton Polo $118, the Cardroom Corduroy Jacket $198, the San Marino pant $178, hats $50 and the Harris Tweed driver cover $132. US shipping is free."),
 ("What is the Quiet Golf x Sentinel Scout?", "A $140 version of Sentinel Golf's small clip-on Scout pouch with the QG monogram, made in the USA, sized for a rangefinder or valuables."),
 ("Is Quiet Golf independent?", "It is founder-run, but Old Tom Capital led a seed round in 2024, so it has outside investors."),
]
FRN = json.loads((ROOT / "research/quiet-golf-2026/frames.json").read_text())
FRN = {k: FRN[v[3]] for k, v in P.items()}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-QG-GRID*/.products-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.products-grid[data-n="9"],.products-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}'
            '@media(max-width:1024px){.products-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:820px){.products-grid[data-n="9"],.products-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:480px){.products-grid[data-n="4"],.products-grid[data-n="9"],.products-grid[data-n="3"]{grid-template-columns:1fr}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-08-03", "dateModified": "2026-10-07",
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
    <span>Costa Mesa, California &middot; revisited October 2026</span><span class="dot"></span>
    <span>20 pieces &middot; all in stock, checked 7 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Two golfers walking a sandy path between the fairways, from Quiet Golf&rsquo;s About page" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Old Ghosts", "Hypebeast", "Retail for us"):
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
