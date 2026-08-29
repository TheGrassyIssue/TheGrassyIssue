#!/usr/bin/env python3
"""
build-forden.py — Brand to Know: Forden Golf.

THE STORY, AND HOW IT WAS VERIFIED
----------------------------------
Forden's "SWINGMAN" logo is a reference to Harold "Doc" Edgerton's stroboscopic
golf photography. The brand states this on its own About page; I did NOT take
their word for it. Edgerton was the MIT engineer who invented the stroboscope,
and in 1938 he photographed pro Densmore Shute at 100 flashes per second for half
a second - "Densmore Shute Bends the Shaft" - capturing the shaft flexing after
impact. The print is held by Syracuse University Art Museum, the Smithsonian's
Photographic History Collection and the MIT Museum. That is the hook the post
leads on, because it is true and nobody else has written it up.

FOUNDER QUOTE - VERBATIM, SOURCED
---------------------------------
Chad Gurman, published on fordengolf.com/pages/about-us. Reproduced exactly as
printed. Per house rule: never paraphrase into quotation marks, never invent.

WHY THE TEE PACKETS LEAD (Lenny, 2026-08-28)
--------------------------------------------
"lead with those tee packages that look like newports". They do: Newport green,
gold-and-white top stripe, the wordmark in the same slab idiom, "SWING KINGS"
across the bottom where a cigarette brand puts its format. It is the most
distinctive object Forden makes and the only photograph in their whole library
that is styled rather than flat - it scored 0 on the packshot classifier where
45 of their images score 100. It is the hero and the first product.

THE IMAGERY PROBLEM - STATED PLAINLY
------------------------------------
Forden has NO on-model or lifestyle photography anywhere. All 58 product images
are flat packshots; their /pages/lookbook "Gallery" is an empty template (I
rendered it in a headless browser - the only images on it are the 238 country
flags in the currency selector). So the closing gallery is DETAIL crops, not IRL:
the umbrella canopy from beneath, the towel weave, the tin interior, an
embroidery macro. Labelled honestly as details rather than dressed up as
lifestyle. If Forden ever sends lookbook files, that section is the place for
them.

PRICES
------
Every price is the live Shopify first-variant price, verified against
products.json on 2026-08-29 and stored in research/forden-skus.json. Nearly the
whole range is discounted right now (30% off Collection II, 50% off the archive),
so `was` is printed only where a real discount exists - 14 of their 20 hats carry
compare_at == price, and two carry compare_at "0.00", which would render as a
nonsense "was $0.00" if trusted blindly.

LINK BY HANDLE, NEVER BY TITLE
------------------------------
Forden's Shopify handles do not match their titles. "Black Forden x New Era
Golfer Snapback" lives at a white-and-green-...-copy slug, and the two blade
putter covers have their colours swapped between title and handle. Handles are
stored in the SKU file for exactly this reason.
"""
import os, re, glob, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL   = os.path.join(ROOT, "drops", "the-niche-grip-report.html")
OUT   = os.path.join(ROOT, "drops", "brand-to-know-forden-golf.html")
IMGD  = "/images/forden/"
SLUG  = "brand-to-know-forden-golf"
TITLE = "Brand to Know &mdash; Forden Golf"
DESC  = ("Forden Golf's Swingman logo comes from Doc Edgerton's 1938 strobe photograph of a golf "
         "swing at MIT. The New Era hat line, the Swing Kings tee packets, and 19 pieces from "
         "Collection II.")
META  = json.load(open(os.path.join(ROOT, "research", "forden-skus.json"), encoding="utf-8"))
SHOP  = "https://www.fordengolf.com/products/"


def frames(key, limit=4):
    # Match ONLY key-<digits>.jpg. A loose glob also caught the pass-1 filenames
    # (umbrella-green.jpg) and blew up the numeric sort.
    pat = re.compile(rf"^{re.escape(key)}-(\d+)\.jpg$")
    hits = []
    for f in glob.glob(os.path.join(ROOT, "images", "forden", "*.jpg")):
        m = pat.match(os.path.basename(f))
        if m:
            hits.append((int(m.group(1)), f))
    return [IMGD + os.path.basename(f) for _, f in sorted(hits)][:limit]


def card(key, brandline, desc, alt, name=None):
    d = META[key]
    imgs = [i for i in frames(key) if os.path.exists(os.path.join(ROOT, i.lstrip("/")))]
    if not imgs:
        raise SystemExit("NO IMAGES for card: " + key)
    n = len(imgs)
    title = name or d["title"]
    price = f"${float(d['price']):,.2f}".replace(".00", "")
    # Only print a strike-through where the discount is real - see docstring.
    # <s> not a new class: verify-post.py fails any class without a CSS rule, and
    # inventing one renders it unstyled. <s> strikes through natively.
    was = ""
    if d.get("was") and float(d["was"]) > float(d["price"]):
        w = f"${float(d['was']):,.2f}".replace(".00", "")
        was = f" &middot; <s>{w}</s>"
    fr = "".join(f'<div class="pg-frame"><img src="{u}" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, u in enumerate(imgs))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    arrows = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              f'<span class="pg-count">1/{n}</span>') if n > 1 else ""
    return (f'<div class="product-card" id="{key}" data-frames="{n}">\n'
            f'    <div class="product-gallery"><div class="pg-track">{fr}</div>{arrows}'
            f'<div class="pg-dots">{dots}</div></div>\n'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{brandline}</div>\n'
            f'        <div class="product-name">{title} &middot; {price}{was}</div>\n'
            f'        <div class="product-desc">{desc}</div>\n'
            f'        <a class="product-link" href="{SHOP}{d["handle"]}" target="_blank" '
            f'rel="noopener">fordengolf.com &#8599;</a>\n'
            f'      </div>\n    </div>')


SECTIONS = []

SECTIONS.append(("swing-kings", "The Tee Packet", "SWING KINGS &middot; $14",
  "Start here, because it is the most Forden object Forden makes. The tee picks come in a foil "
  "sachet in Newport green, gold and white stripe across the top, the wordmark set in the same "
  "heavy slab a cigarette pack uses, and SWING KINGS printed across the bottom where the format "
  "would normally go. The tees inside are wooden and stamped 33. It is a joke that took real work "
  "to land, and it is the only thing in the range photographed with any styling at all.", [
  card("teepicks", "Forden &times; N&ordm;33 &middot; In stock",
    "A collaboration with N&ordm;33 that arrives as six stamped wooden tees in a sachet built to "
    "read as a pack of menthols. The green is the giveaway, and so is the word MINT tucked into the "
    "corner. Fourteen dollars, and the cheapest way into the brand.",
    "Forden Golf x No33 Swing Kings tee picks in green foil packets"),
]))

SECTIONS.append(("swingman", "The Swingman Line", "THE LOGO, ON EVERYTHING ELSE",
  "The Swingman mark is a figure mid-swing rendered as overlapping strokes, and it is a direct "
  "reference to a photograph. Doc Edgerton fired a strobe a hundred times a second at a golfer at "
  "MIT in 1938 and produced a body dissolving into fifty superimposed selves. Forden has flattened "
  "that into a logo, and it works hardest on the accessories, where the repeat has room to run.", [
  card("umbrella", "Accessories &middot; In stock",
    "The canopy runs sixty-eight inches and repeats the Swingman across its panels in white on "
    "dark green. Open it and look up and the repeat reads properly for the first time &mdash; the "
    "photograph it comes from was about repetition, and this is the only piece that gets to say so.",
    "Forden Golf Swingman golf umbrella in green"),
  card("mallet-cover", "Accessories &middot; In stock",
    "A mallet cover in black with the figure printed across the crown in a small allover. Magnetic "
    "closure, and the same print runs on a blade version and on the barrel headcovers, which are "
    "both sold out.",
    "Forden Golf Swingman mallet putter cover in black"),
  card("tin", "Accessories &middot; In stock",
    "An aluminium alloy pouch tin with the Swingman on the lid, sold in black and in green. It is a "
    "small thing to make and an easy one to get wrong, and the lid engraving is deep enough to "
    "catch light rather than sitting flat under a print.",
    "Forden Golf aluminium pouch tin in black"),
]))

SECTIONS.append(("tees", "The Tees and Long Sleeves", "COLLECTION II &middot; $42&ndash;$45.50",
  "This is where the brand does its talking. The graphics are in-jokes about being a normal "
  "golfer: municipal courses, missed putts, the scorecard as a document of failure. They are set "
  "in type rather than illustration, which keeps them the right side of novelty. Everything here "
  "is cotton, cut boxy, and currently thirty per cent off.", [
  card("script-tee", "Collection II &middot; In stock",
    "The script logo on cream, and the plainest thing they make. If the rest of the range is a "
    "series of punchlines, this is the piece that has to work without one, and it does &mdash; the "
    "script is drawn with enough weight to read across a fairway.",
    "Forden Golf script t-shirt in cream"),
  card("local-muni-tee", "Collection II &middot; In stock",
    "The line reads &ldquo;I broke 90 at our local muni&rdquo;, set small and centred in a "
    "typewriter face on lavender. The colour is the surprise. It is the single best-judged piece in the range and the "
    "one that tells you the brand actually plays public golf.",
    "Forden Golf Local Muni t-shirt in lavender"),
  card("scorecard-tee", "Collection II &middot; In stock",
    "A scorecard graphic sits on pale indigo, its boxes filled with numbers nobody would frame. The joke "
    "is dry and the execution is quiet, which is the correct order for those two things.",
    "Forden Golf Scorecard t-shirt in indigo"),
  card("divot-masters", "Collection II &middot; In stock",
    "Divot Masters runs across the back in a stacked lockup with a flag graphic, on black. The heaviest "
    "graphic in the line and the one closest to the streetwear half of the brief.",
    "Forden Golf Divot Masters t-shirt in black"),
  card("geo-putter-ls", "Collection II &middot; In stock",
    "This one puts a geometric putter-path diagram on the chest of a brown long sleeve. Brown is doing a lot "
    "of work across Collection II &mdash; it turns up on the hoodie and two of the hats &mdash; and "
    "it is the colour that separates this from every other golf label currently reaching for sage.",
    "Forden Golf Geo Putter long sleeve in brown"),
  card("swinging-ls", "Collection II &middot; In stock",
    "The Swingman printed large on the back of a white long sleeve, which is the clearest look at "
    "the Edgerton reference anywhere in the range. Front carries the wordmark small at the chest.",
    "Forden Golf Swinging Golf long sleeve in white"),
]))

SECTIONS.append(("sweats", "Crewnecks and Hoodies", "$63&ndash;$77 &middot; DOWN FROM $90&ndash;$110",
  "The heavier pieces are where the price drops start to look serious, and where the brand's "
  "collegiate instinct comes out. Nothing here is technical. These are cotton fleece sweatshirts "
  "with golf graphics on them, which is either the whole point or a limitation depending on how "
  "you feel about playing in a hoodie.", [
  card("retro-club-hoodie", "Collection II &middot; In stock",
    "Brown fleece carries FORDEN GOLF CLUB across the chest in a cream collegiate serif. The best "
    "garment they make. The arc is drawn properly, the brown is warm rather than muddy, and it is "
    "the one piece here that would pass without anyone clocking it as a golf brand.",
    "Forden Golf Retro Club hoodie in brown"),
  card("cut-spin-hoodie", "Collection II &middot; In stock",
    "CUT SPIN inside a ball-dimple circle across the back, black on black-adjacent. A back graphic "
    "does more work than a chest one on a hoodie and this is sized to know that.",
    "Forden Golf Cut Spin hoodie in black"),
  card("flag-crew", "Collection II &middot; In stock",
    "A small flag mark sits at the chest of a black crewneck. The most restrained piece in the "
    "range and the one to buy if the graphics elsewhere are louder than you want.",
    "Forden Golf Flag crewneck in black"),
  card("undulations-crew", "Collection II &middot; In stock",
    "UNDULATIONS printed as a warped grid inside a box on the chest &mdash; a green read as a "
    "topographic drawing. The most design-literate graphic in the line and the one that rewards "
    "standing closer.",
    "Forden Golf Undulations crewneck in black"),
  card("last-priority-crew", "Collection II &middot; In stock",
    "Glacier grey, and the scorecard is cut down to one line of small type. The colour is soft enough to "
    "wear off a course without explaining yourself.",
    "Forden Golf Last Priority crewneck in glacier grey"),
]))

SECTIONS.append(("hats", "The New Era Line", "ALL $48 &middot; NOT ON SALE",
  "Forden makes hats with New Era, which for a brand this size is the real credential in the range. "
  "The 9Forty A-Frame comes in eight two-tone colourways and the Golfer snapback in six, all at "
  "forty-eight dollars, and none of them are discounted while nearly everything else is &mdash; "
  "which tells you which part of the business is working.", [
  card("9forty-walnut", "Forden &times; New Era &middot; In stock",
    "The Swingman is embroidered at the front panel of a walnut and black two-tone. The A-Frame is "
    "the taller crown in the New Era range and it carries a logo this busy better than a low profile "
    "would.",
    "Forden Golf x New Era 9Forty A-Frame snapback in walnut two-tone"),
  card("9forty-khaki", "Forden &times; New Era &middot; In stock",
    "The same shape comes in khaki and black. Khaki is the quiet one in a line that runs to deep purple "
    "and royal, and it is the colourway that will still look right in three seasons.",
    "Forden Golf x New Era 9Forty A-Frame snapback in khaki two-tone"),
  card("golfer-snapback", "Forden &times; New Era &middot; In stock",
    "The Golfer shape carries the script logo in cream on brown, with a New Era flag at the side. A "
    "rope-free, unstructured five-panel that sits closer to a caddie hat than a trucker.",
    "Forden Golf x New Era Golfer snapback in brown"),
]))

SECTIONS.append(("bottoms", "Bottoms", "THE SHORT LIST, LITERALLY",
  "Bottoms are the thinnest part of the range and Forden knows it &mdash; three shorts and three "
  "sweat pants, most of them plain. The mesh short is the one with any design in it.", [
  card("scorecard-short", "Collection II &middot; In stock",
    "A navy mesh short with the scorecard print worked small into the leg. Lined, mid-length, and "
    "the closest the brand comes to something you would actually tee off in. The black colourway is "
    "already gone.",
    "Forden Golf Scorecard mesh short in navy"),
]))

HERO = IMGD + "hero-tee-picks.jpg"

WRITEUP = """<p>In 1938 a golfer called Densmore Shute stood in a laboratory at MIT and hit a driver
while Harold Edgerton fired a strobe at him one hundred times a second. Edgerton was an engineer, not
a photographer &mdash; he had invented the stroboscope, and he was working out what it could see that
the eye could not. What came back was a body dissolved into fifty superimposed selves and, at the
centre of it, the shaft visibly bending after the ball had gone. Nobody had photographed that before.
The print is called <em>Densmore Shute Bends the Shaft</em> and it now sits in the Smithsonian, the
MIT Museum and the Syracuse University Art Museum.</p>

<p>It is also, eighty-eight years later, a golf logo. Forden Golf calls its mark the Swingman, and
the brand is explicit that it comes from Edgerton's swing photography. Flattened to a single colour
and printed on an umbrella panel, the figure keeps the thing that made the original work: it is a
picture of motion rather than of a golfer.</p>

<p>Forden was founded by Chad Gurman, and the brief has stayed narrow. <em>&ldquo;Forden Golf was
founded on the belief that golf fashion should be as dynamic and expressive as the game itself. Our
mission is to provide a wardrobe that effortlessly blends the elegance of the sport with the boldness
of street style,&rdquo;</em> Gurman says on the brand's own site. In practice that means cotton
fleece, boxy tees, type-led graphics about municipal golf, and a hat line made with New Era.</p>

<p>The range is on its second collection. Collection II is the current one and most of it is thirty
per cent off; Collection 1 has been moved to an archive and cut in half. The hats are the exception
&mdash; every New Era piece holds at forty-eight dollars while the apparel discounts around it, which
is usually a sign of where the demand actually is.</p>

<p>What Forden does not have is photography of anyone wearing any of it. There is no lookbook, no
on-course imagery, no on-model shots at all; the Gallery page on their site is an empty template. For
a brand whose stated business is expression, that is the obvious gap, and it is the one thing holding
the range back from reading as clearly as it deserves to. The clothes are better than the pictures of
them.</p>"""

FAQ = [
 ("Who founded Forden Golf?",
  "Chad Gurman. The brand publishes his founding statement on its About page: &ldquo;Forden Golf was "
  "founded on the belief that golf fashion should be as dynamic and expressive as the game itself.&rdquo;"),
 ("What is the Forden Swingman logo?",
  "A figure mid-swing drawn as overlapping strokes. Forden states it references Harold &ldquo;Doc&rdquo; "
  "Edgerton's stroboscopic golf photography &mdash; Edgerton was the MIT engineer who invented the "
  "stroboscope and in 1938 photographed pro Densmore Shute at 100 flashes per second, capturing the "
  "shaft bending after impact."),
 ("Does Forden Golf work with New Era?",
  "Yes. The headwear line is made with New Era across the 9Forty A-Frame and Golfer snapback shapes, "
  "plus a 59Fifty fitted. All the snapbacks are $48 and, unlike the apparel, are not discounted."),
 ("What are the Swing Kings tee picks?",
  "A collaboration with N&ordm;33 &mdash; six stamped wooden tees in a foil sachet designed to read "
  "as a cigarette pack, in Newport green with a gold stripe. $14, down from $20."),
 ("Is Forden Golf on sale?",
  "Most of it, at the time of writing. Collection II is around thirty per cent off and the Collection "
  "1 archive is half price. Headwear is excluded."),
]

# ── closing gallery ───────────────────────────────────────────────────────────
# DETAIL crops, not lifestyle - Forden has no on-model photography at all. Named
# honestly in the intro so the section is not pretending to be something it isn't.
GALLERY = [
 ("d-umbrella-canopy.jpg", "Looked at from beneath, the umbrella canopy runs the Swingman on every panel"),
 ("d-tee-picks.jpg",       "The Swing Kings sachets come in Newport green and gold"),
 ("d-swinging-ls-red.jpg", "The red long sleeve carries the Swingman large across the back"),
 ("d-towel-weave.jpg",     "The golf towel runs the Swingman small and repeated"),
 ("d-tin-open.jpg",        "The aluminium pouch tin opens to a plain interior"),
 ("d-sweatpant-embroidery.jpg", "The wordmark is embroidered at the hip of the classic logo sweat pant"),
 ("d-umbrella-handle.jpg", "The umbrella handle and collar are finished in matte black"),
 ("d-mallet-on-club.jpg",  "The mallet cover sits over a putter head"),
]


def build():
    tpl = open(TPL, encoding="utf-8").read()
    head, tail = tpl.split('<section class="products">', 1)

    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>", head, flags=re.S)
    for k in ("description", "og:description", "twitter:description"):
        head = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")',
                      lambda m: m.group(1) + DESC + m.group(2), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                  lambda m: m.group(1) + TITLE + m.group(2), head)
    head = re.sub(r'(<meta property="og:image" content="https://thegrassyissue\.com)[^"]*(")',
                  lambda m: m.group(1) + HERO + m.group(2), head)
    for pat in (r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")',
                r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")'):
        head = re.sub(pat, lambda m: m.group(1) + SLUG + m.group(2), head)
    head = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + TITLE + m.group(2), head, flags=re.S)
    head = re.sub(r'(<div class="breadcrumb">).*?(</div>)',
                  lambda m: m.group(1) + '<a href="/">The Feed</a> &rsaquo; <a href="/#drops">Drops</a> '
                            '&rsaquo; Forden Golf' + m.group(2), head, flags=re.S)
    head = re.sub(r'(<div class="drop-meta">).*?(</div>)',
                  lambda m: m.group(1) + "Drops &amp; Brands &middot; 29 August 2026 &middot; "
                            "19 pieces &middot; $14&ndash;$77" + m.group(2), head, flags=re.S)
    head = re.sub(r'(<div class="drop-hero-img">)\s*<img[^>]*>',
                  lambda m: m.group(1) + f'<img src="{HERO}" alt="Forden Golf x No33 Swing Kings tee '
                            f'packets in Newport green" loading="eager">', head)
    head = re.sub(r'(<div class="writeup-body"[^>]*>).*?(</div>)',
                  lambda m: m.group(1) + WRITEUP + m.group(2), head, flags=re.S)
    head = re.sub(r'(<div class="sidebar-card">).*?(</div>\s*</aside>)',
                  lambda m: m.group(1) + SIDEBAR + m.group(2), head, flags=re.S)
    head = re.sub(r'("headline"\s*:\s*")[^"]*(")',
                  lambda m: m.group(1) + "Brand to Know - Forden Golf" + m.group(2), head)
    for k in ("datePublished", "dateModified"):
        head = re.sub(rf'("{k}"\s*:\s*")[^"]*(")', lambda m: m.group(1) + "2026-08-29" + m.group(2), head)

    clean = lambda s: re.sub(r"\s+", " ", re.sub(r"&[a-z]+;|&#\d+;", " ", s)).strip()
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": clean(q),
         "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in FAQ]}
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", '
                  r'"@type": "FAQPage".*?</script>',
                  '<script type="application/ld+json">' + json.dumps(faq_ld) + '</script>',
                  head, flags=re.S)

    body = []
    for sid, h2, kicker, intro, cards in SECTIONS:
        body.append(f'  <h2 id="{sid}">{h2}</h2>')
        body.append(f'  <p class="cat-kicker"><strong>{kicker}</strong> &mdash; {intro}</p>')
        body.append('  <div class="products-grid">')
        body.extend("  " + c for c in cards)
        body.append('  </div>')

    gal = ('  <h2 id="details">In the Details</h2>\n'
           '  <p class="cat-kicker"><strong>NO LOOKBOOK, SO: DETAILS</strong> &mdash; Forden has no '
           'on-model or on-course photography &mdash; no lookbook, and a Gallery page with nothing on '
           'it. So this is the range close up instead: the repeats, the embroidery, the inside of the '
           'tin. It is the most you can see of these clothes until somebody photographs them being '
           'worn.</p>\n  <div class="products-grid">\n' +
           "".join(f'    <div class="product-card" id="det{i}" data-frames="1">\n'
                   f'      <div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                   f'<img src="{IMGD}{f}" loading="lazy" alt="{c}"></div></div></div>\n'
                   f'      <div class="product-body"><div class="product-desc">{c}</div></div>\n'
                   f'    </div>\n' for i, (f, c) in enumerate(GALLERY)) +
           '  </div>')
    body.append(gal)

    faq_html = ('<div class="faq">\n' + "".join(
        f'  <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>\n'
        for q, a in FAQ) + '</div>\n')
    rest = re.sub(r'<div class="faq">.*?</div>\s*(?=<section|<div class="more")',
                  faq_html, tail, count=1, flags=re.S)

    out = head + '<section class="products">\n' + "\n".join(body) + "\n" + rest
    open(OUT, "w", encoding="utf-8").write(out)
    words = len(re.sub(r"<[^>]+>", " ", out).split())
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"  sections={len(SECTIONS)} product cards={sum(len(s[4]) for s in SECTIONS)} "
          f"detail frames={len(GALLERY)} words~{words}")


SIDEBAR = """<div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded by</span><span>Chad Gurman</span></div>
      <div class="sidebar-detail"><span class="l">Logo</span><span>The Swingman</span></div>
      <div class="sidebar-detail"><span class="l">After</span><span>Doc Edgerton, 1938</span></div>
      <div class="sidebar-detail"><span class="l">Hats with</span><span>New Era</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$14&ndash;$77</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>
      <a href="/brands/" class="sidebar-cta">Browse the Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#FordenGolf</span>
        <span class="hashtag">#IndependentGolf</span>
      </div>
    """

if __name__ == "__main__":
    build()
