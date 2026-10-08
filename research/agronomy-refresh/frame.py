import numpy as np, json
from PIL import Image
R='research/agronomy-refresh/raw/'; L='images/agronomy/'
SEL={"work-shirt":["4","L:p-work-shirt","0","1"],
"heavyweight-work-shirt-navy":["4","L:p-heavyweight-work-shirt-navy","0","1"],
"heavyweight-work-shirt-natural":["4","L:p-heavyweight-work-shirt-natural","0","1"],
"heavyweight-work-shirt-ss-earth":["4","5","1","0"],
"heavyweight-work-shirt-ss-navy":["4","5","0","1"],
"golf-brand-hat-earth":["0","1","2","3"],
"golf-brand-hat-black":["4","3","0","1"],
"tree-hat":["3","4","0","1"],
"tree-hat-earth":["0","1","2"],
"agronomy-work-hat":["3","0","1"],
"unusual-lies-towel":["2","0","1","3"],
"unusual-lies-towel-navy":["3","2","0","1"]}
W,H=1000,1250; out={}
for h,lst in SEL.items():
  out[h]=[]
  for j,s in enumerate(lst,1):
    p=L+s[2:]+'.jpg' if s.startswith('L:') else R+f'{h}-{s}.jpg'
    im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int)
    border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    if border.std(axis=0).max()<12:
      col=tuple(int(x) for x in np.median(border,axis=0))
      s2=min(W*0.86/im.width,H*0.86/im.height); im2=im.resize((int(im.width*s2),int(im.height*s2)),Image.LANCZOS)
      c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2))
    else:
      s2=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s2)),max(H,round(im.height*s2))),Image.LANCZOS)
      x=(im2.width-W)//2; y=(im2.height-H)//2; c=im2.crop((x,y,x+W,y+H))
    f=f'{L}g-{h}-{j}.jpg'; c.save(f,quality=87); out[h].append('/'+f)
json.dump(out,open('research/agronomy-refresh/frames.json','w'),indent=1)
print('ok')
