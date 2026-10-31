"""Austin work spots frames (venue-site photos), 16:9 at 1200x675. 31 Oct 2026."""
import json
from PIL import Image
R='research/work-spots-atx/raw/'; O='images/austin-work-spots/'
def cover(im,w,h,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
F={'library':['austin-central-library-2','austin-central-library-0'],'carpenter':['carpenter-coffee-bar-1','carpenter-coffee-bar-0','carpenter-coffee-bar-2'],
 'alfred':['line-alfred-1','line-alfred-0','line-alfred-2'],'brewbrew':['brew-and-brew-0','brew-and-brew-2','brew-and-brew-1'],
 'radio':['radio-a3','radio-a2','radio','radio-a4'],'leona':['leona','leona-a2','leona-a3'],'spokesman':['spokesman-south-1','spokesman-south-0'],
 'saten':['sa-ten-canopy-1','sa-ten-canopy-0','sa-ten-canopy-2'],'medici':['medici-springdale-0','medici-springdale-2'],
 'spread':['spread-and-co-cherrywood-1','spread-and-co-cherrywood-0','spread-and-co-cherrywood-2'],'palomino':['palomino-airport-1','palomino-airport-0','palomino-airport-2'],
 'createscape':['createscape-0','createscape-1','createscape-2'],'strangelove':['strangelove-0','strangelove-1'],
 'flightpath':['flightpath-2','flightpath-0','flightpath-1','flightpath-3'],'hanks':['hanks-0','hanks-1','hanks-2']}
FR={}
for k,fs in F.items():
    FR[k]=[]
    for j,f in enumerate(fs,1):
        o=f'{O}{k}-{j}.jpg'; cover(Image.open(R+f).convert('RGB'),1200,675).save(o,quality=86,optimize=True); FR[k].append('/'+o)
json.dump(FR,open('research/work-spots-atx/frames.json','w'),indent=1)
h=Image.open(R+'flightpath-2').convert('RGB')
cover(h,2000,857,.5,.5).save(O+'hero.jpg',quality=86,optimize=True); cover(h,1200,630).save(O+'og.jpg',quality=84)
cover(Image.open(R+'carpenter-coffee-bar-1').convert('RGB'),1000,1250,.45,.5).save(O+'card-hero.jpg',quality=84,optimize=True)
print({k:len(v) for k,v in FR.items()})
