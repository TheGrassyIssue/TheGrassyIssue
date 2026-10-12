"""Frames for the three-brand On Our Radar post. 12 October 2026.
Three Putt galleries use flat/back-print shots only (several of the brand's on-model photos look AI-generated)."""
import json,glob,numpy as np
from PIL import Image
R='research/radar-three/raw/'; O='images/radar-three/'
SEL={1:[0,3,5,6],8:[4,3,6,2],9:[9,8,13,3],10:[2,4,12,0],11:[1,11,13,0],17:[3,6,8,2],24:[3,1,2,4],
25:[0,1,2,3],29:[0,1,2],31:[0,1,2],32:[0,1,2],36:[0,1,2],45:[0,1,2],46:[0,1,2],
66:[1,0,2],67:[1,0,2],70:[1,3,0,2],74:[1,0,3,2],80:[1,3,0,4,5],92:[1,3,0,2],95:[1,0,2,3]}
W,H=1000,1250
def trim(im):
    g=np.asarray(im.convert('L')).astype(int); cols=np.where(g.mean(axis=0)>10)[0]
    return im.crop((cols[0],0,cols[-1]+1,im.height)) if len(cols) and (cols[0]>4 or cols[-1]<im.width-5) else im
def frame(im,pos=.2):
    im=trim(im); a=np.asarray(im).astype(int); border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if border.std(axis=0).max()<14 and abs(im.width/im.height-.8)>.02:
        col=tuple(int(x) for x in np.median(border,axis=0)); s=min(W*.9/im.width,H*.9/im.height)
        im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2)); return c
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
def raw(n,i): return glob.glob(f'{R}{n:03d}-*-{i}.jpg')[0]
fr={}
for n,idx in SEL.items():
    fr[n]=[]
    for k,i in enumerate(idx,1):
        out=f'{O}p{n:03d}-{k}.jpg'; frame(Image.open(raw(n,i)).convert('RGB')).save(out,quality=86); fr[n].append('/'+out)
json.dump(fr,open('research/radar-three/frames.json','w'),indent=1)
def panel(f,w,h,pos=.2):
    im=trim(Image.open(f).convert('RGB')); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-w)//2; y=int((im.height-h)*pos); return im.crop((x,y,x+w,y+h))
def tri(files,W2,H2,gap,pos):
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for i,(f,p) in enumerate(zip(files,pos)): c.paste(panel(f,pw,H2,p),(i*(pw+gap),0))
    return c
# Hero: lifestyle trio picked by Lenny (option C with the buggy in the centre), 12 Oct
def lpanel(f,w,h,py,px):
    im=Image.open('research/radar-three/life/'+f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
# Hero: one lifestyle photo per brand, in post order (Lenny, 12 Oct: "the group of three", no buggy)
HERO=[('tp-Happy_Place_Front_6.png',.5,.88),('tg-instagram-vest-back.png',.3,.5),('rb-Ajuar_Rebolf_ShootingHype__19.jpg',.5,.36)]
for (W2,H2,gap,name) in [(2000,857,8,'hero.jpg'),(1200,630,6,'og.jpg')]:
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for k,(f,py,px) in enumerate(HERO): c.paste(lpanel(f,pw,H2,py,px),(k*(pw+gap),0))
    c.save(O+name,quality=88)
frame(Image.open(raw(74,1)).convert('RGB')).save(O+'card.jpg',quality=86)
print(sum(map(len,fr.values())))
# Lifestyle bands (added 12 Oct after Lenny: "add a bunch of lifestyle pics")
L='research/radar-three/life/'
BANDS=[('tp-TP_About_Me.png',.5,.5),('tp-TP_About_Me_3.png',.5,.25),('tp-tee-time-back.jpg',.35,.5),
 ('tg-instagram-vest-back.png',.3,.5),('tg-Tarraing-golf-hats.jpg',.5,.03),('tg-Tarraing-white-blue-polo-folded.jpg',.5,.5),  # IG shot supplied by Lenny 12 Oct

 ('rb-34.jpg',.2,.5),('rb-Look8.jpg',.2,.5),('rb-foto_buggy_volcado_e2ad904e-f045-4a80-aa',.5,.62),
 ('rb-69.jpg',.2,.5),('rb-73.jpg',.2,.5),('rb-14.jpg',.2,.5)]
def fcrop(f,py,px):
    im=Image.open(L+f).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=int((im.width-W)*px); y=int((im.height-H)*py); return im.crop((x,y,x+W,y+H))
for n,(f,py,px) in enumerate(BANDS,1): fcrop(f,py,px).save(f'{O}band-{n}.jpg',quality=86)
# No stark white backgrounds (Lenny, 12 Oct): Three Putt packshots sit on pure white; flood that backdrop with a warm stone tone.
# Multiply-blend inside a slightly dilated mask so anti-aliased garment edges don't leave a white halo.
from PIL import ImageDraw, ImageFilter
STONE=np.array([232,226,214],float)
def destark(path):
    im=Image.open(path).convert('RGB'); a=np.asarray(im).astype(float); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if b.mean(axis=0).min()<=250: return False
    w,h=im.size; probe=im.copy()
    for s_ in [(x,y) for x in range(0,w,20) for y in (0,h-1)]+[(x,y) for y in range(0,h,20) for x in (0,w-1)]:
        if min(probe.getpixel(s_))>=240: ImageDraw.floodfill(probe,s_,(255,0,255),thresh=(20 if 'p024-4' in path else 34))
    pa=np.asarray(probe); m=((pa[...,0]==255)&(pa[...,1]==0)&(pa[...,2]==255)).astype('uint8')*255
    light = path.endswith(('p024-4.jpg','p001-2.jpg','p008-3.jpg','p017-3.jpg'))  # white tee, cream sweatshirt: keep a tight mask
    m=np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(13 if light else 41)).filter(ImageFilter.GaussianBlur(2))).astype(float)[...,None]/255
    if not light:  # soft drop-shadow halo: tint by brightness so dark garments are untouched
        lum=np.asarray(im.convert('L')).astype(float)[...,None]
        m=m*np.clip((lum-150)/60,0,1)
    out=a*(1-m)+(a*STONE/255)*m
    Image.fromarray(out.clip(0,255).astype('uint8')).save(path,quality=86); return True
import glob as _g
n=sum(destark(f) for f in _g.glob(O+'p0[0-2]*.jpg')+_g.glob(O+'band-*.jpg'))
print('destarked',n)
