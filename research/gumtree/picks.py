import json,re,os,urllib.request,concurrent.futures as cf
I={it['urlId']:it for it in json.load(open('items.json'))}
O={x['n']:x for x in json.load(open('options.json'))}
nums=[1,2,6,8,10,11,12,14,16,17,18,21,23,24,29,30,31,32,34,35,36,37,38,39,46,47,50,55]
SEC={1:'covers1',2:'covers1',6:'covers1',8:'covers1',10:'covers1',11:'covers2',12:'covers2',14:'covers2',16:'covers2',
17:'tees',18:'tees',21:'tees',23:'tees',24:'tees',29:'clothing',30:'clothing',31:'clothing',32:'clothing',34:'clothing',35:'clothing',36:'clothing',37:'clothing',
38:'hats',39:'hats',46:'collabs',47:'collabs',50:'collabs',55:'collabs'}
ARCH=['made-in-manhattan-headcover','state-flora-fauna-headcover-20','heirloomquiltcover-acmwd-phsea','fishing-wader-headcover','gumtree-coffee-studio-espresso-3hywd-wp5bx-lp9ea-n3fyy','nyc-subway-token-ball-marker-set','vintage-new-york-state-outdoor-license-ball-markers','nature-club-fish-species-handmade-pitch-repair-tool']
def st(it): return sum(1 for x in it['variants'] if x.get('unlimited') or (x.get('qtyInStock') or 0)>0)
def money(it):
    v=it['variants']; p=float(v[0]['priceMoney']['value']); s=None
    for x in v:
        if x.get('onSale'): s=float(x['salePriceMoney']['value']); break
    return p,s
out=[];jobs=[]
os.makedirs('raw',exist_ok=True)
def add(u,sec):
    it=I[u]; key=re.sub(r'[^a-z0-9]','',u)[:22]; p,s=money(it)
    body=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',it.get('body') or '')).replace('&amp;','&').replace('&nbsp;',' ')
    out.append(dict(sec=sec,urlId=u,key=key,title=it['title'],price=p,sale=s,instock=st(it),nvar=len(it['variants']),url='https://www.gumtreegolfandnature.com'+it['fullUrl'],body=body[:1600],
                    variants=[(v.get('attributes'),v.get('qtyInStock')) for v in it['variants']]))
    imgs=[x['assetUrl'] for x in it.get('items',[])][:6] or [it['assetUrl']]
    for i,a in enumerate(imgs,1): jobs.append((a+'?format=1500w',f'raw/{key}-{i}.img'))
for n in nums: add(O[n]['urlId'],SEC[n])
for u in ARCH: add(u,'archive')
json.dump(out,open('picks.json','w'),indent=1)
def dl(j):
    u,f=j
    if os.path.exists(f): return
    try: open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
    except Exception as e: print('fail',f)
with cf.ThreadPoolExecutor(10) as ex: list(ex.map(dl,jobs))
for d in out:
    flag='' if (d['instock']>0)==(d['sec']!='archive') else '  <-- STOCK MISMATCH'
    print(d['sec'],'|',d['title'][:50],'|',d['price'],d['sale'],'|',d['instock'],'/',d['nvar'],flag)
print(len(out),len(jobs))
