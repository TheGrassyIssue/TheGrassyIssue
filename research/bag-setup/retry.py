import json,subprocess,re,time,sys
sys.path.insert(0,'research/bag-setup')
C=json.load(open('research/bag-setup/catalog.json'))
KW=re.compile(r'\b(bag|headcover|head cover|cover|towel|pouch|valuables|scorecard|yardage|tee holder|divot|ball marker|brush)\b',re.I)
todo=[d for d,v in C['stores'].items() if d!='_meta' and not v]
todo=[('www.manorsgolf.com' if d=='manorsgolf.com' else d) for d in todo]
t0=time.time()
for dom in todo:
    if time.time()-t0>150: print('time'); break
    out=[];err=''
    for page in (1,2):
        r=subprocess.run(['curl','-sL','-m','15','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36',f'https://{dom}/products.json?limit=250&page={page}'],capture_output=True,text=True)
        try: ps=json.loads(r.stdout).get('products',[])
        except Exception: err=r.stdout[:30].replace('\n',' '); break
        for p in ps:
            if not KW.search(p['title']+' '+(p.get('product_type') or '')): continue
            av=[v for v in p['variants'] if v.get('available')]
            if not av: continue
            out.append({'dom':dom,'title':p['title'],'handle':p['handle'],'type':p.get('product_type'),'price':min(float(v['price']) for v in av),'nvar':len(p['variants']),'instock':len(av),'published':(p.get('published_at') or '')[:10],'tags':p.get('tags'),'imgs':[i['src'] for i in p.get('images',[])][:8],'desc':re.sub('<[^>]+>',' ',p.get('body_html') or '')[:600]})
        if len(ps)<250: break
        time.sleep(1.5)
    key='manorsgolf.com' if 'manors' in dom else dom
    if out: C['stores'][key]=out
    print(f'{dom:28} {len(out):4} {err}'); time.sleep(2.5)
json.dump(C,open('research/bag-setup/catalog.json','w'),indent=1)
