"""Golf video games frames: official screenshots, 16:9 at 1600x900. 30 Oct 2026."""
import json
from PIL import Image
R='research/golf-games/raw/'; O='images/best-golf-video-games/'
def cover(im,w,h,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
F={'pga2k25':[1,0,2,3],'eapga':[0,3,1,2],'golfplus':[0,1,2],'hotshots':[0,1,2],'easy':[1,0,2],'superrush':[0,1,3,2],'switchsports':[0,1,2],
   'normal':[4,0,1,2,3],'cursed':[0,1,2,3],'wasteland':[0,1,2,3],'wtg':[0,1,2],'battle':[0,1,2,3],'gwyf':[0,1,2],'walkabout':[1,0,2,3]}
FR={}
for k,ix in F.items():
    FR[k]=[]
    for j,i in enumerate(ix,1):
        im=Image.open(f'{R}{k}-{i}').convert('RGB'); o=f'{O}{k}-{j}.jpg'
        cover(im,1600,900).save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/golf-games/frames.json','w'),indent=1)
h=Image.open(R+'eapga-3').convert('RGB')
cover(h,2000,857,.5,.55).save(O+'hero.jpg',quality=86,optimize=True)
cover(h,1200,630,.5,.5).save(O+'og.jpg',quality=84)
cover(Image.open(R+'walkabout-0').convert('RGB'),1000,1250,.42,.5).save(O+'card-hero.jpg',quality=84,optimize=True)
cover(Image.open(R+'normal-4').convert('RGB'),1000,1250,.35,.5).save(O+'card-normal.jpg',quality=84,optimize=True)
cover(Image.open(R+'battle-0').convert('RGB'),1000,1250,.4,.5).save(O+'card-battle.jpg',quality=84,optimize=True)
cover(Image.open(R+'pga2k25-1').convert('RGB'),1000,1250,.45,.5).save(O+'card-2k25.jpg',quality=84,optimize=True)
print({k:len(v) for k,v in FR.items()})
