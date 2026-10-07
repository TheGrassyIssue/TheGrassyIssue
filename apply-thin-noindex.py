#!/usr/bin/env python3
"""apply-thin-noindex.py — keep thin brand pages out of Google. 7 Oct 2026.

Lenny picked "Noindex 0–1 post pages" after the site audit flagged 132 thin
/brands/ pages. A brand page that links to zero or one TGI post is a stub, and
search engines read a few dozen of them as filler that drags the whole section.

WHAT IT DOES, every run (idempotent):
  * /brands/<slug>.html with 0 or 1 posts in data/brand-mentions.json gets
    <meta name="robots" content="noindex,follow"> (marked TGI-THIN). "follow"
    keeps the links on it counting, so the posts it points at lose nothing.
  * Any page that has since reached 2+ posts has the tag removed, so a brand
    re-enters the index on its own the deploy after its second post.
  * Noindexed pages are dropped from sitemap.xml (a sitemap should only list
    pages we want indexed); pages that graduate are put back.

The pages stay on the site and in the Brand Index; readers see no difference.
Pages with a written About section are exempt.
Never touches /brands/index.html, tag/attr pages or the Best 25 page.
Runs in Deploy TGI.command, after the brand pages are built. Dry run by default.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TAG = '<meta name="robots" content="noindex,follow" /><!--TGI-THIN-->'
TAG_RE = re.compile(r'\s*<meta name="robots" content="noindex,follow" /><!--TGI-THIN-->')
SKIP = {"index", "best-independent-golf-brands"}
SITE = "https://thegrassyissue.com"


def main(apply_):
    counts = {k: len(v) for k, v in json.load(open(os.path.join(ROOT, "data/brand-mentions.json"))).items()}
    thin, full, changed = [], [], 0
    for p in sorted(glob.glob(os.path.join(ROOT, "brands", "*.html"))):
        slug = os.path.basename(p)[:-5]
        if slug in SKIP or re.search(r" \d+$", slug):
            continue
        s = open(p, encoding="utf-8").read()
        if re.search(r'<meta name="robots"[^>]*noindex', TAG_RE.sub("", s)):
            continue  # already noindexed for some other reason; leave it alone
        # A page with a written About section (data/brand-about.json) is not thin, whatever its post count.
        is_thin = counts.get(slug, 0) <= 1 and 'class="bp-about"' not in s
        (thin if is_thin else full).append(slug)
        new = TAG_RE.sub("", s)
        if is_thin:
            new = new.replace("</head>", "  " + TAG + "\n</head>", 1)
        if new != s:
            changed += 1
            if apply_:
                open(p, "w", encoding="utf-8").write(new)

    # sitemap: drop thin brand URLs, restore graduated ones
    sm_path = os.path.join(ROOT, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    before = sm
    for slug in thin:
        sm = re.sub(r"\s*<url>\s*<loc>%s/brands/%s</loc>.*?</url>" % (re.escape(SITE), re.escape(slug)), "", sm, flags=re.S)
    present = set(re.findall(r"<loc>%s/brands/([^<]+)</loc>" % re.escape(SITE), sm))
    add = [s for s in full if s not in present]
    if add:
        rows = "".join("\n  <url>\n    <loc>%s/brands/%s</loc>\n  </url>" % (SITE, s) for s in add)
        sm = sm.replace("</urlset>", rows + "\n</urlset>", 1)
    if sm != before and apply_:
        open(sm_path, "w", encoding="utf-8").write(sm)

    print(f"apply-thin-noindex: {len(thin)} thin brand page(s) noindexed, {len(full)} indexed; "
          f"{changed} page(s) {'updated' if apply_ else 'would change'}; "
          f"sitemap {'updated' if sm != before else 'unchanged'}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
