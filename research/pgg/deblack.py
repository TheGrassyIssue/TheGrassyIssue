import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter
STONE=(232,226,214)
def deblack(src,dst):
    im=Image.open(src).convert('RGB'); a=np.array(im).astype(int)
    if a[5,5].max()>10: im.save(dst,quality=95); return False
    m=im.copy(); W,H=m.size
    seeds=[(0,0),(W-1,0),(0,H-1),(W-1,H-1),(W//2,0),(W//2,H-1),(0,H//2),(W-1,H//2)]
    for s in seeds:
        if max(m.getpixel(s))<=10: ImageDraw.floodfill(m,s,(255,0,255),thresh=10)
    b=np.array(m); mask=(b[...,0]==255)&(b[...,1]==0)&(b[...,2]==255)
    # soften: grow into dark antialias pixels touching the background
    mk=Image.fromarray((mask*255).astype(np.uint8))
    grow=np.array(mk.filter(ImageFilter.MaxFilter(5)))>0
    lum=a.max(2)
    edge=grow&~mask&(lum<30)
    alpha=mask.astype(float)
    alpha[edge]=np.clip(1-lum[edge]/30,0,1)
    al=np.array(Image.fromarray((alpha*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)/255
    al=np.maximum(al,mask)[...,None]
    out=a*(1-al)+np.array(STONE)*al
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(dst,quality=95); return True
if __name__=='__main__':
    for f in sys.argv[1:]: print(f,deblack(f'raw/{f}.jpg',f'raw/{f}-s.jpg'))
