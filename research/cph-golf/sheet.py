import json,re,base64,subprocess,os,html
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
A={p['handle']:p for p in json.load(open('p1.json'))['products']+json.load(open('p2.json'))['products']}
G=[('AW26 (live Oct 7)',['chg26-aw-j01','chg26-aw-p01','chg26-aw-p02','chg26-aw-t01','chg26-aw-t02']),
   ('A.P.C. Golf collab (Sept 2) &mdash; what&rsquo;s left',['chg26-apcg-t04','chg26-apcg-t05','chg26-apcg-p01','chg26-apcg-a01']),
   ('BAGGY PANTS GOLF collab (late July)',['chg26-bp-t01','chg26-bp-t02','chg26-bp-t03','chg26-bp-c01']),
   ('SS26 core',['chg26-ss-t16','chg26-ss-t17','chg26-ss-s01','chg26-ss-s02','chg26-ss-c06','chg26-ss-p03','chg26-ss-j02','chg26-ss-t13','chg26-ss-c07','chg26-ss-c04','chg26-ss-sx05','chg26-ss-sx04','chg26-ss-set1']),
   ('Other 2026 collabs',['mu6slpg0m','chg26-cl-t02','chg26-pb-t01']),
   ('AW25 still in stock',['chg25-aw-t21-khaki','chg25-aw-j05-black','chg25-aw-j05-khaki','chg25-aw-j06-beige','fire-easy-chino-pants-green','classic-cotton-rib-polo-shirt-navy','classic-cotton-rib-polo-shirt-yellow','classic-cotton-rib-polo-shirt-green','thunder-stripes-jet-cap-gray-1'])]
def thumb(u):
    fn='raw/t_'+re.sub(r'\W','_',u.split('/')[-1].split('?')[0])[:70]+'.jpg'
    if not os.path.exists(fn): subprocess.run(['curl','-sL','-m','40','-A','Mozilla/5.0','-o',fn,u.split('?')[0]+'?width=420'])
    try:
        im=Image.open(fn).convert('RGB'); im.thumbnail((420,525)); im.save(fn,quality=72); return 'data:image/jpeg;base64,'+base64.b64encode(open(fn,'rb').read()).decode()
    except Exception: return ''
def lead(p):
    # prefer a model/lifestyle frame (non-light border) among first 12
    return p['images'][0]['src'] if p['images'] else ''
items=[(g,h) for g,hs in G for h in hs]
with ThreadPoolExecutor(12) as ex: T=dict(zip([h for _,h in items],ex.map(lambda h:thumb(lead(A[h])),[h for _,h in items])))
css="body{font:14px/1.45 Georgia,serif;background:#f3efe6;color:#1d2a1c;margin:0;padding:28px 36px}h1{font-size:26px;margin:0 0 6px}h2{font-size:20px;margin:28px 0 4px}.sub{font:12px/1.5 monospace;opacity:.8;max-width:980px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-top:8px}.c{background:#fff;border:1px solid #ddd6c6;padding:7px}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#eee}.n{font:bold 12px monospace;color:#2d4a2b}.t{font-size:12.5px;margin:3px 0}.p{font:10.5px monospace;opacity:.75}.rec{background:#2d4a2b;color:#fff;font:bold 9px monospace;padding:1px 4px}"
REC={'chg26-aw-j01','chg26-aw-p01','chg26-aw-p02','chg26-aw-t01','chg26-aw-t02','chg26-apcg-t04','chg26-apcg-t05','chg26-apcg-a01','chg26-bp-t01','chg26-bp-c01','chg26-ss-t16','chg26-ss-s02','chg26-ss-c07','chg26-ss-sx05','mu6slpg0m','chg25-aw-j05-khaki','classic-cotton-rib-polo-shirt-yellow','chg25-aw-t21-khaki'}
h=[f"<!doctype html><meta charset='utf-8'><title>Cph/Golf revisited &mdash; options</title><style>{css}</style><h1>Brand Revisited: Cph/Golf (CAPTAINS HELM) &mdash; options</h1><div class='sub'>We first ran them in the Japan roundup (July 30) and covered the A.P.C. Golf collab (Sept). Since then: AW26 landed Oct 7, the A.P.C. pieces mostly sold out, plus BAGGY PANTS GOLF and Penguin by Munsingwear collabs. Men&rsquo;s pieces in stock today only. Prices in yen with the store&rsquo;s own USD figure. Pick ~18, or take the 18 marked TGI PICK. Women&rsquo;s (MADEMOISELLE) versions left out.</div>"]
i=0
for g,hs in G:
    h.append(f"<h2>{g}</h2><div class='g'>")
    for hd in hs:
        p=A[hd]; i+=1; jp=int(float(p['variants'][0]['price'])); usd=round(jp*0.0064376892)
        av=[v['title'] for v in p['variants'] if v['available']]
        sizes=', '.join(av)[:70]
        tag=" <span class='rec'>TGI PICK</span>" if hd in REC else ''
        h.append(f"<div class='c'><img src='{T[hd]}'><div class='n'>{i}{tag}</div><div class='t'>{html.escape(p['title'])}</div><div class='p'>&yen;{jp:,} (~${usd}) &middot; {html.escape(sizes)}</div></div>")
    h.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/cph-golf-revisited-options.html','w').write(''.join(h))
print(i,len(REC))
