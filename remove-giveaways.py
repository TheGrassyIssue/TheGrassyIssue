#!/usr/bin/env python3
"""Remove the Live Giveaways block from the homepage.

LENNY'S CALL, 9/17/26: it does not add anything to the ethos. The section linked
out to four sweepstakes run by other companies — Reynolds Lake Oconee, Topgolf,
a Callaway gift-card draw, a Corona promotion — none of which we had reported
on, chosen, or had any relationship with. It was the one part of the homepage
pointing readers at somebody else's marketing.

WHAT GOES:
  · the <!-- GIVEAWAYS --> ... </section> block in index.html (4 cards)
  · every .giveaway* CSS rule, including the responsive overrides
  · the same orphaned CSS in field-guide/index.html and brands/index.html, which
    inherited the homepage's <style> block but never had the markup

WHAT WAS CHECKED AND IS NOT AFFECTED: no JavaScript referenced the section, no
nav or in-page anchor linked to it, and it appeared in neither sitemap.xml nor
search-index.json. Nothing 404s as a result of this and no URL disappears — the
block was homepage-only markup pointing at external sites.

The Austin Events section directly below it is untouched.
"""
import re, sys, os

apply_ = "--apply" in sys.argv
PAGES = ["index.html", "field-guide/index.html", "brands/index.html"]
report = []

for p in PAGES:
    if not os.path.exists(p):
        raise SystemExit(f"{p} not found")
    t = open(p, encoding="utf-8").read()
    before = len(t)
    cards = t.count('class="giveaway-card"')

    # ---- 1. the markup ----------------------------------------------------
    s = t.find("<!-- GIVEAWAYS -->")
    if s != -1:
        e = t.find("</section>", s)
        if e == -1:
            raise SystemExit(f"{p}: found the GIVEAWAYS comment but no closing </section>")
        e += len("</section>")
        # take the trailing blank line with it so the file does not gain a gap
        while e < len(t) and t[e] == "\n":
            e += 1
        block = t[s:e]
        if "giveaway-card" not in block:
            raise SystemExit(f"{p}: the block found does not contain giveaway cards — "
                             f"refusing to delete something I have not identified")
        if "<!-- EVENTS -->" in block or "gear-carousel" in block:
            raise SystemExit(f"{p}: the block overruns into another section — aborting")
        t = t[:s] + t[e:]

    # ---- 2. the CSS -------------------------------------------------------
    # every rule whose selector list mentions .giveaway / .giveaways, plus the
    # section comment. Brace-counted rather than regex-greedy so a rule with a
    # nested block cannot swallow the rest of the stylesheet.
    out, i, removed = [], 0, 0
    while i < len(t):
        m = re.compile(r"[^{}\n;]*\.giveaways?\b[^{}]*\{").search(t, i)
        if not m:
            out.append(t[i:]); break
        # walk back to the start of the selector
        sel = t.rfind("\n", 0, m.start()) + 1
        out.append(t[i:sel])
        depth, j = 0, m.end() - 1
        while j < len(t):
            if t[j] == "{": depth += 1
            elif t[j] == "}":
                depth -= 1
                if depth == 0: j += 1; break
            j += 1
        while j < len(t) and t[j] in " \n": j += 1
        i = j; removed += 1
    t = "".join(out)
    t = t.replace("  /* GIVEAWAYS */\n", "").replace("/* GIVEAWAYS */\n", "")

    left = t.count("giveaway")
    report.append((p, cards, removed, left, before - len(t)))
    if apply_:
        open(p, "w", encoding="utf-8").write(t)

# ---------------------------------------------------------------- guards
if apply_:
    for p, *_ in report:
        t = open(p, encoding="utf-8").read()
        if re.search(r"giveaway", t, re.I):
            raise SystemExit(f"{p}: 'giveaway' still present after removal")
        # the section that followed it must have survived intact
        if p == "index.html":
            if "<!-- EVENTS -->" not in t or t.count('class="events"') != 1:
                raise SystemExit("index.html: the Austin Events section was damaged")
            if t.count("<style") != t.count("</style>"):
                raise SystemExit("index.html: unbalanced <style> tags after CSS removal")
        if t.count("{") != t.count("}"):
            raise SystemExit(f"{p}: unbalanced braces after CSS removal")

print(("removed" if apply_ else "DRY RUN") + " — Live Giveaways")
for p, cards, rules, left, delta in report:
    print(f"  {p:26} cards:{cards}  css-rules:{rules:2}  bytes:-{delta:,}  'giveaway' left:{left}")
if not apply_:
    print("\npass --apply to write")
