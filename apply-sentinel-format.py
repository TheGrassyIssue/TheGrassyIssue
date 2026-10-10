#!/usr/bin/env python3
"""Sentinel Golf Brand to Know formatting fixes (Oct 9, 2026). Idempotent; copy untouched.
- Pull quote in the house format: centered, green, ruled top and bottom, no stray "C" glyph.
- Product grids centre their last row (5 Carry, 8 Grail Closet) via data-sg="flex" so verify-post's grid regex still matches."""
import os, re, sys
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drops/brand-to-know-sentinel-golf.html")
CSS = ('<style id="tgi-sg-format">'
 '.pull-quote{margin-top:24px;margin-bottom:24px}'
 '.pull-quote-inner{max-width:900px;margin:0 auto;text-align:center;color:var(--grass);border-top:.5px solid rgba(20,20,20,.15);border-bottom:.5px solid rgba(20,20,20,.15);padding:32px 0}'
 '.pull-quote-inner:before{display:none!important}'
 '.pull-quote-attr{margin-left:auto;margin-right:auto;border-top:0}'
 '.products-grid[data-sg=flex]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
 '.products-grid[data-sg=flex]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
 '@media(max-width:1024px){.products-grid[data-sg=flex]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
 '@media(max-width:480px){.products-grid[data-sg=flex]>.product-card{flex-basis:100%}}'
 '</style>')
def main(apply_):
    s = open(F, encoding="utf-8").read(); o = s
    s = s.replace('<div class="products-grid">', '<div class="products-grid" data-sg="flex">')
    s = re.sub(r'<style id="tgi-sg-format">.*?</style>\n?', '', s, flags=re.S).replace("</head>", CSS + "\n</head>", 1)
    assert s.count('data-sg="flex"') == 4
    print(f"apply-sentinel-format: {'updated' if s != o else 'unchanged'}")
    if apply_ and s != o: open(F, "w", encoding="utf-8").write(s)
if __name__ == "__main__": main("--apply" in sys.argv)
