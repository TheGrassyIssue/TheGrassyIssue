"""Fall colorways frames, 2 Nov 2026. Brand CDN images (research/around-greens/raw/NN-j); pale sweeps remapped to stone."""
import json, os
import numpy as np
from PIL import Image
R='research/around-greens/raw/'; O='images/around-the-greens/'; os.makedirs(O,exist_ok=True)
STONE=np.array((232,226,214),float)
def cover(im,w=1000,h=1250,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def stone(path):
    _im=Image.open(path)
    if _im.mode in ('RGBA','LA','P'):
        _im=_im.convert('RGBA'); _bg=Image.new('RGBA',_im.size,(255,255,255,255)); _bg.alpha_composite(_im); _im=_bg
    a=np.array(_im.convert('RGB')).astype(float)
    k=max(4,a.shape[0]//40); cs=np.concatenate([a[:k,:k].reshape(-1,3),a[:k,-k:].reshape(-1,3),a[-k:,:k].reshape(-1,3),a[-k:,-k:].reshape(-1,3)])
    bg=np.median(cs,0)
    if bg.min()<200 or (bg.max()-bg.min())>14: return Image.fromarray(a.astype(np.uint8))
    d=np.abs(a-bg).max(2); w=np.clip(1-d/26,0,1)[...,None]
    return Image.fromarray((a*(1-w)+np.clip(a*(STONE/bg),0,255)*w).clip(0,255).astype(np.uint8))
def fit(im,w=1000,h=1250):
    # square/landscape flats: trim to the product, then pad onto the background instead of cropping
    if im.width/im.height<=0.9: return cover(im,w,h)
    a0=np.array(im).astype(int); bg=tuple(int(v) for v in a0[3,3]); dm=np.abs(a0-np.array(bg)).max(2)>7; ys,xs=np.where(dm)
    if len(ys):
        mx=int(.12*max(xs.max()-xs.min(),ys.max()-ys.min()))
        im=im.crop((max(0,xs.min()-mx),max(0,ys.min()-mx),min(im.width,xs.max()+mx),min(im.height,ys.max()+mx)))
    s=min(w/im.width,h/im.height)*.92; t=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(w,h),bg); c.paste(t,((w-t.width)//2,(h-t.height)//2)); return c

NOSTONE=set()
def img(t):
    if t in NOSTONE: return cover(Image.open(R+t).convert('RGB'))
    im=stone(t if t.startswith('research') else R+t); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
    cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)])
    return fit(im) if (cs.std(0).max()<8 and cs.mean(0).min()>200) else cover(im)



F={'m1':['m1-1','m1-2','m1-3'],'m2':['n5-0','n5-2','n5-1'],'m3':['m3-0','m3-1','m3-3'],'m4':['n4-0','n4-1'],'m5':['n2-0','n2-1','n2-2'],'m6':['m6-1','m6-0','m6-2'],'m7':['m7-0'],'m8':['m8-0'],'m9':['n3-0','n3-2','n3-3'],
'd1':['d1-1','d1-0','d1-3'],'d2':['d2-0','d2-1'],'d3':['d3-0','d3-1','d3-3'],'d4':['d4-0','d4-1','d4-3'],'d5':['d5-1','d5-0'],'d6':['d6-0','d6-1','d6-2'],'d7':['d7-0','d7-1','d7-2'],'d8':['d8-2','d8-0','d8-3'],'d9':['d9-0','d9-1'],
'p1':['p1-0','p1-1','p1-2'],'p2':['p2-0','p2-1'],'p3':['p3-0','p3-1','p3-3'],'p4':['p4-0','p4-1'],'p5':['p5-0','p5-1'],'p6':['p6-1','p6-0','p6-2'],'p7':['p7-0','p7-2','p7-1'],'p8':['p8-1','p8-0','p8-3'],'p9':['p9-0','p9-1','p9-2'],
'w1':['w1-0','w1-1','w1-2'],'w2':['x1-1','x1-0','x1-2'],'w3':['x2-0','x2-1','x2-2'],'w4':['w4-0','w4-1','w4-2'],'w5':['w5-1','w5-0','w5-3'],'w6':['w6-2','w6-0','w6-3'],'w7':['w7-0','w7-1','w7-2'],'w8':['x3-0','x3-1','x3-2'],'w9':['x4-0']}
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}p{k}-{n}.jpg'; img(t).convert('RGB').save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/around-greens/frames.json','w'),indent=1)
tri=[('m1-0',.5),('w3-0',.4),('p3-1',.5)]
h=Image.new('RGB',(2000,857),tuple(int(v) for v in STONE)); x=0
for (t,fy),w in zip(tri,(666,668,666)):
    h.paste(cover(Image.open(R+t).convert('RGB'),w-4 if x else w-2,857,.5,fy),(x+(2 if x else 0),0)); x+=w
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+'m1-0').convert('RGB'),1000,1250).save(O+'card-hero.jpg',quality=86,optimize=True)
B={'band-1':['d8-1','d1-2','d3-2'],'band-2':['p3-2','w5-2','w3-3']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(R+t).convert('RGB'),1000,1250).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
