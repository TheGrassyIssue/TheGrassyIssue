"""Fabrics post hero (24 Oct 2026, Lenny: "The hero needs to be better and more dynamic"): three on-course lifestyle panels
(Olydoe merino polo, Walker ripstop shorts mid-swing, Sounder cords chipping) with a fabric swatch and label on each."""
from PIL import Image,ImageDraw,ImageFont
R='research/fabrics/raw/'
def cover(im,W,H,cx=.5,cy=.5):
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def zoom(im,box): w,h=im.size; return im.crop((int(box[0]*w),int(box[1]*h),int(box[2]*w),int(box[3]*h)))
F='assets/fonts/editors-note-text-bold.otf'; FI='assets/fonts/editors-note-text-italic.otf'
P=[('R51-4',.2,.5,'R39-4',(.55,.05,.95,.45),'RIPSTOP','light, tough, sheds wind'),
   ('M20-1',.25,.5,'M41-3',(.2,.2,.8,.8),'MERINO','soft, warm, resists odor'),
   ('C46-2',.35,.5,'C20-2',(.3,.35,.6,.65),'CORDUROY','warm, soft, very 70s')]
def panels(W,H,s):
    out=[]
    for src,cy,cx,sw,box,lab,line in P:
        im=cover(Image.open(R+src+'.img').convert('RGB'),W,H,cx=cx,cy=cy)
        g=Image.new('L',(1,H))
        for y in range(H): g.putpixel((0,y),int(max(0,(y-H*.45)/(H*.55))**1.4*210))
        im=Image.composite(Image.new('RGB',(W,H),(18,30,17)),im,g.resize((W,H)))
        d=ImageDraw.Draw(im); r=int(70*s); x0=int(36*s); cyp=H-int(160*s)
        swi=cover(zoom(Image.open(R+sw+'.img').convert('RGB'),box),2*r,2*r)
        m=Image.new('L',(2*r,2*r),0); ImageDraw.Draw(m).ellipse((0,0,2*r-1,2*r-1),fill=255)
        im.paste(swi,(x0,cyp-r),m); d.ellipse((x0,cyp-r,x0+2*r,cyp+r),outline=(244,240,230),width=max(2,int(3*s)))
        f=ImageFont.truetype(F,int(52*s)); fi=ImageFont.truetype(FI,int(26*s)); tx=x0+2*r+int(22*s); x=tx
        for ch in lab: d.text((x,cyp-int(40*s)),ch,font=f,fill=(244,240,230)); x+=d.textlength(ch,font=f)+int(6*s)
        d.text((tx,cyp+int(22*s)),line,font=fi,fill=(232,226,214)); out.append(im)
    return out
def strip(W,H,pw,s,gap):
    S=Image.new('RGB',(W,H),(244,240,230)); x=0
    for im in panels(pw,H,s): S.paste(im,(x,0)); x+=pw+gap
    return S
strip(2000,857,662,1.0,7).save('images/fabrics/hero.jpg',quality=88,optimize=True)
strip(1200,630,396,.62,6).save('images/fabrics/og.jpg',quality=88)
panels(1000,1250,1.4)[0].save('images/fabrics/card-hero.jpg',quality=88)
print('ok')
