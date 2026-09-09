#!/usr/bin/env python3
"""Homepage "cleaner and neater" pass (approved 2026-09-09). Idempotent; dry-run default.

What it does to index.html
  1. One sticky bar: weather banner hidden, its temp/desc + Tee times folded into
     the nav as .nav-wx (JS copies from #wb-temp/#wb-desc); filters go static.
  2. Lead card: the first feed card is duplicated as a full-width <section class="lead">
     above the filters; the source card gets class is-lead-source + inline display:none
     (inline, NOT a CSS class — layoutMasonry measures visibleCards[0].offsetWidth and
     a class-hidden card still counts as visible; that gave 68 columns once).
  3+4. Card diet: feed goes to 3 columns on desktop only (rules are scoped to
     min-width so the 820/480 breakpoints keep 2-up / 1-up), .gear-slide-info hidden,
     card text clamped to 2 lines.
  5. Newsletter: popup overlay hidden; olive .nl-band after the feed posts to the
     SAME Apps Script endpoint as the popup via a hidden iframe (submitNLBand).
  6. Hero: caption gone, tagline enlarged, one "Play Austin →" CTA (desktop only —
     mobile keeps the 30vh hero).
  7. Quote cards: paper background + green rule instead of black blocks.

Traps
  - Every new width/height rule MUST sit inside @media(min-width:821px) or it
    overrides the responsive block, which comes earlier in the file.
  - The lead card is a static duplicate; it does not filter with the chips. Fine.
"""
import re, sys, html as H

SRC = "index.html"
MARK = '<style id="cleaner">'

CSS = """
<style id="cleaner">
/* ---------- 1. one sticky bar ---------- */
.weather-banner{display:none}
.filters{position:static;border-bottom:0;padding:26px 0 6px}
.nav{border-bottom:0.5px solid rgba(20,20,20,.18)}
.nav-wx{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);opacity:.85;white-space:nowrap;margin-left:auto;margin-right:18px}
.nav-wx a{color:inherit;border-bottom:1px solid currentColor;padding-bottom:1px;margin-left:10px}
@media(max-width:1000px){.nav-wx{display:none}}
@media(max-width:820px){.filters{padding:16px 0 4px}}

/* ---------- 6. hero with one job (desktop) ---------- */
.hero-caption{display:none!important}
.hero-cta{display:inline-block;margin-top:22px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--paper);border-bottom:1px solid var(--paper);padding-bottom:3px}
@media(min-width:821px){
  .hero{height:54vh;max-height:600px;min-height:420px}
  .hero-sub{max-width:22ch!important;font-size:clamp(30px,3.6vw,52px)!important;line-height:1.05!important;letter-spacing:-.02em!important}
}
@media(max-width:820px){.hero-cta{display:none}}

/* ---------- 2. lead card ---------- */
.lead{max-width:1400px;margin:0 auto;padding:10px 32px 0;display:grid;grid-template-columns:1.25fr 1fr;gap:0;border:0.5px solid var(--ink);background:var(--paper)}
.lead .lead-img{aspect-ratio:4/3;overflow:hidden;background:var(--ink)}
.lead .lead-img img{width:100%;height:100%;object-fit:cover;display:block}
.lead .lead-body{padding:34px 36px 30px;display:flex;flex-direction:column;justify-content:center;gap:16px;border-left:0.5px solid var(--ink)}
.lead .card-tag{position:static;align-self:flex-start}
.lead .lead-title{font-family:var(--serif);font-weight:700;font-size:clamp(26px,2.6vw,38px);line-height:1.1;letter-spacing:-.01em}
.lead .lead-title a{color:inherit;text-decoration:none}
.lead .lead-text{font-size:15px;line-height:1.6;opacity:.78;max-width:46ch}
.lead .card-link{align-self:flex-start}
@media(max-width:900px){.lead{grid-template-columns:1fr}.lead .lead-body{border-left:0;border-top:0.5px solid var(--ink);padding:22px 20px 22px}}
@media(max-width:820px){.lead{margin:0 20px;padding:0}}
.card.is-lead-source{display:none!important}

/* ---------- 3 + 4. card diet, three columns (desktop only) ---------- */
@media(min-width:821px){
  .feed .card{width:calc(33.333% - 14px)}
  .card-title{font-size:17px}
  .card-body{padding:16px 16px 14px}
}
.gear-slide-info{display:none}
.card-text{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:12px}

/* ---------- 7. quote cards, lighter ---------- */
.card-quote{background:var(--paper);color:var(--ink);border-left:3px solid var(--grass)}
.card-quote blockquote{font-family:var(--serif);font-style:italic;font-weight:400;font-size:19px;line-height:1.3;color:var(--ink)}
.card-quote .card-tag{background:transparent;border:0.5px solid var(--grass);color:var(--grass)}
.card-quote cite{color:var(--ink);opacity:.7}
.card-quote .quote-portrait{background:var(--grass)!important;color:var(--paper)!important}

/* ---------- 5. newsletter: inline band, no popup ---------- */
#nl-overlay{display:none!important}
.nl-band{background:var(--grass);color:var(--paper);margin:56px 0 0;padding:72px 32px 76px}
.nl-band .in{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:end}
.nl-band .k{font-family:var(--mono);font-size:11px;letter-spacing:.24em;text-transform:uppercase;opacity:.75;margin-bottom:18px}
.nl-band h2{font-family:var(--serif);font-weight:700;font-size:clamp(34px,4.2vw,58px);line-height:1;letter-spacing:-.01em;margin:0 0 14px}
.nl-band p{font-size:16px;line-height:1.5;opacity:.8;max-width:34ch;margin:0}
.nl-band form{display:flex;border-bottom:1.5px solid rgba(244,241,234,.6);padding-bottom:12px;max-width:520px}
.nl-band input{flex:1;background:transparent;border:0;outline:0;color:var(--paper);font-family:inherit;font-size:18px;min-width:0}
.nl-band input::placeholder{color:rgba(244,241,234,.55)}
.nl-band button{background:transparent;border:0;color:var(--paper);font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;cursor:pointer;padding-left:18px}
.nl-band .thanks{display:none;font-family:var(--serif);font-style:italic;font-size:20px}
@media(max-width:900px){.nl-band .in{grid-template-columns:1fr;gap:28px}.nl-band{padding:52px 20px 56px;margin-top:32px}}
</style>
"""

BAND = """
<section class="nl-band" id="join">
  <div class="in">
    <div>
      <div class="k">The Newsletter</div>
      <h2>We&rsquo;ll keep looking.</h2>
      <p>Stories, brands and recommendations, in your inbox. One email a week.</p>
    </div>
    <div>
      <form id="nl-band-form" onsubmit="return submitNLBand(event)">
        <input id="nl-band-email" type="email" required placeholder="Your email" aria-label="Email">
        <button type="submit">Join &rarr;</button>
      </form>
      <div class="thanks" id="nl-band-thanks">You&rsquo;re in. First drop incoming.</div>
    </div>
  </div>
</section>
"""

JS = """
<script>
/* cleaner: weather -> nav, band -> same Apps Script endpoint as the popup */
(function(){function sync(){var t=document.getElementById('wb-temp'),s=document.getElementById('wb-desc'),n=document.getElementById('nav-wx');
 if(!n)return; var parts=[t&&t.textContent.trim(),s&&s.textContent.trim()].filter(Boolean);
 n.innerHTML=(parts.length?parts.join(' &middot; '):'Austin, TX')+'<a href="https://txaustinweb.myvscloud.com/webtrac/web/search.html?display=detail&module=GR" target="_blank" rel="noopener">Tee times</a>';}
 sync(); setTimeout(sync,1500); setTimeout(sync,4000);})();
function submitNLBand(e){
  e.preventDefault();
  var email=document.getElementById('nl-band-email').value;
  var f=document.createElement('form'); f.method='POST';
  f.action='__ENDPOINT__'; f.target='nl-hidden-frame';
  var inp=document.createElement('input'); inp.type='hidden'; inp.name='email'; inp.value=email; f.appendChild(inp);
  document.body.appendChild(f); f.submit(); document.body.removeChild(f);
  document.getElementById('nl-band-form').style.display='none';
  document.getElementById('nl-band-thanks').style.display='block';
  return false;
}
</script>
"""


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def main(apply_=False):
    doc = open(SRC, encoding="utf-8").read()
    if MARK in doc:
        print("already applied — nothing to do"); return
    orig = doc

    # endpoint from the existing popup (never hard-code it twice)
    m = re.search(r"f\.action = '(https://script\.google\.com/[^']+)'", doc)
    assert m, "popup endpoint not found"
    endpoint = m.group(1)

    # CSS before </head>
    assert doc.count("</head>") == 1
    doc = doc.replace("</head>", CSS + "</head>", 1)

    # nav-wx before .nav-toggle
    m = re.search(r'\s*<button[^>]*class="nav-toggle"', doc)
    assert m, "nav-toggle not found"
    doc = doc[:m.start()] + '\n    <span class="nav-wx" id="nav-wx"></span>' + doc[m.start():]

    # hero: drop caption, add CTA after h1.hero-sub
    m = re.search(r'\s*<div class="hero-caption">.*?</div>\s*', doc, re.S)
    assert m and len(m.group(0)) < 800, "hero-caption block not found or too big"
    doc = doc[:m.start()] + "\n" + doc[m.end():]
    m = re.search(r'<h1 class="hero-sub">.*?</h1>', doc, re.S)
    assert m, "h1.hero-sub not found"
    doc = doc[:m.end()] + '\n<a class="hero-cta" href="/field-guide/">Play Austin &rarr;</a>' + doc[m.end():]

    # lead card from the first feed card
    fi = doc.index('<section class="feed"') if '<section class="feed"' in doc else doc.index('class="feed"')
    m = re.search(r'<div class="card" data-type="(\w+)">', doc[fi:])
    assert m, "first card not found"
    cs = fi + m.start()
    card = doc[cs:cs + 20000]
    img = re.search(r'<img[^>]+src="([^"]+)"', card).group(1)
    tag = re.search(r'<span class="card-tag[^"]*">(.*?)</span>', card, re.S)
    ttl = re.search(r'<(?:h2|h3|div) class="card-title">\s*<a href="([^"]+)"[^>]*>(.*?)</a>', card, re.S)
    txt = re.search(r'<(?:p|div) class="card-text"[^>]*>(.*?)</(?:p|div)>', card, re.S)
    lnk = re.search(r'<a href="([^"]+)" class="card-link"[^>]*>(.*?)</a>', card, re.S)
    assert tag and ttl and txt and lnk, (bool(tag), bool(ttl), bool(txt), bool(lnk))
    lead = f'''
<section class="lead" id="lead">
  <div class="lead-img"><img src="{img}" alt=""></div>
  <div class="lead-body">
    <span class="card-tag grass">{strip_tags(tag.group(1))}</span>
    <div class="lead-title"><a href="{ttl.group(1)}">{ttl.group(2).strip()}</a></div>
    <div class="lead-text">{strip_tags(txt.group(1))}</div>
    <a href="{lnk.group(1)}" class="card-link">{lnk.group(2).strip()}</a>
  </div>
</section>
'''
    doc = (doc[:cs] + f'<div class="card is-lead-source" data-type="{m.group(1)}" style="display:none">'
           + doc[cs + len(m.group(0)):])
    fs = doc.index('<div class="filters-inner">')
    doc = doc[:fs] + lead + doc[fs:]

    # band after the feed section
    fe = doc.index("</section>", doc.index('class="feed"'))
    doc = doc[:fe + len("</section>")] + BAND + doc[fe + len("</section>"):]

    # JS before </body>
    assert doc.count("</body>") == 1
    doc = doc.replace("</body>", JS.replace("__ENDPOINT__", endpoint) + "</body>", 1)

    print(f"lead: {strip_tags(ttl.group(2))[:70]}")
    print(f"size {len(orig):,} -> {len(doc):,}")
    if apply_:
        open(SRC, "w", encoding="utf-8").write(doc)
        print("written")
    else:
        print("(dry run — pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
