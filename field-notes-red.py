#!/usr/bin/env python3
"""field-notes-red.py — every [Field Notes] tag on the homepage is red (flag).
29 Sep 2026. Lenny: "change the tag color to red on all the field notes boxes on the home page."
Wire scripts clone older cards (some grass, some unclassed), so this runs in the deploy
and re-applies after any new card goes in. Idempotent."""
import re, sys, pathlib
p = pathlib.Path(__file__).resolve().parent / "index.html"
s = p.read_text(encoding="utf-8")
n0 = s
s = re.sub(r'<span class="card-tag(?: (?:grass|ink|rough|flag))?"(?: style="position: static; background: var\(--grass\); color: var\(--paper\);")?>\[Field Notes\]</span>',
           lambda m: '<span class="card-tag flag">[Field Notes]</span>' if 'static' not in m.group(0)
           else '<span class="card-tag" style="position: static; background: var(--flag); color: var(--paper);">[Field Notes]</span>', s)
left = len(re.findall(r'class="card-tag(?! flag)[^"]*"(?![^>]*--flag)[^>]*>\[Field Notes\]', s))
if "--apply" in sys.argv and s != n0: p.write_text(s, encoding="utf-8")
print(f"field-notes-red: {s.count('[Field Notes]')} tags, non-red remaining {left}, {'changed' if s!=n0 else 'no change'}")
