#!/usr/bin/env python3
"""localize-hats-hero.py — cut the masthead for The Hat & Towel Edit.
21 September 2026.

THE PAGE WAS WEARING THE DONOR'S HERO. build-hat-towel-edit.py splices a new
body into drops/the-hat-edit-austin-summer.html, and the donor keeps its hero
*above* the splice point, so the new post shipped with the old post's Nature
Club bucket hat at the top. This script cuts a hero the new post owns.

THE FRAME, SECOND PASS. The first hero was a Sugarloaf cap on a course, which
was a good picture of a hat — and the problem with that is the post is half
towels. Lenny asked for a different one.

Seamus Golf's Spider Rock jacquard is the only frame in the thirty that is
NATIVELY LANDSCAPE (2878x2120). Every other candidate is a 4:5 or square
product shot, so a 21:9 band from them either throws away most of the picture
or crops a model's face off — both of which I cut and looked at before ruling
them out. The Birds of Condor lifestyle frames decapitate the model; the
Metalwood Dewey is a grey cap on white; the Sierra Madre course scene is the
best of the rest but caps out at 1200px wide, below the house masthead size.

CROP BIAS 0.50. A landscape source loses only 42% of its height to the band and
the woven pattern is symmetrical, so the centre is the right cut; there is no
subject to protect at one edge.

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
SRC = "https://cdn.shopify.com/s/files/1/0129/1462/files/spiderrocknewtag_edited.png?v=1765366515"
CREDIT = "Seamus Golf"
MAX_W = 2000
RATIO = 21 / 9
BIAS = 0.50
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
