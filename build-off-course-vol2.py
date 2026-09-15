#!/usr/bin/env python3
"""Off Course, Vol. 2 — golf brands doing non-golf things.

WHY THIS POST EXISTS
--------------------
Vol 1 (/drops/off-course-golf-brands-doing-non-golf-things, published 7/8/26)
was 18 cards and 1,381 words. Lenny, 2026-09-15: "LET'S do a volume 2", then
"let's get it up to 24 total".

THE BRIEF, STATED PRECISELY: a thing made and sold BY a golf brand that is NOT
a golf product. Apparel does not count — a golf brand making a t-shirt is still
golf apparel. Golf-shaped novelty counts as long as the OBJECT is non-golf: a
golf-ball-print air freshener is an air freshener; a divot tool is not.

REPEAT BRANDS ARE PERMITTED HERE. Gumtree (Vol 1: coffee) and Whim (Vol 1: the
Reebok collab) come back with completely different objects. Lenny, 2026-09-15:
"okay to repeat brands in this post if it really is a good fit." The standing
no-repeat rule governs repeats WITHIN one roundup, and nothing repeats here —
24 objects, 24 distinct brands.

WHAT WAS CUT, AND WHY — the dropship test
-----------------------------------------
A golf brand RESELLING somebody else's object is not a golf brand MAKING a
non-golf thing, so anything carrying a `Shopify Collective` tag or a
third-party vendor with no design involvement was disqualified:
  - William Murray 6-can cooler $109.99 — vendor "SHITI Coolers", Collective
    tagged. It was on the shortlist from the 8/30 research and failed on review.
  - Trap Golf x VYCE crystal tumblers — vendor "VYCE Drinkware", Collective.
  - RADMOR x Craft Design Technology — Gifu-forged scissors, Pentel pens. The
    most on-theme thing anyone found and it hurt to cut, but every SKU is
    vendor "Craft Design Technology" and tagged 3RD PARTY.
Co-branded collabs where the golf brand clearly drove the design DO qualify and
are labelled as collabs on the card: RGC x Weatherman, Swag x YETI, SSC x Crazy
Creek, Sand Valley x Ecudane, JBL x Cabot, Gumtree x Almond.

LENNY'S CUTS, 2026-09-15, after seeing the first build:
  - the Dormie faux-croc belt. Cut, not replaced in Packed.
  - the whole "Four That Didn't Make It" section, which listed the four items
    that sold out or were delisted between research and build. Do not bring it
    back; there is a guard for it below.
  - the Swag x YETI lunch box. He asked for a home good instead, so the Bar
    Cart slot went to the Bandon Dunes rock glass and a ninth object went into
    At Home: the Fried Egg Cypress Point poster. Both are variant-confirmed and
    both are own-vendor-adjacent (see the resort note below).
  - the Pins & Aces LiquorStick was the obvious barware candidate and was
    rejected on its own copy: "fits seamlessly in ANY golf bag", "Discreetly
    slides into EVERY golf bag." A thing the brand sells as golf-bag kit is a
    golf accessory, whatever shape it is.

RESORT FABRICATOR VENDORS. Bandon's rock glass lists vendor "Sterling Glass",
the glassmaker, exactly as Sand Valley's blanket lists "Ecudane" and Cabot's
speaker lists "JBL". That is how pro-shop POS is structured and is NOT the same
as a Shopify Collective dropship. The test is whether the golf brand drove the
design; on all three it did, and all three are written as collaborations.

DIED BETWEEN RESEARCH (8/30) AND BUILD (9/15) — do not re-add without checking:
  - Malbon x JBL Clip 5 $88 — sold out. Replaced in this post by JBL x Cabot,
    which is the same speaker family at a different property.
  - johnnie-O waterproof playing cards $40 — no longer a priced SKU, now a
    gift-with-purchase only.
  - Jones "Out of Office" backpack $65 — delisted, 404s on every known handle.
  - MANORS matches £5 — still sold out, and their only non-apparel SKU, so
    there was no substitute to take the slot.

DELIBERATELY NOT ASSERTED (all checked, all unsupported):
  - that the Sunday duffel is a "Sunday x Golf Projects" collab. The product is
    tagged `collabs` and one alt-text string says so, but no published copy
    does, so the card describes the bag and leaves the partner out.
  - a piece count for the Pinehurst puzzle beyond what the box itself prints
    (504). The PDP has no body copy at all.
  - any manufacturing or edition claim for the Metalwood ashtray. Its store is
    a headless Plasmic build with no variant JSON; price and stock come from
    the rendered page, and that is the limit of what is known.
  - that Foray's planter is rare or collectible. It is dated 1962 and sold as a
    one-of-one; that is the whole of the claim.

STOCK: every price and availability state was read on 9/15/26 from the brand's
own product record — variant `available` flags, never page text. Two exceptions
are noted in the manifest and flagged on the page: Scotty Cameron (not used)
and Metalwood/TGJ, which are not Shopify.

BETTINARDI IMAGE TRAP: their CDN filenames are SWAPPED against the variant
names. `...Silver-Update.png` is the BLACK frame and `...Black-Update.png` is
the SILVER. Black is sold out; Silver is what we link. The files on disk were
swapped after a visual check — bettinardi-plate.jpg IS the silver. Do not
"fix" this by trusting the filenames.

DATE FORMAT: numeric M/D, M/D/YY in the header. House rule since 9/14.

FAQ MARKUP: <details class="faq-q"><summary> — div markup fails verify-post.py
and makes apply-faq-style.py append a duplicate.
"""
import re, os, json

SLUG = "off-course-vol-2-golf-brands-doing-non-golf-things"
TITLE = "Off Course, Vol. 2 &mdash; Golf Brands Doing Non-Golf Things"
PLAIN = "Off Course, Vol. 2 — Golf Brands Doing Non-Golf Things"
DESC = ("Twenty-four things made by golf brands that have nothing to do with golf — "
        "a $1,950 surfboard, a 1962 ceramic planter, a hand-woven wool poster, a bourbon, "
        "an $8 coaster. Twenty-four brands, no repeats, every price and stock state "
        "checked on 9/15/26.")
IMG = "/images/off-course-vol2/"
VOL1 = "/drops/off-course-golf-brands-doing-non-golf-things"

M = json.load(open("research/off-course-vol2/manifest.json"))

# stem -> (display name, copy). Two or three sentences. Prices come from the
# manifest at build time and are never typed here.
COPY = {
 # ------------------------------- AT HOME -------------------------------
 "mogshade-poster": ("Eighteen Wool Poster",
  "Mogshade weaves these to order in one hundred per cent wool on an eight-week lead time, from a series it calls Loomed Rounds. Made with Soft Hands Club in two colourways, Blue and Earth."),
 "sandvalley-blanket": ("Ecudane Clubhouse Blanket",
  "A cashmere-blend throw woven with an illustration of the Sand Valley clubhouse &mdash; a drawing rather than a logo, which is the whole difference. Made by Ecudane and published 9/3, so it is about two weeks old."),
 "whim-cupola": ("La Cupola Paperweight",
  "Seven and a half pounds of hand-poured concrete and gypsum, five inches across, leather on the bottom, with a removable concrete flag set into a coffered dome. A scale model of the installation Whim built for Milan Design Week &mdash; <strong>edition of ten</strong>."),
 "foray-planter": ("Vintage Sports Book Planter",
  "A ceramic planter made in Japan in 1962, shaped as a stack of four books spined Fishing, Hunting, Bowling and Golf. Foray is not manufacturing these; it is sourcing actual dated antiques and selling them one at a time, which almost nobody in this business does."),
 "tgj-quietplease": ("Quiet, Please",
  "Eleven by fourteen inches, 250 pages, Smyth-sewn and case-bound on gallery paper with inline spot gloss, in a clamshell case. Writing by Tom Coyne, photographs by Kohjiro Kinno and Christian Hafer."),
 "metalwood-ashtray": ("Putting Trainer Ceramic Ashtray",
  "Red glazed ceramic, shaped like a putting trainer, printed with <em>&ldquo;Put your butts in it / Put your balls in it / I don&rsquo;t care.&rdquo;</em> The joke and the object are the same length."),
 "pinehurst-puzzle": ("Carolina Hotel 504-Piece Puzzle",
  "Sixteen by twenty inches, 504 pieces, reproducing an illustration of the Carolina Hotel. The listing carries no description whatsoever &mdash; the piece count is printed on the box and nowhere else."),
 "pxg-coaster": ("Darkness Coaster",
  "A five-inch silicone coaster carrying the Darkness skull. The 26 is the 26th Marine Regiment, which Bob Parsons served in at Khe Sanh &mdash; a great deal of weight for eight dollars."),
 "friedegg-cypress": ("Cypress Point Closing Holes Poster",
  "An illustrated overhead of Cypress Point&rsquo;s closing stretch by William Eagar, on matte 200gsm stock shipped rolled in an archival sleeve, with framed and photo-paper configurations running to $587. Cypress Point permits no drones and no press, so a drawing is the only way this view exists as an object at all."),
 # ------------------------------ THE BAR CART ----------------------------
 "sweetens-bourbon": ("5 Year Aged Tennessee Bourbon",
  "Seven hundred and fifty millilitres at 93.7 proof, the flagship of a spirits company named after a nine-hole course in South Pittsburg, Tennessee. Backed by Peyton Manning and Andy Roddick, with blends built historically by Marianne Eaves."),
 "bandon-rockglass": ("Single Rock Glass",
  "Twelve ounces of handblown crystal with a golf-ball dimple pressed into the base, etched with one of seven course marks. The dimple is an impression in the glass rather than a print, so it only shows itself once you have finished the drink."),
 "stitch-winetote": ("Insulated Wine Tote",
  "Eight and a half by sixteen and a half inches, structured sides and base, neoprene-lined for two 750ml bottles in Stitch&rsquo;s water- and stain-resistant Touring fabric. Five colourways; Steel Skies is down to five units."),
 "golfgods-koozie": ("Metal Insulated Koozie",
  "Double-walled stainless, sized for a can or a bottle, at twenty Australian dollars. The cheapest object on this list after the coaster and arguably the most used."),
 # ------------------------------ IN THE CAR ------------------------------
 "bettinardi-plate": ("Milled License Plate Holder",
  "Cut from a single block of 6061 aluminium and anodised, carrying the same honeycomb face-milling pattern as the putters, on the same CNC machines in Tinley Park. <strong>Silver only</strong> &mdash; the black is gone &mdash; and it ships without screws."),
 "birds-freshener": ("Neverfind Air Freshener",
  "Seven by ten centimetres of citrus-scented card printed with a ball on a tee and the line <em>&ldquo;So fresh off the greens.&rdquo;</em> Three other designs exist at the same price."),
 # --------------------------- OUT OF THE HOUSE ---------------------------
 "gumtree-almond": ("Nature Club Single Fin Surfboard",
  "Two boards, both handmade in California by Almond in opaque resin: a 7&prime;6&Prime; mid-length with a pintail and slight vee, and a 6&prime;6&Prime; on a narrower outline with a round tail and side-bites. Based on a model from founder Karsten&rsquo;s own quiver, one of each colour, two of each left."),
 "ssc-crazycreek": ("Hidden Gem Crazy Creek Chair",
  "A packable ground-level camp chair, 16.5 inches at the seat, 23 to 25 ounces, rated to 250 pounds, in Sugarloaf&rsquo;s Hidden Gem colourway. Crazy Creek has been making these in Montana since 1987."),
 "cabot-jbl": ("Clip 4 Waterproof Speaker",
  "A JBL Clip 4 &mdash; five watts, ten-hour battery, waterproof and dustproof, carabiner built into the body &mdash; wearing the Saint Lucia turtle rather than the corporate Cabot wordmark. Property-specific merch with actual restraint."),
 "rgc-umbrella": ("Collapsible Umbrella &mdash; Royal Snowball",
  "An auto-open Weatherman umbrella on fibreglass ribs, carrying Random Golf Club&rsquo;s Royal Snowball crest. The one item here you will use most often nowhere near a golf course."),
 "rhoback-bandana": ("Performance Dog Bandanas",
  "Four-way-stretch moisture-wicking neckerchiefs printed to match Rhoback&rsquo;s polos, which is an unusually committed piece of family dressing. <strong>Thirty-two patterns</strong> currently up, two of them marked down."),
 # -------------------------------- PACKED --------------------------------
 "vessel-garment": ("Signature Garment Duffel",
  "A duffel that unzips flat into a garment bag with a hanger hook, rated for up to three suits, in five colourways. Solves the problem of a wedding and a tee time in the same weekend."),
 "sunday-camera": ("Camera Utility Duffel",
  "Nine by seventeen by thirteen inches, 5.5 pounds, weather-resistant matte polyester, with a modular camera divider, a fleece-lined laptop sleeve, a removable wipeable shoe cube, MOLLE loops and a luggage pass-through. A camera bag first."),
 "travismathew-offdaze": ("Offdaze Sunglasses",
  "Italian-made acetate on a custom multi-step hinge, with polarised, anti-smudge, fully coated lenses, cut smaller than the Sundaze. Currently marked down from $224.95, which will not last."),
 "nlu-pouch": ("Twill Stash Pouch",
  "Twill and leather, flat enough for a back pocket, holding roughly twenty pouches with a utility pocket behind. Made for No Laying Up by Spyhold, in navy or green."),
}

# (heading, kicker, [stems])
SECTIONS = [
 ("At Home",
  "Nine objects that end up in a living room, and only one of them has a golf ball on it.",
  ["mogshade-poster", "sandvalley-blanket", "whim-cupola", "foray-planter",
   "tgj-quietplease", "friedegg-cypress", "metalwood-ashtray", "pinehurst-puzzle",
   "pxg-coaster"]),
 ("The Bar Cart",
  "This is the drinking end of the category, and it runs in descending order of ceremony.",
  ["sweetens-bourbon", "bandon-rockglass", "stitch-winetote", "golfgods-koozie"]),
 ("In the Car",
  "Two brands here make something for the drive rather than the round.",
  ["bettinardi-plate", "birds-freshener"]),
 ("Out of the House",
  "Here the brief gets interesting. One of these is a surfboard and one of them is for a dog.",
  ["gumtree-almond", "ssc-crazycreek", "cabot-jbl", "rgc-umbrella", "rhoback-bandana"]),
 ("Packed",
  "Four things that go in a bag, or are the bag.",
  ["vessel-garment", "sunday-camera", "travismathew-offdaze", "nlu-pouch"]),
]

INTRO = f"""<div class="writeup">
  <div class="writeup-body">
    <p>The first <a href="{VOL1}">Off Course</a> ran in July with eighteen things &mdash; coffee, candles, a cologne, a children&rsquo;s book. This one is twenty-four, from twenty-four different brands, and the range has widened considerably. There is a $1,950 surfboard shaped in California, a ceramic planter made in Japan in 1962, a 250-page clothbound book in a clamshell case, and an $8 coaster.</p>
    <p>One rule governs the list. The thing has to be made and sold by a golf brand, and it has to not be a golf product. Apparel is out, because a golf brand making a t-shirt is still a golf brand making apparel. Reselling is also out: three strong candidates were cut on review because the golf brand&rsquo;s name was on the listing and somebody else&rsquo;s was in the vendor field. Co-branded collaborations stay in and are labelled as such.</p>
    <p>Prices and stock were read from each brand&rsquo;s own product record on 9/15.</p>
  </div>
</div>
"""

FAQ_ITEMS = [
 ("What counts as a golf brand doing a non-golf thing?",
  "The object has to be made and sold by a golf brand and has to not be a golf product. Apparel does not count &mdash; a polo company making a t-shirt is still making apparel. Golf-shaped novelty does count as long as the object underneath is genuinely something else: an air freshener printed with a golf ball is an air freshener, while a divot tool shaped like anything at all is a divot tool."),
 ("Why were some products cut?",
  "Three items were dropped because the golf brand was reselling rather than making. If a product carries a Shopify Collective tag or a third-party vendor with no evidence of design involvement, it is a storefront listing rather than something the brand made. A co-branded collaboration where the golf brand clearly drove the design is a different thing, and those are in and labelled."),
 ("Are the prices and stock current?",
  "Every price and availability state here was read on 9/15/26 from the brand&rsquo;s own product record, using variant availability flags rather than what a page says. Two of the twenty-four do not run on Shopify and expose no variant data, so their stock comes from the rendered page: the Metalwood ashtray and The Golfer&rsquo;s Journal book."),
 ("Which of these will go first?",
  "The Whim paperweight is an edition of ten, both Gumtree surfboards show two remaining, and Stitch&rsquo;s Steel Skies wine tote is down to five. The Bettinardi plate holder is already half gone &mdash; the black sold out and only silver remains."),
 ("Does this repeat Volume One?",
  f"Two brands appear in both volumes with entirely different objects: Gumtree, which was coffee in July and is a surfboard here, and Whim, which was the Reebok collaboration and is now a concrete paperweight. No product repeats, and no brand appears twice within this list. <a href=\"{VOL1}\">Volume One is here</a>."),
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
    while os.path.exists(f"images/off-course-vol2/{s}-a{n+1}.jpg"):
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
    p = str(r["price"]).strip()
    a = r["availability"]
    if a == "sold out":
        return f"{p} &middot; sold out"
    if a.startswith("partial"):
        return f"{p} &middot; almost gone"
    return p


def _ent(t):
    return (t.replace("×", "&times;").replace("é", "&eacute;").replace("è", "&egrave;")
             .replace("’", "&rsquo;").replace("&", "&amp;").replace("&amp;times;", "&times;")
             .replace("&amp;eacute;", "&eacute;").replace("&amp;egrave;", "&egrave;")
             .replace("&amp;rsquo;", "&rsquo;"))


def card(s):
    """Brand ALWAYS comes from the manifest, never from the section heading —
    the section says where the object lives, the box says who made it."""
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


def sec(head, kicker, slugs):
    c = "\n    ".join(card(s) for s in slugs)
    return (f'<section class="products">\n  <h2 class="products-hdr">{head}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&ndash;", "–").replace("&times;", "×")
            .replace("&egrave;", "è").replace("&eacute;", "é").replace("&pound;", "£")
            .replace("&prime;", "'").replace("&Prime;", '"'))


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
              lambda m: m.group(1) + f"https://thegrassyissue.com{IMG}gumtree-almond.jpg" + m.group(2), head)
# ---- MIRROR og: -> twitter: --------------------------------------------------
# Every build script in this repo copies a model page's <head> and rewrites the
# og: tags. None of them ever rewrote the twitter: tags, so those rode along
# from the model — and on 2026-09-15 eleven live posts were found sharing on X
# under "Students Golf Summer 2026 — Summer School Is in Session". The page
# renders fine; it only shows when something reads the card. Never rewrite og:
# without rewriting twitter: alongside it.
for _k, _v in [("twitter:title", PLAIN), ("twitter:description", DESC)]:
    head = re.sub(rf'(<meta name="{_k}" content=")[^"]*(")',
                  lambda m, v=_v: m.group(1) + v + m.group(2), head)
_twt = re.search(r'<meta name="twitter:title" content="([^"]*)"', head)
if _twt and _twt.group(1) != PLAIN:
    raise SystemExit("twitter:title did not take — the share card would carry "
                     "another post's headline")
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

N = sum(len(s[2]) for s in SECTIONS)
N_BRANDS = len({M[s]["brand"] for sc in SECTIONS for s in sc[2]})

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Off Course, Vol. 2</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>9/15/26</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{N_BRANDS} Brands &middot; {N} Things</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}gumtree-almond.jpg" '
        'alt="A surfboard from Gumtree Golf and Nature Club, shaped by Almond in California" /></div></div>\n'
        + INTRO
        + "".join(sec(*s) for s in SECTIONS)
        + FAQ)

# ---- guards -------------------------------------------------------------
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(COPY):
    raise SystemExit(f"section/COPY mismatch: unplaced={set(COPY)-set(placed)} "
                     f"extra={set(placed)-set(COPY)}")
if len(placed) != len(set(placed)):
    raise SystemExit("a stem is placed twice")
if N != 24:
    raise SystemExit(f"Lenny asked for 24; this build has {N}")
if N_BRANDS != 24:
    raise SystemExit(f"24 things must come from 24 distinct brands; counted {N_BRANDS} — "
                     "no brand repeats WITHIN a roundup, even though repeats across "
                     "volumes are fine (Lenny, 9/15)")
nomanifest = [s for s in placed if s not in M]
if nomanifest:
    raise SystemExit(f"placed but not in manifest: {nomanifest}")
gone_imgs = [s for s in placed if not os.path.exists(f"images/off-course-vol2/{s}.jpg")]
if gone_imgs:
    raise SystemExit(f"images missing on disk: {gone_imgs}")
_txt = re.sub(r'<[^>]+>', ' ', body)
if re.search(r'\bworth\b', _txt, re.I):
    raise SystemExit("BANNED WORD 'worth' appears in the body copy")
# the three cut items must never reappear as products
for banned, why in [("SHITI", "dropship cooler"), ("VYCE", "Collective-tagged barware"),
                    ("Craft Design Technology", "3rd-party stationery"),
                    ("LiquorStick", "its own copy sells it as golf-bag kit")]:
    if banned.lower() in _txt.lower():
        raise SystemExit(f"{banned} ({why}) does not belong in this post")
# Lenny cut these on 2026-09-15 — see the docstring
if "Didn" in _txt and "Make It" in _txt:
    raise SystemExit("the 'Four That Didn't Make It' section is back; Lenny cut it on 9/15")
for cut in ["dormie-belt", "swag-yeti"]:
    if cut in str(SECTIONS) or cut in COPY:
        raise SystemExit(f"{cut} was cut by Lenny on 9/15 and must stay out")
# apparel is out of scope — catch a drift back into it
for bad in ["polo shirt", "the t-shirt", "our hoodie"]:
    if bad in _txt.lower():
        raise SystemExit(f"'{bad}' — apparel does not qualify for this post")
if 'FAQPage' not in json.dumps(SCHEMA) and '<details class="faq-q">' not in body:
    pass  # ItemList schema + visible FAQ is the intended combination here
if body.count('<details class="faq-q">') != len(FAQ_ITEMS):
    raise SystemExit("FAQ must use <details class=\"faq-q\"><summary> markup")
if VOL1 not in body:
    raise SystemExit("Vol 1 must be linked — this is a sequel and the cluster needs the edge")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(SECTIONS)} sections | {N} things | "
      f"{N_BRANDS} brands | ~{len(re.sub(r'<[^>]+>', ' ', head+body+tail).split())} words")
