#!/usr/bin/env python3
"""build-rss.py — /rss.xml, the site's RSS feed (23 Oct 2026).
Lenny: "Let's reach out to Feedspot". Feedspot (and every feed reader) finds and lists blogs by their RSS feed;
TGI had none. Built from search-index.json (title, summary, image) + each post's JSON-LD datePublished/dateModified.
Newest 50 posts and guides. Also makes sure index.html advertises the feed with <link rel="alternate">. Run every deploy."""
import json, pathlib, re, html, datetime, email.utils
ROOT = pathlib.Path(__file__).resolve().parent
BASE = "https://thegrassyissue.com"
idx = json.loads((ROOT / "search-index.json").read_text())
items = []
for e in idx:
    u = e.get("u", "")
    if not (u.startswith("/drops/") or u.startswith("/guides/")):
        continue
    f = ROOT / (u.lstrip("/") + ".html")
    if not f.is_file():
        continue
    s = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', s)
    if not m:
        continue
    mod = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})', s)
    d = max(m.group(1), mod.group(1) if mod else m.group(1))
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    items.append((d, m.group(1), u, e.get("t", ""), html.unescape(desc.group(1)) if desc else e.get("d", ""), e.get("i", ""), e.get("g", "")))
items.sort(key=lambda x: (x[1], x[0]), reverse=True)
items = items[:50]
def rfc(d):
    dt = datetime.datetime.strptime(d, "%Y-%m-%d").replace(hour=12, tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
    return email.utils.format_datetime(dt)
esc = lambda x: html.escape(html.unescape(x), quote=True)
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:dc="http://purl.org/dc/elements/1.1/">',
       '<channel>',
       '<title>The Grassy Issue</title>', f'<link>{BASE}/</link>',
       f'<atom:link href="{BASE}/rss.xml" rel="self" type="application/rss+xml" />',
       '<description>An independent golf blog from Austin, Texas: small golf brands, new drops, gear and public-course golf, by Lenny Harrington.</description>',
       '<language>en-us</language>', f'<lastBuildDate>{rfc(items[0][0])}</lastBuildDate>',
       f'<image><url>{BASE}/apple-touch-icon.png</url><title>The Grassy Issue</title><link>{BASE}/</link></image>']
for d, pub, u, t, desc, img, cat in items:
    link = BASE + u
    out.append('<item>')
    out += [f'<title>{esc(t)}</title>', f'<link>{link}</link>', f'<guid isPermaLink="true">{link}</guid>',
            f'<pubDate>{rfc(pub)}</pubDate>', '<dc:creator>Lenny Harrington</dc:creator>']
    if cat: out.append(f'<category>{esc(cat)}</category>')
    out.append(f'<description>{esc(desc)}</description>')
    if img: out.append(f'<media:content url="{BASE}{esc(img)}" medium="image" />')
    out.append('</item>')
out += ['</channel>', '</rss>']
(ROOT / "rss.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
# advertise it on the homepage
LINK = '<link rel="alternate" type="application/rss+xml" title="The Grassy Issue" href="/rss.xml" />'
h = (ROOT / "index.html").read_text(encoding="utf-8")
if LINK not in h:
    h = h.replace("</head>", LINK + "\n</head>", 1); (ROOT / "index.html").write_text(h, encoding="utf-8")
print(f"rss.xml: {len(items)} items, newest {items[0][1]} {items[0][2]}")
