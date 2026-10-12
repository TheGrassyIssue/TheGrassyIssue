"""Frames for Grips Vol. 2 (12 Oct 2026). Brands' own full-size photos. Rules from Lenny: high-res only, no stark white
backgrounds, colorways of one model grouped in one card. Packshots are cropped to the product then padded to 4:5 and
destarked; lifestyle shots lead each gallery. Images under 900px on the short side are skipped."""
import json,glob,re,sys,numpy as np
from PIL import Image
sys.path.insert(0,'.')
from destark import destark
sys.path.insert(0,'research/grips-vol2')
from recolor import recolor, grade
D='research/grips-vol2/'; R=D+'raw/'; O='images/grips-vol2/'
W,H=1000,1250
SKIP={'cadmex-03','cadab-03','cadbasic-03','cwzen-02','absolutex-01','absolutex-02','army10-01','blackarmy-01','blackarmy-03','blackarmy-04','blackout-01','blackout-02','evose-01','iclassic-01','ix23-01','sticky18-01','sticky23-01','stickycamo-01','backcountry-03','sinatra-03'}
def uniform(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    return b.std(axis=0).max()<16 and b.mean()>200, np.median(b,axis=0)
def cover(im,py=.5):
    s=max(W/im.width,H/im.height); im=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*py); return im.crop((x,y,x+W,y+H))
def fitpad(im):
    # fit whole photo to 1000 wide, extend top/bottom by edge replication (no hard pad lines)
    s=W/im.width; g=im.resize((W,round(im.height*s)),Image.LANCZOS)
    if g.height>=H: y=(g.height-H)//2; return g.crop((0,y,W,y+H))
    a=np.asarray(g); t=(H-g.height)//2; b=H-g.height-t
    a=np.concatenate([np.repeat(a[:1],t,0),a,np.repeat(a[-1:],b,0)],0); return Image.fromarray(a)
def tight(im,col,fill=.94):
    a=np.asarray(im).astype(int); diff=np.abs(a-col).max(axis=2)>28; ys,xs=np.where(diff)
    x0,x1=np.percentile(xs,[.3,99.7]).astype(int); y0,y1=np.percentile(ys,[.3,99.7]).astype(int)
    m=int(.04*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(im.width,x1+m),min(im.height,y1+m)
    g=im.crop((x0,y0,x1,y1)); s=min(W*fill/g.width,H*fill/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in col)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
exec(open(D+'cards.py').read())
import os
FJ=D+'frames.json'
fr=json.load(open(FJ)) if os.path.exists(FJ) else {}
keys=sys.argv[1:] or list(CARDS)
for k in keys:
    if k=='army10': continue
    files=[f for f in sorted(glob.glob(f'{R}{k}-*.jpg')) if f.split('/')[-1][:-4] not in SKIP]
    life,packs=[],[]
    for f in files:
        im=Image.open(f).convert('RGB')
        if min(im.size)<900: continue
        u,col=uniform(im)
        (packs if u else life).append((f,im,col,u))
    seq=(life[:2]+packs+life[2:]) if k not in ('j25links','j25links2','t01field','tw97') else packs+life
    fr[k]=[]
    for n,(f,im,col,u) in enumerate(seq[:8],1):
        out=f'{O}{k}-{n}.jpg'
        ((fitpad(im) if k.startswith('cw') else tight(im,col)) if u else cover(im,.45)).save(out,quality=88)
        (grade(out) if k.startswith('cw') else recolor(out) if k.startswith('cad') else destark(out,min_white=0.2))
        fr[k].append('/'+out)
    json.dump(fr,open(FJ,'w'),indent=1); print(k,len(fr[k]),flush=True)
print({k:len(v) for k,v in fr.items() if len(v)<2}, sum(map(len,fr.values())))
