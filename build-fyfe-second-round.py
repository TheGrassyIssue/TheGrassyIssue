#!/usr/bin/env python3
"""build-fyfe-second-round.py — Fyfe Golf Second Round: 15 headcovers cut from vintage golf jackets. 10 October 2026.
Lenny: "Let's do a post about Fyfe's second round" + picked "All 15 (Recommended)": every remake, #06 kept and marked sold out.
Cloned from build-howie-benson-btk.py (gallery cards, take + sidebar, FAQ).
FACTS: fyfegolf.com/collections/second-round (collection copy + products JSON), read October 10, 2026. Made counts per
size are Fyfe's own, from each product page. Prices: GBP from the UK store; USD from Fyfe's own US storefront ($95 / $89).
Source-jacket brands are named only because Fyfe names them; Fyfe states this is not a collaboration with any of them.
Founder facts reuse our Fyfe Brand to Know (Neil Rennie, Fife workshop, launched November 2021).
PHOTOS: Fyfe's own product and collection photography (frames: research/fyfe-second-round/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Fyfe Golf Second Round: 15 Headcovers Cut From Vintage Golf Jackets"
DESC = ("Fyfe Golf took 15 old golf jackets, from Mizuno and Reebok to Ashworth and Sunderland of Scotland, and remade them "
        "by hand in Scotland into 73 headcovers. Every remake, what's left and the price.")
H1 = "Fyfe Golf Second Round &mdash; 15 Headcovers Cut From Vintage Golf Jackets"
BC = "Fyfe Golf Second Round"
SLUG = "fyfe-golf-second-round-headcovers-from-vintage-golf-jackets"
IMG = "/images/fyfe-second-round"
SHOP = "https://www.fyfegolf.com/products/"
A = "Fyfe Golf"
PR = "&pound;69 driver / &pound;65 fairway ($95 / $89)"
def st(d, f, dl=True, fl=True):
    return f"Driver &mdash; {d} made{'' if dl else ', sold out'}. Fairway &mdash; {f} made{'' if fl else ', sold out'}."
P = {
 "r01": (A, "Remake 01 &middot; Caviva Jacket, Tartan Inserts", PR, "second-round-remake-01-headcover",
   "Cut from a vintage Caviva golf jacket with contrasting tartan inserts. Where the tartan lands changes from cover to cover, so no two match. Five made from one jacket. " + st(3, 2)),
 "r02": (A, "Remake 02 &middot; Mizuno Green Check", PR, "second-round-remake-02-headcover",
   "A vintage Mizuno golf top in green chequered technical cloth, the kind of fabric that was everywhere on a 1990s range. The fairway covers are already gone. " + st(3, 3, fl=False)),
 "r04": (A, "Remake 04 &middot; RBC Heritage Jacket", PR, "second-round-remake-04-headcover",
   "Cut from a vintage RBC Heritage tournament jacket, so a small piece of Hilton Head ends up on your driver. Fyfe calls it carrying the tournament&rsquo;s history into its next life. " + st(3, 3)),
 "r06": (A, "Remake 06 &middot; Sunderland of Scotland Blue Tartan", PR, "second-round-remake-06-headcover",
   "A Sunderland of Scotland jacket in blue tartan, which makes this the most Scottish cover in a Scottish run. It sold out first: all four were gone within a day of the drop. " + st(2, 2, dl=False, fl=False)),
 "r10": (A, "Remake 10 &middot; ProQuip Red Check", PR, "second-round-remake-10-headcover",
   "A vintage ProQuip golf jacket in a bold red check. Fyfe got only four covers out of the surviving cloth, so this is one of the smallest runs in the drop. " + st(2, 2)),
 "r05": (A, "Remake 05 &middot; Sunderland of Scotland Pink &rsquo;90s", PR, "second-round-remake-05-headcover",
   "A Sunderland of Scotland jacket in what Fyfe calls an unmistakable pink 1990s pattern. Each of the four covers takes a different section of the print. " + st(2, 2)),
 "r07": (A, "Remake 07 &middot; Sunderland of Scotland Red Floral", PR, "second-round-remake-07-headcover",
   "Sunderland again, this time in a loud red floral. It is the cover in the drop most likely to start a conversation on the first tee. " + st(2, 2)),
 "r08": (A, "Remake 08 &middot; Reebok Quarter-Zip", PR, "second-round-remake-08-headcover",
   "Cut from a vintage Reebok quarter-zip golf jacket in a busy 1990s pattern. Five made, and the pattern sits differently on each one. " + st(3, 2)),
 "r09": (A, "Remake 09 &middot; Sunderland of Scotland Blue and Purple", PR, "second-round-remake-09-headcover",
   "A Sunderland of Scotland jacket in a blue and purple 1990s print. The jacket itself is in the gallery, and it is the best before-and-after in the collection. " + st(2, 2)),
 "r13": (A, "Remake 13 &middot; Greg Norman Quarter-Zip", PR, "second-round-remake-13-headcover",
   "A Greg Norman quarter-zip in a diamond pattern that could only be from the 1990s. If you grew up watching the Shark, this is the one. " + st(2, 3)),
 "r15": (A, "Remake 15 &middot; Activology All-Over Golf Print", PR, "second-round-remake-15-headcover",
   "A vintage Activology windbreaker covered in an all-over golf print. A golf jacket printed with golf, now a cover for a golf club. Four made. " + st(2, 2)),
 "r03": (A, "Remake 03 &middot; Mizuno Black With White Lines", PR, "second-round-remake-03-headcover",
   "The quietest cover in the drop: black Mizuno technical cloth with contrasting white line detailing. Where the lines fall depends on where the jacket was cut. Four made. " + st(2, 2)),
 "r11": (A, "Remake 11 &middot; Ashworth Brown Compass", PR, "second-round-remake-11-headcover",
   "An Ashworth golf jacket with a compass pattern in earthy brown tones, the one we would put in our own bag. Six made, so it is also one of the easier ones to get. " + st(3, 3)),
 "r12": (A, "Remake 12 &middot; Ashworth Green Compass", PR, "second-round-remake-12-headcover",
   "The same Ashworth compass pattern in green. Each of the six covers carries a different part of the jacket, detailing included. " + st(3, 3)),
 "r14": (A, "Remake 14 &middot; TaylorMade Orange Windbreaker", PR, "second-round-remake-14-headcover",
   "A vintage TaylorMade windbreaker in classic orange, logo and all. Six made; the fairway covers sold out first. " + st(3, 3, fl=False)),
}
SECTIONS = [
 ("Tartans and Checks", "tartans", ["r01","r02","r04","r06","r10"],
  "<strong>Five remakes &middot; 25 covers</strong>The most Scottish part of the drop: tartan inserts, checks and a Sunderland of Scotland blue tartan that is already gone."),
 ("The &rsquo;90s Prints", "prints", ["r05","r07","r08","r09","r13","r15"],
  "<strong>Six remakes &middot; 26 covers</strong>The loud ones. Four Sunderland of Scotland jackets, a Reebok quarter-zip, a Greg Norman diamond and a golf print on a golf jacket."),
 ("Compasses and Plain Cloth", "plain", ["r03","r11","r12","r14"],
  "<strong>Four remakes &middot; 22 covers</strong>The calmer end: black Mizuno, Ashworth&rsquo;s compass pattern in brown and green, and one TaylorMade orange."),
]
N = 15
PQ = {
 "tartans": ("Worn before. Made again.", "Fyfe Golf, on Second Round"),
 "plain": ("Signs of their former life remain. Patterns shift from piece to piece.", "Fyfe Golf"),
}
CAP = "Photography &middot; Fyfe Golf&rsquo;s own"
BANDS = {
 "tartans": (CAP, "Before: three of the original jackets, photographed by Fyfe before they were cut.", [("band-1","The original Sunderland of Scotland jacket in a blue and purple 1990s print, laid flat","Sunderland, blue and purple"),("band-2","The original Greg Norman quarter-zip in a diamond pattern, laid flat","Greg Norman quarter-zip"),("band-3","The original green Mizuno golf top, laid flat","Mizuno green check")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Every golfer has seen these jackets: hanging in a thrift store, stuffed in a bag room, worn by someone&rsquo;s uncle in a 1996 photo. Fyfe Golf bought fifteen of them, took them apart in its workshop in Scotland and cut what was left into headcovers. The drop is called Second Round, and it is the best version yet of the thing Fyfe does several times a year, turning something that used to be something else into a cover.</p>
    <p>What makes it work is that Fyfe left the history in. Logos stay where they fell, a stripe or a tartan insert shows up on one cover and not the next, and the RBC Heritage jacket still reads like a tournament jacket. There are 73 covers in total, all with a black fleece lining and a FYFE REPURPOSED label, and no more cloth to make others. The blue tartan sold out within a day. If one of these is your jacket, buy it now.</p>
    <h2 class="products-hdr btk-story-hdr">The Drop</h2>
    <p>Second Round went live on October 9, 2026. Fyfe sourced golf jackets that were &ldquo;no longer fit for wearing&rdquo; but still had good cloth, from Mizuno, Reebok, Ashworth, Sunderland of Scotland, TaylorMade, Greg Norman, ProQuip and others. Each was deconstructed and remade by hand in Scotland, in driver and fairway sizes only. Fyfe notes that the original brands&rsquo; names appear only because they were on the garments, and that none of this is an official collaboration. Fyfe was founded by Neil Rennie in Fife in 2021; we covered the brand in our <a href="/drops/brand-to-know-fyfe-golf" style="border-bottom:1px solid currentColor">Fyfe Golf Brand to Know</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Maker</span><span>Fyfe Golf, Scotland</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>October 9, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Remakes</span><span>15 jackets, 73 covers</span></div>
      <div class="sidebar-detail"><span class="l">Sizes</span><span>Driver, fairway</span></div>
      <div class="sidebar-detail"><span class="l">Price</span><span>&pound;69 / &pound;65 ($95 / $89)</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Remake 11, Ashworth Brown Compass</span></div>
      <a href="https://www.fyfegolf.com/collections/second-round" target="_blank" rel="noopener" class="sidebar-cta">Shop Second Round &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#FyfeGolf</span>
        <span class="hashtag">#SecondRound</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#VintageGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What is Fyfe Golf Second Round?", "A limited run of headcovers that Fyfe Golf cut and remade by hand in Scotland from 15 vintage golf jackets. It went live on October 9, 2026, with 73 covers in total across driver and fairway sizes."),
 ("Which jackets were used?", "Jackets from Caviva, Mizuno, the RBC Heritage, Sunderland of Scotland, Reebok, ProQuip, Ashworth, Greg Norman, TaylorMade and Activology. Fyfe says the brand names appear only because they were on the original garments and that it is not an official collaboration."),
 ("How much do Second Round headcovers cost?", "On October 10, 2026, £69 for a driver cover and £65 for a fairway cover in Fyfe's UK store, or $95 and $89 in its US store."),
 ("How many were made?", "Between two and three of each size per jacket, four to six covers per jacket and 73 in total. Each product page lists exactly how many were made."),
 ("Will Fyfe make more?", "Not of these. Each cover is cut from a specific jacket, and once the cloth is used there is nothing left to make more from."),
]
FRN = json.loads((ROOT / "research/fyfe-second-round/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-FYFE-SR-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
            f'  <div class="drop-tag grass">{len(ids)} remakes</div>\n'
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
    <span>Fyfe Golf &middot; handmade in Scotland</span><span class="dot"></span>
    <span>15 remakes &middot; 73 covers &middot; stock checked October 10, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Fyfe Golf Second Round headcovers lined up in two rows on a wooden table, cut from vintage golf jackets" fetchpriority="high" /></div></div>
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
