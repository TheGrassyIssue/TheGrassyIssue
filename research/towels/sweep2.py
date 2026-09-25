import json,urllib.request,concurrent.futures as cf,re,datetime
S=json.load(open('data/brand-stores.json'))['stores']
stores={k:v['domain'] for k,v in S.items()}
EXTRA={'devant':'devantltd.com','malbon':'malbon.com','eastside-golf':'eastsidegolf.com','bogey-boys':'bogeyboys.com',
 'sugarloaf-social-club':'sugarloafsocialclub.com','manors':'manorsgolf.com','pins-and-aces':'pinsandaces.com','muni-kids':'munikids.com',
 'random-golf-club':'randomgolfclub.com','mogshade':'mogshade.com','stitch-golf':'stitchgolf.com','sunday-golf':'sundaygolf.com',
 'jones-sports-co':'jonessportsco.com','vessel':'vesselgolf.com','ghost-golf':'ghostgolf.com','mnml-golf':'mnmlgolf.com','turtleson':'turtleson.com',
 'holderness-bourne':'holdernessandbourne.com','linksoul':'linksoul.com','bad-birdie':'badbirdie.com','frogger':'froggergolf.com','sunfish':'sunfish.com',
 'foreway':'forewaygolf.com','kingfisher-golf':'kingfishergolf.com','metalwood-studio':'metalwoodstudio.com','radmor':'radmorgolf.com',
 'stick-grips':'stickgrips.com','swannies':'swanniesgolf.com','dormie-workshop':'dormieworkshop.com','asbri':'asbrigolf.com','club-glove':'clubglove.com',
 'barrel-and-co':'barrelandco.com','sentinel-golf':'sentinelgolf.com','pluto-golf':'plutogolf.com','odd-ritual':'oddritualgolf.com','good-good':'goodgoodgolf.com',
 'bettinardi':'bettinardi.com','mackenzie':'mackenziegolfbags.com','seamus':'seamusgolf.com','uther':'uthersupply.com','printworks':'printworksgolf.com',
 'waggle':'wagglegolf.com','hedge':'hedgegolf.com','students':'studentsgolf.com','devereux':'devereuxgolf.com','fore-all':'foreallgolf.com',
 'lowercase-golf':'lowercasegolf.com','vice':'vicegolf.com','stix':'stixgolf.com','haywood':'haywoodgolf.com','ace-of-clubs':'aceofclubsgolfco.com',
 'cmyk-golf':'cmykgolf.com','palm-golf':'palmgolfco.com','bunker-mentality':'bunkermentality.com','sounder':'soundergolf.com','manors-golf':'manorsgolf.com',
 'metalwood':'metalwoodstudio.com','axxa':'axxagolf.com','ald':'aimeleondore.com','twentyfour':'twentyfourgolf.com','gumtree':'gumtreegolf.com',
 'wolfe-golf':'wolfegolf.com','shoal':'shoal.golf','shapland':'shaplandgolf.com','late-nine':'latenine.com','criquet':'criquetshirts.com',
 'fairway-fingers':'fairwayfingers.com','caddie-craft':'caddiecraft.com','golf-le-fleur':'golflefleur.com','tee-off-club':'teeoffclub.com',
 'foretrack':'foretrack.com','peachtree-towel':'peachtreetowel.com','pine-hill':'pinehillgolf.com','westward-golf':'westwardgolf.com',
 'burrow-golf':'burrowgolf.com','uncommon-golf':'uncommongolf.com','linksoul-2':'linksoul.com','taylormade-no':'x.invalid','birdie-juice':'birdiejuice.com',
 'nomad-golf':'nomadgolf.com','the-golfers-journal':'golfersjournal.com','tpc-sawgrass-shop':'x.invalid','sunday-red':'sundayred.com','bonobos':'bonobos.com',
 'crap':'crapeyewear.com','goodfellows':'goodfellowsgolf.com','whiskey-hotel':'x.invalid','thursday-golf':'thursdaygolf.com','quiet-golf':'quietgolf.com',
 'eastside':'eastsidegolf.com','foray':'foraygolf.com','bogey-boys-2':'bogeyboys.com','pga-west':'x.invalid','nice-shot':'niceshotgolf.com','stripe-golf':'stripegolf.com',
 'fairway-and-greene':'fairwayandgreene.com','rhoback':'rhoback.com','johnnie-o':'johnnie-o.com','linksoul3':'linksoul.com','kjus':'kjus.com',
 'barstool':'x.invalid','subpar':'subpargolf.com','golf-junkie':'golfjunkie.com','sunnylife':'sunnylife.com','caddyshack':'x.invalid','fore-play':'x.invalid',
 'golfhaus':'golfhaus.com','tour-towel':'x.invalid','club-house-golf':'x.invalid','hudson-sutler':'hudsonsutler.com','dewsweeper':'dewsweepergolf.com',
 'mulligan-golf':'x.invalid','country-club-prep':'x.invalid','smathers-branson':'smathersandbranson.com','lucky-golf':'x.invalid'}
for k,v in EXTRA.items():
    if v!='x.invalid' and v not in stores.values(): stores.setdefault(k,v)
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Accept':'application/json'}
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=15) as r: return json.loads(r.read())
    except Exception: return None
def sweep(item):
    slug,dom=item; out=[]; ok=False
    for page in range(1,5):
        d=get(f'https://{dom}/products.json?limit=250&page={page}')
        if not d or 'products' not in d: break
        ok=True
        if not d['products']: break
        for p in d['products']:
            t=p['title'].lower()
            if 'towel' not in t and 'towel' not in (p.get('product_type') or '').lower(): continue
            v=p['variants']; prices=sorted(float(x['price']) for x in v)
            out.append(dict(brand=slug,domain=dom,title=p['title'],handle=p['handle'],price=prices[0],avail=any(x.get('available') for x in v),
              img=(p['images'][0]['src'] if p['images'] else None),imgs=[i['src'] for i in p['images'][:6]],type=p.get('product_type',''),
              created=(p.get('created_at') or '')[:10],published=(p.get('published_at') or '')[:10]))
    return slug,dom,ok,out
res=[];status={}
with cf.ThreadPoolExecutor(24) as ex:
    for slug,dom,ok,out in ex.map(sweep,stores.items()):
        status[slug]=(dom,ok,len(out)); res+=out
json.dump({'read':datetime.date.today().isoformat(),'status':status,'items':res},open('research/towels/sweep2.json','w'),indent=1)
print('stores',len(stores),'shopify ok',sum(1 for v in status.values() if v[1]),'brands w/ towels',len({r['brand'] for r in res}),'towels',len(res))
