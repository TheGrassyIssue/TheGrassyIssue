#!/usr/bin/env python3
"""Verify a TGI drop page against house format. Usage: python3 verify-post.py drops/foo.html"""
import re, sys, os, json, html

def match_div(s, i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return i + m.end()
    return -1

def verify(path):
    root = os.path.dirname(os.path.abspath(__file__))
    h = open(path, encoding="utf-8").read()
    fails = []
    def chk(name, ok, detail=""):
        print(("  OK   " if ok else "  FAIL ") + name + (("  " + detail) if detail and not ok else ""))
        if not ok: fails.append(name)

    # --- HOUSE FORMAT (the rule that broke Malbon + Lottery Round, 2026-08-20) ---
    grids = list(re.finditer(r'<div class="products-grid">', h))
    cards = list(re.finditer(r'<div class="product-card', h))
    spans = [(m.start(), match_div(h, m.start())) for m in grids]
    outside = [c.start() for c in cards if not any(a < c.start() < b for a, b in spans)]
    chk("every product-card sits inside a .products-grid", not outside,
        "%d card(s) outside the grid — they will render full-width and oversized" % len(outside))
    chk("at least one .products-grid present", bool(grids) or not cards)

    # EVERY class used in the body must have a CSS rule somewhere on the page.
    # Inventing a class name renders it completely unstyled — this has now bitten
    # three times (spec-table on the wedge post, products-grid + faq-item here).
    # NB: these pages carry SEVERAL <style> blocks — concatenate them all, and strip
    # them out before collecting used classes.
    css = "\n".join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
    body_html = re.sub(r'<style[^>]*>.*?</style>', ' ', h, flags=re.S)
    used = set()
    for attr in re.findall(r'class="([^"]+)"', body_html):
        used.update(attr.split())
    styled = set(re.findall(r'\.([A-Za-z][\w-]*)', css))
    # classes only ever targeted by JS/structure, not styling
    # more-kicker/more-title are unstyled across the whole site (pre-existing, not introduced here)
    EXEMPT = {"faq", "products", "more-grid", "more-kicker", "more-title"}
    unstyled = sorted(c for c in used if c not in styled and c not in EXEMPT)
    chk("every class used has a CSS rule", not unstyled, str(unstyled))

    # --- structure ---
    chk("div balance", h.count("<div") == h.count("</div>"), "%d/%d" % (h.count("<div"), h.count("</div>")))
    chk("section balance", h.count("<section") == h.count("</section>"),
        "%d/%d" % (h.count("<section"), h.count("</section>")))
    chk("anchor balance", len(re.findall(r'<a\b', h)) == h.count("</a>"))
    chk("exactly one h1", len(re.findall(r'<h1', h)) == 1)

    # --- galleries ---
    bad = []
    for m in re.finditer(r'<div class="product-card[^"]*" data-frames="(\d+)">', h):
        blk = h[m.start():match_div(h, m.start())]
        if int(m.group(1)) != blk.count('class="pg-frame"'): bad.append(m.group(1))
    chk("data-frames matches actual pg-frame count", not bad, str(bad))

    # Gallery CONTROLS. The page ships JS that drives .pg-dot / .pg-arw / .pg-count; a gallery
    # with 2+ frames must emit all three or the controls silently do nothing. Bare <span> dots
    # (no class) render invisible — that shipped on four posts before this check existed.
    ctl = []
    for m in re.finditer(r'<div class="product-card[^"]*" data-frames="(\d+)">', h):
        n = int(m.group(1)); blk = h[m.start():match_div(h, m.start())]
        dots = len(re.findall(r'<button class="pg-dot[^"]*"', blk))
        cnt = re.search(r'<span class="pg-count">1/(\d+)</span>', blk)
        arw = blk.count('class="pg-arw')
        if n < 2:
            good = dots == 0
        else:
            good = (dots == n and cnt and int(cnt.group(1)) == n
                    and arw == 2 and blk.count('class="pg-dot on"') == 1)
        if not good: ctl.append(n)
    chk("gallery controls complete (dots/arrows/counter)", not ctl,
        "%d gallery(s) wrong — frames %s" % (len(ctl), ctl[:5]))
    chk("no classless <span> dots", '<div class="pg-dots"><span>' not in h)

    # --- images ---
    srcs = re.findall(r'src="(/images/[^"]+)"', h)
    miss = [s for s in srcs if not os.path.exists(root + s)]
    chk("all local images exist", not miss, str(miss[:4]))
    # only <img> tags — third-party <script src> (analytics) is expected and allowed
    chk("no hot-linked images",
        not [i for i in re.findall(r'<img[^>]*>', h)
             if re.search(r'src="https?://(?!thegrassyissue)', i)])
    imgs = re.findall(r'<img[^>]*>', h)
    chk("every img has alt", all('alt="' in i for i in imgs), "%d imgs" % len(imgs))

    # --- metadata / schema ---
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    parsed = []
    for j in lds:
        try: parsed.append(json.loads(j))
        except Exception as e: fails.append("JSON-LD parse"); print("  FAIL JSON-LD parse", e)
    chk("JSON-LD blocks parse", len(parsed) == len(lds))
    slug = os.path.basename(path).replace(".html", "")
    can = re.search(r'<link rel="canonical"[^>]*>', h)
    chk("canonical points at this slug", bool(can) and slug in can.group(0))

    # --- editorial rules ---
    # strip tags first so hrefs/slugs (e.g. the legacy 10-texas-courses-worth-the-trip)
    # don't trip the ban — it applies to prose, not to historical URLs.
    # Drop the More-from-Feed and Instagram strips BEFORE the prose checks. Those
    # cards are auto-generated navigation — their text is another post's TITLE, not
    # copy written for this page. Eight legacy posts still have "worth" in their
    # titles (Lenny declined retitling), so once fix-more-from-feed.py reshuffled
    # which posts each page links to, twelve pages started failing the ban for
    # linking to them. Same principle as the URL strip below: the rule is about
    # prose, not about pointers to things that already exist.
    txt = re.sub(r'<section class="more">.*?</section>', ' ', h, flags=re.S)
    txt = re.sub(r'<a[^>]*class="more-card".*?</a>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = re.sub(r'https?://\S+|/[\w/-]+', ' ', txt)
    # place names containing "Worth" are not the banned word (Fort Worth, Worth Avenue...)
    txt = re.sub(r'\bFort\s+Worth\b', ' ', txt, flags=re.I)
    chk("no banned word 'worth'", not re.search(r'\bworth\b', txt, re.I))
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    words = len(html.unescape(re.sub(r'<[^>]+>', ' ', body)).split())
    # more-cards must use the styled structure — .more-kicker/.more-title have no CSS
    mc = re.findall(r'<a[^>]*class="more-card".*?</a>', h, re.S)
    chk("more-cards carry an image and use .more-card-img/-body",
        all('more-card-img' in c and '<img' in c for c in mc))
    # the sidebar must be nested INSIDE .writeup — if .writeup closes early the
    # sidebar overlaps the first section instead of sitting beside the copy
    _w = h.find('<div class="writeup">')
    _a = h.find('<aside class="sidebar">')
    _depth = None
    if _w >= 0 and _a > _w:
        _d = 0
        for _m in re.finditer(r'<div\b[^>]*>|</div>', h[_w:_a]):
            _d += 1 if _m.group(0).startswith('<div') else -1
        _depth = _d
    chk("sidebar is nested inside .writeup (not closed early)",
        _depth is None or _depth >= 1)
    chk("no legacy .more-kicker/.more-title markup",
        'more-kicker' not in h and 'more-title' not in h)
    chk("word count >= 1200", words >= 1200, str(words))
    print("\n  %s — %d check(s) failed\n" % (os.path.basename(path), len(fails)))
    return len(fails)

if __name__ == "__main__":
    sys.exit(min(1, sum(verify(p) for p in sys.argv[1:])))
