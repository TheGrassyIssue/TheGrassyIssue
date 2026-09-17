#!/usr/bin/env python3
"""Localize every image for the late-season putter switch roundup.

HOUSE RULE: download ALL product imagery, never hot-link. Six of these twenty
brands serve from Shopify's CDN, which is permissive enough that hot-linking
would work -- which is exactly why we do not.

SIZE: 800x1000 (4:5), the product-card size used by every roundup on the site
(see images/divot-tools). Crop is centred on the product's own ink rather than
the frame centre, because several of these are wide packshots where a centre
crop slices the head. Same ink_box/crop_to pair as localize-apres.py.

SOURCE: research/putter-switch-2026.json. Every URL in there was read off the
brand's own live product page on 2026-09-16, not off a retailer.

OUTPUT: images/putter-switch/<key>.jpg, -a2, -a3, -a4

FORMAT NOTE: Sub 70 serves .webp, Ping/Roark/Bettinardi/Vice serve .png with
transparency, Mizuno serves .webp. PIL reads all three; the alpha channel is
composited onto white before the crop or the saved JPEG gets a black backdrop.

Idempotent: skips any file already written. Re-run freely.
"""
import json, os, time, urllib.request
from PIL import Image, ImageChops

SRC = "research/putter-switch-2026.json"
OUT = "images/putter-switch"
CACHE = "research/putter-switch-raw"
PW, PH = 800, 1000
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"}


def fetch(url, path):
    """Cache one remote image locally.

    Zero-byte caches count as MISSES, not hits -- a truncated first download
    that os.path.exists() later treats as a hit is the failure mode that cost
    us an hour on the Apres run.
    """
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) > 1024:
                open(path, "wb").write(data)
                time.sleep(0.3)
                return path
        except Exception as e:
            print(f"       retry {attempt + 1}: {e}")
        time.sleep(2 * (attempt + 1))
    return None


def flatten(im):
    """Composite any alpha onto white. Several of these are transparent PNGs."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, im).convert("RGB")
    return im.convert("RGB")


def ink_box(im):
    """Bounding box of everything that is not the white backdrop.

    Returns None when the 'ink' fills the frame -- that is a lifestyle shot,
    not a packshot, and the caller falls back to a centre crop.
    """
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).convert("L").point(
        lambda p: 255 if p > 18 else 0).getbbox()
    if not bb:
        return None
    w, h = im.size
    if (bb[2] - bb[0]) > w * 0.97 and (bb[3] - bb[1]) > h * 0.97:
        return None
    return bb


def crop_to(im, tw, th):
    im = flatten(im)
    ar = tw / th
    w, h = im.size
    bb = ink_box(im)
    cx = ((bb[0] + bb[2]) / 2) if bb else w / 2
    cy = ((bb[1] + bb[3]) / 2) if bb else h / 2

    if w / h > ar:
        ch, cw = h, int(h * ar)
    else:
        cw, ch = w, int(w / ar)

    # A putter photographed side-on is often wider than the 4:5 window. Pad out
    # rather than slice the toe off.
    if bb and (bb[2] - bb[0]) > cw:
        need_h = int((bb[2] - bb[0]) / ar)
        pad = Image.new("RGB", (w, max(h, need_h)), (255, 255, 255))
        pad.paste(im, (0, (max(h, need_h) - h) // 2))
        im = pad
        w, h = im.size
        cw, ch = w, int(w / ar)
        cx, cy = w / 2, h / 2

    # Pad the source out to at least the crop window before cropping. Without
    # this, a wide packshot padded above leaves ch > h and PIL fills the
    # overflow with BLACK, which showed up as a bar under the MacGregor, Cobra
    # and Vice frames on the first contact sheet.
    if cw > w or ch > h:
        canvas = Image.new("RGB", (max(w, cw), max(h, ch)), (255, 255, 255))
        canvas.paste(im, ((max(w, cw) - w) // 2, (max(h, ch) - h) // 2))
        im = canvas
        cx += (max(w, cw) - w) / 2
        cy += (max(h, ch) - h) / 2
        w, h = im.size

    l = int(max(0, min(cx - cw / 2, w - cw)))
    t = int(max(0, min(cy - ch / 2, h - ch)))
    return im.crop((l, t, l + cw, t + ch)).resize((tw, th), Image.LANCZOS)


def main():
    data = json.load(open(SRC))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    rows = data["picks"] + data["presale"]

    # Guard: Makefield publishes the same frame on two different product records.
    # If the same CDN file ends up on two cards the reader sees one putter twice.
    seen = {}
    for r in rows:
        for u in r["imgs"]:
            # Last TWO path segments, not just the filename: Sub 70 names every
            # clubshot 1.webp/2.webp inside a per-model directory, so a
            # filename-only key collides across models that share nothing.
            stem = "/".join(u.split("?")[0].split("/")[-2:])
            if stem in seen and seen[stem] != r["key"]:
                raise SystemExit(
                    f"{stem} is assigned to both {seen[stem]} and {r['key']} -- "
                    f"two cards would show the same photograph")
            seen[stem] = r["key"]

    made = skipped = 0
    for r in rows:
        got = []
        for i, u in enumerate(r["imgs"]):
            dst = f"{OUT}/{r['key']}.jpg" if i == 0 else f"{OUT}/{r['key']}-a{i + 1}.jpg"
            if os.path.exists(dst) and os.path.getsize(dst) > 1024:
                got.append(dst)
                continue
            # Some frames are good photographs with an award badge composited into
            # a corner. PRE_CROP trims that corner off before the 4:5 crop runs.
            # This removes an overlay the brand added on top of the photograph; it
            # does not retouch the product.
            pre = (r.get("pre_crop") or {}).get(str(i))
            ext = ".webp" if ".webp" in u.lower() else (".png" if ".png" in u.lower() else ".jpg")
            raw = fetch(u, f"{CACHE}/{r['key']}-{i}{ext}")
            if not raw:
                print(f"     !! {r['key']} frame {i + 1} unavailable, skipped")
                skipped += 1
                continue
            try:
                src = Image.open(raw)
                if pre:
                    w0, h0 = src.size
                    src = flatten(src).crop((int(pre[0] * w0), int(pre[1] * h0),
                                             int(pre[2] * w0), int(pre[3] * h0)))
                crop_to(src, PW, PH).save(dst, quality=88)
            except Exception as e:
                print(f"     !! {r['key']} frame {i + 1} undecodable ({e}), skipped")
                os.remove(raw)
                skipped += 1
                continue
            made += 1
            got.append(dst)
        price = r["price"]
        print(f"  {r['key']:16} {r['brand']:16} {len(got)} frame(s)  ${price:,.2f}")

    # The 21:9 header band. It has to be a frame no card uses — the build guard
    # fails the page if any image appears on it twice.
    h = data.get("hero")
    if h and not os.path.exists(h["out"]):
        raw = fetch(h["url"], f"{CACHE}/hero.jpg")
        if raw:
            crop_to(Image.open(raw), *h["size"]).save(h["out"], quality=88)
            made += 1
            print(f"  {'hero':16} {'':16} {h['size'][0]}x{h['size'][1]}")

    print(f"\nwrote {made} new file(s); {skipped} frame(s) skipped")
    thin = [r["key"] for r in rows
            if len([1 for i in range(len(r["imgs"]))
                    if os.path.exists(f"{OUT}/{r['key']}.jpg" if i == 0
                                      else f"{OUT}/{r['key']}-a{i + 1}.jpg")]) < 3]
    if thin:
        print("thin galleries (<3 frames), re-source before building: " + ", ".join(thin))


if __name__ == "__main__":
    main()
