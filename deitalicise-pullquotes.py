#!/usr/bin/env python3
"""deitalicise-pullquotes.py — set .pull-quote-inner roman. 20 Sept 2026.

Lenny, on the Birds of Condor page: "I really like how it's formatted with the
bigger quotes pulled out - I dont love the italics but everything else is super
solid." So: the size, the green, the oversized opening quote mark, the rule and
the mono attribution all stay. Only font-style changes.

THIS IS THE SAME CALL HE ALREADY MADE ONCE. The .cat-kicker rule carries this
comment from an earlier round:

    ROMAN, NOT ITALIC. The first pass set these 25px ITALIC, and Lenny: "I find
    this font kinda hard to read." He was right, and the typeface was not the
    problem - Editors Note Text is a display serif whose italic is fine for a
    one-line pull-quote and punishing over five or six centred lines.

Pull-quotes are exactly that second case: the Birds of Condor quote runs ten
lines at 38px. Same face, same length, same complaint, same fix.

SCOPE: the rule block, not the file. `font-style:italic` also appears in
.more-card-name, .sidebar and the drop-hero caption, all of which are correct
as they are and none of which Lenny mentioned. This rewrites the declaration
ONLY where it sits inside a `.pull-quote-inner{...}` block, found by walking to
the closing brace rather than by matching a fixed rule body - there are three
different .pull-quote-inner variants live on the site (22px, 26px, 38px) and a
literal string replace would have caught one of them.

Idempotent. Dry run by default. --revert puts the italics back.
"""
import glob, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
RULE = re.compile(r"(\.pull-quote-inner\b[^{]*\{)([^}]*)(\})")


def flip(css_body, to):
    """Swap the font-style declaration inside one rule body."""
    frm = "italic" if to == "normal" else "normal"
    return re.sub(r"font-style\s*:\s*" + frm + r"\b", "font-style:" + to, css_body)


def process(path, to, apply_):
    h = open(path, encoding="utf-8").read()
    orig = h
    n = 0

    def sub(m):
        nonlocal n
        body = flip(m.group(2), to)
        if body != m.group(2):
            n += 1
        return m.group(1) + body + m.group(3)

    h = RULE.sub(sub, h)
    if h != orig and apply_:
        open(path, "w", encoding="utf-8").write(h)
    return n, h != orig


def main():
    apply_ = "--apply" in sys.argv
    to = "italic" if "--revert" in sys.argv else "normal"
    pages = sorted(glob.glob(os.path.join(S, "drops", "*.html")) +
                   glob.glob(os.path.join(S, "guides", "*.html")) +
                   glob.glob(os.path.join(S, "brands", "*.html")) +
                   [os.path.join(S, "index.html")])

    hits = touched = 0
    for p in pages:
        n, ch = process(p, to, apply_)
        hits += n
        touched += 1 if ch else 0
    print(f"  {'set' if apply_ else 'would set'} .pull-quote-inner -> {to}")
    print(f"  {hits} rule block(s) across {touched} page(s)")

    if apply_:
        # PROVE IT. Every .pull-quote-inner rule on the site must now agree,
        # and nothing else may have lost its italics.
        bad, other = [], 0
        for p in pages:
            h = open(p, encoding="utf-8").read()
            for m in RULE.finditer(h):
                if "font-style" in m.group(2) and f"font-style:{to}" not in m.group(2):
                    bad.append(os.path.basename(p))
            # italics that are none of our business
            other += len(re.findall(r"font-style:italic", h))
        print(f"  disagreeing rules: {len(set(bad))} {sorted(set(bad))[:5]}")
        print(f"  unrelated italic declarations still present: {other}")
        if bad:
            sys.exit("! not all pull-quote rules agree")
    else:
        print("  (dry run - pass --apply, or --revert --apply to undo)")


if __name__ == "__main__":
    main()
