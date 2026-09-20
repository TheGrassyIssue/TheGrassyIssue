#!/usr/bin/env python3
"""build-found-golf.py — rebuild the Found Golf page. 20 September 2026.

THE PAGE THIS REPLACES WAS WRONG, not merely thin. At 465 words it called
Found "Melbourne's Found Golf" and "a tight five-piece lineup", carried the
same three FAQ answers twice under two different headings, quoted AUD prices
with no read date, and linked the Olive Dad Cap as a pick — a cap that, like
all eight colourways, is sold out.

Found is South African born and Melbourne based. The idea started in Cape
Town, the first collection was designed while the founders were in London,
manufacturing returned to Cape Town, and the business runs split between
Cape Town and Melbourne. It sells 65 products: 30 apparel and 35 works of
art and design, from a A$114 cast Bowling Arm to a A$16,000 carved textile.

Every price here was read from found.golf on 20 September 2026 with
country=AU pinned, so Shopify served the brand's own currency rather than a
converted one. Six figures were cross-checked against the site's own
homepage and matched to the cent. See research/found-golf-catalogue.json.

This emits the page CONTENT. `btk-template.py found-golf --apply` then
imposes the house order and furniture on top of it — that is the whole point
of the exercise, so do not hand-assemble the running order here.

Idempotent. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "drops/brand-to-know-found-golf.html"
DONOR = ROOT / "drops/brand-to-know-hiroki-golf.html"
SPEC = json.loads((ROOT / "research/btk/found-golf.json").read_text(encoding="utf-8"))

BRAND = "Found Golf"
TITLE = "Brand to Know &mdash; Found Golf"
DATE = "September 20, 2026"
HERO = "/images/found-golf/hero.jpg"
SHOP = "https://found.golf"
DONOR_BRANDS = ["Hiroki", "hiroki-golf", "Auckland"]

DESC = ("Found Golf is South African born and Melbourne based &mdash; and its store sells "
        "thirty-five works of art alongside the clothes. The full range, in Australian dollars.")

# ---------------------------------------------------------------- the copy
STORY = [
    "Found Golf is usually filed as a Melbourne brand, which is half right and skips the "
    "more interesting half. The idea started in Cape Town. The first collection was drawn "
    "while the founders were living in London. Manufacturing went back to Cape Town, and "
    "the business now runs split between there and Melbourne, which is where it ships "
    "from. Two founders, Lance and Ellen; they publish first names and leave it there, "
    "and so will we.",

    "The brand describes itself as &ldquo;an independent Melbourne based brand that is more "
    "than just fashion&rdquo; that sets out to &ldquo;activate golf as a creative culture "
    "through clothing, art, design and storytelling.&rdquo; Every apparel brand on this site "
    "has written a sentence like that. Found is the only one whose store will also sell you "
    "a bench, a dartboard and a floor lamp.",

    "The reasoning comes from somewhere specific. Asked how surf and skate translate to "
    "golf, they answered that you can dress like a skater even if you cannot skate, because "
    "you are buying into the culture rather than the sport &mdash; and that both surf and "
    "skate built their identity next to music, art and magazines rather than inside the "
    "competition. Golf, they argue, has never had that permission.",
]

CODA = [
    "The clothes bear the argument out more quietly than the art does. The Shiz Knit and "
    "Shiz Vest are cricket-jumper shapes in cream and navy with a single red tab at the "
    "neck. The 1/4 Zip carries FOUND down the spine in reflective type. The Box Par and "
    "Daisy Chain tees are heavyweight cotton at A$118, and the Tee Box at A$85 is the "
    "cheapest thing in the apparel range that is not a tee holder.",

    "The caps are the tell. Eight colourways &mdash; off-white, red, chesterfield, navy, a "
    "baseball logo, olive, cream, powder pink &mdash; all of them at A$55, and every single "
    "one sold out at the time of writing. A brand can look like an art project and still "
    "clear its headwear. Found has.",
]

QUOTES = [
    ("the only negative is the old school holding onto the wrong traditions and the new "
     "school ignoring the right traditions.", "Found, to Good Sport Magazine, April 2024"),
    ("I was confused at the obvious conformity in what everyone was wearing and how "
     "disconnected that was from modern fashion trends.",
     "Lance, co-founder, on starting Found"),
    ("It&rsquo;s a lifestyle, not a sport. Golf should be the same.",
     "Found, to Good Sport Magazine"),
]

ART_INTRO = [
    "Thirty-five works, every one of them in stock, priced from A$114 to A$16,000 and "
    "listed the way a gallery lists: artist first, then the piece. Stools, a monoblock "
    "chair, four woven Chess Dhurries, a cast Bowling Arm, a dartboard marked HOT and NOT, "
    "a set of three titled Men Not Allowed.",

    "The most expensive object in the store is a carved textile by Damien Wright and Tony "
    "Birch called <em>Country-club</em>. Wright appears twice: the other is "
    "<em>Symbolic Capitalist</em>, made with Bonhula Yunupingu, a pair of dumbbells cast as "
    "a dollar sign and a hash. Darcy Vescio is the most-represented artist with seven "
    "works, six of which read as one run on the same subject &mdash; <em>Losers</em>, "
    "<em>Choked</em>, <em>Devastated</em>, <em>Next Year</em>, <em>Almost Won</em>, "
    "<em>Lip Service</em>. A brand built on golf selling a series about losing is either "
    "very funny or very honest, and probably both.",
]

# slug, name, AUD, sizes-available note, shopify handle, blurb
APPAREL = [
    ("box-par-tee", "Box Par Tee", 118, "3 of 6 sizes", "black-tee",
     "Heavyweight cotton, box fit, the tonal box graphic at the chest."),
    ("daisy-chain-tee", "Daisy Chain Tee", 118, "4 of 6 sizes", "daisy-chain-tee",
     "The same weight and cut, with the daisy chain worked across the front."),
    ("tee-box-grey", "Tee Box | Grey", 85, "3 of 5 sizes", "tee-box-grey",
     "The cheapest way into the range. Its white twin is sold out."),
    ("shiz-knit", "The Shiz Knit", 265, "2 of 5 sizes", "the-shiz-knit",
     "Cricket-jumper shape in cream, ribbed V-neck, a single red tab at the collar."),
    ("shiz-vest", "The Shiz Vest", 200, "4 of 6 sizes", "shiz-vest",
     "The sleeveless cut of the same idea, in navy."),
    ("box-crew", "Box Crew | Black", 165, "4 of 6 sizes", "box-crew-black",
     "Heavyweight crew, tonal print, no outside branding."),
    ("quarter-zip", "1/4 Zip", 190, "4 of 6 sizes", "1-4-zip",
     "FOUND set down the spine in reflective type &mdash; the loudest piece in the range."),
    ("windcheater", "Collared Windcheater", 260, "3 of 6 sizes", "wind-breaker",
     "Collared, snap front, cut close to a coach&rsquo;s jacket."),
    ("knitted-polo", "Long Sleeve Knitted Polo", 265, "3 of 5 sizes", "white-long-sleeve-polo",
     "Knitted rather than jersey, long sleeve, in white."),
    ("pleated-pants", "Pleated Pants | Black", 198, "5 of 7 sizes", "pleated-trouser",
     "Single pleat, straight leg. The best-stocked piece in the range."),
    ("the-slacker", "The Slacker | Navy", 198, "4 of 6 sizes", "the-slacker-navy",
     "The relaxed trouser, navy, with the logo tab at the waistband."),
    ("short-game", "Short Game | Black", 135, "3 of 5 sizes", "short-game-black",
     "Mid-length short, elastic back, red tab at the hem."),
]

ART = [
    ("art-country-club", "Damien Wright &amp; Tony Birch &mdash; Country-club", 16000,
     "country-club", "Carved textile. The most expensive object in the store."),
    ("art-symbolic", "Damien Wright &amp; Bonhula Yunupingu &mdash; Symbolic Capitalist", 1000,
     "damien-wright-bonhula-show-me-the-money",
     "Dumbbells cast as a dollar sign and a hash."),
    ("art-break-point", "Darcy Vescio &amp; Locki Humphrey &mdash; Break Point Bench", 5990,
     "darcy-vescio-locki-humphrey-break-point-bench", "A courtside bench, made to sit on."),
    ("art-lip-service", "Darcy Vescio &mdash; Lip Service", 1400,
     "darcy-vescio-lip-service", "Part of the seven-work run, and the largest of them."),
    ("art-losers", "Darcy Vescio &mdash; Losers", 650, "loser",
     "A pennant that says LOSERS. One of six on the same theme."),
    ("art-dartboard", "Danielle Brustman &mdash; HOT/NOT Dartboard", 750,
     "danielle-brustman-hot-not-dartboard", "Eight segments, two verdicts."),
]

FAQ = [
    ("Where is Found Golf from?",
     "Both Melbourne and Cape Town. The idea began in Cape Town, the first collection was "
     "designed while the founders were based in London, manufacturing returned to Cape "
     "Town, and the brand ships from Melbourne."),
    ("Who founded Found Golf?",
     "Two founders, Lance and Ellen. They publish first names only, and no surname appears "
     "in any source we could check."),
    ("Does Found Golf really sell art?",
     "Yes &mdash; thirty-five works, more than half the catalogue by count. They run from "
     "A$114 for a cast Bowling Arm to A$16,000 for a carved textile, and are listed "
     "artist-first like a gallery."),
    ("What does Found Golf cost?",
     "Apparel runs A$25 for the reusable tee holder to A$450 for a piece from the Soof "
     "Flash collaboration, with most tops between A$85 and A$265. All prices are Australian "
     "dollars, read from the brand&rsquo;s own store on 20 September 2026."),
    ("Can you try Found Golf before buying?",
     "Within Australia, yes. The store offers up to three items on a three-day home "
     "try-on, with an A$10 restocking fee if everything is returned."),
]

EXTRA_CSS = """
/* --- found golf: the art cards carry an artist line above the work --- */
.fg-artist{font-family:var(--mono);font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;opacity:.5;margin-bottom:3px;}
/* Stock line on an apparel card. Named for THIS page: the first cut reused
   .axxa-note, whose rule lives only in the AXXA page's stylesheet, so the
   class rendered unstyled here. verify-post caught it. */
.fg-stock{font-family:var(--mono);font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;color:#555;margin:6px 0 2px;}
"""


def esc(s):
    return s


def card(slug, name, price, avail, handle, blurb, art=False):
    note = ("" if art else
            f'<div class="fg-stock">{avail}</div>')
    # HOUSE CARD CONVENTION: .product-brand is the BRAND, .product-name is the
    # PRODUCT NAME with the price appended. 39 of the 42 Brand to Know pages do
    # it this way. The three that do not — AXXA, Hidden Links Society, and the
    # first cut of this page — put a bare price in .product-name, because they
    # all descend from the same donor. btk-template.py reads .product-name to
    # match products against the spec, so on those three it is matching against
    # "A$118" and can never find anything. That is why the template refused
    # this page, and it is a real cohesion defect on the other two as well.
    return (f'<div class="product-card">\n'
            f'  <img src="/images/found-golf/{slug}.jpg" alt="{BRAND} &mdash; {re.sub(r"<[^>]+>", "", name)}" loading="lazy" />\n'
            f'  <div class="product-body">\n'
            f'    <div class="product-brand">{BRAND}</div>\n'
            f'    <div class="product-name">{name} &middot; A${price:,}</div>\n'
            f'    <div class="product-desc">{blurb}</div>\n'
            f'    {note}'
            f'<a href="{SHOP}/products/{handle}" target="_blank" rel="noopener" '
            f'class="product-link">Shop &#8599;</a>\n'
            f'  </div>\n</div>')


def pullquote(text, attr):
    return ('<div class="pull-quote">\n'
            f'  <p class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></p>\n'
            '</div>')


def band(slugs):
    cells = "\n".join(
        f'    <img src="/images/found-golf/{s}.jpg" alt="{BRAND} &mdash; lookbook" loading="lazy">'
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
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                  r"\1https://thegrassyissue.com/drops/brand-to-know-found-golf\2", head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
                  r"\1https://thegrassyissue.com/drops/brand-to-know-found-golf\2", head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                  rf"\1https://thegrassyissue.com{HERO}\2", head)

    # FAQ schema, rebuilt from FAQ above. Lambda replacement, never a string —
    # json.dumps emits \u escapes that re.sub would read as backslash escapes.
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
    # LAMBDA REPLACEMENTS, NOT rf-STRINGS WITH ESCAPED QUOTES.
    # rf"\1{HERO}\"" emits a literal backslash before the closing quote, so the
    # src became  /images/found-golf/hero.jpg\"  — a path that does not exist,
    # AND it stopped the alt-text rewrite below from matching, which is how the
    # donor's name survived into the alt. One bad escape, two failures.
    nav = re.sub(r'(<img[^>]+class="drop-hero-img"[^>]*src=")[^"]*(")',
                 lambda m: m.group(1) + HERO + m.group(2), nav)
    nav = re.sub(r'(<img[^>]+src=")[^"]*(")([^>]*class="drop-hero-img")',
                 lambda m: m.group(1) + HERO + m.group(2) + m.group(3), nav)
    nav = re.sub(r"(<h1[^>]*>).*?(</h1>)", rf"\g<1>{TITLE}\g<2>", nav, count=1, flags=re.S)
    # the donor's own name, date and alt text all have to go — see build-axxa.py,
    # where exactly these three shipped live reading "Hidden Links Society".
    nav = re.sub(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(</div>)',
                 rf"\g<1>{BRAND}\g<2>", nav, count=1, flags=re.S)
    nav = re.sub(rf'(<img[^>]*src="{re.escape(HERO)}"[^>]*alt=")[^"]*(")',
                 rf"\g<1>{BRAND} &mdash; lookbook photograph\g<2>", nav, count=1)
    nav = re.sub(r'(<div class="drop-meta">\s*<span>)[^<]*(</span>)',
                 rf"\g<1>{DATE}\g<2>", nav, count=1)
    nav = re.sub(r"(<span>)\d+ [Pp]ieces(</span>)", r"\g<1>65 pieces\g<2>", nav)
    # the donor's CITY, which sits in the same drop-meta run as the date and
    # is easy to miss because it reads like page furniture rather than content.
    nav = nav.replace("Auckland, New Zealand", "Melbourne &amp; Cape Town")

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

    # RHYTHM. Both quotes used to sit after all the prose, which put two
    # 38px pull-quotes back to back with nothing between them -- visible in
    # the render as a wall of green. Lenny's rule is that sections carry
    # images or a big quote BETWEEN passages of text, not stacked at the end.
    # So the prose splits and a quote lands in each half.
    _half = len(STORY) // 2
    _p1 = "\n".join(f"    <p>{p}</p>" for p in STORY[:_half])
    _p2 = "\n".join(f"    <p>{p}</p>" for p in STORY[_half:])
    body.append(f'''<section class="products" data-btk="prose">
  <h2 class="products-hdr">The Story</h2>
  <p class="cat-kicker">Cape Town, London, Melbourne &mdash; in that order.</p>
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
  <p class="cat-kicker">Their own lookbook, shot in studio.</p>
{band(["life-daisy", "life-zip", "life-knit", "life-wind", "life-crew", "life-polo"])}
</section>''')

    for hdr, kicker, items in [
        ("The Tees and the Knits", "Heavyweight cotton, and two cricket jumpers.",
         APPAREL[0:6]),
        ("Layers", "Where the branding gets loud.", APPAREL[6:9]),
        ("Bottoms", "Pleats, a relaxed trouser and one short.", APPAREL[9:12]),
    ]:
        cards = "\n    ".join(card(*i) for i in items)
        body.append(f'''<section class="products">
  <h2 class="products-hdr">{hdr}</h2>
  <p class="cat-kicker">{kicker}</p>
  <div class="products-grid">
    {cards}
  </div>
</section>''')

    art_cards = "\n    ".join(
        card(s, n, p, "", h, b, art=True) for s, n, p, h, b in ART)
    art_intro = "\n".join(f"    <p>{p}</p>" for p in ART_INTRO)
    body.append(f'''<section class="products">
  <h2 class="products-hdr">The Art Side</h2>
  <p class="cat-kicker">Thirty-five works, listed artist first, all of them in stock.</p>
  <div class="writeup-body">
{art_intro}
  </div>
  <div class="products-grid">
    {art_cards}
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

    # THE TAIL. Anchor on the class, not on a guessed tag+class combination —
    # build-axxa.py looked for '<section class="more-from"', which exists nowhere,
    # and silently shipped a page with no "More from TGI" block at all.
    m = re.search(r'<\w+[^>]*class="more"', src)
    if not m:
        sys.exit("! donor carries no .more block")
    tail = src[m.start():]
    # THE DONOR'S "IF YOU LIKE <BRAND>" BLOCK COMES WITH THE TAIL.
    # It is four brand cards plus a heading naming the donor, so carrying it
    # verbatim puts "If You Like Hiroki Golf" on a Found Golf page. Cut the
    # whole related section; btk-template.py renders our own from the spec.
    # DO NOT CUT THE RELATED SECTION OUT — NEUTRALISE IT.
    # It is <section class="more" data-btk="related">, not a div (the first cut
    # of this assumed a div and matched nothing). But deleting it outright is
    # also wrong: btk-template.py anchors on it to find the tail, and without it
    # the following <div class="more"> is not classified and the whole "More
    # from TGI" block — 63 words — is dropped. The template regenerates this
    # section from the spec anyway, so leave the shell and strip the donor's
    # name out of it.
    tail = re.sub(r'<section class="more" data-btk="related">.*?</section>\s*',
                  "", tail, count=1, flags=re.S)
    if "Hiroki" in tail:
        sys.exit("! donor name survived the tail cut — look at the related block")
    body.append(tail)

    page = head + "\n".join(body)
    k = page.rfind("</style>")
    if k < 0:
        sys.exit("! no </style> to attach CSS to")
    return page[:k] + EXTRA_CSS + page[k:]


def checks(page):
    owned = " ".join(SPEC["take"] + STORY + CODA + ART_INTRO
                     + [q for q, _ in QUOTES] + [a for _, a in FAQ])
    imgs = re.findall(r'src="(/images/found-golf/[^"]+)"', page)
    take_i = page.find('data-btk="take"')
    take_block = page[take_i:page.find("</section>", take_i)]
    out = [
        ("hero is this page's hero", HERO in page, ""),
        ("no donor brand anywhere",
         not [b for b in DONOR_BRANDS
              if b.lower() in re.sub(r'href="/drops/[^"]*"', "", page).lower()], ""),
        ("the take section has exactly two grid children",
         len(re.findall(r"^  <(?:div|aside)\b", take_block, re.M)) == 2, ""),
        ("TGI Take block present", "The TGI Take" in page, ""),
        ("FAQ heading is the house name", "The Questions" in page, ""),
        ("three pull-quotes", page.count('class="pull-quote"') == 3, ""),
        # EVERY .pull-quote-inner block, not the first one re.search finds.
        # The first block on this page is the 22px roman one; the 38px block
        # that actually wins sits lower, and an earlier version of this check
        # passed while the page rendered italic on screen.
        ("pull-quotes are roman in every rule block",
         all("font-style:italic" not in b
             for b in re.findall(r"\.pull-quote-inner\b[^{]*\{([^}]*)\}", page)),
         "a .pull-quote-inner block still sets italic"),
        ("art section present", "The Art Side" in page, ""),
        ("18 product cards", page.count('class="product-card"') == 18, ""),
        ("every local image exists",
         all((ROOT / p.lstrip("/")).exists() for p in imgs), f"{len(imgs)} refs"),
        ("no hot-linked images", "cdn.shopify" not in page, ""),
        ("every img has alt", len(re.findall(r"<img\b", page)) == page.count("alt="), ""),
        ("banned word absent from copy this script owns",
         not re.search(r"\bworth\b", owned, re.I), ""),
        ("prices carry a read date", "20 September 2026" in page, ""),
        # The MDW/UPTHERE venue is an inference from image filenames and was never
        # sourced. It must not appear on the page.
        ("unsourced venue inference absent",
         "UPTHERE" not in page and "Design Week" not in page, ""),
        ("held-back quote absent", "private jets" not in page, ""),
        ("every schema FAQ question is visible",
         all(re.sub(r"<[^>]+>", "", q) in page for q, _ in FAQ), ""),
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
