"""Frame No Dirt Golf store images into 1000x1250 gallery frames + hero/bands/og. 11 October 2026."""
import json,numpy as np
from PIL import Image
R='research/no-dirt-golf/raw/'; O='images/no-dirt-golf/'
SEL={"the-ultimate-caddy-towel-vaspar":[0,1],"the-ultimate-caddy-towel-dutch-boy":[0,1],
"the-ultimate-caddy-towel-white-burgundy-and-yellow-stripes":[0,1],"the-ultimate-caddy-towel-burgundry-silver-stripes":[0,1],
"the-ultimate-caddy-towel-green-white-stripe":[0,1],"the-ultimate-caddy-towel-navy-white-stripe":[0,1],
"the-classic-forest-green":[0,3,4,2],"the-classic-navy":[0,4,3,2],"the-classic-irish-mint":[0,1,3,4],
"magnet-towel-dark-green":[0],"magnet-towel-navy":[0],"the-r-green":[1,0,2]}
W,H=1000,1250; fr={}
def frame(im,pos=.5):
    a=np.asarray(im).astype(int); border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if border.std(axis=0).max()<12:
        col=tuple(int(x) for x in np.median(border,axis=0)); s=min(W*.9/im.width,H*.9/im.height)
        im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2)); return c
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
for h,idx in SEL.items():
    fr[h]=[]
    for k,i in enumerate(idx,1):
        c=frame(Image.open(f'{R}{h}-{i}.jpg').convert('RGB'),.2)
        out=f'{O}{h.replace("the-ultimate-caddy-towel-","uc-")}-{k}.jpg'; c.save(out,quality=86); fr[h].append('/'+out)
json.dump(fr,open('research/no-dirt-golf/frames.json','w'),indent=1)
# hero 2000x857 from the new-caddy banner
b=Image.open(R+'nodirt-newcady-banner.png').convert('RGB'); th=int(b.width*857/2000); y=min(b.height-th,int((b.height-th)*.55))
b.crop((0,y,b.width,y+th)).resize((2000,857),Image.LANCZOS).save(O+'btk-hero.jpg',quality=88)
og=Image.open(R+'nodirt-newcady-banner.png').convert('RGB'); th=int(og.width*630/1200); y=(og.height-th)//2
og.crop((0,y,og.width,y+th)).resize((1200,630),Image.LANCZOS).save(O+'btk-og.jpg',quality=88)
for n,(f,pos) in enumerate([('Caddie_Holding_Pin_Green.jpg',0),('Grey_Towel_Beach_Background.jpg',.5),('Blue_Towel_NDG_Tag_on_Grass.jpg',.5),
  ('Bandon_Dunes_White-1.jpg',.5),('National_Golf_Links_of_America-1.jpg',.5),('Sheeps_Ranch-1.jpg',.5)],1):
    frame(Image.open(R+f).convert('RGB'),pos).save(f'{O}band-{n}.jpg',quality=86)
frame(Image.open(R+'new-colors-highlight.jpg').convert('RGB')).save(O+'card-hero.jpg',quality=86)
print(sum(map(len,fr.values())))
# No stark white backgrounds (Lenny, 12 Oct)
import glob as _g, sys as _s; _s.path.insert(0,'.')
from destark import destark
LIGHT=('uc-white-burgundy-and-yellow-stripes','uc-dutch-boy','band-4','band-6','card-hero')
n=sum(destark(f, light=any(k in f for k in LIGHT), min_white=0.15) for f in _g.glob(O+'*.jpg') if not f.endswith(('btk-hero.jpg','btk-og.jpg')))
print('destarked',n)
