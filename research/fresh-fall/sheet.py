import json, re, base64, subprocess, os, html
from concurrent.futures import ThreadPoolExecutor
CUT='2026-09-29'
B={'students':('Students Golf','https://studentsgolf.com/products/','Fall Drop 2 landed Sept 30 &ndash; Oct 1, with hats and beanies through Oct 12.'),
   'walker':('Walker Golf Things','https://www.walkergolfthings.com/en-us/products/','The &ldquo;Kooka&rdquo; drop: shirts and accessories from Oct 8, polos, knits and a windbreaker Oct 13 (today). US prices.'),
   'sugarloaf':('Sugarloaf Social Club','https://www.sugarloafsocialclub.com/products/','Oct 6 and Oct 12: a rugby, a work jacket, grid fleece and Smathers &amp; Branson-made chevron needlepoint.')}
rows={}
for k in B:
    d=json.load(open(f'{k}.json'))['products']; out=[]
    for p in d:
        if p['published_at'][:10] < CUT: continue
        if re.search(r'women|gift box',p['title'],re.I): continue
        av=[v['title'] for v in p['variants'] if v['available']]
        img=(p['images'][0]['src'] if p['images'] else '')
        old = k=='students' and img and int(re.search(r'v=(\d+)',img).group(1))<1789000000
        out.append(dict(h=p['handle'],t=p['title'],pr=p['variants'][0]['price'],av=av,img=img,n=len(p['images']),d=p['published_at'][:10],old=old,typ=p.get('product_type','')))
    out.sort(key=lambda x:(x['d']),reverse=True); rows[k]=out
json.dump(rows,open('candidates.json','w'),indent=1)
def thumb(u):
    if not u: return ''
    fn='raw/t_'+re.sub(r'\W','_',u.split('/')[-1].split('?')[0])[:80]+'.jpg'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0','-o',fn,u.split('?')[0]+'?width=420'])
    try:
        from PIL import Image; im=Image.open(fn).convert('RGB'); im.thumbnail((420,525)); im.save(fn,quality=72)
        return 'data:image/jpeg;base64,'+base64.b64encode(open(fn,'rb').read()).decode()
    except Exception: return ''
allimgs=[r['img'] for v in rows.values() for r in v]
with ThreadPoolExecutor(12) as ex: T=dict(zip(allimgs,ex.map(thumb,allimgs)))
css="body{font:14px/1.45 Georgia,serif;background:#f3efe6;color:#1d2a1c;margin:0;padding:28px 36px}h1{font-size:26px;margin:0 0 6px}h2{font-size:21px;margin:30px 0 2px}.sub{font:12px/1.5 monospace;opacity:.8;max-width:960px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:10px}.c{background:#fff;border:1px solid #ddd6c6;padding:7px}.c.so{opacity:.45}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#eee}.n{font:bold 12px monospace;color:#2d4a2b}.t{font-size:12.5px;margin:3px 0}.p{font:10.5px monospace;opacity:.75}.tag{background:#2d4a2b;color:#fff;font:bold 9px monospace;padding:1px 4px}"
h=[f"<!doctype html><meta charset='utf-8'><title>Fresh fall drops &mdash; options</title><style>{css}</style><h1>Three Fresh Fall Drops &mdash; options</h1><div class='sub'>Students Golf (Fall Drop 2), Walker Golf Things (the Kooka drop) and Sugarloaf Social Club, all released in the last two weeks, none in our Sept 24 fall-drops post or the Sept 27 Sugarloaf Autumn Layers post. Pick around 5&ndash;7 per brand, or tell me to choose. Faded cards are sold out. Prices read live from each store today, October 13, 2026.</div>"]
i=0
for k,(name,base,note) in B.items():
    h.append(f"<h2>{name}</h2><div class='sub'>{note} {len(rows[k])} pieces.</div><div class='g'>")
    for r in rows[k]:
        i+=1; so='' if r['av'] else ' so'
        sizes=', '.join(a.split(' / ')[-1] for a in r['av'])[:60] if r['av'] else 'sold out'
        tag=" <span class='tag'>RE-LISTED</span>" if r['old'] else ''
        h.append(f"<div class='c{so}'><img src='{T.get(r['img'],'')}'><div class='n'>{i}{tag}</div><div class='t'>{html.escape(r['t'])}</div><div class='p'>${float(r['pr']):.0f} &middot; {r['d'][5:]} &middot; {html.escape(sizes)}</div></div>")
    h.append("</div>")
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/fresh-fall-drops-options.html','w').write(''.join(h))
print({k:len(v) for k,v in rows.items()}, i)
