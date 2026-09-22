#!/usr/bin/env python3
"""build-bag-upgrade.py — "Upgrading Your Golf Bag", three makers. 22 Sep 2026.

Lenny: "post about upgrading your golf bag - 3 brands that are a step above",
naming Shapland, Shoal and Jones, then: "it's a step above, worth the extra
money, more considered bags and beats that hand-me-down or thrift store find."

TWO NOTES ON HOW THAT BRIEF GOT WRITTEN.

The word "worth" is banned site-wide and verify-post.py fails on it, so the
argument is made without it — the bag earns the money, it is chosen rather than
inherited. Lenny set that rule; the brief was describing the idea, not the word.

The hand-me-down line is angled rather than quoted. TGI's readers walk municipal
courses — "more parking-lot beer than member-guest" is the site's own tag — so
copy telling them their inherited bag is not good enough reads down at the
audience it is written for. The version here keeps the upgrade argument and puts
it on the object: the thing you carry for four hours a week should be chosen.

FACTS, all read 22 September 2026 from each brand's own storefront, USD
confirmed via og:price:currency or JSON-LD priceCurrency, nothing converted:
  Shapland Rye 4.0      $495  SOLD OUT, every variant, all five models
  Shoal Standard Bag    $450  preorder; Sage and White live; next window 1 Nov,
                              ships 15 Dec
  Jones Texas Trouper   $410  in stock, Moon Gray
Shapland's sold-out state is stated on the card and again in the closing
section. Lenny's call, and the honest one — a reader finds out here rather than
after clicking.

HERO, SECOND PASS. The first hero was Shapland's colour range lined up across a
fairway, cut from a 1868px square. Lenny asked for something else and
specifically for Jones. Their site turned out to publish almost no landscape
imagery at all — the homepage renders nothing above 600px and the entire
250-product catalogue holds exactly one frame wider than it is tall. That one
frame is the hero now, and it is the right picture anyway: a golfer walking a
fairway with the bag on its single strap, which is the argument the post makes.
1600x686 at 21:9, no upscaling, house hero size exactly.

Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import re
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/the-custom-wedge-report.html"
OUT = ROOT / "drops/upgrading-your-golf-bag.html"
SLUG = "/drops/upgrading-your-golf-bag"
TITLE = "Upgrading Your Golf Bag — Three Makers a Step Above"
# THE ONLY LANDSCAPE FRAME JONES PUBLISHES. Their homepage renders nothing over
# 600px and their whole 250-product catalogue contains exactly one image wider
# than it is tall — this one, a golfer walking a fairway with the Original Jones
# Bag on its single strap. At 1600px wide a 21:9 band is 1600x686, which is the
# house hero size, so it lands at spec with no upscaling. It is also the most
# on-message picture available: the post argues for the walker.
HERO_SRC = "https://cdn.shopify.com/s/files/1/0693/6587/products/I3I1334-medium.jpg"
HERO = "/images/jones-sports-co/bag-upgrade-hero.jpg"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}

BRANDS = [
 ("Shapland", "shapland", "SOLD OUT \u00b7 RESTOCKING THIS MONTH",
  "Three models, one silhouette, and a line that has been sold out since August. "
  "Restock dates are on each card.", [
  dict(brand="Shapland", name="Rye 4.0", price=495, note="Sold out",
       url="https://shaplandbags.com/products/rye-4-0", dir="shapland",
       frames=["rye-4-group","rye-4-navy","rye-4-collar","rye-4-blue"],
       alt="The Shapland Rye 4.0 stand bag",
       desc="The Rye is the flagship, named for Harry Colt&rsquo;s first course. Carbon "
            "fibre stand legs come wrapped in hickory by Caddy Wrap, the seven-ounce "
            "oiled leather trim darkens with use, and the whole bag weighs five pounds "
            "seven ounces. The August run sold out in under a day. The next batch is "
            "due mid-November."),
  dict(brand="Shapland", name="Kantle 3.1", price=490, note="Sold out",
       url="https://shaplandbags.com/products/kantle-3-1", dir="shapland",
       frames=["kantle-31-a","kantle-31-b","kantle-31-c","kantle-31-d"],
       alt="The Shapland Kantle 3.1 stand bag",
       desc="The Kantle carries two separate shoulder straps so it works single or "
            "double, over an eight-inch four-way top with three-quarter-length "
            "dividers. Same oiled leather trim as the Rye, same waterproof canvas and "
            "rainhood, five pounds ten ounces on the shoulder. Ten colours are due back "
            "in late September, Honey and Burgundy among them."),
  dict(brand="Shapland", name="Sunday 3.1", price=425, note="Sold out",
       url="https://shaplandbags.com/products/sunday-3-1", dir="shapland",
       frames=["sunday-31-a","sunday-31-b","sunday-31-c"],
       alt="The Shapland Sunday 3.1 carry bag",
       desc="The Sunday is the cheapest way into the line and the one built on marine "
            "canvas, with a hard plastic bottom and removable straps that switch it "
            "between backpack and single carry. The four-way top measures six inches by "
            "eight and it still takes fourteen clubs. Five colours return in late "
            "September."),
 ]),
 ("Shoal Golf Co.", "shoal", "ONE BAG \u00b7 TEN COLOURS \u00b7 PREORDER",
  "Shoal builds a single model and opens ordering in windows. These are three of the "
  "ten colourways, and which you can have depends on when you are reading.", [
  dict(brand="Shoal Golf Co.", name="The Shoal Standard Bag &middot; Sage", price=450, note="",
       url="https://shoalgolfco.com/products/the-shoal-standard-bag-preorder-sage",
       dir="shoal-golf",
       frames=["standard-sage","standard-sage-legs","standard-sage-angle","standard-sage-back"],
       alt="The Shoal Standard Bag in sage canvas",
       desc="Shoal makes one bag and sells it in windows rather than holding stock. The "
            "Standard is canvas over a light frame, cut plain &mdash; no contrast "
            "piping, no panelling, nothing that dates it to a season. Sage is one of two "
            "colours still live from the August run."),
  dict(brand="Shoal Golf Co.", name="The Shoal Standard Bag &middot; White", price=450, note="",
       url="https://shoalgolfco.com/products/the-shoal-standard-bag-preorder-white",
       dir="shoal-golf",
       frames=["standard-white","standard-white-b","standard-white-c","standard-white-d"],
       alt="The Shoal Standard Bag in white canvas",
       desc="The same bag in an off-white canvas that will show a season on it, which is "
            "what the material is for. Shoal sells the whole thing on one line, "
            "&ldquo;crafted for the walk&rdquo;, and builds it narrow enough to sit flat "
            "on your back. Also live from the August run."),
  dict(brand="Shoal Golf Co.", name="The Shoal Standard Bag &middot; Navy", price=450, note="Sold out",
       url="https://shoalgolfco.com/products/the-shoal-standard-navy-bag",
       dir="shoal-golf",
       frames=["standard-navy","standard-navy-b","standard-navy-c","standard-navy-d"],
       alt="The Shoal Standard Bag in navy canvas",
       desc="Navy is the darkest of the ten and the one that carries a season of use "
            "without showing it. It went in the August run and has not come back. The "
            "next preorder window opens 1 November, and those bags are scheduled to ship "
            "15 December."),
 ]),
 ("Jones Sports Co", "jones", "PORTLAND, SINCE 1971 \u00b7 IN STOCK",
  "Jones runs the oldest manufacturing operation of the three, and it is the only one "
  "here you can order from this afternoon. These three cover two hundred and "
  "twenty-five dollars of range.", [
  dict(brand="Jones Sports Co", name="Texas Trouper &middot; Moon Gray", price=410, note="",
       url="https://www.jonessportsco.com/products/texas-trouper-moon-gray",
       dir="jones-sports-co",
       frames=["texas-trouper-clubhouse","texas-trouper-lockers","texas-trouper-texas",
               "texas-trouper-longhorns"],
       alt="The Jones Texas Trouper carry bag in moon gray",
       desc="The Trouper is the Jones bag with stand legs and a four-way top that keeps "
            "the old narrow profile. The Texas colourway runs burnt orange across moon "
            "grey with the longhorn on the hip pocket. In Austin that is the local bag."),
  dict(brand="Jones Sports Co", name="Utility X &middot; Olive", price=355, note="",
       url="https://www.jonessportsco.com/products/utility-x-olive",
       dir="jones-sports-co",
       frames=["utility-x-a","utility-x-b","utility-x-c","utility-x-d"],
       alt="The Jones Utility X stand bag in olive",
       desc="The Utility X sits between the Original and the Trouper on price, and Jones "
            "describes it as a decade of refinement on one idea rather than a new one. "
            "That is the right description for a company that has spent fifty years "
            "subtracting. Olive, in stock."),
  dict(brand="Jones Sports Co", name="Original Jones Bag &middot; Navy/White", price=185, note="",
       url="https://www.jonessportsco.com/products/original-jones-bag-navy-white",
       dir="jones-sports-co",
       frames=["original-jones-a","original-jones-b","original-jones-c","original-jones-d"],
       alt="The Original Jones Bag in navy and white",
       desc="This is the 1971 bag, still built on George Jones&rsquo;s stylings and still "
            "unstructured: water-resistant nylon, a retro single strap, three pockets and "
            "nothing else. It is the cheapest bag here by a hundred and seventy dollars "
            "and the only one that predates everything else in the post."),
 ]),
]

BAGS = [b for _, _, _, _, bs in BRANDS for b in bs]

INTRO = [
 "Shapland, Shoal and Jones build the same object three different ways, and all "
 "three treat a carry bag as something you choose rather than something you end "
 "up with.",

 "Most golfers do end up with one. The bag in the boot came from a brother-in-law, "
 "or a pro shop clearance rack, or a set someone bought whole in 2014. It works. "
 "It holds fourteen clubs and it stands up, and there is nothing wrong with playing "
 "muni golf out of a bag that owes you nothing. But it is the piece of equipment you "
 "are in contact with for four hours at a time and never actually swing, and at some "
 "point that becomes the argument for picking one on purpose.",

 "What the three have in common is restraint. None of them is selling you storage. "
 "Shapland rebuilds a 1980s Ping silhouette in leather and brass and names its models "
 "after Harry Colt golf courses. Shoal makes a single canvas bag in ten colours and "
 "opens ordering a few times a year. Jones has been making the same single-strap "
 "carry bag in Portland since 1971 and has spent fifty years leaving things off it. "
 "Three different centuries of reference, one shared instinct: a bag should be quiet, "
 "light, and built to still look like itself in ten years.",

 "They run from a hundred and eighty-five dollars to four hundred and ninety-five, "
 "and the top of that band is where the material changes &mdash; canvas and "
 "top-grain leather instead of printed polyester, brass instead of moulded plastic, "
 "stitching you can see. It is also where the runs get small enough that a bag you "
 "want is frequently not in stock. Shapland has been sold out since August. Its next "
 "two production runs finish this month and the third lands in November, which is "
 "the useful thing to know before the restock rather than after it.",

 "This is for the walker. Somebody carrying or pushing, playing a public course most "
 "weeks, who has looked down at the bag on the tee and thought about it.",
]

ESSAY = [
 ("What the extra money is buying",
  "MATERIAL",
  "The gap between a two-hundred-dollar bag and a five-hundred-dollar one is not "
  "pockets. It is what the panels are made of and how the load is carried.",
  ["Mainstream stand bags are built from printed polyester over a moulded frame, with "
   "plastic hardware and a bonded strap. They are light, they are weatherproof, and "
   "they are finished. Nothing about them improves.",
   "Canvas and leather go the other way. Shapland trims the Rye in top-grain leather "
   "and hangs it on antique brass, the two materials in a golf bag that look better "
   "after a season than they did in the box. Shoal&rsquo;s canvas does the same thing "
   "more quietly. Both will mark, and the marks are the point.",
   "The second difference is the strap. Jones built its reputation on a single strap "
   "at a time when the industry had decided double straps were settled, and the "
   "Trouper still carries that geometry &mdash; the bag sits diagonally across the "
   "back and swings clear of the legs when you walk. Shapland engineers around the "
   "same problem from the other direction, with a double harness it describes as the "
   "most comfortable carry it can build. Neither is universally right. Both are a "
   "decision, which is more than most bags contain.",
   "Then there is the frame. A carry bag lives or dies on its stand mechanism, and "
   "all three of these use metal legs with a serviceable pivot. Shapland sells "
   "replacement legs on its own site for twenty dollars in aluminium and thirty-five "
   "in carbon fibre, which tells you what it expects the bag to outlast.",
   "The last thing the money buys is scarcity, and that cuts both ways. A brand "
   "making a few hundred bags a year can specify leather and brass because it is not "
   "costing a container load. It also means the bag you want is frequently not there. "
   "Shapland is sold out across its entire range as this goes up; Shoal sells in "
   "windows and tells you the ship date in advance. Only Jones, which has the oldest "
   "manufacturing operation of the three, behaves like a shop you can walk into.",
   "None of that makes a mainstream stand bag a bad object. A $230 bag from a large "
   "manufacturer is lighter than all three of these, more weatherproof than two of "
   "them, and available in your size on a Tuesday. The case for spending more is "
   "narrower than the marketing on either side suggests: you are buying materials "
   "that age, a frame you can service, and a silhouette that will not look like 2026 "
   "in 2031."]),
 ("Before you buy",
  "AVAILABILITY",
  "Two of the three are not a straightforward add-to-cart, and you should know that "
  "before you click.",
  ["<strong>Shapland is sold out, and that is the reason to read this now.</strong> "
   "Every bag, every colourway, all five models. But the restock dates are published "
   "and they are close. Kantle 3.1 and Sunday 3.1 are both scheduled to finish their "
   "next production run in late September &mdash; this week, as this goes up. Kantle "
   "returns in ten colours including Honey, Burgundy, Chocolate and Forest Green; "
   "Sunday in five. The Rye 4.0 is the longer wait: the batch released on 27 August "
   "sold out in under twenty-four hours, and the next one is due mid-November in the "
   "same colours. The email list on shaplandbags.com is where those go out.",
   "<strong>Shoal is preorder.</strong> Sage and white are available from the August "
   "run, which is shipping now. The next window opens 1 November with bags scheduled "
   "to ship 15 December, which makes it a Christmas bag if you order in the autumn "
   "and a spring bag if you do not.",
   "<strong>Jones is in stock.</strong> The Texas Trouper ships today at $410, and "
   "the core line sits below it &mdash; the Original Jones Bag at $185, the Players "
   "Series at $225, the Utility X at $355 and the standard Trouper at $395. If you "
   "want to spend four hundred dollars on a bag this afternoon, this is the one you "
   "can.",
   "All prices were read from each brand&rsquo;s own storefront on 22 September 2026 "
   "and are in US dollars."]),
]

# THE DONOR CARRIES A FAQPage BLOCK IN ITS HEAD. Splicing a new body in left the
# schema promising questions that appeared nowhere on the page — verify-post.py
# caught it, and Google treats schema-only FAQ as a violation because the markup
# has to describe visible content. Stripping the schema was the lazy fix. These
# are the questions a reader of this particular post actually arrives with, so
# they get answered on the page and the schema is rebuilt from this same list.
FAQ = [
    ("When do Shapland bags come back in stock?",
     "Sooner than the sold-out banner suggests. Shapland has published dates for its "
     "next production runs: the Kantle 3.1 and the Sunday 3.1 are both scheduled to "
     "finish in late September 2026, and the Rye 4.0 is due mid-November 2026. The "
     "27 August run of Rye bags sold out in under twenty-four hours, so the mailing "
     "list on shaplandbags.com is the practical way to catch the next one."),
    ("When does the next Shoal bag ship?",
     "Shoal sells in preorder windows rather than holding stock. The August run is "
     "shipping now, with sage and white still available. The next window opens 1 "
     "November 2026 and those bags are scheduled to ship 15 December 2026."),
    ("Which of the three can you order today?",
     "Jones. The Texas Trouper is in stock at $410, and the rest of the line sits "
     "below it &mdash; the Original Jones Bag at $185, the Players Series at $225, "
     "the Utility X at $355 and the standard Trouper at $395."),
    ("Why does a carry bag cost $450?",
     "Materials and run size. At this level the panels are canvas and the trim is "
     "top-grain leather over brass hardware rather than printed polyester and "
     "moulded plastic, and the makers build a few hundred units a year rather than "
     "a container load. Both choices cost money, and both are why the bags sell out."),
    ("What is the Shapland Rye named after?",
     "Rye Golf Club on the south coast of England, the first course Henry Shapland "
     "Colt designed. The brand takes its name from Colt as well; he went on to "
     "influence Alister MacKenzie, Donald Ross and Charles Hugh Alison."),
]


def cut_hero(apply_):
    raw = urllib.request.urlopen(urllib.request.Request(HERO_SRC, headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    ch = round(w / (21 / 9))
    if ch > h:
        sys.exit(f"! hero source too short for 21:9 — {w}x{h}")
    top = round((h - ch) * 0.25)          # keeps the golfer cap-to-shoes;
                                          # 0.46 cut his head off
    band = im.crop((0, top, w, top + ch))
    tw = min(2000, w)                      # never upscale
    band = band.resize((tw, round(tw / (21 / 9))), Image.LANCZOS)
    p = ROOT / HERO.lstrip("/")
    print(f"  hero: {w}x{h} -> {band.size[0]}x{band.size[1]} (crop y{top})")
    if apply_:
        p.parent.mkdir(parents=True, exist_ok=True)
        band.save(p, "JPEG", quality=88, optimize=True, progressive=True)
    return band.size


def gallery(b):
    fr = "".join(
        f'<div class="pg-frame"><img src="/images/{b["dir"]}/{f}.jpg" '
        f'alt="{b["alt"]} &middot; view {i+1} of {len(b["frames"])}" loading="lazy" /></div>'
        for i, f in enumerate(b["frames"]))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
        f'aria-label="View image {i+1}"></button>' for i in range(len(b["frames"])))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(b["frames"])}</span>'
            f'<div class="pg-dots">{dots}</div></div>')


def card(b):
    meta = f'&middot; ${b["price"]}' + (f' &middot; {b["note"]}' if b["note"] else "")
    return (f'<div class="product-card" data-frames="{len(b["frames"])}">'
            f'{gallery(b)}'
            f'<div class="product-body">'
            f'<div class="product-brand">{b["brand"]}</div>'
            f'<div class="product-name">{b["name"]} {meta}</div>'
            f'<div class="product-desc">{b["desc"]}</div>'
            f'<a href="{b["url"]}" target="_blank" rel="noopener" class="product-link">'
            f'Shop &#8599;</a></div></div>')


def body():
    intro = "\n    ".join(f"<p>{p}</p>" for p in INTRO)
    sections = ""
    for label, anchor, kick, lede, bags in BRANDS:
        grid = "\n      ".join(card(b) for b in bags)
        sections += (f'\n<section class="products">\n<h2 id="{anchor}">{label}</h2>\n'
                     f'<p class="cat-kicker"><strong>{kick}</strong>{lede}</p>\n'
                     f'<div class="products-grid">\n      {grid}\n</div>\n</section>\n')
    essays = ""
    for h2, kick, lede, paras in ESSAY:
        ps = "\n    ".join(f"<p>{p}</p>" for p in paras)
        essays += (f'\n<section class="products">\n'
                   f'<h2 id="{h2.split()[0].lower()}">{h2}</h2>\n'
                   f'<p class="cat-kicker"><strong>{kick}</strong>{lede}</p>\n'
                   f'</section>\n<div class="writeup">\n  <div class="writeup-body">\n    '
                   f'{ps}\n  </div>\n</div>\n')
    qs = "\n    ".join(
        f'<details open class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ)
    faq = (f'\n<div class="writeup">\n  <div class="writeup-body">\n'
           f'  <h2 class="products-hdr sec">Questions</h2>\n'
           f'  <div class="faq">\n    {qs}\n  </div>\n  </div>\n</div>\n')
    essays += faq
    return f"""<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>9 Bags</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" alt="A golfer walking a fairway carrying the Original Jones Bag on its single strap" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    {intro}
  </div>
</div>

{sections}
{essays}"""


def main(apply_):
    cut_hero(apply_)
    donor = DONOR.read_text(encoding="utf-8")

    head_end = donor.find("</head>")
    open_body = donor.find(">", donor.find("<body")) + 1
    hero = donor.find('<div class="drop-hero"', open_body)
    header = donor.find('<header class="drop-header"', open_body)
    more = donor.find('<div class="more"', open_body)
    if min(head_end, open_body, header, hero, more) < 0:
        sys.exit("! donor structure not recognised")
    if not header < hero < more:
        sys.exit("! donor blocks are out of expected order")

    page = donor[:header] + body() + donor[more:]

    # THE BREADCRUMB SITS ABOVE <header class="drop-header">, SO THE SPLICE MISSES
    # IT. First render of this page carried "The Custom Wedge Report — Stamping
    # Shops, Forged Makers and What 'Custom' Actually Means" across the top. Same
    # class of bug as the donor hero on the Hat & Towel Edit: the splice point was
    # chosen for where the new content starts, not for where the old content ends.
    # The guard below now reads the whole body rather than the post-header slice,
    # which is why it did not catch this the first time.
    # REBUILD THE WHOLE ELEMENT rather than pattern-match inside it. The first
    # attempt anchored on the last <span>/</span> and replaced [^<\n]+ after it.
    # Spaces are neither "<" nor a newline, so the regex backtracked and matched
    # the two characters of indentation — it "succeeded", reported one
    # substitution, and left the donor's title exactly where it was. A count of 1
    # is not evidence that the right thing was replaced.
    crumb = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
             '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  '
             + TITLE + '\n</div>')
    page, n_bc = re.subn(r'<div class="breadcrumb">.*?</div>',
                         lambda m: crumb, page, count=1, flags=re.S)
    if not n_bc:
        sys.exit("! breadcrumb not found — it would still name the donor post")

    # head: title, description, canonical, og/twitter, JSON-LD headline
    desc = ("Shapland, Shoal and Jones build a carry bag as something you choose. "
            "Three bags from $410 to $495, with what the money buys and what is in stock.")
    def sub(pat, rep, s):
        s2, n = re.subn(pat, lambda m: rep, s, count=1)
        if not n:
            sys.exit(f"! head pattern not found: {pat[:44]}")
        return s2
    h = page[:page.find("</head>")]
    h = sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h)
    h = sub(r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{desc}"', h)
    h = sub(r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="https://thegrassyissue.com{SLUG}"', h)
    for p, r in ((r'<meta property="og:title" content="[^"]*"',
                  f'<meta property="og:title" content="{TITLE}"'),
                 (r'<meta property="og:description" content="[^"]*"',
                  f'<meta property="og:description" content="{desc}"'),
                 (r'<meta property="og:url" content="[^"]*"',
                  f'<meta property="og:url" content="https://thegrassyissue.com{SLUG}"'),
                 (r'<meta name="twitter:title" content="[^"]*"',
                  f'<meta name="twitter:title" content="{TITLE}"'),
                 (r'<meta name="twitter:description" content="[^"]*"',
                  f'<meta name="twitter:description" content="{desc}"')):
        h = re.sub(p, lambda m: r, h, count=1)
    # A LAMBDA, NOT A STRING. json.dumps escapes the em-dash in TITLE to —,
    # and re.sub parses backslash escapes in a plain replacement string — it read
    # \u as a bad escape and raised. A lambda returns the text literally.
    headline = '"headline": ' + json.dumps(TITLE)
    h = re.sub(r'"headline"\s*:\s*"(?:[^"\\]|\\.)*"', lambda m: headline, h, count=1)

    # Rebuild the FAQPage schema from the SAME list that rendered on the page, so
    # the two cannot drift. Strip the HTML entities — schema text is plain text.
    def plain(s):
        return (s.replace("&mdash;", "—").replace("&rsquo;", "’")
                 .replace("&ldquo;", "“").replace("&rdquo;", "”"))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": plain(q),
                                         "acceptedAnswer": {"@type": "Answer",
                                                            "text": plain(a)}}
                                        for q, a in FAQ]}, ensure_ascii=False)
    h2, n_ld = re.subn(r'\{\s*"@context"[^{]*?"@type"\s*:\s*"FAQPage".*?\}(?=\s*</script>)',
                       lambda m: faq_ld, h, count=1, flags=re.S)
    if not n_ld:
        sys.exit("! no FAQPage block in the donor head to replace")
    h = h2
    h = re.sub(r'"url"\s*:\s*"https://thegrassyissue\.com/drops/[^"]*"',
               lambda m: f'"url": "https://thegrassyissue.com{SLUG}"', h)
    page = h + page[page.find("</head>"):]

    # ---- guards, read on the finished page ----
    bad = []
    # READ FROM <body>, NOT FROM THE HEADER. The first version started this slice
    # at <header class="drop-header"> — i.e. at the content it had just written —
    # so the donor's breadcrumb, sitting immediately above, was outside the
    # window and shipped naming the wrong post. A guard that only inspects what
    # you generated cannot find what you failed to replace.
    body_all = page[page.find(">", page.find("<body")) + 1:page.find('<div class="more"')]
    body_only = page[page.find('<header class="drop-header"'):page.find('<div class="more"')]
    if "custom-wedges" in body_all:
        bad.append("donor imagery survived in the body")
    for phrase in ("Show Out", "Vokey", "wedge", "Grindworks", "Custom Wedge Report"):
        if phrase.lower() in re.sub(r"<[^>]+>", " ", body_all).lower():
            bad.append(f"donor copy survived above or below the splice: {phrase!r}")
    for b in BAGS:
        for f in b["frames"]:
            if not (ROOT / f"images/{b['dir']}/{f}.jpg").is_file():
                bad.append(f"missing image {b['dir']}/{f}.jpg")
    n_cards = body_only.count('<div class="product-card"')
    if n_cards != len(BAGS):
        bad.append(f"{n_cards} cards, expected {len(BAGS)}")
    if body_only.count('<div class="products-grid">') < 1:
        bad.append("no products-grid wrapper — cards will render full width")
    words = len(re.sub(r"<[^>]+>", " ", body_only).split())
    if words < 1200:
        bad.append(f"{words} words, verify-post.py needs 1200")
    if re.search(r"\bworth\b", re.sub(r"fort worth", "", re.sub(r"<[^>]+>", " ", body_only), flags=re.I), re.I):
        bad.append("banned word in body copy")
    if bad:
        sys.exit("! " + "\n    ".join(bad))

    print(f"  {len(BAGS)} cards, {sum(len(b['frames']) for b in BAGS)} frames, {words} words")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    OUT.write_text(page, encoding="utf-8")
    print(f"  wrote {OUT.relative_to(ROOT)} ({len(page)//1024} KB)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
