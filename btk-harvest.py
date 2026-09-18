#!/usr/bin/env python3
"""
btk-harvest.py — turn a browser sweep's URL list into a checked manifest.
18 September 2026.

The sweep itself runs in the browser (same-origin fetch across a brand's
sitemap, journal and pages), because that is the only way to read 16 pages of
a site in one round trip. It hands back a list of candidate image URLs. This
file is the second half: download them, measure them, throw out everything
that is not editorial photography, and write research/lifestyle/<slug>.json.

WHAT GETS THROWN OUT, AND WHY
-----------------------------
  too small          below 1400px wide a 1800px band is an upscale
  packshot           near-white border all round — a product on a sweep.
                     Lenny: IRL, lifestyle, blog or lookbook images. A
                     headcover on white is none of those.
  near-duplicate     brands re-crop the same frame for every collection tile;
                     identical aspect + near-identical average colour is
                     almost always the same photograph twice
  customer photos    review-widget domains (judge.me, yotpo, okendo, loox) are
                     customers' own images and not the brand's to license on

Originals are archived under research/btk/originals/<slug>/ and never deleted,
so a later recrop never needs the brand's CDN again.

USAGE
    python3 btk-harvest.py <slug> <prefix> <name1> <name2> ...
    python3 btk-harvest.py --from-json /tmp/sweep-<slug>.json
"""
import json, pathlib, sys, urllib.request
from PIL import Image, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent
MAN = ROOT / "research" / "lifestyle"
ARCH = ROOT / "research" / "btk" / "originals"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"}
MINW = 1400
BLOCKED = ("judge.me", "yotpo", "okendo", "loox", "review")


def packshot(im):
    w, h = im.size
    b = max(2, min(w, h) // 25)
    e = [im.crop((0, 0, w, b)), im.crop((0, h - b, w, h)),
         im.crop((0, 0, b, h)), im.crop((w - b, 0, w, h))]
    return sum(ImageStat.Stat(x.convert("L")).mean[0] for x in e) / 4 > 225


def signature(im):
    """Cheap near-duplicate key: aspect bucket + coarse average colour."""
    s = im.resize((4, 4), Image.BILINEAR).convert("RGB")
    px = [v for p in s.getdata() for v in p]
    return (round(im.width / im.height, 2),
            tuple(v // 24 for v in px))


def harvest(slug, urls):
    MAN.mkdir(parents=True, exist_ok=True)
    d = ARCH / slug
    d.mkdir(parents=True, exist_ok=True)
    kept, seen, stats = [], set(), {"small": 0, "packshot": 0, "dupe": 0,
                                    "failed": 0, "blocked": 0}
    for u in urls:
        if any(b in u.lower() for b in BLOCKED):
            stats["blocked"] += 1
            continue
        name = u.rsplit("/", 1)[-1][:90]
        p = d / name
        try:
            if not p.exists():
                data = urllib.request.urlopen(
                    urllib.request.Request(u, headers=UA), timeout=45).read()
                if len(data) < 30000:
                    stats["small"] += 1
                    continue
                p.write_bytes(data)
            im = Image.open(p).convert("RGB")
        except Exception:
            stats["failed"] += 1
            continue
        if im.width < MINW:
            stats["small"] += 1
            continue
        if packshot(im):
            stats["packshot"] += 1
            continue
        sig = signature(im)
        if sig in seen:
            stats["dupe"] += 1
            continue
        seen.add(sig)
        kept.append([u, im.width, im.height])

    out = {"brand": slug, "source": "site sweep 18 Sep 2026 — pages, journal, "
                                    "collections (editorial frames only)",
           "captured": "2026-09-18", "imgs": kept}
    if not kept:
        out["note"] = ("swept and kept nothing — every candidate was a packshot, "
                       "too small, or a duplicate. This brand needs a human "
                       "asking it for photography, not a cleverer scraper.")
    (MAN / f"{slug}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return kept, stats


if __name__ == "__main__":
    if sys.argv[1] == "--from-json":
        spec = json.loads(pathlib.Path(sys.argv[2]).read_text())
        urls = [spec["pre"] + n for n in spec["u"]] + spec.get("other", [])
        slug = spec["b"]
    else:
        slug, pre, names = sys.argv[1], sys.argv[2], sys.argv[3:]
        urls = [pre + n for n in names]
    k, s = harvest(slug, urls)
    print(f"  {slug:<24} kept {len(k):>3} of {len(urls):>3}   "
          + "  ".join(f"{a}={b}" for a, b in s.items() if b))
