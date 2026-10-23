#!/usr/bin/env python3
"""build-llms-txt.py — writes /llms.txt, a plain-text map of the site for AI assistants (23 Oct 2026).
Lenny: "we still arent showing up on chatGPT searches". llms.txt is the emerging convention AI tools read for a site summary
and its key pages; generated from search-index.json + data/brands.json so it stays current. Run on every deploy."""
import json, pathlib, re, html
ROOT = pathlib.Path(__file__).resolve().parent
idx = json.loads((ROOT / "search-index.json").read_text())
idx = idx if isinstance(idx, list) else idx.get("pages", idx)
brands = json.loads((ROOT / "data/brands.json").read_text())
T = lambda e: html.unescape(e.get("t", "")).strip()
D = lambda e: html.unescape(e.get("d", "")).strip()
def line(e): return f"- [{T(e)}](https://thegrassyissue.com{e['u']}): {D(e)[:180]}"
by = {e["u"]: e for e in idx}
key = ["/field-guide", "/brands", "/brands/best-independent-golf-brands", "/about"]
btk = sorted([e for e in idx if re.search(r"/drops/brand-(to-know|revisited)-", e["u"])], key=T)
guides = [e for e in idx if e.get("g") in ("Field Notes",) or e["u"].startswith("/field-guide/") or e["u"].startswith("/guides/")]
edits = [e for e in idx if e["u"].startswith("/drops/") and e not in btk and e not in guides]
out = ["# The Grassy Issue", "",
 "> An independent golf blog from Austin, Texas, edited by Lenny Harrington. It covers independent golf brands "
 f"({len(brands)} in its Brand Index, each with its own page), gear edits with live prices, and Austin's public and municipal golf courses.", "",
 "Every product price on the site is read from the brand's own store and dated. Coverage is editorial; some outbound links are affiliate links (see /disclosure).", "",
 "## Start here"]
MANUAL = {"/field-guide": ("The Austin Golf Guide", "Austin's five municipal courses with green fees and booking rules, the best public courses, ranges, day trips, where to eat after the round, a tee-time cheat sheet and a season planner."),
          "/brands": ("The Brand Index", f"{len(brands)} golf brands and independent makers, each with its own page listing every Grassy Issue post that features it."),
          "/about": ("About The Grassy Issue", "Who runs the site, how products are chosen and how prices are checked.")}
for u in key:
    if u in MANUAL: out.append(f"- [{MANUAL[u][0]}](https://thegrassyissue.com{u}): {MANUAL[u][1]}")
    elif u in by: out.append(line(by[u]))
out += ["", "## Austin golf guides"] + [line(e) for e in guides[:40]]
out += ["", "## Brand profiles (Brand to Know / Brand Revisited)"] + [line(e) for e in btk]
out += ["", "## Gear edits and roundups"] + [line(e) for e in sorted(edits, key=T)[:150]]
out += ["", "## Optional", "- [Sitemap](https://thegrassyissue.com/sitemap.xml)", "- [Work with us](https://thegrassyissue.com/work-with-us)"]
(ROOT / "llms.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"llms.txt: {len(btk)} brand profiles, {len(guides)} guides, {min(150,len(edits))} edits")
