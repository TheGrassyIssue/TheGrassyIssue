"""Quiet luxury golf brands: product frames, 26 Oct 2026. Treatment shared with research/capsules/frame.py
(flat light studio sweep -> stone + contain; graded sweep -> soft warm; photos -> 4:5 cover)."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/quiet-luxury/'; O = 'images/quiet-luxury/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
PK = json.load(open(R + 'picks.json'))
KEY = {'late-nine':'ln','alba-golf':'al','whim-golf':'wh','rookline':'rk','sloat':'sl','quiet-golf':'qg','local-rule':'lr','sounder':'sd','casualist':'cs'}
SOFTK = {'al3'}   # cream trouser: the flood mask blotched it (26 Oct render), soft path instead
def fn(u): return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', u.split('?')[0].rsplit('/', 1)[-1])[-90:]
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        q = '' if 'late-nine' in u and 'cdn.shopify' not in u else '?width=1600'
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u.split('?')[0] + q, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    return f
def soft(im):
    s = max(W / im.width, H / im.height); im2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im2.width - W) // 2; y = (im2.height - H) // 2; im2 = im2.crop((x, y, x + W, y + H))
    a = np.array(im2).astype(float); k = 10
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    col = np.median(cc, axis=0); L = a.mean(axis=2); Lb = col.mean()
    if Lb < 150: return im2
    w = np.clip((L - .72 * Lb) / (.28 * Lb), 0, 1)[..., None]
    return Image.fromarray((a * (1 - w) + np.clip(a / np.maximum(col, 1) * np.array(STONE), 0, 255) * w).astype('uint8'))
jobs = []
for slug, rows in PK.items():
    for i, r in enumerate(rows, 1):
        for j, u in enumerate(r['imgs'][:5], 1): jobs.append((f'{KEY[slug]}{i}', j, u))
def do(job):
    k, j, u = job
    try:
        im = Image.open(get(u)); im.seek(0); im = im.convert('RGBA'); CUR[0] = k
        out = soft(im.convert('RGB')) if k in SOFTK else frame(im)
        p = f'{O}{k}-{j}.jpg'; out.save(p, quality=84, optimize=True); return (k, j, '/' + p)
    except Exception as e: print('ERR', k, j, u, e)
with ThreadPoolExecutor(6) as ex: res = [r for r in ex.map(do, jobs) if r]
fr = {}
for k, j, p in sorted(res, key=lambda r: (r[0], r[1])): fr.setdefault(k, []).append(p)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1); print(len(fr), {k: len(v) for k, v in fr.items()})
