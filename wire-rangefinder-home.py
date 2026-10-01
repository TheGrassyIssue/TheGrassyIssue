#!/usr/bin/env python3
"""wire-rangefinder-home.py — the Rangefinder Cases and Pouches card, slot 1.
1 October 2026. Lenny: "yes 1st slot on the homepage". Built on wire-limited-balls-home.py (first run inserts at slot 1;
a rerun updates the card where it sits; every price on the card must be on the post).
Field Notes tag is red (flag) per Lenny, 29 Sep. Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/rangefinder-cases-and-pouches.html"
SLUG = "/drops/rangefinder-cases-and-pouches"
KEY = "rf1"
MARK, END = "<!-- TGI-RF-CARD -->\n", "<!-- /TGI-RF-CARD -->\n"
TITLE = "Keep the Laser Reachable: 16 Rangefinder Cases and Pouches"
CARD_OPEN = '<div class="card" data-type='
IMGDIR = "rangefinder-pouches"

SLIDES = [
    ("qg-sentinel-scout-1", "Quiet Golf x Sentinel Scout rangefinder case in navy X-Pac",
     "Quiet Golf x Sentinel · Our pick", "The Scout you can still buy",
     "Sixteen cases, pouches and straps to keep the laser reachable, plus six rangefinders. Checked 1 October."),
    ("fyfe-marksman-4", "Fyfe Marksman waxed canvas rangefinder case hanging from a golf bag",
     "Fyfe Golf · £69 (~$91)", "Scottish waxed canvas",
     "Waxed canvas, a leather pocket and a brass swivel hook, made in Scotland."),
    ("mogshade-course-case-1", "Round Mogshade wool Course Case hanging from a stone signpost",
     "Mogshade · €96 (~$108)", "Rescued Portuguese wool",
     "A round case sewn by hand from wool woven in the Serra da Estrela."),
    ("walker-canvas-3", "Walker Golf Things canvas rangefinder bag worn crossbody on a rope sling",
     "Walker Golf Things · A$70 (~$49)", "The one you wear",
     "A canvas rangefinder bag that doubles as a crossbody sling."),
    ("vc-tl1-2", "Voice Caddie TL1 rangefinders in white and yellow on a cart bar",
     "Voice Caddie TL1 · $349.99", "Six rangefinders, too",
     "From the 117-gram EL3 at $149.99 to Bushnell's Pro X3+LINK at $599.99."),
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
    print("  wrote index.html — Rangefinder card in slot 1")


if __name__ == "__main__":
    main("--apply" in sys.argv)
