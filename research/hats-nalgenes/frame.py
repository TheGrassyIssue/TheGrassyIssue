"""Frames for Hats & Nalgenes (18 Oct 2026). Each brand's own product photos."""
import json,sys,os,io,urllib.request,concurrent.futures as cf
import numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor, grade
R='research/hats-nalgenes/'; O='images/hats-nalgenes/'; W,H=1000,1250
PK=json.load(open(R+'picks.json'))
UA={'User-Agent':'Mozilla/5.0'}
def big(u):
    if u.startswith('/images/'): return None
    u=u.split('?')[0]
    return u+('?auto=format&fit=max&w=2000' if 'bigcartel' in u else '?width=2000')
def load(u):
    if u.startswith('/images/'): return Image.open('.'+u).convert('RGB')
    f=R+'cache/'+str(abs(hash(u)))+'.img'
    if not os.path.exists(f):
        os.makedirs(R+'cache',exist_ok=True); open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(big(u),headers=UA),timeout=60).read())
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); return bg
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>200 and b.std()<14, tuple(int(x) for x in np.median(b,axis=0))
def cover(im,W=W,H=H,pos=.4):
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
def fit(im,col):
    a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>22; ys,xs=np.where(m)
    if len(xs)<100: return cover(im)
    x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
    pad=int(.08*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
    s=min(W*.84/g.width,H*.84/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
def prod_frame(u,out):
    im=load(u); e=int(.015*min(im.size)); im=im.crop((e,e,im.width-e,im.height-e))
    lt,col=light(im)
    if lt and im.width>=im.height*.95: c=fit(im,col); c.save(out,quality=86); recolor(out,thresh=14)
    else:
        c=cover(im,pos=.35); c.save(out,quality=86)
        if lt: grade(out)
def band_frame(u,out):
    im=load(u); c=cover(im,pos=.35 if im.height>im.width else .5); c.save(out,quality=86)
    lt,_=light(c)
    if lt: grade(out)

fr=[]
jobs=[]
for j,p in enumerate(PK):
    fs=[]
    for k,u in enumerate(p['imgs'][:4]):
        out=f'{O}p{j+1:02d}-{k+1}.jpg'; jobs.append((u,out)); fs.append('/'+out)
    fr.append(fs)
def run(a):
    try: prod_frame(*a)
    except Exception as e: print('ERR',a,e)
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(run,jobs))
json.dump(fr,open(R+'frames.json','w'),indent=1); print(len(jobs),'frames')
