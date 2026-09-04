#!/usr/bin/env python3
"""
add-about-link.py — put /about into the nav (and the footer where one exists).

Idempotent: skips any page that already links to /about. Dry-run by default;
pass --apply to write. Mirrors the apply-header.py convention.
"""
import sys, glob, re

APPLY = "--apply" in sys.argv
pages = sorted(set(glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")))

nav_done = foot_done = skipped = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    o = s
    if 'href="/about"' not in s:
        # nav: insert after the Events link inside .nav-links
        m = re.search(r'(<div class="nav-links">.*?</div>)', s, re.S)
        if m and "Events" in m.group(1):
            blk = m.group(1)
            new = re.sub(r'(<a href="[^"]*events/?"[^>]*>Events</a>)',
                         r'\1\n      <a href="/about">About</a>', blk, count=1)
            if new != blk:
                s = s.replace(blk, new, 1); nav_done += 1
    # footer: sit About next to Contact where that footer shape exists
    if s.count('href="/about"') < 2 and 'mailto:L4harrington@gmail.com' in s:
        new = s.replace('<a href="mailto:L4harrington@gmail.com">Contact</a>',
                        '<a href="/about">About</a><a href="mailto:L4harrington@gmail.com">Contact</a>', 1)
        if new != s:
            s = new; foot_done += 1
    if s == o:
        skipped += 1
    elif APPLY:
        open(p, "w", encoding="utf-8").write(s)

print(f"nav updated: {nav_done} | footer updated: {foot_done} | unchanged: {skipped} | scanned: {len(pages)}")
print("DRY RUN — pass --apply to write" if not APPLY else "applied")
