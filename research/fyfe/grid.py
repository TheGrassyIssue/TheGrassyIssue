import json, os, html
cat={x['handle']:x for x in json.load(open('research/fyfe/catalog.json'))}
G=[("rothesay","rothesay","Rothesay Harris Tweed Headcover","Driver / fairway"),
("arran-harris-tweed-headcover","arran","Arran Harris Tweed Headcover","Oatmeal + rich green"),
("dunbar-harris-tweed-headcover","dunbar","Dunbar Harris Tweed Headcover","Duck egg blue"),
("black-grouse","black-grouse-hc","Black Grouse Harris Tweed Headcover","Houndstooth, red lining"),
("balmedie-harris-tweed-headcover-1","balmedie","Balmedie Harris Tweed Headcover","New — Aug 11, 2026"),
("galloway-driver-fairwaywood-headcovers","galloway-hc","Galloway Harris Tweed Headcover","Organic fleece lining"),
("douglas-grey","douglas-grey","Douglas Grey Headcover","Pure new wool tartan"),
("mackenzie","mackenzie-hc","MacKenzie Headcover","The collab tartan"),
("jura-sunset-harris-tweed-headcover-copy","jura-mini","Jura Sunset Mini Driver Cover","Mini driver"),
("fortrose-harris-tweed-headcover","fortrose-hc","Fortrose Harris Tweed Headcover","Driver / fairway"),
("huntsman","huntsman","Huntsman Harris Tweed Headcover","Estate check"),
("jura-sunset-harris-tweed-drawstring-pouch","jura-pouch","Jura Sunset Drawstring Pouch","Valuables pouch"),
("marine-suede-blade-cover-light-tan","marine-suede-tan","Marine Suede Blade Cover — Light Tan","Between Tides"),
("harbour-seersucker-blade-putter-cover","harbour-seersucker","Harbour Seersucker Blade Cover","Between Tides"),
("five-glens-blade-putter-slip-on-cover","five-glens-slipon","Five Glens Blade Slip-On Cover","Tweed + leather"),
("marksman-vintage-green","marksman-green","Marksman Rangefinder Case — Vintage Green","Waxed canvas"),
("the-brave-copper-hand-forged-ball-marker","brave-marker","The Brave Copper Ball Marker","Hand-forged copper"),
("western-birch-x-fyfe-premium-bamboo-golf-tees","western-birch-tees","Western Birch × Fyfe Bamboo Tees","Collab — bamboo")]
cards=[]
for i,(h,stem,title,note) in enumerate(G,1):
    p=cat[h]; img=f"/images/fyfe-btk/{stem}.jpg"
    assert os.path.exists(img.lstrip("/")), img
    cards.append(f'''<a class="c" href="{html.escape(p['url'])}" target="_blank">
 <div class="n">{i}</div><div class="im"><img src="{img}" loading="lazy"></div>
 <div class="t">{html.escape(title)}</div>
 <div class="m">{html.escape(note)} · <b>£{p['price_gbp_min']}</b></div></a>''')
open('research/fyfe/grid.html','w').write(f'''<!doctype html><meta charset="utf-8"><title>Fyfe 18</title>
<style>@font-face{{font-family:ENT;src:local("Georgia")}}
body{{margin:0;padding:40px;background:#f7f5ef;font:14px/1.45 -apple-system,Helvetica,Arial,sans-serif;color:#111}}
h1{{font:600 30px/1.1 Georgia,serif;margin:0 0 4px}}
.sub{{color:#5a5a52;margin:0 0 28px;font-size:13px;letter-spacing:.02em}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1160px}}
.c{{background:#fff;border:1px solid #e3e0d6;text-decoration:none;color:inherit;position:relative;display:block}}
.n{{position:absolute;top:0;left:0;background:#4a5d3a;color:#fff;font:600 12px/1 sans-serif;padding:7px 9px;z-index:2}}
.im{{aspect-ratio:1/1;background:#fff;overflow:hidden;display:flex;align-items:center;justify-content:center}}
.im img{{width:100%;height:100%;object-fit:cover}}
.t{{font:600 15px/1.3 Georgia,serif;padding:12px 13px 3px}}
.m{{padding:0 13px 13px;font-size:12px;color:#6a6a60;letter-spacing:.02em}}
.m b{{color:#111}}</style>
<h1>Fyfe Golf — 18 in-stock picks</h1>
<p class="sub">Pick 4–5 for the homepage carousel. All confirmed in stock today via the live catalog. Prices in GBP.</p>
<div class="g">{"".join(cards)}</div>''')
print("wrote research/fyfe/grid.html ·",len(G),"cards")
