#!/usr/bin/env python3
"""The Austin simulator map, drawn as a self-contained SVG.

WHY NOT A REAL MAP EMBED
An interactive Leaflet/Mapbox map would mean third-party tile requests on every
page load and, for Mapbox or Google, an API key TGI does not have. It also
fights the house rule about never hot-linking imagery. So this is drawn: a true
Web Mercator projection of verified coordinates over a hand-drawn metro frame.
No tiles, no key, no external request, and it matches the site's type.

COORDINATES were geocoded against OpenStreetMap's Nominatim on 2026-09-16,
bounded to a metro viewbox because an unbounded "Austin TX" query resolves to
Austin COUNTY (Sealy, 90 miles east) — that trap caught the first pass.

PRECISION IS MARKED, NOT FAKED. Twenty-one venues geocoded to a street address
and get a solid pin. Four could not: Fiber Golf, Bogey Master, Back Nine Round
Rock and Southside sit on roads OSM has no house numbers for. Those are placed
at ZIP or locality centroid and drawn as a HOLLOW ring, with the legend saying
so. Dropping them would have been worse — Fiber is a headline venue and
Southside is the imminent opening — but a solid pin would have been a lie.

Two venues are absent entirely and that is deliberate:
  Halftime Co. publishes no street address at all, only "Plum Creek Business
  Park, Kyle". 512 Golf Co has published no address either. Neither can be
  placed, so neither is drawn; both are named underneath instead.
"""

# key, label, lat, lon, kind, exact
#   kind: open | coming    exact: True = street-level geocode, False = centroid
PINS = [
 # ---- open, street-level
 ("golfi",  "Golfinity",              30.43211, -97.84154, "open",   True),
 ("xgolf",  "X-Golf Cedar Park",      30.53209, -97.78148, "open",   True),
 ("spare",  "Spare Birdie",           30.51949, -97.82369, "open",   True),
 ("drg",    "Dr. Golf Studio",        30.46260, -97.79659, "open",   True),
 ("atx",    "ATX Indoor Golf Club",   30.23738, -97.84044, "open",   True),
 ("rokw",   "ROK Golf Westlake",      30.29187, -97.82743, "open",   True),
 ("rokb",   "ROK Golf Bee Cave",      30.30684, -97.94393, "open",   True),
 ("aig",    "Austin Indoor Golf",     30.40171, -97.63279, "open",   True),
 ("1872",   "1872 Golf Club",         30.70279, -97.74222, "open",   True),
 ("swing",  "Swing Station",          29.88108, -97.92269, "open",   True),
 ("cave",   "Man Cave Golf Club",     30.19716, -98.08842, "open",   True),
 ("b9south","Back Nine South",        30.21181, -97.87816, "open",   True),
 ("b9east", "Back Nine East",         30.28431, -97.70428, "open",   True),
 ("b9west", "Back Nine Westlake",     30.33754, -97.80376, "open",   True),
 ("b9lake", "Back Nine Lakeline",     30.46664, -97.80680, "open",   True),
 ("b9pflug","Back Nine Pflugerville", 30.44642, -97.64592, "open",   True),
 ("b9lea",  "Back Nine Leander",      30.58207, -97.85750, "open",   True),
 ("b9kyle", "Back Nine Kyle",         29.98523, -97.87239, "open",   True),
 # ---- open, centroid only
 ("fiber",  "Fiber Golf",             30.24245, -97.92846, "open",   False),
 ("bogey",  "Bogey Master",           30.52200, -97.54844, "open",   False),
 ("b9rr",   "Back Nine Round Rock",   30.53900, -97.55600, "open",   False),
 # ---- coming
 ("southside","Southside Golf Co",    30.14077, -97.83306, "coming", False),
 ("another9", "Another Nine",         30.60181, -97.68444, "coming", True),
 ("gl18",     "Golf Lounge 18",       30.41515, -97.66988, "coming", True),
 ("fiveiron", "Five Iron Golf",       30.26729, -97.74263, "coming", True),
]

# Anchors for orientation. Not venues — they just stop the frame being abstract.
TOWNS = [("Georgetown", 30.6333, -97.6772), ("Round Rock", 30.5083, -97.6789),
         ("Cedar Park", 30.5052, -97.8203), ("Leander", 30.5788, -97.8531),
         ("Pflugerville", 30.4394, -97.6200), ("Hutto", 30.5427, -97.5467),
         ("DOWNTOWN AUSTIN", 30.2672, -97.7431), ("Bee Cave", 30.3080, -97.9464),
         ("Dripping Springs", 30.1902, -98.0867), ("Kyle", 29.9891, -97.8772),
         ("Buda", 30.0855, -97.8403), ("San Marcos", 29.8833, -97.9414)]

W, H = 900, 1000
PAD = 54
LON0, LON1 = -98.20, -97.45
LAT0, LAT1 = 29.82, 30.78


def _merc(lat):
    import math
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def xy(lat, lon):
    x = PAD + (lon - LON0) / (LON1 - LON0) * (W - 2 * PAD)
    y0, y1, ym = _merc(LAT0), _merc(LAT1), _merc(lat)
    y = H - PAD - (ym - y0) / (y1 - y0) * (H - 2 * PAD)
    return round(x, 1), round(y, 1)


def svg():
    open_pins = [p for p in PINS if p[4] == "open"]
    coming = [p for p in PINS if p[4] == "coming"]
    num = {p[0]: i + 1 for i, p in enumerate(open_pins)}
    for i, p in enumerate(coming):
        num[p[0]] = i + 1

    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="Map of 21 open and 4 upcoming indoor golf '
           f'simulators across the Austin metro" style="width:100%;height:auto;'
           f'background:#faf9f6;border:1px solid rgba(0,0,0,.14);">']
    out.append('<defs><style>'
               '.t{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;}'
               '.town{font-size:11px;letter-spacing:.11em;fill:#9a9a94;text-transform:uppercase;}'
               '.dt{font-size:12px;letter-spacing:.15em;fill:#5f5f58;font-weight:700;}'
               '.pn{font-size:11px;fill:#fff;font-weight:700;}'
               '.pnx{font-size:11px;fill:#2f7a3e;font-weight:700;}'
               '.lg{font-size:12px;fill:#3a3a35;}'
               '.hd{font-size:12px;letter-spacing:.16em;fill:#6a6a62;text-transform:uppercase;}'
               '</style></defs>')

    # faint graticule so the projection reads as a map rather than a diagram
    lat = 29.9
    while lat < LAT1:
        _, y = xy(lat, LON0)
        out.append(f'<line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="#e8e6df" stroke-width="1"/>')
        lat += 0.2
    lon = -98.1
    while lon < LON1:
        x, _ = xy(LAT0, lon)
        out.append(f'<line x1="{x}" y1="{PAD}" x2="{x}" y2="{H-PAD}" stroke="#e8e6df" stroke-width="1"/>')
        lon += 0.2

    # I-35 runs the spine of this metro and every reader orients off it
    i35 = [(30.78, -97.66), (30.63, -97.68), (30.51, -97.68), (30.39, -97.69),
           (30.27, -97.73), (30.13, -97.79), (29.99, -97.87), (29.88, -97.94)]
    pts = " ".join(f"{a},{b}" for a, b in (xy(la, lo) for la, lo in i35))
    out.append(f'<polyline points="{pts}" fill="none" stroke="#d8d4c8" stroke-width="7" stroke-linecap="round"/>')
    tx, ty = xy(30.35, -97.71)
    out.append(f'<text class="t town" x="{tx+9}" y="{ty}" transform="rotate(-76 {tx+9} {ty})">I-35</text>')

    # ---- declutter -------------------------------------------------------
    # Pins are r=11, so anything under 22px apart overlaps and anything sitting
    # on a town dot buries it. Relax the pins apart, then keep a hairline back
    # to the true coordinate so a nudged pin still points at the real address.
    true_xy = {p[0]: xy(p[2], p[3]) for p in PINS}
    pos = {k: list(v) for k, v in true_xy.items()}
    keys = [p[0] for p in PINS]
    for _ in range(140):
        moved = False
        for a, b in __import__("itertools").combinations(keys, 2):
            ax, ay = pos[a]; bx, by = pos[b]
            dx, dy = bx - ax, by - ay
            d = (dx * dx + dy * dy) ** 0.5 or 0.01
            if d < 24:
                push = (24 - d) / 2
                ux, uy = dx / d, dy / d
                pos[a][0] -= ux * push; pos[a][1] -= uy * push
                pos[b][0] += ux * push; pos[b][1] += uy * push
                moved = True
        if not moved:
            break
    for k in pos:
        pos[k][0] = max(PAD, min(W - PAD, pos[k][0]))
        pos[k][1] = max(PAD, min(H - PAD, pos[k][1]))

    # town labels flip to the left when a pin would sit on top of the name
    for name, la, lo in TOWNS:
        x, y = xy(la, lo)
        cls = "dt" if name.startswith("DOWNTOWN") else "town"
        clash = any((px - (x + 40)) ** 2 + (py - y) ** 2 < 46 ** 2 for px, py in pos.values())
        out.append(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#c9c6bb"/>')
        if clash:
            out.append(f'<text class="t {cls}" x="{x-7}" y="{y+4}" text-anchor="end">{name}</text>')
        else:
            out.append(f'<text class="t {cls}" x="{x+7}" y="{y+4}">{name}</text>')

    def pin(p, fill, ring):
        x, y = pos[p[0]]
        tx0, ty0 = true_xy[p[0]]
        n = num[p[0]]
        lead = ""
        if (x - tx0) ** 2 + (y - ty0) ** 2 > 9:
            lead = (f'<line x1="{tx0}" y1="{ty0}" x2="{round(x,1)}" y2="{round(y,1)}" '
                    f'stroke="{ring}" stroke-width="1" opacity=".45"/>'
                    f'<circle cx="{tx0}" cy="{ty0}" r="1.8" fill="{ring}" opacity=".7"/>')
        x, y = round(x, 1), round(y, 1)
        if p[5]:
            return (lead + f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}" stroke="#faf9f6" stroke-width="2"/>'
                    f'<text class="t pn" x="{x}" y="{y+4}" text-anchor="middle">{n}</text>')
        return (lead + f'<circle cx="{x}" cy="{y}" r="11" fill="#faf9f6" stroke="{ring}" '
                f'stroke-width="2.5" stroke-dasharray="3 2.4"/>'
                f'<text class="t pnx" x="{x}" y="{y+4}" text-anchor="middle" fill="{ring}">{n}</text>')

    for p in open_pins:
        out.append(pin(p, "#2f7a3e", "#2f7a3e"))
    for p in coming:
        out.append(pin(p, "#b07a2b", "#b07a2b"))

    out.append(f'<text class="t hd" x="{PAD}" y="{PAD-18}">Indoor golf simulators &#183; Austin metro &#183; 9/16/26</text>')
    out.append('</svg>')
    return "\n".join(out), num, open_pins, coming, pos


def section():
    s, num, open_pins, coming, _pos = svg()
    # f-strings cannot carry a backslash, so the approximate marker is a constant
    APPROX = ' <span style="opacity:.5;">&#176;</span>'

    def row(p, colour):
        mark = "" if p[5] else APPROX
        return ('<li style="margin:0 0 3px;"><span style="display:inline-block;min-width:22px;'
                'font-family:var(--mono);font-size:11px;color:' + colour + ';font-weight:700;">'
                + str(num[p[0]]) + '</span>' + p[1] + mark + '</li>')

    ol = "".join(row(p, "#2f7a3e") for p in open_pins)
    cl = "".join(row(p, "#b07a2b") for p in coming)
    return f"""<section class="products">
  <h2 class="products-hdr">The Map</h2>
  <p class="cat-kicker">Twenty-one open rooms and four on the way, plotted from their own published addresses.</p>
  <div class="writeup-body">
    {s}
    <div style="display:flex;flex-wrap:wrap;gap:34px;margin-top:20px;font-size:14px;">
      <div style="flex:1;min-width:230px;">
        <p style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#2f7a3e;margin:0 0 8px;">Open now</p>
        <ol style="list-style:none;padding:0;margin:0;">{ol}</ol>
      </div>
      <div style="flex:1;min-width:230px;">
        <p style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#b07a2b;margin:0 0 8px;">On the way</p>
        <ol style="list-style:none;padding:0;margin:0;">{cl}</ol>
      </div>
    </div>
    <p style="font-size:13px;opacity:.65;margin-top:18px;">A dashed ring and a &#176; mark a venue whose exact address our geocoder could not resolve &mdash; those four sit at the centre of their ZIP or town rather than on their doorstep. <strong>Halftime Co.</strong> in Kyle and <strong>512 Golf Co</strong> are missing from the map entirely because neither publishes a street address to plot. Coordinates from OpenStreetMap, 9/16/26.</p>
    <p>Two things fall straight out of the picture. The first is the hole in the middle: <strong>the closer you get to downtown, the fewer rooms there are</strong>, and the only pin inside the urban core is an amber one that has no opening date. The second is the north-south stretch &mdash; from 1872 in Georgetown down to Swing Station in San Marcos is a little over fifty miles, and the corridor between them is now dense enough that most of the metro has something within a twenty-minute drive.</p>
  </div>
</section>
"""


if __name__ == "__main__":
    import re
    s, num, op, cm, pos = svg()
    print(f"{len(op)} open + {len(cm)} coming = {len(PINS)} pins")
    print(f"approximate: {[p[1] for p in PINS if not p[5]]}")
    xs = [xy(p[2], p[3]) for p in PINS]
    assert all(PAD <= x <= W - PAD and PAD <= y <= H - PAD for x, y in xs), "a pin fell outside the frame"
    print("all pins inside the frame")
