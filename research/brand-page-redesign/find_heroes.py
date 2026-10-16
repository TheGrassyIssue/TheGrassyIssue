import json,re,os,glob
from PIL import Image
B=json.load(open('data/brands.json')); M=json.load(open('data/brand-mentions.json'))
norm=lambda x:re.sub(r'[^a-z0-9]','',(x or '').lower())
cur={}
for f in glob.glob('brands/*.html'):
    if ' ' in f: continue
    s=open(f).read(); i=s.find('<div class="bp2-hero">')
    if i<0: continue
    m=s[i:s.find('bp2-shade',i)]
    cur[os.path.basename(f)[:-5]]='wide' if ('bp2-tri' not in m and 'bp2-solo' not in m and '<img' in m) else ('tri' if 'bp2-tri' in m else ('solo' if 'bp2-solo' in m else 'none'))
W={}
def w(p):
    if p not in W:
        try: W[p]=Image.open(p.lstrip('/')).size
        except Exception: W[p]=(0,0)
    return W[p]
allimgs=[p for p in glob.glob('images/**/*.jpg',recursive=True) if ' ' not in p]
out={}
for b in B:
    s=b['slug']
    if s not in cur or cur[s]=='wide': continue
    n=norm(b['name']); toks={norm(s),n,norm(s.replace('-golf','')),norm(b['name'].split()[0]) if len(norm(b['name'].split()[0]))>4 else n}
    cands=[]
    for e in M.get(s,[]):
        u=e['url'].split('#')[0]; p=u.lstrip('/')+'.html'
        if not os.path.exists(p): continue
        h=open(p).read()
        t=norm(e['title'])
        hm=re.search(r'<div class="drop-hero-img">\s*<img src="([^"]+)"',h)
        if hm and n[:6] in t:
            sz=w(hm.group(1))
            if sz[0]>=1600 and sz[0]/max(1,sz[1])>=1.5: cands.append(('posthero',hm.group(1),sz,e['title'][:60]))
    for p in allimgs:
        fn=norm(os.path.basename(p))
        if any(len(t)>4 and t in fn for t in toks):
            sz=w('/'+p)
            if sz[0]>=1600 and sz[0]/max(1,sz[1])>=1.45: cands.append(('file','/'+p,sz,''))
    out[s]=dict(name=b['name'],posts=len(M.get(s,[])),cur=cur[s],cands=cands[:8])
json.dump(out,open('research/brand-page-redesign/hero-cands.json','w'),indent=1)
have=[k for k,v in out.items() if v['cands']]
print(len(out),'non-wide;',len(have),'with on-site candidates')
for k in sorted(out,key=lambda k:-out[k]['posts'])[:60]:
    v=out[k]; print(v['posts'],k,v['cur'],[ (c[0],c[1].split('/')[-2]+'/'+c[1].split('/')[-1],c[2]) for c in v['cands'][:3]])
