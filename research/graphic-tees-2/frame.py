"""Graphic Tee Edit Vol. 2: tee-wall frames. Primary = the graphic (flat where the brand has one), hover = other side / on-model.
Flats on flat light backgrounds are cut out onto stone (GrabCut), so the wall reads as one set; everything else is cover-cropped. 29 Oct 2026."""
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, 'research/graphic-tees-2'); from gcut import cutout, bg_flat
R = 'research/graphic-tees-2/raw/'; O = 'images/graphic-tee-edit-vol-2/'; os.makedirs(O, exist_ok=True)
def cover(f, w=1000, h=1250, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
PICK = {  # v2: lead with on-model / IRL where the brand has it; flat graphic on hover
 'dicey-booze': [3, 1], 'dicey-19th': [5, 1], 'dev-highway': [4, 1], 'hin-wild': [3, 1], 'hin-redwing': [3, 1], 'hin-koi': [3, 1],
 'hin-river': [3, 1], 'gg-story': [1], 'gg-gilmore': [1, 2], 'gg-gimme': [1, 3], 'palm-rhythm': [1, 3], 'palm-cart': [3, 1],
 'saha-drive': [1, 2], 'axxa-manly': [2, 1], 'axxa-cold': [2, 1], 'axxa-surf': [1, 2], 'sa-trynot': [1, 2], 'sa-justgolf': [5, 1],
 'mog-human': [1, 3], 'pw-roll': [4, 3], 'pw-deepcuts': [4, 1], 'malbon-gd': [5, 1], 'hls-faster': [2, 1],
 'dicey-ice': [4, 1], 'dicey-camo': [4, 1], 'gg-brogey': [1], 'gg-swing': [1], 'sa-nascart': [1], 'walker-rodeo': [2, 1],
 'students-swang': [2, 1], 'pw-toon': [1, 2], 'parm-motor': [1, 2], 'parm-nmr': [2, 1], 'winslow': [4, 1], 'both-fade': [2, 1], 'both-malibu': [2, 1],
 'lazy-frank': [2, 1], 'saha-knight': [1], 'dicey-maroon': [2, 1],
}
FY = {('dicey-maroon', 2): .3, ('hin-wild', 3): .4, ('hin-redwing', 3): .4, ('dicey-booze', 3): .4, ('dicey-19th', 5): .4, ('dev-highway', 4): .3, ('pw-roll', 4): .4, ('pw-deepcuts', 4): .4, ('malbon-gd', 5): .3, ('dicey-ice', 4): .3, ('dicey-camo', 4): .3, ('palm-cart', 3): .4, ('axxa-manly', 2): .3, ('walker-rodeo', 2): .35, ('students-swang', 2): .3, ('parm-motor', 1): .4, ('parm-nmr', 2): .3, ('both-fade', 2): .3, ('both-malibu', 2): .3,
      ('axxa-cold', 1): .35, ('axxa-cold', 2): .35, ('axxa-surf', 1): .35, ('axxa-surf', 2): .35, ('mog-human', 1): .3, ('winslow', 4): .3}
FR, MODE = {}, {}
for k, ns in PICK.items():
    FR[k] = []
    for j, n in enumerate(ns, 1):
        f = f'{R}{k}-{n}.jpg'; a = np.array(Image.open(f).convert('RGB')).astype(float); flat, col = bg_flat(a)
        im = cutout(f, .86, .82) if flat else None
        MODE[f'{k}-{n}'] = 'cut' if im is not None else 'cover'
        if im is None: im = cover(f, fy=FY.get((k, n), .5))
        o = f'{O}{k}-{j}.jpg'; im.save(o, quality=86, optimize=True); FR[k].append('/' + o)
json.dump(FR, open('research/graphic-tees-2/frames.json', 'w'), indent=1)
print(sum(v == 'cut' for v in MODE.values()), 'cut of', len(MODE))
# v2 hero: three on-model back prints, side by side
tri = [('hin-wild-4', .45), ('axxa-cold-1', .4), ('dev-highway-2', .3)]
h = Image.new('RGB', (2000, 857), (232, 226, 214)); x = 0
for (src, fy), w in zip(tri, (666, 668, 666)):
    h.paste(cover(R + src + '.jpg', w - 4 if x else w - 2, 857, .5, fy), (x + (2 if x else 0), 0)); x += w
h.save(O + 'hero.jpg', quality=86, optimize=True)
og = h.resize((1200, 514), Image.LANCZOS); c = Image.new('RGB', (1200, 630), (232, 226, 214)); c.paste(og, (0, 58)); c.save(O + 'og.jpg', quality=84)
cover(R + 'hin-wild-4.jpg', 1000, 1250, .5, .45).save(O + 'card-hero.jpg', quality=84, optimize=True)
# lookbook bands (3-up), none of these are a tile's lead image
BANDS = {'band-1': ['hin-redwing-4', 'hin-wild-5', 'axxa-surf-2'], 'band-2': ['axxa-manly-5', 'dev-highway-3', 'malbon-gd-4'],
         'band-3': ['hin-redwing-5', 'students-swang-3', 'axxa-manly-3'], 'band-4': ['both-fade-4', 'dicey-ice-3', 'walker-rodeo-5']}
BFY = {'axxa-manly-3': .3, 'walker-rodeo-5': .35, 'axxa-surf-2': .35, 'dev-highway-3': .3, 'dev-highway-4': .3, 'students-swang-3': .3, 'students-swang-4': .3, 'both-fade-4': .3, 'axxa-manly-5': .35, 'malbon-gd-4': .3}
for b, srcs in BANDS.items():
    for i, src in enumerate(srcs, 1):
        cover(R + src + '.jpg', 1000, 1250, .5, BFY.get(src, .45)).save(O + f'{b}-{i}.jpg', quality=84, optimize=True)
