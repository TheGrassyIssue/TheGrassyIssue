"""AAGGG BTK frames. Product shots sit on a pale grey sweep: remap colours near the sweep to TGI stone with a soft weight (no masks, no cutouts). 30 Oct 2026."""
import json, os
import numpy as np
from PIL import Image
O = 'images/angus-grace-go-golfing/'; R = 'research/angus-grace/opt/'; L = 'research/angus-grace/life/'
STONE = np.array((232, 226, 214), float)
def cover(im, w=1000, h=1250, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def stone(path):
    a = np.array(Image.open(path).convert('RGB')).astype(float)
    k = max(4, a.shape[0] // 40); corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    bg = np.median(corners, 0)
    if bg.min() < 200 or (bg.max() - bg.min()) > 14: return Image.fromarray(a.astype(np.uint8))   # not a pale sweep: leave alone
    d = np.abs(a - bg).max(2)
    w = np.clip(1 - d / 28, 0, 1)[..., None]
    out = a * (1 - w) + np.clip(a * (STONE / bg), 0, 255) * w
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))
F = {
 'upf': ['13-0', '4-0', '7-0', '10-0', '11-0'],
 'knit': ['15-0', '16-0', '35-0', '36-0'],
 'cashpolo': ['05-0'],
 'gdtee': ['01-0', '19-0', '33-0'],
 'heavy': ['20-0', '20-1'],
 'crew': ['17-0', '18-0', '17-1'],
 'hoodie': ['02-0'],
 'coach': ['00-0', '32-0', '00-1'],
 'puffer': ['08-0', '08-1'],
 'fleece': ['21-0', '21-1'],
 'shorts': ['09-0', '03-0', '06-0', '22-0', '23-0', '24-0', '25-0'],
 'trouser': ['29-0', '26-0', '27-0', '28-0', '30-0', '31-0'],
 'gdcap': ['12-0', '14-0', '37-0', '47-0', '48-0'],
 'gdaaggg': ['38-0', '39-0'],
 'dogs': ['40-0', '41-0'],
 'fivepanel': ['45-0', '46-0'],
 'visor': ['49-0', '50-0'],
 'bucket': ['34-0', '34-1'],
 'fliers': ['42-0', '43-0'],
 'flierspolo': ['51-0'],
 'agp': ['52-0', '52-1'],
}
FR = {}
for k, srcs in F.items():
    FR[k] = []
    for j, s in enumerate(srcs, 1):
        if s.startswith('LIFE:'): im = Image.open(L + s[5:] + '.jpg').convert('RGB')
        else:
            a, b = s.split('-'); im = stone(f'{R}{int(a):02d}-{b}.img')
        o = f'{O}{k}-{j}.jpg'; cover(im).save(o, quality=86, optimize=True); FR[k].append('/' + o)
json.dump(FR, open('research/angus-grace/frames.json', 'w'), indent=1)
LB = 'AAGGG_Jan_LookBook_-_Hi_Res_-_Take_Studios_-_Jan_2025-'
shop = Image.open(L + 'AAGGG_-_Hi_Res_-_Chad_Konik_-_Feb_2024-4.jpg').convert('RGB')
cover(shop, 2000, 857, .5, .45).save(O + 'hero.jpg', quality=86, optimize=True)
cover(shop, 1200, 630, .5, .5).save(O + 'og.jpg', quality=84)
cover(Image.open(L + 'AGGG_NLU_Excess_Photos-59.jpg').convert('RGB'), 1000, 1250, .5, .4).save(O + 'card-hero.jpg', quality=84, optimize=True)
BANDS = {'band-1': [(LB + '3', .5, .3), (LB + '19', .5, .3), (LB + '7', .5, .5)],
         'band-2': [('AGGG_NLU_Excess_Photos-59', .5, .4), ('WhatsApp_Image_2026-08-05_at_19.59.36', .5, .6), ('WhatsApp_Image_2026-08-06_at_07.30.04', .5, .5)]}
for b, srcs in BANDS.items():
    for i, (s, fx, fy) in enumerate(srcs, 1):
        cover(Image.open(L + s + '.jpg').convert('RGB'), 1000, 1250, fx, fy).save(O + f'{b}-{i}.jpg', quality=84, optimize=True)
print({k: len(v) for k, v in FR.items()})
