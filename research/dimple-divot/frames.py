import os,json,re,io,statistics,urllib.request
from PIL import Image, ImageOps
C={x['handle']:x for x in json.load(open('research/dimple-divot/catalog.json'))['items']}
L=json.load(open('research/dimple-divot/irl/log.json'))
OUT='images/dimple-divot'; os.makedirs(OUT,exist_ok=True)
def base(u): return re.sub(r'\?.*','',u).split('/')[-1]
IRL={'hero':8,'founder':7,'band-a1':1,'band-a2':2,'band-a3':0,'band-b1':19,'band-b2':25,'band-b3':24,'band-c1':43,'band-c2':45,'band-c3':46,'band-d1':26,'band-d2':29,'band-d3':33}
USED={base(L[i]['key']) for i in IRL.values()}
PICKS=['carved-hickory-golf-brush','hickory-golf-brush-highland','hickory-golf-brush-murphy','hickory-golf-brush-pro-hybrid-green','hickory-golf-brush-mini-grass',
       'clay-pigeon-ballmarker','every-round-carry-divot-tool','fleece-reversible-headcover-driver','essentials-pouch-rust','d-d-icon-dad-hat-olive','d-d-fall-tees-50-ct','infinity-leather-valet-tray']
def uniform(im):
    s=im.convert('RGB').resize((64,80)); px=s.load(); W,H=s.size
    e=[px[x,0] for x in range(W)]+[px[x,H-1] for x in range(W)]+[px[0,y] for y in range(H)]+[px[W-1,y] for y in range(H)]
    return sum(statistics.pstdev([c[i] for c in e]) for i in range(3))/3<10, tuple(int(statistics.median([c[i] for c in e])) for i in range(3))
def frame(im):
    im=ImageOps.exif_transpose(im).convert('RGB'); u,bg=uniform(im)
    if u:
        c=im.copy(); c.thumbnail((920,1150)); cv=Image.new('RGB',(1000,1250),bg); cv.paste(c,((1000-c.width)//2,(1250-c.height)//2)); return cv
    return ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.5))
def get(u):
    return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(re.sub(r'\?.*','',u)+'?width=2000',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()))
res={}
for h in PICKS:
    srcs=[u for u in C[h]['imgs'] if base(u) not in USED][:5]
    res[h]=[]
    for n,s in enumerate(srcs,1):
        p=f'{OUT}/{h}-{n}.jpg'
        try: frame(get(s)).save(p,quality=82,optimize=True,progressive=True); res[h].append(dict(local='/'+p,src=s))
        except Exception as e: print('fail',h,s[-40:],e)
for k,i in IRL.items():
    im=Image.open('research/dimple-divot/irl/'+L[i]['file']).convert('RGB')
    if k=='hero':
        ImageOps.fit(im,(1600,685),Image.LANCZOS,centering=(.5,.55)).save(f'{OUT}/hero.jpg',quality=84,optimize=True,progressive=True)
        ImageOps.fit(im,(1200,630),Image.LANCZOS,centering=(.5,.55)).save(f'{OUT}/og.jpg',quality=84)
        res['hero']=[dict(local=f'/{OUT}/hero.jpg',src=L[i]['key'],page=L[i]['page'])]; continue
    p=f'{OUT}/{k}.jpg'; ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.45)).save(p,quality=82,optimize=True,progressive=True)
    res[k]=[dict(local='/'+p,src=L[i]['key'],page=L[i]['page'])]
json.dump(res,open('research/dimple-divot/frames.json','w'),indent=1)
print({k:len(v) for k,v in res.items()})
