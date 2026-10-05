#!/usr/bin/env python3
"""wire-best25-home.py — a link to Our 25 Best Independent Golf Brands in the homepage hero.

4 Oct 2026. Lenny approved SEO step 3 for "independent golf brands": the 25 Best page had only two pages
linking to it and none from the homepage. This adds one quiet link beside "See the Austin Golf Guide" in the
hero caption, styled the same. Idempotent (marked block). Dry run by default.
"""
import pathlib, re, sys
HOME = pathlib.Path(__file__).resolve().parent / "index.html"
M0, M1 = "<!--TGI-BEST25-HERO-->", "<!--/TGI-BEST25-HERO-->"
LINK = (M0 + '<br/><a href="/brands/best-independent-golf-brands" class="card-readmore" style="display:inline-block;'
        "margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;"
        'border-bottom:1px solid var(--paper);color:var(--paper);padding-bottom:2px;">Our 25 Best Independent Golf Brands →</a>' + M1)
s = HOME.read_text(encoding="utf-8"); s0 = s
s = re.sub(re.escape(M0) + r".*?" + re.escape(M1), "", s, flags=re.S)
anchor = 'padding-bottom:2px;">See the Austin Golf Guide →</a>'
if anchor not in s: sys.exit("! hero Austin Golf Guide link not found")
s = s.replace(anchor, anchor + LINK, 1)
print("  hero link placed" + ("" if "--apply" in sys.argv else " (dry run)"))
if "--apply" in sys.argv and s != s0: HOME.write_text(s, encoding="utf-8"); print("  wrote index.html")
