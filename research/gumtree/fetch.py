import json,urllib.request,time
UA={'User-Agent':'Mozilla/5.0 (Macintosh) Chrome/124'}
def get(u): return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read())
items={};url='https://www.gumtreegolfandnature.com/shop?format=json'
n=0
while url and n<40:
    d=get(url); n+=1
    for it in d.get('items',[]): items[it['id']]=it
    pg=d.get('pagination',{})
    url=('https://www.gumtreegolfandnature.com'+pg['nextPageUrl']+'&format=json') if pg.get('nextPage') else None
json.dump(list(items.values()),open('items.json','w'))
print(len(items),n)
