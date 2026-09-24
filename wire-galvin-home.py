#!/usr/bin/env python3
"""wire-galvin-home.py — the Galvin Green Brand to Know feed card, slot 1.
24 September 2026.

Lenny approved the page ("looks great") and then: "let's push it".

A NEW CARD, built on the markup of the card currently in slot 1 (Home Golf
Decor) so it inherits the exact carousel structure gearSlide() expects. It is
inserted ABOVE that card; everything else moves down one.

THE SLIDES ARE THE TGI TAKE'S OWN KIT, in the order the Take gives it: Larry,
Marty, Del, Adam, Noah. Images are the on-model frame (local[1]) the post leads
each gallery with. Prices come from research/galvin/picks.json, the same file
the post is built from, so card and post cannot disagree.

THE VISIBLE TEXT LIVES IN window._slideTexts, keyed "galvin1". The card's own
<p class="card-text"> is set to slide 1's text too, so crawlers and no-JS
readers see the same thing.

Idempotent: a previous run's card and map entry are removed before writing.
Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/brand-to-know-galvin-green.html"
PICKS = {p["name"]: p for p in json.loads(
    (ROOT / "research/galvin/picks.json").read_text())["products"]}
SLUG = "/drops/brand-to-know-galvin-green"
KEY = "galvin1"
MARK, END = "<!-- TGI-GALVIN-CARD -->\n", "<!-- /TGI-GALVIN-CARD -->\n"
TITLE = "Brand to Know: Galvin Green &mdash; The Swedish Family Firm Built for In-Between Weather"
CARD_OPEN = '<div class="card" data-type='

# CAMPAIGN PHOTOGRAPHY, NOT PACKSHOTS — Lenny, 24 Sep: "let's swap out the
# homepage galvin green images for those in the campaign images. I don't like
# the images on the homepage that are there currently." The first version led
# with the studio product frames. These are Galvin Green's own campaign photos,
# localised to images/galvin-green/, four of them already used on the post.
# Only the Adam slide names a product and a price, because Adam is the one
# campaign photo that shows a piece on the page; the others carry the brand's
# story, so no slide puts a product name over a photo of something else.
# (image, alt, brand line, headline, slide text)
SLIDES = [
    ("life-adam", "A golfer carrying his bag at sunset in Galvin Green's Adam half-zip rain jacket",
     "Galvin Green &middot; Adam &middot; $399", "The half-zip rain pullover, at golden hour",
     "Adam is a half-zip rain pullover in Pertex Shield 3-layer stretch. Galvin Green has "
     "made golf rain gear since 1990, and this is the light end of it."),
    ("life-dusk", "A golfer at the top of his backswing at dusk in a white and red Galvin Green jacket",
     "Galvin Green &middot; Since 1990", "A Swedish family firm that only makes golf clothes",
     "Galvin Green was founded in 1990 in Växjö, Sweden, by Tomas Nilsson, and the Nilsson "
     "family still owns it. It has made nothing but golf clothing since."),
    ("life-insula", "Three golfers talking on a green in Galvin Green INSULA mid-layers",
     "Galvin Green &middot; INSULA", "Mid-layers, graded by warmth",
     "INSULA mid-layers are rated Warming Effect #1 to #3, so you pick the weight for the "
     "morning. Dixon, Del and Dean are on the post, from $89.40."),
    ("life-walk", "A golfer walking off a links fairway in a pale grey Galvin Green jacket",
     "Galvin Green &middot; Comfort Combinations", "Layers for the in-between weather",
     "The brand builds everything as layers: base, mid, wind, then shell. For an Austin "
     "winter of cold fronts and warm afternoons, you take them off one at a time."),
    ("life-links", "A golfer at address beside the water in a navy and orange Galvin Green jacket",
     "Galvin Green &middot; 24 pieces", "The first letter tells you what it does",
     "Every Galvin Green piece has a first name, and the letter tells you the job: M is a "
     "polo, L a wind layer, D insulation, A a rain shell. The post has 24 picks, $77.40 to $399."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for img, alt, brand, headline, _ in SLIDES:
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="/images/galvin-green/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
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
        if not (ROOT / f"images/galvin-green/{img}.jpg").is_file():
            bad.append(f"{img}: image missing on disk")
    # every price the card shows must be a price on the post
    for pr in set(re.findall(r"\$[\d,]+(?:\.\d\d)?", blk + (m.group(1) if (m := re.search(r"\n    %s: \[\n(.*?)\n    \]," % KEY, fin, re.S)) else ""))):
        if pr not in post:
            bad.append(f"card shows {pr}, which is not a price on the post")
    if "gear-slide" in blk and re.search(r'images/galvin-green/[a-z]+(?:-a\d)?\.jpg', blk):
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
    print("  wrote index.html — Galvin Green card in slot 1")


if __name__ == "__main__":
    main("--apply" in sys.argv)
