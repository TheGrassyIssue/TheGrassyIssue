import json,os,datetime
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
d=json.load(open('research/towels/sweep2.json'))
fail={k:v[0] for k,v in d['status'].items() if not v[1]}
fail.update({'goodgood':'goodgoodgolf.com','sunday-golf':'sundaygolf.com','sugarloaf':'sugarloafsocialclub.com','random':'randomgolfclub.com',
 'manors':'manorsgolf.com','metalwood':'metalwoodstudio.com','devant':'devant.com','sunfish':'sunfishgolf.com','barstool':'store.barstoolsports.com',
 'druids':'druidsgolf.com','wolfe':'wolfegolf.co','pga-merch':'x', 'eastside':'eastsidegolf.com','macade':'macadegolf.com','bogeybros':'bogeybros.com',
 'birdie-bell':'x','whiskey':'x','tee-box':'x','imperfect':'x','ranger':'x','devereux':'devereuxgolf.com','kingfisher':'kingfishergolfco.com',
 'fore-birdie':'x','quiet':'quietgolf.com','stripe':'stripe.golf','taboo':'x','foray':'foraygolf.com','sunny':'x','putterholik':'x',
 'pga-tour-no':'x','deuce':'x','aviator':'x','paisley':'x','caddy-daddy':'caddydaddygolf.com','caddie-lounge':'x','pars-and-pints':'x',
 'barbarian':'x','caddie-hall':'x','shinnecock':'x','loudmouth':'loudmouthgolf.com','golf-sickos':'x','scramble':'x','lie':'x',
 'shanks':'x','no-laying-up':'nolayingup.com','fried-egg':'thefriedegg.com','golfers-journal':'golfersjournal.com','foreplay':'foreplaypod.com',
 'rhoback':'rhoback.com','peter-millar-no':'x','seven-iron':'x','radmor':'radmorgolf.com','radda':'raddagolf.com','kjus':'x',
 'imperial':'x','barbados':'x','flag-pin':'x','pga':'x','sunice':'x','uther':'uthersupply.com','printworks':'printworks.golf','swannies':'swannies.com'})
fail={'random':'randomgolfclub.com','manors-me':'manors.me','metalwood':'metalwood.studio','mogshade':'mogshadegolf.com','stick-grips':'stickgripsgolf.com','swannies':'swannies.co','pluto':'pluto.golf','nly':'store.nolayingup.com','friedegg':'proshop.thefriedegg.com','gumtree':'gumtreegolfandnature.com','kingfisher':'kingfisher-golf.com','shoal':'shoalgolfco.com','shapland':'shaplandbags.com','manors-shop':'shop.manorsgolf.com','wolfe':'wolfegolf.com','bogey-boys':'bogeyboys.com','barstool':'barstoolsportsstore.com','turtleson':'turtleson.com','radda':'raddagolf.com','sunday-swagger':'sundayswagger.com','imperfect':'x'}
fail={k:v for k,v in fail.items() if v and v!='x' and v!='x.invalid'}
out=[];st={}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36')
    for slug,dom in fail.items():
        ok=False;n=0
        for page in range(1,5):
            try:
                r=ctx.request.get(f'https://{dom}/products.json?limit=250&page={page}',headers={'referer':f'https://{dom}/'},timeout=15000)
                j=r.json() if r.ok else None
            except Exception: j=None
            if not j or 'products' not in j: break
            ok=True
            if not j['products']: break
            for p_ in j['products']:
                if 'towel' not in p_['title'].lower() and 'towel' not in (p_.get('product_type') or '').lower(): continue
                v=p_['variants']; n+=1
                out.append(dict(brand=slug,domain=dom,title=p_['title'],handle=p_['handle'],price=min(float(x['price']) for x in v),avail=any(x.get('available') for x in v),
                  img=(p_['images'][0]['src'] if p_['images'] else None),imgs=[i['src'] for i in p_['images'][:6]],type=p_.get('product_type','')))
        st[slug]=(dom,ok,n)
    b.close()
json.dump({'read':datetime.date.today().isoformat(),'status':st,'items':out},open('research/towels/sweep4.json','w'),indent=1)
print({k:v for k,v in st.items() if v[1]})
print('fail',[k for k,v in st.items() if not v[1]])
