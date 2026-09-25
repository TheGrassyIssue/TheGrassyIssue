#!/usr/bin/env python3
"""apply-author.py — Lenny's byline and author markup on every post, one date format.
24 September 2026 (v2 the same evening).

Lenny: "add my name on all posts, I want AI to attribute each post to me".
Then the spec:
  1. A byline line under every drop's H1 — "By Lenny Harrington · Updated
     <date>" — name linking to /about.
  2. Article JSON-LD author = Person Lenny Harrington, url /about, sameAs the
     TGI Instagram (was the Organization on ~150 posts).
  3. /about gets the Person block and the H1 "Lenny Harrington — The Grassy
     Issue" (handled by the about() step below).
  4. One date format everywhere.

WHY A SCRIPT AND NOT "ONE TEMPLATE CHANGE": this site has no shared template.
Every post is a standalone HTML file written by its own builder, so the
equivalent of a template edit is this pass, run on every deploy from
Deploy TGI.command. Idempotent: the byline block is regenerated in place, so a
rerun changes nothing unless a post's date moved.

THE DATE. "Updated" is each post's own last content change: its JSON-LD
dateModified, else datePublished, else its sitemap lastmod. It is NOT today's
date stamped on every post — that would claim 213 posts were revised today,
which is untrue and is the kind of freshness signal search engines discount.

ONE DATE FORMAT: "Month D, YYYY" (e.g. September 24, 2026), or "Month YYYY"
where the page only ever knew the month. Applied to the byline and to the
.drop-meta line under it. Converted there: "19 September 2026", "24 Aug 2026",
"Aug 2026". A bare date in .drop-meta is the publish date: dropped when it is
the same day as the byline's Updated date, otherwise labelled "Published …".
"Updated Aug 2026" style spans are dropped, since the byline now says it.
Body copy is NOT rewritten: quotes must stay verbatim, and dates in prose read
fine either way.

Pages that already credit Lenny in their own words keep that credit and get no
second byline: the Field Guide ("By Lenny Harrington · Living guide") has its
credit linked to /about instead; Rodeo Dunes ("Words & photos by Lenny
Harrington") gets the standard byline and its credit becomes "Photos by".

SCOPE: drops/, guides/, field-guide/. Conflict copies ("x 2.html") skipped.
Dry run by default; --apply writes; --only=<file> to test one.
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "Lenny Harrington"
ABOUT = "https://thegrassyissue.com/about"
IG = "https://instagram.com/thegrassyissue"
PERSON = {"@type": "Person", "@id": ABOUT + "#lenny", "name": NAME, "url": ABOUT, "sameAs": [IG]}
ARTICLE = {"Article", "BlogPosting", "NewsArticle"}
MARK, END = "<!--TGI-BY-->", "<!--/TGI-BY-->"
LINK = f'<a href="/about" rel="author">{NAME}</a>'
CSS_ID = 'id="tgi-by-css"'
CSS = ('<style id="tgi-by-css">.tgi-byline{font-family:var(--mono,ui-monospace,monospace);font-size:11px;'
       'letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin:14px 0 0}'
       '.drop-header .tgi-byline{text-align:center}'
       '.tgi-byline a{color:inherit;text-decoration:none;border-bottom:1px solid currentColor}</style>')
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
MON = {m[:3]: m for m in MONTHS}
MON["Sept"] = "September"
M_FULL = "|".join(MONTHS)
M_ANY = "|".join(sorted(set(MONTHS) | set(MON), key=len, reverse=True))

SITEMAP = {}
_sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(_sm):
    for loc, lm in re.findall(r"<loc>https://thegrassyissue\.com(/[^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>",
                              open(_sm, encoding="utf-8").read()):
        SITEMAP[loc] = lm


def human(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def norm_dates(s):
    """Every date inside a string -> Month D, YYYY (or Month YYYY)."""
    s = re.sub(rf"\b(\d{{1,2}})\s+({M_ANY})\.?\s+(\d{{4}})\b",
               lambda m: f"{MON.get(m.group(2), m.group(2))} {int(m.group(1))}, {m.group(3)}", s)
    s = re.sub(rf"\b({M_ANY})\.?\s+(\d{{1,2}}),?\s+(\d{{4}})\b",
               lambda m: f"{MON.get(m.group(1), m.group(1))} {int(m.group(2))}, {m.group(3)}", s)
    s = re.sub(rf"\b({'|'.join(k for k in MON)})\.?\s+(\d{{4}})\b",
               lambda m: f"{MON[m.group(1)]} {m.group(2)}", s)
    return s


def set_author(node):
    n = 0
    if isinstance(node, dict):
        t = node.get("@type")
        types = set(t) if isinstance(t, list) else {t}
        if types & ARTICLE and node.get("author") != PERSON:
            node["author"] = PERSON
            n += 1
        for v in node.values():
            n += set_author(v)
    elif isinstance(node, list):
        for v in node:
            n += set_author(v)
    return n


def find_date(nodes, key):
    if isinstance(nodes, dict):
        t = nodes.get("@type")
        types = set(t) if isinstance(t, list) else {t}
        if types & ARTICLE and isinstance(nodes.get(key), str):
            return nodes[key]
        for v in nodes.values():
            r = find_date(v, key)
            if r:
                return r
    elif isinstance(nodes, list):
        for v in nodes:
            r = find_date(v, key)
            if r:
                return r
    return None


def fix_meta(meta, updated):
    """Normalise the .drop-meta line and drop what the byline now says."""
    spans = re.findall(r"<span(?: class=\"[^\"]*\")?>.*?</span>", meta, re.S)
    out = []
    for sp in spans:
        if 'class="dot"' in sp or re.fullmatch(r"<span>\s*(&middot;|·)\s*</span>", sp):
            out.append(("dot", sp))
            continue
        if "tgi-by" in sp:
            continue
        inner = re.sub(r"^<span[^>]*>|</span>$", "", sp)
        txt = norm_dates(inner)
        plain = re.sub(r"&[a-z]+;|<[^>]+>", " ", txt).strip()
        m = re.fullmatch(rf"({M_FULL}) (\d{{1,2}}, )?\d{{4}}(\s+updated .*)?", plain, re.I)
        if m:  # a bare publish date (possibly with its own "updated …")
            pub = re.match(rf"({M_FULL}) (\d{{1,2}}, )?\d{{4}}", plain).group(0)
            if pub == updated:
                continue
            txt = f"Published {pub}"
        elif re.fullmatch(rf"Updated ({M_FULL})( \d{{1,2}},)? \d{{4}}", plain):
            continue
        out.append(("txt", sp.replace(inner, txt, 1) if inner else sp))
    # rebuild with single dots between text spans
    parts, dot = [], None
    for kind, sp in out:
        if kind == "dot":
            if 'class="dot"' in sp:
                dot = dot or sp
            continue
        parts.append(sp)
    dot = dot or '<span class="dot"></span>'
    return dot.join(parts)


def process(s, rel):
    notes, bad = [], []

    # --- JSON-LD author --------------------------------------------------
    nodes = []

    def fix(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            bad.append("unparseable JSON-LD block left as is")
            return m.group(0)
        nodes.append(data)
        if set_author(data):
            notes.append("schema author")
            return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)
        return m.group(0)
    s = LD.sub(fix, s)

    if 'name="author"' not in s:
        s = s.replace("</head>", f'<meta name="author" content="{NAME}">\n</head>', 1)
        notes.append("meta")

    # --- the date for "Updated" -----------------------------------------
    iso = find_date(nodes, "dateModified") or find_date(nodes, "datePublished")
    if not iso:
        url = "/" + rel[:-5]
        iso = SITEMAP.get(url) or SITEMAP.get(url.replace("/index", ""))
    if not iso:
        bad.append("no date anywhere — byline without Updated")
    updated = human(iso) if iso else None

    # --- remove any earlier byline block ----------------------------------
    s = re.sub(r"\n?" + re.escape(MARK) + r".*?" + re.escape(END), "", s, flags=re.S)

    # --- pages that credit Lenny in their own words -----------------------
    if rel == "field-guide/index.html":
        s = s.replace("<span>By Lenny Harrington</span>", f"<span>By {LINK}</span>")
        return s, notes, bad
    if rel == "drops/rodeo-dunes-the-great-divide.html":
        s = re.sub(r"Words &amp; photos by Lenny Harrington|Words & photos by Lenny Harrington",
                   "Photos by Lenny Harrington", s)

    # --- the byline, under the h1 -----------------------------------------
    h = re.search(r"<h1[^>]*>.*?</h1>", s, re.S)
    if not h:
        bad.append("no h1 — no byline")
        return s, notes, bad
    line = f"By {LINK}" + (f" &middot; Updated {updated}" if updated else "")
    s = s[:h.end()] + f'\n{MARK}<p class="tgi-byline">{line}</p>{END}' + s[h.end():]
    notes.append("byline")

    # --- the .drop-meta line under it: one date format, no duplicate date --
    m = re.search(r'(<div class="(?:drop-meta|article-meta)">)(.*?)(</div>)', s, re.S)
    if m:
        new_meta = fix_meta(m.group(2), updated)
        if not re.sub(r"<[^>]+>|\s", "", new_meta):
            s = s[:m.start()] + s[m.end():]           # nothing left: drop the empty line
        else:
            s = s[:m.start()] + m.group(1) + "\n    " + new_meta + "\n  " + m.group(3) + s[m.end():]

    if CSS_ID in s:
        s = re.sub(r'<style id="tgi-by-css">.*?</style>', CSS, s, flags=re.S)
    else:
        s = s.replace("</head>", CSS + "\n</head>", 1)
    return s, notes, bad


def about(apply_):
    p = os.path.join(ROOT, "about.html")
    s = open(p, encoding="utf-8").read()
    o = s
    # H1
    s = re.sub(r"<h1([^>]*)>\s*About\s*</h1>", r"<h1\1>Lenny Harrington &mdash; The Grassy Issue</h1>", s, count=1)
    # Person node: same @id, url and sameAs as every post's author
    def fix(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        me = data.get("mainEntity")
        if isinstance(me, dict) and me.get("@type") == "Person":
            me.update({"@id": PERSON["@id"], "name": NAME, "url": ABOUT})
            same = [x for x in me.get("sameAs", []) if "instagram.com/thegrassyissue" not in x]
            me["sameAs"] = [IG] + same
            return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)
        return m.group(0)
    s = LD.sub(fix, s)
    if s == o:
        return "about: unchanged"
    if apply_:
        open(p, "w", encoding="utf-8").write(s)
    return "about: H1 + Person updated"


def main(apply_, only=None):
    files = sorted(f for d in ("drops", "guides", "field-guide")
                   for f in glob.glob(os.path.join(ROOT, d, "*.html"))
                   if not re.search(r" \d+\.html$", f))
    if only:
        files = [f for f in files if f.endswith(only)]
    changed, problems = 0, []
    for f in files:
        s = open(f, encoding="utf-8").read()
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        new, notes, bad = process(s, rel)
        if bad:
            problems.append(f"{rel}: {'; '.join(bad)}")
        if new != s:
            changed += 1
            if apply_:
                open(f, "w", encoding="utf-8").write(new)
                if open(f, encoding="utf-8").read() != new:
                    problems.append(f"{rel}: write did not verify")
    print(f"{'wrote' if apply_ else 'DRY RUN'}: {changed} of {len(files)} posts changed")
    print("  " + about(apply_))
    for p in problems:
        print("  !! " + p)


if __name__ == "__main__":
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)
    main("--apply" in sys.argv, only)
