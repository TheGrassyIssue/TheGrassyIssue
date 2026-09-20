#!/usr/bin/env python3
"""localize-muni-kids.py — pull the 18 Muni Kids product shots local. 20 Sept 2026.

House rule: every product image is downloaded and served from our own origin.
Nothing hot-links to a brand CDN — their URLs carry ?v= cache-busters that change
whenever they re-upload, and a roundup whose pictures silently vanish is worse
than one that never had them.

SIZING. Gate on max(im.size), not width. The version of this that checked width
alone let tall portrait shots through at full height, because a 900x1600 frame
has a width under the cap and a height way over it. Two of the Muni Kids shots
are portrait.

FORMAT. Their CDN mixes .webp, .png and .jpg in the same catalogue. Everything is
normalised to RGB JPEG so the page has one decode path; PNGs with alpha are
flattened onto white, which is what their product shots sit on anyway.

Idempotent: skips a file that already exists at the right size. Dry run default.
"""
import io, json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "research/muni-kids.json"
OUT = ROOT / "images/muni-kids"
MAXPX = 1400
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}


def main(apply_):
    from PIL import Image
    rows = json.loads(SRC.read_text(encoding="utf-8"))["rows"]
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)

    done, skipped, failed = [], [], []
    for slug, name, cat, price, mode, url, img in rows:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug)
            continue
        if not apply_:
            done.append((slug, "would fetch", ""))
            continue
        try:
            req = urllib.request.Request(img, headers=UA)
            raw = urllib.request.urlopen(req, timeout=45).read()
            im = Image.open(io.BytesIO(raw))
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA")
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            before = im.size
            if max(im.size) > MAXPX:                 # max(), not width
                r = MAXPX / max(im.size)
                im = im.resize((round(im.width * r), round(im.height * r)),
                               Image.LANCZOS)
            im.save(dest, "JPEG", quality=88, optimize=True)
            done.append((slug, f"{before[0]}x{before[1]}", f"{im.width}x{im.height}"))
        except Exception as e:
            failed.append((slug, str(e)[:70]))

    for s, a, b in done:
        print(f"  ok    {s:26} {a} -> {b}" if b else f"  ok    {s:26} {a}")
    for s in skipped:
        print(f"  skip  {s:26} already local")
    for s, e in failed:
        print(f"  FAIL  {s:26} {e}")

    if failed:
        sys.exit(f"\n! {len(failed)} image(s) failed — refusing to call this done")
    if apply_:
        have = {p.stem for p in OUT.glob("*.jpg")}
        want = {r[0] for r in rows}
        missing = want - have
        if missing:
            sys.exit(f"\n! missing after run: {sorted(missing)}")
        print(f"\n  {len(want)}/{len(rows)} images local in images/muni-kids/")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
