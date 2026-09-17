#!/usr/bin/env python3
"""Give the brand pages something to read.

THE PROBLEM, from the 9/17/26 audit: 131 brand pages, median 105 words, of which
about 60 are chrome. The body of a brand page is one sentence — "Co-founded 2017
by Erica and Stephen Malbon. Started as an Instagram mood board." — followed by a
grid of post cards. For Malbon that one sentence sits above 41 posts and 14,531
words of coverage elsewhere on this site. The page is an index, not a page.

WHAT THIS ADDS: a two-paragraph precis, ~145 words, written by hand into
data/brand-precis.json and injected here. Batch 1 is the twenty brands with the
most measured coverage (research/brand-source-v3.json).

WRITTEN, NOT LIFTED — AND THE GUARD IS THE POINT.
A precis assembled out of sentences from the brand's own profile post would be
the worst possible outcome: two URLs on one domain carrying the same paragraphs,
competing for the same query, and Google picking whichever it likes. So every
precis is checked against a shingle index of EVERY OTHER PAGE ON THE SITE and
rejected if it shares an 8-word run with any of them. The brand pages themselves
are excluded from that corpus, or the second run would flag the first run's work.

ALSO REPAIRS A TEMPLATE BUG. build-brands.py emitted
<h2 class="bp-gridhdr">Every Grassy Issue Post Featuring X</h2> INSIDE
.bp-headtext and ABOVE the one-line description, so all 131 pages read:

    Malbon Golf
    LOS ANGELES, CA · APPAREL
    Every Grassy Issue Post Featuring Malbon Golf      <- header for a grid
    Co-founded 2017 by Erica and Stephen Malbon...        that is 400px below
    Read the full profile ->

The heading is now moved out of the header block to where it belongs, directly
above the grid it heads. The template is fixed too, so a full rebuild stays
correct. Moving it is also what makes room for the precis: header, precis, then
the grid under its own heading.

IDEMPOTENT. Both the move and the injection are marker-fenced and replaced, not
appended, on a re-run. Editing a precis in the JSON and re-running is the whole
update path.

RUN ORDER: after build-brands.py -> build-brand-index.py -> build-brand-taxonomy.py
-> wire-brand-taxonomy.py -> fix-thin-brand-pages.py. Then generate-search-index.py,
because the search snippets change.
"""
import json, re, os, sys, glob, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
brands = {b["slug"]: b for b in json.load(open(os.path.join(ROOT, "data", "brands.json"),
                                              encoding="utf-8"))}
PRECIS = json.load(open(os.path.join(ROOT, "data", "brand-precis.json"), encoding="utf-8"))
PRECIS.pop("_note", None)

apply_ = "--apply" in sys.argv
MIN_W, MAX_W = 110, 200
START, END = "<!--TX-PRECIS-->", "<!--/TX-PRECIS-->"
SHINGLE = 8

CSS = """<style id="tx-precis-css">
.bp-precis{max-width:1200px;margin:34px auto 0;padding:0 24px}
.bp-precis .bp-precis-in{max-width:68ch;border-top:1px solid rgba(20,20,20,.12);padding-top:20px}
.bp-precis p{font-size:17px;line-height:1.72;color:#2b2f2a;margin:0 0 14px}
.bp-precis p:last-child{margin-bottom:0}
@media(max-width:700px){.bp-precis p{font-size:16px;line-height:1.68}}
</style>"""


def words(s):
    """Plain lowercase word list — entities unescaped BEFORE tags are stripped,
    so &amp; does not leave a stray 'amp' in the stream."""
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.findall(r"[a-z0-9']+", H.unescape(s).lower())


# ---- the corpus every precis is checked against ---------------------------
# Everything on the site EXCEPT the brand pages. Excluding brands/ is not
# optional: after one --apply run the precis is on a brand page, so including
# them would make the second run reject every entry as a duplicate of itself.
corpus, files = set(), []
for pat in ("*.html", "drops/*.html", "fieldnotes/*.html", "guides/*.html",
            "events/*.html", "news/*.html", "vs/*.html"):
    files += glob.glob(os.path.join(ROOT, pat))
for f in files:
    w = words(open(f, encoding="utf-8", errors="ignore").read())
    for i in range(len(w) - SHINGLE + 1):
        corpus.add(tuple(w[i:i + SHINGLE]))

# ---- validate every entry before touching a single file -------------------
problems = []
for slug, paras in PRECIS.items():
    if slug not in brands:
        problems.append(f"{slug}: not in brands.json"); continue
    if not os.path.exists(os.path.join(ROOT, "brands", slug + ".html")):
        problems.append(f"{slug}: brands/{slug}.html does not exist"); continue
    if not isinstance(paras, list) or len(paras) != 2:
        problems.append(f"{slug}: expected exactly 2 paragraphs"); continue

    body = " ".join(paras)
    w = words(body)
    if not MIN_W <= len(w) <= MAX_W:
        problems.append(f"{slug}: {len(w)} words, want {MIN_W}-{MAX_W}")
    if re.search(r"\bworth\b", H.unescape(body), re.I) and "fort worth" not in body.lower():
        problems.append(f"{slug}: contains the banned word 'worth'")

    # THE BRAND HAS TO BE NAMED IN ITS OWN PRECIS. Take the distinctive part of
    # the name, not the longest token — "Jones Sports Co" is longest at "Sports",
    # which is in half the names in the Index and in none of the copy.
    name = brands[slug]["name"]
    GENERIC = {"golf", "sports", "sport", "the", "and", "club", "studio", "co",
               "company", "goods", "supply", "brand", "shop", "things", "society"}
    toks = [x.lower() for x in re.findall(r"[A-Za-z0-9']{2,}", name)]
    key = [x for x in toks if x not in GENERIC] or toks
    flat = " ".join(w)
    if not any(x in flat for x in key):
        problems.append(f"{slug}: never names {name} (looked for {'/'.join(key)})")

    # THE DUPLICATE-COPY GUARD
    hits = [" ".join(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)
            if tuple(w[i:i + SHINGLE]) in corpus]
    if hits:
        problems.append(f"{slug}: shares {len(hits)} {SHINGLE}-word run(s) with an existing "
                        f"page — first is \"{hits[0]}\". Rewrite it; duplicate copy would put "
                        f"the brand page and the post it came from in the same auction.")

if problems:
    print("REJECTED — nothing written:\n")
    for p in problems:
        print("  ·", p)
    raise SystemExit(1)

# ---- write ----------------------------------------------------------------
GRIDHDR = re.compile(r'\s*<h2 class="bp-gridhdr">.*?</h2>', re.S)
moved, injected = 0, 0

# The heading repair runs over ALL 131 brand pages, not just this batch — the
# bug is on every one of them and has nothing to do with which brands have a
# precis yet. The injection below only touches the batch.
for slug in brands:
    p = os.path.join(ROOT, "brands", slug + ".html")
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8").read()
    paras = PRECIS.get(slug)
    if paras:
        t = re.sub(re.escape(START) + r".*?" + re.escape(END), "", t, flags=re.S)  # idempotent

    # 1. the misplaced grid heading
    head_end = t.find("</header>")
    if head_end == -1:
        raise SystemExit(f"{slug}: no </header>")
    m = GRIDHDR.search(t, 0, head_end)
    if m:
        h2 = m.group(0).strip()
        t = t[:m.start()] + t[m.end():]
        grid = t.find('<div class="bp-grid">')
        if grid == -1:
            raise SystemExit(f"{slug}: no .bp-grid to put the heading above")
        t = t[:grid] + h2 + "\n" + t[grid:]
        moved += 1
    elif paras is None and 'class="bp-gridhdr"' not in t:
        raise SystemExit(f"{slug}: lost its grid heading entirely")

    # 2. the precis, between the header and that heading
    if paras:
        block = (START + '<section class="bp-precis"><div class="bp-precis-in">'
                 + "".join(f"<p>{x}</p>" for x in paras) + "</div></section>" + END)
        at = t.find("</header>") + len("</header>")
        t = t[:at] + "\n\n" + block + "\n" + t[at:]
        if 'id="tx-precis-css"' not in t:
            t = t.replace("</head>", CSS + "\n</head>", 1)
        injected += 1

    if apply_:
        open(p, "w", encoding="utf-8").write(t)

# ---- post-write guards -----------------------------------------------------
if apply_:
    for slug in PRECIS:
        t = open(os.path.join(ROOT, "brands", slug + ".html"), encoding="utf-8").read()
        if t.count(START) != 1 or t.count(END) != 1:
            raise SystemExit(f"{slug}: precis markers doubled — the run was not idempotent")
        # match the TAG, not the string — ".bp-gridhdr{...}" also appears in the
        # page's own <style> block, which sits above </header> on every page and
        # made the first version of this guard fire on all twenty
        H2 = '<h2 class="bp-gridhdr"'
        if H2 in t[:t.find("</header>")]:
            raise SystemExit(f"{slug}: the grid heading is still inside the header")
        if t.find(START) > t.find(H2):
            raise SystemExit(f"{slug}: the precis landed below the grid heading")
        # a noindexed page getting a precis would be wasted writing
        if "TX-NOINDEX" in t:
            raise SystemExit(f"{slug}: carries noindex but was given a precis — re-run "
                             f"fix-thin-brand-pages.py, it should have cleared the floor")

done = set(PRECIS)
todo = [s for s in brands if s not in done]
wc = {s: len(words(" ".join(v))) for s, v in PRECIS.items()}
print(("applied" if apply_ else "DRY RUN") + f" — batch of {len(PRECIS)}")
print(f"  precis injected           : {injected}")
print(f"  misplaced grid headings fixed: {moved} (all brand pages, not just the batch)")
print(f"  words: min {min(wc.values())}, median {sorted(wc.values())[len(wc)//2]}, max {max(wc.values())}")
print(f"  checked against {len(corpus):,} {SHINGLE}-word shingles from {len(files)} non-brand pages — 0 collisions")
print(f"  brand pages still without a precis: {len(todo)}")
if not apply_:
    print("\npass --apply to write")
