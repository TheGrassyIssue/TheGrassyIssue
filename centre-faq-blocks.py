#!/usr/bin/env python3
"""centre-faq-blocks.py — stop the FAQ block pinning to the left edge.
21 September 2026.

Lenny: "A ton of the pages have the 'The Questions' or 'FAQ' section formatted
all the way on the left edge, let's push it over a bit."

THE CAUSE. The rule is `.faq{max-width:820px}` with no horizontal margins. Its
container (.products) is max-width:1400px and centred, so an 820px child inside
a 1216px content area sits hard left with ~430px of dead space to its right.

WHY IT LOOKS WORST ON BRAND TO KNOW PAGES. Those templates centre the section
heading — `.products-hdr` there carries max-width:760px plus auto margins, so
"The Questions" floats at x=534 while the answers below start at x=32. Heading
centred, body pinned left, measured on brand-to-know-huega-house. On the older
roundup pages the heading is a full-width element with text starting at 32, so
it matched the FAQ and the defect was less obvious — but the dead right margin
was there too, which is why Lenny says "a ton of the pages".

THE FIX IS ONE DECLARATION: give .faq the auto side margins the heading already
has. 820px unchanged, so line length and the .faq-q rules are untouched; the
block just centres in its container.

It also repairs an outlier: on late-season-putter-switch the FAQ rendered at
x=0, flush to the viewport with no padding at all, because there it sits
outside a .products wrapper and inherited no gutter. max-width plus auto
margins centres that one too.

The CSS is inlined per page, so this edits every page carrying the rule.
Verified by re-measuring the rendered geometry, not by reading the file back.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OLD = ".faq{max-width:820px}"
NEW = ".faq{max-width:820px;margin-left:auto;margin-right:auto}"


def targets():
    for p in sorted(ROOT.rglob("*.html")):
        if "drafts" in p.parts or "research" in p.parts or "mockups" in p.parts:
            continue
        yield p


def main(apply_):
    hits, already, skipped = [], [], []
    for p in targets():
        t = p.read_text(encoding="utf-8", errors="ignore")
        if NEW in t:
            already.append(p); continue
        if OLD not in t:
            # a page may carry a variant of the rule — report rather than guess
            if re.search(r"\.faq\s*\{", t):
                skipped.append((p, re.search(r"\.faq\s*\{[^}]*\}", t).group(0)))
            continue
        hits.append(p)
        if apply_:
            p.write_text(t.replace(OLD, NEW), encoding="utf-8")

    print(f"  pages patched: {len(hits)}")
    print(f"  already correct: {len(already)}")
    if skipped:
        print(f"  !! {len(skipped)} pages carry a DIFFERENT .faq rule — not touched:")
        for p, rule in skipped[:8]:
            print(f"       {p.relative_to(ROOT)}: {rule[:70]}")
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    bad = []
    for p in hits:
        t = p.read_text(encoding="utf-8")
        if NEW not in t:
            bad.append(f"{p.relative_to(ROOT)} did not take the new rule")
        if OLD in t:
            bad.append(f"{p.relative_to(ROOT)} still carries the old rule")
    if bad:
        sys.exit("! " + "; ".join(bad[:6]))
    print(f"\n  wrote {len(hits)} pages; the rendered check is the real verification")


if __name__ == "__main__":
    main("--apply" in sys.argv)
