#!/usr/bin/env python3
"""stamp-sitemap-lastmod.py — make every <lastmod> in sitemap.xml tell the truth.
23 September 2026.

Lenny: "are we making sure all links are syndicating to Bing.com"

THE SITEMAP HAS BEEN LYING TO BOTH ENGINES. Nothing regenerates it — the deploy
script is `git add . && git commit && git push` and no more — so a page can be
rewritten from top to bottom and still carry a lastmod from three months ago.
Two live examples on the day this was written:

    /drops/home-golf-decor-edit   sitemap said 2026-06-21, git says 2026-09-23
    /drops/brand-to-know-manors   sitemap said 2026-09-18, git says 2026-09-22

lastmod is the single cheapest recrawl signal there is. Bing and Google both use
it to decide whether a known URL is worth fetching again. A rebuilt page that
still claims to be from June is asking not to be recrawled.

GIT IS THE SOURCE OF TRUTH, not the filesystem mtime. An rsync, a Cloud-sync
round trip or a checkout all touch mtime without changing a byte of content;
`git log -1 --format=%cs` gives the date the file's content actually last
changed, which is the thing lastmod is supposed to mean.

UNCOMMITTED WORK COUNTS AS TODAY. A page edited but not yet deployed has no
commit date that reflects the edit, so it is stamped with today's date — by the
time the sitemap is live, that will be true.

THIS DELIBERATELY OVERWRITES EXISTING DATES, which sync-brand-sitemap.py
explicitly refuses to do ("an existing entry means someone set that date
deliberately"). That rule is right for that script and wrong here: a date set
deliberately in June is still wrong once the page is rewritten in September.
The two scripts are not in conflict — that one adds missing rows and leaves
dates alone, this one only corrects dates and never adds or removes a row.

NEVER STAMPS A FUTURE DATE. A clock skew or a bad commit date that lands in the
future would tell a crawler the page is newer than now, which some crawlers
treat as a reason to distrust the whole file.

Idempotent. Dry run by default.
"""
import datetime
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://thegrassyissue.com"
TODAY = datetime.date.today().isoformat()


def to_file(loc):
    """URL -> the file on disk that serves it, or None."""
    p = loc.replace(BASE, "").strip("/")
    if not p:
        return ROOT / "index.html"
    for cand in (ROOT / f"{p}.html", ROOT / p / "index.html"):
        if cand.is_file():
            return cand
    return None


def git_date(path):
    """Date the file's CONTENT last changed, per git. None if untracked."""
    rel = path.relative_to(ROOT).as_posix()
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel],
                               cwd=ROOT, capture_output=True, text=True,
                               timeout=20).stdout.strip()
        if dirty:
            return TODAY            # edited and not yet deployed
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                             cwd=ROOT, capture_output=True, text=True,
                             timeout=20).stdout.strip()
        return out or None
    except (subprocess.SubprocessError, OSError):
        return None


def main(apply_):
    xml = SITEMAP.read_text(encoding="utf-8")
    original = xml

    entries = list(re.finditer(
        r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml))
    print(f"  {len(entries)} sitemap entries")

    changes, unmapped, skipped = [], [], 0
    for m in entries:
        loc, was = m.group(1), m.group(2)
        f = to_file(loc)
        if f is None:
            unmapped.append(loc)
            continue
        now = git_date(f)
        if not now:
            skipped += 1
            continue
        if now > TODAY:             # never stamp the future
            now = TODAY
        if now != was:
            changes.append((loc, was, now))

    for loc, was, now in changes:
        xml = xml.replace(f"<loc>{loc}</loc>", f"<loc>{loc}</loc>\x00", 1)
        xml = re.sub(r"(<loc>" + re.escape(loc) + r"</loc>\x00\s*<lastmod>)[^<]+",
                     lambda mm: mm.group(1) + now, xml, count=1)
        xml = xml.replace(f"<loc>{loc}</loc>\x00", f"<loc>{loc}</loc>", 1)

    print(f"  {len(changes)} dates corrected, {skipped} untracked, "
          f"{len(unmapped)} unmapped")
    for loc, was, now in sorted(changes, key=lambda c: c[2], reverse=True)[:14]:
        print(f"      {loc.replace(BASE, '')[:46]:<48}{was} -> {now}")
    if len(changes) > 14:
        print(f"      ... and {len(changes) - 14} more")
    for u in unmapped[:5]:
        print(f"      UNMAPPED {u}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return
    if not changes:
        print("\n  nothing to do")
        return
    SITEMAP.write_text(xml, encoding="utf-8")

    # ---- VERIFY ----
    fin = SITEMAP.read_text(encoding="utf-8")
    bad = []
    after = dict((m.group(1), m.group(2)) for m in re.finditer(
        r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", fin))
    if len(after) != len(entries):
        bad.append(f"{len(after)} entries after, {len(entries)} before — "
                   "rows were added or lost")
    for loc, was, now in changes:
        if after.get(loc) != now:
            bad.append(f"{loc}: wanted {now}, file says {after.get(loc)}")
    for loc, d in after.items():
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            bad.append(f"{loc}: malformed date {d!r}")
        elif d > TODAY:
            bad.append(f"{loc}: future date {d}")
    if fin.count("<url>") != original.count("<url>"):
        bad.append("the number of <url> blocks changed")
    if "\x00" in fin:
        bad.append("a placeholder sentinel survived into the file")
    if bad:
        SITEMAP.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))

    newest = max(after.values())
    print(f"\n  wrote sitemap.xml — {len(changes)} corrected, newest lastmod "
          f"now {newest}")
    print("  Bing and Google both read lastmod to decide what to recrawl;")
    print("  these pages were previously telling them not to bother.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
