#!/usr/bin/env python3
"""apply-home-snippet.py — make Google describe the homepage with the tagline. 7 Oct 2026.

Lenny: "the google preview for TGI itself is garbage" — Google was quoting the
Texas Joe Black Cup card from the homepage Events strip instead of the tagline.
Google picks its own snippet from page text when it likes that better than the
meta description, so every homepage block other than the hero is marked
data-nosnippet: the feed, Austin Events, the Vibe Board, the about strip and the
footer. That leaves the tagline H1 and the meta description as the only text it
can quote. Nothing changes for readers. Also adds og:site_name and a WebSite
alternateName so Google settles on "The Grassy Issue" as the site name instead of
the bare domain.

Idempotent; run by Deploy TGI.command after paginate-feed. Dry run by default.
"""
import os, re, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

def main(apply_):
    s = open(P, encoding="utf-8").read(); o = s
    for cls in ("feed", "events", "vibe-board", "about-strip"):
        s = re.sub(r'<section class="%s"(?![^>]*data-nosnippet)' % cls, '<section class="%s" data-nosnippet' % cls, s, count=1)
    s = re.sub(r'<footer(?![^>]*data-nosnippet)([^>]*)>', r'<footer data-nosnippet\1>', s)
    if 'og:site_name' not in s:
        s = s.replace('<meta property="og:title"', '<meta property="og:site_name" content="The Grassy Issue" />\n<meta property="og:title"', 1)
    if '"alternateName"' not in s:
        s = s.replace('"@type": "WebSite",\n  "name": "The Grassy Issue",',
                      '"@type": "WebSite",\n  "name": "The Grassy Issue",\n  "alternateName": ["TGI", "Grassy Issue"],', 1)
    print(f"apply-home-snippet: {'updated' if s != o else 'unchanged'}"
          f"{'' if apply_ or s == o else ' (dry run — pass --apply)'}")
    if apply_ and s != o:
        open(P, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    main("--apply" in sys.argv)
