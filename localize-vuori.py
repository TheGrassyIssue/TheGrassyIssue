#!/usr/bin/env python3
"""localize-vuori.py — imagery for the Vuori Brand to Know. 21 September 2026.

SIZES (house)
  products : 1200x1200           -> images/vuori/<slug>.jpg
  masthead : 1405x602 (21:9)     -> images/vuori/hero.jpg   (see note below)
  body band: 1400w, native shape -> images/vuori/body-1.jpg

URLS ARE READ, NOT RETYPED. Every product URL comes out of
research/btk/vuori-candidates.json, which was written straight from the
browser harvest. Shopify filenames carry random hash suffixes
(..._308dd8db-05cd-4591-8e4b-1c4b03dc516d.png); three 404s on the Pants Edit
came from typing those out by hand. Nothing here is typed by hand.

WHICH PICTURE GETS WHICH JOB — AND THE FIRST ANSWER WAS WRONG.

First pass put the FA26 Mallorca clifftop frame (2000x2500) in the masthead,
reasoning that it was the only source big enough to yield a 21:9 crop of real
pixels at the house 1800px width. That reasoning was about resolution and
ignored composition. The result, on the contact sheet: a 21:9 slice across a
standing man's chest, head cropped off above the frame. Exactly the failure
tgi_bands.py was written to stop, relocated from the body to the masthead. A
portrait of a person does not become a landscape by cropping it.

So the jobs swap:

  masthead  <- the golf PLP banner: four players walking a ridgeline with
               carry bags. Already a landscape, already composed wide, and
               about as close to this publication's subject as a campaign
               image gets. Native 2882x602, so a true 21:9 crop is 1405x602.
  body band <- the Mallorca portrait, kept at its native 4:5 and set 1400
               wide. Uncropped, whole figure, .is-port measure.

THE MASTHEAD IS 1405px WIDE, NOT THE HOUSE 1800. That is deliberate. 1405x602
is every real pixel Vuori published in that frame at 21:9; reaching 1800 would
mean generating 28% of the image. A masthead that is slightly soft on a retina
screen is a smaller problem than a masthead that is partly invented, so the
no-upscale guard stays absolute and the width floats. HERO_MAX_W caps it where
a source is generous.

The banner carries a small "Tom Holland" caption bottom-right, which is Vuori's
campaign furniture and has no business in a TGI masthead. HERO_X_BIAS crops
left — which is where the four walkers are anyway — and drops it.

Nothing is upscaled anywhere. The verify block below proves it against the
archived originals rather than trusting this comment.

PRICES ARE USD, AND THAT WAS CHECKED. vuoriclothing.com blocks products.json
store-wide, so prices were read from the rendered collection tiles, then the
currency was confirmed against a product page's schema.org offer:

    /products/aim-trouser-athletic-slim-fit-30-khaki-linen-texture
    "priceCurrency":"USD"   "price":98      tile: $98

Watch out on a Vuori PDP: it also prints $75 (free-shipping threshold) and
$24.50 (an instalment figure). Neither is the price.

Idempotent — skips any file already written. Dry run by default.
"""
import io
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/vuori"
ARCHIVE = ROOT / "research/vuori/originals"
SPEC = ROOT / "research/btk/vuori-candidates.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}

SQUARE = 1200
HERO_RATIO = 21 / 9
HERO_MAX_W = 1800                   # cap, not a target — never reached by upscaling
BAND_W = 1400
MIN_SRC_W = 800

PRICE_READ_DATE = "21 September 2026"
CURRENCY = "USD"

# slug for each candidate n, in the order Lenny approved the grid.
SLUGS = {
    1: "aim-trouser",            2: "aim-short",
    3: "strato-tech-polo",       4: "torrey-golf-polo",
    5: "gamepoint-polo",         6: "ace-polo",
    7: "ponto-half-zip-mock",    8: "terrain-jacket",
    9: "sunday-insulated-vest", 10: "venture-quarter-zip",
    11: "kore-short",           12: "ponto-performance-pant",
    13: "strato-tech-tee",      14: "ponto-jogger",
    15: "seaside-hoodie",       16: "waffle-henley",
    17: "meta-trouser",         18: "vintage-jean",
}

# Vuori shoots full-length on seamless, so a centred square crop of a TROUSER
# shot lands on the model's knees. Bias is the fraction of image height the
# crop centres on: lower number = higher up the frame.
BIAS = {
    "aim-trouser": 0.40, "meta-trouser": 0.40, "vintage-jean": 0.40,
    "ponto-performance-pant": 0.40, "ponto-jogger": 0.40,
    "aim-short": 0.44, "kore-short": 0.44,
    "strato-tech-polo": 0.30, "torrey-golf-polo": 0.30, "gamepoint-polo": 0.30,
    "ace-polo": 0.30, "strato-tech-tee": 0.30, "waffle-henley": 0.30,
    "ponto-half-zip-mock": 0.30, "terrain-jacket": 0.32,
    "sunday-insulated-vest": 0.38, "venture-quarter-zip": 0.30,
    "seaside-hoodie": 0.32,
}

# The two campaign frames. Both are Vuori's own photography.
HERO_URL = ("https://cdn.bfldr.com/JUZN72U0/at/gvkf2qr9cfwf3nmj8tw85j/"
            "0511_SP26_Tom_Holland_Golf_Collection_PLP_Banner_Desktop.png")
HERO_X_BIAS = 0.34      # centre the crop on the walkers; drops the campaign caption

BAND_URL = ("https://cdn.shopify.com/s/files/1/0022/4008/6074/files/"
            "FA26_LOOK027_M_MATTHEW_SPROUT_MALLORCA_00086.png?width=2000")


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                  timeout=60).read()


def square(im, slug):
    s = min(im.size)
    cx = (im.width - s) // 2
    cy = round(im.height * BIAS.get(slug, 0.5)) - s // 2
    cy = max(0, min(im.height - s, cy))
    return im.crop((cx, cy, cx + s, cy + s)).resize((SQUARE, SQUARE), Image.LANCZOS)


def hero_crop(im):
    """Largest true-resolution 21:9 crop, capped at HERO_MAX_W. Never upscaled.

    A source wider than 21:9 (the banner) is cropped horizontally, biased by
    HERO_X_BIAS. A source taller than 21:9 is cropped vertically — but see the
    docstring: that path produces a decapitated portrait and no longer has a
    caller here. It is kept honest rather than deleted, because a future brand
    may only publish a tall frame.
    """
    if im.width / im.height > HERO_RATIO:
        tw = round(im.height * HERO_RATIO)
        cx = round((im.width - tw) * HERO_X_BIAS)
        cx = max(0, min(im.width - tw, cx))
        im = im.crop((cx, 0, cx + tw, im.height))
    else:
        th = round(im.width / HERO_RATIO)
        cy = max(0, (im.height - th) // 2)
        im = im.crop((0, cy, im.width, cy + th))
    if im.width > HERO_MAX_W:                       # only ever shrink
        im = im.resize((HERO_MAX_W, round(HERO_MAX_W / HERO_RATIO)), Image.LANCZOS)
    return im


def band_resize(im):
    """Native shape, 1400 wide. No crop at all — that is the point of a band."""
    if im.width < BAND_W:
        sys.exit(f"! band source is {im.width}px wide; {BAND_W} would be an upscale")
    h = round(im.height * BAND_W / im.width)
    return im.resize((BAND_W, h), Image.LANCZOS)


def main(apply_):
    global Image
    from PIL import Image

    rows = json.loads(SPEC.read_text(encoding="utf-8"))["candidates"]
    if len(rows) != 18:
        sys.exit(f"! spec holds {len(rows)} candidates, the house grid is 18")
    if set(SLUGS) != {r["n"] for r in rows}:
        sys.exit("! SLUGS and the candidate numbers disagree")

    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
        ARCHIVE.mkdir(parents=True, exist_ok=True)

    jobs = [(SLUGS[r["n"]], r["img"], "square") for r in rows]
    jobs += [("hero", HERO_URL, "hero"), ("body-1", BAND_URL, "band")]

    made, skipped, failed = [], [], []
    for slug, url, kind in jobs:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug); continue
        if not apply_:
            made.append((slug, f"would fetch {url.rsplit('/', 1)[-1][:46]}")); continue
        try:
            raw = fetch(url)
            (ARCHIVE / f"{slug}.orig").write_bytes(raw)
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            src = f"{im.width}x{im.height}"
            if im.width < MIN_SRC_W:
                failed.append((slug, f"source only {im.width}px — would upscale"))
                continue
            out = (square(im, slug) if kind == "square"
                   else hero_crop(im) if kind == "hero" else band_resize(im))
            out.save(dest, "JPEG", quality=90, optimize=True)
            made.append((slug, f"{out.width}x{out.height} from {src}"))
        except Exception as e:
            failed.append((slug, str(e)[:110]))

    for s, d in made:   print(f"  ok    {s:26} {d}")
    for s in skipped:   print(f"  skip  {s:26} already local")
    for s, e in failed: print(f"  FAIL  {s:26} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — a grid with a hole in it is not a grid")
    if not apply_:
        print(f"\n  {len(jobs)} images — dry run, pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK, not this loop's bookkeeping ----
    bad = []
    want = set(SLUGS.values()) | {"hero", "body-1"}
    have = {f.stem for f in OUT.glob("*.jpg")}
    if want - have:
        bad.append(f"missing: {sorted(want - have)}")
    for slug in SLUGS.values():
        f = OUT / f"{slug}.jpg"
        if f.exists():
            im = Image.open(f)
            if (im.width, im.height) != (SQUARE, SQUARE):
                bad.append(f"{slug} is {im.width}x{im.height}, not {SQUARE}x{SQUARE}")
    h = Image.open(OUT / "hero.jpg")
    if abs(h.width / h.height - HERO_RATIO) > 0.01:
        bad.append(f"hero ratio is {h.width / h.height:.3f}, not 21:9")
    if h.width > HERO_MAX_W:
        bad.append(f"hero is {h.width}px wide, over the {HERO_MAX_W} cap")
    b = Image.open(OUT / "body-1.jpg")
    if b.width != BAND_W:
        bad.append(f"band is {b.width}px wide, not {BAND_W}")

    # NO UPSCALING, checked against the archived originals rather than asserted
    for slug in want:
        orig = ARCHIVE / f"{slug}.orig"
        if not orig.exists():
            continue
        o = Image.open(orig)
        f = Image.open(OUT / f"{slug}.jpg")
        if f.width > o.width or f.height > o.height:
            bad.append(f"{slug} upscaled: {o.width}x{o.height} -> {f.width}x{f.height}")

    if len(SLUGS) != 18:
        bad.append(f"{len(SLUGS)} slugs, the house grid is 18")
    if len(set(SLUGS.values())) != len(SLUGS):
        bad.append("duplicate slug")
    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  18 products at {SQUARE}x{SQUARE}, hero {h.width}x{h.height}, "
          f"band {b.width}x{b.height} in images/vuori/")
    print(f"  originals archived to {ARCHIVE.relative_to(ROOT)}/")
    print(f"  prices are {CURRENCY}, read {PRICE_READ_DATE}, not converted")


if __name__ == "__main__":
    main("--apply" in sys.argv)
