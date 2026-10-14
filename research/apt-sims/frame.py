"""Frames for "Austin apartments with golf simulators" (14 Oct 2026). Each property's own gallery photos (sel.json indices);
AMLI from its property page (prismic). Cover-crop to 1000x1250, 3:2 sources cropped from center."""
import json,subprocess,os
from PIL import Image
R='research/apt-sims/raw/'; O='images/austin-apartments-golf-sims/'; W,H=1000,1250
PICK={'alexan':[22,23,21,13],'colorado':[16,15,14,12],'odell':[16,20,15,0],'presidium':[14,2,0,1],'shiloh':[0,1,2,6],
 'bridge':[0,1,2,3],'parkest':[0,1,2,3],'viewest':[18,11,17,21],'howard':[17,0,23,12]}
AMLI=['https://images.prismic.io/amli-website/aMmm9GGNHVfTPSpR_northpark_amenity_golf_93.jpg','https://images.prismic.io/amli-website/aMmnAWGNHVfTPSpX_northpark_amenity_pool_125.jpg',
 'https://images.prismic.io/amli-website/aMmnBWGNHVfTPSpZ_northpark_amenity_patio_139.jpg','https://images.prismic.io/amli-website/aMmnA2GNHVfTPSpY_northpark_amenity_patio_134.jpg']
for i,u in enumerate(AMLI):
    f=f'{R}amli2-{i:02d}.img'
    if not os.path.exists(f): subprocess.run(['curl','-sL','-m','60','-o',f,u])
PICK['amli2']=[0,1,2,3]
def cover(im,fx=.5,fy=.5):
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s)+1,round(im.height*s)+1),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
fr={}
for k,idx in PICK.items():
    key='amli' if k=='amli2' else k; fr[key]=[]
    for n,i in enumerate(idx,1):
        im=Image.open(f'{R}{k}-{i:02d}.img').convert('RGB')
        out=f'{O}{key}-{n}.jpg'; cover(im).save(out,quality=86); fr[key].append('/'+out)
json.dump(fr,open('research/apt-sims/frames.json','w'),indent=1); print({k:len(v) for k,v in fr.items()})
