#!/usr/bin/env python3
"""Fill data/post-thumbs.json for every post the brand pages link to.

WHY: build-brands.py draws each brand page's post cards from post-thumbs.json
(url -> {img, cat}). Nothing regenerated that file when posts were added, so
by 2026-09-14 29 mentioned posts had no entry and 204 cards on 126 brand pages
were the striped "no thumb" placeholder (Lenny: "some images are not working,
like on /brands/jlindeberg"). Run this BEFORE build-brands.py, every time.

Derivation, in order (same rule the memo recorded): the page's .drop-hero-img,
else the first .pg-frame gallery image, else the first /images/ <img> in the
body that is not a nav/wordmark/More-from-Feed asset. Category comes from the
page's own kicker ("Drops & Brands" / "Field Notes" / "News"). Existing
entries are never overwritten unless --refresh. Dry run by default.
"""
import json, re, os, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
TP = os.path.join(ROOT, "data", "post-thumbs.json")
thumbs = json.load(open(TP, encoding="utf-8"))
mm = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json"), encoding="utf-8"))
urls = sorted({e["url"] for v in mm.values() for e in v} | {"/drops/" + os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, "drops", "*.html"))})

CATS = ["Drops & Brands", "Field Notes", "News"]
def derive(url):
    p = os.path.join(ROOT, url.lstrip("/") + ".html")
    if not os.path.exists(p): return None
    h = open(p, encoding="utf-8").read()
    body = h[h.find("<body"):]
    body = re.sub(r'<section class="more".*', "", body, flags=re.S)          # More from the Feed
    body = re.sub(r'<nav.*?</nav>', "", body, flags=re.S)
    img = None
    m = re.search(r'<div class="drop-hero-img">\s*<img[^>]+src="([^"]+)"', body)
    if m: img = m.group(1)
    if not img:
        m = re.search(r'<div class="pg-frame">\s*<img[^>]+src="([^"]+)"', body)
        if m: img = m.group(1)
    if not img:
        for s in re.findall(r'<img[^>]+src="(/images/[^"]+)"', body):
            if not re.search(r'wordmark|logo|icon|weather|ig-crops', s): img = s; break
    if img: img = re.sub(r"^(\.\./)+", "/", img)              # fella-golf hero uses ../images/…
    if not img or not os.path.exists(os.path.join(ROOT, img.lstrip("/"))): return None
    cat = next((c for c in CATS if re.search(r'<span>' + re.escape(c).replace(r'\&', r'(?:&amp;|&)') + r'</span>', body)), None)
    if not cat:
        m = re.search(r'<a href="/#feed">([^<]+)</a>', body)
        cat = (m.group(1).replace("&amp;", "&") if m else "Drops & Brands")
    return {"img": img, "cat": cat}

added, refreshed, failed = [], [], []
for u in urls:
    if u in thumbs and "--refresh" not in sys.argv: continue
    d = derive(u)
    if d: (refreshed if u in thumbs else added).append(u); thumbs[u] = d
    else: failed.append(u)

print(f"{len(urls)} post urls · {len(added)} added · {len(refreshed)} refreshed · {len(failed)} no image/page")
for u in added: print("  +", u, thumbs[u]["img"], "·", thumbs[u]["cat"])
for u in failed: print("  !!", u)
if "--apply" in sys.argv:
    json.dump(dict(sorted(thumbs.items())), open(TP, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"wrote {TP} ({len(thumbs)} entries)")
else:
    print("(dry run — pass --apply)")
