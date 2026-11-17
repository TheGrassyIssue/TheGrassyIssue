#!/usr/bin/env python3
"""build-penfold-btk.py — Brand to Know: Penfold Golf. Cloned from build-fresh-three.py. 17 November 2026.
Lenny: "let's do a brand to know - https://penfoldgolf.net/", options sheet (54 in stock), then "looks good, let's build it" (picks ours, 27).
FACTS: Penfold's About Us page (A.E. Penfold, Maxfli, 1927 Bromford Lane, 1941 loss at sea, Dick Penfold, first to 1m balls in 1960,
Goldfinger 1964, Player/Pinero/Faldo, PGA Championship sponsorship); Forbes, Sept 23 2025 (Gavin Perrett, CEO of Penfold Golf Limited,
a licensee of the parent firm in England; attic restart Jan 2020; quotes); Philadelphia Inquirer 2021. Founding year: Penfold says 1927
(Wikipedia 1929) — use 1927. Colgate sale year disputed (1973 vs 1975) — leave the year out. Goldfinger marker dropped (its listing
photos are the ball box). Junior items left out. Archive photos are Penfold's own; the founder's portrait is not used.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Penfold Golf, the 1927 British Ball Maker Behind James Bond's Penfold Hearts"
DESC = ("Penfold Golf: the Birmingham ball maker James Bond played in Goldfinger, now back with waxed-canvas Sunday bags, "
        "card-suit ball markers and a 100th birthday in 2027. Its story and 27 picks with prices.")
H1 = "Brand to Know: Penfold Golf"
BC = "Brand to Know: Penfold Golf"
SLUG = "brand-to-know-penfold-golf"
IMG = "/images/penfold"
SHOP = "https://penfoldgolf.net/products/"
PF = "Penfold Golf"
P = {
 # Bags
 "heritage-sunday-bag-1": (PF, "Heritage Sunday Bag II", "$289", "heritage-sunday-bag-1",
   "Our pick from Penfold. A Sunday bag in British Millerain waxed canvas and full-grain leather, just under three pounds, modeled on the Penfold Sunday bags of the 1960s and 70s that are still being handed down. Holly Green or Dark Navy."),
 "sunday-stand-bag": (PF, "Sunday Stand Bag, Pine Green", "$295", "sunday-stand-bag",
   "The same idea with legs: a five-pound stand bag in pine green with cream trim and the pennant logo. The navy has sold out."),
 "sunday-stand-bag-copy": (PF, "Sunday Stand Bag, Deep Red", "$175", "sunday-stand-bag-copy",
   "The stand bag in deep red with white trim, for less than two-thirds of the green one&rsquo;s price."),
 "ryder-cup-1927-sunday-bag-europe": (PF, "Ryder Cup 1927 Sunday Bag", "$295", "ryder-cup-1927-sunday-bag-europe",
   "From the official Ryder Cup 1927 collection: a navy waxed-canvas Sunday bag in Team Europe blue and gold with the trophy crest. Penfold and the Ryder Cup both turn 100 in 2027."),
 "heritage-backpack-1": (PF, "Heritage Backpack II", "$169", "heritage-backpack-1",
   "A waxed-canvas backpack on the same full-grain leather base as the Sunday bag. Holly Green, Dark Navy or British Tan."),
 "heritage-shoe-bag-ii": (PF, "Heritage Shoe Bag II", "$129", "heritage-shoe-bag-ii",
   "A shoe bag in the same canvas and leather, with a zip pocket on the front for keys, phone and wallet. Holly Green or Dark Navy."),
 "heritage-wash-bag": (PF, "Heritage Wash Bag", "$89", "heritage-wash-bag",
   "The newest Heritage piece, added in September: a wash bag for the golf trip, in Holly Green or Dark Navy."),
 # Headcovers & accessories
 "heritage-headcover-ii": (PF, "Heritage Headcover II, Driver", "$50", "heritage-headcover-ii",
   "Our pick for the bag. Waxed canvas with a leather &ldquo;wing&rdquo; chevron, drawn from the covers Penfold&rsquo;s staff players used in the 1970s. Holly Green, Dark Navy or British Tan."),
 "heritage-headcover-ii-driver-copy": (PF, "Heritage Headcover II, Fairway", "$45", "heritage-headcover-ii-driver-copy",
   "The same cover for a fairway wood. Only Dark Navy is in stock."),
 "ryder-cup-1927-headcover-driver-1": (PF, "Ryder Cup 1927 Headcover, Driver", "$35", "ryder-cup-1927-headcover-driver-1",
   "A navy driver cover with gold stripes and the Ryder Cup crest, in Team Europe colors."),
 "heritage-shag-bag": (PF, "Heritage Shag Bag", "$119", "heritage-shag-bag",
   "A shag bag for practice balls in British Millerain Tekwax canvas, built, Penfold says, for a lifetime of practice. Three colors."),
 "heritage-accessories-pouch-ii": (PF, "Heritage Accessories Pouch II", "$39", "heritage-accessories-pouch-ii",
   "A small waxed-canvas pouch for tees, markers and a glove. The cheapest way into the Heritage line."),
 # Balls, markers, tees
 "penfold-heart": (PF, "Penfold Heart Golf Balls", "$40", "penfold-heart",
   "The ball. A three-piece urethane ball with a red heart, sold in a pack that says &ldquo;19 Hearty 27.&rdquo; It is the ball Bond plays in <em>Goldfinger</em>."),
 "007-playing-card-ball-marker": (PF, "007 Playing Card Ball Marker", "$25", "007-playing-card-ball-marker",
   "A black playing-card marker with the Penfold heart and 007. Small, and a very good joke on the green."),
 "ace-ball-marker-spades": (PF, "Ace Ball Marker, Spades", "$20", "ace-ball-marker-spades",
   "The card suits go back to Penfold&rsquo;s 1950s balls. There is a marker for each suit, plus a joker."),
 "ryder-cup-1927-ball-marker-europe": (PF, "Ryder Cup 1927 Ball Marker", "$25", "ryder-cup-1927-ball-marker-europe",
   "An official Ryder Cup 1927 marker in Team Europe blue with the trophy."),
 "penfold-man-ball-marker": (PF, "Penfold Man Ball Marker", "$20", "penfold-man-ball-marker",
   "Made to look like the old metal pro-shop signs advertising Penfold balls, with the Penfold Man in plus fours."),
 "heritage-duo-ball-marker": (PF, "Heritage Duo Ball Marker", "$20", "heritage-duo-ball-marker",
   "A heavy marker in Penfold green and gold with a coin insert."),
 "multidentification-tee-pack": (PF, "Multidentification Tee Pack", "$15", "multidentification-tee-pack",
   "Hardwood tees with colored tips, so everyone in the group knows whose is whose."),
 # Clothing
 "british-stripe-rugby": (PF, "British Stripe Rugby", "$50", "british-stripe-rugby",
   "Our pick from the clothes. A 100% cotton rugby shirt in olive and coral stripes with a thick contrast collar. Only small and medium are left."),
 "pinero-polo": (PF, "Pinero Polo", "$35", "pinero-polo",
   "A tribute to Manuel Pi&ntilde;ero, the Penfold staffer who won the 1977 Penfold PGA Championship. Coral pique with a tipped collar."),
 "jersey-pocket-polo": (PF, "Jersey Pocket Polo", "$30", "jersey-pocket-polo",
   "Penfold&rsquo;s signature polo: slim, retro and made for playing in. Green or pink."),
 "flatlock-script-crew": (PF, "Flatlock Script Crew", "$45", "flatlock-script-crew",
   "A French terry sweatshirt modeled on early-90s ones, with the script logo on the chest."),
 "icon-corduroy-dad-hat": (PF, "Icon Corduroy Dad Hat", "$25", "icon-corduroy-dad-hat",
   "A six-panel corduroy cap with the Penfold P, in brown or navy."),
 "gx-performance-pinero-yellow": (PF, "GX Performance Glove", "$24", "gx-performance-pinero-yellow",
   "The glove Perrett calls a flagship of the brand, in thin tour-grade leather with a card suit on the tab. Several colorways."),
 # Desk
 "penfold-tradition-pro-shop-sign-replica": (PF, "Penfold Tradition Pro Shop Sign Replica", "$25", "penfold-tradition-pro-shop-sign-replica",
   "A replica of the old pro-shop sign for the Penfold Tradition, which Penfold says Seve Ballesteros played to win the 1979 Open. For the office wall."),
 "canvas-golf-journal": (PF, "Canvas Golf Journal", "$40", "canvas-golf-journal",
   "A hand-bound journal made in Stamford, England, with pages for courses played, greens and fairways hit, and putts. Beige is in stock."),
}
SECTIONS = [
 ("The Bags", "bags", ["heritage-sunday-bag-1","sunday-stand-bag","sunday-stand-bag-copy","ryder-cup-1927-sunday-bag-europe","heritage-backpack-1","heritage-shoe-bag-ii","heritage-wash-bag"],
  "<strong>Seven picks &middot; $89&ndash;$295</strong>Waxed canvas from British Millerain, the Lancashire mill that pioneered it, and full-grain leather."),
 ("Headcovers &amp; Bag Accessories", "headcovers", ["heritage-headcover-ii","heritage-headcover-ii-driver-copy","ryder-cup-1927-headcover-driver-1","heritage-shag-bag","heritage-accessories-pouch-ii"],
  "<strong>Five picks &middot; $35&ndash;$119</strong>The same canvas and leather, in smaller pieces."),
 ("Balls, Markers &amp; Tees", "balls-markers", ["penfold-heart","007-playing-card-ball-marker","ace-ball-marker-spades","ryder-cup-1927-ball-marker-europe","penfold-man-ball-marker","heritage-duo-ball-marker","multidentification-tee-pack"],
  "<strong>Seven picks &middot; $15&ndash;$40</strong>Where Penfold started: the ball, and the card suits it put on them."),
 ("Clothes &amp; Gloves", "clothes", ["british-stripe-rugby","pinero-polo","jersey-pocket-polo","flatlock-script-crew","icon-corduroy-dad-hat","gx-performance-pinero-yellow"],
  "<strong>Six picks &middot; $24&ndash;$50</strong>Retro polos, a rugby shirt and the glove. Sizes are running low on some."),
 ("For the Wall &amp; Desk", "desk", ["penfold-tradition-pro-shop-sign-replica","canvas-golf-journal"],
  "<strong>Two picks &middot; $25&ndash;$40</strong>For the golfer who also likes the history."),
]
N = 27
PQ = {
 "bags": ("Here&rsquo;s my Penfold Hearts.", "James Bond, in Goldfinger (1964)"),
 "balls-markers": ("We know our lane. We know what we need to do.", "Gavin Perrett, CEO of Penfold Golf Limited, to Forbes"),
 "clothes": ("Our past isn&rsquo;t just a part of who we are, it defines our present, and our future.", "Penfold Golf, on its About Us page"),
}
CAP = "Photography &middot; Penfold Golf&rsquo;s own"
BANDS = {
 "headcovers": ("From the archive", "From Penfold&rsquo;s own history pages.", [("band-1-1","The Penfold factory on Bromford Lane in Birmingham","Bromford Lane"),("band-1-2","A. E. Penfold&rsquo;s patent drawing for golf ball patterns","The patent"),("band-1-3","A vintage Penfold advertisement for the Penfold 75","The ad")]),
 "clothes": ("Penfold now", "From Penfold Golf&rsquo;s own photos.", [("band-2-1","A Penfold ball with a club suit on the grass","The club suit"),("band-2-2","A golfer changing shoes in a locker room","The locker room"),("band-2-3","Golfers sitting in a shelter beside the course","The shelter")]),
 "end": ("Then and now", "From Penfold&rsquo;s own photos.", [("band-3-1","An aerial view of the Penfold factory in Birmingham","The factory"),("band-3-2","A cargo ship at sea in black and white, from Penfold&rsquo;s archive","From the archive"),("band-3-3","A Penfold Heritage Sunday Bag in British Tan","The Sunday bag")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Penfold is one of the oldest names in golf, and the one James Bond named on screen. In <em>Goldfinger</em> (1964), Bond swaps balls on Auric Goldfinger and wins the match on the 18th green: &ldquo;Here&rsquo;s my Penfold Hearts.&rdquo;</p>
    <p>The company started in 1927. A.&nbsp;E. Penfold had designed Dunlop&rsquo;s famous Maxfli ball before leaving to set up his own factory on Bromford Lane in Birmingham, where he worked out a way to wind the rubber thread inside a ball under extreme tension. Penfold balls were marked with playing-card suits, the company opened a second factory in Brooklyn in 1935, and its About Us page says that by 1960 it was the first maker to produce more than a million balls in a year.</p>
    <p>It was not an easy run. A.&nbsp;E. Penfold died in 1941 when the ship he was on was torpedoed off the coast of Ireland, and the factory was bombed during the war. His son Dick rebuilt it. Gary Player played the Penfold Ace, Manuel Pi&ntilde;ero won the 1977 Penfold PGA Championship, and Nick Faldo won his first big title with a Penfold ball in 1978. Then the brand was sold, sold again and went quiet.</p>
    <p>It came back through Gavin Perrett, a British expat in Pennsylvania who, Forbes reports, sent a &ldquo;very cheeky&rdquo; email to Penfold&rsquo;s owner in 2013 and restarted the brand from his attic in January 2020. He runs Penfold Golf Limited, a licensee of the parent company in England, and he does not like the word revival: &ldquo;People don&rsquo;t realize that we weren&rsquo;t revived&mdash;we just weren&rsquo;t really doing anything.&rdquo; Today Penfold makes Sunday bags in British Millerain waxed canvas, an official Ryder Cup 1927 collection, retro polos and a lot of very good ball markers. Penfold and the Ryder Cup both turn 100 in 2027.</p>
    <h2 class="products-hdr" style="margin-top:32px">Where to Start</h2>
    <p><strong>For the bag:</strong> the Heritage Sunday Bag II ($289). It is the piece the rest of the line is built around, and the one most likely to be handed down.</p>
    <p><strong>For a gift:</strong> a sleeve of Penfold Hearts ($40) and the 007 Playing Card marker ($25). Every golfer who has seen <em>Goldfinger</em> will get it.</p>
    <p><strong>For under $50:</strong> the Heritage Headcover ($50) or the British Stripe Rugby ($50).</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1927, Birmingham, England</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>A. E. Penfold</span></div>
      <div class="sidebar-detail"><span class="l">Today</span><span>Penfold Golf Limited, CEO Gavin Perrett</span></div>
      <div class="sidebar-detail"><span class="l">Famous for</span><span>The Penfold Heart in Goldfinger</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$15&ndash;$295</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Heritage Sunday Bag II, Heritage Headcover II, British Stripe Rugby</span></div>
      <div class="hashtags">
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#PenfoldGolf</span>
        <span class="hashtag">#PenfoldHearts</span>
        <span class="hashtag">#SundayBag</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">A Hundred Years Next Year</h2>
    <p>Most of the brands we cover are a few years old and still working out who they are. Penfold has the opposite problem: almost a hundred years of story, and the job of making it mean something to golfers who were not born when Bond played that ball. The waxed-canvas bags and the card-suit markers are a good answer.</p>
    <p>Perrett told Forbes he has &ldquo;three or four really big stories&rdquo; planned on the way to 2027. We will be watching. Prices were checked on November 17, 2026. For more bags like these, see <a href="/drops/upgrading-your-golf-bag">Upgrading Your Golf Bag</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/penfold/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-17", "dateModified": "2026-11-17",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Brand to Know", "item": "https://thegrassyissue.com/#feed"},
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
    <span>Brand to Know</span><span class="dot"></span>
    <span>{N} picks &middot; prices checked November 17, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A Penfold golf ball with a club suit sitting on the grass beside an iron" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Pluto", "Bord", "Pierre", "Studio Grain"):
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
