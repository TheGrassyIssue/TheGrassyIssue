import json,subprocess,io,os,concurrent.futures as cf
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
R='research/best25-signature/';OUT='images/best25/'
W,H=1000,1250
TOP,BOT=np.array((242,238,230),float),np.array((228,222,210),float)
G=(TOP*(1-np.linspace(0,1,H)[:,None,None])+BOT*np.linspace(0,1,H)[:,None,None]).repeat(W,1)
def load(b):
  im=Image.open(io.BytesIO(b))
  if im.mode in ('RGBA','LA','P','PA'):
    im=im.convert('RGBA');bg=Image.new('RGB',im.size,'white');bg.paste(im,mask=im.split()[3]);return bg
  return im.convert('RGB')
def frame(im):
  a=np.asarray(im.resize((200,max(1,int(200*im.height/im.width))))).astype(int)
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);light=(b.min(axis=1)>=185).mean()>0.85 and b.std(axis=0).max()<18
  w,h=im.size;r=W/H
  if light:
    col=np.median(b,axis=0)
    t=im.copy();t.thumbnail((int(W*.88),int(H*.88)),Image.LANCZOS)
    bg=Image.new('RGB',(W,H),tuple(int(c) for c in col));bg.paste(t,((W-t.width)//2,(H-t.height)//2))
    arr=np.asarray(bg).astype(float)
    return Image.fromarray((arr*G/np.maximum(col,1)).clip(0,255).astype(np.uint8)),'pack'
  if w/h>r: nw=int(h*r);x=(w-nw)//2;im=im.crop((x,0,x+nw,h))
  else: nh=int(w/r);y=int((h-nh)*.4);im=im.crop((0,y,w,y+nh))
  return im.resize((W,H),Image.LANCZOS),'life'
import hashlib
os.makedirs(R+'raw',exist_ok=True)
def get(u):
  if not u.startswith('http'): return open(R+u,'rb').read()
  c=R+'raw/'+hashlib.md5(u.encode()).hexdigest()
  if os.path.exists(c) and os.path.getsize(c)>1000: return open(c,'rb').read()
  b=subprocess.run(['curl','-s','-L','--max-time','40','-A','Mozilla/5.0',u],capture_output=True).stdout
  open(c,'wb').write(b);return b
ORDER=json.load(open(R+'order.json'))
jobs=[]
for s in ORDER:
  d=json.load(open(R+s+'.json'))
  for kind,pre in (('picks','p'),('alternates','a')):
    for i,p in enumerate(d.get(kind,[]),1):
      srcs=p.get('images_local') or p.get('images') or p.get('reference_images') or []
      for n,u in enumerate(srcs[:5],1): jobs.append((s,f'{pre}{i}',n,u))
def run(j):
  s,k,n,u=j;os.makedirs(OUT+s,exist_ok=True);dst=f'{OUT}{s}/{k}-{n}.jpg'
  try:
    im,t=frame(load(get(u)));im.save(dst,quality=85,optimize=True,progressive=True);return (s,k,'/'+dst,t)
  except Exception as e: return (s,k,None,str(e)[:60])
with cf.ThreadPoolExecutor(12) as ex: res=list(ex.map(run,jobs))
F={}
for s,k,dst,t in res:
  if dst: F.setdefault(s,{}).setdefault(k,[]).append([dst,t])
  else: print('fail',s,k,t)
for s in F:
  for k in F[s]:
    F[s][k].sort()
    packs=[x for x in F[s][k] if x[1]=='pack'];lifes=[x for x in F[s][k] if x[1]!='pack']
    F[s][k]=packs+lifes
json.dump(F,open(R+'frames.json','w'),indent=1);print('done',sum(len(v) for x in F.values() for v in x.values()))

# MOGSHADE OVERRIDE: Mogshade shoots on coloured paper; lift the product onto the house gradient (6 Oct 2026).
import sys;sys.path.insert(0,R)
from bgcut import cut,cut_flat
d=json.load(open(R+'mogshade.json'))
for kind,pre in (('picks','p'),('alternates','a')):
  for i,pp in enumerate(d[kind],1):
    k=f'{pre}{i}';u=pp['images'][0];im=load(get(u))
    f=(cut_flat if 'towel' in pp['title'].lower() else cut)(im)
    dst=f'{OUT}mogshade/{k}-1.jpg';f.save(dst,quality=85,optimize=True,progressive=True)
    lst=F['mogshade'][k];lst=[x for x in lst if x[0]!='/'+dst];F['mogshade'][k]=[['/'+dst,'pack']]+lst
json.dump(F,open(R+'frames.json','w'),indent=1);print('mogshade cut')
