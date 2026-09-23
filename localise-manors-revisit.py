#!/usr/bin/env python3
"""localise-manors-revisit.py — pull every image the Manors Revisited refresh
needs onto disk, then render a contact sheet so the frames can be CHOSEN BY
LOOKING rather than by index. 22 September 2026.

Lenny: "do 6 from new collection and 9 from core collection ... Pull lookbook
and blog images. They have the best social media production in golf."

TWO SOURCES, TWO SHAPES.

  Products come from the Shopify catalogue already captured in
  research/manors/catalogue.json. Up to four frames each, downloaded at full
  size and resized down to 1400px wide, never up.

  Editorial comes from the brand's Sanity CMS, catalogued in
  research/manors/editorial-images.json. Those originals are 4000x5000, so they
  are requested at ?w=1600 rather than pulled whole.

NOTHING IS HOT-LINKED. Every file lands in images/manors/ and the page points
at the local copy. This is the standing rule and it is also why the ig-grid on
the existing page still renders after the brand reshuffled its CDN.

THE CONTACT SHEET IS THE POINT OF THE SCRIPT. Picking frame [0] for fifteen
products reliably produces a grid with a size chart in it, or the same flat
packshot fifteen times. This writes research/manors/contact-*.jpg for a human
(or Claude) to look at before the page build chooses indices. The build script
carries the chosen indices; this one only fetches and shows.

Idempotent — files already on disk are not re-fetched. Dry run by default.
"""
import io
import json
import pathlib
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
IMGDIR = ROOT / "images/manors"
RESEARCH = ROOT / "research/manors"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
WIDE = 1400
MAXFRAMES = 4

# handle -> local stem. Handles come from the catalogue, never from the title:
# "Lightweight Pleated Trouser" lives at /products/greenskeeper-chino-trousers.
NEW_DROP = [
    ("merino-tech-hoodie", "new-merino-hoodie"),
    ("ripstop-tech-vest", "new-ripstop-vest"),
    ("heritage-primaloft®-cardigan", "new-primaloft-cardigan"),
    ("1-4-zip-primaloft®-mid-layer", "new-primaloft-quarterzip"),
    ("ripstop-tech-trouser", "new-ripstop-trouser"),
    ("mockneck-ranger-polo", "new-ranger-mockneck"),
]
CORE = [
    ("greenskeeper-chino-trousers", "core-pleated-trouser"),
    ("recycled-greenskeeper-shorts", "core-greenskeeper-short"),
    ("insulated-course-gilet", "core-course-gilet"),
    ("highland-mockneck-fleece", "core-highland-fleece"),
    ("track-jacket", "core-ranger-jacket"),
    ("arc-polo", "core-arc-polo"),
    ("course-polo", "core-course-polo"),
    ("manors-logo-t-shirt", "core-logo-tee"),
    ("retro-crown-cap", "core-retro-crown-cap"),
]
PRODUCTS = NEW_DROP + CORE

# Editorial frames for the "In the Wild" grid, chosen off a rendered sheet of
# every non-lookbook Sanity image (journal, homepage, about). Indices into that
# pool are meaningless outside the run that produced them, so the IDs are
# recorded here instead.
WILD = [
    ("wild-clifftop", "coastal clifftop tee shot, sea stack on the horizon"),
    ("wild-flag", "MANORS back print, pulling the pin"),
    ("wild-pileon", "four players piling on each other on the fairway"),
    ("wild-desert", "desert round, red rock buttes behind"),
    ("wild-wall", "pink wall, hands on head, somewhere warm"),
    ("wild-clubhouse", "the full crew, indoors"),
]


def get(url, timeout=60):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=timeout).read()


def save(raw, dest, wide=WIDE):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    tw = min(wide, w)                      # never upscale
    if tw != w:
        im = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
    return im.size


def fetch_products(apply_):
    cat = {p["handle"]: p for p in
           json.loads((RESEARCH / "catalogue.json").read_text())["products"]}
    got = {}
    for handle, stem in PRODUCTS:
        p = cat.get(handle)
        if p is None:
            sys.exit(f"! {handle} is not in the captured catalogue")
        srcs = p["images"][:MAXFRAMES]
        if not srcs:
            sys.exit(f"! {handle} has no images in the catalogue")
        paths = []
        for n, src in enumerate(srcs):
            f = IMGDIR / (f"{stem}.jpg" if n == 0 else f"{stem}-a{n+1}.jpg")
            if not f.is_file():
                if apply_:
                    save(get(src), f)
                else:
                    f = None
            paths.append(f)
        got[stem] = [x for x in paths if x]
        print(f"  {stem:<28}{len(srcs)} frames  {p['title']}")
    return got


def fetch_wild(apply_, ids):
    """ids: [sanity-url] in WILD order, passed in from the chooser run."""
    out = []
    for (stem, _), url in zip(WILD, ids):
        f = IMGDIR / f"{stem}.jpg"
        if not f.is_file() and apply_:
            save(get(url + "?w=1600"), f, wide=1600)
        out.append(f)
        print(f"  {stem:<28}{url.rsplit('/', 1)[-1][:28]}")
    return out


def sheet(files, dest, cell=300, cols=6):
    """Contact sheet of whatever is on disk, numbered, for looking at."""
    files = [f for f in files if f and f.is_file()]
    if not files:
        print("  (nothing on disk yet — run with --apply first)")
        return
    rows = (len(files) + cols - 1) // cols
    out = Image.new("RGB", (cols * cell, rows * cell), (240, 240, 238))
    dr = ImageDraw.Draw(out)
    for n, f in enumerate(files):
        im = Image.open(f)
        im.thumbnail((cell - 8, cell - 8))
        x, y = (n % cols) * cell + 4, (n // cols) * cell + 4
        out.paste(im, (x, y))
        dr.rectangle([x, y, x + 150, y + 15], fill=(0, 0, 0))
        dr.text((x + 3, y + 3), f.stem[:26], fill=(255, 255, 255))
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=82)
    print(f"  contact sheet -> {dest.relative_to(ROOT)}  {out.size[0]}x{out.size[1]}")


def main(apply_, wild_ids):
    print("PRODUCTS")
    got = fetch_products(apply_)
    print("\nEDITORIAL")
    wild = fetch_wild(apply_, wild_ids) if wild_ids else []

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY ----
    bad = []
    for handle, stem in PRODUCTS:
        n = len(got.get(stem, []))
        if n < 2:
            bad.append(f"{stem}: only {n} frames on disk, need at least 2")
        for f in got.get(stem, []):
            if not f.is_file() or f.stat().st_size < 8000:
                bad.append(f"{f.name}: missing or suspiciously small")
            else:
                w, h = Image.open(f).size
                if w < 600:
                    bad.append(f"{f.name}: {w}px wide, too small to use")
    for f in wild:
        if not f.is_file():
            bad.append(f"{f.name}: editorial frame missing")
    if bad:
        sys.exit("! " + "\n    ".join(bad))

    flat = [f for _, stem in PRODUCTS for f in got[stem]]
    sheet(flat, RESEARCH / "contact-products.jpg")
    sheet(wild, RESEARCH / "contact-wild.jpg", cell=420, cols=3)
    print(f"\n  {len(flat)} product frames + {len(wild)} editorial frames in "
          f"{IMGDIR.relative_to(ROOT)}")
    print("  LOOK AT THE CONTACT SHEETS before the build picks lead frames.")


if __name__ == "__main__":
    ids = []
    p = RESEARCH / "wild-picks.json"
    if p.is_file():
        ids = json.loads(p.read_text())
    main("--apply" in sys.argv, ids)
