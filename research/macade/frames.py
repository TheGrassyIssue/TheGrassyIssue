import json,io,urllib.request,pathlib
from PIL import Image
R=pathlib.Path('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site')
d={p['handle']:p for p in json.load(open(R/'research/macade/products.json'))['products']}
H=["hydrocore-rain-jacket-green","hydrocore-rain-trousers-green","storm-wind-shirt-dark-blue","arcweave-gilet-ashwood","black-tx-links-windbreaker",
"flow-light-knit-hoodie-pine","flow-light-bomber-neck-camel","theo-knit-polo-sweater-grey-melange","club-knit-polo-rust","airlite-henley-sweater-navy","tx-intarsia-knit-crewneck-rust",
"clayton-core-shirt-green","brooks-wayline-shirt-dark-green","flight-green-palm-shirt","arcweave-trouser-bone","lightweight-tapered-trouser-stone-blue",
"green-cashmere-blend-course-beanie","dark-green-tour-belt","black-rope-course-snapback"]
def get(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}); return Image.open(io.BytesIO(urllib.request.urlopen(req,timeout=30).read())).convert('RGB')
def frame(im):
    w,h=im.size; cw=min(w,int(h*.8)); ch=int(cw*1.25)
    if ch>h: ch=h; cw=int(h*.8)
    x=(w-cw)//2; y=(h-ch)//2; im=im.crop((x,y,x+cw,y+ch))
    return im.resize((1000,1250),Image.LANCZOS) if im.width>1000 else im
FR={}
for h in H:
    FR[h]=[]
    for j,img in enumerate(d[h]['images'][:4]):
        u=img['src']+('&' if '?' in img['src'] else '?')+'width=1600'
        try:
            im=frame(get(u)); p=f'images/macade/{h}-{j+1}.jpg'; im.save(R/p,quality=84,optimize=True); FR[h].append({'local':'/'+p,'src':img['src']})
        except Exception as e: print('fail',h,j,e)
    print(h,len(FR[h]))
json.dump(FR,open(R/'research/macade/frames.json','w'),indent=1)
