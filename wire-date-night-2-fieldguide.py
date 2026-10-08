#!/usr/bin/env python3
"""wire-date-night-2-fieldguide.py — add Date Night Vol. 2 to the Field Guide. 8 Oct 2026.
Lenny: "make sure it's added to the field guide". One guide card, placed directly after the Vol. 1 card, in the
same house markup. Idempotent; dry run by default."""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "field-guide/index.html")
SLUG = "/drops/date-night-vol-2-austin-restaurants-for-reconnecting"
CARD = f'''    <a href="{SLUG}" class="guide-card">
      <img class="guide-card-img" src="/images/field-guide/date-night-2.jpg" alt="Fish Shop&rsquo;s dining room in East Austin, with leather banquettes and framed art" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">Date Night &middot; 15 Spots</div>
        <div class="guide-card-title">Date Night Vol. 2 &mdash; 15 Austin Restaurants for Reconnecting</div>
        <div class="guide-card-desc">Fifteen rooms where two people can actually talk, from Fish Shop&rsquo;s seafood counter and Lenoir&rsquo;s wine garden to two Michelin stars.</div>
        <span class="guide-card-link">Read the guide &rarr;</span>
      </div>
    </a>
'''
def main(apply_):
    s = open(F, encoding="utf-8").read()
    if f'href="{SLUG}" class="guide-card"' in s:
        print("field guide: Date Night Vol. 2 card already present"); return
    i = s.index('<a href="/drops/date-night-after-36" class="guide-card">')
    j = s.index('</a>', i) + len('</a>\n')
    s = s[:j] + CARD + s[j:]
    assert s.count(SLUG) == 1
    print("field guide: added Date Night Vol. 2 after Vol. 1" + ("" if apply_ else " (dry run)"))
    if apply_: open(F, "w", encoding="utf-8").write(s)
if __name__ == "__main__":
    main("--apply" in sys.argv)
