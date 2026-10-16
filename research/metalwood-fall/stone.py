"""Whole-frame white balance toward TGI stone, sampling the backdrop from the top corners (lookbook shots touch the edges)."""
import numpy as np
from PIL import Image
STONE=np.array([232,226,214],float)
def stone(path):
    im=Image.open(path).convert('RGB'); a=np.asarray(im).astype(float); h,w=a.shape[:2]; p=max(20,w//25)
    s=np.concatenate([a[:p,:p].reshape(-1,3),a[:p,-p:].reshape(-1,3)])
    bg=np.median(s,axis=0)
    if bg.min()<200: return False
    out=np.clip(a*(STONE/bg),0,255); Image.fromarray(out.astype('uint8')).save(path,quality=88); return True
if __name__=='__main__':
    import sys
    for f in sys.argv[1:]: print(f, stone(f))
