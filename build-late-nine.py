#!/usr/bin/env python3
"""build-late-nine.py — Brand Revisited: Late Nine. 21 September 2026.

Emits the page CONTENT at the EXISTING slug. btk-template.py reorders it into
house order afterwards; apply-affiliates.py and fix-more-and-related.py run
after that.

WHY THIS IS A REBUILD AND NOT AN EDIT.

The live page is 287 words with a single <h2>, and it is illustrated with
OTHER BRANDS' PHOTOGRAPHY — its <img> tags point at /images/malbon-fall/,
/images/odd-ritual/ and /images/streetwear26/. There was no /images/late-nine/
directory until localize-late-nine.py made one. A Late Nine page showing
Malbon trousers is the worst defect on the site, so every frame is replaced.

PRICES ARE SEK, AND THE VERIFICATION IS THE POINT.

late-nine.com/products.json has NO currency field. Prices are bare strings:
"2700.00". Local Rule taught the lesson the hard way — its feed returns 125
with country=US and 1199 with country=SE, a ~9.6x Shopify auto-conversion —
so a bare number from a Shopify feed is never self-describing. Here the
currency was confirmed by reading the RENDERED product page:

    late-nine.com/products/5-pocket-cords-navy  ->  "2 700 kr"
    products.json  5-pocket-cords-navy          ->  "2700.00"

with the market selector showing Sweden (SEK) active. All 30 localised
products were then re-read live on the publish date and every price and stock
count was unchanged. Nothing on this page is converted. A guard below refuses
to build if a bare "$" ever lands next to a price.

THE QUOTES. Every quotation is verbatim from Maxim Lundh, co-founder, speaking
to Taylor Stacey for The Old Ghosts, 13 May 2026. Nothing is paraphrased into
quotation marks and nothing is trimmed in a way that changes it. ATTRIBUTIONS
below is checked against every quoted paragraph.

DONOR is the Local Rule page: newest, correct prose-split, roman pull-quotes,
and already a kr-denominated store so the price furniture is right. Its brand,
founders, cities and products all have to be scrubbed — see DONOR_MARKS, and
see build-axxa.py for what happens when they are not.
"""
import json
import pathlib
import re
import sys

import tgi_bands

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "drops/late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf.html"
DONOR = ROOT / "drops/brand-to-know-local-rule.html"
SPEC = json.loads((ROOT / "research/btk/late-nine.json").read_text(encoding="utf-8"))

BRAND = "Late Nine"
SLUG = "late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf"
TITLE = "Brand Revisited &mdash; Late Nine"
HEADLINE = ("Late Nine &mdash; The Clothes Look Private. "
            "The References Never Were.")
SHOP = "https://late-nine.com"
IMG = "/images/late-nine"
READ_DATE = "21 September 2026"
DATE = "21 September 2026"
HERO = "/images/late-nine/hero.jpg"
DESC = ("Late Nine, Stockholm, founded 2024 by Maxim Lundh. Pleated slacks, ribbed "
        "jersey polos and merino knits built on late-nineties tour golf — and why a "
        "brand from a country of public courses reads right on a muni. Prices in SEK, "
        "read 21 September 2026.")

# Everything Local Rule that must not survive the copy.
DONOR_MARKS = [
    (r"\bLocal Rule\b", 0), (r"\blocal-rule\b", 0), (r"local-rule\.com", 0),
    (r"\bGolfbranschen\b", 0), (r"\bMalm(ö|o)\b", 0),
    (r"\bMalbon\b", 0), (r"\bOdd Ritual\b", 0), (r"streetwear26", 0),
    (r"\blr-trans\b", 0),
]

# Every quoted paragraph must name one of these.
ATTRIBUTIONS = ["Lundh", "The Old Ghosts", "Hypebeast", "Skortch", "Skratch"]

# slug, display name, price SEK, avail, total, family, blurb.
# Prices and stock re-read live on the publish date; see the docstring.
FIVE = [
    ("ribbed-polo-taupe", "Ribbed Jersey Polo Taupe", 1800, 1, 5, "Ribbed Jersey Polo",
     "The piece Tommy Fleetwood played the 2026 Masters in, as a free agent with no apparel deal. "
     "Hefty cotton jersey, contrast-stripe ribbed collar, oversized buttons."),
    ("5-pocket-cords-navy", "5-Pocket Cords Navy", 2700, 4, 5, "Five-Pocket",
     "Baby cotton corduroy milled in the UK at 215g, full straight leg, deepened front pockets "
     "and a ticket pocket. New for FW26."),
    ("five-pocket-chino-fawn", "Five-pocket Chino Fawn", 2700, 3, 3, "Five-Pocket",
     "The chino half of the same family and the only pick here with every size live. "
     "Cut tighter than the pleated trouser &mdash; size up between."),
    ("cable-knit-polo-burgundy", "Cable Knit Polo Burgundy", 2950, 2, 4, "Cable Knit Polo",
     "Ultra-fine merino from the first shearing, nodding to the classic knits worn by icons "
     "of past decades. The most colour in the range."),
    ("country-club-cap-beige", "Twilight Cap Beige", 500, 1, 1, "Country Club Cap",
     "It copies the vintage members caps of the nineties. At 500 SEK it is the cheapest "
     "way into the whole look."),
]

CORE = [
    ("double-pleat-slacks-dark-brown", "Double Pleat Slacks Dark Brown", 3200, 4, 5, "Slacks",
     "This is the archetype: double pleats, full straight leg, and no stretch anywhere in it."),
    ("double-pleat-slacks-dark-brown-copy", "Double Pleat Slacks Dark Navy", 3200, 3, 5, "Slacks",
     "Same cut in navy, and the other half of the FW26 trouser drop."),
    ("double-pleats-beige", "Double Pleat Trousers Beige", 2800, 2, 3, "Double Pleats",
     "A separate family from the Slacks and a lighter, warmer-weather cut."),
    ("five-pocket-chino-navy", "Five-pocket Chino Navy", 2700, 3, 3, "Five-Pocket",
     "The navy chino, fully stocked, and the easiest trouser here to wear off a course."),
    ("5-pocket-cords-olive", "5-Pocket Cords Olive", 2700, 3, 5, "Five-Pocket",
     "The olive corduroy, which reads closest to the nineties reference the brand keeps citing."),
    ("ribbed-polo-grey-mix", "Ribbed Jersey Polo Americano", 1800, 2, 5, "Ribbed Jersey Polo",
     "The sibling to the taupe, in a grey mix, with the same dropped shoulder and long sleeve line."),
    ("cable-knit-polo-light-blue", "Cable Knit Polo Light Blue", 2950, 3, 4, "Cable Knit Polo",
     "Light blue merino, and the piece that most clearly belongs to a Ryder Cup team photograph."),
    ("ribbed-vest-grey", "Ribbed Knit Vest Grey", 2450, 4, 4, "Ribbed Vest",
     "Sleeveless knit over a polo, fully stocked, and the most quietly useful thing they make."),
    ("ribbed-vest-dark-brown", "Ribbed Knit Vest Brown", 2450, 4, 4, "Ribbed Vest",
     "The brown vest holds full stock and runs warmest of the three colourways."),
    ("quarter-zip-windbreaker-beige", "Quarter Zip Windbreaker Beige", 3750, 2, 3, "Quarter Zip",
     "It is cut from a water-repellent cotton blend, with a buttoned placket and metal hardware."),
    ("instructors-jacket-cotton-navy", "Instructors Jacket Navy", 4350, 2, 3, "Instructors Wool",
     "Named for the jackets worn by golf instructors through the nineties. "
     "The top of the range."),
    ("loop-belt-brown-suede-silver", "Loop Belt Brown Suede", 1400, 3, 4, "Loop Belt",
     "Suede takes a silver buckle here, on LWG-certified Italian hide."),
    ("sports-cap-burgundy", "Orbit Cap Burgundy", 500, 1, 1, "Sports Cap",
     "This two-tone rope cap cites the caps worn on tour in the early 2000s."),
]

ALL = FIVE + CORE

# Restocking, per Late Nine's own "Coming Soon" collection. Named, not sold.
RESTOCKING = ["Knit Crepe Polo in Forest, Dark Brown, Navy and Ivory",
              "the long-sleeve Ribbed Jersey Polo in Brown Melange"]

# Classes this page introduces. Every one needs a CSS rule — the .axxa-note
# and .pe-stock defect, twice burned.
EXTRA_CSS = """
/* LATE NINE — stock line under a product, and the family chip. Defined here
   because this page emits them; a class with no rule is indistinguishable
   from a forgotten one. */
.ln-stock{font-family:var(--mono);font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;opacity:.5;display:block;margin:6px 0 10px}
.ln-stock.thin{opacity:.85;color:#8A5A2B}
.ln-family{font-family:var(--mono);font-size:8.5px;letter-spacing:.14em;
  text-transform:uppercase;opacity:.4;display:block;margin-bottom:4px}
/* The donor styles .hashtags (the row) but not .hash (the chip inside it) —
   it emits a different child element. verify-post.py caught the gap. */
.hash{font-family:var(--mono);font-size:9px;letter-spacing:.1em;opacity:.55}
"""

FAQ = [
    ("Who makes Late Nine?",
     "Late Nine was founded in 2024 in Stockholm and co-founded by Maxim Lundh, a creative "
     "director who had previously helped build the Swedish label CQP. Hypebeast profiled the "
     "debut collection in October 2025."),
    ("What is Late Nine's aesthetic?",
     "The last years of the nineties and the first of the two-thousands &mdash; a window Lundh "
     "calls &ldquo;a sort of goldilocks period for golf apparel.&rdquo; The moodboard, per "
     "Hypebeast, runs through <em>The Sopranos</em> and <em>Seinfeld</em> as much as it does "
     "the Ryder Cup."),
    ("Did Tommy Fleetwood wear Late Nine at the Masters?",
     "Yes. Fleetwood played the 2026 Masters in Late Nine's taupe ribbed jersey polo, having "
     "split with Nike at the start of the year and carrying no apparel deal at the time."),
    ("What does Late Nine cost?",
     f"From 500 SEK for a cap to 4,350 SEK for the Instructors Jacket, read from late-nine.com "
     f"on {READ_DATE}. Those are the brand's home-market prices in Swedish kronor and are not "
     f"converted here; the store will show you your own currency."),
    ("Does Late Nine ship to the US?",
     "Yes, delivered duty paid. Standard delivery is $25 and the brand states that duties, "
     "taxes and fees are included in the amount shown at checkout, so nothing is charged on "
     "arrival."),
    ("Does Late Nine use stretch fabric?",
     "Largely no, and deliberately. Lundh's position is that more room to breathe &ldquo;reduces "
     "the reliance on excessive elastane.&rdquo; The trousers are cut full and straight in "
     "cotton, wool and corduroy."),
    ("Is Late Nine good for muni golf?",
     "The cut and the fabrics suit walking in heat &mdash; cotton, wide leg, no elastane. The "
     "prices are a different question, and the caps and belts are the cheapest way in."),
]


def esc(s):
    return s


def fmt(n):
    """Swedish kronor, in the brand's own unit. Never a dollar sign."""
    return f"{n:,} SEK"


def thin(a, t):
    return a < t and a <= 2


def stock_line(a, t):
    if a == t:
        return f'<span class="ln-stock">All {t} size{"s" if t > 1 else ""} live</span>'
    cls = "ln-stock thin" if thin(a, t) else "ln-stock"
    return f'<span class="{cls}">{a} of {t} sizes live</span>'


def card(slug, name, price, avail, total, family, blurb):
    """HOUSE CARD CONVENTION: .product-brand is the BRAND, .product-name is the
    PRODUCT NAME with the price appended. btk-template.py matches on
    .product-name, so a bare price there makes the page unmatchable."""
    alt = f'{BRAND} &mdash; {re.sub(r"<[^>]+>", "", name)}'
    return (f'<div class="product-card">\n'
            f'  <img src="{IMG}/{slug}.jpg" alt="{alt}" loading="lazy" />\n'
            f'  <div class="product-body">\n'
            f'    <span class="ln-family">{family}</span>\n'
            f'    <div class="product-brand">{BRAND}</div>\n'
            f'    <div class="product-name">{name} &middot; {fmt(price)}</div>\n'
            f'    <div class="product-desc">{blurb}</div>\n'
            f'    {stock_line(avail, total)}'
            f'<a href="{SHOP}/products/{slug}" target="_blank" rel="noopener" '
            f'class="product-link">Shop &#8599;</a>\n'
            f'  </div>\n</div>')


def pullquote(text, attr):
    return ('<div class="pull-quote">\n'
            f'  <p class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></p>\n'
            '</div>')


def grid(items):
    return ('<div class="products-grid">\n'
            + "\n".join(card(*i) for i in items)
            + "\n</div>")


def checks(page):
    """Read the FINISHED page, not the variables that produced it."""
    bad = []

    # ---- DONOR LEAKAGE, SCOPED TO THE EDITORIAL BODY ----
    # The More from TGI / related tail carries links to OTHER TGI posts, and
    # one of them is the Local Rule page. That is a cross-link, not leakage.
    # An unscoped search cannot tell those apart and fails on correct output —
    # the same mistake as a donor pattern matching "UT " inside "about".
    cut = page.find('<section class="more"')
    if cut < 0:
        cut = page.find('data-btk="related"')
    body = page[:cut] if cut > 0 else page
    for pat, flags in DONOR_MARKS:
        m = re.search(pat, body, flags)
        if m:
            bad.append(f"donor mark survived in the body: {m.group(0)!r}")

    # ---- CURRENCY ----
    # A bare $ next to a number is the Local Rule / AXXA failure mode. The only
    # legitimate dollar figure on this page is the $25 US shipping fee, which
    # the brand itself quotes in USD.
    for m in re.finditer(r"\$\s?[\d,]+", page):
        if m.group(0).replace(" ", "") != "$25":
            bad.append(f"dollar figure on a SEK page: {m.group(0)!r}")
    if "SEK" not in page:
        bad.append("no SEK anywhere — the currency has gone missing")

    # ---- PRICES MATCH THE TABLE ----
    for slug, name, price, *_ in ALL:
        if f"{name} &middot; {fmt(price)}" not in page:
            bad.append(f"price line missing or wrong for {name}")

    # ---- EVERY PRODUCT IMAGE IS LOCAL AND EXISTS ----
    for m in re.finditer(r'<img src="([^"]+)"', page):
        src = m.group(1)
        if src.startswith("http"):
            bad.append(f"hot-linked image: {src[:60]}")
        elif src.startswith("/images/"):
            if not (ROOT / src.lstrip("/")).is_file():
                bad.append(f"missing image file: {src}")
    # and none of them may come from another brand's folder
    for d in ("malbon", "odd-ritual", "streetwear26"):
        if f"/images/{d}" in page:
            bad.append(f"another brand's image folder is still referenced: {d}")

    # ---- QUOTES ARE ATTRIBUTED ----
    for para in re.findall(r"<p>(.*?)</p>", page, re.S):
        if "&ldquo;" in para and not any(a in para for a in ATTRIBUTIONS):
            flat = re.sub(r"<[^>]+>", "", para)[:90]
            bad.append(f"quotation names nobody: {flat}...")

    # ---- HOUSE WORD BAN ----
    for m in re.finditer(r"\bworth\w*", page, re.I):
        ctx = page[max(0, m.start() - 40):m.start() + 40]
        if "Fort Worth" not in ctx:
            bad.append(f"banned word 'worth': ...{re.sub(r'<[^>]+>', '', ctx)}...")

    # ---- EVERY CLASS THIS PAGE INVENTS HAS A RULE ----
    for cls in ("ln-stock", "ln-family", "hash"):
        used = re.search(rf'class="[^"]*\b{cls}\b[^"]*"', page)
        ruled = re.search(rf"\.{cls}\s*[{{,.]", page)
        if used and not ruled:
            bad.append(f".{cls} is used but has no CSS rule")
        if ruled and not used:
            bad.append(f".{cls} has a CSS rule but is never used")

    # ---- THE BAND AND THE QUOTE MUST BE ON THE FINISHED PAGE ----
    # Checked here because the first pair of pull-quotes was dropped by the
    # template pass and nothing failed. This build cannot see the template's
    # output, so verify-late-nine.py re-checks it after that pass too.
    if f"{IMG}/body-1.jpg" not in page:
        bad.append("the body band image is missing")
    n_pq = page.count('class="pull-quote"')
    if n_pq != 1:
        bad.append(f"{n_pq} pull-quotes, expected 1")
    if "remember the size of his pants" not in page:
        bad.append("the pull-quote text is missing")
    if page.count("remember the size of his pants") != 1:
        bad.append("the pull-quote line also still appears in the Story prose")
    bands = tgi_bands.verify_bands(ROOT, page)
    for b in bands:
        bad.append(f"band: {b}")

    # ---- STRUCTURE ----
    if page.count("<h1") != 1:
        bad.append(f"{page.count('<h1')} h1 tags, expected 1")
    if not page.rstrip().endswith("</html>"):
        bad.append("document does not close")
    if '<div class="product-grid"' in page:
        bad.append("product-grid is not a house class — it is products-grid")
    n_grid = page.count('<div class="products-grid">')
    if n_grid != 2:
        bad.append(f"{n_grid} products-grid blocks, expected 2")
    n_cards = page.count('<div class="product-card">')
    if n_cards != len(ALL):
        bad.append(f"{n_cards} product cards, expected {len(ALL)}")

    # ---- THE SPEC AND THIS FILE MUST AGREE ----
    # BOTH DIRECTIONS. The first version checked only spec -> build, so five
    # products this file emitted sat in no spec category at all. btk-template.py
    # keeps them (it drops nothing) but reports them as uncategorised, which is
    # how the gap surfaced. A one-way agreement check is not an agreement check.
    spec_names = [n for sec in SPEC["collection"] for n in sec["match"]]
    ours = [i[1] for i in ALL]
    for n in spec_names:
        if n not in ours:
            bad.append(f"spec names a product this build does not emit: {n!r}")
    for n in ours:
        if n not in spec_names:
            bad.append(f"build emits a product no spec category claims: {n!r}")
    if len(spec_names) != len(set(spec_names)):
        bad.append("a product is claimed by two spec categories")

    for b in bad:
        print(f"  FAIL  {b}")
    return len(bad)


def build():
    src = DONOR.read_text(encoding="utf-8")
    head = src[:src.find("<body")]

    head = re.sub(r"<title>.*?</title>",
                  f"<title>{TITLE} &mdash; The Grassy Issue</title>", head, flags=re.S)
    for k, attr in [("description", "name"), ("og:title", "property"),
                    ("og:description", "property"), ("twitter:title", "name"),
                    ("twitter:description", "name")]:
        v = TITLE if k.endswith("title") else DESC
        head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                      lambda m, _v=v: m.group(1) + _v + m.group(2), head)
    for pat in [r'(<link rel="canonical" href=")[^"]*(")',
                r'(<meta property="og:url" content=")[^"]*(")']:
        head = re.sub(pat, lambda m: m.group(1) +
                      f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                  lambda m: m.group(1) + "https://thegrassyissue.com" + HERO + m.group(2), head)

    # OUR FAQ, NOT THE DONOR'S. Structured data is invisible on the page and
    # was the defect that shipped Lions Municipal's address inside the Wild
    # Spring Dunes Field Note.
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
                          "acceptedAnswer": {"@type": "Answer",
                                             "text": re.sub(r"<[^>]+>", "", a)}}
                         for q, a in FAQ]}
    block = ('<script type="application/ld+json">\n'
             + json.dumps(ld, indent=1, ensure_ascii=False) + "\n</script>")
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context"[^<]*'
                  r'"@type":\s*"FAQPage".*?</script>',
                  lambda _m: block, head, count=1, flags=re.S)
    # DEAD DONOR CSS. The Local Rule page carries a .lr-trans rule for the
    # English translation under its Swedish pull-quotes. Late Nine's quotes are
    # in English, so nothing here uses it — and a rule for a class the page
    # never emits is donor leakage, invisible but real. The reverse defect
    # (.axxa-note, .pe-stock) is a class with no rule; this is a rule with no
    # class, and both get caught.
    head = re.sub(r"\.lr-trans\s*\{[^}]*\}\s*", "", head)
    head = re.sub(r"\.lr-stock\s*\{[^}]*\}\s*", "", head)
    head = head.replace("</head>",
                        f"<style>{tgi_bands.BAND_CSS}{EXTRA_CSS}</style>\n</head>")

    nav = src[src.find("<body"):src.find('<section class="products"')]
    # LAMBDA REPLACEMENTS, NOT rf-STRINGS — rf"\1{HERO}\"" emits a literal
    # backslash into the src attribute and silently breaks the hero path.
    nav = re.sub(r'(<img[^>]+class="drop-hero-img"[^>]*src=")[^"]*(")',
                 lambda m: m.group(1) + HERO + m.group(2), nav)
    nav = re.sub(r'(<img[^>]+src=")[^"]*(")([^>]*class="drop-hero-img")',
                 lambda m: m.group(1) + HERO + m.group(2) + m.group(3), nav)
    nav = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + HEADLINE + m.group(2),
                 nav, count=1, flags=re.S)
    nav = re.sub(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(</div>)',
                 lambda m: m.group(1) + BRAND + m.group(2), nav, count=1, flags=re.S)
    nav = re.sub(rf'(<img[^>]*src="{re.escape(HERO)}"[^>]*alt=")[^"]*(")',
                 lambda m: m.group(1) + BRAND +
                 " &mdash; ribbed knit vest and carry bag, on course" + m.group(2),
                 nav, count=1)
    nav = re.sub(r'(<div class="drop-meta">\s*<span>)[^<]*(</span>)',
                 lambda m: m.group(1) + DATE + m.group(2), nav, count=1)
    nav = re.sub(r"(<span>)\d+ [Pp]ieces(</span>)",
                 lambda m: m.group(1) + f"{len(ALL)} pieces" + m.group(2), nav)
    nav = nav.replace("Melbourne &amp; Cape Town", "Stockholm, Sweden")
    nav = nav.replace("Malm&ouml; &amp; Stockholm", "Stockholm, Sweden")

    # ---- THE TGI TAKE + DETAILS SIDEBAR ----
    c = SPEC["card"]
    rows = "\n".join(
        f'      <div class="sidebar-detail"><span class="l">{k}</span><span>{v}</span></div>'
        for k, v in c["rows"])
    tags = "".join(f'<span class="hash">{t}</span>' for t in c["hashtags"])
    sidebar = (f'  <aside class="sidebar">\n    <div class="sidebar-card">\n'
               f'      <div class="sidebar-label">{c["label"]}</div>\n{rows}\n'
               f'      <a class="sidebar-cta" href="{c["cta"]["href"]}" target="_blank" '
               f'rel="noopener">{c["cta"]["text"]}</a>\n'
               f'      <div class="hashtags">{tags}</div>\n'
               f'    </div>\n  </aside>')
    take = "\n".join(f"      <p>{p}</p>" for p in SPEC["take"])
    take_sec = (f'<section class="writeup" data-btk="take">\n'
                f'  <div class="writeup-body">\n'
                f'    <span class="drop-tag">The TGI Take</span>\n{take}\n'
                f'  </div>\n{sidebar}\n</section>')

    # ---- THE STORY ----
    story_paras = SPEC["story_extra"]
    # THE STORY IS PARAGRAPHS ONLY, ON PURPOSE.
    # btk-template.py rebuilds this section from spec["story_extra"], which
    # holds paragraphs and nothing else. Pull-quotes placed here are dropped on
    # every template pass — two were, silently, on the first build. The one
    # pull-quote this page carries lives in the bespoke band section below,
    # which the template does not touch.
    story = (f'<section class="writeup" data-btk="story">\n'
             f'  <div class="writeup-body">\n'
             f'    <h2>The Story</h2>\n'
             + "\n".join(f"    <p>{p}</p>" for p in SPEC["story_extra"]) + "\n"
             f'  </div>\n</section>')

    # ---- THE BODY BAND + PULL-QUOTE ----
    #
    # WHERE THIS LIVES, AND WHY IT IS NOT IN THE STORY.
    #
    # btk-template.py regenerates The Story from spec["story_extra"], which is
    # PARAGRAPHS ONLY. Two pull-quotes built into the story on the first pass
    # were dropped silently — the live page had zero. The template does try to
    # rescue quotes and images, but its rescue regex wants
    # `<div class="pull-quote">.*?</div>\s*</div>` (two closing divs) and the
    # house pull-quote has one, so it only matches by running on into whatever
    # follows. Anything it does rescue is then stacked at the TOP of The Story
    # by render_story, which is the wrong place for a mid-piece break.
    #
    # THE MARKER MATTERS. The first attempt used data-btk="ln-band" on the
    # assumption that an unrecognised marker would be left alone. It is not:
    # btk-template.py treats ANY data-btk it does not special-case as its own
    # output from a previous run and drops it, so the band and the quote
    # vanished and the "every image survived" guard caught the lost photograph.
    # data-btk="prose" is the sanctioned marker for a writer's own section —
    # the parser appends it to the story rather than regenerating it. SPEC.md
    # calls these bespoke and says the template must not touch them; "prose" is
    # how you say so in markup.
    band = tgi_bands.band(
        ROOT, f"{IMG}/body-1.jpg",
        f"{BRAND} &mdash; the FW26 lookbook: Orbit Cap, knit polo, "
        f"pleated slacks and a travel cover",
        credit="Photography courtesy of Late Nine &middot; FW26 lookbook")
    pq = pullquote(
        "Tiger Woods won the US Open in 2000 by 15 shots, "
        "remember the size of his pants?",
        "Maxim Lundh, co-founder, to The Old Ghosts")
    body_band = (f'<section class="writeup" data-btk="prose">\n'
                 f'  {band}\n  {pq}\n</section>')

    # ---- PRODUCTS ----
    secs = []
    for sec, items in [(SPEC["collection"][0], FIVE), (SPEC["collection"][1], CORE)]:
        secs.append(f'<section class="products">\n'
                    f'  <div class="products-hdr"><h2>{sec["hdr"]}</h2></div>\n'
                    f'  {grid(items)}\n</section>')

    # ---- THE QUESTIONS ----
    # HOUSE FAQ SHAPE, COPIED FROM THE DONOR, NOT INVENTED.
    # The first attempt emitted <div class="faq-item"><h3>, which has no CSS
    # rule anywhere on the site and which btk-template.py cannot parse — it
    # reported both "FAQ heading is the house name" and "prose lost", because
    # the block it could not read was the block it could not carry forward.
    # The real shape is details.faq-q inside div.faq, under an h2.products-hdr.
    qs = "\n".join(f'    <details open class="faq-q"><summary>{q}</summary>'
                   f'<p>{a}</p></details>' for q, a in FAQ)
    faq = (f'<section class="products" data-btk="faq">\n'
           f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n'
           f'  <div class="faq">\n{qs}\n  </div>\n</section>')

    tail = src[src.find('<section class="more"'):] if '<section class="more"' in src \
        else src[src.rfind("<footer"):]

    page = (head + nav + take_sec + "\n\n" + story + "\n\n" + body_band
            + "\n\n" + "\n\n".join(secs) + "\n\n" + faq + "\n\n" + tail)

    # DEAD DONOR CSS, STRIPPED FROM THE WHOLE PAGE.
    #
    # The first attempt stripped this from `head` only and the guard kept
    # firing, because Local Rule keeps its .lr-trans and .lr-stock rules in a
    # <style> block down in the BODY, not the head. Worth the note: "strip it
    # from the head" was an assumption about where CSS lives, and the guard was
    # right and the assumption was wrong. The rule carries a multi-line comment
    # explaining the Swedish translation line, so the comment goes with it.
    for cls in ("lr-trans", "lr-stock"):
        page = re.sub(rf"(?:/\*(?:(?!\*/).)*\*/\s*)?\.{cls}\s*\{{[^}}]*\}}\s*",
                      "", page, flags=re.S)
    return page


def main(apply_):
    page = build()
    bad = checks(page)
    words = len(re.sub(r"<[^>]+>", " ", page[page.find("<body"):]).split())
    print(f"\n  {len(page):,} bytes / {words} words / {len(ALL)} products")
    if bad:
        sys.exit(f"\n! {bad} check(s) failed — refusing to write")
    if apply_:
        OUT.write_text(page, encoding="utf-8")
        print(f"  wrote {OUT.name}")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
