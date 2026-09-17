#!/usr/bin/env python3
"""Add the directory-description block to /brands — 17 September 2026.

Lenny's copy, verbatim, both sentences:

  A continuously updated directory of independent and emerging golf brands from
  around the world, researched and curated by The Grassy Issue.
  Browse golf apparel, equipment, bags, accessories and lifestyle brands by
  location, category, materials and style.

PLACEMENT. Directly under the hero and above "Browse by vibe", so it is the
first thing after the headline and the first prose a crawler meets. It sits
inside #bx so it inherits the Brand Index type scale rather than the post
stylesheet.

WHY NOT IN THE HERO. The hero already carries a one-line lede. Dropping these
two sentences in beside it would say the same thing twice in the same viewport
— see the note printed at the end of this run about that overlap. The hero line
is left alone here because rewriting Lenny's existing headline copy was not what
he asked for.

MARKUP. Uses .sec/.wrap, which already exist in the page's own stylesheet, plus
one new .bx-intro rule installed into the existing <style> block — a class with
no CSS rule renders unstyled full-width, which is the failure mode verify-post.py
catches on post pages and which nothing catches here.

NO H2. This is a description of the page, not a section of it, so it takes the
mono eyebrow treatment rather than a heading — adding a second h2-level heading
above "Browse by vibe" would put a hollow node in the outline.

IDEMPOTENT: marker-fenced (BX-INTRO) and replaced rather than appended.
"""
import re, os, sys

apply_ = "--apply" in sys.argv
P = "brands/index.html"
S, E = "<!--BX-INTRO-->", "<!--/BX-INTRO-->"

COPY_1 = ("A continuously updated directory of independent and emerging golf brands from around the "
          "world, researched and curated by The Grassy Issue.")
COPY_2 = ("Browse golf apparel, equipment, bags, accessories and lifestyle brands by location, "
          "category, materials and style.")

CSS = (".bx-intro{border-top:1px solid var(--bx-ink);padding-top:18px}"
       ".bx-intro .eyebrow{margin-bottom:14px}"
       ".bx-intro p{font-size:clamp(17px,1.5vw,22px);line-height:1.5;max-width:60ch;"
       "color:var(--bx-ink);margin:0 0 12px}"
       ".bx-intro p + p{font-size:clamp(15px,1.2vw,18px);color:var(--bx-ink60);margin:0}")

BLOCK = (f'{S}\n<section class="sec" id="about-the-index"><div class="wrap">\n'
         f'  <div class="bx-intro">\n'
         f'    <div class="eyebrow">ABOUT THE INDEX</div>\n'
         f'    <p>{COPY_1}</p>\n'
         f'    <p>{COPY_2}</p>\n'
         f'  </div>\n'
         f'</div></section>\n{E}\n')

t = open(P, encoding="utf-8").read()
before = len(t)

# ------------------------------------------------------------- idempotency
t = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", t, flags=re.S)

# ----------------------------------------------------------------- insert
anchor = t.find('<section class="sec" id="vibes">')
if anchor == -1:
    raise SystemExit("could not find the 'Browse by vibe' section to insert above")
t = t[:anchor] + BLOCK + t[anchor:]

# -------------------------------------------------------------------- CSS
if ".bx-intro{" not in t:
    s = t.rfind("</style>")
    if s == -1:
        raise SystemExit("no <style> block to install the .bx-intro rule into")
    t = t[:s] + CSS + t[s:]

# ----------------------------------------------------------------- guards
problems = []
if t.count(S) != 1 or t.count(E) != 1:
    problems.append("markers doubled — not idempotent")
if t.count("<div") != t.count("</div>"):
    problems.append("unbalanced divs")
if t.count("<section") != t.count("</section>"):
    problems.append("unbalanced sections")
if t.count("<h1") != 1:
    problems.append(f"{t.count('<h1')} h1 tags")
for cls in ("bx-intro", "eyebrow", "sec", "wrap"):
    if cls + "{" not in t and "." + cls + "{" not in t:
        problems.append(f".{cls} has no CSS rule — it will render unstyled")
for c in (COPY_1, COPY_2):
    if c not in t:
        problems.append("Lenny's copy did not land verbatim")
if re.search(r"\bworth\b", COPY_1 + COPY_2, re.I):
    problems.append("banned word 'worth'")
if t.find(S) > t.find('<section class="sec" id="vibes">'):
    problems.append("the block landed below 'Browse by vibe'")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("added" if apply_ else "DRY RUN") + f" — the directory description on /brands  (+{len(t)-before:,} bytes)")
print("  · sits directly above 'Browse by vibe', inside #bx")
print("  · .bx-intro CSS installed into the page's own <style> block")
print("\n  NOTE — overlap to decide on: the hero still reads")
print("    \"Independent golf brands, makers and oddities from Texas to Tokyo.")
print("     Researched and selected by The Grassy Issue.\"")
print("  which now says much the same as the first new sentence, one screen apart.")
print("  Left as-is deliberately; say the word and the hero line can go or change.")
if not apply_:
    print("\npass --apply to write")
