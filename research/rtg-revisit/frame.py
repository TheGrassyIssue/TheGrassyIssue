"""Frames for the blended-interests post. 19 October 2026. White packshots: tight crop + destark (stone). Lifestyle: cover crop."""
import json,sys,numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,'.')
from destark import destark
R='research/rtg-revisit/raw/'; O='images/rtg-revisited/'; W,H=1000,1250
STONE=np.array([232,226,214.])
SEL={'w1':[0,1,2],'w2':[0,1,2],'w3':[0,1,2],'w4':[0,1,2],'l1':[0,1,2,3,4,5,6],'l2':[0,1,2,3,4],'l3':[0,1,2],'l4':[0,1,2],'l5':[0,1,2],'l6':[0,1,2],'h1':[0,1,2,3],'h2':[0,1,2],'h3':[0,1],'h4':[0,1,2],'m1':[0,2,1,4,5],'m2':[0,6,7,4,1]}
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
        key=f'{k}-{i}'; src=Image.open(f'{R}{key}.jpg').convert('RGB'); out=f'{O}{k}-{j}.jpg'
        t=None if k[0]=='h' or k in('w2','w3','w4') else tight(src)
        if t is not None: t.save(out,quality=86); destark(out,light=False,min_white=.15)
        else: cover(src,POS.get(key,.5)).save(out,quality=86)
        fr[k].append('/'+out)
json.dump(fr,open('research/rtg-revisit/frames.json','w'),indent=1)
print(sum(map(len,fr.values())))
def lp(f,w,h,py,px):
    im=Image.open(f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
L='research/rtg-revisit/life/'
import glob
G=glob.glob(L+'Hero_Images-26_aadf*')[0]
lp(G,2000,857,.42,.5).save(O+'hero.jpg',quality=88); lp(G,1200,630,.42,.5).save(O+'og.jpg',quality=88)
lp(G,1000,1250,.5,.5).save(O+'card-group.jpg',quality=86)
lp(L+'Hero_Images-29.jpg',1000,1250,.5,.5).save(O+'band-1.jpg',quality=86)
lp(glob.glob(L+'Hero_Images-26_cba5*')[0],1000,1250,.5,.15).save(O+'band-2.jpg',quality=86)
lp(G,1000,1250,.5,.85).save(O+'band-3.jpg',quality=86)

lp(R+'m1-4.jpg',1000,1250,.5,.5).save(O+'band-4.jpg',quality=86)
lp(R+'m1-5.jpg',1000,1250,.5,.5).save(O+'band-5.jpg',quality=86)
