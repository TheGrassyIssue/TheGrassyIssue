#!/usr/bin/env python3
"""
make-merrill-revisited.py — 18 September 2026.

Lenny: "I wanted the Merrill golf post to be a brand revisited so it would show
up on the front page as a fresh box."

Two things were wrong, and they are separate problems.

1. THE CARD WAS BURIED. It went in above the Devereux card, which put it at
   position 10 of 131 — nested among the OLD Brand Revisited cards. A reader
   scanning the feed reads position 10 as archive, not as news. It moves to the
   top.

2. THE PAGE STILL SAID "BRAND TO KNOW". The homepage card said Revisited, the
   page it opened said Brand to Know. Retitled throughout — h1, <title>, og,
   twitter, schema headline, breadcrumb.

WHAT IS DELIBERATELY NOT CHANGED: the slug. /drops/brand-to-know-merrill-golf
keeps its URL and therefore its search equity, its brands.json entry and its
five inbound mentions. Jones got a separate brand-revisited- page; doing that
here means a 301 and a fresh URL with no history, which Lenny has not asked for.
Say the word and it is a five-minute follow-up.

Idempotent.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-merrill-golf.html"
IDX  = ROOT / "index.html"
MARK = "<!-- BRAND REVISITED — Merrill Golf -->"

OLD = "Brand to Know &mdash; Merrill Golf"
OLD2 = "Brand to Know — Merrill Golf"
NEW = "Brand Revisited &mdash; Merrill Golf, and the Polo They Never Made"
NEW2 = "Brand Revisited — Merrill Golf, and the Polo They Never Made"


def retitle(apply_):
    t = PAGE.read_text(encoding="utf-8")
    before = t
    n = t.count(OLD) + t.count(OLD2)
    t = t.replace(OLD, NEW).replace(OLD2, NEW2)
    ok = [
        # SCOPE. Not "the string is absent" — the page carries More-from-the-Feed
        # cards pointing at OTHER Brand to Know posts (Cloud & Wind), and those
        # are correct. What must be gone is Merrill being called a Brand to Know.
        ("no 'Brand to Know' still attached to MERRILL",
         not re.search(r"Brand to Know[^<]{0,12}Merrill", t), ""),
        ("h1 is the Revisited title",
         bool(re.search(r"<h1[^>]*>\s*Brand Revisited", t)), ""),
        ("title tag updated", "Brand Revisited" in re.search(r"<title>([^<]*)</title>", t).group(1), ""),
        ("document still closes", t.rstrip().endswith("</html>"), ""),
        ("JSON-LD still parses", _json_ok(t), ""),
    ]
    good = True
    for l, p, d in ok:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d}"); good &= p
    if not good:
        sys.exit("! refusing to write the page")
    print(f"  retitled {n} occurrence(s)")
    if apply_ and t != before:
        PAGE.write_text(t, encoding="utf-8")
    return t != before


def _json_ok(t):
    import json
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(b)
        except Exception: return False
    return True


def move_card(apply_):
    h = IDX.read_text(encoding="utf-8")
    m = re.search(re.escape(MARK) + r".*?(?=\n\s*<!-- )", h, re.S)
    if not m:
        sys.exit("! Merrill card not found in index.html")
    card = m.group(0)
    rest = h[:m.start()] + h[m.end():]

    # first card in the feed = the one the top-of-feed comment precedes
    first = re.search(r'<!-- [^>]{3,70} -->\s*<div class="card"', rest)
    if not first:
        sys.exit("! could not find the first feed card")
    if h.index(MARK) < first.start():
        print("  card already at the top — no move"); return False

    out = rest[:first.start()] + card.rstrip() + "\n\n  " + rest[first.start():]
    checks = [
        ("exactly one Merrill card", out.count(MARK) == 1),
        ("card count unchanged",
         len(re.findall(r'<div class="card"', out)) == len(re.findall(r'<div class="card"', h))),
        ("Merrill is now first",
         out.index(MARK) < re.search(r'<!-- [^>]{3,70} -->\s*<div class="card"',
                                     out[out.index(MARK)+len(MARK):]).start() + out.index(MARK)+len(MARK)),
        ("div tags balance", out.count("<div") == h.count("<div")),
    ]
    good = True
    for l, p in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}"); good &= p
    if not good:
        sys.exit("! refusing to write index.html")
    if apply_:
        IDX.write_text(out, encoding="utf-8")
    return True


if __name__ == "__main__":
    a = "--apply" in sys.argv
    print("== page =="); retitle(a)
    print("== feed card =="); move_card(a)
    print("\n  written" if a else "\n  dry run — pass --apply")
