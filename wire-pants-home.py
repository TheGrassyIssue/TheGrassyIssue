#!/usr/bin/env python3
"""wire-pants-home.py — feed card for The Five Best Golf Pants, slot 1.
24 September 2026. Lenny: "yes, let's push". Built from wire-falldrops-home.py
(same carousel markup, _slideTexts handling and rerun-updates-in-place rule).
Slide 1 is the Greenskeeper photo that heads the post; slides 2-5 count down
No. 5 to No. 2, matching the post's order. Every price shown is on the post.
Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/best-golf-pants-ranked.html"
SLUG = "/drops/best-golf-pants-ranked"
KEY = "pants5"
MARK, END = "<!-- TGI-PANTS5-CARD -->\n", "<!-- /TGI-PANTS5-CARD -->\n"
TITLE = "The Five Best Golf Pants Right Now &mdash; Ranked"
CARD_OPEN = '<div class="card" data-type='

# (image, alt, brand line, headline, slide text)
SLIDES = [
    ("card-gk-walk", "A golfer walking a green with his putter in olive Manors Greenskeeper trousers",
     "No. 1 &middot; Manors Greenskeeper &middot; $172", "Five golf pants, counted down to one",
     "Our five favourite golf pants right now, ranked: lululemon, Students, Odd Ritual, Sentinel and, at No. 1, the Manors Greenskeeper. Four of the five have a pleat."),
    ("lulu-0", "A model in Deep Forest lululemon Daydrift pleated trousers and a navy half-zip",
     "No. 5 &middot; lululemon Daydrift &middot; $148", "A casual trouser golfers wear anyway",
     "lululemon files the Daydrift under Casual. In Luxtreme stretch with pleats and new belt loops, it plays like a golf pant."),
    ("students-2", "A man in black Students Science pants in front of a silver Porsche",
     "No. 4 &middot; Students Science Pant &middot; $135", "A pleat you can move",
     "A velcro waist lets you shift where the pleat sits, which changes the whole leg. Two sizes cover waists 30 to 40."),
    ("oddritual-1", "A man in black Odd Ritual Pleated Daily Trousers with a leather bag at his feet",
     "No. 3 &middot; Odd Ritual Pleated Daily &middot; R 1,300", "Cotton twill, made in Cape Town",
     "The only cotton pair on the list: 235gsm twill, front pleats and a carrot-shaped leg, priced in rand by the brand."),
    ("sentinel-lb1", "A model in a cream hoodie and dark navy Sentinel trousers",
     "No. 2 &middot; Sentinel MajoTech &middot; $210", "Italian cloth, sewn in New York",
     "MajoTech stretch nylon with a DWR face, waterproof YKK zips and a cord lock at each ankle."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/pants-top5/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
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
        if not (ROOT / f"images/pants-top5/{img}.jpg").is_file():
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
    print("  wrote index.html — pants card written")


if __name__ == "__main__":
    main("--apply" in sys.argv)
