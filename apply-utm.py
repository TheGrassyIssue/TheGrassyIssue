#!/usr/bin/env python3
"""apply-utm.py — tag outbound links so brands see TGI in their own analytics.

Appends  utm_source=thegrassyissue & utm_medium=referral
         & utm_campaign=<section> & utm_content=<page slug>
to every external <a href> on live pages, so a click shows up in the brand's
Shopify / GA reports as "thegrassyissue" instead of vanishing into "direct".

  section: brand-index (brands/), editorial (drops/), muni-guide (guides/),
           field-guide, events, home (index.html, feed/), about, work-with-us

Leaves alone:
  * anything inside <script>, <style> or <!-- comments --> (JS-built cards,
    JSON-LD, the search overlay — see reference-js-health-check)
  * affiliate-wrapped links (data-aff="1") and affiliate/redirect networks
  * links that already carry utm_source (a brand's own tags win)
  * social, government, maps and publication domains (SKIP_DOMAINS)
  * private pages: ig.html, instagram-posts.html, stats.html, drafts/

Idempotent. Dry run by default; --apply writes; --revert strips only the tags
this script added (utm_source=thegrassyissue). Self-check per file: every
<script>/<style> block and the count of <a> tags must be identical after the
rewrite, or the file is NOT written.

Run AFTER any generator (build-brands.py, post builds, apply-affiliates.py),
or let deploy.sh run it right before the push.
"""
import re, os, sys, glob, time, urllib.parse

S = os.path.dirname(os.path.abspath(__file__))
SOURCE = "thegrassyissue"

SKIP_DOMAINS = {
    # social
    "instagram.com", "facebook.com", "tiktok.com", "youtube.com", "youtu.be",
    "twitter.com", "x.com", "threads.net", "linkedin.com", "pinterest.com",
    "reddit.com", "strava.com",
    # search / maps / reference
    "google.com", "goo.gl", "maps.app.goo.gl", "maps.apple.com", "wikipedia.org",
    # affiliate + redirect networks (tagging would break or double-count)
    "skimresources.com", "go.skimresources.com", "shareasale.com", "awin1.com",
    "linksynergy.com", "anrdoezrs.net", "dpbolvw.net", "jdoqocy.com",
    "tkqlhce.com", "kqzyfj.com", "pjtra.com", "pntra.com", "sjv.io",
    "impact.com", "rstyle.me", "shopstyle.it", "amzn.to",
}
SKIP_SUFFIXES = (".gov", ".edu", "myvscloud.com")

PRIVATE = {"ig.html", "instagram-posts.html", "stats.html"}
DIRS = ["index.html", "about.html", "work-with-us.html", "disclosure.html",
        "brands", "drops", "events", "feed", "field-guide", "guides"]

PROTECT = re.compile(r'<script\b.*?</script\s*>|<style\b.*?</style\s*>|<!--.*?-->',
                     re.S | re.I)
ATAG = re.compile(r'<a\b[^>]*>', re.S | re.I)
HREF = re.compile(r'(href\s*=\s*")(https?://[^"]+)(")', re.I)


def campaign_for(rel):
    top = rel.split("/")[0]
    return {
        "brands": "brand-index", "drops": "editorial", "guides": "muni-guide",
        "field-guide": "field-guide", "events": "events", "feed": "home",
        "index.html": "home", "about.html": "about",
        "work-with-us.html": "work-with-us", "disclosure.html": "disclosure",
    }.get(top, "site")


def content_for(rel):
    slug = re.sub(r"(/index)?\.html$", "", rel)
    slug = slug.split("/", 1)[1] if "/" in slug else slug
    return slug.replace("/", "-") or "index"


def host_of(url):
    h = urllib.parse.urlsplit(url).hostname or ""
    return h[4:] if h.startswith("www.") else h


def skip_host(h):
    if not h or "thegrassyissue" in h:
        return True
    if h in SKIP_DOMAINS or any(h.endswith("." + d) for d in SKIP_DOMAINS):
        return True
    return h.endswith(SKIP_SUFFIXES)


def add_utm(url, campaign, content):
    raw = url.replace("&amp;", "&")
    parts = urllib.parse.urlsplit(raw)
    if "utm_source=" in parts.query:
        return url
    tags = urllib.parse.urlencode([
        ("utm_source", SOURCE), ("utm_medium", "referral"),
        ("utm_campaign", campaign), ("utm_content", content)])
    q = parts.query + ("&" if parts.query else "") + tags
    out = urllib.parse.urlunsplit(parts._replace(query=q))
    return out.replace("&", "&amp;")


def strip_utm(url):
    raw = url.replace("&amp;", "&")
    parts = urllib.parse.urlsplit(raw)
    pairs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    if ("utm_source", SOURCE) not in pairs:
        return url
    keep = [(k, v) for k, v in pairs if not k.startswith("utm_")]
    out = urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(keep)))
    return out.replace("&", "&amp;")


def rewrite_html(h, fn):
    """Apply fn(url) to external hrefs in <a> tags outside protected blocks."""
    out, last, n = [], 0, 0
    def do_tag(tag):
        nonlocal n
        if 'data-aff="1"' in tag:
            return tag
        m = HREF.search(tag)
        if not m or skip_host(host_of(m.group(2).replace("&amp;", "&"))):
            return tag
        new = fn(m.group(2))
        if new == m.group(2):
            return tag
        n += 1
        return tag[:m.start(2)] + new + tag[m.end(2):]
    def do_chunk(chunk):
        return ATAG.sub(lambda mt: do_tag(mt.group(0)), chunk)
    for pm in PROTECT.finditer(h):
        out.append(do_chunk(h[last:pm.start()]))
        out.append(pm.group(0))
        last = pm.end()
    out.append(do_chunk(h[last:]))
    return "".join(out), n


def read(path, tries=4):
    for i in range(tries):
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except OSError:          # iCloud "Resource deadlock avoided" — retry
            if i == tries - 1:
                raise
            time.sleep(0.5 * (i + 1))


def files():
    for d in DIRS:
        p = os.path.join(S, d)
        if os.path.isfile(p):
            yield d
        elif os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*.html"), recursive=True)):
                rel = os.path.relpath(f, S)
                base = os.path.basename(rel)
                if base in PRIVATE or re.search(r" \d\.html$|copy", base):
                    continue
                yield rel


def main():
    apply_ = "--apply" in sys.argv
    revert = "--revert" in sys.argv
    total_links = total_files = refused = 0
    for rel in files():
        path = os.path.join(S, rel)
        h = read(path)
        if revert:
            new, n = rewrite_html(h, strip_utm)
        else:
            c, t = campaign_for(rel), content_for(rel)
            new, n = rewrite_html(h, lambda u: add_utm(u, c, t))
        if not n:
            continue
        # self-check: scripts/styles/comments byte-identical, same number of <a>
        if (PROTECT.findall(h) != PROTECT.findall(new)
                or len(ATAG.findall(h)) != len(ATAG.findall(new))):
            print("REFUSED (self-check failed):", rel)
            refused += 1
            continue
        total_links += n
        total_files += 1
        if apply_:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
    verb = "stripped" if revert else "tagged"
    print("%s %d links on %d pages%s" % (verb, total_links, total_files,
          "" if apply_ else "  (dry run - pass --apply)"))
    if refused:
        print("%d pages refused - nothing written to them" % refused)
        sys.exit(1)


if __name__ == "__main__":
    main()
