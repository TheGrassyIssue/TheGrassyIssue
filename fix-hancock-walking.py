#!/usr/bin/env python3
"""Hancock: dead City link fixed, walking-only made machine-readable — 17 Sept 2026.

WALKING ONLY WAS ALREADY ON THE PAGE, in four places, and all four are right:
the body ("Walking only."), the stat block ("Only walking"), the comparison
table's Walk column ("Only", where every other muni says "Yes"), and the cheapest-
golf FAQ answer. Nothing there needed changing.

WHAT DID NEED FIXING — A DEAD LINK I HALF-INTRODUCED
-----------------------------------------------------
Yesterday's schema work put Hancock's live City URL into the JSON-LD:

    https://www.austintexas.gov/golfatx/hancock-course

but the visible "Course info ↗" link on the page still pointed at

    https://www.austintexas.gov/golfatx/hancock-golf-course

which returns an EMPTY BODY — verified directly today, and independently before
that. So the page was advertising two different addresses for the same course,
one of which is dead, and the dead one was the one a reader would click. The
internal-link checker never caught it because it is an external URL.

Only the Field Guide carried the stale address; nothing else on the site links it.

WALKING-ONLY, MADE MACHINE-READABLE
-----------------------------------
Given the whole point of the schema work is to be quotable by an assistant, the
single most distinguishing fact about Hancock should not live only in prose. So
each muni now carries an amenityFeature for golf carts:

    Hancock                    Golf carts: false   ("walking only", City's words;
                                                    cart rental listed as N/A)
    Lions, Morris Williams,    Golf carts: true    (City publishes $18 per-person
    Roy Kizer, Jimmy Clay                           cart rental on each page)

Both values were read from the City's own pages today. No other course on the
page gets this property, because no other course's cart policy was verified.
"""
import re, os, sys, json

apply_ = "--apply" in sys.argv
P = "field-guide/index.html"
DEAD = "https://www.austintexas.gov/golfatx/hancock-golf-course"
LIVE = "https://www.austintexas.gov/golfatx/hancock-course"

# Verified on the City's own course pages, 17 September 2026.
CARTS = {
    "Hancock Golf Course": False,          # "walking only"; cart rental N/A
    "Lions Municipal Golf Course": True,   # "$18 per Golfer"
    "Morris Williams Golf Course": True,   # "$18 per Golfer"
    "Roy Kizer Golf Course": True,         # "$18 per Golfer"
    "Jimmy Clay Golf Course": True,        # "$18 per Golfer"
}

t = open(P, encoding="utf-8").read()
orig = t
log, problems = [], []

# ------------------------------------------------------------ 1. dead link
n = t.count(DEAD)
if n == 0:
    problems.append("the stale Hancock URL is not on the page — has this already run?")
else:
    t = t.replace(DEAD, LIVE)
    log.append(f"visible Course info link: {DEAD} -> {LIVE}  (x{n})")

# --------------------------------------------- 2. carts as amenityFeature
ms = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
      if '"ItemList"' in m.group(1) and "Municipal" in m.group(1)]
if len(ms) != 1:
    problems.append(f"expected 1 municipal ItemList, found {len(ms)}")
else:
    m = ms[0]
    d = json.loads(m.group(1))
    hit = 0
    for li in d["itemListElement"]:
        item = li["item"]
        if item["name"] in CARTS:
            item["amenityFeature"] = {
                "@type": "LocationFeatureSpecification",
                "name": "Golf carts",
                "value": CARTS[item["name"]],
            }
            hit += 1
    if hit != len(CARTS):
        problems.append(f"tagged {hit} courses, expected {len(CARTS)}")
    t = t[:m.start()] + ('<script type="application/ld+json">' +
                         json.dumps(d, ensure_ascii=False) + "</script>") + t[m.end():]
    log.append(f"amenityFeature 'Golf carts' added to {hit} munis "
               f"(Hancock false, the other four true)")

# ---------------------------------------------------------------- guards
if DEAD in t:
    problems.append("the dead Hancock URL survived somewhere")
if t.count(LIVE) < 2:
    problems.append("expected the live URL in both the visible link and the schema")

# the visible page must still agree with itself about walking
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
for phrase in ("Walking only", "Only walking"):
    if phrase not in plain:
        problems.append(f"the page no longer says {phrase!r} about Hancock")

# schema and prose must not contradict each other
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    d = json.loads(b)
    for li in d.get("itemListElement", []):
        it = li["item"]
        af = it.get("amenityFeature")
        if af and it["name"] == "Hancock Golf Course" and af["value"] is not False:
            problems.append("schema says Hancock has carts; the page says walking only")

# nothing visible may have moved except the one href
for tag in ("<div", "<section", "<a ", "<details", "<img"):
    if t.count(tag) != orig.count(tag):
        problems.append(f"{tag!r} count changed")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — Hancock on {P}")
for l in log:
    print("  ·", l)
print(f"\n  {len(t)-len(orig):+,} bytes")
if not apply_:
    print("\npass --apply to write")
