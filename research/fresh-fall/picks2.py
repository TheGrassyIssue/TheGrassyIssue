# v2: lead every gallery with an on-model frame where the brand has one (all images scanned, not just the first five)
import json,os,subprocess,numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
P=json.load(open('picks.json'))
def load(k): return {p['handle']:p for p in json.load(open(f'{k}.json'))['products']}
D={'students':load('students'),'walker':load('walker')}
jobs=[]
for b in D:
    for it in P[b]:
        it['all']=[i['src'].split('?')[0] for i in D[b][it['h']]['images']][:10]
        for n,u in enumerate(it['all'],1): jobs.append((f"raw/a_{it['key']}-{n}.jpg",u))
def dl(j):
    fn,u=j
    if not os.path.exists(fn) or os.path.getsize(fn)<5000: subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0','-o',fn,u+'?width=1600'])
with ThreadPoolExecutor(16) as ex: list(ex.map(dl,jobs))
def islight(fn):
    a=np.asarray(Image.open(fn).convert('RGB').resize((200,250))).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>205
for b in D:
    for it in P[b]:
        fs=[f"raw/a_{it['key']}-{n}.jpg" for n in range(1,len(it['all'])+1)]
        life=[f for f in fs if not islight(f)]; pack=[f for f in fs if islight(f)]
        sel=life[:2]+pack[:3]
        if len(sel)<5: sel+= [f for f in life[2:]+pack[3:]][:5-len(sel)]
        for n,f in enumerate(sel,1): os.replace(f,f"raw/{it['key']}-{n}.jpg") if False else subprocess.run(['cp',f,f"raw/{it['key']}-{n}.jpg"])
        it['imgs']=[it['all'][fs.index(f)] for f in sel]; it['lead_life']=bool(life)
        del it['all']
json.dump(P,open('picks.json','w'),indent=1)
print({b:sum(i['lead_life'] for i in P[b]) for b in D})
