#!/usr/bin/env python3
"""wire-gift-guide-home.py — 2026 Holiday Gift Guide, three homepage cards (Parts 1-3), slots 1-3. 9 November 2026.
Published together (Lenny). Cloned from wire-deliberate-practice-home.py. First run inserts Part 1, 2, 3 at the top in
that order; a rerun updates each card where it sits. Dry run by default.
"""
import html, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
CARD_OPEN = '<div class="card" data-type='
PARTS = [
 ("giftguide1", "golf-gift-guide-2026-everyday-range-rat-stocking-stuffers", "The 2026 Gift Guide, Part 1: Everyday Upgrades, Range Rats and Stocking Stuffers", "gift-guide-1b", [
   ("card-hero", "A brass TOTEM divot tool hanging from a wooden chair", "Gift Guide 2026", "Part 1 of 3", "Thirty brands and the gifts each one does best: everyday kit, range gifts and stocking stuffers."),
   ("totem-divot-repair-tool-1pcs-1", "A machined TOTEM divot tool", "TOTEM", "Divot Repair Tool", "The Everyday Item as Well Done as Possible."),
   ("clutchgolfcompany-range-set-alignment-sticks-lea-1", "Clutch alignment sticks in a leather cover", "Clutch Golf Company", "Range Set", "For the Range Rat."),
   ("birdiebalm-birdie-balm-1", "A tin of Birdie Balm with a ball marker in the lid", "Birdie Balm", "Birdie Balm", "Small Enough for a Stocking.")]),
 ("giftguide2", "golf-gift-guide-2026-statement-pieces-colorways-splurges", "The 2026 Gift Guide, Part 2: Statement Pieces, Fresh Colorways and Splurges", "gift-guide-2b", [
   ("card-hero", "A man in a rifle green Criquet quilted jacket among fall leaves", "Gift Guide 2026", "Part 2 of 3", "Thirty brands: pieces that get noticed, colorways nobody else owns, and the splurge they would never buy themselves."),
   ("parmoregolf-camo-1-4-zip-rebrand-1", "Parmore camo quarter-zip", "Parmore", "Camo Quarter-Zip", "Compliments Guaranteed."),
   ("criquetshirts-alpaca-sweater-hoodie-treetop-1", "A man in a green Criquet alpaca hoodie", "Criquet", "Alpaca Sweater Hoodie", "A Fresh New Colorway."),
   ("fyfegolf-mackenzie-golf-bag-x-fyfe-23rd-edtion-1", "The black waxed canvas MacKenzie x Fyfe 23rd Edition bag", "Fyfe x MacKenzie", "23rd Edition Bag", "The One They&rsquo;d Never Buy Themselves.")]),
 ("giftguide3", "golf-gift-guide-2026-heirlooms-tiny-makers-off-season", "The 2026 Gift Guide, Part 3: Heirlooms, Tiny Makers and Off-Season Gifts", "gift-guide-3b", [
   ("card-hero", "A brown leather Sun Mountain stand bag and duffle on the grass", "Gift Guide 2026", "Part 3 of 3", "Thirty brands: things built to be handed down, makers small enough to fit in a golf cart, and layers for the cold months."),
   ("sunmountain-legacy-leather-stand-bag-1", "Sun Mountain Legacy leather stand bag", "Sun Mountain", "Legacy Leather Stand Bag", "Will Last a Lifetime."),
   ("austinknittylimits-two-golf-club-head-covers-ret-1", "Hand-knit blue and white headcovers", "AustinKnittyLimits", "Hand-Knit Headcovers", "Made by a Handful of People."),
   ("sloat-mens-ventile-windbreaker-1", "A man in a SLOAT organic Ventile jacket", "SLOAT", "Organic Ventile Jacket", "For the Off-Season.")]),
]
def marks(key): return f"<!-- TGI-{key.upper()}-CARD -->\n", f"<!-- /TGI-{key.upper()}-CARD -->\n"
def build_card(key, slug, title, imgdir, slides):
    url = f"/drops/{slug}"; m, e = marks(key)
    s = "\n".join(
        f'          <div class="gear-slide">\n            <a href="{url}">\n'
        f'              <img src="/images/{imgdir}/{img}.jpg" alt="{html.escape(alt)}" loading="lazy" />\n'
        f'              <div class="gear-slide-info"><div class="gear-slide-brand">{brand}</div><div class="gear-slide-name">{head}</div></div>\n'
        f'            </a>\n          </div>' for img, alt, brand, head, _ in slides)
    return (m + f'{CARD_OPEN}"drop">\n    <div class="card-media" style="position:relative;">\n'
            f'      <span class="card-tag grass">[Drops &amp; Brands]</span>\n'
            f'      <div class="gear-carousel" data-carousel="{key}">\n        <div class="gear-carousel-track">\n{s}\n        </div>\n'
            f'        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>\n'
            f'        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>\n      </div>\n    </div>\n'
            f'    <div class="card-body">\n'
            f'      <div class="card-title"><a href="{url}" style="color:inherit;text-decoration:none;border-bottom:none;">{title}</a></div>\n'
            f'      <p class="card-text" data-slidetext="{key}">{slides[0][4]}</p>\n'
            f'      <div class="gear-dots" data-dots="{key}"></div>\n'
            f'      <div class="gear-counter" data-counter="{key}">1 / {len(slides)}</div>\n'
            f'    </div>\n  </div>\n' + e)
def main(apply_):
    h = HOME.read_text(encoding="utf-8"); original = h
    new_at_top = []
    for key, slug, title, imgdir, slides in PARTS:
        m, e = marks(key)
        h = re.sub(r"\n    %s: \[\n.*?\n    \],?(?=\n)" % key, "", h, flags=re.S)
        card = build_card(key, slug, title, imgdir, slides)
        if m in h:
            i = h.index(m); h = h[:i] + card + h[h.index(e, i) + len(e):]
        else:
            if f'href="/drops/{slug}"' in h: sys.exit(f"! index already links {slug} outside the card")
            new_at_top.append(card)
        mm = re.search(r"window\._slideTexts\s*=\s*\{\n", h)
        arr = ",\n".join('      "%s"' % html.unescape(t).replace('"', '\\"') for *_, t in slides)
        h = h[:mm.end()] + f"    {key}: [\n{arr}\n    ],\n" + h[mm.end():]
    if new_at_top:
        anchor = 'aria-label="Content feed">\n'; i = h.index(anchor) + len(anchor)
        h = h[:i] + "".join(new_at_top) + h[i:]
    print(f"  feed cards {original.count(CARD_OPEN)} -> {h.count(CARD_OPEN)}")
    if not apply_: print("  dry run — pass --apply"); return
    bad = []
    for key, slug, title, imgdir, slides in PARTS:
        m, e = marks(key); blk = h[h.index(m):h.index(e)]
        if h.count(f'href="/drops/{slug}"') != blk.count(f'href="/drops/{slug}"'): bad.append(f"{key}: outside link")
        for img, *_ in slides:
            if not (ROOT / f"images/{imgdir}/{img}.jpg").is_file(): bad.append(f"{key}: missing {img}")
        if not (ROOT / f"drops/{slug}.html").is_file(): bad.append(f"{key}: post missing")
        if re.search(r"\bworth\b", blk, re.I): bad.append("banned word")
    if bad: sys.exit("! not written. " + "; ".join(bad))
    HOME.write_text(h, encoding="utf-8"); print("  wrote index.html — gift guide Parts 1-3 in slots 1-3")
if __name__ == "__main__": main("--apply" in sys.argv)
