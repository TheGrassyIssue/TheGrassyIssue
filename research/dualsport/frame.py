"""Frames for Brand to Know: Dual Sport (16 Oct 2026). Brand's own photos from dualsportbrand.com.
Studio cutouts fitted on stone (recolor); lifestyle frames cover-cropped. Hero = triptych of three on-course portraits."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor, grade
WHITE={'archathleticclubhatwhi-1','archathleticclubhatwhi-2','dualmalletcover-1','dualmalletcover-2','thegraytshirt1-1','thegraytshirt1-2','vintagedsclassicunstru-c21','vintagedsclassicunstru-c22','iconpoloelectricblue-c11','cloudperformancequarte-1','cloudperformancequarte-2','ballertshirt-1','ballertshirt-2','flightknitpololightgre-c31'}
R='research/dualsport/raw/'; O='images/dualsport/'; W,H=1000,1250
PK=json.load(open('research/dualsport/picks.json'))
SEL={'flightknitpololightgre':[1,2,3,'c11','c21','c31'],'diamondbladepologreen':[3,1,2,'c11'],'iconpoloelectricblue':[3,1,2,'c11','c21'],
'iconpologalaxy':[1,2],'signaturepolodarkflora':[4,1,2],'elitewindbreaker':[3,1,4,5,2],'pursuitwindbreakerblac':[1,2,'c11'],
'cloudperformancequarte':[3,1,4,2,'c11'],'shiverquarterzipmist':[3,1,4,2,'c11'],'knitjersey':[4,1,3,2],'voltknitvest':[4,1,2],
'pursuitshortselectricb':[3,1,6,4,'c11','c21'],'motionpantsblack':[4,1,3,'c11'],'motionshortsplatinumgr':[1,2,'c11','c21'],
'archathleticclubhatwhi':[1,2,'c11','c21'],'dscamohat':[1,2],'dualathleticclubhatgre':[1,2,'c11'],'vintagedsclassicunstru':[1,2,'c11','c21'],
'dualdriverheadcover':[1,3,2],'dualmalletcover':[1,2],'thegraytshirt1':[1,2],'prodaytshirt':[1,2],'ballertshirt':[1,2],'throwbacktshirt':[1,2]}
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>185, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.4,W=W,H=H,fit=True):
    lt,col=light(im)
    if lt and fit:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>22; ys,xs=np.where(m)
        if len(xs)>100:
            x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
            pad=int(.08*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
            s=min(W*.84/g.width,H*.84/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
            c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
def load(n):
    im=Image.open(f'{R}{n}.img').convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1])
    e=int(.02*min(bg.size)); return bg.crop((e,e,bg.width-e,bg.height-e))
fr={}
for d in PK:
    k=d['key']; fr[k]=[]
    for n in SEL[k]:
        im=load(f'{k}-{n}'); c,lt=frame(im,fit=im.width>=im.height*.95,pos=.3); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
        if lt: (grade(out) if f'{k}-{n}' in WHITE else recolor(out,thresh=14))
        fr[k].append('/'+out)
json.dump(fr,open('research/dualsport/frames.json','w'),indent=1)
# bands + card hero (cover crop)
for name,src in [('life-1','life-ME4A3429'),('life-2','signaturepolodarkflora-3'),('life-3','pursuitwindbreakerblac-3'),('life-4','dualmalletcover-3'),
                 ('life-5','knitjersey-5'),('life-6','diamondbladepologreen-4'),('life-7','pursuitshortselectricb-7'),('life-8','voltknitvest-3'),('card-hero','life-ME4A3429')]:
    frame(load(src),fit=False,pos=.45)[0].save(f'{O}{name}.jpg',quality=86)
# hero triptych 2000x857 and og
def tri(Wt,Ht):
    w=Wt//3; c=Image.new('RGB',(Wt,Ht),(20,20,20))
    for i,(s,p) in enumerate([('voltknitvest-3',.35),('life-ME4A3429',.55),('motionpantsblack-5',.5)]):
        c.paste(frame(load(s),fit=False,W=w if i<2 else Wt-2*w,H=Ht,pos=p)[0],(i*w,0))
    return c
tri(2000,857).save(O+'btk-hero.jpg',quality=86); tri(1200,630).save(O+'btk-og.jpg',quality=86)
print(len(fr),sum(len(v) for v in fr.values()))
