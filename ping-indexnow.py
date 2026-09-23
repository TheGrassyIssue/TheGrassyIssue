#!/usr/bin/env python3
"""ping-indexnow.py — tell Bing which URLs changed, the moment they go live.
23 September 2026.

Lenny: "are we making sure all links are syndicating to Bing.com"

WHAT INDEXNOW IS. A one-request protocol Microsoft built so a site can push a
changed URL rather than wait to be crawled. Bing consumes it directly, and so
do DuckDuckGo, Yandex and Copilot, which all sit on Bing's index. There is no
account, no quota and no verification step beyond hosting a key file — which is
why the absence of it here was pure lost ground rather than a trade-off.

Google does NOT consume IndexNow. Google gets the same news from the sitemap's
lastmod, which stamp-sitemap-lastmod.py now keeps honest. The two scripts are
the same job aimed at two engines.

THE KEY FILE IS THE AUTHENTICATION. https://thegrassyissue.com/<key>.txt must
serve the key as plain text; the API refuses submissions it cannot verify that
way. The file is committed alongside the site, so it deploys with everything
else. If it ever 404s, every submission silently fails, so this checks the file
is reachable before submitting anything.

THIS RUNS AFTER DEPLOY, NEVER BEFORE. Submitting a URL that is not yet live
teaches Bing the page 404s, which is worse than not submitting. The script
verifies each URL returns 200 on the live site before including it, and it is
wired into "Deploy TGI.command" AFTER the git push for the same reason.

CLAUDE DOES NOT FIRE THIS. It runs as part of Lenny's own deploy, from his
machine, on URLs that are already public by the time it runs. Dry run by
default, and --apply only submits what it has verified is live.

WHAT IT SUBMITS. URLs whose sitemap lastmod is within --days (default 2).
Capped at 100 a run: IndexNow accepts up to 10,000, but a small site pushing
hundreds of URLs in one burst looks like spam, and the point is to flag genuine
changes rather than to re-announce the archive.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta

ROOT = pathlib.Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"
HOST = "thegrassyissue.com"
BASE = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/IndexNow"
UA = {"User-Agent": "TheGrassyIssue-IndexNow/1.0 (+https://thegrassyissue.com)"}
MAX_URLS = 100


def key_file():
    """The single <32hex>.txt at the site root. Never guessed."""
    found = [p for p in ROOT.glob("*.txt")
             if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(found) != 1:
        sys.exit(f"! expected exactly one IndexNow key file at the site root, "
                 f"found {len(found)}")
    k = found[0].read_text(encoding="utf-8").strip()
    if k != found[0].stem:
        sys.exit(f"! {found[0].name} must contain exactly its own filename stem; "
                 f"it contains {k[:16]!r}")
    return k


def recent(days):
    xml = SITEMAP.read_text(encoding="utf-8")
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    out = [(loc, lm) for loc, lm in
           re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
           if lm >= cutoff]
    return sorted(out, key=lambda x: x[1], reverse=True)


def live(url, timeout=15):
    """200 on the real site? A URL that is not live must not be submitted."""
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        return e.code == 200
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2,
                    help="submit URLs with lastmod within this many days")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--skip-live-check", action="store_true",
                    help="only for testing; submitting a dead URL is harmful")
    a = ap.parse_args()

    key = key_file()
    print(f"  key file : {key[:8]}...{key[-4:]}.txt")

    # the key must be reachable or every submission fails silently
    if not a.skip_live_check:
        if not live(f"{BASE}/{key}.txt"):
            sys.exit(f"! {BASE}/{key}.txt is not reachable — deploy it before "
                     "submitting, or IndexNow will reject every URL")
        print(f"  key live : yes")

    rows = recent(a.days)
    print(f"  {len(rows)} URLs with lastmod in the last {a.days} day(s)")
    if not rows:
        print("  nothing to submit")
        return

    urls = [u for u, _ in rows][:MAX_URLS]
    if len(rows) > MAX_URLS:
        print(f"  capping at {MAX_URLS} (of {len(rows)}) — a burst larger than "
              "this reads as spam")

    if not a.skip_live_check:
        checked, dead = [], []
        for u in urls:
            (checked if live(u) else dead).append(u)
        for d in dead:
            print(f"      SKIPPED, not live: {d}")
        urls = checked
    print(f"  {len(urls)} verified live and ready to submit")
    for u in urls[:8]:
        print(f"      {u.replace(BASE, '') or '/'}")
    if len(urls) > 8:
        print(f"      ... and {len(urls) - 8} more")

    if not a.apply:
        print("\n  dry run — pass --apply to submit")
        return
    if not urls:
        print("\n  nothing live to submit")
        return

    payload = json.dumps({"host": HOST, "key": key,
                          "keyLocation": f"{BASE}/{key}.txt",
                          "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload, headers={
        **UA, "Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code, body = r.status, r.read(400).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read(400).decode("utf-8", "ignore")
    except Exception as e:
        sys.exit(f"! submission failed to send: {e}")

    # 200 accepted, 202 accepted pending key validation
    if code in (200, 202):
        print(f"\n  submitted {len(urls)} URLs to IndexNow — HTTP {code}")
        print("  Bing, DuckDuckGo and Copilot all read this feed.")
    else:
        print(f"\n! IndexNow returned HTTP {code}: {body[:200]}")
        print("  403 usually means the key file is not being served as plain "
              "text at the location above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
