import os,json,re,io,statistics
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps
R='research/towels/'; OUT='images/fall-towels-2026'; os.makedirs(OUT,exist_ok=True); os.makedirs(R+'raw',exist_ok=True)
P=json.load(open(R+'picks.json'))
SPECIAL={'T83':None,'T84':['https://images.squarespace-cdn.com/content/v1/5f7b7302cb6064569d654760/1713456564136-WY1DGHHWKF81ZVMU42RD/c1.jpg','https://images.squarespace-cdn.com/content/v1/5f7b7302cb6064569d654760/1713456562849-2DE6WZI5CRB3T7LEDXLK/c3.jpg']}
def up(u):
    u=('https:'+u) if u.startswith('//') else u
    if 'cdn.shopify' in u or '/cdn/shop/' in u:
        u=re.sub(r'[?&]width=\d+','',u); u=re.sub(r'_\d+x\d*(?=\.)','',u); return u+('&' if '?' in u else '?')+'width=1600'
    if 'sanity.io' in u: return u.split('?')[0]+'?w=1600&fit=max&auto=format&fm=jpg&q=88'
    if 'squarespace' in u: return u.split('?')[0]+'?format=1500w'
    return u
def edge_uniform(im):
    s=im.convert('RGB').resize((64,80)); px=s.load(); W,H=s.size
    e=[px[x,0] for x in range(W)]+[px[x,H-1] for x in range(W)]+[px[0,y] for y in range(H)]+[px[W-1,y] for y in range(H)]
    sd=sum(statistics.pstdev([c[i] for c in e]) for i in range(3))/3
    med=tuple(int(statistics.median([c[i] for c in e])) for i in range(3))
    return sd<10,med
def frame(im):
    im=ImageOps.exif_transpose(im).convert('RGB'); TW,TH=1000,1250
    uni,bg=edge_uniform(im)
    if uni:
        c=im.copy(); c.thumbnail((int(TW*.9),int(TH*.9)),Image.LANCZOS)
        cv=Image.new('RGB',(TW,TH),bg); cv.paste(c,((TW-c.width)//2,(TH-c.height)//2)); return cv,'pad'
    return ImageOps.fit(im,(TW,TH),Image.LANCZOS,centering=(.5,.5)),'crop'
with sync_playwright() as p:
  b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36')
  for x in P:
    srcs=SPECIAL.get(x['id']) or [u for u in (x.get('imgs') or []) if u]
    if x['id']=='T83': srcs=[u for u in x['imgs'] if 'sanity' in u][:3]
    seen=set(); local=[]; modes=[]
    for u in srcs:
        if len(local)>=5: break
        u2=up(u)
        key=re.sub(r'\?.*','',u2)
        if key in seen: continue
        seen.add(key)
        try:
            r=ctx.request.get(u2,headers={'referer':f"https://{x['domain']}/"},timeout=30000)
            im=Image.open(io.BytesIO(r.body()))
        except Exception as e:
            print('fail',x['id'],u2[:90],str(e)[:50]); continue
        if min(im.size)<400: continue
        f,m=frame(im); n=len(local)+1
        path=f"{OUT}/{x['brand']}-{n}.jpg"; f.save(path,quality=82,optimize=True,progressive=True)
        local.append('/'+path); modes.append(m)
    x['local']=local; x['modes']=modes
    print(x['id'],x['brand'],len(local),modes)
  b.close()
json.dump(P,open(R+'picks.json','w'),indent=1)
