"""recolor(path): replace an edge-connected light studio background with TGI stone, keeping shadows (multiply tint).
Used for Cloud & Wind and Cadero packshots (pale gray / pale blue sweeps that destark misses)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
STONE = np.array([232, 226, 214], float)
SENT = (255, 0, 255)
def recolor(path, thresh=26):
    im = Image.open(path).convert('RGB'); w, h = im.size
    a = np.asarray(im).astype(float)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    if border.min(axis=1).mean() < 195: return False          # not a light studio shot
    work = im.copy()
    seeds = [(x, 0) for x in range(0, w, 40)] + [(x, h-1) for x in range(0, w, 40)] + \
            [(0, y) for y in range(0, h, 40)] + [(w-1, y) for y in range(0, h, 40)]
    for s in seeds:
        px = work.getpixel(s)
        if px != SENT and min(px) > 190: ImageDraw.floodfill(work, s, SENT, thresh=thresh)
    m = (np.asarray(work) == SENT).all(axis=2)
    # also catch enclosed pale islands that match the sweep colour closely
    bg = np.median(a[m], axis=0) if m.any() else border.mean(axis=0)
    near = (np.abs(a - bg).max(axis=2) < 14) & (a.min(axis=2) > 200)
    mask = Image.fromarray(((m | near) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2.5))
    k = np.asarray(mask).astype(float)[..., None] / 255
    tint = np.clip(a * (STONE / np.maximum(bg, 1)), 0, 255)
    out = a * (1 - k) + tint * k
    Image.fromarray(out.astype('uint8')).save(path, quality=88); return True

def grade(path):
    """Whole-frame white-balance toward stone: multiply by STONE / border colour. No masks, so no halos.
    Used for Cloud & Wind packshots shot on soft gradient sweeps."""
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(float)
    border = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    if border.min(axis=1).mean() < 185: return False
    bg = np.percentile(border, 60, axis=0)
    out = np.clip(a * (STONE / np.maximum(bg, 1)), 0, 255)
    Image.fromarray(out.astype('uint8')).save(path, quality=88); return True
