#!/usr/bin/env python3
"""localize-axxa-life.py — hero + lookbook frames for the AXXA piece. 20 Sept 2026.

AXXA's product photography is the argument the brand is making. They claim to sit
"in the space between surf, golf, and everyday life", and the shoot backs it up:
the same pieces appear on a fairway at golden hour and on a clifftop above the
surf. Prose can assert that. Two bands of their own frames demonstrate it, which
is why this piece gets lookbook imagery rather than product cut-outs alone.

HERO. Their catalogue is 4:5 portrait almost end to end — of 120 images at or
above 1600px, 105 are portrait and the 15 landscape ones belong to sold-out
products. So the house 1600x685 (2.34:1) hero has to be cut from a portrait
frame, which throws away roughly two thirds of the height. BIAS is the vertical
centre of that band as a fraction of the source height.

WHICH FRAME, DECIDED BY LOOKING. The first attempt used AKL08350 (a model on a
fairway) at bias 0.40 on the reasoning that it had horizontal room. Rendered, it
was a head-and-shoulders portrait with the cap sliced off the top — a headshot,
not a hero, and the garment barely present. Sweeping the bias did not rescue it:
0.55 and 0.68 just walked down the same body, trading a cut-off face for an
anonymous torso. A 2.34:1 band out of 4:5 is always going to be a narrow slice,
so the frame has to be one that reads as a scene at that shape, not one that
merely contains a scene.

AKL08461 does. At 0.45 the band holds a fairway, a pair of arms lowering a cap,
and the embroidery on that cap — "Surf in the morning, Golf in the arvo" — large
enough to read. That sentence is the whole brand thesis, already written on the
product, which makes it a better opening image than any crop of a jumper.

Everything is downloaded and served locally. Nothing hot-links.
Idempotent. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/axxa"
CDN = "https://cdn.shopify.com/s/files/1/0750/2561/3077/files/"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}

HERO_SRC, HERO_BIAS = "AKL08461.jpg", 0.45
HERO_W, HERO_H = 1600, 685

# Band A sits directly under the opening copy: the thesis in three frames —
# coast, course, coast. Band B sits lower, after the products.
BAND_A = [("life-coast-knit", "AKL00012.jpg"),
          ("life-course-tee", "AKL08293.jpg"),
          ("life-coast-hoodie", "AKL01010.jpg")]
BAND_B = [("life-pair-hoodies", "AKL00719.jpg"),
          ("life-sunset-pair", "AKL00815.jpg"),
          ("life-cream-tee", "AKL00595.jpg"),
          ("life-back-graphic", "AKL00704.jpg"),
          ("life-cap-course", "AKL08461.jpg"),
          ("life-cap-held", "AKL08484.jpg")]
SQUARE = 1000


def fetch(name):
    req = urllib.request.Request(CDN + name, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read()


def main(apply_):
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []

    def save(dest, im, label):
        if dest.exists():
            skipped.append(dest.name); return
        if not apply_:
            made.append((dest.name, label)); return
        im.save(dest, "JPEG", quality=88, optimize=True)
        made.append((dest.name, label))

    # ---- hero -------------------------------------------------------------
    hero = OUT / "hero.jpg"
    if hero.exists():
        skipped.append("hero.jpg")
    else:
        try:
            im = Image.open(io.BytesIO(fetch(HERO_SRC))).convert("RGB")
            target = HERO_W / HERO_H
            cw = im.width
            ch = round(cw / target)
            if ch > im.height:                      # frame too short: cut width
                ch = im.height
                cw = round(ch * target)
            cx = (im.width - cw) // 2
            cy = max(0, min(im.height - ch, round(im.height * HERO_BIAS - ch / 2)))
            im = im.crop((cx, cy, cx + cw, cy + ch)).resize((HERO_W, HERO_H),
                                                            Image.LANCZOS)
            if apply_:
                im.save(hero, "JPEG", quality=88, optimize=True)
            made.append(("hero.jpg", f"{HERO_SRC} -> {HERO_W}x{HERO_H}"))
        except Exception as e:
            failed.append(("hero.jpg", str(e)[:70]))

    # ---- lookbook squares -------------------------------------------------
    for slug, src in BAND_A + BAND_B:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(dest.name); continue
        if not apply_:
            made.append((dest.name, f"would crop {src}")); continue
        try:
            im = Image.open(io.BytesIO(fetch(src))).convert("RGB")
            s = min(im.size)
            # Square from the UPPER portion, not the centre. These are full-body
            # 4:5 frames; a centred square lands on waists and legs.
            cx = (im.width - s) // 2
            cy = min(im.height - s, round(im.height * 0.10))
            im = im.crop((cx, cy, cx + s, cy + s)).resize((SQUARE, SQUARE),
                                                          Image.LANCZOS)
            im.save(dest, "JPEG", quality=88, optimize=True)
            made.append((dest.name, f"{src} -> {SQUARE}x{SQUARE}"))
        except Exception as e:
            failed.append((dest.name, str(e)[:70]))

    for n, d in made:
        print(f"  ok    {n:24} {d}")
    for n in skipped:
        print(f"  skip  {n:24} already local")
    for n, e in failed:
        print(f"  FAIL  {n:24} {e}")

    if failed:
        sys.exit(f"\n! {len(failed)} failed")
    if apply_:
        want = {"hero.jpg"} | {f"{s}.jpg" for s, _ in BAND_A + BAND_B}
        have = {p.name for p in OUT.glob("*.jpg")}
        missing = want - have
        if missing:
            sys.exit(f"\n! missing: {sorted(missing)}")
        print(f"\n  hero + {len(BAND_A) + len(BAND_B)} lookbook frames local")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
