#!/usr/bin/env python3
"""Build /search-index.json from all TGI pages. Run after adding posts, then deploy."""
import re, json, html, glob, os

SITE = os.path.dirname(os.path.abspath(__file__))

def extract(path, url):
    h = open(path, encoding="utf-8", errors="ignore").read()
    t = re.search(r"<title>([^<]*)</title>", h)
    # strip the site suffix in either separator style ( — or | ) — 10 posts use the pipe
    title = re.sub(r"\s*[—|]\s*The Grassy Issue\s*$", "", html.unescape(t.group(1))).strip() if t else url
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = html.unescape(d.group(1)).strip() if d else ""
    tag = re.search(r'<span class="drop-tag[^"]*">\[([^\]]+)\]</span>', h)
    tag = tag.group(1) if tag else ("Guide" if "/guides/" in url or "field-guide" in url else "Post")
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
extra = [("field-guide/index.html", "/field-guide/"), ("events/index.html", "/events/"), ("guides/index.html", "/guides"), ("scoreboard.html", "/scoreboard")]
for rel, url in extra:
    p = f"{SITE}/{rel}"
    if os.path.exists(p):
        items.append(extract(p, url))

json.dump(items, open(f"{SITE}/search-index.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(f"indexed {len(items)} pages -> search-index.json")
