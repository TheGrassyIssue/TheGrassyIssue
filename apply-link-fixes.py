#!/usr/bin/env python3
"""apply-link-fixes.py — repoint dead (404) outbound links. 11 Oct 2026.
Lenny: "Fix the ones that are 404'd" after a full outbound-link check (3,678 links, 225 hard 404s).
Mapping lives in data/link-fixes.json (old URL without query -> new URL). Query strings (UTM tags) are kept.
kind=same: the product was relisted under a new handle, so the link goes straight to it.
kind=unlink: the brand's whole site is gone, so the link text stays and the link is removed.
kind=brand: the product is gone; the link goes to the brand's shop and a product card's button reads
"Sold out · Shop the brand". Idempotent; runs on every deploy so a page rebuild can't bring a dead link back.
"""
import glob, html, json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(ROOT, "data/link-fixes.json")))["fixes"]

def fix_page(s):
    n = 0
    def repl(m):
        nonlocal n
        pre, url, mid, text, post = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        raw = html.unescape(url); base, q = (raw.split("?", 1) + [""])[:2]
        f = FX.get(base)
        if not f: return m.group(0)
        whole_card = 'class="product-card"' in (pre + mid)
        if f["kind"] == "unlink":  # the brand's whole site is gone: keep the words, drop the link
            n += 1
            if whole_card:  # card-wide anchor: keep the card, swap the button for a note
                text = re.sub(r'<span class="product-link">.*?</span>', '<span class="product-link">No longer available</span>', text, flags=re.S)
                return f'<div class="product-card">{text}</div>'
            return text
        new = f["new"] + (("?" + q) if q else "")
        new_esc = new.replace("&", "&amp;")
        if f["kind"] == "brand":
            if 'class="product-link"' in (pre + mid):
                text = "Sold out &middot; Shop the brand &#8599;"
            elif whole_card:
                text = re.sub(r'(<span class="product-link">).*?(</span>)', r'\1Sold out &middot; Shop the brand &#8599;\2', text, count=1, flags=re.S)
        n += 1
        return f"{pre}{new_esc}{mid}{text}{post}"
    s2 = re.sub(r'(<a\b[^>]*?href=")(https?://[^"]+)("[^>]*>)(.*?)(</a>)', repl, s, flags=re.S)
    return s2, n

def main(apply_):
    pages = sorted({p for f in FX.values() for p in f["pages"]})
    total, changed = 0, 0
    for p in pages:
        fn = os.path.join(ROOT, "drops", p + ".html")
        if not os.path.isfile(fn): continue
        s = open(fn, encoding="utf-8").read()
        s2, n = fix_page(s)
        total += n
        if s2 != s:
            changed += 1
            if apply_: open(fn, "w", encoding="utf-8").write(s2)
    print(f"apply-link-fixes: {total} dead link(s) repointed across {changed} page(s){'' if apply_ else ' (dry run)'}")

if __name__ == "__main__":
    main("--apply" in sys.argv)
