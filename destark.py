#!/usr/bin/env python3
"""destark.py — replace stark white packshot backdrops with a warm stone tone (Lenny, 12 Oct 2026: "No stark white backgrounds").
Floods the white backdrop from the frame edge, then multiply-blends stone into it so soft shadows survive and
anti-aliased product edges don't leave a white halo. Pale products get a tight mask so their edges aren't tinted.
Usage: from destark import destark; destark(path, light=False)"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
STONE = np.array([232, 226, 214], float)

def destark(path, light=False, min_white=0.4):
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(float)
    b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    if (b.min(axis=1) >= 243).mean() < min_white: return False
    w, h = im.size; probe = im.copy()
    seeds = [(x, y) for x in range(0, w, 20) for y in (0, h - 1)] + [(x, y) for y in range(0, h, 20) for x in (0, w - 1)]
    for s in seeds:
        if min(probe.getpixel(s)) >= 240: ImageDraw.floodfill(probe, s, (255, 0, 255), thresh=20 if light else 34)
    pa = np.asarray(probe); m = ((pa[..., 0] == 255) & (pa[..., 1] == 0) & (pa[..., 2] == 255)).astype('uint8') * 255
    m = np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(13 if light else 41)).filter(ImageFilter.GaussianBlur(2))).astype(float)[..., None] / 255
    if not light:
        lum = np.asarray(im.convert('L')).astype(float)[..., None]; m = m * np.clip((lum - 150) / 60, 0, 1)
    if not light:  # enclosed or boxed near-white areas the flood can't reach (handle loops, off-white mockup boxes)
        mn = a.min(axis=2, keepdims=True); m = np.maximum(m, np.clip((mn - 232) / 12, 0, 1))
    out = a * (1 - m) + (a * STONE / 255) * m
    Image.fromarray(out.clip(0, 255).astype('uint8')).save(path, quality=86); return True
