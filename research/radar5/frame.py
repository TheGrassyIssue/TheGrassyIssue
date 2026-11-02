"""Radar Vol. 5 frames (ITL Golf, Masterpiece Sports Club, 52 Sundays), 2 Nov 2026. Brand CDN images; pale sweeps remapped to TGI stone."""
import json, os
import numpy as np
from PIL import Image
R='research/radar5/raw/'; O='images/radar-three-5/'; os.makedirs(O,exist_ok=True)
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

def img(t):
    im=stone(R+t); a=np.array(im).astype(float); q=max(4,a.shape[0]//40)
    cs=np.concatenate([a[:q,:q].reshape(-1,3),a[:q,-q:].reshape(-1,3),a[-q:,:q].reshape(-1,3),a[-q:,-q:].reshape(-1,3)])
    return fit(im) if (cs.std(0).max()<8 and cs.mean(0).min()>200) else cover(im)
i='itl/'; m='msc/'; s='s52/'
G='mens-itl-2-0-signature-glove-'
F={
 'it-glove':[i+G+'classic-colors-04',i+G+'classic-colors-00',i+G+'seasonal-colors-00',i+G+'seasonal-colors-07',i+G+'seasonal-colors-09',i+G+'seasonal-colors-06'],
 'it-practice':[i+'mens-itl-practice-glove-01',i+'mens-itl-practice-glove-00',i+'mens-itl-practice-glove-06',i+'mens-itl-practice-glove-04'],
 'it-woods':[i+'itl-premium-leather-driver-cover-01',i+'itl-premium-leather-driver-cover-00',i+'itl-premium-leather-driver-cover-05',i+'itl-premium-leather-fairway-cover-01',i+'itl-premium-leather-driver-cover-09'],
 'it-blade':[i+'itl-premium-blade-cover-01',i+'itl-premium-blade-cover-00',i+'itl-premium-blade-cover-06',i+'itl-premium-blade-cover-04'],
 'it-tourn':[i+'mens-itl-leather-tournament-belt-01',i+'mens-itl-leather-tournament-belt-00',i+'mens-itl-leather-tournament-belt-04',i+'mens-itl-leather-tournament-belt-07'],
 'it-woodsbelt':[i+'mens-itl-leather-woods-belt-00',i+'mens-itl-leather-woods-belt-01',i+'mens-itl-leather-woods-belt-04',i+'mens-itl-leather-woods-belt-07'],
 'it-wallet':[i+'itl-leather-glove-wallet-01',i+'itl-leather-glove-wallet-00',i+'itl-leather-glove-wallet-06',i+'itl-leather-glove-wallet-09'],
 'it-duffle':[i+'itl-leather-monarch-duffle-03',i+'itl-leather-monarch-duffle-00',i+'itl-leather-monarch-duffle-06',i+'itl-leather-monarch-duffle-01'],
 'it-cap':[i+'the-players-cap-01',i+'the-players-cap-07',i+'the-players-cap-02',i+'the-players-cap-00'],
 'ms-tritech':[m+'0.1',m+'0.0',m+'0.4',m+'0.3',m+'0.6'],
 'ms-wave':[m+'1.1',m+'1.0',m+'1.3',m+'1.5'],
 'ms-short':[m+'2.1',m+'2.0',m+'3.0',m+'2.4',m+'3.3'],
 'ms-pant':[m+'4.2',m+'4.3',m+'4.0',m+'4.1'],
 'ms-hoodie':[m+'5.1',m+'5.0',m+'5.3',m+'5.5'],
 'ms-vest':[m+'6.3',m+'6.0',m+'6.1'],
 'ms-glove':[m+'7.1',m+'7.0',m+'8.1',m+'8.0',m+'9.0'],
 'ms-cap':[m+'10.1',m+'10.0',m+'10.2',m+'10.3'],
 'ms-bag':[m+'11.1',m+'11.0',m+'11.2',m+'11.4'],
 's5-gsup':[s+'gs-up-holes-down-tee-black-00',s+'gs-up-holes-down-tee-forest-green-00',s+'gs-up-holes-down-tee-white-00',s+'gs-up-holes-down-tee-black-01'],
 's5-cherries':[s+'sunday-cherries-tee-03',s+'sunday-cherries-tee-00',s+'sunday-cherries-tee-05',s+'sunday-cherries-tee-01'],
 's5-hermosa':[s+'hermosa-sage-polo-03',s+'hermosa-sage-polo-00',s+'hermosa-sage-polo-02',s+'hermosa-sage-polo-01'],
 's5-fairway':[s+'fairway-hat-pine-00',s+'fairway-hat-eucalyptus-00',s+'fairway-hat-indigo-blue-00',s+'fairway-hat-burgundy-00',s+'fairway-hat-smoke-00'],
 's5-ballhog':[s+'the-ball-hog-classic-black-walnut-00',s+'the-ball-hog-classic-red-tan-00',s+'the-ball-hog-classic-black-walnut-02',s+'the-ball-hog-classic-red-tan-02'],
 's5-icon':[s+'icon-driver-cover-02',s+'icon-driver-cover-00',s+'52-icon-3wood-headcover-00',s+'icon-driver-cover-04'],
 's5-reserve':[s+'the-pro-five-reserve-driver-headcover-00',s+'the-pro-five-reserve-driver-headcover-01',s+'the-pro-five-reserve-driver-headcover-02'],
 's5-rope':[s+'pro-five-golf-rope-hat-00',s+'pro-five-golf-rope-hat-01',s+'pro-five-golf-rope-hat-02',s+'pro-five-golf-rope-hat-03'],
 's5-towels':[s+'read-the-break-golf-towel-02',s+'course-no-52-golf-towel-00',s+'station-052-golf-towel-02',s+'read-the-break-golf-towel-00',s+'station-052-golf-towel-00'],
}
FR={}
for k,ts in F.items():
    FR[k]=[]
    for n,t in enumerate(ts,1):
        o=f'{O}{k}-{n}.jpg'; img(t).save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/radar5/frames.json','w'),indent=1)
tri=[(i+G+'seasonal-colors-06',.5),(m+'4.2',.5),(s+'hermosa-sage-polo-03',.4)]
h=Image.new('RGB',(2000,857),tuple(int(v) for v in STONE)); x=0
for (t,fy),w in zip(tri,(666,668,666)):
    h.paste(cover(Image.open(R+t).convert('RGB'),w-4 if x else w-2,857,.5,fy),(x+(2 if x else 0),0)); x+=w
h.save(O+'hero.jpg',quality=86,optimize=True)
og=h.resize((1200,514),Image.LANCZOS); c=Image.new('RGB',(1200,630),tuple(int(v) for v in STONE)); c.paste(og,(0,58)); c.save(O+'og.jpg',quality=84)
cover(Image.open(R+i+G+'classic-colors-04').convert('RGB'),1000,1250).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':[i+G+'seasonal-colors-03',i+G+'classic-colors-06',i+'mens-itl-practice-glove-07'],
   'band-2':[m+'4.3',m+'1.2',m+'11.2'],
   'band-3':[s+'hermosa-sage-polo-04',s+'52-icon-3wood-headcover-02',s+'course-no-52-golf-towel-02']}
for b,ts in B.items():
    for n,t in enumerate(ts,1): cover(Image.open(R+t).convert('RGB'),1000,1250).save(f'{O}{b}-{n}.jpg',quality=84,optimize=True)
print('ok',sum(len(v) for v in FR.values()))
