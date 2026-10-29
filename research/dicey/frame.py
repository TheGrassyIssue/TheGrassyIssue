"""Dicey Golf BTK frames, bands, hero. 29 Oct 2026."""
import json, glob, os
from PIL import Image
src = open('research/capsules/frame.py').read(); src = src[:src.index('\nfr = {}')].replace("os.makedirs(O, exist_ok=True)", "")
exec(src)
import sys; sys.path.insert(0, 'research/dicey'); from gcut import cutout  # Lenny 29 Oct: filters were bleeding into the cream polos
O = 'images/dicey-golf/'; R = 'research/dicey/'
FR = {}
for k, t, p, u, imgs in json.load(open(R + 'cards.json')):
    out = []
    for j in range(1, len(imgs) + 1):
        f = glob.glob(f'{R}raw/{k}-{j}.*')[0]; o = f'{O}{k}-{j}-v2.jpg'
        if not os.path.exists(o):
            c = cutout(f)
            (c if c is not None else frame(load(f))).save(o, quality=86, optimize=True)
        out.append('/' + o)
    FR[k] = out
json.dump(FR, open(R + 'frames.json', 'w'), indent=1)
def cover(f, w, h, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
L = R + 'look/'
H = L + 'LREdit_97_of_164_1_1.jpg'
cover(H, 2000, 857, .5, .6).save(O + 'hero.jpg', quality=86, optimize=True)
cover(H, 1200, 630, .5, .55).save(O + 'og.jpg', quality=84)
cover(H, 1000, 1250, .5, .5).save(O + 'card-hero.jpg', quality=84, optimize=True)
for n in ['LREDIT_95_of_356', 'LREdit_316_of_324', 'LREdit_20_of_27_1_4', 'group19_3', 'camo_polo_fixed_2', 'black_hat_2', 'DSC02811', 'Main_Header', 'use_for_fairway', 'Draft_Day_Mobile_Header', 'wholesale_banner', 'eg8', 'seaside_2', 'polo_1_7ea6964a-7584-4a39-8994-02b4ea00c01c']:
    cover(L + n + '.jpg', 1000, 1250).save(O + 'look-' + n.lower().replace('_','-')[:24] + '.jpg', quality=84, optimize=True)
print('ok')
