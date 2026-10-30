import base64,io,html,os
from PIL import Image
rows=[l.rstrip('\n').split('|') for l in open('cat.txt')]
def th(p):
    im=Image.open(p).convert('RGB');im.thumbnail((360,450));b=io.BytesIO();im.save(b,'JPEG',quality=78);return base64.b64encode(b.getvalue()).decode()
def grp(r):
    h=r[1]
    if any(k in h for k in ['cap','hat','visor']): return 'Caps, Visors + Bucket'
    if any(k in h for k in ['short','trouser']): return 'Shorts + Trousers'
    if any(k in h for k in ['jacket','vest','hoodie','crewneck']): return 'Layers'
    return 'Polos + Tees'
order=['Polos + Tees','Layers','Shorts + Trousers','Caps, Visors + Bucket']
out=['<meta charset="utf-8"><style>body{background:#efe9dc;font-family:Georgia,serif;color:#1f2a1d;padding:28px;margin:0}h1{margin:0 0 4px}p.s{font-style:italic;margin:0 0 20px}h3{font:600 12px system-ui;letter-spacing:.14em;text-transform:uppercase;color:#2D4A2B;margin:22px 0 8px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.c{background:#f8f4ea;border-radius:6px;overflow:hidden;font:12px/1.35 system-ui}.im{display:flex}.im img{width:50%;aspect-ratio:4/5;object-fit:cover;background:#f3eee2}.im img:only-child{width:100%}.c div.t{padding:6px 8px}.n{font-weight:700;color:#2D4A2B}.x{color:#8a5a2b}</style>',
'<h1>Angus &amp; Grace Go Golfing — men\'s options</h1><p class="s">Everything in stock in the men\'s collection, plus caps from the wider shop (marked “caps page”). Prices A$ with ~US$ at x0.70. Number your keeps.</p>']
n=0
for g in order:
    out.append(f'<h3>{g}</h3><div class="g">')
    for i,r in enumerate(rows):
        if grp(r)!=g: continue
        n+=1
        ims=''.join(f'<img src="data:image/jpeg;base64,{th(f"opt/{i:02d}-{k}.img")}">' for k in (0,1) if os.path.exists(f'opt/{i:02d}-{k}.img'))
        a=float(r[3]);x=' <span class="x">caps page</span>' if r[0]=='x' else ''
        out.append(f'<div class="c"><div class="im">{ims}</div><div class="t"><span class="n">{n}</span> · {html.escape(r[2])}{x}<br>A${a:.0f} (~${round(a*.7)})</div></div>')
    out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/angus-grace-options.html','w').write('\n'.join(out));print(n)
