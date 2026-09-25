import os,re,io,json,hashlib
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='research/towels/irl/'
P=json.load(open('research/towels/picks.json'))
doms={x['brand']:x['domain'] for x in P}
doms['walker-golf-things']='walkergolfthings.com'; doms['sentinel-golf']='www.sentinelgolf.us'
import sys
log=json.load(open(OUT+'log.json')) if os.path.exists(OUT+'log.json') else []
seen=set(x['src'] for x in log)
WANT=sys.argv[1].split(',')
def imgs_from(html):
    urls=set(re.findall(r'(?:https?:)?//[^"\'\s,)\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s,)\\]*)?',html))
    out=[]
    for u in urls:
        u=('https:'+u) if u.startswith('//') else u
        if any(k in u.lower() for k in ['logo','icon','favicon','badge','payment','svg']): continue
        key=re.sub(r'\?.*','',re.sub(r'_\d+x\d*(?=\.)','',u))
        if key in seen: continue
        seen.add(key)
        if 'cdn.shopify' in u or '/cdn/shop/' in u: u=re.sub(r'[?&]width=\d+','',u); u=u+('&' if '?' in u else '?')+'width=2000'
        if 'sanity.io' in u: u=u.split('?')[0]+'?w=2000&fit=max&auto=format&fm=jpg&q=85'
        if 'squarespace' in u: u=u.split('?')[0]+'?format=2500w'
        out.append(u)
    return out
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36',locale='en-US')
  for brand,d in doms.items():
    if brand not in WANT: continue
    base=f'https://{d}'; pages=[base+'/']
    try:
      h=ctx.request.get(base+'/',timeout=20000).text()
    except Exception: continue
    links=set(re.findall(r'href="(/(?:[a-z-]+/)?(?:blogs|journal|stories|editorial|lookbook|pages/lookbook|pages/journal)[^"#?]*)"',h))
    arts=[l for l in links if l.count('/')>=3][:3] or list(links)[:3]
    pages+= [base+l for l in arts]
    got=0
    for pg in pages:
      try: html=h if pg==base+'/' else ctx.request.get(pg,timeout=20000).text()
      except Exception: continue
      for u in imgs_from(html)[:30]:
        try:
          im=Image.open(io.BytesIO(ctx.request.get(u,headers={'referer':base+'/'},timeout=20000).body()))
        except Exception: continue
        w,hh=im.size
        if min(w,hh)<900: continue
        sm=im.convert('RGB').resize((48,48)); cols=len(set(sm.getdata()))
        if cols<1200: continue
        fn=f"{brand}-{hashlib.md5(u.encode()).hexdigest()[:6]}.jpg"
        im.convert('RGB').save(OUT+fn,quality=85); got+=1
        log.append(dict(file=fn,brand=brand,src=u,page=pg,w=w,h=hh))
        if got>=8: break
      if got>=8: break
    print(brand,got,flush=True)
    json.dump(log,open(OUT+'log.json','w'),indent=1)
  b.close()
