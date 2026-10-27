"""The Pullover Edit: frames, 27 Oct 2026. Lenny: no hoods (SSC Anorak -> Grid Quarter-Zip), V15 Burberry -> V14 Masters,
"make sure all images look crisp and clean": Shopify at width=1600, eBay at s-l1600; flat studio sweeps -> stone + contain
(capsules frame()), resale photos -> 4:5 cover crop as shot."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/pullovers/'; O = 'images/pullovers/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
OPT = [x for x in json.load(open(R + 'options.json')) if x['star']]
NEW = {p['url']: p for v in json.load(open(R + 'new.json'))['stores'].values() for p in v['products']}
VIN = {x['url']: x for x in json.load(open(R + 'vintage.json'))['listings']}
SOFTK = {'n32'}  # Dual Sport packshots sit in a white box the flood can't clear: soft cover instead
DROP = {('n46', 2), ('n46', 5), ('n46', 6), ('v2', 4), ('v8', 4)}  # 600px sources; tape-measure shots  # 600px sources: too soft for the gallery
def fn(u):  # eBay names every file s-l1600.jpg, so key on the last two path parts
    return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', '_'.join(u.split('?')[0].rsplit('/', 2)[-2:]))[-110:]
def big(u):
    if 'ebayimg' in u: return re.sub(r's-l\d+', 's-l1600', u)
    if 'cdn.shopify' in u or '/cdn/shop/' in u: return u.split('?')[0] + '?width=1600'
    return u
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(big(u), headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    return f
def cover(im):
    s = max(W / im.width, H / im.height); im2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im2.width - W) // 2; y = (im2.height - H) // 2; return im2.crop((x, y, x + W, y + H))
def warm(im2):  # bright tones only toward stone, no hard mask (same soft path as research/quiet-luxury/frame.py)
    a = np.array(im2).astype(float); k = 10
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    col = np.median(cc, axis=0); L = a.mean(axis=2); Lb = col.mean()
    if Lb < 150: return im2
    w = np.clip((L - .72 * Lb) / (.28 * Lb), 0, 1)[..., None]
    return Image.fromarray((a * (1 - w) + np.clip(a / np.maximum(col, 1) * np.array(STONE), 0, 255) * w).astype('uint8'))
jobs = []
for x in OPT:
    k = x['code'].lower()
    imgs = (NEW[x['url']]['images'] if x['code'][0] == 'N' else VIN[x['url']]['images'])[:6]
    for j, u in enumerate(imgs, 1):
        if (k, j) not in DROP: jobs.append((k, j, u, x['code'][0] == 'V'))
def do(job):
    k, j, u, vint = job
    try:
        im = Image.open(get(u)); im.seek(0); im = im.convert('RGBA'); CUR[0] = k
        out = warm(cover(im.convert('RGB'))) if vint else (warm(cover(im.convert('RGB'))) if k in SOFTK else frame(im))
        p = f'{O}{k}-{j}.jpg'; out.save(p, quality=86, optimize=True); return (k, j, '/' + p, min(Image.open(get(u)).size))
    except Exception as e: print('ERR', k, j, u, e)
with ThreadPoolExecutor(6) as ex: res = [r for r in ex.map(do, jobs) if r]
fr, low = {}, []
for k, j, p, mn in sorted(res, key=lambda r: (r[0], r[1])):
    fr.setdefault(k, []).append(p)
    if mn < 900: low.append((k, j, mn))
# Lenny 27 Oct: "more on-model product images" -> lead each card with an on-model frame (index into the frame list, 0-based)
LEAD = {'n5': 1, 'n15': 2, 'n23': 2, 'n26': 1, 'n27': 1, 'n32': 2, 'n34': 3, 'n35': 1, 'n38': 1, 'n46': 1, 'n53': 1, 'n57': 1, 'n58': 1}
for k, i in LEAD.items():
    if k in fr and i < len(fr[k]): fr[k] = [fr[k][i]] + fr[k][:i] + fr[k][i + 1:]
json.dump(fr, open(R + 'frames.json', 'w'), indent=1); print(len(fr), {k: len(v) for k, v in fr.items()}); print('low-res sources:', low)
