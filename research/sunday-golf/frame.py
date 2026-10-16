"""Frames for Brand to Know: Sunday Golf (15 Oct 2026). Brand's own photos from sundaygolf.com.
Transparent cutouts composited and fitted on stone (recolor); lifestyle cover-cropped. Infographic frames
(spec call-outs with text) and the publication-badge Ranger shot are skipped via SEL."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor
R='research/sunday-golf/raw/'; O='images/sunday-golf/'; W,H=1000,1250
O_=json.load(open('research/sunday-golf/options.json'))
SEL={'thelomaevergreenpar3':[1,3,4,5],'lomaxlmidnightgreenc':[1,4,5,6],'elcaminoblackyellowm':[1,5,3,6],'ryderevergreenfullsi':[1,3,5,4],
'ryder14midnightgreen':[3,4,5,6],'stormryderwaterproof':[3,1,4,5],'rangersagepremiumsta':[3,4,5,6],'thebigrigevergreenca':[1,3,5,6],
'rydersclasscreamleat':[1,3,5,4],'checkerfamilygolfbag':[1,3,4,5],'ryderduckcamofullsiz':[1,3,5,6],'ryderbobmarleyoliveh':[1,3,4,5],
'lomamossyoak':[1,3,4,5],'sundaygolfropehatusa':[1,4,5,2],'chestpacktan':[1,3,4,5],'magneticgolftowelmid':[1,2,3],'bigfrostygolfbagcool':[1,2,3,4],
'nickelbagtoastedalmo':[1,3,5,2],'caddypenholder':[1,5,4,2],'mickeybeaniebrowngra':[1,2,3],'bladeputterheadcover':[1,5,2,3],
'par3bamboogolftees80':[1,2],'lomagolfbagwallhookb':[1,2,3],'coastergolftravelbag':[1,4,5,3]}
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>205, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,pos=.4):
    lt,col=light(im)
    if lt:
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>20; ys,xs=np.where(m)
        if len(xs)>100:
            x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
            pad=int(.06*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
            s=min(W*.9/g.width,H*.9/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
            c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c,True
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H)),False
keys=[d['key'] for g,d in O_]
SEL={k:next(v for sk,v in SEL.items() if k.startswith(sk)) for k in keys}
missing=[k for k in keys if k not in SEL]; assert not missing, missing
fr={}
for k in keys:
    fr[k]=[]
    for n in SEL[k]:
        im=Image.open(f'{R}{k}-{n}.img').convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1])
        c,lt=frame(bg); out=f'{O}{k}-{n}.jpg'; c.save(out,quality=86)
        if lt: recolor(out,thresh=14)
        fr[k].append('/'+out)
json.dump(fr,open('research/sunday-golf/frames.json','w'),indent=1); print(len(fr),sum(len(v) for v in fr.values()))
