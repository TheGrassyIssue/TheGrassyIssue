#!/usr/bin/env python3
"""add-southside-press.py — add the Southside Golf Co citation to /about.
21 September 2026.

Lenny: "let's also add this mention to the about page —
https://southsidegolfco.com/press"

WHAT THEIR PAGE ACTUALLY SAYS. Southside Golf Co's press page ("Southside Golf
Co in the News") lists four outlets. The Grassy Issue is the first entry, above
Plugged In Golf, Hoodline and What Now Austin, dated July 2026, with the quote
and description transcribed verbatim below.

THE LINK THEY PUBLISHED IS A 301 ON OUR SIDE.
They link /drops/7-indoor-simulators-for-austins-gross-rainy-days, which no
longer exists as a file — it redirects to /drops/austin-indoor-golf-simulators
(the post was rebuilt and reslugged). Their link still resolves, so the
citation stands, but the internal link in this entry points at the LIVE slug.
Pointing our own About page at a URL we 301 would be a self-inflicted hop.
Checked against vercel.json and the filesystem, not assumed.

The quoted line is Southside's own wording about the feature, attributed to
Southside rather than to a person — the same treatment the DEAS MAG entry
gives a publication. Nothing is paraphrased into quotation marks.

Appended after the existing DEAS MAG item, inside the same <ul class="press-list">.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "about.html"
THEIRS = "https://southsidegolfco.com/press"
OURS = "/drops/austin-indoor-golf-simulators"
THEIR_LINK = "/drops/7-indoor-simulators-for-austins-gross-rainy-days"

ITEM = f'''      <li class="press-item">
        <div class="press-outlet">SOUTHSIDE GOLF CO &middot; July 2026</div>
        <blockquote class="press-quote">&ldquo;The Grassy Issue featured Southside
          Golf Co as one of Austin&rsquo;s top indoor golf simulator destinations,
          highlighting our premium TrackMan experience and South Austin
          location.&rdquo;</blockquote>
        <div class="press-meta">Listed first on
          <a href="{THEIRS}" target="_blank" rel="noopener">Southside Golf Co in the
          News</a>, ahead of Plugged In Golf, Hoodline and What Now Austin. The
          feature is our
          <a href="{OURS}">Austin indoor golf simulator guide</a>.</div>
      </li>
'''


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")

    # ---- the citation must still resolve on our side ----
    live = ROOT / (OURS.lstrip("/") + ".html")
    if not live.is_file():
        sys.exit(f"! {OURS} is not a page on disk — do not link it from /about")
    stale = ROOT / (THEIR_LINK.lstrip("/") + ".html")
    note = ("their link 301s to ours" if not stale.is_file()
            else "their link still resolves directly")

    if THEIRS in h:
        print("  Southside entry already on the page")
        if apply_:
            return check(h)
        return

    m = re.search(r'(<ul class="press-list">.*?)(\s*</ul>)', h, re.S)
    if not m:
        sys.exit("! the press list was not found on about.html")
    if apply_:
        PAGE.write_text(h[:m.end(1)] + "\n" + ITEM + h[m.end(1):], encoding="utf-8")
    print(f"  Southside Golf Co entry appended to the press list ({note})")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    check(PAGE.read_text(encoding="utf-8"))


def check(h):
    """Verify the FINISHED page, not the string that went in."""
    bad = []
    items = re.findall(r'<li class="press-item">', h)
    if len(items) < 2:
        bad.append(f"{len(items)} press item(s) — the append did not land")
    if h.count(THEIRS) != 1:
        bad.append(f"the Southside link appears {h.count(THEIRS)} times")
    if THEIR_LINK in h:
        bad.append("/about links the retired sims slug instead of the live one")
    if OURS not in h:
        bad.append("the live sims post is not linked")
    # the entry must sit inside the list, not after it
    lst = re.search(r'<ul class="press-list">(.*?)</ul>', h, re.S)
    if not lst or THEIRS not in lst.group(1):
        bad.append("the entry is outside <ul class=\"press-list\">")
    if h.count("<ul class=\"press-list\">") != h.count("</ul>"):
        bad.append("unbalanced list tags")
    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"  verified: {len(items)} press items, entry inside the list, "
          f"internal link points at the live slug")


if __name__ == "__main__":
    main("--apply" in sys.argv)
