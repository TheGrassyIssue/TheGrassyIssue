import json,re,time,os
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
C=json.load(open('research/bag-setup/catalog.json'))
KW=re.compile(r'\b(bag|headcover|head cover|cover|towel|pouch|valuables|scorecard|yardage|tee holder|divot|ball marker|brush)\b',re.I)
todo=[d for d,v in C['stores'].items() if d!='_meta' and not v]
t0=time.time()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36")
    for dom in todo:
        if time.time()-t0>140: print('time'); break
        host='www.manorsgolf.com' if dom=='manorsgolf.com' else dom
        try:
            r=ctx.request.get(f'https://{host}/products.json?limit=250',timeout=20000); txt=r.text()
            ps=json.loads(txt).get('products',[])
        except Exception as e:
            print(f'{dom:26} ERR {str(e)[:50]}'); continue
        out=[]
        for q in ps:
            if not KW.search(q['title']+' '+(q.get('product_type') or '')): continue
            av=[v for v in q['variants'] if v.get('available')]
            if not av: continue
            out.append({'dom':dom,'title':q['title'],'handle':q['handle'],'type':q.get('product_type'),'price':min(float(v['price']) for v in av),'nvar':len(q['variants']),'instock':len(av),'published':(q.get('published_at') or '')[:10],'tags':q.get('tags'),'imgs':[i['src'] for i in q.get('images',[])][:8],'desc':re.sub('<[^>]+>',' ',q.get('body_html') or '')[:600]})
        if out: C['stores'][dom]=out
        print(f'{dom:26} {len(ps):4} {len(out):4}'); time.sleep(2)
    b.close()
json.dump(C,open('research/bag-setup/catalog.json','w'),indent=1)
