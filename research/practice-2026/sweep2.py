import json,io,hashlib,time,sys,os,re,subprocess
from urllib.parse import urljoin
from PIL import Image
exec(open('research/practice-2026/sweep.py').read().split("keys=sys.argv")[0].split("S={",1)[0].replace('from playwright.sync_api import sync_playwright',''))
S=eval('{'+open('research/practice-2026/sweep.py').read().split("S={",1)[1].split("\n}\n")[0]+'\n}')
keys=sys.argv[1].split(',')
logf='research/practice-2026/img/log.json'
log=json.load(open(logf)) if os.path.exists(logf) else {}
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def get(u,t=10):
    r=subprocess.run(['curl','-sL','-m',str(t),'-A',UA,u],capture_output=True); return r.stdout
t0=time.time()
for k in keys:
    log[k]=[];seen=set()
    for u in S[k]:
        h=get(u).decode('utf-8','ignore')
        cands=re.findall(r'(?:src|data-src|data-lazy-src|href|content)=["\']([^"\']+\.(?:jpe?g|png|webp)(?:\?[^"\']*)?)',h,re.I)
        cands+=[c.split(' ')[0] for s in re.findall(r'srcset=["\']([^"\']+)',h) for c in s.split(',') ]
        cands+=re.findall(r'url\(["\']?([^"\')]+\.(?:jpe?g|png|webp))',h,re.I)
        for c in cands:
            c=urljoin(u,c.strip())
            base=re.sub(r'-\d+x\d+(?=\.\w+$)','',c.split('?')[0])
            if base in seen: continue
            seen.add(base)
            if time.time()-t0>115: break
            b=get(c,8)
            try: im=Image.open(io.BytesIO(b)).convert('RGB')
            except Exception: continue
            if im.width<700 or im.height<400: continue
            f=f'research/practice-2026/img/{k}-{hashlib.md5(base.encode()).hexdigest()[:8]}.jpg'; im.save(f,quality=85)
            log[k].append({'file':f,'src':c,'page':u,'w':im.width,'h':im.height})
    print(k,len(log[k]),int(time.time()-t0)); json.dump(log,open(logf,'w'),indent=1)
