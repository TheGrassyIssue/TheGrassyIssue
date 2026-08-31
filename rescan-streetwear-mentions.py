#!/usr/bin/env python3
"""Resync data/brand-mentions.json for the revamped streetwear page.

The page went from 15 brands to 5. brand-mentions.json still listed 12 brands
against it and was missing the two new ones. prune-brand-mentions.py only
REMOVES false positives, never adds, so this page needed its own pass.

WHY THE LIST IS EXPLICIT, NOT MATCHED
-------------------------------------
Four successive matching heuristics were tried and each traded one error for
another on this exact page:

  1. every distinctive token anywhere in the body   -> matched Read The Green,
     because the page contains "read" and "green" in unrelated sentences
  2. the tokens as an adjacent phrase               -> lost MacKenzie, Gumtree
     and Fyfe, which the prose names in short form
  3. lead token, case-insensitive                   -> matched Inside Story off
     "makes sense inside the ropes"
  4. lead token, capitalised, not sentence-initial  -> lost Sentinel and Manors,
     which each open their own sentence in the cut section

Sixteen brands on one page is a judgement call, not a parsing problem. The list
below was read off the rendered page. The script still ASSERTS that every name
it is about to file actually appears in the editorial body, so a future rewrite
that drops a brand will fail loudly rather than leave a stale entry behind.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
URL = "/drops/best-golf-streetwear-brands-2026"
PAGE = os.path.join(ROOT, "drops", "best-golf-streetwear-brands-2026.html")
TITLE = "The 5 Best Golf Streetwear Brands in 2026"

# slug -> the string that must be present in the editorial body
ON_PAGE = {
    # the five ranked brands
    "metalwood-studio": "Metalwood",
    "students-golf": "Students",
    "malbon": "Malbon",
    "casualist": "Casualist",
    "anti-country-club-tokyo": "ANTi",
    # named and explained in "What We Cut, and Why"
    "sentinel-golf": "Sentinel",
    "fyfe-golf": "Fyfe",
    "mackenzie": "MacKenzie",
    "sugarloaf-social-club": "Sugarloaf",
    "gumtree-nature-club": "Gumtree",
    "manors": "Manors",
    "quiet-golf": "Quiet",
    "pluto-golf": "Pluto",
    "odd-ritual": "Odd Ritual",
    "random-golf-club": "Random Golf Club",
    # named in the body: a Realtree five-panel in the Metalwood paragraph, and
    # Merrill + Badlands in the stockist answer
    "realtree": "Realtree",
    "merrill-golf": "Merrill",
    "badlands": "Badlands",
}


def strip_chrome(h):
    h = re.sub(r'<head>.*?</head>', '', h, flags=re.S)
    h = re.sub(r'<nav\b.*?</nav>', '', h, flags=re.S)
    h = re.sub(r'<div class="breadcrumb">.*?</div>', '', h, flags=re.S)
    h = re.sub(r'<footer\b.*?</footer>', '', h, flags=re.S)
    h = re.sub(r'<section class="more">.*?</section>', '', h, flags=re.S)
    return h


def main(apply_=False):
    body = re.sub(r"<[^>]+>", " ", strip_chrome(open(PAGE, encoding="utf-8").read()))
    missing = [s for s, n in ON_PAGE.items() if not re.search(r'\b' + re.escape(n) + r'\b', body)]
    if missing:
        sys.exit("these brands are no longer on the page: " + ", ".join(missing))

    mentions = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json")))
    added, removed = [], []
    for slug in list(mentions):
        if slug not in ON_PAGE and any(e.get("url") == URL for e in mentions[slug]):
            mentions[slug] = [e for e in mentions[slug] if e.get("url") != URL]
            removed.append(slug)
    for slug in ON_PAGE:
        if slug not in mentions:
            print("  ! %s is not in brand-mentions.json at all — skipped" % slug)
            continue
        hit = [e for e in mentions[slug] if e.get("url") == URL]
        if hit:
            hit[0]["title"] = TITLE
        else:
            mentions[slug].append({"url": URL, "title": TITLE, "profile": False})
            added.append(slug)

    print("on page: %d brands" % len(ON_PAGE))
    print("added:   ", added or "none")
    print("removed: ", removed or "none")
    if apply_:
        json.dump(mentions, open(os.path.join(ROOT, "data", "brand-mentions.json"), "w"),
                  ensure_ascii=False, indent=1)
        print("written — now re-run build-brands.py")


if __name__ == "__main__":
    main("--apply" in sys.argv)
