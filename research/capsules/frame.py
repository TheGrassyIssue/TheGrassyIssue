"""Capsule wardrobe frames. 25 Oct 2026. Picks: 10 per capsule from research/capsules/<capsule>.json (subagent sweeps, live 25 Oct).
Flat light studio backdrops (white/grey) -> flooded to stone + contain; transparent PNG -> stone; photos -> 4:5 cover.
Also renders the outfit boards (one per look) from each piece's first frame."""
import json, os, glob, numpy as np
from PIL import Image, ImageDraw
R = 'research/capsules/'; O = 'images/capsule-wardrobe/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True)
PICKS = {
 'clubhouse': [0, 1, 10, 7, 4, 15, 20, 23, 24, 25],
 'streetwear': [1, 10, 11, 2, 14, 3, 24, 16, 13, 26],  # st9 Parmore cap -> HLS olive cap (Lenny 25 Oct: used that hat a ton)
 'tour97': [0, 24, 17, 7, 3, 11, 21, 19, 15, 10],
 'outdoor': [13, 15, 0, 7, 16, 24, 25, 11, 22, 5],
 'coastal': [0, 5, 22, 12, 20, 8, 14, 19, 3, 13],
}
SKIP = {('tour97', 15): [3], ('clubhouse', 4): [0]}  # (capsule, idx): [image indexes to drop] — RTG cap image 3 is a reviews screenshot
ORDER = {('clubhouse', 4): [3, 1, 0, 2, 4], ('clubhouse', 10): [2, 0, 1, 3, 4]}  # packshot first
def load(f):
    im = Image.open(f); im.seek(0); return im.convert('RGBA')
SOFT = {('coastal', 19)}  # cream garment on a near-white sweep: the flood mask bleeds into the garment, use the soft warm path
CUR = [None]
def frame(im):
    a = np.array(im).astype(float); al = a[:, :, 3]
    k = 10
    cal = np.concatenate([al[:k, :k].ravel(), al[:k, -k:].ravel(), al[-k:, :k].ravel(), al[-k:, -k:].ravel()])
    if cal.min() < 200:
        ys, xs = np.where(al > 20); g = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        person = g.height > 1.6 * g.width
        s = min(W * (.9 if person else .8) / g.width, H * (.94 if person else .74) / g.height); g = g.resize((max(1, round(g.width * s)), max(1, round(g.height * s))), Image.LANCZOS)
        c = Image.new('RGBA', (W, H), STONE + (255,)); c.alpha_composite(g, ((W - g.width) // 2, (H - g.height) // 2)); return c.convert('RGB')
    rgb = a[:, :, :3]
    cc = np.concatenate([rgb[:k, :k].reshape(-1, 3), rgb[:k, -k:].reshape(-1, 3), rgb[-k:, :k].reshape(-1, 3), rgb[-k:, -k:].reshape(-1, 3)])
    src = Image.fromarray(rgb.astype('uint8'))
    flat = cc.min() >= 200 and cc.std() <= 8 and CUR[0] not in SOFT
    if flat:  # flat light studio backdrop: flood from the corners, recolour to stone, then contain
        col = np.median(cc, axis=0); dd = np.abs(rgb - col).max(axis=2)
        mk = Image.fromarray(((dd < 18) * 255).astype('uint8')).copy()
        for pt in [(0, 0), (mk.width - 1, 0), (0, mk.height - 1), (mk.width - 1, mk.height - 1)]: ImageDraw.floodfill(mk, pt, 128)
        bg = np.array(mk) == 128; out = rgb.copy(); out[bg] = np.clip(rgb / np.maximum(col, 1) * np.array(STONE), 0, 255)[bg]
        ys, xs = np.where(~bg)
        if len(xs) > 500:
            x0, x1 = np.percentile(xs, [.3, 99.7]).astype(int); y0, y1 = np.percentile(ys, [.3, 99.7]).astype(int)
            bw, bh = x1 - x0, y1 - y0
            m = int(.05 * max(bw, bh)); x0, y0 = max(0, x0 - m), max(0, y0 - m); x1, y1 = min(src.width, x1 + m), min(src.height, y1 + m)
            g = Image.fromarray(out.astype('uint8')).crop((x0, y0, x1, y1))
            person = bh > 1.6 * bw  # full-length model shot: fill the frame height instead of floating small
            s = min(W * (.9 if person else .8) / g.width, H * (.94 if person else .74) / g.height)
            g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
            c = Image.new('RGB', (W, H), STONE); c.paste(g, ((W - g.width) // 2, (H - g.height) // 2 if not person else H - g.height - int(H * .03))); return c
    elif cc.min() >= 165:  # graded light studio sweep (white/grey): soft warm toward stone on the bright tones only, no hard mask
        col = np.median(cc, axis=0); L = rgb.mean(axis=2); Lb = col.mean()
        w = np.clip((L - .72 * Lb) / (.28 * Lb), 0, 1)[..., None]
        out = rgb * (1 - w) + np.clip(rgb / np.maximum(col, 1) * np.array(STONE), 0, 255) * w
        src = Image.fromarray(out.astype('uint8'))
    s = max(W / src.width, H / src.height); im2 = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    x = (im2.width - W) // 2; y = (im2.height - H) // 2; return im2.crop((x, y, x + W, y + H))
fr = {}
for cap, idxs in PICKS.items():
    for n, i in enumerate(idxs, 1):
        key = f'{cap[:2]}{n}'
        fs = sorted(glob.glob(f'{R}raw/{cap}-i{i:02d}-*.img'), key=lambda f: int(f.rsplit('-', 1)[1].split('.')[0]))
        ix = lambda f: int(f.rsplit('-', 1)[1].split('.')[0])
        if (cap, i) in ORDER: fs = sorted(fs, key=lambda f: ORDER[(cap, i)].index(ix(f)) if ix(f) in ORDER[(cap, i)] else 99)
        fs = [f for f in fs if ix(f) not in SKIP.get((cap, i), [])][:5]; CUR[0] = (cap, i)
        for j, f in enumerate(fs, 1):
            try:
                out = f'{O}{key}-{j}.jpg'; frame(load(f)).save(out, quality=84, optimize=True); fr.setdefault(key, []).append('/' + out)
            except Exception as e:
                print('skip', f, e)
# Lenny 25 Oct: "add a sentinel option to the outdoor technical. Add a Odd Ritual option to the streetwear section" (research/capsules/extra.json)
EXTRA = {'ou11': 'xse-i00', 'st11': 'xod-i01'}
CUR[0] = None
for key, stem in EXTRA.items():
    fs = sorted(glob.glob(f'{R}raw/{stem}-*.img'), key=lambda f: int(f.rsplit('-', 1)[1].split('.')[0]))[:5]
    for j, f in enumerate(fs, 1):
        out = f'{O}{key}-{j}.jpg'; frame(load(f)).save(out, quality=84, optimize=True); fr.setdefault(key, []).append('/' + out)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1)
print({k: len(v) for k, v in fr.items()})
