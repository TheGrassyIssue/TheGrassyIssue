"""Whim Golf BTK frames. 25 Oct 2026. Treatment shared with research/capsules/frame.py."""
import json, os, re, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R='research/whim/'; O='images/whim-golf/'; W,H=1000,1250; STONE=(232,226,214)
os.makedirs(O,exist_ok=True); os.makedirs(R+'raw',exist_ok=True)
src=open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
J={p['title']:p for p in json.load(open(R+'products.json'))['products']}
CARDS={
 'jacket':['Woven Merino Swing Jacket'],
 'navy':['Chartreuse Embroidered Navy Merino Long Sleeve Golf Shirt','White Embroidered Navy Merino Long Sleeve Golf Shirt'],
 'slate':['Sky Embroidered Slate Merino Long Sleeve Golf Shirt','Black Embroidered Slate Merino Long Sleeve Golf Shirt'],
 'black':['Red Embroidered Black Merino Long Sleeve Golf Shirt','Black Embroidered Black Merino Long Sleeve Golf Shirt'],
 'orange':['Orange Merino Long Sleeve Golf Shirt – Light-weight'],
 'short':['Golf Short - Blue Stretch Nylon'],
 'reebok':['WHIM Reebok Classic'],
 'sheephat':['Sheep Hat in Woven Merino'],
 'merinohat':['Eggplant Woven Merino Golf Hat','Dark Navy Woven Merino Golf Hat'],
 'oxford':['Oxford Cotton Hat'],
 'sock':['Featherweight Merino Golf Sock'],
 'sheep':['Merino Fleece Sheep Driver Headcover'],
 'tool':['Steel Ball Mark Repair Tool'],
 'bag':['Big Bag - Sky Blue Logo','Big Bag - Yellow Logo','Big Bag - White Logo'],
 'cupola':['La Cupola Paperweight'],
 'whimowa':['WHIMOWA Portable Putting Green'],
}
def fn(u): return R+'raw/'+re.sub(r'[^A-Za-z0-9_.-]','_',u.split('?')[0].rsplit('/',1)[-1])[-90:]
def get(u):
    f=fn(u)
    if not os.path.exists(f):
        open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(u.split('?')[0]+'?width=1600',headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
    return f
jobs=[]
for k,ts in CARDS.items():
    ims=[]
    if len(ts)==1: ims=[i['src'] for i in J[ts[0]]['images']][:6]
    else:
        per=[[i['src'] for i in J[t]['images']] for t in ts]
        ims=[p[0] for p in per]+per[0][1:4]
    for j,u in enumerate(ims,1): jobs.append((k,j,u))
def do(job):
    k,j,u=job
    try:
        im=Image.open(get(u)).convert('RGBA'); CUR[0]=k; out=frame(im); p=f'{O}{k}-{j}.jpg'; out.save(p,quality=84,optimize=True); return (k,j,'/'+p)
    except Exception as e: print('ERR',k,j,e)
with ThreadPoolExecutor(8) as ex: res=[r for r in ex.map(do,jobs) if r]
fr={}
for k,j,p in sorted(res,key=lambda r:(r[0],r[1])): fr.setdefault(k,[]).append(p)
json.dump(fr,open(R+'frames.json','w'),indent=1); print({k:len(v) for k,v in fr.items()})
