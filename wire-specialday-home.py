#!/usr/bin/env python3
"""wire-specialday-home.py — move the rebuilt Special Day Rounds card to slot 1.
24 September 2026. Lenny: "lets bring it back to the top".

The old card (data-carousel="specialday", unmarked, sitting at feed position
174 with the pre-rebuild slide photos and slide texts) is REMOVED, along with
its window._slideTexts entry, and a new marked card is written at slot 1 with
the course photography from the rebuild. Built from wire-pants-home.py.
Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/8-special-day-rounds-near-austin.html"
SLUG = "/drops/8-special-day-rounds-near-austin"
KEY = "specialday2"
MARK, END = "<!-- TGI-SPECIALDAY-CARD -->\n", "<!-- /TGI-SPECIALDAY-CARD -->\n"
TITLE = "Special Day Rounds Near Austin &mdash; 10 Day Trips and 5 Overnights"
CARD_OPEN = '<div class="card" data-type='

# (image, alt, brand line, headline, slide text)
SLIDES = [
    ("c7-b1", "The Quarry Golf Club in San Antonio at sunset",
     "15 courses &middot; rebuilt", "Where to play when it is not a normal round",
     "Ten day trips inside an hour and a quarter of Austin and five overnights, for the birthday, the anniversary or the friend in from out of town."),
    ("c14-0", "Golfers and caddies walking a fairway through the pines at Wild Spring Dunes",
     "New &middot; Wild Spring Dunes &middot; $275 peak", "Tom Doak&rsquo;s new course in the East Texas pines",
     "All 18 holes opened to the public on 8 September. Walking only, more than 2,400 acres, a little over four hours from Austin."),
    ("c0-b0", "A creek running across the course at Lost Pines Resort",
     "Lost Pines Resort &middot; ~20 min east", "Still Wolfdancer to most people",
     "Arthur Hills routed 7,300 yards through the Lost Pines, and the course plays like two: open pasture first, then the trees and the river bottom."),
    ("c5-b1", "Vaaler Creek Golf Club from above, a fairway beside a long blue lake",
     "Vaaler Creek &middot; $95 Mon&ndash;Thu", "The drive through Blanco is half the point",
     "Vaaler Creek still publishes a real rate: $95 for 18 with the cart included Monday to Thursday, read on 17 September."),
    ("c13-b0", "A green under desert cliffs at Lajitas, Black Jack's Crossing",
     "Lajitas &middot; ~7 hrs west", "Go for three nights or do not go",
     "Black Jack’s Crossing sits on the Rio Grande at the edge of Big Bend, the far end of the list and the one that needs real commitment."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/special-day/v2/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
            f'              <div class="gear-slide-info"><div class="gear-slide-brand">{brand}</div>'
            f'<div class="gear-slide-name">{headline}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    first = html.escape(SLIDES[0][4], quote=False)
    return (MARK +
            f'{CARD_OPEN}"field">\n'
            f'    <div class="card-media" style="position:relative;">\n'
            f'      <span class="card-tag grass">[Field Notes]</span>\n'
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
    # remove the old, unmarked card and its slide texts
    k = h.find('data-carousel="specialday"')
    if k != -1:
        cs = h.rfind('<div class="card" data-type=', 0, k)
        nx = h.find('<div class="card" data-type=', k)
        ce = h.rfind("</div>", cs, nx) + len("</div>")
        h = h[:cs] + h[h.index("\n", ce) + 1:]
    h = re.sub(r"\nspecialday: \[\n.*?\n\s*\],?(?=\n)", "", h, flags=re.S)
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
    if fin.count(CARD_OPEN) != base.count(CARD_OPEN) + (0 if 'data-carousel="specialday"' in base else 1):
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
        if not (ROOT / f"images/special-day/v2/{img}.jpg").is_file():
            bad.append(f"{img}: image missing on disk")
    # every price the card shows must be a price on the post
    for pr in set(re.findall(r"\$[\d,]+(?:\.\d\d)?", blk + (m.group(1) if (m := re.search(r"\n    %s: \[\n(.*?)\n    \]," % KEY, fin, re.S)) else ""))):
        if pr not in post:
            bad.append(f"card shows {pr}, which is not a price on the post")
    if "gear-slide" in blk and False:
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
    print("  wrote index.html — special day card written")


if __name__ == "__main__":
    main("--apply" in sys.argv)
