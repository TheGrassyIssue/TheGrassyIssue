import json,re,base64,subprocess,os,html
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
P=[p for p in json.load(open('products.json'))['products'] if 'gift' not in p['handle']]
def cat(p):
    t=(p['title']+' '+p['product_type']).lower()
    if re.search(r'cap|hat',t): return 'Headwear'
    if re.search(r'headcover|putter|driver|wood|hybrid|tee bag|marker|tees',t): return 'Headcovers & accessories'
    return 'Apparel'
G={'Apparel':[],'Headwear':[],'Headcovers & accessories':[]}
for p in sorted(P,key=lambda p:p['published_at'],reverse=True): G[cat(p)].append(p)
def thumb(u):
    fn='raw/t_'+re.sub(r'\W','_',u.split('/')[-1].split('?')[0])[:70]+'.jpg'
    if not os.path.exists(fn): subprocess.run(['curl','-sL','-m','40','-A','Mozilla/5.0','-o',fn,u.split('?')[0]+'?width=420'])
    try: im=Image.open(fn).convert('RGB'); im.thumbnail((420,525)); im.save(fn,quality=72); return 'data:image/jpeg;base64,'+base64.b64encode(open(fn,'rb').read()).decode()
    except Exception: return ''
imgs=[p['images'][0]['src'] for g in G.values() for p in g if p['images']]
with ThreadPoolExecutor(12) as ex: T=dict(zip(imgs,ex.map(thumb,imgs)))
css="body{font:14px/1.45 Georgia,serif;background:#f3efe6;color:#1d2a1c;margin:0;padding:28px 36px}h1{font-size:26px;margin:0 0 6px}h2{font-size:20px;margin:28px 0 4px}.sub{font:12px/1.5 monospace;opacity:.8;max-width:980px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:8px}.c{background:#fff;border:1px solid #ddd6c6;padding:7px}.c.so{opacity:.42}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#eee}.n{font:bold 12px monospace;color:#2d4a2b}.t{font-size:12.5px;margin:3px 0}.p{font:10.5px monospace;opacity:.75}.new{background:#2d4a2b;color:#fff;font:bold 9px monospace;padding:1px 4px}"
h=[f"<!doctype html><meta charset='utf-8'><title>Mount Tee Golf &mdash; options</title><style>{css}</style><h1>Brand to Know: Mount Tee Golf &mdash; options</h1><div class='sub'>Melbourne, &ldquo;created by 3 friends&rdquo; (Jeremy, Joel and Tom per a third-party newsletter; the brand&rsquo;s own site gives no names). Ethos, verbatim: &ldquo;not everybody has to look the same.&rdquo; Current campaign: &ldquo;This Could Get Ugly.&rdquo; Whole catalogue below, {sum(len(g) for g in G.values())} products, prices in AUD with ~USD (x0.70). Faded = sold out. NEW = this season (June 2026). Pick, or say &ldquo;all in stock.&rdquo;</div>"]
i=0
for g,ps in G.items():
    h.append(f"<h2>{g}</h2><div class='g'>")
    for p in ps:
        i+=1; av=[v['title'] for v in p['variants'] if v['available']]; pr=float(p['variants'][0]['price'])
        so='' if av else ' so'; new=" <span class='new'>NEW</span>" if p['published_at'][:7]>='2026-06' else ''
        sz=', '.join(a for a in av if a!='Default Title')[:50] or ('in stock' if av else 'sold out')
        img=T.get(p['images'][0]['src'],'') if p['images'] else ''
        h.append(f"<div class='c{so}'><img src='{img}'><div class='n'>{i}{new}</div><div class='t'>{html.escape(p['title'])}</div><div class='p'>A${pr:.0f} (~${pr*0.70:.0f}) &middot; {html.escape(sz)}</div></div>")
    h.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/mount-tee-btk-options.html','w').write(''.join(h))
print(i,{k:len(v) for k,v in G.items()}, sum(1 for g in G.values() for p in g if any(v['available'] for v in p['variants'])))
