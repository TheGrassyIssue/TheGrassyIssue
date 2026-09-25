import os,json,re,html
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
R='research/towels/'
P={x['id']:x for x in json.load(open(R+'picks.json'))}
T={'T83':[P['T83']['url']],'T56':[P['T56']['url']],'T84':[P['T84']['url']],
   'T57':[P['T57']['url']+'?country=US&currency=USD'],'T50':['https://walkergolfthings.com/en-us/products/kooka-icon-towel'],
   'T68':['https://mogshadegolf.com/en-us/products/contour-golf-towel',P['T68']['url']+'?country=US&currency=USD'],
   'T01':['https://3puttround.com/en-us/products/the-its-always-tee-time-tour-towel',P['T01']['url']+'?country=US&currency=USD'],
   'T09':[P['T09']['url']+'?country=US&currency=USD'],'T62':[P['T62']['url']],'T64':[P['T64']['url']]}
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36',locale='en-US',timezone_id='America/Chicago')
  pg=ctx.new_page()
  for k,us in T.items():
    for u in us:
      try:
        pg.goto(u,wait_until='domcontentloaded',timeout=45000); pg.wait_for_timeout(3500)
      except Exception as e: print(k,'ERR',str(e)[:60]); continue
      ld=pg.evaluate("[...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s=>s.textContent).join('\\n')")
      pr=re.findall(r'"price"\s*:\s*"?([\d.]+)',ld); cur=re.findall(r'"priceCurrency"\s*:\s*"(\w+)"',ld); av=re.findall(r'availability"\s*:\s*"([^"]+)',ld)
      md=pg.evaluate("(document.querySelector('meta[name=description]')||{}).content||''")
      body=pg.evaluate("(document.querySelector('.product__description,.product-single__description,.product-description,[class*=description]')||{}).innerText||''")[:1500]
      imgs=pg.evaluate("[...new Set([...document.images].filter(i=>i.naturalWidth>=500).map(i=>i.currentSrc||i.src))]")
      vis=re.findall(r'(?:\$|US\$|€|A\$|CA\$|£)\s?\d+(?:\.\d\d)?(?:\s?(?:USD|CAD|AUD|EUR))?',pg.inner_text('body'))[:6]
      print(k,u,'| ld',pr[:2],cur[:2],av[:1],'| visible',vis,'| imgs',len(imgs))
      P[k].setdefault('render',{})[u]=dict(price=pr[:3],cur=cur[:2],avail=av[:1],meta=md,body=body,imgs=imgs[:14],visible=vis)
  b.close()
json.dump(list(P.values()),open(R+'picks.json','w'),indent=1)
