#!/usr/bin/env python3
"""The Drop Report — August into September 2026. VISUAL, BRAND BY BRAND.

WHY THIS SHAPE
--------------
First pass was a ten-card grid with three long prose sections. Lenny, 2026-09-14:
"less words and write up and more of a visual post of what the brands recently
dropped seperated by brands, also include the new Malbon drop."

So: rebuilt as eleven brand sections, each one a one-line kicker over a grid of
that brand's pieces. No essay sections. Every card's copy is two sentences at
most. The long sell-through and also-ran prose from v1 is gone, compressed into
a single short "Already Gone" list.

The no-repeat-brands rule does not bind here — this post is explicitly organised
BY brand, so multiple pieces per brand is the format rather than a violation.

MALBON / ARSHAM — added at Lenny's request, and it is real news. Malbon published
14 Arsham pieces on 2026-09-10 at 08:49 PST under the store tag `9.10.26 Arsham`,
four days before we published. There was NO press release, no Malbon journal post
and no trade coverage; the drop is only visible in the product feed. Our earlier
/drops/arsham-malbon-chapter-three covers the 6.16.26 drop, so this is the next
one. Eight of the fourteen are here, one colourway each.

DO NOT call it "Chapter Four" on the page. Malbon has never used chapter
numbering anywhere — not on the collection, not on a PDP, not in a release. Its
own taxonomy is date tags. The chapter framing is TGI's house convention (one
other outlet arrived at it independently) and attributing it to Malbon would be
wrong, so this post dates the drop instead.

HOW THE DATA WAS GATHERED
-------------------------
Every price and stock state comes from the brand's own Shopify product JSON
(`/products/<handle>.js` or a collection feed), captured 2026-09-14. Availability
is read from variant `available` flags, never page text. `published_at` is a
store record: it says when a product went live, not when it was made. Jones
published fifteen products in the window and created none of them, so its card
says published.

DELIBERATELY NOT ASSERTED (all checked, all unsupported):
  - "Chapter Four" (see above)
  - a partner name for Gamut x Otey — Otey Crisman is the obvious guess and
    nothing confirms it, so it is left out entirely
  - that PAYNTR's EMBER pieces sold out on launch day; zero stock hours after
    publishing reads as an inventory-sync artefact as easily as a real sellout
  - that Sugarloaf's Hidden Gems pieces are collaborations. Their copy says
    "made BY MacKenzie FOR SSC" — work-for-hire, not co-branding.
  - a licence for Apres's bear iconography or Seamus's Palmer umbrella beyond
    what each brand's own copy states
  - oxidized green as the Arsham 2026 palette. That description is sourced to
    Hypebeast's 2024 write-up of the KOHLER capsule; the 2026 naming (Stealth,
    Flint, Shards, Camo) points somewhere darker. Colour is described from the
    product records only.

DATE FORMAT: numeric M/D throughout the shipped copy, M/D/YY in the header
(Lenny, 2026-09-14: "change date formatting to Month/day"). Prose dates were
day-first before that; do not reintroduce "14 September". Bare month names with
no day ("the June drop", "since August") stay spelled out.

FAQ MARKUP: <details class="faq-q"><summary> — div markup fails verify-post.py
and makes apply-faq-style.py append a duplicate.
"""
import re, os, json

SLUG = "the-drop-report-september-2026"
TITLE = "The Drop Report &mdash; Everything That Landed, Brand by Brand"
PLAIN = "The Drop Report — Everything That Landed, Brand by Brand"
DESC = ("Every drop across independent golf from 8/1/26 to 9/14/26, "
        "brand by brand — Malbon's unannounced Arsham release, Sugarloaf with the "
        "First Tee, Mogshade with a London artist, Seamus on Arnold Palmer, and "
        "seven more. Prices and stock checked the day we published.")
IMG = "/images/sept-drops/"

M = json.load(open("research/sept-drops/manifest.json"))

# stem -> (display name, copy). Two sentences maximum. Prices and stock come
# from the manifest at build time and are never typed here.
COPY = {
 # ---------------- MALBON ----------------
 "malbon-shards": ("Shards Hoodie",
  "380 GSM fleece with the Stealth Camo print carried into the hood lining. One of six silhouettes that did not exist in the June drop."),
 "malbon-qzip": ("Stealth Quarter Zip",
  "The new mid-layer, in black or the olive camo. Sits above the carryover Monogram quarter zip at the same price."),
 "malbon-walkingbag": ("Monogram Walking Bag",
  "Nylon ripstop, just under six pounds, and the first bag Arsham and Malbon have made together that is not the &pound;-bracket Stealth cart bag."),
 "malbon-cloudburst": ("Cloudburst Rain Jacket &mdash; Dune",
  "20D nylon ripstop, tricot-backed, rated 20K. A new colourway of the June jacket rather than a new shell."),
 "malbon-pant": ("Stealth Pant",
  "Four-way stretch twill with a durable water finish, in black or olive camo. The trouser the collection was missing."),
 "malbon-glyphtee": ("Bermuda Glyph Tee",
  "Arsham's glyph work on a heavyweight tee, in dune or black. The cheapest way into the drop alongside the bucket hat."),
 "malbon-buckethat": ("Stealth Bucket Hat",
  "First bucket in the collaboration, in the Stealth Camo or plain black. XS is already the first size to move across the range."),
 "malbon-polo": ("Fairway Stealth Polo &mdash; Olive Camo",
  "The polo is the one piece that has consistently sold through &mdash; the white and black colourways from June are both gone, and this olive is the survivor."),
 # ---------------- SUGARLOAF ----------------
 "ssc-riya": ("Riya's Blade Putter Cover",
  "<em>&ldquo;Riya from the First Tee designed this blade cover, inspired by the beauty she finds on golf courses and some of her favorite colors.&rdquo;</em>"),
 "ssc-aadya": ("Aadya's High Crown Visor",
  "The only piece in the capsule that is not a headcover, and the cheapest way in."),
 "ssc-tiago": ("Tiago's Driver Headcover",
  "One of two driver covers, designed by different kids rather than being colourways of each other."),
 "ssc-julien": ("Julien's Driver Headcover",
  "Julien's cover represents his Metro New York chapter of the First Tee."),
 "ssc-camille": ("Camille's Mallet Headcover",
  "Inspired, per Sugarloaf, by her favourite club sandwich &mdash; the detail an adult design team would have edited out."),
 # ---------------- MOGSHADE ----------------
 "mogshade-onlyhuman": ("Only Human 2.0 Headcover",
  "British artist David Shillinglaw with Eritage, a Lisbon art space. Fifteen made, from <em>&ldquo;rescued high-quality fabrics woven at factories in the mountain region of Serra da Estrela&rdquo;</em> &mdash; and gone in five days."),
 "mogshade-highsun": ("High Sun Headcover",
  "Merino hand-woven by Fabricaal on manual wooden looms, in what Mogshade calls <em>&ldquo;one of only three original secular wool handicrafts to still exist in Europe.&rdquo;</em> The sister colourway lasted four days."),
 # ---------------- THE REST, ONE EACH ----------------
 "seamus-palmer": ("Arnold Palmer Yellow Umbrella Driver",
  "A licensed Palmer run that landed 9/9: Citrus Brisa leather under all-over signature umbrella embroidery, handcrafted in Oregon. Six pieces cover the bag, and personalisation is switched off across the whole line."),
 "gamut-lonewolf": ("Lone Wolf Headcover",
  "Black suede over waxed slate canvas, plush black sherpa inside, classic barrel. Three drops in six weeks from a very small shop, and three of the five pieces sold out &mdash; the hand-dyed Shibori cover went in under a week."),
 "payntr-vessel": ("VESSEL &times; PAYNTR SL Limited Edition",
  "Nine of ten sizes already gone. CLARINO Trivela upper, full-grain leather overlays, WATERPROOF+ membrane, CARBITEX GearFlex plate &mdash; one of five collaboration shoes PAYNTR ran in six weeks, four of which are now gone or down to a single size."),
 "eastside-standbag": ("Eastside Golf Stand Bag",
  "Built in house and out on 8/7 &mdash; in Eastside's own words <em>&ldquo;Eastside Golf's first vertically produced Stand Bag&rdquo;</em>, with four pockets, a hood, a magnetic pocket and a four-point strap."),
 "siegelman-bazooka": ("Siegelman Stable &times; Bazooka Hat",
  "Two-tone five-panel with a working pocket sized for a pack of Bazooka. August also brought Siegelman a fourteen-piece Yankees and New Era capsule, but this is the one with a sense of humour."),
 "students-medinah": ("Medinah Crew Knit Sweater",
  "One hundred per cent merino, from Course Studies Fall 2026. Students shipped roughly seventy styles across two overlapping autumn programmes in three weeks; this is the one to own."),
 "apres-pencils": ("Apr&egrave;s-Golf Pencils Bucket Hat",
  "Navy nylon with a pencils graphic across the crown where, per Apr&egrave;s, <em>&ldquo;The text on each pencil represents several different logos we've used over the years.&rdquo;</em> Made with Angus and Grace Go Golfing."),
 "jones-utilityx": ("Utility X &mdash; Pageant Blue",
  "Jones published fifteen products in six weeks and created none of them. This is the one that matters: the 2026 Utility X finally going live."),
}

# (brand, kicker, [stems]) — section order is drop recency, newest first.
SECTIONS = [
 ("Malbon Golf", "Fourteen Arsham pieces went up on 9/10 with no announcement of any kind. Eight of them here.",
  ["malbon-shards", "malbon-qzip", "malbon-walkingbag", "malbon-cloudburst",
   "malbon-pant", "malbon-glyphtee", "malbon-buckethat", "malbon-polo"]),
 ("Sugarloaf Social Club", "Five covers designed by named junior golfers, published 9/13, with all proceeds going to the First Tee.",
  ["ssc-tiago", "ssc-riya", "ssc-camille", "ssc-julien", "ssc-aadya"]),
 ("Mogshade", "Two headcovers arrived from Mogshade with two very different partners: a London artist and a Portuguese hand-weaving workshop.",
  ["mogshade-onlyhuman", "mogshade-highsun"]),
 ("Eight More Brands", "Each of these shipped a single piece in the window. Newest first.",
  ["seamus-palmer", "gamut-lonewolf", "students-medinah", "payntr-vessel",
   "siegelman-bazooka", "eastside-standbag", "apres-pencils", "jones-utilityx"]),
]

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Twenty-six brands went under the lamp for the six weeks to 9/14, read from their own product records rather than from press releases &mdash; which is how Malbon's fourteen unannounced Arsham pieces turned up. Eleven brands had something new. Here it is, brand by brand, priced and stock-checked on the day.</p>
  </div>
</div>
"""

GONE = """<section class="products">
  <h2 class="products-hdr">Already Gone</h2>
  <p class="cat-kicker">Everything below sold out before we could publish it.</p>
  <div class="writeup-body">
    <ul>
      <li><strong>Mogshade</strong> &mdash; every piece with a partner credit: Only Human 2.0 (fifteen made, five days), Fabricaal Verdant, both Draw Golf caps, the four hand-painted KIKO CLJ covers, the Depeche Magazine bundle.</li>
      <li><strong>Sugarloaf</strong> &mdash; a $3,000 numbered set of Boyd Blade &amp; Ferrule irons hand-ground by Don White, plus the $850 MacKenzie bag and both headcover runs from Hidden Gems.</li>
      <li><strong>Students &times; PAYNTR</strong> &mdash; both colourways of the $240 SL, eight sizes each, one pair per customer.</li>
      <li><strong>Jones</strong> &mdash; the Players Series relaunched on 8/25 in three colourways and sold out in all three.</li>
      <li><strong>Gamut</strong> &mdash; the Shibori cover, hand-dyed in house and one-of-one by construction, lasted six days.</li>
      <li><strong>Swag</strong> &mdash; nine of twenty-five Cubs pieces in under four weeks, including a $777.77 Wrigleyville putter.</li>
    </ul>
  </div>
</section>
"""

QUIET = """<section class="products">
  <h2 class="products-hdr">And Four That Went Quiet</h2>
  <p class="cat-kicker">The absences a new-arrivals feed will never show you.</p>
  <div class="writeup-body">
    <p><strong>Kingfisher Golf</strong> has password-gated its entire storefront and paused orders while it moves warehouses. <strong>Radry</strong> has published nothing since 3/8, <strong>Casualist</strong> nothing since 3/31, and <strong>Odd Ritual</strong> nothing since a ten-piece drop on 7/15. <strong>Fella Golf</strong>'s newest product is from 7/29. None of that is failure &mdash; small brands release when they have something &mdash; but it is half the picture, and nobody posts it.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("When did the new Malbon x Arsham pieces drop?",
  "Malbon published fourteen Arsham products on 9/10/26 at 8:49am PST, tagged internally by date. There was no press release, no post on Malbon's journal and no trade coverage &mdash; the drop is visible only in the store's own product feed. The previous Arsham release was 6/16."),
 ("Is the Malbon drop a new chapter of the Arsham collaboration?",
  "Malbon has never used chapter numbering anywhere on its site &mdash; not on the collection page, not on a product page, not in a release. It files releases by date code. We date this one rather than number it."),
 ("How was this roundup assembled?",
  "We resolved the brands TheGrassyIssue links to most often to their own storefronts and read each product feed directly, sorting by publish date and keeping what went live between 8/1/26 and 9/14/26. Prices come from the product records; stock comes from variant availability flags rather than what a page says."),
 ("What is the difference between a drop and a restock here?",
  "A publish date says when something went live, not when it was made. Several brands republished stock created in 2024 or 2025 &mdash; Jones published fifteen products in the window and created none of them. Where a piece was built earlier and held back, the card says published."),
 ("Which of these is most likely to go next?",
  "The VESSEL &times; PAYNTR SL is down to one size in ten, so functionally it already has. After that, Mogshade's High Sun: its sister colourway went in four days and the brand has cleared every partner-credited piece it has released since August."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""


def frames(s):
    n = 1
    while os.path.exists(f"images/sept-drops/{s}-a{n+1}.jpg"):
        n += 1
    return n


def gal(s, name):
    n = frames(s)
    pl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name)).strip()
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}.jpg" alt="{pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}{"" if i==0 else f"-a{i+1}"}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def price_tag(r):
    p = str(r["price"]).replace(" USD", "").strip()
    a = r["availability"]
    if a == "sold out":
        return f"{p} &middot; sold out"
    if a.startswith("partial"):
        return f"{p} &middot; almost gone"
    return p


def _ent(t):
    """Accented brand names -> HTML entities (Après Golf)."""
    return (t.replace("è", "&egrave;").replace("é", "&eacute;")
             .replace("ö", "&ouml;").replace("&", "&amp;").replace("&amp;egrave;", "&egrave;")
             .replace("&amp;eacute;", "&eacute;").replace("&amp;ouml;", "&ouml;"))


def card(s):
    """Brand on the card ALWAYS comes from the manifest, never from the section
    heading. When the eight single-piece brands were merged into one section,
    passing the heading down made all eight boxes read 'One Each From Eight
    More' — Lenny caught it. The heading names the section; the box names the
    brand that made the thing."""
    r = M[s]
    brand = _ent(r["brand"])
    name, desc = COPY[s]
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, name)}
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name} &middot; {price_tag(r)}</div>
        <div class="product-desc">{desc}</div>
        <a href="{r['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""


def sec(brand, kicker, slugs):
    c = "\n    ".join(card(s) for s in slugs)
    return (f'<section class="products">\n  <h2 class="products-hdr">{brand}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&ndash;", "–").replace("&times;", "×")
            .replace("&egrave;", "è").replace("&pound;", "£"))


SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": PLAIN,
    "description": DESC,
    "numberOfItems": sum(len(sc[2]) for sc in SECTIONS),
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "name": st(f"{M[stem]['brand']} {COPY[stem][0]}"),
         "url": M[stem]["url"]}
        for i, stem in enumerate(stem for sc in SECTIONS for stem in sc[2])
    ],
}

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
              lambda m: m.group(1) + f"https://thegrassyissue.com{IMG}malbon-shards.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

n_products = sum(len(s[2]) for s in SECTIONS)
# Brands covered, not sections — the eight singles share one section.
N_BRANDS = len({M[st]['brand'] for sc in SECTIONS for st in sc[2]})
_headings = {sc[0] for sc in SECTIONS}
_cardbrands = {M[st]['brand'] for sc in SECTIONS for st in sc[2]}
if _cardbrands & {h for h in _headings if h not in _cardbrands} or 'Eight More Brands' in _cardbrands:
    raise SystemExit('a card is using a section heading as its brand name')
if N_BRANDS != 11:
    raise SystemExit(f'expected 11 brands across the post, counted {N_BRANDS}')
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  The Drop Report</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>9/14/26</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{N_BRANDS} Brands &middot; {n_products} Pieces</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}malbon-shards.jpg" '
        'alt="The Arsham Shards Hoodie in olive Stealth Camo, from the Malbon drop of 9/10 2026" /></div></div>\n'
        + INTRO
        + "".join(sec(*s) for s in SECTIONS)
        + GONE + QUIET)

# ---- guards -------------------------------------------------------------
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(COPY):
    raise SystemExit(f"section/COPY mismatch: unplaced={set(COPY)-set(placed)} "
                     f"extra={set(placed)-set(COPY)}")
nomanifest = [s for s in placed if s not in M]
if nomanifest:
    raise SystemExit(f"placed but not in manifest: {nomanifest}")
gone_imgs = [s for s in placed if not os.path.exists(f"images/sept-drops/{s}.jpg")]
if gone_imgs:
    raise SystemExit(f"images missing on disk: {gone_imgs}")
if len(placed) != len(set(placed)):
    raise SystemExit("a stem is placed twice")
if 'faq-q' in body or 'FAQPage' in json.dumps(SCHEMA):
    raise SystemExit('FAQ removed from this post (Lenny, 9/14) — schema and markup must both stay out')
_body_txt = re.sub(r'<[^>]+>', ' ', body)
if re.search(r'\bworth\b', _body_txt, re.I):
    raise SystemExit("BANNED WORD 'worth' appears in the body copy")
if re.search(r'chapter\s*(four|4)', _body_txt, re.I):
    raise SystemExit("do NOT call the Malbon drop Chapter Four — Malbon uses no chapter numbering")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(SECTIONS)} brand sections | {n_products} pieces | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
