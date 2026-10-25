"""water when dry Revisited frames. 24 Oct 2026.
Transparent PNG packshots -> composited on stone, trimmed, contain-fit. Opaque photos -> 4:5 cover crop.
Size charts, measurement diagrams, mannequin composites and AI-looking model shots are left out (see SKIP note in CARDS)."""
import json, glob, os, numpy as np
from PIL import Image
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass
R = 'research/water-when-dry/'; O = 'images/water-when-dry-revisit/'; W, H = 1000, 1250; STONE = (232, 226, 214)
os.makedirs(O, exist_ok=True)
# card -> list of raw image ids (picks.json number + image index). AI-looking model shots N2-1, N3-1, N7-1, S7-1, S9-1 skipped.
CARDS = {
 'pants': ['N1-0', 'N4-0', 'N6-0', 'N1-1', 'N1-3', 'N6-2', 'N4-2', 'N1-2'],
 'cap':   ['N8-0', 'N9-0', 'N8-1', 'N9-1'],
 'univ':  ['N2-0', 'N2-2'],
 'socks': ['N5-0'],
 'fw26po': ['N3-0', 'N7-0', 'N3-3', 'N7-3', 'N3-2', 'N7-2'],
 'wwdpo': ['S16-0', 'S17-0', 'S16-4', 'S16-1', 'S17-1', 'S17-3', 'S16-2', 'S17-2'],
 'hoodie': ['S4-0', 'S5-0', 'S4-2', 'S5-2', 'S4-3', 'S5-3', 'S4-1'],
 'fleece': ['S3-0', 'S3-1', 'S3-3', 'S3-4', 'S3-2'],
 'sweats': ['C1-0', 'C1-1'],
 'iconls': ['S8-0', 'S8-1'],
 'juniper': ['C3-0', 'C3-1'],
 'camper': ['S2-0', 'S2-4', 'S2-3', 'S2-5', 'S2-1'],
 'tree':  ['S12-0', 'S12-1'],
 'swim':  ['S14-0', 'S15-0', 'S14-3', 'S15-3', 'S14-1', 'S15-1'],
 'tote':  ['S1-0', 'S1-1', 'S1-2'],
 'raglan': ['S13-0', 'S13-2', 'S13-1'],
 'seeds': ['S10-0', 'S11-0', 'S10-1', 'S11-1'],
 'hands': ['S6-0', 'S6-2'],
 'grass': ['S7-0', 'S7-2', 'S7-3'],
 'rose':  ['S9-0', 'S9-3', 'S9-2'],
 'greenhouse': ['C2-0', 'C2-2'],
}
def load(i):
    f = glob.glob(f'{R}raw/{i}.*')[0]
    im = Image.open(f); im.seek(0)
    return im
def frame(im):
    im = im.convert('RGBA'); a = np.array(im)[:, :, 3]
    corners = np.concatenate([a[:6, :6].ravel(), a[:6, -6:].ravel(), a[-6:, :6].ravel(), a[-6:, -6:].ravel()])
    if corners.min() < 200:   # transparent packshot
        ys, xs = np.where(a > 20)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        g = im.crop((x0, y0, x1 + 1, y1 + 1))
        s = min(W * .8 / g.width, H * .74 / g.height); g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
        c = Image.new('RGBA', (W, H), STONE + (255,)); c.alpha_composite(g, ((W - g.width) // 2, (H - g.height) // 2)); return c.convert('RGB')
    bg = Image.new('RGBA', im.size, STONE + (255,)); bg.alpha_composite(im); im = bg.convert('RGB')
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2; return im.crop((x, y, x + W, y + H))
fr = {}
for k, ids in CARDS.items():
    for j, i in enumerate(ids, 1):
        out = f'{O}{k}-{j}.jpg'; frame(load(i)).save(out, quality=84, optimize=True); fr.setdefault(k, []).append('/' + out)
json.dump(fr, open(R + 'frames.json', 'w'), indent=1)
# lookbook / band photos (brand's own site + product pages)
LB = {'cart': 'site/hero.jpg', 'pond': 'raw/S2-4.jpg', 'putt': 'raw/S2-3.jpg', 'feet': 'raw/S2-5.jpg', 'sock': 'site/DSC05537.png',
      'field': 'site/Screenshot_2025-04-29_at_1.59.25_PM.png', 'pantsdetail': 'site/PANTS.png', 'pullovers': 'site/FW26-pullovers-concrete.png',
      'stairs': 'raw/S16-1.jpg', 'seated': 'raw/S16-4.jpg', 'walk': 'raw/S16-3.jpg', 'soil': 'site/about.jpg', 'pantpane': 'site/utility-pant-pane-centered-v2.jpg',
      'fleecefig': 'raw/S3-4.jpg', 'everyflower': 'raw/S4-4.jpg'}
for k, f in LB.items():
    im = Image.open(R + f).convert('RGBA'); bg = Image.new('RGBA', im.size, STONE + (255,)); bg.alpha_composite(im); im = bg.convert('RGB')
    im.thumbnail((1600, 1600)); im.save(f'{O}lb-{k}.jpg', quality=86, optimize=True)
print({k: len(v) for k, v in fr.items()}, sum(len(v) for v in fr.values()))
