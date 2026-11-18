#!/usr/bin/env python3
"""build-backyard-chipping.py — Backyard fall chipping post, 18 November 2026. Cloned from build-around-the-greens.py.
Lenny: "I recently got a practice mat for my backyard, let's find some good practice tools for chipping along with some wedges,
and then do 6 Hoodies & 6 shorts ... Let's also create a practice game for the post." Then: more casual gym shorts, include Apres Golf
in hoodies, prioritize the best photos. Options sheet v2; Lenny said build. Prices/stock checked live Nov 18, 2026 (Malbon short from
the Nov 16 sweep; its store rate-limited the live check). Nothing here was featured on TGI before (checked against used.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Backyard Chipping Practice: 8 Tools, 5 Wedges, a Game and What to Wear"
DESC = ("A casual fall chipping setup for the backyard: Divot Board, BirdieBall, SKLZ and EyeLine targets, wedges from Miura, Bettinardi, "
        "Fourteen and Haywood, six hoodies, six gym shorts and Nine Inside 50, a nine-shot game for distance and trajectory control.")
H1 = "Backyard Chipping, Fall Edition"
BC = "Backyard Chipping"
SLUG = "backyard-chipping-practice-fall"
IMG = "/images/backyard-chipping"
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "t1": ("Divot Board", "Divot Board", "$99.99", U("divotboard.com","divot-board"),
   "Shows where your club meets the ground and which way it travels through impact, so you see a fat or thin chip before the ball tells you. Works with or without a ball, indoors or out, and clips to a bag."),
 "t2": ("almostGOLF", "Short Shot Bundle", "$79.99", U("almostgolf.com","short-shot"),
   "A pop-up chipping net with three separate targets that sets up in the yard or the living room, and folds away when the lawn is needed for something else."),
 "t3": ("BirdieBall", "Close 2 Pin Backyard Chipping Game", "$17.99", U("birdieball.com","close-2-pin-backyard-chipping-game"),
   "A plastic pin and four colored foam balls. BirdieBall calls it golf plus bocce plus H.O.R.S.E. The cheapest way to turn the yard into a game."),
 "t4": ("BirdieBall", "BirdieTargets, Set of 3 with Bag", "$144.99", U("birdieball.com","birdietargets-set-of-3-with-bag"),
   "Three flag targets that collapse flat into a small bag, used upright or in a half-moon position. Made for BirdieBalls, but they take real balls too."),
 "t5": ("SKLZ", "SKLZ | Barstool Quickster Chipping Net", "$54.99", U("sklz.com","quickster-chipping-net"),
   "Three target holes in different sizes plus ball-collection slots, so you spend more time chipping and less time chasing balls around the yard."),
 "t6": ("EyeLine Golf", "Target Circle Rings", "$24.95", U("eyelinegolf.com","target-circles"),
   "Bright, ultra-thin rings that lie flat, so the ball rolls right over them. In 3- and 6-foot sizes, they are the landing zones for the game below."),
 "t7": ("VESSEL", "Shag Bag", "$44", U("vesselgolf.com","shag-bag"),
   "Holds 90 to 130 balls in black, from the Carlsbad bag maker. Fill it once and the session is set."),
 "t8": ("Kraken Golf", "Kraken Course Flag, White Edition", "$79", U("krakengolf.com","kraken-course-flag-white-edition"),
   "A 14-by-20-inch canvas flag with the Kraken crest embroidered in black and brass grommets. Fly it on the pin at the far end of the yard."),
 "w1": ("Miura", "Forged Wedge Series, C Grind Raw", "$320", U("miuragolf.com","forged-wedge-series-c-grind-raw"),
   "Forged in Japan with Miura&rsquo;s C grind, in a raw finish that ages with every session. The one to buy if you want to keep it for years."),
 "w2": ("Bettinardi Golf", "HLX 6.0 Japanese Bronze Limited Run Wedge", "$199.99", U("bettinardi.com","hlx-6-0-japanese-bronze-limited-run-wedges"),
   "Soft carbon steel in a limited bronze finish, in C and RJ grinds from 48 to 60 degrees. It looks like fall."),
 "w3": ("Fourteen Golf", "RM-&alpha; Wedge", "$240", U("fourteengolf.com","rm-%CE%B1-wedges-stock"),
   "From the Japanese wedge specialist, built with an N.S. Pro TS-101W wedge shaft in lofts from 46 to 58 degrees."),
 "w4": ("Haywood Golf", "&ldquo;Blue &amp; Gold&rdquo; Europe Wedge, 56&deg; or 60&deg;", "$203", U("haywoodgolf.com","haywood-blue-amp-gold-europe-wedges-56-60-rh-limited-edition"),
   "A micro-run of right-hand forged wedges, laser-engraved with gold and blue stars and EUROPE in royal-blue script. When it is gone, it is gone."),
 "w5": ("STIX", "Compete 60&deg; Wedge", "$119", U("stixgolf.com","compete-60-wedge"),
   "431 stainless with a milled face and a 10-degree double sole grind, in matte and satin black. The flop-shot club for the far target."),
 "h1": ("Gumtree Golf &amp; Nature Club", "NY Branches Oversize Logo Hoodie", "$145", "https://www.gumtreegolfandnature.com/shop/p/ny-branches-hoodie",
   "Gumtree&rsquo;s home-team hoodie for New York: 11.8-ounce heavyweight fleece made in the USA, an oversized NY branch logo embroidered on the chest and a boxy fit. Stock is thin, mostly smalls, when we checked."),
 "h2": ("Pins &amp; Aces", "Support Your Local Muni Hoodie, Blue", "$67.96", U("pinsandaces.com","support-your-local-muni-lifestyle-hoodie-blue"),
   "For frosty first tee times: &ldquo;Support Your Local Muni&rdquo; and a greenskeeper pushing a reel mower on the back, an embroidered logo on the front. From Arvada, Colorado."),
 "h3": ("Radmor", "Higgins 2.0 Hoodie", "$94.50", U("radmorgolf.com","higgins-2-0-hoodie"),
   "Lightweight loop terry in organic Peruvian Pima cotton with a little stretch. Substantial without being heavy, for the last light of a cool evening."),
 "h4": ("Jones Sports Co.", "Range Hoodie, Cabernet", "$148", U("jonessportsco.com","range-hoodie-cabernet"),
   "Double-knit performance fleece with a DWR finish, so it sheds the dew. A zippered stash pocket keeps your glove or phone dry."),
 "h5": ("Devereux", "Daily Hoodie, Blue", "$118", U("devereuxgolf.com","daily-hoodie-blue-1"),
   "A fully fashioned knit hoodie with a soft hand, cut to wear over a tee once the weather cools."),
 "h6": ("Apr&egrave;s-Golf", "Find Your Line Hoodie", "$98", U("apresgolf.com","i-will-not-apres-golf%C2%AE-hoodie"),
   "Mid-weight cotton-blend fleece in cream, with APR&Egrave;S-GOLF arched over a gondola on the back. Their line: &ldquo;Gondola? How about golfdola.&rdquo;"),
 "s1": ("Devereux", "Golf Mesh Short, Black", "$58", U("devereuxgolf.com","golf-mesh-short-black"),
   "Heavyweight breathable mesh with an elastic waist, an internal drawstring and a 5.5-inch inseam. Final sale, so check the size chart."),
 "s2": ("Malbon Golf", "Mesh Basket Pocket Short, Olivine", "$138", U("malbon.com","mesh-basket-pocket-short-olivine"),
   "Stretch shell, elastic waist and three sets of pockets, including the mesh basket pocket it is named for. 5.5-inch inseam."),
 "s3": ("Pins &amp; Aces", "Player Preferred Waffle Knit Short, Glacier", "$49.95", U("pinsandaces.com","player-preferred-waffleknit-shorts-blue-gray"),
   "Soft waffle-knit cotton blend with a 7.5-inch inseam. Pins &amp; Aces says they are great for the gym and lounging around the house, which is the brief."),
 "s4": ("Gramicci", "Nylon Block Short", "$70", U("gramicci.com","nylon-block-short"),
   "Recycled nylon with Gramicci&rsquo;s integrated belt, a zippered pocket and a gusseted crotch. Water-resistant, so a wet lawn is no problem."),
 "s5": ("Students Golf", "Oaklawn Mesh Short", "$92", U("studentsgolf.com","oaklawn-mesh-shorts-1"),
   "Lightweight polyester mesh with vertical Students graphics down the side panels, an elastic waist and an above-the-knee cut."),
 "s6": ("Ghost Golf", "Fairway Windshort V2", "$75", U("ghostgolf.com","fairway-windshort-v2"),
   "Wind- and water-resistant for dewy mornings, with invisible zip pockets and a tee pocket on the leg."),
}
SECTIONS = [
 ("The Practice Tools", "tools", ["t1","t5","t2","t6","t4","t3","t7","t8"],
  "<strong>Something to hit off, something to aim at</strong>The mat is the start. After that you need feedback on contact, a few targets at different distances and a bag to hold the balls. Everything here sets up in a few minutes and comes down just as fast."),
 ("The Wedges", "wedges", ["w1","w2","w3","w4","w5"],
  "<strong>One wedge you trust</strong>The game above uses a single club the whole way through, so pick the wedge you like looking down at. Ball position does the rest."),
 ("The Hoodies", "hoodies", ["h1","h2","h3","h4","h5","h6"],
  "<strong>For the cool evening session</strong>Fleece, terry and knit, none of them stiff enough to get in the way of a short swing. Pick one with a hood for when the sun drops behind the fence."),
 ("The Gym Shorts", "shorts", ["s1","s2","s3","s4","s5","s6"],
  "<strong>It is the backyard, not the club</strong>Mesh, waffle knit and nylon with elastic waists. Wear them with the hoodie while it is still warm enough in the afternoon."),
]
N = 25
SECN = {"tools": 8, "wedges": 5, "hoodies": 6, "shorts": 6}
PAIRS = {}
BANDS = {}
GAME = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">The game</div>
  <h2 class="products-hdr" id="nine-inside-50">Nine Inside 50</h2>
  <p class="cat-kicker"><strong>Two skills, nine shots</strong>The goal is to be deadly inside 50 yards, and that comes down to two things: how far the ball goes and how high it flies. This game tests both in about ten minutes.</p>
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <p><strong>Setup.</strong> Put the mat at one end of the yard and a flag or target at three distances: about 10, 20 and 30 yards. Lay a ring around each target. On the weekend, take the same game to the short-game area and stretch the last target to 50 yards.</p>
    <p><strong>Play.</strong> Hit three shots to each target, and call the height before every one: low, middle or high. Use the same wedge for all nine and change the trajectory by moving the ball in your stance: back foot for low, center for middle, front foot for high.</p>
    <p><strong>Score.</strong> One point if the ball flies the height you called. One point if it finishes inside the ring. Nine shots, 18 points possible.</p>
    <p><strong>Keep the number.</strong> Write your score down every time and try to beat it. When you clear 12 regularly, move the targets back.</p>
  </div>
  <div style="overflow-x:auto;max-width:720px;margin:28px auto 0">
  <table class="lp9" style="width:100%;border-collapse:collapse;font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;text-align:center">
    <thead><tr style="background:var(--grass,#2D4A2B);color:#fff"><th style="padding:10px 6px;text-align:left">Shot</th>@@H@@<th style="padding:10px 6px">Total</th></tr></thead>
    <tbody>
      <tr><td style="padding:9px 6px;text-align:left;border-bottom:1px solid rgba(20,20,20,.15)">Yards</td>@@T@@<td style="border-bottom:1px solid rgba(20,20,20,.15)"></td></tr>
      <tr><td style="padding:9px 6px;text-align:left;border-bottom:1px solid rgba(20,20,20,.15)">Height</td>@@W@@<td style="border-bottom:1px solid rgba(20,20,20,.15)"></td></tr>
      <tr><td style="padding:9px 6px;text-align:left;border-bottom:1px solid rgba(20,20,20,.15)">Ball</td>@@P@@<td style="border-bottom:1px solid rgba(20,20,20,.15)"></td></tr>
      <tr><td style="padding:14px 6px;text-align:left;border-bottom:1px solid rgba(20,20,20,.15)">Height pt</td>@@B@@<td style="border-bottom:1px solid rgba(20,20,20,.15)"></td></tr>
      <tr><td style="padding:14px 6px;text-align:left">Ring pt</td>@@B2@@<td>/18</td></tr>
    </tbody>
  </table>
  </div>
</section>
"""
def game_html():
    td = lambda v, b=True: f'<td style="padding:9px 4px;{"border-bottom:1px solid rgba(20,20,20,.15)" if b else ""}">{v}</td>'
    tgt = ["10"]*3 + ["20"]*3 + ["30"]*3
    wd = ["Low","Mid","High"]*3
    par = ["Back","Center","Front"]*3
    g = GAME.replace("@@H@@", "".join(f'<th style="padding:10px 4px">{i}</th>' for i in range(1,10)))
    g = g.replace("@@T@@", "".join(td(t) for t in tgt)).replace("@@W@@", "".join(td(w) for w in wd))
    g = g.replace("@@P@@", "".join(td(p) for p in par)).replace("@@B@@", "".join(td("&nbsp;") for _ in range(9))).replace("@@B2@@", "".join(td("&nbsp;", False) for _ in range(9)))
    return g
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We put a practice mat in the backyard this fall, and it changed how evenings go. Twenty minutes of chips before dinner, a hoodie on once the sun drops behind the fence, nobody keeping score unless somebody wants to. This post is everything that makes that setup better: tools that tell you something, wedges that are a pleasure to hold, clothes you would wear anyway, and a game to keep it from getting boring.</p>
    <p><strong>Start with feedback, then targets.</strong> The Divot Board shows you where the club meets the ground, which is the whole game when you are chipping off a mat. After that, give yourself targets at three distances. EyeLine&rsquo;s rings and a couple of flags are enough to play Nine Inside 50 every night of the week, and that game is built around the two things that make you deadly inside 50 yards: distance control and trajectory control.</p>
    <p><strong>Wedges.</strong> You do not need a new set to chip in the yard, but if one wedge is going to change, this is a good place to try it. Miura&rsquo;s raw C grind will age with you, Bettinardi&rsquo;s bronze HLX looks like the season, and STIX&rsquo;s 60 is the most affordable way to add a lob wedge.</p>
    <p><strong>What to wear.</strong> Six hoodies and six pairs of gym shorts, chosen as much for the photos as the fabric. Fall in the yard means a warm afternoon and a cold evening, often on the same day, so the combination makes sense.</p>
    <p><strong>What is in here.</strong> 25 pieces from @@NB@@ brands, none of them featured on TGI before. All were in stock when we checked on November 18, 2026, at the prices each store shows a US visitor; the Malbon short was last checked on November 16.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>25</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>@@NB@@</span></div>
      <div class="sidebar-detail"><span class="l">The game</span><span>Nine Inside 50, out of 18</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$17.99&ndash;$320</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Divot Board</span></div>
      <div class="hashtags">
        <span class="hashtag">#BackyardGolf</span>
        <span class="hashtag">#ShortGame</span>
        <span class="hashtag">#ChippingPractice</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Ten Minutes Before Dinner</h2>
    <p>The best thing about a backyard setup is how little it asks of you. No tee time, no drive, no range bucket. Walk out, hit nine chips, write down a number and go back inside.</p>
    <p>Do that a few nights a week through the fall and you will feel it the next time you are short-sided on a real course.</p>
    <p>For more short-game kit, see <a href="/drops/around-the-greens-short-game-kit">Around the Greens</a>.</p>
  </div>
</section>
"""
HERO_ALT = "A golfer chipping off a hitting mat into a SKLZ chipping net in a backyard"
FRN = json.loads((ROOT / "research/backyard-chipping/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-AG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-18", "dateModified": "2026-11-18",
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
    for s in SECTIONS: assert len(s[2]) == SECN[s[1]], s[0]
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
    <span>The Kit &middot; Backyard chipping</span><span class="dot"></span>
    <span>25 picks + a game &middot; in stock, checked November 18, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] == "wedges": body += game_html()
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Chippo", "Sunningdale"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\b(worth|genuinely|honestly|straightforward|selling out)\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
