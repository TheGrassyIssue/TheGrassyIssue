"""Cph/Golf x Jones (Oct 2026) frames. Product shots -> 1000x1250 stone; lookbook (Oct 16 2026 shoot, from Cph/Golf's product pages) -> cover crops."""
import numpy as np,glob
from PIL import Image,ImageDraw
R='research/cph-jones/';O='images/cph-jones/';W,H=1000,1250;STONE=np.array([232,226,214.])
P=[R+l.split(' ',1)[1].strip() for l in open(R+'prods.txt')]; L=[R+l.strip() for l in open(R+'looks.txt')]
def cover(src,W=W,H=H,cx=.5,cy=.5):
    s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def frame(src,th=22,fill=(.80,.70)):
    a=np.asarray(src).astype(float)
    mk=Image.fromarray(((np.abs(a-255).max(axis=2)<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=STONE
    ys,xs=np.where(~bg); x0,x1=xs.min(),xs.max(); y0,y1=ys.min(),ys.max()
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1+1,y1+1)); s=min(W*fill[0]/g.width,H*fill[1]/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
def prod(i,**k): return frame(Image.open(P[i]).convert('RGB'),**k)
def look(i,cy=.5): return cover(Image.open(L[i]).convert('RGB'),cy=cy)
CARDS={ # card -> list of ('p',idx) / ('l',idx)
 1:[('p',54),('p',53),('l',15),('l',4)],      # Stadium Wind Breaker Jacket
 2:[('p',61),('p',60),('l',10)],              # Team LS Mock Neck Tee
 3:[('p',62),('p',63),('l',43)],              # Polo Sweat Pullover
 4:[('p',55),('p',56),('l',22),('l',20)],     # Adjustable Pants The 1st
 5:[('p',21),('p',22),('l',5)],               # Team Cap
 6:[('p',23),('p',24),('l',11)],              # Team Corded Bucket Hat
 7:[('p',25),('p',41),('p',31),('l',3)],      # Trouper Stand Bag
 8:[('p',0),('p',4)],                         # Driver cover
 9:[('p',8),('p',12)],                        # Wood cover
 10:[('p',16),('p',18)],                      # Utility cover
}
FR={}
for c,items in CARDS.items():
    FR[c]=[]
    for j,(t,i) in enumerate(items,1):
        im=prod(i,fill=(.84,.80) if c==7 else (.80,.70),th=6 if c in (1,3) else 22) if t=='p' else look(i,cy=.35)
        fn=f'p-{c}-{j}.jpg'; im.save(O+fn,quality=84,optimize=True); FR[c].append(fn)
LOOK=[34,13,2,7,19,25,35,41,39,9,33,0]
for k,i in enumerate(LOOK,1):
    src=Image.open(L[i]).convert('RGB'); im=cover(src,1200,1500,cy=.4); im.save(f'{O}look-{k}.jpg',quality=84,optimize=True)
# hero: triptych of three portrait lookbook frames
tri=[12,6,40]; panel=[cover(Image.open(L[i]).convert('RGB'),666,857,cy=.3) for i in tri]
hero=Image.new('RGB',(2000,857),(20,20,20)); x=0
for p in panel: hero.paste(p,(x,0)); x+=667
hero.save(O+'hero.jpg',quality=86,optimize=True); hero.resize((2000,857)).crop((0,0,2000,857))
og=Image.new('RGB',(1200,630),(20,20,20)); x=0
for i in tri: og.paste(cover(Image.open(L[i]).convert('RGB'),400,630,cy=.3),(x,0)); x+=400
og.save(O+'og.jpg',quality=86)
cover(Image.open(L[15]).convert('RGB'),1000,1250,cy=.3).save(O+'card-hero.jpg',quality=86)
import json; json.dump(FR,open(R+'frames.json','w'),indent=1); print('ok')
