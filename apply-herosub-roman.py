#!/usr/bin/env python3
"""apply-herosub-roman.py — set the Field Guide deck roman, not italic.
22 September 2026.

Lenny: "let's remove the italics from under the title- too hard to read."

Follows apply-title-roman.py (29 Aug, "remove the italics from the post titles"),
which set .drop-header h1 roman and deliberately left .product-name alone. Same
principle here: one selector, on the page that has the problem.

WHY THIS ONE AND NOT THE OTHER. Only two pages define .hero-sub italic:
field-guide/index.html and guides/index.html. They are not the same case.

  field-guide  52 words, four full lines of 22px italic serif. A long italic
               paragraph is the readable-for-a-clause / tiring-for-a-paragraph
               problem, and this deck is a paragraph.
  guides       22 words of short clipped sentences ("Safe for the cautious. Fun
               for the curious. Aggressive for the delusional."). Italic is
               doing work there and never runs long enough to tire.

So guides/index.html is left alone. If Lenny wants it to match, that is a
separate one-line change, not an assumption made on his behalf.

ONLY font-style IS TOUCHED. The serif family, the 22px, the 1.45 line-height and
the 720px measure all stay, so the deck still reads as the same element in the
same design — it is the slant that goes, not the styling.

NOT CHANGED, BUT WORTH KNOWING: the rule also carries opacity: 0.85. Italic at
85% on cream is two readability costs stacked, and removing the slant only fixes
one. Raising the opacity is the obvious follow-up and is deliberately not done
here, because it was not what was asked.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "field-guide/index.html"
SELECTOR = ".hero-sub"


def main(apply_):
    h = TARGET.read_text(encoding="utf-8")

    # Find the rule body for .hero-sub and drop only its font-style declaration.
    m = re.search(r"(\.hero-sub\s*\{)([^}]*)(\})", h)
    if not m:
        sys.exit(f"! no {SELECTOR} rule found in {TARGET.name}")
    before = m.group(2)
    if "italic" not in before:
        print(f"  {SELECTOR} is already roman — nothing to do")
        return
    after = re.sub(r"\s*font-style:\s*italic;?", "", before)
    if after == before:
        sys.exit("! font-style declaration matched the rule but not the pattern")

    def flat(s):
        return re.sub(r"\s+", " ", s).strip()

    print(f"  {SELECTOR} before: {flat(before)}")
    print(f"  {SELECTOR} after : {flat(after)}")

    out = h[:m.start(2)] + after + h[m.end(2):]

    # Guard: the slant must not survive by another route — an inline style on the
    # element, or a later rule re-asserting it, would leave the page unchanged
    # while this script reported success.
    el = re.search(r'<[^>]*class="hero-sub"[^>]*>', out)
    if not el:
        sys.exit("! no element carries class=hero-sub — the rule edit would be invisible")
    if "italic" in el.group(0):
        sys.exit("! the hero-sub element carries an inline italic style; the CSS edit is not enough")
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", out, re.S))
    for mm in re.finditer(r"([^{}]*\.hero-sub[^{}]*)\{([^}]*)\}", css):
        if "italic" in mm.group(2):
            sys.exit(f"! another rule still sets italic: {mm.group(1).strip()}")

    # Everything else about the rule must be intact.
    for keep in ("font-family", "font-size", "line-height", "max-width"):
        if keep not in after:
            sys.exit(f"! {keep} was lost from the rule")

    if not apply_:
        print("\n  dry run — pass --apply")
        return
    TARGET.write_text(out, encoding="utf-8")
    print(f"  wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
