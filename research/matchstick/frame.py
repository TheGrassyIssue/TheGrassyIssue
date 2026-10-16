"""Frames for Brand to Know: Matchstick Golf (15 Oct 2026). Brand's own photos from matchstickgolf.com.
Light-background cutouts fitted on stone (recolor); glove/turf lifestyle frames cover-cropped."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/matchstick/raw/'; O='images/matchstick/'; W,H=1000,1250
PK=json.load(open('research/matchstick/picks.json'))
SEL={'oldfashioned':[1,2,4,3],'transfusion':[1,2,3,4],'icedcoffeegolfballmark':[1,3,4,5],'ballmarkerflamingcoffe':[1,3,4,2],
'putteradefrost':[1,2,4,3],'putteradelemonlime':[1,2,4,3],'devilhornsblackgold':[1,2,3,4],'truffleshuffle':[1,2,3,4],
'pirateflag':[1,2,3,5],'skeletonkey':[1,2,3,5],'vwbus':[1,2],'chefskull':[1,2,3,5],'cash':[1,2,3,5],'pokerchip':[1,2,3],'reddice':[1,2,3],
'gaspumpgolfballmarker':[1,3,2],'firetruckgolfballmarke':[1,3,2],'oregonstatebeavershead':[1,2,5,4],'teddyroosevelt':[1,2],
'ladylibertyballmarker':[1,5,6,4],'buildyourowncustomgolf':[2,5,6,4],'usadreamteambasketball':[1,2,3,4],'ussoccerupcycledheadco':[1,2,4,5],
'newyorkbasketballdrive':[1,2,6,3],'rooseveltpatterndriver':[1,4,5,2],'osubeaversblackdriverno':[1,2,6,4],'rooseveltpatterngolfto':[1],
'keylimepie':[2,1,3,4],'matchstickmanjonesrang':[1],'tigerroarreliefprint':[1,2,3]}
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>190, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.45):
    lt,col=light(im)
    if lt:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>22; ys,xs=np.where(m)
        if len(xs)>100:
            x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
            pad=int(.10*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
            s=min(W*.82/g.width,H*.82/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
            c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
fr={}
for d in PK:
    k=d['key']; fr[k]=[]; SELK=next(v for sk,v in SEL.items() if sk.startswith(k) or k.startswith(sk))
    for n in SELK:
        im=Image.open(f'{R}{k}-{n}.img').convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1])
        e=int(.02*min(bg.size)); bg=bg.crop((e,e,bg.width-e,bg.height-e))
        c,lt=frame(bg); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
json.dump(fr,open('research/matchstick/frames.json','w'),indent=1); print(len(fr),sum(len(v) for v in fr.values()))
