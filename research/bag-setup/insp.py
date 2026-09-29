import json,re,io,os,hashlib,time
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from PIL import Image
from playwright.sync_api import sync_playwright
C=json.load(open('research/bag-setup/catalog.json'))['stores']
K=json.load(open('research/bag-setup/kits.json'))
allp=[x for d,v in C.items() if not d.startswith('_') for x in v]
def items(dom,rx): return [x for x in allp if x['dom']==dom and re.search(rx,x['title'],re.I)]
# extra same-palette products per kit (by dom, regex)
EXTRA={
 'Clubhouse Green':[('hirokigolf.com','Forest Green|Kinloch|Military Green|Towel - Green'),('jonessportsco.com','Dark Green|Evergreen'),('sundaygolf.com','Midnight Green'),('dormieworkshop.com','Green Room|Towel - Green'),('apresgolf.com','Green Trim|Moss'),('dimpledivot.com','Green|Highland|Hunter')],
 'Tweed & Tan':[('seamusgolf.com','.'),('bluetross.com','Castagna|Old Tom|Langford'),('winstoncollection.com','Pull-Up|Torino|Wax Canvas'),('dimpledivot.com','Highland|Murphy')],
 'Navy, With a Pop':[('hirokigolf.com','Navy'),('jonessportsco.com','Rover Stand Bag - Navy$|Original Jones Bag - Navy/White$'),('apresgolf.com','Pink|Yellow Jasmine|Navy Trim'),('dormieworkshop.com','Paisley.*Navy|Towel - Blue'),('dimpledivot.com','Blue')],
 'Stone & Bone':[('jonessportsco.com','Bone|Kodiak|Alpine'),('hirokigolf.com','Stone Grey|Towel - White|Shibuya'),('apresgolf.com','Cream|Sand'),('dormieworkshop.com','White French|White Quilted'),('malbon.com','IRONWORKS|ANTILLES')],
 'Black & White':[('malbon.com','MEMBERS|CHECKERED'),('jonessportsco.com','Black/White|Missouri'),('hirokigolf.com','Anvers|Black'),('ghostgolf.com','CHECKERED|OREO'),('dormieworkshop.com','Black & White|Night Train'),('dimpledivot.com','Black')],
 'One Loud Note':[('hirokigolf.com','Stone Grey|Orange|Grey'),('birdsofcondor.com','Lawn Pawn'),('dimpledivot.com','Gravel|Ember')],
}
def lifestyle(im):
    g=im.convert('RGB').resize((64,64)); px=[g.getpixel((x,y)) for x in range(64) for y in (0,63)]+[g.getpixel((x,y)) for y in range(64) for x in (0,63)]
    lum=[sum(p)/3 for p in px]; spread=max(lum)-min(lum)
    import statistics; sd=statistics.pstdev(lum)
    return sd>14
out=json.load(open('research/bag-setup/insp/log.json')) if os.path.exists('research/bag-setup/insp/log.json') else {}
t0=time.time()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context()
    for k in K:
        name=k['name']; urls=[]
        if out.get(name): continue
        if time.time()-t0>120: break
        for it in k['items']:
            x=[y for y in allp if y['dom']==it['dom'] and y['handle'].startswith(it['handle'])]
            if x: urls+= [(u,x[0]['dom'],x[0]['title']) for u in x[0]['imgs']]
        for dom,rx in EXTRA.get(name,[]):
            for x in items(dom,rx)[:10]: urls+=[(u,x['dom'],x['title']) for u in x['imgs']]
        seen=set(); keep=[]
        for u,dom,title in urls:
            key=u.split('?')[0]
            if key in seen: continue
            seen.add(key)
            if time.time()-t0>155 or len(keep)>=30: break
            try:
                im=Image.open(io.BytesIO(ctx.request.get(key+'?width=900',timeout=20000).body())).convert('RGB')
            except Exception: continue
            if not lifestyle(im): continue
            f=f"research/bag-setup/insp/{hashlib.md5(key.encode()).hexdigest()[:10]}.jpg"; im.save(f,quality=85)
            keep.append({'file':f,'src':key,'dom':dom,'title':title,'w':im.width,'h':im.height})
        out[name]=keep; print(name,len(urls),len(keep),int(time.time()-t0)); json.dump(out,open('research/bag-setup/insp/log.json','w'),indent=1)
    b.close()
json.dump(out,open('research/bag-setup/insp/log.json','w'),indent=1)
