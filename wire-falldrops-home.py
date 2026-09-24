#!/usr/bin/env python3
"""wire-falldrops-home.py — feed card for Three Fall Drops, slot 1.
24 September 2026.

Lenny: "let's push the fall drops post". Built from wire-galvin-home.py (same
carousel markup, same _slideTexts handling, same rerun-updates-in-place rule).

CAMPAIGN PHOTOS, NOT PACKSHOTS, from the start — Lenny's call on the Galvin card
the same afternoon. Two slides are frames from the film on Devereux's homepage,
two are from Students' "The Curriculum" lookbook, one is from Eastside's own
fall banner cropped clear of its sale text. A slide names a product and price
only where the photo shows a piece that is on the post: the Denali, the Course
Camo polo and the Whittier knit.

Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/fall-drops-eastside-students-devereux.html"
SLUG = "/drops/fall-drops-eastside-students-devereux"
KEY = "falldrops1"
MARK, END = "<!-- TGI-FALLDROPS-CARD -->\n", "<!-- /TGI-FALLDROPS-CARD -->\n"
TITLE = "Three Fall Drops We Dig &mdash; Eastside Golf, Students and Devereux"
CARD_OPEN = '<div class="card" data-type='

# (image, alt, brand line, headline, slide text)
SLIDES = [
    ("card-devereux-swing", "A golfer finishing his swing on a dirt road through the high desert, from Devereux's film",
     "Devereux &middot; Pioneertown Golf Club", "Three brands, three directions for fall",
     "Eastside Golf went loud and printed, Students went back to school, and Devereux went "
     "to the high desert. Fifteen pieces from the three fall drops, $74 to $280."),
    ("lb-students-denali", "A man in the black Students Denali wool stadium jacket",
     "Students &middot; Denali Stadium Jacket &middot; $280", "The one piece to buy this fall",
     "The Denali is a heavyweight wool stadium jacket with striped ribbing and leather welt "
     "pockets. Students calls it the defining piece of \u201cThe Curriculum\u201d."),
    ("card-eastside-camo", "A man in Eastside Golf's Course Camo snap placket polo",
     "Eastside Golf &middot; Course Camo Polo &middot; $88", "A golf course, repeated as camo",
     "Eastside's fall print takes a painted golf landscape, trees and all, and repeats it "
     "until it reads as camouflage. The polo is nylon and spandex with a snap placket."),
    ("lb-students-whittier", "A man in the green and cream striped Students Whittier knit polo sweater",
     "Students &middot; Whittier Knit Polo &middot; $158", "Prep-school stripes, on a golf collar",
     "The Whittier is a full-fashion cotton knit in wide stripes with a polo collar, the piece "
     "in the lookbook that most looks like a school yearbook."),
    ("card-devereux-pioneer", "Two golfers from behind in the desert, one in a Devereux Pioneer Country Club tee",
     "Devereux &middot; Fall 1: The Arrival", "Pearl snaps and skull prints, from $74",
     "Devereux's Pioneertown Golf Club is high-desert Western: pearl-snap performance polos, "
     "skull prints and a washed twill jacket. Most polos are $74."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/fall-drops-2026/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
            f'              <div class="gear-slide-info"><div class="gear-slide-brand">{brand}</div>'
            f'<div class="gear-slide-name">{headline}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    first = html.escape(SLIDES[0][4], quote=False)
    return (MARK +
            f'{CARD_OPEN}"drop">\n'
            f'    <div class="card-media" style="position:relative;">\n'
            f'      <span class="card-tag grass">[Drops &amp; Brands]</span>\n'
            f'      <div class="gear-carousel" data-carousel="{KEY}">\n'
            f'        <div class="gear-carousel-track">\n' + "\n".join(slides) + "\n"
            f'        </div>\n'
            f'        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>\n'
            f'        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'    <div class="card-body">\n'
            f'      <div class="card-title"><a href="{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>\n'
            f'      <p class="card-text" data-slidetext="{KEY}">{first}</p>\n'
            f'      <div class="gear-dots" data-dots="{KEY}"></div>\n'
            f'      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>\n'
            f'      <a href="{SLUG}" class="card-readmore" style="display:inline-block;font-size:0.97rem;color:var(--ink);opacity:0.7;text-decoration:none;border-bottom:1px solid var(--ink);padding-bottom:1px;">See the Full Post &rarr;</a>\n'
            f'    </div>\n'
            f'  </div>\n' + END)


def main(apply_):
    h = HOME.read_text(encoding="utf-8")
    original = h
    # A RERUN UPDATES THE CARD WHERE IT SITS. The first version stripped the card
    # and re-inserted it at slot 1 every time, so refreshing its images after a
    # newer post had taken slot 1 would have silently jumped Galvin back above it.
    # Only a first run places the card at the top.
    h = re.sub(r"\n    %s: \[\n.*?\n    \],?(?=\n)" % KEY, "", h, flags=re.S)
    if MARK in h:
        i = h.index(MARK)
        h = h[:i] + h[h.index(END, i) + len(END):]
    else:
        i = None
    if f'href="{SLUG}"' in h:
        sys.exit("! the index already links the post outside this script's card")
    if i is None:
        anchor = '<section class="feed" id="feed" role="tabpanel" aria-label="Content feed">\n'
        i = h.index(anchor) + len(anchor)
    h = h[:i] + build_card() + h[i:]

    # slide texts: insert as the first entry of the _slideTexts map
    m = re.search(r"window\._slideTexts\s*=\s*\{\n", h)
    if not m:
        sys.exit("! no window._slideTexts map")
    arr = ",\n".join('      "%s"' % t.replace("\\", "\\\\").replace('"', '\\"')
                     for *_, t in SLIDES)
    h = h[:m.end()] + f"    {KEY}: [\n{arr}\n    ],\n" + h[m.end():]

    print(f"  card built, {len(SLIDES)} slides; feed cards "
          f"{original.count(CARD_OPEN)} -> {h.count(CARD_OPEN)}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    HOME.write_text(h, encoding="utf-8")
    verify(original)


def verify(original):
    fin = HOME.read_text(encoding="utf-8")
    post = POST.read_text(encoding="utf-8")
    bad = []
    base = re.sub(re.escape(MARK) + r".*?" + re.escape(END), "", original, flags=re.S)
    if fin.count(CARD_OPEN) != base.count(CARD_OPEN) + 1:
        bad.append("feed card count is not exactly one more than before")
    a = fin.index('aria-label="Content feed">')
    if MARK not in original and fin.find(CARD_OPEN, a) != fin.index(MARK) + len(MARK):
        bad.append("a newly placed card is not in slot 1")
    if MARK in original and original.index(MARK) != fin.index(MARK):
        bad.append("a rerun moved the card")
    blk = fin[fin.index(MARK):fin.index(END)]
    if fin.count(f'href="{SLUG}"') != blk.count(f'href="{SLUG}"'):
        bad.append("a link to the post exists outside the card")
    if blk.count('class="gear-slide"') != len(SLIDES):
        bad.append("slide count")
    for img, *_ in SLIDES:
        if not (ROOT / f"images/fall-drops-2026/{img}.jpg").is_file():
            bad.append(f"{img}: image missing on disk")
    # every price the card shows must be a price on the post
    for pr in set(re.findall(r"\$[\d,]+(?:\.\d\d)?", blk + (m.group(1) if (m := re.search(r"\n    %s: \[\n(.*?)\n    \]," % KEY, fin, re.S)) else ""))):
        if pr not in post:
            bad.append(f"card shows {pr}, which is not a price on the post")
    if "gear-slide" in blk and re.search(r'images/fall-drops-2026/(?:eastside|students|devereux)-', blk):
        bad.append("a studio packshot is still on the card")
    m = re.search(r"\n    %s: \[\n(.*?)\n    \]," % KEY, fin, re.S)
    if not m or len(re.findall(r'^\s*"', m.group(1), re.M)) != len(SLIDES):
        bad.append("slide-text map entry wrong")
    if re.search(r"\bworth\b", blk + (m.group(1) if m else ""), re.I):
        bad.append("banned word")
    if fin.count(f'data-carousel="{KEY}"') != 1:
        bad.append("carousel key duplicated")
    if bad:
        HOME.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "; ".join(bad))
    print("  wrote index.html — fall drops card written")


if __name__ == "__main__":
    main("--apply" in sys.argv)
