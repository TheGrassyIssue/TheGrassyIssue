#!/usr/bin/env python3
"""add-feral-press.py — add Feral Golf's write-up of our ferrules guide to the /about Press section. 2 Oct 2026.

Lenny: "another backlink" (feralgolfshop.com/blogs/news/feral-leads-the-grassy-issues-guide-to-custom-ferrules,
published 2 Oct 2026). It quotes our line "Feral is for people who want their irons to start a conversation."
and links the guide twice. Inserted directly after the Forbes item. Idempotent. Dry run by default.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "about.html"
THEIRS = "https://www.feralgolfshop.com/blogs/news/feral-leads-the-grassy-issues-guide-to-custom-ferrules"
OURS = "/drops/golf-ferrules-guide"
ITEM = f'''      <li class="press-item">
        <div class="press-outlet">FERAL GOLF CO. &middot; October 2026</div>
        <blockquote class="press-quote">&ldquo;Feral is for people who want their irons to
          start a conversation.&rdquo;</blockquote>
        <div class="press-meta">Quoted in
          <a href="{THEIRS}" target="_blank" rel="noopener">Feral Leads The Grassy Issue&rsquo;s
          Guide to Custom Ferrules</a>, on Feral&rsquo;s own blog, 2 October 2026. The line is from
          our <a href="{OURS}">guide to custom ferrules</a>.</div>
      </li>
'''
def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    if THEIRS in h:
        print("  already present"); return
    if not (ROOT / (OURS.lstrip("/") + ".html")).is_file(): sys.exit("! guide missing")
    i = h.index("forbes.com/sites/break80")
    j = h.index("</li>\n", i) + len("</li>\n")
    h = h[:j] + ITEM + h[j:]
    print("  Feral added after Forbes")
    if apply_: PAGE.write_text(h, encoding="utf-8")
    else: print("  dry run — pass --apply")
if __name__ == "__main__":
    main("--apply" in sys.argv)
