#!/usr/bin/env python3
"""build-howie-benson-btk.py — Brand to Know: Howie Benson. Cloned from build-mantra-btk.py. 10 October 2026.
Lenny: "Let's do a brand to know -https://howiebenson.com/", then "do all 16" (every in-stock piece; the Taupe crew and
Tan patch hat were sold out on October 10, 2026 and are left out).
FACTS: howiebenson.com products JSON, home page, Our Story page and Vol. 1 collection page, read October 10, 2026.
The brand names no founder anywhere (site, shop listings, press); the copy never invents one. Quotes are verbatim from
the brand's own pages. Ratings and review counts as displayed on howiebenson.com on October 10, 2026. Badlands
(Atlantic Highlands, NJ) stocks seven pieces per its own collection page.
PHOTOS: Howie Benson's own product and Vol. 1 campaign images (frames in research/howie-benson/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Howie Benson: Resort Polos and Better Taste for Golf"
DESC = ("Brand to Know: Howie Benson, the 2025 golf label behind the Resort Camp Collar Polo. Every in-stock piece from "
        "Vol. 1, from $40 caps to $118 layers, with prices and fit notes.")
H1 = "Brand to Know: Howie Benson &mdash; Better Taste, Less Tradition"
BC = "Howie Benson"
SLUG = "brand-to-know-howie-benson"
IMG = "/images/howie-benson"
SHOP = "https://howiebenson.com/products/"
A = "Howie Benson"
P = {
 # The polos
 "resort-camp-collar-polo-off-white": (A, "Resort Camp Collar Polo, Off-White", "$108", "resort-camp-collar-polo-off-white",
   "The best seller, and the reason to know the brand. Howie Benson calls it &ldquo;a resort shirt made to play 18&rdquo;: the relaxed silhouette and flat camp collar of a vacation shirt, rebuilt as a golf polo in a textured 69% cotton, 31% polyester knit with real stretch. Off-white is the summer-dinner version. It runs slightly large, so size down for a closer fit."),
 "resort-camp-collar-polo-brunette": (A, "Resort Camp Collar Polo, Brunette", "$108", "resort-camp-collar-polo-brunette",
   "The same Resort polo in brunette, a warm rust brown that is the color we would pick for an Austin fall round. The hem is cut to wear tucked or untucked, so it goes from the back nine to dinner with linen trousers without a change."),
 "resort-camp-collar-polo-black": (A, "Resort Camp Collar Polo, Black", "$108", "resort-camp-collar-polo-black",
   "Black takes the Resort polo furthest from the golf course. Same textured knit, same flat camp collar, same relaxed body. On the course it reads as a plain black knit shirt, which is the point. All five sizes in stock."),
 "ottoman-camp-collar-polo-forest-green": (A, "Ottoman Camp Collar Polo, Forest Green", "$98", "ottoman-camp-collar-polo-forest-green",
   "The lighter of the two polos. Howie Benson wanted the stretch and breathability of activewear without dressing like it, so this is a 75% cotton, 25% nylon ottoman knit with a fine ribbed texture and the same relaxed camp collar. Forest green is the color most people buy. It runs true to size; size up for extra room."),
 "ottoman-camp-collar-polo-sand": (A, "Ottoman Camp Collar Polo, Sand", "$98", "ottoman-camp-collar-polo-sand",
   "The Ottoman in sand, a pale khaki that looks right on a dry fairway. It is $10 less than the Resort polo and a little lighter, so it is the one for the hottest rounds of the year."),
 # The layers
 "single-button-pullover-brown": (A, "Single Button Polo Pullover, Brown", "$118", "single-button-pullover-brown",
   "Howie Benson built this as &ldquo;the layer that doesn&rsquo;t look like every other quarter-zip.&rdquo; A textured 96% polyester, 4% spandex knit with enough stretch to swing in, a midweight feel and a single-button collar where the zip would be. The brand shot the brown one at a steakhouse table, which tells you where it is meant to end up."),
 "single-button-pullover-black": (A, "Single Button Polo Pullover, Black", "$118", "single-button-pullover-black",
   "The black version, cut modern through the chest and shoulders. It layers over a Resort polo on a cold first tee or works alone, and it runs true to size. Every size is in stock."),
 "relaxed-fit-crew-natural": (A, "Relaxed Fit Textured Crew, Natural", "$118", "relaxed-fit-crew-natural",
   "A crewneck in a custom double-layer fabric, textured outside and smooth and stretchy inside: 55% cotton, 40% polyester, 5% spandex. It is substantial enough for a cool morning without feeling stiff. Natural is a soft cream that goes over any polo above. It runs slightly large."),
 "relaxed-fit-crew-navy": (A, "Relaxed Fit Textured Crew, Navy", "$118", "relaxed-fit-crew-navy",
   "The same textured crew in navy, which works as hard with jeans as it does over a polo. Ribbed cuffs and hem keep the shape clean. The taupe version was already sold out when we checked."),
 # The hats
 "five-panel-patch-hat-black": (A, "Five-Panel Patch Hat, Black", "$50", "five-panel-patch-hat-black",
   "The technical hat: a five-panel in quick-drying, moisture-wicking fabric with structured front panels, a curved brim, a rubber snapback and a rubber oval HB patch on the front. Every patch hat has a 5.0 rating on the brand&rsquo;s site."),
 "five-panel-patch-hat-navy": (A, "Five-Panel Patch Hat, Navy", "$50", "five-panel-patch-hat-navy",
   "The patch hat in navy, the color the brand puts on its models most often. Built for humid days, which is most days in Austin from May to October."),
 "five-panel-patch-hat-white": (A, "Five-Panel Patch Hat, White", "$50", "five-panel-patch-hat-white",
   "White with the black oval patch. The cleanest of the three in stock (tan is sold out) and the one we would wear with the off-white Resort polo."),
 "two-tone-five-panel-rifle-green": (A, "Two-Tone Five-Panel, Rifle Green", "$45", "two-tone-five-panel-rifle-green",
   "A cotton twill five-panel snapback with a cream crown, a rifle-green brim and the Howie Benson wordmark across the front. It is the one hat here with the name spelled out, and it has nineteen reviews averaging 4.95."),
 "two-tone-five-panel-nude": (A, "Two-Tone Five-Panel, Nude", "$45", "two-tone-five-panel-nude",
   "The two-tone in nude, a cream crown over a tan brim. Howie Benson shot it on a coastal cliff path, and it suits the desert-morning, coastal-afternoon palette of the whole collection."),
 "dad-cap-brown": (A, "Low Profile Dad Cap, Brown", "$40", "dad-cap-brown",
   "A six-panel washed-cotton dad cap with an unstructured crown, a curved brim, an adjustable strap and a small embroidered logo. &ldquo;Fatherhood not required,&rdquo; says the brand. At $40 it is the cheapest way in."),
 "dad-cap-green": (A, "Low Profile Dad Cap, Green", "$40", "dad-cap-green",
   "The dad cap in a deep green. Soft and broken-in from the first wear, and the least golf-looking hat on the page."),
}
SECTIONS = [
 ("The Camp Collar Polos", "polos", ["resort-camp-collar-polo-off-white","resort-camp-collar-polo-brunette","resort-camp-collar-polo-black","ottoman-camp-collar-polo-forest-green","ottoman-camp-collar-polo-sand"],
  "<strong>Five picks &middot; $98&ndash;$108</strong>Two polos, both with a flat camp collar and a relaxed fit: the Resort in a textured cotton-blend knit and the lighter Ottoman in a ribbed cotton-nylon. They are the brand&rsquo;s best sellers, with 45 and 31 reviews."),
 ("The Layers", "layers", ["single-button-pullover-brown","single-button-pullover-black","relaxed-fit-crew-natural","relaxed-fit-crew-navy"],
  "<strong>Four picks &middot; $118</strong>A single-button pullover in place of the usual quarter-zip, and a double-layer textured crew. Both go over the polos above, and both are built to wear with jeans just as easily."),
 ("The Hats", "hats", ["five-panel-patch-hat-black","five-panel-patch-hat-navy","five-panel-patch-hat-white","two-tone-five-panel-rifle-green","two-tone-five-panel-nude","dad-cap-brown","dad-cap-green"],
  "<strong>Seven picks &middot; $40&ndash;$50</strong>Three styles: a technical patch hat, a cotton two-tone snapback and a washed dad cap. Add any hat to a polo or layer and the brand takes $15 off."),
]
N = 16
PQ = {
 "polos": ("Golf had everything figured out except how it looked.", "Howie Benson, Our Story"),
 "hats": ("We pulled from desert mornings and coastal afternoons. Places where golf happens but doesn&rsquo;t dominate.", "Howie Benson, on Vol. 1"),
}
CAP = "Photography &middot; Howie Benson&rsquo;s own"
BANDS = {
 "polos": (CAP, "From the Vol. 1 campaign: desert courses, palms and mountains.", [("band-1","A golfer in a cream sweater and cap leaning on a golf cart on a desert fairway","The cart"),("band-2","Two golfers on a green under tall palms, one putting","The green"),("band-3","Two men in Howie Benson polos on a bench against a stone wall, in black and white","The bench")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Howie Benson is a one-collection brand, and it is a good collection. The idea fits on a hang tag: take the resort shirt, the camp-collar knit you would wear to dinner on vacation, and make it work for eighteen holes. The Resort Camp Collar Polo does exactly that. The collar lies flat, the fit is relaxed without being sloppy, and there is nothing on it that says golf until you are standing on a tee. That is the whole pitch, and the brand puts it in four words: better taste, less tradition.</p>
    <p>What we like is how small and specific it is. Seven designs, sixteen pieces in stock, nothing over $118. There is a pullover with a single button instead of a zip, a crew in a double-layer textured knit, and hats from $40. The product pages read like they were written by people who actually wear the clothes: the model &ldquo;loves a steakhouse Old Fashioned,&rdquo; another &ldquo;swears he doesn&rsquo;t have a Boston accent.&rdquo; For an Austin golfer, the brunette Resort polo and the brown pullover are a fall kit you can wear to the course and straight to dinner on South Congress.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Howie Benson started in 2025 and lists New York, Boston and San Diego as home. It does not name a founder; the brand speaks as &ldquo;we&rdquo; throughout, and says it was started &ldquo;because we couldn&rsquo;t find what we were looking for.&rdquo; Its first collection, Vol. 1: Statement for spring and summer 2026, went live in February. Orders ship the next business day, exchanges are free, and the brand&rsquo;s own site shows 196 reviews, with every piece rated 4.9 or higher. Badlands in Atlantic Highlands, New Jersey carries the polos and layers. All 16 pieces below were in stock on howiebenson.com on October 10, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>New York, Boston, San Diego</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2025</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>The Resort Camp Collar Polo</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>Vol. 1: Statement</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$40&ndash;$118</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Resort Polo, Brunette, $108</span></div>
      <a href="https://howiebenson.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Howie Benson &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#HowieBenson</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#CampCollar</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Howie Benson from?", "The brand lists New York, Boston and San Diego. It started in 2025 and released its first collection, Vol. 1: Statement, in February 2026."),
 ("Who founded Howie Benson?", "The brand does not name a founder on its site. It speaks as \"we\" and says it was started because the people behind it couldn't find the golf clothes they were looking for."),
 ("What is the Resort Camp Collar Polo?", "Howie Benson's best seller: a golf polo with the relaxed fit and flat camp collar of a resort shirt, in a textured 69% cotton, 31% polyester knit. It was $108 on October 10, 2026 and runs slightly large."),
 ("How much does Howie Benson cost?", "On October 10, 2026, dad caps were $40, two-tone five-panels $45, patch hats $50, the Ottoman polo $98, the Resort polo $108, and the Single Button Pullover and Textured Crew $118. Shipping is free over $150, and adding a hat to a top saves $15."),
 ("Where can I buy Howie Benson?", "On howiebenson.com, which ships the next business day, and at Badlands in Atlantic Highlands, New Jersey, which stocks the polos and layers."),
]
FRN = json.loads((ROOT / "research/howie-benson/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-HB-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-10", "dateModified": "2026-10-10",
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
    <span>Contemporary golf apparel &middot; New York, Boston, San Diego</span><span class="dot"></span>
    <span>16 picks &middot; all in stock, checked October 10, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A golfer in a black Howie Benson pullover and sunglasses leaning on a golf cart on a desert course below the mountains" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
