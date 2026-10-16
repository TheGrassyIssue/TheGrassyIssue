"""Frames for Brand to Know: Gumtree Golf & Nature Club (15 Oct 2026). Brand's own photos from gumtreegolfandnature.com.
Light-background cutouts fitted on stone (recolor); glove/turf lifestyle frames cover-cropped."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/gumtree/raw/'; O='images/gumtree/'; W,H=1000,1250
PK=json.load(open('research/gumtree/picks.json'))
SEL={'westcoastsurftentheadc':[1,2,3,4],'treefroggreencamptenth':[1,2,3],'stateflowerheadcover20':[1,2,3,4],'heirloomquiltputtercov':[1,2,3,4],
'natureclubneoprenewets':[1,2],'nywoolheadcovers':[2,3,1,5],'americanwoolheadcover':[1,2,3,4],'studiocollectionheadco':[1,2,5,6],'ggncxmalbonbirdsofgeor':[1,2,3,4],
'tofightamockingbirdtee':[1,2],'stateflowerreferencete':[1,2,4,3],'anatomyofaflyreference':[1,2,3],'natureclubbestbirdiest':[1,2],'loseyourballfindyourse':[1,2,3,4],
'natureclubdeadstocklac':[1,2,3],'natureclubrockawaystri':[1,2,3,4],'natureclubtheendlsline':[1,2,3,4],'studiocollectionsspolo':[1,2,3,4],'madeinmanhattanvest':[1,2,4,3],
'natureclubvintagewashb':[1,3,4],'natureclubbeachcombers':[1,2,3,4],'heirloomquiltvest44lwp':[1,2,3],'texasstateflower5panel':[1,2,3],'newyorkbranchesunstruc':[1,2,3,6],
'ggncxpumafieldnotespol':[1,2,3,4],'ggncxpumahelsinkig':[1,2,3,4],'ggncxmackenzienybagnav':[1,2,3,4],'membercaddytowel':[1,2],'madeinmanhattanheadcov':[1,2,4,5],
'stateflorafaunaheadcov':[1,2,3,4],'heirloomquiltcoveracmw':[1,2,3,4],'fishingwaderheadcover':[1,6,2],'gumtreecoffeestudioesp':[1,2],'nycsubwaytokenballmark':[1,2,3],
'vintagenewyorkstateout':[1,2,3,4],'natureclubfishspeciesh':[1,2,4]}
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
json.dump(fr,open('research/gumtree/frames.json','w'),indent=1); print(len(fr),sum(len(v) for v in fr.values()))
