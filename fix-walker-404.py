#!/usr/bin/env python3
"""
fix-walker-404.py — one genuine 404 on a live page. 18 September 2026.

Found by the sitewide /drops/ link sweep written while finishing the Morning
Round Field Note. The Hiroki Brand to Know page says "We covered Walker
separately" and links to /drops/brand-to-know-walker-golf, which has never
existed. There is no redirect for it in vercel.json either, so it is a hard 404
for a reader and a dead internal link for a crawler.

Two Walker posts exist. The right one is the Par-Tec drop, whose <title> is
"Walker Golf — The Australian Skate-Golf Brand" — that is the Brand-to-Know
style piece the Hiroki sentence is pointing at. The Blooming Grounds post is a
seasonal collection drop and would not read as "we covered Walker".

NOT FIXED HERE, deliberately: six brand pages link to
/drops/10-white-tees-to-beat-the-texas-heat, which IS 301'd in vercel.json to
/drops/the-white-tee-edit-2026. Those resolve — they just take an extra hop.
Repointing them is a tidy-up across six files, which is a different job from
this one-line fix, and is Lenny's call.

Idempotent. Dry run by default.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-hiroki-golf.html"
BAD  = '/drops/brand-to-know-walker-golf'
GOOD = '/drops/walker-golf-the-par-tec-drop'


def run(apply_):
    t = PAGE.read_text(encoding="utf-8")

    # ALREADY-APPLIED IS NOT A FAILURE.
    if BAD not in t:
        print("  no change — already applied"); return

    n = t.count(f'href="{BAD}"')
    out = t.replace(f'href="{BAD}"', f'href="{GOOD}"')

    checks = [
        ("the dead slug is gone", BAD not in out, ""),
        ("replaced exactly the links found", n >= 1 and out.count(f'href="{GOOD}"')
         == t.count(f'href="{GOOD}"') + n, f"{n} link(s)"),
        ("the new target exists",
         (ROOT / "drops" / f"{GOOD.split('/')[-1]}.html").exists(), ""),
        ("nothing else changed", len(out) == len(t) - n * (len(BAD) - len(GOOD)), ""),
        ("anchor tags balance", out.count("<a ") == out.count("</a>"), ""),
        ("document closes", out.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d}"); ok &= p
    if not ok:
        sys.exit("\n! refusing to write")

    if apply_:
        PAGE.write_text(out, encoding="utf-8"); print("\n  written")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    run("--apply" in sys.argv)
