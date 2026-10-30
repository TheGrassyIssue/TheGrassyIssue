"""Pinned Golf BTK frames: lifestyle first where Pinned has it, product renders cut out onto stone. 30 Oct 2026."""
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, 'research/pinned'); from gcut import cutout, bg_flat
from soft import soft
R = 'research/pinned/raw/'; L = 'research/pinned/life/'; O = 'images/pinned-golf/'; os.makedirs(O, exist_ok=True)
def cover(f, w=1000, h=1250, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
F = {
 'prism': [R+'prism-1', R+'prism-2', R+'prism-3', R+'prism-4'], 'caddie': [L+'3_0e5b3a97-c390-4f29-bcc9-9f61ad3bcfb5', R+'caddie-2'],
 'sspro': [L+'SSProPDP_1', R+'sspro-1', R+'sspro-2'], 'sstick': [R+'sstick-1', L+'11_8d2b66f4-fda1-439d-a51f-f77e963f44d7', R+'sstick-2', R+'sstick-3'],
 'dart': [R+'dart-1', R+'dart-2', R+'dart-3'], 'roller': [R+'roller-1', R+'roller-2', R+'roller-3'],
 'stickpro': [R+'stickpro-1', R+'stickpro-2', R+'stickpro-3'], 'stick': [R+'stick-1', R+'stick-2', R+'stick-3'],
 'combo': [R+'combo-1', R+'combo-2', R+'combo-3'], 'comboplus': [R+'comboplus-1', R+'comboplus-2', R+'comboplus-3'],
 'mount': [R+'mount-2', R+'mount-1'], 'magpad': [R+'magpad-1'], 'markers': [R+'markers-4', R+'markers-1', R+'markers-2', R+'markers-3'],
 'towels': [R+'towels-1', R+'towels-2', R+'towels-3'], 'hats': [L+'Untitled_267_x_363_px_1', R+'hats-1', R+'hats-2', R+'hats-3'],
 'charger': [R+'charger-2', R+'charger-3'], 'prcase': [R+'prcase-1', R+'prcase-3'], 'spcase': [R+'spcase-1', R+'spcase-2'],
}
FR = {}
for k, srcs in F.items():
    FR[k] = []
    for j, s in enumerate(srcs, 1):
        f = s + '.jpg'; a = np.array(Image.open(f).convert('RGB')).astype(float); flat, col = bg_flat(a)
        im = soft(f, .78, .7) if (flat and col.min() > 230) else None
        if im is None: im = cover(f)
        o = f'{O}{k}-{j}.jpg'; im.save(o, quality=86, optimize=True); FR[k].append('/' + o)
json.dump(FR, open('research/pinned/frames.json', 'w'), indent=1)
# hero + card + bands
cover(L + '6_b66d7fdf-e0a1-4143-8778-507db6c39faf.jpg', 2000, 857, .5, .5).save(O + 'hero.jpg', quality=86, optimize=True)
cover(L + '6_b66d7fdf-e0a1-4143-8778-507db6c39faf.jpg', 1200, 630, .5, .5).save(O + 'og.jpg', quality=84)
cover(L + '6_b66d7fdf-e0a1-4143-8778-507db6c39faf.jpg', 1000, 1250, .5, .5).save(O + 'card-hero.jpg', quality=84, optimize=True)
BANDS = {'band-1': ['7d1e604b0156ec6d54771524c61774952c1ff9e0', '9fdc09d7633136be5e843571a29097a6772741f2', 'eb1648a50334d31cf43c5a3d3ab1a4fed53e178c'],
         'band-2': ['Untitled_design_44', '77bf3bb6aa755b874adaa5707f41c04ed0d308e9', 'Untitled_design_48'],
         'band-3': ['9_d17ad31c-a493-4492-afdc-08310bd39ca9', '7_f5af5ce4-272b-443d-980e-93e5b43322a4', 'e821ac0571f699cd7fc25d8f2c8d9641c3e15202_1']}
BFY = {'7d1e604b0156ec6d54771524c61774952c1ff9e0': .35, '9fdc09d7633136be5e843571a29097a6772741f2': .3, 'eb1648a50334d31cf43c5a3d3ab1a4fed53e178c': .3, 'Untitled_design_44': .5}
BFX = {'9_d17ad31c-a493-4492-afdc-08310bd39ca9': .55, '7_f5af5ce4-272b-443d-980e-93e5b43322a4': .5, '77bf3bb6aa755b874adaa5707f41c04ed0d308e9': .45}
for b, srcs in BANDS.items():
    for i, s in enumerate(srcs, 1):
        cover(L + s + '.jpg', 1000, 1250, BFX.get(s, .5), BFY.get(s, .5)).save(O + f'{b}-{i}.jpg', quality=84, optimize=True)
print({k: len(v) for k, v in FR.items()})
