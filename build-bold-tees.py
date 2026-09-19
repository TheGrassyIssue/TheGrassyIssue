#!/usr/bin/env python3
"""
build-bold-tees.py — "The Bold Tee Edit". 19 September 2026.

Lenny's brief: a full refresh replacing the retired /drops/bold-tees-carousel.
Angle: the graphic tee grew up. 27 tees, one per brand, and both retired URLs
reclaimed (see wire-bold-tees.py for the redirect work).

WHY THIS REPLACES A DELETED PAGE RATHER THAN EDITING IT. The old carousel was a
homepage feed card pasted into a page shell — dead JS, truncated stylesheet, all
twelve write-ups locked inside a JavaScript array where a crawler saw 165 words.
Re-verification on 18 Sept also found five of its twelve products gone. It was
retired by delete-bold-tees.py; this is the rebuild.

WHAT THE SWEEP CHANGED ABOUT THE LINEUP, because the data drove it:
  · EIGHT BRANDS HERE ARE NEW TO TGI, and two of them are Austin: Butler Pitch &
    Putt, open since 1949 and running its own Comfort Colors program, and
    Southside Golf Co out of Manchaca. Neither had appeared on the site before.
  · MUNI KIDS IS ON BACKORDER, not in stock. Every size reports available:true,
    but /products/i-am-tiger-t-shirt.js shows inventory_quantity of -1, -1, -2,
    -4 and -2 against inventory_policy "continue". Two sourcing passes
    disagreed about this; reading the quantity rather than the flag settled it.
    The card says so, because a reader who orders expecting stock is owed that.
  · ODD RITUAL IS PRICED IN RAND. Lenny asked for them in and confirmed they
    ship to the US. Their store serves ZAR even with ?country=US, so R1,000 is
    what is printed. We do not convert. Their shipping-policy and FAQ pages both
    return broken/empty responses right now, so the US-shipping claim rests on
    Lenny's word and is NOT asserted in the page copy.
  · GUERRILLA GOLF DOES NOT TRACK INVENTORY (inventory_management is null on
    every variant), so "available" there is a default, not a count. Not claimed
    as in-stock anywhere in the copy.

STRUCTURE. Three sections, each price-ascending:
  The Muni Shirts (9)  — shirts about a place, and the shops that print them.
  The Heavyweights (12) — the ones that publish a fabric weight.
  The Art Tees (6)     — bought for the artwork.
The non-USD entry sorts last within its section so the price ladder reads clean.

Idempotent: byte-identical across consecutive runs. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = ROOT / "research/bold-tees.json"
SRC  = ROOT / "drops/the-hoodie-and-shorts-edit.html"   # furniture donor
OUT  = ROOT / "drops/the-bold-tee-edit.html"
SLUG = "/drops/the-bold-tee-edit"

TITLE = "The Bold Tee Edit &mdash; The Graphic Tee Grew Up"
DESC  = ("Twenty-seven graphic tees from independent golf brands, with live "
         "prices read 19 September 2026. Heavyweight cotton, real screen "
         "printing and made-in-USA runs &mdash; including two Austin shops.")
HERO  = "/images/bold-tees/hero.jpg"

# More from the Feed — four slugs. Image and title are READ FROM THE CATALOGUE,
# never written here.
#
# THE BUG THIS REPLACES: the first version hand-picked a bold-tees product shot
# for each card, so the Hat Edit card advertised a green T-SHIRT, the streetwear
# card another tee, and so on — four links to four different posts, all
# illustrated with tees from this post. A More card is a thumbnail OF THE POST IT
# LINKS TO; reusing local imagery because it is conveniently to hand misrepresents
# every destination. Hand-writing the titles was the same mistake one level down:
# I typed "The White Tee Edit 2026" when the post is actually called "The White
# Tee Edit — 17 From the Universe and Beyond". research/more-catalogue.json is
# the site's own registry of post name + hero image, so both now come from there
# and cannot drift from what the destination page actually says.
MORE_SLUGS = [
    "/drops/the-hoodie-and-shorts-edit",
    "/drops/best-golf-streetwear-brands-2026",
    "/drops/the-white-tee-edit-2026",
    "/drops/the-hat-edit-austin-summer",
]


def more_entries():
    cat = json.loads((ROOT / "research/more-catalogue.json").read_text(encoding="utf-8"))
    out = []
    for s in MORE_SLUGS:
        e = cat.get(s)
        if not e:
            sys.exit(f"! {s} is not in more-catalogue.json — cannot source its card")
        if not (ROOT / e["img"].lstrip("/")).exists():
            sys.exit(f"! catalogue image for {s} is missing: {e['img']}")
        out.append((s, e["img"], e["name"]))
    return out

SECTIONS = [
    # NOT "printed by Austin golf courses". Butler is a golf course and prints
    # its own; Southside is a label attached to an indoor facility, which is not
    # the same claim. The note says only what is true of both.
    ("muni", "m", "The Muni Shirts &mdash; 9",
     "Shirts about a place. Two of them come from Austin."),
    ("weight", "w", "The Heavyweights &mdash; 12",
     "The ones that publish a number. Ordered by the price their own store showed "
     "on 19 September 2026."),
    ("art", "a", "The Art Tees &mdash; 6",
     "Bought for the artwork, and built to survive it."),
]


def plain(s):
    return (s.replace("&mdash;", "—").replace("&middot;", "·")
             .replace("&amp;", "&").replace("&reg;", "®")
             .replace("&rsquo;", "’").replace("&ldquo;", "“")
             .replace("&rdquo;", "”").replace('"', "&quot;"))


def card(row, pref):
    """One product card.

    THE CARD MUST BE A <div class="product-card"> WITH THE LINK INSIDE IT, not
    an <a class="product-card"> wrapping everything. The anchor-shaped variant is
    what stranded six Brand to Know pages (task #640): btk-template.py searches
    for the literal '<div class="product-card"' and reports "no product cards"
    when it finds an anchor instead.
    """
    slug, brand, name, price, cur, purl, _img, desc = row
    src = f"/images/bold-tees/{pref}-{slug}.jpg"
    # Non-USD gets its currency spelled out; USD is the unmarked default.
    tag = f'{price} <span class="cur">{cur}</span>' if cur != "USD" else price
    return (
        f'    <div class="product-card">\n'
        f'      <div class="product-img"><img src="{src}" alt="{plain(brand + " " + name)}" loading="lazy" /></div>\n'
        f'      <div class="product-body">\n'
        f'        <div class="product-brand">{brand}</div>\n'
        f'        <div class="product-name">{name}</div>\n'
        f'        <div class="product-price">{tag}</div>\n'
        f'        <div class="product-desc">{desc}</div>\n'
        f'        <a href="{purl}" target="_blank" rel="noopener" class="product-link">'
        f'Visit {brand} &#8599;</a>\n'
        f'      </div>\n    </div>\n')


def more_block():
    cards = "\n".join(
        f'    <a href="{h}" class="more-card">\n'
        f'      <div class="more-card-img"><img src="{i}" alt="{plain(n)}" loading="lazy" /></div>\n'
        f'      <div class="more-card-body"><div class="more-card-name">{n}</div>'
        f'<div class="more-card-tag">The Edit</div></div>\n    </a>'
        for h, i, n in more_entries())
    return ('<!-- More from the Feed -->\n<div class="more">\n  <div class="more-hdr">\n'
            '    <span class="more-label">More from TGI</span>\n'
            '    <a href="/" class="more-link">See All &rarr;</a>\n  </div>\n'
            f'  <div class="more-grid">\n{cards}\n  </div>\n</div>\n\n')


EXTRA_CSS = """
/* --- bold-tees --- */
.tee-note{font-size:13px;line-height:1.7;opacity:.72;margin:18px 0 0;
          padding:14px 16px;border-left:2px solid var(--grass);}
"""


def money(price, cur):
    """Sort key. Non-USD sorts last within its section — a rand figure sitting
    between two dollar figures reads as a price jump that is not real."""
    n = float(re.sub(r"[^0-9.]", "", price))
    return (0 if cur == "USD" else 1, n)


def build():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    src = SRC.read_text(encoding="utf-8")

    head = src[:src.find('<div class="breadcrumb">')]
    tail = src[src.find("<footer"):]

    old = "Hoodie and Shorts &mdash; The Best Fall Combo"
    head = head.replace(old, TITLE).replace(plain(old), plain(TITLE))
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{DESC}"', head)
    head = re.sub(r'(property="og:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = re.sub(r'(name="twitter:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = head.replace("/drops/the-hoodie-and-shorts-edit", SLUG)
    head = re.sub(r'("description"\s*:\s*)"[^"]*"', rf'\1"{DESC}"', head, count=1)
    # Image swaps, BOTH forms. The donor carries relative /images/... paths AND
    # absolute https://thegrassyissue.com/images/... ones (og:image, twitter:image,
    # schema). Rewriting only the relative form left a previous post's share card
    # pointing at the donor's photograph — invisible on the page, wrong everywhere
    # the link gets pasted.
    head = re.sub(r'(content=")/images/[^"]*(")', rf'\1{HERO}\2', head)
    head = re.sub(r'(content=")https://thegrassyissue\.com/images/[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = re.sub(r'("image"\s*:\s*")[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = head.replace("</style>", EXTRA_CSS + "</style>", 1)

    allrows = spec["muni"] + spec["weight"] + spec["art"]
    # COMPUTE the sidebar facts rather than typing them. On the hoodie post a
    # hardcoded "Brands 18" was wrong by two; a number in a sidebar is a claim.
    n_brands = len({r[1] for r in allrows})
    usd = [r for r in allrows if r[4] == "USD"]
    lo = min(usd, key=lambda r: money(r[3], r[4]))[3]
    hi = max(usd, key=lambda r: money(r[3], r[4]))[3]
    # MANUFACTURE ONLY. The first version of this regex also matched "USA
    # Cotton", which is where the fibre was grown, not where the shirt was
    # sewn — it counted Badlands and would have counted Swag, turning a
    # material-origin line into a made-in-America claim in the sidebar.
    n_usa = sum(1 for r in allrows
                if re.search(r"made in (the )?usa|sewn in the usa|"
                             r"made in los angeles", r[7], re.I))
    # AUSTIN IS A FACT ABOUT THE BRAND, NOT ABOUT THE PROSE. The first version
    # counted rows whose description happened to contain "Austin" or "Manchaca",
    # and then an unrelated copy edit to Butler's card — removing an invented
    # drive time — silently dropped the count from 3 to 2 while the body text
    # still said three. A derived number must not depend on wording.
    AUSTIN = {"butler-pitch-and-putt", "southside-golf-co", "criquet"}
    slugs = {r[0] for r in allrows}
    if not AUSTIN <= slugs:
        sys.exit(f"! Austin roster names a slug not in the spec: {AUSTIN - slugs}")
    n_atx = len(AUSTIN)
    # NEW TO TGI = no page under brands/. The product slug is not always the
    # brand-page slug (manors-golf -> brands/manors.html, seamus-golf ->
    # brands/seamus.html), so an unmapped check reports two false positives.
    ALIAS = {"manors-golf": "manors", "seamus-golf": "seamus"}
    have = {p.stem for p in (ROOT / "brands").glob("*.html")}
    n_new = sum(1 for r in allrows if ALIAS.get(r[0], r[0]) not in have)
    # Small counts are spelled out in body copy — house voice. The first draft
    # interpolated the integer and rendered "8 of these brands are new".
    WORDS = {6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
             11: "Eleven", 12: "Twelve"}
    if n_new not in WORDS:
        sys.exit(f"! {n_new} new brands — no spelled form; extend WORDS")

    secs = []
    for key, pref, hdr, note in SECTIONS:
        rows = sorted(spec[key], key=lambda r: money(r[3], r[4]))
        body = "\n".join(card(r, pref) for r in rows)
        secs.append(f'<section class="products">\n'
                    f'  <h2 class="products-hdr">{hdr}</h2>\n'
                    f'  <div class="sec-note">{note}</div>\n'
                    f'  <div class="products-grid">\n\n{body}  </div>\n</section>\n')

    body = f'''<div class="breadcrumb">
  <a href="/#feed">Feed</a> / <a href="/#feed">The Edit</a> / The Bold Tee Edit
</div>

<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" alt="Three graphic tees worn on the back and front &mdash; Butler Pitch &amp; Putt&rsquo;s &lsquo;This ain&rsquo;t no country club&rsquo; shot at the course with downtown Austin behind, Gumtree&rsquo;s State Flower Reference Chart printed across the back, and the Reebok x Manors crest" /></div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:8px;">Butler Pitch &amp; Putt &middot; Gumtree Golf &amp; Nature Club &middot; Manors Golf &mdash; photographs courtesy of each brand</div>
</div>

<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>27 Tees</span><span class="dot"></span>
    <span>{n_brands} Brands</span><span class="dot"></span>
    <span>Prices read 19 September 2026</span>
  </div>
</header>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>The independent golf tee started as a joke on a blank.</strong>
    A gag about three-putts, a slogan about country clubs, screened onto whatever
    4.2-ounce shirt the local printer had in a box. It was funny, it was $18, and
    it went translucent by the second summer. That was the whole category for
    most of a decade.</p>

    <p>Read the product pages now and something has changed. Badlands publishes
    the construction: &ldquo;Heavy Weight Jersey / 100% USA Cotton / 6.5 sq oz |
    220 GSM / Side-seamed garment construction. 1x1 rib collar with straddle
    stitching.&rdquo; Casualist lists 380gsm and Made in Portugal. Walker names
    250gsm and a twin-needle stitch. Gumtree says its graphic is printed on 6.5oz
    American cotton and the shirt was sewn in the USA. Merrill gives you four
    lines and three of them are specification.</p>

    <p>That is the shift. Not that the graphics got better &mdash; they were
    always the good part &mdash; but that the thing underneath them turned into a
    garment somebody is willing to describe in public. A brand that prints its
    fabric weight has made a claim you can hold it to. A brand printing on a
    Comfort Colors blank is telling you exactly which garment-dyed body it chose.
    Five years ago almost nobody in this category published either.</p>

    <p>What follows is twenty-seven tees, one per brand, starting at {lo}.
    {WORDS[n_new]} of these brands are new to the site. Three of the twenty-seven
    are Austin businesses, and two of those three had never appeared here before.
    Every price was read off the brand&rsquo;s own store on 19 September 2026 and
    is reproduced in the currency that store displays.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Edit, Counted</div>
      <div class="sidebar-detail"><span class="l">Tees</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>{n_brands}</span></div>
      <div class="sidebar-detail"><span class="l">New to TGI</span><span>{n_new}</span></div>
      <div class="sidebar-detail"><span class="l">Austin brands</span><span>{n_atx}</span></div>
      <div class="sidebar-detail"><span class="l">Made in the USA</span><span>{n_usa}</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>{lo} &ndash; {hi}</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>19 Sept 2026</span></div>
      <div class="sidebar-detail"><span class="l">Sourced from</span><span>Each brand&rsquo;s own store</span></div>
      <a href="/brands" class="sidebar-cta">The Brand Index &rarr;</a>
      <a href="/drops/the-hoodie-and-shorts-edit" class="sidebar-cta" style="margin-top:8px;">Hoodie and Shorts &rarr;</a>
      <a href="/drops/the-white-tee-edit-2026" class="sidebar-cta" style="margin-top:8px;">The White Tee Edit &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#BoldTees</span>
        <span class="hashtag">#GraphicTee</span>
        <span class="hashtag">#TheEdit</span>
        <span class="hashtag">#MuniLife</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</div>

{secs[0]}
<div class="writeup">
  <div class="writeup-body">
    <p><strong>Two of these come out of Austin, and they arrived at the same
    sentence.</strong> Butler Pitch &amp; Putt has been a par-3 course by Lady
    Bird Lake since 1949, and the shop prints its own Comfort Colors rather than
    licensing the logo to a merch company. Southside Golf Co is PGA professional
    Justin Aragon&rsquo;s label out of Manchaca, attached to an indoor facility
    opening this month. One sells a shirt reading &ldquo;This ain&rsquo;t no
    country club.&rdquo; The other sells one reading &ldquo;No Country
    Club.&rdquo;</p>

    <p>That is the muni shirt in one image: the same sentence occurring to two
    people in the same city because it is the true thing to say about the place
    they work. Goat Hill Park in Oceanside sells &ldquo;World Class, Working
    Class.&rdquo; Muni Kids has been printing municipal-golf shirts in Portland
    since 2015. The category exists because public golf has a self-image and
    nobody else was going to print it.</p>
  </div>
</div>

{secs[1]}
<div class="writeup">
  <div class="writeup-body">
    <p><strong>What the numbers actually mean.</strong> Cotton weight is given
    two ways and they describe the same thing: ounces per square yard in the US,
    grams per square metre everywhere else. A standard fashion tee is around
    4.5oz, or 150gsm. Everything in the section above starts at 5.5oz and goes to
    380gsm, which is roughly double &mdash; the difference between a shirt that
    drapes and one that stands slightly away from you and keeps its shape through
    the wash.</p>

    <p>The second number is singles, and Seamus is the only brand here that
    prints it: 22-singles. Higher singles means finer yarn, which means a softer
    hand at the same weight. A 6.5oz shirt in 18-singles and a 6.5oz shirt in
    22-singles weigh the same and feel nothing alike. Garment-dyed is the third
    thing to look for &mdash; Swag, Fried Egg and Merrill all specify it &mdash;
    and it means the shirt was sewn first and dyed after, which is why those
    colours look slightly faded on day one and then stop moving.</p>
  </div>
</div>

{secs[2]}
<div class="writeup">
  <div class="writeup-body">
    <p><strong>Three notes before you click anything.</strong> Muni Kids&rsquo;
    I Am Tiger is sold on backorder &mdash; every size is purchasable, and every
    size currently shows negative inventory on their store, so it ships when they
    print more. Guerrilla Golf does not track inventory at all, so treat their
    sizes as a question for the shop rather than a promise. And Odd Ritual prices
    in South African rand; R1,000 is what their store charges, and we have not
    converted it into anything else.</p>

    <p>The last thing to notice is where the artwork went. The Gumtree shirt puts
    an entire reference chart of American state flowers across the back. Walker,
    Merrill, Southside, Seamus, Hidden Links, BOLD and Casualist all print front
    and back. Butler&rsquo;s whole statement is on the back, which is why the
    photograph at the top of this page is shot from behind. The chest logo has
    become the quiet half of the shirt, and the thing you are actually buying is
    facing the group behind you.</p>
  </div>
</div>

'''
    return head + body + more_block() + tail


def links_ok(page):
    bad = []
    for h in sorted(set(re.findall(r'href="(/drops/[^"#?]+)"', page))):
        s = h[len("/drops/"):].rstrip("/")
        if s == SLUG.split("/")[-1]:
            continue
        if not (ROOT / "drops" / f"{s}.html").exists():
            bad.append(h)
    return (not bad), ("broken: " + ", ".join(bad) if bad else "")


def main(apply_):
    page = build()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    allrows = spec["muni"] + spec["weight"] + spec["art"]
    brands = [r[1] for r in allrows]
    head = page[:page.find("<body")]

    checks = [
        ("27 product cards", page.count('<div class="product-card"') == 27,
         str(page.count('<div class="product-card"'))),
        ("cards are div-shaped, not anchor-shaped",
         '<a class="product-card"' not in page, ""),
        ("three product sections", page.count('<h2 class="products-hdr"') == 3, ""),
        ("spec holds 27 rows", len(allrows) == 27, str(len(allrows))),
        # HOUSE RULE: no repeat brands within a roundup. One tee per brand.
        ("no repeat brand anywhere on the page",
         len(set(brands)) == 27,
         str(sorted(b for b in set(brands) if brands.count(b) > 1))),
        ("every non-USD price carries its currency",
         all(f'{r[3]} <span class="cur">{r[4]}</span>' in page
             for r in allrows if r[4] != "USD"), ""),
        ("no currency was converted",
         not re.search(r'\(?(approx|USD equivalent|roughly \$)', page, re.I), ""),
        # Odd Ritual's shipping-policy page is broken, so the page must not
        # assert US shipping as fact anywhere in the copy.
        ("no unverified US-shipping claim for Odd Ritual",
         not re.search(r'Odd Ritual[^.]{0,120}ships? to the US', page, re.I), ""),
        # Muni Kids is on backorder. If a future edit drops that sentence the
        # page starts implying stock the brand does not have.
        ("Muni Kids backorder is disclosed",
         "backorder" in page.lower(), ""),
        ("Guerrilla Golf untracked inventory is disclosed",
         "does not track inventory" in page, ""),
        ("every local image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/bold-tees/[^"]+)"', page)), ""),
        # Scope: the 27 CARD images must all differ. The hero and the four
        # more-cards deliberately reuse product shots, so counting every src on
        # the page would fail a correct document.
        ("27 distinct product-card images",
         len(set(re.findall(r'class="product-img"><img src="([^"]+)"', page))) == 27,
         str(len(set(re.findall(r'class="product-img"><img src="([^"]+)"', page))))),
        ("no hot-linked images anywhere",
         not re.search(r'<img[^>]+src="https?://', page), ""),
        ("every img has alt", all('alt="' in i for i in re.findall(r"<img[^>]*>", page)), ""),
        ("banned word 'worth' absent", not re.search(r'\bworth\b', page, re.I), ""),
        ("every internal /drops/ link resolves", *links_ok(page)),
        ("has more-grid + aff disclosure",
         page.count('class="more-card"') == 4
         and page.count('class="aff-disclosure"') == 1, ""),
        ("the four More cards are distinct",
         len(set(re.findall(r'<a href="([^"]+)" class="more-card"', page))) == 4, ""),
        # A More card must be a thumbnail OF ITS DESTINATION. The first build
        # illustrated all four with bold-tees product shots, so the Hat Edit card
        # showed a T-shirt. No More card may use this post's own imagery.
        ("no More card uses this post's own product imagery",
         not re.search(r'class="more-card-img"><img src="/images/bold-tees/', page), ""),
        ("every More card image comes from its destination's own image folder",
         all(img.split("/")[2] != "bold-tees" for img in re.findall(
             r'class="more-card-img"><img src="([^"]+)"', page)), ""),
        ("More card titles match the catalogue verbatim",
         all(n in page for _s, _i, n in more_entries()), ""),
        ("sidebar brand count matches the data",
         f'<span class="l">Brands</span><span>{len(set(brands))}</span>' in page, ""),
        # EVERY SIDEBAR NUMBER IS A CLAIM. These three were hardcoded or loosely
        # labelled in the first draft: "Austin shops 3" counted Criquet, which is
        # an Austin brand but not a shop, and the made-in-USA regex also matched
        # "USA Cotton", which says where the fibre grew, not where the shirt was
        # sewn. Re-derive them here independently of the builder so a drift in
        # either the data or the regex fails the build rather than shipping.
        ("made-in-USA count is manufacture only, not fibre origin",
         f'<span class="l">Made in the USA</span><span>'
         f'{sum(1 for r in allrows if re.search(chr(114) and "made in (the )?usa|sewn in the usa|made in los angeles", r[7], re.I))}</span>'
         in page, ""),
        ("no fibre-origin row was counted as manufacture",
         not re.search(r'Made in the USA</span><span>'
                       + str(sum(1 for r in allrows
                                 if re.search(r"usa cotton|u\.s\. cotton", r[7], re.I))
                             + sum(1 for r in allrows
                                   if re.search(r"made in (the )?usa|sewn in the usa|"
                                                r"made in los angeles", r[7], re.I)))
                       + r'</span>', page), ""),
        # The sidebar figure, the body sentence and the roster must agree. They
        # did not after a copy edit changed Butler's card; this pins all three.
        ("Austin sidebar figure is 3",
         '<span class="l">Austin brands</span><span>3</span>' in page, ""),
        # Match against whitespace-collapsed text: the sentence is wrapped
        # across source lines, so a literal `in page` test fails a correct page.
        ("the body sentence agrees with the Austin figure",
         "Three of the twenty-seven are Austin businesses"
         in re.sub(r"\s+", " ", page), ""),
        ("all three Austin brands are actually on the page",
         all(f'/images/bold-tees/{p}-{s}.jpg' in page
             for p, s in (("m", "butler-pitch-and-putt"),
                          ("m", "southside-golf-co"), ("a", "criquet"))), ""),
        ("small counts in body copy are spelled, not numerals",
         not re.search(r'<p>[^<]{0,80}\b\d\b of these brands', page), ""),
        ("no invented drive time or distance survives",
         not re.search(r'\b(nine|ten|eight|five|two)\s+(minutes?|miles?)\s+'
                       r'(from|apart|away)', page, re.I), ""),
        # The hero shows three specific shirts. If an edit drops one, the hero
        # advertises something the reader cannot find below.
        ("all three hero garments are on the page",
         all(b in page for b in ("Butler Pitch &amp; Putt",
                                 "Gumtree Golf &amp; Nature Club", "Manors Golf")), ""),
        ("hero credits the brands it shows",
         "photographs courtesy of each brand" in page, ""),
        ("canonical points at this slug", SLUG in page, ""),
        ("no donor slug survives in the head",
         "the-hoodie-and-shorts-edit" not in head, ""),
        ("no donor imagery survives in the head",
         "/images/hoodie-shorts/" not in head, ""),
        ("og:image and twitter:image are this post's hero",
         all(HERO in m for m in re.findall(
             r'(?:og:image|twitter:image)" content="([^"]*)"', head)), ""),
        ("exactly one h1", len(re.findall(r"<h1", page)) == 1, ""),
        ("div balance", page.count("<div") == page.count("</div>"),
         f'{page.count("<div")}/{page.count("</div>")}'),
        ("section balance", page.count("<section") == page.count("</section>"), ""),
        ("anchor balance", len(re.findall(r"<a\b", page)) == page.count("</a>"), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d if not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {len(page):,} bytes")
    if apply_:
        OUT.write_text(page, encoding="utf-8")
        print(f"  wrote {OUT.name}")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
