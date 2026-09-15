#!/usr/bin/env python3
"""Brand to Know — TwentyFour Golf. CORRECTIONS + REFRESH, not a new page.

WHY THIS RUN
------------
Lenny asked for "a brand to know" on twentyfourgolf.com. We already had one,
published 2026-08-01 and revamped once. Per the Brand Revisited playbook the
answer is to upgrade the existing page at the existing slug, never a second one.

Then the research turned up a problem worth naming plainly.

THE THING WE GOT WRONG, NOW FIXED
---------------------------------
The live page asserted, four separate times (intro, body, sidebar and the meta
description), that the name means "the game doesn't end when you walk off the
18th." TwentyFour has never said that. Anywhere. It was our own inference
printed as the brand's stated meaning. All four are gone. The page now says the
brand has not explained the name, which is the true position.

Related near-miss: an earlier reviewer flagged the "rigid traditions" line as a
misquote. It is not — it runs as paraphrase in prose with no quotation marks,
which is fine. Checked before changing anything. Where we DO quote now, it is
verbatim from https://twentyfourgolf.com/pages/our-vision.

THE OTHER CORRECTIONS
---------------------
  - "12 Pieces" -> the catalogue is 24 products
  - "8 In-Stock Pieces (Checked Aug 2026)" -> 11 buyable on 2026-09-15
  - Motion Polo A$100 -> A$110 (the brand's own blog still says 100; the live
    product page says 110, so the product page wins)
  - "Don't Blame Your Clubs" is now sold out and comes off the buyable grid
  - four buyable pieces were missing entirely: Plaid Quarter Zip, Alpine Camo
    Cap, OG Cap Dark Camo, TFG Sports Cap Black

WHAT THIS BRAND DOES NOT PUBLISH, so we do not print it
-------------------------------------------------------
  - a founder name. Lenny's call, 2026-09-15: do NOT name him. He is not named
    on his own site; the only link is an Australian business register entry for
    a sole trader. We would be the first to attach it, sourced to a tax record.
    The page says "the founder" throughout.
  - any manufacturing information whatsoever. No country of origin, no factory,
    no mill, no "made in". A sweep of all 24 product descriptions for made in /
    origin / batch / handmade / sewn / mill / supplier / factory returned zero
    matches. Do NOT write or imply Australian-made. The brand claims only that
    it was BORN on the east coast.
  - a reason for the name (see above)
  - press. There is none — not Golf Australia, not Inside Golf, nothing.
  - stockists, collaborations, ambassadors, events.

11past11 is a studio whose space the brand borrowed for the AW26 shoot. It is
NOT a collaboration and must not be framed as one.

The Plaid Quarter Zip's own copy contradicts itself — the intro says 100%
brushed cotton flannel, a bullet says 100% french terry cotton. We assert
neither fibre.

FAQ MARKUP: <details class="faq-q"><summary> — div markup fails verify-post.py
and makes apply-faq-style.py append a duplicate.
"""
import re, os, json, html as H

SLUG = "brand-to-know-twentyfour-golf"
TITLE = "Brand to Know &mdash; TwentyFour Golf"
PLAIN = "Brand to Know — TwentyFour Golf"
DESC = ("TwentyFour Golf, the Gold Coast label that started with one camo cap in "
        "January 2025 and now runs 24 products. What's buyable today, what the "
        "AW26 shoot actually was, and the things the brand has never put in writing.")
IMG = "/images/twentyfour-golf/"
TODAY_LABEL = "9/15/26"

CAT = {x["title"]: x for x in json.load(open("research/twentyfour/catalog.json"))}

# stem -> (catalogue title, display name, copy)
COPY = {
 "clubhouse-pants-olive": ("Clubhouse Pants - Olive", "Clubhouse Pants &mdash; Olive",
  "Nylon-spandex with a water-repellent finish, and the only garment in the range with a full size run still intact, 28 through 38. The olive reads closer to a work pant than a golf trouser, which is the point."),
 "clubhouse-pants-black": ("Clubhouse Pants - Black", "Clubhouse Pants &mdash; Black",
  "Same build in black. Three waist sizes have gone &mdash; 28, 34 and 36 &mdash; which tells you where the middle of their customer base sits."),
 "motion-polo-navy": ("Motion Polo - Midnight Navy", "Motion Polo &mdash; Midnight Navy",
  "92% recycled polyester, 8% spandex, four-way stretch, UPF 50+, heat-bonded seams. The brand says the fabric took <em>&ldquo;Over a year in development&rdquo;</em> and calls it a custom blend. Small and medium are gone."),
 "motion-polo-green": ("Motion Polo - Storm Green", "Motion Polo &mdash; Storm Green",
  "The second colourway, same cloth and same story, and it has lost the same two sizes. A muted green that photographs far better than the name suggests."),
 "plaid-quarter-zip": ("Plaid Quarter Zip Jumper", "Plaid Quarter Zip",
  "Published 8/17 and the newest thing they have made. Yarn-dyed and garment-washed, in a plaid that is doing something different from everything else on the site. Only S and XXL remain."),
 "thermal-digital-camo": ("Thermal Digital Camo", "Thermal &mdash; Digital Camo",
  "Flatlock seams and the house digital camo, which the brand traces back to the OG Camo Cap that started the whole thing. Down to XL and XXL."),
 "alpine-camo-cap": ("Alpine Camo Cap", "Alpine Camo Cap",
  "Built on the SignatureFit 5-panel &mdash; short brim, structured front, low crown &mdash; which is the silhouette almost the entire cap line now runs on."),
 "dune-trucker-cap": ("Dune Trucker Cap", "Dune Trucker Cap",
  "The trucker in the AW26 palette, and one of only six pieces in the whole catalogue with every size available today."),
 "og-cap-dark-camo": ("OG Cap - Dark Camo", "OG Cap &mdash; Dark Camo",
  "The darker read on the print the brand was founded on. The original Camo version is sold out and flagged for restock."),
 "tfg-sports-cap-black": ("TFG Sports Cap - Black", "TFG Sports Cap &mdash; Black",
  "Lightweight nylon rather than the cotton the OG caps use, and the cheapest way into the brand at A$55. Published 8/12."),
 "new-tfg-sports-cap-white": ("TFG Sports Cap - White", "TFG Sports Cap &mdash; White",
  "The white version, and the older of the two by five months. Same nylon build."),
}

SECTIONS = [
 ("Buyable Today",
  f"Eleven of the twenty-four pieces can still be bought as of {TODAY_LABEL}. Sizes noted where they have gone.",
  ["clubhouse-pants-olive", "clubhouse-pants-black", "motion-polo-navy", "motion-polo-green",
   "plaid-quarter-zip", "thermal-digital-camo", "alpine-camo-cap", "dune-trucker-cap",
   "og-cap-dark-camo", "tfg-sports-cap-black", "new-tfg-sports-cap-white"]),
]

LOOKBOOK = ["ig-DZ1vwgVEVsh", "ig-DZjx9RRESi0", "ig-DZmTiLTorOE",
            "ig-DZuEEX7kWSU", "ig-DaOknC_Ac_o", "ig-DaWYZNkBhL5"]

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p><strong>TwentyFour Golf</strong> is a Gold Coast label that sells golf caps, and then a few clothes. That is not a slight &mdash; it is the shape of the catalogue. Eighteen of its twenty-four products are hats, and the six garments sit on top of a cap line that is almost permanently sold out.</p>
    <p>It started with one product. The OG Camo Cap went live on 1/15/25, and the digital camo on it has since become the closest thing the brand has to a signature, turning up on a thermal and a second cap colourway. The business behind it registered in Australia in July 2024, runs out of a PO box in Currumbin on the southern Gold Coast, and ships worldwide in Australian dollars.</p>
    <p>The brand writes about itself in the first person and never signs its name. Its vision page says golf <em>&ldquo;shouldn&rsquo;t be bound by rigid traditions. Instead, it should embrace individuality, creativity, and fun&rdquo;</em> and describes a range <em>&ldquo;born on the sun-drenched east coast of Australia&rdquo;</em> reflecting <em>&ldquo;the laid-back lifestyle I love.&rdquo;</em> That is the whole of the origin story as published.</p>
  </div>
</div>
"""

AW26 = """<section class="products">
  <h2 class="products-hdr">AW26, Shot in a Day</h2>
  <p class="cat-kicker">Fifteen pieces, one location, and the clearest look yet at how small this operation is.</p>
  <div class="writeup-body">
    <p>AW26 went up on 6/19 and is still the front-page collection. The brand's own account of the shoot is short and unusually plain about its scale: <em>&ldquo;We shot AW26 on the Gold Coast &mdash; one day, the right crew, no overthinking it. Masa, owner of 11past11, opened his space to us.&rdquo;</em></p>
    <p>11past11 is a photography and film studio in Currumbin Waters, which shares a postcode with the brand's own PO box. Two other people are credited by first name only &mdash; Blake wore the gear, Alex shot it. That is the entire production.</p>
    <p>The collection's stated ambition is bigger than its footprint: <em>&ldquo;TwentyFour Golf started with one idea: Australian golf deserved a brand that treated it seriously. Not stuffy. Not bargain-bin. A brand with a point of view.&rdquo;</em> Fifteen pieces went out in the drop, eight of them caps across two silhouettes.</p>
  </div>
</section>
"""

SOLDOUT = """<section class="products">
  <h2 class="products-hdr">The Thirteen That Are Gone</h2>
  <p class="cat-kicker">Every sold-out product in the catalogue is a cap, which is the most useful fact about this brand.</p>
  <div class="writeup-body">
    <p>Thirteen of the twenty-four products cannot be bought right now, and every single one is headwear: OG Cap in Black, Camo, Red, Woodland and Tour; the Signature Cap in Black and Khaki; the Black TF Trucker; the Development Division Cap; the Blue Checker; both Sun Plaid caps; and the Don&rsquo;t Blame Your Clubs cap, which was still buyable when we last wrote about this brand in August.</p>
    <p>The Blue Checker and both Sun Plaids only went live on 8/20 and are already gone. The original OG Camo Cap &mdash; product number one, from January 2025 &mdash; is the only one carrying a restock flag.</p>
    <p>Caps at A$59.95 clearing this consistently, while A$110 polos hold their sizes, is the whole business model showing through the inventory.</p>
  </div>
</section>
"""

UNKNOWN = """<section class="products">
  <h2 class="products-hdr">What Isn&rsquo;t Published</h2>
  <p class="cat-kicker">A short and honest list, because the gaps are part of the picture.</p>
  <div class="writeup-body">
    <p><strong>Where anything is made.</strong> No country of origin, no factory, no mill, no supplier, and no &ldquo;made in&rdquo; statement appears anywhere on the site or in any of the twenty-four product descriptions. The brand says it was <em>born</em> on the east coast and that AW26 was <em>shot</em> on the Gold Coast. Neither is a manufacturing claim, and we are not going to turn them into one.</p>
    <p><strong>Who runs it.</strong> The vision page is written in the first person and the founder is never named. We have left it that way.</p>
    <p><strong>Why &ldquo;TwentyFour.&rdquo;</strong> The brand has never explained the name. An earlier version of this page offered a reading of it as though it were the brand's own; that was ours, not theirs, and it has been removed. The tagline is Always In Play and a homepage section reads THE GAME NEVER STOPS, which points somewhere, but pointing is not stating.</p>
    <p><strong>Anything written about them.</strong> No press coverage exists in Australian golf media or anywhere else we could find. For a brand fourteen months into selling, that is normal. It also means everything above comes from the shop itself.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What does TwentyFour Golf actually sell?",
  "Twenty-four products, of which eighteen are caps. The rest is two Motion Polos, two pairs of Clubhouse Pants, a Thermal and a Plaid Quarter Zip. Prices run A$55 for a TFG Sports Cap to A$130 for the pants."),
 ("Where is TwentyFour Golf made?",
  "The brand does not say. There is no country of origin, factory, mill or &ldquo;made in&rdquo; statement anywhere on the site or in any product description. It states only that the brand was born on Australia's east coast, and the business operates from Currumbin on the Gold Coast."),
 ("Why is it called TwentyFour?",
  "The brand has never explained it. The tagline is Always In Play and the homepage carries a THE GAME NEVER STOPS header, but no published source gives a reason for the number."),
 ("What was the AW26 collection?",
  "Fifteen pieces, released 6/19/26, shot on the Gold Coast in a single day at 11past11, a studio in Currumbin Waters. Eight of the fifteen were caps across two silhouettes. 11past11 lent the space; it was not a collaboration."),
 ("Can you still buy the Don't Blame Your Clubs cap?",
  "Not right now. It sold out after we first wrote about the brand in August. Thirteen of the twenty-four products are currently sold out and all thirteen are caps."),
 ("Does TwentyFour ship internationally?",
  "Yes, worldwide, priced in Australian dollars and sent via AusPost. Orders are processed in one to fourteen business days, which is a wide window and consistent with a small self-fulfilled operation."),
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
    while os.path.exists(f"images/twentyfour-golf/{s}-a{n+1}.jpg"):
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


def stock_tag(a):
    if a == "in stock":
        return ""
    m = re.search(r'sizes? (.+) gone', a)
    return f" &middot; {m.group(1)} gone" if m else " &middot; limited sizes"


def card(s):
    cat_title, name, desc = COPY[s]
    p = CAT[cat_title]
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, name)}
      <div class="product-body">
        <div class="product-brand">TwentyFour Golf</div>
        <div class="product-name">{name} &middot; A${p['price_aud']}{stock_tag(p['availability'])}</div>
        <div class="product-desc">{desc}</div>
        <a href="{p['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""


def sec(hdr, kicker, slugs):
    c = "\n    ".join(card(s) for s in slugs)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


LOOK = ('<section class="products" style="border-top:none;padding-top:48px">\n'
        '  <h2 class="products-hdr">In the Wild</h2>\n'
        '  <p class="cat-kicker">Almost every frame the brand publishes was shot on the Gold Coast.</p>\n'
        '  <div class="tf-look" style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">\n'
        + "".join(
            '    <figure style="margin:0;border:.5px solid var(--ink);overflow:hidden">'
            f'<img src="{IMG}{s}.jpg" alt="TwentyFour Golf on the Gold Coast" loading="lazy" '
            'style="width:100%;aspect-ratio:1/1;object-fit:cover;display:block" /></figure>\n'
            for s in LOOKBOOK)
        + '  </div>\n</section>\n')
# The old page had no kickers, so it never carried the house .cat-kicker rule.
# verify-post.py fails "cat-kicker has a real CSS rule" without it; copied
# verbatim from the Gamut page so every post renders kickers identically.
LOOK_CSS = ("<style>.cat-kicker{font-family:var(--sans);font-size:15px;line-height:1.75;"
            "color:#3f443e;margin:0 0 36px;max-width:70ch;border-left:3px solid var(--rough);"
            "padding:4px 0 4px 18px}\n"
            "@media(max-width:760px){.tf-look{grid-template-columns:repeat(2,1fr)!important}}</style>")


def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&ndash;", "–"))


SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

P = f"drops/{SLUG}.html"
old = open(P, encoding="utf-8").read()
head = old[:old.find('<div class="breadcrumb">')]
tail = old[old.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)
if "cat-kicker{" not in head:
    head = head.replace("</head>", LOOK_CSS + "\n</head>")

n_buy = sum(len(s[2]) for s in SECTIONS)
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  TwentyFour Golf</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>Updated {TODAY_LABEL}</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>24 Products &middot; {n_buy} Buyable</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}brand-hero.jpg" '
        'alt="TwentyFour Golf apparel photographed on the Gold Coast, Queensland" /></div></div>\n'
        + INTRO + sec(*SECTIONS[0]) + AW26 + LOOK + SOLDOUT + UNKNOWN + FAQ)

# ---- guards -----------------------------------------------------------------
txt = re.sub(r'<[^>]+>', ' ', body)
if re.search(r"walk off the 18th", txt, re.I):
    raise SystemExit("the unsourced name explanation is back — TwentyFour has never said this")
if re.search(r'\bworth\b', txt, re.I):
    raise SystemExit("BANNED WORD 'worth'")
for bad in ["made in australia", "australian-made", "australian made", "hand-sewn", "handmade"]:
    if bad in txt.lower():
        raise SystemExit(f"'{bad}' — the brand publishes NO manufacturing information")
if re.search(r"\bHarlow\b", txt):
    raise SystemExit("founder named — Lenny's call was to leave him unnamed")
if re.search(r"collaborat", txt, re.I) and "11past11" in txt:
    seg = txt[max(0, txt.find("11past11") - 300):txt.find("11past11") + 300]
    if re.search(r"collaborat", seg, re.I) and "not a collaboration" not in seg:
        raise SystemExit("11past11 framed as a collaboration — it lent a studio")
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(COPY):
    raise SystemExit(f"COPY/section mismatch: {set(COPY) ^ set(placed)}")
for s in placed:
    if CAT[COPY[s][0]]["availability"] == "sold out":
        raise SystemExit(f"{s} is sold out and cannot sit in the buyable grid")
gone = [s for s in placed + LOOKBOOK + ["brand-hero"]
        if not os.path.exists(f"images/twentyfour-golf/{s}.jpg")]
if gone:
    raise SystemExit(f"images missing: {gone}")

open(P, "w", encoding="utf-8").write(head + body + tail)
print(f"wrote {P} | 24 products, {n_buy} buyable | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
