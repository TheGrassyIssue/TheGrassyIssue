import json,re,urllib.request,os,concurrent.futures as cf
O=json.load(open('options.json'))
P={p['handle']:p for p in json.load(open('products.json'))['products']}
out=[];jobs=[];os.makedirs('raw',exist_ok=True)
for o in O:
    hs=o['handles'];p=P[hs[0]];key=re.sub(r'[^a-z0-9]','',o['title'].lower())[:22]
    out.append(dict(n=o['n'],group=o['group'],title=o['title'],key=key,handles=hs,price=o['price'],colors=o['colors'],blurb=o['blurb']))
    for i,im in enumerate(p['images'][:6],1): jobs.append((im['src'],f'raw/{key}-{i}.img'))
    for j,h in enumerate(hs[1:],1):
        for i,im in enumerate(P[h]['images'][:2],1): jobs.append((im['src'],f'raw/{key}-c{j}{i}.img'))
json.dump(out,open('picks.json','w'),indent=1)
def dl(j):
    u,f=j
    if os.path.exists(f): return
    try: open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(u+('&' if '?' in u else '?')+'width=2000',headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
    except Exception as e: print('ERR',u,e)
with cf.ThreadPoolExecutor(10) as ex: list(ex.map(dl,jobs))
print(len(out),len(jobs))
