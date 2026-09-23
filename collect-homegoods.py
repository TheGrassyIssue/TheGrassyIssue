#!/usr/bin/env python3
"""collect-homegoods.py — gather verified product data and imagery for the
Home Golf Decor Edit rebuild. 22 September 2026.

Lenny: "less booze stuff, more design forward items ... Gumtree has good stuff,
malbon, sentinel does a putting mat, but keep that bag stand", then "any other
homes goods type items from our brand universe?", then the Foray stash book and
"also maybe some coffee table books".

TWELVE STORES, TWO PLATFORMS, ONE POLITE THREAD. Shopify answers
/products/<handle>.js; Squarespace answers /shop?format=json and carries stock
in qtyInStock. An earlier sweep hit 322 domains on twelve threads and every
request came back 429 for the next several minutes, so this goes one at a time
with a pause between hosts. Slower is the point.

PRICES AND STOCK ARE READ, NOT REMEMBERED. Two figures on the current page are
already wrong: Assouline's Impossible Collection is $1,400, not the $945 the
post prints. Everything below is whatever the store said on the read date, and
the build refuses to run if a price here disagrees with what it writes.

SOLD OUT IS A NUMBER, NOT A WORD. Shopify prints "sold out" whenever any single
variant is gone, which fired on a Gumtree product with 24 units on the shelf.
Availability comes from variants[].available / qtyInStock only.

TWO DELIBERATE SOLD-OUT ENTRIES. The Park Golf Stand ("keep the stand for the
bag, they will restock soon") and the Sugarloaf milk glass mugs ("add those
mugs from sugarloaf"). Both read OutOfStock and are in the post anyway at
Lenny's instruction; both are flagged in the data so the page can say so
rather than pretend.

Writes research/homegoods/picks.json + images/home-golf-decor/. Dry run default.
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
IMGDIR = ROOT / "images/home-golf-decor"
OUT = ROOT / "research/homegoods/picks.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
WIDE, MAXFRAMES, PAUSE = 1400, 4, 1.5

# (stem, brand, shopify|squarespace, host, handle-or-path, expected USD)
PICKS = [
    # --- objects for the room ---
    # Sentinel's Squarespace handles are all mutations of an unrelated product
    # ("no-16-basket-galvanized-..."), so every path here came out of the shop
    # index by title. Guessing a readable slug returned 404 on all three.
    ("chair-sentinel", "Sentinel", "sq", "sentinelgolf.us",
     "/shop/p/no-16-basket-galvanized-76zkc-bj2ct-xf4dn-x8w8x-3ddk7-mjerl", 480),
    ("poster-mogshade", "Mogshade", "sh", "mogshadegolf.com",
     "wool-poster-trio", 890),
    ("stand-park", "Park Golf Goods", "sq", "parkgolfgoods.com",
     "/shop/p/park-golf-stand-9n76h", 175),
    ("chair-sugarloaf", "Sugarloaf Social Club", "sh", "sugarloafsocialclub.com",
     "hidden-gem-crazy-creek-chair", 75),
    ("vase-foray", "Foray Golf", "sh", "foraygolf.com",
     "vintage-golfer-bobble-head-vase", 75),
    ("incense-quiet", "Quiet Golf", "sh", "quietgolf.com",
     "quiet-please-incense-holder", 25),
    # --- desk & shelf ---
    # the Natural colourway is out; Black is the one in stock
    ("yardage-bluegrass", "Bluegrass Fairway", "sh", "bluegrassfairway.com",
     "premium-italian-buttero-leather-golf-scorecard-holder-yardage-book-cover-black", 110),
    ("yardage-seamus", "Seamus Golf", "sh", "seamusgolf.com", None, 100),
    ("print-matchstick", "Matchstick Golf", "sh", "matchstickgolf.com",
     "tiger-roar-relief-print", 95),
    ("stash-foray", "Foray Golf", "sh", "foraygolf.com",
     "vintage-golf-rules-stash-book", 92),
    # titled "Vintage Sports Book Planter", lives at /vintage-book-vase
    ("planter-foray", "Foray Golf", "sh", "foraygolf.com", "vintage-book-vase", 68),
    ("pencil-sentinel", "Sentinel", "sq", "sentinelgolf.us",
     "/shop/p/no-16-basket-galvanized-76zkc-bj2ct", 42),
    # --- kitchen & table ---
    ("mugs-gumtree", "Gumtree Golf & Nature Club", "sq", "gumtreegolfandnature.com",
     "/shop/p/gumtree-coffee-studio-espresso-3hywd-wp5bx-zwf4a", 45),
    ("moka-gumtree", "Gumtree Golf & Nature Club", "sq", "gumtreegolfandnature.com",
     "/shop/p/gumtree-coffee-studio-espresso", 38),
    # NOT the Matchstick "Flaming Coffee Mug" / "Iced Coffee" — both read as
    # mugs from their titles and are golf BALL MARKERS shaped like mugs
    # (product_type "Golf Ball Markers", magnetic, USGA conforming). A ball
    # marker is not homeware; two of them nearly shipped in a home-goods post.
    ("poster-apres", "Apres Golf", "sh", "apresgolf.com", None, 34),
    # Lenny's original pick, and the second deliberate sold-out entry: "add
    # those mugs from sugarloaf". Re-read 23 September 2026 and still
    # available:false on the only variant, so the card says so.
    ("mugs-sugarloaf", "Sugarloaf Social Club", "sh", "sugarloafsocialclub.com",
     "ssc-milk-glass-mugs-2-pack", 48),
    ("poster-sugarloaf", "Sugarloaf Social Club", "sh", "sugarloafsocialclub.com",
     "yale-biarritz-framed-poster", 40),
    # --- coffee table books ---
    ("book-impossible", "Assouline", "sh", "assouline.com",
     "golf-the-impossible-collection", 1400),
    ("book-morocco", "Assouline", "sh", "assouline.com",
     "morocco-kingdom-of-golf", 120),
]
# Handles that had to be found by search rather than guessed.
SEARCH = {
    "yardage-seamus": r"irish national tartan.*yardage",
    "poster-apres": r"pencils poster",
}


def get(url, timeout=40):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=timeout).read()


def shopify(host, handle, pattern):
    if handle is None:
        cat = json.loads(get(f"https://{host}/products.json?limit=250"))
        hit = next((p for p in cat["products"]
                    if re.search(pattern, p["title"], re.I)), None)
        if hit is None:
            raise LookupError(f"no product on {host} matching {pattern!r}")
        handle = hit["handle"]
    p = json.loads(get(f"https://{host}/products/{handle}.js"))
    v = p["variants"]
    return {"title": p["title"], "usd": p["price"] / 100,
            "in_stock": bool(p.get("available")),
            "url": f"https://{host}/products/{handle}",
            "desc": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                               p.get("description") or "")).strip(),
            "imgs": ["https:" + i if i.startswith("//") else i
                     for i in (p.get("images") or [])][:MAXFRAMES],
            "variants": len(v)}


def squarespace(host, path):
    cat = json.loads(get(f"https://{host}/shop?format=json"))
    item = next((i for i in cat.get("items", []) if i.get("fullUrl") == path), None)
    if item is None:
        raise LookupError(f"no item at {host}{path}")
    vs = (item.get("structuredContent") or {}).get("variants") or []
    imgs = []
    if item.get("assetUrl"):
        imgs.append(item["assetUrl"])
    for sub in (item.get("items") or []):
        if sub.get("assetUrl"):
            imgs.append(sub["assetUrl"])
    return {"title": item["title"], "usd": vs[0]["price"] / 100 if vs else None,
            "in_stock": sum(v.get("qtyInStock") or 0 for v in vs) > 0,
            "url": f"https://{host}{path}",
            "desc": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                               item.get("body") or "")).strip(),
            "imgs": imgs[:MAXFRAMES], "variants": len(vs)}


def main(apply_):
    rows, bad, last_host = [], [], None
    for stem, brand, plat, host, handle, want in PICKS:
        if last_host == host:
            time.sleep(PAUSE)
        last_host = host
        try:
            d = (squarespace(host, handle) if plat == "sq"
                 else shopify(host, handle, SEARCH.get(stem, "")))
        except Exception as e:
            bad.append(f"{stem}: {type(e).__name__} {e}")
            print(f"  {stem:<20}FAILED  {str(e)[:52]}")
            time.sleep(PAUSE)
            continue
        d.update(stem=stem, brand=brand)
        if d["usd"] is not None and abs(d["usd"] - want) > 0.01:
            bad.append(f"{stem}: expected ${want}, store says ${d['usd']:.0f}")
        rows.append(d)
        flag = "" if d["in_stock"] else "   SOLD OUT"
        print(f"  {stem:<20}${d['usd']:>7.0f}  {len(d['imgs'])}img  "
              f"{d['title'][:38]:<40}{flag}")
        time.sleep(PAUSE)

    if bad:
        print("\n  PROBLEMS:")
        for b in bad:
            print("   ", b)
    if len(rows) != len(PICKS):
        sys.exit(f"\n! {len(PICKS) - len(rows)} product(s) could not be read; "
                 "fix those before localising")
    if not apply_:
        print(f"\n  {len(rows)} products read — dry run, pass --apply to download")
        return

    # ---- download ----
    for r in rows:
        r["local"] = []
        for n, src in enumerate(r["imgs"]):
            f = IMGDIR / (f"{r['stem']}.jpg" if n == 0 else f"{r['stem']}-a{n+1}.jpg")
            if not f.is_file():
                try:
                    im = Image.open(io.BytesIO(get(src))).convert("RGB")
                except Exception as e:
                    bad.append(f"{r['stem']} frame {n+1}: {e}")
                    continue
                w, h = im.size
                tw = min(WIDE, w)
                if tw != w:
                    im = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
                IMGDIR.mkdir(parents=True, exist_ok=True)
                im.save(f, "JPEG", quality=88, optimize=True, progressive=True)
            r["local"].append(f"/images/home-golf-decor/{f.name}")
        time.sleep(0.4)

    thin = [r["stem"] for r in rows if len(r["local"]) < 2]
    if thin:
        bad.append(f"only one usable frame for: {', '.join(thin)}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"_read": "23 September 2026",
                               "_currency": "USD, read from each brand's own store",
                               "products": rows}, indent=1))

    # contact sheet — frames get chosen by looking, not by index
    files = [ROOT / p.lstrip("/") for r in rows for p in r["local"]]
    cols, cell = 6, 300
    sheet = Image.new("RGB", (cols * cell, ((len(files) + cols - 1) // cols) * cell),
                      (240, 240, 238))
    dr = ImageDraw.Draw(sheet)
    for n, f in enumerate(files):
        im = Image.open(f)
        im.thumbnail((cell - 8, cell - 8))
        x, y = (n % cols) * cell + 4, (n // cols) * cell + 4
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + 168, y + 15], fill=(0, 0, 0))
        dr.text((x + 3, y + 3), f.stem[:30], fill=(255, 255, 255))
    sheet.save(ROOT / "research/homegoods/contact.jpg", quality=82)

    print(f"\n  {len(files)} frames in {IMGDIR.relative_to(ROOT)}")
    print(f"  data -> {OUT.relative_to(ROOT)}")
    print("  contact sheet -> research/homegoods/contact.jpg — LOOK AT IT")
    if bad:
        print("\n  PROBLEMS:")
        for b in bad:
            print("   ", b)


if __name__ == "__main__":
    main("--apply" in sys.argv)
