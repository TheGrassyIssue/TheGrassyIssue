#!/usr/bin/env python3
"""
lifestyle-lines.py — one distinct line of wording per slide, EXTRACTED from the post.
17 September 2026.

WHY THIS EXISTS
---------------
Lenny: "each image needs wording."

The first version of lifestyle-slides.py passed the post title to every slide, so
all twelve Manors frames carried the identical headline. Twelve photographs, one
sentence, repeated. That is the bug this module fixes.

EXTRACTION, NOT WRITING — AND WHY THAT IS THE WHOLE POINT
---------------------------------------------------------
Every line here is lifted verbatim from the post it belongs to. Nothing is
composed, paraphrased or "adapted". This follows the same rule as hook() in
export-ig.py, and it exists because these slides are published under TGI's name:
a line invented by a script is a claim nobody checked.

The deliberate consequence is that lines are ABOUT THE COLLECTION, not about the
specific garment in frame. We do not know which product appears in which campaign
photograph — the manifests record where a frame came from, not what is in it. So
"Merino Tech Hoodie - $310" over an unidentified photograph would be a guess with
a price attached, and if wrong it is a wrong price on a public post. Section
headings and editorial sentences are true of the collection no matter which frame
they sit on, which is why they are what this returns.

THE FOUR SOURCES, in the order they are used
--------------------------------------------
    1. h2 headings   the post's editorial spine — "What the Fabrics Actually Do"
    2. FAQ questions the curiosity hooks        — "What is a condor in golf?"
    3. blockquotes   verbatim sourced quotes
    4. body lines    short complete sentences   — "Curtis Strange became a customer"

Headings and questions come first because both are written to be read on their
own. Prose comes last and is filtered hardest, because a sentence lifted out of
its paragraph is the most likely thing here to stop making sense.

RUNNING OUT IS ALLOWED. If a post yields fewer lines than there are photographs,
the carousel gets shorter — it does not repeat a line to pad the count, because
a repeated line is the bug we came here to fix.
"""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent

# Instagram takes at most 20 items in a carousel. 18 photographs plus an end card
# leaves one spare and keeps us inside that limit without arithmetic at the edge.
MAX_SLIDES = 18

MAXLEN = 52          # longer than this wraps past three lines in the condensed face
MINLEN = 14

# A HEADLINE HAS TO STAND ON ITS OWN, and most prose sentences do not.
# "Most of it is not." and "Neither club exists." are fine in a paragraph, where
# the previous sentence said what "it" and "club" were. Alone over a photograph
# they are baffling. Anything opening with a backward-pointing word is therefore
# refused rather than cleaned up, because the referent it needs is in a sentence
# we are not showing.
_ANAPHORIC = re.compile(
    r"^(it|its|they|their|them|that|this|those|these|both|neither|either|"
    r"most|some|each|all|one|none|he|she|his|her|we|our|us|"
    r"and|but|so|then|there|here|which|who|also|too|instead)\b", re.I)

# A sentence split on ". " can end mid-abbreviation: "…in our Off Course Vol. 2"
# becomes "…in our Off Course Vol", which reads as a typo on a published slide.
_TRUNCATED = re.compile(r"\b(vol|no|st|mr|mrs|dr|ave|rd|inc|ltd|co|jr|sr|vs|approx|est)$", re.I)

# Structural labels. They are real h2s, but they name a part of a web page rather
# than saying anything — "The Questions" over a clifftop photograph is furniture.
_FURNITURE = {"the questions", "faq", "faqs", "more from the feed", "the lineup",
              "frequently asked questions", "frequently asked",
              "in his words", "in her words", "in the wild",
              "the details", "notes", "sources", "related", "the answers"}

# "The Story — FAQ" and "Frequently Asked" are headings for a page section, and on
# a photograph they read as a stray label rather than a line. Matching the word
# anywhere catches the compound forms the exact-match set above misses.
_FURNITURE_RE = re.compile(r"\bfaqs?\b|\bfrequently asked\b|\bmore from\b", re.I)


# Lenny: "give me detail about the brand/product/drop itself instead of using the
# FAQ questions." A line earns its place on a slide by carrying something
# concrete — a price, a material, a place, a date, a method. This scores that,
# and everything below the threshold is left out rather than used as filler.
_MATERIAL = re.compile(
    r"\b(merino|tweed|wool|leather|nylon|cotton|cordura|primaloft|dyneema|"
    r"ripstop|canvas|suede|brass|steel|aluminium|aluminum|milled|forged|"
    r"cashmere|linen|denim|sherpa|fleece|polyester|waxed|tartan|felt)\b", re.I)
_MADE = re.compile(
    r"\b(made|built|cut|sewn|woven|stitched|founded|launched|started|opened|"
    r"lined|dyed|printed)\b", re.I)


def _detail_score(s):
    n = 0
    if re.search(r"[$£€]\s?\d", s):          # a price is the hardest detail there is
        n += 3
    if re.search(r"\b\d{2,}\b", s):          # a count, a year, a measurement
        n += 2
    if _MATERIAL.search(s):
        n += 3
    if _MADE.search(s):
        n += 2
    if re.findall(r"\b[A-Z][a-z]{2,}", s):   # a named place, mill, person or model
        n += 1
    return n


def _txt(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _ok(s, strict=False, heading=False):
    # A lowercase opening means the split landed mid-sentence: "collaboration bags
    # run $850 to $1,100" is the tail of a longer sentence, not a line.
    if not s[:1].isupper():
        return False
    if " " not in s or len(s) > MAXLEN:
        return False
    if re.fullmatch(r"[^a-zA-Z]*", s):
        return False
    if s.lower().strip(" .—-") in _FURNITURE or _FURNITURE_RE.search(s):
        return False
    # Headings are already written to be read alone, so short ones are good
    # headlines — "On Course", "The Hats". Prose needs more to stand up.
    if heading:
        if len(s) < 8:
            return False
    else:
        if len(s) < MINLEN or len(s.split()) < 3:
            return False
    if not strict:
        return True
    # strict mode is for prose pulled out of its paragraph
    if _ANAPHORIC.match(s) or _TRUNCATED.search(s):
        return False
    # a self-contained line almost always carries something specific — a name,
    # a number or a price. Without one it is usually a linking sentence.
    if not re.search(r"\d|\$|£|[A-Z][a-z]{2,}", s[1:]):
        return False
    return True


def lines_for(post_slug, limit=MAX_SLIDES):
    """Distinct verbatim lines for one post, best-first, never padded."""
    p = ROOT / "drops" / (post_slug + ".html")
    if not p.exists():
        return []
    h = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"<(script|style|nav|footer|head)[^>]*>.*?</\1>", "", h,
                  flags=re.S | re.I)

    out, seen = [], set()

    def push(s, strict=False, heading=False):
        s = s.rstrip(" .")
        if not _ok(s, strict, heading):
            return
        k = re.sub(r"[^a-z0-9]", "", s.lower())
        if k in seen:
            return
        seen.add(k)
        out.append(s)

    # 1. the editorial spine — section headings, which name the thing being shown
    #    ("The Headcovers — Harris Tweed", "Made in Scotland, and Specifically
    #    Where"). These are product detail, not page furniture.
    for x in re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.S):
        push(_txt(x), heading=True)

    # 2. anything quoted verbatim from a named person
    for x in re.findall(r"<blockquote[^>]*>(.*?)</blockquote>", body, re.S):
        push(_txt(x))

    # 3. the detail lines — prose carrying something concrete about the brand,
    #    the product or the drop, best-first. FAQ QUESTIONS ARE DELIBERATELY NOT
    #    A SOURCE: "Who founded Fyfe Golf?" is a hook, not information, and a
    #    carousel of questions tells a reader nothing about what they are
    #    looking at.
    detail = []
    for para in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
        for s in re.split(r"(?<=[.!?])\s+", _txt(para)):
            s = s.strip().rstrip(" .")
            if not s or not s[:1].isupper() or len(s.split()) < 4:
                continue
            sc = _detail_score(s)
            if sc >= 2:
                detail.append((sc, s))
    for sc, s in sorted(detail, key=lambda x: -x[0]):
        push(s, strict=True)

    return out[:limit]


if __name__ == "__main__":
    POSTS = {
        "manors": "manors-golf-aw26-collection",
        "fyfe-golf": "brand-to-know-fyfe-golf",
        "birds-of-condor": "brand-to-know-birds-of-condor",
        "hidden-links-society": "brand-to-know-hidden-links-society",
        "takomo": "brand-to-know-takomo-golf",
        "apres-golf": "brand-to-know-apres-golf",
        "gamut-golf": "brand-to-know-gamut-golf",
        "bluegrass-fairway": "brand-to-know-bluegrass-fairway",
    }
    for slug, post in POSTS.items():
        L = lines_for(post)
        print(f"\n=== {slug} — {len(L)} lines")
        for i, l in enumerate(L, 1):
            print(f"  {i:2d}. {l}")
