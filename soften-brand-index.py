#!/usr/bin/env python3
"""soften-brand-index.py — soft gradient backgrounds for the /brands card images (1 Oct 2026).
Lenny: "Let's also update those stark white backgrounds on the brand index page".
Card images are shared with the posts they came from, so this never edits the original: it writes a softened
copy to /images/brand-index/<slug>.jpg (same method as soften-product-frames.py) and points that brand's "img"
in data/brands.json at the copy, which is the index builder's source of truth, so a rebuild keeps it.
Idempotent: brands already pointing at /images/brand-index/ are skipped. Dry run by default.
"""
import importlib.util, json, pathlib, re, shutil, sys
import numpy as np
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("soft", ROOT / "soften-product-frames.py")
soft = importlib.util.module_from_spec(spec); spec.loader.exec_module(soft)
# white products the flood fill bleeds into (checked by eye, 1 Oct 2026): leave these on white
SKIP = {"3-putt-round", "bluegrass-fairway", "pluto-golf", "owala", "payntr", "ripit-grips", "sunday-golf"}


def main(apply_):
    page = (ROOT / "brands/index.html").read_text(encoding="utf-8")
    cards = dict(re.findall(r'<a class="bc" href="/brands/([^"]+)"[^>]*>.*?<img src="([^"]+)"', page, re.S))
    data = json.loads((ROOT / "data/brands.json").read_text())
    out = ROOT / "images/brand-index"; out.mkdir(exist_ok=True)
    n = 0
    for b in data:
        img = b.get("img") or cards.get(b["slug"])
        if not img or img.startswith("/images/brand-index/") or b["slug"] in SKIP:
            continue
        a = np.asarray(Image.open(ROOT / img.lstrip("/")).convert("RGB")).astype(np.int16)
        if soft.bg_mask(a) is None:
            continue
        n += 1
        if apply_:
            dst = out / f'{b["slug"]}.jpg'
            shutil.copy(ROOT / img.lstrip("/"), dst)
            if soft.soften(dst) == "soft":
                b["img"] = f'/images/brand-index/{b["slug"]}.jpg'
            else:
                dst.unlink()
    print(f"  {n} card images with white studio backgrounds" + ("" if apply_ else " (dry run — pass --apply)"))
    if apply_:
        (ROOT / "data/brands.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
if __name__ == "__main__":
    main("--apply" in sys.argv)
