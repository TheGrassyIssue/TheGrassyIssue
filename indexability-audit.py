#!/usr/bin/env python3
"""indexability-audit.py — can Google index every TGI page? 21 September 2026.

Lenny: "can we check that all TGI pages are indexed on google?"

WHAT THIS CAN AND CANNOT ANSWER. Whether a URL is actually IN Google's index is
a fact only Google holds, and the only reliable readout is Search Console's Page
Indexing report (or the URL Inspection API). A `site:` search is a sampled,
throttled estimate that Google explicitly says not to use for coverage counts.
So this script answers the half that is knowable from here, completely and
deterministically: is every page DISCOVERABLE and ELIGIBLE?

If a page fails anything below, it is either not in the index or at risk of
dropping out, and no amount of waiting fixes it. If a page passes everything
and is still missing from GSC, that is a crawl-budget or quality question, not
a plumbing one — a different problem with a different fix.

THE CHECKS, per published page:
  in_sitemap     listed in sitemap.xml (its only discovery path besides links)
  indexable      no <meta name="robots" content="noindex">
  canonical_self canonical points at itself, not at some other URL
  robots_ok      not blocked by a Disallow rule in robots.txt
  linked         at least one internal <a href> from another published page
  not_redirected not also a 301 source in vercel.json (that would be a loop)

AND THE REVERSE SWEEP, per sitemap entry:
  exists         resolves to a real file on disk
  not_a_redirect the sitemap must never list a URL that 301s away
  no_dupes       no URL listed twice

URL SHAPE. vercel.json sets cleanUrls, so /drops/x.html on disk is served at
/drops/x and that extensionless form is canonical. Every comparison below is
done on the clean form; comparing raw filenames is what would make this whole
audit meaningless.

Read-only. Writes a JSON report and prints the failures.
"""
import json
import pathlib
import re
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://thegrassyissue.com"
SKIP_DIRS = {"drafts", "research", "mockups", "node_modules", ".git"}

# DELIBERATELY OUT OF THE INDEX. These carry noindex,nofollow and are not meant
# to rank: /ig and /instagram-posts are the private Instagram tiling tools,
# /stats is an internal dashboard, /previews/* are build scaffolds. The first
# run flagged all six as "missing from sitemap / no canonical / orphan", which
# is true and entirely intended. Listing them here keeps the report honest —
# they are still checked, but a page that is SUPPOSED to be hidden failing the
# public-page checks is not a finding.
INTENTIONALLY_PRIVATE = {"/ig", "/instagram-posts", "/stats"}
PRIVATE_PREFIXES = ("/previews/",)


def is_private(u):
    return u in INTENTIONALLY_PRIVATE or u.startswith(PRIVATE_PREFIXES)


def clean(rel):
    """Disk path -> the URL Vercel serves, given cleanUrls."""
    u = "/" + rel.as_posix()
    if u.endswith("/index.html"):
        u = u[: -len("index.html")].rstrip("/") or "/"
    elif u.endswith(".html"):
        u = u[: -len(".html")]
    return u


def published():
    for p in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        if ".bak" in p.name:
            continue
        yield p


def main():
    pages = list(published())
    urls = {clean(p.relative_to(ROOT)): p for p in pages}

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm)
    sm_paths = [u.replace(SITE, "") or "/" for u in sm_urls]
    sm_set = set(sm_paths)

    v = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    redirect_src = {r["source"] for r in v.get("redirects", [])}

    rb = (ROOT / "robots.txt").read_text(encoding="utf-8")
    disallow = [l.split(":", 1)[1].strip()
                for l in rb.splitlines() if l.lower().startswith("disallow:")
                and l.split(":", 1)[1].strip()]

    # internal link graph, built from the rendered href values
    inbound = defaultdict(set)
    for u, p in urls.items():
        h = p.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'<a[^>]+href="([^"#?]+)', h):
            if href.startswith("http") or href.startswith("mailto"):
                continue
            t = href.rstrip("/") or "/"
            if t in urls and t != u:
                inbound[t].add(u)

    rows, fail = [], defaultdict(list)
    for u, p in sorted(urls.items()):
        h = p.read_text(encoding="utf-8", errors="ignore")
        noindex = bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
                                 h, re.I))
        cm = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', h, re.I)
        # NO rstrip HERE. The first version normalised the trailing slash away,
        # so /brands declaring canonical=/brands/ — a URL that 301s under
        # trailingSlash:false — passed this check. It surfaced only through the
        # sitemap cross-reference. Compare the exact string.
        can = (cm.group(1) if cm else "").replace(SITE, "") or ("/" if cm else "")
        r = {
            "url": u,
            "in_sitemap": u in sm_set,
            "indexable": not noindex,
            "has_canonical": bool(cm),
            "canonical_self": bool(cm) and can == u,
            "robots_ok": not any(u.startswith(d) for d in disallow),
            "inbound_links": len(inbound[u]),
            "not_redirected": u not in redirect_src,
        }
        rows.append(r)
        if is_private(u):
            # the only failure mode that matters for these is being INDEXABLE
            if r["indexable"]:
                fail["private page is missing its noindex"].append(u)
            if r["in_sitemap"]:
                fail["private page listed in the sitemap"].append(u)
            continue
        if not r["in_sitemap"]:
            fail["missing from sitemap"].append(u)
        if not r["indexable"]:
            fail["noindex tag"].append(u)
        if not r["has_canonical"]:
            fail["no canonical"].append(u)
        elif not r["canonical_self"]:
            fail["canonical points elsewhere"].append(f"{u} -> {can}")
        if not r["robots_ok"]:
            fail["blocked by robots.txt"].append(u)
        if r["inbound_links"] == 0 and u != "/":
            fail["orphan (no internal links in)"].append(u)
        if not r["not_redirected"]:
            fail["page exists AND 301s away"].append(u)

    # reverse sweep
    seen = set()
    for s in sm_paths:
        if s in seen:
            fail["listed twice in sitemap"].append(s)
        seen.add(s)
        if s not in urls:
            fail["in sitemap, no such page"].append(s)
        if s in redirect_src:
            fail["in sitemap but 301s away"].append(s)

    print(f"  {len(pages)} published pages on disk")
    print(f"  {len(sm_paths)} sitemap entries ({len(seen)} unique)")
    print(f"  robots.txt disallows: {disallow or 'nothing'}\n")

    ok = sum(1 for r in rows if all(
        r[k] for k in ("in_sitemap", "indexable", "canonical_self", "robots_ok", "not_redirected"))
        and r["inbound_links"])
    print(f"  {ok} of {len(rows)} pages pass every eligibility check")

    if fail:
        print("\n  ISSUES")
        for k in sorted(fail, key=lambda k: -len(fail[k])):
            print(f"\n  {k} — {len(fail[k])}")
            for x in fail[k][:15]:
                print(f"     {x}")
            if len(fail[k]) > 15:
                print(f"     ... and {len(fail[k]) - 15} more")
    else:
        print("\n  no issues found")

    out = ROOT / "research/indexability.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"rows": rows, "fail": dict(fail)}, indent=1), encoding="utf-8")
    print(f"\n  full report: {out.relative_to(ROOT)}")
    print("\n  NOTE: this proves eligibility, not index membership. Actual "
          "indexed/not-indexed\n  status lives in Search Console's Page Indexing report.")


if __name__ == "__main__":
    main()
