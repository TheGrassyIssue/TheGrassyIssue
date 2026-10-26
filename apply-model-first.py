#!/usr/bin/env python3
"""apply-model-first.py — product galleries lead with an on-model photo. 25 Oct 2026.
Lenny: "on the most recent posts, lets lead with more images of the products on the models."
For each product card on the posts in POSTS, the gallery frames are reordered so the first on-model frame (a person
wearing the piece) comes first; the rest keep their order. On-model is judged by skin-tone coverage in the frame
(YCbCr skin range), cached in data/model-first.json, with hand overrides in OVERRIDE. Cards with no on-model frame
are left alone. Idempotent; runs in Deploy TGI.command before apply-gallery-wrap. Dry run by default.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS = ["drops/east-coast-vs-west-coast-golf-brands.html", "drops/golf-capsule-wardrobe.html", "drops/brand-revisited-water-when-dry.html",
         "drops/golf-fabrics-merino-ripstop-corduroy.html", "drops/new-golf-drops-malbon-gumtree-mogshade.html"]
CACHE = os.path.join(ROOT, "data/model-first.json")
THRESH = 0.035
# image path -> True (on-model) / False (not), where the skin measure gets it wrong
OVERRIDE = {
 "/images/capsule-wardrobe/cl3-4.jpg": False,
 "/images/capsule-wardrobe/cl10-2.jpg": False,
 "/images/capsule-wardrobe/to4-2.jpg": False,
 "/images/capsule-wardrobe/to9-3.jpg": False,
 "/images/water-when-dry-revisit/pants-2.jpg": False,
 "/images/water-when-dry-revisit/cap-2.jpg": False,
 "/images/water-when-dry-revisit/swim-2.jpg": False,
 "/images/fabrics/p-R37-3.jpg": False,
 "/images/fabrics/p-R33-3.jpg": False,
 "/images/new-drops-oct23/p-m9-2.jpg": False,
 "/images/new-drops-oct23/p-m10-2.jpg": False,
 "/images/new-drops-oct23/p-m11-2.jpg": False,
 "/images/new-drops-oct23/p-g6-3.jpg": False,
 "/images/new-drops-oct23/p-g9-2.jpg": False,
 "/images/capsule-wardrobe/to4-4.jpg": True,
 "/images/capsule-wardrobe/ou6-3.jpg": True,
 "/images/capsule-wardrobe/co9-5.jpg": True,
 "/images/fabrics/p-R20-3.jpg": True,
 "/images/new-drops-oct23/p-m7-2.jpg": True,
 "/images/capsule-wardrobe/cl4-3.jpg": True,
 "/images/capsule-wardrobe/cl4-1.jpg": False,
 "/images/capsule-wardrobe/cl4-2.jpg": False,
 "/images/water-when-dry-revisit/hoodie-3.jpg": True,
 "/images/water-when-dry-revisit/fleece-3.jpg": True,
 "/images/water-when-dry-revisit/fleece-1.jpg": False,
 "/images/water-when-dry-revisit/fleece-2.jpg": False,
}  # False: close-ups, packshots and caps that read as skin tone; True: model shots with little skin showing (25 Oct check)


def skin(path):
    import numpy as np  # only needed for frames not yet in the cache; the deploy Mac may not have numpy
    from PIL import Image
    im = Image.open(os.path.join(ROOT, path.lstrip("/"))).convert("YCbCr").resize((250, 312))
    a = np.asarray(im).astype(int); y, cb, cr = a[..., 0], a[..., 1], a[..., 2]
    m = (cb >= 80) & (cb <= 125) & (cr >= 138) & (cr <= 170) & (y > 45)
    return round(float(m.mean()), 4)


def main(apply_):
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    moved = 0
    for rel in POSTS:
        p = os.path.join(ROOT, rel); s = open(p, encoding="utf-8").read(); orig = s
        def fix(m):
            nonlocal moved
            track = m.group(1)
            frames = re.findall(r'<div class="pg-frame">.*?</div>', track, re.S)
            if len(frames) < 2: return m.group(0)
            srcs = [re.search(r'src="([^"]+)"', f).group(1) for f in frames]
            def on(src):
                if src in OVERRIDE: return OVERRIDE[src]
                if src not in cache:
                    try: cache[src] = skin(src)
                    except ImportError: return False
                return cache[src] >= THRESH
            flags = [on(x) for x in srcs]
            if flags[0] or not any(flags): return m.group(0)
            k = flags.index(True)
            order = [k] + [i for i in range(len(frames)) if i != k]
            new = [frames[i] for i in order]
            # keep the "view n of N" alt numbering in display order
            n = len(new)
            new = [re.sub(r'view \d+ of \d+', f'view {j+1} of {n}', f) for j, f in enumerate(new)]
            moved += 1
            return m.group(0).replace(track, "".join(new))
        s = re.sub(r'<div class="pg-track">(.*?)</div><button class="pg-arw prev"', lambda m: fix(m), s, flags=re.S)
        if s != orig and apply_: open(p, "w", encoding="utf-8").write(s)
    json.dump(cache, open(CACHE, "w"), indent=0)
    print(f"apply-model-first: {moved} card(s) {'reordered' if apply_ else 'would reorder'} across {len(POSTS)} posts")


if __name__ == "__main__":
    main("--apply" in sys.argv)
