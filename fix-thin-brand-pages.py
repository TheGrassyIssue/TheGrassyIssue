#!/usr/bin/env python3
"""The 49 brand pages with no profile post behind them.

FROM THE 9/17/26 AUDIT. 132 brand pages, median 105 words. Splitting them by
what source material actually exists produced a clean line rather than a
gradient:

  82 brands have a dedicated Brand to Know profile post (median 1,500-2,100
     words of researched copy, already on the site). Their brand page can carry
     a real precis written from it. Handled by build-brand-precis.py.

  49 brands have NO profile post. They appear only inside roundups. Their page
     is a one-line description and a grid of roundup appearances — for 24 of
     them, a single appearance. There is nothing to write a precis FROM.

TWO THINGS ARE WRONG WITH THOSE 49 AND ONLY ONE IS ABOUT SEO.

1. A BROKEN PROMISE. Every one of the 49 carries the CTA "Read the full profile
   →" pointing at a roundup. Bettinardi's links to the wedge report. ANTi
   Country Club Tokyo's links to the White Tee Edit. Neither is a profile. A
   reader clicking that link does not get what the link said. That is a
   correctness bug and it would need fixing even if Google did not exist. The
   CTA is REMOVED — the grid immediately below is already headed "Every Grassy
   Issue Post Featuring <brand>" and lists the same coverage honestly.

2. THIN CONTENT AT SCALE. Lenny's call, 9/17/26: noindex,follow them until they
   earn a profile. FOLLOW is the important half — the page keeps passing equity
   to the profile posts, roundups and taxonomy pages it links to, and keeps
   working as navigation and in on-site search. Only the thin page itself leaves
   the index.

   A noindex page in a sitemap is a contradictory signal, so these are pulled
   from sitemap.xml too.

REVERSIBLE BY CONSTRUCTION. The noindex tag and the removal are both fenced with
markers, and a brand automatically leaves this set the moment data/brand-mentions.json
gains a profile:true entry for it. Write the profile post, re-run, and the page
returns to the index with its CTA back.
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
mentions = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json"), encoding="utf-8"))

# WHICH BRANDS KEEP THEIR PAGE INDEXED
#
# The first version of this script used mentions' profile:true flag. That flag
# is WRONG for 33 brands: the multi-brand roundups (women-founded, Texas makers,
# Australian brands) were flagged profile:true for every brand appearing in them,
# so a brand whose only coverage is a paragraph inside a roundup looked identical
# to one with a dedicated 2,000-word profile. Using it de-indexed 33 pages that
# have real material behind them — Eastside Golf has 3,657 words of coverage
# across 13 posts and was marked thin.
#
# The signal now is measured, not declared: how many words of prose across the
# whole site are actually ABOUT this brand (research/brand-source-v3.json, built
# by measure-brand-source.py). 150 words is the line — enough to write a precis
# from without padding.
SOURCE = json.load(open(os.path.join(ROOT, "research", "brand-source-v3.json"), encoding="utf-8"))
FLOOR = 150
HAS_PROFILE = {k for k, v in SOURCE.items() if v["words"] >= FLOOR}

# THE CTA IS A SEPARATE QUESTION. "Read the full profile →" is a promise about
# what sits at the other end of the link, and it is only true when the linked
# post actually profiles this one brand. A brand can clear the indexing floor on
# roundup coverage alone (Eastside Golf, 3,657 words across 13 posts) and still
# have no profile to send anyone to. Conflating the two is what put a link
# reading "Read the full profile" on 49 pages pointing at wedge roundups.
REAL_PROFILE = set(json.load(open(os.path.join(ROOT, "research", "profile-truth.json"),
                                 encoding="utf-8"))["real"])
NOINDEX = '<meta name="robots" content="noindex,follow"><!--TX-NOINDEX thin: no profile post-->'
# The removed CTA is stashed inside a REAL html comment so it does not render,
# and so re-indexing can put it back verbatim. Delimiting it with two comment
# markers instead (the first version of this script) leaves the anchor LIVE
# between them — it looked removed in a grep and was still on the page.
CTA_OPEN, CTA_SHUT = "<!--TX-NOCTA ", " TX-NOCTA-->"

apply_ = "--apply" in sys.argv
deindexed, reindexed, cta_removed, cta_restored, missing = [], [], [], [], []

for r in brands:
    slug = r["slug"]
    p = os.path.join(ROOT, "brands", slug + ".html")
    if not os.path.exists(p):
        missing.append(slug); continue
    t = open(p, encoding="utf-8").read()
    thin = slug not in HAS_PROFILE          # governs noindex
    no_cta = slug not in REAL_PROFILE       # governs the profile link

    # ---- robots ----------------------------------------------------------
    had_ni = "TX-NOINDEX" in t
    t = re.sub(r'<meta name="robots"[^>]*><!--TX-NOINDEX[^>]*-->', "", t)
    if thin:
        t = t.replace("</head>", NOINDEX + "\n</head>", 1)
        if not had_ni:
            deindexed.append(slug)
    elif had_ni:
        reindexed.append(slug)

    # ---- the CTA that lied ------------------------------------------------
    # unstash first, so every run starts from the same shape and re-running can
    # never nest or double a marker
    stash = re.search(re.escape(CTA_OPEN) + r"(.*?)" + re.escape(CTA_SHUT), t, re.S)
    if stash:
        t = t[:stash.start()] + "\n    " + stash.group(1).strip() + t[stash.end():]
        if not no_cta:
            cta_restored.append(slug)
    t = re.sub(r"\s*<!--TX-NOCTA-->", "", t)          # clean up the broken first version

    cta = re.search(r'\s*<a class="bp-profile" href="[^"]*"[^>]*>.*?</a>', t, re.S)
    if no_cta and cta:
        body = cta.group(0).strip()
        if "--" in body:
            raise SystemExit(f"{slug}: the CTA markup contains '--' and cannot be stashed "
                             f"inside an html comment; remove it by hand")
        t = t[:cta.start()] + f"\n    {CTA_OPEN}{body}{CTA_SHUT}" + t[cta.end():]
        cta_removed.append(slug)

    if apply_:
        open(p, "w", encoding="utf-8").write(t)

# ---- sitemap: a noindex page must not be advertised in it -------------------
sp = os.path.join(ROOT, "sitemap.xml")
sm = open(sp, encoding="utf-8").read()
TODAY = "2026-09-17"
pulled, kept, readded = 0, 0, 0
for r in brands:
    loc = f"https://thegrassyissue.com/brands/{r['slug']}"
    row = re.compile(r"\s*<url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>", re.S)
    if r["slug"] not in HAS_PROFILE:
        if row.search(sm):
            sm = row.sub("", sm); pulled += 1
    else:
        kept += 1
        # a page coming BACK into the index needs its row back — pulling without
        # ever re-adding makes this a one-way door and silently shrinks the sitemap
        if not row.search(sm):
            sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                            f'<changefreq>monthly</changefreq><priority>0.5</priority></url>\n</urlset>')
            readded += 1
if apply_:
    open(sp, "w", encoding="utf-8").write(sm)

# ---- guards ----------------------------------------------------------------
if missing:
    raise SystemExit(f"brand pages missing on disk: {missing}")
thin_set = {r["slug"] for r in brands if r["slug"] not in HAS_PROFILE}
# noindex must never land on a brand that has a profile
for r in brands:
    if r["slug"] in HAS_PROFILE:
        t = open(os.path.join(ROOT, "brands", r["slug"] + ".html"), encoding="utf-8").read()
        if "TX-NOINDEX" in t and apply_:
            raise SystemExit(f"{r['slug']} clears the floor but carries noindex")
# a thin page must carry NO live profile CTA — the whole point of removing it
if apply_:
    for r in brands:
        if r["slug"] in REAL_PROFILE:
            continue
        t = open(os.path.join(ROOT, "brands", r["slug"] + ".html"), encoding="utf-8").read()
        live = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        if 'class="bp-profile"' in live:
            raise SystemExit(f"{r['slug']}: the profile CTA is still live on the page — "
                             f"stashing it between two comment markers does not remove it")
# follow must survive — losing it would strand the link equity
if apply_ and thin_set:
    s = next(iter(thin_set))
    t = open(os.path.join(ROOT, "brands", s + ".html"), encoding="utf-8").read()
    if "noindex,follow" not in t:
        raise SystemExit("the robots tag lost 'follow' — that would strand link equity")

if apply_:
    sm2 = open(sp, encoding="utf-8").read()
    for r in brands:
        inmap = f"https://thegrassyissue.com/brands/{r['slug']}</loc>" in sm2
        if inmap != (r["slug"] in HAS_PROFILE):
            raise SystemExit(f"{r['slug']}: sitemap says {inmap}, robots says "
                             f"{r['slug'] in HAS_PROFILE} — they must agree")

print(("applied" if apply_ else "DRY RUN") + f" — {len(brands)} brand pages examined")
print(f"  >= {FLOOR}w of own coverage, indexed   : {len(HAS_PROFILE)}")
print(f"  under {FLOOR}w, noindex,follow         : {len(thin_set)}")
print(f"    newly de-indexed this run          : {len(deindexed)}")
print(f"    returned to the index this run     : {len(reindexed)} "
      + (", ".join(reindexed) if reindexed else ""))
print(f'  no genuine profile, CTA removed      : {len(cta_removed)}')
print(f"    CTAs restored this run             : {len(cta_restored)} "
      + (", ".join(cta_restored) if cta_restored else ""))
print(f"  sitemap: {pulled} pulled, {readded} re-added, {kept} indexed brand rows")
if not apply_:
    print("\npass --apply to write")
