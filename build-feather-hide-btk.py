"""build-feather-hide-btk.py — Brand to Know: Feather & Hide, 8 November 2026. Cloned from build-hidden-details.py.
Lenny: "Let's do a brand to know - https://featherandhidegolf.com/", then "build the post" on my suggested 12 (the Salty Golfer crewneck swapped
for The Links hat because every crewneck photo is on a woman). FACTS: product pages, About, Members Only page, Sunday Letters 7.26.26 and 8.9.26.
No city or founder surname is published, so none is given.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Brand to Know: Feather & Hide, the Small Golf Brand Reviving the Game's Old Culture"
DESC = ("Feather & Hide makes stretch polos, quarter-zips and hoodies, plus tees for caddies and grounds crews, from a founder who signs off "
        "every newsletter “Go low.” 12 picks, the Salty Golfer collab and the Members Only box.")
H1 = "Feather &amp; Hide: Reviving the Old Culture of Golf, One Caddie Tee at a Time"
BC = "Feather &amp; Hide"
SLUG = "brand-to-know-feather-and-hide"
IMG = "/images/feather-hide"
U = lambda h: f"https://featherandhidegolf.com/products/{h}"
B = "Feather &amp; Hide"
P = {
 "rs": (B, "The Ranger Golf Polo, Solid", "$65", U("the-ranger"),
   "The polo the brand is built on: four-way stretch, an athletic fit and the embroidered feather tee on the chest. Six colors, from pale blue and dusk to pine green. It fits true to size."),
 "rf": (B, "The Ranger Golf Polo, Feathered", "$68", U("the-ranger-feathered-polo"),
   "The same Ranger, covered in a small print of scattered feather tees, in maroon or gray. Their copy promises it will look good on the course, in the office and at College GameDay brunch."),
 "st": (B, "The Starter Golf Quarter-Zip", "$68", U("the-starter"),
   "Lightweight but warm four-way stretch, in navy, pale blue and lavender. Feather &amp; Hide recommends sizing down for a more contoured fit."),
 "ho": (B, "The Honours Golf Hoodie", "$78", U("honours-hoodie"),
   "Their fan favorite: a polyester-spandex golf hoodie that, in their words, breaks the wind better than your 80-year-old grandad. Navy, pale blue, maroon and smoke; the lavender is on sale for $40. Size down for swing."),
 "ri": (B, "The Ringer Golf Hat", "$36", U("the-ringer"),
   "A structured, high-crown five-panel in white with the red feather tee embroidered on the front, moisture-wicking with a snapback."),
 "sc": (B, "The Scratch Golf Hat", "$36", U("the-scratch"),
   "The black version: structured high crown, a white feather tee, perforated back panels and a snapback."),
 "ct": (B, "Support Your Local Caddie Golf Tee", "$32", U("support-your-local-caddie"),
   "The shirt with the message: &ldquo;Carts are overrated and overpriced.&rdquo; Heavy ring-spun cotton, pre-shrunk, with the caddie illustration on the back. Expect someone to tap you on the shoulder and agree."),
 "ch": (B, "Support Your Local Caddie Golf Hat", "$32", U("support-your-local-caddie-hat"),
   "Cream crown, green brim and the same message up front: a nod to walking golf and the caddies who keep the game grounded in tradition."),
 "ng": (B, "Nicotine and Gasoline Golf Tee", "$32", U("nicotine-and-gasoline"),
   "A tribute to the grounds crews who have the course ready before the first tee time, with a mower on the sleeve and the script on the back. Written for anyone who loves the smell of gasoline and grass clippings at sunrise."),
 "lt": (B, "Forever Loopin&rsquo; Tee (with Salty Golfer)", "$40", U("forever-loopin-salty-golfer-and-feather-hide"),
   "The collaboration with Salty Golfer, the Myrtle Beach brand Lou met over a round at True Blue: a skeleton caddie still looping on the back, a pin flag on the chest. Heavy cotton, pre-shrunk."),
 "lk": (B, "The Links Golf Hat", "$32", U("the-links-golf-hat"),
   "A smoke-grey trucker with a charcoal feather tee and mesh back panels, all grey, the quietest piece in the line."),
 "tw": (B, "The Looper Golf Towel", "$38", U("the-looper-golf-towel"),
   "A 44&Prime; by 22&Prime; ribbed cotton towel for clean grooves and shiny balls. The tagline used to be &ldquo;Keep &rsquo;Em Dirty&rdquo;; they say they have cleaned up their act."),
}
SECS = [
 ("the-performance-line", "The Performance Line", "Polos, a quarter-zip, a hoodie and two hats", ["rs","rf","st","ho","ri","sc"],
  "Everything here carries the feather tee, the little logo that ties the name together: a tee drawn as a feather. The Ranger, the Starter and the Honours are the three pieces Feather &amp; Hide keeps restocking in new colors."),
 ("support-your-local-caddie", "Support Your Local Caddie", "Tees and a hat for the people who keep golf going", ["ct","ch","ng"],
  "This is where the brand&rsquo;s point of view is loudest. The graphic pieces are for caddies and grounds crews, the people who make a round possible and rarely get a shirt of their own."),
 ("forever-loopin", "Forever Loopin&rsquo; and the Kit", "The Salty Golfer collab, a trucker and a towel", ["lt","lk","tw"],
  "Forever Loopin&rsquo; came out of one round in Myrtle Beach with Salty Golfer, another small brand building from the ground up. Lou wrote that the chance to talk openly about ideas and struggles with someone doing the same thing is rare."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 12
PAIRS = {}
BANDS = {
 "the-performance-line": ("In the wild", "Feather &amp; Hide on the course", [("life-a-1","A golfer in the maroon feathered Ranger polo holding a headcover by a pond","Feather &amp; Hide"),("life-a-2","A golfer seen from behind in the Nicotine and Gasoline tee","Feather &amp; Hide"),("life-a-3","A man in a navy Starter quarter-zip in a leather armchair","Feather &amp; Hide"),("life-a-4","A golfer in a red Honours hoodie on the course","Feather &amp; Hide"),("life-a-5","A golfer in the white Ranger polo","Feather &amp; Hide"),("life-a-6","The Links trucker hat at sunset","Feather &amp; Hide")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Feather &amp; Hide says it is &ldquo;committing to the culture of historical golf. Not a trend.&rdquo; We read the name as a nod to the featherie, golf&rsquo;s first ball, made by stuffing feathers into a leather hide, and their About page describes golf as an arduous love-hate relationship. Their line is &ldquo;Revive the Game.&rdquo;</p>
    <p>What we like most is how honest it is. The founder, who signs his letters &ldquo;Lou,&rdquo; writes a candid newsletter called the Sunday Letter. In July he wrote about the company&rsquo;s third year: moves, a return to a day job, a death in the family and a wedding, then placing the largest inventory order in the brand&rsquo;s history and, in his words, biting his nails down to the nubs. It reads like a conversation over a beer, which is exactly what he says he was going for.</p>
    <p>The clothes back up the attitude. The Ranger polo and the Honours hoodie are good, plain performance pieces with a small logo, and the graphic tees stand up for caddies and grounds crews instead of the clubhouse. &ldquo;Carts are overrated and overpriced&rdquo; is not a line you see from many golf brands.</p>
    <p><strong>Where to start.</strong> The Ranger Golf Polo, $65, in pine green or dusk, and the Support Your Local Caddie hat, $32. If you want the whole story in one box, look at Members Only below.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Feather &amp; Hide</span></div>
      <div class="sidebar-detail"><span class="l">Run by</span><span>Lou, now in year three</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>12</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$32&ndash;$78</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Ranger Golf Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#ReviveTheGame</span>
        <span class="hashtag">#SupportYourLocalCaddie</span>
        <span class="hashtag">#IndieGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">Members Only</div>
    <h2 class="products-hdr" id="members-only">A Golf Box Four Times a Year</h2>
    <p>Feather &amp; Hide&rsquo;s membership is $300 a year for four seasonal boxes, arriving in April, July, October and January. Each one has exclusive Feather &amp; Hide apparel, a print from golf photographer RJ Gilbert and a golf artwork by Claire Nilan, and members get 15% off the site all year. The 2026 window closed on April 10; it is a good one to watch for 2027, and an easy gift for the golfer who already has everything.</p>
  </div>
  <div class="writeup-body" style="max-width:720px;margin:40px auto 0">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Go Low</h2>
    <p>Feather &amp; Hide is a small brand still finding its feet. Lou compares it to a baby horse taking its first steps: standing up, a little wobbly. That honesty is the reason to pay attention. The brand is working on collegiate licensing, a Salty Golfer collab came out of a single round, and new colors of the Ranger, the Starter and the Honours keep arriving.</p>
    <p>Buy the polo because it is a good polo. Buy the caddie tee because you agree with it. And read the Sunday Letter, because there are not many golf brands writing to their customers like that. Every letter ends the same way: &ldquo;Go low.&rdquo;</p>
    <p>Prices are in US dollars as shown on November 8, 2026, and all 12 picks were in stock.</p>
  </div>
</section>
"""
HERO_ALT = "Three Feather & Hide photos: a golfer in a white hoodie by the flag, a golfer in the Support Your Local Caddie tee by a cart, and a golfer mid-swing with the Looper towel on his bag"
FRN = json.loads((ROOT / "research/feather-hide/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
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
         "url": URL, "image": og, "datePublished": "2026-11-08", "dateModified": "2026-11-08",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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


CBY = {s[0]: s for s in SECS}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    s = CBY[anchor]
    num = [x[0] for x in SECS].index(anchor) + 1
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;"><p style="margin:0 0 16px;">{s[4]}</p></div>\n'
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Brand to Know &middot; Revive the Game</span><span class="dot"></span>
    <span>12 picks &middot; in stock, checked November 8, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    if "end" in BANDS: body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Vest Edit", "Collab "):
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
