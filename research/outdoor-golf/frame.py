"""Outdoor brands x golf frames. 22 Oct 2026. Products -> 1000x1250 stone. Light studio backdrops flood to stone; photos cover-crop.
Bands -> 1200x1500 cover crops of each brand's own lookbook; hero/og/card from PMO AW26 campaign (look-1)."""
import json,glob,numpy as np
from PIL import Image,ImageDraw
R='research/outdoor-golf/';O='images/outdoor-golf/';W,H=1000,1250;STONE=np.array([232,226,214.])
def cover(src,W=W,H=H,cx=.5,cy=.5):
    s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def topflood(src,th=14):
    # cover-crop, then turn the white studio connected to the TOP corners into stone; for crops that run off the bottom edge
    im=cover(src); a=np.asarray(im).astype(float); dd=np.abs(a-255).max(axis=2)
    mk=Image.fromarray(((dd<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; a[bg]=STONE; return Image.fromarray(a.clip(0,255).astype('uint8'))
def frame(src,th=24,force=False,fill=(.80,.74)):
    a=np.asarray(src).astype(float)
    cc=np.concatenate([a[:12,:12].reshape(-1,3),a[:12,-12:].reshape(-1,3),a[-12:,:12].reshape(-1,3),a[-12:,-12:].reshape(-1,3)])
    if not force and (cc.min()<190 or cc.std()>10): return cover(src)
    col=np.median(cc,axis=0); dd=np.abs(a-col).max(axis=2)
    mk=Image.fromarray(((dd<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=STONE
    ys,xs=np.where(~bg)
    x0,x1=np.percentile(xs,[.2,99.8]).astype(int); y0,y1=np.percentile(ys,[.2,99.8]).astype(int)
    m=int(.05*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*fill[0]/g.width,H*fill[1]/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
PICKS=[('arcteryx',['a1','a3','a5','a6','a7','a10','a11']),('salomon',['s1','s2','s3','s6','s8','s9','s11']),
 ('gramicci',['x2','x3','x5','x6','x7','x8','x11']),('purple-mountain-observatory',['x1','x2','x3','x5','x7','x9','x11']),
 ('goldwin',['x1','x3','x4','x6','x7','x9','x10'])]
SHOES={'a10','s1','s2','s3'}
FORCE={'purple-mountain-observatory:x5'}  # white studio with a soft vignette defeats the corner test
n=0; idx={}
for slug,ids in PICKS:
    for pid in ids:
        n+=1; f=glob.glob(f'{R}{slug}/p-{pid}.*')[0]; src=Image.open(f).convert('RGB')
        im=frame(src,force=True,fill=(.80,.50)) if pid in SHOES else (topflood(src) if f'{slug}:{pid}' in FORCE else frame(src))
        im.save(f'{O}p-{n}.jpg',quality=84,optimize=True); idx[f'{slug}:{pid}']=n
json.dump(idx,open(R+'idx.json','w'),indent=1)
BANDS={'arcteryx':[(1,.5,.5),(2,.62,.5),(6,.5,.5)],'salomon':[(3,.5,.5),(4,.5,.5),(5,.5,.5)],'gramicci':[(1,.42,.5),(2,.55,.5),(5,.5,.5)],
 'purple-mountain-observatory':[(2,.5,.5),(4,.5,.5),(5,.5,.5)],'goldwin':[(3,.5,.5),(4,.5,.5),(5,.5,.5)]}
for slug,ls in BANDS.items():
    for k,(i,cx,cy) in enumerate(ls,1):
        src=Image.open(glob.glob(f'{R}{slug}/look-{i}.*')[0]).convert('RGB')
        cover(src,1200,1500,cx,cy).save(f'{O}band-{slug}-{k}.jpg',quality=84,optimize=True)
h=Image.open(glob.glob(f'{R}purple-mountain-observatory/look-1.*')[0]).convert('RGB')
cover(h,2000,857,.5,.5).save(O+'hero.jpg',quality=86,optimize=True)
cover(h,1200,630,.5,.5).save(O+'og.jpg',quality=86,optimize=True)
cover(h,1000,1250,.5,.5).save(O+'card-hero.jpg',quality=86,optimize=True)
print('ok',n)
