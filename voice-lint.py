#!/usr/bin/env python3
"""Flag the AI tics catalogued in VOICE.md across product copy and section kickers.

Usage:
    python3 voice-lint.py                    # every post since 2026-08-14
    python3 voice-lint.py drops/foo.html     # one post
    python3 voice-lint.py --all              # every drop page on the site
    python3 voice-lint.py --deck             # lint data/copy-deck.json instead

Exit code is the number of flagged passages, so it can gate a build.
"""
import re, sys, glob, json, html, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- rules

SOURCING = [
    r"\bwe (?:did|could|couldn't|can't|cannot) (?:look|find)\b",
    r"\bwe looked\b", r"\bcould find\b", r"\bwe (?:have |'ve )?covered\b",
    r"\btook the longest\b", r"\bhardest to (?:fill|find)\b",
    r"\bcurrently unavailable\b", r"\bthis (?:post|list|roundup|edit)\b",
    r"\bour index\b", r"\bon this page\b", r"\bmade the cut\b",
    r"\bearned (?:its|a) (?:slot|place|spot)\b",
]
# "worth" is banned site-wide, but not inside place names (Fort Worth, Wentworth)
WORTH = re.compile(r"(?<!fort )(?<!went )(?<!ails)(?<!wools)\bworth\b", re.I)
HEDGES = [
    r"\bgenuinely\b", r"\bessentially\b", r"\btruly\b", r"\barguably\b",
    r"\badmittedly\b", r"\bthe rare\b", r"\bquite simply\b",
]
FLIP_TAIL = [
    r"\.\s*(?:It|That|This|They|He|She)\s+(?:is|does|was|did|are|do)\s+not\.\s*$",
    r"\.\s*(?:It|That|This)\s+(?:is|was)\s*n['’]t\.\s*$",
    r"\bdoes not look like\b", r"\bdoesn['’]t look like\b",
    r"\babsolutely would not\b", r"\bnobody would blink\b",
    r"\band it is not\b", r"\bexcept it (?:is|does)n['’]t\b",
]
VERBS = set("""is are was were be been being has have had do does did make makes made
comes come came sits sit sat runs run ran looks look looked reads read wears wear wore
takes take took gets get got puts put keeps keep kept goes go went built build builds
uses use used costs cost sells sell sold cuts cut ships ship shipped feels feel felt
means mean meant works work worked lands land landed carries carry carried
interrupts interrupt hangs hang hung holds hold held stays stay stayed sends send sent
brings bring brought turns turn turned starts start started opens open opened closes close
covers cover covered runs ran begins begin began stands stand stood knows know knew
prices price priced charges charge charged milled mills mill built builds cuts cut
photographs photograph reads reading arrives arrive arrived explains explain explained
treat treats treated change changes changed decide decides decided ships wants want""".split())


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s.strip()]


def check(text, label, out):
    # kickers open with a <strong> label ("THREE · BAG, COVER, BELT") — that is a
    # label, not a sentence, so drop it before linting the prose that follows
    text = re.sub(r"^\s*<strong>.*?</strong>", "", text, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "", text)).strip()
    t = re.sub(r"\s+", " ", t)
    if not t:
        return
    hits = []
    for pat in SOURCING:
        m = re.search(pat, t, re.I)
        if m: hits.append(("sourcing-narration", m.group(0)))
    for pat in HEDGES:
        m = re.search(pat, t, re.I)
        if m: hits.append(("hedge/intensifier", m.group(0)))
    m = WORTH.search(t)
    if m: hits.append(("banned word: worth", m.group(0)))
    for pat in FLIP_TAIL:
        m = re.search(pat, t, re.I)
        if m: hits.append(("punchline-flip", m.group(0)))

    ss = sentences(t)
    if ss:
        first = ss[0]
        words = re.findall(r"[a-z']+", first.lower())
        if len(words) >= 2 and not (set(words) & VERBS):
            hits.append(("verbless-opener", first[:60]))
        last = ss[-1]
        lw = re.findall(r"[a-z']+", last.lower())
        if len(ss) >= 2 and len(lw) <= 5 and re.match(r"^(it|that|this|they)\b", last, re.I):
            hits.append(("punchline-flip", last[:50]))
        if re.search(r",\s*[^,]{2,28},\s*[^,]{2,28},\s*[^,.]{2,34}\.$", last):
            hits.append(("rule-of-three closer", last[-60:]))

    em = t.count("—") + t.count("&mdash;")
    if em > 2:
        hits.append(("em-dash pile-up", f"{em} em-dashes"))

    if hits:
        out.append((label, t, hits))


def scan_html(path, out):
    h = open(path, encoding="utf-8").read()
    slug = os.path.basename(path)
    for m in re.finditer(r'id="([^"]+)"[^>]*>.*?<div class="product-desc">(.*?)</div>', h, re.S):
        check(m.group(2), f"{slug} :: card #{m.group(1)}", out)
    for i, m in enumerate(re.finditer(r'<p class="cat-kicker">(.*?)</p>', h, re.S)):
        check(m.group(1), f"{slug} :: kicker {i+1}", out)
    w = re.search(r'class="writeup-body"[^>]*>(.*?)</div>\s*</(?:section|div)>', h, re.S) \
        or re.search(r'class="writeup-body"[^>]*>(.*?)</div>', h, re.S)
    if w:
        for i, p in enumerate(re.findall(r"<p[^>]*>(.*?)</p>", w.group(1), re.S)):
            check(p, f"{slug} :: writeup ¶{i+1}", out)


def recent():
    fs = []
    for f in glob.glob(os.path.join(ROOT, "drops", "*.html")):
        h = open(f, encoding="utf-8").read()
        m = re.search(r'datePublished"\s*:\s*"([\d-]+)', h)
        if m and m.group(1) >= "2026-08-14":
            fs.append(f)
    return sorted(fs)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    out = []
    if "--deck" in args:
        deck = json.load(open(os.path.join(ROOT, "data", "copy-deck.json"), encoding="utf-8"))
        for slug, post in deck.items():
            for cid, c in post.get("cards", {}).items():
                check(c.get("desc", ""), f"{slug} :: card #{cid}", out)
            for kid, k in post.get("kickers", {}).items():
                check(k, f"{slug} :: kicker {kid}", out)
    else:
        files = ([a for a in args if a.endswith(".html")]
                 or (sorted(glob.glob(os.path.join(ROOT, "drops", "*.html")))
                     if "--all" in args else recent()))
        for f in files:
            scan_html(f, out)

    for label, text, hits in out:
        print(f"\n\033[1m{label}\033[0m")
        for kind, ev in hits:
            print(f"   [{kind}] {ev}")
        print(f"   > {text[:190]}{'…' if len(text) > 190 else ''}")

    kinds = {}
    for _, _, hits in out:
        for k, _ in hits:
            kinds[k] = kinds.get(k, 0) + 1
    print(f"\n{'='*60}\n{len(out)} passage(s) flagged")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f"   {v:>4}  {k}")
    sys.exit(min(len(out), 250))
