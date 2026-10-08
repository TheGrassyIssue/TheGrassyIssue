#!/usr/bin/env python3
"""stamp-field-guide-date.py — keep the Field Guide's "updated" date honest and current.
29 Sep 2026. Lenny: "let's update the updated date on the field guide- I want SEOs to
know it's regularly updated".

Runs in Deploy TGI.command before stamp-sitemap-lastmod. If field-guide/index.html has
changes not yet committed (i.e. this deploy changes the guide), it sets:
  - the Article JSON-LD "dateModified"  -> today (YYYY-MM-DD)
  - the visible header line "Updated <d Month YYYY>"
  - the footer line "last updated <d Month YYYY>"
If the guide is unchanged, it does nothing, so the date only moves when the guide
really changed. --force stamps regardless. Dry run by default; --apply to write.
"""
import datetime, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "field-guide/index.html"

def changed():
    r = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", str(F.relative_to(ROOT))], cwd=ROOT)
    return r.returncode != 0

def main(apply_, force):
    if not force and not changed():
        print("field guide: unchanged this deploy, date left alone"); return
    today = datetime.date.today()
    iso, human = today.isoformat(), f"{today.strftime('%B')} {today.day}, {today.year}"
    s = F.read_text(encoding="utf-8"); o = s
    s, a = re.subn(r'("dateModified"\s*:\s*")[^"]*(")', rf'\g<1>{iso}\2', s, count=1)
    s, b = re.subn(r'(<span>Updated )[^<]*(</span>)', rf'\g<1>{human}\2', s, count=1)
    s, c = re.subn(r'(Field Guide updated regularly &middot; last updated )[^<&]*( &middot;)', rf'\g<1>{human}\2', s, count=1)
    print(f"field guide: dateModified {a}, header {b}, footer {c} -> {iso}")
    if a != 1 or b != 1:
        sys.exit("! pattern not found, nothing written")
    if apply_ and s != o:
        F.write_text(s, encoding="utf-8")

if __name__ == "__main__":
    main("--apply" in sys.argv, "--force" in sys.argv)
