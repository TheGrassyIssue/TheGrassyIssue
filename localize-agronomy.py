#!/usr/bin/env python3
"""
localize-agronomy.py — pull Agronomy Workshop imagery local. 19 September 2026.

HOUSE RULE: never hot-link a brand's CDN. Framer and Shopify URLs here carry
width/height query params and content hashes; both rotate.

Gate on max(width, height), not width — every asset on this site is square or
portrait (there is not one landscape image on the whole domain), so a
width-only cap would let 4096px-tall files through.

Idempotent: a file already present is left alone.
"""
import json, pathlib, sys, urllib.request
from io import BytesIO
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = ROOT / "research/agronomy-catalogue.json"
OUTD = ROOT / "images/agronomy"
MAXPX = 1600
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()


def save(raw, dest):
    im = Image.open(BytesIO(raw))
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    else:
        im = im.convert("RGB")
    if max(im.size) > MAXPX:
        r = MAXPX / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)
    return im.size


def main(apply_):
    d = json.loads(SPEC.read_text(encoding="utf-8"))
    jobs = []
    for p in d["products"]:
        imgs = p.get("images") or []
        if imgs:
            jobs.append((f"p-{p['handle']}.jpg", imgs[0], p["title"]))
        if len(imgs) > 1:                       # a second frame for galleries
            jobs.append((f"p-{p['handle']}-2.jpg", imgs[1], p["title"] + " alt"))
    # 0-7 were the first pass. 9-25 are the on-model and in-situ frames —
    # the real lookbook. 26-31 are defect documentation and flat scans,
    # deliberately skipped. 32-33 are video.
    WANT = list(range(0, 8)) + [9, 11, 12, 13, 14, 16, 17, 20, 21, 22, 24]
    for i in WANT:
        l = d["lifestyle_images"][i]
        jobs.append((f"life-{i}.jpg", l["url"], l.get("shows", "")[:50]))

    if apply_:
        OUTD.mkdir(parents=True, exist_ok=True)
    got = fail = skip = 0
    for name, url, label in jobs:
        dest = OUTD / name
        if dest.exists():
            skip += 1; continue
        if not apply_:
            print(f"  would fetch {name}"); continue
        try:
            sz = save(fetch(url), dest)
            print(f"  ok   {name:44} {sz[0]}x{sz[1]}"); got += 1
        except Exception as e:
            print(f"  FAIL {name:44} {type(e).__name__}: {e}"); fail += 1
    print(f"\n  fetched {got}, skipped {skip}, failed {fail}")
    if apply_ and fail:
        sys.exit("! some assets did not land")


if __name__ == "__main__":
    main("--apply" in sys.argv)
