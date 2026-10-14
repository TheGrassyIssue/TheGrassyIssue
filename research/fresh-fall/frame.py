"""Frames for "Three fresh fall drops" (13 Oct 2026): Students Fall Drop 2, Walker Kooka Classics, Sugarloaf October drop.
Brands' own photos from each store. Light packshots fitted on stone (recolor); lifestyle cover-cropped. argv: brand keys to run."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/fresh-fall/raw/'; O='images/fresh-fall/'; W,H=1000,1250
P=json.load(open('research/fresh-fall/picks.json'))
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>205, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.3):
    lt,col=light(im)
    if lt:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>20; ys,xs=np.where(m)
        if len(xs)>100:
            x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
            pad=int(.06*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
            s=min(W*.9/g.width,H*.9/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
            c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
try: fr=json.load(open('research/fresh-fall/frames.json'))
except Exception: fr={}
for b in (sys.argv[1:] or P):
    for it in P[b]:
        k=it['key']; fr[k]=[]
        for n in range(1,len(it['imgs'])+1):
            src=f'{R}{k}-{n}.jpg'
            try: im=Image.open(src); im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); im=bg
            except Exception as e: print('bad',src,e); continue
            c,lt=frame(im); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
            if lt: recolor(out,thresh=14)
            fr[k].append('/'+out)
json.dump(fr,open('research/fresh-fall/frames.json','w'),indent=1); print(len(fr))
