#!/usr/bin/env python3
"""build-loud-headcovers.py — The Loud Headcover Edit.

Lenny's brief, 2026-08-31: "punchy, loud headcovers. Not gimmicks or dogs but
great eye catching design. Mogshade is a great example." Selection went through
three rounds — a name-based sweep, then an image colorfulness scorer
(saturation + hue variety on the non-background pixels of every in-stock cover
across ~40 brands), which is what finally separated real colour from product
names that merely sounded loud.

Ruled out by house rules and by Lenny: novelty animals and character
illustration, pin-ups, licensed team merch, political covers, plain
leather/tweed solids, flag covers, Radry (recently over-used) and Pins & Aces.

13 picks: 10 from the TGI brand universe, 3 from outside it. Prices and stock
verified live via each store's product JSON on 2026-08-31.
Chassis cloned from drops/public-drip-fw26-nightshift.html.
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
ch = open(os.path.join(S, "drops", "public-drip-fw26-nightshift.html"), encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)

# The Nightshift chassis carries the flat .drop-hero rule (it has no hero block,
# so nobody noticed). Upgrade it to the sitewide 21:9 cover crop used on Lions,
# Hancock and every other post with a hero.
css_main = css_main.replace(
    ".drop-hero-img{width:100%;border:.5px solid var(--ink);overflow:hidden}"
    ".drop-hero-img img{width:100%;display:block}",
    ".drop-hero-img{width:100%;aspect-ratio:21/9;border:.5px solid var(--ink);overflow:hidden}"
    ".drop-hero-img img{width:100%;height:100%;object-fit:cover}")
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

URL   = "https://thegrassyissue.com/drops/loud-on-purpose-headcovers"
TITLE = "Loud on Purpose &mdash; 18 Headcovers Built on Design, Not Punchlines"
TITLE_PLAIN = "Loud on Purpose — 18 Headcovers Built on Design, Not Punchlines"
DESC  = ("Headcovers loud enough to see from the next fairway, chosen for graphic design rather "
         "than novelty: Mogshade's woven tile patterns, Devereux's iconography, Stitch's flat "
         "graphics, Fyfe's tartans and a Ferrari-red leather mallet. No dogs, no gimmicks.")

IMG = "/images/loud-headcovers"

def card(base, brand, name, price, frames, desc, alt, url):
    gal = "".join(
        '<div class="pg-frame"><img src="%s/%s-%d.jpg" alt="%s &middot; view %d of %d" loading="lazy" /></div>'
        % (IMG, base, i, alt, i + 1, frames) for i in range(frames))
    dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                   % (" on" if i == 0 else "", i, i + 1) for i in range(frames))
    controls = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
                '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
                '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>' % (frames, dots)) if frames > 1 else ""
    return ('<div class="product-card" data-frames="%d">'
            '<div class="product-gallery"><div class="pg-track">%s</div>%s</div>'
            '<div class="product-body">'
            '<div class="product-brand">%s</div>'
            '<div class="product-name">%s &middot; %s</div>'
            '<div class="product-desc">%s</div>'
            '<a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>'
            '</div></div>' % (frames, gal, controls, brand, name, price, desc, url))

SECTIONS = [
 ("Pattern Does the Talking",
  "The quietest way to be loud: no logo, no punchline, just a woven pattern strong enough to read from the cart path. Mogshade builds theirs in Portugal on the tile-work and textile traditions of the Iberian peninsula, and nobody in golf is doing it better.",
  [
   ("mogshade-deco-magenta", "Mogshade", "Deco Magenta", "$78", 2,
    "The loudest thing they make and still nothing like a novelty cover. A deco grid woven in magenta and bone, dense enough that the pattern reads as texture up close and as a block of colour from fifty yards.",
    "Mogshade Deco Magenta headcover, woven magenta and cream pattern",
    "https://mogshadegolf.com/products/deco-magenta-headcover"),
   ("mogshade-tiles-olive-orange", "Mogshade", "Tiles Olive &amp; Orange", "$78", 3,
    "Olive and burnt orange in a tile repeat that belongs on a Lisbon wall. The colour pairing is the trick &mdash; two shades that have no business working together, doing exactly that.",
    "Mogshade Tiles headcover in olive and orange",
    "https://mogshadegolf.com/products/tile-olive-orange-headcover"),
   ("fyfe-clare-county", "Fyfe Golf", "Clare County Tartan", "$69", 3,
    "Tartan is the original loud pattern and Fyfe treats it that way &mdash; a red and green Clare County check, cut and sewn in Scotland, that carries more colour than anything else in their range.",
    "Fyfe Golf Clare County tartan headcover in red and green",
    "https://fyfegolf.com/products/clare-county-headcover"),
   ("fyfe-jura-sunset", "Fyfe Golf", "Jura Sunset Harris Tweed", "$69", 3,
    "Harris Tweed woven in sunset colours &mdash; rust, gold and heather flecked through a grey ground. Proof that heritage cloth can still throw colour when the mill is willing.",
    "Fyfe Golf Jura Sunset Harris Tweed headcover",
    "https://fyfegolf.com/products/jura-sunset"),
   ("mogshade-waffle-yellow", "Mogshade", "Waffle Yellow", "$78", 2,
    "A waffle grid in school-bus yellow and cream. The third Mogshade here and the one that photographs loudest &mdash; on a bag in flat light it looks like a lit window.",
    "Mogshade Waffle Yellow headcover in yellow and cream grid",
    "https://mogshadegolf.com/products/waffle-yellow-headcover"),
   ("winston-checkerboard", "Winston Collection", "Collegiate Checkerboard Blade", "$119.99", 3,
    "Orange-and-white checkerboard in full-grain leather. The checker is the most abused pattern in golf right now, and this is the version that earns it &mdash; hand-stitched, high contrast, no logo shouting over the top.",
    "Winston Collection orange and white checkerboard leather blade putter cover",
    "https://winstoncollection.com/products/orange-white-checkerboard-blade-leather-putter-covers"),
   ("malbon-checkered", "Malbon", "Checkered Driver Cover", "$128", 3,
    "Black-and-white checker with the Malbon script kept small. Graphic, high-contrast, and the one piece here that will look at home on a bag full of blacked-out clubs.",
    "Malbon black and white checkered driver headcover",
    "https://malbon.com/products/checkered-driver-cover-black-white"),
  ]),
 ("Flat Graphic",
  "Illustration used as design rather than as a joke &mdash; iconography, lettering and colour blocking that would work as a poster if you flattened it out.",
  [
   ("dvx-guadalupe", "Devereux", "Our Lady of Guadalupe Driver", "$48", 4,
    "Devereux&rsquo;s best piece of art on a headcover: the Guadalupe figure in gold and red against chartreuse, the whole thing composed like a devotional candle. Loud, but reverent about it.",
    "Devereux Our Lady of Guadalupe driver headcover in green",
    "https://devereuxgolf.com/products/our-lady-of-guadalupe-driver-cover-green"),
   ("dvx-cactus-voodoo", "Devereux", "Cactus Voodoo Blade", "$48", 4,
    "A skeleton cactus in orange on midnight blue, drawn with proper linework rather than clip art. At $48 it is the cheapest thing here and one of the sharpest.",
    "Devereux Cactus Voodoo blade putter cover in blue and orange",
    "https://devereuxgolf.com/products/cactus-voodoo-blade-putter-cover-blue"),
   ("cayce-swing-thoughts", "Cayce Golf", "Swing Thoughts", "$65", 3,
    "Every swing thought you have ever had, hand-lettered across a navy cover in white &mdash; keep your head down, hold the finish, tempo, tempo, tempo. Funny at arm&rsquo;s length, genuinely good type up close.",
    "Cayce Golf Swing Thoughts headcover covered in hand-lettered swing tips",
    "https://caycegolf.com/products/swing-thoughts-golf-head-cover"),
   ("stitch-nice-roll", "Stitch Golf", "Nice Roll", "$78", 4,
    "Cobalt blue scattered with candy-coloured dots and a small &lsquo;Nice&rsquo; script. The colour does all the work; there is no character, no mascot, nothing to explain.",
    "Stitch Golf Nice Roll putter cover in cobalt blue with coloured dots",
    "https://stitchgolf.com/products/nice-roll-putter-cover"),
   ("stitch-warning", "Stitch Golf", "Warning", "$78", 4,
    "Fire-engine red with a skull and crossbones and CAUTION &mdash; SERIOUS INJURY set in tight condensed caps. It is a warning label, executed properly, and the type is doing as much work as the graphic.",
    "Stitch Golf Warning putter cover in red with skull and warning type",
    "https://stitchgolf.com/products/warning-putter-cover"),
   ("cayce-til-death", "Cayce Golf", "&rsquo;Til Death Bloom", "$40", 1,
    "Tattoo-flash roses and skulls in red and green on black, drawn the way an old parlour would have drawn them. The cheapest cover in the edit and the one with the most ink on it.",
    "Cayce Golf Til Death Bloom mallet putter cover with tattoo roses and skulls",
    "https://caycegolf.com/products/till-death-bloom-mallet-putter-cover"),
   ("malbon-markarian", "Malbon", "Markarian Blade", "$118", 3,
    "Sage green with a botanical line drawing running across the flank &mdash; the quietest thing in this section and still a long way from a plain cover. Proof that loud can mean confident rather than bright.",
    "Malbon Markarian blade putter cover in sage green with botanical linework",
    "https://malbon.com/products/markarian-blade-cover-sage-green"),
   ("swag-bing-bong", "Swag Golf", "New York Bing Bong", "$125", 1,
    "Swag at its most restrained, which still means blue and yellow with BING BONG in block caps across the crown. Pure typography &mdash; no illustration, no licensed logo, just New York volume.",
    "Swag Golf New York Bing Bong driver headcover in blue and yellow",
    "https://swaggolf.com/products/new-york-bing-bong-driver-cover"),
  ]),
 ("One Colour, Turned Up",
  "The other way to be loud: pick a single saturated colour and commit to it completely.",
  [
   ("stitch-lifesaver", "Stitch Golf", "Lifesaver Knit", "$78", 2,
    "Every colour at once. A ribbed knit in candy stripes finished with a multicolour pom that sits above the bag like a flag &mdash; the most cheerful object in golf and the piece we would put on our own driver.",
    "Stitch Golf Lifesaver knit headcover in rainbow stripes with pom",
    "https://stitchgolf.com/products/lifesaver-knit-head-cover"),
   ("jones-circa71-orange", "Jones Sports Co", "Circa &rsquo;71 &mdash; Orange", "$55", 3,
    "Terry cloth in a burnt seventies orange, cut to the same pattern Jones has used since 1971. One colour, one material, no graphic at all &mdash; and it still reads from the far side of the range.",
    "Jones Sports Co Circa 71 headcover in orange terry cloth",
    "https://jonessportsco.com/products/circa-71-headcover-orange"),
   ("fyfe-gt-rosso", "Fyfe Golf", "GT Rosso Scuderia Mallet", "$69", 4,
    "Ferrari red leather, shearling lining, nothing else. No pattern, no graphic, no logo doing laps &mdash; just a colour loud enough that it does not need any of them.",
    "Fyfe Golf GT Rosso Scuderia red leather mallet putter cover",
    "https://fyfegolf.com/products/gt-rosso-scuderia-leather-mallet-putter-cover"),
  ]),
]

FAQS = [
 ("What makes a headcover loud without being a gimmick?",
  "Design intent. A gimmick cover leans on the object — an animal, a mascot, a punchline — and stops being funny by the third round. A loud cover leans on pattern, colour and type, so it still reads well when the joke would have worn off. Every pick here is pattern, iconography or saturated colour rather than a novelty shape."),
 ("Which brand makes the best patterned headcovers?",
  "Mogshade, made in Portugal, whose woven tile and deco patterns are the reference point for this whole category. Their Deco Magenta and Tiles Olive & Orange are the two loudest covers we would put on a bag without hesitation."),
 ("How much do good headcovers cost?",
  "The picks here run $40 to $128. Cayce and Devereux sit at the bottom, $40 and $48, Mogshade and Stitch in the $78 range, Fyfe at $69 for leather and tweed, and Malbon, Swag and Winston at the top between $119 and $128."),
 ("Do loud headcovers fit modern drivers?",
  "The barrel-style covers here — Mogshade, Fyfe, Malbon, Swag, Cayce — are cut for 460cc heads and pull on over the crown. The blade and mallet putter covers are shape-specific, so match the cover to the putter head: blade covers will not fit a mallet, and centre-shafted mallets need their own cut."),
 ("Where are these headcovers made?",
  "Mogshade is made in Portugal, Fyfe cut and sewn in Scotland, and Devereux, Stitch, Cayce, Winston and Swag are US-made or US-assembled. Malbon's covers are produced overseas to their spec."),
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
<meta property="og:image" content="https://thegrassyissue.com/images/loud-headcovers/mogshade-deco-magenta-0.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE_PLAIN}" />
<meta name="twitter:description" content="18 headcovers chosen for graphic design, not novelty. No dogs, no gimmicks." />
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
  Loud on Purpose</div>

<header class="drop-header">
  <h1>Loud on Purpose &mdash; 18 Headcovers Built on Design, Not Punchlines</h1>
  <div class="drop-meta">
    <span>August 31, 2026</span><span class="dot"></span>
    <span>18 picks &middot; $40&ndash;$128</span><span class="dot"></span>
    <span>Status checked Aug 31, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="/images/loud-headcovers/hero.jpg" alt="A weaver standing at a manual wooden loom in the Portuguese wool mill that makes Mogshade&rsquo;s headcover textiles, striped blankets stacked on the bench beside her" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>A headcover is the one piece of equipment nobody can tell you is wrong. It does not affect ball flight, it does not need fitting, and it is the only thing on the bag you choose purely because you like looking at it. So the question is only ever whether the thing is any good to look at.</p>
    <p>Most loud covers fail that test. Golf has an enormous supply of headcovers shaped like animals, printed with punchlines, or built around a single joke that dies somewhere on the front nine. The eighteen below are the other kind: loud because of pattern, colour and type &mdash; design that would hold up printed on a poster, not just stitched onto a driver.</p>
    <p>Mogshade set the standard, which is why they open the list and take three slots. From there it runs through Devereux&rsquo;s iconography, Stitch&rsquo;s flat graphics, three from Fyfe in Scotland, and a Ferrari-red leather mallet that gets by on colour alone. Fourteen come from brands already in the TGI universe; four are from outside it. Prices run $40 to $128, and everything here was in stock when we checked.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>9</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$40&ndash;$128</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Cayce, $40</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Mogshade Deco</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 31, 2026</span></div>
      <a href="https://mogshadegolf.com/collections/headcovers" target="_blank" rel="noopener" class="sidebar-cta">Start with Mogshade ↗</a>
      <div class="hashtags">
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#GolfDesign</span>
        <span class="hashtag">#Mogshade</span>
        <span class="hashtag">#LoudGolf</span>
        <span class="hashtag">#GearEdit</span>
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
    <a href="/drops/brand-to-know-mogshade" class="more-card">
      <div class="more-card-img"><img src="/images/loud-headcovers/mogshade-tiles-olive-orange-0.jpg" alt="Mogshade — Brand to Know" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Brand to Know &mdash; Mogshade</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/the-driver-headcover-edit" class="more-card">
      <div class="more-card-img"><img src="/images/headcover-edit/mogshade-churra-mono.jpg" alt="The Driver Headcover Edit" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Driver Headcover Edit</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/public-drip-fw26-nightshift" class="more-card">
      <div class="more-card-img"><img src="/images/publicdrip-fw26/herringbone-half-zip-coffee-1.jpg" alt="Public Drip FW26: Nightshift" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Public Drip FW26: Nightshift</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "loud-on-purpose-headcovers.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
print("wrote", out, "| words:", words, "| cards:", page.count('class="product-card'))
