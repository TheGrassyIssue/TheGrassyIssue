#!/usr/bin/env python3
"""wire-quiet-golf-home.py — Quiet Golf, Revisited card, slot 1. 7 October 2026.
Lenny: "brought back to the 1st homepage slot". Cloned from wire-mackem-home.py. The August Quiet Golf card
(<!-- BRAND TO KNOW — Quiet Golf -->, carousel key "quietgolf") is removed from whichever feed page holds it first,
so the post is linked from exactly one card.
Cloned from wire-golden-hour-home.py (first run inserts at slot 1; a rerun
updates the card where it sits; every price on the card must be on the post). Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
POST = ROOT / "drops/brand-to-know-quiet-golf.html"
SLUG = "/drops/brand-to-know-quiet-golf"
KEY = "quietgolf2"
MARK, END = "<!-- TGI-QUIETGOLF-CARD -->\n", "<!-- /TGI-QUIETGOLF-CARD -->\n"
TITLE = "Quiet Golf, Revisited: Less Performance, More Presence"
CARD_OPEN = '<div class="card" data-type='
IMGDIR = "quiet-golf-2026"

SLIDES = [
    ("card-hero", "Two golfers walking a sandy path between the fairways",
     "Quiet Golf", "Brand Revisited",
     "The Costa Mesa label rebuilt its range for fall: nine polos, a Sentinel Scout and Harris Tweed covers."),
    ("qg-x-sentinel-golf-scout-bag-1-0", "The navy Quiet Golf x Sentinel Golf Scout pouch with the QG monogram",
     "QG x Sentinel Scout · $140", "The collab",
     "Sentinel's clip-on Scout, made in the USA, with the QG monogram."),
    ("vintage-supima-cotton-polo-0", "The Quiet Golf Vintage Supima Cotton Polo in green",
     "Vintage Supima Cotton Polo · $118", "Our pick",
     "Supima cotton, made in Portugal, in seven colors."),
    ("cardroom-corduroy-jacket-1", "A model wearing the tan Quiet Golf Cardroom Corduroy Jacket",
     "Cardroom Corduroy Jacket · $198", "For fall",
     "Tan cotton corduroy with a small embroidered QG flag."),
    ("band-4", "Two golfers with carry bags on a fairway at Maidstone",
     "Maidstone", "From the journal",
     "Christion Lennon wrote up a spring day at Maidstone for the brand's journal."),
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


OLD_MARK = "<!-- BRAND TO KNOW — Quiet Golf -->"


def drop_old_card(apply_):
    """Remove the August card (and its slide-text entry) wherever it sits."""
    for p in [HOME] + sorted((ROOT / "feed").glob("page-*.html")):
        t = p.read_text(encoding="utf-8")
        if OLD_MARK not in t:
            continue
        a = t.index(OLD_MARK)
        b = t.index('<div class="card"', a)
        depth, k = 0, b
        for m in re.finditer(r"<div\b|</div>", t[b:]):
            depth += 1 if m.group(0) == "<div" else -1
            if depth == 0:
                k = b + m.end(); break
        t2 = t[:a] + t[k:].lstrip("\n")
        t2 = re.sub(r"\n    quietgolf: \[\n.*?\n    \],?(?=\n)", "", t2, flags=re.S)
        print(f"  removed the August Quiet Golf card from {p.relative_to(ROOT)}")
        if apply_:
            p.write_text(t2, encoding="utf-8")


def main(apply_):
    drop_old_card(apply_)
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
        anchor = 'aria-label="Content feed">\n'
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
    print("  wrote index.html — Quiet Golf card in slot 1")


if __name__ == "__main__":
    main("--apply" in sys.argv)
