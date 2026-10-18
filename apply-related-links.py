#!/usr/bin/env python3
"""apply-related-links.py — a static "Keep Reading" block of three related posts on every post (17 Oct 2026).
Lenny: "My SEO rankings have dropped. Let's give all the recent pages a better chance to rank higher on google."
WHY: the "More from TGI" grid rotates in JavaScript, so Google sees a random, shifting set of links. Most posts from the last
month had only two to four crawlable internal links pointing at them (the homepage feed and a brand page). This adds a fixed,
relevant set of three links per post, chosen by shared brands (data/brand-mentions.json) with a bonus for recent posts, so new
posts pick up inbound links from the older pages Google already crawls often.
Placement: just before the first <div class="more"> (the Brand Index strip or the More from TGI grid). Marked <!-- TGI-RELATED -->; reruns replace
it. Skips links already in the post body. Idempotent; dry run without --apply."""
import glob, html, json, pathlib, re, sys, collections, datetime
ROOT = pathlib.Path(__file__).resolve().parent
S, E = "<!-- TGI-RELATED -->", "<!-- /TGI-RELATED -->"
MENT = json.loads((ROOT / "data/brand-mentions.json").read_text())
THUMB = json.loads((ROOT / "data/post-thumbs.json").read_text())
CSS = ('<style data-tgi="related-css">.tgi-rel{max-width:1200px;margin:56px auto 8px;padding:0 32px}.tgi-rel-h{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;border-bottom:.5px solid var(--ink);padding-bottom:10px;margin-bottom:16px}'
       '.tgi-rel-g{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.tgi-rel a{color:var(--ink);border-bottom:none;text-decoration:none;display:block}.tgi-rel img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;border:.5px solid var(--ink);margin-bottom:10px}'
       '.tgi-rel-c{font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin-bottom:4px}.tgi-rel-t{font-family:var(--serif);font-size:17px;line-height:1.25}.tgi-rel a:hover .tgi-rel-t{text-decoration:underline}'
       '@media(max-width:720px){.tgi-rel{padding:0 16px}.tgi-rel-g{grid-template-columns:1fr;gap:14px}.tgi-rel a{display:grid;grid-template-columns:110px 1fr;gap:12px;align-items:center}.tgi-rel img{margin:0}.tgi-rel-t{font-size:15px}}</style>\n')
posts = {}
for f in sorted(glob.glob(str(ROOT / "drops/*.html"))):
    if re.search(r" \d+\.html$", f): continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    if 'name="robots" content="noindex' in t: continue
    slug = pathlib.Path(f).stem; url = "/drops/" + slug
    m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', t)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if not (h1 and url in THUMB and '<div class="more"' in t): continue
    title_txt = re.sub(r"<[^>]+>", "", h1.group(1))
    nolink = bool(re.search(r"\bworth\b", re.sub(r"(?i)fort worth", "", title_txt), re.I))   # house banned word: host the block, never be linked
    posts[url] = dict(nolink=nolink, f=f, date=m.group(1) if m else "2026-06-01", title=re.sub(r"<[^>]+>", "", h1.group(1)).strip())
brands_of = collections.defaultdict(set)
for b, rows in MENT.items():
    for r in rows:
        if r["url"] in posts: brands_of[r["url"]].add(b)
today = max(p["date"] for p in posts.values())
def recent(u): return (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(posts[u]["date"])).days <= 45
inbound = collections.Counter()
def pick(u, body):
    mine = brands_of[u]
    cands = []
    for v in posts:
        if v == u or posts[v]['nolink'] or f'href="{v}"' in body: continue
        shared = len(mine & brands_of[v])
        if not shared: continue
        score = min(shared, 3) + (3 if recent(v) else 0) - 1.2 * inbound[v]
        cands.append((score, posts[v]["date"], v))
    cands.sort(reverse=True)
    out = [v for _, _, v in cands[:3]]
    if len(out) < 3:   # top up with recent posts that have the fewest links so far
        for v in sorted(posts, key=lambda x: (not recent(x), inbound[x], x)):
            if len(out) == 3: break
            if v != u and not posts[v]['nolink'] and v not in out and f'href="{v}"' not in body: out.append(v)
    for v in out: inbound[v] += 1
    return out
changed = 0
for u in sorted(posts, key=lambda x: posts[x]["date"]):   # oldest first, so newer posts collect inbound slots
    p = posts[u]; t = open(p["f"], encoding="utf-8").read()
    t0 = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", t, flags=re.S)
    body = t0[:t0.index('<div class="more"')]
    rel = pick(u, body)
    cards = "".join(f'<a href="{v}"><img src="{THUMB[v]["img"]}" alt="" loading="lazy" /><div class="tgi-rel-c">{html.escape(THUMB[v].get("cat",""))}</div><div class="tgi-rel-t">{posts[v]["title"]}</div></a>' for v in rel)
    block = f'{S}\n<section class="tgi-rel" aria-label="Keep reading"><div class="tgi-rel-h">Keep Reading</div><div class="tgi-rel-g">{cards}</div></section>\n{E}\n'
    i = t0.index('<div class="more"')
    u2 = t0[:i] + block + t0[i:]
    if 'data-tgi="related-css"' not in u2: u2 = u2.replace("</head>", CSS + "</head>", 1)
    if u2 != t:
        changed += 1
        if "--apply" in sys.argv: open(p["f"], "w", encoding="utf-8").write(u2)
rec = [u for u in posts if recent(u)]
print(f"apply-related-links: {len(posts)} posts, {changed} {'updated' if '--apply' in sys.argv else 'would change'}; "
      f"recent posts: {len(rec)}, min/median inbound from this block: {min(inbound[u] for u in rec)}/{sorted(inbound[u] for u in rec)[len(rec)//2]}")
