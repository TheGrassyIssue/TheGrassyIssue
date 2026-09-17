#!/usr/bin/env python3
"""Put /work-with-us where the qualified visitor actually is.

THREE PLACEMENTS, none of them the top nav:

1. THE 131 BRAND PAGES. This is the whole point. A brand employee who googled
   their own name and landed on /brands/<them> is the most qualified visitor the
   site gets, and until now the page ended with a grid of post cards and nothing
   else. One quiet line under the grid, in the mono kicker style, addressed to
   them rather than to a reader.

2. THE FOOTER, SITEWIDE. Follows the add-about-link.py convention: sit it next to
   the existing About link wherever that footer shape exists.

3. /about. One sentence at the end pointing brands at the new page, since /about
   is where a curious brand looks first and currently says nothing about working
   together.

NOT IN THE TOP NAV, deliberately. The nav is reader-facing — The Feed, Brands,
Field Guide, Events, About. Hanging "Work With Us" off it tells every reader the
site is for sale. Footer plus brand pages is full coverage without that.

IDEMPOTENT. Every insertion is marker-fenced (TGI-WWU) and replaced rather than
appended on a re-run, so this is safe after any brand rebuild.
"""
import re, os, sys, glob, json

URL = "/work-with-us"
S, E = "<!--TGI-WWU-->", "<!--/TGI-WWU-->"
apply_ = "--apply" in sys.argv

if not os.path.exists("work-with-us.html"):
    raise SystemExit("work-with-us.html does not exist — run build-work-with-us.py --apply first")

brands = json.load(open("data/brands.json", encoding="utf-8"))
notes = []

# ---------------------------------------------------------- 1. brand pages
CSS = """<style id="wwu-css">
.wwu{max-width:1200px;margin:8px auto 64px;padding:0 24px}
.wwu-in{border-top:1px solid rgba(20,20,20,.12);padding-top:16px;display:flex;flex-wrap:wrap;
 gap:6px 10px;align-items:baseline}
.wwu-lab{font-family:var(--mono,ui-monospace,monospace);font-size:9.5px;letter-spacing:.15em;
 text-transform:uppercase;opacity:.5}
.wwu-in p{margin:0;font-size:14.5px;line-height:1.5;opacity:.85}
.wwu-in a{color:inherit;border-bottom:1px solid currentColor;text-decoration:none}
</style>"""

touched, skipped = [], []
for b in brands:
    p = os.path.join("brands", b["slug"] + ".html")
    if not os.path.exists(p):
        skipped.append(b["slug"]); continue
    t = open(p, encoding="utf-8").read()
    t = re.sub(re.escape(S) + r".*?" + re.escape(E), "", t, flags=re.S)   # idempotent

    name = b["name"]
    block = (f'{S}<section class="wwu"><div class="wwu-in">'
             f'<span class="wwu-lab">For {name}</span>'
             f'<p>Work at {name}? This coverage is independent and always will be, but if you want '
             f'to talk about sending product, a sponsored Field Note or something longer, '
             f'<a href="{URL}">here is how that works</a>.</p>'
             f'</div></section>{E}')

    # after the post grid, before the footer — the end of what they came to read
    grid = t.find('<div class="bp-grid">')
    if grid == -1:
        skipped.append(b["slug"] + " (no grid)"); continue
    depth, j, end = 0, grid, None
    while j < len(t):
        m = re.compile(r"<div\b|</div>").search(t, j)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end(); break
        j = m.end()
    if end is None:
        skipped.append(b["slug"] + " (unbalanced grid)"); continue
    t = t[:end] + "\n" + block + t[end:]

    if 'id="wwu-css"' not in t:
        t = t.replace("</head>", CSS + "\n</head>", 1)
    if apply_:
        open(p, "w", encoding="utf-8").write(t)
    touched.append(b["slug"])
notes.append(f"brand pages given a work-with-us line: {len(touched)}")
if skipped:
    notes.append(f"  !! skipped: {', '.join(skipped)}")

# ------------------------------------------------------- 2. footer sitewide
pages = sorted(set(glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")))
pages = [p for p in pages if "drafts/" not in p and "research/" not in p
         and not os.path.basename(p).startswith("_")]
foot = 0
for p in pages:
    t = open(p, encoding="utf-8").read()
    if f'href="{URL}"' in t and "<footer" in t and t.count(f'href="{URL}"') >= 1:
        # already has it somewhere; only add to the footer if the footer lacks it
        fi = t.find("<footer")
        if fi != -1 and URL in t[fi:]:
            continue
    o = t
    t = t.replace('<a href="/">Back to Feed</a>',
                  f'<a href="{URL}">Work With Us</a><a href="/">Back to Feed</a>', 1)
    if t != o:
        foot += 1
        if apply_:
            open(p, "w", encoding="utf-8").write(t)
notes.append(f"footer link added on: {foot} pages")

# ------------------------------------------------------------- 3. /about
t = open("about.html", encoding="utf-8").read()
t = re.sub(re.escape(S) + r".*?" + re.escape(E), "", t, flags=re.S)
line = (f'{S}<p>If you make something and you are wondering whether there is a version of this '
        f'where we work together, <a href="{URL}" style="border-bottom:1px solid var(--ink)">'
        f'that is written down here</a>.</p>{E}')
anchor = t.find('<p class="sig">')
if anchor == -1:
    notes.append("  !! no signature block in about.html — link not added")
else:
    t = t[:anchor] + line + "\n    " + t[anchor:]
    if apply_:
        open("about.html", "w", encoding="utf-8").write(t)
    notes.append("/about: one line added above the signature")

# ----------------------------------------------------------------- sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>2026-09-17</lastmod>'
                    f'<changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    notes.append("sitemap: row added")
else:
    notes.append("sitemap: already present")
if apply_:
    open("sitemap.xml", "w", encoding="utf-8").write(sm)

# ------------------------------------------------------------------ guards
if apply_:
    for b in brands[:]:
        p = os.path.join("brands", b["slug"] + ".html")
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        if t.count(S) > 1 or t.count(E) > 1:
            raise SystemExit(f"{b['slug']}: work-with-us markers doubled — not idempotent")
        if t.count(S) == 1 and t.count("</footer>") != 1:
            raise SystemExit(f"{b['slug']}: footer damaged")
        if t.count("<div") != t.count("</div>"):
            raise SystemExit(f"{b['slug']}: unbalanced divs after insertion")
    a = open("about.html", encoding="utf-8").read()
    if a.count(S) > 1:
        raise SystemExit("about.html: marker doubled")
    if not os.path.exists("work-with-us.html"):
        raise SystemExit("the target page vanished")

print(("wired" if apply_ else "DRY RUN") + f" {URL}")
for n in notes:
    print("  ·", n)
if not apply_:
    print("\npass --apply to write")
