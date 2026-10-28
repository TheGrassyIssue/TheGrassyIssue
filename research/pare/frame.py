"""Paré Golf Brand to Know: product frames. 27 Oct 2026. Treatment shared with research/capsules/frame.py.
Lenny: stars + "a section about the sold out stuff, especially the more colorful options" + Prada logo note + "I love the drawing of the guy putting"."""
import json, os, re, urllib.request, time
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R = 'research/pare/'; O = 'images/pare-golf/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True); os.makedirs(R + 'raw', exist_ok=True)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
CAT = {p['handle']: p for p in json.load(open(R + 'catalogue.json'))['products']}
def im(h, *idx): return [(h, i) for i in idx]
CARDS = {
 # 27 Oct (Lenny: "the first section needs more products"): one card per Imperial colourway, product shot first
 'imp-walnut': im('pare-x-imperial-manila-hat-walnut', 1, 0, 2, 3),
 'imp-white': im('pare-x-imperial-manila-hat-white', 0, 2, 1),
 'imp-black': im('pare-x-imperial-manila-hat-black', 1, 0, 2),
 'imp-olive': im('pare-x-imperial-manila-hat-olive', 1, 0, 2),
 'manila-ls': im('pare-manila-long-sleeve-shirt', 1, 0, 2),
 'manila-nylon': im('pare-manila-nylon-hat', 0, 1, 2),
 'manila-visor': im('hypegolf-exclusive-pare-manila-tour-visor', 0, 1, 2, 3),
 'manila-mock': im('pare-manila-mockneck-shirt', 0, 1, 2),
 'bt-driver': im('pare-x-bluetross-driver-headcover', 0, 1, 2, 3),
 'bt-putter': im('pare-x-bluetross-blade-putter-headcover', 0, 1, 2, 3),
 'paretex': im('pare-tex-waterproof-5-panel-long-bill-hat', 0, 1, 2, 3, 4),
 'maganda': im('pare-maganda-ang-buhay-mockneck-shirt', 0, 1, 2),
 'sock': im('pare-logo-crew-sock-v2', 0, 1, 2),
 'club': im('pare-club-shirt', 0, 1, 2, 3, 4),
 'wind': im('pare-cool-grey-short-sleeve-wind-shirt', 0, 1, 2, 3),
 'plisse2': im('pare-plisse-pants-2-0', 0, 1, 2, 3),
 'plisse': im('pare-plisse-pants', 0, 1, 2, 3),
 'adobo': im('pare-adobo-mockneck-shirt', 0, 1, 2),
 'forgood': im('pare-for-good-long-sleeve-shirt', 0, 1, 2, 3),
 'eldrick': im('pare-blonde-eldrick-long-sleeve-shirt', 0, 1, 2),
 'gulay': im('pare-gulay-hooded-pullover-sweatshirt', 0, 1, 2, 3),
 'logotee': im('pare-classic-new-york-logo-t-shirt', 0, 1, 2, 3),
 'am94': im('pare-94-am-sensation-mockneck', 0, 1, 2, 3, 4),
 'azalea': im('pare-azalea-mockneck', 0, 1, 2),
 'eggsalad': im('pare-egg-salad-mockneck', 0, 1, 2),
 'magnolia': im('pare-magnolia-mockneck', 0, 1, 2, 3),
 'faces': im('pare-faces-rope-hat', 0, 1, 2, 3, 4),
 'maasim': im('pare-maasim-nylon-hat', 0, 1),
 'pakwan': im('pare-pakwan-snapback-hat', 0, 1, 2),
 'pink': im('pare-pink-nylon-hat', 0, 1, 2, 3),
 'barnabys': im('barnabys-x-pare-driver-headcover', 0, 1, 2, 3),
 'mogshade': im('pare-x-mogshade-driver-headcover', 0, 1),
 'toddler': im('little-sundays-x-pare-toddler-golf-bag', 0, 1, 2, 3, 4),
 'sunflower': im('sunflower-mockneck-long-sleeve-shirt', 0, 1),
 'pgg': im('pare-x-paris-golf-gallery-snapback-hat', 0, 1, 2, 3),
 'camphat': im('5-panel-camp-hat', 0),
}
def url(h, i):
    imgs = CAT[h]['images']; return (imgs[i]['src'] if isinstance(imgs[i], dict) else imgs[i]) if i < len(imgs) else None
def fn(u): p = u.split('?')[0].split('/'); return R + 'raw/' + re.sub(r'[^A-Za-z0-9_.-]', '_', p[-1])[-90:]
def get(u):
    f = fn(u)
    if not os.path.exists(f):
        for t in range(3):
            try: open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u + '?width=1600', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read()); break
            except Exception: time.sleep(3)
    return f
ONLY = set(os.environ.get('ONLY', '').split(',')) - {''}
jobs = []
for k, lst in CARDS.items():
    if ONLY and k not in ONLY: continue
    for j, (h, i) in enumerate([x for x in lst if url(*x)], 1): jobs.append((k, j, url(h, i)))
def do(job):
    k, j, u = job
    try:
        img = Image.open(get(u)); img.seek(0); img = img.convert('RGBA'); bg = Image.new('RGBA', img.size, (255, 255, 255, 255)); bg.alpha_composite(img)
        CUR[0] = k; out = frame(bg.crop((2, 2, bg.width - 2, bg.height - 2))); p = f'{O}{k}-{j}.jpg'; out.save(p, quality=84, optimize=True); return (k, j, '/' + p)
    except Exception as e: print('ERR', k, j, u, e)
with ThreadPoolExecutor(4) as ex: res = [r for r in ex.map(do, jobs) if r]
fr = json.load(open(R + 'frames.json')) if ONLY else {}
for k in ONLY: fr.pop(k, None)
fr.pop('imperial', None)
for k, j, p in sorted(res, key=lambda r: (r[0], r[1])): fr.setdefault(k, []).append(p)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1); print({k: len(v) for k, v in fr.items()})
