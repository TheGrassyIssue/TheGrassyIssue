#!/usr/bin/env python3
"""build-publicdrip-fw26.py — Public Drip FW26: Nightshift drop post.

Chassis cloned from drops/reebok-x-manors-ii.html (bold headers, gallery CSS/JS,
house FAQ). Product data verified live via publicdrip.com Shopify JSON on
2026-08-31; all 13 pieces in stock at build time. Images local in
images/publicdrip-fw26/ (4 frames per product).
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
ch = open(os.path.join(S, "drops", "reebok-x-manors-ii.html"), encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

KICKER_CSS = ("/*TGI-KICKER-V1*/\n.cat-kicker{font-family:var(--sans);font-size:15px;"
    "line-height:1.75;color:#3f443e;margin:0 0 36px;max-width:70ch;"
    "border-left:3px solid var(--rough);padding:4px 0 4px 18px}")
if "TGI-KICKER-V1" not in css_main:
    css_main = css_main.replace("</style>", KICKER_CSS + "\n</style>", 1)

URL   = "https://thegrassyissue.com/drops/public-drip-fw26-nightshift"
TITLE = "Public Drip FW26: Nightshift &mdash; Brooklyn&rsquo;s Muni Label Goes Dark for Fall"
TITLE_PLAIN = "Public Drip FW26: Nightshift — Brooklyn's Muni Label Goes Dark for Fall"
DESC  = ("Public Drip's FW26 Nightshift drop, released August 21: waffle knit polos, herringbone "
         "half zips, double-pleated trousers and indigo denim hats in a coffee-and-charcoal fall "
         "palette. Every piece, every price, all still in stock.")

IMG = "/images/publicdrip-fw26"
PD  = "https://publicdrip.com/products"

def card(handle, base, name, price, frames, desc, alt):
    gal_frames = "".join(
        '<div class="pg-frame"><img src="%s/%s-%d.jpg" alt="%s &middot; view %d of %d" loading="lazy" /></div>'
        % (IMG, base, i, alt, i + 1, frames) for i in range(frames))
    dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                   % (" on" if i == 0 else "", i, i + 1) for i in range(frames))
    return ('<div class="product-card" data-frames="%d">'
            '<div class="product-gallery"><div class="pg-track">%s</div>'
            '<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div></div>'
            '<div class="product-body">'
            '<div class="product-brand">Public Drip</div>'
            '<div class="product-name">%s &middot; %s</div>'
            '<div class="product-desc">%s</div>'
            '<a href="%s/%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>'
            '</div></div>'
            % (frames, gal_frames, frames, dots, name, price, desc, PD, handle))

SECTIONS = [
 ("The Knits",
  "Four colorways of one idea: a long-sleeve polo in textured waffle knit, cut from a nylon-elastane blend with four-way stretch and a spread collar. It reads sweater from across the room and plays like a performance shirt.",
  [
   ("triborough-waffle-knit-polo-dark-slate", "waffle-knit-polo-dark-slate", "Triborough Waffle Knit Polo (Dark Slate)", "$110", 4,
    "The pick of the four &mdash; a grey-blue that works over anything in the drop. The 80/20 nylon-elastane knit dries quick, and the four-button placket sits under a spread collar that holds its shape.",
    "Public Drip Triborough Waffle Knit Polo in dark slate"),
   ("triborough-waffle-knit-polo-coffee", "waffle-knit-polo-coffee", "Triborough Waffle Knit Polo (Coffee)", "$110", 4,
    "The colorway that names the palette. Same waffle texture and stretch, in the brown that runs through the whole collection.",
    "Public Drip Triborough Waffle Knit Polo in coffee"),
   ("triborough-waffle-knit-polo-navy", "waffle-knit-polo-navy", "Triborough Waffle Knit Polo (Navy)", "$110", 4,
    "The quiet one. Navy waffle knit with the tonal placket &mdash; the version you can wear to work without anyone asking about your handicap.",
    "Public Drip Triborough Waffle Knit Polo in navy"),
   ("triborough-waffle-knit-polo-black", "waffle-knit-polo-black", "Triborough Waffle Knit Polo (Black)", "$110", 4,
    "Black on black, collar to cuff. Pairs with the charcoal Anywhere pants for the full after-dark fit.",
    "Public Drip Triborough Waffle Knit Polo in black"),
  ]),
 ("The Layers",
  "The mock neck returns from summer in a long-sleeve cotton version, and the new Herringbone Half Zip does the heavy lifting &mdash; a cotton-blend knit in a woven-look herringbone with a gold YKK zipper.",
  [
   ("the-herringbone-half-zip-coffee", "herringbone-half-zip-coffee", "The Herringbone Half Zip (Coffee)", "$140", 4,
    "The piece of the drop. Classic herringbone texture in a soft cotton-poly knit, felt P appliqu&eacute; and script embroidery, finished with the gold zipper pull.",
    "Public Drip Herringbone Half Zip in coffee"),
   ("the-herringbone-half-zip", "herringbone-half-zip-cream", "The Herringbone Half Zip (Cream)", "$140", 4,
    "Same knit in off-white &mdash; the layer for the first cold-front round of the fall.",
    "Public Drip Herringbone Half Zip in cream"),
   ("public-athlete-long-sleeve-mock-coffee", "pa-long-sleeve-mock-coffee", "Public Athlete Long Sleeve Mock (Coffee)", "$110", 4,
    "The player&rsquo;s shirt with sleeves &mdash; 100% cotton mock neck with the script logo at the chest and a tonal P on the sleeve. True to size.",
    "Public Drip Public Athlete Long Sleeve Mock in coffee"),
   ("public-athlete-long-sleeve-mock-cream", "pa-long-sleeve-mock-cream", "Public Athlete Long Sleeve Mock (Cream)", "$110", 4,
    "The cream version, for the Tiger-Sunday-red crowd who&rsquo;d rather dress like a &rsquo;70s club champion.",
    "Public Drip Public Athlete Long Sleeve Mock in cream"),
  ]),
 ("The Trousers",
  "The Anywhere Pleated Pant gets two new fall fabrics. Double pleats and a straight-leg taper off the classic suit trouser, cut in a lightweight nylon blend with stretch &mdash; the same course-to-dinner brief as the summer versions.",
  [
   ("anywhere-pleated-pants-pinstripe", "anywhere-pleated-pants-pinstripe", "Anywhere Pleated Pants (Pinstripe)", "$170", 4,
    "The loudest quiet pant in golf right now &mdash; a chalk pinstripe on charcoal that reads boardroom until you see the swing gusset.",
    "Public Drip Anywhere Pleated Pants in pinstripe"),
   ("anywhere-pleated-pants-charcoal", "anywhere-pleated-pants-charcoal", "Anywhere Pleated Pants (Charcoal)", "$170", 4,
    "The solid. Double pleats, sharp taper, and enough stretch that the dress-pant look is a costume, not a constraint.",
    "Public Drip Anywhere Pleated Pants in charcoal"),
  ]),
 ("The Finish",
  "The drop closes with indigo denim headwear and a marker set in a faux-suede pouch &mdash; the pieces that keep it under $70.",
  [
   ("p-script-denim-bucket-indigo", "denim-bucket-indigo", "&ldquo;P&rdquo; Script Denim Bucket (Indigo)", "$65", 4,
    "Raw-denim bucket with the felt P front and center and branded tape in the lining. Built to fade the way denim should.",
    "Public Drip P Script Denim Bucket in indigo"),
   ("p-script-denim-snapback-indigo", "denim-snapback-indigo", "&ldquo;P&rdquo; Script Denim Snapback (Indigo)", "$60", 4,
    "The flat-brim version of the same idea &mdash; indigo denim, gold script, two sizes.",
    "Public Drip P Script Denim Snapback in indigo"),
   ("3-pack-drip-marker", "3-pack-drip-marker", "Script Drip 3-Pack Marker Set", "$45", 3,
    "Three gold metal markers &mdash; green, black and maroon &mdash; with a drip alignment line, in a faux-suede pouch. The stocking stuffer of the drop.",
    "Public Drip Script Drip ball marker three pack with pouch"),
  ]),
]

FAQS = [
 ("What is Public Drip's FW26 Nightshift drop?",
  "Nightshift is Public Drip's Fall/Winter 2026 collection, released August 21, 2026. It runs 13 pieces: the Triborough Waffle Knit Polo in four colors, the Herringbone Half Zip in coffee and cream, long-sleeve Public Athlete Mocks, two new Anywhere Pleated Pants fabrics, indigo denim headwear and a ball marker set."),
 ("How much does the Nightshift collection cost?",
  "Pieces run $45 to $170. The marker set is $45, denim hats are $60 to $65, knits and mocks are $110, the Herringbone Half Zip is $140 and the Anywhere Pleated Pants are $170. Public Drip ships free in the US on orders over $175."),
 ("What is the Triborough Waffle Knit Polo made of?",
  "An 80% nylon, 20% elastane waffle knit with four-way stretch and quick-dry performance, with a spread collar, four-button placket and a silicone P applique. It comes in black, coffee, dark slate and navy."),
 ("Who is Public Drip?",
  "Public Drip is a Brooklyn golf label born out of New York's municipal golf scene — the name is a bet that public-course golf can dress as well as the private kind. TGI profiled the brand in full in our Brand to Know piece."),
 ("Is the Nightshift drop still in stock?",
  "As of August 31, 2026, all 13 pieces were in stock in most sizes. Two pieces from the wider August release — the short-sleeve Public Athlete Polo in white and storm — had already sold out, so the knits are the ones to move on."),
]

faq_schema = ",\n  ".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (json.dumps(q), json.dumps(a)) for q, a in FAQS)
faq_html = "\n    ".join(
    '<details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)

sections_html = ""
for hdr, kick, cards in SECTIONS:
    sections_html += ('\n<section class="products" style="margin-top:40px;">\n'
        '  <h2 class="products-hdr">%s</h2>\n'
        '  <p class="cat-kicker">%s</p>\n'
        '  <div class="products-grid">\n    %s\n  </div>\n</section>\n'
        % (hdr, kick, "\n    ".join(card(*c) for c in cards)))

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
<meta property="og:image" content="https://thegrassyissue.com/images/publicdrip-fw26/herringbone-half-zip-coffee-0.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE_PLAIN}" />
<meta name="twitter:description" content="13 pieces, $45&ndash;$170, dropped August 21. Waffle knits, herringbone, pinstripes, indigo denim." />
<link rel="canonical" href="{URL}" />
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "Article",
 "headline": "{TITLE_PLAIN}",
 "description": "{DESC}",
 "url": "{URL}",
 "datePublished": "2026-08-31",
 "dateModified": "2026-08-31",
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
  Public Drip FW26</div>

<header class="drop-header">
  <span class="drop-tag flag">[Drops &amp; Brands]</span>
  <h1>Public Drip FW26: Nightshift &mdash; Brooklyn&rsquo;s Muni Label Goes Dark for Fall</h1>
  <div class="drop-meta">
    <span>August 31, 2026</span><span class="dot"></span>
    <span>Dropped Aug 21 &middot; 13 pieces &middot; $45&ndash;$170</span><span class="dot"></span>
    <span>Status checked Aug 31, 2026</span>
  </div>
</header>

<div class="writeup">
  <div class="writeup-body">
    <p>Public Drip called its fall collection Nightshift, and the name does the describing: coffee, cream, charcoal, black, navy and raw indigo, cut for the round that starts after work and ends somewhere that isn&rsquo;t a golf course. Thirteen pieces, released August 21, all still in stock as we write this.</p>
    <p>The <a href="/drops/public-drip-brooklyns-muni-born-golf-label" style="border-bottom:1px solid var(--ink)">Brooklyn label</a> built its reputation on making New York muni golf look like a scene rather than a compromise, and Nightshift is its most tailored outing yet. The centerpiece moves are a waffle-knit long-sleeve polo that reads sweater but plays like a performance shirt, a herringbone half zip with a gold YKK pull, and the Anywhere Pleated Pant in a chalk pinstripe that would pass at a downtown office.</p>
    <p>The drop is built for the golfer whose tee time and dinner reservation share a fit. Nothing here needs a locker room between the 18th and the rest of the night &mdash; that has always been the Public Drip pitch, just never this dressed up. The knits move first at this brand, and the two short-sleeve polos from the same August release are already gone, so the waffle four-pack is where to start. Sizing runs true across the collection, and the pants carry the same fit as the summer Anywhere versions if you already own a pair.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brand</span><span>Public Drip</span></div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>FW26: Nightshift</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>Aug 21, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>13</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$45&ndash;$170</span></div>
      <div class="sidebar-detail"><span class="l">From</span><span>Brooklyn, NY</span></div>
      <a href="https://publicdrip.com/collections/fall-winter-26" target="_blank" rel="noopener" class="sidebar-cta">Shop the Drop ↗</a>
      <div class="hashtags">
        <span class="hashtag">#PublicDrip</span>
        <span class="hashtag">#Nightshift</span>
        <span class="hashtag">#FW26</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#GolfDrops</span>
      </div>
    </div>
  </aside>
</div>
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
    <a href="/drops/public-drip-brooklyns-muni-born-golf-label" class="more-card">
      <div class="more-card-img"><img src="/images/feed/c7ba29a9-DSC06723.jpg" alt="Public Drip — Brooklyn's muni-born golf label" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Public Drip &mdash; Brooklyn&rsquo;s Muni-Born Golf Label</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/best-golf-streetwear-brands-2026" class="more-card">
      <div class="more-card-img"><img src="/images/streetwear26/hero.jpg" alt="The 5 best golf streetwear brands in 2026" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The 5 Best Golf Streetwear Brands in 2026</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/students-golf-summer-2026" class="more-card">
      <div class="more-card-img"><img src="/images/studentsgolf-summer26/slide-pants.jpg" alt="Students Golf Summer 2026 drop" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Students Golf &mdash; Summer 2026 Drop</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "public-drip-fw26-nightshift.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
cards_n = page.count('class="product-card')
print("wrote", out, "| words:", words, "| cards:", cards_n)
