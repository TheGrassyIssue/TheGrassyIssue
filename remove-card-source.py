#!/usr/bin/env python3
"""remove-card-source.py — drop the grey .card-source line from every homepage card.
21 September 2026.

Lenny: "let's clean up all the homepage cards to be more consistent we shouldn't
have that grey worded section on any card on the entire homepage."

A SECOND CLASS, FOUND THE SAME WAY AS THE FIRST.

Lenny, after the first pass shipped: "some of the older cards are still
displaying that grey text." Older cards carry .card-meta — a byline and date,
"The Grassy Issue | 26 Aug 2026" — which is the same grey mono treatment in the
same slot, under a different class name. 68 cards had one. That is now removed
too, on his explicit call, since a publication date is a real thing to drop and
not something to assume.

Three classes, three passes to find them all: card-source as a div, card-source
as a span, card-meta as a div. The lesson is not "check for spans" — it is that
an element is identified by what it LOOKS like to the reader, and the class name
is an implementation detail that varies by whoever wrote the card that week.

WHAT IT IS. A mono, 55%-opacity line between the carousel counter and the
read-more link, carrying whatever the card's author felt like: a source domain
("merrillgolf.com"), a stat line ("77 markers · 20 brands · 9 categories ·
$6 to $214"), a price-read date, a city, or just "Various". It is on 106 of
216 cards, which is the actual problem — half the feed has a metadata line and
half does not, and no two of them mean the same kind of thing.

ONE CARD IS MALFORMED AND A NAIVE REGEX WOULD BREAK IT.

The Merrill Golf card opens <div class="card-source"> and never closes it, so
its .card-readmore anchor is nested INSIDE the source div:

    <div class="card-source">
      <a ... class="source-link">merrillgolf.com</a> ·
      <a ... class="source-link">@merrillgolf</a>
    <a ... class="card-readmore">See the Full Post →</a>      <-- inside

A `<div class="card-source">.*?</div>` replacement would either stop at the
first </div> (deleting the read-more link on that card) or run on and eat the
rest of the card body. So each block is bounded by walking div depth, and if a
read-more/card-link anchor turns up before the matching close, the cut stops at
that anchor — which removes the unclosed <div> and leaves the link alone. That
case does not just avoid damage, it repairs the balance: one open div goes, no
close goes with it.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

# TWO MARKUP VARIANTS, AND THE FIRST PASS ONLY KNEW ABOUT ONE.
#
# 106 of these are <div class="card-source">. Another 62 are
# <span class="card-source">. The first version matched only the div form,
# reported "106 removed", and its own file-level guard passed — because the
# guard counted the thing it had been taught to look for. The render is what
# disagreed: 61 .card-source elements still in #feed. Hence OPEN_RE, and hence
# the guard below now counts by CSS class rather than by opening tag.
OPEN_RE = re.compile(r'<(div|span) class="(?:card-source|card-meta)"', re.I)
KEEP_ANCHOR = re.compile(r'<a\b[^>]*class="(?:card-readmore|card-link)"', re.I)


def block_end(h, start, tag_name):
    """(end, rescued_html). Walks div depth to the card-source element's real
    closing </div>, then rescues any read-more/card-link anchor found INSIDE it.

    THE BUG THIS FIXES. The first version treated an anchor appearing before the
    close as proof the div was unclosed, and cut at the anchor. It is not proof:
    on the Merrill Golf card the anchor is simply nested inside a card-source
    that closes normally afterwards. Cutting at the anchor removed the opening
    <div> and left its </div> behind, and the div balance went -1 -> -4. Three
    orphan closing tags, reported by the guard as "got worse" — which is the
    only reason it was caught. Unwrap instead: delete the whole element and
    re-emit the rescued anchor in its place.
    """
    depth = 0
    i = start
    tag = re.compile(rf"<{tag_name}\b|</{tag_name}>", re.I)
    while i < len(h):
        m = tag.search(h, i)
        if not m:
            sys.exit("! card-source block never closes")
        if not m.group(0).startswith("</"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end()
                inner = h[start:end]
                a = KEEP_ANCHOR.search(inner)
                if not a:
                    return end, None
                # take the whole <a ...>...</a>, not just its opening tag
                close = inner.find("</a>", a.start())
                if close < 0:
                    sys.exit("! rescued anchor has no closing tag")
                return end, inner[a.start():close + 4]
        i = m.end()
    sys.exit("! ran off the end of the document")


def strip(h):
    out, notes, malformed = [], [], 0
    pos = 0
    n = 0
    while True:
        m = OPEN_RE.search(h, pos)
        if not m:
            out.append(h[pos:])
            break
        start = m.start()
        end, rescued = block_end(h, start, m.group(1).lower())
        out.append(h[pos:start])
        if rescued is not None:
            out.append(rescued)                    # unwrap: keep the link
            malformed += 1
        pos = end
        n += 1
    h2 = "".join(out)
    # the blank line the removal leaves behind between counter and read-more
    h2 = re.sub(r"\n[ \t]*\n([ \t]*<a[^>]*class=\"(?:card-readmore|card-link)\")",
                r"\n\1", h2)
    notes.append(f"{n} .card-source blocks removed")
    if malformed:
        notes.append(f"{malformed} had a read-more link nested inside — unwrapped, "
                     f"link kept as a sibling")
    return h2, notes


def strip_dead_css(h):
    """A rule for a class the page no longer emits is dead CSS — the same defect
    class as .lr-trans surviving a donor copy, just in the other direction."""
    notes = []
    for cls in ("card-source", "source-link", "card-meta"):
        if f'class="{cls}"' in h or f'class="{cls} ' in h:
            continue                                # still used somewhere
        h2 = re.sub(rf"\.{cls}\s*\{{[^}}]*\}}\s*", "", h)
        if h2 != h:
            notes.append(f".{cls} CSS rule removed (no longer emitted)")
            h = h2
    return h, notes


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")

    before_cards = h.count('<div class="card"')
    before_read = len(re.findall(r'class="(?:card-readmore|card-link)"', h))
    before_srcs = len(OPEN_RE.findall(h))
    before_bal = len(re.findall(r"<div\b", h)) - h.count("</div>")

    h2, n1 = strip(h)
    h2, n2 = strip_dead_css(h2)
    for x in n1 + n2:
        print("  " + x)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    INDEX.write_text(h2, encoding="utf-8")

    # ---- VERIFY THE FINISHED FILE ----
    hh = INDEX.read_text(encoding="utf-8")
    bad = []
    left = hh.count('class="card-source"') + hh.count('class="card-meta"')
    if left:
        bad.append(f"{left} card-source elements still on the page")
    if hh.count('<div class="card"') != before_cards:
        bad.append(f"cards went from {before_cards} to {hh.count(chr(60)+'div class=')}")
    after_read = len(re.findall(r'class="(?:card-readmore|card-link)"', hh))
    if after_read != before_read:
        bad.append(f"read-more links went from {before_read} to {after_read}")
    after_bal = len(re.findall(r"<div\b", hh)) - hh.count("</div>")
    if after_bal > before_bal:
        bad.append(f"div balance got worse: {before_bal} -> {after_bal}")
    # nothing else on the page should have lost content
    for must in ("gear-carousel", "card-title", "card-text", "_slideTexts"):
        if must not in hh:
            bad.append(f"{must} disappeared from the page")
    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  verified: {before_srcs} removed, {before_cards} cards intact, "
          f"{after_read} read-more links intact, div balance {before_bal} -> {after_bal}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
