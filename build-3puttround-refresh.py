#!/usr/bin/env python3
"""build-3puttround-refresh.py — refresh of /drops/3-putt-round-golf-tees-disguised-as-bad-habits (first run 15 June 2026),
same URL, homepage card left where it is. Cloned from build-woodgrain-btk.py. 12 October 2026.
Lenny: "let's give this page a refresh but keep it in the same position on the home page", then "combine all the golf tees into
one box add some towels and hats". FACTS: 3puttround.com products JSON (research/3puttround-refresh/products-2026-10-12.json) and
About page, read 12 Oct 2026. Prices in euros first (x1.1203). Note the store reuses product URLs: the handle
"the-its-just-another-addiction-knit-polo-green" is now the Golf Shop long-sleeve tee, and "...golf-shop-ls-tee" is the knitted polo.
PHOTOS: 3 Putt Round's own (frames in research/3puttround-refresh/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "3 Putt Round: Golf Tees Disguised as Bad Habits"
DESC = ("3 Putt Round, the Milan brand that packs golf tees like cigarettes, snus tins and matchbooks: every tee pack, "
        "the Tee Case, towels, caps and clothing, from €6 to €120. Refreshed October 2026.")
H1 = "3 Putt Round &mdash; Golf Tees Disguised as Bad Habits"
BC = "3 Putt Round"
SLUG = "3-putt-round-golf-tees-disguised-as-bad-habits"
IMG = "/images/3puttround-2026"
SHOP = "https://3puttround.com/"
A = "3 Putt Round"
def e(x): return f"&euro;{x} (~${round(float(x.replace(',','.'))*1.120287)})"
P = {
 "addiction": (A, "&ldquo;Golf Addiction&rdquo; Tee Packs, Gold", "&euro;31 for three (~$35)", "products/set-of-3-golf-golf-addiction-tee-packs",
   "The pack that started it: 20 bamboo tees in a box made to look like a carton of cigarettes, with a warning that golf &ldquo;can be highly addictive.&rdquo; The gold version is &euro;12.90 a pack or &euro;31 for three, and a collectible carton of eight packs is &euro;75. The red packs from our first list were sold out when we checked; the gold ones were in stock."),
 "scented": (A, "Scented Tee Packs", "&euro;12.90 each (~$14)", "collections/golf-tees",
   "New since June: eight scented packs, from mint and watermelon to lemon, eucalyptus and peach, each holding 20 bamboo tees that are lightly scented to match the box. There are also named blends like The Club Champion and Members Only. Buy one for the bag and one for whoever you are playing with."),
 "upperdecky": (A, "Upper Decky Tee Tins, Set of Three", e("26"), "products/3-upper-decky-tee-packs",
   "Golf tees packed in snus-style tins with blue lids, 15 short bamboo tees in each. They fit a pocket, and they look exactly like something you should not leave on the dashboard of the cart."),
 "matches": (A, "Golf Tee Matchboxes, Set of Four", e("20"), "products/set-of-4-golf-matches",
   "Two red and two green matchboxes that say &ldquo;Fire Up Your Drive,&rdquo; with 12 bamboo tees inside each. The Vecchio x Lost Balls version, in red-and-white trattoria checks, is &euro;6 for a single box."),
 "teecase": (A, "The Tee Case", e("35"), "products/the-tee-case-iphone-17",
   "The newest thing in the shop: a silicone iPhone case with a tee holder built into the back, which 3 Putt Round calls the world&rsquo;s first. It comes for the iPhone 16 Pro, 16 Pro Max, 17 Pro and 17 Pro Max. Pull a tee from your phone on the first tee and see who asks."),
 "vecchiotowel": (A, "Vecchio x Lost Balls Towel, 40 x 60cm", e("25"), "products/the-vecchio-x-lost-balls-golf-towel",
   "A collaboration between Vecchio, a New York&ndash;style Italian restaurant in Paris, and the Japanese-French golf brand Lost Balls, sold through 3 Putt Round. Red and white checks like a trattoria tablecloth, sized to clip to a bag. There is a matching tee matchbox for &euro;6."),
 "morningtowel": (A, "The Morning Truth Towel, 40 x 60cm", "&euro;9.75, was &euro;15 (~$11)", "products/the-drive-to-survive-tour-towel-50cm-x-100cm-copy",
   "A coffee-brown microfiber towel that reads &ldquo;Fueled by caffeine. Driven by golf,&rdquo; with a little coffee cup that hides a ruder message inside. It was marked down when we checked, which makes it the cheapest laugh in the shop."),
 "capgreen": (A, "Lost Balls x 3 Putt Round &ldquo;Addiction&rdquo; Cap, Green", e("45"), "products/the-lost-balls-x-3-putt-round-addicted-cap-green",
   "Green corduroy, low profile and unstructured, with &ldquo;It&rsquo;s just another addiction&rdquo; stitched across the front and an adjustable strap. The best hat in the shop for fall and winter rounds."),
 "captweed": (A, "Lost Balls x 3 Putt Round &ldquo;Addiction&rdquo; Cap, Tweed", e("45"), "products/the-lost-balls-x-3-putt-round-addicted-cap-tweed",
   "The same cap in a soft brown herringbone tweed, new since our first look at the brand. It is the one to wear with a knit or a wool layer."),
 "capnot3putt": (A, "&ldquo;I Will Not 3 Putt&rdquo; Cap", e("35"), "products/the-i-will-not-3-putt-baseball-cap",
   "The brand&rsquo;s name turned into a promise you will break by the third hole. A classic baseball cap with the line embroidered on the front."),
 "capdangerous": (A, "&ldquo;Golf Is Dangerous&rdquo; Cap", e("35"), "products/the-golf-is-dangerous-baseball-cap",
   "A red cap with &ldquo;Golf is dangerous&rdquo; in white, and 3 Putt Round across the back. Loud enough to find your group in a car park."),
 "caposlock": (A, "&ldquo;It&rsquo;s Golf O&rsquo;Clock&rdquo; Cap", e("35"), "products/the-its-golf-oclock-baseball-cap-copy",
   "Navy with white embroidery. The one for the Friday afternoon you leave work early."),
 "capcaddie": (A, "&ldquo;Who&rsquo;s Your Caddie?&rdquo; Cap", e("35"), "products/the-whos-your-caddy-baseball-cap-1",
   "A structured cap with a flat visor and a stretch band, in two sizes, in dark navy or black. The joke is in the embroidery."),
 "knitpolo": (A, "Lost Balls x 3 Putt Round Addiction Knitted Polo", e("120"), "products/the-lost-balls-x-3-putt-round-golf-shop-ls-tee",
   "The most expensive piece in the shop, and the one that looks least like a novelty. A textured knit polo in green or grey, breathable and light, with the Lost Balls graphic on the back. The brand says to size up for a relaxed fit."),
 "lstee": (A, "Lost Balls x 3 Putt Round Golf Shop Long-Sleeve Tee", e("60"), "products/the-its-just-another-addiction-knit-polo-green",
   "A white long sleeve with a half mock neck and a golf-shop graphic on the back. Size up for a relaxed fit. Only L and XL were left when we checked."),
 "morningtee": (A, "The Morning Truth T-Shirt", e("50"), "products/the-morning-thruth-t-shirt-c",
   "Made with Casualist: a 200gsm organic cotton tee in cream, relaxed fit, with the Morning Truth coffee graphic. It matches the towel above."),
 "sundaytee": (A, "&ldquo;Sunday&rsquo;s Golfing Club&rdquo; T-Shirt", e("45"), "products/unisex-organic-cotton-t-shirt",
   "A white organic cotton tee with the 3 Putt Round icon on the chest and Sunday&rsquo;s Golfing Club printed big across the back. Ring-spun cotton, ribbed neck, and the brand says to size up."),
 "buggytee": (A, "&ldquo;Golf Buggy&rdquo; T-Shirt", e("45"), "products/the-golf-buggy-t-shirt",
   "A relaxed 100% cotton tee with a small golf buggy on the chest, in black, navy, white or pink, sizes S to 3XL. The quiet one."),
}
SECTIONS = [
 ("The Tees", "tees", ["addiction","scented","upperdecky","matches"],
  "<strong>Four picks &middot; &euro;12.90&ndash;&euro;31</strong>Every way 3 Putt Round packs a golf tee: cigarette-style packs, scented packs, snus tins and matchboxes."),
 ("The Tee Case and Towels", "towels", ["teecase","vecchiotowel","morningtowel"],
  "<strong>Three picks &middot; &euro;9.75&ndash;&euro;35</strong>A phone case that holds a tee, a trattoria-check collab towel and a coffee towel with a rude secret."),
 ("The Hats", "hats", ["capgreen","captweed","capnot3putt","capdangerous","caposlock","capcaddie"],
  "<strong>Six picks &middot; &euro;35&ndash;&euro;45</strong>Two Lost Balls collab caps in corduroy and tweed, and four baseball caps that each tell a joke."),
 ("The Clothing", "clothing", ["knitpolo","lstee","morningtee","sundaytee","buggytee"],
  "<strong>Five picks &middot; &euro;45&ndash;&euro;120</strong>The knitted polo and long sleeve from the Lost Balls collab, a tee made with Casualist, the Sunday&rsquo;s Golfing Club tee and the everyday buggy tee."),
]
N = 18
PQ = {
 "towels": ("Redefining what it means to be a golfer.", "3 Putt Round, on its mission"),
}
CAP = "Photography &middot; 3 Putt Round&rsquo;s own"
BANDS = {
 "hats": ("From 3 Putt Round", "Tee tins, a black cap after dark and the &ldquo;Foreee Right&rdquo; cap on a classic car.", [("band-1","Snus-style Upper Decky tee tins piled on a blue towel","The tins"),("band-2","A black 3 Putt Round cap embroidered Golf Is Social, shot in low light","Golf is social"),("band-3","A black Foreee Right cap resting on the seat of a classic car","Foreee right")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>3 Putt Round has one joke and commits to it completely: golf is an addiction, so the accessories should look like vices. Tees come in cigarette packs with warning labels, in snus tins and in matchbooks. It is novelty done with enough design sense that the packs end up on the dashboard of the cart, which is exactly where the brand wants them.</p>
    <p>A lot has changed since we first wrote about them in June. There are now eight scented tee packs, gold packs and &euro;75 collectible cartons, a silicone iPhone case with a tee holder built into the back, and a tweed version of the corduroy Addiction cap. Some of the original picks have sold out, so this is a fresh list: four kinds of tee pack, the Tee Case and towels, six caps and five pieces of clothing. The knitted polo from the Lost Balls collab is still the piece we would buy first.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>3 Putt Round was founded in Milan in 2023 and describes itself as &ldquo;an addictive game born from the passion for the game.&rdquo; It makes fun, unconventional golf accessories and has collaborated with Lost Balls, the Japanese-French golf brand, the Paris restaurant Vecchio and Casualist. Prices are in euros and everything ships from Europe. All 18 picks below were in stock on 3puttround.com on October 12, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Milan, Italy</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2023</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Tees packed like vices</span></div>
      <div class="sidebar-detail"><span class="l">Collabs</span><span>Lost Balls, Vecchio, Casualist</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&euro;6&ndash;&euro;120</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Addiction Knitted Polo, &euro;120</span></div>
      <a href="https://3puttround.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit 3 Putt Round &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#3PuttRound</span>
        <span class="hashtag">#GolfTees</span>
        <span class="hashtag">#GolfAddiction</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is 3 Putt Round from?", "Milan, Italy. The brand was founded there in 2023."),
 ("What does 3 Putt Round make?", "Golf accessories that look like vices: tees in cigarette-style packs, snus tins and matchboxes, plus scented tee packs, a phone case with a tee holder, towels, caps and clothing."),
 ("How much are 3 Putt Round tees?", "On October 12, 2026, a single tee matchbox was €6, a Golf Addiction or scented tee pack was €12.90, three Upper Decky tins were €26, three Golf Addiction packs were €31 and a collectible carton of eight packs was €75."),
 ("What is the 3 Putt Round Tee Case?", "A silicone iPhone case with a tee holder built into the back, which the brand calls the world's first. It was €35 for the iPhone 16 Pro, 16 Pro Max, 17 Pro and 17 Pro Max."),
 ("Does 3 Putt Round ship to the US?", "Prices are in euros and orders ship from Europe; check the shipping options at checkout."),
]
FRN = json.loads((ROOT / "research/3puttround-refresh/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-3PR-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-06-15", "dateModified": "2026-10-12",
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
    <span>Golf accessories and clothing &middot; Milan, Italy</span><span class="dot"></span>
    <span>Refreshed &middot; 18 picks, all in stock, checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="3 Putt Round&rsquo;s scented tee packs in eight colors fanned out against lemons, oranges, watermelon, mint and grapes" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Woodgrain", "Brewster", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
