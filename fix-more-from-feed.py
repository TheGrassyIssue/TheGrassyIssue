#!/usr/bin/env python3
"""
fix-more-from-feed.py — spread the "More from the Feed" suggestions evenly.

THE PROBLEM (Lenny, 2026-08-29: "same three keep showing up")
-------------------------------------------------------------
Measured across the 144 drop pages that carry a more-grid:
    Mogshade            24 appearances
    Cloud & Wind        18
    Read The Green      12
    Towel Edit          12
    Sentinel            12
...while **49 posts were never suggested anywhere at all**. Suggestions had been
hand-picked per post over many sessions, and whatever was recent at the time got
stamped in and never revisited. So the feed was quietly funnelling readers into
the same handful of pages and burying a third of the catalogue.

THE FIX
-------
Balanced assignment rather than random choice. Random would still clump - with
144 posts drawing 3 each from ~170, plain sampling leaves some posts unused and
others hit six or seven times. Instead each post picks the LEAST-USED eligible
candidates, so exposure is levelled by construction:

    target = ceil(144 * 3 / eligible)  ->  every post lands within 1 of the mean.

Deterministic: seeded with the post slug, so a rebuild produces the same result
and the diff stays reviewable. Not time-based, not random per run.

CONSTRAINTS ENFORCED
--------------------
* Never links to itself.
* Only links to posts that actually exist on disk AND have a usable image.
* Prefers a different category where possible (a Brand to Know suggests at least
  one non-BTK), so the module reads as a feed rather than a brand list.
* Leaves the 29 posts that have no more-grid alone - adding one is a separate job.

Re-run after publishing, alongside build-ig.py.
"""
import os, re, glob, json, math, random, html, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
DROPS = os.path.join(ROOT, "drops")
N = 3


def slug_of(path):
    return "/drops/" + os.path.basename(path)[:-5]


# The homepage is the single source of truth for a post's category - see the
# three-category rule (Field Notes / Drops & Brands / News). Reading it from the
# post's own drop-meta was wrong: that field's first segment is sometimes a
# SOURCE DOMAIN, which is how a card ended up tagged "themunyconservancy.com".
TYPE_LABEL = {"drop": "Drops &amp; Brands", "field": "Field Notes", "news": "News",
              "guide": "Field Notes", "score": "Field Notes"}

# 131 of 173 posts point og:image at this generic social-share fallback. Using it
# as the card art gave three different suggestions the SAME sunset photo.
GENERIC_OG = "/images/og-image.jpg"


def feed_cards(root):
    """slug -> (category, card image), read off the homepage feed cards.

    The homepage is authoritative for both. 17 posts are legacy JS-rendered
    pages whose images live in a script array, not in static markup - there is
    no hero or product-card <img> to scrape. Their feed card has the art, so
    reading it here keeps them eligible instead of silently dropping them back
    into the never-suggested pile this script exists to empty.
    """
    s = open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace").read()
    out = {}
    for m in re.finditer(r'<div class="card" data-type="([a-z]+)"', s):
        seg = s[m.start():m.start() + 5000]
        h = re.search(r'href="(/drops/[^"#?]+)"', seg)
        if not h:
            continue
        im = re.search(r'<img[^>]+src="(/images/[^"]+)"', seg)
        out.setdefault(h.group(1), (m.group(1), im.group(1) if im else None))
    return out


def meta(path, cards):
    """title, category tag and a usable image - the post's OWN art, not the og fallback."""
    s = open(path, encoding="utf-8", errors="replace").read()
    t = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip() if t else ""

    slug = "/drops/" + os.path.basename(path)[:-5]
    kind, card_img = cards.get(slug, ("drop", None))

    # Order matters: hero first (the post's real lead image), then its first
    # product frame, then the homepage card, and og:image only if it is not the
    # shared fallback.
    img = None
    m = re.search(r'<div class="drop-hero-img">\s*<img[^>]+src="([^"]+)"', s)
    if m:
        img = m.group(1)
    if not img:
        m = re.search(r'<div class="product-card"[^>]*>.*?<img[^>]+src="([^"]+)"', s, re.S)
        img = m.group(1) if m else None
    if not img:
        img = card_img
    if not img:
        og = re.search(r'<meta property="og:image" content="https://thegrassyissue\.com([^"]+)"', s)
        if og and og.group(1) != GENERIC_OG:
            img = og.group(1)

    return title, TYPE_LABEL.get(kind, "Drops &amp; Brands"), img, kind


def main(apply_=False):
    posts = sorted(glob.glob(os.path.join(DROPS, "*.html")))
    cards_meta = feed_cards(ROOT)
    info, has_grid = {}, []
    for p in posts:
        title, tag, img, kind = meta(p, cards_meta)
        if not title:
            continue
        info[slug_of(p)] = dict(path=p, title=title, tag=tag, img=img, kind=kind)
        s = open(p, encoding="utf-8", errors="replace").read()
        if '<div class="more-grid">' in s:
            has_grid.append(slug_of(p))

    # eligible = has a title AND an image on disk (a card with no image looks broken)
    eligible = [u for u, d in info.items()
                if d["img"] and os.path.exists(os.path.join(ROOT, d["img"].lstrip("/")))]
    print(f"posts: {len(info)}   with more-grid: {len(has_grid)}   eligible as suggestions: {len(eligible)}")

    used = collections.Counter()
    target = math.ceil(len(has_grid) * N / max(1, len(eligible)))
    assign = {}
    for slug in sorted(has_grid):
        rnd = random.Random(slug)                    # deterministic per post
        pool = [u for u in eligible if u != slug]
        rnd.shuffle(pool)
        # least-used first; shuffle breaks ties differently for each post
        picks, kinds = [], []
        for _ in range(N):
            # Balance FIRST, variety only as a tiebreak within the same usage
            # count. An earlier version let the kind rule skip a least-used
            # candidate outright, which is what produced the ragged 2..5 spread -
            # variety was quietly buying itself extra imbalance.
            best = min((u for u in pool if u not in picks),
                       key=lambda u: (used[u], kinds.count(info[u]["kind"])))
            picks.append(best); kinds.append(info[best]["kind"])
        for u in picks:
            used[u] += 1
        assign[slug] = picks

    cards = lambda picks: "\n".join(
        f'    <a href="{u}" class="more-card">\n'
        f'      <div class="more-card-img"><img src="{info[u]["img"]}" '
        f'alt="{html.escape(info[u]["title"], quote=True)}" loading="lazy" /></div>\n'
        f'      <div class="more-card-body"><div class="more-card-name">{info[u]["title"]}</div>'
        f'<div class="more-card-tag">{info[u]["tag"]}</div></div>\n    </a>' for u in picks)

    def grid_span(s):
        """Locate the more-grid by DIV DEPTH, not by a lookahead.

        The obvious `<div class="more-grid">.*?</div>\\s*(?=</section>)` silently
        missed 18 pages - the Austin/field-guide posts carry a `.fg-backlink`
        block between the grid and `</section>`, so the lookahead never fired and
        those grids kept their old hand-picked suggestions with no error. Counting
        tags is structural and matches all 162.
        """
        i = s.find('<div class="more-grid">')
        if i < 0:
            return None
        depth, j = 0, i
        tag = re.compile(r"<div\b|</div>")
        while True:
            m = tag.search(s, j)
            if not m:
                return None
            depth += -1 if m.group(0) == "</div>" else 1
            j = m.end()
            if depth == 0:
                return i, j

    changed = 0
    for slug, picks in assign.items():
        p = info[slug]["path"]
        s = open(p, encoding="utf-8").read()
        span = grid_span(s)
        if not span:
            print(f"  !! could not locate grid in {slug}")
            continue
        a, b = span
        new = '<div class="more-grid">\n' + cards(picks) + "\n  </div>"
        out = s[:a] + new + s[b:]
        if out != s:
            changed += 1
            if apply_:
                open(p, "w", encoding="utf-8").write(out)

    dist = collections.Counter(used.values())
    print(f"{'rewrote' if apply_ else 'would rewrite'} {changed} more-grids")
    print(f"  target appearances per post: {target}")
    print(f"  appearance spread: {dict(sorted(dist.items()))}")
    print(f"  max appearances: {max(used.values())}   never used: {len(eligible)-len(used)}")
    if not apply_:
        print("\n(dry run - pass --apply to write)")


if __name__ == "__main__":
    import sys
    main("--apply" in sys.argv)
