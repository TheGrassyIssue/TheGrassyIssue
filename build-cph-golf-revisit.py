#!/usr/bin/env python3
"""build-cph-golf-revisit.py — "Brand Revisited: Cph/Golf" 14 October 2026.
Lenny: "let's do a brand revisited- https://captainshelmgolf.com/en", then took the 18 TGI picks ("let's build the post").
One swap from the sheet: AW26 Gentleman Half Mock Neck LS Tee had only Navy L left on Oct 14, replaced by the CPH GOLF PRO
Half Mock Neck Tee (the "I PLAY GOLF FOR MONEY" partner to the Amateur tee).
FACTS: brand history from captainshelm.jp/pages/about ("Est.2011 Born in California, based in Tokyo"; JP copy translated by
us), captainshelmgolf.com mission copy (translated), A.P.C. Japan journal (collab dates, pop-ups), Descente (Penguin collab,
March 2026). Founder name (Mitch Abshire) rests on one 2017 retailer post, so it is NOT used. No founder quotes exist on record.
Products: captainshelmgolf.com products.json, Oct 14, 2026; JPY is the store currency, USD shown is the store's own
conversion (x0.006438). Product copy paraphrases the brand's Japanese descriptions.
PHOTOS: hero is a crop of the AW26 lookbook (CHG26-AW-P01-LOOK-302, 2667px). Others brand's own (research/cph-golf/frame.py). The BAGGY PANTS collab and Fly Me to the Green cap lifestyle shots exist
only at 500px, so those cards use packshots. Homepage "moda-ai" images are AI-generated and are never used.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand Revisited: Cph/Golf, the Tokyo Brand That Isn't a Golf Gentleman"
DESC = ("We revisit Cph/Golf, the golf line of Tokyo's CAPTAINS HELM: the AW26 collection, what's left of the A.P.C. Golf collab, "
        "the I PAY MONEY FOR GOLF tees and 18 pieces in stock now, with yen and dollar prices.")
H1 = "Brand Revisited &mdash; Cph/Golf, the Tokyo Brand That Isn&rsquo;t a Golf Gentleman"
BC = "Brand Revisited: Cph/Golf"
SLUG = "brand-revisited-cph-golf"
IMG = "/images/cph-golf-revisited"
SHOP = "https://captainshelmgolf.com/en/products/"
P = {
 "chg26awj01": ("Cph/Golf", "Gentleman No Collar Jacket", "&yen;22,000 (~$142)", "chg26-aw-j01",
   "This is the center of AW26: a boxy, collarless stretch jacket with a drawcord hem you can cinch, and NOT A GOLF GENTLEMAN across the back. Cph/Golf calls it one of its regular pieces. Khaki in M to XL; navy and charcoal in fewer sizes."),
 "chg26awp01": ("Cph/Golf", "Adjustable Pants The 2nd", "&yen;18,700 (~$121)", "chg26-aw-p01",
   "The second version of their tapered stretch trouser, with a logo jacquard elastic that sits across the waist like a belt and adjusts the fit. Khaki, black, navy and charcoal."),
 "chg26awp02": ("Cph/Golf", "Belted Adjustable Wide Pants", "&yen;18,700 (~$121)", "chg26-aw-p02",
   "The wide version is a roomy stretch trouser with a webbing belt at the waist. The lookbook pairs the white version with the charcoal jacket. White, black and charcoal in M and L."),
 "chg26awt01": ("Cph/Golf", "Jacquard Mock Neck LS Tee", "&yen;14,300 (~$93)", "chg26-aw-t01",
   "A long-sleeve mock neck in cotton stretch jersey with Cph/Golf knitted around the collar, ribbed at the cuffs and hem. The brand recommends it worn on its own. Khaki and indigo blue in stock."),
 "chg26apcgt04": ("A.P.C. Golf &times; Cph/Golf", "A.P.Cph/Golf L/S Polo Pullover", "&yen;18,700 (~$121)", "chg26-apcg-t04",
   "The best thing left from September&rsquo;s collab: a long-sleeve polo with a jacquard collar, the A.P.Cph logo embroidered on the chest and a dropped shoulder. Navy in M to XL, plus a few white and black."),
 "chg26apcgt05": ("A.P.C. Golf &times; Cph/Golf", "A.P.Cph/Golf Thermal L/S Mock Neck Tee", "&yen;15,400 (~$100)", "chg26-apcg-t05",
   "A thermal mock neck with A.P.Cph embroidered at the center of the collar, so it shows when you layer a jacket over it. Navy, M and L only."),
 "chg26apcga01": ("A.P.C. Golf &times; Cph/Golf", "A.P.Cph/Golf Green Fork", "&yen;4,400 (~$29)", "chg26-apcg-a01",
   "This folding silver divot tool comes with a magnetic A.P.Cph ball marker. The cheapest way to own a piece of the collab."),
 "chg26sst16": ("Cph/Golf", "CPH GOLF Amateur Half Mock Neck Tee", "&yen;9,900 (~$64)", "chg26-ss-t16",
   "Cotton jersey with I PAY MONEY FOR GOLF printed on the back, a line the brand itself calls direct and a little sarcastic. Black, off-white and charcoal, M to XL."),
 "chg26sst17": ("Cph/Golf", "CPH GOLF Pro Half Mock Neck Tee", "&yen;9,900 (~$64)", "chg26-ss-t17",
   "The other half of the joke: the same tee with I PLAY GOLF FOR MONEY on the back. Buy the one that is true."),
 "chg26sss02": ("Cph/Golf", "CPH GOLF Pro Rip Stop Shirt", "&yen;14,300 (~$93)", "chg26-ss-s02",
   "A crisp ripstop snap-front shirt cut oversized and boxy, with I PLAY GOLF FOR MONEY across the back. Black, white and charcoal."),
 "chg26sssx05": ("Cph/Golf", "Holy Shit In One 2PC Socks", "&yen;3,850 (~$25)", "chg26-ss-sx05",
   "Two pairs with a lightning bolt on the back. The brand suggests rolling your trousers up a little so they show."),
 "chg26ssc07": ("Cph/Golf", "Fly Me to the Green Cap", "&yen;7,700 (~$50)", "chg26-ss-c07",
   "A brought-back favorite: the Fly Me to the Green script on a cap with a leather strap. Black, white and green."),
 "chg26bpt01": ("Cph/Golf &times; BAGGY PANTS GOLF", "Breathable Polo", "&yen;14,300 (~$93)", "chg26-bp-t01",
   "The summer collab with BAGGY PANTS GOLF: a cooling stretch pique polo with raglan sleeves and gussets under the arms, cut to swing in. Not a Golf Gentleman on the back. Black and slate khaki."),
 "chg26bpc01": ("Cph/Golf &times; BAGGY PANTS GOLF", "Pants Golf BB Cap", "&yen;7,700 (~$50)", "chg26-bp-c01",
   "Made from the same fabric as the polo, so the two match. Black and olive."),
 "mu6slpg0m": ("Penguin by Munsingwear &times; Cph/Golf", "Penguin by Cph/Golf Adjust Pants", "&yen;20,900 (~$135)", "mu6slpg0m",
   "The spring collab with Penguin by Munsingwear made this plain chino with a small penguin, a small Cph/Golf logo and a co-branded tag. XL only, in black or cream."),
 "chg25awj05khaki": ("Cph/Golf", "Side Quilt Knit Vest, Khaki", "&yen;16,500 (~$107)", "chg25-aw-j05-khaki",
   "Last fall&rsquo;s hybrid: a 12-gauge knit body with quilted side panels and NOT A GOLF GENTLEMAN knitted across the back. Still M to XL."),
 "classiccottonribpolosh": ("Cph/Golf", "Classic Cotton Rib Polo Shirt, Yellow", "&yen;14,300 (~$93)", "classic-cotton-rib-polo-shirt-yellow",
   "Cph/Golf&rsquo;s fall polo in a vintage yellow, with CPH/G knitted into the collar and printed on the back. The brand calls it old American style. M to XL."),
 "chg25awt21khaki": ("Cph/Golf", "CPH/GOLF Club Jacket, Khaki", "&yen;26,400 (~$170)", "chg25-aw-t21-khaki",
   "An American club jacket in a light, warm brushed fabric with stretch ribbing so it does not fight your swing. CPHIGOLF TKY 2025 is on the back. One XL left."),
}
SECTIONS = [
 ("AW26: The Gentleman Collection", "aw26", ["chg26awj01", "chg26awp01", "chg26awp02", "chg26awt01"],
  "<strong>Four picks &middot; live October 7</strong>The fall collection is built on regular pieces: a collarless jacket, two adjustable trousers and a knit-collar mock neck, mostly in khaki and charcoal."),
 ("What&rsquo;s Left of A.P.C. Golf", "apc", ["chg26apcgt04", "chg26apcgt05", "chg26apcga01"],
  "<strong>Three picks &middot; released September 2</strong>Most of the A.P.Cph/Golf collection sold out within weeks. These three were still on the shelf on October 14." ),
 ("I Pay Money for Golf", "slogans", ["chg26sst16", "chg26sst17", "chg26sss02", "chg26sssx05", "chg26ssc07"],
  "<strong>Five picks &middot; spring and summer 2026</strong>Here are the jokes. Cph/Golf prints its punchlines on the back, where your playing partners will read them."),
 ("The Collabs", "collabs", ["chg26bpt01", "chg26bpc01", "mu6slpg0m"],
  "<strong>Three picks &middot; 2026</strong>Cph/Golf worked with BAGGY PANTS GOLF in the summer and Penguin by Munsingwear in the spring, on top of A.P.C."),
 ("Still Here From Last Fall", "aw25", ["chg25awj05khaki", "classiccottonribpolosh", "chg25awt21khaki"],
  "<strong>Three picks &middot; AW25</strong>Three pieces from last year&rsquo;s fall collection that are still in stock, and still good."),
]
N = 18
PAIRS = {}
LIFE = []
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We first put Cph/Golf in our Japan roundup in July, as a new name: the golf line of the Tokyo label CAPTAINS HELM. Three months later it has done a collab with A.P.C. Golf that mostly sold out, another with BAGGY PANTS GOLF, and a full fall collection that went up on October 7. Time for a proper look.</p>
    <h2 class="products-hdr btk-story-hdr">Born in California, Based in Tokyo</h2>
    <p>CAPTAINS HELM describes itself as a community brand that began in Oceanside, California, and its tagline is &ldquo;Est.2011 Born in California , based in Tokyo&rdquo; (the spacing is theirs). The idea, in the brand&rsquo;s Japanese copy, is California outdoor life (surfing, camping, fishing) seen through a Tokyo filter, in clothes you can also wear in town. The golf line, Cph/Golf, arrived in 2021 with its own slogan: &ldquo;I&rsquo;m Not a Golf Gentleman.&rdquo; The brand says it makes golfwear for adults who want to play their own way, mixing street and standard.</p>
    <p>You can see it in the names. The men&rsquo;s and women&rsquo;s versions of each piece are called Gentleman and Mademoiselle, and NOT A GOLF GENTLEMAN is knitted or printed across the backs of the jackets and vests. The golf line has stores in Daikanyama in Tokyo and in Nagoya.</p>
    <h2 class="products-hdr btk-story-hdr">What Changed Since July</h2>
    <p>September brought A.P.Cph/Golf, its collab with A.P.C. Golf, the Paris label&rsquo;s golf line. It went on sale September 2, with pop-ups at Shinjuku Takashimaya and Hankyu Umeda. <a href="/drops/apc-golf-cph-golf-collab">Our collab post</a> has the full list, and most of it is now gone. The summer brought a smaller collab with BAGGY PANTS GOLF, and the spring one with Penguin by Munsingwear. Then AW26, which is Cph/Golf at its calmest: a collarless jacket, adjustable stretch trousers and a knit-collar mock neck in khaki and charcoal. The slogans are still there, but this fall they are on the back.</p>
    <p>All 18 pieces were in stock on captainshelmgolf.com on October 14, 2026. The store charges in yen; the dollar figure is the store&rsquo;s own conversion, before shipping from Japan, which the site does not price for the US. Sizes run M to XL.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Cph/Golf (CAPTAINS HELM)</span></div>
      <div class="sidebar-detail"><span class="l">Base</span><span>Tokyo, est. 2011</span></div>
      <div class="sidebar-detail"><span class="l">Golf line</span><span>Since 2021</span></div>
      <div class="sidebar-detail"><span class="l">Slogan</span><span>I&rsquo;m Not a Golf Gentleman</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&yen;3,850&ndash;&yen;26,400</span></div>
      <div class="sidebar-detail"><span class="l">Stores</span><span>Daikanyama, Nagoya</span></div>
      <a href="#aw26" class="sidebar-cta">See AW26 &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#CphGolf</span>
        <span class="hashtag">#CaptainsHelm</span>
        <span class="hashtag">#JapaneseGolf</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">Where we first found them: <a href="/drops/japan-golf-roundup">our Japan golf roundup</a>. The collab: <a href="/drops/apc-golf-cph-golf-collab">A.P.C. Golf &times; Cph/Golf</a>.</p>
</section>
"""
FAQ = [
 ("What is Cph/Golf?", "Cph/Golf is the golf line of CAPTAINS HELM, a brand that says it began in Oceanside, California and has been based in Tokyo since 2011. The golf line launched in 2021 with the slogan I'm Not a Golf Gentleman."),
 ("What is in the Cph/Golf AW26 collection?", "Released October 7, 2026: the Gentleman No Collar Jacket (¥22,000), Adjustable Pants The 2nd and Belted Adjustable Wide Pants (¥18,700 each) and the Jacquard Mock Neck LS Tee (¥14,300), plus women's versions."),
 ("Can you still buy the A.P.C. Golf x Cph/Golf collab?", "Most of it sold out after the September 2, 2026 release. On October 14 the long-sleeve polo pullover, thermal mock neck, adjustable pants and the Green Fork divot tool were still in stock in some sizes."),
 ("Does Cph/Golf ship to the US?", "The store shows US dollar prices and its legal notice covers overseas orders, but it does not publish a US shipping rate, so check the total at checkout."),
]
HERO_ALT = "Two models in the Cph/Golf AW26 Gentleman No Collar Jacket, one khaki and one charcoal, with Cph/Golf knitted around their collars"
FRN = json.loads((ROOT / "research/cph-golf/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-CPHR-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-14", "dateModified": "2026-10-14",
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
    <span>Tokyo &middot; est. 2011 &middot; golf line since 2021</span><span class="dot"></span>
    <span>18 picks &middot; in stock, checked October 14, 2026</span>
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
    for leak in ("Mackem", "Kalamunda", "Lehi", "Rookline", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram", "moda-ai", "Abshire"):
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
