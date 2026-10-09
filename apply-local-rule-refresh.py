#!/usr/bin/env python3
"""Local Rule Brand to Know: turn every product card into a multi-image gallery (Local Rule's own store images).
Idempotent. Copy, SEK prices and Swedish quotes are untouched. Rerun after build-local-rule.py (which would undo this).
Frames: research/local-rule-refresh/frame.py -> images/local-rule/g/, listed in research/local-rule-refresh/frames.json."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "drops/brand-to-know-local-rule.html")
FR = json.load(open(os.path.join(ROOT, "research/local-rule-refresh/frames.json")))

def main(apply_):
    s = open(F, encoding="utf-8").read(); o = s
    donor = open(os.path.join(ROOT, "drops/brand-to-know-manors.html"), encoding="utf-8").read()
    js = [m.group(0) for m in re.finditer(r"<script>.*?</script>", donor, re.S) if "pg-track" in m.group(0)][0]
    js = js.replace("<script>", '<script id="tgi-lr-gallery-js">', 1)
    def repl(m):
        card = m.group(0)
        h = re.search(r'local-rule\.com/products/([a-z0-9-]+)', card).group(1)
        fr = FR[h]
        name = re.search(r'<div class="product-name">(.*?)</div>', card).group(1)
        alt = re.sub(r"\s*&middot;.*$", "", re.sub(r"<[^>]+>", "", name)).replace("&amp;", "&").replace("&", "&amp;")
        imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="Local Rule &mdash; {alt} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        gal = (f'<div class="product-gallery"><div class="pg-track">{imgs}</div>'
               f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>')
        card = re.sub(r'<img src="/images/local-rule/[^"]*" alt="[^"]*" loading="lazy" />|<div class="product-gallery">.*?<div class="pg-dots">.*?</div></div>', gal, card, count=1, flags=re.S)
        card = re.sub(r'<div class="product-card"( data-frames="\d+")? id="(p-\d+)">', rf'<div class="product-card" data-frames="{len(fr)}" id="\2">', card, count=1)
        return card
    s, n = re.subn(r'<div class="product-card"[^>]*id="p-\d+">.*?class="product-link">.*?</a>', repl, s, flags=re.S)
    s = re.sub(r'<script id="tgi-lr-gallery-js">.*?</script>\n?', '', s, flags=re.S)
    k = s.rfind("</body>"); s = s[:k] + js + "\n" + s[k:]
    assert n == 18, n
    assert s.count('class="product-gallery"') == 18, s.count('class="product-gallery"')
    print(f"apply-local-rule-refresh: {n} cards -> galleries ({sum(len(v) for v in FR.values())} frames); {'updated' if s != o else 'unchanged'}")
    if apply_ and s != o:
        open(F, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    main("--apply" in sys.argv)
