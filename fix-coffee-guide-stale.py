#!/usr/bin/env python3
"""
fix-coffee-guide-stale.py — two stale entries on a live page. 18 Sept 2026.

Found while researching the new café Field Note. Both are the kind of error a
reader discovers by driving somewhere.

1. GREATER GOODS' AUSTIN CAFÉS ARE CLOSED. Both of them — 2501 E 5th St and
   12005 Bee Caves Rd. Their own website no longer lists an Austin café at all,
   only the Dripping Springs roastery, and Yelp has both marked closed as of
   Aug/Sep 2026. The roasting company still exists; the cafés a golfer would
   drive to at 7am do not. The card comes out, and the count drops 18 -> 17.

2. CAFFÉ MEDICI IS NOW MEDICI ROASTING. caffemedici.com redirects to
   mediciroasting.com. The name and the outbound link both need updating, on
   this page and on the homepage card.

Idempotent. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
GUIDE = ROOT / "drops/austin-coffee-guide.html"
INDEX = ROOT / "index.html"

COUNTS = [
    ("18 Austin Coffee Shops", "17 Austin Coffee Shops"),
    ("Eighteen independent Austin coffee shops", "Seventeen independent Austin coffee shops"),
    ("<span>18 Shops</span>", "<span>17 Shops</span>"),
    ("Eighteen shops, one rule", "Seventeen shops, one rule"),
    ("<span>18</span>", "<span>17</span>"),
    ("18 Pre-Round Pours", "17 Pre-Round Pours"),
]
MEDICI = [
    ("Caff&eacute; Medici", "Medici Roasting"),
    ("Caffé Medici", "Medici Roasting"),
    ("Caffe Medici", "Medici Roasting"),
    ("https://caffemedici.com/", "https://mediciroasting.com/"),
    ("caffemedici.com", "mediciroasting.com"),
]


def drop_greater_goods(t):
    """Cut the whole <a class="product-card"> ... </a> block for Greater Goods."""
    i = t.find("greatergoodsroasting.com")
    if i < 0:
        return t, False
    start = t.rfind('<a href=', 0, i)
    if start < 0:
        sys.exit("! could not find the start of the Greater Goods card")
    end = t.find("</a>", t.find("product-link", start))
    if end < 0:
        sys.exit("! could not find the end of the Greater Goods card")
    end += len("</a>")
    return t[:start].rstrip() + "\n\n    " + t[end:].lstrip(), True


def run(apply_):
    g = GUIDE.read_text(encoding="utf-8")
    before_cards = g.count('class="product-card"')
    orig = g

    # ALREADY-APPLIED IS NOT A FAILURE. The checks below assert "exactly one card
    # was removed", which can only be true on the first run. On a second pass
    # there is nothing left to remove, the count check fails, and the script
    # would report a broken page that is in fact already correct. Same trap the
    # Merrill FAQ fixer hit. Detect the finished state first.
    if ("greatergoodsroasting" not in g and "caffemedici" not in g
            and "Medici Roasting" in g and "17 Austin Coffee Shops" in g):
        print("  no change — already applied")
        return

    g, cut = drop_greater_goods(g)
    for a, b in COUNTS + MEDICI:
        g = g.replace(a, b)

    idx = INDEX.read_text(encoding="utf-8")
    idx_orig = idx
    for a, b in MEDICI:
        idx = idx.replace(a, b)

    checks = [
        ("Greater Goods card removed",
         "greatergoodsroasting" not in g and "greater-goods.jpg" not in g, ""),
        ("exactly one card removed",
         g.count('class="product-card"') == before_cards - 1,
         f"{before_cards} -> {g.count(chr(34)+'product-card'+chr(34))}"),
        ("no '18 shops' claim left",
         not re.search(r"\b18 (Austin Coffee Shops|Shops|Pre-Round)", g)
         and "Eighteen" not in g, ""),
        ("no stale Medici name on the guide",
         "Medici" not in g or "Caff" not in g, ""),
        ("no caffemedici.com anywhere",
         "caffemedici" not in g and "caffemedici" not in idx, ""),
        ("guide still closes", g.rstrip().endswith("</html>"), ""),
        ("anchor tags balance",
         g.count("<a ") == g.count("</a>"), f'{g.count("<a ")}/{g.count("</a>")}'),
        ("no other content lost",
         abs(len(re.findall(r"<img", g)) - (len(re.findall(r"<img", orig)) - 1)) == 0, ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d}"); ok &= p
    if not ok:
        sys.exit("\n! refusing to write")

    if g == orig and idx == idx_orig:
        print("\n  no change — already applied"); return
    print(f"\n  guide: {len(orig):,} -> {len(g):,} bytes  (card removed: {cut})")
    print(f"  index: {'updated' if idx != idx_orig else 'unchanged'}")
    if apply_:
        GUIDE.write_text(g, encoding="utf-8")
        INDEX.write_text(idx, encoding="utf-8")
        print("  written")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    run("--apply" in sys.argv)
