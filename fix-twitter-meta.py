#!/usr/bin/env python3
"""Make twitter:title / twitter:description agree with og:title / og:description.

THE BUG, found 2026-09-15 by fetching the live Off Course Vol 2 page and reading
its meta tags back:

    meta-og:title      Off Course, Vol. 2 — Golf Brands Doing Non-Golf Things
    meta-twitter:title Students Golf Summer 2026 — Summer School Is in Session

Eleven live posts were sharing on X under the wrong post's headline.

ROOT CAUSE. Every build-*.py starts by copying the <head> of an existing model
page, then rewrites description, og:title, og:description, og:url and og:image.
None of them ever rewrote twitter:title or twitter:description. So whatever
those said on the model page rode along, and because model pages were
themselves copied from earlier model pages, the whole recent chain traces back
to students-golf-summer-2026.html.

This is invisible in the built HTML unless you go looking — verify-post.py did
not check it, and the page renders perfectly. It only shows up when something
actually reads the card, which is why fetching the live URL caught it.

THE FIX IS TWO-PART:
  1. this script, which repairs what already shipped
  2. the og->twitter mirror added to build-off-course-vol2.py, so new builds
     from that script cannot reintroduce it

Any FUTURE build script copied from an older model must do the same. If you are
writing one, copy the `_mirror_twitter` block, not just the og rewrites.

WHAT IT CHANGES. twitter:title becomes og:title with the " — The Grassy Issue"
site suffix stripped (that suffix belongs in <title>, not on a share card), and
twitter:description becomes og:description verbatim. Pages already in agreement
are left untouched. Entity-encoding differences (&mdash; vs —) are normalised
for the comparison but the og form is what gets written.
"""
import re, sys, glob, html

SUFFIX = " — The Grassy Issue"
apply_ = "--apply" in sys.argv

TARGETS = sorted(set(
    glob.glob("*.html") + glob.glob("drops/*.html") + glob.glob("brands/*.html")
    + glob.glob("brands/tag/*.html") + glob.glob("brands/attr/*.html")
    + glob.glob("guides/*.html") + glob.glob("events/*.html")
    + glob.glob("field-guide/*.html")
))


def get(h, key, attr):
    m = re.search(rf'<meta {attr}="{re.escape(key)}" content="([^"]*)"', h)
    return m.group(1) if m else None


def setmeta(h, key, attr, val):
    return re.sub(rf'(<meta {attr}="{re.escape(key)}" content=")[^"]*(")',
                  lambda m: m.group(1) + val.replace("\\", "\\\\") + m.group(2), h, count=1)


def norm(s):
    """Compare on decoded text so &mdash; and — are the same thing."""
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def strip_suffix(og):
    """og:title sometimes carries the site suffix and sometimes doesn't, in
    either literal or entity form. Strip it however it is written."""
    d = norm(og)
    return d[:-len(SUFFIX)].strip() if d.endswith(SUFFIX) else d


# A page's twitter tag is only PROVABLY leaked when it is character-for-character
# another page's og tag. Anything looser overreaches: several pages carry a
# deliberately different, on-topic twitter description (Hancock leads with
# "1899, nine holes, par 35, $20 to walk it" where og leads with prose), and a
# "these two strings differ" rule would flatten that bespoke copy into the og
# text. Only exact cross-page matches get rewritten.
OG_TITLES, OG_DESCS = {}, {}
for _p in TARGETS:
    if _p.startswith("_tmp_"):
        continue
    _h = open(_p, encoding="utf-8").read()
    _t, _d = get(_h, "og:title", "property"), get(_h, "og:description", "property")
    if _t:
        OG_TITLES.setdefault(norm(_t), set()).add(_p)
        OG_TITLES.setdefault(norm(_t).replace(SUFFIX, "").strip(), set()).add(_p)
    if _d:
        OG_DESCS.setdefault(norm(_d), set()).add(_p)


def leaked_from(val, page, table):
    """Return the page this value was copied from, if it belongs to another."""
    owners = table.get(norm(val), set()) - {page}
    return sorted(owners)[0] if owners else None


changed, leaks, skipped = [], [], 0
for p in TARGETS:
    if p.startswith("_tmp_"):
        continue
    h = open(p, encoding="utf-8").read()
    ogt = get(h, "og:title", "property")
    ogd = get(h, "og:description", "property")
    twt = get(h, "twitter:title", "name")
    twd = get(h, "twitter:description", "name")
    if not (ogt and twt):
        skipped += 1
        continue

    want_t = strip_suffix(ogt)
    new = h
    hits = []
    src_t = leaked_from(twt, p, OG_TITLES)
    if src_t and norm(twt) != norm(want_t):
        new = setmeta(new, "twitter:title", "name", want_t)
        hits.append(("title", norm(twt)[:58], want_t[:58], src_t))
    # The leaked DESCRIPTION is the source page's twitter:description, not its
    # og:description, so it matches nothing in OG_DESCS and the cross-page test
    # misses it. But a page whose TITLE is proven leaked had its whole share
    # block copied — so once src_t is established, sync the description too.
    src_d = leaked_from(twd, p, OG_DESCS) if twd else None
    if (src_d or src_t) and ogd and twd and norm(twd) != norm(ogd):
        new = setmeta(new, "twitter:description", "name", norm(ogd))
        hits.append(("desc", norm(twd)[:58], norm(ogd)[:58], src_d or src_t))

    if new != h:
        changed.append((p, hits))
        leaks.append(p)
        if apply_:
            open(p, "w", encoding="utf-8").write(new)

print(f"scanned {len(TARGETS)} pages ({skipped} had no twitter tags)")
print(f"{len(changed)} page(s) {'updated' if apply_ else 'would change'}, "
      f"{len(leaks)} of them carrying ANOTHER POST'S headline\n")
for p, hits in changed:
    print(f"  {p}")
    for k, old, new, src in hits:
        print(f"     {k}: {old!r}\n        -> {new!r}\n        (leaked from {src})")
if not apply_:
    print("\nDRY RUN — pass --apply")
