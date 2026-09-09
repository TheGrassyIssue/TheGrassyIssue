#!/usr/bin/env python3
"""Make sitemap.xml agree with the brand coverage pages actually on disk.

WHY
---
Found 2026-09-09 while checking the Après push: four `/brands/<slug>` coverage
pages were live and linked from /brands, but absent from sitemap.xml —
apc-golf, cph-golf, public-drip and apres-golf. Only the last was mine; the
other three had been missing for days.

The cause is structural. `build-brands.py` writes a coverage page for every
entry in brands.json, but the per-post wire scripts each add only their own
`/drops/...` URL to the sitemap. Adding the `/brands/...` row was left to
whoever wrote that post's wire script, so it got done sometimes and not others.
Nothing checked. A page that no sitemap lists and that only /brands links to is
exactly the orphan pattern that put seven drop pages in indexing limbo.

WHAT THIS DOES
Adds a sitemap row for any brands/<slug>.html that has none. Never removes
rows, never touches a lastmod that already exists — an existing entry means
someone set that date deliberately. lastmod for new rows comes from the brand's
`added` date in brands.json, falling back to today.

Run it after build-brands.py, alongside the nav chain. Idempotent; safe to
re-run. Dry run by default.
"""
import json, glob, os, re, sys, datetime

TODAY = datetime.date.today().isoformat()
ROW = ('<url><loc>{loc}</loc><lastmod>{lm}</lastmod>'
       '<changefreq>monthly</changefreq><priority>0.8</priority></url>\n')


def main(apply_=False):
    sm = open("sitemap.xml", encoding="utf-8").read()
    added = {b["slug"]: b.get("added", TODAY)
             for b in json.load(open("data/brands.json"))}

    missing = []
    for f in sorted(glob.glob("brands/*.html")):
        slug = os.path.basename(f)[:-5]
        if slug == "index":
            continue                       # /brands/ is listed separately
        loc = f"https://thegrassyissue.com/brands/{slug}"
        if f"{loc}<" not in sm:
            missing.append((slug, loc, added.get(slug, TODAY)))

    # tag and attribute hubs are generated too, and deserve the same check
    for pat, kind in (("brands/tag/*.html", "tag"), ("brands/attr/*.html", "attr")):
        for f in sorted(glob.glob(pat)):
            slug = os.path.basename(f)[:-5]
            loc = f"https://thegrassyissue.com/brands/{kind}/{slug}"
            if f"{loc}<" not in sm:
                missing.append((f"{kind}/{slug}", loc, TODAY))

    for slug, loc, lm in missing:
        print(f"  + {slug:34} {lm}")
    print(f"\n{'added' if apply_ else 'would add'} {len(missing)} sitemap row(s)")

    if missing and apply_:
        rows = "".join(ROW.format(loc=l, lm=d) for _, l, d in missing)
        sm = sm.replace("</urlset>", rows + "</urlset>")
        open("sitemap.xml", "w", encoding="utf-8").write(sm)
        # cheap integrity check: one <loc> per <url>, and the doc still closes
        n_url, n_loc = sm.count("<url>"), sm.count("<loc>")
        if n_url != n_loc or not sm.rstrip().endswith("</urlset>"):
            raise SystemExit(f"sitemap looks malformed after write: "
                             f"{n_url} <url> vs {n_loc} <loc>")
        print(f"sitemap.xml now lists {n_url} URLs")
    elif not apply_:
        print("(dry run — pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
