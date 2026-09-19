import json, pathlib
d = json.load(open('research/bold-tees-candidates.json'))
C = d['candidates']
newrec  = [c for c in C if c['rec']==1 and c.get('new')]
oddrec  = [c for c in C if c.get('odd')]
oldrec  = [c for c in C if c['rec']==1 and not c.get('new') and not c.get('odd')]
alts    = [c for c in C if c['rec']==0]

def card(c, n=None, kind=''):
    if n:   badge = f'<div class="n">{n}</div>'
    else:   badge = '<div class="n alt">ALT</div>'
    flag = f'<div class="hq">{c["hq"]}</div>' if c.get('hq') else ''
    return f'''<div class="c {kind}">{badge}
      <div class="im"><img src="{c['img']}" loading="eager"></div>
      <div class="b"><div class="br">{c['brand']}{flag}</div>
      <div class="nm">{c['name']}</div>
      <div class="pr">{'R' if c['cur']=='ZAR' else '$'}{c['price']} {c['cur']}</div>
      <div class="st">{c['stock']}</div>
      <div class="sy">{c['story']}</div></div></div>'''

n = 0
def run(items, kind=''):
    global n
    out = []
    for c in items:
        n += 1
        out.append(card(c, n, kind))
    return ''.join(out)

html = f'''<!doctype html><meta charset="utf-8"><style>
*{{box-sizing:border-box}} body{{margin:0;background:#f6f5f1;font:14px/1.4 -apple-system,Helvetica,Arial,sans-serif;color:#1b1b18;padding:34px}}
h1{{font-size:30px;margin:0 0 4px;letter-spacing:-.5px}}
h2{{font-size:17px;margin:32px 0 12px;text-transform:uppercase;letter-spacing:1.6px;color:#3c6e47;border-bottom:2px solid #3c6e47;padding-bottom:6px}}
h2 span{{text-transform:none;letter-spacing:0;color:#777;font-weight:400;font-size:13px}}
.sub{{color:#666;margin:0 0 6px;font-size:14px}}
.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}
.c{{background:#fff;border:1px solid #ddd9d0;border-radius:6px;overflow:hidden;position:relative;display:flex;flex-direction:column}}
.c.new{{border-color:#b8843a;border-width:2px}}
.c.odd{{border-color:#2f5d8a;border-width:2px}}
.c.a{{background:#faf9f6;border-style:dashed}}
.n{{position:absolute;top:7px;left:7px;background:#3c6e47;color:#fff;width:24px;height:24px;border-radius:50%;font:700 12px/24px sans-serif;text-align:center;z-index:2}}
.c.new .n{{background:#b8843a}} .c.odd .n{{background:#2f5d8a}}
.n.alt{{width:auto;padding:0 8px;border-radius:11px;background:#8a8578;font-size:10px;line-height:22px;height:22px}}
.im{{height:205px;background:#fff;display:flex;align-items:center;justify-content:center;border-bottom:1px solid #eee}}
.im img{{max-width:100%;max-height:205px;object-fit:contain}}
.b{{padding:9px 10px 11px}}
.br{{font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:#3c6e47}}
.c.new .br{{color:#b8843a}} .c.odd .br{{color:#2f5d8a}}
.hq{{font-weight:400;text-transform:none;letter-spacing:0;color:#8a8578;font-size:11px}}
.nm{{font-size:13px;font-weight:600;margin:2px 0 4px;line-height:1.25}}
.pr{{font-size:15px;font-weight:700}}
.st{{font-size:11px;color:#8a6d3b;margin:3px 0 5px}}
.sy{{font-size:11px;color:#5c5a54;line-height:1.35}}
</style>
<h1>The Bold Tee Edit &mdash; expanded candidate grid</h1>
<p class="sub">46 verified tees across 44 brands. Every price read from the brand&rsquo;s own store, 19 September 2026. Nothing converted.</p>

<h2>New to the TGI universe &mdash; 8 brands <span>&nbsp;gold border</span></h2>
<div class="g">{run(newrec, 'new')}</div>

<h2>Odd Ritual &mdash; added per your call <span>&nbsp;ZAR, see note</span></h2>
<div class="g">{run(oddrec, 'odd')}</div>

<h2>The original 18 <span>&nbsp;already in our universe</span></h2>
<div class="g">{run(oldrec)}</div>

<h2>19 verified alternates &mdash; swap any of these in</h2>
<div class="g">{''.join(card(c) for c in alts)}</div>
'''
pathlib.Path('research/teegrid.html').write_text(html)
print('recommended cards numbered 1..%d' % n, '| alternates', len(alts))
