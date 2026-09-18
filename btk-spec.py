#!/usr/bin/env python3
"""
btk-spec.py — derive a Brand to Know spec from the page that already exists.
18 September 2026.

WHY THIS DERIVES RATHER THAN WRITES
------------------------------------
Rolling the redesigned format across 34 pages needs a spec for each. Written by
hand that is 34 opinions, 136 connective lines and 170 pick annotations — and
every one of them would be copy nobody has checked, on a page that is already
live. Lenny chose the other route: "split the existing write-up."

So every field here comes from something already published and already
approved:

    take        the first paragraph of the page's own .writeup
    story       the rest of that .writeup, unchanged
    card        the page's own .sidebar-card, lifted verbatim
    collection  the headings the product grids already sit under
    related     neighbours from brands.json, described with the `line` that
                brands.json already holds for them

NOTHING IS INVENTED. The one thing the Hiroki page has that these will not is
START HERE, because its five annotations are the only part of that spec that
could not be derived. A page gets that section when somebody writes the picks;
until then it is absent rather than filled with a machine's guess at why a
product matters.

WHAT IT REFUSES TO DO
---------------------
  - split a write-up of fewer than two paragraphs (there is no Take to take)
  - group products it cannot find a heading for (they would vanish)
  - name a related brand that has no image or no line in brands.json

USAGE
    python3 btk-spec.py --all            # write specs for every eligible page
    python3 btk-spec.py seamus manors    # just these
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SPECS = ROOT / "research" / "btk"
EMPTY = {"aug-11", "beams-golf", "found-golf", "merrill-golf",
         "morning-people-clothiers", "olydoe"}          # no products at all


def brands():
    d = json.loads((ROOT / "data" / "brands.json").read_text(encoding="utf-8"))
    return d["brands"] if isinstance(d, dict) else d


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def writeup_paras(html):
    m = re.search(r'<div class="writeup">(.*?)(?=<section|<div class="btk-card")',
                  html, re.S)
    if not m:
        return []
    # DON'T GUESS WHERE THE BODY ENDS. The old regex stopped at the first
    # </div> followed by </div> or <aside, which on Birds of Condor is a div
    # NESTED inside the body — so it captured 1 of 3 paragraphs and the page was
    # skipped for "nothing to split". The whole write-up block is already
    # bounded by the caller; every <p> inside it is write-up copy.
    return [p.strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S)]


def sidebar(html):
    m = re.search(r'<aside class="sidebar">(.*?)</aside>', html, re.S)
    if not m:
        return None
    blk = m.group(1)
    # TWO ROW SHAPES. Most pages write <span class="l">Label</span><span>Value
    # </span>; J.Lindeberg writes <strong>Label</strong>Value. Only the first was
    # recognised, so its Brand Card read as absent and the page was skipped.
    rows = [[text(a), text(b)] for a, b in re.findall(
        r'<div class="sidebar-detail"><span class="l">(.*?)</span><span>(.*?)</span></div>',
        blk, re.S)]
    if not rows:
        rows = [[text(a), text(b)] for a, b in re.findall(
            r'<div class="sidebar-detail"><strong>(.*?)</strong>(.*?)</div>', blk, re.S)]
    lab = re.search(r'<div class="sidebar-label">(.*?)</div>', blk, re.S)
    cta = re.search(r'<a href="([^"]+)"[^>]*class="sidebar-cta">(.*?)</a>', blk, re.S)
    tags = re.findall(r'<span class="hashtag">#(.*?)</span>', blk, re.S)
    if not (rows and cta):
        return None
    return {"label": text(lab.group(1)) if lab else "Details", "rows": rows,
            "cta": {"href": cta.group(1), "text": cta.group(2).strip()},
            "hashtags": [text(t) for t in tags]}


def collection(html):
    """Each products-grid and the heading it already sits under."""
    out = []
    for g in re.finditer(r'<div class="products-grid">', html):
        pre = html[max(0, g.start() - 900):g.start()]
        hd = re.findall(r"<h2[^>]*>(.*?)</h2>", pre, re.S)
        if not hd:
            return None                       # a grid with no heading: refuse
        names = []
        seg = html[g.start():]
        nxt = seg.find('<div class="products-grid">', 10)
        seg = seg[:nxt] if nxt > 0 else seg
        for n in re.findall(r'<div class="product-name">(.*?)</div>', seg, re.S):
            # PLAIN TEXT, not markup. Product names carry sold-out spans and
            # currency notes ("A$69 <span>(about US$49)</span>"); storing the
            # raw HTML made every one of them unmatchable on the template side.
            names.append(text(n))
        if names:
            out.append({"hdr": hd[-1].strip(), "match": names})
    return out or None


def related(slug, B):
    me = next((b for b in B if b["slug"] == slug), None)
    if not me:
        return []
    mine, myreg = set(me.get("cats", [])), set(me.get("regions", []))
    scored = []
    for b in B:
        if b["slug"] == slug or not b.get("img") or not b.get("line"):
            continue
        s = len(mine & set(b.get("cats", []))) * 2 + len(myreg & set(b.get("regions", [])))
        if s:
            scored.append((s, b))
    scored.sort(key=lambda x: (-x[0], x[1]["slug"]))
    # the "why" is the brand's OWN line from brands.json — already approved copy
    return [{"slug": b["slug"], "why": b["line"]} for _, b in scored[:4]]


def derive_card(slug, html, B):
    """Eight pages never had a .sidebar-card. Rather than skip them, build one
    out of facts already ON the page: the brand's own entry in brands.json, the
    product count, the price range read off the product names, and the store
    link the products already point at. Nothing here is a new claim."""
    b = next((x for x in B if x["slug"] == slug), None)
    if not b:
        return None
    names = re.findall(r'<div class="product-name">(.*?)</div>', html, re.S)
    prices = [float(m.group(1).replace(",", ""))
              for n in names for m in [re.search(r"\$([\d,]+(?:\.\d\d)?)", n)] if m]
    host = None
    # ATTRIBUTE ORDER. The markup is <a href="..." target rel class="product-link">,
    # so a pattern that looks for the class first finds nothing — which is why
    # all eight of these pages reported "not enough in brands.json" when the
    # real problem was this regex.
    for u in re.findall(r'<a href="(https?://[^"]+)"[^>]*class="product-link"', html):
        host = u.split("/")[0] + "//" + u.split("/")[2]
        break
    if not host:
        return None
    rows = []
    if b.get("loc"):
        rows.append(["Based", b["loc"]])
    if b.get("cats"):
        rows.append(["Known For", ", ".join(c.title() for c in b["cats"][:3])])
    rows.append(["Pieces", f"{len(names)} items"])
    if prices:
        lo, hi = min(prices), max(prices)
        fmt = lambda v: f"${int(v):,}" if v == int(v) else f"${v:,.2f}"
        rows.append(["Range", f"{fmt(lo)} &ndash; {fmt(hi)}"])
    tags = [re.sub(r"[^a-z0-9]", "", slug)] + ["brandtoknow"] + \
           [re.sub(r"[^a-z0-9]", "", c) for c in b.get("cats", [])[:2]]
    return {"label": "Details", "rows": rows,
            "cta": {"href": host + "/", "text": f"Shop {b['name']} &rarr;"},
            "hashtags": tags}


def build(slug, B):
    page = ROOT / "drops" / f"brand-to-know-{slug}.html"
    if not page.exists():
        return None, "no page"
    h = page.read_text(encoding="utf-8")
    paras = writeup_paras(h)
    if len(paras) < 2:
        return None, f"write-up has {len(paras)} paragraph(s) — nothing to split"
    col = collection(h)
    if not col:
        return None, "could not group products under headings"
    card = sidebar(h) or derive_card(slug, h, B)
    if not card:
        return None, "no Brand Card, and not enough in brands.json to derive one"
    name = next((b["name"] for b in B if b["slug"] == slug), slug.replace("-", " ").title())
    rel = related(slug, B)
    if len(rel) < 3:
        return None, f"only {len(rel)} related brands with an image and a line"
    return {"slug": slug, "brand": name, "page": page.name,
            "take": [paras[0]],                 # the verdict
            "story_extra": paras[1:],           # stays in The Story
            "card": card, "collection": col, "related": rel}, "ok"


if __name__ == "__main__":
    B = brands()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    slugs = args or sorted(
        p.stem.replace("brand-to-know-", "")
        for p in (ROOT / "drops").glob("brand-to-know-*.html"))
    SPECS.mkdir(parents=True, exist_ok=True)
    ok = skip = 0
    for s in slugs:
        if s in EMPTY or s == "hiroki-golf":
            continue
        spec, why = build(s, B)
        if not spec:
            print(f"  SKIP {s:<24} {why}")
            skip += 1
            continue
        (SPECS / f"{s}.json").write_text(
            json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ok   {s:<24} {len(spec['collection'])} categories, "
              f"{sum(len(c['match']) for c in spec['collection'])} products, "
              f"{len(spec['related'])} related")
        ok += 1
    print(f"\n  {ok} spec(s) written, {skip} skipped")
