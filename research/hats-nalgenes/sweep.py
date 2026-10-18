import json,urllib.request,sys,concurrent.futures as cf,os
stores=sys.argv[1:]
def get(d):
    out=[]
    for page in range(1,6):
        u=f"https://{d}/products.json?limit=250&page={page}"
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20); j=json.load(r)
        except Exception as e: return d,out,str(e)[:60]
        ps=j.get('products',[])
        out+=ps
        if len(ps)<250: break
    json.dump(out,open(f"stores/{d}.json","w"))
    return d,out,None
with cf.ThreadPoolExecutor(12) as ex:
    for d,ps,err in ex.map(get,stores):
        n=[p for p in ps if any(k in (p['title'] or '').lower() for k in ['nalgene','water bottle','bottle'])]
        h=[p for p in ps if any(k in p['title'].lower() for k in ['cap','hat','snapback','trucker','5-panel','5 panel','beanie'])]
        print(f"{d}: {len(ps)} prods, nalgene {len(n)}, hats {len(h)} {err or ''}")
        for p in n: print('   N|',p['title'],'|',p['variants'][0]['price'],'|',any(v['available'] for v in p['variants']))
