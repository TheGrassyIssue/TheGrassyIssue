#!/usr/bin/env python3
"""tgi_bands.py — in-body photo bands that show the whole photograph.

WHY THIS EXISTS, AND THE BUG IT FIXES.

The house rule for a masthead is 21:9, and `.drop-hero-img` enforces it in CSS:

    .drop-hero-img{width:100%;aspect-ratio:21/9;overflow:hidden}
    .drop-hero-img img{width:100%;height:100%;object-fit:cover}

That is right for a masthead, which is cut to 21:9 on the way in. It is wrong
for an in-body band. Both the Pants Edit and the Wild Spring Dunes Field Note
localised their body bands in the shape they were SHOT in — deliberately, so a
portrait would not be decapitated by a crop — and then handed them to a CSS box
that cropped them to 21:9 anyway. Measured on the finished files:

    wild-spring-dunes/band-4.jpg  1400x2100   28.6% of the frame visible
    pants-edit/band-3.jpg         1400x1861   32.2% visible

So roughly seven-tenths of every portrait band was being thrown away at render
time. The caddie band showed a bib with the head and the legs outside the box.
Lenny, looking at the page: "can we also zoom out a bit on those hero images in
the body."

The lesson is the familiar one in a new place. The localiser verified the FILES
— right dimensions, right shape, archived originals — and never verified the
RENDER. A guard that checks the artifact it produces, but not the artifact the
reader sees, will report success while the page is wrong.

WHAT THIS DOES INSTEAD. A body band keeps its own aspect ratio and is sized so
it sits in the column rather than swallowing it: portraits get a narrower
measure, squares a little wider, landscapes the full width. Nothing is cropped.

verify_bands() below reads the finished HTML and the image files together and
refuses any band that would be cropped by more than a few percent.
"""
import pathlib
import re

# Injected into <head>. The `.tgi-free` class overrides the 21:9 box; the
# wrapper classes set the measure so a 2:3 portrait does not run 1400px wide
# and push everything else off the screen.
BAND_CSS = """
/* IN-BODY PHOTO BANDS — see tgi_bands.py. The masthead keeps the house 21:9
   box because it is cut to 21:9. Body bands are NOT cut, so they must not be
   dropped into a fixed-ratio box: that discarded ~70% of every portrait. */
.drop-hero-img.tgi-free{aspect-ratio:auto;height:auto;overflow:visible}
.drop-hero-img.tgi-free img{width:100%;height:auto;object-fit:contain;display:block}
.drop-hero.tgi-band{margin-top:40px;margin-bottom:40px}
.drop-hero.tgi-band.is-port{max-width:840px}
.drop-hero.tgi-band.is-sq{max-width:980px}
@media(max-width:900px){
  .drop-hero.tgi-band.is-port,.drop-hero.tgi-band.is-sq{max-width:100%}
}
/* the photo credit under a band. Defined HERE rather than per page, because
   the helper emits it and a class with no rule is the .axxa-note bug. */
.tgi-band-credit{font-family:var(--mono);font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;opacity:.5;margin-top:8px}
"""

MAST_AR = 21 / 9


def shape_of(path):
    """Measured off the real file, never guessed from the filename."""
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    if h > w * 1.08:
        return "is-port", w, h
    if w > h * 1.08:
        return "is-land", w, h
    return "is-sq", w, h


def band(root, src, alt, credit=None, masthead=False):
    """One photo band. `src` is the site-absolute path, e.g. /images/x/band-1.jpg.

    masthead=True keeps the 21:9 house box, because the masthead file IS 21:9.
    Everything else gets .tgi-free and its measured shape class.
    """
    cap = (f'\n  <div class="tgi-band-credit">{credit}</div>' if credit else "")
    if masthead:
        return (f'<div class="drop-hero"><div class="drop-hero-img">'
                f'<img src="{src}" alt="{alt}" /></div>{cap}\n</div>\n\n')
    cls, _, _ = shape_of(pathlib.Path(root) / src.lstrip("/"))
    return (f'<div class="drop-hero tgi-band {cls}">'
            f'<div class="drop-hero-img tgi-free">'
            f'<img src="{src}" alt="{alt}" loading="lazy" /></div>{cap}\n</div>\n\n')


def verify_bands(root, html, tolerance=0.04):
    """Read the FINISHED HTML and the files together.

    For every band on the page, work out how much of the photograph the reader
    actually sees, and refuse anything cropped past `tolerance`. This is the
    check that was missing: it closes the loop between what the localiser wrote
    and what the browser shows.
    """
    from PIL import Image
    bad = []
    root = pathlib.Path(root)

    # the CSS override has to be present or .tgi-free means nothing
    flat = html.replace(" ", "").replace("\n", "")
    if ".drop-hero-img.tgi-free{" not in flat:
        bad.append("the .tgi-free rule is missing — body bands will be cropped to 21:9")

    for m in re.finditer(r'<div class="drop-hero([^"]*)"><div class="drop-hero-img([^"]*)">'
                         r'<img src="([^"]+)"', html):
        wrap_cls, img_cls, src = m.group(1), m.group(2), m.group(3)
        f = root / src.lstrip("/")
        if not f.exists():
            bad.append(f"band file missing: {src}")
            continue
        with Image.open(f) as im:
            w, h = im.size
        is_free = "tgi-free" in img_cls
        if not is_free:
            # forced into the 21:9 box — only acceptable if the file IS 21:9
            shown = min(1.0, (w * 9 / 21) / h)
            if shown < 1 - tolerance:
                bad.append(f"{src} is {w}x{h} in a 21:9 box — only "
                           f"{shown*100:.0f}% of the frame is visible")
        else:
            # free box shows everything; just check the measure class matches
            want, _, _ = shape_of(f)
            if want not in wrap_cls:
                bad.append(f"{src} is {w}x{h} ({want}) but the wrapper says "
                           f"'{wrap_cls.strip()}'")
    return bad
