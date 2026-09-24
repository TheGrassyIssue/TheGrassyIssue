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

SLIDES = [
    ("Larry", "Half-Zip Windbreaker", "Lighter than a sleeve of golf balls",
     "Start here. Larry is a half-zip INTERFACE-1 windbreaker that weighs less than a "
     "sleeve of golf balls, in the brand's own words. The layer for a 7:40 tee time."),
    ("Marty", "Polo", "The plain polo that goes under all of it",
     "Marty is a solid stretch polo with a contrast collar and cuffs, UV 20+. Every "
     "Galvin Green polo name starts with M; the first letter tells you what a piece does."),
    ("Del", "Quarter-Zip Vest", "For the one morning a front comes through",
     "Del is a thermal quarter-zip vest at Warming Effect #1. It goes over a polo on its "
     "own, or under a wind jacket when the norther arrives."),
    ("Adam", "Half-Zip Rain Jacket", "Pertex Shield, for the day it pours",
     "Adam is a half-zip rain pullover in Pertex Shield 3-layer stretch. Galvin Green has "
     "made golf rain gear since 1990, and this is the light end of it."),
    ("Noah", "Pants", "What you wear the rest of the year",
     "Noah pants have a shirt-gripper waistband, stretch and UV 20+. The Core Collection "
     "on the post covers the everyday pieces: pants, shorts, knitwear."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_card():
    slides = []
    for name, kind, headline, _ in SLIDES:
        p = PICKS[name]
        img = p["local"][1] if len(p["local"]) > 1 else p["local"][0]
        slides.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="{img}" alt="Galvin Green {name} {kind}" loading="lazy" />\n'
            f'              <div class="gear-slide-info"><div class="gear-slide-brand">Galvin Green '
            f'&middot; {name} &middot; {money(p["usd"])}</div>'
            f'<div class="gear-slide-name">{headline}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    first = html.escape(SLIDES[0][3], quote=False)
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
    # strip a previous run
    h = re.sub(re.escape(MARK) + r".*?" + re.escape(END), "", h, flags=re.S)
    h = re.sub(r"\n    %s: \[\n.*?\n    \],?(?=\n)" % KEY, "", h, flags=re.S)
    if f'href="{SLUG}"' in h:
        sys.exit("! the index already links the post outside this script's card")

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
    if fin.find(CARD_OPEN, a) != fin.index(MARK) + len(MARK):
        bad.append("the Galvin card is not in slot 1")
    blk = fin[fin.index(MARK):fin.index(END)]
    if fin.count(f'href="{SLUG}"') != blk.count(f'href="{SLUG}"'):
        bad.append("a link to the post exists outside the card")
    if blk.count('class="gear-slide"') != len(SLIDES):
        bad.append("slide count")
    for name, *_ in SLIDES:
        p = PICKS[name]
        img = p["local"][1]
        if not (ROOT / img.lstrip("/")).is_file():
            bad.append(f"{name}: image missing on disk")
        if money(p["usd"]) not in post:
            bad.append(f"{name}: {money(p['usd'])} is not a price on the post")
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
