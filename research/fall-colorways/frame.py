"""Fall colorways frames, 2 Nov 2026. Brand CDN images (research/fall-colorways/raw/NN-j); pale sweeps remapped to stone."""
import json, os
import numpy as np
from PIL import Image
R='research/fall-colorways/raw/'; O='images/fall-colorways/'; os.makedirs(O,exist_ok=True)
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

def img(t):
    im=stone(t if t.startswith('research') else R+t); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
    cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)])
    return fit(im) if (cs.std(0).max()<8 and cs.mean(0).min()>200) else cover(im)

W='research/radar5/raw/itl/itl-leather-glove-wallet-'
F={}
for l in open('research/fall-colorways/picks.txt'):
    i=int(l.split('|')[0]); n=len(l.split('|')[4].split())
    F[i]=[f'{i:02d}-{j}' for j in range(n)]
F[16]=F[16][:3]; F[46]=F[46][:1]
for x in (4,5,10,21,36,41,42,47): F[x]=[]
for l in open('research/fall-colorways/picks2.txt'):
    k=l.split('|')[0]; n=len(l.split('|')[1].split()); F[k]=[f'{k}-{j}' for j in range(n)]
F['w3']=['w3-1','w3-0'];
for x in (0,1,2,3): F[x]=[]
for x in ('n0','n1','n2','n3','n4'): F[x]=[]
F['s1']=['s1-0','s1-2','s1-3','s1-1']; F['s2']=['s2-0','s2-1','s2-2','s2-3']; F['s3']=['s3-0','s3-1','s3-3','s3-2']; F['s4']=['s4-1','s4-2']; F['s5']=['s5-0','s5-1']; F['s6']=['s6-0','s6-1','s6-2','s6-3']; F['s7']=['s7-0','s7-1','s7-2','s7-3']; F['s8']=['s8-0']; F['s9']=['s9-0']; F['t1']=['t1-0','t1-1','t1-3']; F[17]=[]; F['n16']=['n16-1','n16-2','n16-3']; F['n8']=['n8-1','n8-2','n8-3','n8-0']; F['m4']=['m4-3','m4-2','m4-0','m4-1']; F['m1']=['m1-3','m1-0','m1-1','m1-2']
F['wallet']=[W+'00',W+'05',W+'06',W+'01']
FR={}
for k,ts in F.items():
    if not ts: continue
    FR[str(k)]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}p{k}-{n}.jpg'; img(t).save(o,quality=86,optimize=True); FR[str(k)].append('/'+o)
json.dump(FR,open('research/fall-colorways/frames.json','w'),indent=1)
tri=[('s6-0',.3),('12-0',.4),('w2-1',.3)]
h=Image.new('RGB',(2000,857),tuple(int(v) for v in STONE)); x=0
for (t,fy),w in zip(tri,(666,668,666)):
    h.paste(cover(Image.open(R+t).convert('RGB'),w-4 if x else w-2,857,.5,fy),(x+(2 if x else 0),0)); x+=w
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+'25-1').convert('RGB'),1000,1250,.5,.2).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':['07-1','33-1','34-1'],'band-2':['m3-3','n16-0','43-1']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(R+t).convert('RGB'),1000,1250).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
