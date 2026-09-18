#!/usr/bin/env python3
"""
expand-faqs.py — every FAQ on the site opens on load.
18 September 2026.

WHY
---
Lenny, first about the Brand to Know pages and then about everything else:
"automatically expand all the FAQ sections so we're not clicking to expand."

btk-template.py already does this for the 36 pages it builds, at build time. The
rest of the site — roundups, guides, course deep-dives, the six Brand to Know
pages with no products that the template cannot touch — still shipped collapsed.
This is the sitewide pass.

WHAT IT DOES, AND WHAT IT LEAVES ALONE
--------------------------------------
Adds `open` to any <details> that lacks it. <details open> shows the answer on
load and KEEPS the disclosure triangle working, so a reader can still collapse
one. It also puts the answers in the rendered text for anything reading the page
without running the click.

It does not touch <details> written inside <script>, <style> or JSON-LD: those
are code and data, not markup, and rewriting them would corrupt the payload.
Nothing else on the page is altered — this is the narrowest possible edit.

USAGE
    python3 expand-faqs.py            # dry run, lists what would change
    python3 expand-faqs.py --apply
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SKIP = ("research/", "mockups/", "node_modules", ".pre-template.", "backups",
        "drafts/")

# <details> that is not already open. The negative lookahead has to allow for
# other attributes before `open` (class="faq-q" comes first on most pages), so
# it scans the whole tag rather than just the character after the name.
DETAILS = re.compile(r"<details(?![^>]*\bopen\b)([^>]*)>")


def protect(html):
    """Blank out script/style/JSON-LD so a <details> inside them is untouched."""
    spans = [m.span() for m in
             re.finditer(r"<(script|style)\b[^>]*>.*?</\1>", html, re.S)]
    return spans


def expand(html):
    spans = protect(html)

    def inside(i):
        return any(a <= i < b for a, b in spans)

    out, last, n = [], 0, 0
    for m in DETAILS.finditer(html):
        if inside(m.start()):
            continue
        out.append(html[last:m.start()])
        out.append(f"<details open{m.group(1)}>")
        last = m.end()
        n += 1
    out.append(html[last:])
    return "".join(out), n


if __name__ == "__main__":
    apply_ = "--apply" in sys.argv
    files = changed = total = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = str(p.relative_to(ROOT))
        if any(x in rel for x in SKIP):
            continue
        try:
            html = p.read_text(encoding="utf-8")
        except OSError as e:                      # locked or not a regular file
            print(f"  -- unreadable, skipped: {rel} ({e.strerror})")
            continue
        files += 1
        new, n = expand(html)
        if not n:
            continue
        changed += 1
        total += n
        print(f"  {rel:<64} +{n}")
        if apply_:
            p.write_text(new, encoding="utf-8")
    print(f"\n  {files} file(s) scanned, {changed} changed, {total} FAQ(s) opened "
          + ("" if apply_ else "— dry run, pass --apply to write"))
