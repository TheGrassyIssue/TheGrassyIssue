import json,re,io,base64,urllib.request,html,concurrent.futures as cf
from collections import OrderedDict
from PIL import Image
ps=json.load(open('all.json'))
def own(p): return 'Criquet Custom' not in p['tags']
new=[p for p in ps if p['published_at'][:10]>'2026-08-25' and p['product_type']!='iziGift']
willie=[p for p in new if re.search(r'willie|nelson',p['title']+p['handle'],re.I)]
newown=[p for p in new if own(p)]
def groups(lst,key):
    g=OrderedDict()
    for p in sorted(lst,key=lambda p:p['published_at'],reverse=True): g.setdefault(key(p),[]).append(p)
    return g
def wkey(p):
    t=re.sub(r'\s*-\s*The Icon.*$','',p['title']); t=re.sub(r' - (Navy|Heather.*|Peacoat|Burnt Orange|Blackstone|Midnight Ash)$','',t); return t
SEC=[("Willie Forever: the officially licensed Willie Nelson collection (Oct 15–16)",groups(willie,wkey))]
OUT=['Waxed Ranch Jacket','Corduroy Quilted Shacket','Quilted Shacket','Heavy Twill Shacket','Chill-Knit Fleece Shacket',"Member's Guest Jacket",'Vintage Polar Fleece','Rogue Knit Overshirt','Herringbone Field Hoodie','Chill-Knit Hoodie','Chill-Knit Vest','Quilted Hoodie']
g=groups(newown,lambda p:p['product_type'])
SEC.append(("Fall outerwear & layers",OrderedDict((k,g[k]) for k in OUT if k in g)))
HAT=[k for k in g if 'Hat' in k]; PANT=[k for k in g if 'Pant' in k]
rest=[k for k in g if k not in OUT and k not in HAT and k not in PANT]
SEC.append(("Shirts, knits & pearl snaps",OrderedDict((k,g[k]) for k in rest)))
SEC.append(("Pants & hats",OrderedDict((k,g[k]) for k in PANT+HAT)))
items=[]
for s,gg in SEC:
    for k,l in gg.items(): items.append((s,k,l))
def th(l):
    p=l[0]; u=p['images'][0]['src'].split('?')[0]+'?width=500' if p['images'] else ''
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB'); im.thumbnail((360,360))
        o=io.BytesIO(); im.save(o,'JPEG',quality=78); return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
    except: return ''
with cf.ThreadPoolExecutor(8) as ex: T=list(ex.map(lambda x:th(x[2]),items))
css="body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h1{font-size:26px}h2{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c img{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}.t{font-size:13px;margin:6px 0 3px;line-height:1.25}.p{font:11.5px monospace;color:#555}.v{font-size:11.5px;color:#444;margin-top:3px;line-height:1.3}p.s{max-width:860px;font-size:14px;line-height:1.5}"
out=[f"<!doctype html><meta charset='utf-8'><title>Criquet revisit — options</title><style>{css}</style><h1>Criquet, Revisited — options</h1><p class='s'>Live catalogue checked Oct 20, 2026. About 100 own-line products plus a 12-piece licensed Willie Nelson collection since our Aug 25 Brand to Know (custom/licensed team pieces left out). Colorways are grouped into one option. Pick by number.</p>"]
sec=None; num={}
for i,((s,k,l),img) in enumerate(zip(items,T),1):
    if s!=sec:
        if sec: out.append('</div>')
        sec=s; out.append(f"<h2>{html.escape(s)}</h2><div class='g'>")
    num[i]=[p['handle'] for p in l]
    prices=sorted(set(float(p['variants'][0]['price']) for p in l))
    pr='$%g'%prices[0]+('–$%g'%prices[-1] if len(prices)>1 else '')
    cols=[re.sub(r'^.*? - ','',p['title']) for p in l]
    so=[p for p in l if not any(v['available'] for v in p['variants'])]
    out.append(f"<div class='c'><div class='n'>{i}</div><a href='https://criquetshirts.com/products/{l[0]['handle']}' target='_blank'><img src='{img}'></a><div class='t'>{html.escape(k)}</div><div class='p'>{pr} · {len(l)} colorway{'s' if len(l)>1 else ''}</div><div class='v'>{html.escape(', '.join(cols[:8]))}{'…' if len(cols)>8 else ''}</div></div>")
out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/criquet-revisit-options.html','w').write(''.join(out))
json.dump(num,open('opts.json','w'),indent=1); print(len(items))
