"""Frame Local Rule store images into 1000x1250 gallery frames (images/local-rule/g/). No soften pass: the studio floor shadows blotch."""
import json,numpy as np
from PIL import Image
SEL={"tech-polo-light-brown":[0,1,2,4,5],"knit-polo-offwhite":[0,1,2,3,4],"performance-polo-dark-green":[0,1,3,2,4],
"long-sleeve-performance-polo-dark-navy":[0,1,2,3],"football-jersey-striped-navy":[2,0,1],"q-zip-fleece-sweatshirt-light-blue":[0,1,3,2,4],
"fleece-pullover-blue":[0,1,4,2,3],"tech-vest-light-green":[0,1,3,2],"tech-anorak-navy":[0,1,3,4,2],"pleated-trousers-offwhite":[1,4,3,2],
"tech-pants-light-grey":[1,3,4],"shibuya-shorts-dark-navy":[1,5,4],"tech-shorts-green":[1,4,3],"vintage-wool-cap-burgundy":[1,0,2,3],
"buckethat-military-green":[0,1],"pom-pom-beanie-navy":[3,0,1,2],"leather-belt":[0,1,3,2],"lclrl-towel":[0,1,2,3]}
W,H=1000,1250; fr={}
for h,idx in SEL.items():
    fr[h]=[]
    for k,i in enumerate(idx,1):
        im=Image.open(f'research/local-rule-refresh/raw/{h}-{i}.jpg').convert('RGB')
        if h=='tech-pants-light-grey': im=im.crop((0,0,int(im.width*.86),int(im.height*.93)))
        a=np.asarray(im).astype(int); border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
        r=im.width/im.height
        if border.std(axis=0).max()<12 and abs(r-0.8)>0.02:
            col=tuple(int(x) for x in np.median(border,axis=0)); s=min(W*.88/im.width,H*.88/im.height)
            im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2))
        else:
            s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
            x=(im2.width-W)//2; y=int((im2.height-H)*0.3); c=im2.crop((x,y,x+W,y+H))
        out=f'images/local-rule/g/{h}-{k}.jpg'; c.save(out,quality=86); fr[h].append('/'+out)
json.dump(fr,open('research/local-rule-refresh/frames.json','w'),indent=1)
print(sum(map(len,fr.values())))
