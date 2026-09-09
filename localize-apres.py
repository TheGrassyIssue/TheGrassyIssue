#!/usr/bin/env python3
"""Localize every Après Golf image at house sizes.

WHY THIS EXISTS
---------------
House rule: download ALL product imagery, never hot-link (see the site's image
sourcing playbook). Après serves from Shopify's CDN, which is a permissive host,
which is exactly why it is tempting to hot-link and exactly why we do not.

SIZES
  products : 800x1000 (4:5)  -> images/apres-golf/<slug>.jpg, -a2, -a3 ...
  hero     : 1600x685 (21:9) -> images/apres-golf/hero.jpg

CROP NOTE: Après shoots on white seamless with the cover standing vertically,
often as a 3-piece set (driver / fairway / hybrid) laid side by side. A centred
4:5 crop of a WIDE set shot slices the outer two covers in half. So the crop is
centred on the image's own ink: we find the bounding box of non-white pixels and
centre the crop on that, which keeps a 3-piece set whole when it fits and
centres on the driver when it does not.

Idempotent: skips any file already written. Re-run freely.
"""
import json, os, io, sys, time, urllib.request
from PIL import Image, ImageChops

SRC = "research/apres/all.json"
OUT = "images/apres-golf"
CACHE = "research/apres/raw"
PW, PH = 800, 1000
HW, HH = 1600, 685

# slug -> (handle, frames_to_take)
LINEUP = json.load(open("research/apres/lineup.json"))


def fetch(url, path):
    """Cache one CDN image locally.

    Zero-byte caches are treated as MISSES, not hits. A truncated/failed
    download on the first run left an empty sweater-jack-1.jpg behind, and
    because os.path.exists() was the only check, every later run happily
    "found" it and then died in Image.open with UnidentifiedImageError.
    """
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path
    req = urllib.request.Request(url.split("?")[0] + "?width=1400",
                                 headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) > 1024:
                open(path, "wb").write(data)
                time.sleep(0.35)
                return path
        except Exception as e:
            print(f"     retry {attempt+1}: {e}")
        time.sleep(2 * (attempt + 1))
    return None


def ink_box(im):
    """Bounding box of everything that is not the white backdrop.

    Shopify packshots are on pure white. difference() against a white plate
    leaves the product; getbbox() gives its extent. Returns None on lifestyle
    shots that fill the frame (no white margin to subtract), and the caller
    falls back to a centre crop.
    """
    g = im.convert("RGB")
    bg = Image.new("RGB", g.size, (255, 255, 255))
    bb = ImageChops.difference(g, bg).convert("L").point(lambda p: 255 if p > 18 else 0).getbbox()
    if not bb:
        return None
    w, h = im.size
    # if the "ink" is basically the whole frame it is not a packshot
    if (bb[2] - bb[0]) > w * 0.97 and (bb[3] - bb[1]) > h * 0.97:
        return None
    return bb


def crop_to(im, tw, th):
    ar = tw / th
    w, h = im.size
    bb = ink_box(im)
    cx = ((bb[0] + bb[2]) / 2) if bb else w / 2
    cy = ((bb[1] + bb[3]) / 2) if bb else h / 2

    if w / h > ar:                      # too wide -> full height, crop width
        ch = h
        cw = int(h * ar)
    else:                               # too tall -> full width, crop height
        cw = w
        ch = int(w / ar)

    # If a packshot's ink is wider than the crop window, we would slice the
    # outer covers of a 3-piece set. Pad out to the target ratio instead.
    if bb and (bb[2] - bb[0]) > cw:
        need_h = int((bb[2] - bb[0]) / ar)
        pad = Image.new("RGB", (w, max(h, need_h)), (255, 255, 255))
        pad.paste(im.convert("RGB"), (0, (max(h, need_h) - h) // 2))
        im = pad
        w, h = im.size
        cw, ch = w, int(w / ar)
        cx, cy = w / 2, h / 2

    l = int(max(0, min(cx - cw / 2, w - cw)))
    t = int(max(0, min(cy - ch / 2, h - ch)))
    return im.crop((l, t, l + cw, t + ch)).convert("RGB").resize((tw, th), Image.LANCZOS)


def main():
    cat = json.load(open(SRC))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    made = miss = 0
    for slug, spec in LINEUP.items():
        handle, nframes = spec["handle"], spec.get("frames", 3)
        p = cat.get(handle)
        if not p:
            print(f"  !! {slug:34} handle not in catalogue: {handle}")
            miss += 1
            continue
        urls = p["imgs"][:nframes]
        for i, u in enumerate(urls):
            dst = f"{OUT}/{slug}.jpg" if i == 0 else f"{OUT}/{slug}-a{i+1}.jpg"
            if os.path.exists(dst):
                continue
            raw = fetch(u, f"{CACHE}/{slug}-{i}.jpg")
            if not raw:
                print(f"     !! {slug} frame {i+1} unavailable, skipped")
                continue
            try:
                crop_to(Image.open(raw), PW, PH).save(dst, quality=88)
            except Exception as e:
                print(f"     !! {slug} frame {i+1} undecodable ({e}), skipped")
                os.remove(raw)
                continue
            made += 1
        print(f"  {slug:34} {len(urls)} frame(s)  ${p['price']:.0f}  "
              f"{'IN' if p['avail'] else 'OUT'}")
    print(f"\nwrote {made} new file(s); {miss} handle(s) missing")


if __name__ == "__main__":
    main()
