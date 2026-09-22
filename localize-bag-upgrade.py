#!/usr/bin/env python3
"""localize-bag-upgrade.py — pull imagery for the three-bag upgrade post.
22 September 2026.

Lenny: "post about upgrading your golf bag - 3 brands that are a step above",
naming Shapland, Shoal and Jones. Full house treatment, so 4 gallery frames per
bag.

FRAMES WERE CHOSEN BY LOOKING AT THEM, not by reading filenames — and on this
job that distinction mattered twice.

1. EVERY JONES FILE IS NAMED "Tennessee". The Texas Trouper's images come back
   as JonesSportsCo_Tennessee_Trouper_Moongray_*. Rendered, every one of them
   reads TEXAS and LONGHORNS in burnt orange with the longhorn silhouette. It is
   a vendor template name, not the wrong product. Had I trusted the filename I
   would have dropped a correct bag; had I trusted it the other way I could have
   shipped Tennessee on an Austin site. The two frames chosen here are the
   JSC_Texas_Studio pair, which are unambiguously the Texas shoot.

2. SHOPIFY'S PER-PRODUCT .json LIES ABOUT STOCK. It reported zero available
   variants for the Shoal Sage bag and the Texas Trouper; the product pages show
   both live (Shoal as preorder, Jones in stock). Stock in this post comes from
   the product page every time. Shapland is the reverse case and genuinely is
   sold out — 18-20 "Sold Out" strings per page, every variant false.

PRICES are read from og:price / JSON-LD on the product page with the currency
attached, never converted: Shapland Rye 4.0 $495 USD, Shoal Standard $450 USD,
Jones Texas Trouper $410 USD, all on 22 September 2026.

Output: 1400px-wide JPEGs under images/<brand>/. Downloaded, never hot-linked.
Idempotent — re-running reproduces the same files. Dry run by default.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
WIDE = 1400

# (brand dir, product .json, [(image index, output stem, alt)])
JOBS = [
    ("shapland", "https://shaplandbags.com/products/rye-4-0.json", [
        (0, "rye-4-group", "The Shapland Rye 4.0 in its full colour range, lined up on a fairway"),
        (1, "rye-4-navy", "The Shapland Rye 4.0 stand bag in navy, standing on a fairway"),
        (3, "rye-4-collar", "Top-down view of the Shapland Rye 4.0 collar and tan leather trim"),
        (7, "rye-4-blue", "The Shapland Rye 4.0 in light blue, stand legs deployed"),
    ]),
    ("shoal-golf", "https://shoalgolfco.com/products/the-shoal-standard-bag-preorder-sage.json", [
        (0, "standard-sage", "The Shoal Standard Bag in sage canvas, loaded and standing on a fairway"),
        (2, "standard-sage-legs", "The Shoal Standard Bag with its stand legs out"),
        (3, "standard-sage-angle", "The Shoal Standard Bag seen from the side on the course"),
        (1, "standard-sage-back", "The back and strap of the Shoal Standard Bag"),
    ]),
    ("jones-sports-co", "https://www.jonessportsco.com/products/texas-trouper-moon-gray.json", [
        (1, "texas-trouper-clubhouse", "The Jones Texas Trouper resting against a clubhouse bar"),
        (2, "texas-trouper-lockers", "The Jones Texas Trouper in front of a locker room bench"),
        (6, "texas-trouper-texas", "The Jones Texas Trouper laid flat, TEXAS across the panel"),
        (4, "texas-trouper-longhorns", "The Jones Texas Trouper laid flat, LONGHORNS across the panel"),
    ]),

    # --- second pass, 22 Sep: Lenny asked for three picks per brand ---
    # Shoal makes exactly one bag, so its three are colourways rather than
    # models. Lenny's call, made knowing that. Sage and White are the two live
    # from the August run; Navy is sold out and is in for colour separation.
    ("shapland", "https://shaplandbags.com/products/kantle-3-1.json", [
        (0, "kantle-31-a", "The Shapland Kantle 3.1 stand bag"),
        (1, "kantle-31-b", "The Shapland Kantle 3.1 from the side"),
        (2, "kantle-31-c", "The Shapland Kantle 3.1 with its stand legs out"),
        # Index 3 is the NAVY colourway while 0-2 are cream — a gallery that
        # changes colour halfway reads as a mistake. 8 is the cream detail.
        (8, "kantle-31-d", "Detail of the Shapland Kantle 3.1 fabric and clasp"),
    ]),
    ("shapland", "https://shaplandbags.com/products/sunday-3-1.json", [
        (0, "sunday-31-a", "The Shapland Sunday 3.1 carry bag"),
        (1, "sunday-31-b", "The Shapland Sunday 3.1 from the side"),
        (2, "sunday-31-c", "The Shapland Sunday 3.1 on a fairway"),
    ]),
    ("shoal-golf", "https://shoalgolfco.com/products/the-shoal-standard-bag-preorder-white.json", [
        # Only four frames exist and index 1 has the bag lying flat on the
        # grass, which is a weak lead. Reordered so it comes last.
        (2, "standard-white", "The Shoal Standard Bag in white canvas, stand legs out"),
        (0, "standard-white-b", "The Shoal Standard Bag in white on the course"),
        (3, "standard-white-c", "The Shoal Standard Bag in white, further down the hole"),
        (1, "standard-white-d", "The Shoal Standard Bag in white, laid on the grass"),
    ]),
    ("shoal-golf", "https://shoalgolfco.com/products/the-shoal-standard-navy-bag.json", [
        (0, "standard-navy", "The Shoal Standard Bag in navy canvas"),
        (1, "standard-navy-b", "The Shoal Standard Bag in navy, side view"),
        (2, "standard-navy-c", "The Shoal Standard Bag in navy with stand legs out"),
        (3, "standard-navy-d", "The Shoal Standard Bag in navy on the course"),
    ]),
    ("jones-sports-co", "https://www.jonessportsco.com/products/utility-x-olive.json", [
        (0, "utility-x-a", "The Jones Utility X stand bag in olive"),
        (1, "utility-x-b", "The Jones Utility X from the side"),
        (2, "utility-x-c", "The Jones Utility X with stand legs out"),
        (3, "utility-x-d", "Detail of the Jones Utility X pockets"),
    ]),
    ("jones-sports-co", "https://www.jonessportsco.com/products/original-jones-bag-navy-white.json", [
        # Index 1 is a golfer actually carrying it up a fairway — the only
        # lifestyle frame in the set, so it leads.
        (1, "original-jones-a", "A golfer carrying the Original Jones Bag up a fairway"),
        (0, "original-jones-b", "The Original Jones Bag in navy and white with its strap"),
        (2, "original-jones-c", "The Original Jones Bag single strap"),
        (3, "original-jones-d", "Detail of the Original Jones Bag panel"),
    ]),
]


def fetch(u, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return r if raw else json.loads(r)


def main(apply_):
    wrote, bad = [], []
    for brand, purl, frames in JOBS:
        p = fetch(purl)["product"]
        imgs = p.get("images", [])
        out = ROOT / "images" / brand
        print(f"\n  {brand}: {p['title']} — {len(imgs)} source frames")
        for idx, stem, alt in frames:
            if idx >= len(imgs):
                bad.append(f"{brand}: no frame {idx} (only {len(imgs)})")
                continue
            src = imgs[idx]["src"]
            im = Image.open(io.BytesIO(fetch(src, raw=True))).convert("RGB")
            w0, h0 = im.size
            target = min(WIDE, w0)          # never upscale
            im = im.resize((target, round(h0 * target / w0)), Image.LANCZOS)
            f = out / f"{stem}.jpg"
            print(f"     {stem:<26} {w0}x{h0} -> {im.size[0]}x{im.size[1]}  {src.split('/')[-1][:44]}")
            if apply_:
                out.mkdir(parents=True, exist_ok=True)
                im.save(f, "JPEG", quality=88, optimize=True, progressive=True)
            wrote.append((f, alt))

    if bad:
        sys.exit("! " + "; ".join(bad))
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK ----
    probs = []
    for f, alt in wrote:
        if not f.is_file():
            probs.append(f"{f.name}: missing"); continue
        im = Image.open(f)
        if im.width > WIDE:
            probs.append(f"{f.name}: {im.width}px wider than {WIDE}")
        if f.stat().st_size > 900_000:
            probs.append(f"{f.name}: {f.stat().st_size/1024:.0f} KB is heavy")
        if im.width < 600:
            probs.append(f"{f.name}: only {im.width}px wide, too small for a gallery frame")
    if probs:
        sys.exit("! " + "\n    ".join(probs))

    alts = ROOT / "images/bag-upgrade-alts.json"
    alts.write_text(json.dumps({f.relative_to(ROOT).as_posix(): a for f, a in wrote},
                               indent=1) + "\n", encoding="utf-8")
    print(f"\n  verified: {len(wrote)} frames on disk, none upscaled, alt text in "
          f"{alts.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
