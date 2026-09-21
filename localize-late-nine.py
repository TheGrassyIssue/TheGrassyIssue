#!/usr/bin/env python3
"""localize-late-nine.py — imagery for the Late Nine Brand Revisited.
21 September 2026.

WHY THIS IS A REVISITED AND NOT A TOUCH-UP.

The existing page at /drops/late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf
is 287 words with one <h2>, and — the part that actually matters — it is
illustrated entirely with OTHER BRANDS' PHOTOGRAPHY:

    /images/malbon-fall/...     Malbon product shots
    /images/odd-ritual/...      Odd Ritual product shots
    /images/streetwear26/...    a mixed roundup folder
    /images/feed/...            generic feed imagery

There is no /images/late-nine/ directory at all. A brand page showing a
competitor's trousers is worse than a brand page with no pictures, so every
frame gets replaced here with Late Nine's own photography.

PRICES ARE SEK, AND THAT WAS VERIFIED, NOT ASSUMED.

products.json carries no currency field — prices are bare strings like
"2700.00". "Stockholm brand, therefore SEK" is areasonable guess and a
guess is not a source. So the rendered product page was read directly:

    late-nine.com/products/5-pocket-cords-navy  ->  "2 700 kr"
    products.json  5-pocket-cords-navy          ->  "2700.00"

and the market selector on that page shows "* Sweden (SEK)" as active. The
numbers are SEK. Nothing here is converted to USD; Late Nine ships to the US
DDP ($25 delivery, duties included) so the SEK figure is the real price.

Hypebeast quoted USD at launch (windbreaker $515, trousers $430, polos $275,
caps $70 — 7 Oct 2025). Those are a year-old debut-collection figure from a
different market and are NOT mixed with the SEK read below. If they appear on
the page at all they appear attributed to Hypebeast and dated.

THE CDN HASH TRAP. Shopify filenames carry ?v= version suffixes. They are
pasted from products.json, never retyped — three 404s on the Pants Edit came
from typing them out by hand.

Idempotent. Dry run by default.
"""
import io
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/late-nine"
ARCHIVE = ROOT / "research/late-nine/originals"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}

SQUARE = 1200          # house product square
MIN_SRC_W = 800

PRICE_READ_DATE = "21 September 2026"
CURRENCY = "SEK"

# slug, display name, price (SEK, from products.json, verified against the
# rendered page), avail/total variants, tag/drop, image URL.
#
# 18 picks, all with at least one variant in stock. The five fully sold-out
# products (Knit Crepe Polo in Dark Brown / Forest / Navy / Ivory, and the
# Ribbed Jersey Polo LS Brown Melange) are deliberately excluded — a pick
# nobody can buy is not a pick.
PICKS = [
    # THE FLEETWOOD PIECE. Skratch and The Old Ghosts both place a Late Nine
    # taupe ribbed polo on Tommy Fleetwood at the 2026 Masters. Down to one
    # variant of five, so it carries a thin-stock flag.
    ("ribbed-polo-taupe", "Ribbed Jersey Polo Taupe", 1800, 1, 5, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05339.jpg?v=1758662517"),

    ("instructors-jacket-cotton-navy", "Instructors Jacket Navy", 4350, 2, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/navy-jacket-02-front.jpg?v=1778141337"),
    ("quarter-zip-windbreaker-navy", "Quarter Zip Windbreaker Navy", 3750, 2, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Blue_QZ_1.jpg?v=1777618175"),
    ("quarter-zip-windbreaker-beige", "Quarter Zip Windbreaker Beige", 3750, 2, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Beige_QZ_1.jpg?v=1777618227"),

    # The FW26 drop — created 2 Sept 2026, the newest thing in the store and
    # the reason this Revisited has something to say.
    ("double-pleat-slacks-dark-brown", "Double Pleat Slacks Dark Brown", 3200, 4, 5, "FW26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Frame14_b02fb208-c820-4378-bce4-db34f9c4925c.jpg?v=1788938691"),
    ("double-pleat-slacks-dark-brown-copy", "Double Pleat Slacks Dark Navy", 3200, 3, 5, "FW26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Frame19.jpg?v=1788938633"),
    ("pleated-trousers-taupe", "Double Pleat Slacks Taupe", 3200, 4, 5, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/fejewnklkfenw.jpg?v=1789071984"),
    ("5-pocket-cords-navy", "5-Pocket Cords Navy", 2700, 4, 5, "FW26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Frame22.jpg?v=1788938749"),
    ("5-pocket-cords-cream", "5-Pocket Cords Cream", 2700, 3, 5, "FW26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Frame4.jpg?v=1788938808"),
    ("5-pocket-cords-olive", "5-Pocket Cords Olive", 2700, 3, 5, "FW26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Frame28.jpg?v=1788938844"),

    ("cable-knit-polo-burgundy", "Cable Knit Polo Burgundy", 2950, 2, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05822.jpg?v=1758662291"),
    ("cable-knit-polo-light-blue", "Cable Knit Polo Light Blue", 2950, 3, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05886.jpg?v=1758662327"),
    ("long-sleeve-polo-dark-brown", "Cable Knit Polo Dark Brown", 2950, 4, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05631.jpg?v=1758662417"),

    ("ribbed-vest-sage", "Ribbed Knit Vest Sage", 2450, 2, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05470.jpg?v=1758662074"),
    ("ribbed-vest-grey", "Ribbed Knit Vest Grey", 2450, 4, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05744.jpg?v=1758662204"),

    ("double-pleat-shorts-beige", "Double Pleat Shorts Beige", 2500, 4, 4, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Beige_shorts_1.jpg?v=1777618373"),

    ("sports-cap-burgundy", "Orbit Cap Burgundy", 500, 1, 1, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05901.jpg?v=1758747776"),
    ("90s-belt-brown", "Tipped Double Loop Belt Brown", 1400, 2, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Belt_2.jpg?v=1758749331"),
]

# A pick is flagged thin when stock is genuinely shallow. Same rule as the
# Pants Edit: available < total AND available <= 2.
def thin(avail, total):
    return avail < total and avail <= 2


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=90).read()


# Where the square is taken from, as a fraction of source height. 0.5 is a
# centre cut.
#
# THIS TABLE EXISTS BECAUSE THE FIRST PASS WAS WRONG. Every pick was cut dead
# centre, a contact sheet was rendered, and the Orbit Cap came back with the
# crown of the cap — the actual product — clipped off the top of the frame.
# Late Nine shoot full-length portraits at roughly 2:3, so where the garment
# sits in the frame depends entirely on what the garment is: a cap is at the
# top of a standing figure, trousers are at the bottom, a polo is in the
# middle. One global crop cannot serve all three. Same lesson as the Pants
# Edit, where a single 18% top-bias framed faces and cut the trousers at the
# knee.
#
# Anything not listed takes the 0.5 default, and that default is only trusted
# because the sheet was read frame by frame — not because plain backgrounds
# imply safe framing.
BIAS = {
    "sports-cap-burgundy": 0.22,   # headwear sits high; centre clipped the crown
    "sports-cap-brown":    0.22,
    "country-club-cap-white": 0.22,
    "country-club-cap-beige": 0.22,
    "90s-belt-brown":      0.42,   # belt sits just above centre on a full figure
    "90s-belt-black":      0.42,
    "loop-belt-brown-suede-silver": 0.42,
    "loop-belt-black-suede-silver": 0.42,
}

# ---------------------------------------------------------------------------
# THE CORE COLLECTION.
#
# "Core collection" is not a Late Nine term — there is no such collection on
# their site. What they do have is a taxonomy of recurring PRODUCT FAMILIES,
# visible in collections.json, and that is the honest reading of the idea:
#
#   Ribbed Jersey Polo (2)   Cable Knit Polo (3)   Knit Polo (5)
#   Ribbed Vest (3)          Quarter Zip (4)       Instructors Wool (2)
#   Slacks (5)               Double Pleats (2)     Five-Pocket (2)
#   Loop Belt (2)            90s belt (2)
#   Country Club Cap (3)     Sports Cap (2)
#
# The first eighteen picks covered most of those but missed FOUR families
# outright — Five-Pocket, Double Pleats (which is a different trouser from
# Slacks), Loop Belt (suede, not the tipped 90s belt) and Country Club Cap
# (the Twilight). Picking eighteen by eye across a flat 38-product list is
# how you miss a family: nothing in products.json says these are families,
# because product_type is an empty string on all 38 items. The structure only
# exists in the collections endpoint.
#
# Knit Crepe Polo Flax Yellow is included here because it is the last live
# colourway of a core family whose other four are sold out — and those four
# sit in Late Nine's "Coming Soon" collection, i.e. flagged for restock, not
# discontinued. Worth saying on the page rather than silently dropping them.
CORE = [
    ("five-pocket-chino-fawn", "Five-pocket Chino Fawn", 2700, 3, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/5-_Pocket_Beige_2.jpg?v=1776772276"),
    ("five-pocket-chino-navy", "Five-pocket Chino Navy", 2700, 3, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC08738.jpg?v=1776772453"),
    ("double-pleats-beige", "Double Pleat Trousers Beige", 2800, 2, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Pleat_Beige_1.jpg?v=1777618445"),
    ("double-pleats-white", "Double Pleat Trousers White", 2800, 1, 3, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC08816.jpg?v=1776772901"),
    ("country-club-cap-beige", "Twilight Cap Beige", 500, 1, 1, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05895.jpg?v=1758747869"),
    ("country-club-cap-white", "Twilight Cap White", 500, 1, 1, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05915.jpg?v=1758747850"),
    ("loop-belt-brown-suede-silver", "Loop Belt Brown Suede", 1400, 3, 4, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Brown_Belt_1.jpg?v=1777617626"),
    ("loop-belt-black-suede-silver", "Loop Belt Black Suede", 1400, 2, 4, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/Black_Belt_1.jpg?v=1777617735"),
    ("ribbed-polo-grey-mix", "Ribbed Jersey Polo Americano", 1800, 2, 5, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05548.jpg?v=1758662490"),
    ("knit-crepe-polo-flax-yellow", "Knit Crepe Polo Flax Yellow", 1800, 1, 5, "SS26",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC08683.jpg?v=1776775002"),
    ("ribbed-vest-dark-brown", "Ribbed Knit Vest Brown", 2450, 4, 4, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05602-StudioMiladAbedi-FullRes_be36e115-3f43-4377-8361-63ead3b52dc5.jpg?v=1758806085"),
    ("sports-cap-brown", "Orbit Cap Brown", 500, 1, 1, "FW25",
     "https://cdn.shopify.com/s/files/1/0848/3261/6716/files/DSC05899.jpg?v=1758747814"),
]

# Restocking, per Late Nine's own "Coming Soon" collection. Not picks — every
# variant is unavailable — but named on the page so a reader who wants the
# Knit Crepe knows it is returning rather than gone.
RESTOCKING = [
    ("Knit Crepe Polo Forest", 1800),
    ("Knit Crepe Polo Dark Brown", 1800),
    ("Knit Crepe Polo Navy", 1800),
    ("Knit Crepe Polo Ivory", 1800),
    ("Ribbed Jersey Polo LS Brown Melange", 2000),
]


def square(im, slug):
    """House 1200x1200 product square, biased per BIAS above."""
    s = min(im.size)
    cx = (im.width - s) // 2
    cy = round(im.height * BIAS.get(slug, 0.5)) - s // 2
    cy = max(0, min(im.height - s, cy))
    im = im.crop((cx, cy, cx + s, cy + s))
    return im.resize((SQUARE, SQUARE), Image.LANCZOS)


def main(apply_):
    global Image
    from PIL import Image

    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
        ARCHIVE.mkdir(parents=True, exist_ok=True)

    made, skipped, failed = [], [], []
    for slug, name, price, avail, total, drop, url in PICKS + CORE:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug); continue
        if not apply_:
            made.append((slug, f"would fetch {url.rsplit('/',1)[-1][:40]}")); continue
        try:
            raw = fetch(url)
            (ARCHIVE / f"{slug}.orig.jpg").write_bytes(raw)
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            if im.width < MIN_SRC_W:
                failed.append((slug, f"source only {im.width}px — would upscale"))
                continue
            square(im, slug).save(dest, "JPEG", quality=90, optimize=True)
            made.append((slug, f"{SQUARE}x{SQUARE} from {im.width}x{im.height}"))
        except Exception as e:
            failed.append((slug, str(e)[:110]))

    for s, d in made:   print(f"  ok    {s:38} {d}")
    for s in skipped:   print(f"  skip  {s:38} already local")
    for s, e in failed: print(f"  FAIL  {s:38} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — a grid with a hole in it is not a grid")

    if not apply_:
        print(f"\n  {len(PICKS)} picks — dry run, pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK, not this loop's bookkeeping ----
    bad = []
    want = {p[0] for p in PICKS + CORE}
    have = {f.stem for f in OUT.glob("*.jpg")}
    if want - have:
        bad.append(f"missing: {sorted(want - have)}")
    for slug, name, *_ in PICKS + CORE:
        f = OUT / f"{slug}.jpg"
        if not f.exists():
            continue
        im = Image.open(f)
        if (im.width, im.height) != (SQUARE, SQUARE):
            bad.append(f"{slug} is {im.width}x{im.height}, not {SQUARE}x{SQUARE}")
    # no pick may reuse another brand's folder — the bug this page has today
    for slug, *_ in PICKS + CORE:
        if not (OUT / f"{slug}.jpg").exists():
            bad.append(f"{slug} not in images/late-nine/")
    if len(PICKS) != 18:
        bad.append(f"{len(PICKS)} picks defined, the house grid is 18")
    allp = PICKS + CORE
    if len({p[0] for p in allp}) != len(allp):
        bad.append("a slug appears in both PICKS and CORE")
    if len({p[0] for p in PICKS}) != len(PICKS):
        bad.append("duplicate slug in PICKS")
    if len({p[0] for p in CORE}) != len(CORE):
        bad.append("duplicate slug in CORE")
    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  {len(PICKS)} picks + {len(CORE)} core at {SQUARE}x{SQUARE} in images/late-nine/")
    print(f"  originals archived to {ARCHIVE.relative_to(ROOT)}/")
    print(f"  prices are {CURRENCY}, read {PRICE_READ_DATE}, not converted")
    print(f"  thin stock: {[p[0] for p in PICKS if thin(p[3], p[4])]}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
