"""Fyfe Golden Restless Age: product frames (GrabCut cut-outs on stone), lookbook resizes, hero. 29 Oct 2026."""
import json, glob, os, sys
from PIL import Image
src = open('research/capsules/frame.py').read(); src = src[:src.index('\nfr = {}')].replace("os.makedirs(O, exist_ok=True)", "")
exec(src)
sys.path.insert(0, 'research/fyfe-gra'); from gcut import cutout
O = 'images/fyfe-golden-restless-age/'; R = 'research/fyfe-gra/'
FR = {}
for k, t, p, u, imgs in json.load(open(R + 'cards.json')):
    out = []
    for j in range(1, len(imgs) + 1):
        f = f'{R}raw/{k}-{j}.jpg'; o = f'{O}{k}-{j}.jpg'
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
cover(L + 'GRA_On_Course-5.jpg', 2000, 857, .5, .55).save(O + 'hero.jpg', quality=86, optimize=True)
cover(L + 'GRA_On_Course-5.jpg', 1200, 630, .5, .5).save(O + 'og.jpg', quality=84)
cover(L + 'GRA_Car_Shots-82.jpg', 1000, 1250).save(O + 'card-hero.jpg', quality=84, optimize=True)
for f in glob.glob(L + '*.jpg'):
    im = Image.open(f).convert('RGB'); im.thumbnail((1800, 1800), Image.LANCZOS)
    im.save(O + 'lb-' + os.path.basename(f).lower().replace('_', '-'), quality=84, optimize=True)
print('ok', len(FR))
