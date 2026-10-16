"""Collect each brand's own website + Instagram handle (15 Oct 2026, brand page redesign).
Website: data/brand-stores.json first; else the most common domain of that brand's own product links in our posts.
Instagram: read from the brand's own homepage (footer/header links). Nothing is guessed; misses stay empty."""
import json,re,os,collections,urllib.request,urllib.parse,concurrent.futures as cf,html as H
ROOT='.'
B=json.load(open('data/brands.json')); M=json.load(open('data/brand-mentions.json'))
ST=json.load(open('data/brand-stores.json'))['stores']
norm=lambda x:re.sub(r'[^a-z0-9]','',(x or '').lower())
BAD={'amazon.com','www.amazon.com','instagram.com','www.instagram.com','etsy.com','www.etsy.com','ebay.com','www.ebay.com','thegrassyissue.com','shop.app','golfgalaxy.com','dickssportinggoods.com','pgatoursuperstore.com','bit.ly','linktr.ee','nordstrom.com','www.nordstrom.com','mrporter.com','www.mrporter.com','ssense.com','www.ssense.com','fairwaystyles.com'}
def site_from_posts(b):
    c=collections.Counter(); n=norm(b['name'])
    for e in M.get(b['slug'],[]):
        p=e['url'].split('#')[0].lstrip('/')+'.html'
        if not os.path.exists(p): continue
        h=open(p,encoding='utf-8').read()
        for m in re.finditer(r'<div class="product-brand">(.*?)</div>(.*?)class="product-link"',h,re.S):
            bt=norm(H.unescape(re.sub(r'<[^>]+>','',m.group(1))).split('·')[0])
            if not bt or not (bt==n or n.startswith(bt) and len(bt)>4 or bt.startswith(n) and len(n)>4): continue
            seg=h[m.end()-200:m.end()+400]
            hm=re.search(r'href="(https?://[^"]+)"[^>]*class="product-link"|class="product-link"[^>]*href="(https?://[^"]+)"',h[m.start():m.end()+600])
            if hm:
                d=urllib.parse.urlparse(hm.group(1) or hm.group(2)).netloc.lower()
                if d and d not in BAD: c[d]+=1
    return ('https://'+c.most_common(1)[0][0]+'/') if c else None
SKIP={'p','reel','reels','explore','accounts','sharer','share','tv','stories','direct','about','legal','developer','instagram'}
def ig(url):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}),timeout=20)
        h=r.read(1500000).decode('utf-8','ignore'); final=r.geturl()
    except Exception as e: return None,None,str(e)[:60]
    hs=[x for x in re.findall(r'instagram\.com/([A-Za-z0-9_.]{2,30})',h) if x.lower() not in SKIP]
    c=collections.Counter(x.lower().rstrip('.') for x in hs)
    return (c.most_common(1)[0][0] if c else None), final, None
out={}
jobs={}
for b in B:
    if not M.get(b['slug']): continue
    s=(ST.get(b['slug']) or {}).get('url'); src='brand-stores'
    if not s: s=site_from_posts(b); src='post links'
    out[b['slug']]={'name':b['name'],'site':s,'site_src':src if s else None,'instagram':None}
    if s: jobs[b['slug']]=s
with cf.ThreadPoolExecutor(12) as ex:
    res=dict(zip(jobs,ex.map(ig,jobs.values())))
for k,(h,final,err) in res.items():
    out[k]['instagram']=h; out[k]['final']=final; out[k]['err']=err
json.dump(out,open('research/brand-page-redesign/socials-raw.json','w'),indent=1)
print(len(out),'brands |',sum(1 for v in out.values() if v['site']),'with site |',sum(1 for v in out.values() if v['instagram']),'with instagram')
