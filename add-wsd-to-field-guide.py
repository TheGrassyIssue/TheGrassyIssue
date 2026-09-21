#!/usr/bin/env python3
"""add-wsd-to-field-guide.py — put the Wild Spring Dunes Field Note into the
Field Guide's "Beyond the City" section. 21 September 2026.

Lenny: "let's add that on our radar post to the field guide in the Beyond the
City section."

WHERE IT GOES. section#day-trips, inside its .guide-cards grid, FIRST. The two
cards already there are evergreen roundups (14 courses, 10 courses); this is one
specific course that opened two weeks ago, so it is the news in that section and
leads. It is not a replacement for either.

THE CARD SHAPE IS COPIED, NOT INVENTED. Every .guide-card on the page is an
<a> wrapping .guide-card-img + .guide-card-body{tag,title,desc,link}. The link
text is one of exactly two strings in use on this page — "Read the guide →" (18)
and "Read the story →" (2). A Field Note on a single course is a story, not a
guide, so it takes the existing second variant rather than a third one invented
for this card. Inventing a variant is what created the .card-source / .card-meta
mess on the homepage that got cleaned up this morning.

THE IMAGE. images/field-guide/ siblings are ~1200x800 (3:2) and the CSS renders
them at height:300px, object-fit:cover. Source is images/wild-spring-dunes/
card-1.jpg (1200x1500) — the sandy bunkering against the East Texas pine wall,
centre-cropped to 3:2. Never upscaled; the guard checks against the source.

EVERY CLAIM ON THE CARD IS FROM THE FIELD NOTE, WHICH WAS SOURCED:
  Tom Doak; 2,400 acres of former timber land; Mount Enterprise, East Texas;
  open to the public since 8 September 2026; walking only, caddies available;
  4hr 15min from Austin.
Nothing else is asserted. In particular the page does NOT say this is Doak's
first Texas course — that would be easy to assume and was never verified.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
GUIDE = ROOT / "field-guide/index.html"
POST = "/drops/on-our-radar-wild-spring-dunes"
SRC_IMG = ROOT / "images/wild-spring-dunes/card-1.jpg"
OUT_IMG = ROOT / "images/field-guide/wild-spring-dunes.jpg"
IMG_W, IMG_H = 1200, 800

SECTION_ID = 'id="day-trips"'

CARD = f'''    <a href="{POST}" class="guide-card">
      <img class="guide-card-img" src="/images/field-guide/wild-spring-dunes.jpg" alt="Sandy bunkering and a wall of East Texas pine at Wild Spring Dunes" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">East Texas &middot; 4hr 15min</div>
        <div class="guide-card-title">Wild Spring Dunes</div>
        <div class="guide-card-desc">A Tom Doak course on 2,400 acres of former timber land outside Mount Enterprise, open to the public since 8 September. Walking only, caddies available.</div>
        <span class="guide-card-link">Read the story &rarr;</span>
      </div>
    </a>
'''


def make_image(apply_):
    from PIL import Image
    if OUT_IMG.exists():
        return ["card image already local"]
    if not apply_:
        return [f"would cut {OUT_IMG.name} from {SRC_IMG.name}"]
    im = Image.open(SRC_IMG).convert("RGB")
    sc = max(IMG_W / im.width, IMG_H / im.height)
    if sc > 1:
        sys.exit(f"! {SRC_IMG.name} is {im.width}x{im.height}; "
                 f"{IMG_W}x{IMG_H} would be an upscale")
    r = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    cx, cy = (r.width - IMG_W) // 2, (r.height - IMG_H) // 2
    r.crop((cx, cy, cx + IMG_W, cy + IMG_H)).save(OUT_IMG, "JPEG", quality=90,
                                                  optimize=True)
    return [f"cut {IMG_W}x{IMG_H} from {im.width}x{im.height} ({SRC_IMG.name})"]


def add_card(h):
    if POST in h:
        return h, ["card already in the field guide"]
    i = h.find(SECTION_ID)
    if i < 0:
        sys.exit('! section id="day-trips" not found')
    j = h.find('<div class="guide-cards">', i)
    if j < 0:
        sys.exit("! no .guide-cards grid inside the Beyond the City section")
    j += len('<div class="guide-cards">')
    return h[:j] + "\n" + CARD + h[j:].lstrip("\n"), ["card added, first in the section"]


def main(apply_):
    h = GUIDE.read_text(encoding="utf-8")
    before_cards = h.count('class="guide-card"')

    notes = make_image(apply_)
    h2, n2 = add_card(h)
    for x in notes + n2:
        print("  " + x)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    GUIDE.write_text(h2, encoding="utf-8")

    # ---- VERIFY THE FINISHED FILE ----
    hh = GUIDE.read_text(encoding="utf-8")
    bad = []
    if hh.count(POST) != 1:
        bad.append(f"{hh.count(POST)} links to the post, expected 1")
    if hh.count('class="guide-card"') != before_cards + 1:
        bad.append(f"guide-cards went {before_cards} -> "
                   f"{hh.count(chr(39) + 'class=' + chr(34) + 'guide-card' + chr(34) + chr(39))}")
    # the new card must sit INSIDE the Beyond the City section, not somewhere else
    s = hh.find(SECTION_ID)
    e = hh.find("</section>", s)
    if not (s < hh.find(POST) < e):
        bad.append("the card landed outside the Beyond the City section")
    # the two cards that were already there must both survive
    for sib in ("/drops/8-special-day-rounds-near-austin",
                "/drops/10-texas-courses-worth-the-trip"):
        if hh.count(sib) < 1:
            bad.append(f"existing card lost: {sib}")
    # target page and image must actually exist on disk
    if not (ROOT / (POST.lstrip("/") + ".html")).is_file():
        bad.append(f"{POST} has no page on disk")
    if not OUT_IMG.is_file():
        bad.append("card image missing")
    else:
        from PIL import Image
        im = Image.open(OUT_IMG)
        if (im.width, im.height) != (IMG_W, IMG_H):
            bad.append(f"card image is {im.width}x{im.height}, not {IMG_W}x{IMG_H}")
    # link text must be one the page already uses
    if "Read the story &rarr;" not in hh:
        bad.append("link text is not one of the page's existing variants")
    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  verified: 1 card added to Beyond the City "
          f"({before_cards} -> {hh.count(chr(34)) and hh.count('class=' + chr(34) + 'guide-card' + chr(34))} "
          f"guide-cards), both existing cards intact")


if __name__ == "__main__":
    main("--apply" in sys.argv)
