"""Fyfe GRA v2: product cards lead with the brand's own IRL / on-model shots; studio cut-outs (handle-safe GrabCut) only where no IRL shot exists. 29 Oct 2026."""
import json, os, sys
from PIL import Image
sys.path.insert(0, 'research/fyfe-gra'); from gcut import cutout
O = 'images/fyfe-golden-restless-age/'; R = 'research/fyfe-gra/'
IRL = {
 'mackenzie-24': ['look/GRA_Car_Shots-46', 'look/GRA_Car_Shots-85', 'look/GRA_MACS-10'],
 'weekender': ['look/DUFFELLS_ETC-12', 'look/DUFFELLS_ETC-10'],
 'shoe-bag': [], 'glove-caddy': [],
 'player-crew': ['look/GRA_Car_Shots-82', 'look/GRALOCKERROOM-16', 'look/GRA_On_Course-12', 'irl/GRAOnCourse-32', 'irl/GRA_Dining_Room-36'],
 'shawl': ['look/CLUBHOUSE-SHAWL-GRA-LOCKER-ROOM-8', 'look/GRA_Dining_Room-39', 'irl/CLUBHOUSE-SHAWL-BUTTON-GRA-LOCKER-ROOM-11'],
 'diary': ['look/GRA_BOOKS_HOLDERS-25'],
 'keeper': ['look/GRA_BOOKS_HOLDERS-12', 'look/GRA_BOOKS_HOLDERS-5'],
}
PD = {'carlogie': [8, 9, 298, 274], 'burnside': [26, 320, 312, 305], 'auchmithie': [55, 141, 100, 126], 'airlie': [258, 254, 17, 244],
      'broughty': [36, 46, 195, 292, 280], 'monikie': [165, 174, 112, 294], 'edzell': [22, 'GRA_PDP_HEAD_COVERS-54', 278, 286],
      'glamis': [118, 109, 42, 302, 272], 'tealing': [130, 136, 204, 207], 'letham': ['GRA_PDP_HEAD_COVERS-70', 288, 311],
      'brechin': [95, 96, 43, 276, 314], 'gt-vanquish': [175, 178, 5, 15]}
for k, v in PD.items(): IRL[k] = [f'irl/pd-{n}' if isinstance(n, int) else f'irl/{n}' for n in v]
STUDIO = {'mackenzie-24': [1], 'weekender': [1, 3], 'shoe-bag': [1, 2, 3], 'glove-caddy': [1, 2, 3, 4], 'shawl': [1], 'diary': [1, 2], 'keeper': [1]}
def cover(f, w=1000, h=1250, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
FR = {}
for k, t, p, u, imgs in json.load(open(R + 'cards.json')):
    out = []
    for j, src in enumerate(IRL[k], 1):
        o = f'{O}{k}-irl-{j}.jpg'; cover(R + src + '.jpg').save(o, quality=84, optimize=True); out.append('/' + o)
    for j in STUDIO.get(k, []):
        o = f'{O}{k}-v2-{j}.jpg'; c = cutout(f'{R}raw/{k}-{j}.jpg'); assert c is not None, (k, j)
        c.save(o, quality=86, optimize=True); out.append('/' + o)
    FR[k] = out
json.dump(FR, open(R + 'frames.json', 'w'), indent=1)
print({k: len(v) for k, v in FR.items()})
