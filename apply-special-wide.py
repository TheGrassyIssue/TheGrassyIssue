#!/usr/bin/env python3
"""apply-special-wide.py — the homepage "Special Field Note" double-wide box.

4 Nov 2026. Lenny: "mock up an idea of a double wide box for more special stories on the homepage",
then "it's too tall let's make it more in line with the other boxes", "these will still be field notes",
"what if we put the split on the post box horizontaly?", "let's try it out and push the update".

What it does (IDEMPOTENT — removes its own previous output, then re-adds):
  1. CSS between /*TGI-SPECIAL-WIDE*/ markers in <head>.
  2. The card (between <!-- TGI-SPECIAL-WIDE --> markers) after the Nth regular card in the feed
     (data/special-field-notes.json "after_card", default 3). Content comes from that JSON file.
  3. Patches layoutMasonry() so a .card-wide spans two columns and its height matches a normal card.
     Regular cards then go into the shortest column (standard masonry) instead of strict left-to-right.

paginate-feed.py strips this block before it splits the feed, so the box never moves to /feed/page-N
and never de-duplicates the lead story's own card. Deploy TGI.command runs this right after
paginate-feed.py. Dry run by default; pass --apply.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
DATA = ROOT / "data/special-field-notes.json"
CARD_RE = re.compile(r'\n?<!-- TGI-SPECIAL-WIDE -->.*?<!-- /TGI-SPECIAL-WIDE -->\n?', re.S)
CSS_RE = re.compile(r'<style>/\*TGI-SPECIAL-WIDE\*/.*?</style>\n?', re.S)
FEED_OPEN = re.compile(r'<section class="feed"[^>]*>')
TOP_CARD = re.compile(r'<div class="card(?:\s[^"]*)?"')

CSS = """<style>/*TGI-SPECIAL-WIDE*/
.feed .card.card-wide{border:0.5px solid var(--ink);background:var(--ink);color:var(--paper)}
.card-wide .wide-in{display:grid;grid-template-columns:1fr;grid-template-rows:minmax(0,1fr) auto;height:var(--wide-h,auto)}
.card-wide .wide-media{position:relative;overflow:hidden;min-height:0;display:block;border:0}
.card-wide .wide-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease}
.card-wide:hover .wide-media img{transform:scale(1.03)}
.card-wide .wide-flag,.card-wide .wide-star{position:absolute;top:12px;font-family:var(--mono);font-size:8.5px;font-weight:500;letter-spacing:.15em;text-transform:uppercase;padding:5px 10px}
.card-wide .wide-flag{left:12px;background:var(--flag);color:var(--paper)}
.card-wide .wide-star{left:118px;background:var(--paper);color:var(--ink)}
.card-wide .wide-body{display:grid;grid-template-columns:1.25fr 1fr;column-gap:26px;padding:20px 22px 18px;align-items:start}
.card-wide .wide-kick{font-family:var(--mono);font-size:9px;letter-spacing:.18em;text-transform:uppercase;opacity:.7;margin-bottom:8px}
.card-wide .wide-title{font-family:var(--serif);font-style:italic;font-weight:400;font-size:25px;line-height:1.1;letter-spacing:-.01em;margin-bottom:8px}
.card-wide .wide-title a{color:inherit;border:0;text-decoration:none}
.card-wide .wide-dek{font-family:var(--serif);font-size:13.5px;line-height:1.55;opacity:.85;margin:0 0 12px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card-wide .wide-cta{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--paper);border:0.5px solid var(--paper);padding:8px 13px;text-decoration:none}
.card-wide .wide-cta:hover{background:var(--paper);color:var(--ink)}
.card-wide .wide-more{padding-left:22px;border-left:0.5px solid rgba(255,255,255,.25);height:100%}
.card-wide .wide-more-l{font-family:var(--mono);font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.6;margin:2px 0 12px}
.card-wide .wide-mini{display:flex;gap:12px;align-items:center;color:var(--paper);text-decoration:none;border:0;margin-bottom:10px}
.card-wide .wide-mini img{width:58px;height:58px;object-fit:cover;flex:0 0 58px}
.card-wide .wide-mini span{font-family:var(--serif);font-style:italic;font-size:14px;line-height:1.25}
.card-wide .wide-mini:hover span{text-decoration:underline}
@media(max-width:760px){
.card-wide .wide-in{height:auto;grid-template-rows:auto auto}
.card-wide .wide-media img{height:auto;aspect-ratio:16/10}
.card-wide .wide-body{display:block;padding:14px}
.card-wide .wide-kick{font-size:8.5px}
.card-wide .wide-title{font-size:21px}
.card-wide .wide-dek{font-size:13px;line-height:1.5}
.card-wide .wide-cta{padding:7px 12px;font-size:9.5px;margin-bottom:14px}
.card-wide .wide-more{padding:0;border-left:0;border-top:0.5px solid rgba(255,255,255,.25);height:auto}
.card-wide .wide-more-l{margin:12px 0 8px}
.card-wide .wide-more-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.card-wide .wide-mini{margin-bottom:0;gap:8px;align-items:flex-start}
.card-wide .wide-mini img{width:44px;height:44px;flex:0 0 44px}
.card-wide .wide-mini span{font-size:12px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
}
</style>
"""

OLD_LOOP = """    visibleCards.forEach((card, index) => {
      const col = index % cols;
      const x = col * (colWidth + gap);
      const y = colHeights[col];
      card.style.position = 'absolute';
      card.style.left = x + 'px';
      card.style.top = y + 'px';
      card.style.width = colWidth + 'px';
      colHeights[col] += card.offsetHeight + gap;
    });"""
NEW_LOOP = """    /*TGI-SPECIAL-WIDE-JS*/
    const refCard = visibleCards.find(c => !c.classList.contains('card-wide'));
    visibleCards.forEach((card, index) => {
      card.style.position = 'absolute';
      if (card.classList.contains('card-wide')) {
        if (cols >= 2) {
          let best = 0, bestY = Infinity;
          for (let c = 0; c < cols - 1; c++) { const yy = Math.max(colHeights[c], colHeights[c + 1]); if (yy < bestY - 1) { bestY = yy; best = c; } }
          card.style.setProperty('--wide-h', refCard ? refCard.offsetHeight + 'px' : 'auto');
          card.style.left = (best * (colWidth + gap)) + 'px';
          card.style.top = bestY + 'px';
          card.style.width = (colWidth * 2 + gap) + 'px';
          colHeights[best] = colHeights[best + 1] = bestY + card.offsetHeight + gap;
          return;
        }
        card.style.setProperty('--wide-h', 'auto');
      }
      let col = 0;
      for (let c = 1; c < cols; c++) if (colHeights[c] < colHeights[col] - 1) col = c;
      card.style.left = (col * (colWidth + gap)) + 'px';
      card.style.top = colHeights[col] + 'px';
      card.style.width = colWidth + 'px';
      colHeights[col] += card.offsetHeight + gap;
    });"""
OLD_FIRST = "const firstCard = visibleCards[0];"
NEW_FIRST = "const firstCard = visibleCards.find(c => !c.classList.contains('card-wide')) || visibleCards[0];"


def card_html(d):
    L = d["lead"]
    e = lambda s: s  # values in the JSON are already HTML-safe (entities allowed)
    minis = "\n".join(
        f'        <a class="wide-mini" href="{m["url"]}"><img src="{m["img"]}" alt="" loading="lazy" width="58" height="58"><span>{e(m["title"])}</span></a>'
        for m in d.get("more", []))
    return f"""<!-- TGI-SPECIAL-WIDE -->
<div class="card card-wide" data-type="field">
  <div class="wide-in">
    <a class="wide-media" href="{L['url']}">
      <img src="{L['img']}" alt="{html.escape(html.unescape(L['alt']))}" loading="lazy" width="1600" height="900" />
      <span class="wide-flag">[Field Notes]</span><span class="wide-star">Special</span>
    </a>
    <div class="wide-body">
      <div class="wide-main">
        <div class="wide-kick">{L['kicker']}</div>
        <div class="wide-title"><a href="{L['url']}">{e(L['title'])}</a></div>
        <p class="wide-dek">{e(L['dek'])}</p>
        <a class="wide-cta" href="{L['url']}">Read the story &rarr;</a>
      </div>
      <div class="wide-more">
        <div class="wide-more-l">More Special Field Notes</div>
        <div class="wide-more-row">
{minis}
        </div>
      </div>
    </div>
  </div>
</div>
<!-- /TGI-SPECIAL-WIDE -->
"""


def strip(s):
    return CSS_RE.sub("", CARD_RE.sub("\n", s))


def main(apply_):
    d = json.loads(DATA.read_text())
    s0 = HOME.read_text(encoding="utf-8")
    s = strip(s0)
    s = s.replace("</head>", CSS + "</head>", 1)
    # JS patch (once)
    if "/*TGI-SPECIAL-WIDE-JS*/" not in s:
        if OLD_LOOP not in s:
            sys.exit("! masonry loop not found — not patched")
        s = s.replace(OLD_LOOP, NEW_LOOP, 1)
    if OLD_FIRST in s:
        s = s.replace(OLD_FIRST, NEW_FIRST, 1)
    # card after Nth top-level card in the feed
    m = FEED_OPEN.search(s)
    n = int(d.get("after_card", 3))
    pos = m.end()
    for _ in range(n + 1):
        nm = TOP_CARD.search(s, pos + 1)
        if not nm:
            sys.exit("! not enough feed cards")
        pos = nm.start()
    # step back over any marker comment that belongs to the card at pos
    pre = s.rfind("\n", 0, pos)
    while True:
        line_start = s.rfind("\n", 0, pre) + 1
        line = s[line_start:pre].strip()
        if line.startswith("<!--") and line.endswith("-->") and not line.startswith("<!-- /"):
            pos, pre = line_start, line_start - 1
        else:
            break
    s = s[:pos] + card_html(d) + s[pos:]
    print(f"  special box after card {n}: {d['lead']['title']} (+{len(d.get('more', []))} more)")
    if not apply_:
        print("  dry run — pass --apply"); return
    HOME.write_text(s, encoding="utf-8")
    print("  wrote index.html")


if __name__ == "__main__":
    main("--apply" in sys.argv)
