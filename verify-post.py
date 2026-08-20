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

    # --- images ---
    srcs = re.findall(r'src="(/images/[^"]+)"', h)
    miss = [s for s in srcs if not os.path.exists(root + s)]
    chk("all local images exist", not miss, str(miss[:4]))
    chk("no hot-linked images", not re.findall(r'src="https?://(?!thegrassyissue)', h))
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
    txt = re.sub(r'<[^>]+>', ' ', h)
    chk("no banned word 'worth'", not re.search(r'\bworth\b', txt, re.I))
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    words = len(html.unescape(re.sub(r'<[^>]+>', ' ', body)).split())
    chk("word count >= 1200", words >= 1200, str(words))
    print("\n  %s — %d check(s) failed\n" % (os.path.basename(path), len(fails)))
    return len(fails)

if __name__ == "__main__":
    sys.exit(min(1, sum(verify(p) for p in sys.argv[1:])))
