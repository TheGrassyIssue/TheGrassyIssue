#!/usr/bin/env python3
"""
apply-bold-headers.py — retire the tiny mono section header for the bold serif one.

Lenny, 2026-08-30, shown both styles side by side: "I prefer the bold headers
not that other option on the bottom and keep the paragraph sizing consistent."

The site had two section-header families:
  * bold serif  — h2 at clamp(24px,2.6vw,32px), weight 600 (27 recent posts)
  * tiny mono   — .products-hdr at 10px uppercase mono, opacity .55 (159 pages,
                  the Kingfisher-template family)
This converts the second family to the first by rewriting the .products-hdr
CSS rule on every page that defines it. No markup is touched — the class stays
in the HTML, only what it MEANS changes, which also future-proofs the builders
that copy template heads.

The `.sec` modifier (30 pages) keeps its hairline divider and spacing but loses
its 11px font override so the serif size applies there too.

Idempotent via the /*TGI-HDR-BOLD-V1*/ marker. Dry run by default.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "/*TGI-HDR-BOLD-V1*/"

OLD_BASE = re.compile(
    r"\.products-hdr\s*\{\s*font-family:\s*var\(--mono\)[^}]*\}")
NEW_BASE = (MARK +
    ".products-hdr{font-family:var(--serif);font-weight:600;"
    "font-size:clamp(24px,2.6vw,32px);line-height:1.15;margin:0 0 20px}")

OLD_SEC = re.compile(r"\.products-hdr\.sec\s*\{[^}]*\}")
NEW_SEC = (".products-hdr.sec{margin:44px 0 20px;"
           "border-top:.5px solid var(--ink);padding-top:18px}")


def fix(path, apply_):
    h = open(path, encoding="utf-8").read()
    if MARK in h:
        return None
    out, n = OLD_BASE.subn(NEW_BASE, h)
    if not n:
        return None
    out = OLD_SEC.sub(NEW_SEC, out)
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return n


def main(apply_=False):
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "drops", "*.html")) +
                    glob.glob(os.path.join(ROOT, "guides", "*.html"))):
        if fix(p, apply_):
            n += 1
    print(("converted" if apply_ else "would convert"), n, "pages to bold serif headers")
    if not apply_:
        print("(dry run - pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
