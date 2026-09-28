import os,re,io,json,sys,hashlib
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
from PIL import Image
T=json.loads(sys.argv[1])
log=json.load(open('img/log.json')) if os.path.exists('img/log.json') else []
seen={x['src'] for x in log}
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36',viewport={'width':1400,'height':900})
  pg=ctx.new_page()
  for key,urls in T.items():
    got=0
    for u in urls:
      try:
        pg.goto(u,wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(2500)
        for y in range(0,6000,1200): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(200)
        h=pg.content()
        dom=pg.evaluate("[...document.images].map(i=>i.currentSrc||i.src)")
      except Exception as e: print(key,u,'ERR',str(e)[:50]); continue
      cands=set(dom)|set(re.findall(r'(?:https?:)?//[^"\'\s,)\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s,)\\]*)?',h))
      for s in cands:
        if not s or s.startswith('data:'): continue
        s=('https:'+s) if s.startswith('//') else s; s=s.replace('&amp;','&')
        if any(k in s.lower() for k in ['logo','icon','favicon','sprite']): continue
        up=s
        if 'squarespace' in s: up=s.split('?')[0]+'?format=2500w'
        elif 'wixstatic' in s: up=re.sub(r'/v1/.*','',s)
        elif 'cdn.shopify' in s or '/cdn/shop/' in s: up=re.sub(r'[?&]width=\d+','',s)+('&' if '?' in s else '?')+'width=2000'
        k=re.sub(r'\?.*','',up)
        if k in seen: continue
        seen.add(k)
        try:
          r=ctx.request.get(up,timeout=15000,headers={'referer':u}); im=Image.open(io.BytesIO(r.body()))
        except Exception: continue
        w,hh=im.size
        if min(w,hh)<700: continue
        sm=im.convert('RGB').resize((32,32))
        if len(set(sm.getdata()))<500: continue
        fn=f"{key}-{hashlib.md5(k.encode()).hexdigest()[:6]}.jpg"; im.convert('RGB').save('img/'+fn,quality=82)
        log.append(dict(file=fn,key=key,src=up,page=u,w=w,h=hh)); got+=1
        if got>=10: break
      if got>=10: break
    print(key,got,flush=True); json.dump(log,open('img/log.json','w'),indent=1)
  b.close()
