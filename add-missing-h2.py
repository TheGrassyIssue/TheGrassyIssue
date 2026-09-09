#!/usr/bin/env python3
"""Add a real <h2> to the drop pages that ship without one.

WHY
---
Audit 2026-09-09: 14 drop pages had zero <h2>. They predate the house
"h2.products-hdr + p.cat-kicker per section" convention, so their product
groups are unlabelled — the page goes <h1> straight to a grid. That is a
heading-structure gap Google reads as a flat page, and on the multi-section
pages it means three distinct product groups are visually separated but
semantically identical.

EVERY HEADING BELOW IS HAND-WRITTEN AGAINST THE PAGE'S ACTUAL CONTENT.
Nothing is generated from a template. On the two multi-section pages the
groupings were read off the products themselves:

  the-golf-ball-edit   §1 tour balls (Titleist/Callaway/TaylorMade/Bridgestone)
                       §2 direct-to-consumer (Vice/Maxfli/Snell)
                       §3 alignment + visual (TP5 Pix, Truvis, Pro Drip, Divide)
  the-jersey-polo-edit §1 golf labels  §2 fashion houses  §3 football shirts

Idempotent: skips any page that already has an <h2>. Dry-run by default.
"""
import re, sys, os

# slug -> list of headings, one per <section class="products"> in document order.
SECTION_H2 = {
 "the-golf-ball-edit": [
   ("The Tour Balls &mdash; 9 Picks",
    "The premium urethane tier, and the balls the rest of the market is measured against."),
   ("Direct-to-Consumer &mdash; 3 Picks",
    "Same urethane construction, sold without the retail markup."),
   ("Alignment and Visual &mdash; 4 Picks",
    "Balls printed to help you see the line, or just to be findable."),
 ],
 "the-jersey-polo-edit": [
   ("The Golf Labels &mdash; 5 Picks",
    "Golf brands cutting a polo with a jersey collar rather than a placket."),
   ("The Fashion Houses &mdash; 3 Picks",
    "Where the knit polo crosses over from the pro shop into menswear."),
   ("Actual Football Shirts &mdash; 6 Picks",
    "The source material, from a Nike retro England kit to a Umbro johnny collar."),
 ],
}

# slug -> single heading inserted before the first product grid
GRID_H2 = {
 "ald-golf-ss26-new-releases": ("The Collection &mdash; 10 Pieces",
   "Aim&eacute; Leon Dore&rsquo;s SS26 golf range, priced and linked."),
 "manors-ss26": ("The Press Room Capsule &mdash; 6 Pieces",
   "The full SS26 Press Room drop from Manors."),
 "sugarloaf-ss26": ("The Collection &mdash; 6 Pieces",
   "Sugarloaf Social Club&rsquo;s SS26 range."),
}

# slug -> heading inserted after the intro on prose pages that carry no grid
PROSE_H2 = {
 "rodeo-dunes-the-great-divide": "Three Rounds, Red Versus Blue",
 "muni-kids-10-years": "Ten Years of the Muni Kids Program",
 "manors-gentleman-jack": "The Collaboration",
 "metalwood-ss26-picks": "The SS26 Picks",
 "malbon-summer-gallo-colorido": "Inside the Gallo Colorido Collection",
 "premium-tees-carousel": "Six Tees That Cost More Than Lunch",
 "bold-tees-carousel": "The Bold Tees",
 "hats-carousel": "The Hats",
 "the-masters-ticket-lottery-is-open-you-have-twenty-days": "How the Lottery Works",
}

HDR = '  <h2 class="products-hdr">{h}</h2>\n  <p class="cat-kicker">{k}</p>\n'

def fix(path, apply_):
    h = open(path, encoding="utf-8").read()
    if re.search(r'<h2[\s>]', h):
        return "already has h2"
    slug = os.path.basename(path)[:-5]
    out, what = h, None

    if slug in SECTION_H2:
        heads = SECTION_H2[slug]
        secs = list(re.finditer(r'<section class="products">', h))
        if len(secs) != len(heads):
            return f"!! {len(secs)} sections but {len(heads)} headings — skipped"
        # insert back-to-front so earlier offsets stay valid
        for m, (hd, kk) in zip(reversed(secs), reversed(heads)):
            out = out[:m.end()] + "\n" + HDR.format(h=hd, k=kk) + out[m.end():]
        what = f"{len(heads)} section h2"

    elif slug in GRID_H2:
        hd, kk = GRID_H2[slug]
        m = re.search(r'<section class="products">', out)
        if not m: return "!! no <section class=\"products\"> anchor"
        out = out[:m.end()] + "\n" + HDR.format(h=hd, k=kk) + out[m.end():]
        what = "1 grid h2"

    elif slug in PROSE_H2:
        hd = PROSE_H2[slug]
        # place it after the intro writeup, before the body continues
        m = re.search(r'</div>\s*</div>\s*(?=<)', out[out.find('class="writeup"'):]) if 'class="writeup"' in out else None
        if m:
            base = out.find('class="writeup"')
            pos = base + m.end()
        else:
            m2 = re.search(r'</header>', out)
            if not m2: return "!! no anchor for prose h2"
            pos = m2.end()
        out = out[:pos] + f'\n<h2 class="products-hdr">{hd}</h2>\n' + out[pos:]
        what = "1 prose h2"
    else:
        return "not in map"

    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return what

def main():
    apply_ = "--apply" in sys.argv
    targets = sorted(set(SECTION_H2) | set(GRID_H2) | set(PROSE_H2))
    n = 0
    for slug in targets:
        p = f"drops/{slug}.html"
        if not os.path.exists(p):
            print(f"  {slug:56} !! missing file"); continue
        r = fix(p, apply_)
        print(f"  {slug:56} {r}")
        if r and not r.startswith(("!!", "already", "not in")): n += 1
    print(f"\n{'updated' if apply_ else 'would update'} {n} page(s)")
    if not apply_: print("(dry run — pass --apply)")

if __name__ == "__main__":
    main()
