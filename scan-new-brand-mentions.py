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
    # added 21 Sep 2026 with The Hat & Towel Edit. A brand with no DOMAINS
    # entry is never visited by --rescan, gets no mentions row, and so
    # build-brands.py silently skips its page — while /brands still lists
    # it and links a 404. That is what happened here.
    "matchstick-golf": ["matchstickgolf.com"],
    # metalwoodstudio.com now redirects to an unrelated woodworking shop;
    # the brand lives at metalwood.studio. Mapping the dead domain would
    # have matched nothing and silently produced no mentions.
    "metalwood-studio": ["metalwood.studio"],
    "shapland": ["shaplandbags.com"],
    "shoal-golf": ["shoalgolfco.com"],
    # added 24 Sep 2026 with Brand to Know — Galvin Green. The BTK links
    # www.galvingreen.com; the Rain Gear Edit links the bare domain. Both match.
    "galvin-green": ["galvingreen.com"],
    # added 24 Sep 2026 with the Three Fall Drops roundup; neither had a DOMAINS
    # entry, so --rescan never reached them and the post would not appear on
    # /brands/students-golf or /brands/devereux-golf.
    "students-golf": ["studentsgolf.com"],
    "devereux-golf": ["devereuxgolf.com"],
    # Birds of Condor had NO entry at all, so every --rescan skipped it and its
    # brand page never picked up coverage. Both storefronts are listed: the .com
    # is the Australian store and us. is the USD one the post links.
    "birds-of-condor": ["birdsofcondor.com", "us.birdsofcondor.com"],
    # hiddenlinkssociety.com ONLY. hiddenlinksgolf.com is a different company
    # entirely — a custom club builder — and must never map to this slug.
    "hidden-links-society": ["hiddenlinkssociety.com"],
    "vuori":             ["vuoriclothing.com"],
    # Added 21 September 2026 with the Late Nine Brand Revisited. The brand
    # sat in brands.json with no domain here, so it got a row on the /brands
    # index and no coverage page at all — exactly the gap this script exists
    # to close, and the reason Lenny could not find it on the index.
    "late-nine":         ["late-nine.com"],
    "bettinardi":        ["bettinardi.com"],
    "eastside-golf":     ["eastsidegolf.com"],
    "ghost-golf":        ["ghostgolf.com"],
    "gumtree-golf":      ["gumtreegolf.com", "gumtreegolfandnature.com"],
    "pins-and-aces":     ["pinsandaces.com"],
    # Added 2026-09-18 with Salomon. Three other posts say the word "Salomon"
    # without linking out; by this script's domain rule they are not coverage,
    # which is right — a passing mention is not a post about the brand.
    "salomon":           ["salomon.com"],
    # Added 2026-09-20 with the Local Rule Brand to Know. The brand's own store
    # is local-rule.com; the slug and the domain stem match exactly, which is the
    # bar this map sets. Do not add localrule.com — not theirs.
    "local-rule":        ["local-rule.com"],
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
import copy; was = copy.deepcopy(ment)   # pre-scan state, for sticky profile flags
# --rescan RE-READS brands that already have entries.
#
# THE BUG THIS FIXES. The default pass only visits brands with NO mentions
# entry. That is right for onboarding a new brand and wrong forever after: once
# a brand has any entry it is never looked at again, so a NEW post about an
# EXISTING brand never reaches its coverage page. Vuori had two roundup
# mentions from 4 September, so when Brand to Know — Vuori shipped on the 21st
# the scan skipped Vuori entirely and /brands/vuori showed the two roundups and
# no profile card. Lenny found it by looking at the page.
#
# Matching is deterministic (outbound domain), so re-reading a mapped brand is
# safe and idempotent — it recomputes the same list plus anything new.
RESCAN = "--rescan" in sys.argv
todo   = ([b for b in brands if DOMAINS.get(b["slug"])] if RESCAN
          else [b for b in brands if not ment.get(b["slug"])])
print(f"{'rescanning mapped brands' if RESCAN else 'brands with no mentions entry'}: {len(todo)}\n")

for b in todo:
    doms = DOMAINS.get(b["slug"])
    if not doms:
        print(f"  !! {b['name']}: no domain mapped, skipped"); continue
    hits = []
    for f in sorted(glob.glob(f"{ROOT}/drops/*.html")):
        # Cloud-sync conflict copies ("x 2.html") hold an OS lock (Errno 35) and
        # are not real posts; skip them rather than crash the whole scan.
        if re.search(r" \d+\.html$", f):
            continue
        try:
            h = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if not matches(hosts(strip_chrome(h)), doms):
            continue
        t = re.search(r"<title>([^<]*)</title>", h)
        title = re.sub(r"\s*[—|]\s*The Grassy Issue\s*$", "",
                       html.unescape(t.group(1))).strip() if t else ""
        slug = os.path.basename(f)[:-5]
        # A Brand to Know page for this brand is its profile.
        #
        # PROFILE IS STICKY — never recompute it to False.
        # This rule only recognises the brand-to-know- prefix, but 45 entries in
        # the map are profiles under other slugs (texas-golf-brands-and-makers,
        # golf-brands-founded-by-women, gumtree-nature-club-drop …), set outside
        # this script. On the first --rescan the plain recomputation silently
        # unset gumtree-golf's, which would have dropped the profile card off
        # /brands/gumtree-golf while "fixing" /brands/vuori. A domain rescan
        # knows what a post LINKS, not what it IS, so it may only ever promote.
        prev = {x["url"]: x for x in was.get(b["slug"], [])}
        url  = "/drops/" + slug
        # THE TITLE IS THE HONEST SIGNAL, NOT THE SLUG.
        # The slug rule misses any profile piece not named for the format.
        # Late Nine's Brand Revisited lives at /drops/late-nine-stockholm-
        # relaxed-fits-and-the-quiet-part-of-golf, so the prefix test failed and
        # /brands/late-nine showed no profile card — the same symptom as Vuori,
        # a different cause. The <title> says "Brand Revisited — Late Nine",
        # which states what the post IS. Revisited counts as a profile: the
        # precedent is /drops/brand-revisited-jones-sports-co, already flagged.
        titled = bool(re.match(
            rf"brand\s+(?:to\s+know|revisited)\s*[—–-]\s*{re.escape(b['name'].lower())}$",
            title.strip().lower()))
        prof = (titled
                or (slug.startswith("brand-to-know-") and b["slug"].split("-")[0] in slug)
                or bool(prev.get(url, {}).get("profile")))
        hits.append({"url": url, "title": title, "profile": prof})
    # A RESCAN MAY ONLY ADD. Found 24 Sep 2026: the first --rescan of Students and
    # Devereux dropped ten real mentions (Sugarloaf collab posts, the camo and tee
    # carousels) because those posts name the brand but link the partner's store.
    # Domain matching finds new coverage; it cannot prove old coverage is gone.
    have = {x["url"] for x in hits}
    hits += [x for x in was.get(b["slug"], []) if x["url"] not in have]
    ment[b["slug"]] = hits
    print(f"  {b['name']:30} {len(hits):3} posts   {', '.join(x['url'].split('/')[-1] for x in hits[:4])}{' …' if len(hits)>4 else ''}")

if APPLY:
    json.dump(ment, open(f"{ROOT}/data/brand-mentions.json", "w"), indent=1, ensure_ascii=False)
print(f"\nmentions map: {len(ment)} brands")
print("applied" if APPLY else "DRY RUN — pass --apply")
