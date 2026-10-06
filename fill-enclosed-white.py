#!/usr/bin/env python3
"""fill-enclosed-white.py — paint the white holes the soft-gradient pass missed.
5 Oct 2026. Lenny: "the loop on the bags for this page are still stark white" (Local GC).

soften-product-frames.py flood-fills the studio white from the frame edge, so any white the
product encloses — the gap inside a handle loop, a strap, a carabiner — is never reached and stays
stark white on top of the warm gradient. This finds near-pure-white, flat regions that do NOT touch
the edge, on frames that have already been softened (gradient border), and paints them with the
gradient colour for their row. White product surfaces are left alone: they are shaded and textured,
so they fail the flatness test.

Usage: python3 fill-enclosed-white.py images/local-gc [more dirs] [--apply]
"""
import sys, pathlib
import numpy as np
from PIL import Image, ImageFilter
from PIL import ImageDraw
TOP, BOT = np.array((242, 238, 230), float), np.array((228, 222, 210), float)
def is_soft(a):
    b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]).astype(int)
    return (np.abs(b - np.array((236, 231, 221))).max(axis=1) < 14).mean() > 0.8
def fix(path, apply_):
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(np.int16)
    if not is_soft(a): return 0
    h, w, _ = a.shape
    white = (a.min(axis=2) >= 238) & ((a.max(axis=2) - a.min(axis=2)) < 14)
    # edge-connected white, via one flood fill from a padded border ring
    pad = np.zeros((h + 2, w + 2), np.uint8); pad[1:-1, 1:-1] = white * 255
    pad[0, :] = pad[-1, :] = pad[:, 0] = pad[:, -1] = 255
    img = Image.fromarray(pad).copy(); ImageDraw.floodfill(img, (0, 0), 128)
    enc = (np.asarray(img)[1:-1, 1:-1] == 255)
    fill = np.zeros((h, w), bool); hit = 0
    lum = a.mean(axis=2)
    work = Image.fromarray((enc * 255).astype(np.uint8)).copy()
    for _ in range(400):
        arr = np.asarray(work)
        ys, xs = np.nonzero(arr == 255)
        if len(ys) == 0: break
        ImageDraw.floodfill(work, (int(xs[0]), int(ys[0])), 77)
        arr = np.asarray(work); m = arr == 77
        vals = lum[m]
        if m.sum() >= 150 and vals.mean() >= 244 and vals.std() <= 4.5:
            fill |= m; hit += 1
        work = Image.fromarray(np.where(m, 0, arr).astype(np.uint8)).copy()
    if not hit: return 0
    if apply_:
        rows = np.linspace(0, 1, h)[:, None]
        grad = (TOP * (1 - rows[..., None]) + BOT * rows[..., None]).repeat(w, 1)
        mask = Image.fromarray((fill * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
        k = np.asarray(mask).astype(float)[..., None] / 255
        out = (a * (1 - k) + grad * k).clip(0, 255).astype(np.uint8)
        Image.fromarray(out).save(path, 'JPEG', quality=88)
    return hit
if __name__ == '__main__':
    apply_ = '--apply' in sys.argv
    tot = 0
    for d in [x for x in sys.argv[1:] if not x.startswith('--')]:
        for f in sorted(pathlib.Path(d).glob('*.jpg')):
            if ' 2' in f.name: continue
            try: n = fix(f, apply_)
            except OSError: continue
            if n: tot += 1; print(f'  {f}: {n} hole(s)')
    print(f'{tot} frames {"fixed" if apply_ else "would be fixed (dry run)"}')
