#!/usr/bin/env python3
"""build-criquet-revisit.py — "Brand Revisited: Criquet" (Willie Forever + fall 2026). Cloned from build-rtg-revisit.py. 20 October 2026.
Lenny: "Let's do a brand revisited - Criquet" -> options sheet -> "build it" (our picks: Willie Forever #2,3,4,6,7,8; fall #9,10,11,13,14,15,24,25,28,34,35,39).
FACTS: criquetshirts.com products.json, Oct 20, 2026 (~100 own-line products new since our Aug 25 Brand to Know; custom/licensed team
pieces excluded except the officially licensed "Willie Forever" collection, published Oct 15-16). Product copy paraphrased; Willie pieces
are made to order (6-8 business days per Criquet). Founders/story from our Aug 25 Brand to Know.
PHOTOS: Criquet's own.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Criquet Revisited: Willie Forever and the Fall 2026 Line"
DESC = ("We revisit Austin's Criquet: the officially licensed Willie Nelson 'Willie Forever' collection, the Coach Nelson "
        "players shirt, quilted shackets, the waxed ranch jacket and cashmere. 18 picks with prices.")
H1 = "Brand Revisited: Criquet, Willie Forever and a Real Fall Line"
BC = "Brand Revisited: Criquet"
SLUG = "brand-revisited-criquet"
IMG = "/images/criquet-revisited"
SHOP = "https://criquetshirts.com/products/"
C = "Criquet"
P = {
 "w1": (C, "Willie Nelson Players Shirt, The Icon", "$128", "willie-nelson-performance-players-shirt-iconic-braids-navy",
   "The Players Shirt with Willie&rsquo;s bandana-and-braids embroidered on the chest pocket, in a performance blend with removable collar stays. Navy, heather navy or heather grey. Like every Willie piece, it&rsquo;s made to order and ships in six to eight business days."),
 "w2": (C, "Willie Nelson Quilted Shacket", "$228", "willie-nelson-quilted-shacket-the-icon-navy",
   "Light quilted nylon with pearl snaps and the Icon embroidered on the right chest. Criquet calls it made for a life spent on the road again, and it packs down small. Navy."),
 "w3": (C, "The Coach Nelson Players Shirt", "$128", "willie-nelson-performance-players-shirt-the-signature-burnt-orange",
   "Our favorite piece here. Burnt orange, a W. Nelson signature on the chest, and a story: Criquet made it to honor Willie&rsquo;s deep roots in Texas football and his long friendship with Longhorn coach Darrell Royal. A college-coach polo you can actually play in."),
 "w4": (C, "Willie Nelson Long Sleeve Players Shirt", "$148", "willie-nelson-long-sleeve-players-shirt-the-icon-peacoat",
   "Pima cotton pique with the Icon on the pocket, cut to wear alone or over another shirt. Peacoat, burnt orange or blackstone."),
 "w5": (C, "Willie Nelson Corduroy Pearl Snap", "$178", "willie-nelson-corduroy-pearl-snap-the-icon-heather-steel-blue",
   "Criquet&rsquo;s cotton corduroy pearl snap with a western back yoke and the Icon on the right chest. Criquet&rsquo;s own words for it: a little outlaw-country soul built in. Heather steely blue."),
 "w6": (C, "Willie Nelson Trucker Hat, Willie Forever Patch", "$35", "willie-nelson-trucker-hat-willie-forever-patch-navy",
   "A navy mesh-back trucker with the red, white and blue Willie Forever patch. The cheapest way into the collection."),
 "o1": (C, "Waxed Ranch Jacket", "$298", "waxed-ranch-jacket-dark-forest",
   "Waxed cotton and nylon with a corduroy collar, built for wind and drizzle. Criquet says it never needs rewaxing and the wax doesn&rsquo;t rub off. Dark forest or bourbon; size up if you layer heavy."),
 "o2": (C, "Corduroy Quilted Shacket", "$218", "corduroy-quilted-shacket-willow",
   "Their Corduroy Pearl Snap and Quilted Shacket combined: cotton corduroy outside, quilted fill inside, pearl snaps at the front, cuffs and pocket. Six colors, from willow and pinecone to a dusty blue plaid ($224)."),
 "o3": (C, "Quilted Shacket", "$208", "quilted-shacket-firewood",
   "The lighter, packable version in diamond-quilted polyester with western pearl snaps, the layer Criquet says you&rsquo;ll grab nine times out of ten. Firewood, hunter green, charcoal, olive, black or navy."),
 "o4": (C, "Member&rsquo;s Guest Jacket", "$218", "members-guest-jacket-camel",
   "Criquet&rsquo;s take on the old Members Only jacket, in faded washed moleskin with a flannel lining and ribbed cuffs and hem. The name alone earns it a spot. Sequoia."),
 "o5": (C, "Vintage Polar Fleece", "$198", "vintage-polar-fleece-blue",
   "The fleece you wore to the lake, the ski lodge and the tailgate, brought back: a soft pullover with a kangaroo pocket and the Grassy C embroidered on the chest. Blue, released October 19."),
 "o6": (C, "Chill-Knit Fleece Shacket", "$188", "chill-knit-fleece-shacket-horizon-stripe-cedar",
   "Soft fleece cut like a button-up, with a western yoke, pearl snaps and collar stays, in two earthy Horizon Stripes. Made for cool tee times and dinner after."),
 "s1": (C, "Legacy Cashmere Pocket Crew", "$348", "legacy-cashmere-pocket-crew-stonewash-blue",
   "The most expensive thing here: 100% cashmere crewneck with Criquet&rsquo;s signature pocket, which they call cashmere for guys who don&rsquo;t take themselves too seriously. Rainey, espresso or brick road."),
 "s2": (C, "Long Sleeve Bungalow Sweater Polo", "$168", "long-sleeve-bungalow-sweater-polo-navy",
   "Their best-selling Bungalow Sweater Polo with long sleeves: soft pima cotton knit, contrast cuffs and faux horn buttons. Navy or oat."),
 "s3": (C, "Corduroy Pearl Snap", "$158", "corduroy-pearl-snap-midnight-oil",
   "The Criquet shirt Austin wears most from October on: cotton corduroy, a western back yoke, pearl snaps and a pocket with a sunglasses slot. Nine colors this fall, including Dirty Martini and Whiskey Barrel."),
 "s4": (C, "Slim Fit Long Sleeve Players Shirt", "$134", "slim-fit-long-sleeve-players-shirt-stay-frosty",
   "The long-sleeve Players Shirt in Peruvian pima, now in a slim fit, with names only Criquet would choose: Knight Rider, Christian Slater, River City, Stay Frosty, Chestnut and Glacier."),
 "s5": (C, "Collared Sweatshirt", "$168", "collared-sweatshirt-heather-blue",
   "A fleece-lined sweatshirt with a crisp collar, rugby details and a kangaroo pocket. Criquet calls it the easiest style upgrade since matching socks. Seven heathers, burnt orange included."),
 "s6": (C, "Comfort Corduroy Pant", "$154", "comfort-corduroy-pant-khaki",
   "The classic Criquet pant in a cotton-Tencel corduroy with a little stretch, in 30, 32 or 34-inch inseams and a Grassy C on the back hip. Khaki or faded navy."),
}
SECTIONS = [
 ("Willie Forever", "willie", ["w1","w2","w3","w4","w5","w6"],
  "<strong>Officially licensed &middot; new Oct 15&ndash;16 &middot; $35&ndash;$228</strong>An Austin golf brand and Willie Nelson. Criquet&rsquo;s officially licensed &ldquo;Willie Forever&rdquo; collection puts &ldquo;The Icon,&rdquo; Willie&rsquo;s bandana and braids, on players shirts, a shacket and a pearl snap. Every piece is made to order."),
 ("Fall Outerwear", "outerwear", ["o1","o2","o3","o4","o5","o6"],
  "<strong>Six layers &middot; $188&ndash;$298</strong>The biggest change since August: Criquet now has a full rack of fall jackets, from a waxed ranch jacket to quilted and corduroy shackets and a polar fleece."),
 ("Shirts, Knits &amp; Pants", "shirts", ["s1","s2","s3","s4","s5","s6"],
  "<strong>Six picks &middot; $134&ndash;$348</strong>Cashmere, a long-sleeve sweater polo, nine corduroy pearl snaps and the long-sleeve Players Shirt in a new slim fit."),
]
N = 18
PQ = {"willie": ("A little outlaw-country soul built in.", "Criquet, on the Willie Nelson Corduroy Pearl Snap")}
CAP = "Photography &middot; Criquet"
BANDS = {"willie": ("Willie Forever, on the course and off", "From Criquet&rsquo;s campaign shoot.", [("band-1","A golfer in the burnt-orange Coach Nelson Players Shirt and a white cap on a course","The Coach Nelson"),("band-2","A man in the Willie Nelson Corduroy Pearl Snap playing an acoustic guitar","The pearl snap"),("band-3","A man in the Willie Nelson Quilted Shacket in front of red, white and blue bunting","The shacket")])}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we wrote our <a href="/drops/brand-to-know-criquet" style="border-bottom:1px solid var(--ink)">Brand to Know on Criquet</a> in August, the story was one shirt: Billy Nachman and Hobson Brown&rsquo;s Players Shirt, rebuilt from his grandfather&rsquo;s closet in Austin in 2010. Two months later, Criquet has released roughly a hundred new products of its own, and the most Austin thing it has ever made.</p>
    <p>That&rsquo;s Willie Forever, an officially licensed Willie Nelson collection that landed October 15 and 16. It&rsquo;s done with restraint: a small embroidered bandana and braids, &ldquo;The Icon,&rdquo; on a pocket or chest. The standout is the Coach Nelson Players Shirt, a burnt-orange polo Criquet made to honor Willie&rsquo;s friendship with Longhorn coach Darrell Royal. It is hard to imagine a shirt that belongs more to this city.</p>
    <p>The rest of the fall line answers the one question we had in August, which was what Criquet looks like when it&rsquo;s cold. The answer is shackets in quilted nylon and corduroy, a waxed ranch jacket, a cashmere crew and nine colors of the corduroy pearl snap. It still reads as golf on a tee box and as nothing in particular on South Congress three hours later.</p>
    <p>If you buy one thing: the Coach Nelson Players Shirt. If it&rsquo;s cold: the Corduroy Quilted Shacket.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Criquet</span></div>
      <div class="sidebar-detail"><span class="l">Based in</span><span>Austin, Texas</span></div>
      <div class="sidebar-detail"><span class="l">First covered</span><span>August 25, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Collab</span><span>Willie Forever (licensed)</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$35&ndash;$348</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Coach Nelson Players Shirt, $128</span></div>
      <div class="hashtags">
        <span class="hashtag">#Criquet</span>
        <span class="hashtag">#WillieForever</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is the Criquet Willie Nelson collection?", "Willie Forever is Criquet's officially licensed Willie Nelson collection, released October 15–16, 2026. It includes players shirts ($128), a long-sleeve players shirt ($148), a quilted shacket ($228), a corduroy shacket ($238), a corduroy pearl snap ($178) and hats ($35), all with Willie's bandana-and-braids 'The Icon' embroidery. Pieces are made to order and ship in 6–8 business days."),
 ("What is the Coach Nelson Players Shirt?", "A burnt-orange Criquet players shirt ($128) from the Willie Forever collection that honors Willie Nelson's roots in Texas football and his friendship with Longhorn coach Darrell Royal."),
 ("What's new from Criquet for fall 2026?", "Outerwear: the Waxed Ranch Jacket ($298), Corduroy Quilted Shacket ($218–$224), Quilted Shacket ($208), Member's Guest Jacket ($218) and Vintage Polar Fleece ($198), plus a Legacy Cashmere Pocket Crew ($348) and nine colors of the Corduroy Pearl Snap ($158). Prices checked October 20, 2026."),
 ("Where is Criquet from?", "Austin, Texas. Billy Nachman and Hobson Brown started it there in 2010, building the Players Shirt from a vintage golf shirt left by Nachman's grandfather."),
]
FRN = json.loads((ROOT / "research/criquet-revisit/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-19", "dateModified": "2026-10-19",
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
    <span>Brand Revisited &middot; Austin &middot; first covered August 25, 2026</span><span class="dot"></span>
    <span>18 picks &middot; checked October 20, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three Criquet photos: a golfer in the burnt-orange Coach Nelson Players Shirt, a man in a cowboy hat and the Willie Nelson Corduroy Pearl Snap, and a man in a cowboy hat and the Waxed Ranch Jacket" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Dim Sum", "Rowena", "Swisher", "Read The Green", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
