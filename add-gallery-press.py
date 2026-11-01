#!/usr/bin/env python3
"""add-gallery-press.py — add Gallery Streetwear's Malbon x Grateful Dead explainer to the /about Press section. 1 Nov 2026.

Lenny: "let's add this page to the press section on the about page" (gallerystreetwear.ca Gallery Journal, Oct 30 2026).
It cites The Grassy Issue for the Long Vacation release date and description and links our Malbon/Gumtree/Mogshade drops post.
Inserted at the top of the list (newest). Idempotent. Dry run by default.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "about.html"
THEIRS = "https://gallerystreetwear.ca/blogs/gallery-journal/malbon-x-grateful-dead-explained-canada"
OURS = "/drops/new-golf-drops-malbon-gumtree-mogshade"
ITEM = f'''      <li class="press-item">
        <div class="press-outlet">GALLERY STREETWEAR &middot; October 2026</div>
        <blockquote class="press-quote">&ldquo;The Long Vacation chapter released on October 23, 2026, according to
          The Grassy Issue.&rdquo;</blockquote>
        <div class="press-meta">Cited and linked twice in
          <a href="{THEIRS}" target="_blank" rel="noopener">Malbon x Grateful Dead Explained: The 60th
          Anniversary Golf Collab</a>, on the Kelowna shop&rsquo;s Gallery Journal, October 30, 2026. The
          details are from our <a href="{OURS}">Malbon, Gumtree and Mogshade drops post</a>.</div>
      </li>
'''
def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    if THEIRS in h:
        print("  already present"); return
    if not (ROOT / (OURS.lstrip("/") + ".html")).is_file(): sys.exit("! post missing")
    i = h.index('<ul class="press-list">\n') + len('<ul class="press-list">\n')
    h = h[:i] + ITEM + h[i:]
    print("  Gallery Streetwear added at top")
    if apply_: PAGE.write_text(h, encoding="utf-8")
    else: print("  dry run — pass --apply")
if __name__ == "__main__":
    main("--apply" in sys.argv)
