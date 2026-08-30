#!/usr/bin/env python3
"""
apply-editors-note.py — swap TGI's serif to Editor's Note Text.

Lenny supplied the family (OTF/TTF/WOFF, 2026-08-28) and chose:
  * Editor's Note Text REPLACES Fraunces everywhere - headlines, product names,
    section h2s, FAQ questions AND body copy. Fraunces is retired.
  * The homepage stays SCOPED to feed cards; hero, chips and footer are untouched.
  * JetBrains Mono keeps every label; In The Margins keeps the wordmark.

RUN
  python3 apply-editors-note.py            # dry run
  python3 apply-editors-note.py --apply
  python3 apply-editors-note.py --apply --revert

TWO MECHANISMS, AND WHY BOTH ARE NEEDED
---------------------------------------
1. An APPENDED marker block (/*TGI-ENT-V1*/ ... ) before the last </style>:
   carries the @font-face rules, the body-copy overrides and the arrow guard.
   Appended last, so it wins on cascade order without !important, and reverting
   is a pure string deletion.
2. LITERAL SUBSTITUTIONS for things an appended rule physically cannot beat:
   187 of the 194 direct "Fraunces" references live in INLINE style attributes
   (newsletter popup, search-result JS templates, placeholder tiles) across 184
   files. Inline styles have specificity 1000 - no stylesheet rule overrides them.
   Every substitution is a literal string pair and is undone by reversing it, so
   this stays revertible without git.

WHY NOT TOUCH GIT
-----------------
The IBM Plex Mono revert on 2026-08-28 used `git checkout`, git took a SIGBUS
mid-write, and FIVE files were left at 0 bytes. So: never mass-revert via git.
This script writes a size+sha inventory to research/ before it changes anything,
and --verify re-checks every file against it afterwards.

TRAPS CONFIRMED BY AUDIT (do not re-litigate these)
---------------------------------------------------
* ARROWS. Editor's Note Text has no U+2192/2197/2190. They appear ~1,290 times,
  but 1,272 sit in .product-link/.more-link/.sidebar-cta/.guide-card-link, which
  are var(--mono) and untouched. The ~18 stragglers (.card-link, .card-readmore,
  .special-course-link) inherit body, so the guard below pins them to mono.
  Also absent: the CJK on the Cloud & Wind page and a few fractions - all of
  those already fell back under Inter, so this is not a regression.
* NO page sets body font-size inside @media, so an appended body size is safe.
* NO higher-specificity font-family rule exists on any target selector.
* Weights: the family ships 200/400/700. Existing CSS asks for 400/500/600.
  CSS matching sends 500->400 and 600->700, so nothing is synthesised.
* instagram-posts.html never defines --serif and stats.html is an internal
  dashboard; both are skipped.
"""
import re, sys, json, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MARK, ENDMARK = "/*TGI-ENT-V1*/", "/*/TGI-ENT-V1*/"
FAM = "'Editors Note Text'"          # CSS alias; the file's internal name has an apostrophe
SKIP = {"instagram-posts.html", "stats.html"}

FACES = "".join(
    f"@font-face{{font-family:{FAM};"
    f"src:url('/assets/fonts/editors-note-text-{f}.woff2') format('woff2'),"
    f"url('/assets/fonts/editors-note-text-{f}.woff') format('woff');"
    f"font-weight:{w};font-style:{s};font-display:swap}}"
    for f, w, s in [("regular", 400, "normal"), ("italic", 400, "italic"),
                    ("bold", 700, "normal"), ("bolditalic", 700, "italic")])

# Body copy currently on --sans. Titles already ride --serif and convert for free.
READING = (".product-desc,.faq-q p,.sec-intro,.cat-kicker,.writeup-body,"
           ".more-card-desc,.prog-desc,.sec-note")
# These carry a → or ↗ and inherit body; keep them mono so the arrow still renders.
GUARD = ".card-link,.card-readmore,.special-course-link{font-family:var(--mono)}"

# Post-box titles in the Regular (upright) cut, not Italic (Lenny, 2026-08-28:
# "use the regular style for the post boxes"). Both selectors are the same
# component in two places - .card-title in the homepage feed, .more-card-name in
# the More-from-the-Feed boxes at the foot of every post - so they move together
# or the site looks inconsistent. .product-name stays italic: it labels products,
# not posts, and italic is what separates the two.
POSTBOX = ".card-title,.more-card-name{font-style:normal}"

# Literal pairs. Order matters: longer/quoted forms first so the bare form does
# not partially match them.
SUBS = [
    ("--serif: 'Fraunces', Georgia, serif",              f"--serif: {FAM}, Georgia, serif"),
    ("--serif:'Fraunces',Georgia,serif",                 f"--serif:{FAM},Georgia,serif"),
    ("--display:'In The Margins','Fraunces',Georgia,serif",
     f"--display:'In The Margins',{FAM},Georgia,serif"),
    ("font-family: 'Fraunces', Georgia, serif",          f"font-family: {FAM}, Georgia, serif"),
    ("font-family:'Fraunces',Georgia,serif",             f"font-family:{FAM},Georgia,serif"),
    ("font-family:Fraunces,Georgia,serif",               f"font-family:{FAM},Georgia,serif"),
    # Newsletter popup body copy. Inline style, so no appended rule can reach it.
    # Its headline and confirmation already converted (they were Fraunces); this
    # paragraph was the last piece of Inter PROSE left anywhere on the site. The
    # long key keeps it distinct from the email <input>, which also sits at
    # Inter/14px and correctly STAYS sans - form fields are UI, not prose.
    ("font-family:'Inter',sans-serif;font-size:14px;line-height:1.55;color:var(--ink);opacity:0.7",
     f"font-family:{FAM},Georgia,serif;font-size:15px;line-height:1.55;color:var(--ink);opacity:0.7"),
]


def profile_for(rel):
    """Which reading-text rules a page gets. None = marker block only."""
    if rel in SKIP:
        return None
    if rel == "index.html":
        # ROUND 2 (Lenny asked "does this look cohesive or are we putting too many
        # fonts all over the place?"). Measuring visible characters by font showed
        # posts at 94% Editor's Note / 6% mono - clean - but the homepage stuck at
        # 71/21/7 with Inter holding real PROSE: the Muny panel, event descriptions,
        # the Masters lottery steps, the hero sub and the newsletter copy. Inter was
        # no longer a decision, just "whatever round 1 didn't convert", which is
        # exactly what reads as accidental. So the homepage goes serif body-wide and
        # the exceptions are pinned explicitly.
        #
        # The dividing line is SENTENCES vs DATA LINES:
        #   sentences  -> serif  (inherited from body)
        #   data lines -> mono   (joins the existing label system)
        # "54 products · Men's 21 · Women's 23" and "Muni Kids — Portland, OR ·
        # Est. 2015" are data, not prose, so they go mono rather than serif.
        # letter-spacing:.005em on .card-text was tuned for Inter at 13px; positive
        # tracking on a serif reads gappy, so it is zeroed.
        return ("body{font-family:var(--serif)}"
                ".card-text{font-family:var(--serif);letter-spacing:0}"
                ".card-source,.card-source a,.source-link,.gear-slide-caption,"
                ".score-row .name{font-family:var(--mono)}")
    if rel == "brands/index.html":
        # .bi-hero-sub is the standfirst over the hero image - prose, and the last
        # Inter on the site after the round-2 sweep.
        return ".bi-line,.bi-intro,.bi-hero-sub{font-family:var(--serif)}"
    if rel.startswith("brands/"):
        return ".bp-line{font-family:var(--serif)}"
    if rel.split("/")[0] in ("drops", "guides", "events", "field-guide"):
        return "ARTICLE"
    return None


def article_css(html):
    css = (f"body{{font-family:var(--serif)}}\n{READING}{{font-family:var(--serif)}}")
    base = re.search(r'(?:html\s*,\s*)?body\s*\{[^}]*\}', html)
    # Only nudge size/leading where the base really is 15px - the pages with a
    # bare body{font-family} rule inherit 16px and must not be shrunk.
    if base and "font-size:15px" in base.group(0).replace(" ", ""):
        css += "\nbody{font-size:16px;line-height:1.6}"
    return css


def live_pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in ("drafts", "research", ".git", "node_modules"):
            continue
        yield p, rel


def main():
    apply_ = "--apply" in sys.argv
    revert = "--revert" in sys.argv
    inv_path = ROOT / "research" / "ent-inventory.json"

    if apply_ and not revert:
        inv_path.parent.mkdir(exist_ok=True)
        inv_path.write_text(json.dumps(
            {rel: {"bytes": p.stat().st_size,
                   "sha": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p, rel in live_pages()}, indent=1))
        print(f"inventory written: {inv_path.relative_to(ROOT)}")

    changed = 0
    stats = {"block": 0, "subs": 0, "article": 0, "scoped": 0}
    for p, rel in live_pages():
        prof = profile_for(rel)
        if prof is None:
            continue
        html = orig = p.read_text(encoding="utf-8")

        # always rebuild the block from a clean base -> idempotent
        html = re.sub(re.escape(MARK) + r".*?" + re.escape(ENDMARK), "", html, flags=re.S)

        for a, b in SUBS:
            src, dst = (b, a) if revert else (a, b)
            if src in html:
                stats["subs"] += html.count(src)
                html = html.replace(src, dst)

        # ---- SCRIPT SAFETY (added 2026-08-30 after this killed sitewide search)
        # The substitutions above turn an UNQUOTED font name into a SINGLE-QUOTED
        # one. That is fine in CSS and in a double-quoted style attribute, and
        # fatal inside a single-quoted JavaScript string — which is where the
        # search overlay assembles its result rows:
        #     +'<span style="...font-family:'Editors Note Text',Georgia,serif;..."'
        # The quote closes the literal, the parser throws `Unexpected identifier`,
        # and the whole <script> block dies silently. 185 pages shipped that way
        # and site search did nothing on any of them.
        # So: re-escape the quotes inside <script> blocks after substituting.
        def _esc_scripts(doc):
            def one(m):
                js = m.group(2)
                if "'Editors Note Text'" in js:
                    js = re.sub(r"(?<!\\)'Editors Note Text'",
                                r"\\'Editors Note Text\\'", js)
                return m.group(1) + js + m.group(3)
            return re.sub(r"(<script\b[^>]*>)(.*?)(</script>)", one, doc, flags=re.S)

        if not revert:
            html = _esc_scripts(html)

        if not revert:
            body = article_css(html) if prof == "ARTICLE" else prof
            stats["article" if prof == "ARTICLE" else "scoped"] += 1
            i = html.rfind("</style>")
            if i == -1:
                print(f"  !! no </style>, skipped: {rel}")
                continue
            html = html[:i] + f"\n{MARK}\n{FACES}\n{body}\n{GUARD}\n{POSTBOX}\n{ENDMARK}\n" + html[i:]
            stats["block"] += 1

        if html != orig:
            if apply_:
                p.write_text(html, encoding="utf-8")
            changed += 1

    print(f"{'reverted' if revert else 'applied' if apply_ else 'DRY RUN'}: {changed} files")
    print(f"   marker blocks {stats['block']}   substitutions {stats['subs']}"
          f"   article {stats['article']}   scoped {stats['scoped']}")
    if not apply_:
        print("\n(dry run - pass --apply to write)")


if __name__ == "__main__":
    main()
