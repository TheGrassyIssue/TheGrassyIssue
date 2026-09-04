#!/usr/bin/env python3
"""
scan-new-brand-mentions.py — add mention entries for brands newly added to brands.json.

build-brands.py skips any brand with no entry in data/brand-mentions.json
("if not MENTIONS.get(slug): continue"), so a brand can sit in brands.json and be
listed on the /brands index while having no coverage page at all. That is what
happened to the 10 brands added 2026-09-04.

MATCHING IS BY OUTBOUND DOMAIN, not by name.
The first version of this script reused prune-brand-mentions.py's keys_for(), which
does substring matching on tokenised names. On these brands that is disastrous:
  STITCH      -> "stitch"  matches "stitching"/"stitched"  -> 41 bogus posts
  Pins & Aces -> "pins"    matches every flagstick mention -> 35 bogus posts
  Sunday Golf -> "sunday"  matches the day of the week     -> 24 bogus posts
A post that features a brand links to it, so the href domain is the honest signal.

Two domain traps found while building the map, both live on the site:
  sundayrollsgolf.com   is Sunday Rolls, a DIFFERENT brand from Sunday Golf
  winstonskitchenatx.com is an Austin restaurant, not Winston Collection
so domains are matched exactly (host, or host ending in ".<domain>"), never by
substring.

Dry-run default; --apply writes.
"""
import json, re, os, html, glob, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

DOMAINS = {
    "bettinardi":        ["bettinardi.com"],
    "eastside-golf":     ["eastsidegolf.com"],
    "ghost-golf":        ["ghostgolf.com"],
    "gumtree-golf":      ["gumtreegolf.com", "gumtreegolfandnature.com"],
    "pins-and-aces":     ["pinsandaces.com"],
    "sounder":           ["soundergolf.com"],
    "stitch-golf":       ["stitchgolf.com"],
    "sunday-golf":       ["sundaygolf.com"],          # NOT sundayrollsgolf.com
    "vessel":            ["vesselgolf.com", "vesselbags.com"],
    "winston-collection":["winstoncollection.com"],   # NOT winstonskitchenatx.com
}

def strip_chrome(h):
    """Drop nav/footer/More-from-the-Feed so a sitewide link never reads as coverage."""
    h = re.sub(r'<head>.*?</head>', '', h, flags=re.S)
    h = re.sub(r'<nav\b.*?</nav>', '', h, flags=re.S)
    h = re.sub(r'<div class="breadcrumb">.*?</div>', '', h, flags=re.S)
    h = re.sub(r'<footer\b.*?</footer>', '', h, flags=re.S)
    h = re.sub(r'<a[^>]*class="more-card"[^>]*>.*?</a>', '', h, flags=re.S)
    return h

def hosts(h):
    out = set()
    for u in re.findall(r'href="https?://([^/"]+)', h):
        out.add(re.sub(r'^www\.', '', u.lower()))
    return out

def matches(host_set, domains):
    return any(hst == d or hst.endswith("." + d) for hst in host_set for d in domains)

APPLY  = "--apply" in sys.argv
brands = json.load(open(f"{ROOT}/data/brands.json"))
ment   = json.load(open(f"{ROOT}/data/brand-mentions.json"))
todo   = [b for b in brands if not ment.get(b["slug"])]
print(f"brands with no mentions entry: {len(todo)}\n")

for b in todo:
    doms = DOMAINS.get(b["slug"])
    if not doms:
        print(f"  !! {b['name']}: no domain mapped, skipped"); continue
    hits = []
    for f in sorted(glob.glob(f"{ROOT}/drops/*.html")):
        h = open(f, encoding="utf-8", errors="ignore").read()
        if not matches(hosts(strip_chrome(h)), doms):
            continue
        t = re.search(r"<title>([^<]*)</title>", h)
        title = re.sub(r"\s*[—|]\s*The Grassy Issue\s*$", "",
                       html.unescape(t.group(1))).strip() if t else ""
        slug = os.path.basename(f)[:-5]
        # a Brand to Know page for this brand is its profile
        prof = slug.startswith("brand-to-know-") and b["slug"].split("-")[0] in slug
        hits.append({"url": "/drops/" + slug, "title": title, "profile": prof})
    ment[b["slug"]] = hits
    print(f"  {b['name']:30} {len(hits):3} posts   {', '.join(x['url'].split('/')[-1] for x in hits[:4])}{' …' if len(hits)>4 else ''}")

if APPLY:
    json.dump(ment, open(f"{ROOT}/data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
print(f"\nmentions map: {len(ment)} brands")
print("applied" if APPLY else "DRY RUN — pass --apply")
