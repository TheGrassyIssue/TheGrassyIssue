"""Dogs & Golf frames. 22 Oct 2026. One image per pick -> 1000x1250. Flat light studio backdrops flood to stone; photos cover-crop."""
import json,numpy as np
from PIL import Image,ImageDraw
R='research/dogs-golf/';O='images/dogs-golf/';W,H=1000,1250;STONE=np.array([232,226,214.])
def cover(src):
    s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
def frame(src,th=24,force=False):
    a=np.asarray(src).astype(float)
    cc=np.concatenate([a[:12,:12].reshape(-1,3),a[:12,-12:].reshape(-1,3),a[-12:,:12].reshape(-1,3),a[-12:,-12:].reshape(-1,3)])
    if not force and (cc.min()<190 or cc.std()>10): return cover(src)
    col=np.median(cc,axis=0); dd=np.abs(a-col).max(axis=2)
    mk=Image.fromarray(((dd<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=STONE
    ys,xs=np.where(~bg)
    if len(xs)<100: return cover(src)
    x0,x1=np.percentile(xs,[.3,99.7]).astype(int); y0,y1=np.percentile(ys,[.3,99.7]).astype(int)
    m=int(.06*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.78/g.width,H*.72/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
FORCE={15:(30,True)}
ALT={20:'alt/bd2.jpg',27:'alt/sg-Untitled_design_c2f6a250-d15d-4ac2-bb05-a67465e3c080.png'}
for p in json.load(open(R+'picks.json')):
    f=R+'raw/'+p['img_file'].split('/')[-1]
    if p['n'] in ALT: cover(Image.open(R+ALT[p['n']]).convert('RGB')).save(f"{O}p-{p['n']}.jpg",quality=84); continue
    frame(Image.open(f).convert('RGB'),*FORCE.get(p['n'],(24,False))).save(f"{O}p-{p['n']}.jpg",quality=84,optimize=True)
for f,o in [('life/sounder-3.jpg','life-1'),('life/sounder-4.jpg','life-2'),('life/sounder-5.jpg','life-3'),('life/sounder-6.jpg','life-4'),('life/foggy-1.jpg','life-5')]:
    im=Image.open(R+f).convert('RGB');im.thumbnail((1600,1600));im.save(O+o+'.jpg',quality=86)
print('ok')
