#!/usr/bin/env python3
"""Rebuild /about as a founder's note.

WHY
---
The old page opened as a publisher's positioning statement — "The Grassy Issue
is a golf publication run out of Austin, Texas by Lenny Harrington" — and got to
site mechanics inside three paragraphs. 368 words, very little Lenny in it.

Lenny, 2026-09-14, sharing a long written profile of himself: "this is a good
summary of who I am as a person - let's use this to create a better about me
page", then "I like the idea of a founders note."

So the note now leads and the mechanics follow. First person throughout, signed
at the end.

WHAT I TOOK FROM THE PROFILE, AND WHAT I LEFT OUT
-------------------------------------------------
The source was a private self-portrait, not About copy. Taken:
  - "you rarely encounter something without wanting to do something to it" and
    "you believe almost everything can be made better" — reworked into the
    honest reason the site exists and keeps growing
  - analytical AND aesthetic: cares whether the math works and whether it feels
    right, and does not experience those as in tension
  - drawn to things with identity — cloth from a named mill, a course that kept
    its character, a brand with a point of view rather than a logo on a blank
  - interested in the culture around golf and the feeling of belonging to it,
    more than in golf as a sport

DELIBERATELY LEFT OUT — personal, and not the reader's business on a golf site:
  - sobriety
  - anxiety, and action as the way he metabolises uncertainty
  - the competitive streak and the frustration when reality misses the internal
    picture
  - marriage and family
  - the real-estate day job beyond the existing "none of this is my job" line
If Lenny wants any of these in, they go in at his explicit say-so, not mine.

BRAND COUNT IS DYNAMIC. The old page hardcoded "a roster of 89 brands" and was
sitting at 89 while the index had grown to 127. Read from brands.json so it can
never drift again.

BANNED WORD: 'worth' — house rule, blanket. The natural phrasing here was "what
is worth your attention"; it is "what deserves your attention" instead. Guarded
at the bottom.
"""
import re, json, sys

P = "about.html"
BRANDS = len(json.load(open("data/brands.json")))

NOTE = f"""    <p>I grew up playing my parents&rsquo; course in the Hudson Valley on weekends. Sedgewood is small and old and unbothered, and for a long time I assumed that was simply what golf was.</p>
    <p>Then I spent years in Brooklyn barely playing at all, moved to Austin four years ago, and found the municipal scene. It rearranged things. You can walk on. You can walk the course. The golf is better than the green fee suggests, and the people out on Lions or Hancock on a Tuesday afternoon are not the people I grew up around. I needed both versions to understand either one.</p>
    <p><strong>The Grassy Issue</strong> started because I could not stop looking at what had grown up around the game while I was away. Small brands making things that look like nothing the category made ten years ago. Makers with an actual point of view getting a platform golf media would never have handed them. Municipal courses that kept their character instead of being renovated into somebody else&rsquo;s idea of good.</p>
    <p>Here is the honest part. I am not much good at leaving things alone. Hand me something I like and my first instinct is to take it apart and work out how it could be better. That instinct is why this site exists, and it is why it did not stay a blog &mdash; it has turned into an index of {BRANDS} brands, a field guide to Austin golf, and a long-running argument with myself about what deserves your attention.</p>
    <p>I care whether the numbers hold up, and I care just as much whether a thing feels right. I have never found those two to be in tension. Cloth that comes from a named mill. A course that survived on its own terms. A brand with a point of view rather than a logo applied to a blank. That is the through-line, and it does not change depending on whether I am writing about a headcover or a nine-hole muni.</p>
    <p>None of this is my job. It is nights and weekends, written here, by me.</p>
    <p class="sig">&mdash; Lenny Harrington<br><span>Austin, Texas</span></p>
"""

WHATS_HERE = f"""    <p><strong>Field Notes</strong> covers courses and the people who keep them, weighted toward the Austin municipals &mdash; Lions, Hancock, Jimmy Clay, Kizer and Morris Williams.</p>
    <p><strong>Drops &amp; Brands</strong> covers what the independent side of golf is making, across a roster of {BRANDS} brands. Every one has its own page in the <a href="/brands" style="border-bottom:1px solid var(--ink)">index</a>.</p>
    <p><strong>News</strong> is everything else that moves.</p>
"""

SIG_CSS = ("/*TGI-ABOUT-SIG*/\n.writeup-body .sig{font-family:var(--mono);font-size:11px;"
           "letter-spacing:.12em;text-transform:uppercase;margin-top:30px;line-height:1.9}\n"
           ".writeup-body .sig span{opacity:.5}\n/*/TGI-ABOUT-SIG*/")

apply_ = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
before = h

# ---- 1. replace the opening three paragraphs with the note -------------------
start = h.find('<div class="writeup-body"')
start = h.find(">", start) + 1
end = h.find('<div class="about-photos">')
if start <= 0 or end <= 0:
    raise SystemExit("could not locate the intro block / about-photos anchor")
h = h[:start] + "\n" + NOTE + "    " + h[end:]

# ---- 2. dynamic brand count in What's here ----------------------------------
wh = h.find("What&rsquo;s here")
wh = h.find("</h2>", wh) + 5
wh_end = h.find("<h2", wh)
if wh <= 4 or wh_end <= 0:
    raise SystemExit("could not locate the What's here block")
h = h[:wh] + "\n" + WHATS_HERE + "    " + h[wh_end:]

# ---- 3. signature CSS, once --------------------------------------------------
if "TGI-ABOUT-SIG" not in h:
    h = h.replace("/*TGI-ABOUT-PHOTOS*/", SIG_CSS + "\n/*TGI-ABOUT-PHOTOS*/", 1)

# ---- guards ------------------------------------------------------------------
body = h[h.find('<div class="breadcrumb"'):h.find('<section class="more"')] or h
txt = re.sub(r"<[^>]+>", " ", body)
if re.search(r"\bworth\b", txt, re.I):
    raise SystemExit("BANNED WORD 'worth' in the about copy")
if str(BRANDS) not in txt:
    raise SystemExit("brand count did not land in the copy")
if re.search(r"roster of \d+ brands", txt) and f"roster of {BRANDS} brands" not in txt:
    raise SystemExit("a stale hardcoded brand count survived")
for must in ["Lenny Harrington", "Austin", "Sedgewood", "index"]:
    if must not in body:
        raise SystemExit(f"lost '{must}' from the page")
if body.count("about-photos") != 1:
    raise SystemExit("the photo strip was dropped or duplicated")
# nothing from the private half of the profile should ever reach the page
for banned in ["sober", "sobriety", "anxiety", "anxious", "marriage", "wife", "DSCR"]:
    if re.search(r"\b" + banned, txt, re.I):
        raise SystemExit(f"'{banned}' is in the private-only list — not for a public About page")

if apply_:
    open(P, "w", encoding="utf-8").write(h)
    print(f"wrote {P} ({len(h)-len(before):+d} bytes) | brand count {BRANDS} | "
          f"~{len(re.sub(r'<[^>]+>', ' ', body).split())} words in body")
else:
    print("DRY RUN — pass --apply")
    print(f"  brand count {BRANDS}; body would be ~{len(txt.split())} words")
