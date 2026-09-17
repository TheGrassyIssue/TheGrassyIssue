#!/usr/bin/env python3
"""Wire the Hidden Links Society BTK — homepage card, brand index, sitemap.
17 September 2026.

THE FOUR CAROUSEL SLIDES ARE LENNY'S PICKS (01, 02, 05, 18 off the grid):
  1  Play Faster Fairway Wood Cover - Black   $82
  2  The Play Faster Tee - Ivory              $48
  3  Always Tinkering Hat - Navy              $37
  4  Print Series - Score Keepers             $35

CARD TYPE "drop", not "drops". The feed types are drop / drops / field / guide /
news / quote / score. "drops" plus a [Drops & Brands] chip is the multi-brand
roundup treatment; this is one brand, so it takes the single-brand "drop" card
the other Brand to Know posts use.

ARROWS NEED INLINE onclick="gearSlide(this, ±1)". The homepage carousel does not
delegate — a card built without the inline handlers renders arrows that do
nothing, which is how the scroll buttons broke last time.

CAPTIONS GO IN THE CANONICAL window._slideTexts LITERAL, which is JAVASCRIPT, NOT
JSON. It is validated with node below; json.loads would reject it on the unquoted
keys and take the build down for no reason.
"""
import re, os, sys, json, glob, subprocess, tempfile

apply_ = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "brand-to-know-hidden-links-society"
URL = f"/drops/{SLUG}"
KEY = "hiddenlinks"
S, E = "<!--TGI-HLS-->", "<!--/TGI-HLS-->"

SKU = {k: v for k, v in json.load(open(os.path.join(ROOT, "research/hls-skus.json"),
                                      encoding="utf-8")).items() if not k.startswith("_")}

SLIDES = [
 ("play-faster-fairway-wood-cover-black", "Play Faster Fairway Wood Cover",
  "100% wool &middot; made with Ross Co Golf &middot; $82"),
 ("the-play-faster-tee-ivory", "The Play Faster Tee",
  "230gsm garment-washed cotton &middot; Ivory &middot; $48"),
 ("always-tinkering-society-navy", "Always Tinkering Hat",
  "Five panel &middot; made with Golf Gimmes &middot; $37"),
 ("print-series-score-keepers", "Print Series &mdash; Score Keepers",
  "8x10 on 230gsm matte &middot; $35"),
]

CAPTIONS = [
 "A 220cc fairway cover in 100% wool, handcrafted in the USA with Ross Co Golf out of Bandon, Oregon, with a dancing PLAY FASTER running round the barrel. A headcover that doubles as a position on pace of play, which is roughly the whole brand in one object. Preorder — their page says covers ship the first week of October.",
 "The same message, worn. 230gsm garment-washed cotton, relaxed and slightly oversized, drop shoulders, the imprint front and back. Their line on it is the good one: some messages are better said than shouted from the tee box.",
 "Made with Golf Gimmes and aimed at anyone who has rebuilt their bag three times this season. Mid-weight cotton, five panels, flat peak, metal clasp, tonal under-peak lining. The patch reads ALWAYS TINKERING SOCIETY, which is either a compliment or a diagnosis.",
 "Not gear at all. An 8x10 study of pencils and scorecards on 230gsm heavyweight matte, packaged on acid-free foamcore, described by the brand as the smallest souvenir in golf. A clothing brand running a print series is a clothing brand that wants to be a publisher.",
]

TITLE = "Brand to Know &mdash; Hidden Links Society"
TEXT = ("Thirty products, and a documentary series about a hundred golf courses. Hidden Links Society "
        "makes headwear, headcovers and a properly heavy overshirt, gives 2% of every sale to Youth on "
        "Course, and is quietly working through Golf Digest's Top 100 Public list one course at a time. "
        "Eighteen pieces, prices read 17 September 2026.")


def img(key):
    f = sorted(glob.glob(os.path.join(ROOT, "images", "hls", f"{key}-*.jpg")))
    if not f:
        raise SystemExit(f"no localized image for {key}")
    return "/images/hls/" + os.path.basename(f[0])


slides = "".join(
    f'<div class="gear-slide">\n<a href="{URL}">\n'
    f'<img src="{img(k)}" alt="{re.sub(r"&[a-z]+;", " ", n)} by Hidden Links Society" loading="lazy" />\n'
    f'<div class="gear-slide-info"><div class="gear-slide-brand">#{i} &middot; {n}</div>'
    f'<div class="gear-slide-name">{m}</div></div>\n</a>\n</div>\n'
    for i, (k, n, m) in enumerate(SLIDES, 1))

CARD = f'''{S}
      <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{slides}        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{TEXT}</div>
      <a href="{URL}" class="card-link">See all 18 &#8599;</a>
    </div>
  </div>
{E}
'''

log, problems = [], []
h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
before = len(h)

# ------------------------------------------------------------- idempotency
h = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", h, flags=re.S)
m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]
log.append("card inserted at the top of the feed")

# ------------------------------------------- captions into _slideTexts
k = h.find("window._slideTexts = {")
if k < 0:
    problems.append("could not find the _slideTexts literal")
else:
    ins = h.index("{", k) + 1
    caps = ",\n".join('        ' + json.dumps(c, ensure_ascii=False) for c in CAPTIONS)
    h = h[:ins] + f"\n      {KEY}: [\n{caps}\n      ]," + h[ins:]
    log.append(f"{len(CAPTIONS)} captions added to _slideTexts under {KEY!r}")

# ----------------------------------------------------------------- guards
if h.count(S) != 1 or h.count(E) != 1:
    problems.append("markers doubled — not idempotent")
# Each slide wraps its own anchor, so the count is one per slide plus the title
# and the CTA. My first guess of 4 was wrong and the guard caught it, which is
# the guard doing its job.
_want = len(SLIDES) + 2
if h.count(URL) != _want:
    problems.append(f"{h.count(URL)} links to the post — expected {_want} "
                    f"({len(SLIDES)} slides + title + CTA)")
if h.count("<div") != h.count("</div>"):
    problems.append("unbalanced divs")
if h.count("<a ") != h.count("</a>"):
    problems.append("unbalanced anchors")
if 'onclick="gearSlide(this, -1)"' not in CARD or 'onclick="gearSlide(this, 1)"' not in CARD:
    problems.append("arrows are missing their inline gearSlide handlers — they would do nothing")
if len(SLIDES) != len(CAPTIONS):
    problems.append(f"{len(SLIDES)} slides but {len(CAPTIONS)} captions")
for key, _n, meta in SLIDES:
    if key not in SKU:
        problems.append(f"slide {key} is not in the SKU file")
    else:
        want = "$" + str(int(float(SKU[key]["price"])))
        if want not in meta:
            problems.append(f"slide {key}: meta says {meta!r}, SKU says {want}")
if not os.path.exists(os.path.join(ROOT, "drops", SLUG + ".html")):
    problems.append("the post does not exist yet")
if "hiddenlinksgolf" in h:
    problems.append("hiddenlinksgolf.com — different company")
if re.search(r"\bworth\b", re.sub(r"&[a-z]+;", " ", TITLE + " " + TEXT + " ".join(CAPTIONS)), re.I):
    problems.append("banned word 'worth' in the card copy")

# the _slideTexts literal is JS, not JSON — validate with node
if k >= 0:
    d, end = 0, None
    for j in range(h.index("{", k), len(h)):
        if h[j] == "{":
            d += 1
        elif h[j] == "}":
            d -= 1
            if d == 0:
                end = j
                break
    js = h[k:end + 1].replace("window._slideTexts", "var _st")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(js + f"\nif(!_st.{KEY}||_st.{KEY}.length!=={len(CAPTIONS)})"
                      f"{{throw new Error('caption block wrong');}}"
                      "\nconsole.log(Object.keys(_st).length);")
        tmp = fh.name
    r = subprocess.run(["node", tmp], capture_output=True, text=True)
    if r.returncode:
        problems.append("_slideTexts no longer parses as JS — " + r.stderr.strip().splitlines()[-1])
    else:
        log.append(f"_slideTexts parses, {r.stdout.strip()} keys")
    os.unlink(tmp)

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(h)

    # sitemap
    sp = os.path.join(ROOT, "sitemap.xml")
    s = open(sp, encoding="utf-8").read()
    if SLUG not in s:
        entry = (f"  <url>\n    <loc>https://thegrassyissue.com{URL}</loc>\n"
                 f"    <lastmod>2026-09-17</lastmod>\n    <changefreq>monthly</changefreq>\n"
                 f"    <priority>0.7</priority>\n  </url>\n")
        s = s.replace("</urlset>", entry + "</urlset>")
        open(sp, "w", encoding="utf-8").write(s)
        log.append("sitemap entry added")
    else:
        log.append("sitemap already had the slug")

print(("wired" if apply_ else "DRY RUN") + f" {URL}  ({len(h)-before:+,} bytes)")
for l in log:
    print("  ·", l)
print(f"  {len(SLIDES)} slides · type drop · [Drops & Brands] chip · See all 18")
if not apply_:
    print("\npass --apply to write")
