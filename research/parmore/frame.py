"""Frame Parmore Golf images into 1000x1250 gallery frames + hero/og/card. 12 October 2026.
Real photos only: Parmore's AI-generated images (ChatGPT / Kive.ai / Generated Image file names) are never downloaded.
Galleries lead with an on-model shot where one exists. Light studio backgrounds -> stone via recolor (edge flood fill)."""
import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import recolor, grade
R='research/parmore/raw/'; O='images/parmore/'; W,H=1000,1250
SEL={"green-1-4-zip-rebrand":[3,1,2,4,5],"camo-1-4-zip-rebrand":[3,1,2,4,5],"long-sleeved-windbreaker-rebrand":[3,4,1,2,5],
"brown-zip-windbreaker-rebrand":[3,4,1,2,5],"green-stripes-polo-rebrand":[3,1,2,4],"brown-stripes-polo-rebrand":[3,1,2,4],
"grey-paneled-tee-rebrand":[3,1,2,4],"red-paneled-tee-rebrand":[3,1,2,4],"parm-050":[2,1],"parm-043":[1],"parm-042":[1,2],
"parm-038":[2,1],"parm-049":[3,1,2],"casual-pants-black":[3,4,1,2,5],"parm-044":[3,1,2],"parmore-embroidered-5-panel":[3,1,2],
"active-grip-socks":[1,2,3],"zip-up-camo-jacket-rebrand":[1,2],"zip-up-fleece-rebrand":[1,2],"pod-rebrand-hoodie-1":[1]}
TIGHT={'parm-043','active-grip-socks','parm-044','parmore-embroidered-5-panel','pod-rebrand-hoodie-1','zip-up-fleece-rebrand','zip-up-camo-jacket-rebrand'}
def flat(im):
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(245,245,245)); bg.paste(im,mask=im.split()[-1]); return bg
    return im.convert('RGB')
def light(im):
    a=np.asarray(im).astype(int); b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); return b.min(axis=1).mean()>215, tuple(int(x) for x in np.median(b,axis=0))
def frame(im,h,pos=.3):
    lt,col=light(im)
    if lt and abs(im.width/im.height-.8)>.03 or (lt and h in TIGHT):
        a=np.asarray(im).astype(int); m=np.abs(a-col).max(axis=2)>18; ys,xs=np.where(m)
        x0,x1=np.percentile(xs,[.5,99.5]).astype(int); y0,y1=np.percentile(ys,[.5,99.5]).astype(int)
        pad=int(.06*max(x1-x0,y1-y0)); g=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
        s=min(W*.92/g.width,H*.92/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
        c=Image.new('RGB',(W,H),col); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
fr={}
keys=sys.argv[1:] or list(SEL)
try: fr=json.load(open('research/parmore/frames.json'))
except Exception: pass
for h in keys:
    fr[h]=[]
    for n,k in enumerate(SEL[h],1):
        out=f'{O}{h}-{n}.jpg'; frame(flat(Image.open(f'{R}{h}-{k}.png')),h,.2).save(out,quality=86); (grade(out) if h in ('parm-050','parm-038') else recolor(out,thresh=14)); fr[h].append('/'+out)
    print(h,len(fr[h]),flush=True)
json.dump(fr,open('research/parmore/frames.json','w'),indent=1)
