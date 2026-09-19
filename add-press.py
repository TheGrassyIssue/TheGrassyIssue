#!/usr/bin/env python3
"""
add-press.py — a small Press / Citations block on /about. 19 September 2026.

Lenny's brief: not a homepage banner, just a quiet section on the About page
listing who has referenced TGI.

WHAT VERIFICATION FOUND, because it changed what goes on the page.
The DEAS MAG piece cites The Grassy Issue TWICE, not once:

  1. "Behind it, one designer in San Francisco and, per The Grassy Issue,
     'a catalog so small it fits on a scorecard': twelve SKUs."
  2. "The Grassy Issue put it best: 'greenkeeper who reads design blogs'."

Quote 1 is VERIFIABLY OURS. It is live on
/drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no and on the
homepage card, word for word. That is the one this block quotes.

QUOTE 2 IS NOT ON THIS SITE. A full-text search of every published page, every
draft and the whole research folder returns nothing for "greenkeeper who reads
design blogs", "design blog", or any near variant. It may well be Lenny's —
from Instagram, the newsletter, an email to the writer, or a version of the page
that predates this repo — but it cannot be sourced from anything here, and the
house rule is that a quote is verbatim from a traceable source or it does not
run. So it is deliberately NOT on the page pending confirmation, and the guard
below fails the build if it appears without the sourcing note being updated
first.

Idempotent: detects its own marker and rewrites in place. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
ABOUT = ROOT / "about.html"
MARK = "<!-- PRESS / CITATIONS -->"

H2 = ('<h2 style="font-family:var(--serif);font-weight:600;font-size:24px;'
      'margin:32px 0 14px">Press</h2>')

# Both quotes DEAS took from us. The second was missing from the site when this
# block was first built and was therefore withheld; add-agronomy-line.py has
# since restored it to the post, so it is now traceable and runs here too.
# Every quote in this list is checked against SOURCE_PAGE at build time.
QUOTES = [
    "a catalog so small it fits on a scorecard",
    "greenkeeper who reads design blogs",
]
QUOTE = QUOTES[0]
SOURCE_PAGE = "/drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no"
ARTICLE = ("https://deasmag.com/the-raw-material-of-the-fairway-"
           "agronomy-workshop-and-the-long-game")

CSS = """
/* --- press / citations --- */
.press-list{list-style:none;padding:0;margin:14px 0 0;}
.press-item{padding:16px 0;border-top:1px solid rgba(0,0,0,.12);}
.press-item:last-child{border-bottom:1px solid rgba(0,0,0,.12);}
.press-outlet{font-family:var(--mono);font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;opacity:.55;}
.press-quote{font-family:var(--serif);font-size:19px;line-height:1.45;
  margin:8px 0 8px;}
.press-meta{font-size:13px;line-height:1.6;opacity:.7;}
.press-meta a{border-bottom:1px solid currentColor;}
"""

BLOCK = f'''    {MARK}
    {H2}

    <p>Where the site has been referenced elsewhere.</p>

    <ul class="press-list">
      <li class="press-item">
        <div class="press-outlet">DEAS MAG &middot; August 2026</div>
        <blockquote class="press-quote">&ldquo;The Grassy Issue put it best:
          &lsquo;{QUOTES[1]}&rsquo;.&rdquo;</blockquote>
        <div class="press-meta">Cited twice &mdash; also for
          &ldquo;{QUOTES[0]}&rdquo; &mdash; in
          <a href="{ARTICLE}" target="_blank" rel="noopener">The Raw Material of
          the Fairway</a>, 27 August 2026. Both lines are from our
          <a href="{SOURCE_PAGE}">Agronomy Workshop piece</a>.</div>
      </li>
    </ul>
'''


def build():
    t = ABOUT.read_text(encoding="utf-8")

    if MARK in t:
        # IDEMPOTENT EXCISE. The first version computed a start offset that
        # accounted for the block's leading indent and then threw it away,
        # cutting from t.index(MARK) instead. The four spaces in front of the
        # marker therefore survived every run and a fresh "    \n" accumulated
        # ahead of the block each time — the file grew by one blank line per
        # rebuild and was never byte-stable. Cut whole LINES: from the start of
        # the line holding the marker through the end of the line holding the
        # closing </ul>.
        s = t.rfind("\n", 0, t.index(MARK)) + 1
        e = t.index("\n", t.index("</ul>", s)) + 1
        t = t[:s] + t[e:]
        t = re.sub(r"[ \t]+\n", "\n", t)     # no trailing whitespace-only lines
        t = re.sub(r"\n{3,}", "\n\n", t)

    # Place it BEFORE "Get in touch" — press belongs with what the site is, not
    # after the contact details, which read as the end of the page.
    anchor = t.find(">Get in touch</h2>")
    if anchor < 0:
        sys.exit("! could not find the 'Get in touch' heading to anchor against")
    at = t.rfind("<h2", 0, anchor)
    at = t.rfind("\n", 0, at) + 1

    out = t[:at] + BLOCK + "\n" + t[at:]
    if ".press-item{" not in out:
        k = out.rfind("</style>")
        if k < 0:
            sys.exit("! no </style> on the about page to append rules to")
        out = out[:k] + CSS + out[k:]
    return out


def _fixed_point(page):
    """Would a second build over this output change anything? Runs build()
    against `page` in memory, without touching about.html on disk."""
    orig = ABOUT.read_bytes()
    try:
        ABOUT.write_text(page, encoding="utf-8")
        return build() == page
    finally:
        ABOUT.write_bytes(orig)           # always restore, even on exception


def main(apply_):
    page = build()
    body = page[page.find("<body"):]

    checks = [
        ("exactly one Press block", page.count(MARK) == 1, ""),
        ("exactly one Press heading", page.count(">Press</h2>") == 1, ""),
        ("Press sits above Get in touch",
         page.index(MARK) < page.index(">Get in touch</h2>"), ""),
        # THE RULE, GENERALISED. Any line this page attributes to TGI must be
        # findable, verbatim, on the page we credit it to. This started as a
        # narrow "don't publish the greenkeeper line" check; that was the right
        # instinct but the wrong shape — it hard-coded one string instead of
        # stating the principle. Now every quote in QUOTES is checked against
        # the source page, so withholding or restoring a line is a data change
        # rather than an edit to the guard.
        ("every attributed quote is verbatim on the page we credit",
         all(q in (ROOT / SOURCE_PAGE.lstrip("/")).with_suffix(".html")
                   .read_text(encoding="utf-8") for q in QUOTES),
         str([q for q in QUOTES
              if q not in (ROOT / SOURCE_PAGE.lstrip("/")).with_suffix(".html")
                          .read_text(encoding="utf-8")])),
        ("every quote appears on the about page",
         all(q in page for q in QUOTES), ""),
        ("the source page it credits exists",
         (ROOT / SOURCE_PAGE.lstrip("/")).with_suffix(".html").exists(), ""),
        ("outlet and date are present",
         "DEAS MAG" in page and "August 2026" in page, ""),
        ("outbound press link opens in a new tab and is rel=noopener",
         f'href="{ARTICLE}" target="_blank" rel="noopener"' in page, ""),
        ("every class used has a rule",
         all(f".{c}{{" in page for c in
             ("press-list", "press-item", "press-outlet", "press-quote", "press-meta")), ""),
        ("no <li> outside the press list",
         body.count("<li") == body.count("</li>"), ""),
        ("div balance", page.count("<div") == page.count("</div>"),
         f'{page.count("<div")}/{page.count("</div>")}'),
        ("ul balance", page.count("<ul") == page.count("</ul>"), ""),
        ("anchor balance", len(re.findall(r"<a\b", page)) == page.count("</a>"), ""),
        ("banned word 'worth' absent", not re.search(r"\bworth\b", page, re.I), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
        # IDEMPOTENCY, ASSERTED IN THE BUILD rather than checked by hand after.
        # Running build() against its own output must be a fixed point; the
        # accumulating-indent bug above is exactly what this catches.
        ("rebuilding from this output is byte-identical",
         _fixed_point(page), ""),
        ("no whitespace-only lines were left behind",
         not re.search(r"\n[ \t]+\n", page), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}{('  ' + d) if d and not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {len(page):,} bytes")
    if apply_:
        ABOUT.write_text(page, encoding="utf-8")
        print("  wrote about.html")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
