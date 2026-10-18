import json,re,os,urllib.request,concurrent.futures as cf,sys
S=json.load(open('../../data/brand-socials.json'))
L=['whim-golf','left-of-field-golf','sentinel-golf','found-golf','kingfisher-golf','cloud-and-wind-golf','forden-golf','radry-golf','axxa','slice-town','mogshade','puttwell','hidden-links-society']
UA={'User-Agent':'Mozilla/5.0 (Macintosh)'}
def get(u,t=40): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t).read()
jobs=[]
for s in L:
    os.makedirs(f'raw/{s}',exist_ok=True); w=S[s]['website'].rstrip('/')
    try: h=get(w+'/').decode('utf8','ignore'); open(f'raw/{s}/home.html','w').write(h)
    except Exception as e: print('home ERR',s,e); h=''
    urls=[]
    for m in re.findall(r'(?:https?:)?//[^"\'\s]+?(?:cdn/shop/files|images\.squarespace-cdn\.com/content)[^"\'\s]+?\.(?:jpg|jpeg|png|webp)',h,re.I):
        u=('https:'+m if m.startswith('//') else m); u=re.sub(r'_\d+x\d*(?=\.)','',u)
        if not re.search(r'(?i)logo|icon|favicon|badge|payment',u) and u not in urls: urls.append(u)
    for i,u in enumerate(urls[:14]): jobs.append((u+('&' if '?' in u else '?')+('width=2000' if 'shopify' in u or 'cdn/shop' in u else 'format=2500w'),f'raw/{s}/home-{i:02d}.img'))
def dl(j):
    u,f=j
    if os.path.exists(f): return
    try: open(f,'wb').write(get(u,60))
    except Exception as e: print('ERR',u[:90],e)
with cf.ThreadPoolExecutor(12) as ex: list(ex.map(dl,jobs))
print(len(jobs))
