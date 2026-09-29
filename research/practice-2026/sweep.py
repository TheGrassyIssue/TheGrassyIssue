import json,io,hashlib,time,sys,os
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from PIL import Image
from playwright.sync_api import sync_playwright
S={
 'drr':['https://drivingrangerr.com/','https://drivingrangerr.com/facility/'],
 'clay':['https://www.austintexas.gov/golfatx/jimmy-clay-course','https://www.austintexas.gov/department/roy-kizer-course','https://www.austintexas.gov/department/joe-balander-short-course'],
 'penick':['https://www.harveypenickgc.com/','https://www.harveypenickgc.com/course/'],
 'plum':['https://www.plumcreekgolf.com/golf/toptracer-range','https://www.plumcreekgolf.com/golf/course','https://www.plumcreekgolf.com/'],
 'tera':['https://teravistagolf.com/practice-facility/','https://teravistagolf.com/'],
 'forest':['https://forestcreek.com/practice-facilities/','https://forestcreek.com/'],
 'butler':['https://butlerpitchandputt.com/','https://butlerpitchandputt.com/learn','https://butlerpitchandputt.com/about'],
 'dscc':['https://drippingspringscountryclub.com/','https://drippingspringscountryclub.com/toptracer/'],
 'grey':['https://www.greyrockgolfandtennis.com/golf/elite-motion-golf','https://www.greyrockgolfandtennis.com/golf','https://www.greyrockgolfandtennis.com/'],
 'topgolf':['https://topgolf.com/us/austin/'],
}
keys=sys.argv[1].split(',')
logf='research/practice-2026/img/log.json'
log=json.load(open(logf)) if os.path.exists(logf) else {}
t0=time.time()
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1400,'height':900})
    for k in keys:
        log[k]=[];seen=set();tk=time.time()
        for u in S[k]:
            if time.time()-t0>120 or time.time()-tk>60: break
            try:
                pg.goto(u,wait_until='domcontentloaded',timeout=15000);pg.wait_for_timeout(2000)
                for _ in range(4): pg.mouse.wheel(0,2500);pg.wait_for_timeout(400)
                srcs=pg.evaluate("""[...document.querySelectorAll('img')].map(i=>i.currentSrc||i.src).concat([...document.querySelectorAll('*')].map(e=>{const b=getComputedStyle(e).backgroundImage;const m=b&&b.match(/url\\(["']?([^"')]+)/);return m?m[1]:null}).filter(Boolean))""")
            except Exception as e: print('ERR',u,str(e)[:60]); continue
            for s in srcs[:40]:
                if time.time()-tk>60: break
                if s.startswith('data:') or s in seen: continue
                seen.add(s)
                try:
                    r=pg.request.get(s,timeout=8000); im=Image.open(io.BytesIO(r.body())).convert('RGB')
                except Exception: continue
                if im.width<700 or im.height<400: continue
                f=f'research/practice-2026/img/{k}-{hashlib.md5(s.encode()).hexdigest()[:8]}.jpg'; im.save(f,quality=85)
                log[k].append({'file':f,'src':s,'page':u,'w':im.width,'h':im.height})
        print(k,len(log[k]),int(time.time()-t0))
        json.dump(log,open(logf,'w'),indent=1)
    b.close()
