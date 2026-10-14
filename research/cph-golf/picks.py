import json,re,os,subprocess
from concurrent.futures import ThreadPoolExecutor
A={p['handle']:p for p in json.load(open('p1.json'))['products']+json.load(open('p2.json'))['products']}
R=['chg26-aw-j01','chg26-aw-p01','chg26-aw-p02','chg26-aw-t01','chg26-apcg-t04','chg26-apcg-t05','chg26-apcg-a01','chg26-bp-t01','chg26-bp-c01','chg26-ss-t16','chg26-ss-t17','chg26-ss-s02','chg26-ss-c07','chg26-ss-sx05','mu6slpg0m','chg25-aw-j05-khaki','classic-cotton-rib-polo-shirt-yellow','chg25-aw-t21-khaki']
PACK=re.compile(r'^(CHG\d\d|CH\d\d)-|^CaptureOne',re.I)
out=[];jobs=[]
for h in R:
    p=A[h]; srcs=[i['src'].split('?')[0] for i in p['images']]
    av=[v['title'] for v in p['variants'] if v['available']]
    cols=sorted({a.split(' / ')[0] for a in av})
    life=[u for u in srcs if (not PACK.search(u.split('/')[-1])) or '-LOOK-' in u]
    pack=[u for u in srcs if PACK.search(u.split('/')[-1]) and '-LOOK-' not in u]
    tok=lambda c:c.replace(' ','_')
    pk=[u for u in pack if any('-'+tok(c)+'-' in u.split('/')[-1].upper() for c in cols)] or pack
    sel=life[:2]+pk[:3]
    key=re.sub(r'[^a-z0-9]','',h)[:22]
    out.append(dict(key=key,h=h,t=p['title'],jpy=int(float(p['variants'][0]['price'])),av=av,cols=cols,imgs=sel,body=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',p['body_html']))[:700]))
    for n,u in enumerate(sel,1): jobs.append((f'raw/{key}-{n}.img',u))
json.dump(out,open('picks.json','w'),indent=1,ensure_ascii=False)
def dl(j):
    fn,u=j
    if not os.path.exists(fn) or os.path.getsize(fn)<5000: subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0','-o',fn,u+'?width=1600'])
with ThreadPoolExecutor(16) as ex: list(ex.map(dl,jobs))
for o in out: print(o['key'],o['jpy'],o['cols'],[u.split('/')[-1][:24] for u in o['imgs']])
