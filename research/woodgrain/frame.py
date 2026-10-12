"""Frame Woodgrain Golf images into 1000x1250 gallery frames + hero/bands/og. 12 October 2026.
Galleries lead with full-length on-model shots; tight waist/crotch crops are left out (house rule)."""
import json,numpy as np
from PIL import Image
R='research/woodgrain/raw/'; O='images/woodgrain/'
SEL={"relaxed-double-pleated-trouser":["1","4","2","5"],"relaxed-double-pleated-trouser-tan":["1","4","3","2"],
"relaxed-double-pleated-trouser-chocolate-brown":["1","2","3","5"],"relaxed-double-pleated-trouser-black":["L:CE941515-DB43-4F47-AFB8-024D97762193_1_105_c.jpg","0","1"],
"the-double-pleated-short-cream":["1","2"],"the-double-pleated-short-tan":["1","2","3","4"],
"the-double-pleated-short-cream-copy":["1","5","3"],"the-double-pleated-short-black":["1","3","4"],
"the-cable-knit-sweater-vest-black":["1","0","3"],"the-cable-knit-sweater-vest-black-copy":["1","2","3","0"],
"nylon-vest-tan":["1","5","0","3"],"script-hat":["1","3","4","7"],"script-hat-copy":["1","2","5","0"],"wool-hat":["5","0","3"]}
W,H=1000,1250; fr={}
def frame(im,pos=.3):
    g=np.asarray(im.convert('L')).astype(int); cols=np.where(g.mean(axis=0)>10)[0]
    if len(cols) and (cols[0]>4 or cols[-1]<im.width-5): im=im.crop((cols[0],0,cols[-1]+1,im.height))  # trim black letterbox bars
    a=np.asarray(im).astype(int); border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if border.std(axis=0).max()<12 and abs(im.width/im.height-.8)>.02:
        col=tuple(int(x) for x in np.median(border,axis=0)); s=min(W*.9/im.width,H*.9/im.height)
        im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2)); return c
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
def src(h,k): return R+('life-'+k[2:] if k.startswith('L:') else f'{h}-{k}.jpg')
for h,idx in SEL.items():
    fr[h]=[]
    for n,k in enumerate(idx,1):
        c=frame(Image.open(src(h,k)).convert('RGB'),.2); out=f'{O}{h}-{n}.jpg'; c.save(out,quality=86); fr[h].append('/'+out)
json.dump(fr,open('research/woodgrain/frames.json','w'),indent=1)
def panel(f,w,h,pos=.25):
    im=Image.open(R+f).convert('RGB'); g=np.asarray(im.convert('L')).astype(int); cols=np.where(g.mean(axis=0)>10)[0]; im=im.crop((cols[0],0,cols[-1]+1,im.height)); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-w)//2; y=int((im.height-h)*pos); return im.crop((x,y,x+w,y+h))
def tri(files,W2,H2,gap,pos=.15):
    pw=(W2-2*gap)//3; c=Image.new('RGB',(W2,H2),(24,40,23))
    for i,f in enumerate(files): c.paste(panel(f,pw,H2,pos),(i*(pw+gap),0))
    return c
T=['the-cable-knit-sweater-vest-black-1.jpg','nylon-vest-tan-1.jpg','the-cable-knit-sweater-vest-black-copy-1.jpg']  # Lenny picked option B, 12 Oct
tri(T,2000,857,8).save(O+'btk-hero.jpg',quality=88)
tri(T,1200,630,6).save(O+'btk-og.jpg',quality=88)
for n,(f,pos) in enumerate([('the-double-pleated-short-cream-4.jpg',.3),('life-2_251a2b6f-1bfa-4aa6-8554-4419f64f6264.png',.3),('life-1EF8DD3E-D2DC-47F9-B974-A76710E9303E_1_105_c.jpg',.3),
   ('nylon-vest-tan-2.jpg',.2),('script-hat-2.jpg',.2),('wool-hat-4.jpg',.2)],1):
    frame(Image.open(R+f).convert('RGB'),pos).save(f'{O}band-{n}.jpg',quality=86)
frame(Image.open(R+'relaxed-double-pleated-trouser-tan-1.jpg').convert('RGB'),.2).save(O+'card-hero.jpg',quality=86)
print(sum(map(len,fr.values())))
