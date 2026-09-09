#!/usr/bin/env python3
"""Drop — Manors Golf, The Honourable Company AW26.

Sequel to drops/manors-golf-ss26-collection.html (2026-06-15), which is the
seasonal-collection slot. NOT a competitor to brand-to-know-manors.html; the
Brand Revisited rule covers BTK pages, and a genuinely new season gets its own
Drop post (precedent: reebok-x-manors-ii.html).

DATA SOURCING NOTE
------------------
manorsgolf.com is no longer a Shopify-fronted storefront: it is a headless
Next.js app, so /products.json, /products/<handle>.json and
/collections/<c>/products.json ALL return a 404 HTML shell. Every price, name,
stock state and image here came from the per-product JSON-LD <script> block.
Two handles contain a literal ® character (heritage-primaloft®-cardigan,
1-4-zip-primaloft®-mid-layer); a [a-z0-9-]+ handle regex silently truncates
them and both product pages 404. They must be URL-encoded.

Handles do NOT match product names. Stableford Trousers lives at /work-trousers
and Club Pant at /club-trousers. Guessing handles from titles would have
produced two dead links, which is the Bluegrass Fairway lesson applied.

SEASON CODES. The SKU carries the season: M-AW26-... Ranger Beanie is 24AW and
Retro Crown Cap / Tech Cap are 26AW. The Ranger Beanie is therefore a carryover
and is DELIBERATELY EXCLUDED — it is not part of this drop and must not be sold
as new. The two 26AW caps are current-generation and are included.

IMAGERY. Product frames are Manors' own packshot/on-model photography, matched
to each product by the CANONICAL JSON-LD image filename prefix (e.g.
MERINO_TECH_HOODIE_), not by name tokens. Token matching cross-contaminated
badly — "TECH" and "CAP" pulled cap photography onto the Merino Hoodie,
Windbreaker, Crewneck and Ripstop Vest. Colour tokens must be matched at a
boundary or GREEN matches inside GREENSKEEPER.

The hero is Manors' own IRL course photography from their Sanity CMS. It is
brand imagery, NOT an AW26 campaign shot, and the alt text describes only what
is visible — no seasonal claim.

Deliberately NOT asserted (no source found):
  - that any piece is made in a named country (no manufacturing origin published)
  - a fabric mill, factory or supplier for any garment
  - that AW26 is tied to The Addington or the /journal M25 piece (adjacent
    editorial, published Oct 2025, with no stated link to the collection)
  - sell-through, units, or that anything is limited
  - any founder quote about AW26 — none exists. The only quoted lines are the
    collection statement and product copy, both labelled as Manors' own writing.
"""
import re, os, json

SLUG  = "manors-golf-aw26-collection"
TITLE = "Manors&rsquo; Honourable Company AW26 &mdash; Dressed for the Sub-Four-Hour Round"
PLAIN = "Manors' Honourable Company AW26 — Dressed for the Sub-Four-Hour Round"
DESC  = ("Manors Golf's AW26 Honourable Company collection: merino mid-layers, Primaloft insulation, "
         "Cordura ripstop and pleated trousers. Twenty-two pieces with prices, and what the fabrics actually do.")
B = "https://manorsgolf.com/products/"
IMG = "/images/manors-aw26/"

# (image-slug, display name, url-handle, price, copy)
MID = [
 ("merino-tech-hoodie","Merino Tech Hoodie","merino-tech-hoodie","$305",
  "The most expensive piece in the collection and the one that explains it. Merino regulates temperature across a wider band than synthetic fleece, which matters on a round that starts cold and finishes warm. A hood on a golf sweater is a choice &mdash; it reads off-course, and Manors has never pretended its clothes stop working at the car park."),
 ("merino-tech-windbreaker","Merino Tech Windbreaker","merino-wool-1-4-windbreaker","$292",
  "A quarter-zip in the same Dune colourway, cut as a wind layer rather than a sweater. Merino against wind is an old idea executed with modern seaming; the collar sits high enough to cover the back of the neck when the temperature drops on the closing stretch."),
 ("merino-tech-crewneck","Merino Tech Crewneck","merino-wool-crewneck","$244",
  "The plainest thing Manors makes this season and probably the most wearable. A crew-neck merino sweater in Dune, no zip, no branding beyond the small chequer at the chest. This is the piece that survives the collection being fashionable."),
 ("heritage-primaloft-cardigan","Heritage Primaloft&reg; Cardigan","heritage-primaloft%C2%AE-cardigan","$217",
  "Burgundy and ivory, buttoned, insulated with Primaloft. A cardigan on a golf course is a deliberately old-fashioned silhouette, and the synthetic fill is the concession to actually playing in it &mdash; Primaloft keeps working when it gets damp, which wool cardigans famously do not."),
 ("quarter-zip-primaloft","1/4 Zip Primaloft&reg; Mid-Layer","1-4-zip-primaloft%C2%AE-mid-layer","$190",
  "The cardigan's practical sibling in the same burgundy and ivory. Quarter-zip, insulated, cut to go under a shell. If you buy one insulated layer from this collection and expect to play in weather, it is more likely to be this one."),
 ("highland-mockneck-fleece","Highland Mockneck Fleece","highland-mockneck-fleece","$163",
  "Black, mock-necked, fleece-backed and made partly from recycled fabric. The mockneck is doing the same job as the windbreaker's collar for half the money, with more give in the shoulders."),
 ("quarter-zip-lightweight","1/4 Zip Lightweight Mid-Layer","lightweight-1-4-zip-tech-mid-layer","$122",
  "Powder blue and the thinnest layer in the range &mdash; a long-sleeve to put over a polo in early autumn rather than anything you would call insulation. The cheapest way into the mid-layer group."),
]

WIND = [
 ("crosswind-cordura-vneck","Crosswind Cordura&reg; V-Neck","crosswind-cordura-vneck","$265",
  "Cordura ripstop nylon, a fabric originally developed for military use, cut into a V-neck wind top. It carries a PFC-free water-repellent finish, side vent zips and concealed pockets with internal compartments. Manors' own product copy ends the technical spec with a line that tells you exactly who the collection is for: &ldquo;You will also look very good in a warm pub.&rdquo;"),
 ("ripstop-tech-vest","Ripstop Tech Vest","ripstop-tech-vest","$217",
  "A gilet in recycled ripstop with a water-resistant finish, in Dune and Steel. The vest is the layer that solves the actual autumn problem &mdash; a cold core and arms that need to swing &mdash; and it is the piece in this collection most likely to live in a bag year-round."),
 ("tour-shirt","Tour Shirt","tour-shirt","$163",
  "A short-sleeved wind top at 148gsm with four-way stretch, inspired by vintage wind proofs. Bonded YKK centre-front zip, adjustable hem with cord and toggle, raglan sleeves and curved panelling. Short sleeves on a wind layer sounds like a contradiction until the first genuinely blustery warm day."),
]

TROUSERS = [
 ("ripstop-tech-trouser","Ripstop Tech Trouser","ripstop-tech-trouser","$204",
  "The vest's matching half, in the same recycled ripstop with a water-resistant finish. Cut wide and pleated rather than tapered, which is the single clearest signal that Manors is designing for people who dress this way off the course too."),
 ("stableford-trousers","Stableford Trousers","work-trousers","$190",
  "Vintage indigo, wrinkle-resistant, soft-handed. Named for the scoring format that rewards a good hole and forgives a blow-up &mdash; which is a reasonable summary of the whole collection's attitude to a round of golf."),
 ("recycled-greenskeeper-trouser","Recycled Greenskeeper Trouser","recycled-greenskeeper-trouser","$177",
  "Ivory, four-way stretch, water-resistant, recycled fabric. Named after the people who are on the course before anyone else and dressed for a full day outdoors, which is the reference Manors keeps returning to."),
 ("club-pant","Club Pant","club-trousers","$163",
  "Black, four-way stretch, water and wind resistant. The most conservative trouser here and the one that will pass unremarked at a club with a dress code &mdash; the reason it exists."),
 ("stableford-short","Stableford Short","stableford-shorts","$129",
  "The Stableford in short form, vintage indigo, wrinkle-resistant and cut from recycled fabric. A short in an autumn-winter collection is Manors acknowledging that a good part of its customer base does not live somewhere with a real winter."),
]

POLOS = [
 ("ranger-mockneck-polo","Ranger Mockneck Polo","mockneck-ranger-polo","$129",
  "Black, mock-necked, with moisture management, odour control and UV protection. Panelled at the shoulder in a way that reads closer to technical outerwear than to a polo, and the most modern-looking shirt in the collection."),
 ("links-pique-polo","Links Pique Polo","links-pique-polo","$129",
  "A pique polo with four-way stretch and a soft hand. Pique is the traditional golf-shirt fabric and this is the collection's most straightforward use of it &mdash; the check pattern does the talking."),
 ("goat-pique-polo","GOAT Pique Polo","goat-pique-polo-stripe","$116",
  "Striped pique in burgundy. The stripe is set wide enough to read from across a fairway, which is either the appeal or the objection depending on how you feel about being visible."),
 ("pine-course-polo","Pine Course Polo","pine-course-polo","$116",
  "The print piece. A dense botanical pattern across the whole shirt, in the Course Polo body with moisture management and odour control. Every collection needs one shirt that is a decision rather than a default."),
 ("arc-polo","Arc Polo","arc-polo","$129",
  "Panelled at the sides in a contrasting tone, with moisture management, odour control and UV protection. The panelling is the only structural styling on any polo here, and it is subtle enough to survive a strict dress code."),
]

CAPS = [
 ("retro-crown-cap","Retro Crown Cap","retro-crown-cap","$61",
  "A flat-brimmed, high-crown five-panel in burgundy and black with MANORS across the front. The most overtly retro thing in the collection and the piece doing the most work to place the brand outside traditional golf."),
 ("course-cap","Course Cap","course-cap","$48",
  "The plain one. An unstructured cap in Dune with the chequer mark at the front, at the lowest price point in the collection. The cap you buy to find out whether you like the brand."),
]

ALL = MID + WIND + TROUSERS + POLOS + CAPS

def frames(s):
    n = 1
    while os.path.exists(f"images/manors-aw26/{s}-a{n+1}.jpg"): n += 1
    return n

def gal(s, name):
    n = frames(s)
    pl = re.sub(r'<[^>]+>|&[a-z]+;', '', name)
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}.jpg" alt="Manors {pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}{"" if i==0 else f"-a{i+1}"}.jpg" '
                 f'alt="Manors {pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def sec(hdr, kicker, items):
    c = "\n    ".join(
     f"""<div class="product-card" data-frames="{frames(sl)}">
      {gal(sl, nm)}
      <div class="product-body">
        <div class="product-brand">Manors Golf</div>
        <div class="product-name">{nm} &middot; {pr}</div>
        <div class="product-desc">{d}</div>
        <a href="{B}{h}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>""" for sl, nm, h, pr, d in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>The Honourable Company is Manors&rsquo; autumn-winter 2026 collection: twenty-two pieces built around merino, Primaloft insulation and Cordura ripstop, priced from a $48 cap to a $305 hooded sweater. It is a layering collection, which is the correct answer to a season where the first tee is cold and the ninth is not.</p>
    <p>The name points at the Honourable Company of Edinburgh Golfers, the club that wrote the first surviving rules of golf in 1744. Manors has spent its whole existence borrowing that formal vocabulary &mdash; Stableford, Greenskeeper, Ranger, Club &mdash; and then cutting the trousers wide and pleated. The collection statement is the brand&rsquo;s own and sets the terms plainly: this is for <em>&ldquo;the Scrambler in every golfer who appreciates good company, great shots and a round wrapped up in less than four hours.&rdquo;</em></p>
    <p>If you play in genuine cold, the mid-layers are the reason to look. If you mostly want golf clothes that do not announce themselves as golf clothes in a bar afterwards, that is the same collection from a different angle &mdash; and it is the angle Manors writes to.</p>
  </div>
</div>
"""

FABRIC = """<section class="products">
  <h2 class="products-hdr">What the Fabrics Actually Do</h2>
  <p class="cat-kicker">Three material choices carry most of the collection, and each one solves a different autumn problem.</p>
  <div class="writeup-body">
    <p><strong>Merino.</strong> Four pieces &mdash; the Hoodie, Windbreaker, Crewneck and the wool mid-layers &mdash; run on merino, listed with moisture management, insulation and odour control. Merino&rsquo;s advantage over synthetic fleece is range: it holds warmth when the temperature drops and sheds it when you start walking uphill, so one layer covers a wider band of conditions. Its other property is the unglamorous one &mdash; it resists smelling after repeated wear, which is why it dominates hiking and has taken so long to reach golf.</p>
    <p><strong>Primaloft.</strong> The Heritage Cardigan and the 1/4 Zip Mid-Layer are insulated with Primaloft, a synthetic fill originally developed as a down substitute. The relevant difference from down is behaviour when wet: down clumps and stops insulating, synthetic fill largely does not. On a course, in autumn, that is the whole argument.</p>
    <p><strong>Cordura ripstop.</strong> The Crosswind V-Neck uses high-tenacity Cordura nylon ripstop, a fabric first developed for military use, with a PFC-free water-repellent finish. Ripstop is woven with a reinforcing grid so a puncture stops rather than runs; Cordura is the abrasion-resistant version. It is more fabric than a round of golf strictly requires, which is a reasonable description of the appeal.</p>
    <p>The recycled content is spread across the trousers and the vest rather than concentrated in a single &ldquo;sustainable&rdquo; capsule &mdash; the Ripstop Vest and Trouser, the Recycled Greenskeeper Trouser, the Stableford Short and the Highland Fleece all list recycled fabric among their properties.</p>
  </div>
</section>
"""

CONTEXT = """<section class="products">
  <h2 class="products-hdr">Reading the Collection</h2>
  <p class="cat-kicker">Prices, silhouettes and one detail that tells you which pieces are actually new.</p>
  <div class="writeup-body">
    <p>The range runs $48 to $305. The mid-layers occupy the top: Merino Hoodie at $305, Merino Windbreaker at $292, Crosswind V-Neck at $265, Merino Crewneck at $244. Polos cluster between $116 and $129 and caps sit at $48 to $61, so the collection is priced like a knitwear label that also makes shirts rather than a golf brand that also makes sweaters.</p>
    <p>The silhouette is the consistent argument. Trousers are pleated and cut wide across the Ripstop, Stableford, Greenskeeper and Club Pant. Polos are boxy rather than fitted. The Retro Crown Cap is flat-brimmed and high-crowned. None of this is performance-driven &mdash; it is a set of proportions borrowed from menswear and applied to a sport that spent thirty years in tapered polyester.</p>
    <p>One practical note for anyone buying: not everything on the collection page is new. Manors encodes the season in the SKU, and while the AW26 pieces carry an AW26 code, the Ranger Beanie is coded 24AW &mdash; a carryover being sold alongside the new collection rather than part of it. The Retro Crown Cap and the Tech Cap use a 26AW code, a different generation of the same season. It is a small thing, but it is the difference between buying this year&rsquo;s collection and buying stock from two winters ago.</p>
    <p>Manors is a London brand, founded in 2019 by Charlie Coppola and Jojo Regan, and it sells in dollars to a US audience through its own site. Sizes run XS to XXL across the apparel.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is the Honourable Company AW26 collection?",
  "It is Manors Golf's autumn-winter 2026 range: twenty-two pieces built around merino mid-layers, Primaloft insulation, Cordura ripstop wind tops and pleated trousers, priced from $48 to $305. Manors describes it as being for &ldquo;the Scrambler in every golfer who appreciates good company, great shots and a round wrapped up in less than four hours.&rdquo;"),
 ("Which piece should I buy first?",
  "For playing in genuine cold, the 1/4 Zip Primaloft Mid-Layer at $190 &mdash; insulated, cut to go under a shell, and it keeps insulating when damp. For year-round use, the Ripstop Tech Vest at $217 solves the specific autumn problem of a cold core and arms that need to swing. The Course Cap at $48 is the cheapest way to try the brand."),
 ("What does the Cordura fabric on the Crosswind V-Neck do?",
  "Cordura is a high-tenacity nylon originally developed for military use, and the ripstop weave includes a reinforcing grid so a tear stops instead of running. Manors adds a PFC-free water-repellent finish, side vent zips and concealed internal pockets. It resists abrasion and sheds light rain."),
 ("Is the Ranger Beanie part of AW26?",
  "No. The Ranger Beanie's SKU carries a 24AW season code while the new pieces are AW26, so it is carryover stock listed alongside the collection rather than part of it. The Retro Crown Cap and Tech Cap use a 26AW code, which is the current generation."),
 ("How does AW26 differ from the SS26 collection?",
  "SS26 was a warm-weather range built on recycled fabrics, organic cotton and lighter colourways. AW26 moves to insulation and wind resistance &mdash; merino across four pieces, Primaloft in two, Cordura ripstop on the Crosswind &mdash; and to a darker palette of burgundy, Dune, vintage indigo and black."),
 ("Where is Manors from?",
  "London. The brand was founded in 2019 by Charlie Coppola and Jojo Regan and sells directly in US dollars. It has previously collaborated with Reebok, most recently on a second joint collection in 2026."),
]

FAQ = """<section class="products">
  <h2 class="products-hdr">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <div class="faq-q">{q}</div>\n    <div class="faq-a">{a}</div>' for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&reg;", "®").replace("&middot;", "·").replace("&hellip;", "..."))

SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]

head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com/images/manors-aw26/hero.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Manors AW26</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 8, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        '    <span>22 Pieces</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/manors-aw26/hero.jpg" '
        'alt="Three golfers on a links green under open sky, one stretched flat on the turf to read a putt, '
        'from Manors&#39; own course photography" /></div></div>\n'
        + INTRO + FABRIC
        + sec("The Mid-Layers &mdash; 7 Pieces",
              "Merino carries four of these and Primaloft fills two more, which is where the collection makes its case for autumn golf.", MID)
        + sec("Wind and Weather &mdash; 3 Pieces",
              "The layers built to be worn over the top when the forecast turns.", WIND)
        + sec("The Trousers &mdash; 5 Pieces",
              "Pleated and cut wide, which is the clearest signal of where this brand takes its proportions from.", TROUSERS)
        + sec("The Polos &mdash; 5 Pieces",
              "Manors treats the same shirt four different ways across pique, stripe, print and panelling.", POLOS)
        + sec("The Caps &mdash; 2 Pieces",
              "The cheapest entry to the collection, and the piece doing the most styling work.", CAPS)
        + CONTEXT + FAQ)

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(ALL)} products | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
