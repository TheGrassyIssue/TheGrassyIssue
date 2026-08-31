#!/usr/bin/env python3
"""apply-affiliates.py — wrap outbound product links in affiliate URLs.

Reads data/affiliates.json. Only touches merchants with status=active AND a
non-null id/template. For each page in drops/ + guides/ + index.html:

  * rewrites `class="product-link"` (and gear-slide) hrefs whose domain matches
    an active merchant — mode=param appends the params in `template`
    (e.g. "?sca_ref=XXXX" or "?aff=123"), mode=wrap replaces the href with
    `template` where {url} is the URL-encoded original
  * adds rel="sponsored noopener" to every rewritten link
  * inserts the FTC disclosure line once per monetized page (under the sidebar
    Details card), linking to /disclosure

If _skimlinks.publisher_id is set, installs the snippet before </body> on every
page that carries outbound product links (marker <!--TGI-AFF-SKIM-->), and the
disclosure line goes on those pages too.

Idempotent: wrapped links carry data-aff="1"; disclosure carries
class="aff-disclosure"; snippet carries its marker. Dry run by default,
--apply to write, --revert to strip everything back to bare merchant URLs.

Run AFTER any generator (build-brands.py etc.), same as the typography chain.
"""
import re, os, sys, glob, json, urllib.parse

S = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(S, "data", "affiliates.json")))

DISCLOSURE = ('<div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;'
    'letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">'
    'Some links may earn TGI a commission &mdash; <a href="/disclosure" '
    'style="border-bottom:1px solid currentColor;">details</a></div>')

SKIM_MARK = "<!--TGI-AFF-SKIM-->"

def active_merchants():
    out = {}
    for dom, m in CFG.get("merchants", {}).items():
        if m.get("status") == "active" and (m.get("id") or m.get("template")):
            out[dom] = m
    return out

def skim_snippet():
    sk = CFG.get("_skimlinks", {})
    if not sk.get("publisher_id"):
        return None
    if sk.get("provider") == "skimlinks":
        return ('%s<script type="text/javascript" src="https://s.skimresources.com/js/%s.skimlinks.js"></script>'
                % (SKIM_MARK, sk["publisher_id"]))
    if sk.get("provider") == "sovrn":
        return ('%s<script async src="//js-sec.indexww.com/vl/%s.js"></script>'
                % (SKIM_MARK, sk["publisher_id"]))
    return None

LINK = re.compile(r'<a\s+([^>]*?)href="(https?://(?:www\.)?([^"/]+)[^"]*)"([^>]*)>', re.S)

def wrap_url(url, m):
    if m["mode"] == "wrap":
        return m["template"].replace("{url}", urllib.parse.quote(url, safe=""))
    # param mode: append template params
    t = m["template"].lstrip("?&")
    return url + ("&" if "?" in url else "?") + t

def process(path, merchants, snippet, apply_):
    h = open(path, encoding="utf-8").read()
    orig = h
    changed_links = 0

    def sub(mt):
        nonlocal changed_links
        pre, url, dom, post = mt.group(1), mt.group(2), mt.group(3), mt.group(4)
        attrs = pre + post
        if 'class="product-link"' not in attrs and "gear-slide" not in attrs:
            # only rewrite product links / slide links; leave editorial links alone
            return mt.group(0)
        if 'data-aff="1"' in attrs:
            return mt.group(0)
        m = merchants.get(dom)
        if not m:
            return mt.group(0)
        new = wrap_url(url, m)
        changed_links += 1
        # normalize rel
        pre2, post2 = pre, post
        relre = re.compile(r'rel="[^"]*"')
        if relre.search(pre2): pre2 = relre.sub('rel="sponsored noopener"', pre2)
        elif relre.search(post2): post2 = relre.sub('rel="sponsored noopener"', post2)
        else: post2 = post2 + ' rel="sponsored noopener"'
        return '<a %shref="%s" data-aff="1"%s>' % (pre2, new, post2)

    h = LINK.sub(sub, h)

    has_outbound = ('class="product-link"' in h and "http" in h) or \
        bool(re.search(r'<div class="gear-slide">\s*<a href="https?://(?!thegrassyissue)', h))
    monetized = changed_links > 0 or (snippet and has_outbound)

    if snippet and has_outbound and SKIM_MARK not in h:
        h = h.replace("</body>", snippet + "\n</body>", 1)
    if monetized and 'class="aff-disclosure"' not in h:
        if "</aside>" in h:
            h = h.replace("</aside>", DISCLOSURE + "\n  </aside>", 1)
        elif '<footer><div class="inner">' in h:
            h = h.replace('<footer><div class="inner">',
                '<footer><div class="inner" style="flex-wrap:wrap;gap:10px;">'
                + DISCLOSURE.replace('margin-top:14px;','margin-top:0;'), 1)
        elif '<div class="footer-brand">' in h:
            # homepage footer: tuck the line under the brand tag
            h = h.replace('<div class="footer-brand">',
                '<div class="footer-brand">' + DISCLOSURE.replace('margin-top:14px;','margin:0 0 10px;'), 1)

    if h != orig and apply_:
        open(path, "w", encoding="utf-8").write(h)
    return changed_links, (h != orig)

def revert(path, apply_):
    h = open(path, encoding="utf-8").read()
    orig = h
    h = re.sub(SKIM_MARK + r'<script[^>]*></script>\n?', "", h)
    h = re.sub(r'<div class="aff-disclosure".*?</div>\n?', "", h, flags=re.S)
    # strip data-aff + restore rel (leave URLs; reverting params needs the map)
    for dom, m in CFG.get("merchants", {}).items():
        if m.get("template") and m.get("mode") == "param":
            t = m["template"].lstrip("?&")
            h = h.replace("&" + t, "").replace("?" + t + '"', '"')
    h = h.replace(' data-aff="1"', "").replace('rel="sponsored noopener"', 'rel="noopener"')
    if h != orig and apply_:
        open(path, "w", encoding="utf-8").write(h)
    return h != orig

def main():
    apply_ = "--apply" in sys.argv
    rev = "--revert" in sys.argv
    merchants = active_merchants()
    snippet = skim_snippet()
    pages = sorted(glob.glob(os.path.join(S, "drops", "*.html")) +
                   glob.glob(os.path.join(S, "guides", "*.html")) +
                   [os.path.join(S, "index.html")])
    if rev:
        n = sum(1 for p in pages if revert(p, apply_))
        print(("reverted" if apply_ else "would revert"), n, "page(s)")
    else:
        if not merchants and not snippet:
            print("nothing active: no merchant has status=active + id/template, and no skimlinks publisher_id.")
            print("fill in data/affiliates.json first. (dry run either way)")
            return
        total = 0; touched = 0
        for p in pages:
            c, ch = process(p, merchants, snippet, apply_)
            total += c; touched += 1 if ch else 0
        print(("wrapped" if apply_ else "would wrap"), total, "link(s) across", touched, "page(s)",
              "| skimlinks:", "yes" if snippet else "no")
    if not apply_:
        print("(dry run - pass --apply)")

if __name__ == "__main__":
    main()
