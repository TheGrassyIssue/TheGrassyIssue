import json,subprocess,re,sys,time
from concurrent.futures import ThreadPoolExecutor
D=['jonessportsco.com','stitchgolf.com','sundaygolf.com','ghostgolf.com','hirokigolf.com','vesselgolf.com','mnmlgolf.com','shoalgolf.com','seamusgolf.com','dormieworkshop.com','winstoncollection.com','pinsandaces.com','manorsgolf.com','malbon.com','jancraigheadcovers.com','zaleasgolf.com','apresgolf.com','gamutgolf.com','twentyfourgolf.com','clutchgolfcompany.com','sinkingbirdies.co.uk','bluetross.com','mackemgolf.com','mackenziegolfbags.com','sentinelgolf.com','shaplandgolf.com','standre.golf','fairwayandgreen.com','birdsofcondor.com','radmorgolf.com','metalwood.studio','lonetreesociety.com','bubbawhips.com','hickoryandheath.com','gumtreegolf.com','dimpledivot.com','wearemnml.com','qwaygolf.com','randomgolfclub.com','whimgolf.com']
KW=re.compile(r'\b(bag|headcover|head cover|cover|towel|pouch|valuables|scorecard|yardage|tee holder|divot|ball marker|brush)\b',re.I)
def get(dom):
    out=[]
    for page in (1,2,3):
        try:
            r=subprocess.run(['curl','-sL','-m','20','-A','Mozilla/5.0',f'https://{dom}/products.json?limit=250&page={page}'],capture_output=True,text=True,timeout=25)
            ps=json.loads(r.stdout).get('products',[])
        except Exception as e:
            return dom,out,str(e)[:40]
        if not ps: break
        for p in ps:
            t=p['title']+' '+(p.get('product_type') or '')
            if not KW.search(t): continue
            av=[v for v in p['variants'] if v.get('available')]
            if not av: continue
            out.append({'dom':dom,'title':p['title'],'handle':p['handle'],'type':p.get('product_type'),'price':min(float(v['price']) for v in av),
                        'nvar':len(p['variants']),'instock':len(av),'published':(p.get('published_at') or '')[:10],'tags':p.get('tags'),
                        'imgs':[i['src'] for i in p.get('images',[])][:8],'desc':re.sub('<[^>]+>',' ',p.get('body_html') or '')[:600]})
        if len(ps)<250: break
    return dom,out,''
res={}
with ThreadPoolExecutor(10) as ex:
    for dom,out,err in ex.map(get,D):
        res[dom]=out; print(f'{dom:28} {len(out):4} {err}')
# currency
for dom in D:
    try:
        r=subprocess.run(['curl','-sL','-m','15','-A','Mozilla/5.0',f'https://{dom}/meta.json'],capture_output=True,text=True,timeout=20)
        m=json.loads(r.stdout); res.setdefault('_meta',{})[dom]={'cur':m.get('currency'),'name':m.get('name'),'city':m.get('city'),'country':m.get('country')}
    except Exception: pass
json.dump({'read':'2026-09-28','stores':res},open('research/bag-setup/catalog.json','w'),indent=1)
