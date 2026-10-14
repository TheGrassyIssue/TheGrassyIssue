import json,re,os,subprocess
from concurrent.futures import ThreadPoolExecutor
def load(k): return {p['handle']:p for p in json.load(open(f'{k}.json'))['products']}
S,W,G=load('students'),load('walker'),load('sugarloaf')
PICKS={
 'students':[('obispo-nylon-jacket',None),('perris-nylon-coat',None),('oso-nylon-jacket-1',None),('locke-cardigan-sweater-1',None),('visalia-knit-ls-polo-sweater',None),('carlsbad-knit-l-s-polo-sweater-1',None),('palmdale-stripe-knit-crew-sweater',None),('irvine-waffle-knit-crew-sweater-1',None),('viejo-flannel-ls-shirt',None),('newport-s-s-polo-shirt-1',None),('oroville-s-s-polo-shirt',None),('san-diego-track-pants-2',None)],
 'walker':[('outback-knit-polo',None),('kooka-two-tone-polo-1',None),('kooka-two-tone-polo',None),('kooka-loom-knit-polo',None),('kooka-windbreaker',None),('featherlite-kooka-polo-7',None),('vacation-terry-polo',None),('whitsundays-ss-shirt',None),('pitch-cargo-short-1',None),('scorecard-t-shirt',None),('rodeo-cap',None),('cursive-nylon-cap',None)],
 'sugarloaf':[('ssc-work-jacket','SLTS'),('ssc-work-jacket','BRWNS'),('ssc-rugby-shirt','NVYS'),('ssc-rugby-shirt','GRYS'),('grid-t-zip-fleece','NANT'),('grid-t-zip-fleece','NVY'),('grid-t-zip-fleece','OAT'),('grid-fleece-hoody','OAT'),('grid-fleece-hoody','NANT'),('big-s-chevron-card-wallet',None),('nantucket-red-needlepoint-can-cooler',None),('nantucket-red-needlepoint-bottle-opener',None)]}
COL={'SLTS':'Slate','BRWNS':'Brown','NVYS':'Navy','GRYS':'Grey','NANT':'Nantucket Red','NVY':'Heather Blue','OAT':'Oatmeal'}
D={'students':S,'walker':W,'sugarloaf':G}
out={}; jobs=[]
for b,lst in PICKS.items():
    out[b]=[]
    for h,cw in lst:
        p=D[b][h]; imgs=[i['src'].split('?')[0] for i in p['images']]
        if cw:  # colorway group: from its packshot _1 up to next colorway's _1
            st=[i for i,u in enumerate(imgs) if f'-{cw}_1' in u or f'{cw}_1copy' in u][0]
            starts=sorted(i for i,u in enumerate(imgs) if re.search(r'_1copy',u))
            en=min([s for s in starts if s>st]+[len(imgs)])
            grp=imgs[st:en]; life=[u for u in grp if 'SugarloafF26' in u]; pack=[u for u in grp if 'SugarloafF26' not in u]
            sel=(life[:2]+pack[:3])
            av=[v['option2'] for v in p['variants'] if v['option1'].startswith(COL[cw].split()[0]) and v['available']]
        else:
            sel=imgs[:5]; av=[v['title'] for v in p['variants'] if v['available']]
        key=re.sub(r'[^a-z0-9]','',(h+(cw or '')).lower())[:24]
        out[b].append(dict(key=key,h=h,cw=COL.get(cw),t=p['title'],pr=p['variants'][0]['price'],av=av,imgs=sel,d=p['published_at'][:10]))
        for n,u in enumerate(sel,1): jobs.append((f'raw/{key}-{n}.jpg',u))
json.dump(out,open('picks.json','w'),indent=1)
def dl(j):
    fn,u=j
    if not os.path.exists(fn) or os.path.getsize(fn)<5000:
        subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0','-o',fn,u+'?width=1600'])
with ThreadPoolExecutor(16) as ex: list(ex.map(dl,jobs))
print(len(jobs),{b:len(v) for b,v in out.items()})
