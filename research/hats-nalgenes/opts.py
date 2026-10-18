import json,re,urllib.request,base64,io,os
from PIL import Image
R=1.34
def shop(store,pat,brand,note=''):
    out=[]
    for p in json.load(open(f'stores/{store}.json')):
        if re.fullmatch(pat,p['title'],re.I) or (pat.startswith('~') and re.search(pat[1:],p['title'],re.I)):
            av=any(v['available'] for v in p['variants'])
            out.append(dict(brand=brand,title=p['title'],price=float(p['variants'][0]['price']),cur='GBP' if store in('drawgolf.co','hikerdelic.com') else 'USD',avail=av,url=f"https://{store}/products/{p['handle']}",img=p['images'][0]['src'] if p['images'] else '',note=note))
    return out
H=[];N=[]
# Draw
import urllib.request as u
dj=json.load(u.urlopen(u.Request('https://drawgolf.co/products.json?limit=250',headers={'User-Agent':'Mozilla/5.0'})))['products']
json.dump(dj,open('stores/drawgolf.co.json','w'))
for p in dj:
    if 'CAP' in p['title']:
        H.append(dict(brand='Draw',title=p['title'].title(),price=float(p['variants'][0]['price']),cur='GBP',avail=any(v['available'] for v in p['variants']),url='https://drawgolf.co/products/'+p['handle'],img=p['images'][0]['src'],note='Your pick'))
H+=shop('wearebraindead.com','~UD Ibiza Cap','Brain Dead')
H+=shop('golfwang.com','~GOLF SHORES 5 PANEL|TIGER VARSITY G HAT|GLASS LOGO HAT|FEEL THE LIGHT 5 PANEL HAT - GREEN','Golf Wang')
H+=shop('hikerdelic.com','~Sol Cap|Worker Cap (Brown|Forest)','Hikerdelic')
H+=shop('mustardbeetle.com','~Ball Cap: Quail','Mustard Beetle')
H+=shop('howlerbros.com','~ACL Fest 2026 Snapback|Machete Sun Snapback - Antique','Howler Bros','Austin')
H+=shop('topodesigns.com','~New Belgium Brewing Corduroy Trucker','Topo Designs')
H+=shop('parksproject.us','~Nature Conservancy x Parks Project Patch Hat','Parks Project')
H+=shop('poler.com','~Font Patch Hat','Poler')
H+=shop('frogskateboards.com','~Trash Talk Hat','Frog Skateboards')
H+=shop('linksoul.com','~Sandbagger Unstructured','Linksoul')
H+=shop('williammurraygolf.com','~Fish Outta Water Sun Guru','William Murray')
H+=shop('crustbikes.com','~Crooked Captain Trucker','Crust Bikes')
H+=shop('pleasuresnow.com','~FILM SNAPBACK','Pleasures')
# Canto bigcartel
cj=json.load(u.urlopen(u.Request('https://www.canto.vision/products.json',headers={'User-Agent':'Mozilla/5.0'})))
json.dump(cj,open('stores/canto.json','w'))
for p in cj:
    img=p['images'][0]['url'] if p.get('images') else ''
    d=dict(brand='Canto',title=p['name'],price=float(p['price']),cur='USD',avail=p['status']=='active',url='https://www.canto.vision/product/'+p['permalink'],img=img,note='')
    if 'Nalgene' in p['name']: d['note']='Your pick' if 'Double' in p['name'] else ''; N.append(d)
    elif re.search('Snapback|Trucker|59FIFTY',p['name']) and p['status']=='active': H.append(d)
N.insert(0,dict(brand='Brain Dead',title='Brain Dead x Sound & Fury 2026 Nalgene – Brown',price=42,cur='USD',avail=True,url='https://wearebraindead.com/products/brain-dead-x-sound-fury-2026-nalgene-brown',img='https://cdn.shopify.com/s/files/1/0642/8893/files/Sound_and_Fury_Nalgene_Bottle_320z_Amber_Front_optimized.jpg',note='Your pick'))
N+=shop('mustardbeetle.com','~Nalgene 32oz: (Joshua Tree|Toad|Monarch|Hummingbirds|Prairie)','Mustard Beetle')
N+=shop('topodesigns.com','~Pine Printshop Nalgene Water Bottle - Proceed','Topo Designs × Pine Printshop')
N+=shop('parksproject.us','~Dark Sky Recycled|Defend the Parks Water','Parks Project')
N+=shop('crustbikes.com','~Cold Steel Will Forgive','Crust Bikes')
N+=shop('golfwang.com','~QUAKE WATER','Golf Wang','Wide-mouth 32oz; listing doesn’t say Nalgene')
N.append(dict(brand='Otso Cycles',title='Mythology Nalgene 32oz (art by Mary Lytle)',price=24.95,cur='USD',avail=True,url='https://otsocycles.com/products/mythology-nalgene-bottle-32oz',img=json.load(u.urlopen(u.Request('https://otsocycles.com/products/mythology-nalgene-bottle-32oz.json',headers={'User-Agent':'Mozilla/5.0'})))['product']['images'][0]['src'],note=''))
N.append(dict(brand='Gumtree Golf & Nature Club',title='NY Branches Nalgene (at Soft Hands Club)',price=29.70,cur='USD',avail=True,url='https://softhands.club/products/gumtree-golf-nature-club-ny-branches-widemouth-nalgene-water-bottle',img='https://cdn.shopify.com/s/files/1/0841/9020/0141/files/DSCF0975.webp?v=1771348184',note='Already in our 11 Water Bottles post'))
N.append(dict(brand='and wander × Yu Nagaba',title='Printed Bottle Clear (Maple Store AU)',price=95,cur='AUD',avail=True,url='https://maplestore.com.au/products/yu-nagaba-printed-bottle-clear',img=json.load(u.urlopen(u.Request('https://maplestore.com.au/products/yu-nagaba-printed-bottle-clear.json',headers={'User-Agent':'Mozilla/5.0'})))['product']['images'][0]['src'],note='Splurge; ships from Australia'))
H=[h for h in H if h['avail']]
json.dump({'hats':H,'nalgenes':N},open('opts.json','w'),indent=1)
print(len(H),len(N))
for i,h in enumerate(H,1): print('H',i,h['brand'],'|',h['title'],'|',h['cur'],h['price'])
for i,h in enumerate(N,1): print('N',i,h['brand'],'|',h['title'],'|',h['cur'],h['price'],h['avail'])
