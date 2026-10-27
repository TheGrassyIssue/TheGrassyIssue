import json,re,os,urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
jobs=[]
for s in ['aberdeen-west','we-hit-fairways','grind-city-golf']:
    d=json.load(open(s+'.json')); seen=set()
    for p in d['products']:
        base=re.sub(r'(-copy)?(-\d+)?$','',p['handle'])
        if s=='grind-city-golf' and base in seen: continue
        seen.add(base)
        imgs=p.get('images') or p.get('image_urls')
        for i,u in enumerate(imgs[:4]): jobs.append((s,p['handle'],i,u))
def get(j):
    s,h,i,u=j; f=f'thumbs/{s[:2]}_{re.sub(r"[^a-z0-9-]","",h)[:50]}_{i}.jpg'
    if os.path.exists(f): return
    try:
        b=urllib.request.urlopen(urllib.request.Request(u+'?width=500',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
        open(f+'.tmp','wb').write(b); im=Image.open(f+'.tmp').convert('RGB'); im.thumbnail((400,400)); im.save(f,quality=80); os.remove(f+'.tmp')
    except Exception as e: print('ERR',h,i,e)
with ThreadPoolExecutor(8) as ex: list(ex.map(get,jobs))
print(len(jobs), len(os.listdir('thumbs')))
