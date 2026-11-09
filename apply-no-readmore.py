#!/usr/bin/env python3
"""apply-no-readmore.py — remove the "See the Full Post" link from every homepage feed card. 9 November 2026.
Lenny: "remove the 'see the full post' from all homepage boxes". The card title (and carousel slides) already link
to the post. Runs on index.html and feed/page-*.html; idempotent, and runs every deploy after paginate-feed.py so a
wire-*-home.py script that still emits the link cannot bring it back. Dry run by default.
Safety: a card left with no title link would be left untouched and reported.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
LINK = re.compile(r'[ \t]*<a\s[^>]*href="([^"]+)"[^>]*>\s*See the full post\s*(?:&rarr;|&#8594;|→)?\s*</a>[ \t]*\n?', re.I)
CARD = re.compile(r'<div class="card"[ >].*?(?=<div class="card"[ >]|<!-- /TGI-|\Z)', re.S)
apply_ = "--apply" in sys.argv
total = kept = 0
for p in [os.path.join(ROOT, "index.html")] + sorted(f for f in glob.glob(os.path.join(ROOT, "feed/page-*.html")) if " " not in os.path.basename(f)):
    h = open(p, encoding="utf-8").read()
    def fix_card(m):
        global total, kept
        c = m.group(0); out = c
        for lm in list(LINK.finditer(c)):
            href = lm.group(1)
            rest = out.replace(lm.group(0), "", 1)
            # removable if the card still links to the post — or links to any post at all from its title
            # (found: the Manors x Gentleman Jack card's button pointed at /drops/manors-ss26, a different post)
            if f'href="{href}"' in rest or re.search(r'class="card-title"><a href="/', rest):
                out = rest; total += 1
            else:
                kept += 1; print(f"  kept (only link): {os.path.basename(p)} {href}")
        return out
    new = CARD.sub(fix_card, h)
    if new != h and apply_:
        open(p, "w", encoding="utf-8").write(new)
print(f"  removed {total} 'See the Full Post' links, kept {kept}" + ("" if apply_ else " — dry run, pass --apply"))
