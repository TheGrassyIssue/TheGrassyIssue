"""Upgrading Your Golf Bag v2 frames, 1 Nov 2026. Each maker's own CDN images; white/pale-gray sweeps remapped to TGI stone.
MacKenzie cards use its collaboration editions (ACL Golf, Jain Golf) and the band uses Fyfe x MacKenzie lookbook photos already on site."""
import json, os, sys
import numpy as np
from PIL import Image
STONE=np.array((232,226,214),float)
def cover(im,w=1000,h=1250,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def stone(path):
    a=np.array(Image.open(path).convert('RGB')).astype(float)
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
R='research/bag-upgrade-v2/raw/'; S2='research/bag-upgrade-v2/st2/'; M='images/mackenzie/'; FY='images/fyfe-mackenzie/'
O='images/bag-upgrade/'; os.makedirs(O,exist_ok=True)
def src(t):
    p,f=t.split(':',1)
    return {'r':R,'s':S2,'m':M,'f':FY}[p]+f
F={
 'rye':['r:sh-custom-rye-4-0-00','r:sh-custom-rye-4-0-04','r:sh-custom-rye-4-0-03','r:sh-custom-rye-4-0-02'],
 'kantle':['r:sh-custom-kantle-4-0-00','r:sh-custom-kantle-4-0-02','r:sh-custom-kantle-4-0-06','r:sh-custom-kantle-4-0-12'],
 'shsun':['r:sh-custom-sunday-4-0-00','r:sh-custom-sunday-4-0-10','r:sh-custom-sunday-4-0-02','r:sh-custom-sunday-4-0-08'],
 'standard':['r:sho-standard-black-00','r:sho-standard-sage-00','r:sho-standard-black-01','r:sho-standard-sage-02'],
 'reserve':['r:sho-reserve-00','r:sho-reserve-01','r:sho-reserve-02','r:sho-reserve-03'],
 'simple':['r:sho-sunday-00','r:sho-sunday-01','r:sho-sunday-02','r:sho-sunday-03'],
 'trouper':['r:jo-trouper-4-0-evergreen-kodiak-01','r:jo-trouper-4-0-onyx-kodiak-01','r:jo-trouper-4-0-ecru-01','r:jo-trouper-4-0-cedar-01','r:jo-trouper-4-0-ecru-00'],
 'rover':['r:jo-rover-stand-bag-high-desert-06','r:jo-rover-stand-bag-cedar-02','r:jo-rover-stand-bag-high-desert-07','r:jo-rover-stand-bag-cedar-00'],
 'original':['r:jo-original-jones-bag-navy-white-01','r:jo-original-jones-bag-navy-white-05','r:jo-original-jones-bag-navy-white-00'],
 'mkwax':['m:acl-mackenzie-x-acl-golf-8-green-waxed-canvas-ca-1.jpg','m:acl-mackenzie-x-acl-golf-8-olive-waxed-canvas-ca-1.jpg','m:acl-mackenzie-x-acl-golf-8-green-waxed-canvas-ca-2.jpg','m:acl-mackenzie-x-acl-golf-8-olive-waxed-canvas-ca-3.jpg'],
 'mknylon':['m:acl-mackenzie-x-acl-golf-8-nylon-adult-carry-bag-1.jpg','m:acl-mackenzie-x-acl-golf-8-nylon-adult-carry-bag-4.jpg','m:acl-mackenzie-x-acl-golf-8-nylon-adult-carry-bag-2.jpg','m:acl-mackenzie-x-acl-golf-8-nylon-adult-carry-bag-3.jpg'],
 'mktreated':['m:jain-jain-mackenzie-canvas-bag-1.jpg','m:jain-jain-mackenzie-canvas-bag-3.jpg','m:jain-jain-mackenzie-canvas-bag-5.jpg','m:jain-jain-mackenzie-canvas-bag-6.jpg'],
 'vsunday':['r:ve-sunday-iv-leather-stand-crimson-00','r:ve-sunday-iv-leather-stand-croc-black-00','r:ve-sunday-iv-leather-stand-crimson-03','r:ve-sunday-iv-leather-stand-croc-black-05'],
 'vlux':['r:ve-lux-stand-crosshatch-navy-05','r:ve-lux-stand-crosshatch-navy-06','r:ve-lux-stand-crosshatch-navy-00','r:ve-lux-stand-crosshatch-navy-03'],
 'vcarry':['r:ve-sunday-carry-olive-04','r:ve-sunday-carry-03','r:ve-sunday-carry-01','r:ve-sunday-carry-olive-00'],
 'sl2':['s:l-gb','s:l-1276','s:g-orange','s:g-mid','s:g-glacier'],
 'air':['s:a-fog','s:a-onyx','r:st-air-00','r:st-air-06'],
 'slsun':['s:s-mid','r:st-sunday-00','r:st-sunday-02','r:st-sunday-06'],
 'ryder':['r:sg-ryder-green-04','r:sg-ryder-green-05','r:sg-ryder-black-02','r:sg-ryder-almond-02'],
 'elcamino':['r:sg-elcamino-seafoam-02','r:sg-elcamino-gray-02','r:sg-elcamino-seafoam-00','r:sg-elcamino-gray-00'],
 'loma':['r:sg-loma-00','r:sg-loma-01','r:sg-loma-02'],
}
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}{k}-{n}.jpg'
        im=stone(src(t)); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
        cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)]); flat=cs.std(0).max()<8
        (fit(im) if flat else cover(im)).save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/bag-upgrade-v2/frames.json','w'),indent=1)
h=Image.open(M+'life-crinan-28.jpg').convert('RGB')
cover(h,2000,857,.5,.6).save(O+'hero.jpg',quality=88,optimize=True)
cover(h,1200,630,.5,.6).save(O+'og.jpg',quality=84)
cover(h,1000,1250,.5,.5).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':['r:jo-rover-stand-bag-cedar-08','r:jo-trouper-4-0-cedar-06','r:jo-rover-stand-bag-high-desert-01'],
   'band-2':['m:life-affric-hut.jpg','m:life-dunes-fescue.jpg','f:7th-camper.jpg'],
   'band-3':['r:sg-ryder-black-01','s:l-1182','r:sg-elcamino-seafoam-03']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(src(t)).convert('RGB'),1000,1250).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
