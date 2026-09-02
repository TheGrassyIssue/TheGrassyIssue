#!/usr/bin/env python3
"""build-manors-btk.py — Brand Revisited: Manors Golf.

Lenny, 2026-09-02: "Let's do Manors first - Brand revisited, deep dive, quotes,
lookbook images, collabs, etc."

WHY THIS IS A NEW PAGE, against the usual "upgrade in place" rule:
Manors had 29 pieces of coverage — 2nd most on the site — but its "profile" in
data/brand-mentions.json was /drops/manors-ss26, a 1,479-word seasonal drop post
with no founder quote, no FAQ and no galleries. Every internal link pointed at a
page never built to carry a brand. Lenny chose (2026-09-02) to build the
evergreen profile here and leave manors-ss26 alone as the seasonal drop post it
actually is, repointing the mentions-map profile flag rather than 301-ing.

THE ANGLE: Manors launched in 2019 rejecting technical golf apparel, then in
spring 2023 wiped its socials and relaunched as a technical golf brand. The
reversal is the story, and the current catalogue shows both halves — Polartec
and recycled tech sitting next to a heritage check polo and a reversible knit vest.

SOURCING: every quote is verbatim from the Hypebeast interview (Jack Stanley,
7 May 2021) — see research/manors-dossier.md. The 859% growth figure traces to
one marketing newsletter, not trade press or a filing, so it is attributed in
the text rather than stated flat (Lenny's call, 2026-09-02).

Product data and imagery scraped from the rendered storefront on 2026-09-02 —
manorsgolf.com has Shopify's products.json and per-product .js disabled.

Chassis cloned from drops/brand-to-know-kingfisher-golf.html (the gold standard).
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "drops", "brand-to-know-kingfisher-golf.html")
if not os.path.exists(SRC):
    SRC = os.path.join(S, "drops", "lions-municipal-golf-course-austin.html")
ch = open(SRC, encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

# The Kingfisher chassis carries no .cat-kicker rule, so section ledes render
# full-width and verify-post fails. Install the canonical house rules.
if ".cat-kicker{" not in css_main:
    css_main = css_main.replace("</style>",
        ".products h2{font-family:var(--serif);font-weight:600;font-size:clamp(24px,2.6vw,32px);"
        "letter-spacing:-.01em;line-height:1.1;margin:14px 0 16px}"
        ".cat-kicker{font-size:15px;line-height:1.75;color:#3f443e;margin:0 0 36px;max-width:70ch;"
        "border-left:3px solid var(--rough);padding:4px 0 4px 18px}"
        ".cat-kicker strong{font-family:var(--mono);font-size:11px;letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--grass);opacity:1;display:block;margin-bottom:8px}"
        "\n</style>", 1)

if ".pull-quote{" not in css_main:
    css_main = css_main.replace("</style>",
        ".pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
        ".pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
        "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
        "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
        ".pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
        "@media(max-width:820px){.pull-quote{padding:0 20px}}\n</style>", 1)

# Photo rows for the journal imagery. Same markup as the NY field note.
if ".ig-grid{" not in css_main:
    css_main = css_main.replace("</style>",
        ".ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 34px}"
        ".ig-grid figure{margin:0}"
        ".ig-grid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5}"
        ".ig-cap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;"
        "color:var(--ink);opacity:.5;margin-top:8px;line-height:1.5}"
        "@media(max-width:720px){.ig-grid{grid-template-columns:repeat(2,1fr);gap:10px}}"
        "\n</style>", 1)

URL         = "https://thegrassyissue.com/drops/brand-to-know-manors"
TITLE       = "Manors Golf, Revisited &mdash; The Brand That Rejected Technical Golf, Then Became a Technical Golf Brand"
TITLE_PLAIN = "Manors Golf, Revisited — The Brand That Rejected Technical Golf, Then Became a Technical Golf Brand"
DESC        = ("Manors launched in London in 2019 arguing nobody needed a technical polo. In 2023 it wiped its "
               "socials and relaunched as a technical golf brand. The founders, the reversal, the collabs, "
               "and what is actually in the range now.")
IMG   = "/images/manors"
STORE = "https://manorsgolf.com/products/"


def photos(*items):
    """items: (file, alt, caption) — renders an ig-grid row."""
    figs = "\n  ".join(
        '<figure><img src="%s/%s.jpg" alt="%s" loading="lazy" />'
        '<figcaption class="ig-cap">%s</figcaption></figure>' % (IMG, f, a, c)
        for f, a, c in items)
    return '<div class="ig-grid">\n  %s\n</div>' % figs


# Frame counts per product, from the rendered manorsgolf.com galleries (2026-09-02).
# Manors serves product media from Sanity, not Shopify — the .js/.json endpoints are
# 404, so these were read off the rendered DOM (imgs with .aspect-4/5.fadeIn) and
# saved as {base}-a2/-a3/-a4. See research/manors-dossier.md.
FRAMES = json.load(open(os.path.join(S, "data", "manors-frames.json")))


def card(base, name, price, frames, desc, alt, handle):
    n = FRAMES.get(base, 1)
    srcs = [base] + ["%s-a%d" % (base, i) for i in range(2, n + 1)]
    gal = "".join('<div class="pg-frame"><img src="%s/%s.jpg" alt="%s" loading="lazy" /></div>'
                  % (IMG, s, alt) for s in srcs)
    if n > 1:
        dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                       % (" on" if i == 0 else "", i, i + 1) for i in range(n))
        ctrl = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
                '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
                '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>' % (n, dots))
    else:
        ctrl = ""
    tmpl = ('<div class="product-card" data-frames="%(n)d">'
            '<div class="product-gallery"><div class="pg-track">%(gal)s</div>%(ctrl)s</div>'
            '<div class="product-body">'
            '<div class="product-brand">Manors</div>'
            '<div class="product-name">%(name)s &middot; %(price)s</div>'
            '<div class="product-desc">%(desc)s</div>'
            '<a href="%(store)s%(handle)s" target="_blank" rel="noopener" '
            'class="product-link">Shop &#8599;</a>'
            '</div></div>')
    return tmpl % dict(n=n, gal=gal, ctrl=ctrl, name=name, price=price,
                       desc=desc, store=STORE, handle=handle)


SECTIONS = [
 ("The Collab Archive",
  "<strong>Collabs &middot; adidas, Reebok, Gentleman Jack</strong>Three partners in five years, and they get progressively stranger: a sportswear giant, a footwear icon, and a Tennessee whiskey. The adidas capsule is the one that explains the brand&rsquo;s sense of humour; the Reebok run is the one that put Manors on American feet.",
  [
   ("rbk-clubc", "Reebok x Manors Club C Revenge Golf", "$176",1,
    "The Club C comes rebuilt here as a golf shoe in Legacy Green. Reebok&rsquo;s first Manors collaboration landed globally on 10 June 2025 as a ten-piece collection, with this and the OG Pump Golf carrying the footwear.",
    "Reebok x Manors Club C Revenge golf shoe in legacy green","reebok-x-manors-club-c-revenge-golf"),
   ("rbk-harrington", "Reebok x Manors Harrington Jacket", "$243",1,
    "The most expensive piece in the collab and the one that reads least like golf. A Harrington is a 1960s British jacket; putting one on a fairway is the whole Manors thesis in a single garment.",
    "Reebok x Manors Harrington jacket in pebble","manors-x-reebok-harrington-jacket"),
   ("rbk-mockneck", "Reebok x Manors Mock Neck Polo", "$129",1,
    "Legacy Green, raised neck, the two marks sharing a chest. The colourway is Reebok&rsquo;s archive, the silhouette is Manors&rsquo; own.",
    "Reebok x Manors mock neck polo in legacy green","manors-x-reebok-mockneck-polo"),
   ("gj-blade", "Gentleman Jack&reg; x MANORS Blade Polo", "$115",1,
    "The third partner, and the least predictable: a Jack Daniel&rsquo;s label. Pine green, blade collar, and a co-brand that makes more sense at the halfway house than on the tee.",
    "Gentleman Jack x Manors blade polo in pine green","gentleman-jack-x-manors-blade-polo"),
   ("gj-merino", "Gentleman Jack&reg; x MANORS Merino Crewneck", "$284",1,
    "The most expensive thing Manors currently sells. Merino, antique colourway, and proof the whiskey collab was given real budget rather than treated as a logo swap.",
    "Gentleman Jack x Manors merino crewneck in antique","gentleman-jack-x-manors-merino-crewneck-mens"),
  ]),

 ("The Technical Turn",
  "<strong>Post-2023 &middot; The Technical Line</strong>This is the half of the range that would not have existed in 2021. Polartec, recycled fabric, tech mid-layers, packable shells &mdash; the vocabulary of exactly the technical golf apparel the founders originally said nobody needed.",
  [
   ("tech-polartec", "Outsider Polartec&reg; Polo", "$115",1,
    "A branded performance fabric on a Manors polo. In 2021 the pitch was that a sweat-wicking polo would not change your score; in 2026 Polartec is on the label.",
    "Manors Outsider Polartec polo in vapour","outside-polartec-polo"),
   ("tech-hoodie", "Outsider Polartec&reg; Hoodie", "$176",1,
    "The same fabric in a hoodie, in Shark grey. Golf hoodies were a punchline five years ago and are now a category.",
    "Manors Outsider Polartec hoodie in shark grey","outside-polartec-hoodie"),
   ("tech-midlayer", "1/4 Zip Tech Mid-Layer", "$162",1,
    "The quarter-zip mid-layer is the single most technical-looking garment in the range and one of the better-cut ones. Dune, ribbed cuffs, high collar.",
    "Manors quarter zip tech mid-layer in dune","quarter-zip-tech-mid-layer"),
   ("tech-trouser", "Recycled Greenskeeper Trouser", "$176",1,
    "Recycled fabric, workwear name, black. The Greenskeeper line is where the technical reposition and the old British-labour romance actually meet.",
    "Manors recycled Greenskeeper trouser in black","recycled-greenskeeper-trouser"),
   ("tech-jacket", "Lightweight Course Jacket", "$216",1,
    "Packable shell in Dune. The kind of piece a 2019 Manors would have left to Galvin Green.",
    "Manors lightweight course jacket in dune","lightweight-course-jacket"),
  ]),

 ("What Survived the Rebrand",
  "<strong>Carried Over &middot; The Original Argument</strong>The reposition did not erase the original brand. The golden-age research Nick Watts describes &mdash; archive footage, Getty images of majors, the crowds as much as the players &mdash; is still visible in the cuts and the knitwear.",
  [
   ("old-stableford", "Stableford Trouser", "$190",1,
    "Manors describes it as classic workwear with a nod to golf&rsquo;s golden era, which is the whole pre-2023 pitch stated as a product description. The silhouette is wide and cuffed and belongs to no current golf brand; the Primeflex fabric it is cut from belongs to all of them.",
    "Manors Stableford Trouser in stone, wide cuffed workwear silhouette","work-trousers"),
   ("old-check", "Heritage Check Polo", "$115",1,
    "Black, checked, and named for the thing it is. The heritage line is the counterweight to the Polartec end of the rail.",
    "Manors heritage check polo in black","heritage-check-polo"),
   ("old-vest", "Reversible V-Neck Vest", "$162",1,
    "The V-neck vest is pure Palmer-era golf, reversible so it earns its place in a small wardrobe. Dune.",
    "Manors reversible v-neck vest in dune","reversible-v-neck-vest"),
   ("old-clubpolo", "Club Polo", "$129",1,
    "The house polo in black. Dropped shoulder, relaxed body &mdash; cut so you could wear it off the course, which was the founding argument and still holds.",
    "Manors club polo in black","club-polo"),
   ("old-tourshirt", "Tour Shirt", "$162",1,
    "A camp-collar shirt in dark olive, sized to be worn open. The single most un-golf garment Manors makes.",
    "Manors tour shirt in dark olive","tour-shirt"),
   ("hc-driver", "Barrel Driver Cover", "$68",1,
    "Black barrel cover, no pattern, no joke. Manors&rsquo; accessories are deliberately the quietest things they sell.",
    "Manors barrel driver headcover in black","blade-putter-headcover-copy"),
  ]),
]

FAQS = [
 ("Who founded Manors Golf?",
  "Jojo Regan and Luke Davies, school friends who reconnected over golf as adults, set up Manors in London in 2019. Regan is a lifelong golfer; Davies came to the sport later. They were joined by Nick Watts as Fashion Director, who shaped the brand's look around golf's golden age."),
 ("Why did Manors rebrand in 2023?",
  "In spring 2023 Manors wiped its social channels and relaunched — a repositioning it called 'A Change of Course', handled by Stink Studios — moving from a heritage-leaning lifestyle label to a technical golf brand. It is a genuine reversal of the brand's founding pitch, which was that golfers did not need technical apparel."),
 ("Did the Manors rebrand work?",
  "By the available accounts, yes. A marketing case study of the repositioning reports the brand up 859% year on year with a shift from wholesale to direct-to-consumer. That figure comes from a single industry newsletter rather than a filing, so treat it as indicative. What is independently visible: a Harrods stockist, the Reebok collaboration, and Manors appearing as a playable skin in 2K's PGA Tour 2025."),
 ("What collabs has Manors done?",
  "Three notable ones. adidas Golf, 'The Beautiful Game' in SS21, a golf-meets-football capsule launched against The Open and Euro 2020 whose crest swapped England's three lions for three golf irons. Reebok, first in June 2025 as a ten-piece collection with the OG Pump Golf and Club C Revenge, and again in 2026. And an ongoing Gentleman Jack® partnership with Jack Daniel's."),
 ("Where is Manors based and where does it ship?",
  "London. The brand sells direct through manorsgolf.com with US dollar pricing, and is stocked at Harrods among other retailers. Prices in the current range run about $48 for a course cap to $284 for the Gentleman Jack merino crewneck."),
 ("Is Manors actually technical now, or is it styling?",
  "Both, and the range splits cleanly. The Outsider pieces use Polartec, the Greenskeeper line uses recycled fabric, and the quarter-zip mid-layers are built as mid-layers. Alongside them sit a knitted baker boy cap and a reversible V-neck vest that make no performance claim at all. The rebrand added a technical half rather than replacing the original one."),
 ("What does Manors mean by 'personality before performance'?",
  "It is the line the brand used at launch, drawn from studying Arnold Palmer, Gary Player and Jack Nicklaus — the argument that how golf looked in its golden age counts for more than marginal fabric gains. The phrase predates the 2023 reposition, which is part of what makes the reposition interesting."),
]

faq_schema = ",\n  ".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (json.dumps(q), json.dumps(a)) for q, a in FAQS)
faq_html = "\n    ".join('<details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)

sections_html = ""
for hdr, kick, cards in SECTIONS:
    sections_html += ('\n<section class="products" style="margin-top:40px;">\n'
        '  <h2 class="products-hdr">%s</h2>\n  <p class="cat-kicker">%s</p>\n'
        '  <div class="products-grid">\n    %s\n  </div>\n</section>\n'
        % (hdr, kick, "\n    ".join(card(*c) for c in cards)))

photo_row_a = photos(
    ("irl-piper",
     "A kilted piper handing a club to a golfer in a Manors jacket at Royal Dornoch",
     "Royal Dornoch &middot; the piper on the first"),
    ("irl-dunes-swing",
     "A golfer in a navy Manors polo and stone trousers at the finish of a swing on the links at Machrihanish Dunes",
     "Machrihanish Dunes &middot; stone trouser, navy polo"),
    ("irl-flagstick",
     "A golfer in a Manors sweater walking off a coastal green holding a red flagstick",
     "Tending the stick on a Scottish coastal green"),
)

photo_row_b = photos(
    ("irl-bunker-sunset",
     "A golfer in Manors playing out of a greenside bunker into low evening sun at TPC Sawgrass",
     "TPC Sawgrass &middot; greenside, last light"),
    ("irl-cliff-swing",
     "A golfer in a navy Manors shirt swinging on a clifftop tee above the ocean",
     "Clifftop tee &middot; the shirt as outerwear"),
    ("irl-pines",
     "A golfer in a striped Manors polo and olive trousers addressing a ball among pines",
     "Striped polo, olive trouser, pine straw"),
)

photo_row_c = photos(
    ("irl-dune-run",
     "A golfer in a navy Manors shirt running up a grassed dune",
     "Between shots at Machrihanish"),
    ("irl-caddie-bib",
     "A man in a black Manors caddie bib walking away across a desert course in Arizona",
     "Arizona &middot; the caddie bib"),
    ("irl-carrybag",
     "A golfer in a navy Manors sweater vest and cream shirt carrying a bag on a coastal course",
     "Sweater vest and carry bag, Scotland"),
)

photo_row_d = photos(
    ("irl-divot",
     "A golfer in a striped Manors polo and olive cap spraying a divot on a fairway",
     "Striped polo, olive cap, divot"),
    ("irl-redrock",
     "A golfer in Manors walking a desert course beneath a red rock wall",
     "Red rock, olive kit"),
    ("irl-gorse-swing",
     "A golfer in a Manors beanie mid-swing on a Scottish links course, gorse in the foreground",
     "Scotland, into the wind"),
)

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
<meta property="og:image" content="https://thegrassyissue.com/images/manors/hero.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE_PLAIN}" />
<meta name="twitter:description" content="They said nobody needed a technical polo. Then they became a technical golf brand." />
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
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {faq_schema}
 ]
}}
</script>
{css_main}
</head>
<body>
{nav}

<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Manors, Revisited</div>

<header class="drop-header">
  <h1>Manors Golf, Revisited &mdash; The Brand That Rejected Technical Golf, Then Became a Technical Golf Brand</h1>
  <div class="drop-meta">
    <span>September 2, 2026</span><span class="dot"></span>
    <span>London &middot; est. 2019</span><span class="dot"></span>
    <span>16 pieces &middot; $68&ndash;$284</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a green Manors shirt at the top of his backswing on a desert course in Arizona, a red rock butte behind him" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>Manors is a London golf label founded in 2019 by two school friends who could not find clothes they wanted to play in. Seven years on it sells Polartec polos, recycled technical trousers and quarter-zip mid-layers &mdash; which is remarkable mainly because the brand was built on the argument that none of that matters.</p>
    <p>The founding pitch was explicit. Jojo Regan and Luke Davies had been playing together through the summer of 2018 dressed nothing like golfers, and concluded that the industry was solving a problem they did not have. Nick Watts joined as Fashion Director and pointed the aesthetic at golf&rsquo;s golden age &mdash; Palmer, Player, Nicklaus &mdash; under a line the brand still uses: <strong>personality before performance</strong>.</p>
    <p>The brand went dark on social in spring 2023 and came back as a technical golf brand. What follows is who they were, what changed, the three collaborations that mark the arc, and what is actually hanging on the rail now &mdash; because the most interesting thing about the current range is that both halves of the argument are still on it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2019, London</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Regan &amp; Davies</span></div>
      <div class="sidebar-detail"><span class="l">Fashion Dir.</span><span>Nick Watts</span></div>
      <div class="sidebar-detail"><span class="l">Rebrand</span><span>Spring 2023</span></div>
      <div class="sidebar-detail"><span class="l">Collabs</span><span>adidas, Reebok, Gentleman Jack</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$68&ndash;$284</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Reversible V-Neck Vest</span></div>
      <a href="https://manorsgolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Manors ↗</a>
      <div class="hashtags">
        <span class="hashtag">#Manors</span>
        <span class="hashtag">#BrandRevisited</span>
        <span class="hashtag">#LondonGolf</span>
        <span class="hashtag">#ReebokXManors</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  </aside>
</div>

<section class="products" style="margin-top:4px;">
  <h2 id="the-pictures">What the Pictures Are Doing</h2>
  <p class="cat-kicker"><strong>Photography &middot; Manors Journal</strong>The clearest read on Manors is not the product page. It is the Journal &mdash; trips to Royal Dornoch, Machrihanish Dunes, Arizona and the Players, shot like a magazine rather than a catalogue. The clothes are on people who are playing badly in weather, which is the argument the brand has been making since 2019. All photography below is Manors&rsquo; own.</p>
  {photo_row_a}
</section>

<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;We didn&rsquo;t need a technical polo. If I&rsquo;m wearing a sweat-wicking performance polo, it&rsquo;s not going to be the difference between me hitting 89 or 79.&rdquo;<span class="pull-quote-attr">&mdash; Jojo Regan, co-founder, to Hypebeast, 2021</span></div>
</div>

<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr">Who They Were</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Regan grew up in the game. Davies came to it late. They played together through the summer of 2018 dressed completely differently &mdash; Regan in nothing that resembled golf clothing, Davies in streetwear &mdash; and the gap between what they wore and what the industry sold them became the business.</p>
    <p style="margin-top:16px">The critique was not that technical apparel was bad. It was that it was aimed at the wrong person. &ldquo;The game is very committed to focusing on the technical side, the performance, hitting bombs, hitting the balls harder, faster and further,&rdquo; Regan told Hypebeast in 2021. &ldquo;We were just about trying to break 90, or 80 on a very good day.&rdquo;</p>
    <p style="margin-top:16px">The second half of the pitch was about class, and it is the part that has aged best. Manors&rsquo; own site called golf &ldquo;the snobbish sport of suburbia&rdquo; and its perception &ldquo;uptight, entrenched in tradition and deeply unstylish.&rdquo; Regan put it more plainly: the country-club stereotype &ldquo;frustrates us because it&rsquo;s wrong. You have hackers up and down the country who aren&rsquo;t part of a club, or are part of a club because it&rsquo;s a community. That message was being lost.&rdquo; The brand backed it up by endorsing Adem Wahbi, then ranked among the world&rsquo;s top 50 golfers with disabilities.</p>
  </div>
</section>

<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;We look at a lot of archive footage, and I couldn&rsquo;t believe how well the old golfers dressed. The great thing is, everyone is dressed in these outfits. It&rsquo;s not just the golfers, it&rsquo;s also the audience. Even the caddies look great.&rdquo;<span class="pull-quote-attr">&mdash; Nick Watts, Fashion Director, to Hypebeast, 2021</span></div>
</div>

<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr">A Change of Course</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>In spring 2023 Manors deleted its social history and started again. The repositioning was called <strong>A Change of Course</strong>, handled by Stink Studios, and it moved the brand from a heritage-leaning lifestyle label to a technical golf brand &mdash; the exact category the founders had spent four years arguing was solving the wrong problem.</p>
    <p style="margin-top:16px">The reported results are strong, with one caveat about where they come from. A marketing case study of the reposition puts Manors up <strong>859% year on year</strong> with a shift away from wholesale toward direct-to-consumer. That figure comes from an industry newsletter rather than a filing or trade press, so hold it loosely. What can be seen from outside is harder to argue with: a Harrods stockist, a Reebok collaboration, and Manors turning up as a playable skin in 2K&rsquo;s PGA Tour 2025.</p>
    <p style="margin-top:16px">The reversal reads less like a contradiction the closer you look at the clothes. The original argument was about who golf apparel was designed for, not what it was made of. A Polartec polo cut loose enough to wear off the course is still answering Regan&rsquo;s question; it just stopped pretending fabric was the enemy.</p>
  </div>
  <div style="margin-top:30px">{photo_row_b}</div>
  <div>{photo_row_c}</div>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>The range of terrain is the other tell. A brand arguing that golf clothing was designed for the wrong person has to show the clothing on courses that are not the same manicured parkland every time &mdash; Scottish links in a gale, Arizona desert, a clifftop above the Atlantic, pine straw in Florida. The kit reads the same in all four.</p>
  </div>
  <div style="margin-top:26px">{photo_row_d}</div>
</section>
{sections_html}
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">Frequently Asked</h2>
  <div class="faq">
    {faq_html}
  </div>
</section>

<section class="more">
  <div class="more-hdr">
    <span class="more-label">More from TGI</span>
    <a href="/" class="more-link">Back to Feed &rarr;</a>
  </div>
  <div class="more-grid">
    <a href="/drops/manors-ss26" class="more-card">
      <div class="more-card-img"><img src="/images/manors/rbk-harrington.jpg" alt="Manors SS26" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Manors SS26 &mdash; The Drop</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/apc-golf-cph-golf-collab" class="more-card">
      <div class="more-card-img"><img src="/images/apcph-golf/polo-1.jpg" alt="A.P.Cph/Golf" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">A.P.Cph/Golf &mdash; Paris Meets Tokyo</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/best-golf-streetwear-brands-2026" class="more-card">
      <div class="more-card-img"><img src="/images/manors/old-clubpolo.jpg" alt="The best golf streetwear brands" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Best Golf Streetwear Brands</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "brand-to-know-manors.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
print("wrote %s | words: %d | cards: %d" % (out, words, page.count('class="product-card"')))
