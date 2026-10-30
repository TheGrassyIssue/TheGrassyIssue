"""Gentle background swap: only near-white pixels connected to the image border become stone. No GrabCut, no hole punching."""
import numpy as np, cv2
from PIL import Image
W, H = 1000, 1250; STONE = np.array((232, 226, 214), float)
def soft(path, sw=.8, sh=.74, thr=244):
    a = np.array(Image.open(path).convert('RGB'))
    if max(a.shape[:2]) > 2400:
        s = 2400 / max(a.shape[:2]); a = cv2.resize(a, (round(a.shape[1]*s), round(a.shape[0]*s)), interpolation=cv2.INTER_AREA)
    nw = ((a.min(2) >= thr) & ((a.max(2).astype(int) - a.min(2)) < 10)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(nw, connectivity=4)
    edge = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    bg = np.isin(lab, list(edge))
    fg = ~bg
    ys, xs = np.where(fg)
    if len(ys) == 0: return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    alpha = cv2.GaussianBlur(fg.astype(np.float32), (3, 3), 0)[..., None]
    out = a.astype(float) * alpha + STONE * (1 - alpha)
    crop = out[y0:y1, x0:x1]
    s = min(W * sw / crop.shape[1], H * sh / crop.shape[0])
    crop = cv2.resize(crop.astype(np.uint8), (max(1, round(crop.shape[1]*s)), max(1, round(crop.shape[0]*s))), interpolation=cv2.INTER_LANCZOS4 if s > 1 else cv2.INTER_AREA)
    c = np.tile(STONE.astype(np.uint8), (H, W, 1))
    oy, ox = (H - crop.shape[0]) // 2, (W - crop.shape[1]) // 2
    c[oy:oy+crop.shape[0], ox:ox+crop.shape[1]] = crop
    return Image.fromarray(c)
