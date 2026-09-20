#!/usr/bin/env python3
"""build-pants-edit.py — drops/the-pants-edit.html. 20 September 2026.

DONOR: drops/the-bold-tee-edit.html, the most recent roundup built to the
current house structure — nav, breadcrumb, 21:9 hero, drop-header, alternating
.writeup / section.products, .more tail, footer, nav-drawer.

THE DONOR LEAKS IF YOU LET IT. On the Local Rule build the donor's own brand
names survived in a CSS comment and in dead .fg-* rules that rode over inside
the stylesheet, and a guard that searched the whole page for a donor name
tripped on a legitimate cross-link in the More-from-TGI tail. Both lessons are
baked in below: donor CSS comments and dead rules are stripped, and the
donor-name and stray-currency guards are SCOPED ABOVE the .more block, because
that tail is supposed to name other posts.

EVERY FIGURE ON THIS PAGE WAS RE-READ. recheck-pants-prices.py ran immediately
before this build: 16 of 18 machine-read from products.json, Manors and
Sentinel checked by hand in a browser because neither serves products.json.
That re-read caught Casualist at $160 against the $199 carried in the sweep
notes — not a price move, a misread that had already shipped to the grid.

PRODUCT COPY IS BUILT FROM EACH BRAND'S OWN PRODUCT PAGE. Fabric content,
construction and country of make come from the brand's body_html, quoted or
paraphrased as fact. Nothing about a garment on this page is invented, and
nowhere does the page rank the picks against each other or explain why
anything was left out.

Dry run by default.
"""
import importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/the-bold-tee-edit.html"
OUT = ROOT / "drops/the-pants-edit.html"
TAKE = ROOT / "research/pants-edit.json"

SLUG = "the-pants-edit"
TITLE = "The Pants Edit &mdash; The Pleat Came Back"
DESC = ("Eighteen trousers from independent golf brands, one per brand, with live "
        "prices read 20 September 2026 &mdash; and a count of every trouser style on "
        "sale across the TGI universe to show what is actually changing.")

spec = importlib.util.spec_from_file_location("lp", ROOT / "localize-pants.py")
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)
PICKS = lp.PICKS

# Donor identity. Anything here appearing ABOVE the .more tail is a leak.
DONOR_MARKS = ["Bold Tee", "bold-tees", "Guerrilla Golf", "Fried Egg",
               "Butler Pitch", "Gumtree", "graphic tee", "Graphic Tee",
               "Muni Shirts", "Heavyweights", "Art Tees"]

# slug -> the one-paragraph card note. Every factual clause traces to the
# brand's own product page; the last clause is TGI's read of the garment.
NOTES = {
 "odd-ritual":
  "235gsm cotton twill, cut loose with a subtle carrot silhouette, front pleats and "
  "an elasticated back waistband. Made locally in Cape Town. Priced in rand because "
  "Odd Ritual runs no US market &mdash; the store served ZAR to a US browser.",
 "manors":
  "The Greenskeeper shape in recycled cloth, and the piece Manors has rebuilt most "
  "often. Shot on a model head to toe on their own page, which on a trouser this "
  "full is the only photograph that tells you anything.",
 "walker":
  "Lightweight stretch twill with an internal ball-marker pocket and rear tee-holder "
  "slots. Walker say it plainly: designed as an oversized fit, size down for standard. "
  "The shelf this came off repriced twice in an afternoon &mdash; check before you buy.",
 "sentinel":
  "MajoTech in olive, $210, and the most technical trouser here by some distance. "
  "Sentinel is a Squarespace store with no machine-readable feed, so this price was "
  "read by eye on 20 September rather than pulled from a catalogue.",
 "quiet-golf":
  "57% cotton, 35% nylon, 8% spandex &mdash; four-way stretch, quick-drying, snap front "
  "with a secondary button. Quiet Golf note it is cut with added length and shrinkage "
  "allowance for the cotton content and say to order true size.",
 "casualist":
  "Organic cotton twill, high waist with a hidden drawstring, clean front pleats, "
  "straight leg. Made in Portugal, in taupe and beige. Casualist&rsquo;s own line for it "
  "&mdash; &ldquo;the kind of drape that rewards standing still&rdquo; &mdash; is the whole pitch.",
 "students":
  "50% polyester, 50% wool, double-pleated, with satin trim on the inner waistband and "
  "buttoned welt pockets at the back. The most tailored thing on this list and the one "
  "that most clearly is not a performance chino.",
 "public-drip":
  "A nylon blend with a little stretch, double-pleated, straight leg with a taper. "
  "Public Drip name the reference outright: the classic menswear suit pant. In "
  "pinstripe, which is the part that will get looked at.",
 "criquet":
  "74% cotton, 25% Tencel, 1% spandex corduroy, in 30, 32 and 34 inch inseams with an "
  "embroidered Grassy C at the back right hip. Designed in Austin. Twenty-one size "
  "combinations live, which is the deepest run here.",
 "gramicci":
  "12oz 100% cotton slub denim, garment-washed, five wide pockets, and an elastic "
  "waistband with Gramicci&rsquo;s integrated nylon belt. Not a golf trouser and never "
  "claimed to be &mdash; it is on this list because the shape is exactly right.",
 "malbon":
  "Stone-washed cotton herringbone twill, army-derived, relaxed leg, mid rise, 100% "
  "cotton. Malbon call it military-inspired utility and for once the copy matches the "
  "garment. Seven of seven sizes live.",
 "siegelman":
  "70% cotton, 30% polyester, nylon coil zips lined in athletic mesh, elastic drawcord "
  "waist, unisex, made in Los Angeles. Dry clean only, which tells you what kind of "
  "track pant this is.",
 "birds-of-condor":
  "A classic black chino in cotton-spandex with a DWR coating, a fixed waist with belt "
  "loops and a zipped stash pocket. Birds of Condor warn the sizing runs large &mdash; "
  "their 30 fits like a 32. The cheapest trouser on this list.",
 "merrill":
  "Baggy and pleated in a lightweight stretch blend with an elastic waistband and belt "
  "loops. Merrill&rsquo;s own advice is to buy your normal waist and have the length "
  "taken up, which is honest about what a baggy trouser needs.",
 "stitch":
  "96% polyester, 4% spandex, five-pocket, moisture-wicking. This is the performance "
  "chino the rest of the list is reacting against, built well &mdash; and with ninety "
  "size-and-colour combinations it is also the easiest one here to actually fit.",
 "anti":
  "Single tuck, straight and deliberately not tapered below the knee, 100% cotton, with "
  "an Old English logo embroidered on the back pocket. Priced in yen: ANTi&rsquo;s "
  "storefront serves a converted dollar figure, and the yen is the number the brand set.",
 "olydoe":
  "Cotton, Tencel and linen &mdash; linen for breathability, Tencel for the recovery "
  "linen does not have. PRE-SALE: Olydoe state this ships in October or November, so "
  "it is not a trouser you will have this week.",
 "eastside":
  "100% nylon, relaxed with a tapered leg, dual cargo patch pockets, elastic waistband "
  "with a drawcord. The only cargo on the list, and the workwear reference is the point "
  "rather than a detail.",
}
# the PICKS slug for ANTi is anti-country-club; the note key is shorter
NOTES["anti-country-club"] = NOTES.pop("anti")


# CSS THIS PAGE ADDS THAT THE DONOR DOES NOT HAVE.
# On Found Golf a .axxa-note class shipped on 20 cards with no rule anywhere in
# the stylesheet, so it rendered as unstyled body text and nobody noticed until
# the page was looked at. EXTRA_CSS below is injected into <head>, and
# verify() refuses the build if any class the builder emits has no rule.
EXTRA_CSS = """
.pe-stock{font-family:var(--mono);font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;color:#555;margin:6px 0 2px;}
"""

# Every custom class this builder writes. Each must have a rule in the page.
OWN_CLASSES = ["pe-stock"]

# WHICH PICKS THE BRAND ITSELF CALLS PLEATED, with the phrase that says so.
# The sidebar count is computed from THIS, not typed. The first cut of the page
# carried "Pleated 9 of 18", a number nobody had counted — the same class of
# error as a guard that returns a plausible value. Malbon's Station Pant
# photographs as pleated and is deliberately NOT in here: Malbon's own copy
# says "relaxed leg", never "pleat", and a photograph is not a sourced fact.
PLEATED = {
 "odd-ritual":  "Front pleats and an elasticated back waistband",
 "manors":      "The double-pleat at the front nods to timeless on-course etiquette",
 "casualist":   "Clean front pleats",
 "students":    "Double pleated front trousers",
 "public-drip": "The double pleat design offers a refined, structured look",
 "merrill":     "Baggy Pleated Trousers",
 "anti-country-club": "Single tuck",
 "olydoe":      "Pleated Walker Pant",
}


def esc(s):
    return s


def head_block(donor_head):
    """Rewrite every donor-specific string in <head>, then prove none survive."""
    h = donor_head
    plain = re.sub(r"&mdash;", "—", TITLE)
    subs = [
      (r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>"),
      (r'(<meta name="description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")',
       rf"\g<1>{SLUG}\g<2>"),
      (r'(<meta property="og:title" content=")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'(<meta property="og:description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<meta property="og:image" content="https://thegrassyissue\.com/images/)[^"]*(")',
       r"\g<1>pants-edit/band-hero.jpg\g<2>"),
      (r'(<meta name="twitter:title" content=")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'(<meta name="twitter:description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")',
       rf"\g<1>{SLUG}\g<2>"),
      (r'("headline":\s*")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'("description":\s*")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'("url":\s*"https://thegrassyissue\.com/drops/)[^"]*(")', rf"\g<1>{SLUG}\g<2>"),
      (r'("@id":\s*"https://thegrassyissue\.com/drops/)[^"]*(")', rf"\g<1>{SLUG}\g<2>"),
      (r'("datePublished":\s*")[^"]*(")', r"\g<1>2026-09-20\g<2>"),
      (r'("dateModified":\s*")[^"]*(")', r"\g<1>2026-09-20\g<2>"),
    ]
    for pat, rep in subs:
        h = re.sub(pat, rep, h, flags=re.S)

    # DONOR CSS COMMENTS AND DEAD RULES. This is the Local Rule leak, exactly.
    for m in DONOR_MARKS:
        h = re.sub(rf"/\*[^*]*{re.escape(m)}.*?\*/", "", h, flags=re.S | re.I)

    # append this page's own rules to the LAST <style> block in the head
    i = h.rfind("</style>")
    if i < 0:
        sys.exit("! donor head has no <style> block to extend")
    h = h[:i] + EXTRA_CSS + h[i:]
    return h


def band(src, alt, credit=None):
    cap = (f'\n  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;'
           f'text-transform:uppercase;opacity:.5;margin-top:8px;">{credit}</div>'
           if credit else "")
    return (f'<div class="drop-hero"><div class="drop-hero-img">'
            f'<img src="/images/pants-edit/{src}.jpg" alt="{alt}" loading="lazy" />'
            f'</div>{cap}\n</div>\n\n')


def writeup(paras, hdr=None, sidebar=""):
    h = f'    <h2 class="products-hdr" style="margin-top:0;">{hdr}</h2>\n' if hdr else ""
    body = "\n".join(f"    <p>{p}</p>" for p in paras)
    return ('<div class="writeup">\n  <div class="writeup-body">\n'
            + h + body + "\n  </div>\n" + sidebar + "</div>\n\n")


def sidebar_card():
    rows = [("Trousers", "18"), ("Brands", "18"),
            ("Shot on a model", "14 of 18"),
            ("Pleated", f"{len(PLEATED)} of {len(PICKS)}"),
            ("Currencies", "USD, ZAR, JPY &mdash; unconverted"),
            ("Prices read", "20 Sept 2026"),
            ("Sourced from", "Each brand&rsquo;s own store")]
    det = "\n".join(
        f'      <div class="sidebar-detail"><span class="l">{a}</span><span>{b}</span></div>'
        for a, b in rows)
    tags = "\n".join(f'        <span class="hashtag">#{t}</span>'
                     for t in ["ThePantsEdit", "PleatedTrousers", "GolfStyle",
                               "TheEdit", "IndependentGolf"])
    return f'''  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Edit, Counted</div>
{det}
      <a href="/brands" class="sidebar-cta">The Brand Index &rarr;</a>
      <a href="/drops/the-hoodie-and-shorts-edit" class="sidebar-cta" style="margin-top:8px;">Hoodies and Shorts &rarr;</a>
      <a href="/drops/the-bold-tee-edit" class="sidebar-cta" style="margin-top:8px;">The Bold Tee Edit &rarr;</a>
      <div class="hashtags">
{tags}
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
'''


def product_cards():
    out = []
    for slug, brand, name, price, avail, kind, url, img in PICKS:
        note = NOTES[slug]
        stock = f'<div class="pe-stock">{avail}</div>' if avail != "in stock" else ""
        out.append(f'''
    <div class="product-card">
      <div class="product-img"><img src="/images/pants-edit/{slug}.jpg" alt="{brand} {name}" loading="lazy" /></div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name}</div>
        <div class="product-price">{price}</div>
        {stock}<div class="product-desc">{note}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Visit {brand} &#8599;</a>
      </div>
    </div>''')
    return "".join(out)


def build():
    donor = DONOR.read_text(encoding="utf-8")
    take = json.loads(TAKE.read_text(encoding="utf-8"))
    t = take["take"]

    head = head_block(donor[:donor.find("</head>")])
    # everything from <body> to the breadcrumb, and the .more tail onward, is reused
    body_start = donor.find("<body")
    nav_end = donor.find('<div class="breadcrumb">')
    nav = donor[body_start:nav_end]
    tail = donor[donor.find('<div class="more">'):]

    # the .more tail names other TGI posts; replace this post's own name if present
    tail = tail.replace("The Bold Tee Edit", "The Bold Tee Edit")   # left as a real link

    page = head + "</head>\n" + nav

    page += ('<div class="breadcrumb">\n'
             '  <a href="/#feed">Feed</a> / <a href="/#feed">The Edit</a> / The Pants Edit\n'
             '</div>\n\n')

    page += band("band-hero",
                 "Four golfers on a links headland, three of them in trousers",
                 "Manors Golf &mdash; photograph courtesy of the brand")

    page += ('<header class="drop-header">\n'
             f'  <h1>{TITLE}</h1>\n'
             '  <div class="drop-meta">\n'
             '    <span>18 Trousers</span><span class="dot"></span>\n'
             '    <span>18 Brands</span><span class="dot"></span>\n'
             '    <span>Prices read 20 September 2026</span>\n'
             '  </div>\n</header>\n\n')

    page += writeup([f"<strong>{t[0]}</strong>", t[1]], sidebar=sidebar_card())

    page += band("band-1", "Criquet Shirts corduroy trousers, carrying a duffel",
                 "Criquet Shirts &mdash; photograph courtesy of the brand")

    page += ('<section class="products">\n'
             '  <h2 class="products-hdr">Eighteen Trousers &mdash; One Per Brand</h2>\n'
             '  <div class="sec-note">All in stock as of 20 September 2026. '
             'Prices in the currency each brand sets, unconverted.</div>\n'
             '  <div class="products-grid">\n'
             + product_cards() +
             '\n  </div>\n</section>\n\n')

    page += writeup([t[2]], hdr="Why the Pleat Came Back")
    page += band("band-2", "ANTi Country Club Tokyo one-tuck chino, worn",
                 "ANTi Country Club Tokyo &mdash; photograph courtesy of the brand")

    page += writeup([t[3]], hdr="The Cloth Changed Too")
    page += band("band-3", "Odd Ritual pleated trouser from behind, showing the break",
                 "Odd Ritual &mdash; photograph courtesy of the brand")

    page += writeup([t[4]], hdr="What Happens Next")
    page += band("band-4", "Students Golf double-pleated wool trousers, full length",
                 "Students Golf &mdash; photograph courtesy of the brand")

    page += writeup([t[5]], hdr="How to Buy One")
    page += band("band-5", "Public Drip pinstripe pleated trousers, foot raised on a rail",
                 "Public Drip &mdash; photograph courtesy of the brand")

    page += tail
    return page


def verify(path):
    """READ THE FINISHED FILE. Not the string build() returned."""
    h = path.read_text(encoding="utf-8")
    bad = []

    # scope the donor-leak and stray-currency checks ABOVE the .more tail,
    # which legitimately names other posts (the Local Rule lesson)
    i = h.find('<div class="more">')
    ours = h[:i] if i > 0 else h

    for m in DONOR_MARKS:
        if m in ours and m not in ("Bold Tee",):    # sidebar links to it on purpose
            bad.append(f"donor content leaked: {m}")
    if ours.count("Bold Tee") > 1:
        bad.append("Bold Tee appears more than the one deliberate sidebar link")

    n_cards = h.count('class="product-card"')
    if n_cards != len(PICKS):
        bad.append(f"{n_cards} product cards, expected {len(PICKS)}")
    for slug, brand, name, price, *_ in PICKS:
        for needle, what in ((f"/images/pants-edit/{slug}.jpg", "image"),
                             (name, "name"), (price, "price")):
            if needle not in h:
                bad.append(f"{slug} {what} missing")
        if not (ROOT / f"images/pants-edit/{slug}.jpg").exists():
            bad.append(f"{slug} image file not on disk")

    for b in ("band-hero", "band-1", "band-2", "band-3", "band-4", "band-5"):
        if f"/images/pants-edit/{b}.jpg" not in h:
            bad.append(f"{b} not on the page")
        if not (ROOT / f"images/pants-edit/{b}.jpg").exists():
            bad.append(f"{b}.jpg not on disk")

    # the retired picks must be gone
    for gone in ("Bushmills", "Coaches Pant"):
        if gone in h:
            bad.append(f"retired pick on the page: {gone}")

    # house rules
    if re.search(r"\bworth\b", ours, re.I):
        bad.append("the word 'worth' is on the page")
    if re.search(r"what we (cut|left out)|didn&rsquo;t make the", ours, re.I):
        bad.append("a what-we-cut passage is on the page")
    # a dollar figure must not appear for the two non-USD picks
    for slug, cur in (("odd-ritual", "R1,300"), ("anti-country-club", "&yen;28,600")):
        card = re.search(rf'{slug}\.jpg.*?</div>\s*</div>', h, re.S)
        if card and re.search(r"\$\d", card.group(0)):
            bad.append(f"{slug} card carries a dollar figure; it prices in {cur}")

    # THE PLEAT COUNT MUST BE COUNTED, NOT TYPED.
    slugs = {p[0] for p in PICKS}
    for s in PLEATED:
        if s not in slugs:
            bad.append(f"PLEATED names {s}, which is not a pick")
    m = re.search(r'<span class="l">Pleated</span><span>(\d+) of (\d+)</span>', h)
    if not m:
        bad.append("the sidebar has no Pleated row")
    elif (int(m.group(1)), int(m.group(2))) != (len(PLEATED), len(PICKS)):
        bad.append(f"sidebar says {m.group(1)} of {m.group(2)} pleated; "
                   f"the evidence list has {len(PLEATED)} of {len(PICKS)}")

    # A CLASS WITH NO RULE IS THE .axxa-note BUG. Check the finished file.
    for c in OWN_CLASSES:
        if f'class="{c}"' not in h:
            bad.append(f"{c} is declared but never used")
        if f".{c}{{" not in h.replace(" ", "").replace("\n", ""):
            bad.append(f"{c} is used on the page but has no CSS rule")

    if "</html>" not in h:
        bad.append("page is truncated")
    return bad


def main(apply_):
    page = build()
    if not apply_:
        print(f"  would write {OUT.relative_to(ROOT)}  ({len(page):,} bytes)")
        print("\n  dry run — pass --apply")
        return
    OUT.write_text(page, encoding="utf-8")
    bad = verify(OUT)
    if bad:
        sys.exit("! " + "\n! ".join(bad))
    h = OUT.read_text(encoding="utf-8")
    print(f"  wrote {OUT.relative_to(ROOT)}  ({len(h):,} bytes)")
    n_cards = h.count('class="product-card"')
    n_bands = h.count('class="drop-hero-img"')
    print(f"  {n_cards} product cards, {n_bands} bands, {h.count('<h2')} section headings")


if __name__ == "__main__":
    main("--apply" in sys.argv)
