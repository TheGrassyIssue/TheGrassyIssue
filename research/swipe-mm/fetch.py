import re,json,subprocess,io,concurrent.futures as cf
from PIL import Image
P={'merrill':'../../drops/brand-to-know-merrill-golf.html','metalwood':'../../drops/brand-to-know-metalwood-studio.html'}
def get(u,b=False):
  r=subprocess.run(['curl','-s','-L','--max-time','25','-A','Mozilla/5.0',u],capture_output=True);return r.stdout if b else r.stdout.decode('utf8','ignore')
jobs=[]
for k,f in P.items():
  s=open(f).read()
  for n,c in enumerate(re.findall(r'<div class="product-card".*?class="product-link"',s,re.S),1):
    u=re.findall(r'href="(https?://[^"]+)"[^>]*class="product-link"',c)
    jobs.append((k,n,u[0] if u else ''))
def run(j):
  k,n,u=j;res={'page':k,'n':n,'url':u,'imgs':[],'avail':None,'price':None}
  if '/products/' not in u: return res
  try: p=json.loads(get(u.split('?')[0]+'.json'))['product']
  except Exception: res['err']='nojson';return res
  res['avail']=any(v.get('available',True) for v in p['variants']) if 'available' in p['variants'][0] else None
  res['price']=p['variants'][0]['price']
  for i,im in enumerate(p['images'][:6]):
    r=get(im['src'].split('?')[0]+'?width=1600',True)
    fn=f'raw/{k}-{n}-{i}.jpg'
    try: Image.open(io.BytesIO(r)).convert('RGB').save(fn,quality=92);res['imgs'].append(fn)
    except Exception: pass
  return res
with cf.ThreadPoolExecutor(8) as ex: R=list(ex.map(run,jobs))
json.dump(R,open('fetch.json','w'),indent=1)
for r in R: print(r['page'],r['n'],len(r['imgs']),r.get('err',''),r['price'],r['url'][-50:])
