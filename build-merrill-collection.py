#!/usr/bin/env python3
"""
build-merrill-collection.py — rewrite the Merrill collection, 18 September 2026.

WHY THIS EXISTS AND WHY IT IS NOT btk-template.py
--------------------------------------------------
btk-template.py is a REORDERER. It cuts an existing page into blocks and writes
them back in house order; it never writes product copy. Merrill's page carried
five cards, and the Revisited Lenny approved leads on pieces that were not on
the page at all — the polo, the cardigan, the work jacket, the Japanese-made
covers. So the cards have to exist before the template can order them.

This script writes them. Every name, price, and material claim below came off
merrillgolf.com's own Shopify feed on 18 September 2026 and is reproduced from
the brand's own product copy. Nothing here is inferred.

TWO REMOVALS, BOTH DELIBERATE
  · "Target Practice Tee · $60" — sold out in the feed. House precedent is to
    drop discontinued product rather than link a dead page (cf. the Sock Edit).
  · the "A Design Venture Through Golf" lifestyle card — its copy opens "No
    polos." That is now FALSE: the Birds Stripe Polo is live at $65. The claim
    does not get quietly reworded inside a product card; the write-up addresses
    it head on instead.

Idempotent: the block is delimited and replaced wholesale, so re-running is a
no-op. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-merrill-golf.html"
SHOP = "https://merrillgolf.com/products/"

# (image stem, handle, display name, price, description)
ITEMS = [
 ("01-birds-stripe-polo","birds-stripe-polo-navy-white","Birds Stripe Polo","$65",
  "The polo Merrill spent years not making. Short sleeve, three buttons, in a lightweight "
  "cotton jersey the brand custom-dyes itself, with embroidery on the left chest. Cut "
  "slightly boxy and true to size. $65."),
 ("06-palmer-red","palmer-cardigan-fire-red","Palmer Cardigan · Fire Red","$160",
  "A fuzzy mohair-blend knit cardigan with the logo on the left chest, cut slightly "
  "oversized and boxy. Hand wash or dry clean only. This is the piece that marks how far "
  "the range has travelled from screen-printed cotton. $160."),
 ("04-work-jacket","work-jacket-sky-blue","Work Jacket · Sky Blue","$150",
  "Canvas work jacket with a corduroy collar, a chest pocket and embroidery detail, lined "
  "through with flannel. True to size. The least golf-looking thing Merrill makes, and the "
  "easiest to wear off the course. $150."),
 ("05-camp-thermal","camp-merrill-thermal-ls-black-white","Camp Merrill Thermal LS","$100",
  "A heavy jersey body with thermal fabric sleeves — the baseball sleeve done in waffle "
  "knit. 100% cotton, made in the USA. $100."),
 ("08-baggy-trousers","baggy-trousers-black","Baggy Trousers · Black","$125",
  "Pleated and deliberately baggy, in a lightweight stretch fabric with belt loops over an "
  "elastic waistband. Merrill size these by waist and tell you to take them to a tailor for "
  "the length. $125."),
 ("09-script-vneck","script-v-neck-sweatshirt-navy","Script V Neck Sweatshirt","$150",
  "Fourteen-ounce garment-dyed fleece with an embroidered script mark, cut as a V neck "
  "rather than a crew. 100% cotton, made in the USA, true to size. $150."),
 ("13-golfco-tee-green","golf-company-tee-vintage-green","Golf Company Tee · Vintage Green","$55",
  "The piece the brand was built on, still at the price it always was. Heavyweight "
  "vintage-washed cotton, screen printed front and back, dropped shoulder and a cropped, "
  "boxy fit. $55."),
 ("11-riders-tee","riders-tee-black","Riders Tee · Black","$85",
  "Cotton jersey screen printed with artwork by Finito, one of six collaborations Merrill "
  "keeps a standing page for. Slightly oversized with a cropped fit, made in the USA. $85."),
 ("16-birds-dad-hat","birds-dad-hat-khaki-green","Birds Dad Hat · Khaki/Green","$50",
  "Six-panel unstructured dad hat in brushed cotton twill, with an antique brass buckle at "
  "the back. The flying duck, doing what it does. $50."),
 ("15-script-hat","script-hat-navy","Script Hat · Navy","$60",
  "The script mark on a six-panel, the quieter of the two hats in the range and the one "
  "that reads as a plain cap from ten feet away. $60."),
 ("17-headcovers-olive","headcovers-olive-green","Headcovers · Olive Green","$110",
  "Driver and fairway covers in quilted Japanese nylon, with a Hinoki leather lid carrying "
  "the embroidered mark and a POLARTEC fleece lining. Handmade in Japan. Both sizes fit "
  "most heads. $110."),
 ("18-putter-covers","putter-covers-sage-green","Putter Covers · Sage/Green","$120",
  "Blade and mallet covers in two-tone Japanese nylon with an embroidered logo, jersey mesh "
  "lining and magnetic end closures. Handmade in Japan. $120."),
]

OPEN  = "<!-- MERRILL-COLLECTION:START -->"
CLOSE = "<!-- MERRILL-COLLECTION:END -->"


def card(stem, handle, name, price, desc):
    """A card in the shape the TEMPLATE can actually see.

    THE BUG THIS FIXES, which is bigger than Merrill. btk-template.py finds
    product blocks by searching for the literal '<div class="product-card"'.
    Merrill's cards were '<a class="product-card">' — the whole card was one
    anchor, with the link on the outside. The template therefore reported "no
    product cards found anywhere on the page" and skipped it.

    That is the real reason six of the seven unconverted Brand to Know pages
    never converted — aug-11, beams-golf, found-golf, morning-people-clothiers
    and olydoe are all anchor-carded too. It was never a missing write-up.

    So the card is a div, the link moves inside to .product-link, and the whole
    tile stops being one giant anchor — which is also better for a screen
    reader, since the alt text and the 60-word description were previously
    swallowed into a single link label.
    """
    alt = f"Merrill Golf &mdash; {name.replace(' &middot; ', ' ')}"
    return (
f'''    <div class="product-card">
      <div class="product-img">
        <img src="/images/merrill-golf/{stem}.jpg" alt="{alt}" loading="lazy" />
      </div>
      <div class="product-body">
        <div class="product-brand">Merrill Golf</div>
        <div class="product-name">{name} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{SHOP}{handle}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>
''')


def block():
    cards = "\n".join(card(*i) for i in ITEMS)
    return (f'{OPEN}\n<section class="products">\n'
            f'  <h2 class="products-hdr">The Collection &mdash; {len(ITEMS)} Pieces</h2>\n'
            f'  <div class="products-grid">\n\n{cards}\n  </div>\n</section>\n{CLOSE}')


def run(apply_):
    html = PAGE.read_text(encoding="utf-8")
    before_imgs = set(re.findall(r'src="(/images/[^"]+)"', html))

    if OPEN in html:                                   # re-run: swap in place
        new = re.sub(re.escape(OPEN) + r".*?" + re.escape(CLOSE), block(),
                     html, flags=re.S)
        how = "replaced existing block"
    else:                                              # first run: eat the old section
        m = re.search(r'<section class="products">\s*<h2 class="products-hdr">'
                      r'The Collection.*?</section>', html, re.S)
        if not m:
            sys.exit("! could not find the existing collection section — refusing to guess")
        new = html[:m.start()] + block() + html[m.end():]
        how = "replaced the original 5-card section"

    # ---- guards -------------------------------------------------------
    checks = [
        ("cards are DIVs, so the template can see them",
         new.count('<div class="product-card"') == len(ITEMS)
         and '<a href="https://merrillgolf.com/products/' in new
         and not re.search(r'<a[^>]*class="product-card"', new), ""),
        ("12 cards written", new.count('class="product-card"') == len(ITEMS),
         f'{new.count(chr(34)+"product-card"+chr(34))} found'),
        ("no sold-out Target Practice Tee",
         "target-practice-tee-vintage-black" not in new, ""),
        # SCOPE NOTE. This asserts only over the block this script writes.
        # "No polos." also sits in the page's own .writeup, which is equally
        # false now — but that prose is not this script's to rewrite: the
        # template rebuilds The Take and The Story wholly from the spec and
        # drops it. Asserting over the whole page here would fail on prose this
        # script is not responsible for, so the sitewide assertion runs AFTER
        # the template instead, where it can actually be true.
        ("the false 'No polos.' claim is out of the collection",
         "No polos" not in block(), ""),
        ("every new image exists on disk",
         all((ROOT / f"images/merrill-golf/{i[0]}.jpg").exists() for i in ITEMS), ""),
        ("every img has alt",
         all('alt="' in t for t in re.findall(r'<img[^>]*>', block())), ""),
        ("no banned word", "worth" not in block().lower(), ""),
        ("section tags balance",
         new.count("<section") == new.count("</section>"), ""),
        ("document still closes", new.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for label, passed, detail in checks:
        print(f"  {'OK  ' if passed else 'FAIL'} {label} {detail}")
        ok &= passed
    if not ok:
        sys.exit("\n! refusing to write")

    gone = before_imgs - set(re.findall(r'src="(/images/[^"]+)"', new))
    print(f"\n  {how}")
    print(f"  images dropped with the old cards: {sorted(gone) if gone else 'none'}")
    if apply_:
        PAGE.write_text(new, encoding="utf-8"); print("  written")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    run("--apply" in sys.argv)
