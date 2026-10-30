"""BEAMS Golf Revisited frames, 30 Oct 2026. Product + staff-styling shots from cdn.beams.co.jp (O size, 1200x1440);
pale studio sweeps remapped to TGI stone with a soft weight. FW26 lookbook frame aw25 downloaded via Chrome with Lenny's OK."""
import json, os, glob
import numpy as np
from PIL import Image
R='research/beams-revisit/raw/'; L='research/beams-revisit/life/'; O='images/beams-golf-revisit/'
STONE=np.array((232,226,214),float)
def cover(im,w=1000,h=1250,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def stone(path):
    a=np.array(Image.open(path).convert('RGB')).astype(float)
    if '11180218403' in path: h,w=a.shape[:2]; a[:int(h*.2),int(w*.72):]=a[2:6,2:6].reshape(-1,3).mean(0)
    k=max(4,a.shape[0]//40); cs=np.concatenate([a[:k,:k].reshape(-1,3),a[:k,-k:].reshape(-1,3),a[-k:,:k].reshape(-1,3),a[-k:,-k:].reshape(-1,3)])
    bg=np.median(cs,0)
    if bg.min()<200 or (bg.max()-bg.min())>14: return Image.fromarray(a.astype(np.uint8))
    d=np.abs(a-bg).max(2); w=np.clip(1-d/26,0,1)[...,None]
    return Image.fromarray((a*(1-w)+np.clip(a*(STONE/bg),0,255)*w).clip(0,255).astype(np.uint8))
IDS=open('research/beams-revisit/ids.txt').read().split()
FR={}
for i in IDS:
    order=[f'{R}{i}_{p}.jpg' for p in ('D_1','C_1','D_2','D_3','C_2','D_4')]
    fs=[f for f in order if os.path.exists(f)][:4]
    FR[i]=[]
    for j,f in enumerate(fs,1):
        o=f'{O}{i}-{j}.jpg'; cover(stone(f)).save(o,quality=86,optimize=True); FR[i].append('/'+o)
json.dump(FR,open('research/beams-revisit/frames.json','w'),indent=1)
def tri(fs,o,w=2000,h=857):
    c=Image.new('RGB',(w,h)); cw=w//3
    for k,(f,fx,fy) in enumerate(fs): c.paste(cover(Image.open(f).convert('RGB'),cw if k<2 else w-2*cw,h,fx,fy),(k*cw,0))
    c.save(o,quality=86,optimize=True)
from PIL import ImageFilter
_h=Image.open(L+'beams-golf26aw18.jpg').convert('RGB')
cover(_h,2000,857,.5,.55).filter(ImageFilter.UnsharpMask(radius=1.2,percent=60,threshold=2)).save(O+'hero.jpg',quality=88,optimize=True)
cover(_h,1200,630,.5,.55).save(O+'og.jpg',quality=84)
cover(Image.open(L+'beams-golf26aw27.jpg').convert('RGB'),1000,1250,.5,.6).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':[('beams-golf26aw19',.5,.5),('beams-golf26aw28',.5,.6),('beams-golf26aw31',.5,.5)],
   'band-2':[('beams-golf26aw16',.5,.4),('beams-golf26aw6',.5,.4),('beams-golf26aw5',.5,.5)],
   'band-3':[('beams-golf26aw26',.5,.5),('beams-golf26aw29',.5,.55),('beams-golf26aw30',.5,.5)]}
for b,fs in B.items():
    for k,(f,fx,fy) in enumerate(fs,1): cover(Image.open(L+f+'.jpg').convert('RGB'),1000,1250,fx,fy).save(O+f'{b}-{k}.jpg',quality=84,optimize=True)
print(len(FR),sum(len(v) for v in FR.values()))
