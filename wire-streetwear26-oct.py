#!/usr/bin/env python3
"""wire-streetwear26-oct.py — refresh the streetwear card IN PLACE (1 Oct 2026, nine-brand rebuild).
Lenny: "keep the position on the homepage and URL". Finds the card by data-carousel="streetwear26" in index.html
or whichever feed/page-N.html holds it, and swaps slides, title and text without moving it. Idempotent.
"""
import glob, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
URL = "/drops/best-golf-streetwear-brands-2026"
SLIDES = [
    ("/images/streetwear-oct/band-students-0.jpg", "Students Golf Art Dept. tee and shorts, on model"),
    ("/images/streetwear-oct/band-metalwood-1.jpg", "A Metalwood player kicking a ball in the adidas x Metalwood golf shoe"),
    ("/images/streetwear-oct/band-eastside-0.jpg", "Eastside Golf Fall 26 Gravity look"),
    ("/images/streetwear-oct/band-publicdrip-0.jpg", "Public Drip P Script cap, on model"),
    ("/images/streetwear-oct/band-midiron-0.jpg", "Midiron after dark, in a bunker"),
]
TITLE = "The 9 Best Golf Streetwear Brands in 2026"
TEXT = ("Nine brands, nine awards: Students is best overall, Metalwood best retro, Malbon most influential, plus Eastside, "
        "Public Drip, Midiron, Clamp, ALD and Hidden Links Society. Six pieces from each.")
def main(apply_):
    files = [f for f in [ROOT / "index.html"] + sorted(map(pathlib.Path, glob.glob(str(ROOT / "feed/page-*.html"))))
             if 'data-carousel="streetwear26"' in f.read_text(encoding="utf-8")]
    if len(files) != 1: sys.exit(f"! card found in {len(files)} files")
    f = files[0]; t = f.read_text(encoding="utf-8")
    i = t.index('data-carousel="streetwear26"')
    a = t.index('<div class="gear-carousel-track">', i) + len('<div class="gear-carousel-track">')
    b = t.index('</div>\n        <button class="gear-arrow prev"', a)
    track = "".join(f'<div class="gear-slide"><a href="{URL}"><img src="{u}" alt="{alt}" loading="lazy"></a></div>' for u, alt in SLIDES)
    t = t[:a] + track + t[b:]
    t = re.sub(r'(<div class="card-title"><a href="%s"[^>]*>)[^<]*(</a>)' % re.escape(URL), rf"\g<1>{TITLE}\g<2>", t, count=1)
    t = re.sub(r'(<div class="card-text" data-slidetext="streetwear26">)[^<]*(</div>)', rf"\g<1>{TEXT}\g<2>", t, count=1)
    for u, _ in SLIDES:
        assert (ROOT / u.lstrip("/")).is_file(), u
    print(f"  {f.relative_to(ROOT)}: card updated in place")
    if apply_: f.write_text(t, encoding="utf-8")
    else: print("  dry run — pass --apply")
if __name__ == "__main__":
    main("--apply" in sys.argv)
