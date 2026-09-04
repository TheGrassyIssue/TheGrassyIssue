#!/usr/bin/env python3
"""
add-nav-search-box.py — insert the #tgi-sbox search input into navs that lack it.

WHY THIS EXISTS
---------------
Two separate pieces make site search work on a page:
  1. the BOX   — <div id="tgi-sbox"> with #tgi-search-input / #tgi-search-results
  2. the WIRING — the "<!-- TGI SEARCH -->" script that fetches /search-index.json
install-search.py owns (2) and explicitly refuses to guess about (1): its docstring
assumes apply-header.py has already put the box in the nav.

But apply-header.py works off a fixed TARGETS dict, and build-brands.py writes its
own nav for the 98 per-brand coverage pages — a nav with no search box (the same
omission that left those pages with no hamburger, see reference_mobile_nav bug 3).
Net effect found 2026-09-04: brand pages carried the search CSS and JS but had no
input element at all, so search was simply absent there. /brands/index.html was
fine; only the per-brand children were affected.

Idempotent (skips a nav that already has the box), dry-run by default.
Re-run after build-brands.py, alongside fix-mobile-menu.py / fix-mobile-nav.py.
"""
import os, re, sys, glob

BOX = ('    <div id="tgi-sbox">\n'
       '      <input id="tgi-search-input" type="search" placeholder="Search" '
       'autocomplete="off" aria-label="Search the site" />\n'
       '      <div id="tgi-search-results"></div>\n'
       '    </div>\n')

def fix(path, apply_):
    h = open(path, encoding="utf-8").read()
    if 'id="tgi-sbox"' in h:
        return "already has box"
    if "tgi-search-input" not in h:
        return "no search JS — run install-search.py first"
    m = re.search(r'(<button class="nav-toggle".*?</button>\s*\n)', h, re.S)
    if not m:
        return "!! no .nav-toggle anchor — skipped"
    out = h[:m.end()] + BOX + h[m.end():]
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return "inserted"

def main():
    apply_ = "--apply" in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(glob.glob("brands/*.html"))
    n = 0
    for p in paths:
        r = fix(p, apply_)
        if r == "inserted": n += 1
        elif r.startswith("!!"): print(f"  {os.path.basename(p):34} {r}")
    print(f"{'inserted' if apply_ else 'would insert'} box on {n} page(s) of {len(paths)}")
    if not apply_: print("(dry run — pass --apply)")

if __name__ == "__main__":
    main()
