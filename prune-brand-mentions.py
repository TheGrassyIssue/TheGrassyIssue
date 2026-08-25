#!/usr/bin/env python3
"""Remove false-positive brand mentions from data/brand-mentions.json.

THE BUG (found 2026-08-25): the mentions scan matched brand names anywhere in the
page HTML, including the "More from the Feed" cards at the bottom. That meant a post
that merely *recommends* a brand's profile at the end got filed under that brand on
/brands/<slug> — e.g. Sentinel Golf showed up under the Austin Golf Road Trip even
though the road trip never mentions Sentinel in the editorial.

This script re-validates every non-profile entry: it strips page chrome (head, nav,
breadcrumb, footer, .more-card links, .more-grid) and keeps the entry only if the
brand still appears in the remaining editorial body.

Matching note: brands.json stores full names ("Devereux Golf") but posts often use a
short form ("Devereux"), so we match on the full name OR any distinctive token,
ignoring generic words like "golf" / "club" / "studio". Matching on the full name
alone produces ~10 bogus removals.

Run after any mentions rescan, then: python3 build-brands.py
"""
import json, re, os, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GENERIC = {'golf','the','and','co','clothiers','sports','studio','club','stable',
           'workshop','company','shirts','house','goods','supply','apparel'}

def keys_for(name):
    n = name.lower().replace('&', 'and')
    ks = {n, name.lower()}
    toks = [t for t in re.split(r'[^a-z0-9]+', n) if t and t not in GENERIC and len(t) > 2]
    if toks:
        ks.add(' '.join(toks)); ks.update(toks)
    return {k for k in ks if k}

def strip_chrome(h):
    h = re.sub(r'<head>.*?</head>', '', h, flags=re.S)
    h = re.sub(r'<nav\b.*?</nav>', '', h, flags=re.S)
    h = re.sub(r'<div class="breadcrumb">.*?</div>', '', h, flags=re.S)
    h = re.sub(r'<footer\b.*?</footer>', '', h, flags=re.S)
    h = re.sub(r'<a[^>]*class="more-card"[^>]*>.*?</a>', '', h, flags=re.S)
    h = re.sub(r'<div class="more-grid">.*?</div>\s*(?:</section>)?', '', h, flags=re.S)
    return h

def text(h):
    return html.unescape(re.sub(r'<[^>]+>', ' ', h)).lower()

def main(apply=True):
    brands = json.load(open(os.path.join(ROOT, 'data', 'brands.json')))
    mpath  = os.path.join(ROOT, 'data', 'brand-mentions.json')
    ment   = json.load(open(mpath))
    NAMES  = {b['slug']: b['name'] for b in brands}

    removed, kept = [], 0
    for slug, entries in ment.items():
        ks = keys_for(NAMES.get(slug, slug))
        keep = []
        for e in entries:
            if e.get('profile'):
                keep.append(e); continue
            p = os.path.join(ROOT, e['url'].lstrip('/') + '.html')
            if not os.path.exists(p):
                keep.append(e); continue          # can't verify -> leave alone
            raw = open(p, encoding='utf-8', errors='ignore').read()
            if any(k in text(strip_chrome(raw)) for k in ks):
                keep.append(e)
            else:
                removed.append((NAMES.get(slug, slug), e['url']))
        kept += len(keep)
        ment[slug] = keep

    print(f"removed {len(removed)} false positives, {kept} mentions kept")
    for n, u in removed:
        print(f"   - {n:26} {u}")
    if apply and removed:
        json.dump(ment, open(mpath, 'w'), indent=1, ensure_ascii=False)
        print("wrote data/brand-mentions.json")

if __name__ == '__main__':
    main(apply='--dry-run' not in sys.argv)
