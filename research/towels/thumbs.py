import os,json,re,io
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
from PIL import Image
R='research/towels/'
c=json.load(open(R+'cands.json')); cur=json.load(open(R+'currency.json')); usd=json.load(open(R+'usd.json'))
drop={('vessel','VESSEL x MagnetOwl Mini Towel Magnet'),('vice-golf','Vice Golf Terry Towel Shorts'),('sinking-birdies','Magnetic Landing Pad'),('vessel','Magnetic Golf Towel | 5” x 5”')}
c=[x for x in c if (x['brand'],x['title']) not in drop]
s=json.load(open(R+'sentinel.json')); c.append(dict(brand='sentinel-golf',domain='sentinelgolf.us',title=s['title'],handle=s['handle'],price=s['price'],avail=True,img=s['img'],imgs=[s['img']],url=s['url'],note='Squarespace; price read 21 Sep, re-check at build'))
os.makedirs(R+'thumbs2',exist_ok=True)
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36')
  # usag
  j=ctx.request.get('https://usuckatgolf.com/products.json?limit=250',headers={'referer':'https://usuckatgolf.com/'}).json()
  for pr in j['products']:
    if pr['title']=='Tour Championship Towel':
      c.append(dict(brand='usag',domain='usuckatgolf.com',title=pr['title'],handle=pr['handle'],price=min(float(v['price']) for v in pr['variants']),avail=any(v['available'] for v in pr['variants']),img=pr['images'][0]['src'],imgs=[i['src'] for i in pr['images'][:6]]))
  # vessel 10x10
  for x in json.load(open(R+'sweep2.json'))['items']:
    if x['brand']=='vessel' and '10”' in x['title']: c.append(x)
  # manors images
  pg=b.new_page()
  for x in c:
    if x['brand']=='manors' and not x.get('img'):
      pg.goto(f"https://manorsgolf.com/products/{x['handle']}",wait_until='domcontentloaded',timeout=40000); pg.wait_for_timeout(2500)
      im=pg.evaluate("[...document.images].filter(i=>i.naturalWidth>=600).map(i=>i.currentSrc)")
      x['img']=im[0] if im else None; x['imgs']=im[:6]
  for i,x in enumerate(c):
    x['id']=f"T{i+1:02d}"
    d=x['domain']; x['currency']=cur.get(d) or 'USD'
    k=f"{d}|{x.get('handle')}"
    if usd.get(k) and usd[k][2]=='USD': x['usd']=usd[k][1]
    x.setdefault('url',f"https://{d}/products/{x['handle']}")
    u=x.get('img')
    if not u: continue
    u=('https:'+u) if u.startswith('//') else u
    if 'cdn.shopify' in u or '/cdn/shop/' in u: u=re.sub(r'([?&])width=\d+','',u)+('&' if '?' in u else '?')+'width=600'
    try:
      r=ctx.request.get(u,headers={'referer':f'https://{d}/'},timeout=20000)
      im=Image.open(io.BytesIO(r.body())).convert('RGB'); im.thumbnail((400,400)); im.save(R+f"thumbs2/{x['id']}.jpg",quality=80); x['thumb']=f"thumbs2/{x['id']}.jpg"
    except Exception as e: print('thumb fail',x['id'],x['brand'],str(e)[:60])
  b.close()
json.dump(c,open(R+'grid2.json','w'),indent=1); print(len(c),'options',len({x['brand'] for x in c}),'brands')
