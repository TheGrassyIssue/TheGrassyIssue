#!/usr/bin/env python3
"""lean-pages.py — keep public pages lean on every deploy.

1) FONTS: stop public pages downloading fonts they never use.
25 September 2026. Lenny: "let's clean up the site so we can stay lean and fast"

The house type is Editor's Note Text (self-hosted), JetBrains Mono and Inter.
Fraunces was retired by apply-editors-note.py and Playfair Display was never
used on a public page, but both were still in the Google Fonts link on ~500
pages — two extra font families fetched on every visit for nothing.

This rewrites the Google Fonts request to Inter + JetBrains Mono only. It runs
on every deploy, so a post built from an old donor page ships lean anyway.

SKIPPED: stats.html and instagram-posts.html (noindex internal tools that still
set Fraunces directly), drafts/, research/, cloud-sync conflict copies.

2) LAZY IMAGES: any <img> with no loading attribute gets loading="lazy",
   except the first image on a page and anything marked hero / fetchpriority
   (those are the LCP image and must load straight away). 43 homepage carousel
   slides had no attribute, so the browser fetched every one of them before the
   page had even laid out.

Idempotent. Dry run by default; --apply to write.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SKIP_FILES = {"stats.html", "instagram-posts.html"}
SKIP_DIRS = {"drafts", "research", ".git", "node_modules"}
LEAN = "family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap"
URL = re.compile(r"(https://fonts\.googleapis\.com/css2\?)([^\"')]+)")


def fix_url(m):
    q = m.group(2)
    if "Fraunces" not in q and "Playfair" not in q:
        return m.group(0)
    # keep every other family exactly as requested (weights included)
    parts = re.split(r"&(?:amp;)?", q)
    keep = [x for x in parts if not re.match(r"family=(Fraunces|Playfair)", x)]
    if not any(x.startswith("family=") for x in keep):
        return m.group(1) + LEAN
    return m.group(1) + "&".join(keep)


IMG = re.compile(r"<img\b[^>]*>", re.I)


def lazy(s):
    out, seen = [], False
    pos = 0
    for m in IMG.finditer(s):
        out.append(s[pos:m.start()])
        t = m.group(0)
        if not seen:
            seen = True
            out.append(t)
        elif "loading=" in t or "hero" in t or "fetchpriority" in t:
            out.append(t)
        else:
            out.append(t[:4] + ' loading="lazy" decoding="async"' + t[4:])
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)


def main(apply):
    changed = 0
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or p.name in SKIP_FILES:
            continue
        if re.search(r" \d+\.html$", p.name) or "copy" in p.name:
            continue
        try:
            s = p.read_text(encoding="utf-8")
        except OSError:
            continue
        t = lazy(URL.sub(fix_url, s))
        if t != s:
            changed += 1
            if apply:
                p.write_text(t, encoding="utf-8")
    print(f"lean-pages: {changed} page(s) {'updated' if apply else 'would change'}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
