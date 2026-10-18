import json
o=json.load(open('opts.json'))
def get(store,handle,brand,cur='USD',note='',base=None):
    for p in json.load(open(f'stores/{store}.json')):
        if p['handle']==handle:
            av=[v for v in p['variants'] if v['available']]
            t=p['title']
            if brand=='Agronomy Workshop': t+=' – '+('Earth' if 'earth' in handle else 'Black' if 'black' in handle else 'Natural')
            return dict(brand=brand,title=t,price=float(av[0]['price']),cur=cur,avail=True,url=f"https://{base or store}/products/{handle}",img=p['images'][0]['src'],note=note)
    raise SystemExit('missing '+handle)
A='stv0e1-s1.myshopify.com'
x=[get(A,'tree-hat-earth','Agronomy Workshop',base='agronomywork.shop'),get(A,'tree-hat','Agronomy Workshop',base='agronomywork.shop'),
   get(A,'golf-brand-hat-earth','Agronomy Workshop',base='agronomywork.shop'),get(A,'golf-brand-hat-black','Agronomy Workshop',base='agronomywork.shop'),
   get(A,'agronomy-work-hat','Agronomy Workshop',base='agronomywork.shop'),
   get('parmoregolf.com','parmore-embroidered-5-panel','Parmore','GBP','Your pick'),
   get('slice-town.com','canvas-logo-cap-brown','SLICE TOWN','SEK'),get('slice-town.com','green-sports-cap','SLICE TOWN','SEK'),
   get('found.golf','dad-cap-off-white','Found','AUD'),
   get('lazyface.com','the-chenille-sun-cap','Lazyface'),get('lazyface.com','the-river-cap','Lazyface'),
   get('soundergolf.com','logo-cap-stone-copy','Sounder','GBP'),
   get('mountteegolf.com.au','untitled-feb11_07-58','Mount Tee','AUD'),get('mountteegolf.com.au','monoball-5-panel-cap-cream-chocolate-brown','Mount Tee','AUD'),
   get('softhands.club','ggnc-x-puma-field-notes-6-panel-dad-hat','Gumtree × Puma'),
   get('districtvision.com','paneled-nylon-hat-cool-sage','District Vision'),
   get('puttwellgolfclub.com','snake-hat','Puttwell')]
o['hats3']=x; json.dump(o,open('opts.json','w'),indent=1)
for i in x: print(i['brand'],i['title'],i['cur'],i['price'])
