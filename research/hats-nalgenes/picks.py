import json,re,urllib.request as U
def J(u): return json.load(U.urlopen(U.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
def txt(h): return re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',h or '')).strip()
def shop(dom,handle,brand,cur='USD',pub=None,sec=''):
    p=J(f'https://{dom}/products/{handle}.json')['product']
    av=[v for v in p['variants'] if v.get('inventory_quantity',1)!=0] or p['variants']
    v=p['variants'][0]
    return dict(brand=brand,title=p['title'],price=float(v['price']),cmp=float(v['compare_at_price']) if v.get('compare_at_price') else None,cur=cur,
                url=f'https://{pub or dom}/products/{handle}',imgs=[i['src'] for i in p['images']][:5],body=txt(p['body_html']),sec=sec)
def canto(perm,sec):
    p=J(f'https://www.canto.vision/product/{perm}.js')
    return dict(brand='Canto',title=p['name'],price=float(p['price']),cmp=None,cur='USD',url='https://www.canto.vision/product/'+perm,imgs=[i['url'] for i in p['images']][:5],body=txt(p.get('description')),sec=sec)
P=[]
for h in ['forest-green-unstructured-corduroy-cap','off-white-unstructured-corduroy-cap','deep-navy-unstructured-corduroy-cap','khaki-green-unstructured-ripstop-nylon-cap','brown-unstructured-ripstop-nylon-cap','lilac-unstructured-ripstop-nylon-cap','cobalt-blue-unstructured-ripstop-nylon-cap','copper-orange-unstructured-ripstop-nylon-cap','off-white-midnight-navy-unstructured-ripstop-nylon-cap']:
    P.append(shop('drawgolf.co',h,'Draw','GBP',sec='draw'))
A='stv0e1-s1.myshopify.com'
for h in ['tree-hat-earth','golf-brand-hat-black','agronomy-work-hat']: P.append(shop(A,h,'Agronomy Workshop',pub='agronomywork.shop',sec='on'))
P+=[shop('parmoregolf.com','parmore-embroidered-5-panel','Parmore','GBP',sec='on')]
for d,h,b,c in [('quietgolf.com',None,'Quiet Golf','USD'),('www.mogshadegolf.com',None,'Mogshade','EUR'),('lazyface.com','the-chenille-sun-cap','Lazyface','USD'),('soundergolf.com','logo-cap-stone-copy','Sounder','GBP'),
                ('softhands.club','ggnc-x-puma-field-notes-6-panel-dad-hat','Gumtree Golf & Nature Club × Puma','USD'),('radmorgolf.com',None,'Radmor','USD'),('seamusgolf.com',None,'Seamus','USD'),('whimgolf.com',None,'Whim Golf','USD')]:
    if h is None:
        pat={'quietgolf.com':'Monogram Nylon Dad Hat','www.mogshadegolf.com':'Only Human Cap','radmorgolf.com':'Corduroy Script Cap','seamusgolf.com':'Seamus Vintage Patch Two-Tone','whimgolf.com':'Forest Green Embroidered Hat'}[d]
        h=[p['handle'] for p in json.load(open(f'stores/{d}.json')) if pat.lower() in p['title'].lower()][0]
    P.append(shop(d,h,b,c,sec='on'))
P.append(canto('cyco-vision-snapback-tree-camo-w-orange-embroidery','off'))
for d,pat,b,c in [('ebbets.com','Tokyo Giants Wool Mesh Trucker','Ebbets Field Flannels','USD'),('battenwear.com','Club Cap / Acorn Corduroy','Battenwear','USD'),('mustardbeetle.com','Ball Cap: Quail','Mustard Beetle','USD'),
                  ('hikerdelic.com','Sol Cap Olive','Hikerdelic','GBP'),('howlerbros.com','ACL Fest 2026 Snapback - Midnight Corduroy','Howler Bros','USD'),('districtvision.com','Paneled Nylon Hat, Cool Sage','District Vision','USD')]:
    h=[p['handle'] for p in json.load(open(f'stores/{d}.json')) if pat.lower() in p['title'].lower()][0]
    P.append(shop(d,h,b,c,sec='off'))
# bottles
P.append(shop('wearebraindead.com','brain-dead-x-sound-fury-2026-nalgene-brown','Brain Dead',sec='brand'))
P.append(canto('double-overhead-32oz-wide-mouth-nalgene','art')); P.append(canto('lemon-heads-32oz-wide-mouth-nalgene','art'))
for pat in ['Joshua Tree','Toad','Monarch','Hummingbirds','Prairie']:
    h=[p['handle'] for p in json.load(open('stores/mustardbeetle.com.json')) if p['title']=='Nalgene 32oz: '+pat][0]
    P.append(shop('mustardbeetle.com',h,'Mustard Beetle',sec='art'))
P.append(shop('topodesigns.com','topo-designs-x-pine-printshop-nalgene-water-bottle-proceed-slow-light-blue','Topo Designs × Pine Printshop',sec='art'))
P.append(shop('otsocycles.com','mythology-nalgene-bottle-32oz','Otso Cycles',sec='art'))
P.append(shop('parksproject.us','dark-sky-recycled-glow-in-the-dark-water-bottle','Parks Project',sec='brand'))
P.append(shop('parksproject.us','defend-the-parks-water-bottle','Parks Project',sec='brand'))
P.append(shop('crustbikes.com','magic-carpet-ride-nalgene','Crust Bikes',sec='brand'))
P.append(shop('golfwang.com','quake-water-bottle-by-golf-wang','Golf Wang',sec='brand'))
P.append(shop('softhands.club','gumtree-golf-nature-club-ny-branches-widemouth-nalgene-water-bottle','Gumtree Golf & Nature Club',sec='brand'))
P.append(shop('maplestore.com.au','yu-nagaba-printed-bottle-clear','and wander × Yu Nagaba','AUD',sec='brand'))
json.dump(P,open('picks.json','w'),indent=1)
for i,p in enumerate(P,1): print(i,p['sec'],p['brand'],'|',p['title'],'|',p['cur'],p['price'],p['cmp'],'| imgs',len(p['imgs']),'\n    ',p['body'][:230])
