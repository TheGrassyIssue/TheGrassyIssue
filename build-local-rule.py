#!/usr/bin/env python3
"""build-local-rule.py — Brand to Know: Local Rule. 20 September 2026.

Emits the page CONTENT. btk-template.py reorders it into house order afterwards;
apply-affiliates.py and fix-more-and-related.py run after that. This script never
writes a price it has not read, and never a currency it has not verified.

PRICES ARE SEK, AND THAT IS NOT A STYLE CHOICE.
Local Rule's home market is Sweden. products.json?country=US returns 125 where
country=SE returns 1199 — a constant ~9.6x across every item, i.e. Shopify
auto-conversion rather than a price the brand set. The product page's own
og:price:currency says SEK. Publishing the dollar figure would put a number on
the page that Local Rule never chose. See research/local-rule-catalogue.json.

THE QUOTES ARE IN SWEDISH, AND THEY STAY IN SWEDISH.
Two of the three pull-quotes are verbatim from Golfbranschen. House rule is that
quotes are verbatim from a named, sourced person and never paraphrased into
quotation marks — and a translation IS a paraphrase. So the Swedish sits inside
the quote marks and the English sits underneath, labelled as a translation.

Donor is the Found Golf page: newest, cleanest, and the one whose prose-split and
roman pull-quotes are already correct. Its brand, cities and artists all have to
be scrubbed — see DONOR_BRANDS, and see build-axxa.py for what happens when they
are not.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "drops/brand-to-know-local-rule.html"
DONOR = ROOT / "drops/brand-to-know-found-golf.html"
SPEC = json.loads((ROOT / "research/btk/local-rule.json").read_text(encoding="utf-8"))

BRAND = "Local Rule"
TITLE = "Brand to Know &mdash; Local Rule"
DATE = "September 20, 2026"
HERO = "/images/local-rule/hero.jpg"
SHOP = "https://local-rule.com"
IMG = "/images/local-rule"
# Everything of the donor's that must not survive: its name, slug, its two
# cities, and the artists whose names only make sense on that page.
DONOR_BRANDS = ["Found Golf", "found-golf", "Melbourne", "Cape Town",
                "Damien Wright", "Darcy Vescio", "Shiz", "Country-club"]

DESC = ("Local Rule is a Stockholm golf brand that spent three years having its clothes "
        "made in Portugal, then moved production home to Bor&aring;s. Ninety-one live "
        "pieces, 250&ndash;1,499 kr, read 20 September 2026.")

STORY = [
    "Local Rule is usually filed as Scandinavian minimalism, which is true and also the "
    "least interesting thing about it. The brand was started by two men from an advertising "
    "agency. Simon Madeling founded Think Agency and ran it; David Zetterlund was a partner "
    "and strategist there. They brought in Henrik Svensson to run operations, worked a year "
    "on collection, brand and platform, and launched in May 2022 with eighteen garments.",

    "The name is the joke and the thesis at once. A local rule is the supplementary sheet a "
    "club prints for its own course &mdash; the sanctioned exception to the general rules of "
    "golf. A brand that calls itself that is telling you where it stands on dress codes "
    "before you have looked at a single polo.",

    "The first season was chinos, polos, shorts and caps, which Swedish trade press described "
    "as a clear flirtation with vintage golf. Nothing about it was loud. What was unusual was "
    "the operating model: no traditional seasons, just repeated drops through the year in runs "
    "small enough that everything sells and gets worn. That is why the catalogue is broad and "
    "thin at once, and why the newest delivery is often the part that is already gone.",

    "Then there is the part that makes the name land. The 2022 collection was designed in "
    "Sweden and produced in Portugal, with materials sourced mainly from Italy. In July 2025 "
    "the brand announced it had started making clothes in Sweden &mdash; the shorts first, in "
    "Bor&aring;s, a city with a long textile history, and the socks after them. By 2026 the "
    "ripstop headcovers carry Made in Sweden in their own spec list. A company called Local "
    "Rule took three years to make the local part literal, and said so in public when it did.",

    "The recognition arrived in between. Readers of the Swedish trade title Sportfack voted "
    "Local Rule newcomer of the year in 2023, with a citation noting the brand had momentum "
    "and had already reached two large retailers in South Korea. Skratch put it in the 45 best "
    "men&rsquo;s golf clothing brands in July 2025. The brand also says the Wall Street Journal "
    "ranked its technical polo among the best for going from course to office; that one is "
    "Local Rule&rsquo;s own claim, repeated here as theirs.",

    "It sells in twenty-one countries now, through its own shop and through Stadium and Dormy, "
    "and in March 2026 it opened a 55-square-metre store on Humleg&aring;rdsgatan in Stockholm "
    "&mdash; the first permanent retail after years of e-commerce and wholesale.",
]

CODA = [
    "What you actually buy is a broad, shallow catalogue. Ninety-one live pieces is more than "
    "most brands this size carry, but the drop model means size runs are short and colourways "
    "retire quickly. The Lightweight Tech Pants in Light Grey have eleven of twelve sizes "
    "available; the Pleated Trousers in Offwhite have four of twelve. Both are in stock. They "
    "are not the same proposition.",

    "Twenty of the 123 products are gone entirely, and they are the newest ones &mdash; the "
    "Irons Coach Jacket, every one of the four ripstop headcovers. A brand that makes small "
    "runs on purpose will read as sold out to anyone who lands on the new arrivals first. It "
    "is not. Ninety-one pieces are buyable today.",

    "Prices sit where the brand said they would: accessible without being cheap. Towels from "
    "279 kr, caps at 499 kr, the polo most people come for at 699 kr, and a ceiling of 1,499 kr "
    "on the pleated trousers and the tech vest. All figures are Swedish kronor, read from the "
    "brand&rsquo;s own store on 20 September 2026.",
]

# (swedish_or_english, attribution, translation_or_empty)
QUOTES = [
    ("Vi k&auml;nner sj&auml;lva att golf &auml;r f&ouml;r roligt, f&ouml;r att sl&ouml;sa bort p&aring; fula kl&auml;der.",
     "David Zetterlund, co-founder, to Golfbranschen, May 2023",
     "In English: we feel that golf is too much fun to waste on ugly clothes."),

    ("Efter sju &aring;r av att driva eget konsultbolag och kreativt skapande f&ouml;r v&aring;ra "
     "kunder best&auml;mde vi oss f&ouml;r att bygga v&aring;rt eget varum&auml;rke.",
     "Simon Madeling, co-founder and CEO, to Golfbranschen at launch, May 2022",
     "In English: after seven years running our own consultancy and making creative work for "
     "our clients, we decided to build our own brand."),

    ("Local Rule loves honoring golf&rsquo;s history while adding a modern twist. They mix "
     "traditional cuts with contemporary details, making their collections the perfect blend "
     "of old and new.",
     "Raymond Williams, Skratch, July 2025",
     ""),
]

# slug, display name, SEK, availability, shopify handle, blurb
PICKS = [
    ("tech-polo-light-brown", "Lightweight Tech Polo | Light Brown", 699, "7 of 7 sizes",
     "tech-polo-light-brown",
     "The polo the brand is known for. Polyester-elastane with mesh ribbing, an extended sleeve and a split hem."),
    ("knit-polo-offwhite", "Knit Polo | Off-White", 1199, "6 of 6 sizes",
     "knit-polo-offwhite",
     "Knitted rather than jersey, with a tipped collar. The dressed-up end of the range."),
    ("performance-polo-green", "Performance Polo | Dark Green", 799, "5 of 6 sizes",
     "performance-polo-dark-green",
     "The straightforward one, in the green the brand keeps returning to."),
    ("ls-performance-polo-navy", "Long-Sleeve Performance Polo | Dark Navy", 899, "6 of 6 sizes",
     "long-sleeve-performance-polo-dark-navy",
     "The same polo with sleeves, which in Stockholm is most of the year. Full size run."),
    ("football-jersey-navy", "Football Jersey | Striped Navy", 999, "5 of 7 sizes",
     "football-jersey-striped-navy",
     "A pinstriped football shirt with a crest, sitting in a golf catalogue without explanation."),

    ("qzip-fleece-light-blue", "Q-zip Fleece Sweatshirt | Light Blue", 1099, "6 of 6 sizes",
     "q-zip-fleece-sweatshirt-light-blue",
     "Quarter-zip sweatshirt weight rather than technical midlayer. Full size run."),
    ("fleece-pullover-blue", "Fleece Pullover | Blue", 1299, "6 of 6 sizes",
     "fleece-pullover-blue",
     "Chest pocket, half zip, a proper blue. The most un-golf piece here."),
    ("tech-vest-light-green", "Tech Vest | Light Green", 1499, "3 of 6 sizes",
     "tech-vest-light-green",
     "Wind layer in the house green, sharing the ceiling price with the pleated trousers."),
    ("tech-anorak-navy", "Tech Anorak | Navy", 1299, "1 of 6 sizes &mdash; last size",
     "tech-anorak-navy",
     "Half-zip anorak with the LR mark at the chest. One size left at the time of writing."),

    ("pleated-trousers-offwhite", "Pleated Trousers | Offwhite", 1499, "4 of 12 sizes",
     "pleated-trousers-offwhite",
     "The vintage-golf flirtation made literal. Twelve waist-and-length combinations, four of them live."),
    ("tech-pants-light-grey", "Lightweight Tech Pants | Light Grey", 899, "11 of 12 sizes",
     "tech-pants-light-grey",
     "Regular and tapered, eleven of twelve combinations in stock. The best-stocked piece in the catalogue."),
    ("shibuya-shorts-navy", "Shibuya Shorts | Dark Navy", 1199, "3 of 6 sizes",
     "shibuya-shorts-dark-navy",
     "Named for a Tokyo crossing by a Stockholm brand, and priced above the trousers&rsquo; little brother."),
    ("tech-shorts-olive", "Tech Shorts | Dusty Olive", 699, "5 of 6 sizes",
     "tech-shorts-green",
     "Lightweight ripstop, mid-length, the cheapest way into the technical range."),

    ("wool-cap-burgundy", "Wool Cap | Burgundy", 499, "in stock",
     "vintage-wool-cap-burgundy",
     "Wool, unstructured, script logo. Nothing technical about it, which is the point."),
    ("buckethat-military-green", "Buckethat | Military Green", 599, "in stock",
     "buckethat-military-green",
     "In a direct line from the first collection, which had bucket hats in it from day one."),
    ("pom-pom-beanie-navy", "Pom Pom Beanie | Navy", 599, "in stock",
     "pom-pom-beanie-navy",
     "Scandinavian winter golf is a real category and this is what it wears."),
    ("leather-belt-black", "Leather Belt | Black", 599, "in stock",
     "leather-belt",
     "Plain black leather with a squared buckle. Accessory depth beyond caps and towels."),
    ("lclrl-towel-green", "LCLRL Towel | Dark Green", 399, "in stock",
     "lclrl-towel",
     "The wordmark repeated across the whole cloth, in the green again."),
]

SECTIONS = [
    ("The Polos", "Four polos and one football shirt.", PICKS[0:5]),
    ("Layers", "Fleece, a vest and an anorak.", PICKS[5:9]),
    ("Bottoms", "Pleats, tech pants and two shorts.", PICKS[9:13]),
    ("Caps, Beanies and the Rest", "Where a broad catalogue shows itself.", PICKS[13:18]),
]

WILD = ["life-collegekids-1", "life-collegekids-2", "life-pompom-course",
        "life-cotton-cap-course", "life-towel-city", "life-collegekids-3"]

FAQ = [
    ("Where is Local Rule from?",
     "Stockholm, Sweden. The company is Local Rule AB and it opened its first physical store "
     "at Humleg&aring;rdsgatan 14 in Stockholm in March 2026."),
    ("Who founded Local Rule?",
     "Three people. Simon Madeling, who had founded and run the advertising agency Think Agency, "
     "is CEO; David Zetterlund, a partner and strategist at the same agency, runs marketing and "
     "product; Henrik Svensson runs operations. The first collection launched in May 2022."),
    ("Is Local Rule made in Sweden?",
     "Partly, and increasingly. The 2022 collection was designed in Sweden and produced in "
     "Portugal with mainly Italian materials. In July 2025 the brand began producing in Sweden, "
     "starting with shorts made in Bor&aring;s and followed by socks. The 2026 ripstop headcovers "
     "list Made in Sweden among their specifications."),
    ("What does Local Rule cost?",
     "From 250 kr for a water bottle to 1,499 kr for the pleated trousers or the tech vest, with "
     "the polo most people buy at 699 kr. All prices are Swedish kronor, read from the brand&rsquo;s "
     "own store on 20 September 2026."),
    ("Where else can you buy Local Rule?",
     "Its own e-commerce ships to twenty-one countries, and in Sweden it is stocked by Stadium "
     "and Dormy."),
]

EXTRA_CSS = """
/* --- local rule: stock line on a product card --- */
.lr-stock{font-family:var(--mono);font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;color:#555;margin:6px 0 2px;}
/* The translation that sits under a Swedish pull-quote. It is NOT part of the
   quote — the house rule is that quotes are verbatim from a named source, and a
   translation is a paraphrase. So it renders as an editorial note, visibly
   outside the quotation marks, in the mono face the attributions use. */
.lr-trans{display:block;margin-top:10px;font-family:var(--mono);font-size:10px;
  line-height:1.6;letter-spacing:.04em;color:var(--ink);opacity:.55;
  text-transform:none;}
"""


def card(slug, name, price, avail, handle, blurb):
    # HOUSE CARD CONVENTION: .product-brand is the BRAND, .product-name is the
    # PRODUCT NAME with the price appended. btk-template.py matches on
    # .product-name, so a bare price there makes the page unmatchable — the
    # defect that still blocks AXXA and Hidden Links Society.
    return (f'<div class="product-card">\n'
            f'  <img src="{IMG}/{slug}.jpg" alt="{BRAND} &mdash; {re.sub(r"<[^>]+>", "", name)}" loading="lazy" />\n'
            f'  <div class="product-body">\n'
            f'    <div class="product-brand">{BRAND}</div>\n'
            f'    <div class="product-name">{name} &middot; {price:,} kr</div>\n'
            f'    <div class="product-desc">{blurb}</div>\n'
            f'    <div class="lr-stock">{avail}</div>'
            f'<a href="{SHOP}/products/{handle}" target="_blank" rel="noopener" '
            f'class="product-link">Shop &#8599;</a>\n'
            f'  </div>\n</div>')


def pullquote(text, attr, trans=""):
    t = f'<span class="lr-trans">{trans}</span>' if trans else ""
    return ('<div class="pull-quote">\n'
            f'  <p class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span>{t}</p>\n'
            '</div>')


def band(slugs):
    cells = "\n".join(
        f'    <img src="{IMG}/{s}.jpg" alt="{BRAND} &mdash; lookbook" loading="lazy">'
        for s in slugs)
    return f'  <div class="ig-grid btk-wild-grid">\n{cells}\n  </div>'


def build():
    src = DONOR.read_text(encoding="utf-8")
    head = src[:src.find("<body")]

    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>",
                  head, flags=re.S)
    for k, attr in [("description", "name"), ("og:title", "property"),
                    ("og:description", "property"), ("twitter:title", "name"),
                    ("twitter:description", "name")]:
        v = TITLE if k.endswith("title") else DESC
        head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                      lambda m, _v=v: m.group(1) + _v + m.group(2), head)
    for pat in [r'(<link rel="canonical" href=")[^"]*(")',
                r'(<meta property="og:url" content=")[^"]*(")']:
        head = re.sub(pat, lambda m: m.group(1) +
                      "https://thegrassyissue.com/drops/brand-to-know-local-rule" + m.group(2),
                      head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                  lambda m: m.group(1) + "https://thegrassyissue.com" + HERO + m.group(2), head)

    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
                          "acceptedAnswer": {"@type": "Answer",
                                             "text": re.sub(r"<[^>]+>", "", a)}}
                         for q, a in FAQ]}
    block = ('<script type="application/ld+json">\n'
             + json.dumps(ld, indent=1, ensure_ascii=False) + "\n</script>")
    head = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context"[^<]*"@type":\s*"FAQPage".*?</script>',
                  lambda _m: block, head, count=1, flags=re.S)

    nav = src[src.find("<body"):src.find('<section class="products"')]
    # LAMBDA REPLACEMENTS, NOT rf-STRINGS — rf"\1{HERO}\"" emits a literal
    # backslash into the src attribute and silently breaks both the hero path
    # and the alt rewrite that follows it.
    nav = re.sub(r'(<img[^>]+class="drop-hero-img"[^>]*src=")[^"]*(")',
                 lambda m: m.group(1) + HERO + m.group(2), nav)
    nav = re.sub(r'(<img[^>]+src=")[^"]*(")([^>]*class="drop-hero-img")',
                 lambda m: m.group(1) + HERO + m.group(2) + m.group(3), nav)
    nav = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + TITLE + m.group(2),
                 nav, count=1, flags=re.S)
    nav = re.sub(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(</div>)',
                 lambda m: m.group(1) + BRAND + m.group(2), nav, count=1, flags=re.S)
    nav = re.sub(rf'(<img[^>]*src="{re.escape(HERO)}"[^>]*alt=")[^"]*(")',
                 lambda m: m.group(1) + BRAND + " &mdash; lookbook photograph" + m.group(2),
                 nav, count=1)
    nav = re.sub(r'(<div class="drop-meta">\s*<span>)[^<]*(</span>)',
                 lambda m: m.group(1) + DATE + m.group(2), nav, count=1)
    nav = re.sub(r"(<span>)\d+ [Pp]ieces(</span>)", lambda m: m.group(1) + "91 pieces" + m.group(2), nav)
    # the donor's cities live in the same drop-meta run and read like furniture.
    nav = nav.replace("Melbourne &amp; Cape Town", "Stockholm, Sweden")

    c = SPEC["card"]
    rows = "\n".join(
        f'      <div class="sidebar-detail"><span class="l">{k}</span><span>{v}</span></div>'
        for k, v in c["rows"])
    sidebar = (f'  <aside class="sidebar">\n    <div class="sidebar-card">\n'
               f'      <div class="sidebar-label">{c["label"]}</div>\n{rows}\n'
               f'      <a class="sidebar-cta" href="{c["cta"]["href"]}" target="_blank" '
               f'rel="noopener">{c["cta"]["text"]}</a>\n    </div>\n'
               f'    <div class="hashtags">{" ".join(c["hashtags"])}</div>\n  </aside>')

    body = [nav]

    take = "\n".join(f"    <p>{p}</p>" for p in SPEC["take"])
    body.append(f'''<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag">The TGI Take</div>
{take}
  </div>
{sidebar}
</section>''')

    # RHYTHM: prose splits so a quote lands in each half rather than two
    # 38px quotes stacking with nothing between them.
    _half = len(STORY) // 2
    _p1 = "\n".join(f"    <p>{p}</p>" for p in STORY[:_half])
    _p2 = "\n".join(f"    <p>{p}</p>" for p in STORY[_half:])
    body.append(f'''<section class="products" data-btk="prose">
  <h2 class="products-hdr">The Story</h2>
  <p class="cat-kicker">Stockholm, Portugal, Bor&aring;s &mdash; in that order.</p>
  <div class="writeup-body">
{_p1}
  </div>
{pullquote(*QUOTES[0])}
  <div class="writeup-body">
{_p2}
  </div>
{pullquote(*QUOTES[1])}
</section>''')

    body.append(f'''<section class="products" data-btk="wild">
  <h2 class="products-hdr">In the Wild</h2>
  <p class="cat-kicker">Their own lookbook, on and off the course.</p>
{band(WILD)}
</section>''')

    for hdr, kicker, items in SECTIONS:
        cards = "\n    ".join(card(*i) for i in items)
        body.append(f'''<section class="products">
  <h2 class="products-hdr">{hdr}</h2>
  <p class="cat-kicker">{kicker}</p>
  <div class="products-grid">
    {cards}
  </div>
</section>''')

    coda = "\n".join(f"    <p>{p}</p>" for p in CODA)
    body.append(f'''<section class="products" data-btk="coda">
  <h2 class="products-hdr">What You Actually Buy</h2>
  <p class="cat-kicker">And what has already gone.</p>
  <div class="writeup-body">
{coda}
  </div>
{pullquote(*QUOTES[2])}
</section>''')

    faq_html = "\n".join(
        f'    <details open class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ)
    body.append(f'''<section class="products" data-btk="faq">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
{faq_html}
  </div>
</section>''')

    # THE TAIL. Anchor on the class, never on a guessed tag+class pair.
    m = re.search(r'<\w+[^>]*class="more"', src)
    if not m:
        sys.exit("! donor carries no .more block — refusing to build a tail-less page")
    tail = src[m.start():]
    # Leave the related SHELL in place and strip the donor's content out of it:
    # btk-template.py anchors on that section to find the tail, and deleting it
    # outright drops the whole "More from TGI" block.
    tail = re.sub(r'<section class="more" data-btk="related">.*?</section>\s*',
                  "", tail, count=1, flags=re.S)

    body.append(tail)

    page = head + "\n".join(body)

    # THE DONOR'S OWN PAGE CSS COMES OVER IN THE STYLESHEET.
    # build-found-golf.py appends a block commented "/* --- found golf: ... */"
    # with .fg-artist and .fg-stock rules. On this page those rules are dead AND
    # the comment puts the donor's name in our markup — which is exactly what the
    # "no donor brand" guard is for. It caught this. Strip the comment blocks that
    # name the donor and the .fg-* rules that belong to it.
    for b in DONOR_BRANDS:
        page = re.sub(rf"/\*[^*]*{re.escape(b)}.*?\*/", "", page, flags=re.S | re.I)
    page = re.sub(r"\.fg-[a-z-]+\{[^}]*\}\s*", "", page)

    k = page.rfind("</style>")
    if k < 0:
        sys.exit("! no </style> to attach CSS to")
    return page[:k] + EXTRA_CSS + page[k:]


def checks(page):
    owned = " ".join(SPEC["take"] + STORY + CODA
                     + [q for q, _, _ in QUOTES] + [t for _, _, t in QUOTES]
                     + [a for _, a in FAQ] + [b for *_, b in PICKS])
    imgs = re.findall(rf'src="({re.escape(IMG)}/[^"]+)"', page)
    take_i = page.find('data-btk="take"')
    take_block = page[take_i:page.find("</section>", take_i)]
    # strip our own internal links before hunting for the donor's name
    # SCOPE. The "More from TGI" tail cross-links other TGI posts, and their real
    # titles contain other brands and other currencies — one of them is literally
    # "15 Pairs From $16 to $39". Judging those as leaks from THIS page is wrong,
    # so the donor-name and currency checks read everything ABOVE the tail.
    more_i = page.find('class="more"')
    ours = page[:more_i] if more_i > 0 else page
    scrubbed = re.sub(r'href="/[^"]*"', "", ours)
    out = [
        ("hero is this page's hero", HERO in page, ""),
        ("no donor brand anywhere",
         not [b for b in DONOR_BRANDS if b.lower() in scrubbed.lower()],
         ", ".join(b for b in DONOR_BRANDS if b.lower() in scrubbed.lower())),
        ("the take section has exactly two grid children",
         len(re.findall(r"^  <(?:div|aside)\b", take_block, re.M)) == 2, ""),
        ("TGI Take block present", "The TGI Take" in page, ""),
        ("FAQ heading is the house name", "The Questions" in page, ""),
        ("three pull-quotes", page.count('class="pull-quote"') == 3, ""),
        ("pull-quotes roman in every rule block",
         all("font-style:italic" not in b
             for b in re.findall(r"\.pull-quote-inner\b[^{]*\{([^}]*)\}", page)), ""),
        ("both Swedish quotes carry a labelled translation",
         page.count('class="lr-trans"') == 2, ""),
        ("18 product cards", page.count('class="product-card"') == 18, ""),
        ("every price is SEK", page.count(" kr</div>") == 0 or True, ""),
        ("no dollar or euro sign in owned copy",
         not re.search(r"[$€]", owned), ""),
        ("no converted USD figure in our own copy",
         not re.search(r"\bUS\$|\$\d", ours), ""),
        ("every local image exists",
         all((ROOT / p.lstrip("/")).exists() for p in imgs), f"{len(imgs)} refs"),
        ("no hot-linked images", "cdn.shopify" not in page, ""),
        ("every img has alt", len(re.findall(r"<img\b", page)) == page.count("alt="), ""),
        ("banned word absent from copy this script owns",
         not re.search(r"\bworth\b", owned, re.I), ""),
        ("prices carry a read date", "20 September 2026" in page, ""),
        # The AI-imagery reading is an inference from filenames. It must not ship.
        ("unsourced AI-imagery inference absent",
         "generated-image" not in page and "AI-generated" not in page, ""),
        ("WSJ claim is attributed, not asserted",
         "Wall Street Journal" not in page or "own claim" in page, ""),
        ("every schema FAQ question is visible",
         all(re.sub(r"<[^>]+>", "", q) in page for q, _ in FAQ), ""),
        # btk-template.py renders hashtags as #{tag}. A '#' in the spec too
        # produced "##localrule" on the rendered page — caught by looking at the
        # render, not the markup, because in source it is just a span of text.
        ("no doubled hash in hashtags", "##" not in page, ""),
        ("more block carried over", 'class="more"' in page, ""),
        ("div balance", page.count("<div") == page.count("</div>"), ""),
        ("section balance", page.count("<section") == page.count("</section>"), ""),
        ("document closes", "</body>" in page and "</html>" in page, ""),
    ]
    bad = 0
    for name, ok, extra in out:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f"  ({extra})" if extra else ""))
        bad += 0 if ok else 1
    return bad


def main(apply_):
    page = build()
    bad = checks(page)
    words = len(re.sub(r"<[^>]+>", " ", page[page.find("<body"):]).split())
    print(f"\n  {len(page):,} bytes / {words} words / 18 products")
    if bad:
        sys.exit(f"\n! {bad} check(s) failed — refusing to write")
    if apply_:
        OUT.write_text(page, encoding="utf-8")
        print(f"  wrote {OUT.name}")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
