#!/usr/bin/env python3
"""apply-hover-fix.py — stop homepage feed cards jumping under the sticky filter bar. 9 November 2026.
Lenny: "when i hover the mouse over the filters theres a box that spazzes out" (a card under the bar jumps).
Cause: .card:hover lifts the card 3px (translateY). Near the sticky filter bar and at card edges the lift moves
the card out from under the cursor, hover drops, the card falls back, hover returns: a loop.
Fix: feed cards keep the hover shadow and image zoom but no longer move; the bar sits above the feed on its own
layer; pills only fade colors. Injected as one marked <style> into index.html and feed/page-*.html; idempotent.
Runs every deploy after apply-no-readmore.py. Dry run by default.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "tgi-hover-fix"
CSS = (f'<style id="{MARK}">'
       '.feed .card:hover,.feed .card.visible:hover{transform:translateY(0)!important}'
       '.filters{z-index:30;isolation:isolate}'
       '.pill{transition:background-color .15s,color .15s!important}'
       '</style>')
apply_ = "--apply" in sys.argv
n = 0
for p in [os.path.join(ROOT, "index.html")] + sorted(f for f in glob.glob(os.path.join(ROOT, "feed/page-*.html")) if " " not in os.path.basename(f)):
    h = open(p, encoding="utf-8").read()
    new = re.sub(rf'<style id="{MARK}">.*?</style>', CSS, h, flags=re.S) if MARK in h else h.replace("</head>", CSS + "\n</head>", 1)
    if new != h:
        n += 1
        if apply_: open(p, "w", encoding="utf-8").write(new)
print(f"  hover fix: {n} file(s) " + ("updated" if apply_ else "would change — dry run, pass --apply"))
