import json,re,urllib.request as U,io,base64,html,concurrent.futures as cf
from PIL import Image
O=[]
for p in json.load(open('stores/www.dimsumgolfclub.com.json')) if False else []: pass
d=json.load(open('stores/dimsum.json'))
for it in d['items']:
    vs=it['structuredContent']['variants']
    ok=any(v.get('unlimited') or (v.get('qtyInStock') or 0)>0 for v in vs)
    if not ok or 'Gift Card' in it['title'] or 'Little Dumplings' in it['title']: continue
    pr=float(vs[0]['priceMoney']['value'])
    O.append(dict(brand='Dim Sum Golf Club',title=it['title'],price=pr,cur='HKD',url='https://www.dimsumgolfclub.com'+it['fullUrl'],img=it.get('assetUrl'),imgs=[x.get('assetUrl') for x in it.get('items',[])][:4] or [it.get('assetUrl')],body=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',it.get('excerpt','') or it.get('body','') or ''))[:600]))
for dom,brand in [('rowenagolf.com','Rowena Golf Club'),('drvngolfco.com','DRVN Golf Co.')]:
    for p in json.load(open(f'stores/{dom}.json'))['products']:
        av=any(v['available'] for v in p['variants'])
        O.append(dict(brand=brand,title=p['title'],price=float(p['variants'][0]['price']),cur='USD',url=f'https://{dom}/products/{p["handle"]}',img=p['images'][0]['src'] if p['images'] else '',imgs=[i['src'] for i in p['images']][:5],avail=av,body=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',p.get('body_html') or ''))[:600]))
json.dump(O,open('opts.json','w'),indent=1)
def thumb(u):
    if not u: return ''
    src=u.split('?')[0]+('?format=500w' if 'squarespace' in u else '?width=600')
    try:
        im=Image.open(io.BytesIO(U.urlopen(U.Request(src,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB'); im.thumbnail((420,420))
        b=io.BytesIO(); im.save(b,'JPEG',quality=78); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    except Exception as e: print('ERR',u,e); return ''
with cf.ThreadPoolExecutor(10) as ex: T=list(ex.map(lambda o:thumb(o['img']),O))
def money(o):
    if o['cur']=='HKD': return f"HK${o['price']:.0f} (~${o['price']*0.128:.0f})"
    return f"${o['price']:g}"
secs=[]; n=0
for brand in ['Dim Sum Golf Club','Rowena Golf Club','DRVN Golf Co.']:
    cards=''
    for o,t in zip(O,T):
        if o['brand']!=brand: continue
        n+=1; o['n']=n
        so='' if o.get('avail',True) else ' · <b>sold out</b>'
        cards+=f'<div class="c"><div class="n">{n}</div><img src="{t}"><div class="t">{html.escape(o["title"])}</div><div class="p">{money(o)}{so}</div></div>'
    secs.append(f'<h2>{brand}</h2><div class="g">{cards}</div>')
json.dump(O,open('opts.json','w'),indent=1)
page=f'''<!doctype html><meta charset="utf-8"><title>Three brands — options</title><style>body{{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}}h1{{font-size:26px}}h2{{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}}.c{{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}}.c img{{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}}.n{{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}}.t{{font-size:13px;margin:6px 0 3px;line-height:1.25}}.p{{font:12px monospace;color:#555}}p.s{{max-width:800px;font-size:14px}}</style>
<h1>Three small brands, three styles — options</h1><p class="s">Live catalogues checked {__import__("datetime").date.today():%b %d, %Y}. Dim Sum shows in-stock pieces only (HKD with approx. USD). Rowena&rsquo;s whole range is six pieces. Pick by number.</p>{"".join(secs)}'''
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/radar-three-2-options.html','w').write(page); print(n)
