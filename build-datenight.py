#!/usr/bin/env python3
"""Build drops/date-night-after-36.html — Field Notes: Austin date-night spots
after a 36-hole weekend. All 15 spots verified open Aug 2026 via web research.

FACT NOTES:
  * Launderette REQUIRED anchor — converted 1950s laundromat, 2115 Holly St,
    opened 2015 (Rene Ortiz & Laura Sawicki), Hank Longworth head chef Dec 2025,
    Michelin Guide listed, birthday-cake ice cream sandwich (Eater iconic list).
  * Olamaie CLOSED July 2026 — do not mention as open. Original Bufalina closed.
  * Texas French Bread reopened spring 2026 at 2900 Rio Grande after Jan 2022
    fire; dinner Tue–Sat; bakery since 1981.
  * Hestia: Michelin one star 2024 AND 2025. Birdie's: Food & Wine 2023
    Restaurant of the Year; Beard noms 2024/2025. Canje: No.3 Food & Wine 2026
    Global Tastemakers. Nixta: Edgar Rico, Beard Best Emerging Chef 2022.
  * Tag = [Field Notes], data-type=field. No "worth".
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open('/tmp/datenight/manifest.json'))
MAN.setdefault('justines', ['justines-x0.jpg','justines-x1.jpg'])
MAN.setdefault('tfb', ['tfb-x0.jpg','tfb-x1.jpg'])
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "date-night-after-36.html")
SLUG = "date-night-after-36"
TITLE = "Date Night After 36 &mdash; Where to Take Them When You Played All Weekend"
TITLE_TXT = "Date Night After 36 — Where to Take Them When You Played All Weekend"
DESC = ("You played 36 holes this weekend. Dinner is the peace treaty. Fifteen Austin date-night spots from "
        "Michelin-star splurges to queso at Matt's — with Launderette leading, all verified open in 2026.")
IMG = "/images/date-night/"

def card(slug, name, hood, tier, link, desc):
    frames = MAN[slug]; n = len(frames)
    alt = re.sub(r'&[a-z]+;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" alt="{alt}, Austin date night restaurant"></div>' for f in frames)
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}" id="{slug}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{hood} &middot; {tier}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">View &#8599;</a>
      </div>
  </div>'''

S1 = [  # The Splurge
 ("launderette","Launderette","East Austin (Holly)","$$$","https://launderetteaustin.com/",
  "The anchor of this list and the reason it exists. A 1950s laundromat-turned-neighborhood-restaurant on Holly Street, open since 2015, Michelin Guide listed, with a new head chef as of last December. Order the plancha burger, the wood-grilled octopus, and no matter what else happens, the birthday cake ice cream sandwich &mdash; Eater has it on the shortlist of Austin&rsquo;s most iconic dishes. The neon sign alone is date-worthy&hellip; scratch that: the neon sign alone closes the argument."),
 ("hestia","Hestia","Downtown (W 3rd)","$$$$","https://hestiaaustin.com/",
  "Austin&rsquo;s live-fire church: Kevin Fink&rsquo;s hearth-driven room held a Michelin star in both 2024 and 2025, and everything &mdash; the scallops, the sourdough with beef-fat butter &mdash; passes through the fire. If the weekend included a personal best, this is where you tell the story."),
 ("uchiko","Uchiko","Rosedale (Burnet)","$$$$","https://haihospitality.com/uchiko/",
  "Tyson Cole&rsquo;s flagship sibling and still the hardest table on this list &mdash; book weeks out. Ham and eggs (crispy pork belly, soft yolk) and the jasmine cream br&ucirc;l&eacute;e have been closing Austin arguments for fifteen years. The move: book it the same day you book the weekend tee times."),
 ("sammies","Sammie&rsquo;s Italian","West 6th","$$$","https://sammiesitalian.com/",
  "Red-sauce glamour from the McGuire Moorman group &mdash; veal parm, martinis, valet, and a dining room that runs to midnight on weekends. The right answer when the second eighteen finished at seven and you still want to feel like the evening is an occasion."),
 ("este","Este","East Austin","$$$","https://www.esteatx.com/",
  "Coastal Mexican seafood from the Suerte team &mdash; aguachiles, wood-fired whole fish, and the prettiest blue building on the east side. The reservation is hard; the hour on the patio once you have it is the easiest part of the weekend."),
 ("clarks","Clark&rsquo;s Oyster Bar","Old West Austin","$$$","https://www.clarksoysterbar.com/locations/austin",
  "A tiny, preppy-nautical room on West 6th that has been the city&rsquo;s default celebration spot since 2012. Oysters, a lobster roll, something cold and French by the glass. Small enough that the reservation is the hard part &mdash; the bar seats reward walk-in optimism."),
]
S2 = [  # The Sweet Spot
 ("josephine","Josephine House","Clarksville","$$$","https://www.josephineofaustin.com/",
  "A blue cottage with a gravel garden patio in Clarksville, sister to Jeffrey&rsquo;s next door. This is the golden-hour option &mdash; go before sunset, sit outside, and let the steak frites and the string lights do the apologizing for your five-hour absence."),
 ("oddduck","Odd Duck","South Lamar","$$$","https://oddduckaustin.com/",
  "Bryce Gilmore&rsquo;s farm-to-table original, a Michelin Bib Gourmand, and the best small-plates ordering in town: hand the menu back and ask the kitchen to feed you. The trailer-to-institution story is the most Austin arc in this post."),
 ("justines","Justine&rsquo;s Brasserie","East 5th","$$$","https://justines1937.com/",
  "The late-night insurance policy. A candlelit French brasserie in a 1937 bungalow that seats late and pours later &mdash; steak frites, escargot, red wine, no rush. When the second round ran long and every other kitchen is closing, Justine&rsquo;s is just getting good."),
 ("canje","Canje","East Austin","$$$","https://canjeatx.com/",
  "Tavel Bristol-Joseph&rsquo;s modern Caribbean room &mdash; pepper fish, West Indian curry, rum drinks &mdash; and freshly ranked No. 3 on Food &amp; Wine&rsquo;s 2026 Global Tastemakers list. The loudest, warmest, most alive room in this section."),
 ("tfb","Texas French Bread","West Campus","$$","https://texasfrenchbread.com/",
  "The comeback of the year. A fire leveled the 1981 institution in January 2022; four and a half years later it reopened on Rio Grande this spring, and the farm-to-table dinner service &mdash; Tuesday through Saturday, lamb meatballs, trout with braised cabbage &mdash; is back. Bring someone who understands why that matters."),
]
S3 = [  # The Casual Close
 ("birdies","Birdie&rsquo;s","East 12th","$$","https://birdiesaustin.com/",
  "Obviously it was making this list. A counter-service wine bar named Birdie&rsquo;s &mdash; Food &amp; Wine&rsquo;s 2023 Restaurant of the Year, with Beard nominations for both halves of the couple that runs it. Seasonal pastas, an olive-oil soft-serve sundae, and a line that forms before open. The name alone settles where you go after a round with birdies in it."),
 ("loro","Loro","South Lamar","$$","https://www.loroeats.com/locations/austin/south-lamar/",
  "Aaron Franklin and Tyson Cole&rsquo;s Asian smokehouse &mdash; smoked brisket with chili gastrique, oak-grilled ribs, frozen drinks, big shaded patio. Walk-in, sandals-acceptable, and the correct answer when date night needs to start twenty minutes after the last putt."),
 ("nixta","Nixta Taqueria","East 12th","$$","https://www.nixtataqueria.com/",
  "Edgar Rico&rsquo;s heirloom-masa taqueria &mdash; a James Beard Best Emerging Chef win and a TIME100 nod attached to a duck carnitas taco and a beet &ldquo;tartare&rdquo; tostada. Casual in price and dress code only; the cooking is as serious as anything in the splurge section."),
 ("matts","Matt&rsquo;s El Rancho","South Lamar","$$","https://www.mattselrancho.com/",
  "The 1952 Tex-Mex institution, for the partner who does not want a tasting menu &mdash; they want a Bob Armstrong queso, a frozen margarita, and for you to stop talking about your back nine. Closed Tuesdays; there will be a wait; the wait is part of it."),
]

def section(hid, h2, strong, kicker, items):
    cards = "\n".join(card(*it) for it in items)
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n{cards}\n</div>\n')

products = "\n".join([
 section("splurge","The Splurge","Six spots &middot; $$$ to $$$$",
  "The full-apology tier: a Michelin star, the hardest sushi table in town, red-sauce glamour and the laundromat that started this whole idea. Book these when you book the tee times, not after.", S1),
 section("sweetspot","The Sweet Spot","Five spots &middot; $$ to $$$",
  "Special without the ceremony &mdash; garden patios, candlelit brasseries, a Caribbean room on a global best-of list, and the greatest comeback story in Austin dining. Most of these can absorb a same-day plan.", S2),
 section("casual","The Casual Close","Four spots &middot; all $$",
  "For when the second eighteen took it out of you: walk-in wine bars, smoked brisket with a patio, Beard-winning tacos and fifty-year-old queso. One of them is literally named Birdie&rsquo;s.", S3),
])

FAQS = [
 ("What is the best date night restaurant in East Austin?",
  "Launderette — the converted 1950s laundromat on Holly Street that has anchored east-side dining since 2015. It's Michelin Guide listed, the patio is one of the neighborhood's best, and the birthday cake ice cream sandwich is on Eater's list of Austin's most iconic dishes. Este, Canje and Justine's Brasserie give the east side three more at different volumes."),
 ("Where should we eat after playing golf in Austin?",
  "Depends on the state of you. Straight off the course: Loro's patio or Matt's El Rancho, no shower judgment. Cleaned up: Launderette or Josephine House at golden hour. Celebrating a career round: Hestia, which held a Michelin star in 2024 and 2025."),
 ("Which Austin restaurants are hardest to book?",
  "From this list: Uchiko (book weeks out), Este, Suerte's sibling reservations generally, Clark's (a very small room) and Sammie's on weekends. Birdie's takes no reservations at all — the line forms before open, which is its own kind of date."),
 ("Is Birdie's in Austin related to golf?",
  "No — it's a counter-service wine bar on East 12th named Birdie's, run by Tracy Malechek-Ezekiel and Arjav Ezekiel. But it was Food & Wine's 2023 Restaurant of the Year, both owners have James Beard nominations, and we are constitutionally incapable of leaving a place called Birdie's out of a golf publication's dinner list."),
 ("Did Texas French Bread reopen?",
  "Yes. The 1981 bakery-turned-bistro was destroyed by fire in January 2022 and reopened in spring 2026 at 2900 Rio Grande in West Campus, with dinner service Tuesday through Saturday — lamb meatballs, trout with braised cabbage, and the bread that made the name."),
 ("What happened to Olamaie?",
  "It closed in July 2026 after twelve years, Michelin star and all — which is why it isn't on this list. Maie Day, Michael Fojtasek's chophouse at the South Congress Hotel, carries the lineage if you were an Olamaie loyalist."),
 ("What are the most romantic restaurants in Austin?",
  "Candlelight and patios do the work: Justine's Brasserie (a 1937 bungalow, late seatings), Josephine House's garden in Clarksville, Este's courtyard at dusk, and Clark's if your idea of romance involves oysters in a room the size of a rail car."),
 ("Where can you get a late dinner in Austin?",
  "Justine's Brasserie is the classic late-night answer — seating well past most kitchens' close since 2009. Sammie's runs to midnight on weekends. Both are on this list precisely because 36 holes has a way of destroying a dinner schedule."),
 ("What is the dress code situation at these spots?",
  "The casual tier (Birdie's, Loro, Nixta, Matt's) is come-as-you-are. The sweet spot is clean-shirt territory. For Hestia, Uchiko and Sammie's, change out of the golf clothes — you own a Players Shirt for exactly this occasion."),
 ("How were these restaurants chosen?",
  "Every spot was verified open as of late August 2026 — which mattered, because the research caught two significant closures this summer. The list optimizes for one scenario: you spent the weekend on a golf course, you owe someone a great dinner, and Austin has fifteen correct answers at three volumes."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC.replace('&mdash;','—'),
 "author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-25","dateModified":"2026-08-25",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>Here is the math of a 36-hole weekend: ten hours on the course, two more at the range or the bar, and a
    partner at home who has watched you leave in the dark twice. Dinner is not a suggestion at that point. Dinner
    is the peace treaty, and this is the map of where to sign it.</p>
    <p>The list runs at three volumes. The Splurge is for real occasions and real apologies &mdash; the Michelin
    star, the impossible sushi table, the laundromat on Holly Street that became one of Austin&rsquo;s defining
    restaurants. The Sweet Spot is special without ceremony: garden patios, a candlelit brasserie that seats
    late, and the best comeback story in Austin dining. The Casual Close is for when the second eighteen took
    everything you had &mdash; wine bars, brisket, tacos, queso.</p>
    <p>Everything here was verified open in late August 2026, which turned out to matter: the research caught
    Olamaie closing in July after twelve years and a Michelin star, and the original Bufalina going dark on Cesar
    Chavez. Austin restaurants move like Austin tee sheets. And yes &mdash; there is a spot called Birdie&rsquo;s
    on the list, it is spectacular, and no, we could not have left it off if we tried.</p>
    <p>One planning note from experience: the splurge tier books like a Saturday morning tee time. Reserve dinner
    the same day you reserve the golf, and the whole weekend becomes defensible.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Spots</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$$ &ndash; $$$$</span></div>
      <div class="sidebar-detail"><span class="l">Verified</span><span>Aug 2026</span></div>
      <div class="sidebar-detail"><span class="l">Anchor</span><span>Launderette</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#AustinEats</span>
        <span class="hashtag">#DateNight</span>
        <span class="hashtag">#After36</span>
      </div>
    </div>
  </aside>
</div>'''

tpl = open(TPL, encoding="utf-8").read()
head, rest = tpl.split('<section class="products">', 1)
_, tail = rest.split('</section>', 1)

def rep(s, pat, new, count=1):
    out, n = re.subn(pat, new, s, count=count, flags=re.S)
    assert n > 0, pat
    return out

head = rep(head, r'<title>.*?</title>', f'<title>{TITLE_TXT} | The Grassy Issue</title>')
head = rep(head, r'<meta name="description" content=".*?"', f'<meta name="description" content="{DESC}"')
head = rep(head, r'<meta property="og:url" content=".*?"', f'<meta property="og:url" content="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{DESC}"')
head = rep(head, r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta name="twitter:description" content=".*?"', f'<meta name="twitter:description" content="{DESC}"')
head = rep(head, r'<link rel="canonical" href=".*?"', f'<link rel="canonical" href="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
           f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', r'\g<1>'+TITLE_TXT+r'\g<2>')
head = rep(head, r'<a href="/#feed">[^<]*</a>(<span>/</span>)', '<a href="/#feed">Field Notes</a>\\1', count=5)
head = rep(head, r'<span class="drop-tag grass">\[[^\]]*\]</span>', '<span class="drop-tag grass">[Field Notes]</span>')
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>', '<div class="drop-meta">\n    <span>15 Spots</span><span>&middot;</span><span>Austin, TX &middot; Verified Aug 2026</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}launderette-0.jpg" alt="The Launderette neon sign in East Austin at dusk" style="object-position:center 40%;" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP)

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/best-sandwiches-before-the-round" class="more-card"><div class="more-kicker">Field Notes</div><div class="more-title">Sandwiches Before the Round</div></a>
    <a href="/drops/the-best-pizza-in-austin" class="more-card"><div class="more-kicker">Field Notes</div><div class="more-title">The Best Pizza in Austin</div></a>
    <a href="/drops/the-pre-round-pour-austin-coffee" class="more-card"><div class="more-kicker">Field Notes</div><div class="more-title">The Pre-Round Pour &mdash; 18 Austin Coffee Shops</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>',' ',page).split())
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words)")
