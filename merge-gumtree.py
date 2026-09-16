#!/usr/bin/env python3
"""Merge gumtree-nature-club INTO gumtree-golf. One brand, one index entry.

THE PROBLEM. The index carried two records for what readers experience as one
Brooklyn brand:

  gumtree-golf         14 mentions, NO profile at all, name "Gumtree Golf & Nature Club"
  gumtree-nature-club   9 mentions, holds the only profile:true

So the half with the link equity had no coverage page, and /brands listed the
same Greenpoint studio twice. Lenny called the merge on 2026-09-15.

CANONICAL IS gumtree-golf, on two grounds: it carries the larger share of the
internal links, and its `name` is the brand's full one — the Off Course Vol 2
surfboard listing is branded GGNC, "Gumtree Golf & Nature Club".

WHAT MERGES
  cats     union — headcovers, apparel, bags gain accessories
  regions  identical, no change
  attrs    union — gumtree-golf gains drops-and-vanishes
  added    the EARLIER of the two dates, because the brand has been in the
           index since 2026-08-24 even if this particular record is newer
  url      takes gumtree-nature-club's, because that record held the profile
           and /drops/gumtree-nature-club-drop is about the brand's own
           collection. The PUMA post gumtree-golf pointed at is a collab drop,
           which is a worse profile for a brand page.
  line     rewritten to carry facts from BOTH records — the Greenpoint studio
           and upcycled textiles from one, the Melbourne-transplant founder and
           the gum-leaf name from the other. Neither original line said both.
  mentions union, deduplicated by url, exactly one profile:true

TAGS ARE CAPPED AT THREE (house rule) and the union is four: independent,
made-by-hand, loud-on-purpose, gorpcore. This script KEEPS gumtree-golf's
curated three and drops `gorpcore`, on the principle that absorbing a record
should not silently rewrite the surviving record's taste tags. If gorpcore is
the better read, swap it for loud-on-purpose by hand — it is a one-line change.

THE 301 IS NOT OPTIONAL. /brands/gumtree-nature-club is a live, indexed URL
that build-brands.py will stop generating the moment the entry disappears.
Without the redirect it 404s and the link equity evaporates — which is the
opposite of the point. Added to vercel.json alongside the fifteen existing
redirects.

Idempotent: re-running detects the merge is already done and exits clean.
"""
import json, re, sys, glob, os

KEEP = "gumtree-golf"
DROP = "gumtree-nature-club"
MERGED_LINE = ("Small-batch headcovers, bags and apparel sewn in a Greenpoint studio "
               "from upcycled and vintage textiles, by a Melbourne transplant who put "
               "the gum leaf in the name.")
apply_ = "--apply" in sys.argv
notes = []

brands = json.load(open("data/brands.json"))
mm = json.load(open("data/brand-mentions.json"))
by = {b["slug"]: b for b in brands}

if DROP not in by and KEEP in by:
    print(f"already merged — {DROP} is gone and {KEEP} remains. Nothing to do.")
    sys.exit(0)
for s in (KEEP, DROP):
    if s not in by:
        raise SystemExit(f"{s} missing from brands.json — cannot merge")

k, d = by[KEEP], by[DROP]

# ---------------------------------------------------------------- brands.json
CATS_OK = {"apparel", "equipment", "bags", "headcovers", "headwear",
           "accessories", "grips", "art", "community"}
cats = list(dict.fromkeys(k.get("cats", []) + d.get("cats", [])))
bad = set(cats) - CATS_OK
if bad:
    raise SystemExit(f"build-brands.py CATS is a fixed list; {bad} will KeyError")

tags_union = list(dict.fromkeys(k.get("tags", []) + d.get("tags", [])))
tags = k.get("tags", [])[:3]
dropped_tags = [t for t in tags_union if t not in tags]
attrs = list(dict.fromkeys(k.get("attrs", []) + d.get("attrs", [])))
regions = list(dict.fromkeys(k.get("regions", []) + d.get("regions", [])))
added = min(x for x in (k.get("added"), d.get("added")) if x)

k["cats"], k["tags"], k["attrs"], k["regions"], k["added"] = cats, tags, attrs, regions, added
k["line"] = MERGED_LINE
k["url"] = d["url"]                       # the record that held the profile
if d.get("img") and not k.get("img"):
    k["img"] = d["img"]

brands = [b for b in brands if b["slug"] != DROP]
brands.sort(key=lambda b: b["slug"])
notes.append(f"cats -> {cats}")
notes.append(f"attrs -> {attrs} | added -> {added} | url -> {k['url']}")
if dropped_tags:
    notes.append(f"TAG DROPPED by the 3-tag cap: {dropped_tags} "
                 f"(kept {tags}) — swap by hand if you disagree")

# ------------------------------------------------------------------- mentions
merged, seen = [], set()
for e in mm.get(DROP, []) + mm.get(KEEP, []):     # DROP first: it holds the profile
    if e["url"] in seen:
        continue
    seen.add(e["url"])
    merged.append(dict(e))
bad = [e for e in merged if set(e) != {"url", "title", "profile"}]
if bad:
    raise SystemExit(f"brand-mentions schema drift: {bad[:2]}")
n_prof = sum(1 for e in merged if e.get("profile"))
if n_prof != 1:
    raise SystemExit(f"merged mentions must carry exactly one profile:true, found {n_prof}")
if merged[0]["url"] != k["url"]:
    raise SystemExit("the profile entry must be the same url as the brands.json entry")
mm[KEEP] = merged
mm.pop(DROP, None)
notes.append(f"mentions {len(mm.get(DROP, []) or [])}+{len(merged)} -> {len(merged)} unique, "
             f"profile = {merged[0]['url']}")

# ---------------------------------------------------------------------- 301
vj = json.load(open("vercel.json"))
src, dst = f"/brands/{DROP}", f"/brands/{KEEP}"
if not any(r.get("source") == src for r in vj.get("redirects", [])):
    vj.setdefault("redirects", []).append(
        {"source": src, "destination": dst, "permanent": True})
    notes.append(f"301 added: {src} -> {dst}")
else:
    notes.append("301 already present")

# --------------------------------------------------------- internal link sweep
# Scoped to the directories that can contain a /brands/ link. A recursive
# **/*.html glob over the whole tree takes long enough through the sandbox
# mount to blow the 180s tool timeout, and everything outside these four
# directories is generated output that never hand-links a brand slug.
stale = []
for p in (glob.glob("*.html") + glob.glob("brands/*.html")
          + glob.glob("brands/tag/*.html") + glob.glob("brands/attr/*.html")
          + glob.glob("drops/*.html")):
    if p.startswith("_tmp_") or p == f"brands/{DROP}.html":
        continue
    try:
        h = open(p, encoding="utf-8").read()
    except OSError:
        continue
    if src in h:
        stale.append(p)
if stale:
    notes.append(f"{len(stale)} page(s) still link {src} directly — "
                 f"the 301 covers them, but build-brand-index will refresh most: {stale[:5]}")

# -------------------------------------------------------------------- guards
if any(b["slug"] == DROP for b in brands):
    raise SystemExit("the dropped slug survived in brands.json")
if DROP in mm:
    raise SystemExit("the dropped slug survived in brand-mentions.json")
if len(tags) > 3:
    raise SystemExit("three taste tags maximum (house rule)")

if apply_:
    json.dump(brands, open("data/brands.json", "w"), indent=1, ensure_ascii=False)
    json.dump(mm, open("data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
    json.dump(vj, open("vercel.json", "w"), indent=1, ensure_ascii=False)
    old = f"brands/{DROP}.html"
    if os.path.exists(old):
        os.remove(old)
        notes.append(f"removed stale {old} (the 301 now covers it)")
    print(f"merged {DROP} -> {KEEP} | brands.json now {len(brands)} entries")
else:
    print("DRY RUN — pass --apply")
    print(f"  would merge {DROP} -> {KEEP}, leaving {len(brands)} brands")
for n in notes:
    print("  ·", n)
