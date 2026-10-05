#!/usr/bin/env python3
"""build-break80.py — The Break 80 Kit, refreshed on the same URL. 2 October 2026.

Lenny: "Let's refresh this page ... redo it and bring it back to the number 1 slot", then "select better
Practice options - Newer tools that are well reviewed", "I liked the tiger candle", "no on K11, let's find a
tempo/speed trainer", "remove K34, K35", "build the post preview". Picks are a first pass from the v3 options
sheet (research/break80/opts.json) for Lenny to swap. The July original is backed up at
research/break80/break-80-kit-july.html.

FACTS: every price read on the maker's own site on 2 Oct 2026 (Garmin from its US page data; books from
publisher pages; Adam Young's book from his site/Amazon listing; Daruma via Daimonya's Amazon storefront).
TRS is a UK store, shown in GBP with its own USD switcher figure. Images: makers' own, softened onto the paper
gradient. The Pro V1 image is the July page's local copy (Titleist blocks downloads).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "break-80-kit"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/break-80-2026"

TITLE = "The Break 80 Kit: 22 Picks to Finally Shoot 79"
DESC = ("A refreshed kit for golfers stuck in the low 80s: strokes-gained tracking, a laser, newer training aids "
        "like HackMotion and the TRS Slider, scoring wedges, the right ball, three books and a Tiger candle.")
H1 = "The Break 80 Kit, Revisited: 22 Things Between You and 79"

# key -> (brand, item, price, url, copy)
P = {
 "arccos": ("Arccos", "Smart Sensors", "$249.99",
   "https://arccosgolf.com/products/smart-sensors",
   "Screw a sensor into the end of every grip and Arccos logs each shot without you touching your phone. After ten rounds it tells you, in strokes gained, whether the 80s are coming from your driver, your irons or your putter. There is also a hardware-only version for $124.99."),
 "garmin-z30": ("Garmin", "Approach Z30 rangefinder", "$449.99",
   "https://www.garmin.com/en-US/p/1411809/",
   "Shoots pins to 400 yards and sends the number to a Garmin watch or the app, with a PlaysLike distance that accounts for slope. It was in our rangefinder roundup this week, and it is the one to buy if you already wear a Garmin."),
 "vc-el3": ("Voice Caddie", "EL3 rangefinder", "$149.99",
   "https://voicecaddie.com/products/el3-laser-rangefinder",
   "At 117 grams the EL3 is the smallest laser we have found, with switchable slope, a magnet for the cart and USB-C charging. Knowing the exact number to the flag is the cheapest stroke in this kit."),
 "rapsodo": ("Rapsodo", "MLM2PRO launch monitor", "$599.99 (was $699.99)",
   "https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator",
   "Carry, spin and launch from your phone, at the range or into a net at home, and it doubles as a simulator. It is on sale for $100 off, and stock yardages are the fastest way to stop coming up short."),
 "hackmotion": ("HackMotion", "Sensor 4", "$345",
   "https://hackmotion.com/hackmotion-sensor-4/",
   "A wrist sensor that buzzes the moment your lead wrist breaks down, which is where most slices and flips start. The new Sensor 4 records at 800 frames a second, and one major training-aid test names it the best for clubface control. Core is $345; Plus, with putting, is $490."),
 "trs-slider": ("TRS Golf", "TRS Slider", "&pound;64.95 (~$90)",
   "https://trsgolf.com/products/trs-slider",
   "Robert Rock's strap connects your trail elbow to your torso so the arm cannot fly away at the top. It was named one major review's top training aid of 2026, and it fixes the over-the-top move that costs most mid-handicaps their good drives."),
 "butterblade": ("RYP Golf", "ButterBlade", "$149",
   "https://rypgolf.com/products/butterblade",
   "A 7-iron with a head about the size of a matchbox. Hit twenty balls with it and your own irons look enormous, which is the point: it trains a centred strike by making anything else obvious."),
 "orange-whip": ("Orange Whip", "Trainer, 47in", "$119.99",
   "https://orangewhipgolf.com/products/the-orange-whip-trainer",
   "A weighted orange ball on a whippy shaft. Rush the transition and it fights you; swing in sequence and it loads and releases on its own. It is the tempo trainer every 2026 roundup agrees on."),
 "rypstick": ("RYP Golf", "Rypstick", "$199",
   "https://rypgolf.com/products/rypstick",
   "A speed stick with three weights and a counterweight, eight setups in all, built for ten minutes, three times a week. More speed means a shorter club into every green, and the bundle with the ButterBlade is $329."),
 "speed-trap": ("EyeLine Golf", "Speed Trap 2.0", "$99.95",
   "https://eyelinegolf.com/products/speed-trap",
   "Four foam rods on a base that gate your swing path. Hit them and you know your path was off; miss them and the ball starts where you aimed. One major training-aid test calls it the best for swing path."),
 "edel-sms": ("Edel Golf", "SMS Pro Wedge", "$180",
   "https://edelgolf.com/products/sms-pro-wedge",
   "Edel built its name on fitting, and the SMS Pro wedge comes in more loft, bounce and grind combinations than almost anything else. Most strokes between 85 and 79 are lost inside 100 yards."),
 "newlevel-spn": ("New Level", "SPN V3 Raw Forged", "$149",
   "https://newlevelgolf.com/products/spnv3-raw-wedges",
   "A raw forged face that rusts in over time for extra bite on partial shots, from a direct-to-consumer brand that sells for a lot less than the tour names."),
 "takomo-sf002": ("Takomo", "Skyforger 002", "$99",
   "https://takomogolf.com/products/skyforger-002-wedges",
   "A forged wedge for under $100, from our guide to buying clubs direct. If you carry three wedges, this is how you afford all three."),
 "pro-v1": ("Titleist", "Pro V1", "$58/dozen",
   "https://www.titleist.com/product/pro-v1/005PV1T.html",
   "The benchmark. Playing one ball every round takes a variable out, and the Pro V1 spins enough around the greens to make your wedge practice count."),
 "snell-mtb": ("Snell", "MTB Black LTD", "$38.99/dozen",
   "https://www.snellgolf.com/products/mtb-black-ltd",
   "Dean Snell designed tour balls for the big brands before selling his own direct. The MTB Black is a limited re-release of the one that made his name, at two-thirds the price of a Pro V1."),
 "vice-pro": ("Vice", "Pro", "$39.99/dozen",
   "https://vicegolf.com/products/vice-golf-pro-white",
   "A urethane tour ball for $40 a dozen from the Munich brand. If you lose two balls a round, this is the one that stops that from costing you."),
 "every-shot-counts": ("Mark Broadie", "Every Shot Counts", "$40 hardcover",
   "https://www.penguinrandomhouse.com/books/309737/every-shot-counts-by-mark-broadie/",
   "The book that invented strokes gained. Read it and you will stop blaming your putting for the shots you lost with your irons."),
 "rotella": ("Bob Rotella", "Golf Is Not a Game of Perfect", "$28.99 hardcover",
   "https://www.simonandschuster.com/books/Golf-is-Not-a-Game-of-Perfect/Bob-Rotella/9780684803647",
   "Rotella coached major winners on the idea that you score with the swing you brought that day. It is the book for the double bogey on the 4th that ruins the next five holes."),
 "practice-manual": ("Adam Young", "The Practice Manual", "$25.99",
   "https://www.adamyounggolf.com/book/",
   "A coach's guide to practising so it actually shows up on the course: variable targets, random practice and why a bucket of 7-irons does very little. It is new to this kit, and the one we would read first."),
 "seamus-horseshoe": ("Seamus Golf", "Lucky Horseshoe ball marker", "$48",
   "https://seamusgolf.com/products/hand-forged-mild-steel-lucky-horshoe-ball-mark",
   "A real horseshoe shape, hand forged from mild steel in Oregon. Mark the putt for 79 with it."),
 "tiger-candle": ("Illuminidol", "Tiger Woods Saint Candle", "$16.95",
   "https://www.illuminidol.com/products/tiger-woods-saint-candle",
   "Back from the first version of this kit, now with a real maker: an 8-inch, 65-hour candle made in Texas. Light it the night before."),
 "daruma": ("Daimonya", "Daruma doll, 4.7in", "$29.99",
   "https://daimonya.com/shop-for-daruma",
   "A good-luck doll from a fifth-generation maker in Takasaki. Paint one eye when you set the goal and the other when you sign for 79, and keep it where you will see it."),
}

SECTIONS = [
 ("Know Your Numbers", "numbers", ["arccos", "garmin-z30", "vc-el3", "rapsodo"],
  "<strong>Four tools &middot; $149.99&ndash;$599.99</strong>You cannot fix what you cannot see. Shot tracking tells you where the strokes go, a laser takes the guessing out of every approach, and a launch monitor tells you how far each club actually carries. Most golfers shooting 84 think it is their putting; the data usually says otherwise."),
 ("Practice That Transfers", "practice", ["hackmotion", "trs-slider", "butterblade", "orange-whip", "rypstick", "speed-trap"],
  "<strong>Six training aids &middot; $99.95&ndash;$345</strong>The newest and best-reviewed tools for the faults that keep you in the 80s: a wrist that breaks down, a trail arm that flies away, a strike that wanders and a transition that rushes. Each one gives you instant feedback, and each one fits in a bag or a garage."),
 ("Scoring Clubs", "wedges", ["edel-sms", "newlevel-spn", "takomo-sf002"],
  "<strong>Three wedges &middot; $99&ndash;$180</strong>Breaking 80 happens inside 100 yards. These three come from the direct-to-consumer brands in our clubs guide, so you get a forged, fitted wedge for less than a tour model."),
 ("The Ball", "ball", ["pro-v1", "snell-mtb", "vice-pro"],
  "<strong>Three balls &middot; $38.99&ndash;$58 a dozen</strong>Pick one and play it every round. Consistency matters more than the brand, and all three are urethane tour balls that spin around the greens."),
 ("The Head Game", "books", ["every-shot-counts", "rotella", "practice-manual"],
  "<strong>Three books &middot; $25.99&ndash;$40</strong>One on where strokes are really lost, one on what to do after a bad hole, and one on how to practise so it sticks."),
 ("The Ritual", "ritual", ["seamus-horseshoe", "tiger-candle", "daruma"],
  "<strong>Three totems &middot; $16.95&ndash;$48</strong>None of these will lower your handicap. All of them will remind you what the goal is."),
]
N = 22

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Breaking 80 is not about one magic club. It is about finding the three or four strokes a round you are giving away and closing them one at a time. For most golfers shooting 82 to 85, those strokes come from bad yardages, a swing fault that shows up under pressure, loose wedges and a double bogey that turns into three.</p>
    <p>When we first built this kit in July, half of it was the usual big-brand gear. This version keeps what works, swaps in the newer training aids that reviewers rate highest this year, and adds three forged wedges from the direct brands we cover. The rituals stay, Tiger candle included. Every price was read on the maker's own site on 2 October 2026.</p>
    <h2 class="products-hdr btk-story-hdr">How to Use It</h2>
    <p>Start with data. Play ten rounds with Arccos or keep your own stats, and let the numbers tell you which section of this kit to buy from. If it is approach play, get a laser and a launch monitor. If it is the long game, pick one training aid and use it three times a week. If it is inside 100 yards, buy the wedge and read the books. Then light the candle.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>22 across six sections</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$16.95&ndash;$599.99</span></div>
      <div class="sidebar-detail"><span class="l">Start with</span><span>Arccos Smart Sensors</span></div>
      <div class="sidebar-detail"><span class="l">New this time</span><span>HackMotion, TRS Slider, ButterBlade, three wedges</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>2 October 2026</span></div>
      <a href="#scorecard" class="sidebar-cta">What 79 looks like &darr;</a>
      <a href="#numbers" class="sidebar-cta" style="margin-top:8px">See the kit &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#Break80</span>
        <span class="hashtag">#GolfTraining</span>
        <span class="hashtag">#GolfImprovement</span>
        <span class="hashtag">#GolfGear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

GUIDE = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">The Guide</div>
  <h2 class="products-hdr" id="scorecard">What 79 Looks Like on the Scorecard</h2>
  <p class="cat-kicker"><strong>No birdies required</strong>On a par-72 course, 79 is seven over. That is eleven pars and seven bogeys, or twelve pars, five bogeys and one double. Add a second double and you are at 81. Breaking 80 is less about good holes than about never having a really bad one.</p>
  <div style="max-width:860px;margin:0 auto 18px;overflow-x:auto">
  <table style="width:100%;border-collapse:collapse;font-family:var(--mono);font-size:12px;text-align:center;min-width:640px">
    <tr style="border-bottom:.5px solid var(--ink)"><th style="text-align:left;padding:6px">Hole</th>""" + "".join(f'<th style="padding:6px">{h}</th>' for h in list(range(1,10))+["Out"]+list(range(10,19))+["In","Tot"]) + """</tr>
    <tr style="border-bottom:.5px solid rgba(0,0,0,.15)"><td style="text-align:left;padding:6px">Par</td>""" + "".join(f'<td style="padding:6px">{x}</td>' for x in [4,4,3,5,4,4,3,4,5,36,4,3,4,5,4,4,3,4,5,36,72]) + """</tr>
    <tr><td style="text-align:left;padding:6px"><strong>79</strong></td>""" + "".join((f'<td style="padding:6px"><span style="display:inline-block;min-width:18px;border:1px solid var(--ink)">{x}</span></td>' if b else f'<td style="padding:6px">{x}</td>') for x,b in [(4,0),(5,1),(3,0),(5,0),(5,1),(4,0),(3,0),(5,1),(5,0),(39,0),(4,0),(4,1),(4,0),(6,1),(4,0),(5,1),(3,0),(5,1),(5,0),(40,0),(79,0)]) + """</tr>
  </table>
  <p style="font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin-top:8px">Eleven pars, seven bogeys (boxed), no birdies, no doubles.</p>
  </div>
  <div style="max-width:760px;margin:0 auto;font-size:16px;line-height:1.75">
    <p><strong>Keep the double off the card.</strong> The gap between an 84 and a 79 is usually three or four doubles, not a shortage of birdies. Every decision below is about turning a possible double into a bogey.</p>
    <p style="margin-top:14px"><strong>Off the tee, avoid recovery shots.</strong> A drive in the fairway bunker, behind a tree or deep in the rough costs nearly as much as a penalty. Play to the safe side of the hole and club down when the fairway gets narrow.</p>
    <p style="margin-top:14px"><strong>From 150 to 200 yards, aim for the green plus one.</strong> This is where doubles pile up for a ten-handicap. Instead of firing at the flag, aim for the middle or the side with the easiest miss, and count a chip or putt for par as a win.</p>
    <p style="margin-top:14px"><strong>Lag it close.</strong> Three-putts are the quiet leak. Practise from 30 feet and beyond until two putts is automatic, and the putts for par will start to drop on their own.</p>
    <p style="margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.6">Adapted from Luke Kerr-Dineen&rsquo;s <a href="https://www.youtube.com/watch?v=SoXqklRpYxI" target="_blank" rel="noopener">The Easiest Way To Break 80</a>, which uses Arccos data and Lou Stagner&rsquo;s research.</p>
  </div>
</section>
"""

FAQ = [
    ("What is the fastest way to break 80?",
     "Find out where you lose strokes before you buy anything. Shot tracking like Arccos, or simple stats on fairways, greens and putts, usually shows that approach shots and wedges cost more than putting. Fix the biggest leak first."),
    ("Do golf training aids actually work?",
     "The good ones do, if you use them regularly. Aids that give instant feedback, like the HackMotion sensor, the TRS Slider or the EyeLine Speed Trap, work best because you feel the fault the moment it happens."),
    ("Do I need a launch monitor to break 80?",
     "No, but knowing exactly how far each club carries helps a lot. A rangefinder plus a session on a launch monitor to set your yardages covers most of the benefit."),
    ("Which golf ball should I use to break 80?",
     "Any urethane tour ball, played every round. The Titleist Pro V1, Snell MTB Black and Vice Pro all fit, from $38.99 to $58 a dozen as of 2 October 2026."),
    ("What does a Daruma doll have to do with golf?",
     "Nothing officially. It is a Japanese good-luck doll: you paint one eye when you set a goal and the other when you reach it. Ours is for the day you sign for 79."),
]

FRN = {k: [f"{IMG}/{k}.jpg"] for k in P}
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
         "url": URL, "image": og, "datePublished": "2026-07-23", "dateModified": "2026-10-02",
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
            {"@type": "ListItem", "position": 3, "name": "The Break 80 Kit", "item": URL}]},
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



def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert (ROOT / FRN[k][0].lstrip("/")).is_file(), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  The Break 80 Kit</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Data, practice, wedges, ball, books and rituals</span><span class="dot"></span>
    <span>22 picks &middot; refreshed 2 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The Break 80 Kit: an EyeLine Speed Trap on the range, a red Daruma doll and a Tiger Woods saint candle" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += GUIDE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
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
