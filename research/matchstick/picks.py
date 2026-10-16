import json,re,urllib.request,os,concurrent.futures as cf
P={p['handle']:p for p in json.load(open('p1.json'))['products']}
GROUPS=[
("drinks",["old-fashioned","transfusion","iced-coffee-golf-ball-marker","ball-marker-flaming-coffee-mug","putterade-frost","putterade-lemon-lime"]),
("pop",["devil-horns-black-gold","truffle-shuffle","pirate-flag","skeleton-key","vw-bus","chef-skull"]),
("gamble",["cash","poker-chip","red-dice","gas-pump-golf-ball-marker","fire-truck-golf-ball-marker"]),
("home",["oregon-state-beavers-head-golf-ball-marker-brushed-gold","teddy-roosevelt","lady-liberty-ball-marker","build-your-own-custom-golf-ball-marker"]),
("covers",["usa-dream-team-basketball-upcycled-headcover-drive","u-s-soccer-upcycled-headcover-driver","new-york-basketball-driver-golf-headcover","roosevelt-pattern-driver-headcover","osu-beavers-black-driver-no-1"]),
("around",["roosevelt-pattern-golf-towel","key-lime-pie","matchstick-man-jones-ranger-r-shag-bag-black","tiger-roar-relief-print"]),
]
out=[];jobs=[]
os.makedirs('raw',exist_ok=True)
for g,hs in GROUPS:
    for h in hs:
        h=sorted([k for k in P if k.startswith(h)],key=len)[0]; p=P[h]
        v=p['variants'][0]; key=re.sub(r'[^a-z0-9]','',h)[:22]
        assert any(x['available'] for x in p['variants']),h
        out.append(dict(group=g,handle=h,key=key,title=p['title'],price=v['price'],cmp=v.get('compare_at_price'),n=len(p['images']),body=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p['body_html'] or ''))[:1500]))
        for i,im in enumerate(p['images'][:6],1): jobs.append((im['src'],f'raw/{key}-{i}.img'))
json.dump(out,open('picks.json','w'),indent=1)
def dl(j):
    u,f=j
    if os.path.exists(f): return
    open(f,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(dl,jobs))
print(len(out),len(jobs))
