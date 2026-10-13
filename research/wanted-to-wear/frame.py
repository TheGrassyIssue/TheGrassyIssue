"""Frames for the "clothes we wanted to wear" post (12 Oct 2026). Each brand's own photos.
Light studio packshots -> fitted on stone (recolor); lifestyle -> cover crop. Existing TGI frames reused where already 1000x1250."""
import json,sys,shutil,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/wanted-to-wear/raw/'; O='images/wanted-to-wear/'; W,H=1000,1250
NEW={"smathers":["1.jpg","2.jpg","3.webp"],"devereux":["3.jpg","1.jpg","4.jpg","2.jpg","5.jpg"],"oddritual":["2.jpg","1.jpg","3.jpg","5.jpg"],
"olydoe":["2.jpg","1.jpg","3.jpg","4.jpg"],"latenine":["2.jpg","1.jpg","3.jpg","4.jpg"],"jancraig":["1.jpg","2.jpg","3.jpg"]}
REUSE={"manors":["images/manors/core-course-polo-a2.jpg","images/manors/core-course-polo.jpg","images/manors/core-course-polo-a3.jpg","images/manors/core-course-polo-a4.jpg"],
"lof":[f"images/left-of-field/bridgewater-1-4-zip-8-{i}.jpg" for i in range(5)],
"woodgrain":[f"images/woodgrain/relaxed-double-pleated-trouser-{i}.jpg" for i in (1,2,3,4)],
"parmore":[f"images/parmore/camo-1-4-zip-rebrand-{i}.jpg" for i in (1,2,3,4,5)]}
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>205, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.25):
    lt,col=light(im)
    if lt:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>20; ys,xs=np.where(m)
        x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
        pad=int(.06*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
        s=min(W*.9/g.width,H*.9/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
        c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
fr={}
for k,fs in NEW.items():
    fr[k]=[]
    for n,f in enumerate(fs,1):
        out=f'{O}{k}-{n}.jpg'; c,lt=frame(Image.open(R+f'{k}-{f}').convert('RGB')); c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
for k,fs in REUSE.items():
    fr[k]=[]
    for n,f in enumerate(fs,1):
        out=f'{O}{k}-{n}.jpg'; im=Image.open(f).convert('RGB')
        (im if im.size==(W,H) else im.resize((W,H),Image.LANCZOS)).save(out,quality=86); fr[k].append('/'+out)
json.dump(fr,open('research/wanted-to-wear/frames.json','w'),indent=1); print({k:len(v) for k,v in fr.items()})

# ---- v2 (Lenny: "needs more everything"): second pieces + four more brands ----
import os
def flat(im):
    if im.mode in ('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); return bg
    return im.convert('RGB')
NEW2={"latenine2":["1.jpg","2.jpg","3.jpg"],"olydoe2":["1.jpg","2.jpg","3.jpg","4.jpg"],"localgc2":["1.png","2.png","3.png"]}
for k,fs in NEW2.items():
    fr[k]=[]
    for n,f in enumerate(fs,1):
        out=f'{O}{k}-{n}.jpg'; c,lt=frame(flat(Image.open(R+f'{k}-{f}'))); c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
for k,fs in json.load(open('research/wanted-to-wear/reuse2.json')).items():
    fr[k]=[]
    for n,f in enumerate(fs,1):
        out=f'{O}{k}-{n}.jpg'; im=Image.open(f.lstrip('/')).convert('RGB')
        if abs(im.width/im.height-.8)>.02: c,lt=frame(im)
        else: c=im.resize((W,H),Image.LANCZOS); lt=light(c)[0]
        c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
json.dump(fr,open('research/wanted-to-wear/frames.json','w'),indent=1); print({k:len(v) for k,v in fr.items()})
