import json,glob,os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
R='research/hat-brands/'
SEL={'BOTH1':[0,1,2,3,4],'BOTH2':[0,1,3,4,5],'BOTH3':[0,1,2,4],'BOTH4':[0,1,2,4],'BOTH5':[0,4,5,2],
'ENG1':[0,3],'ENG2':[0,3],'ENG3':[0,2],
'REP1':[0,1,2,4],'REP2':[0,1,2,4],'REP3':[0,1,2,4],'REP4':[0,1,2,3],'REP5':[0,1,2,4],
'ORI1':[0,1,2,3],'ORI2':[0,1,2,3],'ORI3':[0,1,2,3],'ORI4':[0,1,3,4],
'FTP1':[0],'FTP2':[0,1,2,3],'FTP3':[0,2,1,5],'FTP4':[0,1,2,3],'FTP6':[0,1],
'FCO1':[0,1,2],'FCO2':[0,2,3,5],'FCO3':[0,2,4,5],'FCO6':[0,2,4,5],'FCO7':[0,2,4,5]}
W,H=1000,1250
TOP,BOT=np.array((242,238,230),float),np.array((228,222,210),float)
grad=(TOP*(1-np.linspace(0,1,H)[:,None,None])+BOT*np.linspace(0,1,H)[:,None,None]).repeat(W,1)
def load(p):
  im=Image.open(p)
  if im.mode in('RGBA','LA','P'): im=im.convert('RGBA');bg=Image.new('RGB',im.size,'white');bg.paste(im,mask=im.split()[3]);im=bg
  return im.convert('RGB')
def frame(p):
  im=load(p);a=np.asarray(im.resize((200,max(1,int(200*im.height/im.width))))).astype(int)
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);light=(b.min(axis=1)>=228).mean()>0.9 and b.std(axis=0).max()<10
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
    f=frame(glob.glob(f'{R}raw/{c}-{i}.*')[0]);dst=f'images/hat-brands/{c.lower()}-{n+1}.jpg';f.save(dst,'JPEG',quality=86,optimize=True,progressive=True);out[c].append('/'+dst)
json.dump(out,open(R+'frames.json','w'),indent=1)
L=json.load(open(R+'life.json'))
B={'both':[('both',0,.25),('both',3,.3),('both',9,.5)],'engel':[('engel',2,.5),('engel',6,.5),('engel',5,.5)],
'represent':[('represent',0,.3),('represent',32,.3),('represent',31,.3)],'orien':[('orien',0,.3),('orien',12,.3),('orien',13,.3)],
'ftp':[('ftp',3,.3),('ftp',9,.25),('ftp',10,.4)],'fandco':[('fandco',0,.3),('fandco',26,.3),('fandco',27,.5)]}
for sec,lst in B.items():
  for n,(k,i,cy) in enumerate(lst):
    im=load(R+L[k][i][0]);w,h=im.size;r=W/H
    if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
    else: nh=int(w/r);y=int((h-nh)*cy);im=im.crop((0,y,w,y+nh))
    if im.width>W: im=im.resize((W,H),Image.LANCZOS)
    im.save(f'images/hat-brands/band-{sec}-{n+1}.jpg','JPEG',quality=85,optimize=True,progressive=True)
im=load(R+L['fandco'][1][0]);w,h=im.size;nh=int(w*685/1600);y=int((h-nh)*.55)
c=im.crop((0,y,w,y+nh));c.resize((1600,685),Image.LANCZOS).save('images/hat-brands/hero.jpg',quality=86);c.resize((1200,514)).save('images/hat-brands/og.jpg',quality=84)
print(sum(len(v) for v in out.values()),'frames')
