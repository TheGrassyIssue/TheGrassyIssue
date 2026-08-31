#!/usr/bin/env python3
"""strip-post-chips.py — remove the category chip from dedicated post headers.

Lenny, 2026-08-31: the [Field Notes] / [Drops & Brands] chip at the top of a
post repeats what the breadcrumb two lines above already says. This strips it
from post headers ONLY.

Deliberately untouched, because they are load-bearing:
  * homepage .card-tag chips (236) — they make the filter tabs legible
  * data-type attributes — drive the All/Drops/News/Field Notes tabs
  * breadcrumb category — now the sole on-page label
  * more-card-tag labels + search-index "g" field

Records what it removed in research/post-chips-removed.json so --revert can put
each page's original chip back exactly (colour class and all).

Idempotent: a page with no chip is skipped. Dry run by default, --apply to
write, --revert to restore. Run after any generator, before/after the
typography chain — order does not matter, it only touches the header span.
"""
import re, os, sys, glob, json

S = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(S, "research", "post-chips-removed.json")

# the chip always sits between <header class="drop-header"> and the <h1>
CHIP = re.compile(r'(<header class="drop-header">)\s*(<span class="drop-tag[^"]*">\[[^\]]*\]</span>)\s*')


def strip(path, apply_, ledger):
    h = open(path, encoding="utf-8").read()
    m = CHIP.search(h)
    if not m:
        return False
    ledger[os.path.relpath(path, S)] = m.group(2)
    out = CHIP.sub(r"\1\n  ", h, count=1)
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return True


def restore(path, apply_, ledger):
    rel = os.path.relpath(path, S)
    chip = ledger.get(rel)
    if not chip:
        return False
    h = open(path, encoding="utf-8").read()
    if 'class="drop-tag' in h:
        return False
    out = h.replace('<header class="drop-header">',
                    '<header class="drop-header">\n  ' + chip, 1)
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return True


def main():
    apply_ = "--apply" in sys.argv
    rev = "--revert" in sys.argv
    pages = sorted(glob.glob(os.path.join(S, "drops", "*.html")) +
                   glob.glob(os.path.join(S, "guides", "*.html")))
    if rev:
        ledger = json.load(open(LEDGER)) if os.path.exists(LEDGER) else {}
        if not ledger:
            print("no ledger at research/post-chips-removed.json — nothing to restore")
            return
        n = sum(1 for p in pages if restore(p, apply_, ledger))
        print(("restored" if apply_ else "would restore"), n, "chip(s)")
    else:
        ledger = json.load(open(LEDGER)) if os.path.exists(LEDGER) else {}
        n = sum(1 for p in pages if strip(p, apply_, ledger))
        if apply_ and n:
            os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
            json.dump(ledger, open(LEDGER, "w"), indent=1, sort_keys=True)
        print(("stripped" if apply_ else "would strip"), n, "chip(s) from post headers")
    if not apply_:
        print("(dry run - pass --apply)")


if __name__ == "__main__":
    main()
