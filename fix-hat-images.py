#!/usr/bin/env python3
"""fix-hat-images.py — repair the product squares on The Hat & Towel Edit.
21 September 2026.

Lenny: "some of the hat images are messed up".

THE BUG, AND WHY NOTHING CAUGHT IT.
localize-hats-towels.py does `Image.open(...).convert("RGB")`. On an RGBA
source that maps every transparent pixel to BLACK, not white. Two of the
eighteen hat sources are transparent PNG cutouts:
    eastside-golf  1365x2048 RGBA  -> black wedges around the cap
    sunday-golf    1500x1500 RGBA  -> a grey-black box behind the cap
    ghost-golf     2160x2700 RGBA  -> a pale towel adrift on a full black field
Its verification block checked that each file existed, was square, and was not
upscaled. All three were true of a picture with a black rectangle through it.
The guard measured the geometry and never looked at the picture — the same
mistake as the donor-bleed hero earlier today.

A third image was wrong for an unrelated reason:
    morning-people-clothiers  1024x1535 RGB, an on-model portrait. A centre
    crop of a 1535-tall frame takes rows 255..1279; the cap sits high in the
    frame, so the crown was sliced off. It needs a top-biased crop, not a
    different picture.

THE REPAIR.
  * RGBA sources are composited onto WHITE, then cropped to the alpha bounding
    box and padded back to square with a 7% margin — which is what a cutout
    wants anyway, and incidentally fixes the framing as well as the colour.
  * RGB sources keep the centre crop, with a per-item vertical bias where the
    subject is not centred.
  * Nothing is upscaled; the clamp from the original script is kept.

VERIFICATION LOOKS AT PIXELS THIS TIME. Every output is checked for dark
corners against a light body (the alpha-on-black signature) and for a
low-variance border band (a letterboxed or pillarboxed source). Those two
checks are run over ALL THIRTY images, not just the three being repaired, so
any other instance is reported rather than assumed absent.

Idempotent: re-running reproduces byte-identical output. Dry run by default.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/hats-towels"
SQ = 1200
MARGIN = 0.07
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}

# vertical crop bias for RGB sources whose subject is not centred
# 0.0 = flush top, 0.5 = centre (default), 1.0 = flush bottom
BIAS = {"morning-people-clothiers": 0.12}

# only these are rewritten; the other 27 are checked but left alone
REPAIR = {"eastside-golf", "sunday-golf", "morning-people-clothiers", "ghost-golf"}


def items():
    hats = [("hat", i) for i in json.load(open(ROOT / "research/hats/grid18.json"))]
    tows = [("towel", i) for i in json.load(open(ROOT / "research/towels/grid.json"))]
    return hats + tows


def square(raw, bias):
    """Return a square RGB image, alpha composited onto white."""
    im = Image.open(io.BytesIO(raw))
    if "A" in im.getbands():
        im = im.convert("RGBA")
        alpha = im.getchannel("A")
        if alpha.getextrema()[0] < 250:          # genuinely transparent
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=alpha)             # WHITE, not black
            box = alpha.getbbox() or (0, 0, *im.size)
            sub = bg.crop(box)
            side = round(max(sub.size) * (1 + 2 * MARGIN))
            out = Image.new("RGB", (side, side), (255, 255, 255))
            out.paste(sub, ((side - sub.width) // 2, (side - sub.height) // 2))
            return out, f"cutout on white, trimmed to content ({sub.size[0]}x{sub.size[1]})"
        im = im.convert("RGB")
    else:
        im = im.convert("RGB")
    w, h = im.size
    side = min(w, h)
    cx = (w - side) // 2
    cy = round((h - side) * bias)
    return im.crop((cx, cy, cx + side, cy + side)), f"centre crop, bias {bias}"


def look(p):
    """Pixel checks. Geometry is not enough — this is what was missed."""
    im = Image.open(p).convert("RGB")
    n = im.width
    body = ImageStat.Stat(im.crop((n // 4, n // 4, 3 * n // 4, 3 * n // 4))).mean
    body_l = sum(body) / 3
    k = max(8, n // 20)
    corners = [im.crop((0, 0, k, k)), im.crop((n - k, 0, n, k)),
               im.crop((0, n - k, k, n)), im.crop((n - k, n - k, n, n))]
    cl = [sum(ImageStat.Stat(c).mean) / 3 for c in corners]
    bad = []
    # THE SIGNATURE IS FLAT PURE BLACK ON ALL FOUR CORNERS, not merely "dark".
    # A first version flagged any dark corner and cried wolf on two legitimate
    # photographs: Kingfisher (cap in a box on a patterned floor, one corner at
    # mean 27) and Sierra Madre (towel on grass in shadow, three corners in the
    # 40s). Real photographs have texture — their dark corners carry stddev 13
    # to 48. The alpha artefact is mean 0.0, stddev 0.00, on every corner.
    cs = [ImageStat.Stat(c).stddev for c in corners]
    csd = [sum(s) / 3 for s in cs]
    if body_l > 110 and all(m < 12 for m in cl) and all(s < 3 for s in csd):
        bad.append(f"all four corners flat black (mean {max(cl):.0f}, "
                   f"stddev {max(csd):.1f}) against a light body ({body_l:.0f}) "
                   f"— alpha flattened onto black")
    # a uniform band down both sides is a pillarboxed source
    edge = max(4, n // 100)
    l = ImageStat.Stat(im.crop((0, 0, edge, n))).mean
    r = ImageStat.Stat(im.crop((n - edge, 0, n, n))).mean
    if abs(sum(l) / 3 - sum(r) / 3) < 4 and 60 < sum(l) / 3 < 200:
        bad.append(f"uniform mid-grey side bands ({sum(l)/3:.0f}) — letterboxed source")
    return bad


def main(apply_):
    todo = [(k, i) for k, i in items() if i["brand"] in REPAIR]
    if len(todo) != len(REPAIR):
        sys.exit(f"! only found {len(todo)} of {len(REPAIR)} to repair")

    for kind, it in todo:
        name = f"{kind}-{it['brand']}.jpg"
        raw = urllib.request.urlopen(
            urllib.request.Request(it["img"], headers=UA), timeout=40).read()
        im, how = square(raw, BIAS.get(it["brand"], 0.5))
        target = min(SQ, im.width)               # never upscale
        im = im.resize((target, target), Image.LANCZOS)
        print(f"  {name}: {how} -> {target}x{target}")
        if apply_:
            im.save(OUT / name, "JPEG", quality=88, optimize=True, progressive=True)

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- LOOK AT ALL THIRTY, NOT JUST THE THREE ----
    flags = []
    for kind, it in items():
        p = OUT / f"{kind}-{it['brand']}.jpg"
        if not p.is_file():
            flags.append(f"{p.name}: missing"); continue
        for b in look(p):
            flags.append(f"{p.name}: {b}")
    if flags:
        sys.exit("! pixel checks failed:\n    " + "\n    ".join(flags))
    print(f"\n  verified: {len(items())} squares, no dark-corner alpha artefacts, "
          f"no letterboxed sources")


if __name__ == "__main__":
    main("--apply" in sys.argv)
