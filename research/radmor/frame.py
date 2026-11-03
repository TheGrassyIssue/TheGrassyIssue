"""Fall colorways frames, 2 Nov 2026. Brand CDN images (research/radmor/raw/NN-j); pale sweeps remapped to stone."""
import json, os
import numpy as np
from PIL import Image
R='research/radmor/raw/'; O='images/radmor/'; os.makedirs(O,exist_ok=True)
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



F={'0': ['0-1', '0-0', '0-2'], '1': ['1-1', '1-0', '1-2'], '2': ['2-0', '2-1'], '3': ['3-0', '3-1', '3-2'], '5': ['5-1', '5-0', '5-2'], '6': ['6-1', '6-0', '6-2'], '11': ['11-0', '11-1'], '12': ['12-1', '12-0', '12-2'], '13': ['13-1', '13-0', '13-2'], '14': ['14-0', '14-1'], '15': ['15-0', '15-1'], '22': ['22-1', '22-0', '22-2'], '23': ['23-1', '23-0', '23-2'], '24': ['24-0', '24-1'], '27': ['27-0', '27-1'], '28': ['28-1', '28-0'], '37': ['37-1', '37-0', '37-2'], '41': ['41-0', '41-1', '41-2'], '42': ['42-1', '42-0', '42-2'], '43': ['43-1', '43-0', '43-2'], '44': ['44-1', '44-0', '44-2'], '45': ['45-0', '45-2'], '61': ['61-0', '61-1', '61-2'], '63': ['63-0', '63-2'], '64': ['64-0', '64-2'], '65': ['65-0', '65-2'], '67': ['67-1', '67-0', '67-2'], '71': ['71-1', '71-0', '71-2'], '72': ['72-0', '72-1', '72-2'], '96': ['96-1', '96-0'], '113': ['113-1', '113-0', '113-2'], '115': ['115-1', '115-0', '115-2'], '121': ['121-0', '121-1', '121-2'], '127': ['127-1', '127-0', '127-2'], '128': ['128-1', '128-0', '128-2'], '129': ['129-0', '129-2'], '135': ['135-0', '135-1'], '136': ['136-1', '136-0', '136-2'], '139': ['139-0', '139-1'], '140': ['140-0', '140-1', '140-2'], '142': ['142-0', '142-1', '142-2'], '143': ['143-0', '143-1', '143-2'], '146': ['146-0', '146-1', '146-2'], '77': ['77-0'], '98': ['98-0', '98-2'], '86': ['86-0', '86-1'], '97': ['97-0', '97-1', '97-2'], '144': ['144-0', '144-1'], '82': ['82-0', '82-2'], '103': ['103-0', '103-1', '103-2'], '99': ['99-0'], '90': ['90-0', '90-2'], '123': ['123-0', '123-1', '123-2'], '91': ['91-0']}
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}p{k}-{n}.jpg'; img(t).convert('RGB').save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/radmor/frames.json','w'),indent=1)
h=cover(Image.open(R+'w-Shadow_Course_1_Shopify_Wide.jpg').convert('RGB'),2000,857,.5,.12)
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+'128-1').convert('RGB'),1000,1250).save(O+'card-hero.jpg',quality=86,optimize=True)
B={'band-1':['64-1','65-1','63-1'],'band-2':['77-1','45-1','90-1']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(R+t).convert('RGB'),1000,1250,.5,.3).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
