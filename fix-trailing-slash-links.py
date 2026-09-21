#!/usr/bin/env python3
"""fix-trailing-slash-links.py — stop 2,456 internal links going through a 301.
21 September 2026.

FOUND WHILE ANSWERING "are all TGI pages indexed?". Fetching the live
/brands/ showed it 301s to /brands (vercel.json sets trailingSlash: false) —
and that the nav on every page links the trailing-slash form:

    /brands/        930 links
    /field-guide/   770 links
    /events/        751 links
    /guides/          5 links
                   ----
                  2,456 links across 373 files

WHY THIS MATTERS. These are the three hub pages the whole site points at. Every
nav link currently spends a redirect hop before arriving, on every page, for
every crawl. Redirected links still pass signals, but Google treats the hop as
a weaker, slower path, and it burns crawl budget site-wide on links that could
resolve directly. /brands is the page we are actively trying to rank for
"independent golf brand directory"; it should be receiving 930 direct internal
links, not 930 redirects.

WHY THE INDEXABILITY AUDIT MISSED IT. Its inbound-link graph does
`href.rstrip("/")` before matching, so a link to /brands/ was counted as a link
to /brands and the hop was normalised out of existence. Same failure as the
canonical check on the same page, for the same reason: the audit compared
tidied-up values instead of the literal thing the browser follows. Both are
fixed.

SCOPE. Only the four paths above, only where the no-slash form is a real page,
only in href attributes. /brands/tag/quiet-luxury and /brands/casualist do not
end in a slash and are not touched. The one stray og:url on field-guide is
corrected too.

PROVE ONE, THEN BATCH: `--one <file>` edits a single file so the result can be
rendered and checked before the sweep. House rule.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://thegrassyissue.com"
SKIP = {"drafts", "research", "mockups", "node_modules", ".git", "previews"}
TARGETS = ["/brands/", "/field-guide/", "/events/", "/guides/"]


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if SKIP & set(p.relative_to(ROOT).parts) or ".bak" in p.name:
            continue
        yield p


def fix(h):
    """Rewrite only href/og:url values, never bare text."""
    n = 0
    for t in TARGETS:
        bare = t.rstrip("/")
        for form in (t, SITE + t):
            want = form[:-1]
            for attr in ('href="', 'content="'):
                before = h
                h = h.replace(f'{attr}{form}"', f'{attr}{want}"')
                n += (len(before) - len(h)) // 1 and before.count(f'{attr}{form}"')
    return h, n


def main(apply_, only):
    todo = [ROOT / only] if only else list(pages())
    if only and not todo[0].is_file():
        sys.exit(f"! no such file: {only}")

    total, touched = 0, []
    for p in todo:
        h = p.read_text(encoding="utf-8")
        h2, _ = fix(h)
        if h2 == h:
            continue
        n = sum(h.count(f'href="{f}"') + h.count(f'content="{f}"')
                for t in TARGETS for f in (t, SITE + t))
        total += n
        touched.append((p, n))
        if apply_:
            p.write_text(h2, encoding="utf-8")

    print(f"  {len(touched)} file(s), {total} link(s) repointed off the redirect")
    for p, n in touched[:8]:
        print(f"     {p.relative_to(ROOT)}  {n}")
    if len(touched) > 8:
        print(f"     ... and {len(touched) - 8} more")
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY: no published page may still link a redirecting URL ----
    left = 0
    for p in pages():
        h = p.read_text(encoding="utf-8")
        for t in TARGETS:
            for f in (t, SITE + t):
                left += h.count(f'href="{f}"') + h.count(f'content="{f}"')
    if left and not only:
        sys.exit(f"! {left} trailing-slash link(s) survive")
    # and the targets must still exist as real pages
    for t in TARGETS:
        d = ROOT / t.strip("/") / "index.html"
        if not d.is_file():
            sys.exit(f"! {t} has no page at {d.relative_to(ROOT)} — do not link it")
    print(f"\n  verified: {left} trailing-slash links remain, all four targets exist")


if __name__ == "__main__":
    a = sys.argv[1:]
    one = a[a.index("--one") + 1] if "--one" in a else None
    main("--apply" in a, one)
