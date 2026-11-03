"""Fall colorways frames, 2 Nov 2026. Brand CDN images (research/vest-edit-2/raw/NN-j); pale sweeps remapped to stone."""
import json, os
import numpy as np
from PIL import Image
R='research/vest-edit-2/raw/'; O='images/vest-edit/'; os.makedirs(O,exist_ok=True)
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

NOSTONE={'57-0','57-2'}
def img(t):
    if t in NOSTONE: return cover(Image.open(R+t).convert('RGB'))
    im=stone(t if t.startswith('research') else R+t); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
    cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)])
    return fit(im) if (cs.std(0).max()<8 and cs.mean(0).min()>200) else cover(im)


F={'2':['jl-1','jl-0','jl-2'],'30':['30-0','30-1','30-4'],'41':['41-0','41-1','41-4'],'57':['57-0','57-1','57-2'],'22':['22-0','22-1'],'14':['14-0','14-2','14-1'],
'0':['0-0','0-2','0-1'],'8':['8-1','8-0','8-3'],'15':['15-1','15-0','15-3'],'40':['40-0','40-1','40-3'],'27':['27-0','27-2','27-1'],'5':['5-1','5-0','5-4'],
'1':['1-0','1-1','1-3'],'9':['9-1','9-0','9-3'],'12':['12-2','12-0','12-4'],'13':['13-0','13-4','13-1'],'3':['3-1','3-0','3-2'],'10':['10-1','10-0','10-3'],
'21':['21-2','21-0','21-3'],'32':['32-0','32-1','32-4'],'33':['33-1','33-0','33-2'],'52':['52-0','52-1'],'59':['59-0','59-2'],'43':['43-0','43-1','43-2']}
F.update({'s16':['s16-0','s16-1','s16-2','s16-3'],'s29':['s29-1','s29-0','s29-2','s29-3'],'s50':['s50-1','s50-0','s50-2'],
's4':['s4-0','s4-1','s4-4','s4-2'],'s59':['s59-1','s59-0','s59-3','s59-2'],'s125':['s125-0','s125-1','s125-3'],
'sen':['sen-1','sen-0','sen-4'],'s0':['s0-1','s0-0','s0-3'],'s81':['s81-1','s81-0','s81-2'],
'pd':['pd-1','pd-0','pd-4'],'s90':['s90-1','s90-0','s90-4'],'s151':['s151-1','s151-3','s151-2']})
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}p{k}-{n}.jpg'; img(t).convert('RGB').save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/vest-edit-2/frames.json','w'),indent=1)
tri=[('14-0',.3),('13-0',.25),('8-1',.25)]
h=Image.new('RGB',(2000,857),tuple(int(v) for v in STONE)); x=0
for (t,fy),w in zip(tri,(666,668,666)):
    h.paste(cover(Image.open(R+t).convert('RGB'),w-4 if x else w-2,857,.5,fy),(x+(2 if x else 0),0)); x+=w
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+'14-0').convert('RGB'),1000,1250).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':['12-3','10-2','13-3'],'band-2':['21-1','8-2','59-1']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(R+t).convert('RGB'),1000,1250).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
