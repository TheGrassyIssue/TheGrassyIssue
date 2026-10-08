import json,numpy as np
from PIL import Image
R='research/small-things/raw'; O='images/small-things'
SEL={1:[2,0,6,3],2:[1,4,2,0,5],3:[1,0,2],4:[2,0,1],5:[0,1],6:[0,1],7:[0,1],11:[2,1,4,0],15:[2,0,1],16:[0,1,2],
19:[2,0,1],20:[2,0],22:[1,4,0,3],23:[3,0,2],10:[0,1],27:[0,1],28:[0,1,3],31:[0],33:[0],36:[0],41:[0,2],42:[0,1,2],43:[1,0,2],44:[1,0,2],45:[0,1,4]}
W,H=1000,1250; frames={}
for n,idx in SEL.items():
  frames[n]=[]
  for j,i in enumerate(idx):
    im=Image.open(f'{R}/{n}-{i}.jpg').convert('RGB'); a=np.asarray(im).astype(int)
    border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    uniform=border.std(axis=0).max()<12
    if uniform:
      col=tuple(int(x) for x in np.median(border,axis=0))
      s=min(W*0.86/im.width,H*0.86/im.height); im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
      c=Image.new('RGB',(W,H),col); c.paste(im2,((W-im2.width)//2,(H-im2.height)//2))
    else:
      s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
      x=(im2.width-W)//2; y=(im2.height-H)//2; c=im2.crop((x,y,x+W,y+H))
    f=f'{O}/st{n:02d}-{j+1}.jpg'; c.save(f,quality=88); frames[n].append('/'+f)
json.dump(frames,open('research/small-things/frames.json','w'),indent=1)
print('ok')
