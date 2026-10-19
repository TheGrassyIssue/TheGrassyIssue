"""Frames for three small brands Vol. 2 (Dim Sum, Rowena, DRVN). 19 October 2026.
Packshots (Dim Sum, DRVN) are cropped tight and destarked; Rowena on-model shots are cover-cropped."""
import json,glob,sys,numpy as np
from PIL import Image
sys.path.insert(0,'.'); sys.path.insert(0,'research/radar-three')
from destark import destark
R='research/radar-three-2/raw/'; O='images/radar-three-2/'; L='research/radar-three-2/life/'
SEL={13:[0],14:[0],17:[0],19:[0,1],30:[1,0,3],32:[0,1,3,2],35:[0,1],40:[0,1],
44:[1,0,2],45:[1,0,2],46:[0,1,2],47:[0,4,3,1,2],48:[2,1,0,3,4],49:[0,1,2],
56:[3,2,0,4,1],59:[0,2,4,1,3],60:[0,3,2,4,1],68:[0,1,3],64:[0,3,2,4],73:[2,0,1],52:[0,1,4,2],67:[0,3,1,4,2]}
LIGHT=('030-1','030-2','032-0','032-2','035-0','035-1','040-0','040-1','019-0','019-1','014-0','067-0','067-1','067-2','064-0','064-1','064-3')
W,H=1000,1250
def cover(im,py=.2,px=.5):
    s=max(W/im.width,H/im.height); im=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=int((im.width-W)*px); y=int((im.height-H)*py); return im.crop((x,y,x+W,y+H))
def tight(im, fill=.86):
    a=np.asarray(im).astype(int); border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if border.std(axis=0).max()>=16 or border.mean()<232: return None
    col=np.median(border,axis=0); diff=np.abs(a-col).max(axis=2)>22
    ys,xs=np.where(diff)
    if len(xs)<500: return None
    x0,x1=np.percentile(xs,[.2,99.8]).astype(int); y0,y1=np.percentile(ys,[.2,99.8]).astype(int)
    m=int(.04*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(im.width,x1+m),min(im.height,y1+m)
    g=im.crop((x0,y0,x1,y1)); s=min(W*.92/g.width,H*fill/g.height)
    g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS); c=Image.new('RGB',(W,H),tuple(int(v) for v in col)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
from PIL import ImageDraw, ImageFilter
STONE=np.array([232,226,214.])
def soft(im,zoom=1.18):
    """White-on-white packshots: flood only the true backdrop (thresh 5) so white garments keep their color."""
    a=np.asarray(im).astype(float); p=im.copy(); w,h=im.size
    for s_ in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(w//2,h-1),(0,h//2),(w-1,h//2)]:
        if min(p.getpixel(s_))>=245: ImageDraw.floodfill(p,s_,(255,0,255),thresh=5)
    pa=np.asarray(p); m=((pa[...,0]==255)&(pa[...,1]==0)&(pa[...,2]==255)).astype('uint8')*255
    m=np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.5))).astype(float)[...,None]/255
    o=Image.fromarray((a*(1-m)+(a*STONE/255)*m).clip(0,255).astype('uint8'))
    s=max(W/w,H/h)*zoom; o=o.resize((round(w*s),round(h*s)),Image.LANCZOS); x=(o.width-W)//2; y=(o.height-H)//2
    return o.crop((x,y,x+W,y+H))
fr={}
for n,idx in SEL.items():
    fr[n]=[]
    for k,i in enumerate(idx,1):
        key=f'{n:03d}-{i}'; src=Image.open(f'{R}{key}.jpg').convert('RGB')
        out=f'{O}p{n:03d}-{k}.jpg'
        if n<=43 and key in LIGHT: soft(src).save(out,quality=86); fr[n].append('/'+out); continue
        t=None if 44<=n<=49 else tight(src)
        (t if t is not None else cover(src)).save(out,quality=86)
        if not 44<=n<=49: destark(out, light=key in LIGHT, min_white=.15)
        fr[n].append('/'+out)
json.dump(fr,open('research/radar-three-2/frames.json','w'),indent=1)
def lp(f,w,h,py,px):
    im=Image.open(f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
HERO=[(L+'ds-2547.jpg',.5,.12),(L+'rw-DSC07046.jpg',.45,.5),(L+'dr-streamsong.jpg',.5,.62)]
for (W2,H2,gap,name) in [(2000,857,8,'hero.jpg'),(1200,630,6,'og.jpg')]:
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for k,(f,py,px) in enumerate(HERO): c.paste(lp(f,pw,H2,py,px),(k*(pw+gap),0))
    c.save(O+name,quality=88)
BANDS=[(L+'ds-8806.jpg',.5,.5),(L+'ds-2545.jpg',.5,.5),(L+'ds-2547.jpg',.5,.2),
 (L+'rw-DSC07046.jpg',.4,.5),(R+'049-2.jpg',.5,.5),(R+'048-2.jpg',.5,.5),
 (L+'dr-streamsong.jpg',.5,.6),(R+'052-3.jpg',.5,.5),(R+'064-4.jpg',.5,.5)]
for n,(f,py,px) in enumerate(BANDS,1): lp(f,W,H,py,px).save(f'{O}band-{n}.jpg',quality=86)
soft(Image.open(L+'ds-protour.jpg').convert('RGB'),zoom=1.0).save(O+'band-3.jpg',quality=86)  # ProTour polo; hero carries the tee photo
lp(L+'dr-streamsong.jpg',1000,1250,.5,.62).save(O+'card-drvn.jpg',quality=86)
lp(R+'013-0.jpg',1000,1250,.5,.5).save(O+'card-dimsum.jpg',quality=86); destark(O+'card-dimsum.jpg',min_white=.15)
lp(L+'rw-DSC07046.jpg',1000,1250,.4,.5).save(O+'card-rowena.jpg',quality=86)
print(sum(map(len,fr.values())))
