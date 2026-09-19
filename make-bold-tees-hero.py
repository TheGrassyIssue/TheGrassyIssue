#!/usr/bin/env python3
"""
make-bold-tees-hero.py — the 1600x685 hero band for The Bold Tee Edit.

THE REQUIREMENT IS "SHOW THE GRAPHIC TEE", not "look editorial". That is the
lesson written into build-hoodie-shorts.py after four rejected heroes: every
version that failed was solving for atmosphere when the brief was to show the
garment. So all three frames here are photographs of a person wearing one of
the shirts that appears in the post, and two of the three are shot from behind,
because a full back print is the thing this post is actually about.

  left    Butler Pitch & Putt, "This Ain't No Country Club" — shot at Butler,
          downtown Austin behind the fence. Our own par-3 course, our own city,
          and the shirt is card #3 below.
  centre  Gumtree Golf & Nature Club, State Flower Reference Tee — the full
          list of American state flowers printed across the back.
  right   Manors Golf, Reebok x Manors — on-model, the crest at the chest.

Each frame is a centre-weighted crop to 533x685, so nothing is squashed.
Idempotent: same inputs, same bytes.
"""
import pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SRC  = ROOT / "images/bold-tees"
OUT  = ROOT / "images/bold-tees/hero.jpg"
W, H = 1600, 685
FRAMES = ["m-butler-pitch-and-putt.jpg", "w-gumtree-golf.jpg", "w-manors-golf.jpg"]
# Vertical bias per frame, 0.0 = top of the image, 1.0 = bottom. The Butler and
# Gumtree shots put the graphic in the upper-middle of a tall frame; a plain
# centre crop cuts the top of the print off.
BIAS = [0.42, 0.40, 0.34]


def crop(path, w, h, bias):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * scale)), max(h, round(im.height * scale))),
                   Image.LANCZOS)
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
            sys.exit(f"! missing frame source {f}")
        w = fw if i < len(FRAMES) - 1 else W - x
        band.paste(crop(p, w, H, b), (x, 0))
        x += w + gap
    if band.size != (W, H):
        sys.exit(f"! band is {band.size}, expected {(W, H)}")
    if apply_:
        band.save(OUT, "JPEG", quality=90, optimize=True)
        print(f"  wrote {OUT.relative_to(ROOT)}  {band.size[0]}x{band.size[1]}"
              f"  {OUT.stat().st_size//1024}kb")
    else:
        band.save(ROOT / "research/hero-preview.jpg", "JPEG", quality=90)
        print("  dry run — preview at research/hero-preview.jpg")


if __name__ == "__main__":
    main("--apply" in sys.argv)
