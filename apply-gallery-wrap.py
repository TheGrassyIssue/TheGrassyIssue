#!/usr/bin/env python3
"""apply-gallery-wrap.py — post galleries loop around. 8 Oct 2026.
Lenny: "when you click the last arrow on the boxes scrolling through the images it circles back around to the first
image". Every post gallery runs the same inline script; its arrows clamped at the ends. This rewrites the two arrow
handlers so "next" on the last frame goes to the first and "prev" on the first goes to the last. Dots and swipe are
unchanged. The homepage carousels (gearSlide) already wrap. Idempotent; runs in Deploy TGI.command. Dry run by default.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = [("go(idx()-1); });", "go((idx()-1+n)%n); });"), ("go(idx()+1); });", "go((idx()+1)%n); });")]

def main(apply_):
    changed = 0; total = 0
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in ("research", "drafts", "previews", ".git") or re.search(r" \d+\.html$", rel):
            continue
        try: s = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError): continue
        if "pg-track" not in s: continue
        total += 1
        new = s
        for a, b in OLD: new = new.replace(a, b)
        if new != s:
            changed += 1
            if apply_: open(f, "w", encoding="utf-8").write(new)
    print(f"apply-gallery-wrap: {total} gallery page(s), {changed} {'updated' if apply_ else 'would change'}")

if __name__ == "__main__":
    main("--apply" in sys.argv)
