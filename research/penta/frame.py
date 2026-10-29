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
SOFTK = {'grid-sorbet', 'glove-green', 'glove-salt', 'cap-bone', 'elements-butter', 'gear'}  # white/cream product on a white sweep: the flood mask eats the product
SOFT.add('penta-soft')
def soft_contain(im):
    """White/cream product on a flat white sweep: warm the light tones toward stone (no hard mask, so the product
    keeps its edges), then crop to the product and contain it at the same scale as the flooded packshots."""
    a = np.array(im.convert('RGB')).astype(float); k = 10
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    if cc.min() < 200 or cc.std() > 8: return frame(im)
    col = np.median(cc, axis=0); L = a.mean(axis=2); Lb = col.mean()
    w = np.clip((L - .72 * Lb) / (.28 * Lb), 0, 1)[..., None]
    out = a * (1 - w) + np.clip(a / np.maximum(col, 1) * np.array(STONE), 0, 255) * w
    d = np.abs(a - col).max(axis=2) > 10
    ys, xs = np.where(d)
    x0, x1 = np.percentile(xs, [.2, 99.8]).astype(int); y0, y1 = np.percentile(ys, [.2, 99.8]).astype(int)
    m = int(.04 * max(x1 - x0, y1 - y0)); x0, y0 = max(0, x0 - m), max(0, y0 - m); x1, y1 = min(a.shape[1], x1 + m), min(a.shape[0], y1 + m)
    g = Image.fromarray(out.astype('uint8')).crop((x0, y0, x1, y1))
    sc = min(W * .8 / g.width, H * .74 / g.height); g = g.resize((round(g.width * sc), round(g.height * sc)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), STONE); c.paste(g, ((W - g.width) // 2, (H - g.height) // 2)); return c
from PIL import ImageFilter
def tight_cutout(im, tol=4):
    """Product on a pure-white (255) sweep with a near-white product (gloves sit at ~240-249): flood only the
    pure white from the corners, feather the edge, and keep the product's own whites. Falls back to soft_contain."""
    a = np.array(im.convert('RGB')).astype(int); k = 10
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    if cc.min() < 250: return soft_contain(im)
    mk = Image.fromarray(((255 - a.min(axis=2) <= tol) * 255).astype('uint8'))
    for pt in [(0, 0), (mk.width - 1, 0), (0, mk.height - 1), (mk.width - 1, mk.height - 1)]: ImageDraw.floodfill(mk, pt, 128)
    bg = np.array(mk) == 128
    alpha = Image.fromarray(((~bg) * 255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    ys, xs = np.where(~bg)
    x0, x1 = xs.min(), xs.max(); y0, y1 = ys.min(), ys.max()
    m = int(.03 * max(x1 - x0, y1 - y0)); x0, y0 = max(0, x0 - m), max(0, y0 - m); x1, y1 = min(a.shape[1], x1 + m), min(a.shape[0], y1 + m)
    g = Image.fromarray(a.astype('uint8')).convert('RGBA'); g.putalpha(alpha); g = g.crop((x0, y0, x1, y1))
    sc = min(W * .8 / g.width, H * .74 / g.height); g = g.resize((round(g.width * sc), round(g.height * sc)), Image.LANCZOS)
    c = Image.new('RGBA', (W, H), STONE + (255,)); c.alpha_composite(g, ((W - g.width) // 2, (H - g.height) // 2)); return c.convert('RGB')
TIGHT = set()  # tight_cutout tried for the gloves 28 Oct; Lenny said nvm, so not in use
FR = {}
for k, (h, ix) in K.items():
    out = []
    CUR[0] = 'penta-soft' if k in SOFTK else None
    for j, i in enumerate(ix, 1):
        f = glob.glob(f'{R}{h}-{i}.*')[0]
        (tight_cutout(load(f)) if k in TIGHT else soft_contain(load(f)) if k in SOFTK else frame(load(f))).save(f'{O}{k}-v2-{j}.jpg', quality=86, optimize=True); out.append(f'/{O}{k}-v2-{j}.jpg')
    FR[k] = out
json.dump(FR, open('research/penta/frames.json', 'w'), indent=1)
def cover(f, w, h, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
OR = 'research/penta/orig/'
hero = cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 2000, 857, .35); hero.save(O + 'hero.jpg', quality=86, optimize=True)
cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 1200, 630, .3).save(O + 'og.jpg', quality=84)
cover(OR + 'optical_33e6212e-ff89-476e-a382-da1f329e8e46.webp', 1000, 1250, .5).save(O + 'card-hero.jpg', quality=84, optimize=True)
B = {'band-metal-sun': ('Metal-1.webp', .3), 'band-metal-beach': ('metal-3.webp', .5), 'band-digital': ('../raw/penta-golf-polo-digital-2.webp', .5),
     'band-swing': ('moss-3_8e3f7575-ccd1-4142-b50b-af89270c2d70.webp', .5), 'band-bunker': ('moss-1_76bbacc5-a77e-4c06-a347-20b9f126dca5.webp', .5),
     'band-black': ('hazard-black-3.webp', .5), 'band-cap': ('Players-Cap-Navy-1.webp', .4)}
for n, (f, fy) in B.items(): cover(OR + f, 1000, 1250, fy).save(O + n + '-v2.jpg', quality=84, optimize=True)
print('ok', len(FR))
