#!/usr/bin/env python3
"""localize-hats-hero.py — cut the masthead for The Hat & Towel Edit.
21 September 2026.

THE PAGE WAS WEARING THE DONOR'S HERO. build-hat-towel-edit.py splices a new
body into drops/the-hat-edit-austin-summer.html, and the donor keeps its hero
*above* the splice point, so the new post shipped with the old post's Nature
Club bucket hat at the top. This script cuts a hero the new post owns.

THE FRAME. Sugarloaf Social Club's own product photography for the Cotton SSC
Arrow Cap — the cap Lenny picked out of the grid himself. It is the only
candidate frame shot on a golf course rather than in a cabin or against a wall:
cap, mown grass, a windmill and sky. A hat post should open on a hat outdoors.

CROP BIAS 0.32, CHOSEN BY LOOKING. The source is square (3669x3669) and a 21:9
band throws away 57% of the height, so the bias decides whether the cap keeps
its crown or its brim. 0.20 cuts the brim; 0.45 cuts the crown and lands on the
chin. 0.32 holds the whole cap with the course behind it.

NO UPSCALING. target_w is clamped to the source width, and the verify block
asserts the output is no wider than the source — the same guard as
localize-casualist-2026.py, for the same reason.

Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/hats-towels/hero.jpg"
SRC = ("https://www.sugarloafsocialclub.com/cdn/shop/files/Untitled-45.jpg"
       "?v=1776806155")
CREDIT = "Sugarloaf Social Club"
MAX_W = 2000
RATIO = 21 / 9
BIAS = 0.32
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def main(apply_):
    raw = urllib.request.urlopen(urllib.request.Request(SRC, headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    print(f"  source: {w}x{h}  ({len(raw)/1024:.0f} KB)")

    ch = round(w / RATIO)
    if ch > h:
        sys.exit(f"! source is too short for {RATIO:.2f}:1 — {w}x{h}")
    top = round((h - ch) * BIAS)
    band = im.crop((0, top, w, top + ch))
    print(f"  crop:   y {top}..{top + ch} of {h}  (bias {BIAS})")

    target_w = min(MAX_W, w)          # never upscale
    band = band.resize((target_w, round(target_w / RATIO)), Image.LANCZOS)

    if not apply_:
        print(f"  would write {OUT.relative_to(ROOT)} at {band.size}")
        print("\n  dry run — pass --apply")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    band.save(OUT, quality=88, optimize=True, progressive=True)

    # ---- VERIFY THE FILE ON DISK, NOT THE OBJECT IN MEMORY ----
    got = Image.open(OUT)
    bad = []
    if got.width > w:
        bad.append(f"upscaled: {got.width}px from a {w}px source")
    if abs(got.width / got.height - RATIO) > 0.01:
        bad.append(f"ratio is {got.width / got.height:.3f}, expected {RATIO:.3f}")
    if OUT.stat().st_size > 900_000:
        bad.append(f"{OUT.stat().st_size/1024:.0f} KB is too heavy for a masthead")
    if bad:
        sys.exit("! " + "; ".join(bad))

    cr = ROOT / "images/hats-towels/credits.json"
    c = json.loads(cr.read_text(encoding="utf-8")) if cr.exists() else {}
    c["hero.jpg"] = {"credit": CREDIT, "source": SRC}
    cr.write_text(json.dumps(dict(sorted(c.items())), indent=1) + "\n", encoding="utf-8")

    print(f"\n  wrote {OUT.relative_to(ROOT)} {got.size} "
          f"({OUT.stat().st_size/1024:.0f} KB), credit {CREDIT}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
