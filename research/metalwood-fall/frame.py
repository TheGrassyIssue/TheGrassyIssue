"""Frames for Metalwood Studio FW26 (16 Oct 2026). Metalwood's own product photos + FW26 Pt 1 lookbook
(shot by Ryan Thomas Murray & Chase Thompson). 4:5 shots resized; squares fitted onto a 4:5 canvas; light frames graded to stone."""
import json,sys,os,glob
from PIL import Image
sys.path.insert(0,'research/grips-vol2'); from recolor import grade
R='research/metalwood-fall/'; O='images/metalwood-fw26/'; W,H=1000,1250
PK=json.load(open(R+'picks.json'))
def cover(im,W=W,H=H,pos=.4):
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=(im2.width-W)//2; y=int((im2.height-H)*pos); return im2.crop((x,y,x+W,y+H))
def fit(im):
    px=im.getpixel((3,3)); s=min(W*.96/im.width,H*.96/im.height); g=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),px); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
def frame(src,out):
    im=Image.open(src).convert('RGB')
    c=cover(im) if im.height>=im.width*1.15 else fit(im)
    c.save(out,quality=86); grade(out)
fr={}
for d in PK:
    k=d['key']; fs=[f'{R}raw/{k}-{i}.img' for i in range(1,7) if os.path.exists(f'{R}raw/{k}-{i}.img')]
    fs+=sorted(glob.glob(f'{R}raw/{k}-c*.img'))
    fs=fs[:9]; fr[k]=[]
    for f in fs:
        out=O+os.path.basename(f)[:-4]+'.jpg'; frame(f,out); fr[k].append('/'+out)
json.dump(fr,open(R+'frames.json','w'),indent=1)
for f in sorted(glob.glob(R+'lb/*.img')):
    im=Image.open(f).convert('RGB'); n=os.path.basename(f)[:-4]
    cover(im,pos=.3 if im.height>im.width else .5).save(f'{O}{n}.jpg',quality=86)
Image.open(O+'lb-01.jpg').save(O+'card-hero.jpg',quality=86)
def tri(Wt,Ht):
    w=Wt//3; c=Image.new('RGB',(Wt,Ht),(240,240,240))
    for i,(s,p) in enumerate([('lb-15',.25),('lb-10',.2),('lb-17',.2)]):
        ww=w if i<2 else Wt-2*w; c.paste(cover(Image.open(f'{R}lb/{s}.img').convert('RGB'),ww,Ht,p),(i*w,0))
    return c
tri(2000,857).save(O+'btk-hero.jpg',quality=86); tri(1200,630).save(O+'btk-og.jpg',quality=86)
print(len(fr),sum(len(v) for v in fr.values()))
