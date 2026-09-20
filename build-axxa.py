#!/usr/bin/env python3
"""build-axxa.py — Brand to Know: AXXA. 20 September 2026.

Sydney's Northern Beaches, founded 2022, sits between surf and golf. New to TGI —
not in the Australian brands post and not on the brand index.

THE PRICE PROBLEM, WHICH IS THE WHOLE REASON THIS FILE IS CAREFUL.
axxa.com.au runs Shopify Markets with geolocation. Read from a US IP, the entire
storefront — the rendered pages AND /products.json AND /products/<handle>.js —
returns prices auto-converted to USD at 0.72652152. The Golf-Surf Club Hoodie
reads "$87" that way. AXXA's own price is A$119. Publishing the first number
would have been wrong by about 27% on every line, and wrong in the direction
that makes a brand look cheaper than it is.

research/axxa.json holds AUD figures read with ?country=AU, which is the store
speaking in its own currency rather than us doing arithmetic. The house rule is
that nothing gets converted, so the page prints A$ throughout and tells overseas
readers plainly that their own view of the store will differ. A guard below
refuses to build if a bare "$" ever appears next to a price.

THE FOUNDER. AXXA's own About page says the brand was "Founded in 2022 by then
14-year-old Axel", which puts him around 17 or 18 now. That is the brand's own
published claim about itself and is fair to report. It is also the whole of what
this page says about him: first name, the year, the age they state. No surname,
no school, no town beyond the region they publish, and the piece is not built
around his age as a novelty — the clothes are the subject.

MONETISED. Lenny holds an AXXA affiliate arrangement (GoAffPro) and a reader
code. Product links are left BARE here; apply-affiliates.py appends ?ref= and
adds rel="sponsored noopener" and the disclosure from data/affiliates.json. Do
not hand-write the ref into this file — one source of truth for the money.

Idempotent. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "drops/brand-to-know-hidden-links-society.html"     # furniture donor
DEST = ROOT / "drops/brand-to-know-axxa.html"
DATA = json.loads((ROOT / "research/axxa.json").read_text(encoding="utf-8"))
ROWS = {r[0]: r for r in DATA["rows"]}
F = DATA["facts"]

SLUG = "brand-to-know-axxa"
TITLE = "Brand to Know &mdash; AXXA"
DESC = ("AXXA, the Northern Beaches label built between surf and golf. Founded 2022, "
        "jacquard knits, the Golf-Surf Club line, and what it all costs in Australian dollars.")
HERO = "/images/axxa/hero.jpg"
STORE = "https://www.axxa.com.au"

CODE = "LENNY1085"
CODE_VALUE = "A$10 off"

FAQ = [
    ("Where is AXXA based?",
     "Sydney's Northern Beaches, in New South Wales. The brand describes itself as a "
     "coastal lifestyle label built between surf, golf and everyday life, and the product "
     "names carry the geography &mdash; the Manly Country Club line is the clearest example."),
    ("Is AXXA a golf brand or a surf brand?",
     "Both, deliberately. Their own line is that they are &ldquo;not defined by one sport "
     "or trend&rdquo;. In practice the catalogue splits between golf-specific pieces &mdash; "
     "polos in their own GolfComfort fabric, caps, a jersey &mdash; and heavyweight fleece "
     "and knitwear that works anywhere."),
    ("What do AXXA prices look like from outside Australia?",
     "Lower, but only on screen. The store converts to your local currency automatically, so "
     "a hoodie AXXA prices at A$119 can display as roughly US$87. That is a live conversion, "
     "not a discount, and your card is charged the equivalent either way. Every figure on "
     "this page is the Australian dollar price read from their own store."),
    ("Does AXXA ship internationally?",
     "They sell to the United States and elsewhere &mdash; the storefront switches currency "
     "by location, which is what the conversion above reflects. Shipping cost and timing are "
     "set at checkout and we have not tested a delivery, so check those before ordering."),
]

# ---- sections: (heading, kicker, [slugs], [paragraphs]) ---------------------
SECTIONS = [
    ("The Knitwear",
     "Three weights, and the graphic is knitted in rather than printed on.",
     ["brushed-surfer-knit", "golfer-knit", "staple-knit"],
     ["The knits are the most interesting thing AXXA makes, and the reason is construction "
      "rather than design. The surfer on the heaviest one and the golfer on the middle one "
      "are jacquard-knitted &mdash; worked into the fabric on the machine &mdash; not screen "
      "printed onto a finished jumper. That is a slower and less forgiving way to put an "
      "image on knitwear, and it is the difference between a motif that is part of the cloth "
      "and one sitting on top of it.",
      "They publish the weights, which not everyone does: 980g for the Brushed Surfer Knit in "
      "a nylon-viscose blend, 730g for the cotton Golfer Knit, 550g for the Staple. Those are "
      "substantial numbers. AXXA recommend sizing up if you want the relaxed fit the "
      "photography shows."]),

    ("The Golf-Surf Club Line",
     "AGSC on the art, and the closest thing they have to a uniform.",
     ["golf-surf-club-hoodie", "golf-surf-club-sweatshirt", "manly-country-club-hoodie",
      "birdies-please-hoodie", "no-bad-weather-hoodie", "chasing-landscapes-canvas-jacket"],
     ["Golf-Surf Club is the core, abbreviated to AGSC on the product art, and the hoodie is "
      "the piece the brand is built on &mdash; seven colourways and by some distance the "
      "deepest stock in the catalogue. The fleece is 420GSM at a 75/25 cotton-poly blend, cut "
      "oversized.",
      "Manly Country Club is the other running line, and the joke lands harder if you know "
      "that Manly is a real Northern Beaches suburb with a real golf club in it. The graphic "
      "does what good course merch does: reads as a members' sweatshirt from a distance and "
      "as something else entirely up close.",
      "The canvas jacket sits apart from the fleece &mdash; structured workwear cut, "
      "heavyweight cotton canvas, a back graphic. It is the one piece here that has nothing "
      "to do with either sport."]),

    ("The Polos",
     "Their own fabric, and the only pieces built specifically to swing in.",
     ["liney-lip-out-polo", "blossom-bogey-polo", "paper-par-polo"],
     ["The polos run on what AXXA call GolfComfort &mdash; a polyester-spandex blend they "
      "describe as moisture-wicking and quick-drying, in a regular rather than oversized fit. "
      "Naming your own fabric is a small thing that tells you the golf side is not an "
      "afterthought.",
      "All three are at A$59 and all three are thin on stock at the time of writing: the Liney "
      "Lip Out has one size left, the Paper Par two. The Anchor Ace, which draws the warmest "
      "review on their own site from a buyer playing in Queensland heat, is sold out entirely."]),

    ("Caps, Tees and the Anniversary Jersey",
     "Where the brand is funniest, and where it keeps count.",
     ["golf-bag-cap", "surf-then-golf-cap", "too-cold-to-golf-tee", "shop-closed-tee",
      "golf-bag-tee", "3-year-jersey"],
     ["The Surf Then Golf cap carries the brand's entire argument stitched across the front "
      "&mdash; <em>Surf in the morning, Golf in the arvo</em> &mdash; and it is the single "
      "most Australian object in the catalogue. The Golf Bag Cap is the quieter one: canvas "
      "crown, corduroy brim, an embroidered bag on the front.",
      "The tees are 270GSM cotton in an oversized box fit, which is heavier than the usual "
      "graphic tee and cut deliberately loose. Too Cold To Golf and Shop Closed are both "
      "printed front and back.",
      "The 3 Year Jersey is the one that dates the brand. A retro football kit marking three "
      "years, which AXXA say is limited to fifty pieces and will not be restocked, and whose "
      "product page describes the run so far as coming &ldquo;from a 14 year olds dream&rdquo;. "
      "It has been discounted from A$80."]),
]

# THE SIDEBAR. Dropped from the first build, which is a bigger miss than it
# looks. Assembling this page as donor-head + donor-nav + my sections + donor-tail
# silently discarded the <aside> that sits between the nav and the first prose
# section, so the page shipped without the Details card every other Brand to Know
# carries — AND without the anchor apply-affiliates.py uses to place the FTC
# disclosure. The result was a page with eighteen affiliate links, a reader
# coupon, and no notice that any of it earns a commission. Nothing reached a
# reader, but that is the defect this block exists to close.
#
# Price range is computed from the rows rather than typed, so it cannot drift
# from the cards, and it carries the A$ prefix like everything else here.
_prices = [r[3] for r in DATA["rows"]]
SIDEBAR = f'''  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Sydney, Australia</span></div>
      <div class="sidebar-detail"><span class="l">Known For</span><span>Apparel, Headwear</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2022</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>{len(DATA["rows"])} items</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>A${min(_prices):g} &ndash; A${max(_prices):g}</span></div>
      <a href="{STORE}/" target="_blank" rel="noopener" class="sidebar-cta">Shop AXXA &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#axxa</span>
        <span class="hashtag">#brandtoknow</span>
        <span class="hashtag">#apparel</span>
        <span class="hashtag">#headwear</span>
      </div>
    </div>
  </aside>'''

LOOK_A = [("life-course-tee", "Manly Country Club on the fairway"),
          ("life-coast-knit", "The heavyweight knit, on the cliffs"),
          ("life-coast-hoodie", "Golf-Surf Club at dusk")]
LOOK_B = [("life-cap-course", "Surf in the morning, golf in the arvo"),
          ("life-cap-held", "The embroidery, close"),
          ("life-pair-hoodies", "420GSM fleece, both ways"),
          ("life-sunset-pair", "No such thing as bad weather"),
          ("life-cream-tee", "270GSM, box fit"),
          ("life-back-graphic", "The back graphic, coast side")]


def _classless(page):
    """Class names in the markup that nothing in this page ever styles.

    verify-post.py caught seven of these on the first build — .product-grid,
    .faq-item, .faq-a, .product-price, .product-was, .product-note,
    .btk-story-h. Every one looked like a house class and none of them existed,
    so eighteen cards and the whole FAQ would have shipped unstyled. My own
    guards had only checked that the markup was PRESENT. Presence is not the
    property that matters; being a class the stylesheet knows about is.
    """
    used = set()
    for attr in re.findall(r'class="([^"]+)"', page):
        used.update(c for c in attr.split() if c)
    return sorted(c for c in used
                  if not re.search(r"\." + re.escape(c) + r"[\s,{:.]", page))


def money(v):
    """AUD, always labelled. Never a bare dollar sign — see the guard."""
    return f"A${v:g}"


def card(slug, n):
    """House card structure, copied from the donor rather than invented.

    The naming is counter-intuitive and was worth checking rather than guessing:
    .product-brand carries the PRODUCT NAME and .product-name carries the PRICE.
    The first version of this function used a .product-grid wrapper and its own
    .product-price / .product-was / .product-note classes — none of which have a
    rule anywhere in the stylesheet, so all eighteen cards would have rendered
    full-width and unstyled. verify-post.py caught it; my own guards did not,
    because they checked that cards EXISTED rather than that they sat in the
    house grid with classes the CSS knows about.
    """
    s, name, cat, aud, was, avail, total, url, _img, spec = ROWS[slug]
    price = money(aud)
    if was:
        price += f' <span class="axxa-was">{money(was)}</span>'
    low = (f'<div class="axxa-note">Low stock &mdash; {avail} of {total} left</div>'
           if avail <= 2 else "")
    return f'''<div class="product-card" id="p-{n}">
      <img src="/images/axxa/{s}.jpg" alt="AXXA {name}" loading="lazy" />
      <div class="product-body">
        <div class="product-brand">{name}</div>
        <div class="product-name">{price}</div>
        <div class="product-desc">{spec}.</div>
        {low}<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>'''


# Two classes the donor stylesheet has no rule for, because the donor never
# showed a struck-through price or a stock note. Injected once, in the page's
# own <style>, rather than left to fall back to unstyled text.
EXTRA_CSS = """
/* --- axxa: was-price and low-stock note --- */
.axxa-was{opacity:.5;text-decoration:line-through;font-weight:400;margin-left:6px;}
.axxa-note{font-family:var(--mono);font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;color:#a33;margin:6px 0 2px;}
"""


def band(frames, cls="btk-wild-grid"):
    out = [f'  <div class="{cls}">']
    for slug, alt in frames:
        out.append(f'    <img src="/images/axxa/{slug}.jpg" alt="AXXA &mdash; {alt}" loading="lazy">')
    out.append("  </div>")
    return "\n".join(out)


def build():
    src = SRC.read_text(encoding="utf-8")
    head = src[:src.find("<body")]

    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>",
                  head, count=1, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\1{DESC}"', head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\1{TITLE}"', head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*"', rf'\1{DESC}"', head, count=1)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*"', rf'\1{TITLE}"', head, count=1)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', rf'\1{DESC}"', head, count=1)
    head = re.sub(r'(<(?:meta property="og:image"|meta name="twitter:image") content=")[^"]*"',
                  rf'\1https://thegrassyissue.com{HERO}"', head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*"',
                  rf'\1https://thegrassyissue.com/drops/{SLUG}"', head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*"',
                  rf'\1https://thegrassyissue.com/drops/{SLUG}"', head, count=1)

    # The donor's Article JSON-LD and FAQPage are about Hidden Links Society.
    # Both are replaced wholesale — shipping another brand's FAQs to Google under
    # this URL is the exact bug the Agronomy build hit.
    head = re.sub(r'("headline"\s*:\s*)"[^"]*"', rf'\1"{TITLE.replace("&mdash;", "—")}"', head, count=1)
    head = re.sub(r'("description"\s*:\s*)"[^"]*"', rf'\1"{DESC.replace("&mdash;", "—")}"', head, count=1)
    head = re.sub(r'("datePublished"\s*:\s*)"[^"]*"', r'\1"2026-09-20"', head, count=1)
    head = re.sub(r'("dateModified"\s*:\s*)"[^"]*"', r'\1"2026-09-20"', head, count=1)
    head = re.sub(r'"@id"\s*:\s*"https://thegrassyissue\.com/drops/[^"]*"',
                  f'"@id": "https://thegrassyissue.com/drops/{SLUG}"', head)
    # mainEntityOfPage is a SEPARATE field from @id and the donor set it to its
    # own slug. Left alone it publishes structured data saying this URL is the
    # Hidden Links Society post.
    head = re.sub(r'"mainEntityOfPage"\s*:\s*"[^"]*"',
                  f'"mainEntityOfPage": "https://thegrassyissue.com/drops/{SLUG}"', head)
    # And the Article's "about" names the brand the piece covers. The donor's
    # said Hidden Links Society — i.e. Google would have been told this page is
    # about a company it does not mention. Same failure class as the donor
    # FAQPage; both are replaced rather than patched around.
    head = re.sub(r'"about"\s*:\s*\{[^}]*\}',
                  '"about": {"@type": "Brand", "name": "AXXA", "url": "https://www.axxa.com.au/"}',
                  head, count=1)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q),
                              "acceptedAnswer": {"@type": "Answer",
                                                 "text": re.sub(r"<[^>]+>", "", a)
                                                 .replace("&mdash;", "—").replace("&ldquo;", "“")
                                                 .replace("&rdquo;", "”").replace("&rsquo;", "’")}}
                             for q, a in FAQ]}
    # LAMBDA, NOT A STRING. json.dumps emits “ for curly quotes, and re.sub
    # parses backslashes in a replacement STRING as escapes — "bad escape \u".
    # A callable replacement is passed through untouched. ensure_ascii=False
    # keeps the real characters in the output as well.
    faq_block = ('<script type="application/ld+json">\n'
                 + json.dumps(faq_ld, indent=1, ensure_ascii=False) + "\n</script>")
    head = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context"[^<]*?"@type":\s*"FAQPage".*?</script>',
        lambda _m: faq_block, head, count=1, flags=re.S)

    nav = src[src.find("<body"):src.find('<section class="products"')]
    nav = re.sub(r'(<img[^>]+class="post-hero"[^>]*src=")[^"]*"', rf'\1{HERO}"', nav)
    nav = re.sub(r"(<h1[^>]*>).*?(</h1>)", rf"\g<1>{TITLE}\g<2>", nav, count=1, flags=re.S)
    nav = re.sub(r'(<img[^>]+src=")[^"]*"([^>]*class="post-hero")', rf'\1{HERO}"\2', nav)
    if HERO not in nav:      # donor markup varies; force the hero in
        nav = re.sub(r'(<img[^>]+src=")[^"]*\.jpg"', rf'\1{HERO}"', nav, count=1)

    k = head.rfind("</style>")
    if k < 0:
        sys.exit("! no </style> in the donor head to attach card CSS to")
    head = head[:k] + EXTRA_CSS + head[k:]

    body = [nav]

    body.append(f'''<section class="products" data-btk="story">
  <h2 class="products-hdr">The Story</h2>
  <p class="cat-kicker">Northern Beaches, 2022, and a catalogue that refuses to pick a sport.</p>
  <div class="writeup-body">
    <p>AXXA describes itself as &ldquo;a youth-driven coastal lifestyle brand born on Sydney&rsquo;s Northern Beaches, built in the space between surf, golf, and everyday life.&rdquo; That is a lot of positioning for one sentence, and most brands that write it are describing a mood board. This one is describing the photography, which is the test that matters: the same jumper appears on a fairway at golden hour and on a clifftop above the break, shot the same week.</p>
    <p>It started in 2022. The brand&rsquo;s own line is that it was &ldquo;founded in 2022 by then 14-year-old Axel&rdquo;, and the anniversary jersey describes the run since as coming &ldquo;from a 14 year olds dream to a growing Axxa family across Australia and beyond&rdquo;. They publish a first name and leave it there, and so will we.</p>
    <p>The useful thing about the surf half is that it explains the clothes. A golf brand that only thinks about golf makes polos and caps and stops. AXXA makes 980g jacquard knitwear and a canvas workwear jacket, because the customer they have in mind is in the water at seven and on the first tee after lunch and at the pub after that. Their phrasing for it &mdash; &ldquo;the coastal rhythm of surf, golf, mates, and living well, all in one day&rdquo; &mdash; is marketing copy, but the catalogue actually matches it.</p>
  </div>
{SIDEBAR}
{band(LOOK_A)}
</section>''')

    n = 0
    for hdr, kicker, slugs, paras in SECTIONS:
        ps = "\n".join(f"    <p>{p}</p>" for p in paras)
        numbered = []
        for s in slugs:
            n += 1
            numbered.append(card(s, n))
        cards = "\n    ".join(numbered)
        body.append(f'''<section class="products">
  <h2 class="products-hdr">{hdr}</h2>
  <p class="cat-kicker">{kicker}</p>
  <div class="writeup-body">
{ps}
  </div>
  <div class="products-grid">
    {cards}
  </div>
</section>''')

    body.append(f'''<section class="products" data-btk="look">
  <h2 class="products-hdr">The Argument, Photographed</h2>
  <p class="cat-kicker">Same pieces, two coastlines, one afternoon.</p>
{band(LOOK_B)}
</section>''')

    body.append(f'''<section class="products" data-btk="cost">
  <h2 class="products-hdr">What It Costs From Here</h2>
  <p class="cat-kicker">The number you see is probably not the number AXXA set.</p>
  <div class="writeup-body">
    <p>Every price on this page is in Australian dollars, read from AXXA&rsquo;s own store. If you open that store from the United States it will not show you these numbers. Shopify converts automatically by location, so the Golf-Surf Club Hoodie AXXA prices at {money(119)} displays at roughly US$87 from a US address &mdash; a live exchange rate doing its work, not a sale, and your card settles the equivalent either way.</p>
    <p>We are flagging it because the gap is about a quarter of the price and it runs in the flattering direction. A reader who sees US$87, orders, and then reads a statement in Australian dollars has not been overcharged, but they have been surprised, and being surprised by a number is the part that sours a purchase.</p>
    <p>Lenny has an arrangement with AXXA that gets TGI readers <strong>{CODE_VALUE}</strong> with the code <strong>{CODE}</strong> at checkout. The value is quoted in Australian dollars, as everything here is. Shipping to the US is set at checkout and we have not run an order through, so treat the delivery estimate as theirs rather than ours.</p>
  </div>
</section>''')

    faq_html = "\n".join(
        f'    <details open class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ)
    body.append(f'''<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <p class="cat-kicker">The four that come up, answered from their own material.</p>
  <div class="faq">
{faq_html}
  </div>
</section>''')

    tail = src[src.find('<section class="more-from"'):] if '<section class="more-from"' in src \
        else src[src.rfind("<footer"):]
    body.append(tail)

    return head + "\n".join(body)


def main(apply_):
    page = build()
    flat = re.sub(r"\s+", " ", page)
    bodytxt = page[page.find("<body"):]
    words = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bodytxt)).split())
    prices = re.findall(r"A\$\d", page)

    # Text the SCRIPT owns — used to scope the banned-word check away from the
    # donor's More-from cards, which carry other posts' titles.
    owned = "\n".join([DESC] + [p for _, _, _, ps in SECTIONS for p in ps]
                      + [a for _, a in FAQ] + [q for q, _ in FAQ])

    checks = [
        ("every product rendered", page.count('class="product-card"') == 18,
         str(page.count('class="product-card"'))),
        ("all 18 slugs used once",
         all(page.count(f"/images/axxa/{s}.jpg") == 1 for s in ROWS), ""),
        # THE CURRENCY GUARD. A bare "$12" anywhere in body copy means a price
        # slipped in unlabelled, which on this brand is the difference between
        # AUD and a US-converted figure. US$ is allowed because the cost section
        # names that currency deliberately.
        ("no unlabelled dollar figures",
         not re.search(r"(?<![AU])(?<!US)\$\d", re.sub(r"A\$\d", "", bodytxt)), ""),
        ("prices are present and AUD-labelled", len(prices) >= 18, str(len(prices))),
        ("no converted USD price printed as AXXA's own",
         "$87" not in bodytxt.replace("US$87", ""), ""),
        ("the conversion is disclosed to readers",
         "converts automatically" in flat or "Shopify converts automatically" in flat, ""),
        ("coupon code and value both stated",
         CODE in page and CODE_VALUE in page, ""),
        # Product links stay BARE. apply-affiliates.py owns the ref param.
        ("no affiliate ref hand-written into product links",
         "ref=gfinczjd" not in page, ""),
        ("founder is named no further than the brand does",
         page.count("Axel") <= 2 and not re.search(r"\bAxel\s+[A-Z]", page), ""),
        ("hero is this post's hero", page.count(HERO) >= 1, ""),
        ("the house sidebar is present",
         page.count("<aside class=\"sidebar\">") == 1
         and page.count("</aside>") == 1, ""),
        # THE ANCHOR GUARD, AND THE POINT OF IT. apply-affiliates.py places the
        # FTC disclosure by replacing the first "</aside>". This page is
        # monetised — ref-tagged product links plus a reader coupon — so if that
        # anchor is missing the disclosure silently does not appear and the page
        # ships taking a commission without saying so. Asserting the LINKS exist
        # was never enough; the hook the disclosure hangs on has to exist too.
        ("the affiliate disclosure has an anchor to land on",
         "</aside>" in page, ""),
        ("sidebar price range matches the cards",
         f"A${min(_prices):g}" in page and f"A${max(_prices):g}" in page, ""),
        ("two lookbook bands", page.count('class="btk-wild-grid"') == 2, ""),
        ("lookbook frames all distinct",
         len(set(re.findall(r"/images/axxa/(life-[a-z-]+)\.jpg", page)))
         == len(LOOK_A) + len(LOOK_B), ""),
        # SCOPE TO THE MARKUP, NOT THE CLASS NAME. The first version searched
        # from page.find("btk-wild-grid"), which matches the CSS rule in the
        # <style> block long before any grid markup — so "after the first band"
        # actually meant "after the stylesheet", and the page's own hero <img>
        # tripped it. Anchor on the opening tag instead.
        ("hero not reused in a band",
         "hero.jpg" not in page[page.find('<div class="btk-wild-grid">'):], ""),
        ("every local image exists",
         all((ROOT / p.lstrip("/")).exists()
             for p in re.findall(r'src="(/images/axxa/[^"]+)"', page)), ""),
        ("no hot-linked images", "cdn.shopify" not in page, ""),
        ("every img has alt", len(re.findall(r"<img\b", page)) == page.count("alt="), ""),
        ("banned word absent from copy this script owns",
         not re.search(r"\bworth\b", owned, re.I), ""),
        ("every schema FAQ question is visible",
         all(re.sub(r"<[^>]+>", "", q) in page for q, _ in FAQ), ""),
        ("visible FAQ count matches schema",
         page.count('class="faq-q"') == len(FAQ), ""),
        ("cards sit in the house products-grid",
         page.count('class="products-grid"') == len(SECTIONS)
         and 'class="product-grid"' not in page, ""),
        # THE ONE verify-post.py CAUGHT AND I DID NOT. Every class this page
        # emits must have a rule somewhere in it, or the markup renders naked.
        ("every class this page emits has a CSS rule",
         not _classless(page), ", ".join(_classless(page))),
        ("no donor brand left in the head",
         "hidden-links" not in page[:page.find("<body")].lower()
         and "Hidden Links" not in page[:page.find("<body")], ""),
        ("canonical points at this slug",
         f'href="https://thegrassyissue.com/drops/{SLUG}"' in page, ""),
        ("word count is a feature, not a stub", words >= 1200, str(words)),
        ("exactly one h1", page.count("<h1") == 1, ""),
        ("div balance", page.count("<div") == page.count("</div>"), ""),
        ("section balance", page.count("<section") == page.count("</section>"), ""),
        ("anchor balance", len(re.findall(r"<a\b", page)) == page.count("</a>"), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}{('  ' + d) if d and not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    # count the MARKUP, not the bare string — 'product-card' also appears in the
    # stylesheet, which inflates this to 23.
    n_cards = page.count('class="product-card"')
    print(f"\n  {len(page):,} bytes / {words} words / {n_cards} products")
    if apply_:
        DEST.write_text(page, encoding="utf-8")
        print(f"  wrote {DEST.name}")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
