#!/usr/bin/env python3
"""build-mackem-btk.py — Brand to Know: Mackem Golf (cloned from build-slice-town-btk.py). 6 October 2026.
Lenny: "let's do a brand to know - https://mackemgolf.com/". Options sheet: the recommended 18, hero C then
"actually, D is better" (the check alignment-stick cover across a set of irons).
FACTS: catalogue, AUD prices and stock from mackemgolf.com on 6 Oct 2026 (research/mackem/options.json). Story
from Mackem's About Us, Perth shop, custom and football-shirt pages; founders' names and Adam's quote as already
verified for drops/golf-brands-founded-by-women and drops/australian-golf-brands-and-trips. A$1 = ~$0.66.
PHOTOS: Mackem's own store and site images, localised to /images/mackem (research/mackem/make_frames.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Mackem Golf: Wool Headcovers Hand-Sewn in the Perth Hills"
DESC = ("Brand to Know: Mackem Golf, the Perth headcover studio run by Paige Harding and Adam Brown. Tartan, corduroy "
        "and houndstooth covers, waxed canvas pouches and custom work, with prices.")
H1 = "Brand to Know: Mackem Golf &mdash; Wool Headcovers from the Perth Hills"
BC = "Mackem Golf"
SLUG = "brand-to-know-mackem-golf"
IMG = "/images/mackem"
SHOP = "https://mackemgolf.com/products/"
A = "Mackem Golf"
WOOD = "A$85&ndash;100 (~$56&ndash;66)"
P = {
 "M01": (A, "Killhope", WOOD, "killhope",
   "The newest cover in the corduroy line, in a rusty brown the brand says comes from the colour of the Australian bush. Thick, soft and warm-looking, it sits well next to tweeds and checks. Every size is in stock, from A$100 for a driver down to A$85 for a hybrid."),
 "M03": (A, "Fawcett", WOOD, "fawcett",
   "Cut from deadstock wool-blend fabric in deep red, burnt orange and brown checks. It is the cover that best shows what Mackem does: old-school cloth, quiet colours, and a short run because the fabric will not come back. All four sizes in stock."),
 "M04": (A, "Wolsingham", "A$85&ndash;90 (~$56&ndash;59)", "wolsingham",
   "This is a jumbo houndstooth in a thick, brushed wool. Mackem says it only got a few metres of the cloth, so this is a limited drop, and only the fairway and hybrid sizes are left."),
 "M05": (A, "Oakfield Barrel", "A$95&ndash;120 (~$63&ndash;79)", "oakfield-barrels",
   "The Oakfield comes in the barrel shape, a straight tube rather than a fitted head, in a deadstock houndstooth of cream, black, ochre and bordeaux. It has a soft sherpa lining. Driver A$120, fairway A$100, hybrid A$95."),
 "M22": (A, "Alnwick", WOOD, "alnwick",
   "A loud yellow check with red, green, blue and white running through it, woven in a wool blend. It is the brightest cover in the range and the one that ties a bag of darker covers together. All four sizes in stock."),
 "M27": (A, "Patchwork Headcover", "A$140 (~$92)", "patchwork-headcover",
   "Pieced together from current fabrics and deadstock offcuts, so no two are the same. You choose a colour family, or pick Lucky Dip and let the studio decide. If you order other covers, they will work some of that fabric into the patchwork so the set matches."),
 "M66": (A, "Contours", "A$110&ndash;125 (~$73&ndash;83)", "contours",
   "Indigo denim with a topographic contour pattern sewn into it by machine, made to order so every one is different. The brand says it is &ldquo;for the golf nerds, the architect lovers, the green readers &amp; nature needers.&rdquo; The denim fades with use like a pair of jeans."),
 "M48": (A, "Whitburn", "A$90&ndash;100 (~$59&ndash;66)", "whitburn",
   "A classic grey and white herringbone for a bag that wants good cloth without a loud pattern. Driver A$100 and fairway A$90 are in stock."),
 "M21": (A, "Alnwick Mallet Putter Cover", "A$110&ndash;120 (~$73&ndash;79)", "alnwick-mallet-putter-cover",
   "The yellow Alnwick check on a mallet cover, with a fleece lining and a magnetic closure. It comes in a standard mallet shape and three centre-shaft fits, including Spider, DF3 and OZ1 shapes."),
 "M54": (A, "Greenford Blade Putter Cover", "A$100&ndash;110 (~$66&ndash;73)", "greenford-blade-putter-cover",
   "Olive waxed canvas on the outside, which darkens and picks up a patina the more it is used, and a patterned wool lining inside. Magnetic closure, in standard or double-wide blade."),
 "M65": (A, "Contours Putter Cover", "A$110&ndash;125 (~$73&ndash;83)", "contours-putter-headcover",
   "The contour-stitched denim in a putter cover, made to order in a blade, a standard mallet or three centre-shaft shapes. Every one has a magnetic closure."),
 "M26": (A, "Patchwork Putter Cover", "A$125 (~$83)", "patchwork-putter-cover",
   "The patchwork idea on a blade putter cover: offcuts and deadstock pieced together by colour family, or Lucky Dip if you trust them."),
 "M61": (A, "Kielder Rangefinder Pouch", "A$125 (~$83)", "kielder-rangefinder-pouch",
   "Olive waxed canvas with checked wool on the back and through the lining, a padded interior, a magnetic flap you can open with one hand and a metal clip for the bag. It leads the rangefinder section of our <a href=\"/drops/golf-bag-accessories-what-to-hang-from-your-bag\">bag accessories guide</a>."),
 "M62": (A, "Redesdale Rangefinder Pouch", "A$125 (~$83)", "redesdale-rangefinder-pouch",
   "This is the same pouch in rust waxed canvas, with a white and rust houndstooth on the back and inside. Magnetic closure, padded and lined, metal clip."),
 "M59": (A, "Kielder Shag Bag", "A$145 (~$96)", "kielder-shag-bag",
   "A green waxed canvas practice bag that holds more than 30 balls, with a checked, water-resistant ripstop lining and a drawstring top. It is the kind of thing you leave by the practice green or in the sim room."),
 "M08": (A, "Killhope Valuables Pouch", "A$55 (~$36)", "killhope-valuables-pouch",
   "This drawstring pouch comes in the rust Killhope corduroy and is big enough for a dozen balls or your phone, keys and wallet, in the same cloth as the Killhope covers."),
 "M12": (A, "Mackem Golf x ThreePuttPar Hickory Brush", "A$55 (~$36)", "threeputtpar-brush",
   "A groove brush made with ThreePuttPar in real hickory, painted in Mackem&rsquo;s burgundy, white and gold, engraved, and hung on a matching burgundy strap."),
 "M41": (A, "Sutherland Tartan Sunglasses Pouch", "A$25 (~$17)", "sutherland-tartan-sunglasses-pouch",
   "This soft pouch holds sunglasses and comes in a green tartan with black, red and blue, and the cheapest way into Mackem, in a limited run."),
}
SECTIONS = [
 ("Woods", "woods", ["M01","M03","M04","M05","M22","M27","M66","M48"],
  "<strong>Eight picks &middot; ~$56&ndash;$92</strong>Most covers are A$100 for a driver and step down to A$85 for a hybrid, so a driver, fairway and hybrid together come to about $180. The cloth is the point: rust corduroy, deadstock checks, a jumbo houndstooth, a loud yellow tartan, grey herringbone, contour-stitched denim and patchwork made from the offcuts. Every cover is sewn in the Kalamunda studio, and several fabrics run out for good when the roll does."),
 ("Putter Covers", "putter-covers", ["M21","M54","M65","M26"],
  "<strong>Four picks &middot; ~$66&ndash;$83</strong>All of them close with a magnet, and the mallet covers come in centre-shaft shapes as well as a standard mallet. The Greenford&rsquo;s waxed canvas will wear in; the Alnwick is for a putter that should be seen."),
 ("On the Bag", "on-the-bag", ["M61","M62","M59","M08","M12","M41"],
  "<strong>Six picks &middot; ~$17&ndash;$96</strong>Waxed canvas rangefinder pouches with magnetic flaps, a shag bag for practice, a corduroy valuables pouch, a hickory brush made with ThreePuttPar, and a tartan sunglasses pouch for A$25."),
]
N = 18
PQ = {
 "putter-covers": ("We&rsquo;re not Amazon Prime and never want to be.", "Adam Brown, Mackem Golf"),
}
CAP = "Photography &middot; Mackem Golf&rsquo;s own"
BANDS = {
 "woods": (CAP, "The studio on Haynes Street in Kalamunda, where everything is cut and sewn.", [("band-1","Paige Harding and Adam Brown standing in their studio in front of shelves of headcovers, with their dog","Paige and Adam"),("band-2","An industrial sewing machine in the Mackem studio","The machine"),("band-3","A worktable in the studio with boxes of fabric and finished pieces","The workroom")]),
 "putter-covers": (CAP, "Mackem photographs its cloth up close and on the bag.", [("band-4","A close-up of a black, white and red houndstooth headcover","Houndstooth"),("band-5","Pastel check headcovers on a bag against a green wall","Pastels"),("band-6","An old leather golf bag by a window","The leather bag")]),
 "on-the-bag": (CAP, "The brand also takes its covers out on the course.", [("band-7","A tartan rangefinder pouch and a rangefinder on the grass","On the grass"),("band-8","Check headcovers on a bag on a golf cart on the course","On the cart"),("band-9","A tartan pouch clipped to a black golf bag in the late sun","Clipped on")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Mackem Golf makes headcovers the way a good tailor makes a jacket: they choose the cloth themselves, cut it in their own studio and sew it by hand. Paige Harding and her partner Adam Brown run it from a studio and shop on Haynes Street in Kalamunda, in the hills outside Perth. Paige has the textiles background and does the pattern-making; the brand describes itself as a small team that makes everything in-house.</p>
    <p>The name comes from Adam. He is from Sunderland, in the north-east of England, where locals are called Mackems. The brand tells the shipyard story behind it on its About page: Sunderland built the ships and other towns fitted the engines, so in the local accent, &ldquo;we would &lsquo;mack &rsquo;em&rsquo;, they would &lsquo;tak &rsquo;em&rsquo;.&rdquo; Most of the covers are named after places in that part of England, from Killhope and Kielder to Roker and Seaburn.</p>
    <h2 class="products-hdr btk-story-hdr">The Cloth</h2>
    <p>Mackem uses wool blends for their natural water resistance, and a lot of deadstock, so many fabrics are gone when the roll runs out. The influences are Scottish tartan and what the brand calls &ldquo;a moody colour palette drawn from beautiful landscapes all around the world.&rdquo; Alongside the range there is custom work: family tartans, in-house embroidery, dog portraits, and covers made from old football shirts, sent in by the customer and cut up in the studio.</p>
    <p>For an American bag, a Mackem cover is the easiest way to look like you shopped somewhere nobody else did. A driver cover is A$100, about $66, and the brand offers free delivery to the US on orders over A$500. Start with the Fawcett or the Alnwick, and add a Kielder pouch for the rangefinder. Prices and stock were read on mackemgolf.com on 6 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Kalamunda, Perth, Western Australia</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Paige Harding and Adam Brown</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Cut and sewn in their own studio</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Wool, tartan and corduroy headcovers</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>A$25&ndash;A$145 (~$17&ndash;$96)</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Fawcett driver cover, A$100</span></div>
      <a href="https://mackemgolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Mackem Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MackemGolf</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#AustralianMade</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who owns Mackem Golf?", "Paige Harding and her partner Adam Brown. Paige has the textiles background and does the pattern-making, and the pair run the brand as a small team in Perth, Western Australia."),
 ("Where are Mackem headcovers made?", "In Mackem's own studio and shop at Haynes Street in Kalamunda, in the hills outside Perth. The brand designs, cuts and sews everything in-house."),
 ("Why is it called Mackem?", "Co-founder Adam is from Sunderland in England, where locals are called Mackems. The brand's story is that Sunderland built ships and other towns fitted the engines: 'we would mack 'em, they would tak 'em.'"),
 ("How much are Mackem headcovers?", "On 6 October 2026 most covers were A$100 for a driver, A$95 mini driver, A$90 fairway and A$85 hybrid, about $56 to $66. Putter covers are A$100 to A$125 and rangefinder pouches A$125. Mackem offers free delivery to the US over A$500."),
 ("Can Mackem make a custom headcover?", "Yes. It sources fabric to order, including family tartans, embroiders in-house, makes dog-portrait covers, and turns old football shirts and leather jackets into headcovers."),
]
FRN = json.loads((ROOT / "research/mackem/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-MK-GRID*/.products-grid[data-n="8"],.products-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.products-grid[data-n="6"]{grid-template-columns:repeat(3,minmax(0,1fr))}'
            '@media(max-width:1024px){.products-grid[data-n="8"],.products-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:820px){.products-grid[data-n="6"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '@media(max-width:480px){.products-grid[data-n="8"],.products-grid[data-n="6"],.products-grid[data-n="4"]{grid-template-columns:1fr}}</style>\n')
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
    <span>Hand-sewn headcovers from Perth, Western Australia</span><span class="dot"></span>
    <span>18 picks &middot; checked 6 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A Mackem check alignment-stick cover lying across a set of irons on a timber table" fetchpriority="high" /></div></div>
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
