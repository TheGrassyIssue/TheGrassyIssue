#!/usr/bin/env python3
"""build-fyfe-gra.py — Fyfe Golf, Golden Restless Age drop. 29 October 2026. Cloned from build-golden-soul-btk.py.
Lenny: "Let's do a post about this Fyfe Drop" + lookbook link + "I want this post to really have extra special visuals":
four full-bleed lookbook chapters (Drive, Locker Room, Dining Room, Course) with mosaic collages, manifesto opener, full-bleed close.
FACTS: fyfegolf.com collection products.json + product copy + lookbook page, read in Chrome 29 Oct 2026 (USD presentment); Neil Rennie quote from our Fyfe BTK (Wandering Golfers 2022).
OLD HEADER (Golden Soul):
Lenny: "Let's do a brand to know - goldensoulgolf.com" -> options -> "less bags and more headcovers" -> "let's build it with good lookbook and IRL images" (all 52 from options v2).
FACTS: goldensoulgolf.com About/Mission/Vision + product copy (research/golden-soul/catalogue.json, 28 Oct 2026, USD); Bisque Golf collection page. No founder is published: never name one.
OLD HEADER (Penta):
Lenny: "Let's do a brand to know - https://penta-golf.com/" -> options sheet -> "Lets build the post" (all 20: 14 in stock + 6 sold out).
FACTS: penta-golf.com About + live catalogue (research/penta/catalogue.json, USD, 28 Oct 2026); Monster Children Q&A (Feb 2024).
Founders stay unnamed (the brand never names them). Never "worth".
OLD HEADER (Paré):
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Fyfe Golf Golden Restless Age: Harris Tweed, Lambswool and a Game of Feel"
DESC = ("Fyfe Golf's Golden Restless Age drop: twelve Harris Tweed, waxed canvas and leather headcovers, Scottish lambswool knits, "
        "a Glasgow-bound golfer's diary and the 24th MacKenzie x Fyfe bag. The full lookbook, with prices.")
H1 = "Golden Restless Age: Fyfe Golf&rsquo;s New Drop Is a Game of Feel"
BC = "Fyfe Golf: Golden Restless Age"
SLUG = "fyfe-golf-golden-restless-age"
IMG = "/images/fyfe-golden-restless-age"
SHOP = ""
C = "Fyfe Golf"
SO = " &middot; sold out"
_CARDS = json.loads((ROOT / "research/fyfe-gra/cards.json").read_text())
COPY = {
 "mackenzie-24": "Our pick. The 24th MacKenzie x Fyfe edition: green leather with mahogany trim, a seven-inch opening and single divider, a split cream-and-mahogany base, and a pocket lined in this collection&rsquo;s Harris Tweed. A special-edition leather patch marks it.",
 "weekender": "A duffle in dark green or dark grey canvas with a leather base and Fyfe patch. Made in Scotland on pre-order, dispatching from November 9.",
 "shoe-bag": "The matching shoe bag, in dark green or dark grey, with a tartan-lined interior.",
 "glove-caddy": "A case for your spare gloves, in the same green or grey. Made in Scotland on pre-order, dispatching from November 9.",
 "player-crew": "Knitted in Scotland from single-ply Super Geelong lambswool, the finest grade of first-clip merino, on a fine 21-gauge frame. Tartan green, grey flannel or dark navy. Swipe for all three.",
 "shawl": "The big-ticket knit: a shawl-collar cardigan knitted in Scotland from Geelong lambswool in a full cardigan stitch, with real weight to it. Fyfe calls it a modern heirloom.",
 "diary": "A place to keep scores, matches and stats by hand, bound in Glasgow by second-generation bookbinders in black Scottish cowhide.",
 "keeper": "A leather scorecard holder from the same Glasgow bookbinders, black pebble-grain outside and tan inside, with a pencil.",
 "carlogie": "The showpiece cover: deep green Harris Tweed with the Lion Rampant and crossed clubs embroidered in gold. Driver, fairway, blade and mallet.",
 "burnside": "Greens that blend into each other with hints of grey, which Fyfe likens to a course in autumn. Two driver styles, plus blade and mallet.",
 "auchmithie": "A light grey, almost bone-colored tweed crossed by fine grey overchecks. The cleanest of the twelve.",
 "airlie": "Light grey tweed with a brown leather belly band, Fyfe&rsquo;s update of a long-running favorite, the Gun Dog.",
 "broughty": "A charcoal check with brown running through it. Every shape: driver, fairway, blade and mallet.",
 "monikie": "Soft greys running vertically, which Fyfe says recall the lines the sea leaves on coastal rock.",
 "edzell": "A darker grey houndstooth on a very light grey base. The blade cover had already sold out.",
 "glamis": "Deep charcoal and black lifted by flecks of light grey. The darkest tweed in the drop.",
 "tealing": "Charcoal tweed with a black leather belly band, tweed against leather in two tones.",
 "letham": "A deep purple-black tweed that reads plain until you get close. Driver, blade and mallet.",
 "brechin": "Not tweed: charcoal Scottish waxed canvas from Halley Stevensons in Dundee, with a semi-dry finish.",
 "gt-vanquish": "Dark olive Italian nappa leather, very soft, in the deep green of Fyfe&rsquo;s GT series.",
}
P = {k: (C, t, p, u, COPY[k]) for k, t, p, u, _ in _CARDS}
SECTIONS = [
 ("In the Boot", "drive", ["mackenzie-24", "weekender", "shoe-bag", "glove-caddy"],
  "<strong>Four pieces &middot; $122&ndash;$1,161</strong>The bag, and everything that goes in the boot with it."),
 ("The Knits", "locker-room", ["player-crew", "shawl"],
  "<strong>Two knits &middot; $171&ndash;$676</strong>Scottish lambswool, knitted in Scotland."),
 ("Keeping Score", "dining-room", ["diary", "keeper"],
  "<strong>Two pieces &middot; $67&ndash;$89</strong>For keeping the score by hand, bound in Glasgow."),
 ("The Headcovers", "course", ["carlogie", "burnside", "auchmithie", "airlie", "broughty", "monikie", "edzell", "glamis", "tealing", "letham", "brechin", "gt-vanquish"],
  "<strong>Twelve headcovers &middot; from $89</strong>Ten Harris Tweeds, one waxed canvas and one nappa leather. Each card groups the shapes made in that cloth."),
]
N = 20
PQ = {}
CH = {
 "drive": ("I", "The Drive In", "A familiar road to the first tee.", "lb-gra-car-shots-89.jpg", "A grey BMW parked under pine trees with two golf bags leaning on the back",
   [("lb-gra-car-shots-82.jpg", "w4 t", "A man in a green crew neck leaning on the car with his bags"), ("lb-gra-car-shots-46.jpg", "w2 t", "Golf bags in the open back door of the car"),
    ("lb-gra-car-shots-7.jpg", "w2", "Hands on a wood-rimmed steering wheel"), ("lb-gra-car-shots-107.jpg", "w2", "The open boot with headcovers inside"),
    ("lb-gra-car-shots-45.jpg", "w2", "Tweed headcovers on the car&rsquo;s back seat")]),
 "locker-room": ("II", "The Locker Room", "The sound of spikes on timber floors.", "lb-gra-crew-necks-12.jpg", "Close-up of a grey lambswool crew neck and its Fyfe label on a wooden bench",
   [("lb-gra-look-book-8.jpg", "w2 t", "A man in a grey crew neck leaning back in a dark locker room"), ("lb-clubhouse-shawl-gra-locker-room-8.jpg", "w2 t", "The grey shawl cardigan hanging on a wooden locker"),
    ("lb-gra-locker-room-31.jpg", "w2 t", "A cardigan and golf bag in an open wooden locker"), ("lb-gra-macs-7.jpg", "w3", "Harris Tweed headcovers in a leather bag in the locker room"),
    ("lb-duffells-etc-12.jpg", "w3", "The Weekender bag on a wooden bench")]),
 "dining-room": ("III", "The Dining Room", "A handwritten scorecard. A pencil worn smooth through use.", "lb-gra-look-book-2.jpg", "A man in a green crew neck standing by his bag in a red-carpeted clubhouse dining room",
   [("lb-gra-dining-room-29.jpg", "w2 t", "A man in the shawl cardigan in the clubhouse dining room"), ("lb-gra-dining-room-39.jpg", "w2 t", "A man reading in a leather chair by a window"),
    ("lb-gra-books-holders-12.jpg", "w2 t", "Hands opening the Keeper scorecard holder"), ("lb-gra-books-holders-25.jpg", "w3", "The Golfer&rsquo;s Diary open in a hand"),
    ("lb-gra-books-holders-5.jpg", "w3", "The Golfer&rsquo;s Diary held over the grass")]),
 "course": ("IV", "The Course", "No notifications. No algorithms. No feeds. Just the game.", "lb-gra-look-book-12.jpg", "A golfer standing beside a stone hut under a huge bush on a links course",
   [("lb-gra-on-course-42.jpg", "w4 t", "A man in a navy crew neck walking a fairway under pines"), ("lb-gra-on-course-4.jpg", "w2 t", "A tweed headcover and glove on the grass beside a bag"),
    ("lb-gra-on-course.jpg", "w2", "A golfer walking across the course in a grey knit"), ("lb-gra-on-course-12.jpg", "w2", "A golfer with his bag against a pale sky"),
    ("lb-gra-look-book-9.jpg", "w2", "A golfer mid-stride on the fairway")]),
}
BANDS = {k: None for k in CH}
TAKE = """
<section class="products gra-open" style="border-top:none">
  <div class="gra-manifesto">
    <p class="gra-kick">Fyfe Golf &middot; Golden Restless Age</p>
    <p class="gra-big">&ldquo;In an age that measures everything, golf is still a game of feel.&rdquo;</p>
    <p class="gra-small">&ldquo;Coffee brewed slowly before dawn. A familiar road to the first tee.&rdquo; That&rsquo;s how Fyfe introduces its new collection, and the lookbook below is shot the same way: a drive out, the locker room, the dining room, then the course.</p>
  </div>
</section>
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Fyfe Golf is a Scottish brand we&rsquo;ve covered since its <a href="/drops/brand-to-know-fyfe-golf">Brand to Know</a>, and Golden Restless Age is one of its biggest drops yet. It went to an early-access list first, and the full collection is now on Fyfe&rsquo;s site: twelve headcovers, three lambswool knits, a weekender, a shoe bag, a glove caddy, two leather books for keeping score and the 24th edition of the <a href="/drops/fyfe-x-mackenzie-every-edition">MacKenzie x Fyfe</a> bag.</p>
    <p><strong>The idea.</strong> Fyfe&rsquo;s note for the collection is about what golf still has that most of life has lost: presence and feel. &ldquo;No notifications. No algorithms. No feeds. Just the game.&rdquo; Everything is made to be handled: Harris Tweed woven in the Outer Hebrides, waxed canvas from Dundee, lambswool knitted in Scotland, and scorebooks bound by hand in Glasgow.</p>
    <p><strong>What to buy.</strong> The MacKenzie bag is the centerpiece, and at $1,161 the most expensive piece. The headcovers are where most people will start, from $89, in ten Harris Tweeds and a waxed canvas. The Player Crew Neck at $171 is the knit we&rsquo;d buy. Prices are in US dollars as Fyfe&rsquo;s store shows them to US shoppers; the Weekender and Glove Caddy are pre-orders that dispatch from November 9.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Drop</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Fyfe Golf, Scotland</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>Golden Restless Age</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>51 listings</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$67&ndash;$1,161</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>MacKenzie x Fyfe 24th Edition</span></div>
      <div class="hashtags">
        <span class="hashtag">#FyfeGolf</span>
        <span class="hashtag">#HarrisTweed</span>
        <span class="hashtag">#GoldenRestlessAge</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<div class="gra-bleed gra-close"><img src="/images/fyfe-golden-restless-age/lb-gra-macs-10.jpg" alt="Close-up of a golf bag&rsquo;s leather straps and houndstooth tweed in warm low light" loading="lazy" />
  <div class="gra-cap"><p class="gra-big">Just the game.</p></div></div>
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">Heritage and Provenance</h2>
  <div class="writeup-body">
    <p>Fyfe began with a complaint. Founder Neil Rennie spent years walking into Scottish pro shops and finding nothing that had anything to do with Scotland. &ldquo;Going around the pro shops and golf retailers, I couldn&rsquo;t find that more elevated product, with heritage and provenance,&rdquo; he told The Wandering Golfers in 2022. &ldquo;Everything was mass-produced and heavily branded.&rdquo; Fyfe launched in November 2021.</p>
    <p>Golden Restless Age is that idea at full size. Every cloth has an address: the Harris Tweed is woven in the Outer Hebrides from pure new wool, the waxed canvas comes from Halley Stevensons in Dundee, the knitwear is made in Scotland from Geelong lambswool, and the leather books are bound in Glasgow from cowhide tanned in Barrhead.</p>
    <p>It&rsquo;s also the 24th time Fyfe has worked with MacKenzie, the Oregon bag maker. If you want to see the other twenty-three, our <a href="/drops/fyfe-x-mackenzie-every-edition">Fyfe x MacKenzie archive</a> has every edition.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
GRA_CSS = """<style>/*GRA*/
.gra-bleed{position:relative;width:100vw;margin-left:calc(50% - 50vw);margin-top:48px;overflow:hidden;background:#111}
.gra-bleed img{display:block;width:100%;height:min(78vh,820px);object-fit:cover}
.gra-cap{position:absolute;left:0;right:0;bottom:0;padding:48px 6vw 40px;background:linear-gradient(transparent,rgba(10,14,10,.72));color:#f3efe6}
.gra-cap .gra-num{font-family:var(--mono);font-size:12px;letter-spacing:.24em;text-transform:uppercase;opacity:.85;margin:0 0 6px}
.gra-cap h2{font-size:clamp(34px,6vw,76px);line-height:1;margin:0 0 10px;color:#f3efe6;font-weight:500}
.gra-cap .gra-line{font-style:italic;font-size:clamp(16px,2vw,22px);margin:0;opacity:.95}
.gra-close .gra-cap{text-align:center}.gra-close .gra-big{font-size:clamp(32px,5vw,64px);font-style:italic;margin:0;color:#f3efe6}
.gra-collage{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:clamp(150px,19vw,260px);gap:10px;max-width:1240px;margin:10px auto 0;padding:0 16px}
.gra-collage figure{margin:0;overflow:hidden;position:relative}.gra-collage img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s ease}
.gra-collage figure:hover img{transform:scale(1.03)}
.gra-collage .w2{grid-column:span 2}.gra-collage .w3{grid-column:span 3}.gra-collage .w4{grid-column:span 4}.gra-collage .t{grid-row:span 2}
.gra-manifesto{max-width:880px;margin:24px auto 44px;text-align:center;padding:0 20px}
.gra-manifesto .gra-kick{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;opacity:.6;margin:0 0 14px}
.gra-manifesto .gra-big{font-size:clamp(28px,4.2vw,50px);line-height:1.12;font-style:italic;margin:0 0 18px}
.gra-manifesto .gra-small{font-size:17px;line-height:1.7;opacity:.85;margin:0}
.gra-open{display:block}
@media(max-width:760px){.gra-collage{grid-template-columns:repeat(2,1fr);grid-auto-rows:44vw}.gra-collage .w2,.gra-collage .w3,.gra-collage .w4{grid-column:span 1}.gra-collage .w4{grid-column:span 2}.gra-collage .t{grid-row:span 1}.gra-bleed img{height:62vh}}
</style>
"""
FRN = json.loads((ROOT / "research/fyfe-gra/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-29", "dateModified": "2026-10-29",
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
    num, title, line, big, bigalt, tiles = CH[k]
    figs = "\n".join(f'    <figure class="{cls}"><img src="{IMG}/{f}" alt="{alt}" loading="lazy" /></figure>' for f, cls, alt in tiles)
    return (f'\n<div class="gra-bleed" id="ch-{k}"><img src="{IMG}/{big}" alt="{bigalt}" loading="lazy" />\n'
            f'  <div class="gra-cap"><p class="gra-num">Chapter {num}</p><h2>{title}</h2><p class="gra-line">{line}</p></div></div>\n'
            f'  <div class="gra-collage">\n{figs}\n  </div>\n')


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
    <span>The Drop &middot; Fyfe Golf &middot; Scotland</span><span class="dot"></span>
    <span>20 picks, the full lookbook &middot; checked October 29, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer finishing his swing beneath tall Scots pines in low autumn light, from Fyfe Golf&rsquo;s Golden Restless Age lookbook" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + GRA_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
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
