#!/usr/bin/env python3
"""apply-brand-counts.py — keep the About page's brand count equal to data/brands.json (16 Oct 2026).
The About page said "181 brands" after the index grew to 187. Rewrites only the two phrases that state
the count ("an index of N brands", "a roster of N brands"). Idempotent; dry run without --apply."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
n = len(json.loads((ROOT / "data/brands.json").read_text()))
changed = []
for rel in ["about.html"]:
    f = ROOT / rel; t = f.read_text(encoding="utf-8")
    u = re.sub(r"(an index of |a roster of )\d+( brands)", rf"\g<1>{n}\g<2>", t)
    if u != t:
        changed.append(rel)
        if "--apply" in sys.argv: f.write_text(u, encoding="utf-8")
print(f"apply-brand-counts: {n} brands; {len(changed)} page(s) {'updated' if '--apply' in sys.argv else 'would change'} {changed}")
