#!/usr/bin/env python3
"""remove-newsletter-popup.py — take the scroll-triggered newsletter popup off
the homepage. 21 September 2026.

Lenny: "let's remove the newsletter pop up, it's not getting any traction."

WHAT IS BEING REMOVED, AND WHAT IS NOT.

There are TWO email captures on this site and they are easy to confuse:

  1. THE POPUP (this is the one going)  — id="nl-overlay" / "nl-popup", around
     line 16378. A modal that fires once per session at 50% scroll depth, posts
     to a Google Apps Script endpoint through a hidden iframe, and remembers it
     fired via sessionStorage key `tgi_nl_seen`.

  2. THE FOOTER FORM (this one STAYS) — id="mailingForm" / "mailingSuccess",
     around line 14369, sitting in the footer next to the wordmark. It posts to
     formsubmit.co, not to the Apps Script.

They are two thousand lines apart and share no code. A careless grep for
"mail" or "email" or "signup" would have taken both, and Lenny only asked for
the popup. So the guards below assert the footer form SURVIVES — the check
that matters here is not "did the popup go" but "did anything else go with it".

The popup block is self-contained: every reference to closeNL, submitNL,
nl-overlay, nl-popup and tgi_nl_seen lives inside it. Verified by grep across
every .html and .js on the site before this script was written, which is why
the removal can be a clean cut rather than a hunt.

THE SUBSCRIBER DATA IS NOT TOUCHED. The Apps Script endpoint and the Google
Sheet behind it keep existing; this only stops the site sending to them. The
endpoint is recorded here so it is not lost with the markup:

    https://script.google.com/macros/s/AKfycbwY5Q8KyPZssb0m1PHiDdBzEZhWERESK1W8XFduRsWvNFSRhwwxDtjxzo8tElys9H8d/exec

NOT TOUCHED: drafts/cleaner/index.cleaner-applied.html also contains the
popup. It is a scratch artifact — not in sitemap.xml, not linked from any
page on the site — so it is left alone rather than edited for tidiness.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

OPEN_MARK = "<!-- ==================== NEWSLETTER POPUP ==================== -->"

# Tokens that must be GONE afterwards.
POPUP_TOKENS = ["nl-overlay", "nl-popup", "nl-close", "nl-form", "nl-email",
                "nl-thanks", "nl-hidden-frame", "closeNL", "submitNL",
                "tgi_nl_seen", "NEWSLETTER POPUP"]

# Tokens that must SURVIVE. This is the real guard: the footer signup, and the
# two neighbouring script blocks the cut sits between.
KEEP_TOKENS = ["mailingForm", "mailingSuccess", 'class="mailing"',
               "formsubmit.co", "wb-weather", "G-G89M4116SB", "goatcounter"]


def find_block(h):
    """Bound the popup: from its comment marker to the </script> that closes
    its behaviour block. Returns (start, end) or None.

    The end is found by walking forward from the marker through the script
    tags that belong to the popup, rather than by a line number, so the script
    keeps working if the file shifts.
    """
    i = h.find(OPEN_MARK)
    if i < 0:
        return None
    # the popup is: comment, <div id="nl-overlay">...</div>, <script>...</script>
    j = h.find('<script>', i)
    if j < 0:
        sys.exit("! found the popup marker but no <script> after it")
    end = h.find("</script>", j)
    if end < 0:
        sys.exit("! popup script block is unterminated")
    end += len("</script>")
    seg = h[i:end]
    # sanity: the slice must contain the popup and NOT swallow a neighbour
    if "nl-overlay" not in seg or "submitNL" not in seg:
        sys.exit("! the bounded slice does not look like the popup")
    for t in KEEP_TOKENS:
        if t in seg:
            sys.exit(f"! the bounded slice contains {t!r}, which must survive "
                     f"— refusing to cut")
    # swallow one trailing blank line so we don't leave a gap
    while end < len(h) and h[end] == "\n" and h[end:end + 2] == "\n\n":
        end += 1
    return i, end


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")

    if not any(t in h for t in ("nl-overlay", OPEN_MARK)):
        print("  popup already removed — nothing to do")
        return

    found = find_block(h)
    if not found:
        sys.exit("! popup markers present but the block could not be bounded")
    i, end = found
    seg = h[i:end]
    print(f"  popup block found: {len(seg)} bytes, "
          f"lines {h[:i].count(chr(10))+1}–{h[:end].count(chr(10))+1}")
    print(f"  contains: {sum(1 for t in POPUP_TOKENS if t in seg)}/"
          f"{len(POPUP_TOKENS)} popup tokens")

    if h.count(OPEN_MARK) != 1:
        sys.exit(f"! popup marker appears {h.count(OPEN_MARK)} times, expected 1")

    out = h[:i] + h[end:]

    if not apply_:
        print(f"\n  would remove {len(h)-len(out)} bytes")
        print("  dry run — pass --apply")
        return

    INDEX.write_text(out, encoding="utf-8")

    # ---- VERIFY THE FINISHED FILE ON DISK ----
    hh = INDEX.read_text(encoding="utf-8")
    bad = []

    for t in POPUP_TOKENS:
        if t in hh:
            bad.append(f"popup token still present: {t!r}")

    # THE SCOPING GUARD. Removing too much is the failure mode here, not too
    # little, so every survivor is checked by name against the finished file.
    for t in KEEP_TOKENS:
        if t not in hh:
            bad.append(f"REMOVED SOMETHING IT SHOULD NOT HAVE: {t!r} is gone")

    # structural integrity — an unbalanced cut would orphan a tag
    if hh.count("<script") != hh.count("</script>"):
        bad.append(f"script tags unbalanced: {hh.count('<script')} open, "
                   f"{hh.count('</script>')} close")
    if hh.count("<div") != hh.count("</div>"):
        bad.append(f"div tags unbalanced: {hh.count('<div')} open, "
                   f"{hh.count('</div>')} close")
    if not hh.rstrip().endswith("</html>"):
        bad.append("document no longer closes with </html>")

    # the cut should be roughly the block, not the page
    delta = len(h) - len(hh)
    if not (2000 < delta < 8000):
        bad.append(f"removed {delta} bytes — outside the expected range for "
                   f"this block; check what went")

    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  removed {delta} bytes")
    print(f"  verified on disk: popup gone, footer signup intact, "
          f"tags balanced, document closes")


if __name__ == "__main__":
    main("--apply" in sys.argv)
