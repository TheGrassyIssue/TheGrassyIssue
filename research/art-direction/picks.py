import json,re,os,glob
S=json.load(open('../../data/brand-socials.json'))
def hv(s): return {r['i']:r['u'] for r in json.load(open(f'harvest-{s}.json'))}
def homeurl(s,i):
    # home images saved as raw/<s>/home-ii.img; recover URL by re-parsing home.html in same order as collect.py
    h=open(f'raw/{s}/home.html').read(); urls=[]
    for m in re.findall(r'(?:https?:)?//[^"\'\s]+?(?:cdn/shop/files|images\.squarespace-cdn\.com/content)[^"\'\s]+?\.(?:jpg|jpeg|png|webp)',h,re.I):
        u=('https:'+m if m.startswith('//') else m); u=re.sub(r'_\d+x\d*(?=\.)','',u)
        if not re.search(r'(?i)logo|icon|favicon|badge|payment',u) and u not in urls: urls.append(u)
    return urls[i].split('?')[0]
BAND={'whim-golf':[('home',4),31,64],'left-of-field-golf':[('home',2),('home',3),('home',4)],'sentinel-golf':[15,80,85],
'found-golf':[65,29,47],'kingfisher-golf':[0,60,54],'cloud-and-wind-golf':[3,12,26],'forden-golf':[('tgi','/images/forden/d-umbrella-canopy.jpg'),('tgi','/images/forden/d-swinging-ls-red.jpg'),('home',5)],
'radry-golf':[('home',0),51,65],'fyfe-golf':[14,48,66],'slice-town':[2,28,47],'mogshade':[16,21,13],'puttwell':[('home',3),32,31],'hidden-links-society':[('home',0),('home',2),45]}
PROD={'whim-golf':['white-embroidered-navy-merino-long-sleeve-golf-shirt','la-cupola-paperweight','big-bag-sky-blue-logo'],
'left-of-field-golf':['mornington-polo-blue-white-stripe','heritage-plaid-cap-red','portsea-jacket'],
'sentinel-golf':['Basecamp Walker - White Dyneema','Sørensen Fairway Cover - Dark Nubuck','Kvadrat Headcovers - Heather'],
'found-golf':['soof-flash-box-sweater','dad-cap-off-white','briony-wright-cone-piece-vase'],
'kingfisher-golf':['golf-tee-box','worst-golfer-in-dallas-tee','scallop-polo-in-maroon'],
'cloud-and-wind-golf':['The Blossom','Cloud & Wave: Afterglow','Serenade Trio'],
'forden-golf':['black-forden-x-new-era-trucker-swingman-snapback','forden-golf-aluminem-alloy-pouch-can','off-white-golf-swing-long-sleeve'],
'radry-golf':['mouthful-tee','belly-up-hat','staple-crew'],
'fyfe-golf':['second-round-remake-03-headcover','fulmar-herringbone-summer-tweed-headcover-limited-edition','marksman-range-finder-case-orange-desert'],
'slice-town':['knitted-golf-balaclava','track-jacket-cobalt','short-sleeve-windbreaker-charcoal'],
'mogshade':['ria-course-case','golf-curated-t-shirt','links-wool-poster'],
'puttwell':['waikahalulu-fridays-only-polo-1','sig-on-smith-golf-bag','course-cali-stripe-polo'],
'hidden-links-society':['dead-run-hoodie-oatmeal','society-skateboard-deck-orange-green','play-faster-hat-walnut']}
out={}
for s in BAND:
    H=hv(s); band=[]
    for b in BAND[s]:
        if isinstance(b,int): band.append(H[b])
        elif b[0]=='home': band.append(homeurl(s,b[1]))
        else: band.append(b[1])
    w=S[s]['website'].rstrip('/'); d=json.load(open(f'stores/{s}.json')); prods=[]
    for key in PROD[s]:
        if 'products' in d:
            p=next(p for p in d['products'] if p['handle']==key)
            assert any(v['available'] for v in p['variants']),key
            v=p['variants'][0]
            prods.append(dict(title=p['title'],price=float(v['price']),cmp=float(v.get('compare_at_price') or 0),url=f"{w}/products/{key}",imgs=[i['src'] for i in p['images'][:5]],body=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',p['body_html'] or ''))[:900]))
        else:
            x=next(x for x in d['items'] if x['title']==key); v=x['structuredContent']['variants']
            prods.append(dict(title=key,price=float(v[0]['priceMoney']['value']),cmp=0,url=w+x['fullUrl'],imgs=[i['assetUrl'] for i in (x.get('items') or [])[:5]],body=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',x.get('excerpt') or ''))[:900]))
    out[s]=dict(band=band,prods=prods)
json.dump(out,open('picks.json','w'),indent=1,ensure_ascii=False)
print({s:(len(v['band']),len(v['prods'])) for s,v in out.items()})
