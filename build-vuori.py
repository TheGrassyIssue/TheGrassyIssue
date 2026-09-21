#!/usr/bin/env python3
"""build-vuori.py — Brand to Know: Vuori. 21 September 2026.

Emits the page CONTENT at a new slug. btk-template.py reorders it into house
order afterwards; apply-affiliates.py and fix-more-and-related.py run after.

DONOR is brand-to-know-sun-mountain: newest template-era BTK that is already
USD-denominated, so the price furniture is right, and it carries no
brand-prefixed CSS of its own (its .pg-* are the shared gallery classes and
its .btk-* are the template's). Local Rule and Late Nine were both wrong
donors here — both are kr stores. Every Sun Mountain token still has to be
scrubbed; see DONOR_MARKS and see build-axxa.py for what happens otherwise.

PRICES ARE USD, AND THE VERIFICATION IS THE POINT.

vuoriclothing.com blocks products.json store-wide — it returns an empty body
rather than a 404, which is the sort of thing you can mistake for "no
products" — and every collection page is client-rendered, so a plain fetch
returns a shell. Prices were read from the rendered tiles in a browser and
then the currency was confirmed against the schema.org offer on a product
page:

    /products/aim-trouser-athletic-slim-fit-30-khaki-linen-texture
    "priceCurrency":"USD"   "price":98        collection tile: $98

A Vuori PDP also prints $75 (free-shipping threshold) and $24.50 (instalment).
Neither is a price, and a regex that takes the first dollar figure on the page
gets one of them.

NO STOCK LINES ON THIS PAGE. Late Nine carried "3 of 5 sizes live" because
Late Nine's feed exposed per-variant availability. Vuori's does not, and it was
not harvested. A stock claim we did not verify is worse than no stock claim, so
the card has none — rather than copying the donor's furniture because it was
there.

THE SCORECARD POCKET, AND WHY IT IS NOT ON THIS PAGE.

TheIndustry.fashion and Sporting Goods Intelligence both describe the Aim
trousers as having "scorecard-sized magnetic rear pockets". It reads like
press-release language and neither outlet attributes it to a named person.
Vuori's own product copy for the Aim Trouser says only "a back pocket with a
magnetic closure for easy entry" — no scorecard, no dimension. So the magnetic
closure is on the page as fact and the scorecard sizing is not. NO_SCORECARD
below fails the build if it ever creeps back in, because the tempting version
of this sentence is the one with the vivid detail in it.

THE QUOTES. Kudla to CNBC (Tom Huddleston Jr, 20 March 2023); Holland to
Highsnobiety (Chris Erik Thomas, 8 April 2026). Both bylined, both on the
record, nothing paraphrased into quotation marks. ATTRIBUTIONS is checked
against every quoted paragraph.
"""
import json
import pathlib
import re
import sys

import tgi_bands

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "drops/brand-to-know-vuori.html"
DONOR = ROOT / "drops/brand-to-know-sun-mountain.html"
SPEC = json.loads((ROOT / "research/btk/vuori.json").read_text(encoding="utf-8"))

BRAND = "Vuori"
SLUG = "brand-to-know-vuori"
TITLE = "Brand to Know &mdash; Vuori"
HEADLINE = "Vuori &mdash; The Golf Line Is New. The Reason To Care Isn&rsquo;t."
SHOP = "https://vuoriclothing.com"
IMG = "/images/vuori"
READ_DATE = "21 September 2026"
DATE = "21 September 2026"
HERO = "/images/vuori/hero.jpg"
DESC = ("Vuori, founded 2015 in Encinitas and now headquartered in Carlsbad, "
        "launched two golf collections in 2026 behind Tom Holland. The Aim Trouser, "
        "the Strato Tech Polo, and the off-course pieces that built the company &mdash; "
        "and why they read correctly on an Austin muni. Prices in USD, read "
        "21 September 2026.")

# Everything Sun Mountain that must not survive the copy.
DONOR_MARKS = [
    (r"\bSun Mountain\b", 0), (r"\bsun-mountain\b", 0), (r"\bsunmountain\b", 0),
    (r"\bMissoula\b", 0), (r"\bRick Reimers\b", 0), (r"\bSpeed Cart\b", 0),
]

# Every quoted paragraph must name one of these.
ATTRIBUTIONS = ["Kudla", "CNBC", "Holland", "Highsnobiety", "Vuori"]

# The claim we deliberately do not make — see the module docstring.
NO_SCORECARD = r"scorecard"

# slug, display name, price USD, family, blurb.
GOLF = [
    ("aim-trouser", "Aim Trouser Athletic Slim Fit 30&Prime;", 98, "Aim",
     "The most golf-specific thing Vuori makes: athletic-slim, lightweight "
     "technical fabric, and a back pocket that shuts with a magnet instead of a "
     "button. Launched with the May collection."),
    ("aim-short", "Aim Short 8&Prime;", 78, "Aim",
     "Same family, 8in inseam, in a linen-texture weave. The Austin answer to "
     "the trouser for nine of the twelve months."),
    ("strato-tech-polo", "Strato Tech Polo", 68, "Strato",
     "Flagged a best seller in four separate colourways, and the cheapest way "
     "into the golf line. Heathered, soft-collared, no logo doing any work."),
    ("torrey-golf-polo", "Short Sleeve Torrey Golf Polo", 88, "Torrey",
     "Named for a course, and the most conventionally golf-shaped shirt in the "
     "range &mdash; structured collar, plain body."),
    ("gamepoint-polo", "Short Sleeve Gamepoint Polo 2.0", 88, "Gamepoint",
     "Crossed over from the tennis side of the business, tipped collar and all. "
     "It reads as a club shirt from ten feet."),
    ("ace-polo", "Ace Polo", 78, "Ace",
     "One of the pieces named in the May collection announcement. Lighter and "
     "less structured than the Torrey."),
    ("ponto-half-zip-mock", "Ponto Half Zip Mock Neck", 118, "Ponto",
     "Vuori put the Ponto fabric in a mock neck. Named in the May launch, and the "
     "layer most likely to get used here between December and February."),
    ("terrain-jacket", "Terrain Jacket", 138, "Terrain",
     "This is the outerwear piece of the golf collection. Plain black shell, zip "
     "front, nothing on it."),
    ("sunday-insulated-vest", "Sunday Insulated Hybrid Vest", 158, "Sunday",
     "Quilted front, knit back. A vest earns roughly six weeks a year in Austin "
     "and this is the one to spend them on."),
    ("venture-quarter-zip", "Venture Quarter Zip", 158, "Venture",
     "Top of the golf layering range, and the piece that looks least like "
     "activewear of anything in the collection."),
]

OFF = [
    ("kore-short", "Kore Short Unlined 7&Prime;", 68, "Kore",
     "The piece that built the company. Runs 5, 7 and 9in, lined or unlined, and "
     "it is the reason most people own this brand at all."),
    ("ponto-performance-pant", "Ponto Performance Pant 30&Prime;", 110, "Ponto",
     "Call it the drive-home trouser. Soft enough to sleep in, plain enough to eat "
     "dinner in."),
    ("strato-tech-tee", "Strato Tech Tee", 58, "Strato",
     "This is the cheapest thing in the selection, and it is the same fabric as the "
     "polo without the collar."),
    ("ponto-jogger", "Ponto Performance Jogger", 110, "Ponto",
     "This covers the travel-day half of the Ponto family. Cuffed, tapered, grey."),
    ("seaside-hoodie", "Seaside Pullover Hoodie 2.0", 144, "Seaside",
     "Heavier than the technical layers and cut like a sweatshirt rather than "
     "sportswear. Clubhouse to car park."),
    ("waffle-henley", "Waffle Henley", 98, "Waffle",
     "The least sporty garment Vuori makes, and the one that does the most work "
     "once you are off the property."),
    ("meta-trouser", "Vuori Meta&trade; Trouser Classic Fit 30&Prime;", 138, "Meta",
     "This trouser sits in the golf collection and the general "
     "pants collection at the same time, same name, same price. It is the argument "
     "for this whole post in one garment."),
    ("vintage-jean", "Vuori Vintage Jean Classic Fit 30&Prime;", 198, "Vintage",
     "The most expensive piece here, and proof of how far the range now runs "
     "from the yoga studios it started in."),
]
ALL = GOLF + OFF

FAQ = [
    ("Does Vuori actually make golf clothes, or is this a logo on a polo?",
     "Two dedicated collections in 2026 &mdash; the first in April alongside the "
     "<em>Play It As It Lies</em> campaign, the second and more technical one on "
     "12 May. The May collection introduced the Aim Trouser, the Ace Polo, the "
     "Ponto Half Zip Mock Neck and the Terrain Jacket. It is a real line, though "
     "a good deal of it is existing Vuori fabric with a collar added."),
    ("What does the Aim Trouser&rsquo;s magnetic pocket actually do?",
     "Vuori&rsquo;s own product copy describes &ldquo;a back pocket with a "
     "magnetic closure for easy entry&rdquo; &mdash; it shuts by magnet rather "
     "than button or zip, so it opens one-handed. The trouser is $98, cut "
     "athletic slim, in a lightweight technical fabric."),
    ("Where do I start if I only buy one thing?",
     "The Strato Tech Polo at $68. It is flagged a best seller in four "
     "colourways, it is the cheapest entry to the golf line, and it is the piece "
     "you will still wear when you are not playing. The Kore Short at $68 is the "
     "same answer from the other direction."),
    ("How big is the golf range, really?",
     "The men&rsquo;s golf collection displays 48 product tiles, but that is "
     "roughly nineteen distinct styles. The Strato Tech Polo alone accounts for "
     "seven of them on colour, and the Aim Short for five. Deep on colourways, "
     "narrow on silhouettes."),
    ("Where is Vuori from, and who owns it?",
     "Founded in Encinitas, California in 2015 by Joe Kudla, who began "
     "developing it in 2014 and is still chief executive with majority "
     "ownership. The company is now headquartered in Carlsbad. A November 2024 "
     "secondary tender led by General Atlantic and Stripes valued it at about "
     "$5.5 billion."),
]

EXTRA_CSS = """
/* Product family chip on a Vuori card. Named for the product FAMILY (Kore,
   Ponto, Aim, Meta), because the families are how this catalogue is actually
   organised and the colourway count makes style names ambiguous. */
.vu-family{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;opacity:.55;margin-bottom:6px}
"""


def fmt(n):
    """US dollars. This is a US brand read on its US store; never a kr figure."""
    return f"${n:,}"


def card(slug, name, price, family, blurb):
    """HOUSE CARD CONVENTION: .product-brand is the BRAND, .product-name is the
    PRODUCT NAME with the price appended. btk-template.py matches on
    .product-name, so a bare price there makes the page unmatchable."""
    alt = f'{BRAND} &mdash; {re.sub(r"<[^>]+>", "", name)}'
    return (f'<div class="product-card">\n'
            f'  <img src="{IMG}/{slug}.jpg" alt="{alt}" loading="lazy" />\n'
            f'  <div class="product-body">\n'
            f'    <span class="vu-family">{family}</span>\n'
            f'    <div class="product-brand">{BRAND}</div>\n'
            f'    <div class="product-name">{name} &middot; {fmt(price)}</div>\n'
            f'    <div class="product-desc">{blurb}</div>\n'
            f'    <a href="{SHOP}/products/{slug}" target="_blank" rel="noopener" '
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
    body = page[page.find("<body"):]
    # editorial body only — More from TGI legitimately links other brands
    cut = body.find('data-btk="related"')
    if cut < 0:
        cut = body.find('<section class="more"')
    editorial = body[:cut] if cut > 0 else body

    for pat, _ in DONOR_MARKS:
        hits = re.findall(pat, editorial, flags=re.I)
        if hits:
            bad.append(f"donor mark survived: {pat} x{len(hits)}")

    # CURRENCY. This is the mirror of build-late-nine's dollar guard.
    for pat in (r"\bSEK\b", r"\bkr\b", r"&yen;", r"\bA\$", r"£"):
        if re.search(pat, editorial):
            bad.append(f"non-USD currency in a USD page: {pat}")
    for slug, name, price, *_ in ALL:
        if fmt(price) not in page:
            bad.append(f"{slug} price {fmt(price)} missing from the page")

    # THE CLAIM WE DO NOT MAKE
    if re.search(NO_SCORECARD, page, flags=re.I):
        bad.append("'scorecard' is on the page — that is the press release's "
                   "claim, not Vuori's (see docstring)")

    # HOUSE VOICE
    if re.search(r"\bworth\b", editorial, flags=re.I):
        bad.append("'worth' is banned in TGI copy")

    # QUOTES MUST BE ATTRIBUTED
    for m in re.finditer(r"<p>((?:(?!</p>).)*&ldquo;(?:(?!</p>).)*)</p>",
                         editorial, flags=re.S):
        para = m.group(1)
        if not any(a in para for a in ATTRIBUTIONS):
            bad.append(f"unattributed quote: {re.sub(r'<[^>]+>', '', para)[:70]!r}")

    # STRUCTURE
    if "product-grid" in page.replace("products-grid", ""):
        bad.append("product-grid is not a house class — it is products-grid")
    n_grid = page.count('<div class="products-grid">')
    if n_grid != 2:
        bad.append(f"{n_grid} products-grid blocks, expected 2")
    n_card = page.count('<div class="product-card">')
    if n_card != len(ALL):
        bad.append(f"{n_card} product cards, expected {len(ALL)}")
    if len(ALL) != 18:
        bad.append(f"{len(ALL)} products, the house grid is 18")
    if len({p[0] for p in ALL}) != len(ALL):
        bad.append("duplicate product slug")

    # SPEC AND BUILD MUST AGREE, BOTH DIRECTIONS. Checking only one way let
    # five Late Nine products sit in no spec category at all.
    # NORMALISE THE SAME WAY btk-template.py DOES, NOT A HAND-ROLLED VERSION.
    #
    # This check used to unescape by hand — .replace("&Prime;", '"'). That made
    # the two sides agree here and disagree in the template, which unescapes
    # properly and so reads &Prime; as U+2033 PRIME, not a straight quote. The
    # build passed its own check and then btk-template.py refused the page with
    # 'matched no unused product'. A guard that normalises differently from the
    # consumer is not checking the thing that matters.
    import html as _html

    def _norm(s):
        return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", s))).strip().lower()

    spec_names = {_norm(n) for sec in SPEC["collection"] for n in sec["match"]}
    build_names = {_norm(n) for _, n, *_ in ALL}
    if spec_names - build_names:
        bad.append(f"in spec, not built: {sorted(spec_names - build_names)}")
    if build_names - spec_names:
        bad.append(f"built, not in spec: {sorted(build_names - spec_names)}")

    # EVERY IMAGE MUST BE LOCAL AND MUST EXIST
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', body):
        s = m.group(1)
        if s.startswith("http"):
            bad.append(f"hot-linked image: {s[:60]}")
        elif s.startswith("/") and not (ROOT / s.lstrip("/")).is_file():
            bad.append(f"missing image {s}")

    # FURNITURE
    for need in ("The TGI Take", "The Story", "The Questions"):
        if need not in page:
            bad.append(f"missing house heading: {need}")
    if 'class="vu-family"' in page and ".vu-family" not in page:
        bad.append(".vu-family emitted with no CSS rule")

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
                  lambda m: m.group(1) + "https://thegrassyissue.com" + HERO + m.group(2),
                  head)

    # OUR FAQ, NOT THE DONOR'S. Structured data is invisible on the page and was
    # the defect that shipped Lions Municipal's address inside the Wild Spring
    # Dunes Field Note.
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

    # THE *ARTICLE* LD+JSON, WHICH THE FAQ REPLACEMENT ABOVE DOES NOT TOUCH.
    # The donor head carries TWO ld+json blocks — Article at [0], FAQPage at [1].
    # Replacing only the FAQPage left Sun Mountain's headline and description
    # sitting in the Article schema: invisible on the page, fully visible to
    # Google. The donor-mark guard caught it, which is the whole reason that
    # guard reads the finished page rather than the parts that made it.
    plain_title = re.sub(r"<[^>]+>", "", TITLE).replace("&mdash;", "—")
    plain_desc = re.sub(r"<[^>]+>", "", DESC).replace("&mdash;", "—")
    for key, val in (("headline", plain_title), ("description", plain_desc)):
        head = re.sub(rf'("{key}":\s*")[^"]*(")',
                      lambda m, _v=val: m.group(1) + _v + m.group(2), head, count=1)
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
                 " &mdash; four players walking a ridgeline with carry bags, from the "
                 "2026 golf campaign" + m.group(2), nav, count=1)
    # THE WHOLE drop-meta, NOT JUST ITS FIRST SPAN.
    # The donor's meta is three spans: "18 Picks" / "·" / "Missoula, MT · Est.
    # 1981". Replacing only the first span (the shape every previous build used,
    # because those donors put the date there) left Sun Mountain's home town on
    # a Vuori page. Rebuilding the block outright is the only version that
    # cannot leave a donor's city behind.
    nav = re.sub(r'<div class="drop-meta">.*?</div>',
                 lambda _m: ('<div class="drop-meta">\n'
                             f'    <span>{len(ALL)} Picks</span><span>&middot;</span>'
                             f'<span>Carlsbad, CA &middot; Est. 2015</span>\n'
                             '  </div>'), nav, count=1, flags=re.S)

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
    # PARAGRAPHS ONLY, ON PURPOSE. btk-template.py rebuilds this section from
    # spec["story_extra"], which holds paragraphs and nothing else. Pull-quotes
    # placed here are dropped on every template pass — two were, silently, on
    # the Late Nine build. The pull-quote this page carries lives in the
    # bespoke band section below, which the template does not touch.
    story = (f'<section class="writeup" data-btk="story">\n'
             f'  <div class="writeup-body">\n'
             f'    <h2>The Story</h2>\n'
             + "\n".join(f"    <p>{p}</p>" for p in SPEC["story_extra"]) + "\n"
             f'  </div>\n</section>')

    # ---- THE BODY BAND + PULL-QUOTE ----
    # data-btk="prose" is the sanctioned marker for a writer's own section.
    # btk-template.py treats ANY data-btk it does not special-case as its own
    # output from a previous run and DELETES it — a bespoke "ln-band" marker
    # silently ate a photograph and a quote on the Late Nine build.
    band = tgi_bands.band(
        ROOT, f"{IMG}/body-1.jpg",
        f"{BRAND} &mdash; the FA26 lookbook: quarter-zip and trousers on a "
        f"clifftop course",
        credit="Photography courtesy of Vuori &middot; FA26 lookbook")
    pq = pullquote(
        "We were left with few options, and we were running out of money very "
        "fast. I was really frightened we were going to lose the business.",
        "Joe Kudla, founder and CEO, to CNBC")
    body_band = (f'<section class="writeup" data-btk="prose">\n'
                 f'  {band}\n  {pq}\n</section>')

    # ---- PRODUCTS ----
    secs = []
    for sec, items in [(SPEC["collection"][0], GOLF), (SPEC["collection"][1], OFF)]:
        secs.append(f'<section class="products">\n'
                    f'  <div class="products-hdr"><h2>{sec["hdr"]}</h2></div>\n'
                    f'  {grid(items)}\n</section>')

    # ---- THE QUESTIONS ----
    # HOUSE FAQ SHAPE, COPIED FROM THE DONOR, NOT INVENTED: details.faq-q
    # inside div.faq, under an h2.products-hdr. An invented <div class="faq-item">
    # has no CSS rule anywhere on the site and btk-template.py cannot parse it.
    qs = "\n".join(f'    <details open class="faq-q"><summary>{q}</summary>'
                   f'<p>{a}</p></details>' for q, a in FAQ)
    faq = (f'<section class="products" data-btk="faq">\n'
           f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n'
           f'  <div class="faq">\n{qs}\n  </div>\n</section>')

    tail = src[src.find('<section class="more"'):] if '<section class="more"' in src \
        else src[src.rfind("<footer"):]

    page = (head + nav + take_sec + "\n\n" + story + "\n\n" + body_band
            + "\n\n" + "\n\n".join(secs) + "\n\n" + faq + "\n\n" + tail)
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
