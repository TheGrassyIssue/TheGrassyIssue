import re,json,subprocess,io,concurrent.futures as cf
from PIL import Image
def get(u,b=False):
  r=subprocess.run(['curl','-s','-L','--max-time','30','-A','Mozilla/5.0',u],capture_output=True);return r.stdout if b else r.stdout.decode('utf8','ignore')
R=json.load(open('fetch.json'))
MP=json.load(open('merrill-products.json'))['products']
def base(t): return t.split(' (')[0].strip().lower()
def run(r):
  k,n,u=r['page'],r['n'],r['url']
  if '/products/' not in u: return r
  if k=='merrill':
    h=u.rstrip('/').split('/')[-1]
    me=[p for p in MP if p['handle']==h]
    srcs=[i['src'] for i in me[0]['images']] if me else []
    if me:
      for p in MP:
        if p['handle']!=h and base(p['title'])==base(me[0]['title']) and p['images']: srcs.append(p['images'][0]['src'])
    r['avail']=any(v['available'] for v in me[0]['variants']) if me else None
  else:
    h=get(u)
    names=[]
    for x in re.findall(r'https://cdn\.shopify\.com/s/files/[^"\\ ?]+\.(?:jpg|jpeg|png|webp)',h):
      x=re.sub(r'_\d+x(\.progressive)?(?=\.)','',x)
      if x not in names: names.append(x)
    # keep this product's images: share the stem of the first V1 image
    stem=None
    for x in names:
      m=re.search(r'/([^/]+?)_V\d+\.',x)
      if m: stem=m.group(1);break
    srcs=[x for x in names if stem and f'/{stem}_' in x] if stem else names[:4]
    r['avail']='"availableForSale":true' in h
    r['stem']=stem
  r['imgs']=[]
  for i,s in enumerate(srcs[:5]):
    b=get(s.split('?')[0]+'?width=1600',True);fn=f'raw/{k}-{n}-{i}.jpg'
    try: Image.open(io.BytesIO(b)).convert('RGB').save(fn,quality=92);r['imgs'].append(fn)
    except Exception: pass
  return r
with cf.ThreadPoolExecutor(8) as ex: R=list(ex.map(run,R))
json.dump(R,open('fetch.json','w'),indent=1)
for r in R: print(r['page'],r['n'],len(r['imgs']),r.get('avail'),r.get('stem',''))
