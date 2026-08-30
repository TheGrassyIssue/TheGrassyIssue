#!/usr/bin/env python3
"""
fix-js-fontquote.py — repair the font substitution that killed sitewide search.

Lenny, 2026-08-30: "the search isnt working"

THE BUG
-------
`apply-editors-note.py` swaps the old serif for the new one everywhere:

    "font-family:Fraunces,Georgia,serif"  ->  "font-family:'Editors Note Text',Georgia,serif"

That is correct inside CSS and inside a double-quoted HTML style attribute. It is
FATAL inside a single-quoted JavaScript string, which is exactly where the search
overlay builds its result rows:

    +'<span style="display:block;font-family:'Editors Note Text',Georgia,serif;...'
                                            ^ terminates the JS string literal

The parser then hits a bare identifier and throws `Unexpected identifier 'Editors'`.
A syntax error aborts the ENTIRE <script> block, so everything defined in it — the
search handler, and on the homepage the carousel helpers too — never loads. The box
still renders, so the page looks fine; typing into it just does nothing.

185 pages carried it. Search has been dead site-wide.

WHY NOTHING CAUGHT IT
---------------------
verify-post.py checks structure and voice-lint checks prose. Neither executes the
page. The only way to catch this class of bug is to LOAD the page in a browser and
read the console — which is now worth doing after any sitewide substitution.

THE FIX
-------
Inside <script> blocks only, escape the quotes so they survive the string literal:

    font-family:\\'Editors Note Text\\',Georgia,serif

Idempotent — an already-escaped occurrence is skipped. Writes a size+sha inventory
to research/ before touching anything, per the house rule.
"""
import os, re, glob, json, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# the exact broken token: an UNescaped 'Editors Note Text' sitting inside a
# single-quoted JS string. The negative lookbehind keeps this idempotent.
BAD = re.compile(r"(?<!\\)'Editors Note Text'(?!\s*[,;]?\s*$)")


def fix_scripts(s):
    """Escape the font quotes, but ONLY inside <script> blocks."""
    out, last, n = [], 0, 0
    for m in re.finditer(r"(<script\b[^>]*>)(.*?)(</script>)", s, re.S):
        js = m.group(2)
        # only touch a script that actually builds HTML in single-quoted strings
        if "'Editors Note Text'" in js:
            fixed, k = BAD.subn(r"\\'Editors Note Text\\'", js)
            n += k
            out.append(s[last:m.start()] + m.group(1) + fixed + m.group(3))
            last = m.end()
    out.append(s[last:])
    return "".join(out), n


def main(apply_=False):
    paths = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if "/drafts/" not in p.replace(os.sep, "/")]
    inv, changed, total = {}, 0, 0
    for p in paths:
        s = open(p, encoding="utf-8", errors="replace").read()
        new, n = fix_scripts(s)
        if n:
            changed += 1
            total += n
            if apply_:
                b = s.encode()
                inv[os.path.relpath(p, ROOT)] = {"size": len(b),
                                                 "sha1": hashlib.sha1(b).hexdigest()}
                open(p, "w", encoding="utf-8").write(new)
    if apply_ and inv:
        os.makedirs(os.path.join(ROOT, "research"), exist_ok=True)
        json.dump(inv, open(os.path.join(ROOT, "research", "jsfont-inventory.json"), "w"),
                  indent=1)
    print(f"{'fixed' if apply_ else 'would fix'} {total} occurrence(s) across {changed} page(s)")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
