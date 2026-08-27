#!/usr/bin/env python3
"""The Niche Grip Report — five independent golf grip makers.

Commissioned by Lenny 2026-08-27: "find me golf grip options that are a little
more niche, ripit grips, stick grips, etc." He first asked for four, then said
include all eight from the candidate grid.

ROSTER (5 brands, one card each — the no-repeat-brand rule applies).
Lenny picked these five from a grid of eight on 2026-08-27:
  RIPIT Grips (AU) · Stick Grips (US) · BestGrips (Conroe TX)
  Garsen Golf (US) · Rosemark Grips (US)
All five are in stock, which is why the sold-out disclaimer came out.

DROPPED from the grid of eight, by Lenny: Cloud & Wind Golf, The Grip Master
(sold out), Flat Cat (entire catalogue sold out). Their image frames were
deleted with them — re-download from the session notes if they come back.

CUT, and why — do not re-attempt without new information:
  PURE Grips (Mesa, AZ). Their own store carries a banner reading "We are
    currently not delivering or fulfilling products directly from this store"
    and redirects to Amazon. We do not link readers at a shop that will not
    ship. Otherwise a reasonable fit — family-owned, 100% US-made since 2009.
  Sacks Parente. Site returns 403 to everything; not bypassed on purpose.
  Iomic, Loudmouth, Sweet Rollz, Gimme Grips, Stinger. All already covered in
    /drops/7-grips-to-add-a-little-flavor — kept out to avoid repeating a brand
    across two grip posts.

STOCK, verified against the live product pages rather than the JSON feed
(2026-08-27). The single-product .json endpoint reports available:false for
everything and the list feed disagrees with both — only the rendered page is
trustworthy. All five picks were confirmed buyable that way.

ROSEMARK is a Wix store, not Shopify. No products.json, and its product links
are not exposed to a crawler, so the card points at the /grips collection page.
Its imagery had to be pulled from network-observed wixstatic requests; the first
three attempts returned Instagram/Facebook/YouTube icons, which is why there is
exactly one usable frame.

HERO is composed, not photographed. None of the five brands publishes a single
landscape editorial frame, and per the house rule a 2.34:1 band cut from a
portrait packshot always slices the subject. Five white tiles on TGI cream,
built by this script's sibling step — a specimen board rather than a lifestyle
shot. Regenerate with the hero block in the session notes if frames change.

Copy follows VOICE.md. Card prose is owned by data/copy-deck.json once this has
run and the deck has been extracted.
"""
import json, os, re, glob

ROOT   = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "images", "grips")
IMG    = "/images/grips/"
TPL    = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
SLUG   = "the-niche-grip-report"
OUT    = os.path.join(ROOT, "drops", SLUG + ".html")
TITLE  = "The Niche Grip Report"
TITLE_TXT = "The Niche Grip Report"
DESC = ("Five independent golf grip makers worked into one report: RIPIT's art series, Stick Grips, "
        "BestGrips handmade leather, Garsen's QUAD and Rosemark's tour-proven MFS. The one part of "
        "the club you actually touch.")
DATE = "2026-08-27"


def frames(key):
    fs = sorted(glob.glob(os.path.join(IMGDIR, f"{key}-*.jpg")),
                key=lambda p: int(re.search(r'-(\d+)\.jpg$', p).group(1)))
    return [os.path.basename(f) for f in fs]


def card(key, brand, kicker, name, desc, link):
    ff = frames(key)
    n = len(ff)
    assert n, f"no frames for {key}"
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="{brand} golf grip &middot; view {i+1} of {n}"></div>'
                 for i, f in enumerate(ff))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" id="{key}" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{kicker}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Visit {brand} &#8599;</a>
      </div>
  </div>'''


PRINTED = [
 ("ripit", "RIPIT Grips", "Australia &middot; In stock", "Eldrick &middot; $24.95",
  "RIPIT is an Australian brand built on the idea that a grip can carry artwork, and founder Todd Watts spent three years getting a print to survive the moulding before he sold one. The Eldrick is a deep oxblood with a line drawing worked into the surface rather than laid on top of it, and every RIPIT carries an alignment mark at both ends. They release in limited art series the way an apparel label runs drops.",
  "https://ripitgrips.com/products/eldrick"),
 ("stick", "Stick Grips", "United States &middot; In stock", "Country Club &middot; $13.49",
  "Stick Grips came to golf out of industrial rubber, and the one thing they changed is the taper. Their Ascension profile runs wider and straighter than a standard grip so both hands sit at close to the same diameter, which is a comfort argument rather than a performance one. The Country Club is a green and cream monogram repeat with hand and club-face alignment markers moulded in.",
  "https://stickgripsgolf.com/products/stick-grips-golf-country-club-golf-grip"),
]

PUTTER = [
 ("bestgrips", "BestGrips", "Conroe, Texas &middot; In stock", "Custom Major Leaguer Putter Grip &middot; $35",
  "BestGrips has been cutting and wrapping leather grips by hand in Conroe, Texas since 2003, and the Major Leaguer takes its stitch straight off a baseball. Top-grain cowhide, dyed and tacked in house, with a raised seam running the length of the grip where the thumbs sit. Leather moves under a hand in a way rubber does not, and that is the whole argument for thirty-five dollars.",
  "https://bestgrips.com/products/custom-major-leaguer-putter-grip"),
 ("garsen", "Garsen Golf", "United States &middot; In stock", "Chasing Daylight QUAD Tour NT &middot; $39.99",
  "Garsen makes putter grips only, and the QUAD is the shape the whole company rests on: a trapezoid with a flat top for the thumbs and angled sides that tuck the elbows in and take the hands out of the stroke. It works for claw and saw grips as well as conventional. This one is a collaboration with the Chasing Daylight podcast in black and safety yellow.",
  "https://garsengolf.com/products/chasing-daylight-podcast-quad-tour-nt"),
 ("rosemark", "Rosemark Grips", "United States &middot; In stock", "1.25 MFS &middot; $35",
  "Rosemark has a tour record that brands ten times its size would take: more than ten million dollars won with its grips, including Russell Knox at the 2018 Travelers Championship on this exact 1.25 MFS. The MFS surface is a moulded micro-texture rather than a cord or a wrap, which gives traction without the abrasion. The grips ship to more than twenty-five countries.",
  "https://www.rosemarkgrips.com/grips"),
]


def section(hid, h2, strong, kicker, items):
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n' + "\n".join(card(*it) for it in items) + '\n</div>\n')


products = (
 section("printed", "The Printed Ones", "Two &middot; art series and monograms",
   "These two treat the grip as the last unclaimed surface on a golf club, which is the newest idea "
   "in the category and the one the big four have not followed.", PRINTED)
 + section("putter", "The Putter Specialists", "Three &middot; leather, trapezoid, micro-texture",
   "The putter grip is where a golfer will accept something unusual, so it is where the small houses "
   "do their most interesting work &mdash; one in leather, one in a shape, one in a surface.", PUTTER)
)

FAQS = [
 ("What are the best niche golf grip brands?",
  "Five are covered here. RIPIT out of Australia for printed art-series grips at $24.95 and Stick Grips at $13.49 for full-swing sets; BestGrips in Conroe, Texas for handmade leather at $35, Garsen for the trapezoid QUAD at $39.99, and Rosemark for tour-proven micro-texture at $35 on the putter side."),
 ("What does it cost to regrip a full set?",
  "A full set is thirteen grips. At Stick's $13.49 that comes to about $175, and at RIPIT's $24.95 about $324. That arithmetic is why several small brands lead with putter grips instead, which are a single purchase."),
 ("Are leather golf grips any good?",
  "Leather was the standard before rubber won on price and durability, and BestGrips has been making them by hand in Conroe, Texas since 2003. Leather moves under the hand differently to rubber and it patinas with use. It also costs more and wants more care."),
 ("What is the Garsen QUAD grip?",
  "A putter grip with a trapezoid cross-section &mdash; a flat top for the thumbs and angled sides that set the shoulders back and tuck the elbows in, which reduces wrist action through the stroke. It comes in tapered and non-tapered versions and works with claw and saw grips."),
 ("Which grip brands have tour credibility?",
  "Rosemark is the clearest case: more than ten million dollars won on tour with its grips, and Russell Knox took the 2018 Travelers Championship using the 1.25 MFS. Garsen's QUAD has also been in play on tour."),
 ("What is a grip alignment mark and does it matter?",
  "It is a moulded or printed reference on the grip that shows you where the club face is pointing without looking down at it. RIPIT puts one at both ends of every grip, and Stick moulds in separate hand and club-face markers. It is a rules-legal aid as long as it does not indicate line of play once you are over the ball."),
 ("Do any of these ship outside the US?",
  "Rosemark sells into more than twenty-five countries. RIPIT is Australian and ships internationally from there. BestGrips, Stick and Garsen are US-based, so check shipping on the product page before ordering from abroad."),
 ("What about PURE Grips?",
  "PURE is a family-owned maker in Mesa, Arizona producing 100 per cent US-made grips, and on the face of it belongs in this company. Its own store currently carries a notice saying it is not fulfilling orders directly and points buyers to Amazon instead, so it is left out here."),
]

faq_html = "\n".join(
 f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)

art_ld = json.dumps({
 "@context": "https://schema.org", "@type": "Article",
 "headline": TITLE_TXT,
 "description": re.sub(r'&amp;', '&', DESC),
 "datePublished": DATE, "dateModified": DATE,
 "author": {"@type": "Organization", "name": "The Grassy Issue"},
 "publisher": {"@type": "Organization", "name": "The Grassy Issue"},
 "mainEntityOfPage": f"https://thegrassyissue.com/drops/{SLUG}",
 "image": f"https://thegrassyissue.com{IMG}hero.jpg"}, ensure_ascii=False)

faq_ld = json.dumps({
 "@context": "https://schema.org", "@type": "FAQPage",
 "mainEntity": [{"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": re.sub(r'&[a-z]+;', ' ', a)}} for q, a in FAQS]},
 ensure_ascii=False)

WRITEUP = '''<div class="writeup">
    <div class="writeup-body">
      <p>The grip is the only part of a golf club you actually touch, and four companies decide what almost everyone holds. Golf Pride, Lamkin, Winn and SuperStroke work from a shared assumption &mdash; that a grip is a consumable, black and ribbed, replaced when it goes shiny. Five smaller houses start somewhere else, and they are why the category has become interesting again.</p>
      <p>What the independents sell splits two ways. RIPIT and Stick Grips work on the full-swing set and treat the grip as a surface to print on, in limited art series and monogram repeats. The other three work on the putter, where BestGrips wraps cowhide by hand the way grips were made before rubber won on price, Garsen builds a trapezoid nobody else tools up for, and Rosemark moulds a micro-texture that has won ten million dollars on tour.</p>
      <p>The economics explain the shape of the field. A full set is thirteen grips, so a Stick set runs about a hundred and seventy-five dollars and a RIPIT set about three hundred and twenty-five. That is why so many of these brands lead with putter grips. A putter grip is a single purchase, an easy first buy, and the one club where a golfer will tolerate something that looks unusual.</p>
      <p>The five below run from thirteen dollars to forty, and all of them are in stock as of late August. Two are for the whole set, three are for the one club where a golfer will try something strange.</p>
    </div>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Countries</span><span>2</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$13.49&ndash;$39.99</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>
      <a href="/brands/" class="sidebar-cta">Browse the Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfGrips</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#GearEdit</span>
      </div>
    </div>
  </aside>'''

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
           lambda m: f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           lambda m: f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', lambda m: m.group(1) + TITLE_TXT + m.group(2))
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>5 Brands</span><span>&middot;</span>'
           '<span>Independent grip makers &middot; All in stock &middot; Checked Aug 2026</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="Five independent golf grips from RIPIT, Stick Grips, BestGrips, Garsen and Rosemark" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', lambda m: WRITEUP)

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/brand-to-know-cloud-and-wind-golf" class="more-card">
      <div class="more-card-img"><img src="/images/cloud-and-wind/classic-collection.jpg" alt="Cloud and Wind Golf" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Cloud &amp; Wind Golf</div><div class="more-card-tag">Brand to Know</div></div>
    </a>
    <a href="/drops/texas-golf-brands-and-makers" class="more-card">
      <div class="more-card-img"><img src="/images/texas-brands/hero-texas-brands.jpg" alt="Texas Golf Brands and Makers" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Texas Golf Brands and Makers</div><div class="more-card-tag">The Roundup</div></div>
    </a>
    <a href="/drops/the-custom-wedge-report" class="more-card">
      <div class="more-card-img"><img src="/images/custom-wedges/hero.jpg" alt="The Custom Wedge Report" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Custom Wedge Report</div><div class="more-card-tag">The Report</div></div>
    </a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
n = len(PRINTED) + len(PUTTER)
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words, {n} brands)")

# --- house voice guard -------------------------------------------------------
# Card copy and section kickers are owned by data/copy-deck.json, not by this
# script (see VOICE.md). Re-applying the deck here means a rebuild can never
# silently restore pre-2026-08-27 copy. Safe to run repeatedly.
import subprocess as _sp
_sp.run(["python3", os.path.join(ROOT, "copy-deck.py"), "apply"], check=False)
