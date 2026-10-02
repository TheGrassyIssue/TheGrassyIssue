#!/usr/bin/env python3
"""add-forbes-press.py — add the Forbes citation to the /about Press section. 2 October 2026.

Lenny: "we just got quoted in Forbes" then "Let's add it to the about us press section".
Tim Corlett, "Quiet Golf Is Bringing Understated Style Back To The Course", Forbes (Break80 contributor
column), 30 Sep 2026, quotes Christion Lennon "said in The Grassy Issue" and links our Quiet Golf Brand to
Know. The quote below is Forbes's sentence, verbatim. Inserted FIRST in the press list (biggest outlet,
newest). Idempotent. Dry run by default.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "about.html"
FORBES = "https://www.forbes.com/sites/break80/2026/09/30/quiet-golf-is-bringing-understated-style-back-to-the-course/"
OURS = "/drops/brand-to-know-quiet-golf"
ITEM = f'''      <li class="press-item">
        <div class="press-outlet">FORBES &middot; September 2026</div>
        <blockquote class="press-quote">&ldquo;Some people go on runs, others go rock
          climbing or mountain biking, but for us, golf is a way to get outside, get
          away from your phone, and have some quiet time for yourself,&rdquo; Christion
          Lennon said in The Grassy Issue.</blockquote>
        <div class="press-meta">Quoted and linked by Tim Corlett in
          <a href="{FORBES}" target="_blank" rel="noopener">Quiet Golf Is Bringing
          Understated Style Back To The Course</a>, Forbes, 30 September 2026. The
          quote is from our <a href="{OURS}">Quiet Golf Brand to Know</a>.</div>
      </li>
'''
def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    if not (ROOT / (OURS.lstrip("/") + ".html")).is_file():
        sys.exit(f"! {OURS} is not on disk")
    if FORBES in h:
        print("  already present"); return
    anchor = '<ul class="press-list">\n'
    assert h.count(anchor) == 1, "press list anchor not unique"
    h = h.replace(anchor, anchor + ITEM, 1)
    print("  Forbes added at the top of the press list")
    if apply_: PAGE.write_text(h, encoding="utf-8")
    else: print("  dry run — pass --apply")
if __name__ == "__main__":
    main("--apply" in sys.argv)
