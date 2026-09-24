#!/usr/bin/env python3
"""collect-galvin.py — verified product data and imagery for the Galvin Green
Brand to Know. 24 September 2026.

Lenny: "Let's do a brand to know - galvingreen.com. it will get cold and wet in
Austin eventually", then "let's focus more on the transitional weather - no
parkas, heavy duty stuff", "also add some tees or polos", and "add the core
collection, a section about normal everyday wearables."

CURRENCY WAS CHECKED, NOT ASSUMED. products.json, /products/<h>.js and the
rendered product page all read $99 for the same item on 24 Sep 2026, so this
store's base currency really is USD — unlike Manors, where products.json
returned GBP while the storefront showed dollars.

ONE COLOURWAY PER MODEL, AND IT IS ONE THAT IS IN STOCK. Galvin Green lists
every colourway as its own product (1,250 listings, 288 men's models), so each
pick names the model and this resolves it to the first colourway with at least
one size available, re-read live at collection time.

Downloads to images/galvin-green/, never hot-links. Writes
research/galvin/picks.json. Dry run by default.
"""
import io
import json
import pathlib
import re
import sys
import time
import urllib.request

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
RAW = pathlib.Path("/tmp/gg_raw.json")
IMGDIR = ROOT / "images/galvin-green"
OUT = ROOT / "research/galvin/picks.json"
HOST = "https://www.galvingreen.com"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
WIDE, FRAMES, PAUSE = 1400, 4, 1.2

# (group, model name) — group order is page order
PICKS = [
    ("polo", "Marty"), ("polo", "Muir"), ("polo", "Mulligan"), ("polo", "Medley"),
    ("wind", "Luis"), ("wind", "Lawrence"), ("wind", "Larry"), ("wind", "Leo"),
    ("wind", "Lane"), ("wind", "Lloyd"),
    ("mid", "Dixon"), ("mid", "Daxton"), ("mid", "Del"), ("mid", "Dean"),
    # Aden and Armstrong (GORE-TEX Paclite) were the first picks and are down to
    # ONE size in every colourway on 24 Sep — the packable line has sold through.
    # Replaced with the two lightweight shells that still have a full run.
    ("rain", "Adam"), ("rain", "Aston"), ("rain", "Air"),
    ("core", "Noah"), ("core", "Nixon"), ("core", "Paul"), ("core", "Pedro"),
    ("core", "Donnie"), ("core", "Danby"), ("core", "Carl"),
    # Chester dropped: two sizes left in its best colourway.
]


def get(url, t=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()


def resolve(raw, name):
    """The men's colourway of this model with the MOST sizes in stock.

    The first version took the first in-stock colourway it met, and four picks
    (Aden, Armstrong, Daxton, Nixon) came back with a single size left — a link
    to a colourway that will be gone within days. The widest size run is the
    one a reader can actually buy. Ties go to the lower price.
    """
    best = None
    for p in raw:
        if p["title"].split(" - ")[0].strip() != name:
            continue
        blob = (p["title"] + " " + " ".join(p.get("tags", []))).upper()
        if re.search(r"\bWOMEN|\bLADIES|JUNIOR", blob):
            continue
        n = sum(1 for v in p["variants"] if v.get("available"))
        if not n:
            continue
        key = (n, -float(p["variants"][0]["price"]))
        if best is None or key > best[0]:
            best = (key, p["handle"])
    return best[1] if best else None


def main(apply_):
    raw = json.loads(RAW.read_text())
    rows, bad = [], []
    for group, name in PICKS:
        h = resolve(raw, name)
        if not h:
            bad.append(f"{name}: no in-stock colourway")
            continue
        try:
            p = json.loads(get(f"{HOST}/products/{h}.js"))
        except Exception as e:
            bad.append(f"{name}: {e}")
            continue
        sizes = [v["title"] for v in p["variants"] if v.get("available")]
        colour = p["title"].split(" - ")[-1] if p["title"].count(" - ") >= 2 else ""
        body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", p.get("description") or "")).strip()
        imgs = ["https:" + i if i.startswith("//") else i for i in (p.get("images") or [])]
        rows.append({"group": group, "name": name, "title": p["title"], "handle": h,
                     "url": f"{HOST}/products/{h}", "usd": p["price"] / 100,
                     "in_stock": bool(p.get("available")), "sizes": sizes,
                     "desc": body, "imgs": imgs[:FRAMES], "type": p.get("type")})
        print(f"  {group:<5}{name:<10}${p['price']/100:>6.0f}  {len(sizes)} sizes  "
              f"{len(imgs)}img  {p['title'][:52]}")
        time.sleep(PAUSE)
    if bad:
        print("\n  PROBLEMS:\n    " + "\n    ".join(bad))
    if len(rows) != len(PICKS):
        sys.exit(f"! {len(PICKS)-len(rows)} pick(s) unresolved")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    for r in rows:
        r["local"] = []
        for n, src in enumerate(r["imgs"]):
            stem = r["name"].lower()
            f = IMGDIR / (f"{stem}.jpg" if n == 0 else f"{stem}-a{n+1}.jpg")
            if not f.is_file():
                im = Image.open(io.BytesIO(get(src))).convert("RGB")
                w, hgt = im.size
                if w > WIDE:
                    im = im.resize((WIDE, round(hgt * WIDE / w)), Image.LANCZOS)
                IMGDIR.mkdir(parents=True, exist_ok=True)
                im.save(f, "JPEG", quality=86, optimize=True, progressive=True)
                time.sleep(0.3)
            r["local"].append(f"/images/galvin-green/{f.name}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"_read": "24 September 2026", "_currency": "USD, "
                               "verified three ways", "products": rows}, indent=1))
    files = [ROOT / p.lstrip("/") for r in rows for p in r["local"]]
    cell, cols = 260, 8
    sheet = Image.new("RGB", (cols * cell, ((len(files) + cols - 1) // cols) * cell), (240, 240, 238))
    dr = ImageDraw.Draw(sheet)
    for n, f in enumerate(files):
        im = Image.open(f); im.thumbnail((cell - 6, cell - 6))
        x, y = (n % cols) * cell + 3, (n // cols) * cell + 3
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + 110, y + 14], fill=(0, 0, 0))
        dr.text((x + 3, y + 2), f.stem[:18], fill=(255, 255, 255))
    sheet.save(ROOT / "research/galvin/contact.jpg", quality=80)
    print(f"\n  {len(files)} frames -> images/galvin-green/  contact sheet written")


if __name__ == "__main__":
    main("--apply" in sys.argv)
