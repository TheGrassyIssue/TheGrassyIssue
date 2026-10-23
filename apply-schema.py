#!/usr/bin/env python3
"""apply-schema.py — entity schema for The Grassy Issue (Lenny, 15 Oct 2026: "let's do the first two items").

What it adds, idempotently, to every deployed page:
  1. Brand entities: each /brands/<slug> page gets a Brand JSON-LD block (@id .../brands/<slug>#brand)
     from data/brands.json + data/brand-stores.json (official site) and declares the page is about it.
  2. Article mentions: every post's Article block gets "mentions" -> the Brand @ids for the brands that
     post covers (inverted from data/brand-mentions.json), and its publisher gets "@id": .../#org.
  3. One publisher identity: index.html gets an Organization block (@id .../#org); the existing WebSite
     block's publisher points to it.
  4. BreadcrumbList on every post / guide / brand page that lacks one, built from the visible breadcrumb
     (or Feed > section > title when a page has none).

Our own blocks carry data-tgi="schema-*" so re-runs replace rather than duplicate. Builders that rewrite
a page drop these; that's why this runs in Deploy TGI.command. Dry run by default; --apply writes.
Every block is json-validated before any file is written; a failure aborts the whole run.
"""
import glob
import html as H
import json
import re
import sys

ROOT_URL = "https://thegrassyissue.com"
ORG_ID = f"{ROOT_URL}/#org"
LD_RE = re.compile(r'<script type="application/ld\+json"( data-tgi="[^"]*")?>(.*?)</script>\n?', re.S)

BRANDS = {b["slug"]: b for b in json.load(open("data/brands.json"))}
STORES = json.load(open("data/brand-stores.json"))["stores"]
MENTIONS = json.load(open("data/brand-mentions.json"))
POST_BRANDS = {}
for slug, entries in MENTIONS.items():
    if slug not in BRANDS:
        continue
    for e in entries:
        POST_BRANDS.setdefault(e["url"].split("#")[0], set()).add(slug)

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "The Grassy Issue",
    "alternateName": ["TGI", "Grassy Issue"],
    "url": f"{ROOT_URL}/",
    "logo": f"{ROOT_URL}/apple-touch-icon.png",
    "description": "An independent golf blog from Austin, Texas, covering small golf brands, new drops, gear and public-course golf.",
    "knowsAbout": ["Golf", "Independent golf brands", "Golf apparel", "Golf equipment", "Public golf courses", "Austin golf"],
    "sameAs": ["https://instagram.com/thegrassyissue"],
    "founder": {"@type": "Person", "@id": f"{ROOT_URL}/about#lenny", "name": "Lenny Harrington"},
}


def brand_ref(slug):
    return {"@type": "Brand", "@id": f"{ROOT_URL}/brands/{slug}#brand", "name": BRANDS[slug]["name"]}


def brand_entity(slug):
    b = BRANDS[slug]
    desc = " ".join(x for x in (b.get("loc", "") + ".", H.unescape(re.sub(r"<[^>]+>", "", b.get("line", "")))) if x.strip(". "))
    ent = {
        "@context": "https://schema.org",
        "@type": "Brand",
        "@id": f"{ROOT_URL}/brands/{slug}#brand",
        "name": b["name"],
        "description": desc.strip(),
        "subjectOf": {"@type": "CollectionPage", "@id": f"{ROOT_URL}/brands/{slug}"},
    }
    st = STORES.get(slug)
    if st and st.get("url"):
        ent["url"] = st["url"]
    if b.get("img"):
        ent["image"] = ROOT_URL + b["img"]
    return ent


def block(obj, tag):
    return f'<script type="application/ld+json" data-tgi="{tag}">\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>\n'


def crumbs_from_page(s, url, title, section):
    m = re.search(r'<div class="breadcrumb">(.*?)</div>', s, re.S)
    items = []
    if m:
        inner = m.group(1)
        parts = re.split(r"<span>\s*/\s*</span>", inner)
        for p in parts:
            a = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', p, re.S)
            if a:
                href = a.group(1)
                href = ROOT_URL + href if href.startswith("/") else href
                items.append((H.unescape(re.sub(r"<[^>]+>|\s+", " ", a.group(2))).strip(), href))
            else:
                t = H.unescape(re.sub(r"<[^>]+>", " ", p))
                t = re.sub(r"\s+", " ", t).strip()
                if t:
                    items.append((t, None))
    if len(items) < 2:
        items = [("Feed", f"{ROOT_URL}/"), section, (title, None)]
    # an unlinked middle crumb has no URL of its own; drop it rather than repeat this page's URL
    items = [it for j, it in enumerate(items) if it[1] or j == len(items) - 1]
    out = []
    for i, (name, href) in enumerate(items, 1):
        out.append({"@type": "ListItem", "position": i, "name": name, "item": href or url})
    out[-1]["item"] = url
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": out}


def page_title(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S) or re.search(r"<title>(.*?)</title>", s, re.S)
    t = H.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else ""
    return re.sub(r"\s+", " ", t.split(" | The Grassy Issue")[0].split(" — The Grassy Issue")[0]).strip()


def strip_ours(s):
    return LD_RE.sub(lambda m: "" if (m.group(1) or "").startswith(' data-tgi="schema-') else m.group(0), s)


def insert_before_head(s, blocks):
    i = s.index("</head>")
    return s[:i] + "".join(blocks) + s[i:]


def process(path):
    s0 = open(path, encoding="utf-8").read()
    s = strip_ours(s0)
    rel = path[:-5]
    url = f"{ROOT_URL}/" if rel == "index" else f"{ROOT_URL}/{rel}".replace("/index", "")
    adds = []
    stats = {}

    # Article blocks: publisher @id + mentions
    def fix_article(m):
        attr, body = m.group(1), m.group(2)
        try:
            obj = json.loads(body)
        except Exception:
            return m.group(0)
        if not isinstance(obj, dict) or obj.get("@type") not in ("Article", "NewsArticle", "BlogPosting"):
            return m.group(0)
        pub = obj.get("publisher") or {}
        if isinstance(pub, dict):
            pub = {"@type": "Organization", "@id": ORG_ID, "name": pub.get("name", "The Grassy Issue"), "url": pub.get("url", f"{ROOT_URL}/")}
            obj["publisher"] = pub
        key = "/" + rel
        slugs = sorted(POST_BRANDS.get(key, ()), key=lambda x: BRANDS[x]["name"].lower())
        if slugs:
            obj["mentions"] = [brand_ref(x) for x in slugs]
            stats["mentions"] = len(slugs)
        else:
            obj.pop("mentions", None)
        return f'<script type="application/ld+json"{attr or ""}>\n{json.dumps(obj, indent=1, ensure_ascii=False)}\n</script>\n'

    s = LD_RE.sub(fix_article, s)

    # Brand pages
    if rel.startswith("brands/") and rel != "brands/index":
        slug = rel.split("/", 1)[1]
        if slug in BRANDS:
            adds.append(block(brand_entity(slug), "schema-brand"))
            stats["brand"] = 1

    # Homepage org + WebSite publisher pointer
    if rel == "index":
        adds.append(block(ORG, "schema-org"))
        def fix_site(m):
            try:
                obj = json.loads(m.group(2))
            except Exception:
                return m.group(0)
            if isinstance(obj, dict) and obj.get("@type") == "WebSite":
                obj["publisher"] = {"@type": "Organization", "@id": ORG_ID, "name": "The Grassy Issue"}
                return f'<script type="application/ld+json"{m.group(1) or ""}>\n{json.dumps(obj, indent=2, ensure_ascii=False)}\n</script>\n'
            return m.group(0)
        s = LD_RE.sub(fix_site, s)
        stats["org"] = 1

    # Breadcrumbs where missing
    if rel != "index" and "BreadcrumbList" not in s:
        title = page_title(s)
        if rel.startswith("brands/"):
            section = ("Brands", f"{ROOT_URL}/brands")
            if rel == "brands/index":
                bl = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Feed", "item": f"{ROOT_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Brands", "item": url}]}
            else:
                name = BRANDS.get(rel.split("/", 1)[1], {}).get("name", title)
                bl = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Feed", "item": f"{ROOT_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Brands", "item": f"{ROOT_URL}/brands"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": url}]}
        elif rel.startswith("guides/"):
            bl = crumbs_from_page(s, url, title, ("Muni Guides", f"{ROOT_URL}/guides"))
        else:
            bl = crumbs_from_page(s, url, title, ("Drops & Brands", f"{ROOT_URL}/#feed"))
        adds.append(block(bl, "schema-breadcrumb"))
        stats["crumbs"] = 1

    if adds:
        s = insert_before_head(s, adds)
    # validate every LD block on the page
    for m in LD_RE.finditer(s):
        json.loads(m.group(2))
    return s0, s, stats


def main(apply_):
    files = sorted(set(glob.glob("drops/*.html") + glob.glob("guides/*.html") + glob.glob("brands/*.html")
                       + glob.glob("field-guide/*.html") + ["index.html", "about.html"]))
    files = [f for f in files if not re.search(r" \d\.html$", f)]
    out, totals, changed = {}, {"mentions": 0, "brand": 0, "org": 0, "crumbs": 0, "posts_with_mentions": 0}, 0
    for f in files:
        try:
            s0, s, st = process(f)
        except Exception as e:
            sys.exit(f"! {f}: {e} — nothing written")
        for k in ("brand", "org", "crumbs"):
            totals[k] += st.get(k, 0)
        if st.get("mentions"):
            totals["mentions"] += st["mentions"]; totals["posts_with_mentions"] += 1
        if s != s0:
            out[f] = s; changed += 1
    print(f"apply-schema: {len(files)} pages checked, {changed} to change | brand entities {totals['brand']} | "
          f"posts with brand mentions {totals['posts_with_mentions']} ({totals['mentions']} links) | "
          f"breadcrumbs added {totals['crumbs']} | org {totals['org']}")
    if not apply_:
        print("  dry run — pass --apply"); return
    for f, s in out.items():
        open(f, "w", encoding="utf-8").write(s)
    print("  written")


if __name__ == "__main__":
    main("--apply" in sys.argv)
