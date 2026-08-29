#!/usr/bin/env python3
"""
fix-fieldnote-cards.py — clean the bottom of the Field Notes feed cards.

Lenny, 2026-08-28: "we do need to fix the bottom on the field notes post cards,
it should just be a link to view the full post/choices/story etc."

WHAT WAS THERE
--------------
All 29 Field Notes cards are on the LEGACY card design, so each one ended with a
stack of clutter under the copy:
    <div class="gear-dots">          carousel dots
    <div class="gear-counter">       "1 / 4"
    <div class="card-source">        "15 spots · $$–$$$$ · Austin, TX"
    <span class="card-votes">        fake vote + comment counts, permanently 0
    <a class="card-readmore" style="...80 chars of inline CSS...">
Some also carried a <div class="card-meta"> byline/date row, and in at least one
card that div was left unclosed with the readmore link nested inside it.

WHAT IT IS NOW
--------------
    <a href="SLUG" class="card-link">See the full post &#8594;</a>
and nothing else - the same .card-link the current (non-legacy) cards use.

The card body is REBUILT from its parts (title, text, link) rather than having
the unwanted nodes deleted. Deleting would have inherited the malformed card-meta
nesting; rebuilding guarantees well-formed output.

THE FIVE CARDS THIS MUST NOT TOUCH
----------------------------------
29 cards carry data-type="field", but five are not posts - they are the
interstitial vignette cards ("The Turn", "Solo twilight at Hancock, a Tuesday.",
"Eighteen cars in the Lions lot before 7 a.m."). They are marked
style="cursor:default;" and have no destination, so giving them a "See the full
post" link would send readers nowhere. They are skipped. That leaves 24.

Roy Kizer is the opposite case: a real post that had NO bottom link at all. It
gains one.

TWO TRAPS CHECKED BEFORE WRITING
--------------------------------
* Removing the dots is safe. initGearCarousels() null-guards both dotsContainer
  and counter (`if (dotsContainer)`, `if (counter)`), so their absence throws
  nothing - verified in the page's own JS, not assumed.
* BUT "The Lottery Round" has a .gear-carousel with dots and NO gear-arrow
  buttons, so the dots were its only navigation. It gets arrows here, otherwise
  this fix would silently strand a 4-slide carousel on slide 1 - the same bug
  Lenny caught in the J.Lindeberg and Bird Edit cards.

card-meta (the "The Grassy Issue · 25 Aug 2026" row) is dropped too. It sat at
the top on 9 cards and the bottom on 11, and the current card design has no
card-meta at all, so keeping it would leave the 24 cards disagreeing with each
other AND with the rest of the feed. Say the word if the date should come back.
"""
import re, sys, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent
LABEL = "See the full post &#8594;"


def match_div(s, i):
    """Return index just past the </div> that closes the <div at i."""
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0:
            return i + m.end()
    return -1


def fix(path, apply_=False):
    s = path.read_text(encoding="utf-8")
    opens = [m.start() for m in re.finditer(r'<div class="card"', s)]
    bounds = opens + [len(s)]
    edits = []          # (start, end, replacement)
    skipped, arrowed = [], []

    for i, a in enumerate(opens):
        seg = s[a:bounds[i + 1]]
        head = seg[:200]
        if 'data-type="field"' not in head:
            continue
        # vignette cards: no destination, leave completely alone
        if 'cursor:default' in head:
            t = re.search(r'class="card-title"[^>]*>(.*?)</div>', seg, re.S)
            skipped.append(re.sub(r'<[^>]+>', '', t.group(1)).strip()[:46] if t else '?')
            continue

        bstart = seg.find('<div class="card-body"')
        if bstart == -1:
            continue
        bend = match_div(seg, bstart)
        if bend == -1:
            print(f"  !! unbalanced card-body, skipped card #{i}")
            continue
        body = seg[bstart:bend]

        # Three markup variants exist in the feed: <div class="card-title">,
        # <h2 class="card-title"> and <p class="card-text">. Match the tag rather
        # than assuming div - the h2/p cards are real posts and were silently
        # skipped on the first pass. The original tag is preserved, because
        # rewriting h2 -> div would change the page's heading outline.
        title = re.search(r'<(div|h2|h3)\s+class="card-title".*?</\1>', body, re.S)
        text = re.search(r'<(div|p)\s+class="card-text"[^>]*>.*?</\1>', body, re.S)
        href = re.search(r'class="card-title"[^>]*>\s*<a href="([^"]+)"', body)
        if not (title and href):
            print(f"  !! no title/href, skipped card #{i}")
            continue

        parts = ['<div class="card-body">', '      ' + title.group(0)]
        if text:
            parts.append('      ' + text.group(0))
        parts.append(f'      <a href="{href.group(1)}" class="card-link">{LABEL}</a>')
        parts.append('    </div>')
        newbody = "\n      ".join(parts[:1]) + "\n" + "\n".join(parts[1:])

        # The Lottery Round: carousel whose only nav was the dots we are removing.
        newseg = seg[:bstart] + newbody + seg[bend:]
        if 'gear-carousel' in newseg and 'gear-arrow' not in newseg:
            newseg = newseg.replace(
                '</div>\n      </div>', '</div>\n'
                '        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>\n'
                '        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>\n'
                '      </div>', 1)
            arrowed.append(href.group(1))

        edits.append((a, bounds[i + 1], newseg))

    for a, b, new in reversed(edits):        # reverse so offsets stay valid
        s = s[:a] + new + s[b:]

    print(f"{path.name}: rebuilt {len(edits)} field-note cards")
    print(f"  arrows added to: {arrowed if arrowed else 'none needed'}")
    print(f"  left alone ({len(skipped)} vignette cards, no destination):")
    for t in skipped:
        print(f"      · {t}")
    if apply_:
        shutil.copy2(path, path.with_suffix('.html.bak'))
        path.write_text(s, encoding="utf-8")
        print("  written (backup at index.html.bak)")
    return s


if __name__ == "__main__":
    fix(ROOT / "index.html", "--apply" in sys.argv)
    if "--apply" not in sys.argv:
        print("\n(dry run - pass --apply to write)")
