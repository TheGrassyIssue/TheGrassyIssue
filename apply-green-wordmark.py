#!/usr/bin/env python3
"""
apply-green-wordmark.py — masthead in the house green.

Lenny, 2026-08-29: "let's do The header in a nice dark green that fits the motif."
Chose the wordmark text in green over a full green nav bar, because on the
homepage a green bar sits directly under the green ticker strip and the two merge
into one slab (and post pages have no ticker, so the two page types would diverge).

Uses var(--grass) #2D4A2B - already in the palette, nothing new introduced.

Runs AFTER apply-wordmark.py: it appends `color` to the same .nav-wordmark rule
that script writes, matching on its /*TGI-WM-V1*/ marker so the two stay coupled.
Idempotent.
"""
import os, re, glob, json, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "/*TGI-WM-V1*/"


def main(apply_=False):
    paths = sorted(p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
                   if "/drafts/" not in p.replace(os.sep, "/"))
    inv, changed, missing = {}, 0, 0
    for p in paths:
        s = open(p, encoding="utf-8", errors="replace").read()
        if MARK not in s:
            if "nav-wordmark" in s:
                missing += 1
            continue
        m = re.search(r"(\.nav-wordmark\{" + re.escape(MARK) + r")([^}]*)\}", s)
        if not m:
            continue
        body = m.group(2)
        if "color:var(--grass)" in body:
            continue
        body_new = re.sub(r";?color:[^;}]*", "", body) + ";color:var(--grass)"
        new = s[:m.start()] + m.group(1) + body_new + "}" + s[m.end():]
        if new != s:
            changed += 1
            if apply_:
                b = open(p, "rb").read()
                inv[os.path.relpath(p, ROOT)] = {"size": len(b),
                                                 "sha1": hashlib.sha1(b).hexdigest()}
                open(p, "w", encoding="utf-8").write(new)
    if apply_ and inv:
        os.makedirs(os.path.join(ROOT, "research"), exist_ok=True)
        json.dump(inv, open(os.path.join(ROOT, "research",
                                         "green-wordmark-inventory.json"), "w"), indent=1)
    print(f"{'greened' if apply_ else 'would green'} {changed} page(s)")
    if missing:
        print(f"  !! {missing} page(s) have a wordmark but no {MARK} marker "
              f"- run apply-wordmark.py first")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
