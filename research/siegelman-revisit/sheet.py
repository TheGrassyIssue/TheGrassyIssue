import json,re,os,io,base64,html,urllib.request,time
from PIL import Image
A=json.load(open('products.json'))
def col(x):
  for o in x['options']:
    if re.search('colou?r',o['name'],re.I): return o['values']
  return []
G=[("New for Fall/Winter '26 (Sept–Oct)",['Track Jacket','Track Pant','Retro Crewneck','Retro Sweatpant','Henley Sweatshirt','Rib Zip Up Cardigan','Cable Knit Sweater','Cable Knit Pants','Logo Knit','Knit Pant','Embroidered Hoodie','Racing Stable Crewneck','Racing Stable Hoodie','Racing Stable Long Sleeve Raglan Tee','Racing Stable Mesh Jersey','Denim Pant','Wide Leg Parachute Pant']),
("Golf: Maxfli + Harness pieces still in stock",['Siegelman Stable x Maxfli Golf Polo','Siegelman Stable x Maxfli Pull Over Jacket','Siegelman Stable x Maxfli Printed Boxy Tee','Siegelman Stable x Maxfli Hat','Siegelman Stable x Maxfli Dad Hat','Siegelman Stable x Maxfli Golf Tote','Short Sleeve Harness Shirt','Long Sleeve Harness Button Up','Coaches Harness Short','Racing Stable Track Shorts']),
("Outerwear + fall layers from the archive",['Mock Neck Sherpa Jacket','Barn Jacket','Race Coat','Racing Stable Coaches Jacket','Knit Cardigan','Collar Tip Button Up','Pleated Pant','Coaches Pant']),
("Hats",['Siegelman Stable Contrast Denim Hat','Siegelman Stable Contrast Denim Dad Hat','Siegelman Beanie','Siegelman Stable Canvas Dad Hat','Siegelman Stable Suede Dad Hat','Siegelman Stable Corduroy Hat','Siegelman Stable Wool Dad Hat','Siegelman Stable Heritage Crest Dad Hat','Siegelman Stable Hat','Siegelman Stable 2026 Champions Hat']),
("Collabs since August: Prince, Yankees, Mets",['Siegelman Stable x Prince Tennis Hat','Siegelman Stable x Prince Tennis Dad Hat','Prince Tennis Boxy Tee','New York Yankees Coaches Jacket','Siegelman Stable x New York Yankees x New Era 59FIFTY A-Frame Fitted Cap','New York Yankees Zip Hoodie','Siegelman Stable x New York Mets x New Era 9FORTY A-Frame Snapback']),
("Accessories",['Oval Belt','Horseshoe Belt','Siegelman Stable Wool Scarf'])]
os.makedirs('opt',exist_ok=True)
def get(u,p):
  if os.path.exists(p): return p
  u=u.split('?')[0]+'?width=500'
  for t in range(3):
    try: urllib.request.urlretrieve(u,p);return p
    except Exception as e: time.sleep(3)
def th(p):
  im=Image.open(p).convert('RGB');im.thumbnail((360,450));b=io.BytesIO();im.save(b,'JPEG',quality=76);return base64.b64encode(b.getvalue()).decode()
out=['<meta charset="utf-8"><style>body{background:#efe9dc;font-family:Georgia,serif;color:#1f2a1d;padding:28px;margin:0}h1{margin:0 0 4px}p.s{font-style:italic;margin:0 0 20px}h3{font:600 12px system-ui;letter-spacing:.14em;text-transform:uppercase;color:#2D4A2B;margin:22px 0 8px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}.c{background:#f8f4ea;border-radius:6px;overflow:hidden;font:12px/1.35 system-ui}.im{display:flex}.im img{width:50%;aspect-ratio:4/5;object-fit:cover;background:#f3eee2}.c div.t{padding:6px 8px}.n{font-weight:700;color:#2D4A2B}.x{color:#8a5a2b}</style>',
'<h1>Siegelman Stable Revisited — options</h1><p class="s">Everything below is in stock on siegelmanstable.com as of Oct 31, 2026 (USD). Colorways are combined into one tile. Women\'s pieces are left out. Number your keeps.</p>']
n=0;cat=[]
for g,ts in G:
  out.append(f'<h3>{g}</h3><div class="g">')
  for t in ts:
    xs=[p for p in A if p['title']==t and any(v['available'] for v in p['variants'])]
    if not xs: print('MISSING',t);continue
    n+=1;x=xs[0];cols=[c for p in xs for c in col(p)];cols=list(dict.fromkeys(cols))
    ims=[]
    for k in (0,1):
      if len(x['images'])>k:
        p=get(x['images'][k]['src'],f'opt/{n:02d}-{k}.jpg')
        if p: ims.append(f'<img src="data:image/jpeg;base64,{th(p)}">')
    pr=sorted({int(float(v['price'])) for p in xs for v in p['variants'] if v['available']})
    prs=f'${pr[0]}' if len(pr)==1 else f'${pr[0]}–${pr[-1]}'
    cs=', '.join(cols[:6])+(f' +{len(cols)-6} more' if len(cols)>6 else '')
    nm=t.replace('Siegelman Stable x ','SS × ').replace('Siegelman Stable ','')
    out.append(f'<div class="c"><div class="im">{"".join(ims)}</div><div class="t"><span class="n">{n}</span> · {html.escape(nm)} · {prs}<br><span class="x">{html.escape(cs)}</span></div></div>')
    cat.append({'n':n,'title':t,'handles':[p['handle'] for p in xs],'colors':cols,'price':prs,'group':g})
  out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/siegelman-revisit-options.html','w').write('\n'.join(out));json.dump(cat,open('cands.json','w'),indent=1);print(n)
