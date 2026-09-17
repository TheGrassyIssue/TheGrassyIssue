#!/usr/bin/env python3
"""How many words of prose on this site are actually ABOUT each brand.

This is the signal fix-thin-brand-pages.py uses to decide which brand pages stay
indexed, replacing brand-mentions.json's profile:true flag — which was wrong for
33 brands because every brand inside a multi-brand roundup got flagged as having
a profile.

TWO EXTRACTION BUGS THIS VERSION FIXES, both found by sanity-checking the output
against brands we know the coverage for:

  ENTITIES FIRST. The earlier pass blanked every &xxx; entity before matching, so
  "Apr&egrave;s Golf" became "Apr s Golf" and Apres Golf measured 99 words against
  a dedicated profile post. Entities are now decoded, THEN accents folded.

  SHORT NAMES. A 4-character floor on match keys dropped "OVO" and "PXG"
  entirely, and both measured zero. The floor is 3 with whole-word matching, so a
  short name still cannot match inside a longer word.

Writes research/brand-source-v3.json.
"""
import json, re, os, html as H, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
mentions = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json"), encoding="utf-8"))

def fold(s):
    s = H.unescape(s)                                   # entities BEFORE anything else
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip()

TRAIL = r"\s+(Golf|Shirts|Sports Co\.?|Co\.?|Company|Design|Headcovers|Putters|Irons|Grips|Studio|Club|Collection)\b.*$"

def keys_for(name, slug):
    n = fold(name)
    ks = {n, re.sub(TRAIL, "", n).strip(), fold(slug.replace("-", " "))}
    return sorted({k for k in ks if len(k) >= 3}, key=len, reverse=True)

def about(name, slug, path):
    if not os.path.exists(path):
        return []
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    blocks = [m.group(1) for m in re.finditer(r'<div class="product-body">(.*?)</div>\s*</div>', t, re.S)]
    blocks += [m.group(1) for m in re.finditer(r"<(?:p|li)[^>]*>(.*?)</(?:p|li)>", t, re.S)]
    pats = [re.compile(r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?![A-Za-z0-9])", re.I)
            for k in keys_for(name, slug)]
    out = []
    for s in blocks:
        s = fold(re.sub(r"<[^>]+>", " ", s))
        if len(s.split()) < 15:
            continue
        if any(p.search(s) for p in pats) and s not in out:
            out.append(s)
    return out

rows = {}
for r in brands:
    src = []
    for p in mentions.get(r["slug"], []):
        src += about(r["name"], r["slug"], os.path.join(ROOT, p["url"].lstrip("/") + ".html"))
    seen, ded = set(), []
    for s in src:
        k = s[:60]
        if k not in seen:
            seen.add(k); ded.append(s)
    rows[r["slug"]] = {"name": r["name"], "posts": len(mentions.get(r["slug"], [])),
                       "words": sum(len(x.split()) for x in ded), "src": ded[:8]}

json.dump(rows, open(os.path.join(ROOT, "research", "brand-source-v3.json"), "w"),
          indent=1, ensure_ascii=False)

# every brand with a GENUINE dedicated profile post must measure well over the
# floor; if one does not, the extractor is broken again rather than the brand thin
real = set(json.load(open(os.path.join(ROOT, "research", "profile-truth.json"),
                          encoding="utf-8"))["real"])
susp = sorted((rows[s]["words"], rows[s]["name"]) for s in real if rows[s]["words"] < 300)
ws = sorted(v["words"] for v in rows.values())
print(f"{len(rows)} brands | words about them: min {ws[0]} median {ws[len(ws)//2]} max {ws[-1]}")
for lo, hi in [(0, 150), (150, 300), (300, 1000), (1000, 10 ** 9)]:
    print(f"  {lo:>4}-{hi if hi < 10**8 else '+':>5} : {sum(1 for w in ws if lo <= w < hi):>3}")
if susp:
    raise SystemExit("\nbrands WITH a dedicated profile measuring under 300 words — "
                     "the extractor is missing them:\n  " +
                     "\n  ".join(f"{w:>4}w  {n}" for w, n in susp))
print("\nsanity: every brand with a dedicated profile clears 300 words")
