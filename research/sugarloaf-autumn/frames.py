import os,json,re,io,statistics,urllib.request
from PIL import Image, ImageOps
I=json.load(open('research/sugarloaf-autumn/images.json')); L=json.load(open('research/sugarloaf-autumn/cand/log.json'))
OUT='images/sugarloaf-autumn'; os.makedirs(OUT,exist_ok=True)
def base(u): return re.sub(r'\?.*','',u).split('/')[-1]
BAND={'b1':9,'b2':6,'b3':3,'b4':15,'b5':17,'b6':26}
EXCL={base(L[i]['src']) for i in BAND.values()}|{'I1070653.jpg'}
def block(h,col):
    im=I[h]; st=next((n for n,x in enumerate(im) if col in x['colours']),None)
    if st is None: return [x['src'] for x in im]
    out=[im[st]['src']]
    for x in im[st+1:]:
        if x['colours']: break
        out.append(x['src'])
    return out
P={'jacket-green':('ssc-tech-jacket','Glow Green',[0,1,2,5]),'jacket-navy':('ssc-tech-jacket','Navy',[0,1,5,6,8]),
   'windcrew-stone':('windcrew','Stone',[0,1,4,6]),'windcrew-navy':('windcrew','Navy',[0,1,2,3]),
   'vest-red':('tech-vest-2026','Dark Red',[0,1,2,5]),'vest-navy':('tech-vest-2026','Navy',[0,1,2,5]),
   'windshirt':('windshirt','Stone/Navy',[0,1,2,3]),'bigarrow':('big-arrow-cover','Driver',[0,1,2,3]),
   'polo-spruce':('the-club-stripe-polo','Spruce Green',[0,1,4,5,6]),
   'mallet':('hidden-gem-mallet-putter-cover',None,[0,1,2,3]),'blade':('hidden-gem-blade-putter-cover',None,[0,1,2,3,4])}
def uniform(im):
    s=im.convert('RGB').resize((64,80)); px=s.load(); W,H=s.size
    e=[px[x,0] for x in range(W)]+[px[x,H-1] for x in range(W)]+[px[0,y] for y in range(H)]+[px[W-1,y] for y in range(H)]
    return sum(statistics.pstdev([c[i] for c in e]) for i in range(3))/3<10, tuple(int(statistics.median([c[i] for c in e])) for i in range(3))
def frame(im):
    im=ImageOps.exif_transpose(im).convert('RGB'); u,bg=uniform(im)
    if u:
        c=im.copy(); c.thumbnail((920,1150)); cv=Image.new('RGB',(1000,1250),bg); cv.paste(c,((1000-c.width)//2,(1250-c.height)//2)); return cv
    return ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.4))
def get(u):
    u=('https:'+u) if u.startswith('//') else u
    return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(re.sub(r'\?.*','',u)+'?width=2000',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()))
res={}
for k,(h,col,idx) in P.items():
    b=block(h,col) if col else [x['src'] for x in I[h]]
    srcs=[b[i] for i in idx if i<len(b) and base(b[i]) not in EXCL]
    res[k]=[]
    for n,s in enumerate(srcs,1):
        p=f'{OUT}/{k}-{n}.jpg'; frame(get(s)).save(p,quality=82,optimize=True,progressive=True); res[k].append(dict(local='/'+p,src=s))
socks=[I['sock-3-pack'][0]['src']]+[x['src'] for x in I['sock-3-pack'][2:5]]
res['socks']=[]
for n,s in enumerate(socks,1):
    p=f'{OUT}/socks-{n}.jpg'; frame(get(s)).save(p,quality=82,optimize=True,progressive=True); res['socks'].append(dict(local='/'+p,src=s))
for k,i in BAND.items():
    im=Image.open('research/sugarloaf-autumn/cand/'+L[i]['file']).convert('RGB')
    p=f'{OUT}/band-{k}.jpg'; ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.4)).save(p,quality=82,optimize=True,progressive=True); res['band-'+k]=[dict(local='/'+p,src=L[i]['src'])]
json.dump(res,open('research/sugarloaf-autumn/frames.json','w'),indent=1)
print({k:len(v) for k,v in res.items()})
