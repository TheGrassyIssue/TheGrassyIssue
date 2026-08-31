#!/usr/bin/env python3
"""Wire the revamped streetwear post into the homepage feed.

The post has been live at /drops/best-golf-streetwear-brands-2026 for months
with NO homepage card — index.html contained zero references to the slug. It
was reachable only from /brands pages, the sitemap and search. Adding the card
here, at the top of the feed, is part of the revamp.
"""
import re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
URL = "/drops/best-golf-streetwear-brands-2026"
KEY = "streetwear26"

SLIDES = [
    ("/images/streetwear26/hero.jpg",
     "A golfer mid-swing in pleated trousers and an open camp shirt, a second figure in neon behind &mdash; Metalwood Studio campaign"),
    ("/images/streetwear26/students-0-0.jpg",
     "Students Golf Oaklawn mesh short sleeve tee, shot on model"),
    ("/images/streetwear26/pluto-2-0.jpg",
     "Pluto Golf PlutoDry Target Jacket in steel blue"),
    ("/images/streetwear26/anti-2-0.jpg",
     "ANTi Country Club Tokyo varsity jacket in brown, club crest across the back"),
]

TEXTS = [
    "Five brands, fifteen pieces, every one in stock on 30 August 2026. The old version of this page ranked fifteen — ten are gone, and the reasoning is on the page.",
    "Students Golf came out of Publish and sits in Bodega, HBX and Culture Kings. Two decades in the actual streetwear trade, then pattern making applied to golf.",
    "Pluto Golf out of Indianapolis. Oversized graphics, baggy ripstop, a sneaker program, and about half the catalogue sold through when we checked.",
    "ANTi Country Club Tokyo: an adidas Golf collaboration, shelf space at HBX, and page one of Google has never covered them.",
]

def slide(u, alt):
    return ('<div class="gear-slide"><a href="%s" target="_blank" rel="noopener">'
            '<img src="%s" alt="%s" loading="lazy"></a></div>' % (URL, u, alt))

CARD = '''  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="%s">
        <div class="gear-carousel-track">%s</div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="%s" style="color:inherit;text-decoration:none;border-bottom:none;">The 5 Best Golf Streetwear Brands in 2026</a></div>
      <div class="card-text" data-slidetext="%s">%s</div>
      <a href="%s" class="card-link">Read the edit &#8594;</a>
    </div>
  </div>
''' % (KEY, "".join(slide(u, a) for u, a in SLIDES), URL, KEY, TEXTS[0], URL)


def main(apply_=False):
    p = os.path.join(ROOT, "index.html")
    h = open(p, encoding="utf-8").read()
    if URL in h:
        sys.exit("already wired — refusing to duplicate the card")

    # ASSERT EVERY IMAGE. A card whose <img> 404s renders as an empty grey box
    # and nothing on the page complains.
    for u, _ in SLIDES:
        if not os.path.exists(ROOT + u):
            sys.exit("missing image: " + u)

    # 1. insert the card at the head of the feed
    anchor = '<section class="feed" id="feed" role="tabpanel" aria-label="Content feed">\n'
    i = h.find(anchor)
    if i < 0:
        sys.exit("feed section not found")
    h = h[:i + len(anchor)] + CARD + h[i + len(anchor):]

    # 2. register the slide captions in the LIVE registry.
    #    window._slideTexts (single underscore) is what gearSlide reads. The
    #    inline <script> blocks further down the file write window.__slideTexts
    #    (double) and are a dead path — do not copy them.
    reg = "  window._slideTexts = {\n"
    j = h.find(reg)
    if j < 0:
        sys.exit("_slideTexts registry not found")
    lit = ",\n".join('      "%s"' % t.replace('"', '\\"') for t in TEXTS)
    h = h[:j + len(reg)] + '    "%s": [\n%s\n    ],\n' % (KEY, lit) + h[j + len(reg):]

    if apply_:
        open(p, "w", encoding="utf-8").write(h)
        print("card + %d slide captions wired" % len(TEXTS))
    else:
        print("dry run OK (pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
