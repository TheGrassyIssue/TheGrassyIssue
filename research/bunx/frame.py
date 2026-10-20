"""BUNX BTK frames. 20 Oct 2026. Square grey-seamless packshots -> 1000x1250 by extending top/bottom edge rows (no crop of wide hats)."""
import json,os,io,urllib.request,numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
R='research/bunx/'; O='images/bunx/'
d={p['handle']:p for p in json.load(open(R+'products.json'))['products']}
CARDS=[('h1','long-iron-country-golf-hat'),('h2','rough-rodeo-golf-hat'),('h3','bunx-fort-worth-golf-hat'),('h4','club-champ-golf-hat'),('h5','texas-wedge-golf-hat'),('h6','cashmere-caddie'),('h7','bunx-golf-hat-sandy-pars-snapback'),('h8','bunx-golf-hat-big-sky-birds'),('h9','bunx-golf-hat-moonlit-mulligan'),('h10','bunx-golf-hat-signature-b-a-frame'),('h11','golf-dept'),('f1','tex-camo-adult-youth'),('f2','toc-father-son'),
('w1','bunx-golf-towel-technical-typography'),('w2','bunx-golf-towel-squiggy-abstract'),('w3','bunx-golf-towel-sandy-breakfast-club'),('w4','bunx-golf-towel-dats-good-gimme-ruler'),('w5','bunx-golf-towel-camo'),('w6','bunx-golf-towel-cart-path-only-rebel'),
('t1','drt-divot-repair-tool'),('t2','bunx-v01-tee'),('t3','scrub-pouch')]
def srcs(p):
    av=[v for v in p['variants'] if v['available']]
    fe=[]
    for v in av:
        s=(v.get('featured_image') or {}).get('src')
        if s:
            s=s.split('?')[0]
            if s not in fe: fe.append(s)
    imgs=[i['src'].split('?')[0] for i in p['images']]
    if len(fe)>=2: return fe[:5]
    bad=set((v.get('featured_image') or {}).get('src','').split('?')[0] for v in p['variants'] if not v['available'])
    rest=[u for u in imgs if u not in bad and u not in fe]
    if fe:
        # keep only shots of the in-stock colourway: product images listed right after its featured image
        i0=imgs.index(fe[0]) if fe[0] in imgs else 0
        others=[v.get('featured_image',{}) for v in p['variants'] if v.get('featured_image')]
        starts=sorted(set(imgs.index(o['src'].split('?')[0]) for o in others if o['src'].split('?')[0] in imgs))
        nxt=[s for s in starts if s>i0]; end=nxt[0] if nxt else len(imgs)
        if len(starts)>1: rest=imgs[i0+1:end]
    return (fe+rest)[:4]
def fit(im):
    W,H=1000,1250
    s=W/im.width; im=im.resize((W,round(im.height*s)),Image.LANCZOS)
    if im.height>=H:
        y=(im.height-H)//2; return im.crop((0,y,W,y+H))
    a=np.array(im); top=(H-im.height)//2; bot=H-im.height-top
    t=np.repeat(a[:1],top,0); b=np.repeat(a[-1:],bot,0)
    # soften: blend toward row mean to hide vertical streaks
    from PIL import ImageFilter
    def smooth(row,n):
        r=Image.fromarray(row).resize((W,1)); r=r.resize((W//40,1),Image.BILINEAR).resize((W,1),Image.BILINEAR)
        return np.repeat(np.asarray(r),n,0)
    t=smooth(a[:1],top); b=smooth(a[-1:],bot)
    # feather the seam over 24px
    for k in range(min(24,im.height)):
        w=1-k/24
        a[k]=(a[k]*(1-w)+t[-1]*w).astype('uint8') if top else a[k]
        a[-1-k]=(a[-1-k]*(1-w)+b[0]*w).astype('uint8') if bot else a[-1-k]
    return Image.fromarray(np.concatenate([t,a,b]))
def get(u,fn):
    if not os.path.exists(fn):
        b=urllib.request.urlopen(urllib.request.Request(u+'?width=1600',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read(); open(fn,'wb').write(b)
    return fn
jobs=[]
for k,h in CARDS:
    for i,u in enumerate(srcs(d[h])): jobs.append((k,i,u))
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda j:get(j[2],f'{R}raw/{j[0]}-{j[1]}.img'),jobs))
fr={}
for k,i,u in jobs:
    im=Image.open(f'{R}raw/{k}-{i}.img').convert('RGB'); out=f'{O}{k}-{i+1}.jpg'; fit(im).save(out,quality=86); fr.setdefault(k,[]).append('/'+out)
json.dump(fr,open(R+'frames.json','w'),indent=1); json.dump(dict(CARDS),open(R+'cards.json','w'),indent=1); print(len(jobs))

# POST-FIX (applied after run): t3 -> first frame only (others carry burned-in text); h8 drop frame 2 (source not square, white band)
