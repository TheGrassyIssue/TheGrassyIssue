#!/usr/bin/env python3
"""wire-sounder-home.py — the Sounder Brand to Know feed card, slot 1.
25 September 2026.

Lenny, on the Sounder post: "your call on the homepage feature but lean on the
options with the best photos". So every slide is Sounder's own campaign
photography, localised to images/sounder/. Only the Pac Mach slide names a
product and a price, because it is the one photo that clearly shows a pick; the
rest carry the brand's story, so no slide puts a product name over a photo of
something else.

Built on wire-galvin-home.py: a first run inserts the card at slot 1, a rerun
updates it where it sits. Every price the card shows must be on the post.
Slide text lives in window._slideTexts (key "sounder1") as real characters, not
entities, because the card sets it with textContent. Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/brand-to-know-sounder.html"
SLUG = "/drops/brand-to-know-sounder"
KEY = "sounder1"
MARK, END = "<!-- TGI-SOUNDER-CARD -->\n", "<!-- /TGI-SOUNDER-CARD -->\n"
TITLE = "Brand to Know: Sounder &mdash; The London Golf Brand Named for Seve&rsquo;s First Clubs"
CARD_OPEN = '<div class="card" data-type='

# Campaign photography only (house rule since the Galvin card, 24 Sep 2026).
# (image, alt, brand line, headline, slide text)
SLIDES = [
    ("life-pacmach", "A golfer in a red Sounder Pac Mach jacket and grey beanie holding a club on a beach at dusk",
     "Sounder · Pac Mach Jacket · $197", "The packable jacket, at dusk",
     "The Pac Mach is Japanese recycled ripstop, light enough to stuff into its own bag once the sun is up. "
     "It is the Sounder layer we would pick for Austin's windy winter mornings."),
    ("life-first-tee", "Three golfers with carry bags on a first tee in low sun, from Sounder's campaign",
     "Sounder · London · since 2021", "Named for the clubs Seve played",
     "Sounder was the brand of clubs Seve Ballesteros played in the seventies. Cathal McAteer of Folk "
     "and James Day of Urban Golf revived the name in 2021."),
    ("life-trevose", "A golfer in an olive Sounder polo and dark trousers on a links course in England",
     "Sounder · The Polos", "Cotton polos, made in Portugal",
     "Sounder built its name on the organic cotton polo. The Play Well cut took nearly five years to "
     "get right, and it sits under most of the range."),
    ("life-spain", "A golfer in a striped polo carrying a Sounder bag towards a flag on a course in Spain",
     "Sounder · On the course", "Clothes that look right at lunch",
     "The founders wanted golf clothes you could wear straight to dinner. Everything on the post passes "
     "that test, from $55 caps to $372 rain jackets."),
    ("life-rgc", "Two golfers walking with a carry bag, from Sounder's Random Golf Club collaboration",
     "Sounder · Collaborations", "Grenson, Random Golf Club, Protected Species",
     "Sounder has made a golf shoe with Grenson, a range with Random Golf Club and a waterproof with "
     "Protected Species. The post has 20 picks and the founders' own words."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/sounder/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
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
        if not (ROOT / f"images/sounder/{img}.jpg").is_file():
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
    print("  wrote index.html — Sounder card in slot 1")


if __name__ == "__main__":
    main("--apply" in sys.argv)
