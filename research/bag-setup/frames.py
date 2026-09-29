import json,io,os,statistics
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from PIL import Image,ImageOps
from playwright.sync_api import sync_playwright
C=json.load(open('research/bag-setup/catalog.json'))['stores']
K=json.load(open('research/bag-setup/kits.json'))
allp=[x for d,v in C.items() if not d.startswith('_') for x in v]
def prod(d,h):
    e=[x for x in allp if x['dom']==d and x['handle']==h]
    return e[0] if e else [x for x in allp if x['dom']==d and x['handle'].startswith(h)][0]
OUT='images/bag-setup/'
def edge(im):
    g=im.convert('RGB').resize((80,100)); px=[g.getpixel((x,y)) for x in range(80) for y in (0,99)]+[g.getpixel((x,y)) for y in range(100) for x in (0,79)]
    lum=[sum(p)/3 for p in px]; return statistics.pstdev(lum)<6, tuple(sorted(px,key=sum)[len(px)//2])
def frame(im):
    im=im.convert('RGB'); uni,bg=edge(im)
    if uni:
        t=im.copy(); t.thumbnail((900,1125),Image.LANCZOS)
        if t.width<700 and t.height<880:
            s=min(900/im.width,1125/im.height); t=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
        cv=Image.new('RGB',(1000,1250),bg); cv.paste(t,((1000-t.width)//2,(1250-t.height)//2)); return cv
    return ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.5))
fr=json.load(open('research/bag-setup/frames.json')) if os.path.exists('research/bag-setup/frames.json') else {}
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context()
    for k in K:
        for it in k['items']:
            if not it['star']: continue
            x=prod(it['dom'],it['handle']); key=x['handle']
            if key in fr: continue
            fr[key]=[]
            for j,u in enumerate(x['imgs'][:4],1):
                try:
                    r=ctx.request.get(u.split('?')[0]+'?width=1600',timeout=30000); im=Image.open(io.BytesIO(r.body()))
                    if im.mode in('RGBA','LA','P'):
                        im=im.convert('RGBA'); bgc=Image.new('RGB',im.size,(255,255,255)); bgc.paste(im,mask=im.split()[3]); im=bgc
                except Exception as e: continue
                f=f'{OUT}{key[:60]}-{j}.jpg'; frame(im).save(f,quality=84,optimize=True,progressive=True)
                fr[key].append({'local':'/'+f,'src':u.split('?')[0]})
            print(key,len(fr[key]))
            json.dump(fr,open('research/bag-setup/frames.json','w'),indent=1)
    b.close()
