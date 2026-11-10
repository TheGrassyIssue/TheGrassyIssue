#!/usr/bin/env python3
"""apply-gift-guide-links.py — a "2026 Gift Guide" strip on related posts, linking the three parts. 9 November 2026.
Lenny: "now we need to promote this post and get it more eyes on". Puts a compact strip right after each post's hero
image, pointing readers (and crawlers) at the part of the guide that matches the post, with the other two alongside.
Idempotent (marker-wrapped, replaced on rerun); runs every deploy so a post rebuild cannot drop it. Dry run by default.
Take it down after the holidays by emptying POSTS and running once with --apply (the strips are then removed).
"""
import os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
G = {1: ("golf-gift-guide-2026-everyday-range-rat-stocking-stuffers", "Part 1", "Everyday upgrades, range rat gifts and stocking stuffers"),
     2: ("golf-gift-guide-2026-statement-pieces-colorways-splurges", "Part 2", "Statement pieces, fresh colorways and splurges"),
     3: ("golf-gift-guide-2026-heirlooms-tiny-makers-off-season", "Part 3", "Heirlooms, tiny makers and off-season gifts")}
POSTS = {  # post slug -> the part that matches it best
    "small-golf-accessories-small-things-big-impact": 1, "the-ball-marker-atlas": 1, "10-indie-ball-marker-brands-worth-knowing": 1,
    "7-divot-tools-actually-worth-carrying": 1, "the-alignment-stick-edit": 1, "around-the-greens-short-game-kit": 1,
    "golf-bag-accessories-what-to-hang-from-your-bag": 1, "accessories-on-and-off-the-course": 1,
    "fall-golf-colorways-2026": 2, "loud-on-purpose-headcovers": 2, "the-driver-headcover-edit": 2, "favorite-golf-collabs-november-2026": 2,
    "fyfe-x-mackenzie-every-edition": 2, "golf-hats-and-nalgenes": 2, "the-camo-edit": 2,
    "best-quiet-luxury-golf-brands": 3, "small-golf-club-makers-putters-irons-drivers": 3, "the-fall-hoodie-edit-2026": 3,
    "golf-pullovers-fall-layer": 3, "golf-capsule-wardrobe": 3, "the-bag-edit-6-bags-for-golfers-who-care-what-they-carry": 3,
    "home-golf-decor-edit": 3,
}
M0, M1 = "<!-- TGI-GIFTGUIDE-STRIP -->", "<!-- /TGI-GIFTGUIDE-STRIP -->"
CSS = ('<style>/*TGI-GG-STRIP*/.gg-strip{max-width:1180px;margin:28px auto 0;padding:18px 22px;border:1px solid rgba(20,20,20,.16);'
       'display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;background:rgba(45,74,43,.06)}'
       '.gg-strip .gg-k{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2d4a2b;flex:0 0 auto}'
       '.gg-strip .gg-t{flex:1 1 320px;font-size:15px;line-height:1.5;margin:0}.gg-strip .gg-ps{display:flex;flex-wrap:wrap;gap:8px}'
       '.gg-strip .gg-ps a{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.1em;text-transform:uppercase;padding:6px 10px;'
       'border:1px solid rgba(20,20,20,.25);text-decoration:none;border-bottom:1px solid rgba(20,20,20,.25)}'
       '.gg-strip .gg-ps a.gg-best{background:#2d4a2b;color:#f4efe4;border-color:#2d4a2b}</style>')
def strip(part):
    slug, label, desc = G[part]
    best = ' class="gg-best"'
    links = "".join(f'<a href="/drops/{s}"{best if n == part else ""}>{l}</a>' for n, (s, l, _) in G.items())
    return (f'{M0}{CSS}<aside class="gg-strip" aria-label="2026 Gift Guide"><span class="gg-k">The 2026 Gift Guide</span>'
            f'<p class="gg-t">Shopping for a golfer? <a href="/drops/{slug}">{label}: {desc}</a> picks up where this post leaves off. '
            f'Ninety independent brands across three parts.</p><span class="gg-ps">{links}</span></aside>{M1}')
def after_hero(h):
    i = h.find('class="drop-hero"')
    if i < 0: return None
    start = h.rfind("<div", 0, i); depth = 0
    for m in re.finditer(r"<div\b|</div>", h[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0: return start + m.end()
    return None
apply_ = "--apply" in sys.argv; n = 0
for f in sorted(os.listdir(os.path.join(ROOT, "drops"))):
    if not f.endswith(".html") or " " in f: continue
    p = os.path.join(ROOT, "drops", f); h = open(p, encoding="utf-8").read(); orig = h
    h = re.sub(re.escape(M0) + ".*?" + re.escape(M1), "", h, flags=re.S)
    slug = f[:-5]
    if slug in POSTS:
        j = after_hero(h)
        if j is None: print("  ! no hero on", slug); continue
        h = h[:j] + "\n" + strip(POSTS[slug]) + "\n" + h[j:]; n += 1
    if h != orig and apply_: open(p, "w", encoding="utf-8").write(h)
print(f"  gift guide strip on {n} posts" + ("" if apply_ else " — dry run, pass --apply"))
