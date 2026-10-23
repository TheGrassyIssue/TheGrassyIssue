"""Frame the extra product images (23 Oct 2026, Lenny: "the last few posts need more images in each products box").
research/extra-images/<post>/c<card>-<n>.jpg -> images/<dir>/p-<card>-x<n>.jpg (1000x1250, stone for flat light backdrops, cover-crop for photos).
Writes research/extra-images/<post>/frames.json {card: [web paths]} for the builders."""
import json,glob,os,re,numpy as np
from PIL import Image,ImageDraw
W,H=1000,1250;STONE=np.array([232,226,214.])
DIR={'outdoor-golf':'outdoor-golf','dogs-golf':'dogs-golf','golfer-style':'golfer-style'}
DROP={'outdoor-golf':{'c33-1.jpg','c33-2.jpg','c34-2.jpg','c34-3.jpg','c35-1.jpg','c35-2.jpg','c35-3.jpg'},  # Goldwin colours not on sale
      'dogs-golf':{'c9-2.jpg'}}  # 516px
def cover(src,cx=.5,cy=.5):
    s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def frame(src,th=18):
    a=np.asarray(src).astype(float)
    cc=np.concatenate([a[:10,:10].reshape(-1,3),a[:10,-10:].reshape(-1,3),a[-10:,:10].reshape(-1,3),a[-10:,-10:].reshape(-1,3)])
    if cc.min()<200 or cc.std()>8: return cover(src)
    col=np.median(cc,axis=0); mk=Image.fromarray(((np.abs(a-col).max(axis=2)<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128
    if bg.mean()>0.97 or bg.mean()<0.05: return cover(src)
    out=a.copy(); out[bg]=STONE; ys,xs=np.where(~bg)
    x0,x1=np.percentile(xs,[.2,99.8]).astype(int); y0,y1=np.percentile(ys,[.2,99.8]).astype(int)
    m=int(.05*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.80/g.width,H*.74/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
for post,d in DIR.items():
    R=f'research/extra-images/{post}/'; FR={}
    for f in sorted(glob.glob(R+'c*-*.jpg'),key=lambda x:[int(t) for t in re.findall(r'\d+',os.path.basename(x))]):
        b=os.path.basename(f)
        if b in DROP.get(post,()): continue
        card,n=re.match(r'c(\d+)-(\d+)\.jpg',b).groups()
        out=f'images/{d}/p-{card}-x{n}.jpg'
        if not os.path.exists(out):
            im=Image.open(f).convert('RGB'); im.thumbnail((1250,1250)); frame(im).save(out,quality=84,optimize=True)
        FR.setdefault(card,[]).append('/'+out)
    json.dump(FR,open(R+'frames.json','w'),indent=1); print(post,len(FR),'cards',sum(len(v) for v in FR.values()),'frames')
