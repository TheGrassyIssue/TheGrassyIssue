"""Public Drip revisit frames. 22 Oct 2026. Multi-colorway cards: first image of each colorway (max 6); single products: up to 4 images.
White packshots: tight crop + flood to stone; else cover crop. Lifestyle -> life-N.jpg."""
import json,os,urllib.request,numpy as np
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor
R='research/publicdrip-revisit/';O='images/publicdrip-revisit/';W,H=1000,1250;STONE=np.array([232,226,214.])
d={p['handle']:p for p in json.load(open(R+'products.json'))['products']}
CARDS={'a1':['pa-ls-mock-neck-akashi-kama-coffee'],'a2':['swing-vest-patchwork'],'a3':['swing-vest-sharkskin'],
'n1':['triborough-waffle-knit-polo-coffee','triborough-waffle-knit-polo-dark-slate','triborough-waffle-knit-polo-black','triborough-waffle-knit-polo-navy'],
'n2':['the-herringbone-half-zip-coffee','the-herringbone-half-zip'],'n3':['public-athlete-long-sleeve-mock-coffee','public-athlete-long-sleeve-mock-cream'],
'n4':['anywhere-pleated-pants-pinstripe','anywhere-pleated-pants-charcoal','anywhere-pleated-pants-sand','anywhere-pleated-pants-black','anywhere-pleated-pants'],
'n5':['p-script-denim-snapback-indigo'],'n6':['p-script-denim-bucket-indigo'],'n7':['3-pack-drip-marker'],
'c1':['public-athlete-polo-coffee','public-athlete-polo-pine-grove','public-athlete-polo-cream','public-athlete-polo-white','public-athlete-polo-storm','public-athlete-polo-olive'],
'c2':['public-athlete-blade-polo-cream','public-athlete-blade-polo-slate','public-athlete-blade-polo-sage'],
'c3':['public-athlete-striped-polo-olive-cream','public-athlete-striped-polo-storm-white'],'c4':['dinner-polo'],
'c5':['swing-shirt-green','swing-shirt-cream','swing-shirt-black'],'c6':['anywhere-tech-short-olive','anywhere-tech-short-black'],
'h1':['p-script-nylon-snapback-sand','p-script-nylon-snapback-pine-grove','p-script-nylon-snapback-white','p-script-nylon-snapback'],
'h2':['script-nylon-bucket-hat-black','script-nylon-bucket-hat-pine-grove','script-nylon-bucket-hat-sand','script-nylon-bucket-hat-white'],
'h3':['script-driver-cover-whiskey','script-driver-cover-green','script-driver-cover-black'],
'p1':['public-athlete-up-down-polo'],'p2':['public-athlete-frequency-polo'],'p3':['public-athlete-retro-polo'],'p4':['public-athlete-drip-stripe-polo'],
'p5':['public-athlete-camo-polo'],'p6':['public-athlete-tonal-polo-black','public-athlete-tonal-polo-navy'],'p7':['public-athlete-knit-polo-ochre','public-athlete-knit-polo-green','public-athlete-knit-polo-navy'],
'l1':['public-athlete-mock-neck-cream','public-athlete-mock-neck-pine-grove'],'l2':['public-athlete-rugby-navy-gold','public-athlete-rugby-navy-red'],'l3':['elevated-tee-green','elevated-tee-cream','elevated-tee-black'],
'b1':['anywhere-p-script-cord-shorts-navy'],'h4':['public-drip-classic-baseball-cap-sand','public-drip-classic-baseball-cap-navy','public-drip-baseball-cap-forest-green','public-drip-baseball-cap-black'],
'h5':['copy-of-copy-of-p-script-classic-hat-sand'],'h6':['fore-all-nylon-snapback-black'],'h7':['p-script-applique-bucketwhite','p-script-applique-bucketblack'],'x1':['public-athlete-crew-sock-cream']}
def frame(src,th=24,force=False):
    a=np.asarray(src).astype(float)
    cc=np.concatenate([a[:12,:12].reshape(-1,3),a[:12,-12:].reshape(-1,3),a[-12:,:12].reshape(-1,3),a[-12:,-12:].reshape(-1,3)])
    if not force and (cc.min()<190 or cc.std()>10):   # not a flat light studio backdrop (grey or white): cover crop
        s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
    col=np.median(np.concatenate([a[:8,:8].reshape(-1,3),a[:8,-8:].reshape(-1,3),a[-8:,:8].reshape(-1,3),a[-8:,-8:].reshape(-1,3)]),axis=0)
    dd=np.abs(a-col).max(axis=2)
    mk=Image.fromarray(((dd<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=(STONE if force else np.clip(a/np.maximum(col,1)*STONE,0,255)[bg])
    ys,xs=np.where(~bg)
    if len(xs)<100: return frame_cover(src)
    x0,x1=np.percentile(xs,[.3,99.7]).astype(int); y0,y1=np.percentile(ys,[.3,99.7]).astype(int)
    m=int(.06*max(x1-x0,y1-y0)); x0,y0=max(0,x0-m),max(0,y0-m); x1,y1=min(src.width,x1+m),min(src.height,y1+m)
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1,y1)); s=min(W*.78/g.width,H*.72/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
def frame_cover(src):
    s=max(W/src.width,H/src.height); im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS); x=(im.width-W)//2;y=(im.height-H)//2; return im.crop((x,y,x+W,y+H))
TH={'n5':(48,True),'n6':(48,True)}
jobs=[]
for k,hs in CARDS.items():
    srcs=[(h,0) for h in hs[:6]] if len(hs)>1 else [(hs[0],i) for i in range(min(4,len(d[hs[0]]['images'])))]
    for j,(h,i) in enumerate(srcs,1): jobs.append((k,j,h,i,d[h]['images'][i]['src'].split('?')[0]))
def get(job):
    k,j,h,i,u=job;fn=f'{R}raw/{h}-{i}.img'
    if not os.path.exists(fn): open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(u+'?width=1600',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
with ThreadPoolExecutor(8) as ex: list(ex.map(get,jobs))
fr={}
for k,j,h,i,u in jobs:
    out=f'{O}{k}-{j}.jpg';frame(Image.open(f'{R}raw/{h}-{i}.img').convert('RGB'),*TH.get(k,(24,False))).save(out,quality=84,optimize=True);fr.setdefault(k,[]).append('/'+out)
SITE=[l.strip() for l in open(R+'site/list.txt')]
for i in [8,9,10,11,12,13,14,15,16,17,18,19,20,25,26,30,31,63,64,97,99]:
    im=Image.open(f'{R}site/s{i}.img').convert('RGB'); im.thumbnail((1600,1600)); im.save(f'{O}site-{i}.jpg',quality=86,optimize=True)
for n in range(1,16):
    im=Image.open(f'{R}life/life-{n}.jpg').convert('RGB');im.save(f'{O}life-{n}.jpg',quality=84,optimize=True)
json.dump(fr,open(R+'frames.json','w'),indent=1);json.dump(CARDS,open(R+'cards.json','w'),indent=1)
print({k:len(v) for k,v in fr.items()})
