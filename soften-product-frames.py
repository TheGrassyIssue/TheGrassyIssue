#!/usr/bin/env python3
"""soften-product-frames.py — swap stark white studio backgrounds for a soft warm gradient.

1 October 2026. Lenny: "can we change these stark white backgrounds on the products to a gradient?
or something softer".

For each gallery frame in the given image folders: if the frame's border is near-white studio
background, flood-fill that background from the edges (so white parts of the product itself are left
alone), re-frame the product a little tighter (it was padded small in most store shots), and paint the
background as a top-to-bottom gradient in the site's paper tones, keeping the product's own soft shadow.
Lifestyle photos (no white border) are skipped. Already-softened frames are skipped too, because their
border is no longer white, so it is safe to re-run.

Usage: python3 soften-product-frames.py images/local-gc images/rangefinder-pouches [--apply]
"""
import sys
from collections import deque
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TOP, BOT = (242, 238, 230), (228, 222, 210)  # TOP min < THR, so a softened frame never re-qualifies
THR = 232
W, H = 1000, 1250
SKIP = ("hero", "og", "band-")


def bg_mask(a):
    h, w, _ = a.shape
    near = (a.min(axis=2) >= THR) & ((a.max(axis=2) - a.min(axis=2)) < 18)
    border = np.concatenate([near[0], near[-1], near[:, 0], near[:, -1]])
    if border.mean() < 0.85:
        return None
    # pad with a 1px ring of background, then one C-speed flood fill from the corner reaches every
    # near-white region that touches the edge (white inside the product stays put)
    pad = np.zeros((h + 2, w + 2), np.uint8); pad[1:-1, 1:-1] = near * 255; pad[0, :] = pad[-1, :] = pad[:, 0] = pad[:, -1] = 255
    img = Image.fromarray(pad).copy()  # copy: a fromarray image can be read-only, and floodfill then silently does nothing
    ImageDraw.floodfill(img, (0, 0), 128)
    mask = (np.asarray(img)[1:-1, 1:-1] == 128)
    return mask


def soften(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    mask = bg_mask(a)
    if mask is None:
        return "skip"
    ys, xs = np.where(~mask)
    if len(ys) < 500:
        return "skip"
    # re-frame: subject bounding box + 14% margin, expanded to 4:5, clamped to the image
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    bh, bw = y1 - y0, x1 - x0
    m = int(max(bh, bw) * 0.14)
    cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    ch = max(bh + 2 * m, (bw + 2 * m) * H / W); cw = ch * W / H
    h, w = mask.shape
    ch, cw = min(ch, h), min(cw, w)
    if cw / ch > W / H: cw = ch * W / H
    else: ch = cw * H / W
    top = int(min(max(cy - ch / 2, 0), h - ch)); left = int(min(max(cx - cw / 2, 0), w - cw))
    box = (left, top, left + int(cw), top + int(ch))
    im = im.crop(box).resize((W, H), Image.LANCZOS)
    mk = Image.fromarray((mask * 255).astype("uint8")).crop(box).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    a = np.asarray(im).astype(np.float32)
    t = np.linspace(0, 1, H)[:, None, None]
    g = np.repeat(np.array(TOP) * (1 - t) + np.array(BOT) * t, W, axis=1)
    lum = a.mean(axis=2, keepdims=True) / 255.0          # keeps the product's soft contact shadow
    bg = Image.fromarray(np.clip(g * lum, 0, 255).astype("uint8"))
    Image.composite(bg, im, mk).save(path, quality=82, optimize=True, progressive=True)
    return "soft"


def main(dirs, apply_):
    n = {"soft": 0, "skip": 0}
    for d in dirs:
        for f in sorted(pathlib.Path(d).glob("*.jpg")):
            if f.name.startswith(SKIP):
                continue
            if not apply_:
                a = np.asarray(Image.open(f).convert("RGB")).astype(np.int16)
                n["soft" if bg_mask(a) is not None else "skip"] += 1
                continue
            n[soften(f)] += 1
    print(f"  {n['soft']} frames softened, {n['skip']} left as they are" + ("" if apply_ else " (dry run — pass --apply)"))


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")], "--apply" in sys.argv)
