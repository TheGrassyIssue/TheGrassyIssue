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
DESC = ("Why the slow round is the best round on an Austin muni: the birds and wildflowers to look for, how to "
        "switch off and let bad shots go, and how to get a real conversation going with whoever you are paired with.")
H1 = "In Defense of the Slow Round"

OPEN = [
 "The slow round is the best round you can play on an Austin muni, and the people complaining about pace are missing most of it. Five hours on a public course in October is five hours outside with nothing to answer, in the best light Texas gets all year, with three people you either know well or are about to. The score is the least interesting thing that happens.",
 "To be clear about what we are defending: slow does not mean holding up the group behind you. Wave them through, play ready golf when it is your turn, and keep up with the pace of the course. Slow is about what you do with the waiting. A backed-up tee box is a place to look up, breathe and talk, and most golfers spend it checking email.",
 "Henry David Thoreau wrote an essay about this in 1862 and called it <em>Walking</em>. He said he could not stay healthy &ldquo;unless I spend four hours a day at least&mdash;and it is commonly more than that&mdash;sauntering through the woods and over the hills and fields, absolutely free from all worldly engagements.&rdquo; Four hours, sauntering, over hills and fields. He described a round of golf without ever playing one. This is our case for taking the long way round, in three parts: what to look at, how to quiet your head, and who you are talking to.",
]

PARTS = [
 dict(n="Part I", h2="Flora and Fauna of Central Texas", anchor="flora-and-fauna",
  kicker="<strong>What to look for</strong>An Austin muni in autumn sits right under one of the busiest migration routes in North America.",
  band=[("band-1", "A duck swimming on rippled water at the Jimmy Clay and Roy Kizer golf complex", "Jimmy Clay and Kizer &middot; October"),
        ("band-2", "Live oaks reflected in a pond at sunset at Jimmy Clay Golf Course", "Jimmy Clay &middot; October"),
        ("band-3", "Oaks and a bunker in late light at Grey Rock Golf Club", "Grey Rock")],
  prose=[
   "Austin sits on the Central Flyway, the main north-south route for birds crossing the middle of the continent, and October is the peak. The city&rsquo;s golf courses happen to be some of the best open ground in town to watch it: big skies, ponds, creek corridors and edges of oak and juniper that nobody mows.",
   "Start by looking up, and listening. The Travis Audubon Society&rsquo;s October forecast tells birders to listen for Sandhill Cranes and Franklin&rsquo;s Gulls passing overhead in flocks, and notes that cranes are loud enough to hear long before you find them. On a day with a north wind, watch for American White Pelicans, huge and silent, with black along the back edge of their wings. Very rarely a Whooping Crane travels with the Sandhills; Travis County&rsquo;s past sightings cluster in the third and fourth weeks of October.",
   "Closer to the ground, Scissor-tailed Flycatchers gather in noticeable groups on the wires before they leave for the winter, the long forked tails easy to spot from the fairway. Ducks start arriving on the ponds, and the pond at the eastern edge of Mueller, across Manor Road from Morris Williams, is one of the best places in Austin to see them close up; Travis Audubon has counted eight species there in past Octobers. Roy Kizer, with 35 acres of lakes and 22 acres of wetlands, is the city&rsquo;s best birding round, and the duck in our photo was working a pond at the Jimmy Clay and Kizer complex on a Monday evening this month. Then there is the bird that never leaves: the Northern Mockingbird, the state bird since 1927, doing impressions from the top of the nearest light pole.",
   "Roy Bedichek, the Austin naturalist who wrote <em>Adventures with a Texas Naturalist</em> in 1947, loved mockingbirds and refused to be impressed by their act. &ldquo;I have never been fooled more than momentarily by the so-called mimicry of the mockingbird,&rdquo; he wrote. Spend a slow round listening to one and decide for yourself.",
   "October is also monarch month. The butterflies cross Central Texas on their way to Mexico, and local forecasters put the peak in the last two weeks of October and the first two of November. They feed on the fall wildflowers along the rough: Maximilian sunflower, which blooms from August to November and grows up to six feet tall, plus Gregg&rsquo;s mistflower, frostweed, goldenrod and fall aster. Come back in late March and April for bluebonnets and Indian paintbrush.",
   "The trees are the course architecture nobody credits. Live oaks spread low and wide over the fairways, and cedar elm and Ashe juniper, which Texans call cedar, line the edges. That juniper matters: the endangered Golden-cheeked Warbler nests only in Central Texas and builds its nest from strips of Ashe juniper bark, arriving in March and leaving by early August. You will not see one in October, but the trees you are hitting out of are the reason it exists. Add the white-tailed deer, armadillos and red-eared sliders that come out at dusk, and a four-and-a-half-hour round starts to look short.",
  ],
  pq=("Some of the external beauty is always in sight, enough to keep every fibre of us tingling.", "John Muir, <em>My First Summer in the Sierra</em>, 1911")),
 dict(n="Part II", h2="Meditation and Mindfulness", anchor="mindfulness",
  kicker="<strong>How to switch off</strong>A slow round is only frustrating if you are trying to be somewhere else.",
  band=[("band-4", "A golfer watching his tee shot under a layered evening sky at Jimmy Clay", "Jimmy Clay &middot; tee shot"),
        ("band-5", "The low sun flaring over a green and flag at Jimmy Clay", "Jimmy Clay &middot; 7:47 PM"),
        ("band-6", "A Texas flag on a flagstick at sunset on an Austin municipal course", "The last flag")],
  prose=[
   "Thoreau worried about the same thing every golfer coming straight from the office knows: getting to the woods with your head still back in town. In <em>Walking</em> he admitted that the thought of some work would run through his mind and he would not be where his body was. Most of us play the first three holes still in the meeting we just left. The fix is to arrive on purpose.",
   "Leave work in the car. Get there twenty minutes early, put the phone on silent and zip it into the bag, and hit a few putts without counting them. On the first tee, before you swing, stop and name three things you can hear. It sounds soft. It works, because it moves your attention from your head to the place you are standing.",
   "Then use the waiting. A backed-up par three is a free five minutes, so take it as one. Breathe in for four counts, hold for four, out for four, hold for four, and look at something that is not a phone: the tree line, the light on the water, whatever is circling overhead. Walk the course when you can. The time between shots is where the round actually happens, and a cart makes it disappear.",
   "Bad shots are where slow rounds go sour, so give each one a short life. Feel it fully for ten paces after you hit it, then let it go before you reach the ball. Say one useful thing about it, like &ldquo;tempo&rdquo; or &ldquo;committed to the wrong club,&rdquo; and nothing else. The ball does not know it was a bad shot. The next one is a new problem, and on a slow day you have plenty of time to look at it.",
   "Finally, stop doing arithmetic. Try one round a month without writing down a score, or play the back nine with one club and a putter. Nothing loosens a mind like taking away the thing it was keeping track of. Thich Nhat Hanh, who wrote more clearly than anyone about walking meditation, told readers to walk as if they were kissing the earth with their feet. On a muni at sunset, that is not a hard instruction to follow.",
  ],
  pq=("I am alarmed when it happens that I have walked a mile into the woods bodily, without getting there in spirit.", "Henry David Thoreau, <em>Walking</em>, 1862")),
 dict(n="Part III", h2="Conversations", anchor="conversations",
  kicker="<strong>Who you are talking to</strong>Austin has always had a rock where people sat for hours and talked.",
  band=[("band-7", "A golf cart parked on the fairway at Morris Williams at sunset", "Morris Williams &middot; May"),
        ("band-8", "A golfer mid-swing on an evening fairway", "Mid-swing"),
        ("band-9", "The sky turning blue and pink over oaks at Lions Municipal at dusk", "Lions &middot; dusk")],
  prose=[
   "On summer afternoons in the 1940s and 50s, three of the most important writers in Texas met at Barton Springs to swim and talk: the naturalist Roy Bedichek, the folklorist J. Frank Dobie and the historian Walter Prescott Webb. Bedichek named their spot Philosophers&rsquo; Rock. A bronze of the three of them, mid-conversation and in their swim trunks, has sat by the pool since 1994, a short walk from Butler Pitch &amp; Putt and a few minutes&rsquo; drive from Lions. A slow round is the closest thing most of us have to that rock: hours outdoors with nowhere else to be and nothing to do but talk.",
   "The trick is to get past the first two holes of handicaps and where you work. Start with the course, because everyone has an opinion about it: &ldquo;Where do you usually play?&rdquo; becomes &ldquo;What&rsquo;s the best round you&rsquo;ve ever played?&rdquo; and then &ldquo;Who taught you?&rdquo; That last one is where people start telling you about their dad.",
   "From there, ask questions that need a story rather than a number. What did you want to be when you were a kid? What&rsquo;s the best thing you&rsquo;ve eaten in Austin this year? Where would you go if you had a week and no budget? What are you reading? Which course would you play if you only had one round left? Then listen, and ask a second question about the answer. The second question is where conversations are made.",
   "Being paired with strangers is the muni&rsquo;s best feature, not its worst. Introduce yourself on the first tee with your first name and one easy fact. Compliment a good shot by name, because people remember who noticed. Hold back on swing tips unless somebody asks. Find a shared enemy, like the wind at Kizer or the green on a hole that never breaks the way it looks. By the turn, you are not strangers. By the eighteenth, you are trading numbers or making plans for next week.",
   "And do not let it end on the last green. Morris Williams has rocking chairs on its porch looking out over the whole course, and most munis have a patio, a cooler and a sunset still going. Stay for one. Bedichek once wrote that mockingbirds &ldquo;have qualities we admire and talk about.&rdquo; Good playing partners are the same.",
  ],
  pq=None),
]

CLOSE = [
 "Nobody remembers the round that took three hours and fifty minutes. They remember the cranes going over, the heron on the pond, the shot they let go of, and the guy they met on the fourth tee who turned out to be from their hometown. The slow round gives you room for all of that, if you stop fighting it.",
 "So book the late tee time, walk if you can, leave the phone in the bag and let the group behind you through. Look up at the sky on the back nine and talk to whoever is standing next to you. Thoreau had the line for it, in <em>Walden</em>: &ldquo;I love a broad margin to my life.&rdquo; A slow round is a broad margin with a scorecard nobody has to read.",
]
FINAL_PQ = ("I love a broad margin to my life.", "Henry David Thoreau, <em>Walden</em>, 1854")

COURSES = [
 ("MW", "Morris Williams", "Manor Road &middot; opened 1964", "morris-williams-course",
  "Leon Howard laid out Austin&rsquo;s third public course in 1964 over rolling ground with raised, contoured greens, and it reopened in 2013 after a renovation and a new pro shop. The porch has rocking chairs that look over the whole course. In October, walk across Manor Road afterwards: the pond at the edge of Mueller is one of the best places in town to watch the ducks arrive."),
 ("JC", "Jimmy Clay", "Southeast Austin &middot; opened 1974", "jimmy-clay-course",
  "Joe Finger&rsquo;s 1974 design plays 6,918 yards of tree-lined fairways with Williamson Creek running around it, and three holes were rebuilt in 2007 around a pond and an island green. This is the evening course, when the low sun comes through the oaks and the creek corridor fills with birds."),
 ("KZ", "Roy Kizer", "Southeast Austin &middot; opened 1994", "roy-kizer-course",
  "Randy Russell built Kizer in 1994 as a links-style course over about 200 acres, with 35 acres of lakes and 22 acres of wetlands that the city says are home to migratory waterfowl. It is named for the Lions Municipal superintendent from 1937 to 1973. Open, windy and wild at the edges, it is the best birding round in Austin."),
]
FRAMES = {"MW": ["mw-1"], "JC": ["jc-1"], "KZ": ["kz-1"]}
ALTS = {"MW": "A rolling fairway at Morris Williams Golf Course under a wide sky",
        "JC": "A red flag on a green beside a pond at Jimmy Clay Golf Course",
        "KZ": "Rolling links-style mounds at sunset at Roy Kizer Golf Course"}

FAQ = [
 ("What birds can you see on Austin golf courses in October?",
  "October is peak migration on the Central Flyway. Listen for Sandhill Cranes and Franklin's Gulls overhead, watch for American White Pelicans on north-wind days and flocks of Scissor-tailed Flycatchers getting ready to leave, and check the ponds for arriving ducks. Roy Kizer, with 35 acres of lakes and 22 acres of wetlands, is the best course for it."),
 ("What wildflowers bloom on Central Texas golf courses in the fall?",
  "Maximilian sunflower blooms from August to November, along with Gregg's mistflower, frostweed, goldenrod and fall aster. They feed the monarch butterflies that cross Central Texas from late September, peaking in late October and early November. Bluebonnets and Indian paintbrush come in late March and April."),
 ("How do you stay calm during a slow round of golf?",
  "Arrive early and leave the phone in the bag, use the waits to breathe and look around instead of checking email, walk if you can, and give each bad shot about ten paces before you let it go. Wave faster groups through so nobody is waiting on you."),
 ("How do you start a conversation with strangers on the golf course?",
  "Start with the course, then ask questions that need a story instead of a number: the best round they have played, who taught them, what they are reading, where they would go with a free week. Compliment good shots by name and hold back on swing tips unless asked."),
]

GRID_CSS = ('<style>/*TGI-SLOW*/.products-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}'
            '@media(max-width:820px){.products-grid[data-n="3"]{grid-template-columns:1fr}}'
            '.slow-part{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase}</style>\n')


def gallery_card(k, idx):
    code, name, meta, slug, copy = next(c for c in COURSES if c[0] == k)
    fr = FRAMES[k]
    imgs = "".join(f'<div class="pg-frame"><img src="{IMG}/{f}.jpg" alt="{H.escape(ALTS[k])}" loading="lazy" /></div>' for f in fr)
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{meta}</div>'
            f'<div class="product-name">{name}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{GA}{slug}" target="_blank" rel="noopener" class="product-link">Book a tee time &#8599;</a></div></div>')


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
    out += prose(p["prose"])
    if p["pq"]:
        out += pq(*p["pq"])
    return out


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-06", "dateModified": "2026-10-06",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
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


TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
{paras}
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Slow Round</div>
      <div class="sidebar-detail"><span class="l">Part I</span><span><a href="#flora-and-fauna">Flora and Fauna</a></span></div>
      <div class="sidebar-detail"><span class="l">Part II</span><span><a href="#mindfulness">Mindfulness</a></span></div>
      <div class="sidebar-detail"><span class="l">Part III</span><span><a href="#conversations">Conversations</a></span></div>
      <div class="sidebar-detail"><span class="l">Best month</span><span>October, peak migration</span></div>
      <div class="sidebar-detail"><span class="l">Best course</span><span>Roy Kizer, for the birds</span></div>
      <div class="sidebar-detail"><span class="l">Reading</span><span>Thoreau, <em>Walking</em></span></div>
      <a href="#where-to-play" class="sidebar-cta">Where to play it slow &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#SlowGolf</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  </aside>
</section>
"""


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
    <span>Three parts &middot; October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer walking down the fairway at Morris Williams with his carry bag as the sun sets" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("{paras}", "\n".join(f"    <p>{p}</p>" for p in OPEN))
    for p in PARTS:
        body += part(p)
    body += prose(CLOSE)
    cards = "\n".join(gallery_card(k, i + 1) for i, k in enumerate(["MW", "JC", "KZ"]))
    body += (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">Three courses</div>\n'
             f'  <h2 class="products-hdr" id="where-to-play">Where to Play It Slow</h2>\n'
             f'  <p class="cat-kicker"><strong>City courses &middot; GolfATX</strong>Three Austin munis built for a long evening, all bookable through the city.</p>\n'
             f'    <div class="products-grid" data-n="3">\n{cards}\n    </div>\n</section>\n')
    body += faq_html()
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
