"""Frames for On Our Radar: Loraloma (19 Oct 2026). Club's own photos (Evan Schiller for the course shots), from loralomaclub.com."""
from PIL import Image
R='research/loraloma/raw/'; O='images/loraloma/'
def crop(src,W,H,cx=.5,cy=.5,out=None,q=86):
    im=Image.open(R+src).convert('RGB'); w,h=im.size
    if w/h>W/H: nw=int(h*W/H); x=int((w-nw)*cx); im=im.crop((x,0,x+nw,h))
    else: nh=int(w*H/W); y=int((h-nh)*cy); im=im.crop((0,y,w,y+nh))
    im.resize((W,H),Image.LANCZOS).save(O+out,quality=q)
crop('Loraloma8_DSC01479.jpg',2000,857,cy=.62,out='btk-hero.jpg',q=88)
crop('Loraloma8_DSC01479.jpg',1200,630,cy=.6,out='btk-og.jpg')
crop('Loraloma2_DSC01545-.jpg',1000,1250,cx=.45,out='card-hero.jpg')
for n,(s,cx) in enumerate([('Loraloma9_DSC00655-.jpg',.5),('Loraloma15_DSC01035-1.jpg',.35),('Loraloma10_DSC00615-.jpg',.55)],1):
    crop(s,1000,1250,cx=cx,out=f'land-{n}.jpg')
for name,s,cy in [('hole-2','Loraloma2_DSC01545-.jpg',.5),('hole-8','Loraloma8_DSC00687-.jpg',.55),('hole-18','Loraloma18_DSC00777-.jpg',.5),('hole-18b','Loraloma18_DSC00736-.jpg',.5),('hole-4','Loraloma4_DSC01267.jpg',.55),('hole-5','Loraloma5_DSC00606-.jpg',.5)]:
    crop(s,1800,1200,cy=cy,out=name+'.jpg')
for n,(s,cx) in enumerate([('LoraLomaOpening-184-3.jpg',.5),('LoraLomaOpening-160-1.jpg',.55),('Loraloma16_DSC00723-.jpg',.5)],1):
    crop(s,1000,1250,cx=cx,out=f'day-{n}.jpg')
print('ok')
