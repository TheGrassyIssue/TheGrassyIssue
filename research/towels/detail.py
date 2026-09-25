import os,json,re,html
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
R='research/towels/'
P=json.load(open(R+'picks.json'))
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s or ''))).strip()
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36',locale='en-US')
  for x in P:
    d=x['domain']; h=x.get('handle')
    if d=='sentinelgolf.us' or not h: continue
    ctx.clear_cookies()
    base=f'https://{d}'
    try:
      r=ctx.request.get(f'{base}/products/{h}.js',headers={'referer':base+'/'},timeout=20000); j=r.json()
    except Exception as e:
      print('FAIL',x['id'],d,h,str(e)[:60]); continue
    x['desc']=clean(j.get('description'))
    x['imgs']=[('https:'+u if u.startswith('//') else u) for u in j['images']]
    x['price_native']=j['price']/100; x['avail']=j['available']
    x['variants']=[(v['title'],v['price']/100,v['available']) for v in j['variants']]
    try: x['currency']=ctx.request.get(f'{base}/cart.js',timeout=15000).json().get('currency')
    except: pass
    # try US pricing
    if x.get('currency')!='USD':
      ctx.add_cookies([{'name':'localization','value':'US','domain':d,'path':'/'},{'name':'cart_currency','value':'USD','domain':d,'path':'/'}])
      for u in [f'{base}/en-us/products/{h}.js',f'{base}/products/{h}.js?country=US&currency=USD']:
        try:
          jj=ctx.request.get(u,headers={'referer':base+'/'},timeout=15000).json(); cc=ctx.request.get(f'{base}/cart.js').json().get('currency')
          if cc=='USD': x['usd']=jj['price']/100; x['usd_src']=u; break
        except: pass
    else: x['usd']=x['price_native']
    print(x['id'],x['brand'],'|',x['title'][:34],'|',x.get('currency'),x['price_native'],'usd',x.get('usd'),'| avail',x['avail'],'| imgs',len(x['imgs']),'| desc',len(x['desc']))
  b.close()
json.dump(P,open(R+'picks.json','w'),indent=1)
