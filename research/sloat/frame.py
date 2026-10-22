"""SLOAT BTK frames. 21 Oct 2026. Studio shots are on a warm tan backdrop (no white) -> cover crop to 1000x1250. Up to 4 per card. Lifestyle -> images/sloat/life-N.jpg."""
import json,os,urllib.request
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
R='research/sloat/';O='images/sloat/';W,H=1000,1250
d={p['handle']:p for p in json.load(open(R+'products.json'))['products']}
def cover(im):
    s=max(W/im.width,H/im.height);im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS);x=(im.width-W)//2;y=(im.height-H)//2;return im.crop((x,y,x+W,y+H))
def get(job):
    h,i,u=job;fn=f'{R}raw/{h}-{i}.jpg'
    if not os.path.exists(fn) or i>0:
        if not os.path.exists(fn): open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(u.split('?')[0]+'?width=1600',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
    return fn
jobs=[(h,i,img['src']) for h,p in d.items() for i,img in enumerate(p['images'][:4])]
with ThreadPoolExecutor(8) as ex: list(ex.map(get,jobs))
fr={}
for h,i,u in jobs:
    out=f'{O}{h}-{i+1}.jpg';cover(Image.open(f'{R}raw/{h}-{i}.jpg').convert('RGB')).save(out,quality=84,optimize=True);fr.setdefault(h,[]).append('/'+out)
for n in range(1,21):
    im=Image.open(f'{R}life/life-{n}.jpg').convert('RGB')
    if im.width/im.height>0.9: im.thumbnail((1600,1600))
    else: im=cover(im) if abs(im.width/im.height-0.8)<0.02 else im
    im.save(f'{O}life-{n}.jpg',quality=84,optimize=True)
json.dump(fr,open(R+'frames.json','w'),indent=1);print({k:len(v) for k,v in fr.items()})
