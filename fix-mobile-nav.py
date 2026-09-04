#!/usr/bin/env python3
"""
fix-mobile-nav.py — stop the header overflowing horizontally on phones.

THE BUG (measured 2026-09-03, not assumed)
------------------------------------------
`.nav-inner` is a nowrap flex row with gap:32px and 20px side padding. At 390px
its contents need 444px: wordmark 236 + gap 32 + toggle + gap 32 + search 104
+ padding 40. Every page on the site therefore scrolled sideways on a phone
(scrollWidth 424 vs viewport 390). It was never the photo row or any one page —
`#tgi-sbox` and its input were the elements sticking out, on all 265+ pages.

THE FIX
-------
  <=820px  tighten gap to 12 and padding to 16, drop the wordmark to 17px, and
           let the search box flex-shrink instead of holding a fixed 104px.
           Nav stays one line, 57px tall.
  <=360px  one line genuinely cannot hold masthead + toggle + search without
           truncating the wordmark to "THE GRASSY ISS...", so the nav wraps and
           search takes its own full-width row (87px tall). Only fires on very
           old handsets; every current phone gets the single-line version.

Idempotent via the marker below. Dry-run by default; --apply writes.
RE-RUN after apply-header.py or build-brands.py, both of which rewrite nav CSS.
"""
import sys, glob, re

MARK = "/*TGI-NAV-MOBILE-V1*/"
CSS = MARK + """
@media(max-width:820px){
  /* The 89 brand pages never hid .nav-links on mobile (their only query tweaks
     gap), so the links stayed visible and overflowed. Normalise every nav here
     rather than depending on each page's own rules. */
  .nav-inner{gap:12px;padding-left:16px;padding-right:16px;justify-content:space-between}
  .nav-links{display:none!important}
  .nav-toggle{display:flex!important}
  .nav-wordmark{font-size:17px;letter-spacing:.06em;flex:0 0 auto}
  #tgi-sbox{flex:1 1 60px;min-width:0}
  #tgi-search-input{width:100%;min-width:0}
  #tgi-search-results{width:min(300px,calc(100vw - 32px))}
}
@media(max-width:360px){
  .nav-inner{flex-wrap:wrap;gap:10px 12px}
  .nav-wordmark{font-size:19px;letter-spacing:.07em;flex:1 1 auto}
  .nav-toggle{flex:0 0 auto;order:2}
  #tgi-sbox{flex:1 0 100%;order:3}
  #tgi-search-results{width:100%;right:auto;left:0}
}
"""

APPLY = "--apply" in sys.argv
REVERT = "--revert" in sys.argv
pages = sorted(set(glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")))

done = skipped = nonav = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    if ".nav-inner" not in s:
        nonav += 1; continue
    if REVERT:
        if MARK not in s: skipped += 1; continue
        s = re.sub(re.escape(MARK) + r".*?\n\}\n", "", s, flags=re.S)
        done += 1
    else:
        if MARK in s: skipped += 1; continue
        i = s.rfind("</style>")
        if i < 0: skipped += 1; continue
        s = s[:i] + CSS + s[i:]
        done += 1
    if APPLY:
        open(p, "w", encoding="utf-8").write(s)

verb = "reverted" if REVERT else "patched"
print(f"{verb}: {done} | already done: {skipped} | no nav: {nonav} | scanned: {len(pages)}")
print("DRY RUN — pass --apply to write" if not APPLY else "applied")
