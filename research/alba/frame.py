"""Alba Golf BTK frames. 25 Oct 2026. All 24 products, colorways grouped into 16 cards.
Shopify gallery pattern: _01 flat-lay, _02_hover full length, _03/_04 on-model, _05 detail. On-model first (Lenny 25 Oct).
Frame treatment shared with research/capsules/frame.py (grey studio sweep warmed toward stone)."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/alba/'; O = 'images/alba-golf/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read()
exec(src[src.index('SOFT ='):src.index('fr = {}')])
d = json.load(open(R + 'catalogue.json')); P = {p['handle']: p for p in d['products']}
CARDS = {
 'crest': ['crest-jacket'], 'shire': ['shire-quarter-zip-jacket'],
 'glen': ['glen-padded-vest-in-salmon', 'glen-padded-vest-in-chocolate-brown', 'glen-padded-vest-in-ivory'],
 'haar': ['haar-reversible-vest-in-navy-blue', 'haar-reversible-vest-in-black'],
 'grianls': ['grian-ls-quarter-zip-polo'], 'grianss': ['grian-ss-quarter-zip-polo'],
 'cheviot': ['cheviot-mockneck-in-melange-beige', 'cheviot-mockneck-in-black'],
 'voarls': ['voar-ls-polo-in-mauve', 'voar-ls-polo-in-ivory'], 'voarss': ['voar-ss-polo'],
 'rime': ['rime-thermal-layer'],
 'nevis': ['nevis-tech-trouser-in-mud', 'nevis-tech-trouser-in-ivory', 'nevis-tech-trouser-in-black'],
 'roy': ['roy-tech-shorts-in-mud', 'roy-tech-shorts-in-black'],
 'driver': ['alba-barrel-driver-wood-cover-in-black'], 'fairway': ['alba-barrel-fairway-wood-cover-in-black'],
 'pouch': ['alba-pouch-in-black'], 'towel': ['alba-caddie-towel-in-off-white-black'],
}
RANK = {'_03': 0, '_02': 1, '_04': 2, '_01': 3, '_05': 4}
def rank(u):
    for k, v in RANK.items():
        if k in u.rsplit('/', 1)[-1]: return v
    return 5
def fn(u): return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', u.rsplit('/', 1)[-1].split('?')[0])
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        uu = u.split('?')[0] + '?width=1600'
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(uu, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
allu = [u for hs in CARDS.values() for h in hs for u in P[h]['images']]
with ThreadPoolExecutor(8) as ex: list(ex.map(get, allu))
fr = {}
for key, hs in CARDS.items():
    per = [sorted(P[h]['images'], key=rank) for h in hs]
    if len(hs) == 1:
        seq = per[0][:5]
    else:  # lead on-model shot of each colour first, then the first colour's other views
        seq = [p[0] for p in per] + [u for u in per[0][1:]]
        seq = seq[:6]
    for j, u in enumerate(seq, 1):
        out = f'{O}{key}-{j}.jpg'; frame(Image.open(fn(u)).convert('RGBA')).save(out, quality=84, optimize=True); fr.setdefault(key, []).append('/' + out)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1)
# lifestyle / campaign
L = json.load(open(R + 'lifestyle.json'))
for i, x in enumerate(L):
    try:
        get(x['url']); im = Image.open(fn(x['url'])).convert('RGBA'); bg = Image.new('RGBA', im.size, STONE + (255,)); bg.alpha_composite(im)
        im = bg.convert('RGB'); im.thumbnail((2000, 2000)); im.save(f'{O}lb-{i}.jpg', quality=86, optimize=True)
    except Exception as e: print('lb', i, e)
print({k: len(v) for k, v in fr.items()})
