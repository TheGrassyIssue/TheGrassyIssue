import json,subprocess,io,re,concurrent.futures as cf
from PIL import Image
def get(u,b=False):
  r=subprocess.run(['curl','-s','-L','--max-time','30','-A','Mozilla/5.0',u],capture_output=True);return r.stdout if b else r.stdout.decode('utf8','ignore')
P=json.loads(get('https://slice-town.com/products.json?limit=250'))['products']
skip={'two-stripe-bundle','slate-golf-track-suit-bundle','cobalt-golf-track-suit-bundle','depeche-golf-issue-5'}
P=[p for p in P if p['handle'] not in skip]
opts=[]
for n,p in enumerate(P,1):
  code=f'S{n:02d}'
  usd=None
  try: usd=json.loads(get(f"https://slice-town.com/products/{p['handle']}.js?currency=USD"))['price']/100
  except: pass
  sizes=[v['title'] for v in p['variants'] if v['available']]
  desc=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p['body_html'] or '')).strip()
  opts.append(dict(code=code,handle=p['handle'],title=p['title'],type=p['product_type'],sek=p['variants'][0]['price'],usd_store=usd,sizes=sizes,desc=desc,imgs=[i['src'].split('?')[0] for i in p['images']]))
def dl(o):
  for i,u in enumerate(o['imgs']):
    b=get(u+'?width=1600',True)
    try: Image.open(io.BytesIO(b)).convert('RGB').save(f"raw/{o['code']}-{i}.jpg",quality=90)
    except: pass
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(dl,opts))
json.dump(opts,open('options.json','w'),indent=1,ensure_ascii=False)
for o in opts: print(o['code'],o['title'],o['sek'],o['usd_store'],len(o['imgs']),o['sizes'][:6])
