import json
from PIL import Image,ImageOps
R='research/magazines/img/'; OUT='images/required-reading-mags/'
PLAN={
 'hiatus-no2':['hiatus-1','hiatus-6','hiatus-2'],
 'hiatus-no1':['hiatus-3','hiatus-5','hiatus-4'],
 'depeche-5':['depeche-1','depeche-3','depeche-2','depeche-4','depeche-5','depeche-6'],
 'depeche-4':['depeche-7','depeche-8','depeche-9','depeche-10','depeche-11'],
 'loop-02':['loop-1'],
 'loop-01':['loop-2','loop-4'],
 'gq-58':['gq-1','gq-2','gq-3','gq-4'],
 'sagca-26':['sagca-1','sagca-2','sagca-3'],
 'lftr-2':['lftr-1','lftr-2','lftr-3'],
 'lftr-1':['lftr-4','lftr-5','lftr-6'],
}
PHOTO={'depeche-1','depeche-2','depeche-3','depeche-4','depeche-5','depeche-6','hiatus-5','hiatus-6','loop-4'}
def edge(im):
    g=im.convert('RGB');w,h=g.size
    px=[g.getpixel((x,y)) for x in range(0,w,max(1,w//50)) for y in (1,h-2)]+[g.getpixel((x,y)) for y in range(0,h,max(1,h//50)) for x in (1,w-2)]
    lum=[sum(p)/3 for p in px]
    return max(lum)-min(lum)<22, tuple(sorted(px,key=lambda p:sum(p))[len(px)//2])
fr={}
for k,fs in PLAN.items():
    fr[k]=[]
    for j,f in enumerate(fs,1):
        im=Image.open(R+f+'.jpg').convert('RGB')
        if f in PHOTO:
            out=ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=(.5,.5))
        else:
            uni,bg=edge(im)
            from PIL import ImageChops
            diff=ImageChops.difference(im,Image.new('RGB',im.size,bg)).convert('L').point(lambda v:255 if v>28 else 0)
            bb=diff.getbbox()
            if bb:
                m=int(max(im.size)*0.03); bb=(max(0,bb[0]-m),max(0,bb[1]-m),min(im.width,bb[2]+m),min(im.height,bb[3]+m)); im=im.crop(bb)
            if not uni: bg=(236,232,224)
            t=im.copy(); t.thumbnail((880,1100),Image.LANCZOS)
            if t.width<880 and t.height<1100:
                s=min(880/t.width,1100/t.height); t=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            out=Image.new('RGB',(1000,1250),bg); out.paste(t,((1000-t.width)//2,(1250-t.height)//2))
        p=f'{OUT}{k}-{j}.jpg'; out.save(p,quality=84,optimize=True,progressive=True)
        fr[k].append({'local':'/'+p,'from':f})
json.dump(fr,open('research/magazines/frames.json','w'),indent=1)
im=Image.open(R+'depeche-3.jpg').convert('RGB')
ImageOps.fit(im,(1600,685),Image.LANCZOS,centering=(.5,.55)).save(OUT+'hero.jpg',quality=85,optimize=True,progressive=True)
ImageOps.fit(im,(1200,630),Image.LANCZOS,centering=(.5,.55)).save(OUT+'og.jpg',quality=85,optimize=True,progressive=True)
# sheet
from PIL import ImageDraw
t=[(k,x['local'].lstrip('/')) for k,v in fr.items() for x in v]
S=Image.new('RGB',(10*160,((len(t)+9)//10)*214),'white')
for i,(k,p) in enumerate(t):
    a=Image.open(p);a.thumbnail((156,196));S.paste(a,((i%10)*160+2,(i//10)*214+2));ImageDraw.Draw(S).text(((i%10)*160+2,(i//10)*214+200),k,fill='black')
S.save('/sessions/admiring-pensive-ritchie/mnt/outputs/mag_frames.jpg',quality=80)
