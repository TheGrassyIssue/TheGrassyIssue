#!/usr/bin/env python3
"""fix-meta.py — rewrite <title> and meta descriptions on the pages that already
earn search impressions. 21 September 2026.

WHY. Search Console, 20 Jun – 19 Sep 2026: average position 8, CTR 1.1%. A site
sitting at position 8 normally earns 2–3%, so between a half and two thirds of
the clicks the ranking already deserves are being thrown away at the result
itself. The cause is measurable and dull: every title on these pages ran 66–118
characters and every description 153–304, against display limits of roughly 60
and 160. Google was cutting both mid-phrase, and rewriting the titles it did not
like. The proof sits in the same report — the one page with a 60-character title,
/drops/best-golf-streetwear-brands-2026, converts at 4.8%, four times site
average.

THE COPY LIVES IN data/meta-overrides.json, NOT IN THIS FILE. That separation is
the point: the JSON is reviewable as prose, and re-running this script after any
page rebuild puts the copy back. Post builders write their own <title>, so a
rebuild of any one post would otherwise silently undo this — the same class of
bug as hand-editing post-thumbs.json or the /brands index.

SIX PLACES PER PAGE, NOT ONE. Each page carries <title>, meta description,
og:title, og:description, twitter:title and twitter:description, plus a
"headline" in its JSON-LD. Updating only <title> leaves five stale copies of the
old wording behind, and the social cards then disagree with the search result.
All of them get the same new string — one rule, no special cases. The site-name
suffix is dropped everywhere for the same reason it was dropped from the title:
Google prints the site name on its own line, and a shared card already shows the
domain. index.html is the exception and keeps "The Grassy Issue" inside its own
title, because that is the page Google derives the site name from.

ESCAPING IS NOT OPTIONAL HERE. Two of these titles contain a literal ampersand
("Cloud & Wind Golf", "Gumtree Golf & Nature Club"). Written raw into an
attribute they produce invalid markup that parsers silently repair in different
ways. Titles and attribute values are escaped; the JSON-LD value is JSON-escaped
instead, because it sits inside a script element where &amp; would be literal.

PROVE ONE, THEN BATCH: `--one <path>` does a single page. House rule.

Idempotent. Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OVERRIDES = ROOT / "data/meta-overrides.json"
MAXT, MIND, MAXD = 60, 120, 160


def load():
    raw = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


# Rough per-character widths for Google's ~18px desktop result font. Nothing
# here is precise — the point is only that "i" and "W" are not the same width,
# which is exactly what a character count pretends. Used to sanity-check titles
# that run over 60 characters, never to approve one automatically.
_NARROW, _WIDE = set("ijltfIrí'!.,:;|[]()"), set("mwMW@%—")


def px(s, base=8.4):
    return sum(base * (0.45 if c in _NARROW else 1.55 if c in _WIDE
                       else 1.25 if c.isupper() else 1.0) for c in s)


def esc(s):
    """Escape for a double-quoted attribute — and nothing more.

    html.escape(quote=True) also turns every apostrophe into &#x27;. That is
    valid, and it is wrong here: an apostrophe needs no escaping inside a
    double-quoted attribute, and 74 untouched pages on this site carry literal
    apostrophes in their descriptions while not one carries the entity. Using
    html.escape made the pages this script touched the odd ones out, visible in
    any diff and in anything that reads the raw attribute.
    """
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def rewrite(h, title, desc):
    """Return (html, number_of_fields_changed)."""
    t_esc, d_esc = esc(title), esc(desc)
    n = 0

    def sub(pattern, repl):
        nonlocal h, n
        h2, k = re.subn(pattern, lambda m: repl, h, count=1)
        if k:
            h = h2
            n += 1
        return k

    sub(r"<title>.*?</title>", f"<title>{t_esc}</title>")
    sub(r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{d_esc}"')
    sub(r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{t_esc}"')
    sub(r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{d_esc}"')
    sub(r'<meta name="twitter:title" content="[^"]*"',
        f'<meta name="twitter:title" content="{t_esc}"')
    sub(r'<meta name="twitter:description" content="[^"]*"',
        f'<meta name="twitter:description" content="{d_esc}"')
    # JSON-LD headline: JSON string context, so json-escape rather than html-escape
    sub(r'"headline"\s*:\s*"(?:[^"\\]|\\.)*"',
        '"headline": ' + json.dumps(title, ensure_ascii=False))
    return h, n


def check_copy(page, title, desc, bad, warn, kept):
    if len(title) > MAXT:
        # A "_keep" note means Lenny chose this wording deliberately. The 60-char
        # figure is a rule of thumb standing in for the real limit, which is
        # about 580 PIXELS — so a title of narrow letters can run a few
        # characters over and still fit. Warn, show the estimate, and let it
        # through rather than overruling an editorial decision on a proxy.
        (warn if kept else bad).append(
            f"{page}: title is {len(title)} chars"
            + (f" (~{px(title):.0f}px of ~580)" if kept else f", limit {MAXT}"))
    if not MIND <= len(desc) <= MAXD:
        bad.append(f"{page}: description is {len(desc)} chars, want {MIND}-{MAXD}")
    # house rules. "Fort Worth" is the one legitimate use of the banned word.
    for s, what in ((title, "title"), (desc, "description")):
        if re.search(r"\bworth\b", re.sub(r"fort worth", "", s, flags=re.I), re.I):
            bad.append(f"{page}: banned word in {what}")


def main(apply_, only):
    ov = load()
    bad, warn = [], []
    for page, v in ov.items():
        check_copy(page, v["title"], v["description"], bad, warn, "_keep" in v)
        if not (ROOT / page).is_file():
            bad.append(f"{page}: no such file")
    # a duplicate title or description across pages is its own ranking problem
    for field in ("title", "description"):
        seen = {}
        for page, v in ov.items():
            seen.setdefault(v[field], []).append(page)
        for val, pages in seen.items():
            if len(pages) > 1:
                bad.append(f"duplicate {field} on {', '.join(pages)}")
    if bad:
        sys.exit("! the copy itself is wrong, nothing written:\n    " + "\n    ".join(bad))
    if warn:
        print("  note — kept by choice, over the 60-char guideline:")
        for w in warn:
            print(f"     {w}")

    todo = {only: ov[only]} if only else ov
    if only and only not in ov:
        sys.exit(f"! {only} is not in meta-overrides.json")

    touched, fields = [], 0
    for page, v in todo.items():
        p = ROOT / page
        h = p.read_text(encoding="utf-8")
        h2, n = rewrite(h, v["title"], v["description"])
        fields += n
        if h2 != h:
            touched.append((page, n))
            if apply_:
                p.write_text(h2, encoding="utf-8")

    print(f"  {len(todo)} page(s) targeted, {len(touched)} changed, {fields} fields rewritten")
    for page, n in touched[:6]:
        print(f"     {page}  ({n} fields)")
    if len(touched) > 6:
        print(f"     ... and {len(touched) - 6} more")
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY THE FILES ON DISK, NOT THE STRINGS THAT WENT IN ----
    # The whole reason this script exists is that nobody checked what the reader
    # actually loaded. Read it back.
    problems = []
    for page, v in todo.items():
        h = (ROOT / page).read_text(encoding="utf-8")
        head = h[:h.find("</head>")]
        titles = re.findall(r"<title>(.*?)</title>", head, re.S)
        if len(titles) != 1:
            problems.append(f"{page}: {len(titles)} <title> elements in head")
        elif html.unescape(titles[0]) != v["title"]:
            problems.append(f"{page}: title on disk is {html.unescape(titles[0])!r}")
        for attr, pat, want in (
            ("description", r'<meta name="description" content="([^"]*)"', v["description"]),
            ("og:title", r'<meta property="og:title" content="([^"]*)"', v["title"]),
            ("og:description", r'<meta property="og:description" content="([^"]*)"', v["description"]),
            ("twitter:title", r'<meta name="twitter:title" content="([^"]*)"', v["title"]),
            ("twitter:description", r'<meta name="twitter:description" content="([^"]*)"', v["description"]),
        ):
            m = re.search(pat, head)
            if m and html.unescape(m.group(1)) != want:
                problems.append(f"{page}: {attr} still reads {html.unescape(m.group(1))[:60]!r}")
        # the old site-name suffix must not survive anywhere in the head
        if page != "index.html" and "— The Grassy Issue<" in head:
            problems.append(f"{page}: the old site-name suffix survives in <title>")
        # A raw ampersand in an attribute is the escaping bug this guards
        # against. THE FIRST VERSION OF THIS PATTERN WAS ITSELF THE BUG: it
        # allowed decimal entities (&#39;) but not HEX ones (&#x27;), so it
        # failed 12 pages whose markup was perfectly valid and reported an
        # escaping error that did not exist. Hex entities are allowed now.
        for m in re.finditer(r'content="([^"]*)"', head):
            if re.search(r"&(?!amp;|quot;|lt;|gt;|#\d+;|#x[0-9a-fA-F]+;|[a-zA-Z]+;)",
                         m.group(1)):
                problems.append(f"{page}: unescaped & in a meta attribute")
                break
    if problems:
        sys.exit("! verification failed:\n    " + "\n    ".join(problems))

    # Say what was actually checked. An earlier version of this line claimed
    # "titles <= 60 chars" even when two were deliberately over — a success
    # message asserting something it had not verified, which is the same defect
    # this whole script exists to correct.
    over = sum(1 for v in todo.values() if len(v["title"]) > MAXT)
    print(f"\n  verified on disk: {len(todo)} page(s), descriptions {MIND}-{MAXD} chars, "
          f"all six fields agree, nothing unescaped\n"
          f"  titles: {len(todo) - over} within {MAXT} chars"
          + (f", {over} deliberately over (see _keep)" if over else ""))


if __name__ == "__main__":
    a = sys.argv[1:]
    main("--apply" in a, a[a.index("--one") + 1] if "--one" in a else None)
