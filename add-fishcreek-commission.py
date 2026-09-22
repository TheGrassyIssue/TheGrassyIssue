#!/usr/bin/env python3
"""add-fishcreek-commission.py — two more belts for the Fish Creek section.
22 September 2026.

Lenny: "let's add two more belts to the Fish Creek section so each has three
belts", then chose the commission pair once the stock picture was clear.

WHY COMMISSION BELTS AND NOT TWO MORE FINISHED DESIGNS. Fish Creek's finished
rack is four belts and three of them are dead. Read on the rendered product
pages on 22 September 2026:

  Alabama Traditions  $150  Red available, Navy unavailable  (already in the post)
  Stars and Stripes   $150  all three sizes Unavailable
  Dream Cars          $150  all three sizes Unavailable
  Classic Maine       $150  all three sizes Unavailable
  The Hill School     $175  page title is literally "Private Listing" — a school
                            make-to-order with 31 sizes, not a catalogue item

So the section could not be filled to three with buyable finished designs. The
two commission belts are what Fish Creek actually sells, and they match the
section lede already on the page: "mostly a commission house — you send them the
thing you want stitched and they build it."

THE STOCK READING CAME FROM THE RENDERED PAGE, NOT THE HTML AND NOT THE JSON.
Fetching the raw product HTML returned identical numbers for three different
belts — 111 needlepoint mentions, 5 sold-out strings, the same availability —
because the theme inlines a site-wide blob. Identical counts across distinct
products is the tell that you are reading a template, not a product. The real
per-size state ("Pant Size 34 ... Unavailable") only appears once the page runs.

EVERY MARKETING GRAPHIC IS EXCLUDED BY HAVING LOOKED AT IT. Both products ship
instructional cards in the image array — "How It Works" panels on each, and a
"Pair with a Matching Key Fob!" banner on the Yachtsman. Taking the first four
images would have put a wall of instructional text in a product gallery. The
indices below were chosen off a rendered contact sheet.

Prices are $189.00 USD each, read from the product page on 22 September 2026.
Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import sys
import time
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
RES = ROOT / "research/needlepoint"
OUT = ROOT / "images/needlepoint"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
MINW, FRAME_W = 500, 1100

# slug, handle, title, image indices into the >=500px list (chosen by looking)
JOBS = [
    ("fish-creek-custom", "custom-needlepoint-belt", "Custom Needlepoint Belt",
     [4, 2, 5, 7]),
    ("fish-creek-bespoke-yachtsman", "bespoke-yachtsman-belt", "Bespoke Yachtsman Belt",
     [3, 7, 5, 1]),
]
# Neither is a size-in-stock product: one variant, 31 selectable lengths, built
# to order. "Made to order" is the honest stock string; a size count would be a
# category error.
STOCK = "Made to order"
PRICE = "$189.00"
BANNED = ("how_it_works", "pair_with")


def fetch(u, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return r if raw else json.loads(r)


def main(apply_):
    man = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
    items = json.loads((RES / "items.json").read_text(encoding="utf-8"))
    added = []

    for slug, handle, title, idx in JOBS:
        url = f"https://fishcreekbrands.com/products/{handle}"
        p = fetch(url + ".json")["product"]
        usable = [i for i in p["images"] if (i.get("width") or 0) >= MINW]
        if max(idx) >= len(usable):
            sys.exit(f"! {slug}: frame {max(idx)} requested, only {len(usable)} usable")
        frames = []
        for n, k in enumerate(idx):
            src = usable[k]["src"]
            if any(b in src.lower() for b in BANNED):
                sys.exit(f"! {slug}: frame {k} is a marketing graphic ({src.split('/')[-1]})")
            f = OUT / f"{slug}-{n}.jpg"
            if not f.is_file():
                g = Image.open(io.BytesIO(fetch(src, raw=True))).convert("RGB")
                w0, h0 = g.size
                tw = min(FRAME_W, w0)                      # never upscale
                g = g.resize((tw, round(h0 * tw / w0)), Image.LANCZOS)
                if apply_:
                    OUT.mkdir(parents=True, exist_ok=True)
                    g.save(f, "JPEG", quality=88, optimize=True, progressive=True)
            frames.append(f"/images/needlepoint/{f.name}")
        entry = dict(brand="Fish Creek", title=title, price=PRICE, stock=STOCK,
                     url=url, frames=frames, kind="belt")
        if slug in man and man[slug] == entry:
            print(f"  {slug}: unchanged")
        else:
            added.append(slug)
            print(f"  {slug}: {len(frames)} frames, {PRICE}, {STOCK}")
        man[slug] = entry
        if not any(i.get("url") == url for i in items):
            items.append(dict(kind="belt", brand="Fish Creek", title=title, price=PRICE,
                              stock=STOCK, url=url,
                              frames=[f.split("/")[-1] for f in frames]))
        time.sleep(0.6)

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY ON DISK ----
    bad = []
    seen = {}
    for slug, m in man.items():
        for rel in m["frames"]:
            f = ROOT / rel.lstrip("/")
            if not f.is_file():
                bad.append(f"{rel}: missing"); continue
            if Image.open(f).width < 400:
                bad.append(f"{rel}: too small")
            if rel in seen:
                bad.append(f"{rel} shared by {seen[rel]} and {slug}")
            seen[rel] = slug
    fc = [s for s, m in man.items() if m["brand"] == "Fish Creek" and m["kind"] == "belt"]
    if len(fc) != 3:
        bad.append(f"Fish Creek has {len(fc)} belts, expected 3")
    if bad:
        sys.exit("! " + "\n    ".join(bad))

    (RES / "manifest.json").write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    (RES / "items.json").write_text(json.dumps(items, indent=1) + "\n", encoding="utf-8")
    belts = sum(1 for m in man.values() if m["kind"] == "belt")
    print(f"\n  verified: Fish Creek at {len(fc)} belts, {belts} belts + "
          f"{len(man)-belts} fobs = {len(man)} products, {len(seen)} frames, none shared")


if __name__ == "__main__":
    main("--apply" in sys.argv)
