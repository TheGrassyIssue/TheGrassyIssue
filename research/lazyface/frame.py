"""Frames for the Lazyface Brand to Know (13 Oct 2026). Lazyface's own photos: products shot on a green sweep (no white
backgrounds to fix), plus its lifestyle shots. Hero = the wide grass/towel lifestyle shot."""
import json,glob
from PIL import Image
R='research/lazyface/raw/'; O='images/lazyface/'; W,H=1000,1250
exec(open('research/lazyface/catalog.py').read())
EXTRA={"facescreen":["life-4.png"],"facestick":["life-3.jpg"]}
def cover(im,py=.4):
    s=max(W/im.width,H/im.height); im=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*py); return im.crop((x,y,x+W,y+H))
fr={}
for h,*_ in P:
    files=sorted(glob.glob(f'{R}{h}-*'))+[R+e for e in EXTRA.get(h,[])]
    fr[h]=[]
    for n,f in enumerate(files,1):
        out=f'{O}{h}-{n}.jpg'; cover(Image.open(f).convert('RGB'),.45).save(out,quality=86); fr[h].append('/'+out)
json.dump(fr,open('research/lazyface/frames.json','w'),indent=1)
im=Image.open(R+'life-2.jpg').convert('RGB')
def band(w,h,py):
    s=max(w/im.width,h/im.height); r=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS); y=int((r.height-h)*py); x=(r.width-w)//2; return r.crop((x,y,x+w,y+h))
band(2000,857,.5).save(O+'btk-hero.jpg',quality=88); band(1200,630,.5).save(O+'btk-og.jpg',quality=88)
cover(Image.open(R+'life-4.png').convert('RGB'),.4).save(O+'card-hero.jpg',quality=86)
print({k:len(v) for k,v in fr.items()})
