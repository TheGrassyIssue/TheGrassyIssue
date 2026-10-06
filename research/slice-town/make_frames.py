import json,glob
import numpy as np
from PIL import Image
R='research/slice-town/'
SEL={'S05':[0,2,4,5],'S06':[0,2,1,4],'S03':[1,3,4,2],'S04':[1,3,4,6],'S08':[0,1,3,7,5],'S09':[0,1,2,4],
'S11':[0,1,2],'S27':[2,3,1,0,4],'S02':[0,2,3,1],'S10':[3,4,5,1],'S07':[2,4],'S25':[1,3,4],
'S14':[0,1,3,2],'S13':[1,0,2,3],'S15':[0,1,2],'S28':[0,1,2],'S12':[0,3,1],'S01':[0,1,2],'S20':[1,4,2,3],'S21':[0,1,2,3],'S24':[1],'S26':[1,0,3,4],
'NAL':[('S22',0),('S23',0),('S22',1),('S23',1),('S22',2)]}
W,H=1000,1250
TOP,BOT=np.array((242,238,230),float),np.array((228,222,210),float)
grad=(TOP*(1-np.linspace(0,1,H)[:,None,None])+BOT*np.linspace(0,1,H)[:,None,None]).repeat(W,1)
def frame(p):
  im=Image.open(p).convert('RGB');a=np.asarray(im.resize((200,max(1,int(200*im.height/im.width))))).astype(int)
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);light=(b.min(axis=1)>=200).mean()>0.9 and b.std(axis=0).max()<14
  w,h=im.size;r=W/H
  if light:
    col=tuple(int(c) for c in np.median(b,axis=0))
    if abs(w/h-r)>0.03:
      t=im.copy();t.thumbnail((W,H),Image.LANCZOS);bg=Image.new('RGB',(W,H),col);bg.paste(t,((W-t.width)//2,(H-t.height)//2));im=bg
    else: im=im.resize((W,H),Image.LANCZOS)
    a=np.asarray(im).astype(float);bgc=np.array(col,float)
    return Image.fromarray((a*grad/np.maximum(bgc,1)).clip(0,255).astype(np.uint8))
  if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
  else: nh=int(w/r);y=int((h-nh)*.35);im=im.crop((0,y,w,y+nh))
  return im.resize((W,H),Image.LANCZOS)
out={}
for c,idx in SEL.items():
  out[c]=[]
  for n,i in enumerate(idx):
    src=f'{R}raw/{i[0]}-{i[1]}.jpg' if isinstance(i,tuple) else f'{R}raw/{c}-{i}.jpg'
    dst=f'images/slice-town/{c.lower()}-{n+1}.jpg';frame(src).save(dst,'JPEG',quality=86,optimize=True,progressive=True);out[c].append('/'+dst)
json.dump(out,open(R+'frames.json','w'),indent=1)
L=json.load(open(R+'life.json'))
B=[(8,.4),(7,.4),(14,.3),(11,.35),(27,.35),(3,.5),(12,.5),(2,.5),('5top',.5)]
for n,(i,cy) in enumerate(B,1):
  im=Image.open(R+L[5][0]).convert('RGB').crop((0,0,2000,1290)) if i=='5top' else Image.open(R+L[i][0]).convert('RGB');w,h=im.size;r=W/H
  if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
  else: nh=int(w/r);y=int((h-nh)*cy);im=im.crop((0,y,w,y+nh))
  im.resize((W,H),Image.LANCZOS).save(f'images/slice-town/band-{n}.jpg',quality=85,optimize=True,progressive=True)
h=Image.open(R+'hero-opt-H.jpg');h.save('images/slice-town/btk-hero.jpg',quality=86);h.resize((1200,514),Image.LANCZOS).save('images/slice-town/btk-og.jpg',quality=84)
# homepage card: option B, the white back print in the city (Lenny, 6 Oct)
im=Image.open(R+L[8][0]).convert('RGB');w,hh=im.size;r=1080/1350
if w/hh>r: nw=int(hh*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,hh))
else: nh=int(w/r);y=int((hh-nh)*.4);im=im.crop((0,y,w,y+nh))
im.resize((1080,1350),Image.LANCZOS).save('images/slice-town/btk-card-hero.jpg',quality=85)
print(sum(len(v) for v in out.values()))
