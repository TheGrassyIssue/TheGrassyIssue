#!/usr/bin/env python3
"""build-pants-grid.py — render previews/pants-grid.html from localize-pants.py.

The first version of this grid was hand-written HTML, which meant the swap of
two brands had to be made in two places and could silently disagree. It now
IMPORTS PICKS from localize-pants.py, so the grid cannot drift from the list
that actually fetched the images. If a card and a file disagree, the build
fails rather than rendering a lie.

Thin-stock rule: some sizes gone AND three or fewer left. "4 of 4 sizes" is a
full run, not a warning — an earlier cut matched on the leading digit and
painted 4/4 and 3/3 red.
"""
import importlib.util, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "previews/pants-grid.html"

spec = importlib.util.spec_from_file_location("lp", ROOT / "localize-pants.py")
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)
PICKS = lp.PICKS


def thin(avail):
    m = re.match(r"(\d+) of (\d+)", avail)
    if not m:
        return False
    a, t = int(m.group(1)), int(m.group(2))
    return a < t and a <= 3


CSS = """
@font-face{font-family:"Editors Note Text";src:url("/fonts/EditorsNoteText-Regular.woff2") format("woff2");font-weight:400;font-display:swap}
*{box-sizing:border-box}
body{margin:0;background:#f4f2ed;font-family:"Editors Note Text",Georgia,serif;color:#141414;padding:44px 40px 56px}
.hd{text-align:center;margin-bottom:8px;font-size:30px;letter-spacing:-.01em}
.sub{text-align:center;font-family:ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;opacity:.55;margin-bottom:34px}
.g{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;max-width:1180px;margin:0 auto}
.c{background:#fff;border:.5px solid rgba(20,20,20,.14);padding:0 0 16px;position:relative}
.c img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}
.num{position:absolute;top:10px;left:10px;z-index:2;background:#141414;color:#f4f2ed;
  font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.08em;padding:4px 8px}
.kind{position:absolute;top:10px;right:10px;z-index:2;background:rgba(244,242,237,.92);color:#2f4f2f;
  font-family:ui-monospace,Menlo,monospace;font-size:8px;letter-spacing:.12em;padding:4px 7px;text-transform:uppercase}
.br{font-family:ui-monospace,Menlo,monospace;font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;
  color:#2f4f2f;margin:13px 16px 5px}
.nm{font-size:16px;margin:0 16px;line-height:1.25}
.pr{font-family:ui-monospace,Menlo,monospace;font-size:12px;margin:9px 16px 0;letter-spacing:.04em}
.av{font-family:ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;
  margin:6px 16px 0;opacity:.5}
.av.thin{color:#8a2b2b;opacity:.95}
"""


def main():
    cards, missing, flagged = [], [], []
    for i, (slug, brand, name, price, avail, kind, url, img) in enumerate(PICKS, 1):
        f = ROOT / f"images/pants-edit/{slug}.jpg"
        if not f.exists():
            missing.append(slug)
        if thin(avail):
            flagged.append(brand)
        tag = "packshot" if kind == "pack" else "on model"
        cards.append(
            f'<div class="c">\n'
            f'  <div class="num">{i:02d}</div>\n'
            f'  <div class="kind">{tag}</div>\n'
            f'  <img src="/images/pants-edit/{slug}.jpg" alt="{brand} {name}">\n'
            f'  <div class="br">{brand}</div>\n'
            f'  <div class="nm">{name}</div>\n'
            f'  <div class="pr">{price}</div>\n'
            f'  <div class="av{" thin" if thin(avail) else ""}">{avail}</div>\n'
            f'</div>')

    if missing:
        sys.exit(f"! no local image for {missing} — run localize-pants.py --apply first")

    n_model = sum(1 for p in PICKS if p[5] != "pack")
    html = (
        '<!doctype html><html><head><meta charset="utf-8">\n<style>' + CSS +
        '</style></head><body>\n'
        '<div class="hd">The Pants Edit &mdash; 18 for Lenny</div>\n'
        f'<div class="sub">One per brand &middot; all in stock &middot; {n_model} of 18 shot on a model '
        '&middot; prices read 20 Sep 2026 &middot; ZAR, JPY and USD as each brand sets them</div>\n'
        '<div class="g">' + "".join(cards) + '</div>\n</body></html>')
    OUT.write_text(html, encoding="utf-8")

    # VERIFY THE FILE ON DISK, not the string just built.
    h = OUT.read_text(encoding="utf-8")
    bad = []
    if h.count('<div class="c">') != len(PICKS):
        bad.append(f'{h.count(chr(60)+"div class=" + chr(34) + "c" + chr(34) + chr(62))} cards, expected {len(PICKS)}')
    for slug, brand, name, *_ in PICKS:
        if f"/images/pants-edit/{slug}.jpg" not in h:
            bad.append(f"{slug} image missing from markup")
        if name.replace("&", "&amp;") not in h and name not in h:
            bad.append(f"{slug} name missing from markup")
    # the two swapped-out products must be gone entirely
    for gone in ("Bushmills Track Pant", "Coaches Pant"):
        if gone in h:
            bad.append(f"retired pick still on the grid: {gone}")
    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"  {len(PICKS)} cards, {n_model} on model, {len(PICKS)-n_model} packshot")
    print(f"  flagged thin: {flagged}")
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
