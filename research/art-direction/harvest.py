import json,re,os,io,urllib.request,concurrent.futures as cf
import numpy as np
from PIL import Image
S=json.load(open('../../data/brand-socials.json'))
UA={'User-Agent':'Mozilla/5.0 (Macintosh)'}
def get(u,t=40): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t).read()
EXTRA={'fyfe-golf':['/pages/coastal-tones-lookbook-fyfe-golf','/pages/summer-tweeds-lookbook-fyfe-golf','/pages/the-shooters-club-lookbook'],'whim-golf':['/blogs/editorial.atom'],'left-of-field-golf':['/blogs/journal-entries.atom'],'found-golf':['/blogs/articles.atom'],'forden-golf':['/pages/lookbook'],
'radry-golf':['/blogs/journal.atom'],'axxa':['/blogs/journal.atom'],'mogshade':['/blogs/journal.atom'],'puttwell':['/blogs/lookbooks.atom'],'sentinel-golf':['/story-1','/expedition-one','/about'],'cloud-and-wind-golf':['/our-identity','/']}
import sys
L0=['whim-golf','left-of-field-golf','sentinel-golf','found-golf','kingfisher-golf','cloud-and-wind-golf','forden-golf','radry-golf','axxa','slice-town','mogshade','puttwell','hidden-links-society']
L=sys.argv[1:] or L0
out={}
for s in L:
    w=S[s]['website'].rstrip('/'); urls=[]
    f=f'stores/{s}.json'
    if os.path.exists(f):
        d=json.load(open(f))
        if 'products' in d:
            ps=sorted([p for p in d['products'] if any(v['available'] for v in p['variants'])],key=lambda p:p['published_at'] or '',reverse=True)[:40]
            for p in ps:
                for im in p['images'][:8]: urls.append(('prod',p['handle'],im['src']))
        else:
            for it in d.get('items',[]):
                for im in (it.get('items') or [])[:8]:
                    if im.get('assetUrl'): urls.append(('prod',it.get('urlId'),im['assetUrl']))
    for e in EXTRA.get(s,[]):
        try:
            h=get(w+e).decode('utf8','ignore'); h=h.replace('&amp;','&').replace('&quot;','"')
            for m in re.findall(r'(?:https?:)?//[^"\'\s<>]+?(?:cdn/shop/(?:files|articles)|images\.squarespace-cdn\.com/content)[^"\'\s<>]+?\.(?:jpg|jpeg|png|webp)',h,re.I):
                u='https:'+m if m.startswith('//') else m
                urls.append(('page',e,re.sub(r'_\d+x\d*(?=\.)','',u)))
        except Exception as ex: print('ERR',s,e,ex)
    seen=set();U=[]
    for k,h,u in urls:
        base=u.split('?')[0]
        if base in seen or re.search(r'(?i)logo|icon|favicon|badge|payment',base): continue
        seen.add(base);U.append((k,h,base))
    out[s]=U
def sized(u,w): return u+('?width=%d'%w if ('cdn/shop' in u) else '?format=%dw'%w)
def cls(job):
    s,i,(k,h,u)=job
    try:
        im=Image.open(io.BytesIO(get(sized(u,300),30))).convert('RGB')
        a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
        light=bool(b.min(axis=1).mean()>200 and b.std()<12)
        return s,i,k,h,u,im.size,light
    except Exception as e: return s,i,k,h,u,None,None
jobs=[(s,i,x) for s,U in out.items() for i,x in enumerate(U[:90])]
res=[]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(cls,jobs): res.append(r)
json.dump([dict(s=r[0],i=r[1],k=r[2],h=r[3],u=r[4],size=r[5],light=r[6]) for r in res],open(f'harvest-{L[0]}.json','w'),indent=0)
import collections
c=collections.Counter((r[0],r[6]) for r in res)
for s in L: print(s,'lifestyle',c[(s,False)],'studio',c[(s,True)],'fail',c[(s,None)])
