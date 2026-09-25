import json,re,collections
items=[]
for f in ['sweep2','sweep3','sweep4','sweep5']:
    d=json.load(open(f'research/towels/{f}.json')); items+=d['items']
ALIAS={'goodgood':'good-good','sugarloaf':'sugarloaf-social-club','devereux':'devereux-golf','foray':'foray-golf','nly':'no-laying-up','friedegg':'the-fried-egg','pluto':'pluto-golf','shoal':'shoal-golf'}
NOT_INDIE={'puma-golf','travismathew','bag-boy','winston-collection','sunnylife','johnnie-o','clint-orms','jlindeberg'}
EXCL=re.compile(r'junior|\bjr\b|bundle|combo|clip|holder|ball towel|gift ?card|pga jr|half-zi|mystery|sample|cubs|nfl|mlb|nba|\bfc\b|south park|towelie|tito|bottle|headcover|putter cover|hat\b|custom',re.I)
FALL=re.compile(r'waffle|jacquard|knit|chenille|wool|plaid|tartan|paisley|black|navy|olive|forest|brown|burgundy|rust|oat|tan|cream|camo|green|pine|charcoal|grey|gray|ranger|caddie|caddy|tour|players?',re.I)
seen=set();by=collections.defaultdict(list)
for r in items:
    b=ALIAS.get(r['brand'],r['brand'])
    if b in NOT_INDIE: continue
    key=(r['domain'],r['handle'])
    if key in seen: continue
    seen.add(key)
    if not r.get('avail') or not r.get('price') or r['price']<10: continue
    if EXCL.search(r['title']): continue
    r['brand']=b; r['score']=len(FALL.findall(r['title']))
    by[b].append(r)
cands=[]
for b,v in by.items():
    v.sort(key=lambda x:(-x['score'],x['price']))
    # take up to 2 distinct looks
    picked=[];bases=set()
    for x in v:
        base=re.sub(r'\s*[-–/|]\s*[^-–/|]+$','',x['title']).lower()
        if base in bases: continue
        bases.add(base); picked.append(x)
        if len(picked)==2: break
    cands+=picked
json.dump(cands,open('research/towels/cands.json','w'),indent=1)
print(len(by),'brands',len(cands),'cands'); 
for b in sorted(by): print(b, [ (x['title'][:40],x['price']) for x in cands if x['brand']==b])
