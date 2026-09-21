#!/usr/bin/env python3
"""localize-wild-spring-dunes.py — imagery for the On Our Radar Field Note.
20 September 2026.

Every frame is Wild Spring Dunes' own photography, pulled from their Squarespace
CDN and served from /images/wild-spring-dunes/. Nothing hot-links.

CREDIT. The course's filenames carry "Marsh" and D CEO credits Jeff Marsh on
what is plainly the same shoot. The page still credits the line TGI can stand
behind without a rights conversation — "Photography courtesy of Wild Spring
Dunes" — because a photographer credit inferred from a filename is an
inference, not a permission.

SHAPE FIRST, the rule from btk-lookbook.py. A frame is only a candidate for a
band if cropping it does not throw away most of its height. Forcing a 2:3
portrait into a 21:9 masthead discards ~76% and takes the sky with it.

Wild Spring Dunes shoots BOTH orientations, which is rarer than it sounds and
is why this page gets a real masthead:
  * five 3:2 landscapes (aerials and wide course frames)
  * six 2:3 portraits (the creek, the boardwalk, the caddie, the ravine)

So the masthead is cut 21:9 from a native 3:2 — a 36% loss, inside tolerance —
and the body bands keep the shape they were shot in. render_band in
btk-template.py already measures orientation off the file and tags portraits
.btk-port, so a native portrait band is a supported shape here, not a bodge.

Idempotent. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/wild-spring-dunes"
ARCHIVE = ROOT / "research/wild-spring-dunes/originals"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}
CDN = "https://images.squarespace-cdn.com/content/v1/662a404b2067a541eecdd3d4/"

MAST_W, MAST_AR = 1800, 21 / 9
BODY_W = 1400
MIN_SRC_W = 1200

# name, remote path, slot, what it shows (becomes the alt text and caption)
FRAMES = [
    # THE MASTHEAD. Native 3:2. Sandy bunker complex running into scrub with the
    # pine wall behind — the single frame that answers "this is Texas?" fastest.
    ("band-hero",
     "cd2f7e1b-d49b-474a-933c-d29c3ae16e44/WSD+Aerial+-+June+26+-+Marsh+-51+%281%29.jpg",
     "mast", "Sandy bunkering running into scrub beneath a wall of East Texas pine"),

    # The creek that gives the place its name, and one of the eleven bridges.
    ("band-1",
     "47e8c661-4783-43f7-9dc9-c6bbafadb442/WSD+Sony+-+June+26+-+Marsh-37+%281%29+%281%29.jpg",
     "body", "A spring-fed creek and one of the property&rsquo;s bridges"),

    # A ravine hole seen from above — the back-nine land Doak called heaving.
    ("band-2",
     "6c9a97d9-e633-4ce4-a226-d206625672b0/Wild+Spring+Dunes+-+Public+Golf+-+Texas.jpg",
     "body", "A green set above a ravine, with the crossing below"),

    # Two golfers on the boardwalk. This is the walk the whole place is sold on.
    ("band-3",
     "bdb2cbe4-e9da-4277-87ab-de7091c8a855/WSD+Sony+-+June+26+-+Marsh-121+%281%29.jpg",
     "body", "Golfers crossing a boardwalk through the pines"),

    # A caddie in the bib. Carries the walking-only section on its own.
    ("band-4",
     "c189cc35-52c3-4685-83b1-d2f9f44507e8/WSD+Dec+Media+Day-33.JPG",
     "body", "A Wild Spring Dunes caddie on the course"),

    # Quiet closing frame: a flag against the pine wall.
    ("band-5",
     "bec966dc-0c96-4d4a-bda3-50efcbd48776/WSD+Sony+-+June+26+-+Marsh-45+%281%29.jpg",
     "body", "A green and flag against the pine wall"),
]

CREDIT = "Photography courtesy of Wild Spring Dunes"

# ---------------------------------------------------------------------------
# CARD FRAMES — 4:5, for the homepage carousel.
#
# WHY THIS SLOT EXISTS. The first version of the homepage card dropped the
# 1800x771 masthead straight into .card-media. The masthead is 21:9 and
# .card-media img is `width:100%; height:auto`, with no ratio of its own, so
# the browser drew it exactly as handed over: a 130px letterbox strip above a
# wall of text, in a row where every neighbouring card's media is 379px tall.
# Lenny: "the wild dunes card on the homepage is formatted wierd."
#
# The house card slot is 4:5 and it is not a suggestion — `.gear-slide img`
# sets `aspect-ratio:4/5; object-fit:cover`, so the browser crops whatever it
# is given. Handing it a 2:3 portrait loses ~17%; handing it the 21:9 masthead
# would show ~34% of the width. Cutting the frames to 4:5 here means the crop
# is chosen against the photograph rather than discovered at render time.
#
# Sources are the ARCHIVED ORIGINALS, not the band JPEGs: a band is already
# resized to 1400w, and cutting a 1200x1500 card out of it would upscale.
CARD_W, CARD_H = 1200, 1500

# card name, original to cut from, what the slide says.
# The caption pairs come from research/wild-spring-dunes.json — the facts table
# and the sourced take — never from looking at the picture and guessing.
CARD_FRAMES = [
    ("card-1", "band-hero", "Tom Doak &middot; opened 8 September 2026",
     "Sandy bunkering, and a wall of East Texas pine"),
    ("card-2", "band-4", "Walking only &mdash; caddies available",
     "The bib, and the only way round"),
    ("card-3", "band-3", "2,400 acres of former timber land",
     "Two players, a boardwalk, and the Piney Woods"),
    ("card-4", "band-2", "6,962 yds &middot; 74.6/147 &middot; par 72",
     "A green above the ravine on the back nine"),
    ("card-5", "band-1", "Mount Enterprise &middot; 4hr 15min from Austin",
     "The spring-fed creek the place is named for"),
]


def cut_card(im):
    """4:5 centre cut. The contact sheet was read before this was written:
    all six originals hold their subject in a centred 4:5, so there is no
    per-frame bias here. If a future frame needs one, measure it first."""
    tw, th = CARD_W, CARD_H
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    cx = (im.width - tw) // 2
    cy = (im.height - th) // 2
    return im.crop((cx, cy, cx + tw, cy + th))


def build_cards(apply_):
    """Cut the card frames from the archived originals."""
    made, skipped, failed = [], [], []
    for name, src, _, _ in CARD_FRAMES:
        dest = OUT / f"{name}.jpg"
        orig = ARCHIVE / f"{src}.orig.jpg"
        if dest.exists():
            skipped.append(name); continue
        if not orig.exists():
            failed.append((name, f"no archived original {orig.name}")); continue
        if not apply_:
            made.append((name, f"would cut 4:5 from {orig.name}")); continue
        try:
            im = Image.open(orig).convert("RGB")
            cut = cut_card(im)
            cut.save(dest, "JPEG", quality=90, optimize=True)
            made.append((name, f"{cut.width}x{cut.height} from {im.width}x{im.height} "
                               f"({src})"))
        except Exception as e:
            failed.append((name, str(e)[:100]))

    for n, d in made:   print(f"  ok    {n:11} {d}")
    for n in skipped:   print(f"  skip  {n:11} already local")
    for n, e in failed: print(f"  FAIL  {n:11} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} card frames failed")

    if apply_:
        # VERIFY ON DISK. The card slot is the whole point of this function,
        # so the ratio is checked off the finished file, not off CARD_W/CARD_H.
        for name, _, _, _ in CARD_FRAMES:
            p = OUT / f"{name}.jpg"
            if not p.exists():
                sys.exit(f"! {name} missing after build")
            im = Image.open(p)
            if abs(im.width / im.height - 4 / 5) > 0.01:
                sys.exit(f"! {name} is {im.width}x{im.height} "
                         f"(ar {im.width/im.height:.3f}), not the 4:5 card slot")
        print(f"\n  {len(CARD_FRAMES)} card frames at {CARD_W}x{CARD_H}")


def fetch(path):
    url = CDN + path + "?format=2500w"
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()


def cut_mast(im):
    """21:9 from a landscape source, biased above centre so skyline survives."""
    tw = MAST_W
    th = round(tw / MAST_AR)
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    cx = (im.width - tw) // 2
    cy = max(0, min(im.height - th, round(im.height * 0.46) - th // 2))
    return im.crop((cx, cy, cx + tw, cy + th))


def cut_body(im):
    """NO CROP. Resized only. The shape it was shot in is the shape it keeps."""
    if im.width <= BODY_W:
        return im
    return im.resize((BODY_W, round(im.height * BODY_W / im.width)), Image.LANCZOS)


def main(apply_):
    global Image
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
        ARCHIVE.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []

    for name, path, slot, what in FRAMES:
        dest = OUT / f"{name}.jpg"
        if dest.exists():
            skipped.append(name); continue
        if not apply_:
            made.append((name, f"would fetch ({slot})")); continue
        try:
            raw = fetch(path)
            (ARCHIVE / f"{name}.orig.jpg").write_bytes(raw)   # archive BEFORE cropping
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            if im.width < MIN_SRC_W:
                failed.append((name, f"source only {im.width}px wide — would upscale"))
                continue
            if slot == "mast":
                if im.width <= im.height:
                    failed.append((name, f"masthead source is portrait "
                                         f"{im.width}x{im.height} — a 21:9 cut "
                                         f"would discard most of it"))
                    continue
                cut = cut_mast(im)
            else:
                cut = cut_body(im)
            cut.save(dest, "JPEG", quality=90, optimize=True)
            shape = ("land" if cut.width > cut.height * 1.08 else
                     "port" if cut.height > cut.width * 1.08 else "sq")
            made.append((name, f"{slot} {cut.width}x{cut.height} {shape}  "
                               f"from {im.width}x{im.height}"))
        except Exception as e:
            failed.append((name, str(e)[:100]))

    for n, d in made:    print(f"  ok    {n:11} {d}")
    for n in skipped:    print(f"  skip  {n:11} already local")
    for n, e in failed:  print(f"  FAIL  {n:11} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — a page with a hole in it is worse "
                 f"than a page with fewer bands")

    if apply_:
        # VERIFY THE FILES ON DISK, not this loop's own bookkeeping.
        want = {f[0] for f in FRAMES}
        have = {p.stem for p in OUT.glob("band-*.jpg")}
        if want - have:
            sys.exit(f"\n! missing: {sorted(want - have)}")
        h = Image.open(OUT / "band-hero.jpg")
        if abs(h.width / h.height - MAST_AR) > 0.02:
            sys.exit(f"! masthead is {h.width}x{h.height}, not 21:9")
        for n, _, slot, _ in FRAMES:
            if slot != "body":
                continue
            im = Image.open(OUT / f"{n}.jpg")
            if im.width > BODY_W:
                sys.exit(f"! {n} is {im.width}px wide, over the {BODY_W} body width")
        print(f"\n  1 masthead + {len(FRAMES)-1} body bands in "
              f"images/wild-spring-dunes/")
        print(f"  credit line: {CREDIT}")
        print(f"  originals archived to {ARCHIVE.relative_to(ROOT)}/")

    build_cards(apply_)

    if not apply_:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
