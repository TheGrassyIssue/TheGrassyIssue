"""On our radar Vol. 3: product frames. 27 Oct 2026. Treatment shared with research/capsules/frame.py.
Lenny 27 Oct: stars + A4 colorway (black nylon pullover instead of green), add A13, add G12."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/radar-three-3/'; O = 'images/radar-three-3/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
CARDS = {
 'aw-beige': ('aberdeen-west', 'beige-satin-trucker-jacket'), 'aw-blacksatin': ('aberdeen-west', 'black-satin-trucker-jacket'),
 'aw-nylon': ('aberdeen-west', 'black-nylon-pullover-jacket'), 'aw-cardigan': ('aberdeen-west', '100-cashmere-checker-cardigan'),
 'aw-polo': ('aberdeen-west', 'brown-striped-knit-long-sleeve-polo'), 'aw-plaid': ('aberdeen-west', 'classic-plaid-pant'),
 'aw-pine': ('aberdeen-west', 'pine-aw-wing-tip'), 'aw-oxblood': ('aberdeen-west', 'oxblood-ghost'),
 'aw-harmony': ('aberdeen-west', 'harmony-white'), 'aw-bag': ('aberdeen-west', 'aw-golf-stand-bag'),
 'wh-qzip': ('we-hit-fairways', 'checkered-q-zip-mint-blue'), 'wh-cardigan': ('we-hit-fairways', 'champions-cardigan-off-white'),
 'wh-sweater': ('we-hit-fairways', 'champions-knit-sweater-ivory'), 'wh-zip': ('we-hit-fairways', 'signature-knit-zip-sweater-oat'),
 'wh-vneck': ('we-hit-fairways', 'tour-v-neck-polo-mustard'), 'wh-waffle': ('we-hit-fairways', 'waffle-knit-polo-clay-red'),
 'wh-medalist': ('we-hit-fairways', 'medalist-knit-polo-sky-blue'), 'wh-lion': ('we-hit-fairways', 'lion-cap-green'),
 'gc-sphere': ('grind-city-golf', 'sphere-study-crew-knit'), 'gc-cardigan': ('grind-city-golf', 'the-unofficial-cardigan-copy'),
 'gc-floral': ('grind-city-golf', 'v-neck-copy'), 'gc-clubs': ('grind-city-golf', 'v-vest-1'),
 'gc-varsity': ('grind-city-golf', 'two-tone-fleeced-varsity-jacket-1'), 'gc-pinstripe': ('grind-city-golf', 'pinstripe-protocol-polo'),
 'gc-track': ('grind-city-golf', 'unisex-plaid-full-zip-track-jacket'), 'gc-barrel': ('grind-city-golf', 'men-s-barrel-leg-pants'),
 'gc-lowfade': ('grind-city-golf', 'low-fade-polo'),
}
CAT = {s: {p['handle']: p for p in json.load(open(R + s + '.json'))['products']} for s in ('aberdeen-west', 'we-hit-fairways', 'grind-city-golf')}
DROP = {('gc-barrel', 3)}  # spec infographic, not a photo
# on-model first (Lenny prefers on-model and on-course); source index of the shot to lead with
LEAD = {k: 1 for k in ('gc-barrel', 'gc-cardigan', 'gc-clubs', 'gc-floral', 'gc-lowfade', 'gc-pinstripe', 'gc-sphere', 'gc-track',
                       'wh-lion', 'wh-vneck', 'wh-waffle', 'wh-zip', 'wh-qzip', 'wh-sweater', 'wh-medalist')}
SOFTK = set()
def fn(u): p = u.split('?')[0].split('/'); return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', '_'.join(p[-2:]))[-90:]
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u.split('?')[0] + '?width=1600', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    return f
def cover(src):
    s = max(W / src.width, H / src.height); im2 = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    x = (im2.width - W) // 2; y = (im2.height - H) // 2; im2 = im2.crop((x, y, x + W, y + H))
    a = np.array(im2).astype(float); k = 10
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    col = np.median(cc, axis=0); L = a.mean(axis=2); Lb = col.mean()
    if Lb < 150: return im2
    w = np.clip((L - .72 * Lb) / (.28 * Lb), 0, 1)[..., None]
    out = a * (1 - w) + np.clip(a / np.maximum(col, 1) * np.array(STONE), 0, 255) * w
    return Image.fromarray(out.astype('uint8'))
jobs = []
for k, (s, h) in CARDS.items():
    imgs = (CAT[s][h].get('images') or CAT[s][h].get('image_urls'))[:5]
    order = list(range(len(imgs)))
    if k in LEAD: order.remove(LEAD[k]); order.insert(0, LEAD[k])
    order = [i for i in order if (k, i) not in DROP]
    for f in [f for f in os.listdir(O) if f.startswith(k + '-')]: os.remove(O + f)
    for j, i in enumerate(order, 1): jobs.append((k, j, imgs[i]))
def do(job):
    k, j, u = job
    try:
        im = Image.open(get(u)); im.seek(0); im = im.convert('RGBA'); CUR[0] = k
        # Grind City PNGs pad a white packshot with transparency: flatten onto white so the flood sees one backdrop
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg
        if k.startswith('gc-'): im = im.crop((6, 6, im.width - 6, im.height - 6))  # 1px off-white keyline round the GC packshots blocks the flood
        out = cover(im.convert('RGB')) if k in SOFTK else frame(im)
        p = f'{O}{k}-{j}.jpg'; out.save(p, quality=84, optimize=True); return (k, j, '/' + p)
    except Exception as e: print('ERR', k, j, u, e)
with ThreadPoolExecutor(6) as ex: res = [r for r in ex.map(do, jobs) if r]
fr = {}
for k, j, p in sorted(res, key=lambda r: (r[0], r[1])): fr.setdefault(k, []).append(p)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1); print({k: len(v) for k, v in fr.items()})
