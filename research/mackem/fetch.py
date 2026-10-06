import json,subprocess,io,re,concurrent.futures as cf
from PIL import Image
def get(u,b=False):
  r=subprocess.run(['curl','-s','-L','--max-time','30','-A','Mozilla/5.0',u],capture_output=True);return r.stdout if b else r.stdout.decode('utf8','ignore')
P=json.loads(get('https://mackemgolf.com/products.json?limit=250'))['products']
P=[p for p in P if any(v['available'] for v in p['variants']) and 'gift-card' not in p['handle']]
opts=[]
for n,p in enumerate(P,1):
  desc=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p['body_html'] or '')).strip()
  opts.append(dict(code=f'M{n:02d}',handle=p['handle'],title=p['title'],type=p['product_type'],aud=p['variants'][0]['price'],
    variants=[(v['title'],v['price'],v['available']) for v in p['variants']],tags=p['tags'],desc=desc,imgs=[i['src'].split('?')[0] for i in p['images']]))
def dl(o):
  for i,u in enumerate(o['imgs'][:8]):
    b=get(u+'?width=1600',True)
    try: Image.open(io.BytesIO(b)).convert('RGB').save(f"raw/{o['code']}-{i}.jpg",quality=90)
    except: pass
with cf.ThreadPoolExecutor(10) as ex: list(ex.map(dl,opts))
json.dump(opts,open('options.json','w'),indent=1,ensure_ascii=False)
for o in opts: print(o['code'],o['title'],o['aud'],len(o['imgs']),[v[0] for v in o['variants'] if v[2]][:5])
