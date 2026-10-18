import json,re
o=json.load(open('opts.json'))
old=o['hats']
keep=[h for h in old if h['brand']=='Draw']+[old[34]]  # Draw + H35 Canto
for h in keep: h['note']='Your pick'
def shop(store,pat,brand,cur='USD',note='',n=1):
    out=[]
    for p in json.load(open(f'stores/{store}.json')):
        if re.search(pat,p['title'],re.I):
            av=[v for v in p['variants'] if v['available']]
            if not av: continue
            out.append(dict(brand=brand,title=p['title'],price=float(av[0]['price']),cur=cur,avail=True,url=f"https://{store.replace('www.','www.')}/products/{p['handle']}",img=p['images'][0]['src'] if p['images'] else '',note=note))
    return out[:n]
new=[]
new+=shop('canto.json'.replace('.json',''),'x',"x") if False else []
cj=json.load(open('stores/canto.json'))
for p in cj:
    if p['name'] in ('Cyco Vision New Era 59FIFTY - Brown','Dogpound Snapback - Desert Camo'):
        new.append(dict(brand='Canto',title=p['name'],price=float(p['price']),cur='USD',avail=True,url='https://www.canto.vision/product/'+p['permalink'],img=p['images'][0]['url'],note=''))
new+=shop('quietgolf.com','Monogram Nylon Dad Hat','Quiet Golf')
new+=shop('quietgolf.com','QG Flag Cotton Dad Hat','Quiet Golf')
new+=shop('www.mogshadegolf.com','Only Human Cap','Mogshade','EUR')
new+=shop('kingfisher-golf.com','Sage Green DAL Cap','Kingfisher Golf')
new+=shop('kingfisher-golf.com','Powder Blue DAL Hat','Kingfisher Golf')
new+=shop('www.fordengolf.com','Brown Forden x New Era Golfer Snapback','Forden Golf')
new+=shop('lofgolf.com','Duckbill Birds Cap Navy/Cream','Left of Field','AUD')
new+=shop('lofgolf.com','Heritage Plaid Cap Red','Left of Field','AUD')
new+=shop('radmorgolf.com','Corduroy Script Cap','Radmor')
new+=shop('ebbets.com','Tokyo Giants Wool Mesh Trucker','Ebbets Field Flannels')
new+=shop('ebbets.com','Santurce Wool Mesh Trucker','Ebbets Field Flannels')
new+=shop('battenwear.com','Club Cap / Acorn Corduroy','Battenwear')
new+=shop('fandco.co.nz','Vintage Cord Cap - Short Brim 5 Panel - Green','F and Co.','AUD')
new+=shop('seamusgolf.com','Seamus Vintage Patch Two-Tone','Seamus')
new+=shop('whimgolf.com','Forest Green Embroidered Hat','Whim')
new+=shop('sugarloafsocialclub.com','Runner Cap','Sugarloaf Social Club')
new+=shop('munikids.com','Thank You Anthony Kim','Muni Kids')
new+=shop('mustardbeetle.com','Ball Cap: Quail','Mustard Beetle')
new+=shop('hikerdelic.com','Sol Cap Olive','Hikerdelic','GBP')
new+=shop('howlerbros.com','ACL Fest 2026 Snapback - Midnight Corduroy','Howler Bros',note='Austin')
new+=shop('topodesigns.com','New Belgium Brewing Corduroy Trucker','Topo Designs')
for x in new: print(x['brand'],'|',x['title'],'|',x['cur'],x['price'])
o['hats2']=keep+new; json.dump(o,open('opts.json','w'),indent=1); print(len(keep),len(new))
