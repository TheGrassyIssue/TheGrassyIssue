"""27 Oct 2026: Bluegrass Fairway formatting pass — white-sweep product shots onto TGI stone (capsules frame()).
Originals in research/bluegrass-orig/. Idempotent (always re-frames from the backup)."""
import os, shutil
import numpy as np
from PIL import Image, ImageDraw
W, H = 1000, 1250; STONE = (232, 226, 214)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
D = 'images/bluegrass-fairway/'; B = 'research/bluegrass-orig/'; n = 0
for f in sorted(os.listdir(D)):
    if ' 2.' in f or not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): continue
    p = B + f if os.path.exists(B + f) else D + f
    im = Image.open(p).convert('RGBA'); w0 = Image.new('RGBA', im.size, (255, 255, 255, 255)); w0.alpha_composite(im)
    a = np.asarray(w0.convert('RGB')).astype(int); k = 8
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    if cc.min() < 235: continue
    if not os.path.exists(B + f): shutil.copy2(D + f, B + f)
    CUR[0] = f; out = frame(w0.crop((3, 3, w0.width - 3, w0.height - 3)))
    out.save(D + f, optimize=True) if f.lower().endswith('.png') else out.save(D + f, quality=86, optimize=True); n += 1
print(n)
