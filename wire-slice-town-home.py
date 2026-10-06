#!/usr/bin/env python3
"""wire-slice-town-home.py — the SLICE TOWN Brand to Know card, slot 1.
5 October 2026. Cloned from wire-golden-hour-home.py (first run inserts at slot 1; a rerun
updates the card where it sits; every price on the card must be on the post). Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/brand-to-know-slice-town.html"
SLUG = "/drops/brand-to-know-slice-town"
KEY = "slicetown1"
MARK, END = "<!-- TGI-SLICETOWN-CARD -->\n", "<!-- /TGI-SLICETOWN-CARD -->\n"
TITLE = "Brand to Know: SLICE TOWN, Golf Streetwear Made for the Rough"
CARD_OPEN = '<div class="card" data-type='
IMGDIR = "slice-town"

SLIDES = [
    ("btk-card-hero", "A man from behind in a white SLICE TOWN tee with the big sliced logo down the back, between city buildings",
     "SLICE TOWN", "Brand to Know",
     "Golf streetwear from a Dane and a Swede, started in late 2024: nylon track suits, tech pants and reflective logos."),
    ("s06-1", "The SLICE TOWN Golf Track Jacket in slate with yellow piping",
     "Golf Track Jacket, Slate · 1,750 kr (~$190)", "Our pick",
     "Wide-fit nylon with yellow piping and a golf ball printed on the back."),
    ("band-6", "A man in sunglasses lying flat on a green, lining up a putt",
     "On the green", "The look",
     "SLICE TOWN's own photos, from the course to the city."),
    ("s08-1", "The SLICE TOWN Short Sleeve Windbreaker in charcoal",
     "Short Sleeve Windbreaker · 1,250 kr (~$135)", "Layers",
     "Boxy nylon with a quarter zip and a reflective logo."),
    ("s01-1", "The yellow SLICE TOWN Knitted Golf Balaclava",
     "Knitted Golf Balaclava · 2,200 kr (~$240)", "The joke",
     "For when your game's so bad, you need full anonymity."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/{IMGDIR}/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
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
            f'      <a href="{SLUG}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:\'JetBrains Mono\',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>\n'
            f'    </div>\n'
            f'  </div>\n' + END)


def main(apply_):
    h = HOME.read_text(encoding="utf-8")
    original = h
    # A RERUN UPDATES THE CARD WHERE IT SITS. The first version stripped the card
    # and re-inserted it at slot 1 every time, so refreshing its images after a
    # newer post had taken slot 1 would have silently jumped this card back above it.
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
        if not (ROOT / f"images/{IMGDIR}/{img}.jpg").is_file():
            bad.append(f"{img}: image missing on disk")
    # every price the card shows must be a price on the post
    for pr in set(re.findall(r"\$[\d,]+(?:\.\d\d)?", blk + (m.group(1) if (m := re.search(r"\n    %s: \[\n(.*?)\n    \]," % KEY, fin, re.S)) else ""))):
        if pr not in post:
            bad.append(f"card shows {pr}, which is not a price on the post")
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
    print("  wrote index.html — SLICE TOWN card in slot 1")


if __name__ == "__main__":
    main("--apply" in sys.argv)
