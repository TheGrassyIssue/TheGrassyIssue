import json,glob
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
R='research/golden-hour/'
SEL={'g01':('stripe-pique-polo',[0,1,2,6,7]),'g02':('heritage-polo',[0,2,3,5,1]),'g03':('clubhouse-waffle-polo',[0,1,2,3]),
'g04':('amen-corner-tee',[0,1,2,3]),'g05':('g',[0,2,1,3]),'g06':('rugby-sweatshirt',[0,1,3,4]),
'g07':('lightweight-track-jacket',[0,2,3,4]),'g08':('lightweight-track-pant',[0,2,4,3]),'g11':('the-links-layer',[0,2,3,7]),
'g12':('the-links-pants',[0,1,3,4]),'g10':('double-pleated-shorts',[0,1,2,3,4]),'g13':('golden-hour-tote-bag',[0,1,2])}
W,H=1000,1250
def load(p):
  im=Image.open(p)
  if im.mode in('RGBA','LA','P'): im=im.convert('RGBA');bg=Image.new('RGB',im.size,'white');bg.paste(im,mask=im.split()[3]);im=bg
  return im.convert('RGB')
def uniform_border(im):
  a=np.asarray(im.resize((200,int(200*im.height/im.width)))).astype(int)
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);return b.std(axis=0).max()<8,np.median(b,axis=0)
def cover(im,cy=.5):
  w,h=im.size;r=W/H
  if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
  else: nh=int(w/r);y=int((h-nh)*cy);im=im.crop((0,y,w,y+nh))
  return im.resize((W,H),Image.LANCZOS)
def frame(p,cy=.5):
  im=load(p);u,col=uniform_border(im)
  if u and im.width/im.height>0.85:
    t=im.copy();t.thumbnail((W,H),Image.LANCZOS);bg=Image.new('RGB',(W,H),tuple(int(c) for c in col));bg.paste(t,((W-t.width)//2,(H-t.height)//2));return bg
  return cover(im,cy)
if __name__=='__main__':
  out={}
  for k,(h,idx) in SEL.items():
    out[k]=[]
    for n,i in enumerate(idx):
      f=frame(glob.glob(f'{R}raw/{h}-{i}.*')[0]);dst=f'images/golden-hour/{k}-{n+1}.jpg';f.save(dst,'JPEG',quality=86,optimize=True,progressive=True);out[k].append('/'+dst)
  json.dump(out,open(R+'frames.json','w'),indent=1)
  B={'band-1':('home/62d87b0e-30a2-4e93-977d-2c65034999e0.jpg',.4),'band-2':('home/DSCF0577_cbff93a2-4566-4847-95dd-abc6955aa935.jpg',.4),'band-3':('home/af69ad49-89d0-4a7a-88ed-8e064f251f5a.jpg',.6),
     'band-4':('raw/azalea-stripe-polo-0.*',.3),'band-5':('raw/azalea-stripe-polo-1.*',.3),'band-6':('raw/golden-patch-panel-1-1.*',.3),
     'band-7':('raw/the-track-set-0.*',.4),'band-8':('raw/the-windbreaker-0.*',.5),'band-9':('raw/signiture-logo-long-sleeve-tee-0.*',.4),
     'band-10':('raw/essential-tee-0.*',.5),'band-11':('raw/the-groovy-5-panel-1.*',.4),'band-12':('raw/studio-tee-0.*',.4)}
  for k,(g,cy) in B.items():
    p=glob.glob(R+g)[0];cover(load(p),cy).save(f'images/golden-hour/{k}.jpg','JPEG',quality=85,optimize=True,progressive=True)
  print(sum(len(v) for v in out.values()),'frames')
