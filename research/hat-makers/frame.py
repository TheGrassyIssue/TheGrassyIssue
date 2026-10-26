"""Three hat makers with momentum: product frames. 25 Oct 2026. Treatment shared with research/capsules/frame.py.
Lenny 25 Oct: "build it" on the starred picks (hat-makers-options.html): 6 per brand."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/hat-makers/'; O = 'images/hat-makers/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
CAT = {c['code']: c for c in json.load(open(R + 'catalogue.json'))}
# card key -> (catalogue code, image indexes). Multi-colour hats lead with one packshot per colourway.
CARDS = {
 'dang': ('C11', [0, 4, 8, 11, 1]),
 'anchor': ('C12', [0, 1, 2, 3, 4]),
 'trading': ('C14', [0, 1, 2, 3, 4]),
 'captain': ('C13', [0, 1, 2, 3]),
 'martini': ('C8', [0, 1, 2, 3]),
 'eagle': ('C3', [0, 2, 4, 6, 1]),
 'eatdirt': ('D4', [0, 1, 2, 3, 5]),
 'chateau': ('D5', [0, 1, 2, 3]),
 'pitstop': ('D2', [0, 1, 2, 3, 4]),
 'dukeblack': ('D1', [0, 1, 2, 3]),
 'trucker': ('D7', [0, 1, 2, 3]),
 'dukegreen': ('D3', [0, 1, 2, 3]),
 'whitney': ('W1', [0, 1]),
 'yellow': ('W2', [0, 1, 2]),
 'mesh': ('W3', [0, 1, 2]),
 'amtrucker': ('W4', [0, 1]),
 'cord': ('W5', [0, 1, 2, 3, 4]),
 'weathered': ('W7', [0, 1, 2, 3, 4]),
}
def fn(u): return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', u.split('?')[0].rsplit('/', 1)[-1])[-90:]
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u.split('?')[0] + '?width=1600', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    return f
jobs = []
for k, (code, idx) in CARDS.items():
    imgs = CAT[code]['imgs']
    for j, i in enumerate([i for i in idx if i < len(imgs)], 1): jobs.append((k, j, imgs[i]))
def do(job):
    k, j, u = job
    try:
        im = Image.open(get(u)); im.seek(0); im = im.convert('RGBA'); CUR[0] = k
        out = frame(im); p = f'{O}{k}-{j}.jpg'; out.save(p, quality=84, optimize=True); return (k, j, '/' + p)
    except Exception as e: print('ERR', k, j, u, e)
with ThreadPoolExecutor(6) as ex: res = [r for r in ex.map(do, jobs) if r]
fr = {}
for k, j, p in sorted(res, key=lambda r: (r[0], r[1])): fr.setdefault(k, []).append(p)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1); print({k: len(v) for k, v in fr.items()})
