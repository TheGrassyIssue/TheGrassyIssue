import os,json
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
c=json.load(open('research/towels/cands.json'))
# add USAG
c.append(dict(brand='usag',domain='usuckatgolf.com',title='Tour Championship Towel',handle=None,price=25.0,avail=True,img=None,imgs=[]))
doms=sorted({x['domain'] for x in c})
cur={}
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',locale='en-US')
  for d in doms:
    try:
      j=ctx.request.get(f'https://{d}/cart.js',headers={'referer':f'https://{d}/'},timeout=12000).json(); cur[d]=j.get('currency')
    except Exception as e: cur[d]=None
  b.close()
print({d:v for d,v in cur.items() if v!='USD'})
json.dump(cur,open('research/towels/currency.json','w'))
