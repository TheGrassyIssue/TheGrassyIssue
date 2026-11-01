"""Paris Golf Gallery BTK frames, 1 Nov 2026. Product shots from parisgolfgallery.com Shopify CDN (fetched at 1600w);
pale sweeps remapped to TGI stone. Lifestyle from the shop's own homepage (PGG_Shop.jpg tees shot, BF_4119 perfume)."""
import json, os
import numpy as np
from PIL import Image, ImageFilter
R='research/pgg/raw/'; L='research/pgg/life/'; O='images/paris-golf-gallery/'
os.makedirs(O,exist_ok=True)
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
F={'wash':[3,4,1,0],'classic':[0,2,1,3],'decks':[0,2,1],'gtees':[3,5,4],'music':[0],'football':[0],
   'qzipc':[0,2,1,3],'mat':['PAIR',2,5,1],'scarf':[0,2,3,4],'ashtray':[2,0,1],'palo':[0,2,1],'perfume':[3,0,2],
   'baggy':[0,1],'lof':[0,4,1,3],'pluto':[0,1,2],'odd':[3,0,1],'pare':[4,0,1],'pxg':[0,2,4],
   'vibe':[0,1,2],'brutta':[2,3,0,4],'hof':[3,0,1,2],'lostballs':[0,1,2,3],'val':[0,3,2,5],'slice':[3,0,1]}
import sys; sys.path.insert(0,'research/pgg'); from deblack import deblack
for f in ['wash-0','wash-5','wash-1','wash-2','wash-3','wash-4','classic-0','classic-1','classic-2','classic-3']: deblack(f'{R}{f}.jpg',f'{R}{f}-s.jpg')
def matpair(o):
    ims=[]
    for f in ('mat-0','mat-3'):
        a=np.array(Image.open(R+f+'.jpg').convert('RGB')); m=a.min(2)<235; ys,xs=np.where(m)
        ims.append(Image.fromarray(a[ys.min():ys.max()+1,xs.min():xs.max()+1]))
    c=Image.new('RGB',(1000,1250),tuple(int(v) for v in STONE))
    for i,im in enumerate(ims):
        im=im.resize((round(im.width*1180/im.height),1180),Image.LANCZOS).convert('RGBA').rotate(-14 if i==0 else -14,expand=True,resample=Image.BICUBIC)
        sh=Image.new('RGBA',im.size,(0,0,0,0)); sh.putalpha(im.split()[3].point(lambda v: int(v*.25)))
        x=330+i*250-im.width//2; y=(1250-im.height)//2
        c.paste((60,50,40),(x+14,y+14),sh.split()[3].filter(ImageFilter.GaussianBlur(10))); c.paste(im,(x,y),im)
    c.save(o,quality=88,optimize=True)
FR={}
for k,js in F.items():
    FR[k]=[]
    for n,j in enumerate(js,1):
        o=f'{O}{k}-{n}.jpg'
        if j=='PAIR': matpair(o); FR[k].append('/'+o); continue
        fit(stone(f'{R}{k}-{j}' + ('-s' if k in ('wash','classic') else '') + '.jpg')).save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/pgg/frames.json','w'),indent=1)
s=Image.open(L+'PGG_Shop.jpg').convert('RGB')
cover(s,2000,857,.5,.5).save(O+'hero.jpg',quality=88,optimize=True)
cover(s,1200,630,.5,.5).save(O+'og.jpg',quality=84)
cover(s,1000,1250,.5,.5).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':[('L','BF_4119.jpg',.5,.5),('R','ashtray-3.jpg',.5,.5),('R','gtees-1.jpg',.5,.5)]}
for b,fs in B.items():
    for k,(d,f,fx,fy) in enumerate(fs,1): cover(Image.open((L if d=='L' else R)+f).convert('RGB'),1000,1250,fx,fy).save(O+f'{b}-{k}.jpg',quality=84,optimize=True)
print(len(FR),sum(len(v) for v in FR.values()))
