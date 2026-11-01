"""Siegelman Stable Revisited frames, 31 Oct 2026. Product shots from the brand's Shopify CDN (2400x3000, fetched at 1250w);
pale #f7f7f7 sweeps remapped to TGI stone. Lifestyle: Maxfli 'Harness the Drive' and Yankees SS26 lookbook pages on siegelmanstable.com."""
import json, os
import numpy as np
from PIL import Image, ImageFilter
R='research/siegelman-revisit/raw/'; L='research/siegelman-revisit/life/'; O='images/siegelman-stable-revisit/'
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
F={0:[1,0,2,3],1:[1,0,3,4],5:[1,0,3,4],6:[1,0,4,2],7:[1,0,4],8:[0,1],
   9:[4,3,0],10:[4,3,0],11:[4,1,9,11],12:[1,0,4,3],13:[1,0,4,8],14:[1,0,3,2],15:[1,0,4,5],16:[1,0,4,7],
   18:[0,3,1],19:[0,3,1],20:[0,1,3],21:[0,1],22:[0,3,1],23:[0,3,6],24:[8,0,3,6],25:[1,0,2],26:[0,2,1],
   27:[3,0,4],28:[1,3,7,2],29:[1,3,7,9],30:[3,2,0],31:[1,3,0],32:[0,2],33:[2,4,0],34:['L:SS_NYY_SS2690.jpg',0,1],35:['L:SS_NYY_SS2678.jpg',0],36:[1,0,4]}
FR={}
for i,js in F.items():
    FR[i]=[]
    for n,j in enumerate(js,1):
        o=f'{O}p{i:02d}-{n}.jpg'; src=(L+j[2:]) if isinstance(j,str) else f'{R}{i:02d}-{j:02d}.jpg'; cover(stone(src),fy=.4 if isinstance(j,str) else .5).save(o,quality=86,optimize=True); FR[i].append('/'+o)
json.dump(FR,open('research/siegelman-revisit/frames.json','w'),indent=1)
g=Image.open(L+'Untitled_-_June_16_2026_at_10.40.30-59.png').convert('RGB')
cover(g,2000,857,.5,.55).filter(ImageFilter.UnsharpMask(radius=1.2,percent=60,threshold=2)).save(O+'hero.jpg',quality=88,optimize=True)
cover(g,1200,630,.5,.55).save(O+'og.jpg',quality=84)
cover(Image.open(L+'SS_X_MAXFLI0403-Edit.jpg').convert('RGB'),1000,1250,.5,.4).save(O+'card-hero.jpg',quality=84,optimize=True)
B={'band-1':[('Untitled_-_June_16_2026_at_10.40.30-58.png',.5,.5),('SS_X_MAXFLI0403-Edit.jpg',.5,.4),('Untitled_-_June_16_2026_at_10.40.30-60.png',.5,.5)],
   'band-2':[('SS_NYY_SS26-85.jpg',.5,.4),('SS_NYY_SS2682.jpg',.5,.4),('SS_NYY_SS2677.jpg',.5,.4)]}
for b,fs in B.items():
    for k,(f,fx,fy) in enumerate(fs,1): cover(Image.open(L+f).convert('RGB'),1000,1250,fx,fy).save(O+f'{b}-{k}.jpg',quality=84,optimize=True)
print(len(FR),sum(len(v) for v in FR.values()))
