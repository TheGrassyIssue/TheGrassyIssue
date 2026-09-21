#!/usr/bin/env python3
"""wire-casualist-2026.py — propagate the Casualist retitle + new hero across
the site. 21 September 2026.

The post now reads "Casualist — The Australian Brand That Became a British Golf
Label". Nine files still carried the old headline and the coverage-card thumb
still pointed at the previous hero.

GENERATED FILES GET THEIR GENERATOR, NOT AN EDIT.
  brands/casualist.html   <- data/brand-mentions.json -> build-brands.py -> build-brand-index.py
  search-index.json       <- generate-search-index.py
  data/post-thumbs.json   <- gen-post-thumbs.py
Hand-editing any of those is the mistake that put the Late Nine row in
brands.json and left /brands unchanged. The source files below are edited; the
derived ones are rebuilt.

THE THUMB IS DROPPED, NOT REWRITTEN.
gen-post-thumbs.py never overwrites an existing entry without --refresh, and
--refresh rewrites all 205. Deleting this one key lets the generator re-derive
exactly this post from its new hero, with no blast radius.

BOTH DASH ENCODINGS, AGAIN.
The old headline exists as "Casualist &mdash; ..." and "Casualist — ...".
Matching one spelling is what left the breadcrumb stale on the post itself.

drafts/ is deliberately excluded: it is not published.

Idempotent. Dry run by default.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SLUG = "brand-to-know-casualist"
URL = f"/drops/{SLUG}"

OLD_PLAIN = "The London Brand That Outgrew Its Own Name"
NEW_PLAIN = "The Australian Brand That Became a British Golf Label"
TODAY = "2026-09-21"

# source files only — every generated artefact is rebuilt further down
SOURCES = ["index.html", "ig.html",
           "drops/brand-to-know-twentyfour-golf.html",
           "drops/the-towel-edit-vol-3.html",
           "drops/brand-to-know-axxa.html"]


def run(args, label):
    r = subprocess.run([sys.executable] + args, cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"! {label} failed:\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
    print(f"    {label}: {tail[0].strip() if tail else 'ok'}")


def retitle_sources(apply_):
    notes = []
    for rel in SOURCES:
        p = ROOT / rel
        if not p.is_file():
            notes.append(f"!! {rel} missing"); continue
        h = p.read_text(encoding="utf-8")
        n = h.count(OLD_PLAIN)
        if not n:
            continue
        h2 = h.replace(OLD_PLAIN, NEW_PLAIN)
        if apply_:
            p.write_text(h2, encoding="utf-8")
        notes.append(f"{rel}: {n} occurrence(s) retitled")
    return notes or ["no source file still carries the old title"]


def retitle_mentions(apply_):
    p = ROOT / "data/brand-mentions.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    hits = 0
    for slug, entries in m.items():
        for e in entries:
            if e.get("url") == URL and OLD_PLAIN in e.get("title", ""):
                e["title"] = e["title"].replace(OLD_PLAIN, NEW_PLAIN)
                hits += 1
    if apply_ and hits:
        p.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    return f"brand-mentions.json: {hits} title(s) updated"


def drop_stale_thumb(apply_):
    p = ROOT / "data/post-thumbs.json"
    t = json.loads(p.read_text(encoding="utf-8"))
    cur = t.get(URL, {}).get("img")
    if cur == "/images/casualist/btk-hero-2026.jpg":
        return "post-thumbs already on the new hero"
    if apply_:
        t.pop(URL, None)
        p.write_text(json.dumps(dict(sorted(t.items())), indent=1,
                                ensure_ascii=False), encoding="utf-8")
    return f"post-thumbs: dropped stale entry ({cur}) for the generator to re-derive"


def bump_sitemap(apply_):
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    pat = re.compile(rf"(<loc>https://thegrassyissue\.com{re.escape(URL)}</loc>\s*"
                     rf"<lastmod>)([^<]*)(</lastmod>)")
    m = pat.search(s)
    if not m:
        return "!! sitemap entry not found"
    if m.group(2) == TODAY:
        return "sitemap lastmod already current"
    if apply_:
        p.write_text(pat.sub(rf"\g<1>{TODAY}\g<3>", s, count=1), encoding="utf-8")
    return f"sitemap lastmod {m.group(2)} -> {TODAY}"


def main(apply_):
    for n in retitle_sources(apply_):
        print("  " + n)
    print("  " + retitle_mentions(apply_))
    print("  " + drop_stale_thumb(apply_))
    print("  " + bump_sitemap(apply_))
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  rebuilding derived artefacts:")
    run(["gen-post-thumbs.py", "--apply"], "gen-post-thumbs")
    run(["build-brands.py"], "build-brands")
    run(["build-brand-index.py", "--apply"], "build-brand-index")
    run(["generate-search-index.py"], "generate-search-index")

    # ---- VERIFY THE FINISHED ARTEFACTS, NOT THE INPUTS ----
    bad = []
    published = [p for p in ROOT.rglob("*.html")
                 if "drafts" not in p.parts and "research" not in p.parts]
    for p in published + [ROOT / "search-index.json"]:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if OLD_PLAIN in txt:
            bad.append(f"old title survives in {p.relative_to(ROOT)}")

    thumbs = json.loads((ROOT / "data/post-thumbs.json").read_text(encoding="utf-8"))
    got = thumbs.get(URL, {}).get("img")
    if got != "/images/casualist/btk-hero-2026.jpg":
        bad.append(f"post-thumbs is {got}, expected the new hero")

    bp = (ROOT / "brands/casualist.html").read_text(encoding="utf-8")
    if NEW_PLAIN not in bp:
        bad.append("the brand page does not show the new title")
    if "btk-hero-2026.jpg" not in bp:
        bad.append("the brand page card is not using the new hero")

    si = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    row = next((r for r in si if r.get("u") == URL), None)
    if not row:
        bad.append("post missing from the search index")
    elif NEW_PLAIN not in row.get("t", ""):
        bad.append(f"search index title still {row.get('t')!r}")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified: old title gone from every published page, "
          f"thumb on the new hero, brand page and search index both current")


if __name__ == "__main__":
    main("--apply" in sys.argv)
