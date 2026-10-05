import json,glob,os,re
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
R='research/bag-hang/'
SEL={'G04':[0,2,3,5],'G05':[0,1,3,4,6],'G06':[0,2,4,5],'G08':[2,3,0,1],
'T02':[0,3,4,5],'T04':[0,1,2],'T05':[0,1,2,4],'T07':[0,1,3,2],
'R01':[0,1,2,4],'R02':[4,3,5,6],'R03':[0,4,1,2],'R04':[0,1],'R06':[0,4,9,10],
'H01':[0,2,3,1],'H02':[6,0,2,3],'H04':[0,3,2,1],'H05':[0,1,2],'H06':[0,1,2,6],
'B01':[0,1,2],'B02':[0,1,2,3],'B03':[0,1],'B07':[0,1],
'K01':[0,1,3],'K03':[0,1,5,3],'K04':[0,1,2,3],'K06':[0,1]}
W,H=1000,1250
def load(p):
  im=Image.open(p)
  if im.mode in('RGBA','LA','P'):
    im=im.convert('RGBA');bg=Image.new('RGB',im.size,'white');bg.paste(im,mask=im.split()[3]);im=bg
  return im.convert('RGB')
def light_border(im):
  a=np.asarray(im.resize((200,int(200*im.height/im.width))))
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
  return (b.min(axis=1)>=225).mean()>0.85
def cover(im,cy=0.5):
  w,h=im.size;r=W/H
  if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
  else: nh=int(w/r);y=int((h-nh)*cy);im=im.crop((0,y,w,y+nh))
  return im.resize((W,H),Image.LANCZOS)
def contain(im):
  a=np.asarray(im);col=tuple(int(v) for v in np.median(np.concatenate([a[0],a[-1]]),axis=0))
  im.thumbnail((W,H),Image.LANCZOS);bg=Image.new('RGB',(W,H),col);bg.paste(im,((W-im.width)//2,(H-im.height)//2));return bg
out={}
for c,idx in SEL.items():
  out[c]=[]
  for n,i in enumerate(idx):
    p=glob.glob(f'{R}raw/{c}-{i}.*')[0];im=load(p)
    w,h=im.size
    f=contain(im) if (light_border(im) and abs(w/h-W/H)>0.05) else cover(im)
    dst=f'images/bag-hang/{c.lower()}-{n+1}.jpg';f.save(dst,'JPEG',quality=86,optimize=True,progressive=True);out[c].append('/'+dst)
json.dump(out,open(R+'frames.json','w'),indent=1);print(sum(len(v) for v in out.values()),'frames')
