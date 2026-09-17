#!/usr/bin/env python3
"""Put the Social Club on /events and in the sitemap — 17 September 2026.

PLACEMENT. The events page has one .featured-event slot, currently held by The
Long Walk. Rather than evict it, this adds a SECOND featured block directly
below, using the identical markup and classes so nothing new needs styling. Both
are TGI events gauging interest; neither should outrank the other on the page.

The .featured-event CSS already handles a standalone <a> with a poster and a
body, so a second instance inherits everything.

IDEMPOTENT: marker-fenced (TGI-SOCIAL-CLUB) and replaced rather than appended.
"""
import re, os, sys

apply_ = "--apply" in sys.argv
P = "events/index.html"
URL = "/events/social-club"
S, E = "<!--TGI-SOCIAL-CLUB-->", "<!--/TGI-SOCIAL-CLUB-->"
POSTER = "/images/social-club-poster.jpg"

BLOCK = f'''{S}
<section class="featured-event">
  <a href="{URL}">
    <div class="featured-poster">
      <img src="{POSTER}" alt="The Grassy Issue Social Club poster — a green over a wide Hill Country horizon, with the words Good golf, Good people" />
    </div>
    <div class="featured-body">
      <div class="featured-badges">
        <span class="badge badge-tgi">TGI Event</span>
        <span class="badge badge-interest">Building the List</span>
      </div>
      <h2>The Grassy Issue Social Club</h2>
      <p>Small groups playing good courses in and around Austin. Eight to twelve players an outing, walkers and riders both, no dues. Join the interest list and we&rsquo;ll match you to one that fits.</p>
      <div class="featured-meta">Austin &amp; roughly 90 minutes around it &middot; Ongoing</div>
      <span class="featured-cta">Join The List &rarr;</span>
    </div>
  </a>
</section>
{E}
'''

notes = []
t = open(P, encoding="utf-8").read()
t = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", t, flags=re.S)

# insert directly after the existing featured-event section
i = t.find('<section class="featured-event">')
if i == -1:
    raise SystemExit("no .featured-event block on the events page")
j = t.find("</section>", i) + len("</section>")
t = t[:j] + "\n\n" + BLOCK + t[j:]
notes.append("second featured block added below The Long Walk")

# ------------------------------------------------------------------ sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc in sm:
    sm = re.sub(r"(<loc>" + re.escape(loc) + r"</loc>\s*<lastmod>)[0-9-]+",
                lambda m: m.group(1) + "2026-09-17", sm)
    notes.append("sitemap: lastmod bumped")
else:
    sm = sm.replace("</urlset>", f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-17</lastmod>\n'
                    f'    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
    notes.append("sitemap: row added")

# ------------------------------------------------------------------- guards
problems = []
if t.count(S) != 1 or t.count(E) != 1:
    problems.append("markers doubled — not idempotent")
if t.count('<section class="featured-event">') != 2:
    problems.append(f"{t.count(chr(60)+'section class=')} featured blocks — expected 2")
for tag in ("<div", "<section", "<a "):
    if t.count(tag) != t.count(tag.replace("<", "</").strip() + ">"):
        problems.append(f"unbalanced {tag.strip()}")
if t.count("the-long-walk") < 1:
    problems.append("The Long Walk block was damaged")
if not os.path.exists(POSTER.lstrip("/")):
    problems.append("poster missing on disk")
if not os.path.exists("events/social-club.html"):
    problems.append("the page does not exist — run build-social-club.py --apply first")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)

print(("wired" if apply_ else "DRY RUN") + f" {URL}")
for n in notes:
    print("  ·", n)
if not apply_:
    print("\npass --apply to write")
