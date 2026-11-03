"""Fall colorways frames, 2 Nov 2026. Brand CDN images (research/collabs-nov/raw/NN-j); pale sweeps remapped to stone."""
import json, os
import numpy as np
from PIL import Image
R='research/collabs-nov/raw/'; O='images/collabs-nov/'; os.makedirs(O,exist_ok=True)
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

NOSTONE={'c2-0','c2-1','c2-2','c2-3','c2-4','c2-5','c3-0','c3-1','c3-2','c3-3','c3-4','c4-0','c4-1','c4-2','sm-0','sm-1','sm-2','sm-3','wh-1.jpg','wh-2.jpg','wh-3.jpg','wh-4.jpg','wh-5.jpg','f23-1.jpg','f23-2.jpg','fx-MacKenzie_23rd_edition_lockerroom_Fyfe_Golf.jpg','fx-MacKenzie_24th_Edition_lockerroom_fyfe_golf.jpg'}
def img(t):
    if t in NOSTONE: return fit(Image.open(R+t).convert('RGB')) if False else cover(Image.open(R+t).convert('RGB'))
    im=stone(t if t.startswith('research') else R+t); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
    cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)])
    return fit(im) if (cs.std(0).max()<8 and cs.mean(0).min()>200) else cover(im)



F={'e25':['c1-0','c1-1','c1-3','c1-4'],'cg3':['c0-0','c0-1','c0-2'],
'mahj':['c2-3','c2-0','c2-2'],'blade':['c3-0','c3-3'],'drv':['c4-1','c4-0','c4-2'],
'sock':['c5-0','c5-2','c5-3'],'sdrv':['c8-0','c8-1','c8-3'],'rbag':['c7-0','c7-1'],
'am90':['c9-0','c9-1','c9-4'],'next':['c10-0','c10-1','c10-3'],
'pv':['c11-0','c11-2','c11-3'],'hset':['c16-0','c16-1','c16-2'],'vblade':['c14-0','c14-1','c14-2'],
'diam':['c17-1','c17-3','c17-4'],'mossy':['c18-0','c18-1','c18-3'],'iwn':['c19-0','c19-2','c19-3'],
'rvwb':['rb-0.png','rb-1.png','rb-2.png'],'rvwm':['rm-0.png','rm-1.png'],
'hiroki':['wh-0.png','wh-1.jpg','wh-3.jpg','wh-4.jpg'],
'ftmal':['ft-MALLET_1.jpg','ft-MALLET_3.jpg','ft-MALLET_4.jpg'],'ftbrl':['ft-BRLDRIVER_2.jpg','ft-BRLDRIVER_1.jpg','ft-BRLDRIVER_4.jpg'],'ftbld':['ft-BLADE_1.jpg','ft-BLADE_3.jpg','ft-BLADE_5.jpg'],
'f23':['f23-0.jpg','f23-1.jpg','f23-3.jpg'],'f24':['f24-0.jpg','f24-1.jpg']}
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}p{k}-{n}.jpg'; img(t).convert('RGB').save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/collabs-nov/frames.json','w'),indent=1)
h=cover(Image.open(R+'c2-5').convert('RGB'),2000,857,.5,.45)
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+'sm-3').convert('RGB'),1000,1250).save(O+'card-hero.jpg',quality=86,optimize=True)
BIG={'manors':['sm-3','sm-2'],'pare':['c2-4','c3-1'],'dormie':['c5-1','c8-2'],'eastside':['c9-2','c10-2'],'vessel':['c11-1','c13-2'],'apres':['c17-0','c19-1'],'rvw':['rb-0.png','rm-0.png'],'hiroki':['wh-2.jpg','wh-5.jpg'],'firsttee':['ft-MALLET_3.jpg','ft-BRLDRIVER_2.jpg'],'fyfe':['fx-MacKenzie_23rd_edition_lockerroom_Fyfe_Golf.jpg','fx-MacKenzie_24th_Edition_lockerroom_fyfe_golf.jpg']}
for k,ts in BIG.items():
    for n,t in enumerate(ts,1):
        im=Image.open(R+t); im=stone(R+t) if (im.mode in ('RGBA','P','LA') or (t.endswith('.jpg') and t not in NOSTONE)) else im.convert('RGB')
        (fit(im,1200,1500) if t.startswith(('rb-','rm-','ft-','f24-')) else cover(im,1200,1500,.5,.3)).save(f'{O}big-{k}-{n}.jpg',quality=86,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
