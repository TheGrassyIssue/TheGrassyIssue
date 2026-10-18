#!/usr/bin/env python3
"""apply-pick-of-week.py — "Our Favorite Story This Week" block (renamed from Lenny's Pick, 17 Oct 2026) at the top of the homepage (17 Oct 2026).
Lenny: "I want a place on the top of the home page where we can put my favorite story of the week".
Reads data/pick-of-week.json (url, image, week, note); title comes from the post's own <h1>. Overlaid on the hero (bottom right; full-width card on phones), was between the hero and the
feed filters, marked <!-- TGI-PICK --> so reruns replace it in place. Empty url removes the block. Idempotent; runs after
paginate-feed in Deploy. Dry run without --apply."""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
D = json.loads((ROOT / "data/pick-of-week.json").read_text())
S, E = "<!-- TGI-PICK -->", "<!-- /TGI-PICK -->"
CSS = ('<style data-tgi="pick-css">.hero .tgi-pick{position:absolute;right:32px;bottom:24px;z-index:4;width:min(470px,42vw);background:#DDE6D4;color:var(--ink);border-top:3px solid var(--grass);box-shadow:0 10px 30px rgba(0,0,0,.28)}'
       '.tgi-pick-in{display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:center;padding:12px}'
       '.tgi-pick-img{display:block;overflow:hidden;border-bottom:none;outline:.5px solid var(--ink)}.tgi-pick-img img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;transition:transform .4s}'
       '.tgi-pick-img:hover img{transform:scale(1.04)}.tgi-pick-kick{font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;display:flex;gap:8px;align-items:center;flex-wrap:wrap}'
       '.tgi-pick-kick b{background:var(--grass);color:var(--paper);padding:3px 7px;font-weight:500}.tgi-pick-kick span{opacity:.6}'
       '.tgi-pick h2{font-family:var(--serif);font-size:22px;line-height:1.1;margin:7px 0 5px;letter-spacing:-.01em}.tgi-pick h2 a{color:var(--grass);border-bottom:none;text-decoration:none}'
       '.tgi-pick p{font-family:var(--serif);font-size:13.5px;line-height:1.4;margin:0 0 7px;opacity:.85;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}'
       '.tgi-pick-foot{font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase}.tgi-pick-go{color:var(--ink);border-bottom:1px solid var(--ink);padding-bottom:2px}'
       '@media(max-width:900px){.hero .tgi-pick{width:min(420px,55vw)}.tgi-pick p{display:none}}'
       '@media(max-width:760px){.hero{min-height:290px!important;max-height:none!important;height:auto!important}.hero .hero-bottom{padding-bottom:96px}'
       '.hero .tgi-pick{left:12px;right:12px;bottom:12px;width:auto}.tgi-pick-in{grid-template-columns:72px 1fr;gap:10px;padding:9px}'
       '.tgi-pick-kick span{display:none}.tgi-pick h2{font-size:16px;margin:5px 0 4px}.tgi-pick-foot{font-size:8.5px}}</style>\n')
def block():
    url = D.get("url", "").strip()
    if not url: return ""
    post = (ROOT / (url.lstrip("/") + ".html")).read_text(encoding="utf-8")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", post, re.S).group(1).strip()
    title_txt = html.unescape(re.sub(r"<[^>]+>", "", h1))
    focus = f' style="object-position:{D["focus"]}"' if D.get("focus") else ""
    img = D["image"]; assert (ROOT / img.lstrip("/")).is_file(), img
    return (f'{S}\n<section class="tgi-pick" aria-label="Our favorite story this week"><div class="tgi-pick-in">'
            f'<a class="tgi-pick-img" href="{url}"><img src="{img}" alt="{html.escape(title_txt, quote=True)}" loading="eager"{focus} /></a>'
            f'<div><div class="tgi-pick-kick"><b>Our Favorite Story This Week</b><span>{html.escape(D.get("week",""))}</span></div>'
            f'<h2><a href="{url}">{h1}</a></h2><p>{html.escape(D.get("note",""))}</p>'
            f'<div class="tgi-pick-foot"><a class="tgi-pick-go" href="{url}">Read it &rarr;</a></div></div></div></section>\n{E}\n')
t = HOME.read_text(encoding="utf-8"); u = t
u = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", u, flags=re.S)
# Overlay: the block sits inside the hero, just before the hero's closing tag.
hs = u.index('<section class="hero"'); he = u.index('</section>', hs)
u = u[:he] + block() + u[he:]
u = re.sub(r'<style data-tgi="pick-css">.*?</style>\n?', '', u, flags=re.S)
if D.get("url", "").strip(): u = u.replace("</head>", CSS + "</head>", 1)
changed = u != t
if changed and "--apply" in sys.argv: HOME.write_text(u, encoding="utf-8")
print(f"apply-pick-of-week: {D.get('url') or '(hidden)'} — {'updated' if changed else 'unchanged'}{'' if '--apply' in sys.argv or not changed else ' (dry run)'}")
