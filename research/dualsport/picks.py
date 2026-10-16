import json,re,urllib.request,os,concurrent.futures as cf
P={p['handle']:p for p in json.load(open('p1.json'))['products']}
# (group, handle, alt colorway handles)
G=[
("polos","flight-knit-polo-light-grey",["flight-knit-polo-seafoam-green","flight-knit-polo-black","flight-knit-polo-cream"]),
("polos","diamond-blade-polo-green",["diamond-blade-polo-black"]),
("polos","icon-polo-electric-blue",["icon-polo-white","icon-polo-dark-grey"]),
("polos","icon-polo-galaxy",[]),
("polos","signature-polo-dark-floral",[]),
("layers","elite-windbreaker",[]),
("layers","pursuit-windbreaker-black",["pursuit-windbreaker-electric-blue"]),
("layers","cloud-performance-quarter-zip-grey",["cloud-performance-quarter-zip-copy"]),
("layers","shiver-quarter-zip-mist",["shiver-quarter-zip-black"]),
("layers","knit-jersey",[]),
("layers","volt-knit-vest",[]),
("bottoms","pursuit-shorts-electric-blue",["pursuit-shorts-sage","pursuit-shorts-black"]),
("bottoms","motion-pants-black",["motion-pants-platinum-grey"]),
("bottoms","motion-shorts-platinum-grey",["motion-shorts-navy","motion-shorts-black"]),
("hats","arch-athletic-club-hat-white",["arch-athletic-club-hat-black","arch-athletic-club-unstructured-hat"]),
("hats","ds-camo-hat",[]),
("hats","dual-athletic-club-hat-green",["dual-athletic-club-hat-black"]),
("hats","vintage-ds-classic-unstructured-hat-camo",["vintage-ds-classic-unstructured-hat-black","vintage-ds-classic-unstructured-hat-white-black"]),
("acc","dual-driver-headcover",[]),
("acc","dual-mallet-cover",[]),
("acc","the-gray-t-shirt-1",[]),
("tees","pro-day-tshirt",[]),
("tees","baller-tshirt",[]),
("tees","throwback-tshirt",[]),
]
out=[];jobs=[]
os.makedirs('raw',exist_ok=True)
for g,h,alts in G:
    p=P[h]; v=p['variants'][0]; key=re.sub(r'[^a-z0-9]','',h)[:22]
    assert any(x['available'] for x in p['variants']),h
    alts=[a for a in alts if any(x['available'] for x in P[a]['variants'])]
    out.append(dict(group=g,handle=h,key=key,title=p['title'],price=v['price'],cmp=v.get('compare_at_price'),n=len(p['images']),alts=alts,
      colors=[P[a]['handle'] for a in alts],body=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p['body_html'] or ''))[:1500]))
    for i,im in enumerate(p['images'][:7],1): jobs.append((im['src'],f'raw/{key}-{i}.img'))
    for j,a in enumerate(alts,1):
        for i,im in enumerate(P[a]['images'][:2],1): jobs.append((im['src'],f'raw/{key}-c{j}{i}.img'))
for f in ['665534C9-B093-4B54-BCFA-4ABF5BEA1E7F.jpg','76FC67EE-09D0-476E-9950-597CC6628FD5.jpg','7F8D3BC4-FE13-4D86-A5B6-B17436056983.jpg','855EF4E8-BFF7-4659-A744-56C250CAF5EF.jpg','E3E85A6E-05F2-45A4-8AE2-D768CE63234A.jpg','IMG-4936.jpg','ME4A3429.jpg','afd63128-47c7-4d6c-b326-995d2015ffe8.png']:
    jobs.append(('https://dualsportbrand.com/cdn/shop/files/'+f,'raw/life-'+f.split('-')[0].split('.')[0]+'.img'))
json.dump(out,open('picks.json','w'),indent=1)
def dl(j):
    u,f=j
    if os.path.exists(f): return
    try: open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
    except Exception as e: print('ERR',u,e)
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(dl,jobs))
print(len(out),len(jobs))
