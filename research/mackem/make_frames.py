import json,glob
from PIL import Image
R='research/mackem/'
REC=['M01','M03','M04','M05','M22','M27','M66','M48','M21','M54','M65','M26','M61','M62','M59','M08','M12','M41']
W,H=1000,1250
def fit(im,w,h,cy=.5):
  im=im.convert('RGB');a,b=im.size;r=w/h
  if a/b>r: nw=int(b*r);x=(a-nw)//2;im=im.crop((x,0,x+nw,b))
  else: nh=int(a/r);y=int((b-nh)*cy);im=im.crop((0,y,a,y+nh))
  return im.resize((w,h),Image.LANCZOS)
out={}
for c in REC:
  fs=sorted(glob.glob(f'{R}raw/{c}-*.jpg'),key=lambda f:int(f.split('-')[-1][:-4]))[:5]
  out[c]=[]
  for n,f in enumerate(fs):
    dst=f'images/mackem/{c.lower()}-{n+1}.jpg';fit(Image.open(f),W,H).save(dst,quality=86,optimize=True,progressive=True);out[c].append('/'+dst)
json.dump(out,open(R+'frames.json','w'),indent=1)
L=json.load(open(R+'life.json'))
for n,(i,cy) in enumerate([(11,.4),(13,.5),(16,.5),(3,.5),(6,.5),(2,.5),(52,.5),(65,.5),(51,.5)],1):
  fit(Image.open(R+L[i][0]),W,H,cy).save(f'images/mackem/band-{n}.jpg',quality=85,optimize=True,progressive=True)
# hero: option D (Lenny switched from C, 6 Oct)
h=Image.open(R+'hero-opt-D.jpg');h.save('images/mackem/btk-hero.jpg',quality=86);h.resize((1200,514),Image.LANCZOS).save('images/mackem/btk-og.jpg',quality=84)
fit(Image.open(R+L[17][0]),1080,1350,.4).save('images/mackem/btk-card-hero.jpg',quality=85)
print(sum(len(v) for v in out.values()))
