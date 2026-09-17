#!/usr/bin/env python3
"""Link and price audit of the two water-bottle posts — 17 September 2026.

WHY. Both posts are a year old and neither had been re-checked. Every outbound
link in both was opened; every price was re-read off the seller's own page.

THE CORRECTION THAT STARTED THIS. The Sentinel "Basecamp Water Bottle $68" link
was reported earlier today as dead — as pointing at a galvanized basket. THAT
WAS WRONG. /shop/p/no-16-basket-galvanized-76zkc-nctfn-cx85f resolves to
BASECAMP WATER BOTTLE at $68, exactly as the card says. Squarespace inherits the
slug stem from whatever product was duplicated to create a new one, so the stem
is decorative and tells you nothing about the destination. The error came from
reading the slug instead of opening the page. Both Sentinel bottles are correct
links at correct prices; both are sold out. Nothing about them is edited here
except the stock tag.

WHAT IS ACTUALLY WRONG, all verified by opening the page on 17 Sept 2026:

  DEAD PRODUCTS (URL soft-redirects to the seller's homepage — the product is
  gone, so the card sends a reader nowhere useful):
    · Breezy Golf 22oz Sports Bottle
    · Quiet Golf x SSC MiiR Water Bottle 20oz

  STALE PRICES (post figure -> live figure):
    · Gumtree NY Branches Nalgene        ~$46 -> $42
    · Gumtree Field Research Nalgene     ~$46 -> $40
    · Manors 500ml Explorer              ~$30 -> $34   (the OTHER post already
                                                        says ~$34 — they
                                                        disagreed with each
                                                        other)
    · MARK & LONA Golf OR Cafe Tumbler   ~$55 -> $49
    · SIC 27oz Dimpled Golf              ~$30 -> $31.99

  SOLD OUT but listed as if buyable:
    · Sentinel Basecamp Water Bottle $68
    · Sentinel Basecamp Hybrid Bottle $72
    · Manors 500ml Explorer $34
    · Gumtree Field Research Nalgene $40
    · Tomorrow Golf Reusable Bottle 500ml

VERIFIED CORRECT, left alone: Vessel x MiiR $39, Bivo Trio $49, Gumtree NY
Branches (in stock at $42), and every collection/blog-level link in both posts
(they resolve; they are just coarse targets).

WHAT THIS SCRIPT WILL NOT DO. It does not add replacement products for the two
dead ones. New picks go in front of Lenny first — that is the house rule, and a
link audit is not a licence to edit the lineup. The dead cards are REMOVED, the
counts in the surrounding copy are corrected to match, and the gap is his call.

The sold-out tag follows the divot-tools convention: " &middot; sold out"
appended inside .product-name, which needs no new CSS.
"""
import re, sys, os, html

apply_ = "--apply" in sys.argv
A = "drops/11-water-bottles-wed-actually-carry.html"
B = "drops/the-water-bottle-edit.html"
SOLD = " &middot; sold out"

# (file, exact product-name text, new product-name text)
PRICE = [
 (A, "NY Branches Nalgene &middot; ~$46",        "NY Branches Nalgene &middot; $42"),
 (A, "NY Branches Nalgene · ~$46",               "NY Branches Nalgene · $42"),
 (A, "Field Research Dept. Nalgene &middot; ~$46","Field Research Dept. Nalgene &middot; $40"),
 (A, "Field Research Dept. Nalgene · ~$46",      "Field Research Dept. Nalgene · $40"),
 (A, "500ml Explorer &middot; ~$30",             "500ml Explorer &middot; $34"),
 (A, "500ml Explorer · ~$30",                    "500ml Explorer · $34"),
 (B, "Explorer Bottle 500ml &middot; ~$34",      "Explorer Bottle 500ml &middot; $34"),
 (B, "Golf OR Caf&eacute; Tumbler 650ml &middot; ~$55",
     "Golf OR Caf&eacute; Tumbler 650ml &middot; $49"),
 (B, "27oz Sport Bottle &middot; ~$30",          "27oz Sport Bottle &middot; $31.99"),
]

# (file, product-name text AFTER the price pass, to be tagged sold out)
SOLDOUT = [
 (A, "Basecamp Water Bottle · $68"),
 (A, "Basecamp Water Bottle &middot; $68"),
 (A, "Basecamp Hybrid Bottle · $72"),
 (A, "Basecamp Hybrid Bottle &middot; $72"),
 (A, "500ml Explorer · $34"),
 (A, "500ml Explorer &middot; $34"),
 (A, "Field Research Dept. Nalgene · $40"),
 (A, "Field Research Dept. Nalgene &middot; $40"),
 (B, "Explorer Bottle 500ml &middot; $34"),
 (B, "Reusable Bottle 500ml &middot; ~$15"),
]

# products whose page no longer exists — the whole card goes
DEAD = [
 (B, "https://breezygolf.com/products/breezy-22oz-sports-bottle-navy", "Breezy Golf 22oz Sports Bottle"),
 (B, "https://www.sugarloafsocialclub.com/products/quiet-golf-miir-water-bottle",
     "Quiet Golf x SSC MiiR Water Bottle"),
]

files = {A: open(A, encoding="utf-8").read(), B: open(B, encoding="utf-8").read()}
log = []

# ---------------------------------------------------------------- 1. prices
for f, old, new in PRICE:
    if old in files[f]:
        n = files[f].count(old)
        files[f] = files[f].replace(old, new)
        log.append(f"{os.path.basename(f)}  price  {old}  ->  {new}  (x{n})")

# ------------------------------------------------------------- 2. sold out
for f, name in SOLDOUT:
    # only inside .product-name, and only once per card
    pat = re.compile(r'(product-name"[^>]*>)' + re.escape(name) + r'(</div>)')
    if pat.search(files[f]):
        n = len(pat.findall(files[f]))
        files[f] = pat.sub(lambda m: m.group(1) + name + SOLD + m.group(2), files[f])
        log.append(f"{os.path.basename(f)}  stock  {name}  -> + sold out  (x{n})")

# ------------------------------------------------------- 3. dead cards out
for f, url, label in DEAD:
    t = files[f]
    # cards are either <a href=...class="product-card">...</a> or
    # <div class="product-card">...</div> with the link inside. Handle both.
    m = re.search(r'<a href="' + re.escape(url) + r'"[^>]*class="product-card">.*?</a>', t, re.S)
    if not m:
        s = t.find(url)
        if s == -1:
            log.append(f"  !! {os.path.basename(f)}: {label} not found — nothing removed")
            continue
        cs = t.rfind('<div class="product-card"', 0, s)
        if cs == -1:
            log.append(f"  !! {os.path.basename(f)}: no card wrapper round {label}")
            continue
        depth, j, end = 0, cs, None
        while j < len(t):
            mm = re.compile(r"<div\b|</div>").search(t, j)
            if not mm:
                break
            if mm.group(0).startswith("<div"):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = mm.end(); break
            j = mm.end()
        if end is None:
            log.append(f"  !! {os.path.basename(f)}: unbalanced card round {label}")
            continue
        block = t[cs:end]
    else:
        cs, end, block = m.start(), m.end(), m.group(0)
    if url not in block:
        log.append(f"  !! {os.path.basename(f)}: refusing to delete a block that lacks {label}'s URL")
        continue
    if block.count("product-card") != 1:
        log.append(f"  !! {os.path.basename(f)}: block spans more than one card — aborting {label}")
        continue
    # take the trailing blank line with it
    e = end
    while e < len(t) and t[e] in "\n ":
        e += 1
    files[f] = t[:cs] + t[e:]
    log.append(f"{os.path.basename(f)}  REMOVED dead product card: {label}")

# ------------------------------------------- 4. counts in the surrounding copy
removed_B = sum(1 for f, *_ in DEAD if f == B)
if removed_B:
    n_after = files[B].count('class="product-card"')
    for old, new in [("Sixteen bottles", f"{n_after} bottles"), ("sixteen bottles", f"{n_after} bottles"),
                     ("16 bottles", f"{n_after} bottles")]:
        if old in files[B]:
            files[B] = files[B].replace(old, new)
            log.append(f"{os.path.basename(B)}  count  '{old}' -> '{new}'")

# ---------------------------------------------------------------- 5. guards
problems = []
for f, t in files.items():
    n = t.count('class="product-card"')
    if n < 8:
        problems.append(f"{f}: only {n} product cards left — something over-deleted")
    if t.count("<div") != t.count("</div>"):
        problems.append(f"{f}: unbalanced divs after edit")
    if t.count("<a ") != t.count("</a>"):
        problems.append(f"{f}: unbalanced anchors after edit")
    for _f, url, label in DEAD:
        if _f == f and url in t:
            problems.append(f"{f}: dead URL for {label} survived removal")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", html.unescape(t)), re.I) and "worth" not in f:
        pass  # legacy slugs are exempt; verify-post.py owns this check
    if SOLD.strip() in t and t.count("sold out") > 12:
        problems.append(f"{f}: suspicious number of sold-out tags")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    for f, t in files.items():
        open(f, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + " — water bottle link + price audit, 17 Sept 2026")
for l in log:
    print("  ·", l)
CARD = 'class="product-card"'
for f, t in files.items():
    print(f"  {os.path.basename(f):42} {t.count(CARD)} cards")
if not apply_:
    print("\npass --apply to write")
