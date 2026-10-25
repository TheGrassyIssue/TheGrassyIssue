#!/usr/bin/env python3
"""build-golf-mental-health.py — Field Note: golf, stress and mental health (23 October 2026). Cloned from build-new-drops-oct23.py.
Lenny: "Let's do a Field note about Stress / Mental Health and golf- how we manage stress and mental health and the game."
Angle (Lenny's pick): personal + practical. His habits (stated 23 Oct 2026): walking with the phone away, range sessions or a solo nine,
early or late rounds. Sedgewood: he almost never keeps score there (memory). Never invent his experiences.
RESEARCH (cited in text): Mayo Clinic pedometer study 2006 (42 golfers, 3 munis, ~11,948 steps per walked 18); Bratman et al. 2015 PNAS
(38 adults, 90-min nature walk lowered rumination + sgPFC activity vs urban walk); Spanish registered golfers survey 2024, pub. 2025
(298 golfers, 73.5% said golf improved their mental health; self-reported); Murray et al. scoping review, BJSM (strong physical evidence,
limited mental-health evidence); Balban et al. 2023 Cell Reports Medicine (114 people, 5 min/day for 28 days; cyclic sighing biggest mood gain).
KIT prices checked 23 Oct 2026 on brands' own stores: Jones Original $185 (products/original-jones-bag-navy-white.js); Seamus scorecard
holder $93 + bamboo tees $15 (seamusgolf.com products.json); Gumtree x Wynn pouch $90; Malbon Long Vacation quarter-zip $228.
Hero + bands: Lenny's own photos. Never "worth". Not medical advice; 988 line in the close.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Golf and Mental Health: How the Game Helps With Stress"
DESC = ("How golf helps with stress: walking the round with the phone away, solo nines, quiet early and late rounds, "
        "what the research says, and a small calm kit.")
H1 = "The Quiet Nine: How I Use Golf to Clear My Head"
BC = "Golf and Mental Health"
SLUG = "golf-stress-mental-health"
IMG = "/images/golf-mental-health"
SHOP = ""
P = {
 "k1": ("Jones Sports Co.", "Original Jones Bag", "$185", "https://www.jonessportsco.com/products/original-jones-bag-navy-white",
   "The 1971 carry bag, built for the walking golfer: water-resistant nylon, one retro strap and three pockets. Light enough that a half-set on your shoulder feels like nothing. Navy and white."),
 "k2": ("Gumtree &times; Wynn", "Valuables Pouch", "$90", "https://www.gumtreegolfandnature.com/shop/p/wynn-golf-club-valuables-pouch",
   "Somewhere for the phone to go that is not your pocket. A woven dobby zip pouch with a brass zip and clip; zip it on the first tee and leave it there."),
 "k3": ("Seamus Golf", "Harris Tweed Scorecard Holder", "$93", "https://seamusgolf.com/products/navy-harris-tweed-scorecard-holder",
   "Navy Harris Tweed lined in toffee leather, with a pencil holder, made in Beaverton, Oregon. Keep the card in your back pocket instead of the score on your phone, or skip the score and use it for notes."),
 "k4": ("Seamus Golf", "Signature Bamboo Tees, 50 Pack", "$15", "https://seamusgolf.com/products/seamus-signature-golf-tees-50-pack-1",
   "A box of thick-shank bamboo tees for the range bucket or the solo nine. The cheapest thing here, and the one you will use most."),
 "k5": ("Malbon &times; Grateful Dead", "Long Vacation Quarter Zip", "$228", "https://malbon.com/products/grateful-dead-long-vacation-quarter-zip-heather-oatmeal",
   "A deep-pile fleece for the first tee time of the morning or the last light of the evening, when the course is quiet and the air has a bite."),
}
SECTIONS = [
 ("A Small Calm Kit", "kit", ["k1","k2","k3","k4","k5"],
  "<strong>5 pieces &middot; $15&ndash;$228 &middot; prices checked October 23, 2026</strong>None of this is required. It is just the stuff that makes the habits above easier: a light bag for walking, a place to put the phone, a card instead of an app, tees for the range and a layer for dawn."),
]
N = 5
PQ = {}
BANDS = {
 "a": ("Where my head goes quiet. ", "Late light on Austin courses, from my phone.",
   [("look-pond","A pond on an Austin golf course at sunset","Late light &middot; Lenny Harrington"),
    ("look-dunes","Rolling green fairway mounds under a big sky","Open ground &middot; Lenny Harrington"),
    ("look-duck","A duck swimming on a golf course pond","Company &middot; Lenny Harrington")]),
 "b": ("Early, late and on my own. ", "The rounds that do the most for me.",
   [("look-tee","A golfer on a tee box looking down the fairway","The walk out &middot; Lenny Harrington"),
    ("look-swing","A golfer mid-swing on a quiet evening","Solo nine &middot; Lenny Harrington"),
    ("look-cart","A golf cart parked under trees at sunset","Sunset &middot; Lenny Harrington")]),
}
KIT_CSS = ""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">Field Notes</div>
    <p>Golf has a reputation for causing stress. The three-putt, the slow group in front, the card you keep checking. Some days it does all of that. But most weeks, for me, it does the opposite: it is the one block of time where my phone is in a bag, my feet are moving and the only problem in front of me is the next shot.</p>
    <p>This isn&rsquo;t a medical piece, and I&rsquo;m not a doctor. It&rsquo;s how I use the game to clear my head, what the research actually says, and a few habits you can try on your next round.</p>
    <p><strong>What the research says, honestly.</strong> The evidence is encouraging but not definitive. A big scoping review of golf and health in the <em>British Journal of Sports Medicine</em> found strong links to physical benefits and much thinner evidence on mental health, and called for more research. Walking is a big part of the physical side: in a Mayo Clinic study of 42 golfers on three municipal courses, players averaged about 12,000 steps for a walked 18. A 2024 survey of 298 registered golfers in Spain found that 73.5% said golf had improved their mental health; that is self-reported, so treat it as a signal, not proof. And a small Stanford study found that a 90-minute walk in a natural setting lowered people&rsquo;s rumination, the loop of repetitive negative thinking, compared with the same walk in a city.</p>
    <p>Put those together and you get something most golfers already feel: a few hours of walking, outside, on grass, with your attention on something simple. That is the part I try to protect.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Short Version</div>
      <div class="sidebar-detail"><span class="l">Walk</span><span>Phone in the bag</span></div>
      <div class="sidebar-detail"><span class="l">Go solo</span><span>A range bucket or nine</span></div>
      <div class="sidebar-detail"><span class="l">Go quiet</span><span>First or last tee times</span></div>
      <div class="sidebar-detail"><span class="l">Breathe</span><span>Two in, one long out</span></div>
      <div class="sidebar-detail"><span class="l">Score</span><span>Optional</span></div>
      <div class="hashtags">
        <span class="hashtag">#FieldNotes</span>
        <span class="hashtag">#WalkTheCourse</span>
        <span class="hashtag">#MentalHealth</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
HABITS = """
<section class="products" style="margin-top:8px;">
  <div class="writeup-body" style="max-width:720px;margin:0 auto;">
    <h2 class="products-hdr" id="walk" style="text-align:left">1. Walk it, phone in the bag</h2>
    <p>The single biggest thing for me is walking and putting the phone away. Not on silent in my pocket, actually zipped in the bag. A cart round with a phone on the dash is a different experience from a walk where the only thing you are checking is the wind. Walking also slows everything down in a good way: you have time between shots to look up, and the round has a rhythm instead of a series of sprints. I wrote more about that rhythm in <a href="/drops/in-defense-of-the-slow-round">In Defense of the Slow Round</a>.</p>
    <p><strong>Try it:</strong> carry a lighter bag, or a half-set, so walking isn&rsquo;t a chore. Zip the phone away on the first tee. If you need it for an emergency, it is still in the bag.</p>

    <h2 class="products-hdr" id="solo" style="text-align:left">2. The solo nine and the range bucket</h2>
    <p>Some of my best resets are alone: a bucket at the range or nine holes with nobody to talk to. No small talk, no score to post, just ball, target, walk. Playing alone takes the performance out of it. You can drop a second ball, hit the shot again, or skip a hole you don&rsquo;t feel like playing. Public courses can often get a single out early or late, when the tee sheet has gaps; our <a href="/field-guide">Austin Golf Guide</a> has the booking rules for the city&rsquo;s munis.</p>
    <p><strong>Try it:</strong> when your head is loud, pick one simple goal for the bucket, like hitting every ball to one flag, and let everything else go.</p>

    <h2 class="products-hdr" id="quiet" style="text-align:left">3. Early and late</h2>
    <p>The first tee times of the morning and the last light of the evening are my favorite times on a course. Fewer people, softer light, nobody waiting on the tee. A sunrise nine before work or a twilight nine after it bookends the day in a way nothing else does for me. Twilight is also usually the cheapest tee time of the day at a lot of public courses.</p>
    <p><strong>Try it:</strong> book the first or last time slot once this week. Bring a layer; it is colder out there than you think.</p>

    <h2 class="products-hdr" id="breathe" style="text-align:left">4. Between shots: breathe</h2>
    <p>Golf gives you a lot of dead time between shots, which is where stress tends to creep in. One technique with real research behind it is the &ldquo;cyclic sigh&rdquo;: two inhales through the nose, the second one topping up the first, then a long, slow exhale through the mouth. In a 2023 Stanford study published in <em>Cell Reports Medicine</em>, people who did five minutes a day of breathing exercises or meditation for 28 days all reported less anxiety, and the cyclic sighing group saw the biggest lift in mood. It was a small study, but the technique costs nothing and fits in the walk between shots.</p>
    <p><strong>Try it:</strong> do two or three cyclic sighs as you walk up to your ball, before you start thinking about the shot.</p>

    <h2 class="products-hdr" id="score" style="text-align:left">5. When golf is the stress</h2>
    <p>Sometimes the game itself is the problem. When that happens, I change the rules. At Sedgewood, the nine-hole club where I grew up playing, I almost never keep score, and those are some of the best rounds I play. Play a scramble with friends, play from a forward tee, play nine instead of eighteen, or just don&rsquo;t write anything down. The course will still be there next week.</p>
  </div>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;">
  <div class="writeup-body" style="max-width:720px;margin:0 auto;">
    <h2 class="products-hdr" id="help" style="text-align:left">If it&rsquo;s more than a bad week</h2>
    <p>Golf is a good way to clear your head. It is not a replacement for help when you need it. If stress, anxiety or a low mood is sticking around or getting heavier, talk to someone: a friend, your doctor or a mental health professional. In the US, you can call or text <strong>988</strong> to reach the 988 Suicide &amp; Crisis Lifeline, any time of day.</p>
  </div>
</section>
"""
KIT = ""
LOOKBOOK = ""
FAQ = [
 ("Is golf good for mental health?", "Many golfers say so, and early research is encouraging: in a 2024 survey of registered golfers in Spain, 73.5% said golf had improved their mental health. But the evidence is mostly self-reported and observational, and a major scoping review found the evidence on golf and mental health limited compared with the physical benefits."),
 ("Does walking a round of golf help with stress?", "Walking is a big part of golf's benefits: a Mayo Clinic study found golfers averaged about 12,000 steps when walking 18 holes on municipal courses. Separate research found that a 90-minute walk in a natural setting reduced rumination compared with an urban walk."),
 ("What breathing technique can I use on the golf course?", "Cyclic sighing: two inhales through the nose followed by a long exhale through the mouth. In a 2023 Stanford study, it produced the largest improvement in mood among the breathing and meditation practices tested."),
 ("What should I do if golf isn't enough to manage stress?", "Talk to someone you trust, your doctor or a mental health professional. In the US, you can call or text 988 to reach the 988 Suicide & Crisis Lifeline at any time."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
_FR = json.loads((ROOT / "research/golf-mental-health/frames.json").read_text())
FRN = {k: [f"{IMG}/{f}" for f in _FR[k]] for k in P}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
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
         "url": URL, "image": og, "datePublished": "2026-10-23", "dateModified": "2026-10-23",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
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
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Grassy Issue &middot; Field Notes</span><span class="dot"></span>
    <span>Not medical advice &middot; October 23, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer walking with a carry bag on an Austin course at sunset" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += band("a")
    body += HABITS
    body += band("b")
    o, n = section(SECTIONS[0], 1); body += o
    body += CLOSE
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + KIT_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Climber", "Woodgrain", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
