#!/usr/bin/env python3
"""Render every /ig tile as a real 1080x1080 JPEG you can save.

WHY
---
/ig previously said "Screenshot a tile at 1:1 to get exact pixels" — the tiles
were HTML+CSS composites, so the only way to get a postable image was a manual
screenshot. This renders them as actual files instead.

HOW IT STAYS IN LOCKSTEP
It parses ig.html rather than re-deriving content from the feed. build-ig.py
stays the single source of truth for WHAT is on a tile; this script only
rasterises what that produced. Run it straight after build-ig.py.

LAYOUT — mirrored from the .tile CSS, which sets 1em = 10px at 1080px wide
(`font-size:min(10px,0.926vw)`, and 0.926vw of 1080 = 10px):

    canvas      1080 x 1080, --paper #F4F1EA
    image       top 68%  -> y 0..734. Crops are already exactly 1080x734,
                so they paste 1:1 with no resampling.
    .ig-lower   y 734..1080, padding 3.4em/5.8em/3.2em = 34 / 58 / 32 px
    .ig-logo    --mono 1.3em=13px, letter-spacing .24em=3.12px, uppercase,
                --grass #2D4A2B, margin-bottom 1.077em = 10.77px
    .ig-h       --serif bold 4.5em=45px, line-height 1.08, tracking -.015em,
                margin-bottom .356em = 16px
    .ig-p       --serif 2.7em=27px unless the tile carries an inline override
                (several do), line-height 1.4, opacity .8

FONTS
The site ships woff2, which PIL cannot read. The Editor's Note Text OTF/TTF
originals live in the connected font folders and are used here. If they are not
mounted the script REFUSES to run rather than silently substituting DejaVu —
a wrong typeface on a brand asset is worse than no asset.

Idempotent: skips a tile whose JPEG is newer than both ig.html and its crop.
"""
import os, re, sys, glob, html, zipfile, unicodedata
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
IMG_H = 734                      # 68% of 1080
PAD_X, PAD_TOP, PAD_BOT = 58, 34, 32
PAPER, INK, GRASS = (244, 241, 234), (20, 20, 20), (45, 74, 43)
OUT = "images/ig-tiles"
ZIP = "images/ig-tiles/all-tiles.zip"

FONT_DIRS = [
    "/sessions/admiring-pensive-ritchie/mnt/OTF",
    "/sessions/admiring-pensive-ritchie/mnt/TTF",
    os.path.expanduser("~/Downloads/Editor's Note Text/OTF"),
    os.path.expanduser("~/Downloads/Editor's Note Text/TTF"),
]


def find_font(*names):
    for d in FONT_DIRS:
        for n in names:
            for ext in (".otf", ".ttf"):
                p = os.path.join(d, n + ext)
                if os.path.exists(p):
                    return p
    return None


SERIF_R = find_font("Editor'sNoteText-Regular", "EditorsNoteText-Regular")
SERIF_B = find_font("Editor'sNoteText-Bold", "EditorsNoteText-Bold")
if not (SERIF_R and SERIF_B):
    sys.exit("Editor's Note Text OTF/TTF not found in any of:\n  " +
             "\n  ".join(FONT_DIRS) +
             "\nRefusing to substitute a different typeface on a brand asset.")

# JetBrains Mono is only used for the small uppercase logo line. If it isn't
# available, fall back to a mono the box does have — this is 13px of tracked-out
# caps, where the substitution is not meaningfully visible.
MONO = (find_font("JetBrainsMono-Regular", "JetBrainsMono-Medium")
        or "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def tx(s):
    """Entity-decode, strip tags, normalise whitespace."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def draw_tracked(d, xy, text, font, fill, tracking=0.0):
    """PIL has no letter-spacing; step glyph by glyph."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def wrap(d, text, font, max_w, tracking=0.0):
    def w_of(s):
        return d.textlength(s, font=font) + tracking * max(0, len(s) - 1)
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if w_of(t) <= max_w or not line:
            line = t
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def blend(fg, bg, a):
    return tuple(round(f * a + b * (1 - a)) for f, b in zip(fg, bg))


def parse(hhtml):
    """Split on the tile wrapper, THEN match within each chunk.

    The first version used one regex with several `.*?` spans across the whole
    document. On 186 tiles that backtracked badly enough to hang — it ran past
    two minutes with no output. Splitting first bounds every match to a few KB
    and the whole parse finishes instantly. Same lesson as the character-count
    card slicing: never let a lazy quantifier roam a whole page.
    """
    tiles = []
    chunks = hhtml.split('<div class="wrap">')[1:]
    for body in chunks:
        mu = re.search(r'<a href="(/drops/[^"]+)"', body)
        if not mu:
            continue
        url = mu.group(1)
        crops = re.findall(r"background-image:url\('([^']+)'\)", body)
        logo = re.search(r'<div class="ig-logo">(.*?)</div>', body, re.S)
        head = re.search(r'<div class="ig-h">(.*?)</div>', body, re.S)
        para = re.search(r'<div class="ig-p"([^>]*)>(.*?)</div>', body, re.S)
        psize = 27.0
        if para:
            sz = re.search(r'font-size:\s*([\d.]+)em', para.group(1))
            if sz:
                psize = float(sz.group(1)) * 10        # 1em = 10px
        tiles.append({
            "url": url,
            "slug": url.rsplit("/", 1)[-1],
            "crops": crops,
            "logo": tx(logo.group(1)) if logo else "",
            "head": tx(head.group(1)) if head else "",
            "para": tx(para.group(2)) if para else "",
            "psize": psize,
        })
    return tiles


def render(t, path):
    canvas = Image.new("RGB", (W, H), PAPER)

    if t["crops"]:
        src = t["crops"][0].lstrip("/")
        if os.path.exists(src):
            im = Image.open(src).convert("RGB")
            if im.size != (W, IMG_H):            # cover-crop to the slot
                s = max(W / im.width, IMG_H / im.height)
                im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
                l, tp = (im.width - W) // 2, (im.height - IMG_H) // 2
                im = im.crop((l, tp, l + W, tp + IMG_H))
            canvas.paste(im, (0, 0))

    d = ImageDraw.Draw(canvas)
    y = IMG_H + PAD_TOP
    max_w = W - PAD_X * 2

    if t["logo"]:
        f = ImageFont.truetype(MONO, 13)
        draw_tracked(d, (PAD_X, y), t["logo"].upper(), f, GRASS, 3.12)
        y += 13 + 10.77

    if t["head"]:
        f = ImageFont.truetype(SERIF_B, 45)
        for line in wrap(d, t["head"], f, max_w, -0.675):
            draw_tracked(d, (PAD_X, y), line, f, INK, -0.675)
            y += 45 * 1.08
        y += 16

    if t["para"]:
        size = t["psize"]
        f = ImageFont.truetype(SERIF_R, round(size))
        col = blend(INK, PAPER, 0.8)
        for line in wrap(d, t["para"], f, max_w):
            if y + size > H - PAD_BOT:           # clip like overflow:hidden
                break
            d.text((PAD_X, y), line, font=f, fill=col)
            y += size * 1.4

    canvas.save(path, "JPEG", quality=92, subsampling=0)


def main(apply_=False):
    src = "ig.html"
    hhtml = open(src, encoding="utf-8").read()
    tiles = parse(hhtml)
    print(f"  parsed {len(tiles)} tiles from {src}")

    n_img = sum(1 for t in tiles if t["crops"])
    odd = [t["slug"] for t in tiles if len(t["crops"]) != 1]
    if odd:
        print(f"  !! {len(odd)} tile(s) without exactly 1 crop: {odd[:4]}")
    print(f"  tiles with a crop: {n_img}   with headline: "
          f"{sum(1 for t in tiles if t['head'])}")

    if not apply_:
        print("\n(dry run — pass --apply to write JPEGs)")
        return tiles

    # FIVE SLUGS APPEAR TWICE on /ig, so keying files on slug alone silently
    # overwrote one of each pair — 186 tiles produced 181 files on the first
    # run. Three are Brand Revisited + Brand to Know cards that legitimately
    # point at the same upgraded page (the Revisited playbook edits in place
    # rather than creating a new URL), so BOTH tiles are wanted. Suffix the
    # repeats rather than dropping them.
    seen = {}
    for t in tiles:
        n = seen.get(t["slug"], 0) + 1
        seen[t["slug"]] = n
        t["file"] = t["slug"] if n == 1 else f"{t['slug']}-{n}"

    os.makedirs(OUT, exist_ok=True)
    src_mtime = os.path.getmtime(src)
    made = skipped = 0
    for t in tiles:
        p = f"{OUT}/{t['file']}.jpg"
        if os.path.exists(p) and os.path.getmtime(p) > src_mtime:
            skipped += 1
            continue
        render(t, p)
        made += 1
    print(f"  rendered {made}, skipped {skipped} up-to-date")

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_STORED) as z:
        for f in sorted(glob.glob(f"{OUT}/*.jpg")):
            z.write(f, os.path.basename(f))
    mb = os.path.getsize(ZIP) / 1e6
    print(f"  {ZIP}  ({mb:.1f} MB, {len(glob.glob(f'{OUT}/*.jpg'))} files)")
    return tiles


if __name__ == "__main__":
    main("--apply" in sys.argv)
