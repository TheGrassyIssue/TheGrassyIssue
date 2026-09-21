#!/usr/bin/env python3
"""localize-casualist-2026.py — new hero + two body bands for the Casualist
beef-up. 21 September 2026.

Lenny: "let's beef up this post ... I want to get onto the first page of google.
ALso needs a new hero shot."

THE HERO CHOICE IS NOT ARBITRARY.
The headline is "The London Brand That Outgrew Its Own Name". Of the 56 frames
Casualist publishes at 3000px or wider, exactly one shows the old name being
worn: two players walking away up a fairway with CASUAL PRO across their backs.
The masthead therefore states the thesis of the piece without a caption. It is
also the only genuinely landscape-composed lifestyle frame in the catalogue —
100 of their 101 product images are portrait, shot for a phone.

NO UPSCALING, EVER.
Source is 3812x4766. A 21:9 band off a 3812px-wide original is 3812x1634, which
is downsampled to 1800x771 for the masthead. The guard at the bottom re-opens
every output and asserts it is no larger than the crop it came from. The house
cap is 1800w; it is a cap and not a target (the Vuori hero shipped at 1405w
because that was the honest width of the original).

CROP GEOMETRY. Chosen by rendering four bands and looking at them, not by
reasoning about where the subjects "should" be. At 0.22 the left jacket's PRO
is sliced by the bottom edge; at 0.37 the tree loses its crown and the sky goes.
0.32 is the only band that holds both complete CASUAL PRO wordmarks, the
"MASTER OF NONE, ENTHUSIAST OF MANY" line under the left one, and the full tree.
That small print matters: it is the same phrase The Wedgies used to describe the
brand's philosophy in May 2024, so the garment corroborates the source.

Body bands support the two new sections:
  band-coast  — the shingle-beach frame, for the Melbourne-to-London section
  band-links  — heath and gorse, for the "is it a British brand" section
Both are 1400w native-shape, which is the house body-band width.

Idempotent. Dry run by default.
"""
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "research/casualist/hero"
OUT = ROOT / "images/casualist"

HERO_RATIO = 21 / 9
HERO_MAX_W = 1800          # cap, not a target — never reached by upscaling
BAND_W = 1400

# (source file, output name, crop mode, vertical bias)
JOBS = [
    ("winbreaker-1-53369770541350.jpg", "btk-hero-2026.jpg", "hero", 0.32),
    ("appropriate-dress-code-moc-51603470418214.jpg", "band-coast.jpg", "band", 0.30),
    ("weekend-pique-polo-mocha-51603438534950.jpg", "band-links.jpg", "band", 0.34),
]


def cut(src_name, out_name, mode, bias, apply_):
    s = SRC / src_name
    if not s.is_file():
        sys.exit(f"! missing source frame: {s}")
    o = OUT / out_name
    im = Image.open(s).convert("RGB")
    w, h = im.size

    if mode == "hero":
        ch = int(round(w / HERO_RATIO))
        if ch > h:
            sys.exit(f"! {src_name} is {w}x{h}; too short for 21:9")
        top = int((h - ch) * bias)
        box = (0, top, w, top + ch)
        target_w = min(HERO_MAX_W, w)          # THE no-upscale clamp
        target_h = int(round(target_w / HERO_RATIO))
    else:
        # body bands keep the frame's own shape, only narrowed to house width
        box = (0, 0, w, h)
        target_w = min(BAND_W, w)
        target_h = int(round(h * target_w / w))

    if o.exists():
        ex = Image.open(o)
        return f"{out_name} already local ({ex.width}x{ex.height})"
    if not apply_:
        return f"would cut {out_name} {target_w}x{target_h} from {w}x{h}"

    OUT.mkdir(parents=True, exist_ok=True)
    im.crop(box).resize((target_w, target_h), Image.LANCZOS).save(
        o, "JPEG", quality=88, optimize=True, progressive=True)
    return (f"cut {out_name} {target_w}x{target_h} from {w}x{h} "
            f"(crop {box[2]-box[0]}x{box[3]-box[1]})")


def main(apply_):
    notes = [cut(*j, apply_) for j in JOBS]
    for n in notes:
        print("  " + n)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK, AGAINST THEIR OWN SOURCES ----
    bad = []
    for src_name, out_name, mode, _bias in JOBS:
        o, s = OUT / out_name, SRC / src_name
        if not o.is_file():
            bad.append(f"{out_name} not written")
            continue
        got, orig = Image.open(o), Image.open(s)
        if got.width > orig.width:
            bad.append(f"{out_name} is {got.width}w from a {orig.width}w original "
                       f"— that is an upscale")
        if mode == "hero":
            r = got.width / got.height
            if abs(r - HERO_RATIO) > 0.01:
                bad.append(f"{out_name} ratio {r:.3f}, expected {HERO_RATIO:.3f}")
            if got.width > HERO_MAX_W:
                bad.append(f"{out_name} is {got.width}w, over the {HERO_MAX_W} cap")
        if o.stat().st_size > 900_000:
            bad.append(f"{out_name} is {o.stat().st_size//1024}KB — too heavy for a masthead")
    if bad:
        sys.exit("! " + "; ".join(bad))

    sizes = {n: Image.open(OUT / n).size for _s, n, _m, _b in JOBS}
    print("\n  verified, no upscaling: " +
          ", ".join(f"{k} {v[0]}x{v[1]}" for k, v in sizes.items()))


if __name__ == "__main__":
    main("--apply" in sys.argv)
