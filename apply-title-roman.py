#!/usr/bin/env python3
"""
apply-title-roman.py — set post titles roman (not italic) to match the new caps masthead.

Lenny, 2026-08-29: "remove the italics from the post titles to match them a little better."

SCOPE
-----
Only `.drop-header h1` — the post title. Deliberately NOT touched:

  .product-name   still italic. It is a product name inside a card, a different
                  level of the hierarchy, and italic is doing work there.
  .more-card-name already roman (set by apply-editors-note.py's POSTBOX rule).
  .card-title     already roman, from the same earlier pass.
  .prog-price     unrelated.

So this is a one-selector change; if the product names should follow, that is a
separate decision.

Idempotent. Writes research/title-roman-inventory.json before any write.
"""
import os, re, glob, json, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def main(apply_=False):
    paths = sorted(p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
                   if "/drafts/" not in p.replace(os.sep, "/"))
    inv, changed = {}, 0
    hits = []
    for p in paths:
        s = open(p, encoding="utf-8", errors="replace").read()
        # match the .drop-header h1 rule and flip italic -> normal inside it only
        def repl(m):
            body = m.group(2)
            if "font-style:italic" not in body.replace(" ", ""):
                return m.group(0)
            return m.group(1) + re.sub(r"font-style:\s*italic", "font-style:normal", body) + "}"
        new = re.sub(r"(\.drop-header\s+h1\s*\{)([^}]*)\}", repl, s, count=1)
        if new != s:
            hits.append(os.path.relpath(p, ROOT))
            changed += 1
            if apply_:
                b = open(p, "rb").read()
                inv[os.path.relpath(p, ROOT)] = {"size": len(b),
                                                 "sha1": hashlib.sha1(b).hexdigest()}
                open(p, "w", encoding="utf-8").write(new)
    if apply_ and inv:
        os.makedirs(os.path.join(ROOT, "research"), exist_ok=True)
        json.dump(inv, open(os.path.join(ROOT, "research",
                                         "title-roman-inventory.json"), "w"), indent=1)
    print(f"{'set roman on' if apply_ else 'would set roman on'} {changed} page(s)")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
