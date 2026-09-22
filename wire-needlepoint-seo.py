#!/usr/bin/env python3
"""wire-needlepoint-seo.py — internal links into the needlepoint report.
22 September 2026.

A new post ships with no inbound links. The homepage card is the only way in,
and it rotates off the top of the feed within a week or two. After that the page
is reachable from the sitemap and nothing else, which is the condition that keeps
good pages from ever ranking. Two mechanisms fix it, and this script does both.

JOB A — THE "More from TGI" CATALOGUE HAS BEEN FROZEN SINCE 18 SEPTEMBER.
  research/more-catalogue.json holds 196 entries while drops/ holds 204 pages.
  fix-more-and-related.py rotates four links onto every post in the site from
  that catalogue, so those 8 pages receive ZERO inbound links from the rotation
  — the needlepoint report, the bag report, the Hat & Towel Edit, the Pants
  Edit, Wild Spring Dunes, Fella, Vuori, Local Rule and AXXA. The newest work on
  the site is the least linked, which is exactly backwards. This rebuilds the
  catalogue from what is actually on disk so it cannot silently freeze again.

  ELIGIBILITY IS THE SAME TEST fix-more-and-related.py DOCUMENTED: a post needs
  a title and a local hero image. A More card with a missing image renders as a
  broken box, so the image is checked on disk rather than trusted from the
  thumbs file.

JOB B — TWO CONTEXTUAL LINKS, PLACED WHERE THE SUBJECT ALREADY CAME UP.
  A rotation link is a weak signal: it sits under a "More from TGI" heading with
  three unrelated posts and generic surroundings. A link inside a sentence about
  needlepoint belts is the strong version, and both of these already had the
  sentence:
    · brand-to-know-bluegrass-fairway names "the occasional needlepoint belt"
      in its opening paragraph and carries a Custom Needlepoint Belt card.
    · accessories-on-and-off-the-course is built around "the interesting group
      is the middle" — objects that work on a course and off it, which is the
      needlepoint belt's entire argument and Lenny's own framing of the post.

  THESE EDIT THE PUBLISHED HTML, NOT THE BUILDERS. build-bgf.py and
  build-accessories.py would each re-fetch a live catalogue if re-run, so
  touching them risks churning prices on two settled pages to place a link. The
  cost of the choice is stated rather than hidden: if either post is rebuilt,
  re-run this script. The links are idempotent and anchored on an exact phrase,
  so a second run is a no-op and a failed match is an error rather than a
  silent miss.

Idempotent. Dry run by default.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DROPS = ROOT / "drops"
CAT = ROOT / "research/more-catalogue.json"
SLUG = "/drops/the-needlepoint-belt-report"

# (page, exact phrase that must appear once, the phrase with the link in it)
LINKS = [
    ("brand-to-know-bluegrass-fairway",
     "and the occasional needlepoint belt",
     f'and the occasional <a href="{SLUG}">needlepoint belt</a>'),
    ("accessories-on-and-off-the-course",
     "The interesting group is the middle.",
     "The interesting group is the middle "
     f'&mdash; the <a href="{SLUG}">needlepoint belt</a> is the purest example.'),
]


def catalogue(apply_):
    """Rebuild from disk. Returns (added, dropped, total).

    PRUNING IS NOT HOUSEKEEPING, IT IS THE OTHER HALF OF THE JOB. The catalogue
    carried /drops/hats-carousel — the old Hats & Towels Edit, replaced by
    /drops/the-hat-and-towel-edit and deleted from disk, the sitemap and the
    search index, but never from here. It had been harmless only because the
    rotation over 196 entries never happened to select it. Adding nine entries
    moved every page's stride and it landed on eight posts at once, which is how
    a stale row that had sat quietly for days became eight 404s in one run.
    fix-more-and-related.py's own dead-link check refused the write and is the
    reason this was caught rather than shipped.
    """
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    thumbs = json.loads((ROOT / "data/post-thumbs.json").read_text(encoding="utf-8"))
    dropped = [u for u in list(cat)
               if not (ROOT / (u.lstrip("/") + ".html")).is_file()]
    for u in dropped:
        print(f"    - {u} (no page on disk)")
        del cat[u]
    added = []
    for f in sorted(DROPS.glob("*.html")):
        u = "/drops/" + f.stem
        if u in cat:
            continue
        h = f.read_text(encoding="utf-8", errors="ignore")
        t = re.search(r"<h1>(.*?)</h1>", h, re.S)
        img = thumbs.get(u, {}).get("img")
        if not t or not img:
            print(f"    skip {u} — {'no h1' if not t else 'no thumb'}")
            continue
        if not (ROOT / img.lstrip("/")).is_file():
            print(f"    skip {u} — thumb {img} not on disk")
            continue
        tag = re.search(r'<span class="card-tag[^"]*">\[([^\]]+)\]', h)
        cat[u] = {"img": img,
                  "name": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip(),
                  "tag": tag.group(1) if tag else "Drops &amp; Brands"}
        added.append(u)
    for u in added:
        print(f"    + {u}")
    if apply_ and (added or dropped):
        CAT.write_text(json.dumps(cat, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return added, dropped, len(cat)


def contextual(apply_):
    done = []
    for stem, phrase, linked in LINKS:
        p = DROPS / f"{stem}.html"
        h = p.read_text(encoding="utf-8")
        if linked in h:
            done.append(f"{stem}: already linked"); continue
        n = h.count(phrase)
        if n != 1:
            sys.exit(f"! {stem}: anchor phrase appears {n} times, expected exactly 1 — "
                     f"the copy has changed and the link would land wrong")
        if apply_:
            p.write_text(h.replace(phrase, linked, 1), encoding="utf-8")
        done.append(f"{stem}: linked on {phrase[:38]!r}")
    return done


def run(args, label):
    r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"! {label} failed:\n{r.stdout[-900:]}{r.stderr[-900:]}")
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
    print(f"    {label}: {tail[0].strip() if tail else 'ok'}")


def main(apply_):
    print("  post thumbs (the catalogue needs this post's entry to exist):")
    if apply_:
        run(["gen-post-thumbs.py", "--apply"], "gen-post-thumbs")

    print("\n  More rotation catalogue:")
    added, dropped, total = catalogue(apply_)
    print(f"    {len(added)} added, {len(dropped)} pruned, {total} entries")

    print("\n  contextual links:")
    for d in contextual(apply_):
        print(f"    {d}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  re-rotating More blocks across the site:")
    run(["fix-more-and-related.py", "--apply"], "fix-more-and-related")

    # ---- VERIFY ON THE FINISHED PAGES ----
    bad = []
    inbound = [f.stem for f in DROPS.glob("*.html")
               if f.stem != "the-needlepoint-belt-report"
               and SLUG + '"' in f.read_text(encoding="utf-8", errors="ignore")]
    if len(inbound) < 3:
        bad.append(f"only {len(inbound)} pages link to the post")
    for stem, _, linked in LINKS:
        h = (DROPS / f"{stem}.html").read_text(encoding="utf-8")
        if linked not in h:
            bad.append(f"{stem}: contextual link not on the finished page")
        if h.count(f'href="{SLUG}"') > 2:          # 1 contextual + at most 1 rotation
            bad.append(f"{stem}: {h.count(chr(34))} duplicate links to the post")
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    if SLUG not in cat:
        bad.append("post still absent from the More catalogue")
    for u, e in cat.items():
        if not (ROOT / e["img"].lstrip("/")).is_file():
            bad.append(f"catalogue entry {u} points at a missing image")
        if not (ROOT / (u.lstrip("/") + ".html")).is_file():
            bad.append(f"catalogue entry {u} has no page on disk")
    # a page must never recommend itself
    for f in DROPS.glob("*.html"):
        h = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'<div class="more".*?</div>\s*</div>\s*</div>', h, re.S)
        if m and f'href="/drops/{f.stem}"' in m.group(0):
            bad.append(f"{f.stem} recommends itself")

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: {len(inbound)} pages now link to the report "
          f"({len(LINKS)} in body copy), catalogue at {len(cat)} entries, no self-links")


if __name__ == "__main__":
    main("--apply" in sys.argv)
