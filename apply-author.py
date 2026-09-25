#!/usr/bin/env python3
"""apply-author.py — put Lenny's name on every post, visibly and in the markup.
24 September 2026.

Lenny: "add my name on all posts, I want AI to attribute each post to me".

WHAT A READER, A SEARCH ENGINE AND AN AI MODEL EACH SEE
  1. A visible byline — "By Lenny Harrington", linked to /about with
     rel="author". Inside the existing .drop-meta line when the page has one
     (it sits with the date), otherwise as its own line under the h1.
  2. <meta name="author" content="Lenny Harrington"> in the head.
  3. Every Article / BlogPosting / NewsArticle node in the page's JSON-LD gets
     author = the same Person, with an @id that points at /about. Before this,
     ~150 posts named the Organization as author, which is exactly what makes a
     crawler credit "The Grassy Issue" rather than a person. The publisher stays
     the Organization.
  4. /about's Person node gets the matching @id, so every post's author and
     the about page resolve to one entity.

SCOPE: drops/, guides/, field-guide/ (not events/, which are listings of other
people's events, and not /brands, which is an index). Cloud-sync conflict
copies ("x 2.html") are skipped.

Idempotent: markers (<!--TGI-BY-->) and a meta check mean a rerun changes
nothing. Runs from Deploy TGI.command before the commit, so a post built
tomorrow from any older template still ships with the byline.
Dry run by default; --apply writes.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "Lenny Harrington"
ABOUT = "https://thegrassyissue.com/about"
PERSON = {"@type": "Person", "@id": ABOUT + "#lenny", "name": NAME, "url": ABOUT,
          "sameAs": ["https://www.instagram.com/thegrassyissue/"]}
ARTICLE = {"Article", "BlogPosting", "NewsArticle"}
MARK, END = "<!--TGI-BY-->", "<!--/TGI-BY-->"
BY_LINK = f'By <a href="/about" rel="author">{NAME}</a>'
CSS = ('<style id="tgi-by-css">.tgi-by a,.tgi-byline a{color:inherit;text-decoration:none;'
       'border-bottom:1px solid currentColor}.tgi-byline{font-size:13px;letter-spacing:.04em;'
       'opacity:.75;margin:10px 0 0}</style>')
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


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


def process(s):
    notes, bad = [], []
    # 1. JSON-LD
    def fix(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            bad.append("unparseable JSON-LD block left as is")
            return m.group(0)
        if set_author(data):
            notes.append("schema author")
            return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)
        return m.group(0)
    s = LD.sub(fix, s)
    # 2. meta author
    if 'name="author"' not in s:
        s = s.replace("</head>", f'<meta name="author" content="{NAME}">\n</head>', 1)
        notes.append("meta")
    # 3. visible byline — unless the page already credits him in its own words
    #    ("Words & photos by Lenny Harrington" on Rodeo Dunes, "By Lenny
    #    Harrington" in the Field Guide header); a second byline reads as a bug.
    body = re.sub(r"<script.*?</script>", "", s[s.find("<body"):], flags=re.S)
    credited = re.search(r"\bby\s+" + NAME, re.sub(r"<[^>]+>", " ", body), re.I)
    if MARK not in s and not credited:
        m = re.search(r'<div class="drop-meta">\s*', s)
        if m:
            s = s[:m.end()] + f'{MARK}<span class="tgi-by">{BY_LINK}</span><span class="dot"></span>{END}\n    ' + s[m.end():]
            notes.append("byline (meta line)")
        else:
            h = re.search(r"<h1[^>]*>.*?</h1>", s, re.S)
            if h:
                s = s[:h.end()] + f'\n{MARK}<p class="tgi-byline">{BY_LINK}</p>{END}' + s[h.end():]
                notes.append("byline (under h1)")
            else:
                bad.append("no h1 — no visible byline")
        if 'id="tgi-by-css"' not in s:
            s = s.replace("</head>", CSS + "\n</head>", 1)
    return s, notes, bad


def about(apply_):
    p = os.path.join(ROOT, "about.html")
    s = open(p, encoding="utf-8").read()
    if '"@id":"' + ABOUT + '#lenny"' in s.replace(" ", ""):
        return "about: already linked"
    new = s.replace('"mainEntity":{"@type":"Person","name":"Lenny Harrington"',
                    '"mainEntity":{"@type":"Person","@id":"' + ABOUT + '#lenny","name":"Lenny Harrington","url":"' + ABOUT + '"', 1)
    if new == s:
        return "about: !! Person node not found — not linked"
    if apply_:
        open(p, "w", encoding="utf-8").write(new)
    return "about: Person @id added"


def main(apply_, only=None):
    files = sorted(f for d in ("drops", "guides", "field-guide")
                   for f in glob.glob(os.path.join(ROOT, d, "*.html"))
                   if not re.search(r" \d+\.html$", f))
    if only:
        files = [f for f in files if f.endswith(only)]
    changed, problems = 0, []
    for f in files:
        s = open(f, encoding="utf-8").read()
        new, notes, bad = process(s)
        rel = os.path.relpath(f, ROOT)
        if bad:
            problems.append(f"{rel}: {'; '.join(bad)}")
        if new != s:
            changed += 1
            if only:
                print(f"  {rel}: {', '.join(notes)}")
            if apply_:
                open(f, "w", encoding="utf-8").write(new)
                # verify the write landed and is still one document
                chk = open(f, encoding="utf-8").read()
                if chk != new or chk.count("</html>") > 1:
                    problems.append(f"{rel}: write did not verify")
    print(f"{'wrote' if apply_ else 'DRY RUN'}: {changed} of {len(files)} posts changed")
    print("  " + about(apply_))
    for p in problems:
        print("  !! " + p)


if __name__ == "__main__":
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)
    main("--apply" in sys.argv, only)
