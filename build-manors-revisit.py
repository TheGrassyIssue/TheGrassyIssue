#!/usr/bin/env python3
"""build-manors-revisit.py — the September 2026 refresh of the Manors
brand-to-know page. 22 September 2026.

Lenny: "I want a core section, a new drop section, plus all the other stuff,
use the kingfisher page as a template" and then "do 6 from new collection and 9
from core collection. ALso in the write up, pull good quotes, and talk about the
greenskeeper pants. Pull lookbook and blog images. They have the best social
media production in golf."

WHAT THIS ADDS, IN PAGE ORDER
  1. The Greenskeeper Problem   prose, the requested write-up
  2. three elevated pull-quotes flair, hackers, street (no prose section)
  3. In the Wild                six-frame editorial grid from the Sanity CMS
  4. New from the Collection    6 cards, the September drop
  5. The Core Collection        9 cards, the permanent range
  6. three more FAQs

THE EXISTING SIXTEEN CARDS ALL CARRY STALE PRICES, AND THAT IS WHY THIS TOUCHES
THEM. The page was built on 2 September against a slightly different conversion
and every card reads $1-2 high — Club C $176 against $174 live, Harrington $243
against $241, all sixteen. A page that prints "read 22 September" next to a
September drop cannot carry August numbers three sections further down. Prices
are corrected from a live read; NO OTHER WORD of the existing cards changes.

PRICES ARE READ, NEVER CONVERTED. Every figure below came off manorsgolf.com
with the footer reporting "United States ($ USD)", on 22 September 2026. The
Shopify products.json returns GBP because GBP is the store's base currency, so
it is useless for this; the rendered US storefront is the only honest source.
The earlier instinct to convert from GBP is exactly the error Lenny caught with
"wait, they have a US store".

ALL FIFTEEN WERE CHECKED FOR STOCK INDIVIDUALLY, not by the word "sold out"
appearing in the DOM. Shopify keeps a hidden "Variant sold out or unavailable"
option label on every product regardless of stock, which reported four
brand-new Kingfisher arrivals as gone. None of these fifteen is sold out.

FRAMES WERE CHOSEN BY LOOKING. localise-manors-revisit.py renders
research/manors/contact-products.jpg; the orders below lead with a worn shot
over a flat packshot wherever both exist, which is why several start at index 1
or 2 rather than 0.

THE TITLE AND META DESCRIPTION ARE DELIBERATELY UNTOUCHED. This page runs a
1.9% CTR, the best of any brand page on the site. A refresh is not a reason to
rewrite the one headline that is already winning.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-manors.html"
READ_DATE = "22 September 2026"
MARK, END = "<!-- TGI-MANORS-REVISIT -->", "<!-- /TGI-MANORS-REVISIT -->"

# ---------------------------------------------------------------- products ---
# (stem, display name, price, handle, [frame order], description)
NEW_DROP = [
    ("new-merino-hoodie", "Merino Tech Hoodie", "$301", "merino-tech-hoodie", [1, 0, 2],
     "One hundred per cent merino, which Manors calls the game&rsquo;s original "
     "performance fabric. A hoodie is not a traditional golf garment, and this one "
     "sits at the top of the range."),
    ("new-ripstop-vest", "Ripstop Tech Vest", "$214", "ripstop-tech-vest", [0, 1],
     "Manors builds this one in recycled TORAY ripstop, two-way stretch and water "
     "repellent. Ripstop earned its reputation outdoors on durability, long before "
     "golf took an interest."),
    ("new-primaloft-cardigan", "Heritage Primaloft&reg; Cardigan", "$214",
     "heritage-primaloft%C2%AE-cardigan", [0, 1, 2],
     "A cardigan is about as golden-age as golf knitwear gets. This one is rebuilt "
     "in Primaloft Active Evolve, an open structure that holds warmth without bulk."),
    ("new-primaloft-quarterzip", "1/4 Zip Primaloft&reg; Mid-Layer", "$187",
     "1-4-zip-primaloft%C2%AE-mid-layer", [1, 0, 3, 2],
     "The insulation ultramarathon runners have used for years, cut into the "
     "colour-blocked quarter-zip shape Manors has made its own."),
    ("new-ripstop-trouser", "Ripstop Tech Trouser", "$201", "ripstop-tech-trouser",
     [2, 3, 0, 1],
     "Recycled TORAY ripstop cut slim, with enough stretch in it to bend over a "
     "putt. Elasticated waistband, water and wind repellent."),
    ("new-ranger-mockneck", "Ranger Mockneck Polo", "$127", "mockneck-ranger-polo",
     [1, 0, 3, 2],
     "Manors runs its signature curved style lines through this one, with tonal "
     "mesh gussets set under the arms. A mockneck replaces the collar, which is the "
     "most 2026 thing in the drop."),
]
CORE = [
    ("core-pleated-trouser", "Lightweight Pleated Trouser", "$174",
     "greenskeeper-chino-trousers", [1, 0, 2, 3],
     "Chinos built in Primeflex&trade; for stretch and lightness, with double "
     "pleats and a ticket pocket sized for a scorecard."),
    ("core-greenskeeper-short", "Recycled Greenskeeper Shorts", "$147",
     "recycled-greenskeeper-shorts", [2, 3, 0, 1],
     "Worker pockets and classic double pleats sit in a water- and wind-resistant "
     "recycled performance fabric. This is the Greenskeeper idea at summer length."),
    ("core-course-gilet", "Insulated Course Gilet", "$214", "insulated-course-gilet",
     [0, 3, 1, 2],
     "The 2.0 update uses comfortemp&reg; thermal insulation. A gilet is the most "
     "useful thing on a British golf course and Manors treats it that way."),
    ("core-highland-fleece", "Highland Mockneck Fleece", "$161",
     "highland-mockneck-fleece", [0, 1, 2, 3],
     "Gridded fleece, warm enough to wear alone and light enough to layer. This is "
     "the piece doing the most work between October and March."),
    ("core-ranger-jacket", "Ranger Golf Jacket", "$187", "track-jacket", [0, 1, 3, 2],
     "Manors asked out loud why golf is the only sport without an iconic tracksuit "
     "to warm up in. This is the top half of its answer."),
    ("core-arc-polo", "Arc Polo", "$127", "arc-polo", [0, 1, 3, 2],
     "A twin-tipped collar and a relaxed fit sit against Seawool&reg; fabric. This "
     "is the clearest case of the brand running heritage and performance in one "
     "garment."),
    ("core-course-polo", "Course Polo", "$87", "course-polo", [1, 3, 0, 2],
     "The 2.0 update puts the house polo in soft Seawool&reg;. It is the entry "
     "point to the range and the shirt most often on the models."),
    ("core-logo-tee", "Manors Logo T-Shirt", "$61", "manors-logo-t-shirt", [0, 2, 1, 3],
     "Manors cuts this from 240gsm cotton in a relaxed fit, with a small chest "
     "logo. It is the cheapest thing on the rail and the easiest way in."),
    ("core-retro-crown-cap", "Retro Crown Cap", "$61", "retro-crown-cap", [1, 2, 0, 3],
     "A baseball classic gets adapted for the course: one size, adjustable "
     "snapback, sitting low on the head."),
]

# ------------------------------------------------------------------- prices ---
# handle -> USD as manorsgolf.com displayed it on 22 Sep 2026, US market.
LIVE = {
    "reebok-x-manors-club-c-revenge-golf": "$174",
    "manors-x-reebok-harrington-jacket": "$241",
    "manors-x-reebok-mockneck-polo": "$127",
    "gentleman-jack-x-manors-blade-polo": "$114",
    "gentleman-jack-x-manors-merino-crewneck-mens": "$281",
    "outside-polartec-polo": "$114",
    "outside-polartec-hoodie": "$174",
    "quarter-zip-tech-mid-layer": "$161",
    "recycled-greenskeeper-trouser": "$174",
    "lightweight-course-jacket": "$214",
    "work-trousers": "$187",
    "heritage-check-polo": "$114",
    "reversible-v-neck-vest": "$161",
    "club-polo": "$127",
    "tour-shirt": "$161",
    "blade-putter-headcover-copy": "$67",
}
LOW, HIGH, TOTAL = "$61", "$301", 31

# ----------------------------------------------------------------- editorial ---
WILD = [
    ("wild-clifftop", "A golfer in a Manors polo at the finish of a tee shot on a "
     "clifftop fairway with the sea and a rock stack behind",
     "Clifftop tee shot, sea stack behind"),
    ("wild-flag", "A golfer photographed from behind in a Manors jacket with the "
     "MANORS back print, lifting a yellow flag out of the hole",
     "The back print, doing the work"),
    ("wild-pileon", "Four golfers piling onto each other laughing on a fairway "
     "lined with pines", "Whatever just happened on that green"),
    ("wild-desert", "A golfer mid-swing on a desert course with red rock buttes on "
     "the skyline", "Red rock on the skyline"),
    ("wild-wall", "A golfer in a Manors graphic t-shirt standing against a pink "
     "painted wall under a LUBRI sign", "Off the course entirely"),
    ("wild-clubhouse", "A group portrait of around fifteen people in Manors "
     "clothing inside a wood-floored hall", "The whole crew, indoors"),
]

# --------------------------------------------------------------------- copy ---
GREENSKEEPER = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="greenskeeper">The Greenskeeper Problem</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>The clearest object in the current range is a pair of trousers designed for the person who mows the grass rather than the person playing on it. The Recycled Greenskeeper Trouser is $174, cut from 93% recycled nylon with 7% elastane, with four-way stretch, a PFC-free water-resistant finish, an elasticated waistband with a drawcord and eight storage pockets. Manors describes the double pleat at the front as a nod to &ldquo;timeless on-course etiquette.&rdquo;</p>
    <p style="margin-top:16px">Read that spec sheet with the name taken off and it is a technical golf trouser. Read the silhouette and it is maintenance-shed workwear. That is the argument the brand has been having with itself since 2023, settled inside one garment: the fabric is from this decade, the shape is from the shed behind the pro shop, and neither is pretending to be the other.</p>
    <p style="margin-top:16px">The Lightweight Pleated Trouser at $174 runs the same idea through Primeflex&trade;, with a ticket pocket sized for a scorecard. The Recycled Greenskeeper Shorts at $147 carry the pockets and the pleats into summer. All three hang in the range at once, which is the point. Manors did not replace the original half of its argument. It added the other half alongside.</p>
  </div>
</section>
"""

# PULL-QUOTES, NOT A PROSE SECTION. The first version of this refresh put three
# sourced quotes in an "In Their Words" section as body copy. Lenny: elevate all
# three and dissolve the section. Three quotes stacked as paragraphs read as a
# list; the same three set as pull-quotes carry the argument through the page.
#
# THE QUOTES ARE LIFTED, NOT DUPLICATED. This page's two existing pull-quotes
# appear nowhere else in the body, so that is the house pattern: a pull-quote is
# the only place its words appear. The "hackers" quote is therefore cut out of
# the Who They Were paragraph rather than echoed, and that paragraph is rewritten
# to stand up without it and without a forward reference to the quote below.
#
# SPACING IS A GATE, NOT A PREFERENCE. verify-post fails on two pull-quotes
# stacked with no prose between them. Final order, each separated by a section:
#   Story -> [flair] -> Pictures -> [technical polo] -> Who They Were ->
#   [archive] -> A Change of Course -> [hackers] -> Greenskeeper -> [street] ->
#   In the Wild -> September -> Core
# The last two sit inside this script's own block; [flair] is inserted above it
# under its own marker so a rerun can strip it cleanly.


def pull_quote(text, attr):
    return (f'\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n')


PQ_FLAIR = pull_quote(
    "It&rsquo;s one of the only sports where you can actually choose what to "
    "look like and how to dress. That&rsquo;s such a unique opportunity, and I "
    "don&rsquo;t feel like there&rsquo;s much flair on the tour anymore.",
    "Jojo Regan, co-founder, to Hypebeast, 2021")
PQ_HACKERS = pull_quote(
    "You have hackers up and down the country who aren&rsquo;t part of a club, "
    "or are part of a club because it&rsquo;s a community. That message was "
    "being lost.",
    "Jojo Regan, co-founder, to Hypebeast, 2021")
PQ_STREET = pull_quote(
    "We wanted to get away from current products, which are tight fitting and "
    "you wouldn&rsquo;t want to be seen walking down the street in.",
    "Nick Watts, Fashion Director, to Hypebeast, 2021")

FLAIR_MARK, FLAIR_END = "<!-- TGI-MANORS-PQ1 -->", "<!-- /TGI-MANORS-PQ1 -->"
PICTURES_ANCHOR = '<section class="products" style="margin-top:4px;">\n  <h2 id="the-pictures">'

# The Who They Were paragraph, with the quote lifted out of it.
WTW_OLD = ("Regan put it more plainly: the country-club stereotype "
           "&ldquo;frustrates us because it&rsquo;s wrong. You have hackers up "
           "and down the country who aren&rsquo;t part of a club, or are part of "
           "a club because it&rsquo;s a community. That message was being "
           "lost.&rdquo; The brand backed it up")
WTW_NEW = ("Regan&rsquo;s objection was not that the country-club image was "
           "unappealing but that it was inaccurate. The brand backed it up")


def wild_grid():
    figs = "\n  ".join(
        f'<figure><img src="/images/manors/{stem}.jpg" alt="{alt}" loading="lazy" />'
        f'<figcaption class="ig-cap">{cap}</figcaption></figure>'
        for stem, alt, cap in WILD)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 id="in-the-wild">In the Wild</h2>
  <p class="cat-kicker"><strong>Photography &middot; Manors&rsquo; own channels</strong>The case for Manors being the best-photographed label in golf does not get made on the product page. It gets made on the road: Scottish coastline, a desert highway, a hall full of people who clearly turned up together. In most of these frames the clothes are incidental, which is why they work. All photography below is Manors&rsquo; own.</p>
  <div class="ig-grid">
  {figs}
</div>
</section>
"""


def card(pid, stem, name, price, handle, order, desc, kicker):
    n = len(order)
    frames = [f"/images/manors/{stem}.jpg" if k == 0 else
              f"/images/manors/{stem}-a{k+1}.jpg" for k in order]
    pg = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="Manors {re.sub(r"&[a-z]+;", "", name)} '
        f'&middot; view {i+1} of {n}" loading="lazy" /></div>'
        for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
        f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (
        f'<div class="product-card" id="{pid}" data-frames="{n}">'
        f'<div class="product-gallery"><div class="pg-track">{pg}</div>'
        f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
        f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
        f'<span class="pg-count">1/{n}</span>'
        f'<div class="pg-dots">{dots}</div></div>'
        f'<div class="product-body">'
        f'<div class="product-brand">Manors &middot; {kicker}</div>'
        f'<div class="product-name">{name} &middot; {price}</div>'
        f'<div class="product-desc">{desc}</div>'
        f'<a href="https://manorsgolf.com/products/{handle}" target="_blank" '
        f'rel="noopener" class="product-link">Shop &#8599;</a>'
        f'</div></div>'), frames


def grid(items, hid, heading, kicker, kicker_lead, kicker_body, start, tag):
    cards, files = [], []
    for n, (stem, name, price, handle, order, desc) in enumerate(items):
        c, f = card(f"p-{start + n}", stem, name, price, handle, order, desc, tag)
        cards.append(c)
        files += f
    body = "\n".join(cards)
    return f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">{kicker}</div>
  <h2 class="products-hdr" id="{hid}">{heading}</h2>
  <p class="cat-kicker"><strong>{kicker_lead}</strong>{kicker_body}</p>
    <div class="products-grid">
{body}
    </div>
</section>
""", files


NEW_FAQS = [
    ("What is the Manors Greenskeeper line?",
     "It is the part of the range cut from groundskeeper workwear rather than golf "
     "clothing. The Recycled Greenskeeper Trouser ($174) uses 93% recycled nylon "
     "with a PFC-free water-resistant finish, an elasticated drawcord waist and "
     "eight pockets, and Manors calls its double front pleat a nod to on-course "
     "etiquette. The Lightweight Pleated Trouser ($174) runs the same shape in "
     "Primeflex&trade; with a scorecard-sized ticket pocket, and the Recycled "
     "Greenskeeper Shorts are $147."),
    ("What did Manors release in September 2026?",
     "An autumn/winter drop built almost entirely on performance fabric: a Merino "
     "Tech Hoodie at $301, a Ripstop Tech Vest and a Heritage Primaloft&reg; "
     "Cardigan at $214 each, a 1/4 Zip Primaloft&reg; Mid-Layer at $187, a Ripstop "
     "Tech Trouser at $201 and a Ranger Mockneck Polo at $127. Prices read from the "
     "brand&rsquo;s US storefront on 22 September 2026."),
    ("How much does Manors cost?",
     "The permanent range starts at $61 for the Manors Logo T-Shirt and the Retro "
     "Crown Cap, with the Course Polo at $87 and most polos between $114 and $127. "
     "Outerwear and mid-layers run $161 to $214. The September 2026 Merino Tech "
     "Hoodie at $301 is the most expensive piece in the current collection. All "
     "figures are US dollars, read from manorsgolf.com on 22 September 2026."),
]


def sub_once(h, old, new, why, every=False):
    """Converge from either the original or an earlier run of this script.

    every=True for any string that also lives inside the FAQPage JSON-LD. The
    FAQ copy exists twice on this page — once in the visible <details> and once
    in the schema block at the top — and replacing only the first leaves the
    structured data telling Google a price the page no longer shows.
    """
    if new in h and old not in h:
        return h
    if old not in h:
        sys.exit(f"! could not find {why}: {old[:60]!r}")
    return h.replace(old, new, -1 if every else 1)


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    original = h

    # strip a previous run, whitespace-symmetric so reruns do not drift indent
    h = re.sub(r"[ \t]*" + re.escape(MARK) + r".*?" + re.escape(END) + r"[ \t]*\n?",
               "", h, flags=re.S)
    base = h.count('class="product-card"')
    if base != 16:
        sys.exit(f"! expected 16 existing cards after strip, found {base}")

    # ---- 1. refresh the sixteen stale prices (prices only) ----
    fixed = []
    for m in re.finditer(
            r'product-name">([^<]*?)(\$[\d,]+)([^<]*?)</div>(.*?)'
            r'href="https://manorsgolf\.com/products/([^"]+)"', h, re.S):
        pre, old_p, post, mid, handle = m.groups()
        new_p = LIVE.get(handle)
        if new_p and new_p != old_p:
            h = h.replace(f'product-name">{pre}{old_p}{post}</div>',
                          f'product-name">{pre}{new_p}{post}</div>', 1)
            fixed.append((handle, old_p, new_p))

    # ---- 2. build the new blocks ----
    new_html, new_files = grid(
        NEW_DROP, "new-september", "New from the Collection &mdash; September 2026",
        "The September Drop &mdash; 6 Pieces",
        f"Autumn/Winter 2026 &middot; read {READ_DATE}",
        "Six pieces from the September drop, and every one of them makes the "
        "technical case the 2019 brand said it did not need. Merino, Primaloft, "
        "recycled TORAY ripstop. Prices are US dollars as the brand&rsquo;s US "
        f"storefront showed them on {READ_DATE}; all six were in stock that day.",
        base + 1, "September")
    core_html, core_files = grid(
        CORE, "core-collection", "The Core Collection",
        "The Permanent Range &mdash; 9 Pieces",
        f"Year-round &middot; read {READ_DATE}",
        "What stays on the rail when a drop sells through, from $61 to $214. "
        "Seawool&reg; polos, the Greenskeeper workwear line and the cap the logo "
        "came off.",
        base + 1 + len(NEW_DROP), "Core")

    block = (MARK + PQ_HACKERS + GREENSKEEPER + PQ_STREET + wild_grid()
             + new_html + core_html + END + "\n")

    anchor = '<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">The Collection'
    if anchor not in h:
        anchor = '<div class="drop-tag grass">The Collection &mdash;'
        if anchor not in h:
            sys.exit("! could not find the Collection tag to insert before")
        idx = h.index(anchor)
        idx = h.rfind("<section", 0, idx)
    else:
        idx = h.index(anchor)
    h = h[:idx] + block + h[idx:]

    # ---- 2b. the flair pull-quote, and the paragraph it is NOT duplicated in ----
    h = re.sub(r"[ \t]*" + re.escape(FLAIR_MARK) + r".*?" + re.escape(FLAIR_END)
               + r"[ \t]*\n?", "", h, flags=re.S)
    if PICTURES_ANCHOR not in h:
        sys.exit("! could not find the Pictures section to place the flair quote")
    h = h.replace(PICTURES_ANCHOR,
                  FLAIR_MARK + PQ_FLAIR + FLAIR_END + "\n" + PICTURES_ANCHOR, 1)
    h = sub_once(h, WTW_OLD, WTW_NEW, "the Who They Were hackers sentence")

    # ---- 3. counts, ranges, dates ----
    total = h.count('class="product-card"')
    h = sub_once(h, "The Collection &mdash; 16 Pieces",
                 f"The Collection &mdash; {TOTAL} Pieces", "the collection tag")
    h = sub_once(h, "<span>16 pieces &middot; $68&ndash;$284</span>",
                 f"<span>{TOTAL} pieces &middot; {LOW}&ndash;{HIGH}</span>",
                 "the header meta line")
    h = sub_once(h, '<span class="l">Range</span><span>$68&ndash;$284</span>',
                 f'<span class="l">Range</span><span>{LOW}&ndash;{HIGH}</span>',
                 "the sidebar range")
    h = sub_once(h, '<span class="l">Our pick</span><span>Reversible V-Neck Vest</span>',
                 '<span class="l">Our pick</span>'
                 '<span>Recycled Greenskeeper Trouser</span>', "the sidebar pick")
    h = sub_once(h, "The Outsider Polartec&reg; Polo at $115 is where you see it",
                 "The Outsider Polartec&reg; Polo at $114 is where you see it",
                 "the TGI Take polo price")
    h = sub_once(h, "Entry is $68; the collab racks run to $284.",
                 f"Entry is {LOW}; the collab racks run to $281.",
                 "the TGI Take range sentence")
    h = sub_once(h,
                 "Prices in the current range run about $48 for a course cap to "
                 "$284 for the Gentleman Jack merino crewneck.",
                 f"Prices in the current range run from {LOW} for the logo t-shirt "
                 f"to {HIGH} for the September Merino Tech Hoodie.",
                 "the FAQ price range", every=True)
    h = sub_once(h, '"dateModified": "2026-09-02"', '"dateModified": "2026-09-22"',
                 "the dateModified")
    h = sub_once(h, "<span>September 2, 2026</span>",
                 "<span>September 2, 2026 &middot; updated September 22, 2026</span>",
                 "the header date")

    # ---- 4. three more FAQs ----
    faq_new = "\n    ".join(
        f'<details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in NEW_FAQS)
    faq_mark = "<!-- TGI-MANORS-FAQ -->"
    h = re.sub(r"[ \t]*" + re.escape(faq_mark) + r".*?" + re.escape(faq_mark + "-END")
               + r"[ \t]*\n?", "", h, flags=re.S)
    close = h.rindex("</div>\n</section>", h.index('id="faq"'))
    h = (h[:close] + f"    {faq_mark}\n    {faq_new}\n    {faq_mark}-END\n  "
         + h[close:])

    print(f"  price refresh : {len(fixed)} of 16 cards")
    for hd, o, n in fixed:
        print(f"      {hd[:42]:<44}{o} -> {n}")
    print(f"  cards         : {base} -> {total}")
    print(f"  new sections  : Greenskeeper, In the Wild, "
          f"September ({len(NEW_DROP)}), Core ({len(CORE)})")
    print(f"  pull-quotes   : 5 (3 elevated: flair, hackers, street)")
    print(f"  FAQs          : {h.count('class=' + chr(34) + 'faq-q' + chr(34))}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return
    PAGE.write_text(h, encoding="utf-8")
    verify(original)


def verify(original):
    fin = PAGE.read_text(encoding="utf-8")
    bad = []

    if fin.count(MARK) != 1 or fin.count(END) != 1:
        bad.append(f"{fin.count(MARK)} blocks / {fin.count(END)} ends, expected 1 each")
    blk = fin[fin.index(MARK):fin.index(END)]

    # every new card present, linked and imaged
    for stem, name, price, handle, order, desc in NEW_DROP + CORE:
        if f"{name} &middot; {price}" not in blk:
            bad.append(f"{name}: card missing")
        if f"/products/{handle}" not in blk:
            bad.append(f"{name}: shop link wrong or missing")
        for k in order:
            rel = (f"images/manors/{stem}.jpg" if k == 0
                   else f"images/manors/{stem}-a{k+1}.jpg")
            if not (ROOT / rel).is_file():
                bad.append(f"{name}: {rel} not on disk")
            if "/" + rel not in blk:
                bad.append(f"{name}: {rel} not referenced")
    for stem, alt, cap in WILD:
        if not (ROOT / f"images/manors/{stem}.jpg").is_file():
            bad.append(f"{stem}.jpg not on disk")
        if f"/images/manors/{stem}.jpg" not in blk:
            bad.append(f"{stem}.jpg not referenced")

    # gallery controls complete, dots == frames. COUNT THE BUTTONS: the container
    # class "pg-dots" contains "pg-dot" as a substring and a naive count returns
    # frames+1 on a perfectly correct card.
    for dm, body in re.findall(
            r'data-frames="(\d+)"(.*?)</div><div class="product-body"', blk, re.S):
        if body.count("pg-frame") != int(dm):
            bad.append(f"card says {dm} frames, renders {body.count('pg-frame')}")
        dots = len(re.findall(r'<button class="pg-dot(?: on)?"', body))
        if dots != int(dm):
            bad.append(f"card has {dots} dot buttons for {dm} frames")
        for need in ("pg-arw prev", "pg-arw next", "pg-count"):
            if need not in body:
                bad.append(f"a new card is missing {need}")

    # NO PRICE ON THE PAGE MAY DISAGREE WITH THE LIVE READ
    allcards = re.findall(
        r'product-name">[^<]*?(\$[\d,]+)[^<]*?</div>.*?'
        r'href="https://manorsgolf\.com/products/([^"]+)"', fin, re.S)
    live_all = dict(LIVE)
    for stem, name, price, handle, order, desc in NEW_DROP + CORE:
        live_all[handle.replace("%C2%AE", "®")] = price
        live_all[handle] = price
    for p, hd in allcards:
        want = live_all.get(hd)
        if want and p != want:
            bad.append(f"{hd}: card says {p}, live read says {want}")
    if len(allcards) != TOTAL:
        bad.append(f"{len(allcards)} priced cards, expected {TOTAL}")

    # the three count/range statements must agree with the cards
    m = re.search(r"The Collection &mdash; (\d+) Pieces", fin)
    if not m or int(m.group(1)) != TOTAL:
        bad.append(f"collection tag says {m.group(1) if m else '?'}, page has {TOTAL}")
    prices = [int(p.lstrip("$").replace(",", "")) for p, _ in allcards]
    if f"{LOW}&ndash;{HIGH}" not in fin:
        bad.append("header/sidebar range not updated")
    if min(prices) != int(LOW.lstrip("$")) or max(prices) != int(HIGH.lstrip("$")):
        bad.append(f"stated range {LOW}-{HIGH} but cards span "
                   f"${min(prices)}-${max(prices)}")
    # Stale figures from the 2 September build. Matched as whole prices — a bare
    # "$115" in fin also matches inside "$1150" — and reported WITH THEIR CONTEXT,
    # because "an old price survived somewhere" sends you grepping the reverted
    # file, which is the original and of course still has them.
    for stale in ("$68", "$284", "$115", "$176", "$48", "$129", "$162",
                  "$190", "$216", "$243"):
        for m in re.finditer(re.escape(stale) + r"(?!\d)", fin):
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                             fin[max(0, m.start() - 70):m.end() + 40]))
            bad.append(f"stale price {stale} survived: ...{ctx.strip()}...")

    # the three elevated quotes must be verbatim on the page
    for frag in ("much flair on the tour anymore",
                 "hackers up and down the country",
                 "seen walking down the street in"):
        if frag not in fin:
            bad.append(f"quote fragment missing: {frag!r}")
    # FIVE PULL-QUOTES, EACH ATTRIBUTED, NONE DUPLICATED IN THE BODY.
    pqs = re.findall(r'<div class="pull-quote-inner">&ldquo;(.*?)&rdquo;'
                     r'<span class="pull-quote-attr">&mdash;\s*(.*?)</span>', fin, re.S)
    if len(pqs) != 5:
        bad.append(f"{len(pqs)} pull-quotes, expected 5")
    for text, attr in pqs:
        if not re.search(r"(Regan|Watts|Davies)", attr):
            bad.append(f"a pull-quote is not attributed to a named person: {attr[:40]}")
        if "Hypebeast" not in attr:
            bad.append(f"a pull-quote does not name its source: {attr[:40]}")
        # the words may appear ONCE on the page — inside their own pull-quote
        probe = text[:70]
        if fin.count(probe) != 1:
            bad.append(f"pull-quote text also appears in the body: {probe[:46]}...")
    if "In Their Words" in fin:
        bad.append("the In Their Words section survived; it should be dissolved")
    # the lifted quote must be gone from the Who They Were paragraph
    if "frustrates us because it" in fin:
        bad.append("the hackers quote is still in the Who They Were prose")
    # no two pull-quotes with only whitespace between them (the gate's rule)
    for m in re.finditer(r"</div>\s*</div>\s*(<div class=\"pull-quote\">)", fin):
        bad.append("two pull-quotes are stacked with no prose between them")

    # house rules
    body_text = re.sub(r"<[^>]+>", " ", fin)
    for w in re.finditer(r"\bworth\b", body_text, re.I):
        bad.append("the banned word 'worth' is on the page")
        break
    if "cdn.shopify.com" in fin or "cdn.sanity.io" in fin:
        bad.append("a hot-linked image survived — everything must be local")

    # NOTHING OUTSIDE THE BLOCK MAY HAVE MOVED except the prices and the meta
    for untouched in (
            "Manors Golf, Revisited &mdash; The Brand That Rejected Technical Golf",
            "The Collab Archive", "The Technical Turn", "What Survived the Rebrand",
            "What the Pictures Are Doing", "A Change of Course", "Who They Were",
            "personality before performance"):
        if untouched not in fin:
            bad.append(f"existing content lost: {untouched[:44]}")
    if "<title>Manors Golf — The Brand That Changed Its Mind</title>" not in fin:
        bad.append("the title changed — it should not have, it is the best CTR "
                   "on the site")

    words = len(body_text.split())
    if words < 1200:
        bad.append(f"{words} words, gate wants 1200")

    if bad:
        PAGE.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))

    print(f"\n  wrote {PAGE.name} — {TOTAL} cards, {words} words, "
          f"{fin.count('ig-grid')//2} editorial grids")
    print("\n  FLAGGED, NOT CHANGED:")
    print("    title and meta description left alone (1.9% CTR, best brand page)")
    print("    sidebar 'Our pick' moved to the Recycled Greenskeeper Trouser")
    print("    the Greenskeeper Trouser stays in 'The Technical Turn' rather than")
    print("    being duplicated into Core; the write-up carries it instead")


if __name__ == "__main__":
    main("--apply" in sys.argv)
