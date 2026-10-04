#!/usr/bin/env python3
"""Keep the brand count on About and Work With Us equal to data/brands.json.

The count is written by hand in prose on those pages, so it drifted (About said
131 in one paragraph and 127 in another while the Index held 156). This rewrites
any "<N> brands" / "<N> independent golf brands" phrase on the listed pages to
the live count. Run with --apply; build-brands.py calls it automatically.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["about.html", "work-with-us.html"]
n = len(json.load(open(os.path.join(ROOT, "data/brands.json"))))
pat = re.compile(r"\b\d{2,3}(?= (?:independent |indie )?(?:golf )?brands\b)")
apply_ = "--apply" in sys.argv
for p in PAGES:
    f = os.path.join(ROOT, p)
    s = open(f, encoding="utf-8").read()
    found = pat.findall(s)
    new = pat.sub(str(n), s)
    print(f"{p}: counts found {found or 'none'} -> {n}")
    if apply_ and new != s:
        open(f, "w", encoding="utf-8").write(new)
