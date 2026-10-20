import json,re,io,base64,urllib.request,html,concurrent.futures as cf
from PIL import Image
B=[("Parmore Golf · Bournemouth","parmoregolf.com"),("Three Putt Golf Clothing · West Yorkshire","threeputtgolfclothing.co.uk"),("SINK Golf · West Sussex","sinkgolf.co.uk"),("Son of Edmond · Keighley, Yorkshire","sonofedmond.co.uk"),("Reflo · Manchester","reflo.com"),("6th slot option A — Fyfe · Fife, Scotland","www.fyfegolf.com"),("6th slot option B — FINK Golfwear · Tyne & Wear","finkgolfwear.com")]
SKIP=re.compile(r'gift card|giftcard|e-gift|voucher|sample|customi[sz]|deposit|shipping|insurance|warranty|f1|racing|motorsport|team|williams|alpine|mclaren|aston|haas|sauber',re.I)
items=[]
for name,d in B:
    ps=json.load(open(d+'.json'))['products']
    ps=[p for p in ps if p['images'] and not SKIP.search(p['title']+' '+p['product_type']+' '+' '.join(p['tags'])) and any(v['available'] for v in p['variants'])]
    ps.sort(key=lambda p:p['published_at'],reverse=True)
    for p in ps[:16]: items.append((name,d,p))
def th(x):
    p=x[2]; u=p['images'][0]['src'].split('?')[0]+'?width=500'
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB'); im.thumbnail((340,340))
        o=io.BytesIO(); im.save(o,'JPEG',quality=76); return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
    except: return ''
with cf.ThreadPoolExecutor(8) as ex: T=list(ex.map(th,items))
css="body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h1{font-size:26px}h2{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c img{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}.t{font-size:13px;margin:6px 0 3px;line-height:1.25}.p{font:11.5px monospace;color:#555}p.s{max-width:860px;font-size:14px;line-height:1.5}"
out=[f"<!doctype html><meta charset='utf-8'><title>6 UK brands — options</title><style>{css}</style><h1>6 UK independent golf brands that would look great on US soil — options</h1><p class='s'>Live stores checked Oct 20, 2026; in-stock only, newest first. Prices in GBP with approx USD (×1.34). The sixth slot is Fyfe or FINK — pick from either. Pick by number (6–8 per brand works best).</p>"]
sec=None; num={}
for i,((name,d,p),img) in enumerate(zip(items,T),1):
    if name!=sec:
        if sec: out.append('</div>')
        sec=name; out.append(f"<h2>{html.escape(name)}</h2><div class='g'>")
    pr=sorted(float(v['price']) for v in p['variants']); a=sum(v['available'] for v in p['variants']); t=len(p['variants'])
    prs='£%g'%pr[0]+('–£%g'%pr[-1] if pr[-1]!=pr[0] else '')+' (~$%d)'%round(pr[0]*1.34)
    st='' if a==t else f' · {a}/{t} in stock'
    num[i]=[d,p['handle']]
    out.append(f"<div class='c'><div class='n'>{i}</div><a href='https://{d}/products/{p['handle']}' target='_blank'><img src='{img}'></a><div class='t'>{html.escape(p['title'])}</div><div class='p'>{prs}{st} · {p['published_at'][:10]}</div></div>")
out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/uk-six-options.html','w').write(''.join(out))
json.dump(num,open('opts.json','w'),indent=1); print(len(items))
