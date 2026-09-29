#!/usr/bin/env python3
"""wire-practice-home.py — refresh the existing practiceatx feed card in place (28 Sep 2026)
after the full rewrite of /drops/8-best-practice-facilities-around-austin. Keeps the card's
position; replaces slides, title, card text and the practiceatx slide-text entry, all of
which carried the June page's wrong claims (city-owned Penick, 9-hole Lions, old prices)."""
import html, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
SLUG = "/drops/8-best-practice-facilities-around-austin"
TITLE = "Best Practice Facilities in Austin: 10 Ranges and Short-Game Spots"
S = [
 ("drr-1", "The Driving Range in Round Rock lit at dusk", "The Driving Range", "Round Rock · Lit until 10:30pm",
  "The Driving Range, Round Rock — 35 acres of all-grass practice with no course attached, a separate wedge range, and lights until 10:30pm. Buckets from $10."),
 ("dscc-1", "A golfer on the Toptracer range at Dripping Springs Country Club", "Dripping Springs Country Club", "Dripping Springs · Toptracer",
  "Dripping Springs Country Club — not a club but a family-run range on Highway 290, with Toptracer, a bar and food, open until 9pm."),
 ("clay-1", "The range and bunkers at Jimmy Clay and Roy Kizer", "Jimmy Clay & Roy Kizer", "Southeast Austin · Muni",
  "Jimmy Clay & Roy Kizer — the best-value serious range in Austin at $7 and $11, open until 9pm, with a $5 four-hole short course next door."),
 ("penick-1", "A golf ball at the cup at Harvey Penick Golf Campus", "Harvey Penick Golf Campus", "East Austin · First Tee",
  "Harvey Penick Golf Campus — home of First Tee Greater Austin, with $8 and $12 buckets, a chipping green, two bunkers and a 3-hole short course."),
 ("forest-1", "Forest Creek's range lit at night, seen from above", "Forest Creek Golf Club", "Round Rock · Lit until 10pm",
  "Forest Creek — a big range open until 10pm daily, with buckets at $10 and $15."),
 ("plum-1", "Golfers on the Toptracer range at Plum Creek", "Plum Creek Golf Course", "Kyle · Toptracer",
  "Plum Creek, Kyle — the south-side pick: a Toptracer range, three acres of short-game areas, and Texas State's practice home."),
 ("tera-1", "A junior golfer hitting from a Power Tee at Teravista", "Teravista Golf Club", "Round Rock · Covered Toptracer",
  "Teravista — covered Toptracer bays and Power Tee, one of only three Austin-area clubs with both."),
 ("butler-1", "A golfer chipping at Butler Pitch & Putt", "Butler Pitch & Putt", "Butler Park · 9-hole par 3",
  "Butler Pitch & Putt — nine par 3s and a big practice green by Lady Bird Lake since 1950. $14 weekdays, $16 weekends, no tee times."),
]
def main(apply_):
    h = HOME.read_text(encoding="utf-8"); orig = h
    a = h.index('<div class="gear-carousel" data-carousel="practiceatx">')
    t0 = h.index('<div class="gear-carousel-track">', a) + len('<div class="gear-carousel-track">')
    t1 = h.index('<button class="gear-arrow prev"', t0)
    t1 = h.rindex('</div>', t0, t1)  # end of track
    slides = "\n".join(
        f'          <div class="gear-slide">\n            <a href="{SLUG}">\n'
        f'              <img src="/images/practice-2026/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
        f'              <div class="gear-slide-info"><div class="gear-slide-brand">{html.escape(b)}</div><div class="gear-slide-name">{html.escape(n)}</div></div>\n'
        f'            </a>\n          </div>' for img, alt, b, n, _ in S)
    h = h[:t0] + "\n" + slides + "\n        " + h[t1:]
    h = h.replace('style="color:inherit;text-decoration:none;border-bottom:none;">8 Best Practice Facilities Around Austin</a>',
                  f'style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a>', 1)
    h = re.sub(r'(<div class="card-text" data-slidetext="practiceatx">)[^<]*(</div>)', lambda m: m.group(1) + html.escape(S[0][4], quote=False) + m.group(2), h, 1)
    h = h.replace("<!-- FIELD GUIDE — 8 Best Practice Facilities Around Austin -->", "<!-- FIELD GUIDE — Best Practice Facilities in Austin (rewritten 28 Sep 2026) -->", 1)
    arr = ",\n".join('      "%s"' % t.replace("\\", "\\\\").replace('"', '\\"') for *_, t in S)
    h, k = re.subn(r"\n    practiceatx: \[\n.*?\n    \]", f"\n    practiceatx: [\n{arr}\n    ]", h, count=1, flags=re.S)
    assert k == 1
    blk = h[a:h.index('<!-- FIELD GUIDE — 10 Indie Ball Marker', a)]
    assert blk.count('class="gear-slide"') == len(S), blk.count('class="gear-slide"')
    for bad in ("City-owned", "9-hole short game masterclass", "The Domain · Tech Bays", "Avery Ranch"):
        assert bad not in blk, bad
    print("ok, slides", len(S))
    if apply_: HOME.write_text(h, encoding="utf-8"); print("wrote index.html")
if __name__ == "__main__": main("--apply" in sys.argv)
