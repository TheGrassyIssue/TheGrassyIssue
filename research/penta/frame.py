"""Penta Golf BTK frames + bands + hero. 28 Oct 2026. Reuses the capsule frame() (white studio -> stone)."""
import json, glob, re
from PIL import Image
src = open('research/capsules/frame.py').read(); src = src[:src.index('\nfr = {}')]
src = src.replace("os.makedirs(O, exist_ok=True)", "")
exec(src)
O = 'images/penta-golf/'
R = 'research/penta/raw/'
K = {  # key: (handle, image indexes)
 'grid-lush': ('pentaxbarnabys-grid-polo-lush-ice', [0,1,2,4]),
 'grid-sorbet': ('penta-x-barnabys-grid-polo-lemon-sorbet', [0,1,2,4]),
 'glove-green': ('penta-x-barnabys-hand-in-hand-glove-green-silver', [0,1,2,3]),
 'glove-salt': ('penta-x-barnabys-hand-in-hand-glove-salt-silver', [0,1,2,3]),
 'blade': ('penta-x-barnabys-blade-putter-cover', [0,1]),
 'optical': ('penta-golf-polo-optical', [0,2,3,4]),
 'metal': ('penta-golf-polo-metal', [0,1,2]),
 'digital': ('penta-golf-polo-digital', [0,1,2,3]),
 'jersey': ('penta-golf-jersey', [0,1,2,3]),
 'hazard-moss': ('hazard-short-moss', [0,1,2,3]),
 'hazard-black': ('hazard-short-black', [0,1,2,3]),
 'etiquette': ('etiquette-pants', [0,1,2,3]),
 'footwork': ('footwork-tee-navy', [0,1]),
 'gear': ('gear-specialist-tee', [0,1]),
 'cap-navy': ('players-cap-navy', [0,1,2]),
 'cap-bone': ('off-course-cap-bone', [0,1,2]),
 'cap-black': ('players-cap-black', [0,1,2,3]),
 'elements-black': ('penta-elements-jacket', [0,1,2,3]),
 'elements-butter': ('penta-elements-jacket-butter', [0,1,2,3]),
 'member': ('member-trunks', [0,1,2,3]),
}
FR = {}
for k, (h, ix) in K.items():
    out = []
    for j, i in enumerate(ix, 1):
        f = glob.glob(f'{R}{h}-{i}.*')[0]
        frame(load(f)).save(f'{O}{k}-{j}.jpg', quality=86, optimize=True); out.append(f'/{O}{k}-{j}.jpg')
    FR[k] = out
json.dump(FR, open('research/penta/frames.json', 'w'), indent=1)
def cover(f, w, h, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
OR = 'research/penta/orig/'
hero = cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 2000, 857, .35); hero.save(O + 'hero.jpg', quality=86, optimize=True)
cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 1200, 630, .3).save(O + 'og.jpg', quality=84)
cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 1000, 1250, .5).save(O + 'card-hero.jpg', quality=84, optimize=True)
B = {'band-metal-sun': ('Metal-1.webp', .3), 'band-metal-beach': ('metal-3.webp', .5), 'band-digital': ('Digital-1.webp', .5),
     'band-swing': ('moss-3_8e3f7575-ccd1-4142-b50b-af89270c2d70.webp', .5), 'band-bunker': ('moss-1_76bbacc5-a77e-4c06-a347-20b9f126dca5.webp', .5),
     'band-black': ('hazard-black-3.webp', .5), 'band-cap': ('Players-Cap-Navy-1.webp', .4)}
for n, (f, fy) in B.items(): cover(OR + f, 1000, 1250, fy).save(O + n + '.jpg', quality=84, optimize=True)
print('ok', len(FR))
