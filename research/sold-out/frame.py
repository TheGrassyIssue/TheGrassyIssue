"""Sold-out gallery frames. 22 Oct 2026. Up to 3 images per piece -> 1000x1250. White packshots: tight crop + flood-to-stone; else cover."""
import json,os,io,glob,urllib.request,numpy as np
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor
Image.MAX_IMAGE_PIXELS=None
R='research/sold-out/'; O='images/sold-out/'; W,H=1000,1250; STONE=np.array([232,226,214.])
stores={}
def shop_imgs(dom,handle):
    for f in glob.glob(R+'stores/*.json'):
        d=stores.get(f) or json.load(open(f)); stores[f]=d
        if d['domain']==dom:
            for p in d['products']:
                if p['handle']==handle: return [i['src'].split('?')[0] for i in p['images']]
    return []
SQ=json.load(open(R+'sq-items.json'))
CL={'c1':['supreme-reworked-headcovers-3-1.jpg','supreme-reworked-headcover-1.jpg','supreme-reworked-mallet-headcover-1.jpg'],
    'c2':['palace-reworked-headcovers-1.jpg'],
    'c3':['reworked-louis-vuitton-headcovers-2-1.jpg','reworked-louis-vuitton-headcovers-1-1.jpg','reworked-louis-vuitton-scope-pouch-1-1.jpg']}
SH={'c4':('dormieworkshop.com','sherwood-x-dormie-debrincat-hockey-glove-teardown-headcover'),'c5':('matchstickgolf.com',None),'c6':('www.bluegrassfairway.com',None),'c7':('midiron.shop',None),
    'o1':('pirettigolf.com','workshop-tour-only-801-damascus-steel-putter-1-of-1'),'o2':('pirettigolf.com','workshop-dia-de-los-muertos-1-of-1-goat-303ss-w-ust-shaft'),
    'o3':('bettinardi.com',None),'o4':('bettinardi.com',None),'o5':('showoutengraving.com',None),'o6':('mackemgolf.com',None),'o7':('soundergolf.com',None),
    'u1':('malbon.com',None),'u2':('badlands1st.com',None),'u3':('www.seamusgolf.com',None),'u4':('www.manorsgolf.com',None),'u6':('www.mogshadegolf.com',None),'u7':('vesselgolf.com',None),
    'm6':('www.seamusgolf.com',None),'w1':('3puttround.com',None),'w2':('dimpledivot.com',None),'w3':('radry.com',None),'w4':('vesselgolf.com',None),'w5':('www.seamusgolf.com',None),'w7':('ghostgolf.com',None)}
P={x['n']:x for x in json.load(open(R+'picks3.json'))}
MAP={'c4':33,'c5':40,'c6':43,'c7':41,'o3':27,'o4':29,'o5':38,'o6':60,'o7':65,'u1':21,'u2':26,'u3':57,'u4':51,'u6':66,'u7':53,'m6':59,'w1':48,'w2':50,'w3':68,'w4':54,'w5':58,'w7':72}
SQM={'w6':'18','u5':'14','m1':'7','m2':'8','m3':'9','m4':'13','m5':'17','m7':'15'}
def srcs(k):
    if k in CL: return ['L:'+f for f in CL[k]]
    if k in SQM: return SQ[SQM[k]]['imgs'][:3]
    dom,h=SH[k]
    if h is None: h=P[MAP[k]]['url'].rstrip('/').split('/')[-1]
    return shop_imgs(dom,h)[:3]
KEYS=list(CL)+[k for k in SH if k not in CL]+list(SQM)
def frame(src):
    a=np.asarray(src).astype(float)
    if min(a[:8,:8].min(),a[:8,-8:].min(),a[-8:,:8].min(),a[-8:,-8:].min())<240:
        s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
    col=np.median(np.concatenate([a[:8,:8].reshape(-1,3),a[:8,-8:].reshape(-1,3),a[-8:,:8].reshape(-1,3),a[-8:,-8:].reshape(-1,3)]),axis=0)
    dd=np.abs(a-col).max(axis=2)
    mk=Image.fromarray(((dd<14)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=np.clip(a/np.maximum(col,1)*STONE,0,255)[bg]
    ys,xs=np.where(~bg)
    if len(xs)<100: return None
    x0,x1=np.percentile(xs,[.3,99.7]).astype(int); y0,y1=np.percentile(ys,[.3,99.7]).astype(int)
    m=int(.06*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.86/g.width,H*.8/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
def get(ku):
    k,i,u=ku; fn=f'{R}raw/{k}-{i}.img'
    if not os.path.exists(fn):
        if u.startswith('L:'): Image.open('images/clamp-golf/'+u[2:]).convert('RGB').save(fn,'JPEG',quality=95)
        else:
            uu=u.replace('http://','https://'); uu+=('?format=1500w' if 'squarespace' in uu else '?width=1600')
            open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(uu,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
    return fn
jobs=[(k,i,u) for k in KEYS for i,u in enumerate(srcs(k))]
with ThreadPoolExecutor(8) as ex: list(ex.map(get,jobs))
fr={}
for k,i,u in jobs:
    im=frame(Image.open(f'{R}raw/{k}-{i}.img').convert('RGB'))
    if im is None: continue
    out=f'{O}{k}-{i+1}.jpg'; im.save(out,quality=86); fr.setdefault(k,[]).append('/'+out)
json.dump(fr,open(R+'frames.json','w'),indent=1); print({k:len(v) for k,v in fr.items()})
