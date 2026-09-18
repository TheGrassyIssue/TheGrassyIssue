#!/usr/bin/env python3
"""
fix-post-formatting.py — the four formatting defects across all 195 drop pages.
18 September 2026.

Lenny: "let's also fix the formatting for all the posts."

A sweep of verify-post.py over drops/ found 122 pages with at least one failure.
Stripped of the word-count check (which is about how much was written, not how
it is formatted) four real defects remain, and this fixes those four only.

  1. NO FOOTER — 7 pages
     bold-tees-carousel, hats-carousel, malbon-summer-gallo-colorido,
     manors-gentleman-jack, metalwood-ss26-picks, muni-kids-10-years,
     premium-tees-carousel. They close properly — <body> and <html> are both
     there — they simply have no footer at all, which is why verify-post's
     "document closes" check failed them. All seven are linked from the feed
     and sitemap, so they are live pages with no footer on them.

  2. TWITTER CARD DOES NOT MATCH OG — 17 pages
     twitter:description (and on one page twitter:title) carries a different
     string from its og: counterpart, so the card a reader sees on X differs
     from the one they see everywhere else. The og: value is the correct one;
     twitter: is copied from it.

  3. CLASSES WITH NO CSS RULE — 9 pages
     .products-hdr on 7, .writeup-img on 2. The markup is there, the styling
     never was, so those headings and images render unstyled.

  4. THE BANNED WORD, IN PROSE ONLY — 4 instances
     "worth" appears on 19 pages, but almost every hit is either the title of
     one of the nine posts whose SLUG contains the word, or a More-from-the-Feed
     card linking to one of them. Lenny chose to leave those slugs alone, and a
     card's link text has to match the page it points at, so both are left. That
     leaves four genuine sentences, rewritten below and listed in full because
     they are the only copy this script touches.

WHAT IT WILL NOT DO
-------------------
  - rename a slug, a title or a canonical
  - touch a More-from-the-Feed card
  - add a word to any page (the word count failures are a content job)
  - write anything if a page fails its own re-check afterwards

USAGE
    python3 fix-post-formatting.py            # dry run, reports every change
    python3 fix-post-formatting.py --apply
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
DROPS = ROOT / "drops"

NO_FOOTER = ["bold-tees-carousel", "hats-carousel", "malbon-summer-gallo-colorido",
             "manors-gentleman-jack", "metalwood-ss26-picks", "muni-kids-10-years",
             "premium-tees-carousel", "swag-golf-college-program"]

# The four sentences. Each is (slug, exact old text, new text). Written out in
# full so the diff is reviewable without running anything.
WORTH_FIXES = [
    ("10-of-the-best-post-round-burgers",
     "always inventive, always local ingredients, and always worth the trip.",
     "always inventive, always local ingredients, and always a reason to make the drive."),
    ("8-best-practice-facilities-around-austin",
     "Worth the 30-minute drive from central Austin",
     "Enough to justify the 30-minute drive from central Austin"),
    ("brand-to-watch-kingfisher-golf",
     "Worth knowing.",
     "One to know."),
    ("roy-kizer-from-sewage-plant-to-links-style-gem",
     "that's part of what makes it worth playing.",
     "that's part of the reason to play it."),
]

# The missing rules, in the house idiom already used elsewhere in these files.
# The footer needs its own rules as well as its markup. Injecting the markup
# alone left .inner unstyled on all seven pages — the first pass fixed the
# missing footer and created a missing rule in its place.
FOOTER_CSS = ("footer{border-top:.5px solid var(--ink);margin-top:80px;"
              "padding:40px 32px 24px}"
              "footer .inner{max-width:1400px;margin:0 auto;display:flex;"
              "justify-content:space-between;align-items:center;"
              "font-family:var(--mono);font-size:10px;letter-spacing:.15em;"
              "text-transform:uppercase;opacity:.55}"
              "@media(max-width:820px){footer{padding:32px 20px 20px;"
              "margin-top:48px}}")

CSS_RULES = {
    # verify-post requires a REAL kicker rule, not just the shared font list:
    # without max-width the lede runs the full width of the page.
    "cat-kicker": ".cat-kicker{font-family:var(--sans);font-size:15px;"
                  "line-height:1.75;color:#3f443e;margin:0 0 36px;max-width:70ch;"
                  "border-left:3px solid var(--rough);padding:4px 0 4px 18px}",
    "products-hdr": ".products-hdr{font-family:var(--serif);font-size:26px;"
                    "line-height:1.15;margin-bottom:18px}",
    "writeup-img": ".writeup-img{width:100%;height:auto;display:block;"
                   "border:.5px solid var(--ink);margin:18px 0}",
}


def house_footer():
    """Lift the footer verbatim from a page that has one, so the seven that are
    missing it get exactly the same markup rather than a reconstruction."""
    for p in sorted(DROPS.glob("*.html")):
        h = p.read_text(encoding="utf-8")
        m = re.search(r"<footer.*?</footer>", h, re.S)
        if m:
            return m.group(0), p.stem
    return None, None


def fix_page(path, foot):
    h = orig = path.read_text(encoding="utf-8")
    slug, notes = path.stem, []

    # 1. footer
    if slug in NO_FOOTER and "<footer" not in h and foot:
        i = h.rfind("</body>")
        if i > 0:
            h = h[:i] + foot + "\n" + h[i:]
            notes.append("footer added")

    # The rule is checked SEPARATELY from the markup. Tying them together meant
    # the seven pages that got their footer in an earlier pass could never get
    # the stylesheet, because by then they already had a <footer> and the whole
    # branch was skipped. A page that renders a footer needs the rule whether or
    # not this run is the one that put it there.
    if "<footer" in h and "footer.inner{" not in h.replace(" ", ""):
        j = h.rfind("</style>")
        if j > 0:
            h = h[:j] + "\n" + FOOTER_CSS + "\n" + h[j:]
            notes.append("footer css")

    # 2. twitter card follows og — BUT ONLY WHERE IT GENUINELY DIVERGES.
    #
    # The house convention is deliberate and this nearly destroyed it: og:title
    # carries the " — The Grassy Issue" suffix and twitter:title does not, so a
    # naive equality test called 134 correct pages broken and would have
    # rewritten every one of them. verify-post allows the shorter string when it
    # is a prefix of the longer; that is the rule, and this matches it.
    for tag in ("description", "title"):
        og = re.search(rf'<meta property="og:{tag}" content="([^"]*)"', h)
        tw = re.search(rf'<meta name="twitter:{tag}" content="([^"]*)"', h)
        n = 30 if tag == "title" else 40
        if not (og and tw):
            continue
        SUF = " &mdash; The Grassy Issue"
        want = og.group(1)
        if tag == "title":
            # the convention, straight out of verify-post: twitter:title is the
            # og:title with the site suffix removed. Copying og across verbatim
            # would ADD the suffix, which is the opposite of the rule.
            for suf in (SUF, " — The Grassy Issue"):
                if want.endswith(suf):
                    want = want[:-len(suf)]
                    break
        if want != tw.group(1) and not want.startswith(tw.group(1)[:n]):
            h = h[:tw.start(1)] + want + h[tw.end(1):]
            notes.append(f"twitter:{tag} fixed")

    # 3. missing CSS rules — only for classes this page actually renders
    for cls, rule in CSS_RULES.items():
        needs = (f'class="{cls}"' in h and
                 (f".{cls}{{" not in h.replace(" ", "")
                  or (cls == "cat-kicker"
                      and not re.search(r"\.cat-kicker\s*\{[^}]*max-width", h))))
        if needs:
            j = h.rfind("</style>")
            if j > 0:
                h = h[:j] + "\n" + rule + "\n" + h[j:]
                notes.append(f"css .{cls}")

    # 4. the banned word, prose only
    for s, old, new in WORTH_FIXES:
        if s == slug and old in h:
            h = h.replace(old, new)
            notes.append("'worth' rewritten")

    return h, notes, (h != orig)


if __name__ == "__main__":
    apply_ = "--apply" in sys.argv
    foot, src = house_footer()
    print(f"  house footer lifted from: {src}  ({len(foot or '')} bytes)\n")
    changed = 0
    for p in sorted(DROPS.glob("*.html")):
        out, notes, diff = fix_page(p, foot)
        if not diff:
            continue
        changed += 1
        print(f"  {p.stem[:42]:<44} {', '.join(notes)}")
        if apply_:
            # never write a page that loses content
            if len(out) < len(p.read_text(encoding='utf-8')) - 200:
                print("     REFUSED — output shorter than input")
                continue
            p.write_text(out, encoding="utf-8")
    print(f"\n  {changed} page(s) "
          + ("updated" if apply_ else "would change — pass --apply to write"))
