"""Radar Vol. 4 (Swell Marks, Hinotori, Studio Grain): frames. c=cover crop (brand's own IRL/studio shots), x=GrabCut cut-out on stone (pure-white studio shots only). 29 Oct 2026."""
import json, os, sys
from PIL import Image
sys.path.insert(0, 'research/radar-three-4'); from gcut import cutout
R = 'research/radar-three-4/raw/'; O = 'images/radar-three-4/'; os.makedirs(O, exist_ok=True)
def cover(f, w=1000, h=1250, fx=.5, fy=.5):
    im = Image.open(f).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
S = 'sw-'; HI = 'hi-'; G = 'sg-'
F = {
 'sw-skulligan': [(S+'skulligan-1','c'),(S+'skulligan-3','c'),(S+'skulligan-4','c'),(S+'skulligan-5','c')],
 'sw-redfin': [(S+'fin-theory-red-fin-b-001-1','c'),(S+'fin-theory-red-fin-b-001-2','c'),(S+'fin-theory-red-fin-b-001-3','c'),(S+'fin-theory-red-fin-b-001-5','c'),(S+'fin-theory-red-fin-b-001-6','c')],
 'sw-goodbones': [(S+'good-bones-2','c'),(S+'good-bones-3','c'),(S+'good-bones-4','c'),(S+'good-bones-6','c'),(S+'good-bones-8','c')],
 'sw-trestles': [(S+'trestles-4','c'),(S+'trestles-5','c'),(S+'trestles-6','c'),(S+'trestles-1','c'),(S+'trestles-2','c')],
 'sw-wave': [(S+'wave-1','c'),(S+'wave-2','c'),(S+'wave-3','c'),(S+'wave-6','c')],
 'sw-pipeline': [(S+'pipeline-1','c'),(S+'pipeline-2','c'),(S+'pipeline-3','c'),(S+'pipeline-4','c')],
 'sw-1893': [(S+'1893-brass-golf-ball-marker-1','c'),(S+'1893-brass-golf-ball-marker-3','c'),(S+'1893-brass-golf-ball-marker-4','c'),(S+'1893-brass-golf-ball-marker-6','c')],
 'sw-lightning': [(S+'lightning-1','c'),(S+'lightning-2','c'),(S+'lightning-3','c'),(S+'lightning-4','c')],
 'sw-pitch': [(S+f'resin-pitch-tool-0{n}-1','c') for n in ('14','13','10','09','08','06')],
 'hi-ryujin-hc': [(HI+'ryujin-barrel-headcover-4','c'),(HI+'ryujin-barrel-headcover-5','c'),(HI+'ryujin-barrel-headcover-2','c'),(HI+'ryujin-barrel-headcover-3','c')],
 'hi-duck': [(HI+'duck-camo-barrel-headcover-1','c'),(HI+'duck-camo-barrel-headcover-2','c'),(HI+'duck-camo-barrel-headcover-3','c'),(HI+'duck-camo-barrel-headcover-4','c')],
 'hi-enso': [(HI+'enso-glove-case-2','c'),(HI+'enso-glove-case-4','c'),(HI+'enso-glove-case-5','c'),(HI+'enso-glove-case-6','c'),(HI+'enso-glove-case-7','c'),(HI+'enso-glove-case-1','c')],
 'hi-timekeeper': [(HI+'the-time-keeper-ball-marker-1','c'),(HI+'the-time-keeper-ball-marker-2','c'),(HI+'the-time-keeper-ball-marker-3','c')],
 'hi-cherry': [(HI+'cherry-blossom-6','c'),(HI+'cherry-blossom-4','c'),(HI+'cherry-blossom-5','c'),(HI+'cherry-blossom-1','c')],
 'hi-seigaiha': [(HI+'mens-seigaiha-signature-glove-1','c')],
 'hi-sentinel': [(HI+'sentinel-performance-hat-6','c'),(HI+'sentinel-performance-hat-7','c'),(HI+'sentinel-performance-hat-1','c'),(HI+'sentinel-performance-hat-2','c')],
 'hi-towel': [(HI+'ryujin-towel-3','c'),(HI+'ryujin-towel-2','x')],
 'sg-members': [(G+'members-hat-3','c'),(G+'members-hat-1','x'),(G+'members-hat-2','x')],
 'sg-letterman': [(G+'brown-grain-lettermen-snapback-hat-1','x'),(G+'brown-grain-lettermen-snapback-hat-2','x')],
 'sg-camo': [(G+'camo-studio-grain-outdoors-program-hat-1','x'),(G+'camo-studio-grain-outdoors-program-hat-2','x')],
 'sg-shades': [(G+'sunglasses-2','c'),(G+'sunglasses-1','x'),(G+'fairway-finders-sunglasses-black-1','x')],
 'sg-beanie': [(G+'fisherman-beanie-green-1','x'),(G+'fisherman-beanie-gray-1','x'),(G+'fisherman-beanie-navy-1','x')],
 'sg-deck': [(G+f'grain-fingerboard-deck-{c}-1','x') for c in ('ocean-blue','mosaic','half-half','maple-brown')] + [(G+'grain-fingerboad-deck-forrest-green-1','x')],
}
FY = {S+'skulligan-5': .5}
FR = {}
for k, lst in F.items():
    out = []
    for j, (src, m) in enumerate(lst, 1):
        o = f'{O}{k}-{j}.jpg'
        im = cutout(R + src + '.jpg', .78, .62) if m == 'x' else cover(R + src + '.jpg', fy=FY.get(src, .45))
        assert im is not None, src
        im.save(o, quality=85, optimize=True); out.append('/' + o)
    FR[k] = out
json.dump(FR, open('research/radar-three-4/frames.json', 'w'), indent=1)
# hero triptych, og, card-hero, band
tri = [(S+'trestles-3', .5), (HI+'ryujin-barrel-headcover-5', .5), (G+'members-hat-3', .3)]
h = Image.new('RGB', (2000, 857), (232, 226, 214)); x = 0
for (src, fy), w in zip(tri, (666, 668, 666)):
    h.paste(cover(R + src + '.jpg', w - 4 if x else w - 2, 857, .5, fy), (x + (2 if x else 0), 0)); x += w
h.save(O + 'hero.jpg', quality=86, optimize=True)
og = h.resize((1200, 514), Image.LANCZOS); c = Image.new('RGB', (1200, 630), (232, 226, 214)); c.paste(og, (0, 58)); c.save(O + 'og.jpg', quality=84)
cover(R + HI + 'ryujin-barrel-headcover-5.jpg', 1000, 1250).save(O + 'card-hero.jpg', quality=84, optimize=True)
for i, src in enumerate([S+'good-bones-9', S+'1893-brass-golf-ball-marker-5', S+'fin-theory-red-fin-b-001-4'], 1):
    cover(R + src + '.jpg', 1000, 1250).save(O + f'band-{i}.jpg', quality=84, optimize=True)
print({k: len(v) for k, v in FR.items()})
