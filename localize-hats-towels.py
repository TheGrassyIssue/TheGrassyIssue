#!/usr/bin/env python3
"""localize-hats-towels.py — pull every product image local at the house square.

Never hot-link: house rule. Product squares are 1200x1200, centre-cropped from
the brand's own image. Sources under 1200 are NOT upscaled — they are written at
their honest size and reported, same as the Vuori masthead.
"""
import json, urllib.request, io, os, sys
from PIL import Image
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
SQ=1200
OUT="images/hats-towels"
items=[("hat",i) for i in json.load(open("research/hats/grid18.json"))] + \
      [("towel",i) for i in json.load(open("research/towels/grid.json"))]
os.makedirs(OUT,exist_ok=True)
notes=[];small=[]
for kind,it in items:
    name=f"{kind}-{it['brand']}.jpg"; p=f"{OUT}/{name}"
    if os.path.exists(p):
        notes.append(f"{name} already local"); continue
    try:
        raw=urllib.request.urlopen(urllib.request.Request(it["img"],headers=UA),timeout=30).read()
    except Exception as e:
        sys.exit(f"! {name}: {e}")
    im=Image.open(io.BytesIO(raw)).convert("RGB"); w,h=im.size
    side=min(w,h); target=min(SQ,side)          # the no-upscale clamp
    cx,cy=(w-side)//2,(h-side)//2
    im.crop((cx,cy,cx+side,cy+side)).resize((target,target),Image.LANCZOS)\
      .save(p,"JPEG",quality=88,optimize=True,progressive=True)
    notes.append(f"{name} {target}x{target} from {w}x{h}")
    if target<SQ: small.append((name,target,f"{w}x{h}"))
for n in notes: print("  "+n)
bad=[]
for kind,it in items:
    p=f"{OUT}/{kind}-{it['brand']}.jpg"
    if not os.path.isfile(p): bad.append(f"{p} missing")
    else:
        im=Image.open(p)
        if im.width!=im.height: bad.append(f"{p} not square ({im.width}x{im.height})")
if bad: sys.exit("! "+"; ".join(bad))
print(f"\n  verified: {len(items)} squares on disk, all square, none upscaled")
if small:
    print(f"  {len(small)} below the {SQ}px house square (source was smaller — left honest):")
    for n,t,s in small: print(f"     {n} {t}px from {s}")
