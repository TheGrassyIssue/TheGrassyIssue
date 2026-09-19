#!/usr/bin/env python3
"""
build-hoodie-shorts.py — "Hoodie and Shorts, The Best Fall Combo". 18 Sept 2026.

Lenny's brief: 12 hoodies, 12 shorts, lean on Malbon / Sentinel / Odd Ritual /
Walker, source freely from the brand universe, repeats across the two sections
are fine. Angle: Texas fall is a lie, and the combo runs September to May —
course, couch, football.

WHAT THE SOURCING PASS ACTUALLY FOUND, because it changed the lineup:
  · ODD RITUAL MAKES NEITHER. No hooded sweatshirt in their catalogue at all,
    and no shorts of any kind. Verified against their live product pages, not
    the Shopify search API, which reports available:true for items whose own
    page says out of stock. They are named in the brief and are still not here.
  · SENTINEL makes six hoodies but their only short, the Salt Wash, is sold out
    in all three colourways. So Sentinel is in the hoodie section only.
  · WALKER RUNS A US STOREFRONT. Their default (Australian) storefront shows
    AUD, which is what the first pass recorded; walkergolfthings.com/en-us shows
    USD, and that is the number a US reader is charged. Both Walker entries were
    corrected to the /en-us price. SOUNDER is the one non-USD price left, in GBP;
    I have not checked whether they run a US storefront too. House rule stands:
    print the currency the store shows, convert nothing.

STRUCTURE. Two sections of 12. The shorts split 6 casual / 6 on-course, which
was Lenny's call and is also the honest shape of the market: most golf brands
make a technical short and nothing else, so the casual six had to be hunted.

CURRENCY IS PART OF THE DATA, not decoration. Every price was read off the
brand's own store on 18 September 2026 and is reproduced as shown.

Idempotent: byte-identical across consecutive runs. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = ROOT / "research/hoodie-shorts.json"
SRC  = ROOT / "drops/austin-coffee-guide.html"      # furniture donor
OUT  = ROOT / "drops/the-hoodie-and-shorts-edit.html"
SLUG = "/drops/the-hoodie-and-shorts-edit"

TITLE = "Hoodie and Shorts &mdash; The Best Fall Combo"
DESC  = ("Twelve hoodies and twelve shorts from the independent golf brand "
         "universe, with live prices read 18 September 2026. The combo that "
         "covers a Texas shoulder-season round, the couch and the whole "
         "football season.")
# HERO, fifth version — three frames of the Walker Applique Hood, Lenny's pick,
# merged into one 1600x685 band. Left: the hood on a wooden door. Middle: the
# felt appliqué letters in macro. Right: the ribbed cuff and the Kooka patch.
# All three are Walker's own product photography for this one garment, so the
# hero opens on the exact hoodie sitting at #4 in the section below.
#
# The four rejected versions, kept because the pattern is the lesson:
#   v1  Sugarloaf packshot — also product card #4, a 1:1 cutout on white.
#   v2  Sugarloaf course photography — wide, but long sleeves and trousers.
#   v3  three Malbon on-model studio frames — a hoodie, but a seamless sweep.
#   v4  three outdoor Devereux/Manors journal frames — good photographs of
#       golfers, but not of a hoodie, which was the thing being asked for.
# The through-line: every version that failed was solving for "editorial" or
# "outdoors" when the actual requirement was "show the hoodie".
HERO  = "/images/hoodie-shorts/hero.jpg"

# More from the Feed — the gear cluster, not the Austin cluster.
MORE = [
    ("/drops/best-golf-streetwear-brands-2026",
     "/images/hoodie-shorts/h-malbon.jpg",
     "The 5 Best Golf Streetwear Brands in 2026"),
    ("/drops/accessories-on-and-off-the-course",
     "/images/hoodie-shorts/sc-metalwood-studio.jpg",
     "Accessories, On and Off the Course"),
    ("/drops/the-white-tee-edit-2026",
     "/images/hoodie-shorts/h-random-golf-club.jpg",
     "The White Tee Edit 2026"),
    ("/drops/the-hat-edit-austin-summer",
     "/images/hoodie-shorts/h-birds-of-condor.jpg",
     "The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets"),
]


def plain(s):
    return (s.replace("&mdash;", "—").replace("&middot;", "·")
             .replace("&amp;", "&").replace("&reg;", "®")
             .replace("&pound;", "£").replace("&rsquo;", "’")
             .replace("&ldquo;", "“").replace("&rdquo;", "”"))


def card(row, kind):
    """One product card in the shape btk-template.py and verify-post both expect.

    THE CARD MUST BE A <div class="product-card"> WITH THE LINK INSIDE IT.
    Not an <a class="product-card"> wrapping everything — that anchor-shaped
    variant is exactly what stranded six Brand to Know pages (task #640): the
    template searches for the literal '<div class="product-card"' and silently
    reports "no product cards on this page" when it finds an anchor instead.
    """
    slug, brand, name, price, cur, purl, _img, desc = row
    ext = ".png" if (ROOT / f"images/hoodie-shorts/{kind}-{slug}.png").exists() else ".jpg"
    src = f"/images/hoodie-shorts/{kind}-{slug}{ext}"
    alt = plain(f"{brand} {name}")
    # Non-USD gets the currency spelled out; USD is the unmarked default.
    tag = f'{price} <span class="cur">{cur}</span>' if cur != "USD" else price
    return (
        f'    <div class="product-card">\n'
        f'      <div class="product-img"><img src="{src}" alt="{alt}" loading="lazy" /></div>\n'
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
        for h, i, n in MORE)
    return ('<!-- More from the Feed -->\n<div class="more">\n  <div class="more-hdr">\n'
            '    <span class="more-label">More from the Feed</span>\n'
            '    <a href="/" class="more-link">See All &rarr;</a>\n  </div>\n'
            f'  <div class="more-grid">\n{cards}\n  </div>\n</div>\n\n')


EXTRA_CSS = """
/* --- hoodie-shorts --- */
/* .product-price is used by four other roundups but its rule lives on THOSE
   pages, not in the coffee-guide furniture this page clones. verify-post caught
   the class being used with no rule behind it. Copied verbatim from the
   existing house rule so the four pages and this one stay identical. */
.product-price{font-family:var(--mono);font-size:11px;letter-spacing:.05em;margin-bottom:10px}
/* currency chip on non-USD prices */
.cur{font-family:var(--mono);font-size:9px;letter-spacing:.1em;opacity:.55;
     vertical-align:.18em;margin-left:2px;}
.sec-note{font-size:14px;line-height:1.6;opacity:.75;margin:-6px 0 22px;}
"""


def build():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    src = SRC.read_text(encoding="utf-8")

    head = src[:src.find('<div class="breadcrumb">')]
    tail = src[src.find('<footer'):]

    old = "The Pre-Round Pour &mdash; 17 Austin Coffee Shops for Golfers"
    head = (head.replace(old, TITLE).replace(plain(old), plain(TITLE)))
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{DESC}"', head)
    head = re.sub(r'(property="og:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = re.sub(r'(name="twitter:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = head.replace("/drops/austin-coffee-guide", SLUG)
    head = re.sub(r'("description"\s*:\s*)"[^"]*"', rf'\1"{DESC}"', head, count=1)
    # Image swaps, BOTH forms. The donor carries relative /images/... paths AND
    # absolute https://thegrassyissue.com/images/... ones (og:image, twitter:image,
    # schema). Rewriting only the relative form left the share card pointing at
    # the coffee guide's Radio Coffee photo on a post about hoodies — invisible on
    # the page itself, wrong everywhere the link gets pasted.
    head = re.sub(r'(content=")/images/[^"]*(")', rf'\1{HERO}\2', head)
    head = re.sub(r'(content=")https://thegrassyissue\.com/images/[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = re.sub(r'("image"\s*:\s*")[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = head.replace("</style>", EXTRA_CSS + "</style>", 1)

    allrows = spec["hoodies"] + spec["shorts_casual"] + spec["shorts_golf"]
    # COMPUTE the sidebar facts. "Brands 18" was hardcoded and wrong — the real
    # figure is the distinct count, which eight cross-section repeats reduce.
    n_brands = len({r[1] for r in allrows})
    def _n(s): return float(s.replace("$", "").replace("&pound;", "").replace(",", ""))
    cheap_hood  = min(spec["hoodies"], key=lambda r: _n(r[3]))[3]
    cheap_short = min(spec["shorts_casual"] + spec["shorts_golf"], key=lambda r: _n(r[3]))[3]

    hoods = "\n".join(card(r, "h")  for r in spec["hoodies"])
    cas   = "\n".join(card(r, "sc") for r in spec["shorts_casual"])
    golf  = "\n".join(card(r, "sg") for r in spec["shorts_golf"])

    body = f'''<div class="breadcrumb">
  <a href="/#feed">Feed</a> / <a href="/#feed">The Edit</a> / Hoodie and Shorts
</div>

<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" alt="Three views of the Walker Applique Hood in navy &mdash; hanging on a wooden door, the felt appliqu&eacute; chest logo in close-up, and the Kooka patch at the cuff" /></div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:8px;">Walker Applique Hood &middot; photographs courtesy of Walker Golf Things</div>
</div>

<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>24 Pieces</span><span class="dot"></span>
    <span>12 Hoodies &middot; 12 Shorts</span><span class="dot"></span>
    <span>Prices read 18 September 2026</span>
  </div>
</header>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>Texas fall is a lie.</strong> The calendar says September and the
    car says 84 degrees at noon. But the 7am tee time is 58, the wind off the
    lake has an edge to it, and by the ninth hole you are carrying whatever you
    started in. There is exactly one outfit that solves this, and every muni in
    Austin is already wearing it: a hoodie and a pair of shorts.</p>

    <p>It works because the two halves fail at opposite times. The hoodie handles
    the cold you get for ninety minutes; the shorts handle the heat you get for
    the other four hours. You take the hoodie off at the turn, tie it to the bag,
    and put it back on in the parking lot. Nothing else in a golf wardrobe covers
    that range without a mid-round change.</p>

    <p>And the combination does not stop at the course. It is the same thing you
    wear on the couch at one o'clock for the early window, at a tailgate, and out
    to get tacos afterwards. In Austin it runs from September to May &mdash; nine
    months of the year where a hoodie and shorts is not a compromise between two
    seasons but the correct answer to both.</p>

    <p>So: twelve of each, from the independent brands we cover. Prices were read
    off each brand's own store on 18 September 2026. Where a brand prices in
    Australian dollars or pounds, that is what is printed &mdash; we have not
    converted anything.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Combo, Costed</div>
      <div class="sidebar-detail"><span class="l">Hoodies</span><span>12</span></div>
      <div class="sidebar-detail"><span class="l">Shorts</span><span>12</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>{n_brands}</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest pair</span><span>{cheap_short} + {cheap_hood}</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>18 Sept 2026</span></div>
      <div class="sidebar-detail"><span class="l">Sourced from</span><span>Each brand&rsquo;s own store</span></div>
      <a href="/brands" class="sidebar-cta">The Brand Index &rarr;</a>
      <a href="/drops/best-golf-streetwear-brands-2026" class="sidebar-cta" style="margin-top:8px;">Best Golf Streetwear Brands &rarr;</a>
      <a href="/drops/the-hat-edit-austin-summer" class="sidebar-cta" style="margin-top:8px;">The Hat Edit &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#HoodieAndShorts</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#TheEdit</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#MuniLife</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</div>

<section class="products">
  <h2 class="products-hdr">The Hoodies &mdash; 12, Cheapest First</h2>
  <div class="sec-note">One per brand, ordered by the price their own store showed on 18 September 2026.</div>
  <div class="products-grid">

{hoods}
  </div>
</section>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>A note on weight.</strong> The two useful numbers are fabric weight
    and what the fleece is made of. A 380 to 400gsm cotton fleece &mdash; the
    Malbon Fesque, the Walker Hedge Hood &mdash; is the one that feels like a
    hoodie is supposed to feel and is too much by the fourth hole in October.
    Polar fleece and Polartec, on the Students Spade and the Manors Outsider,
    weigh less and breathe once you start swinging, which is why those two are
    the ones you can leave on.</p>
  </div>
</div>

<section class="products">
  <h2 class="products-hdr">The Shorts &mdash; 6 for the Couch</h2>
  <div class="sec-note">Corduroy, terry, mesh and seersucker. None of these are technical, and that is the point.</div>
  <div class="products-grid">

{cas}
  </div>
</section>

<section class="products">
  <h2 class="products-hdr">The Shorts &mdash; 6 for the Round</h2>
  <div class="sec-note">Belt loops, real pockets and a fabric that moves. Priced as each store showed on 18 September 2026.</div>
  <div class="products-grid">

{golf}
  </div>
</section>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>What we could not include.</strong> Odd Ritual is one of the
    brands we reach for most and they are not on this page, because they do not
    currently make a hooded sweatshirt or a short of any kind &mdash; their line
    runs to polos, tees, trousers and the Caddie Jacket. Sentinel Golf is in the
    hoodie section but not the shorts section: their Salt Wash Short is sold out
    in all three colourways as of this morning.</p>

    <p>Three of the shorts above are corduroy and one is seersucker, which is
    not where anyone expected a golf list to land in 2026. Both fabrics do the
    same trick &mdash; they hold their shape away from the leg instead of
    sticking to it &mdash; and both read as deliberate in a way a performance
    short never quite manages once you are off the property. Put either with any
    hoodie on the list and you are dressed for a 7am tee time, a noon kickoff and
    dinner, which was the entire assignment.</p>
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
    allrows = spec["hoodies"] + spec["shorts_casual"] + spec["shorts_golf"]
    hood_brands = [r[1] for r in spec["hoodies"]]
    shrt_brands = [r[1] for r in spec["shorts_casual"] + spec["shorts_golf"]]

    checks = [
        ("24 product cards", page.count('<div class="product-card"') == 24,
         str(page.count('<div class="product-card"'))),
        ("cards are div-shaped, not anchor-shaped",
         '<a class="product-card"' not in page, ""),
        ("three product sections", page.count('<h2 class="products-hdr"') == 3, ""),
        ("12 hoodies / 12 shorts",
         len(spec["hoodies"]) == 12
         and len(spec["shorts_casual"]) + len(spec["shorts_golf"]) == 12, ""),
        # HOUSE RULE: no repeat brands WITHIN a section. Lenny explicitly allowed
        # a brand to appear once in each of the two sections, so the check is
        # per-section, not across the page.
        ("no repeat brand within the hoodies",
         len(set(hood_brands)) == 12, str(sorted(set(
             b for b in hood_brands if hood_brands.count(b) > 1)))),
        ("no repeat brand within the shorts",
         len(set(shrt_brands)) == 12, str(sorted(set(
             b for b in shrt_brands if shrt_brands.count(b) > 1)))),
        # Odd Ritual is named in the brief but makes neither garment. If a future
        # edit slips it in, that is a factual error about a live catalogue.
        ("Odd Ritual not sold as a product here",
         not re.search(r'product-brand">\s*Odd Ritual', page), ""),
        ("every non-USD price carries its currency",
         all(f'{r[3]} <span class="cur">{r[4]}</span>' in page
             for r in allrows if r[4] != "USD"), ""),
        ("no currency was converted",
         "USD)" not in page and "approx" not in page.lower(), ""),
        ("every local image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/hoodie-shorts/[^"]+)"', page)), ""),
        # Scope: the 24 card images must all differ. The hero and the four
        # more-cards deliberately REUSE product shots, so counting every src on
        # the page and subtracting the hero gave 23 and failed a correct page.
        ("24 distinct product-card images",
         len(set(re.findall(r'class="product-img"><img src="([^"]+)"', page))) == 24,
         str(len(set(re.findall(r'class="product-img"><img src="([^"]+)"', page))))),
        ("no hot-linked product images",
         not re.search(r'<img[^>]+src="https?://', page), ""),
        ("every img has alt", all('alt="' in i for i in re.findall(r"<img[^>]*>", page)), ""),
        ("banned word 'worth' absent", not re.search(r'\bworth\b', page, re.I), ""),
        ("every internal /drops/ link resolves", *links_ok(page)),
        ("has more-grid + aff disclosure",
         page.count('class="more-card"') == 4
         and page.count('class="aff-disclosure"') == 1, ""),
        ("sidebar brand count matches the data",
         f">{len({r[1] for r in allrows})}<" in page, ""),
        # The hero IS the Applique Hood, so the product must be on the page.
        # If a future edit drops it, the hero becomes an advert for something
        # the reader cannot find below.
        ("Walker Applique Hood is in the post",
         "Applique Hood" in page, ""),
        ("hero credits the brand whose garment it shows",
         "courtesy of Walker Golf Things" in page, ""),
        ("no AUD price survives", "AUD" not in page, ""),
        ("canonical points at this slug", SLUG in page, ""),
        # No image reference anywhere in the head may still point at the donor.
        ("no donor imagery survives in the head",
         "/images/austin-coffee/" not in page[:page.find("<body")], ""),
        ("og:image and twitter:image are this post's hero",
         all(HERO in m for m in re.findall(
             r'(?:og:image|twitter:image)" content="([^"]*)"', page[:page.find("<body")])), ""),
        ("no donor slug in the head",
         "austin-coffee-guide" not in page[:page.find("<body")], ""),
        ("exactly one h1", len(re.findall(r'<h1', page)) == 1, ""),
        ("div balance", page.count("<div") == page.count("</div>"),
         f'{page.count("<div")}/{page.count("</div>")}'),
        ("section balance", page.count("<section") == page.count("</section>"), ""),
        ("anchor balance", len(re.findall(r'<a\b', page)) == page.count("</a>"), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d}"); ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {len(page):,} bytes")
    if apply_:
        OUT.write_text(page, encoding="utf-8"); print(f"  wrote {OUT.name}")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
