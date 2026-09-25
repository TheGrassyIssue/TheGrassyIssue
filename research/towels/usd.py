import os,json
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
c=json.load(open('research/towels/cands.json')); cur=json.load(open('research/towels/currency.json'))
out={}
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36',locale='en-US')
  for x in c:
    d=x['domain']
    if cur.get(d) in ('USD',None) or not x['handle']: continue
    ctx.add_cookies([{'name':'localization','value':'US','domain':d,'path':'/'},{'name':'cart_currency','value':'USD','domain':d,'path':'/'}])
    res=None
    for u in [f'https://{d}/products/{x["handle"]}.js?country=US&currency=USD', f'https://{d}/en-us/products/{x["handle"]}.js']:
      try:
        r=ctx.request.get(u,headers={'referer':f'https://{d}/'},timeout=12000)
        if r.ok:
          j=r.json(); cj=ctx.request.get(f'https://{d}/cart.js',timeout=12000).json()
          res=(u,j['price']/100,cj.get('currency')); 
          if cj.get('currency')=='USD': break
      except Exception as e: pass
    out[f"{d}|{x['handle']}"]=res; print(x['brand'],x['title'][:30],cur[d],x['price'],'->',res and res[1:])
  b.close()
json.dump(out,open('research/towels/usd.json','w'),indent=1)
