#!/usr/bin/env python3
"""build-shoal-btk.py — Brand to Know: Shoal Golf Co. (cloned from build-puttwell-btk.py). 4 October 2026.
Lenny: "let's do a brand to know- https://shoalgolfco.com/", then "let's build it and lean on extra lifestyle IRL
images with a smaller catalog". Six cards (Standard colours merged into one card, towels into one), three IRL bands.
FACTS: catalogue, prices and stock from shoalgolfco.com/products.json on 4 Oct 2026 (research/shoal/catalogue-2026-10-04.json);
mission lines quoted verbatim from the shoalgolfco.com homepage; release quantities from Shoal's own post on X;
quality view quoted from MyGolfSpy (Isaiah McGahee, 13 Aug 2026), attribution only, no link (Lenny: no links out
to other golf publications). PHOTOS: Shoal's own store and homepage images, localised to /images/shoal-golf/btk-*.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Shoal Golf Co.: Waxed-Canvas Golf Bags Made for the Walk"
DESC = ("Brand to Know: Shoal Golf Co. makes waxed-canvas carry bags for golfers who walk: the Standard, the new "
        "Simple Sunday, caps and a No Dirt towel, with prices.")
H1 = "Brand to Know: Shoal Golf Co. &mdash; Waxed Canvas, Made for the Walk"
BC = "Shoal Golf Co."
SLUG = "brand-to-know-shoal-golf"
IMG = "/images/shoal-golf"
SHOP = "https://shoalgolfco.com/products/"
A = "Shoal Golf Co."
P = {
 "s01": (A, "The Standard Bag", "$450 (sold out)", "the-shoal-standard-bag",
   "The bag Shoal is built on: 16 oz waxed canvas with leather trim, a 4-way top, a big zippered belly pocket and both single and double straps, at 6.4 lb without straps. It comes in ten colours released in numbered runs, and Sage uses a lighter 12 oz canvas. Every colour was sold out when we checked, so this is the one to watch for the next window."),
 "s02": (A, "The Simple Sunday Bag", "$250", "the-shoal-simple-sunday-bag",
   "New on 30 September, and the one you can buy today. Waxed canvas, 2.65 lb, an 8-inch top with one divider, one strap and no internal rod, so it folds flat for travel. &ldquo;Crafted for the walk&rdquo; is stitched inside the lower pocket."),
 "s03": (A, "The Shag Bag", "$70", "the-shoal-shag-bag",
   "A waxed-canvas drawstring bag that holds 60 to 65 practice balls, with a canvas carry handle. Better looking than mesh on the back of the cart."),
 "s04": (A, "Cotton Canvas Hat", "$44", "shoal-golf-co-cotton-canvas-hat",
   "A structured cotton canvas cap with an embroidered Shoal patch and a contrast brim, modelled on old club and tournament caps."),
 "s05": (A, "Corduroy Hat", "$44", "shoal-golf-co-corduroy-hat",
   "The corduroy version, with Shoal in embroidered script. Adjustable, one size."),
 "s06": (f"{A} x No Dirt", "Caddie Towel", "$35", "shoal-caddie-towel-white-with-green-stripes",
   "A 44 by 22 inch tour-size towel made with No Dirt, with a built-in scrub pad for clubfaces and grooves. Five colourways, from white with green stripes to olive with cream."),
}
SECTIONS = [
 ("The Bags", "bags", ["s01","s02","s03"],
  "<strong>Three picks &middot; $70&ndash;$450</strong>The Standard is the reason to know Shoal. The Simple Sunday is the lighter, cheaper way in, and it is in stock."),
 ("The Rest of the Kit", "kit", ["s04","s05","s06"],
  "<strong>Three picks &middot; $35&ndash;$44</strong>Two caps and a tour towel: the small things that match the bag. All three were in stock when we checked, and the towel comes in five colourways."),
]
N = 6
PQ = {
 "kit": ("crafted not to distract, but to complement the traditions of golf", "Shoal Golf Co.&rsquo;s mission"),
}
BANDS = {
 "bags": ("Crafted for the walk", "Shoal's own photos.", [("btk-band-1","A golfer on a foggy tee box between cypress trees","Fog on the tee"),("btk-band-2","The Grey Standard Bag on a desert course","Desert nine"),("btk-band-3","The Tan Standard Bag among desert grass and boulders","Last light")]),
 "kit": ("The small things", "", [("btk-band-4","The Navy Standard Bag on a course with palms behind","Navy"),("btk-band-5","The Salmon Standard Bag on a course lined with palms","Salmon"),("btk-band-6","The White Standard Bag lying on a practice range","The White")]),
 "after": ("Out on the links", "", [("btk-band-7","A links fairway under a long bank of cloud","Links"),("btk-band-8","The Sage Standard Bag standing on a fairway","Sage"),("btk-band-9","The Simple Sunday Bag lying on the grass","The Sunday")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Shoal Golf Co. makes golf bags for people who walk, and it makes very few of them. The core of the brand is one bag, the Standard: waxed canvas, leather trim and a four-way top, sold in numbered colour runs that open as preorders a few times a year. Shoal says the bag was &ldquo;inspired by four years of collegiate play,&rdquo; and it describes the goal as a bag &ldquo;that feels as natural to the game as the walk itself.&rdquo;</p>
    <p>That restraint is the appeal. There is no cooler pocket and no logo the size of a dinner plate, just heavy canvas that will crease and darken with years of carrying, and it looks as right at a muni as at an old private club. The new Simple Sunday Bag takes the idea further: 2.65 pounds, one strap and no internal rod, made for a nine-hole evening or a quick range session.</p>
    <p>The colours are where Shoal lets itself have some fun. Each one gets its own note on the site: Sage for windswept fairways and coastal grasses, Teal for the colours beyond the fairway that shift between blue and green in different light, Salmon for warm summer evenings and faded coastal tones, and Grey as the plain, versatile one. The small things follow the same rules. The No Dirt towel is a proper tour size with a scrub pad woven in, the shag bag swaps range mesh for waxed canvas, and the caps borrow from old club and tournament hats. Nothing here is loud, and nothing pretends to be technical gear.</p>
    <p>On quality, the most useful outside view we found comes from a golf style editor who carries a Standard as his own bag. He wrote in August that it &ldquo;looks fantastic, feels genuinely premium,&rdquo; with a little more club tangle than the bags he compared it with, and with midsize grips said it is &ldquo;barely noticeable.&rdquo; The honest caveat is availability. At $450 the Standard is a considered buy, and every colour was sold out when we checked, so pick your colour now and be ready when the next window opens. Prices were read on Shoal&rsquo;s own store on 4 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>United States</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Not named; the brand cites four years of college golf</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Waxed-canvas carry bags in numbered colour runs</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$35&ndash;$450</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Simple Sunday Bag, $250</span></div>
      <a href="https://shoalgolfco.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Shoal &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#ShoalGolfCo</span>
        <span class="hashtag">#CraftedForTheWalk</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#WalkingGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Is the Shoal Standard Bag in stock?", "Not on 4 October 2026: all ten colours were sold out. Shoal releases the Standard in numbered colour runs through preorder windows. One spring release offered 60 Olive, 40 Tan, 25 Grey, 20 Light Blue and 10 Navy."),
 ("How much does the Shoal Standard Bag weigh?", "6.4 pounds without straps, in 16 oz waxed canvas. The Sage colourway uses a lighter 12 oz canvas. The Simple Sunday Bag weighs 2.65 pounds."),
 ("What is the difference between the Standard and the Simple Sunday?", "The Standard ($450) is a full stand bag with a 4-way top, a large belly pocket and single and double straps. The Simple Sunday ($250) is soft and unstructured, with an 8-inch top, one divider, one strap and no internal rod, so it folds for travel."),
 ("What colours does the Standard Bag come in?", "Ten: Grey, Olive, Tan, Navy, Teal, Sage, White, Charcoal, Slate Grey and Salmon. All ten were sold out on 4 October 2026; White, Charcoal, Slate Grey and Salmon arrived in the summer release."),
 ("Who founded Shoal Golf Co.?", "The brand does not name its founder on its site. It says the bag was inspired by four years of collegiate play."),
 ("What is the Shoal x No Dirt towel?", "A 44 by 22 inch tour-size caddie towel made with No Dirt, with a built-in scrub pad for cleaning clubfaces. It cost $35 in five colourways on 4 October 2026."),
]
FRN = json.loads((ROOT / "research/shoal/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
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
         "url": URL, "image": og, "datePublished": "2026-10-04", "dateModified": "2026-10-04",
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
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
    <span>Waxed canvas, made for walking</span><span class="dot"></span>
    <span>6 picks &middot; checked 4 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A Tan Shoal Standard Bag among desert grass and boulders above a golf course at sunset" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    if "after" in BANDS: body += band("after")
    body += faq_html()
    out = head_top() + head_rest + body + tail
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
