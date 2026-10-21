import json,re,io,base64,urllib.request,html,concurrent.futures as cf
from PIL import Image
ps=[p for p in json.load(open('products.json'))['products'] if p['images'] and any(v['available'] for v in p['variants'])]
def grp(p):
    ty=p['product_type']
    if ty=='Polos': return '1 · Polos'
    if ty=='Tees': return '2 · Tees'
    if ty in ('Pants','Shorts'): return '3 · Pants & shorts'
    if 'cap' in p['title'].lower(): return '4 · Caps'
    return '5 · Socks, towel & tees'
ps.sort(key=lambda p:(grp(p),p['published_at'][::-1]))
ps.sort(key=lambda p:(grp(p),-int(p['published_at'][:10].replace('-',''))))
def th(p):
    u=p['images'][0]['src'].split('?')[0]+'?width=500'
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB'); im.thumbnail((340,340))
        o=io.BytesIO(); im.save(o,'JPEG',quality=76); return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
    except: return ''
with cf.ThreadPoolExecutor(8) as ex: T=list(ex.map(th,ps))
css="body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h1{font-size:26px}h2{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c img{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}.t{font-size:13px;margin:6px 0 3px;line-height:1.25}.p{font:11px monospace;color:#555;line-height:1.4}p.s{max-width:860px;font-size:14px;line-height:1.5}"
out=[f"<!doctype html><meta charset='utf-8'><title>Saha Golf — options</title><style>{css}</style><h1>Brand to Know: Saha Golf — options</h1><p class='s'>saha.golf, checked Oct 21, 2026. Launched summer 2026; ships from the US and Türkiye. Everything currently in stock ({len(ps)} products), grouped by type, newest first. Colorways listed are the ones in stock; they'd go in one card. Pick by number.</p>"]
sec=None; num={}
for i,(p,img) in enumerate(zip(ps,T),1):
    g=grp(p)
    if g!=sec:
        if sec: out.append('</div>')
        sec=g; out.append(f"<h2>{html.escape(g[4:])}</h2><div class='g'>")
    pr=sorted(float(v['price']) for v in p['variants']); av=[v['title'] for v in p['variants'] if v['available']]
    prs='$%g'%pr[0]+('–$%g'%pr[-1] if pr[-1]!=pr[0] else '')
    cw='' if av==['Default Title'] else ' · '+', '.join(dict.fromkeys(a.split(' / ')[0] for a in av)).title()
    num[i]=p['handle']
    out.append(f"<div class='c'><div class='n'>{i}</div><a href='https://saha.golf/products/{p['handle']}' target='_blank'><img src='{img}'></a><div class='t'>{html.escape(p['title'].title())}</div><div class='p'>{prs}{html.escape(cw)} · {p['published_at'][:10]}</div></div>")
out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/saha-options.html','w').write(''.join(out))
json.dump(num,open('opts.json','w'),indent=1); print(len(ps))
