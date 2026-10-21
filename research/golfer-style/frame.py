"""Golfer style inspo frames. 21 Oct 2026. Products -> 1000x1250 (white packshots flood to stone); golfer photos copied from research frames."""
import json,shutil,numpy as np
from PIL import Image,ImageDraw
Image.MAX_IMAGE_PIXELS=None
R='research/golfer-style/';O='images/golfer-style/';W,H=1000,1250;STONE=np.array([232,226,214.])
def frame(src,force=False):
    a=np.asarray(src).astype(float)
    if not force and min(a[:8,:8].min(),a[:8,-8:].min(),a[-8:,:8].min(),a[-8:,-8:].min())<235:
        s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
    col=np.median(np.concatenate([a[:8,:8].reshape(-1,3),a[:8,-8:].reshape(-1,3),a[-8:,:8].reshape(-1,3),a[-8:,-8:].reshape(-1,3)]),axis=0)
    dd=np.abs(a-col).max(axis=2)
    mk=Image.fromarray(((dd<14)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=np.clip(a/np.maximum(col,1)*STONE,0,255)[bg]
    ys,xs=np.where(~bg)
    x0,x1=np.percentile(xs,[.3,99.7]).astype(int); y0,y1=np.percentile(ys,[.3,99.7]).astype(int)
    m=int(.06*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.86/g.width,H*.8/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
PRE={44:(540,170,880,360)}
FORCE={16,21,32,40,44}
G=json.load(open(R+'final-picks.json'));n=0
for g,ps in G.items():
    for p in ps:
        n+=1;f=p['img_file'].replace('research/golfer-style/','')
        im=Image.open(R+f).convert('RGB')
        if n in PRE: im=im.crop(PRE[n])
        frame(im,n in FORCE).save(f'{O}p-{n}.jpg',quality=84,optimize=True)
STACK={'korda':'pabc','palmer':'cgim','minwoo':'abcd','ak':'abcf','moe':'eacd'}
for k,xs in STACK.items():
    for x in xs: Image.open(f'{R}frames/{k}-{x}.jpg').save(f'{O}g-{k}-{x}.jpg',quality=84,optimize=True)
print(n)
