"""Outfit boards + hero for the capsule wardrobe post. 25 Oct 2026. Each look = the capsule's own pieces, first (or chosen) frame of each."""
import json
from PIL import Image, ImageDraw
O = 'images/capsule-wardrobe/'; STONE = (232, 226, 214); INK = (20, 20, 20)
fr = json.load(open('research/capsules/frames.json'))
BOARD_FRAME = {'cl2': 2, 'ou1': 5, 'ou8': 5, 'ou9': 5, 'co1': 2}  # 1-based frame to use on boards when frame 1 isn't the clearest view
LOOKS = json.load(open('research/capsules/looks.json'))
def tile(k, w, h):
    f = fr[k][min(BOARD_FRAME.get(k, 1), len(fr[k])) - 1]
    im = Image.open(f.lstrip('/')).convert('RGB'); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))
def tile_f(f, w, h):
    im = Image.open(f.lstrip('/')).convert('RGB'); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))
# 2x2 boards (Lenny, 25 Oct: "format the four outfits box better, maybe 2x2 images"). Looks with fewer than four pieces
# fill the spare cells with another photo of a piece in the same look (on-model shots first), never a piece from outside it.
for cap, looks in LOOKS.items():
    for n, (name, keys, _) in enumerate(looks, 1):
        files = [fr[k][min(BOARD_FRAME.get(k, 1), len(fr[k])) - 1] for k in keys]
        spare = [f for k in keys for f in fr[k][1:] if f not in files]
        while len(files) < 4 and spare: files.append(spare.pop(0))
        files = files[:4]
        W, H, pad, gap = 1200, 1500, 0, 14
        tw = (W - 2 * pad - gap) // 2; th = (H - 2 * pad - gap) // 2
        c = Image.new('RGB', (W, H), STONE); d = ImageDraw.Draw(c)
        for i, f in enumerate(files):
            x = pad + (i % 2) * (tw + gap); y = pad + (i // 2) * (th + gap)
            c.paste(tile_f(f, tw, th), (x, y))
        c.save(f'{O}look-{cap}-{n}.jpg', quality=85, optimize=True)
# hero: one lifestyle frame per capsule, five panels
HERO = [('cl6', 2), ('st1', 3), ('to5', 2), ('ou2', 3), ('co2', 3)]
def hero(W, H, gap):
    c = Image.new('RGB', (W, H), INK); pw = (W - 4 * gap) // 5
    for i, (k, j) in enumerate(HERO):
        w = pw if i < 4 else W - 4 * (pw + gap)
        im = Image.open(fr[k][j - 1].lstrip('/')).convert('RGB'); s = max(w / im.width, H / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS); x = (im.width - w) // 2; y = int((im.height - H) * .35)
        c.paste(im.crop((x, y, x + w, y + H)), (i * (pw + gap), 0))
    return c
hero(2000, 857, 6).save(O + 'hero.jpg', quality=86, optimize=True)
hero(1200, 630, 4).save(O + 'og.jpg', quality=86, optimize=True)
im = Image.open(fr['cl6'][1].lstrip('/')).convert('RGB'); im.save(O + 'card-hero.jpg', quality=85)
print('boards', sum(len(v) for v in LOOKS.values()))
