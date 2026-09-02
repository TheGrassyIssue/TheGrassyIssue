#!/usr/bin/env python3
"""build-ny-trip.py — Field Notes: a week of New York golf.

Lenny's trip, Aug 25 - Sep 1 2026. Three courses, in order:
  Sedgewood Club (Carmel, NY)      — Aug 25, his parents' club, where he grew up
  The Links at Union Vale          — Aug 26, shot 84
  Bethpage Black                   — Sep 1, cancellation grab, rain delay, par on 1

All experience, scores, opinions and the dog are Lenny's own, given verbatim in
conversation on 2026-09-02. Course facts (architects, yardage, dates, fees,
booking rules) are sourced separately — see research/ny-trip-dossier.md.
Photos are Lenny's, shot on iPhone, EXIF timestamps used to order the days.

The trip also took in the Gumtree Golf & Nature Club studio in Greenpoint,
Brooklyn on Aug 29 (open studio hours, confirmed on their site). Lenny talked
with founder Karsten Jurkschat. No quotes are attributed to Karsten anywhere on
the page — the conversation was not recorded, so the section reports the visit
and the room, not his words.

While building it: the brand index had Gumtree filed under loc "Australia" /
region "australia", contradicting our own Nature Club post ("runs out of
Brooklyn"). Corrected to Brooklyn, NY / usa. Jurkschat is Melbourne-born and
moved to New York in 2017, which is where the confusion came from.

Chassis cloned from drops/lions-municipal-golf-course-austin.html (the Field
Notes deep-dive layout: 21:9 hero, pull-quote, ig-grid photo rows).
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
ch = open(os.path.join(S, "drops", "lions-municipal-golf-course-austin.html"), encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

URL         = "https://thegrassyissue.com/drops/new-york-golf-trip-sedgewood-union-vale-bethpage-black"
TITLE       = "A Week of New York Golf &mdash; Sedgewood, Union Vale and Bethpage Black"
TITLE_PLAIN = "A Week of New York Golf — Sedgewood, Union Vale and Bethpage Black"
DESC        = ("Three New York courses in a week: a private nine in the Hudson Valley where the dog walks "
               "the green, a links-style public gem in Dutchess County, and Bethpage Black on a "
               "cancellation after a rain delay.")
IMG = "/images/ny-trip"


def fig(slug, alt, cap):
    return ('<figure><img src="%s/%s.jpg" alt="%s" loading="lazy" />'
            '<figcaption class="ig-cap">%s</figcaption></figure>' % (IMG, slug, alt, cap))


sedgewood_photos = ('<div class="ig-grid" style="grid-template-columns:repeat(2,1fr);max-width:900px;">\n    '
    + fig("sedgewood-stella", "A golden mixed lab sitting on the green at the Sedgewood Club while a golfer putts",
          "Stella, holding the green")
    + "\n    "
    + fig("sedgewood-tee", "A golfer at the top of the backswing on a tree-framed tee at the Sedgewood Club",
          "Nine holes, no tee sheet")
    + "\n  </div>")

unionvale_photos = ('<div class="ig-grid">\n    '
    + fig("unionvale-bunker", "A wide sand bunker cut into rolling fescue against open sky at The Links at Union Vale",
          "Pot bunkering and open sky")
    + "\n    "
    + fig("unionvale-pond", "A pond and cart path at The Links at Union Vale with a farm silo on the horizon",
          "A silo on the skyline &mdash; Dutchess County")
    + "\n    "
    + fig("unionvale-fescue", "Tall fescue and reeds in the foreground with a golf cart on the fairway beyond",
          "Fescue everywhere, and still findable")
    + "\n  </div>")

gumtree_photos = ('<div class="ig-grid" style="grid-template-columns:repeat(2,1fr);max-width:900px;">\n    '
    + fig("gumtree-studio", "The Gumtree Golf and Nature Club studio in Greenpoint, Brooklyn — leather sofas, a rug, caps laid out on a low table and rails of clothing under tall windows",
          "Showroom and workshop, same room")
    + "\n    "
    + fig("gumtree-rail", "A tree branch used as a clothing rail at Gumtree, hung with striped knits and denim, caps and sneakers on the plinth below",
          "The rail is a branch")
    + "\n  </div>")

bethpage_photos = ('<div class="ig-grid">\n    '
    + fig("bethpage-bunker", "A deep sand bunker set into native grasses on the Bethpage Black Course",
          "The bunkering is the whole argument")
    + "\n    "
    + fig("bethpage-clubhouse", "A stand bag on a bench overlooking the Bethpage clubhouse across a heavily bunkered hole",
          "Walking only. The bag comes with you")
    + "\n    "
    + fig("bethpage-bag", "A stand bag leaning against the Bethpage State Park post on the brick path by the clubhouse",
          "The brick path back to the clubhouse")
    + "\n  </div>")


page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITLE} &mdash; The Grassy Issue</title>
<meta name="description" content="{DESC}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{TITLE_PLAIN}" />
<meta property="og:description" content="{DESC}" />
<meta property="og:image" content="https://thegrassyissue.com/images/ny-trip/hero.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE_PLAIN}" />
<meta name="twitter:description" content="A private nine, a links-style public gem, and the Black on a cancellation." />
<link rel="canonical" href="{URL}" />
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "Article",
 "headline": "{TITLE_PLAIN}",
 "description": "{DESC}",
 "url": "{URL}",
 "datePublished": "2026-09-02",
 "dateModified": "2026-09-02",
 "author": {{"@type": "Organization", "name": "The Grassy Issue"}},
 "publisher": {{"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}},
 "mainEntityOfPage": {{"@type": "WebPage", "@id": "{URL}"}}
}}
</script>
{css_main}
</head>
<body>
{nav}

<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  A Week of New York Golf</div>

<header class="drop-header">
  <h1>A Week of New York Golf &mdash; Sedgewood, Union Vale and Bethpage Black</h1>
  <div class="drop-meta">
    <span>September 2, 2026</span><span class="dot"></span>
    <span>3 courses + a studio &middot; Aug 25 &ndash; Sep 1</span><span class="dot"></span>
    <span>Hudson Valley to Long Island</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The Bethpage clubhouse seen across a heavily bunkered hole on the Black Course, an oak in the foreground" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>Three courses in a week in New York, and no two of them are trying to do the same thing. A private nine in the Hudson Valley where nobody keeps score and the dog walks onto the green. A links-style public course in Dutchess County that costs a normal amount of money and plays like somewhere much further from a parkway. And Bethpage Black, which is a public golf course in the same way a mountain is a walk.</p>
    <p>The order was accidental &mdash; family first, then a course that justified the drive, then a cancellation that came up on a refresh &mdash; but it turned into a decent argument about what golf is actually for. Sedgewood is the game as a place you belong to. Union Vale is the game as a good afternoon. The Black is the game as a test you have volunteered for.</p>
    <p>There was a Brooklyn detour in the middle of it, to a studio that makes golf clothes out of salvaged fabric, which turned out to belong in the same conversation. What follows is each stop on its own terms, the way the week actually ran, and what the three courses together say about how much golf course you really need.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Week</div>
      <div class="sidebar-detail"><span class="l">Aug 25</span><span>Sedgewood</span></div>
      <div class="sidebar-detail"><span class="l">Aug 26</span><span>Union Vale</span></div>
      <div class="sidebar-detail"><span class="l">Aug 29</span><span>Gumtree, Brooklyn</span></div>
      <div class="sidebar-detail"><span class="l">Sep 1</span><span>Bethpage Black</span></div>
      <div class="sidebar-detail"><span class="l">Holes</span><span>45</span></div>
      <div class="sidebar-detail"><span class="l">Best round</span><span>84, Union Vale</span></div>
      <div class="sidebar-detail"><span class="l">Best moment</span><span>Par on the Black&rsquo;s 1st</span></div>
      <div class="sidebar-detail"><span class="l">Walked</span><span>Bethpage, by rule</span></div>
      <div class="hashtags">
        <span class="hashtag">#FieldNotes</span>
        <span class="hashtag">#BethpageBlack</span>
        <span class="hashtag">#HudsonValley</span>
        <span class="hashtag">#NewYorkGolf</span>
        <span class="hashtag">#MuniEnergy</span>
      </div>
    </div>
  </aside>
</div>

<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr">Sedgewood &mdash; The One You Grew Up On</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Sedgewood is nine holes at 3,005 yards, par 35, founded in 1928, sitting on around 1,200 acres of hilltop woodland an hour or so north of the city, with tennis courts and a spring-fed lake alongside the golf. It is private, and there is no way on without a member. On paper that is a short course. In practice the elevation does the work the yardage does not, and the difficulty sneaks up on people who read the scorecard and relax.</p>
    <p style="margin-top:16px">There are no tee times. It is rarely crowded. You turn up, and there is a deep bench of genuinely good players who will jump on with you, which is the sort of thing that only exists at a club small enough for everyone to know everyone. The views out over the Hudson Valley are the other reason to be there.</p>
    <p style="margin-top:16px">Almost nobody keeps a card. That is not a knock &mdash; it is the point. You still make a mental note of a birdie, because a birdie is a birdie, but the round is not really an accounting exercise. The dog on the green is Stella, a mixed lab, and her presence there tells you everything the club's bylaws would take a page to explain.</p>
  </div>
  {sedgewood_photos}
</section>

<section class="products" style="margin-top:40px;">
  <h2 class="products-hdr">The Links at Union Vale &mdash; The Gem</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Stephen Kay built this one and it opened in 2000, 6,839 yards and par 72, in Lagrangeville in southern Dutchess County, under ninety minutes from midtown. It is daily-fee public, which is the first thing in its favour and nowhere near the best. It is links-style and, unusually for a course that calls itself that, it earns the description &mdash; bent and fescue grasses, pot bunkers, natural hazards, and land that rolls rather than sits.</p>
    <p style="margin-top:16px">It played on a gorgeous day with a gentle breeze, which is exactly the weather this kind of course is built to reward. The holes are interesting without being unfair, it moves quickly, and the ball stays findable &mdash; there is fescue everywhere in the photographs and very little of it actually swallows a golf ball.</p>
    <p style="margin-top:16px">84. The best round of the week, on the course that asked the least and gave the most back.</p>
  </div>
  {unionvale_photos}
</section>

<section class="products" style="margin-top:40px;">
  <h2 class="products-hdr">A Detour to Greenpoint</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Three days between rounds, so: Brooklyn. Gumtree Golf &amp; Nature Club keeps a shop on Nassau Avenue in Greenpoint that is a showroom and a working studio at the same time &mdash; the place the prototypes get made and the place you buy the finished thing, one room, no separation. We went during open studio hours, which the website posts; it is not a shop you can reliably just walk past and wander into.</p>
    <p style="margin-top:16px">Karsten Jurkschat runs it and made every early Gumtree piece by hand himself, in a smaller Brooklyn studio, for the first six months of the brand. He moved from Melbourne to New York in 2017, grew up surfing, and found golf here &mdash; which explains both the name and the surfboards leaning against the wall next to the outerwear. He was around, happy to talk, and generous with his time in a way that is not guaranteed when you turn up at a working studio unannounced.</p>
    <p style="margin-top:16px">The clothes are upcycled from found and heirloom textiles and made in New York, and the merchandising tells you the same thing the label does: the rail is a tree branch, the caps are laid out on a low table between two leather sofas like objects rather than stock, and there is a rug on the floor. It reads like an apartment that happens to sell things. Coming from a week of golf that ran from a family nine to a US Open venue, it was the third distinct idea of what the game can be attached to.</p>
  </div>
  {gumtree_photos}
</section>

<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;The Black Course Is An Extremely Difficult Course Which We Recommend Only For Highly Skilled Golfers.&rdquo;<span class="pull-quote-attr">&mdash; The warning sign by the first tee, Bethpage State Park</span></div>
</div>

<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr">Bethpage Black &mdash; The Test</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Getting on is the first hurdle and it is a real one. Tee times go through the New York State parks system, non-residents booking five days out and residents further ahead, and the good ones evaporate on release. Green fees ran roughly $140 to $160 for non-residents in 2025, with New York residents paying about half that &mdash; which is the part people forget when they call it the best public course in America. This tee time came from refreshing the booking site until a cancellation surfaced. That is the method. There is no trick.</p>
    <p style="margin-top:16px">Then you arrive, and the scale lands before the golf does. Bethpage State Park holds five 18-hole courses &mdash; Black, Red, Blue, Green and Yellow &mdash; and standing in the middle of it is golf as far as the eye can see. Tillinghast drew the Black, the Red and the Blue and reworked what became the Green; Alfred Tull&rsquo;s Yellow followed in 1958. The Black opened in 1936 and has since hosted two US Opens, two Barclays, a PGA Championship and the 2025 Ryder Cup.</p>
    <p style="margin-top:16px">Rain took out most of the morning's tee times. We went off first once the delay lifted, onto a course nobody had touched yet. The intimidation on the first tee is real and it is nerve-wracking. The warning board has stood by that tee for decades and it is not a marketing line &mdash; it is the club telling you, in writing, what you have signed up for. Having played the hole a hundred times on a simulator paid off: par on the first, which settles you more than it should.</p>
    <p style="margin-top:16px">It is walking only, and it is a slog &mdash; 7,468 yards from the tips with the routing giving you nothing between green and tee. What you get in exchange is a course that keeps you thinking on every tee box. The risk-reward is constant, the greens are all seriously well guarded, and the design reads as a relic of an era that has ended. They simply do not build courses like this any more, and you can feel that in the ground. The front nine is solid. The back nine ramps up the distance and the difficulty and does not let go.</p>
    <p style="margin-top:16px">Carts are not permitted on the Black for anyone, at any time, so the walk is not a choice you get to make. None of the trouble is tricked up either &mdash; it is simply long, well-bunkered and uphill in the wrong places. Play a tee forward of where you think you belong and it turns into a great day instead of a grind.</p>
  </div>
  {bethpage_photos}
</section>

<section class="products" style="margin-top:40px;">
  <h2 class="products-hdr">What the Three Add Up To</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Forty-five holes across eight days, and the best round came at the cheapest course. That is not a paradox, it is most of the point. Union Vale gave up an 84 because it is built to be played rather than survived &mdash; wind you can use, a ball you can find, holes that ask a question and accept a reasonable answer.</p>
    <p style="margin-top:16px">The Black is the opposite proposition and is honest about it, in writing, on a sign, before you tee off. It is the better golf course by any measure an architect would use and it is the harder day by every measure a body would. Both of those are true at once, and the walk is the part that decides which one you remember.</p>
    <p style="margin-top:16px">Sedgewood is the one that reframes the other two. Nine holes, no tee sheet, no card, a dog on the green and a hillside of Hudson Valley behind it. It is the smallest golf course of the three and the one that most resembles what people actually want out of the game &mdash; and the Greenpoint studio, of all places, was making the same argument in cloth. If the week proved anything, it is that the amount of golf course you need is almost always less than the amount you think you need &mdash; and that being able to walk on at four in the afternoon beats almost any amount of architecture.</p>
  </div>
</section>

<section class="more">
  <div class="more-hdr">
    <span class="more-label">More from TGI</span>
    <a href="/" class="more-link">Back to Feed &rarr;</a>
  </div>
  <div class="more-grid">
    <a href="/drops/lions-municipal-golf-course-austin" class="more-card">
      <div class="more-card-img"><img src="/images/lions/hole16.jpg" alt="Lions Municipal Golf Course, Austin" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Lions Municipal &mdash; The Fight for Muny</div><div class="more-card-tag">Field Notes</div></div>
    </a>
    <a href="/drops/hancock-golf-course-austin" class="more-card">
      <div class="more-card-img"><img src="/images/hancock/hole4.jpg" alt="Hancock Golf Course, Austin" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Hancock &mdash; The Oldest Nine in Texas</div><div class="more-card-tag">Field Notes</div></div>
    </a>
    <a href="/field-guide/" class="more-card">
      <div class="more-card-img"><img src="/images/lions/course.jpg" alt="The Austin Golf Field Guide" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Austin Golf Field Guide</div><div class="more-card-tag">Field Notes</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "new-york-golf-trip-sedgewood-union-vale-bethpage-black.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
print("wrote %s | words: %d | photos: %d" % (out, words, page.count("<figure>")))
