#!/usr/bin/env python3
"""wire-evening-spots-2-fieldguide.py — add Evening Spots Vol. 2 to the Field Guide. 10 Oct 2026.
One guide card, placed directly after the Vol. 1 card, in the
same house markup. Idempotent; dry run by default."""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "field-guide/index.html")
SLUG = "/drops/evening-spots-vol-2-best-austin-bars"
CARD = f'''    <a href="{SLUG}" class="guide-card">
      <img class="guide-card-img" src="/images/field-guide/evening-spots-2.jpg" alt="The main bar at The Roosevelt Room in downtown Austin" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">Evenings &middot; 15 Bars</div>
        <div class="guide-card-title">Evening Spots Vol. 2 &mdash; 15 of the Best Bars in Austin</div>
        <div class="guide-card-desc">Cocktail rooms, patios, dives and a jazz basement, from The Roosevelt Room to a mug of Lone Star at Deep Eddy.</div>
        <span class="guide-card-link">Read the guide &rarr;</span>
      </div>
    </a>
'''
def main(apply_):
    s = open(F, encoding="utf-8").read()
    if f'href="{SLUG}" class="guide-card"' in s:
        print("field guide: Evening Spots Vol. 2 card already present"); return
    i = s.index('<a href="/drops/5-post-round-evening-spots-in-austin" class="guide-card">')
    j = s.index('</a>', i) + len('</a>\n')
    s = s[:j] + CARD + s[j:]
    assert s.count(SLUG) == 1
    print("field guide: added Evening Spots Vol. 2 after Vol. 1" + ("" if apply_ else " (dry run)"))
    if apply_: open(F, "w", encoding="utf-8").write(s)
if __name__ == "__main__":
    main("--apply" in sys.argv)
