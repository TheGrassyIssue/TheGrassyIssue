"""27 Oct 2026: Lenny "make sure all the Mackenzie bag pages are formatted and looking correct".
The MacKenzie Collab Archive (built Aug 28) predates the no-stark-white rule: re-frame every product shot on a white or
light-grey studio sweep onto TGI stone (capsules frame()). Originals kept in research/mackenzie-orig/. Idempotent: only
touches files whose original is still the white version (tracked by the backup)."""
import os, shutil, json
import numpy as np
from PIL import Image, ImageDraw
W, H = 1000, 1250; STONE = (232, 226, 214)
src = open('research/capsules/frame.py').read(); exec(src[src.index('SOFT ='):src.index('fr = {}')])
D = 'images/mackenzie/'; B = 'research/mackenzie-orig/'; os.makedirs(B, exist_ok=True)
done = []
if not os.environ.get('EXTRA_ONLY'):  # the 56-image pass takes ~3 min; rerun just the extras with EXTRA_ONLY=1
    for f in sorted(os.listdir(D)):
        if ' 2.' in f: continue
        orig = B + f
        p = orig if os.path.exists(orig) else D + f
        im = Image.open(p).convert('RGBA'); a = np.asarray(im.convert('RGB')).astype(int); k = 8
        cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
        if not (cc.min() >= 235 or (f.startswith('sentinel-') and cc.min() >= 200)): continue
        if not os.path.exists(orig): shutil.copy2(D + f, orig)
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        bg = bg.crop((3, 3, bg.width - 3, bg.height - 3)); CUR[0] = f
        out = frame(bg)
        if f.lower().endswith('.png'): out.save(D + f, optimize=True)
        else: out.save(D + f, quality=86, optimize=True)
        done.append(f)
print(len(done))

# MacKenzie cards on the multi-brand bag posts (27 Oct): same treatment, same backup folder.
EXTRA = ['images/stand-bags/mackenzie-walker-nylon.jpg', 'images/stand-bags/mackenzie-walker-canvas.jpg',
         'images/stand-bags/miura-sentinel-mackenzie-walker.jpg', 'images/feed/c79573e4-1ac06fa4bd4b1c281d1914f1b3f8d1da_f3017.jpg',
         'images/feed/25cf59a5-032a6e100c04f1e82e94f436485fc6fd_f3133.png']
for p in EXTRA:
    f = p.split('/')[-1]; orig = B + 'x-' + f
    src_p = orig if os.path.exists(orig) else p
    im = Image.open(src_p).convert('RGBA'); w0 = Image.new('RGBA', im.size, (255, 255, 255, 255)); w0.alpha_composite(im)
    a = np.asarray(w0.convert('RGB')).astype(int); k = 8  # transparent corners count as white
    cc = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3), a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    print(p, int(cc.min()), im.size)
    if cc.min() < 225: continue
    if not os.path.exists(orig): shutil.copy2(p, orig)
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); bg = bg.crop((3, 3, bg.width - 3, bg.height - 3)); CUR[0] = f
    out = frame(bg)
    out.save(p, optimize=True) if p.endswith('.png') else out.save(p, quality=86, optimize=True)
