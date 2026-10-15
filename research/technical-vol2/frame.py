"""Frames for Technical Brands Roundup Vol. 2 (15 Oct 2026). Brands' own photos. Light packshots fitted on stone (recolor); lifestyle cover-cropped."""
import json,sys,glob,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/technical-vol2/raw/'; O='images/technical-vol2/'; W,H=1000,1250
IM=json.load(open('research/technical-vol2/imgs.json'))
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>205, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.4):
    lt,col=light(im)
    if lt:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>20; ys,xs=np.where(m)
        if len(xs)>100:
            x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
            pad=int(.06*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
            s=min(W*.9/g.width,H*.9/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
            c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    # dark/lifestyle wide images: fit on blurred-free solid edge colour if very wide, else cover
    if im.width/im.height>1.25:
        e=np.asarray(im).astype(int); col=tuple(int(x) for x in np.median(np.concatenate([e[0],e[-1]]),axis=0))
        s=W/im.width; g=im.resize((W,round(im.height*s)),Image.LANCZOS)
        if g.height<H*0.45:  # too short: cover instead
            pass
        else:
            c=Image.new('RGB',(W,H),col); c.paste(g,(0,(H-g.height)//2)); return c,False
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
fr={}
for k,L in IM.items():
    fr[k]=[]
    for n in range(1,len(dict.fromkeys(L))+1):
        src=f'{R}{k}-{n}.img'
        im=Image.open(src); im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); im=bg
        c,lt=frame(im); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
json.dump(fr,open('research/technical-vol2/frames.json','w'),indent=1); print(sum(len(v) for v in fr.values()))

