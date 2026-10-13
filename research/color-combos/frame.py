"""Frames for the color combos post (13 Oct 2026). Every photo is the brand's own, reused from earlier TGI posts.
Product frames copied to images/color-combos/<key>-<n>.jpg; stark-white sweeps graded to stone (grade = whole-frame multiply, no halos).
Lifestyle band ("From the Lookbooks and In the Wild") -> life-<n>.jpg. Hero 2000x857 trio + 7-pair swatch strip; og 1200x630."""
import json, sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, 'research/grips-vol2'); from recolor import grade
O = 'images/color-combos/'; W, H = 1000, 1250
G = 'images/grips-vol2/'
SRC = {
 # Royal Blue + Chalk
 "lof": [f"images/left-of-field/sorento-polo-royal-blue-9-{i}.jpg" for i in range(3)],
 "slice": [f"images/slice-town/s05-{i}.jpg" for i in (1, 2, 3)],
 "cwporcelain": [G+"cwblossom-4.jpg", G+"cwblossom-7.jpg"],
 "cadblue": [G+"cadpent-8.jpg"],
 "iomicblue": [G+"sticky23-5.jpg"],
 "jonesglove": [f"images/bag-hang/g04-{i}.jpg" for i in (1, 2, 3)],
 "tarraing": [f"images/radar-three/p032-{i}.jpg" for i in (1, 2, 3)],
 # Red Wine + Light Sand
 "latenine": [f"images/wanted-to-wear/latenine-{i}.jpg" for i in (1, 2, 3)],
 "walkerpolo": ["images/outfits/walker--members-polo-3-2.jpg", "images/outfits/walker--members-polo-3-1.jpg"],
 "nodirtburg": [f"images/no-dirt-golf/uc-burgundry-silver-stripes-{i}.jpg" for i in (1, 2)],
 "hiroki": ["images/hiroki/oriental-maroon.jpg", "images/hiroki/oriental-maroon-a2.jpg"],
 "hypegolf": [G+"hypegolf-1.jpg", G+"hypegolf-3.jpg", G+"hypegolf-4.jpg"],
 "wgshort": [f"images/woodgrain/the-double-pleated-short-tan-{i}.jpg" for i in (1, 2)],
 "wgtan": [f"images/woodgrain/relaxed-double-pleated-trouser-tan-{i}.jpg" for i in (1, 2)],
 # Orange + Linen
 "jonescirca": [f"images/jones-sports-co/circa-71-headcover-orange-{i}.jpg" for i in (0, 1)],
 "palm": [f"images/palm-golf/p09-{i}.jpg" for i in (0, 1)],
 "mogshade": [f"images/loud-headcovers/mogshade-tiles-olive-orange-{i}.jpg" for i in (0, 1, 2)],
 "devereux": ["images/devereux-golf/r-high-noon.jpg", "images/devereux-golf/r-high-noon-a2.jpg"],
 "iomicorange": [G+"sticky18-6.jpg"],
 "flowerclay": [G+"flower-4.jpg", G+"flower-1.jpg"],
 "seamuscopper": [f"images/seamus/markit8-marker-{i}.jpg" for i in (0, 1)],
 "ashworth": [f"images/ashworth/a01-{i}.jpg" for i in (0, 1, 2)],
 # Plum + Cream
 "eastside": ["images/fall-drops-2026/eastside-wild-grape-tip-pique-polo.jpg", "images/fall-drops-2026/eastside-wild-grape-tip-pique-polo-a2.jpg"],
 "cwmoonshade": [G+"cwspring-4.jpg", G+"cwspring-7.jpg"],
 "fyfe09": [f"images/fyfe-second-round/r09-{i}.jpg" for i in (1, 2)],
 "kraken": ["images/divot-tools/kraken-2.jpg"],
 "swag": ["images/ball-markers/swag-golf-tito-s-splash-of-grape-ball-.jpg"],
 "apres": ["images/apres-golf/hally-grapeness.jpg"],
 "iomiclav": [G+"sticky18-5.jpg"],
 "oddritual": [f"images/wanted-to-wear/oddritual-{i}.jpg" for i in (1, 2, 3)],
 # Midnight Indigo + Vanilla
 "criquet": [f"images/wanted-to-wear/criquet2-{i}.jpg" for i in (1, 2, 3)],
 "seamusnavy": [f"images/wanted-to-wear/seamus2-{i}.jpg" for i in (1, 2, 3)],
 "jancraig": [f"images/wanted-to-wear/jancraig-{i}.jpg" for i in (1, 2, 3)],
 "fella": ["images/outfits/fella--boris-quarter-zip-sweater-navy-2.jpg", "images/outfits/fella--boris-quarter-zip-sweater-navy-1.jpg"],
 "walkerhedge": [f"images/walker-blooming-grounds/hedge-mid-cap-2-{i}.jpg" for i in (0, 1)],
 "lofduck": [f"images/outfits/left-of-field--duckbill-birds-cap-navy-cream-{i}.jpg" for i in (1, 2)],
 "wgcream": [f"images/woodgrain/relaxed-double-pleated-trouser-{i}.jpg" for i in (1, 2, 3)],
 # Cherry + Alabaster
 "cwpalace": [G+"cwblossom-3.jpg", G+"cwblossom-6.jpg"],
 "students": ["images/studentsgolf-summer26/society-structured-5-panel-acrylic-wool-hat.jpg", "images/studentsgolf-summer26/society-structured-5-panel-acrylic-wool-hat-a2.jpg"],
 "lofplaid": [f"images/left-of-field/heritage-plaid-cap-red-26-{i}.jpg" for i in (0, 1)],
 "localgc": [f"images/local-gc/nantucket-red-canvas-head-cover-{i}.jpg" for i in (1, 2)],
 "parmorered": [f"images/parmore/red-paneled-tee-rebrand-{i}.jpg" for i in (1, 2)],
 "sugarloaf": [f"images/small-things/st28-{i}.jpg" for i in (1, 2)],
 "both": [f"images/hat-brands/both1-{i}.jpg" for i in (1, 2)],
 # Forest + Leaf
 "lazywood": [f"images/lazyface/the-wood-cover-{i}.jpg" for i in (1, 2)],
 "parmoregreen": [f"images/parmore/green-1-4-zip-rebrand-{i}.jpg" for i in (1, 2)],
 "cwmist": [G+f"cwmist-{i}.jpg" for i in (1, 2, 3)],
 "nodirtgreen": [f"images/no-dirt-golf/the-classic-forest-green-{i}.jpg" for i in (1, 2)],
 "puttwell": [f"images/fall-tees/t26-{i}.jpg" for i in (1, 2)],
 "lazycap": [f"images/lazyface/the-chenille-sun-cap-{i}.jpg" for i in (1, 2)],
 "cadgreen": [G+"cadpent-3.jpg"],
}
LIFE = ["left-of-field/sorento-polo-royal-blue-9-0", "slice-town/s05-1",
        "outfits/walker--members-polo-3-2", "wanted-to-wear/latenine-1", "woodgrain/the-double-pleated-short-tan-1", "woodgrain/relaxed-double-pleated-trouser-tan-1", "woodgrain/band-3",
        "devereux-golf/r-high-noon-a2", "grips-vol2/flower-1",
        "wanted-to-wear/oddritual-1",
        "wanted-to-wear/woodgrain-1", "outfits/fella--boris-quarter-zip-sweater-navy-2", "wanted-to-wear/oddritual2-1", "wanted-to-wear/criquet2-1",
        "walker-blooming-grounds/hedge-mid-cap-2-1", "outfits/left-of-field--duckbill-birds-cap-navy-cream-1", "woodgrain/relaxed-double-pleated-trouser-2",
        "parmore/red-paneled-tee-rebrand-1", "left-of-field/heritage-plaid-cap-red-26-0", "grips-vol2/cwblossom-6",
        "parmore/green-1-4-zip-rebrand-1", "fall-tees/t26-1", "fall-tees/t26-2", "lazyface/card-hero"]
def fit(im):
    if im.size == (W, H): return im
    s = max(W/im.width, H/im.height); im = im.resize((max(W, round(im.width*s)), max(H, round(im.height*s))), Image.LANCZOS)
    x = (im.width-W)//2; y = (im.height-H)//3; return im.crop((x, y, x+W, y+H))
def stark(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(int); b = np.concatenate([a[:4].reshape(-1,3), a[-4:].reshape(-1,3), a[:, :4].reshape(-1,3), a[:, -4:].reshape(-1,3)])
    return b.min(axis=1).mean() > 242
fr, graded = {}, []
for k, fs in SRC.items():
    fr[k] = []
    for n, f in enumerate(fs, 1):
        out = f'{O}{k}-{n}.jpg'; fit(Image.open(f).convert('RGB')).save(out, quality=88)
        if stark(out): grade(out); graded.append(out)
        fr[k].append('/'+out)
for n, f in enumerate(LIFE, 1):
    out = f'{O}life-{n}.jpg'; fit(Image.open(f'images/{f}.jpg').convert('RGB')).save(out, quality=86)
    if stark(out): grade(out); graded.append(out)
json.dump(fr, open('research/color-combos/frames.json', 'w'), indent=1)
print(len(fr), 'cards;', len(LIFE), 'life; graded', graded)
# hero: trio + swatch strip
PAIRS = [("#014BAA", "#F8F3F0"), ("#7F011F", "#F5EBD0"), ("#EC5E27", "#FDFDF1"), ("#381932", "#FFF3E6"), ("#282B4A", "#EEEBDA"), ("#890149", "#F3F3E7"), ("#064734", "#E0FFC2")]
def hx(c): return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
def hero(w, h, files, strip):
    c = Image.new('RGB', (w, h), (232, 226, 214)); ph = h - strip; tw = w // 3
    for i, f in enumerate(files):
        im = Image.open(f).convert('RGB'); s = max(tw/im.width, ph/im.height); im = im.resize((round(im.width*s)+1, round(im.height*s)+1), Image.LANCZOS)
        x = (im.width-tw)//2; y = int((im.height-ph)*.3); c.paste(im.crop((x, y, x+tw, y+ph)), (i*tw, 0))
    d = ImageDraw.Draw(c); sw = w / 7
    for i, (a, b) in enumerate(PAIRS):
        x0 = round(i*sw); x1 = round((i+1)*sw); xm = (x0+x1)//2
        d.rectangle((x0, ph, xm, h), fill=hx(a)); d.rectangle((xm, ph, x1, h), fill=hx(b))
    return c
T = [f'{O}life-1.jpg', f'{O}life-3.jpg', f'{O}life-21.jpg']
hero(2000, 857, T, 70).save(f'{O}hero.jpg', quality=88)
hero(1200, 630, T, 48).save(f'{O}og.jpg', quality=86)

# ---- v2 hero (Lenny picked "middle one", 13 Oct): single Students Golf shot, studentsgolf.com homepage carousel_fall2026_d2.jpg (3000x1739)
def single(w, h, fy=0.0):
    im = Image.open('research/color-combos/hero-raw/st1.jpg').convert('RGB'); s = max(w/im.width, h/im.height)
    im = im.resize((round(im.width*s)+1, round(im.height*s)+1), Image.LANCZOS); x = (im.width-w)//2; y = int((im.height-h)*fy)
    return im.crop((x, y, x+w, y+h))
single(2000, 857).save(f'{O}hero.jpg', quality=90)
single(1200, 630).save(f'{O}og.jpg', quality=88)
