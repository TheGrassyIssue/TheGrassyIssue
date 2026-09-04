#!/usr/bin/env python3
"""Build /search-index.json from all TGI pages. Run after adding posts, then deploy."""
import re, json, html, glob, os

SITE = os.path.dirname(os.path.abspath(__file__))


# Homepage feed cards are the other source of truth for category (data-type).
# Used only where a page's breadcrumb has no category in it.
_TYPE = {"drop": "Drops & Brands", "field": "Field Notes", "news": "News",
         "guide": "Field Notes", "score": "News"}
FEED_TYPE = {}
try:
    _idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    for _m in re.finditer(r'<div class="card"[^>]*data-type="(\w+)"', _idx):
        _seg = _idx[_m.start():_m.start() + 3000]
        _a = re.search(r'href="(/(?:drops|guides)/[^"]+)"', _seg)
        if _a:
            FEED_TYPE.setdefault(_a.group(1), _TYPE.get(_m.group(1), "Drops & Brands"))
except FileNotFoundError:
    pass

def extract(path, url):
    h = open(path, encoding="utf-8", errors="ignore").read()
    t = re.search(r"<title>([^<]*)</title>", h)
    # strip the site suffix in either separator style ( — or | ) — 10 posts use the pipe
    title = re.sub(r"\s*[—|]\s*The Grassy Issue\s*$", "", html.unescape(t.group(1))).strip() if t else url
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = html.unescape(d.group(1)).strip() if d else ""
    # CATEGORY. This used to read <span class="drop-tag">[X]</span>, but those chips
    # were deliberately removed from every dedicated post header (2026-08). The regex
    # then matched nothing, everything fell through to the "Post" fallback, and that
    # mapped to "Field Notes" — so ALL 187 search results were labelled Field Notes.
    # Read the breadcrumb instead (it survived), and fall back to the homepage feed
    # card's data-type for the ~22 pages whose crumb carries no category.
    tag = None
    crumb = re.search(r'<div class="breadcrumb">(.*?)</div>', h, re.S)
    if crumb:
        ctext = html.unescape(re.sub(r"<[^>]+>", " ", crumb.group(1)))
        for c in ("Drops & Brands", "Field Notes", "News"):
            if c in ctext:
                tag = c; break
    if not tag:
        tag = FEED_TYPE.get(url)
    if not tag:
        tag = "Field Notes" if ("/guides/" in url or "field-guide" in url) else "Drops & Brands"
    # UNESCAPE. The tag is scraped straight out of the HTML, so it arrives as
    # "Drops &amp; Brands". The search overlay runs its own esc() over every field
    # before injecting, which double-escaped it to &amp;amp; and printed
    # "Drops &amp; Brands" in the results list. Store plain text; let the renderer escape.
    tag = html.unescape(tag).strip()
    # Every post is Field Notes, Drops & Brands or News — the three-category rule.
    # "Post" and "Guide" are fallbacks for pages with no drop-tag; map them so the
    # search results never show a label that exists nowhere else on the site.
    tag = {"Post": "Field Notes", "Guide": "Field Notes"}.get(tag, tag)
    img = re.search(r'src="(/images/[^"]+)"', h)
    img = img.group(1) if img else ""
    # product names as keywords
    names = re.findall(r'class="product-name">([^<]+)<', h)
    brands = re.findall(r'class="product-brand">([^<]+)<', h)
    kw = " ".join(html.unescape(x) for x in set(names + brands))
    return {"u": url, "t": title, "d": desc[:180], "g": tag, "i": img, "k": kw[:600]}

items = []
for f in sorted(glob.glob(f"{SITE}/drops/*.html")):
    slug = os.path.basename(f)[:-5]
    items.append(extract(f, f"/drops/{slug}"))
for f in sorted(glob.glob(f"{SITE}/guides/*.html")):
    slug = os.path.basename(f)[:-5]
    if slug != "index":
        items.append(extract(f, f"/guides/{slug}"))
for f in sorted(glob.glob(f"{SITE}/brands/*.html")):
    slug = os.path.basename(f)[:-5]
    if slug != "index":
        items.append(extract(f, f"/brands/{slug}"))

extra = [("field-guide/index.html", "/field-guide/"), ("brands/index.html", "/brands/"), ("events/index.html", "/events/"), ("guides/index.html", "/guides"), ("scoreboard.html", "/scoreboard")]
for rel, url in extra:
    p = f"{SITE}/{rel}"
    if os.path.exists(p):
        items.append(extract(p, url))

json.dump(items, open(f"{SITE}/search-index.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(f"indexed {len(items)} pages -> search-index.json")
