import json,urllib.request,base64,io,html,concurrent.futures as cf
from PIL import Image
o=json.load(open('opts.json'))
seen={};H=[]
for h in o['hats']:
    k=(h['brand'],h['title'].split(' - ')[0] if h['brand']!='Draw' else h['title'])
    seen[k]=seen.get(k,0)+1
    if seen[k]<= (2 if h['brand'] in('Howler Bros','Linksoul') else 1) or h['brand'] in ('Draw','Canto','Brain Dead','Hikerdelic','Frog Skateboards'): H.append(h)

def thumb(it):
    src=it['img']
    if 'shopify' in src: src=src.split('?')[0]+'?width=600'
    elif 'bigcartel' in src: src=src.split('?')[0]+'?auto=format&fit=max&w=600'
    try:
        b=urllib.request.urlopen(urllib.request.Request(src,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((420,420))
        bio=io.BytesIO(); im.save(bio,'JPEG',quality=78); return 'data:image/jpeg;base64,'+base64.b64encode(bio.getvalue()).decode()
    except Exception as e: return ''
def usd(it):
    if it['cur']=='GBP': return f"£{it['price']:.0f} (~${it['price']*1.34:.0f})"
    if it['cur']=='AUD': return f"A${it['price']:.0f} (~${it['price']*0.70:.0f})"
    if it['cur']=='SEK': return f"{it['price']:.0f} kr (~${it['price']*0.1086:.0f})"
    if it['cur']=='EUR': return f"€{it['price']:.0f} (~${it['price']*1.16:.0f})"
    return f"${it['price']:g}"
def cards(items,prefix):
    with cf.ThreadPoolExecutor(10) as ex: ims=list(ex.map(thumb,items))
    s=''
    for i,(it,im) in enumerate(zip(items,ims),1):
        s+=f'''<div class="c"><div class="n">{prefix}{i}</div><img src="{im}"><div class="b">{html.escape(it['brand'])}</div><div class="t">{html.escape(it['title'])}</div><div class="p">{usd(it)}{' · '+html.escape(it['note']) if it['note'] else ''}</div></div>'''
    return s

H2=o['hats2']; keep=H2[:10]; new=H2[10:]
page=f'''<!doctype html><meta charset="utf-8"><title>Hats round 2</title><style>
body{{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}}h1{{font-size:26px;margin:0 0 4px}}h2{{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}}.c{{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}}
.c img{{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}}.n{{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}}
.b{{font:600 11px monospace;letter-spacing:.08em;text-transform:uppercase;margin-top:6px}}.t{{font-size:13px;line-height:1.25;margin:3px 0}}.p{{font:12px monospace;color:#555}}
p.s{{font-size:14px;max-width:820px}}</style>
<h1>Hats — round 2</h1><p class="s">Golf Wang, Brain Dead caps and the filler (Frog, Poler, Pleasures, Crust, William Murray, Linksoul) are out. Draw and your Canto camo stay. New options are small golf labels with a real point of view plus a few heritage/outdoor makers. All in stock today; pick by A# or D#. Parmore ripstop (D6) is marked as yours.</p>
<h2>Staying in</h2><div class="g">{cards(keep,'K')}</div><h2>New options</h2><div class="g">{cards(new,'A')}</div><h2>Agronomy Workshop &amp; more design-forward labels</h2><div class="g">{cards(o['hats3'],'D')}</div>'''
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/hats-options-round2.html','w').write(page)
