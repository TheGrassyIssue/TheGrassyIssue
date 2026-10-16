#!/usr/bin/env python3
"""apply-field-guide-quotes.py — pull quotes in the Field Guide (Lenny, 16 Oct 2026: "I want to add some good quotes
into the field guide and have a good one at the top as well."). Idempotent: every block carries data-tgi="fg-quote" and is
removed and re-inserted on each run. Runs in Deploy TGI.command before stamp-field-guide-date.py.

Sourcing (checked 16 Oct 2026), Austin-first on purpose:
  * "Take dead aim." Harvey Penick, Harvey Penick's Little Red Book (1992), the chapter of the same name. Penick was the
    longtime pro at Austin Country Club and taught Ben Crenshaw and Tom Kite.
  * Willie Nelson, "It's just a place to get out and walk around outside," answering why he likes golf so much, Larry King
    Live transcript, April 16, 2010 (CNN). He has owned the Pedernales course in Spicewood since 1979.
  * Walter Hagen's "short visit" line, from The Walter Hagen Story (1956), wording as widely reproduced.
  * "I had a 15th club in my bag." Ben Crenshaw after winning the 1995 Masters, the week Penick died (wording varies slightly
    between reports; this is the most cited form).
Lee Trevino's 1-iron lightning line was left out: no primary source for the exact wording.
"""
import re
import sys

PATH = "field-guide/index.html"
CSS = ('<style data-tgi="fg-quote">.fgq{max-width:920px;margin:0 auto;padding:46px 32px 40px;text-align:center}'
       '.fgq blockquote{margin:0;font-family:var(--serif,Georgia,serif);font-style:italic;font-weight:400;color:var(--grass,#2D4A2B);'
       'font-size:clamp(26px,3.2vw,38px);line-height:1.22;letter-spacing:-.01em}'
       '.fgq cite{display:block;margin-top:16px;font-family:var(--mono,monospace);font-style:normal;font-size:10.5px;letter-spacing:.16em;'
       'text-transform:uppercase;color:var(--ink,#141414);opacity:.55;line-height:1.6}'
       '.fgq-top{padding:54px 32px 50px;border-bottom:.5px solid var(--ink,#141414)}'
       '.fgq-top blockquote{font-size:clamp(44px,7vw,84px);line-height:1}'
       '.fgq-rule{width:56px;height:1px;background:var(--grass,#2D4A2B);opacity:.5;margin:0 auto 22px}'
       '@media(max-width:640px){.fgq{padding:34px 20px 30px}.fgq-top{padding:40px 20px 36px}}</style>\n')
Q = [
 # (anchor to insert BEFORE, quote, attribution, top?) — one quote per person (Lenny, 16 Oct 2026: "lets not repeat people")
 ('<figure class="muni-photo"', "Take dead aim.",
  "Harvey Penick, longtime pro at Austin Country Club, who taught Ben Crenshaw and Tom Kite &middot; Harvey Penick&rsquo;s Little Red Book, 1992", True),
 ('<section class="index" id="munis">', "You&rsquo;re only here for a short visit. Don&rsquo;t hurry, don&rsquo;t worry. And be sure to smell the flowers along the way.",
  "Walter Hagen &middot; The Walter Hagen Story, 1956", False),
 ('<section class="guide-section" id="events">', "I had a 15th club in my bag.",
  "Ben Crenshaw, Austin&rsquo;s own, after winning the 1995 Masters the week Harvey Penick died", False),
 ('<section class="guide-section" id="day-trips">', "It&rsquo;s just a place to get out and walk around outside.",
  "Willie Nelson, asked why he loves golf, 2010 &middot; he owns the Pedernales Cut-N-Putt in Spicewood", False),
]


def block(q, a, top):
    cls = "fgq fgq-top" if top else "fgq"
    rule = "" if top else '<div class="fgq-rule"></div>'
    return (f'<div class="{cls}" data-tgi="fg-quote">{rule}<blockquote>&ldquo;{q}&rdquo;</blockquote>'
            f'<cite>&mdash; {a}</cite></div>\n')


def main(apply_):
    s0 = open(PATH, encoding="utf-8").read()
    s = re.sub(r'<style data-tgi="fg-quote">.*?</style>\n?', "", s0, flags=re.S)
    s = re.sub(r'<div class="fgq[^"]*" data-tgi="fg-quote">.*?</div>\n', "", s, flags=re.S)
    for anchor, q, a, top in Q:
        i = s.find(anchor)
        if i < 0:
            sys.exit(f"! anchor not found: {anchor}")
        s = s[:i] + block(q, a, top) + s[i:]
    j = s.rindex("</head>")
    s = s[:j] + CSS + s[j:]
    if re.search(r"\bworth\b", " ".join(x[1] + x[2] for x in Q), re.I):
        sys.exit("! banned word")
    print(f"apply-field-guide-quotes: {'updated' if s != s0 else 'unchanged'} ({len(Q)} quotes)")
    if apply_ and s != s0:
        open(PATH, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main("--apply" in sys.argv)
