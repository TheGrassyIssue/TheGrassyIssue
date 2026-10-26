"""East vs West frames. 25 Oct 2026. Treatment shared with research/capsules/frame.py."""
import json, os, re, io, urllib.request
import numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R='research/east-west/'; O='images/east-vs-west/'; W,H=1000,1250; STONE=(232,226,214)
os.makedirs(O,exist_ok=True); os.makedirs(R+'raw',exist_ok=True)
src=open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
cat=json.load(open(R+'catalogue.json'))
J=json.load(open('/tmp/ew-jonessportsco.com.json'))['products']
for p in J:
    cat.append(dict(brand='Jones Sports Co',title=p['title'],price=min(float(v['price']) for v in p['variants']),url='https://jonessportsco.com/products/'+p['handle'],img=[i['src'] for i in p['images']][:6],avail=any(v['available'] for v in p['variants'])))
PICKS={
 'wg1':('Whim Golf','Woven Merino Swing Jacket'),'wg2':('Whim Golf','Chartreuse Embroidered Navy Merino Long Sleeve Golf Shirt'),
 'wg3':('Whim Golf','Sky Embroidered Slate Merino Long Sleeve Golf Shirt'),'wg4':('Whim Golf','Golf Short - Blue Stretch Nylon'),
 'wg5':('Whim Golf','WHIM Reebok Classic'),'wg6':('Whim Golf','Sheep Hat in Woven Merino'),
 'mw1':('Metalwood Studio','Western Yolk Track Jacket'),'mw2':('Metalwood Studio','Pleated Western Track Pant'),'mw3':('Metalwood Studio','Piped Longsleeve Quarter Zip Polo'),
 'mw4':('Metalwood Studio','Contrast Stitch Mock Neck Sweatshirt'),'mw5':('Metalwood Studio','Raglan Sleeve Blouson'),'mw6':('Metalwood Studio','King of the Greens Jersey'),
 'rl1':('Rookline','Signature Blend Polo'),'rl2':('Rookline','Grid Fleece Windbreaker'),'rl3':('Rookline','Ottoman Rib Cashmere Crew'),
 'rl4':('Rookline','Hudson Quarter Zip'),'rl5':('Rookline','Brushed Twill Pivot Pant'),'rl6':("Rookline","Yeoman's Performance Short"),
 'sl1':('SLOAT','MERINO POLO'),'sl2':('SLOAT','ORGANIC VENTILE WIND SHIRT'),'sl3':('SLOAT','ORGANIC COTTON FLEECE CREWNECK'),
 'sl4':('SLOAT','ORGANIC COTTON FLEECE QUARTER ZIP'),'sl5':('SLOAT','ORGANIC COTTON CADDIE PANT'),'sl6':('SLOAT','ORGANIC COTTON CORDUROY SHORT'),
 'gt1':('Gumtree','State Flower - Headcover 2.0'),'gt2':('Gumtree','Archive Quilt - Blade Putter Cover'),'gt3':('Gumtree','GUMTREE (COFFEE) Sack Headcover'),
 'gt4':('Gumtree','Vintage Floral Patchwork Quilt - Valuables Pouch'),'gt5':('Gumtree','GGNC x Samuel Falzone - Italian Leather Card Holder'),'gt6':('Gumtree','Member Caddy Towel'),
 'jn1':('Jones Sports Co','Trouper - Evergreen/Kodiak'),'jn2':('Jones Sports Co','Original Jones Bag - Navy/Red/White'),'jn3':('Jones Sports Co',"Circa '71 Headcover - Brown"),
 'jn4':('Jones Sports Co','Clubhouse Duffle - Ecru/Kodiak'),'jn5':('Jones Sports Co','Mt. Hood Ball Marker'),'jn6':('Jones Sports Co','Tour Towel - Green'),
}
def fn(u): return R+'raw/'+re.sub(r'[^A-Za-z0-9_.-]','_',u.split('?')[0].rsplit('/',1)[-1])[-90:]
def get(u):
    f=fn(u)
    if not os.path.exists(f):
        uu=u.split('?')[0]+('?format=1500w' if 'squarespace' in u else '?width=1600')
        open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(uu,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
    return f
meta={}; jobs=[]
for k,(b,t) in PICKS.items():
    m=[o for o in cat if o['brand']==b and o['title']==t and o.get('avail')]
    assert m,(k,b,t); o=m[0]; us=[u for u in o['img'] if u][:4]
    meta[k]=dict(brand=b,title=t,price=o['price'],url=o['url']); jobs+=[(k,j,u) for j,u in enumerate(us,1)]
def do(job):
    k,j,u=job
    try:
        im=Image.open(get(u)).convert('RGBA')
        if im.width<300: return None
        CUR[0]=k; out=frame(im); p=f'{O}{k}-{j}.jpg'; out.save(p,quality=84,optimize=True); return (k,j,'/'+p)
    except Exception as e: print('ERR',k,j,e); return None
with ThreadPoolExecutor(8) as ex: res=[r for r in ex.map(do,jobs) if r]
fr={}
for k,j,p in sorted(res): fr.setdefault(k,[]).append(p)
json.dump(fr,open(R+'frames.json','w'),indent=1); json.dump(meta,open(R+'meta.json','w'),indent=1)
print({k:len(v) for k,v in fr.items()})
