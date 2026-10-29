"""GrabCut cut-out for light products on light studio sweeps (no colour flood, so white/cream product bodies keep their own tone). 29 Oct 2026."""
import cv2, numpy as np
from PIL import Image, ImageFilter
W, H = 1000, 1250; STONE = (232, 226, 214)
def bg_flat(a):
    k = 12
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    return cc.std() <= 6 and cc.min() >= 190, np.median(cc, axis=0)
def cutout(path, scale_w=.8, scale_h=.74):
    im = Image.open(path).convert('RGB'); a = np.array(im)
    flat, col = bg_flat(a.astype(float))
    if not flat: return None
    s = 900 / max(a.shape[:2]); sm = cv2.resize(a, (int(a.shape[1] * s), int(a.shape[0] * s)), interpolation=cv2.INTER_AREA)
    d = np.abs(sm.astype(float) - col).max(axis=2) > 10
    ys, xs = np.where(d)
    if len(xs) < 200: return None
    x0, x1 = np.percentile(xs, [.5, 99.5]).astype(int); y0, y1 = np.percentile(ys, [.5, 99.5]).astype(int)
    m = 12; x0, y0 = max(1, x0 - m), max(1, y0 - m); x1, y1 = min(sm.shape[1] - 2, x1 + m), min(sm.shape[0] - 2, y1 + m)
    mask = np.zeros(sm.shape[:2], np.uint8); bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(cv2.cvtColor(sm, cv2.COLOR_RGB2BGR), mask, (x0, y0, x1 - x0, y1 - y0), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    fg = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    # keep the largest blobs, fill holes
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 0.02 * st[1:, cv2.CC_STAT_AREA].max()]
        fg = np.isin(lab, keep).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(fg, cnts, -1, 255, -1)
    fg = cv2.resize(fg, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_LINEAR)
    alpha = Image.fromarray(fg).filter(ImageFilter.GaussianBlur(1.5))
    ys, xs = np.where(fg > 127)
    if len(xs) < 500: return None
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    g = im.convert('RGBA'); g.putalpha(alpha); g = g.crop((bx0, by0, bx1 + 1, by1 + 1))
    sc = min(W * scale_w / g.width, H * scale_h / g.height); g = g.resize((round(g.width * sc), round(g.height * sc)), Image.LANCZOS)
    c = Image.new('RGBA', (W, H), STONE + (255,)); c.alpha_composite(g, ((W - g.width) // 2, (H - g.height) // 2)); return c.convert('RGB')
