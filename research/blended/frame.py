"""Frames for the blended-interests post. 19 October 2026. White packshots: tight crop + destark (stone). Lifestyle: cover crop."""
import json,sys,numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,'.')
from destark import destark
R='research/blended/raw/'; O='images/blended/'; W,H=1000,1250
STONE=np.array([232,226,214.])
SEL={'c1':[0,1,2],'c2':[0,1],'c3':[0,1],'c4':[0,1],'c5':[0,1,2],'c6':[0,1],
't1':[1,0,2],'t2':[0],'t3':[0,1],'t4':[0,1],'t5':[0,1,2],'t6':[0,1,2],
'f1':[0,1,2],'f2':[0,1,2],'f3':[0,1],'f4':[0,1],'f5':[0,1,2],'f6':[0,2,1],
'v1':[0,1],'v2':[0,1,2],'v3':[0],'v4':[0,1],'v5':[0,1],'v6':[0,1,2],
'r1':[0,1,2],'r2':[0,1],'r3':[0,1],'r4':[2,0,1],'r5':[0,1,2],'r6':[0,1],
's1':[0,1],'s2':[0,1,2],'s3':[0,1],'s4':[0,1],'s5':[0],'s6':[0]}
POS={'c3-1':.5,'c6-0':.3,'t5-0':.5,'s2-0':.35,'s2-2':.3,'r5-1':.3,'c1-0':.15,'f1-0':.2,'f1-1':.2,'s2-1':.15,'s2-2':.15,'s1-1':.4}
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
        key=f'{k}-{i}'; src=Image.open(f'{R}{key}.jpg').convert('RGB'); out=f'{O}{k}-{j}.jpg'
        t=tight(src)
        if t is not None: t.save(out,quality=86); destark(out,light=False,min_white=.15)
        else: cover(src,POS.get(key,.5)).save(out,quality=86)
        fr[k].append('/'+out)
json.dump(fr,open('research/blended/frames.json','w'),indent=1)
print(sum(map(len,fr.values())))
def lp(f,w,h,py,px):
    im=Image.open(f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
HERO=[(R+'c1-0.jpg',.2,.5),(R+'f2-1.jpg',.5,.5),(R+'s2-0.jpg',.4,.5)]
for (W2,H2,gap,name) in [(2000,857,8,'hero.jpg'),(1200,630,6,'og.jpg')]:
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for k,(f,py,px) in enumerate(HERO): c.paste(lp(f,pw,H2,py,px),(k*(pw+gap),0))
    c.save(O+name,quality=88)
lp(R+'f2-1.jpg',1000,1250,.5,.5).save(O+'card-fly.jpg',quality=86)
lp(R+'c1-0.jpg',1000,1250,.2,.5).save(O+'card-climb.jpg',quality=86)
