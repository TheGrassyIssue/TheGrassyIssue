import os,sys
from PIL import Image,ImageDraw
pre,idx,out=sys.argv[1],sys.argv[2],sys.argv[3]
fs=sorted(f for f in os.listdir('thumbs') if f.startswith(pre) and (idx=='all' or f.endswith(f'_{idx}.jpg')))
c=8; T=220; rows=(len(fs)+c-1)//c
sh=Image.new('RGB',(c*T,rows*(T+16)),'white'); d=ImageDraw.Draw(sh)
for k,f in enumerate(fs):
    im=Image.open('thumbs/'+f); im.thumbnail((T,T)); x=(k%c)*T; y=(k//c)*(T+16)
    sh.paste(im,(x,y)); d.text((x+2,y+T+2),f[3:][:34],fill='black')
sh.save(out,quality=70); print(len(fs))
