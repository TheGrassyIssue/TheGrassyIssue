#!/usr/bin/env python3
"""rotate-more-from-tgi.py — keep every post's "More from TGI" boxes fresh and rotating,
favouring newer posts. 29 Sep 2026. Lenny: "Make sure the more from TGI boxes are fresh for
each post and always rotating, favor newer posts for those boxes".

WHAT WAS WRONG. New posts are built from a donor page and inherited its four More cards, so
18 posts all showed the identical Swag / Hancock / Devereux / Nikes row.

THREE PARTS, all idempotent, run on every deploy:
 1. data/more-pool.json  every post with a title, image, category and publish date.
 2. STATIC fallback      any post whose four cards duplicate another post's (the donor
    problem) gets its own set, drawn with a recency weighting and seeded by its slug, so it
    is stable between deploys (no fake lastmod churn) and crawlers still see varied links.
 3. ROTATION             /assets/js/more-rotate.js, injected into every page with a
    more-grid, redraws the four cards on each page view from the pool: newest posts
    weighted most (half-life 21 days), never the page itself, at least one post from the
    last two weeks, mixed categories. Static HTML stays as the no-JS / crawler version.
Dry run by default; --apply to write.
"""
import glob, html, json, math, os, random, re, subprocess, sys, datetime, collections
ROOT = os.path.dirname(os.path.abspath(__file__))
TAG = '<script src="/assets/js/more-rotate.js" defer></script>'
TYPE = {"drop": "Drops &amp; Brands", "field": "Field Notes", "news": "News", "guide": "Field Notes", "score": "Field Notes"}
GENERIC = "/images/og-image.jpg"
TODAY = datetime.date.today()

def feed_kinds():
    s = open(os.path.join(ROOT, "index.html"), encoding="utf-8", errors="replace").read()
    out = {}
    for m in re.finditer(r'<div class="card" data-type="([a-z]+)"', s):
        seg = s[m.start():m.start() + 5000]
        h = re.search(r'href="(/drops/[^"#?]+)"', seg); im = re.search(r'<img[^>]+src="(/images/[^"]+)"', seg)
        if h: out.setdefault(h.group(1), (m.group(1), im.group(1) if im else None))
    return out

def git_added(rel):
    try:
        o = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cs", "--", rel], cwd=ROOT,
                           capture_output=True, text=True, timeout=20).stdout.split()
        return o[-1] if o else None
    except Exception:
        return None

def pool():
    kinds = feed_kinds(); thumbs = {}
    try: thumbs = json.load(open(os.path.join(ROOT, "data/post-thumbs.json")))
    except Exception: pass
    P = []
    for f in sorted(glob.glob(os.path.join(ROOT, "drops", "*.html"))):
        if " " in os.path.basename(f): continue
        s = open(f, encoding="utf-8", errors="replace").read()
        if re.search(r'name=["\']robots["\'][^>]*noindex', s): continue
        slug = "/drops/" + os.path.basename(f)[:-5]
        t = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip()) if t else ""
        if not title: continue
        kind, card_img = kinds.get(slug, ("drop", None))
        img = (thumbs.get(slug) or {}).get("img")
        if not img:
            m = re.search(r'<div class="drop-hero-img">\s*<img[^>]+src="([^"]+)"', s); img = m.group(1) if m else None
        if not img:
            m = re.search(r'<div class="product-card"[^>]*>.*?<img[^>]+src="([^"]+)"', s, re.S); img = m.group(1) if m else card_img
        if not img or img == GENERIC or not os.path.exists(os.path.join(ROOT, img.lstrip("/"))): continue
        d = re.search(r'"datePublished":\s*"(\d{4}-\d\d-\d\d)', s)
        d = d.group(1) if d else git_added(os.path.relpath(f, ROOT)) or "2026-01-01"
        P.append({"u": slug, "t": title, "i": img, "k": TYPE.get(kind, "Drops &amp; Brands"), "d": d})
    P.sort(key=lambda x: x["d"], reverse=True)
    return P

def weight(d):
    age = max(0, (TODAY - datetime.date.fromisoformat(d)).days)
    return 0.04 + 0.5 ** (age / 21)

def pins():
    # Pinned cards (1 Oct 2026, Lenny on Local GC: "add [The Bird Edit] to the more from TGI section").
    # data/more-pins.json maps a page slug to post URLs that always lead its More from TGI grid.
    try:
        return json.load(open(os.path.join(ROOT, "data/more-pins.json")))
    except FileNotFoundError:
        return {}

def pick(P, self_slug, n=4, seed=None, pinned=()):
    rnd = random.Random(seed or self_slug)
    cand = [p for p in P if p["u"] != self_slug]
    out = [p for u in pinned for p in cand if p["u"] == u]
    fresh = [p for p in cand if (TODAY - datetime.date.fromisoformat(p["d"])).days <= 14 and p not in out]
    if fresh and len(out) < n: out.append(rnd.choice(fresh))
    while len(out) < n:
        rest = [p for p in cand if p not in out]
        kinds = collections.Counter(p["k"] for p in out)
        w = [weight(p["d"]) / (1 + kinds[p["k"]] * 0.6) for p in rest]
        out.append(rnd.choices(rest, weights=w, k=1)[0])
    return out

def cards(ps):
    return "\n".join(
        f'    <a href="{p["u"]}" class="more-card">\n'
        f'      <div class="more-card-img"><img src="{p["i"]}" alt="{html.escape(p["t"], quote=True)}" loading="lazy" /></div>\n'
        f'      <div class="more-card-body"><div class="more-card-name">{html.escape(p["t"], quote=False)}</div>'
        f'<div class="more-card-tag">{p["k"]}</div></div>\n    </a>' for p in ps)

def grid_span(s):
    m0 = re.search(r'<div class="more-grid"[^>]*>', s)
    i = m0.start() if m0 else -1
    if i < 0: return None
    depth, j = 0, i; tag = re.compile(r"<div\b|</div>")
    while True:
        m = tag.search(s, j)
        if not m: return None
        depth += -1 if m.group(0) == "</div>" else 1; j = m.end()
        if depth == 0: return i, j

def main(apply_):
    P = pool()
    if apply_:
        json.dump(P, open(os.path.join(ROOT, "data/more-pool.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    pages = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if " " not in f and "/drafts/" not in f and "/research/" not in f and "/previews/" not in f]
    grids = {}
    for f in pages:
        s = open(f, encoding="utf-8", errors="replace").read()
        if '<div class="more-grid"' in s:
            sp = grid_span(s)
            grids[f] = tuple(re.findall(r'<a href="([^"]+)" class="more-card"', s[sp[0]:sp[1]])) if sp else ()
    dupcount = collections.Counter(grids.values())
    fixed = injected = 0
    PIN = pins()
    for f, hrefs in grids.items():
        s = open(f, encoding="utf-8").read(); o = s
        slug = "/" + os.path.relpath(f, ROOT)[:-5]
        pin = PIN.get(slug, [])
        open_tag = '<div class="more-grid"' + (f' data-pin="{",".join(pin)}"' if pin else "") + '>'
        if dupcount[hrefs] > 1 or slug in hrefs or len(hrefs) < 4 or tuple(hrefs[:len(pin)]) != tuple(pin) or open_tag not in s:
            sp = grid_span(s)
            s = s[:sp[0]] + open_tag + '\n' + cards(pick(P, slug, pinned=pin)) + "\n  </div>" + s[sp[1]:]
            fixed += 1
        if TAG not in s:
            k = s.rfind("</body>")
            if k > 0: s = s[:k] + TAG + "\n" + s[k:]; injected += 1
        if s != o and apply_:
            open(f, "w", encoding="utf-8").write(s)
    print(f"more-from-tgi: pool {len(P)} posts (newest {P[0]['d']}), pages with grid {len(grids)}, "
          f"duplicate/self grids re-drawn {fixed}, rotation script added to {injected}")
    if not apply_: print("  dry run — pass --apply")

if __name__ == "__main__":
    main("--apply" in sys.argv)
