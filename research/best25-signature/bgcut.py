import hashlib
import numpy as np
from PIL import Image,ImageFilter
W,H=1000,1250
TOP,BOT=np.array((242,238,230),float),np.array((228,222,210),float)
G=(TOP*(1-np.linspace(0,1,H)[:,None,None])+BOT*np.linspace(0,1,H)[:,None,None]).repeat(W,1)
def cut(im,thr=0.12):
  im=im.convert('RGB');im.thumbnail((int(W*.86),int(H*.86)),Image.LANCZOS)
  a=np.asarray(im).astype(float);h,w,_=a.shape
  ys,xs=np.mgrid[0:h,0:w]
  bm=np.zeros((h,w),bool);k=max(4,int(min(h,w)*.04));bm[:k]=bm[-k:]=True;bm[:,:k]=bm[:,-k:]=True
  A=np.c_[xs[bm],ys[bm],np.ones(bm.sum()),xs[bm]*ys[bm],xs[bm]**2,ys[bm]**2]
  Af=np.c_[xs.ravel(),ys.ravel(),np.ones(h*w),(xs*ys).ravel(),(xs**2).ravel(),(ys**2).ravel()]
  bg=np.stack([(Af@np.linalg.lstsq(A,a[...,c][bm],rcond=None)[0]).reshape(h,w) for c in range(3)],-1)
  # chromaticity distance + allow darker (shadow) of same chroma
  s1=a.sum(2,keepdims=True)+1;s2=bg.sum(2,keepdims=True)+1
  cd=np.abs(a/s1-bg/s2).sum(2)
  ratio=(a.sum(2)+1)/(bg.sum(2)+1)
  isbg=(cd<thr*0.5)&(ratio>0.45)&(ratio<1.25)
  m=Image.fromarray(((~isbg)*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
  out=Image.fromarray(G.astype(np.uint8));out.paste(im,((W-w)//2,(H-h)//2),m);return out
def cut_flat(im,thr=38):
  im=im.convert('RGB');im.thumbnail((int(W*.86),int(H*.86)),Image.LANCZOS)
  a=np.asarray(im).astype(float)
  b=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);col=np.median(b,axis=0)
  dist=np.sqrt(((a-col)**2).sum(axis=2))
  m=Image.fromarray(((dist>thr)*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
  out=Image.fromarray(G.astype(np.uint8));out.paste(im,((W-im.width)//2,(H-im.height)//2),m);return out
