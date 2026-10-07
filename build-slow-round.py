#!/usr/bin/env python3
"""build-slow-round.py — In Defense of the Slow Round. 6 October 2026.

Lenny: "Let's do a post called 'In defense of the slow round' Three parts; Flora and Fauna of Central Texas,
Meditation and mindfulness and conversations. Pull images from sunsets of the muni courses and some good quotes."
His answers: TGI "we" voice; long essay + photo bands; quotes from nature writers and mindfulness; his own photos
plus sunsets already on the site. Then: flora and fauna from our own research (what to look for, migrants, flowers);
mindfulness = how to handle a slow round, decompress from work, leave bad shots behind; conversations = how to start
one, get personal, questions to ask, playing with strangers. Liked: Philosophers' Rock, Thoreau's Walking, John Muir.

FACTS: GolfATX course pages (austintexas.gov); Travis Audubon "October Bird Forecast"; USFWS and Audubon on the
golden-cheeked warbler; KXAN on monarch timing; Lady Bird Johnson Wildflower Center on fall nectar plants;
Philosophers' Rock (Frommer's, Humanities Texas, Texas Monthly).
QUOTES, verbatim: Thoreau, Walking (1862) and Walden (1854), checked against the Project Gutenberg texts; Muir,
My First Summer in the Sierra (1911), Gutenberg; Bedichek, Adventures with a Texas Naturalist (1947), as quoted in
Texas Co-op Power (Aug 2018).
PHOTOS: Lenny's own (research/slow-round/own, from ~/Desktop/Golf Pics) and sunsets already on the site.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "in-defense-of-the-slow-round"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/slow-round"
GA = "https://www.austintexas.gov/department/"

TITLE = "In Defense of the Slow Round"
DESC = ("The slow round is miserable and you can't fix it. What you can control on an Austin muni: what you look at, "
        "how you handle the wait and the bad shots, and who you talk to.")
H1 = "In Defense of the Slow Round"

OPEN = [
 "Let&rsquo;s not pretend. The slow round is miserable. You find a swing on the range, get to the fourth tee at Jimmy Clay, and there are two groups waiting and a fivesome in the fairway. By the turn your tempo is gone and your back is stiff. It jams up your game, and anyone who says they don&rsquo;t mind is lying.",
 "You can&rsquo;t speed up the group in front. You can&rsquo;t move the wind at Kizer, fix the greens in August or make the week ahead any lighter. Most of what happens to us, on the course and off it, is out of our hands. What is left is small: where you look, how you breathe, what you do with a bad shot and whether you talk to the person next to you. That&rsquo;s the whole case.",
 "Thoreau wrote in <em>Walking</em> in 1862 that he could not stay sane &ldquo;unless I spend four hours a day at least&mdash;and it is commonly more than that&mdash;sauntering through the woods and over the hills and fields, absolutely free from all worldly engagements.&rdquo; He never played golf. On a slow Saturday at a muni, you will get your four hours whether you want them or not. You might as well saunter.",
]

PARTS = [
 dict(n="Part I", h2="Flora and Fauna of Central Texas", anchor="flora-and-fauna",
  kicker="<strong>Look up</strong>When you can&rsquo;t move forward, look around.",
  band=[("band-1", "A duck swimming on rippled water at the Jimmy Clay and Roy Kizer golf complex", "Jimmy Clay and Kizer &middot; October"),
        ("band-2", "Live oaks reflected in a pond at sunset at Jimmy Clay Golf Course", "Jimmy Clay &middot; October"),
        ("band-3", "Oaks and a bunker in late light at Grey Rock Golf Club", "Grey Rock")],
  blocks=[
   "Austin sits under the Central Flyway, the main bird route through the middle of the continent, and October is rush hour. Our munis are some of the best open ground in town to watch it: big sky, ponds and creeks, and edges nobody mows.",
   ("il-crane", "Audubon&rsquo;s Hooping Crane, engraved by Robert Havell, 1834", "right"),
   "Listen first. Sandhill Cranes and Franklin&rsquo;s Gulls pass over in flocks this month, and the cranes are loud enough that you hear them long before you find them. On a north-wind day, look for American White Pelicans, huge and silent, black along the back of the wings. If you are very lucky, a Whooping Crane travels with the Sandhills; Travis County&rsquo;s sightings cluster in the third and fourth weeks of October.",
   ("il-flycatcher", "Audubon&rsquo;s flycatchers, 1837. The swallow-tailed is our scissor-tail", "left"),
   "On the wires over the fairway, Scissor-tailed Flycatchers gather in groups before they head south for the winter. You will know them by the tail, twice the length of the bird. Then the ducks arrive. Roy Kizer has 35 acres of lakes and 22 of wetlands, and the duck in our photo was working a pond on the Jimmy Clay and Kizer complex on a Monday evening this month. After a round at Morris Williams, walk across Manor Road to the pond at the edge of Mueller; Travis Audubon has counted eight duck species there in past Octobers.",
   ("il-redtail", "Red-tailed Hawk, New York Forest, Fish and Game Commission report, 1902", "right"),
   "Some birds never leave. Red-tailed Hawks hunt the open rough all year, sitting on a light pole or a dead branch until something moves in the grass, and we watched one work the edges at Jimmy Clay. Watching one beats checking your phone on any tee. The other year-round local is the Northern Mockingbird, the state bird since 1927, doing impressions from the top of the nearest pole. Roy Bedichek, Austin&rsquo;s great naturalist, loved them and refused to be impressed: &ldquo;I have never been fooled more than momentarily by the so-called mimicry of the mockingbird.&rdquo;",
   ("il-mallard", "Audubon&rsquo;s Mallard Duck, 1834", "left"),
   "Look down, too. Monarchs cross Central Texas on their way to Mexico, peaking in late October and early November, and they feed in the rough on Maximilian sunflowers up to six feet tall, Gregg&rsquo;s mistflower, frostweed and goldenrod. The trees framing every hole are live oak, cedar elm and Ashe juniper. That juniper is why the endangered Golden-cheeked Warbler exists: it nests only in Central Texas, builds with strips of juniper bark and leaves by early August. You are hitting out of its home.",
  ],
  pq=("Some of the external beauty is always in sight, enough to keep every fibre of us tingling.", "John Muir, <em>My First Summer in the Sierra</em>, 1911")),
 dict(n="Part II", h2="Meditation and Mindfulness", anchor="mindfulness",
  kicker="<strong>What you can control</strong>You decide where your attention goes, how you breathe and what happens after a bad shot.",
  band=[("band-4", "A golfer watching his tee shot under a layered evening sky at Jimmy Clay", "Jimmy Clay &middot; tee shot"),
        ("band-5", "The low sun flaring over a green and flag at Jimmy Clay", "Jimmy Clay &middot; 7:47 PM"),
        ("band-6", "A Texas flag on a flagstick at sunset on an Austin municipal course", "The last flag")],
  blocks=[
   "Thoreau knew the problem. In <em>Walking</em> he admits that some days the thought of work runs through his head and he is not where his body is. Most of us play the first three holes still in the meeting we just left.",
   "So leave work in the car. Get there twenty minutes early, zip the phone into the bag and roll a few putts without counting. On the first tee, before you swing, name three things you can hear. It moves you out of your head and onto the grass.",
   ("il-heron", "Audubon&rsquo;s Great Blue Heron, 1834", "right"),
   "Then use the wait. A backed-up par three is five free minutes, so take them. Breathe in for four counts, hold for four, out for four, hold for four. Watch something that is not a screen. A Great Blue Heron will stand in the shallows at Kizer without moving for longer than you will wait on any tee, and it does not look frustrated.",
   "Bad shots get ten paces. Feel it, say one useful word about it, like &ldquo;tempo,&rdquo; and let it go before you reach the ball. The ball does not know it was a bad shot, and the next one is a new problem. Once a month, leave the scorecard in the cart. Nothing quiets a head faster than taking away the thing it was counting.",
  ],
  pq=("I am alarmed when it happens that I have walked a mile into the woods bodily, without getting there in spirit.", "Henry David Thoreau, <em>Walking</em>, 1862")),
 dict(n="Part III", h2="Conversations", anchor="conversations",
  kicker="<strong>Who is next to you</strong>The one part of a slow round that gets better the slower it goes.",
  band=[("band-7", "A golf cart parked on the fairway at Morris Williams at sunset", "Morris Williams &middot; May"),
        ("band-8", "A golfer mid-swing on an evening fairway", "Mid-swing"),
        ("band-9", "The sky turning blue and pink over oaks at Lions Municipal at dusk", "Lions &middot; dusk")],
  blocks=[
   "In the 1940s and &rsquo;50s, three of the best writers in Texas spent summer afternoons at Barton Springs doing nothing but talking: the naturalist Roy Bedichek, the folklorist J. Frank Dobie and the historian Walter Prescott Webb. Bedichek named their spot Philosophers&rsquo; Rock, and a bronze of the three, mid-argument in their swim trunks, has sat by the pool since 1994. A slow round is the closest most of us get to that rock.",
   ("photo", "philosophers-rock", "Philosophers&rsquo; Rock at Barton Springs: Glenna Goodacre&rsquo;s 1994 bronze of Bedichek, Dobie and Webb, mid-conversation. Photo: The Grassy Issue", "The Philosophers\u2019 Rock bronze of Roy Bedichek, J. Frank Dobie and Walter Prescott Webb talking at Barton Springs"),
   "Get past handicaps and jobs by the third hole. Start with the course, because everyone has an opinion: &ldquo;Where do you usually play?&rdquo; leads to &ldquo;What&rsquo;s the best round you&rsquo;ve ever had?&rdquo; and then &ldquo;Who taught you?&rdquo; That is usually where somebody starts talking about their dad.",
   "Ask questions that need a story, not a number. A few that work on any tee:",
   ("ul", ["Who taught you to play?", "What&rsquo;s the best round you&rsquo;ve ever had, and where?", "One round left anywhere in the world. Which course?", "What did you want to be when you were a kid?", "Best thing you&rsquo;ve eaten in Austin this year?", "What are you reading, watching or listening to right now?", "Free week, no budget. Where are you going?", "If you could only keep one club, which one?", "What got you into golf, and what keeps you coming back?"]),
   "Then ask a second question about the answer. That is where conversations start.",
   "Strangers are the muni&rsquo;s best feature. First name and one easy fact on the first tee. Name the good shots, keep the swing tips to yourself, and find a common enemy, like the wind at Kizer or a green that never breaks the way it looks. Strangers on the first tee are usually swapping numbers by the eighteenth.",
   ("il-mockingbird", "Audubon&rsquo;s Mocking Bird, 1827", "right"),
   "And don&rsquo;t let it end on the last green. Morris Williams has rocking chairs on a porch that looks over the whole course. Sit in one. Bedichek said mockingbirds &ldquo;have qualities we admire and talk about.&rdquo; So do good playing partners.",
  ],
  pq=None),
]

CLOSE = [
 "The slow round will still be slow next weekend. The group ahead will still be looking for a ball in the creek. You don&rsquo;t control any of it, and you never did.",
 "You control the rest. Look up on the back nine. Breathe on the tee. Give the bad shot ten paces. Talk to the person next to you. Thoreau had the line in <em>Walden</em>: &ldquo;I love a broad margin to my life.&rdquo; A slow round is a broad margin. It just takes some getting used to.",
]
GRID_CSS = ('<style>/*TGI-SLOW*/.products-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}'
            '@media(max-width:820px){.products-grid[data-n="3"]{grid-template-columns:1fr}}'
            'section.products.slow-wrap[data-btk] .writeup-body{text-align:left!important}section.products.slow-wrap[data-btk] .writeup-body p{margin:0 0 16px}'
            '.slow-illus{width:190px;margin:6px 0 14px}.slow-illus.right{float:right;margin-left:26px}.slow-illus.left{float:left;margin-right:26px}.slow-illus.wide{width:250px}'
            '.slow-illus img{width:100%;display:block;box-shadow:0 1px 8px rgba(20,20,20,.12)}.slow-illus figcaption{margin-top:8px;line-height:1.45;text-align:left;font-size:8.5px}'
            '.slow-photo{clear:both;margin:26px 0 30px}.slow-photo img{width:100%;display:block}.slow-photo figcaption{margin-top:10px;text-align:left}'
            '.slow-qs{margin:14px 0 18px 1.2em;padding:0;list-style:disc}.slow-qs li{margin:6px 0;line-height:1.55}'
            '@media(max-width:640px){.slow-illus,.slow-illus.wide{width:140px}.slow-illus.right{margin-left:16px}.slow-illus.left{margin-right:16px}}</style>\n')


def pq(q, who):
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def prose(paras):
    ps = "\n".join(f"    <p>{p}</p>" for p in paras)
    return f'\n<section class="products" data-btk="coda" style="margin-top:8px;">\n  <div class="writeup-body">\n{ps}\n  </div>\n</section>\n'


def part(p):
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in p["band"])
    out = (f'\n<section class="products" style="margin-top:8px;">\n'
           f'  <div class="drop-tag grass">{p["n"]}</div>\n'
           f'  <h2 class="products-hdr" id="{p["anchor"]}">{p["h2"]}</h2>\n'
           f'  <p class="cat-kicker">{p["kicker"]}</p>\n'
           f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')
    inner = []
    for blk in p["blocks"]:
        if isinstance(blk, tuple):
            if blk[0] == "photo":
                _, f, cap, alt = blk
                inner.append(f'    <figure class="slow-photo"><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>')
                continue
            if blk[0] == "ul":
                lis = "".join(f"<li>{x}</li>" for x in blk[1])
                inner.append(f'    <ul class="slow-qs">{lis}</ul>')
                continue
            f, cap, side = blk
            credit = "" if f == "il-redtail" else ". National Gallery of Art, open access"
            alt = re.sub(r"&[a-z]+;", "'", cap.split(",")[0])
            cls = f"slow-illus {side}" + (" wide" if f == "il-mallard" else "")
            inner.append(f'    <figure class="{cls}"><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" />'
                         f'<figcaption class="ig-cap">{cap}{credit}</figcaption></figure>')
        else:
            inner.append(f"    <p>{blk}</p>")
    out += f'\n<section class="products slow-wrap" data-btk="coda" style="margin-top:8px;">\n  <div class="writeup-body">\n' + "\n".join(inner) + '\n    <div style="clear:both"></div>' + '\n  </div>\n</section>\n'
    if p["pq"]:
        out += pq(*p["pq"])
    return out


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-06", "dateModified": "2026-10-06",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "The Slow Round", "item": URL}]},
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




def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  The Slow Round</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Birds, breathing and conversation on Austin&rsquo;s munis</span><span class="dot"></span>
    <span>A story in three parts</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer walking down the fairway at Morris Williams with his carry bag as the sun sets" fetchpriority="high" /></div></div>
"""
    body += prose(OPEN)
    for p in PARTS:
        body += part(p)
    body += prose(CLOSE)
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    words = len(re.sub(r"<[^>]+>", " ", above).split())
    print(f"  wrote {OUT.relative_to(ROOT)} ({words} words above the fold-out)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
