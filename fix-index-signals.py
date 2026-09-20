#!/usr/bin/env python3
"""fix-index-signals.py — resolve the robots.txt/noindex contradiction on the
private pages, and remove two leftover deck files. 20 September 2026.

WHY THIS EXISTS. Search Console reported "Excluded by 'noindex' tag" as a new
reason. A sweep of all 368 live URLs found the report is correct and benign:
exactly two pages carry noindex, /ig and /stats, and both are meant to be
private. All 365 sitemap URLs are clean. Nothing that should rank is blocked.

But the sweep turned up a configuration that works against itself.

THE CONTRADICTION. /ig, /stats and /instagram-posts are all Disallow'd in
robots.txt. Two of them ALSO carry noindex. Those two directives do not stack —
they conflict:

  - Disallow stops Googlebot FETCHING the page.
  - noindex only works if Googlebot fetches the page and reads the tag.

So the disallow suppresses the very signal that does the work. Google evidently
crawled /ig and /stats anyway — that is why the alert fired at all — but relying
on a crawler ignoring robots.txt is not a plan. The failure mode is specific: a
robots-blocked URL can still be indexed URL-only (title and bare link, no
snippet) if anything external links to it, and because Google never fetched it,
there is no noindex available to stop that.

To keep a page out of the index you let it be crawled and let noindex do the
job. So the Disallow lines come out and the noindex stays.

/instagram-posts was the worst of the three: Disallow'd, so presumed handled,
but carrying NO noindex and no canonical. It had the contradiction without the
safety net. It gets the tag the other two already have.

/drafts/ KEEPS its Disallow. Those URLs 404 in production (checked — all 170),
so nothing is being suppressed and the line costs nothing.

THE DECK FILES. /_deckbold and /_deckopts are layout experiments from the BTK
template work on 18 September that were never meant to ship. Both are live and
indexable and carry the SAME <title> as the real Forden Golf post. They do
canonical to it, which is why this is a tidy-up rather than an emergency. Lenny's
call: delete. Nothing in the repo links to them (checked across html/json/xml/
js/py), they have no inbound links and no traffic, so a 404 is the right exit —
a 301 would be inventing a redirect for a URL nobody has.

Idempotent: safe to re-run once the files are gone and the lines are removed.
Dry run by default.
"""
import os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
ROBOTS = ROOT / "robots.txt"
IGPOSTS = ROOT / "instagram-posts.html"

# The Disallow lines that suppress a noindex. /drafts/ is deliberately absent.
DROP = ["Disallow: /ig", "Disallow: /instagram-posts", "Disallow: /stats"]
KEEP = "Disallow: /drafts/"
NOINDEX = '<meta name="robots" content="noindex, nofollow" />'
DECKS = ["_deckbold.html", "_deckopts.html"]


def _tagged(path):
    """True only if the file carries a real <meta name="robots" ...noindex...>.
    Deliberately NOT a substring test — see the guard comment below."""
    t = path.read_text(encoding="utf-8")
    return bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', t, re.I))


def robots_text():
    t = ROBOTS.read_text(encoding="utf-8")
    out = [l for l in t.splitlines()
           if l.strip() not in DROP]
    return "\n".join(out).rstrip("\n") + "\n"


def igposts_text():
    t = IGPOSTS.read_text(encoding="utf-8")
    if re.search(r'<meta[^>]+name=["\']robots["\']', t, re.I):
        return t                                   # already tagged
    # After <title>, so it sits with the other head metadata rather than being
    # buried below the stylesheet.
    m = re.search(r"</title>", t, re.I)
    if not m:
        sys.exit("! instagram-posts.html has no </title> to anchor against")
    return t[:m.end()] + "\n" + NOINDEX + t[m.end():]


def main(apply_):
    rb = robots_text()
    ig = igposts_text()
    decks = [ROOT / d for d in DECKS]

    checks = [
        ("robots.txt no longer blocks the private pages",
         not any(d in rb for d in DROP),
         str([d for d in DROP if d in rb])),
        ("robots.txt still blocks /drafts/", KEEP in rb, ""),
        ("robots.txt still allows the site", "Allow: /" in rb, ""),
        ("robots.txt still declares the sitemap",
         "Sitemap: https://thegrassyissue.com/sitemap.xml" in rb, ""),
        # The whole point of dropping the Disallow is that noindex takes over.
        # If the tag were missing, this change would OPEN the pages instead of
        # closing them — the exact opposite of the intent. Assert the tag is
        # present on all three BEFORE the block comes off.
        ("/instagram-posts now carries noindex",
         bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', ig, re.I)), ""),
        # MUST MATCH THE TAG, NOT THE WORD. The first version of these two
        # asserted `"noindex" in text`. Both pages print the sentence "Private —
        # noindex, disallowed in robots.txt" in their visible footer, so the
        # word is on the page whether or not the meta tag is. Fault-injecting —
        # deleting the real tag from ig.html — did not trip the guard, which is
        # the only reason this was caught. A guard that cannot fail is not a
        # guard, and this one sits in front of a change that REMOVES the
        # robots.txt block: had it been wrong in production, it would have
        # published both private pages to the index.
        ("/ig still carries noindex", _tagged(ROOT / "ig.html"), ""),
        ("/stats still carries noindex", _tagged(ROOT / "stats.html"), ""),
        ("instagram-posts has exactly one robots tag",
         len(re.findall(r'<meta[^>]+name=["\']robots["\']', ig, re.I)) == 1, ""),
        ("instagram-posts still closes",
         ig.rstrip().endswith("</html>"), ""),
        # Deleting a file that something links to would manufacture a 404 on a
        # reachable path. Nothing may point at the decks.
        ("nothing in the repo links to the deck files",
         not _linked(), str(_linked())),
        ("deck files are not in the sitemap",
         not any(d[:-5] in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
                 for d in DECKS), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}{('  ' + d) if d and not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")

    print("\n  robots.txt after:")
    for l in rb.splitlines():
        print(f"    {l}")
    print(f"\n  deck files to delete: {[d.name for d in decks if d.exists()] or 'none (already gone)'}")

    if apply_:
        ROBOTS.write_text(rb, encoding="utf-8")
        IGPOSTS.write_text(ig, encoding="utf-8")
        for d in decks:
            if d.exists():
                d.unlink()
        print("\n  wrote robots.txt + instagram-posts.html, removed deck files")
    else:
        print("\n  dry run — pass --apply")


def _linked():
    """Every repo reference to the deck files, excluding the files themselves
    and the non-deployed research/ and drafts/ trees."""
    hits = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in ("research", "drafts", ".git", "__pycache__")]
        for f in fn:
            if f in DECKS or not f.endswith((".html", ".json", ".xml", ".js")):
                continue
            p = pathlib.Path(dp) / f
            try:
                t = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "_deckbold" in t or "_deckopts" in t:
                hits.append(str(p.relative_to(ROOT)))
    return hits


if __name__ == "__main__":
    main("--apply" in sys.argv)
