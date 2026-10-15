"""Frames for The Hoodie Edit (14 Oct 2026). Brands' own photos. Light packshots fitted on stone (recolor); lifestyle cover-cropped."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/hoodie-edit/raw/'; O='images/hoodie-edit/'; W,H=1000,1250
sel=json.load(open('research/hoodie-edit/sel.json'))
SKIP={'i-will-not-apres-golf®-hoodie':[3]}
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
fr={}
for i in sel:
    h=i['h']; k=h[:30].replace('®',''); i['key']=k; fr[k]=[]
    for n in range(1,len(i['imgs'])+1):
        if n in SKIP.get(h,[]): continue
        src=f'{R}{h[:30]}-{n}.img'
        try: im=Image.open(src); im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); im=bg
        except Exception as e: print('bad',src,e); continue
        c,lt=frame(im); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
json.dump(fr,open('research/hoodie-edit/frames.json','w'),indent=1)
json.dump(sel,open('research/hoodie-edit/sel.json','w'),indent=1,ensure_ascii=False)
# NOTE: hero/og later replaced by a single Jones Range Hoodie shot (see build-hoodie-edit.py)
# hero triptych 2000x857 + og 1200x630 + card
def cover(p,w,h,fx=.5,fy=.3):
    im=Image.open(R+p).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
parts=[('i-will-not-apres-golf®-hoodie-4.img',.5,.4),('range-hoodie-loden-green-2.img',.5,.3),('flow-light-knit-hoodie-pine-1.img',.5,.25)]
hero=Image.new('RGB',(2000,857)); xs=[0,667,1334]; ws=[667,667,666]
for (p,fx,fy),x,w in zip(parts,xs,ws): hero.paste(cover(p,w,857,fx,fy),(x,0))
hero.save(O+'hero.jpg',quality=88)
og=Image.new('RGB',(1200,630)); 
for (p,fx,fy),x,w in zip(parts,[0,400,800],[400,400,400]): og.paste(cover(p,w,630,fx,fy),(x,0))
og.save(O+'og.jpg',quality=86)
cover('flow-light-knit-hoodie-pine-1.img',1000,1250,.5,.2).save(O+'card-hero.jpg',quality=86)
print(len(fr),sum(len(v) for v in fr.values()))
