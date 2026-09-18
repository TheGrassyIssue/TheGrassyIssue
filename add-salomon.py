#!/usr/bin/env python3
"""
add-salomon.py — put Salomon in the brand index, and hand it Realtree's seat
on the Gorpcore tag. 18 September 2026. Idempotent: run it twice, nothing moves.

Lenny: "let's swap out realtree for a different brand" -> "let's do Salomon".

Realtree is NOT deleted. It keeps its own TGI post and its loud-on-purpose and
collab-machine tags; only the gorpcore tag changes hands, because the swap Lenny
asked for was on the Gorpcore page. Removing a brand from the index outright
would break /drops/puma-golf-x-realtree-precision-in-the-wild and two other tag
pages for no reason he asked for.

Every fact in the Salomon line is from salomon.com/en-us/lp/g/who-we-are,
read 18 September 2026: founded 1947 in Annecy, French Alps; the XT-6 (2013)
and Speedcross are its own named icon lines.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
BRANDS = ROOT / "data/brands.json"
EXTRAS = ROOT / "tag-page-extras.py"

SALOMON = {
    "slug": "salomon",
    "name": "Salomon",
    "loc": "Annecy, France",
    "regions": ["europe"],
    "cats": ["apparel"],
    "line": ("Alpine sports house founded in Annecy in 1947; its XT-6 and "
             "Speedcross trail shoes are the ones that turn up on muni tee boxes."),
    "url": "/drops/the-best-non-golfing-golf-shoe-5-trail-runners-that-belong-o",
    "tags": ["gorpcore", "post-round-friendly"],
    "attrs": ["heritage", "new-to-index"],
    "added": "2026-09-18",
    "img": "/images/salomon/xt-6-walnut-card.jpg",
}

TILE = ('  ("Salomon", "/brands/salomon", "/images/gorpcore/salomon-xt6-1.jpg",\n'
        '   "Salomon XT-6 trail shoe in walnut, side profile"),\n')

OLD_TAIL = ('out of San Francisco, and Realtree &mdash; the camouflage licensor, now "\n'
            '    "turning forty &mdash; has golf collabs running at PUMA and Sun Mountain. Ten "\n'
            '    "brands, one shared instinct: dress for the walk, not the clubhouse.",')
NEW_TAIL = ('out of San Francisco, and Salomon has been making alpine gear in "\n'
            '    "Annecy since 1947 &mdash; the XT-6 arrived as a trail shoe and got "\n'
            '    "adopted by everyone else. Ten brands, one shared instinct: dress for "\n'
            '    "the walk, not the clubhouse.",')

OLD_NOTE = ("# Realtree is the tenth brand on this tag and has no localised imagery yet, so\n"
            "# it is absent from the grid rather than represented by a borrowed photograph;\n"
            "# nine tiles also happen to make a clean 3x3.\n")
NEW_NOTE = ("# Salomon took Realtree's seat on this tag in September 2026 and arrived with\n"
            "# its own localised product shot, so the grid is ten tiles rather than nine.\n")


def do_brands(apply_):
    items = json.loads(BRANDS.read_text(encoding="utf-8"))
    changed = []

    idx = next((i for i, x in enumerate(items) if x["slug"] == "salomon"), None)
    if idx is None:
        # Slot it in alphabetically and leave every other entry exactly where it
        # is. The file's order is human, not machine-sorted (ANTi before A.P.C.),
        # and build-brands.py re-sorts at render time anyway — so a global sort
        # here would churn 133 lines to no effect and lose whatever that order
        # is carrying.
        at = next((i for i, x in enumerate(items)
                   if x["name"].lower() > SALOMON["name"].lower()), len(items))
        items.insert(at, dict(SALOMON))
        changed.append(f"added salomon (position {at}, after {items[at-1]['name']!r})")
    elif items[idx] != SALOMON:
        items[idx] = dict(SALOMON); changed.append("refreshed salomon")

    rt = next((x for x in items if x["slug"] == "realtree"), None)
    if rt and "gorpcore" in rt.get("tags", []):
        rt["tags"] = [t for t in rt["tags"] if t != "gorpcore"]
        changed.append("realtree: dropped gorpcore (kept %s)" % ", ".join(rt["tags"]))

    if apply_ and changed:
        BRANDS.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    return changed, items


def do_extras(apply_):
    s = EXTRAS.read_text(encoding="utf-8")
    orig, changed = s, []

    if '"/brands/salomon"' not in s:
        anchor = ('  ("Sunday Golf", "/brands/sunday-golf", '
                  '"/images/gorpcore/sunday-elcamino-1.jpg",\n'
                  '   "Sunday Golf El Camino lightweight carry bag"),\n')
        if anchor not in s:
            sys.exit("! gallery anchor not found — refusing to guess where the tile goes")
        s = s.replace(anchor, anchor + TILE, 1); changed.append("gallery: +Salomon tile")

    if OLD_NOTE in s:
        s = s.replace(OLD_NOTE, NEW_NOTE, 1); changed.append("gallery note rewritten")

    if OLD_TAIL in s:
        s = s.replace(OLD_TAIL, NEW_TAIL, 1); changed.append("write-up: Realtree -> Salomon")
    else:
        # Guard against a half-done swap: Realtree must be gone from the PROSE.
        # Checking the bare name is wrong — NEW_NOTE says "Salomon took
        # Realtree's seat", which is a comment and should stay.
        prose = "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("#"))
        if "Realtree" in prose and "Salomon has been making alpine gear" not in prose:
            sys.exit("! Realtree still in the write-up but the tail did not match "
                     "— refusing to guess; fix OLD_TAIL by hand")

    if apply_ and s != orig:
        EXTRAS.write_text(s, encoding="utf-8")
    return changed


if __name__ == "__main__":
    apply_ = "--apply" in sys.argv
    b, items = do_brands(apply_)
    e = do_extras(apply_)
    for line in b + e:
        print("  " + line)
    if not (b or e):
        print("  no change — already applied")
    print(f"\n  {len(items)} brands in the index"
          + ("" if apply_ else "   [dry run — pass --apply]"))
