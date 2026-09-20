#!/usr/bin/env python3
"""localize-pants-lookbook.py — the in-body photographs for the Pants Edit.
20 September 2026.

The 1200x1200 squares in localize-pants.py are CARDS. They are cropped to sit
in a grid and they tell you nothing about a room, a course, or how a trouser
moves. This script pulls the wide editorial frames that run BETWEEN the
sections — the masthead and the body bands — from the same brands' own shoots.

SHAPE FIRST, THE RULE FROM btk-lookbook.py.
A frame is only a candidate for a band if cropping it does not throw away most
of its height. Forcing a 4:5 portrait into a 21:9 band discards 76% of the
frame and the first thing to go is whatever was at the top of it, which on a
photograph of a person is their head.

That rule decided the whole set here. Of every editorial frame these sixteen
brands publish for a trouser, EXACTLY ONE is natively landscape: Manors' 3:2
links photograph (7746x5166), four men on a headland, three of them in
trousers. Everything else — Criquet's FW26 shoot, Odd Ritual's studio, Public
Drip, Students, ANTi — is shot 4:5 or 1:1 for Instagram. So:

  * ONE masthead, 21:9, cut from the only landscape frame available. A 3:2
    source loses 36% of its height to a 21:9 band, which is inside tolerance.
  * FIVE body bands kept in the shape they were shot in. btk-template's
    render_band already measures orientation off the file and tags portrait
    frames .btk-port, so a native portrait band is a supported shape, not a
    workaround. Cropping these to 16:9 would decapitate four of the five.

A guard at the bottom refuses the run if any band would be an upscale or if a
portrait ever ends up in the masthead slot. Originals are archived to
research/pants-edit/originals/ before anything is written, so a re-crop never
needs the brand's CDN a second time.

Idempotent. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/pants-edit"
ARCHIVE = ROOT / "research/pants-edit/originals"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}

MAST_W, MAST_AR = 1800, 21 / 9
BODY_W = 1400
MIN_SRC_W = 900          # below this a 1400px band is an upscale

SAN = "https://cdn.sanity.io/images/9aznesrq/production/"

# name, brand, credit-line brand, source url, slot
BANDS = [
    # THE ONLY NATIVE LANDSCAPE FRAME IN THE WHOLE SWEEP. Four men on a links
    # headland; three are in trousers. 7746x5166 down to 2400 wide, then cut.
    ("band-hero", "Manors Golf",
     SAN + "0e4e19786407d6da0095f81bdb0ecf7529e544d7-7746x5166.jpg"
           "?auto=format&fit=max&q=90&w=2600", "mast"),

    # Criquet's FW26 shoot: the duffel frame. Full leg break, boots, daylight —
    # the single best argument on the page for photographing trousers outdoors.
    ("band-1", "Criquet Shirts",
     "https://cdn.shopify.com/s/files/1/2546/6304/files/R6SF8557.jpg?v=1788898919", "body"),

    # ANTi's one-tuck, shot in a dim panelled room. Carries the wide-leg section.
    # Same colour-cast caveat as the card — see localize-pants.py.
    ("band-2", "ANTi Country Club Tokyo",
     "https://cdn.shopify.com/s/files/1/0459/5633/3732/files/"
     "ANTiCOUNTRYCLUB00580_82788158-8f17-4bee-964e-c6774efa23f2.jpg?v=1774173088", "body"),

    # Odd Ritual from behind: the cuff, the break, the drape of a pleat.
    ("band-3", "Odd Ritual",
     "https://cdn.shopify.com/s/files/1/0584/7551/1907/files/DSC05872.jpg?v=1783855838", "body"),

    # Students Golf, full length, taupe. Studio, but it shows the rise.
    ("band-4", "Students Golf",
     "https://cdn.shopify.com/s/files/1/0565/3581/0232/files/"
     "Studentsgolf6a94738269f1866a9473826a15d.672364336a9473826a15d.jpg?v=1788113832", "body"),

    # Public Drip: foot up on a rail, pinstripe. A detail frame that earns its
    # place because it shows the break, which no packshot on this page does.
    ("band-5", "Public Drip",
     "https://cdn.shopify.com/s/files/1/0475/7218/9333/files/"
     "DSC09395_5f620c26-323f-4a59-a55b-a7c8a60813cd.jpg?v=1784829245", "body"),
]


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()


def cut_mast(im):
    """21:9 from a landscape source, biased slightly above centre so horizons
    and heads survive. Refuses a portrait outright — see the guard."""
    tw = MAST_W
    th = round(tw / MAST_AR)
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    cx = (im.width - tw) // 2
    cy = max(0, min(im.height - th, round(im.height * 0.40) - th // 2))
    return im.crop((cx, cy, cx + tw, cy + th))


def cut_body(im):
    """NO CROP. Resized to BODY_W and left in the shape it was shot in."""
    if im.width <= BODY_W:
        return im
    return im.resize((BODY_W, round(im.height * BODY_W / im.width)), Image.LANCZOS)


def main(apply_):
    global Image
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
        ARCHIVE.mkdir(parents=True, exist_ok=True)
    made, skipped, failed, notes = [], [], [], []

    for name, brand, url, slot in BANDS:
        dest = OUT / f"{name}.jpg"
        if dest.exists():
            skipped.append(name); continue
        if not apply_:
            made.append((name, f"would fetch ({slot})")); continue
        try:
            raw = fetch(url)
            (ARCHIVE / f"{name}.orig.jpg").write_bytes(raw)   # archive BEFORE cropping
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            if im.width < MIN_SRC_W:
                failed.append((name, f"source only {im.width}px wide — would upscale"))
                continue
            if slot == "mast":
                if im.width <= im.height:
                    failed.append((name, f"masthead source is portrait {im.width}x{im.height} "
                                         "— a 21:9 cut would discard most of it"))
                    continue
                cut = cut_mast(im)
            else:
                cut = cut_body(im)
            cut.save(dest, "JPEG", quality=90, optimize=True)
            shape = "land" if cut.width > cut.height * 1.08 else (
                    "port" if cut.height > cut.width * 1.08 else "sq")
            made.append((name, f"{slot} {cut.width}x{cut.height} {shape}  from {im.width}x{im.height}"))
        except Exception as e:
            failed.append((name, str(e)[:100]))

    for n, d in made:    print(f"  ok    {n:12} {d}")
    for n in skipped:    print(f"  skip  {n:12} already local")
    for n, e in failed:  print(f"  FAIL  {n:12} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — a page with a hole in it is worse than a page with fewer bands")

    if apply_:
        # VERIFY THE FILES ON DISK, not the loop's own bookkeeping.
        want = {b[0] for b in BANDS}
        have = {p.stem for p in OUT.glob("band-*.jpg")}
        if want - have:
            sys.exit(f"\n! missing: {sorted(want - have)}")
        h = Image.open(OUT / "band-hero.jpg")
        if abs(h.width / h.height - MAST_AR) > 0.02:
            sys.exit(f"! masthead is {h.width}x{h.height}, not 21:9")
        for b in BANDS:
            if b[3] != "body": continue
            im = Image.open(OUT / f"{b[0]}.jpg")
            if im.width > BODY_W:
                sys.exit(f"! {b[0]} is {im.width}px wide, over the {BODY_W} body width")
        credits = sorted({b[1] for b in BANDS})
        print(f"\n  1 masthead + {len(BANDS)-1} body bands in images/pants-edit/")
        print(f"  photography courtesy of: {', '.join(credits)}")
        print(f"  originals archived to {ARCHIVE.relative_to(ROOT)}/")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
