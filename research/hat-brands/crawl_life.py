import re,subprocess,io,json,sys,os,concurrent.futures as cf
from PIL import Image
from urllib.parse import urljoin,urlparse
Image.MAX_IMAGE_PIXELS=None
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u,t=20,b=False):
  r=subprocess.run(['curl','-s','-L','--max-time',str(t),'-A',UA,u],capture_output=True); return r.stdout if b else r.stdout.decode('utf8','ignore')
def run(key,start):
  host=urlparse(start).netloc; h=get(start); pages=[start]
  for l in re.findall(r'href="([^"#]+)"',h):
    l=urljoin(start,l.replace('&amp;','&'))
    if urlparse(l).netloc==host and re.search(r'/pages/|/blogs/|journal|about|story|lookbook',l,re.I) and l not in pages and not re.search(r'\.(jpg|png|pdf)',l): pages.append(l)
  pages=pages[:5]; urls=[]
  for p in pages:
    hh=h if p==start else get(p)
    for x in re.findall(r'(?:https?:)?//[^"\'\s,)]+?\.(?:jpe?g|png|webp)',hh,re.I): urls.append(x if x.startswith('http') else 'https:'+x)
  seen=[]
  for x in urls:
    x=re.sub(r'_(\d+x\d*|\d*x\d+)(?=\.(jpe?g|png|webp))','',x.split('?')[0])
    if x in seen or re.search(r'logo|icon|favicon|sprite|badge|payment|flag',x,re.I): continue
    seen.append(x)
  got=[]
  for i,x in enumerate(seen[:45]):
    u=x+('?width=2400' if 'shopify' in x or '/cdn/shop/' in x else '')
    r=get(u,25,True)
    try:
      im=Image.open(io.BytesIO(r)); w,hh=im.size
      if w>=1200 and hh>=700:
        ext=x.rsplit('.',1)[-1][:4]; p=f'life/{key}-{len(got)}.{ext}'; open(p,'wb').write(r); got.append((p,u,w,hh))
    except Exception: pass
  return key,got
sites=dict(l.split() for l in open(sys.argv[1]) if l.strip())
res={}
with cf.ThreadPoolExecutor(8) as ex:
  for k,g in ex.map(lambda kv: run(*kv), sites.items()): res[k]=g; print(k,len(g),flush=True)
old=json.load(open('life.json')) if os.path.exists('life.json') else {}
old.update(res); json.dump(old,open('life.json','w'),indent=1)
