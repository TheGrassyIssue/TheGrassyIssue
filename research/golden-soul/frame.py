"""Golden Soul Golf BTK frames + bands + hero. 28 Oct 2026. Product shots are on a warm cream sweep: run through the capsule frame()."""
import json, glob, subprocess, os, re
from PIL import Image
src = open('research/capsules/frame.py').read(); src = src[:src.index('\nfr = {}')].replace("os.makedirs(O, exist_ok=True)", "")
exec(src)
O = 'images/golden-soul-golf/'; R = 'research/golden-soul/'
sel = json.load(open(R + 'options.json'))
FR = {}
for i, c in enumerate(sel, 1):
    k = re.sub(r'[^a-z0-9]+', '-', c['t'].lower()).strip('-')
    c['key'] = k; out = []
    for j, u in enumerate(c['imgs'][:4], 1):
        f = f'{R}raw/{k}-{j}.jpg'
        if not os.path.exists(f) or os.path.getsize(f) < 1000: subprocess.run(['curl', '-s', '-m', '40', '-o', f, u + '?format=1500w'])
        if os.path.exists(f'{O}{k}-{j}.jpg'): out.append(f'/{O}{k}-{j}.jpg'); continue
        try: frame(load(f)).save(f'{O}{k}-{j}.jpg', quality=86, optimize=True); out.append(f'/{O}{k}-{j}.jpg')
        except Exception as e: print('skip', f, e)
    FR[k] = out
json.dump(sel, open(R + 'options.json', 'w'), indent=1)
json.dump(FR, open(R + 'frames.json', 'w'), indent=1)
L = R + 'look/'
def cover(f, w, h, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
cover(L + 'l05.jpg', 2000, 857, .5, .45).save(O + 'hero.jpg', quality=86, optimize=True)
cover(L + 'l05.jpg', 1200, 630, .5, .4).save(O + 'og.jpg', quality=84)
cover(L + 'l06.jpg', 1000, 1250).save(O + 'card-hero.jpg', quality=84, optimize=True)
for n in ['02','03','04','06','17','18','19','20','21','22','23','24','25','26','27','31','32','34','35','36','37','40','44','39','01']:
    cover(L + f'l{n}.jpg', 1000, 1250).save(O + f'look-{n}.jpg', quality=84, optimize=True)
print('ok', len(FR))
