"""Saha BTK frames. 21 Oct 2026. Stark-white packshots -> tight crop + corner flood-fill to stone (multiply keeps shadows)."""
import json,os,numpy as np
from PIL import Image,ImageDraw
R='research/saha/'; O='images/saha/'; W,H=1000,1250; STONE=np.array([232,226,214.])
CARDS={'a1':['playfield-polo'],'a2':['fairway-knight-tee'],'a3':['saha-logo-cap'],'a4':['pack-of-tees'],
'p1':['playground-polo'],'p2':['lounge-polo-green','lounge-polo-white'],
't1':['apres-golf-tee-1'],'t2':['burning-golf-cart-tee-1'],'t3':['slice-tee'],'t4':['hows-my-drive-tee'],
'b1':['locker-room-pants'],'b2':['mulligan-shorts'],
'x1':['hows-my-drive-cap'],'x2':['saha-crew-sock-pack'],'x3':['saha-crew-sock-white','saha-crew-sock-green','saha-crew-sock-black'],'x4':['saha-clip-towel']}
WHITE={'saha-crew-sock-white','lounge-polo-white','fairway-knight-tee','hows-my-drive-tee','pack-of-tees','saha-crew-sock-pack'}
d={p['handle']:p for p in json.load(open(R+'products.json'))['products']}
def frame(src,th):
    a=np.asarray(src).astype(float)
    if a[:4].min()<235 or a[-4:].min()<235:   # not a white packshot (detail/lifestyle): cover crop
        s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
    dd=255-a.min(axis=2)
    mk=Image.fromarray(((dd<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128
    out=a.copy(); w=np.clip(1-dd/40,0,1)[...,None]
    out[bg]=(a*(1-w)+a/255*STONE*w)[bg] if False else (a/255*STONE)[bg]
    ys,xs=np.where(~bg); x0,x1=np.percentile(xs,[.2,99.8]).astype(int); y0,y1=np.percentile(ys,[.2,99.8]).astype(int)
    m=int(.06*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.86/g.width,H*.8/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    edge=np.concatenate([np.asarray(g)[:3].reshape(-1,3),np.asarray(g)[-3:].reshape(-1,3)]); col=tuple(int(v) for v in np.median(edge,axis=0))
    c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
fr={}
for k,hs in CARDS.items():
    fr[k]=[]
    srcs=[(h,0) for h in hs] if len(hs)>1 else [(hs[0],i) for i in range(len(d[hs[0]]['images']))]
    if len(hs)>1: srcs+= [(h,1) for h in hs if len(d[h]['images'])>1][:1]
    for j,(h,i) in enumerate(srcs,1):
        f=f'{R}raw/{h}-{i}.img'
        if not os.path.exists(f): continue
        im=frame(Image.open(f).convert('RGB'),6 if h in WHITE else 18); out=f'{O}{k}-{j}.jpg'; im.save(out,quality=86); fr[k].append('/'+out)
json.dump(fr,open(R+'frames.json','w'),indent=1); json.dump(CARDS,open(R+'cards.json','w'),indent=1)
print({k:len(v) for k,v in fr.items()})
