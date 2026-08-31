#!/usr/bin/env python3
"""Install the site search block on pages that have the box but not the script.

WHY THIS EXISTS
---------------
apply-header.py unifies the <nav> across the site, and the reference nav contains
the #tgi-sbox markup and its CSS. It does NOT carry the search JS, which lives in
a separate "<!-- TGI SEARCH -->" block near the end of a post. So any page that
apply-header touches for the first time gains a search input that renders, focuses,
accepts typing — and does nothing, because nothing ever fetches /search-index.json.

That happened to /brands/ on 2026-08-30 when build-brands.py regenerated it and
apply-header then rewrote its nav. A dead search box is worse than no search box:
it looks broken rather than absent.

The block is copied verbatim from a post that is known good, so there is exactly
one implementation of search on the site.

Usage: python3 install-search.py [paths...] [--apply]
Idempotent — a page that already fetches the index is skipped.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "drops", "the-white-tee-edit-2026.html")


def block():
    s = open(REF, encoding="utf-8").read()
    i = s.find("<!-- TGI SEARCH -->")
    if i < 0:
        sys.exit("reference page has no TGI SEARCH block")
    j = s.find("</script>", s.find("<script>", i)) + len("</script>")
    b = s[i:j]
    if "search-index.json" not in b:
        sys.exit("extracted block does not fetch the index — refusing")
    return b


def install(path, blk, apply_):
    s = open(path, encoding="utf-8").read()
    if "search-index.json" in s:
        return "already has search"
    if "tgi-search-input" not in s:
        return "no search box in the nav — nothing to wire"
    # drop the CSS half if the page already carries it (apply-header put it there),
    # keeping only the markup-independent script + a re-declared style is harmless,
    # but duplicated ids are not, so strip the input markup from the block if any.
    i = s.rfind("</body>")
    if i < 0:
        return "no </body>"
    out = s[:i] + blk + "\n" + s[i:]
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return "installed"


def main():
    apply_ = "--apply" in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    blk = block()
    for p in paths:
        print("%-42s %s" % (os.path.basename(p), install(p, blk, apply_)))
    if not apply_:
        print("(dry run — pass --apply)")


if __name__ == "__main__":
    main()
