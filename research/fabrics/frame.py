"""Fabrics post frames (24 Oct 2026): brands' own product images, 4:5 cover crops.
Lenny: "get rid of the stark white backgrounds" -> near-white backgrounds connected to the corners are recoloured to TGI stone.
Fella pants: on-model shots first, black-background flats dropped. Criquet cord: crotch close-up dropped. Stitch swapped out (M10 Casualist, C7 ACC Tokyo)."""
import json,glob
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
W,H=1000,1250; STONE=(232,226,214)
ORDER={'R20':[3,4,5,6],'C16':[1,3,4],'M10':[1,2,4,3],'C7':[4,1,2,3]}
def cover(im,W=W,H=H,cx=.5,cy=.5):
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def destark(im,th=16):
    a=np.asarray(im).astype(int); h,w,_=a.shape
    pts=[(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
    seeds=[(x,y) for x,y in pts if a[min(max(y,2),h-3),min(max(x,2),w-3)].min()>=236]
    if not seeds: return im
    ref=np.array([250,250,250])
    mk=Image.fromarray(((np.abs(a-ref).max(axis=2)<th+6)*255).astype('uint8')).copy()
    for pt in seeds: ImageDraw.floodfill(mk,pt,128)
    m=Image.fromarray(((np.array(mk)==128)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    return Image.composite(Image.new('RGB',im.size,STONE),im,m)
LIVE=[p['label'] for p in json.load(open('research/fabrics/live.json'))]
CARDS=[l for l in LIVE if l not in ('M29','C48')]+['M10','C7']
FR={}
for k in CARDS:
    idx=ORDER.get(k) or sorted(int(f.split('-')[-1][:-4]) for f in glob.glob(f'research/fabrics/raw/{k}-*.img'))[:4]
    FR[k]=[]
    for n,j in enumerate(idx,1):
        im=Image.open(f'research/fabrics/raw/{k}-{j}.img').convert('RGB'); im.thumbnail((2000,2000))
        out=cover(destark(im),cy=.4); fn=f'p-{k}-{n}.jpg'; out.save('images/fabrics/'+fn,quality=84,optimize=True); FR[k].append(fn)
json.dump(FR,open('research/fabrics/frames.json','w'),indent=1)
for n,cy in [('C51-4',.3),('C7-4',.3)]:
    cover(Image.open(f'research/fabrics/raw/{n}.img').convert('RGB'),1200,1500,cy=cy).save(f'images/fabrics/look-{n}.jpg',quality=84,optimize=True)
print('ok',len(FR))
