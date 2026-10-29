"""Fall pants 2026 frames, bands, hero. 29 Oct 2026."""
import json, glob, os
from PIL import Image
src = open('research/capsules/frame.py').read(); src = src[:src.index('\nfr = {}')].replace("os.makedirs(O, exist_ok=True)", "")
exec(src)
O = 'images/fall-pants-2026/'; R = 'research/fall-pants/'
F = json.load(open(R + 'final.json')); FR = {}
for c in F:
    out = []
    for j in range(1, len(c['imgs']) + 1):
        f = glob.glob(f'{R}raw/{c["k"]}-{j}.*')[0]; o = f'{O}{c["k"]}-{j}.jpg'
        if not os.path.exists(o): frame(load(f)).save(o, quality=86, optimize=True)
        out.append('/' + o)
    FR[c['k']] = out[:5]
json.dump(FR, open(R + 'frames.json', 'w'), indent=1)
def cover(f, w, h, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
H = R + 'raw/walker-easy-2.jpg'
cover(H, 2000, 857, .5, .62).save(O + 'hero.jpg', quality=86, optimize=True)
cover(H, 1200, 630, .5, .6).save(O + 'og.jpg', quality=84)
cover(H, 1000, 1250).save(O + 'card-hero.jpg', quality=84, optimize=True)
for n in ['pd-charcoal-2', 'pd-pinstripe-2', 'odd-ritual-daily-2', 'sloat-caddie-2', 'metalwood-western-4', 'students-tradition-2', 'walker-easy-4', 'malbon-scouting-3', 'pd-pinstripe-4']:
    cover(glob.glob(f'{R}raw/{n}.*')[0], 1000, 1250).save(O + f'band-{n}.jpg', quality=84, optimize=True)
print('ok')
