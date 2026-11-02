import json,urllib.request,time,sys,os,concurrent.futures as cf
D=sys.argv[1:]
def get(u):
  r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Macintosh)'});return urllib.request.urlopen(r,timeout=25).read()
def one(d):
  o=f'cat/{d}.json'
  if os.path.exists(o) and os.path.getsize(o)>100: return d,'cached'
  allp=[]
  for base in (f'https://{d}/products.json',f'https://{d}/collections/all/products.json'):
    try:
      for pg in (1,2,3):
        b=get(f'{base}?limit=250&page={pg}')
        if b.startswith(b'local_rate'): raise Exception('rl')
        ps=json.loads(b)['products']; allp+=ps
        if len(ps)<250: break
      break
    except Exception as e: allp=[]; err=str(e)[:40]
  if allp: json.dump(allp,open(o,'w')); return d,len(allp)
  return d,'FAIL '+err
with cf.ThreadPoolExecutor(8) as ex:
  for r in ex.map(one,D): print(*r)
