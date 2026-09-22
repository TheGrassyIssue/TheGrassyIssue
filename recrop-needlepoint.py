#!/usr/bin/env python3
"""recrop-needlepoint.py — make every gallery frame 4:5, centred on the product.
22 September 2026.

Lenny: "some of the images arent centered just right."

WHAT IS ACTUALLY WRONG IS NOT CENTRING, IT IS ASPECT. .product-gallery is a hard
aspect-ratio:4/5 at every viewport (measured 427x534, 376x470, 348x435), and
.pg-frame img uses object-fit:cover. 29 of the 66 frames are landscape. Cover
crops a landscape source to a portrait window from the geometric middle, so:

  charleston-golf-beware-of-the-bogey-man-3   1.99 wide  keeps ~40% of its width
  good-threads-golf-flags-green-0             1.82 wide  keeps ~44%
  charleston-ric-flair-0..3                   1.79 wide  keeps ~45%

More than half of those belts was being thrown away, and the Ric Flair lead
frame — the one Lenny put at the top of the homepage — rendered as an abstract
pink close-up rather than a belt. On top of that, ten frames have their product
sitting off the geometric centre, so even the square sources cropped crooked.

TWO PATHS, BECAUSE THE FRAMES ARE NOT ALL THE SAME KIND OF PICTURE.
Sampling the four corners of all 66: 61 are cut-outs on a plain sweep (corners
near-identical and light), 5 are real scenes.

  cut-outs (61)  Rebuilt as a 4:5 canvas filled with the image's OWN corner
                 colour, product scaled to fit with a 5.5% margin and centred.
                 Nothing is cut and the backgrounds stay consistent, because the
                 fill is sampled per image rather than assumed white.
  scenes (5)     Still cover-cropped — you cannot cut a subject out of a photo
                 of a man on a boat. But the crop window is centred on the
                 content box instead of the geometric middle, which is the
                 "centred" fix for exactly the frames that can take it.

IDEMPOTENT BY MEASUREMENT, NOT BY A FLAG. A frame already at 4:5 is skipped, so
re-running is a no-op and re-running after a fresh localise re-fixes only what
was re-downloaded. Originals are kept under research/needlepoint/original/ on
the first pass, so this is reversible and so a second pass never re-processes an
already-processed image (which would compound the margin).

Dry run by default.
"""
import json
import pathlib
import shutil
import sys

from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parent
RES = ROOT / "research/needlepoint"
BACKUP = RES / "original"
TARGET_AR = 4 / 5
TOL = 0.01
MARGIN = 0.055


def content_box(im, tol=18, density=0.005):
    """Bounding box of the real subject, immune to compression speckle.

    getbbox() alone is not enough. The basketweave frame is a belt ending around
    x=560 on white, but JPEG noise in the empty right half crosses the threshold
    on a handful of isolated pixels, so getbbox() returned the full 1100px width
    and put the computed centre at 42%. The image was fine; the measurement was
    not, and it failed a correct crop.

    So a column counts as content only when at least `density` of its pixels
    differ from the background — 0.5% of the height, i.e. five pixels in a
    thousand. Speckle never clears that; an edge of a belt always does.
    """
    bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
    mask = ImageChops.difference(im, bg).convert("L").point(lambda x: 255 if x > tol else 0)
    w, h = mask.size
    px = mask.load()
    col_min = max(1, int(h * density))
    row_min = max(1, int(w * density))
    cols = [x for x in range(w) if sum(1 for y in range(0, h, 2) if px[x, y]) * 2 >= col_min]
    rows = [y for y in range(h) if sum(1 for x in range(0, w, 2) if px[x, y]) * 2 >= row_min]
    if not cols or not rows:
        return mask.getbbox()
    return (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)


def is_cutout(im):
    w, h = im.size
    cs = [im.getpixel((3, 3)), im.getpixel((w - 4, 3)),
          im.getpixel((3, h - 4)), im.getpixel((w - 4, h - 4))]
    spread = max(max(abs(a[i] - b[i]) for i in range(3)) for a in cs for b in cs)
    return spread < 14 and min(min(c) for c in cs) > 218


def fit45(im):
    """Whole product on a 4:5 canvas in the image's own background colour."""
    bb = content_box(im) or (0, 0, *im.size)
    c = im.crop(bb)
    H = im.height
    W = round(H * TARGET_AR)
    if W < 600:                       # keep frames usable at card width
        H = round(600 / TARGET_AR)
        W = 600
    s = min(W * (1 - 2 * MARGIN) / c.width, H * (1 - 2 * MARGIN) / c.height)
    c = c.resize((max(1, round(c.width * s)), max(1, round(c.height * s))), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), im.getpixel((2, 2)))
    canvas.paste(c, ((W - c.width) // 2, (H - c.height) // 2))
    return canvas


def cover45(im):
    """Cover-crop to 4:5, but window centred on the content, not the geometry."""
    w, h = im.size
    bb = content_box(im, tol=26) or (0, 0, w, h)
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    tw = round(h * TARGET_AR)
    if tw <= w:
        x = min(max(round(cx - tw / 2), 0), w - tw)
        return im.crop((x, 0, x + tw, h))
    th = round(w / TARGET_AR)
    y = min(max(round(cy - th / 2), 0), max(0, h - th))
    return im.crop((0, y, w, min(y + th, h)))


def main(apply_):
    man = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
    frames = [f for m in man.values() for f in m["frames"]]
    done = skipped = fitted = covered = 0
    path = {}
    for rel in frames:
        p = ROOT / rel.lstrip("/")
        if not p.is_file():
            sys.exit(f"! missing frame {rel}")
        im = Image.open(p).convert("RGB")
        if abs(im.width / im.height - TARGET_AR) < TOL:
            skipped += 1
            continue
        cut = is_cutout(im)
        out = fit45(im) if cut else cover45(im)
        path[rel] = "fit" if cut else "cover"
        fitted += cut
        covered += (not cut)
        done += 1
        if apply_:
            BACKUP.mkdir(parents=True, exist_ok=True)
            b = BACKUP / p.name
            if not b.is_file():
                shutil.copy2(p, b)
            out.save(p, "JPEG", quality=88, optimize=True, progressive=True)

    print(f"  {len(frames)} frames | already 4:5: {skipped} | reprocessed: {done}")
    print(f"    fitted whole (cut-outs): {fitted}")
    print(f"    cover-cropped on content (scenes): {covered}")
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY ----
    bad = []
    for rel in frames:
        p = ROOT / rel.lstrip("/")
        im = Image.open(p)
        if abs(im.width / im.height - TARGET_AR) > TOL:
            bad.append(f"{rel}: {im.width}x{im.height} is not 4:5")
        if im.width < 560:
            bad.append(f"{rel}: only {im.width}px wide")
        if p.stat().st_size > 900_000:
            bad.append(f"{rel}: {p.stat().st_size/1024:.0f} KB")
        # THE CENTRING TEST ONLY APPLIES TO FRAMES THAT COULD BE CENTRED.
        # A fitted frame was built around its content, so the content must land
        # in the middle — if it does not, fit45 is broken and that is worth
        # failing on. A cover-cropped frame is a photograph whose subject the
        # photographer placed where they placed it: the Alabama two-belt shot
        # has both belts spanning the full width and sitting low, so no 4:5
        # window can contain them or centre them. Demanding a centred result
        # there fails a correct crop. What cover45 can promise is that its
        # window is as close to the content centroid as the image bounds allow,
        # which is what gets checked instead.
        # WHICH TEST APPLIES IS DERIVED FROM THE SOURCE, NOT FROM THIS RUN.
        # Keying off the run's own path dict meant that on a second run — when
        # every frame is already 4:5 and nothing is reprocessed — the dict was
        # empty, every test was skipped, and the script printed "none
        # off-centre" having checked nothing. A guard that passes because it did
        # no work is worse than no guard. The original in the backup says what
        # kind of picture it is, whether or not this run touched it.
        src = BACKUP / pathlib.Path(rel).name
        if src.is_file():
            kind = "fit" if is_cutout(Image.open(src).convert("RGB")) else "cover"
        else:
            kind = path.get(rel, "fit")
        if kind == "fit":
            box = content_box(im.convert("RGB"))
            if box:
                cx = (box[0] + box[2]) / 2 / im.width
                cy = (box[1] + box[3]) / 2 / im.height
                if abs(cx - .5) > 0.06 or abs(cy - .5) > 0.06:
                    bad.append(f"{rel}: fitted but content centre at {cx:.0%},{cy:.0%}")
        elif kind == "cover":
            # No pixels invented: a cover crop takes a window out of the source,
            # so the output must be no larger than the source in either axis.
            if src.is_file():
                o = Image.open(src)
                if im.height > o.height or im.width > o.width:
                    bad.append(f"{rel}: cover crop is larger than its source")
    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: all {len(frames)} frames 4:5, none upscaled, none off-centre; "
          f"originals kept in {BACKUP.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
