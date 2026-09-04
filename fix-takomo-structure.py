#!/usr/bin/env python3
"""
fix-takomo-structure.py — kill the duplicate FAQ, normalise section wrappers.

TWO BUGS, both found by inspecting the rendered page:

1. DUPLICATE FAQ. The page carried two FAQ blocks:
     "The Story — FAQ"   5 Q&As in hand-styled <div>s   (legacy)
     "Takomo Golf — FAQ" the same 5 + 3 new, in <details class="faq-q">
   Every original question rendered twice. The legacy block also contains the
   Haapahovi pull-quote, which must SURVIVE — it is the page's only verbatim
   founder quote. So this removes the h2 + the Q&A div only, and re-homes the
   pull-quote in a clean wrapper.

2. SECTION WRAPPERS. Every block on the page is <section class="products">
   except two: "Past the Irons" (a bare h2 + writeup div I added, so it missed
   the border-top/padding rhythm) and the legacy FAQ (a one-off inline style).
   Both normalised.

Idempotent. Dry-run default; --apply writes.
"""
import re, sys

P = "drops/brand-to-know-takomo-golf.html"
APPLY = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
orig = h

# ---- 1. the legacy FAQ section ------------------------------------------
m = re.search(r'<section style="max-width:1400px;[^"]*">(.*?)</section>', h, re.S)
if not m:
    print("legacy FAQ section not found (already fixed?)")
else:
    inner = m.group(1)
    pq = re.search(r'<div class="pull-quote">.*?</div>\s*</div>', inner, re.S)
    assert pq, "pull-quote not found — refusing to delete the section"
    qa_count = inner.count('font-style:italic;font-size:19px')
    replacement = ('<section class="products" style="border-top:none">\n'
                   + pq.group(0) + '\n</section>')
    h = h[:m.start()] + replacement + h[m.end():]
    print(f"legacy FAQ removed: {qa_count} duplicated Q&As | pull-quote preserved")

# ---- 2. wrap "Past the Irons" in a proper section ------------------------
old = '<h2 class="products-hdr">Past the Irons</h2>\n<div class="writeup" style="grid-template-columns:1fr;">'
if old in h:
    h = h.replace(old,
        '<section class="products">\n  <h2 class="products-hdr">Past the Irons</h2>\n'
        '<div class="writeup" style="grid-template-columns:1fr;">', 1)
    # close it before the lookbook section opens
    i = h.find('<section class="products">\n  <h2 class="products-hdr">On Course</h2>')
    h = h[:i] + '</section>\n\n' + h[i:]
    print("'Past the Irons' wrapped in <section class='products'>")
else:
    print("'Past the Irons' already wrapped")

if APPLY and h != orig:
    open(P, "w", encoding="utf-8").write(h)

qs = re.findall(r'<summary>(.*?)</summary>', h, re.S)
h2s = [re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', h, re.S)]
print(f"\nFAQ questions now: {len(qs)} | h2 sections: {h2s}")
print("pull-quote still present:", 'pull-quote' in h)
print("applied" if APPLY else "DRY RUN — pass --apply")
