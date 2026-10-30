import base64,io,html
from PIL import Image
C=[("Plum & Periwinkle","#490B24","#B5BEDD","plum","peri"),("Vermilion & Serenade","#FA4D01","#FFEDE3","verm","sere"),("Perfume & Gulf Blue","#E6ACF6","#050454","perf","gulf"),("Regent St Blue & Tory Blue","#A9CDE5","#1243B2","regent","tory"),("Corn & Eden","#E1C300","#0E6958","corn","eden"),("Seance & Cheese","#742092","#FFC973","seance","cheese")]
CN={'top':'Top','bottom':'Bottom','hat':'Hat','shoe':'Shoes','bag':'Bag','hc':'Headcover','towel':'Towel','grip':'Grip'}
rows=[l.rstrip('\n').split('|') for l in open('picks.txt')]
def thumb(i):
    im=Image.open(f'opt/{i:03d}.img').convert('RGB');im.thumbnail((360,450))
    b=io.BytesIO();im.save(b,'JPEG',quality=78);return base64.b64encode(b.getvalue()).decode()
out=['<meta charset="utf-8"><title>Color combos: outfits + bag setups — options</title><style>body{background:#efe9dc;font-family:Georgia,serif;color:#1f2a1d;margin:0;padding:28px}h1{font-size:28px;margin:0 0 4px}p.s{margin:0 0 24px;font-style:italic}section{margin:0 0 40px}h2{display:flex;align-items:center;gap:12px;font-size:22px;margin:0 0 8px}.sw{display:inline-block;width:34px;height:34px;border-radius:50%;border:1px solid #0002}h3{font:600 12px/1 system-ui;letter-spacing:.14em;text-transform:uppercase;margin:16px 0 8px;color:#2D4A2B}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}.c{background:#f8f4ea;border-radius:6px;overflow:hidden;font:12px/1.35 system-ui}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#f3eee2}.c div{padding:6px 8px}.n{font-weight:700;color:#2D4A2B}.b{border-left:6px solid}</style>',
 '<h1>Outfits + Bag Setups — six color combos</h1><p class="s">Number your keeps per combo. Every item is in stock now; prices USD unless noted. Swatch stripe on each card shows which half of the pair it covers.</p>']
n=0
for ci,(name,h1,h2,k1,k2) in enumerate(C):
    out.append(f'<section><h2><span class="sw" style="background:{h1}"></span><span class="sw" style="background:{h2}"></span>{ci+1}. {name} <small style="font:13px system-ui;color:#666">{h1} / {h2}</small></h2>')
    for grp,cats in (("The Outfit",['top','bottom','hat','shoe']),("The Bag Setup",['bag','hc','towel','grip'])):
        items=[(i,r) for i,r in enumerate(rows) if int(r[0])==ci and r[2] in cats]
        items.sort(key=lambda x:cats.index(x[1][2]))
        out.append(f'<h3>{grp}</h3><div class="g">')
        for i,r in items:
            n+=1;r[0]
            hx=h1 if r[1]==k1 else h2
            cur=' AUD' if r[3].endswith('.au') else ''
            brand=r[3].split('.')[0]
            out.append(f'<div class="c b" style="border-color:{hx}"><img src="data:image/jpeg;base64,{thumb(i)}"><div><span class="n">{ci+1}.{n}</span> · {CN[r[2]]}<br><b>{html.escape(brand)}</b><br>{html.escape(r[9][:48])}{" — "+html.escape(r[6]) if r[6] else ""}<br>${r[5]}{cur}</div></div>')
        out.append('</div>')
    out.append('</section>');n=0
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/color-outfits-options.html','w').write('\n'.join(out))
