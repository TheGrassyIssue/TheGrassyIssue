"""Frames for the blended-interests post. 19 October 2026. White packshots: tight crop + destark (stone). Lifestyle: cover crop."""
import json,sys,numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,'.')
from destark import destark
R='research/uk-six/raw/'; O='images/uk-six/'; W,H=1000,1250
STONE=np.array([232,226,214.])
SEL={'c1': [0, 1, 2, 3], 'c2': [0, 1, 2, 3], 'c3': [0, 1, 2], 'c4': [0, 1, 2], 'c5': [0, 1, 2, 3], 'c6': [0, 1, 2, 3], 'd1': [0, 1, 2, 3], 'd2': [0, 1, 2, 3], 'd3': [0, 1, 2, 3], 'd4': [0, 1, 2, 3], 'd5': [0, 1, 2], 'd6': [0, 1, 2, 3], 'k1': [0, 1, 2], 'k2': [0, 1, 2, 3], 'k3': [0, 1, 2], 'k4': [0, 1, 2], 'k5': [0, 1, 2], 'k6': [0, 1, 2], 'p1': [0, 1, 2, 3], 'p2': [0, 1, 2], 'p3': [0, 1, 2, 3], 'p4': [0, 1, 2, 3], 'p5': [0, 1, 2], 'p6': [0, 1, 2], 's1': [0, 1, 2, 3], 's2': [0, 1, 2, 3], 's3': [0, 1, 2, 3], 's4': [0, 1, 2, 3], 's5': [0, 1, 2, 3], 's6': [2, 1], 't1': [0, 1, 2, 3], 't2': [0, 1, 2, 3], 't3': [0, 1, 2, 3], 't4': [0, 1, 2, 3], 't5': [0, 1, 2, 3], 't6': [0, 1, 2, 3]}
POS={}
def cover(im,py=.5,px=.5):
    s=max(W/im.width,H/im.height); im=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=int((im.width-W)*px); y=int((im.height-H)*py); return im.crop((x,y,x+W,y+H))
def tight(im,fill=.84):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if b.std(axis=0).max()>=16 or b.mean()<225: return None
    col=np.median(b,axis=0); d=np.abs(a-col).max(axis=2)>22; ys,xs=np.where(d)
    if len(xs)<500: return None
    x0,x1=np.percentile(xs,[.2,99.8]).astype(int); y0,y1=np.percentile(ys,[.2,99.8]).astype(int)
    m=int(.05*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(im.width,x1+m),min(im.height,y1+m)
    g=im.crop((x0,y0,x1,y1)); s=min(W*.9/g.width,H*fill/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in col)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
fr={}
for k,idx in SEL.items():
    fr[k]=[]
    for j,i in enumerate(idx,1):
        key=f'{k}-{i}'; out=f'{O}{k}-{j}.jpg'
        if __import__('os').path.exists(out): fr[k].append('/'+out); continue
        src=Image.open(f'{R}{key}.jpg').convert('RGB'); out=f'{O}{k}-{j}.jpg'
        t=tight(src)
        if t is not None: t.save(out,quality=86); destark(out,light=False,min_white=.15)
        else: cover(src,POS.get(key,.5)).save(out,quality=86)
        fr[k].append('/'+out)
json.dump(fr,open('research/uk-six/frames.json','w'),indent=1)
print(sum(map(len,fr.values())))
def lp(f,w,h,py,px):
    im=Image.open(f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
HERO=[(R+'p1-2.jpg',.3,.5),(R+'c3-2.jpg',.3,.5),(R+'d2-2.jpg',.4,.35)]
for (W2,H2,gap,name) in [(2000,857,8,'hero.jpg'),(1200,630,6,'og.jpg')]:
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for k,(f,py,px) in enumerate(HERO): c.paste(lp(f,pw,H2,py,px),(k*(pw+gap),0))
    c.save(O+name,quality=88)
lp(R+'c3-2.jpg',1000,1250,.3,.5).save(O+'card-hero.jpg',quality=86)
