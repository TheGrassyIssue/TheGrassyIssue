#!/usr/bin/env python3
"""Usage: python3 dl.py <slug-n> <url>  -> downloads url, converts to img/<slug-n>.jpg (max 1600px long side, q85)"""
import sys, subprocess, os
from PIL import Image
base = os.path.dirname(os.path.abspath(__file__))
name, url = sys.argv[1], sys.argv[2]
tmp = os.path.join(base, 'tmp', name + '.raw')
os.makedirs(os.path.dirname(tmp), exist_ok=True)
r = subprocess.run(['curl','-sL','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','-o',tmp,'-w','%{http_code}',url],capture_output=True,text=True)
if r.stdout.strip()!='200': print('HTTP',r.stdout); sys.exit(1)
try:
    im = Image.open(tmp)
except Exception as e:
    print('NOT AN IMAGE (maybe avif/svg):', e); sys.exit(1)
if im.mode in ('RGBA','LA','P'):
    im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255,255,255)); bg.paste(im, mask=im.split()[-1]); im = bg
else:
    im = im.convert('RGB')
im.thumbnail((1600,1600))
out = os.path.join(base,'img',name+'.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
im.save(out,'JPEG',quality=85)
print('OK', out, im.size)
