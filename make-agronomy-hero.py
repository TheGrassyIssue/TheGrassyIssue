#!/usr/bin/env python3
"""
make-agronomy-hero.py — 1600x685 hero band for the Agronomy Workshop feature.

THE REQUIREMENT IS TO SHOW THE GARMENT AND THE DETAIL, not to look moody. The
centre frame is the chest pocket with tees in it — the hidden tee holder is the
brand's signature and was the hook of our original 2026 post, the one DEAS MAG
quoted. Flanking it: the shirt on a links course, and a pair at golden hour.

NOTE ON SOURCES: there is not a single landscape image on the brand's entire
domain — everything is 1:1 or portrait — so all three frames are aggressive
centre crops from tall originals. Vertical bias is tuned per frame so the crop
lands on the subject rather than the middle of the file.
"""
import pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SRC  = ROOT / "images/agronomy"
OUT  = SRC / "hero.jpg"
W, H = 1600, 685
# SINGLE FULL-WIDTH FRAME, not a three-up band.
# Lenny: "find a full sized hero image and move those three into the body."
# life-9 is the brand's own photograph of the L/S Work Shirt hung on a garment
# rack in the middle of a golf course, light stand and all — their art direction
# rather than ours, it is the product, and at 1600x1600 a 1600x685 crop needs no
# upscaling at all. The three frames it replaces now run as a lookbook band in
# the body.
FRAMES = ["life-9.jpg"]
BIAS   = [0.42]


def crop(p, w, h, bias):
    im = Image.open(p).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = round((im.height - h) * bias)
    return im.crop((x, y, x + w, y + h))


def main(apply_):
    gap = 4
    fw = (W - gap * (len(FRAMES) - 1)) // len(FRAMES)
    band = Image.new("RGB", (W, H), (246, 245, 241))
    x = 0
    for i, (f, b) in enumerate(zip(FRAMES, BIAS)):
        p = SRC / f
        if not p.exists():
            sys.exit(f"! missing {f}")
        w = fw if i < len(FRAMES) - 1 else W - x
        band.paste(crop(p, w, H, b), (x, 0))
        x += w + gap
    if band.size != (W, H):
        sys.exit(f"! band is {band.size}")
    dest = OUT if apply_ else ROOT / "research/agronomy-hero-preview.jpg"
    band.save(dest, "JPEG", quality=90, optimize=True)
    print(f"  {'wrote' if apply_ else 'preview'} {dest.name}  {band.size[0]}x{band.size[1]}"
          f"  {dest.stat().st_size//1024}kb")


if __name__ == "__main__":
    main("--apply" in sys.argv)
