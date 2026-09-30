import json,html
d={p['handle']:p for p in json.load(open('products.json'))['products']}
picks=[
("Rainwear","hydrocore-rain-jacket-green",True,"The most technical piece they've made: 3-layer shell, 20,000mm waterproof, taped seams, YKK AquaGuard zips, PFAS-free DWR. New 23 Sep."),
("Rainwear","hydrocore-rain-trousers-green",True,"Matching trousers, placketed zips at the hem."),
("Outerwear","storm-wind-shirt-dark-blue",True,"Wind shirt for fall rounds."),
("Outerwear","black-tx-links-windbreaker",False,"Windbreaker."),
("Outerwear","black-padded-core-tech-jacket",False,"Padded winter jacket."),
("Outerwear","arcweave-gilet-ashwood",True,"ArcWeave texture, the fabric story of Fall '26."),
("Knit Capsule","flow-light-knit-hoodie-pine",True,"Knit Capsule: 45% extrafine merino / 55% ThermoCool. The hero of the capsule."),
("Knit Capsule","flow-light-bomber-neck-camel",True,"Bomber-neck knit, same blend."),
("Knit Capsule","theo-knit-polo-sweater-grey-melange",True,"Striped knit polo sweater."),
("Knits","club-knit-polo-rust",True,"Knit polo in rust."),
("Knits","airlite-henley-sweater-navy",True,"Henley sweater."),
("Knits","tx-intarsia-knit-crewneck-rust",True,"Intarsia crewneck, the most patterned piece."),
("Knits","blades-palm-polo-sweatshirt",False,"Polo sweatshirt, palm print."),
("Shirts","clayton-core-shirt-green",True,"Overshirt."),
("Shirts","brooks-wayline-shirt-dark-green",True,"Long-sleeve shirt."),
("Shirts","flight-green-palm-shirt",True,"Printed polo, the summer signature."),
("Shirts","heath-bomber-shirt-green",False,"Bomber-collar shirt."),
("Bottoms","arcweave-trouser-olive",True,"ArcWeave trouser."),
("Bottoms","lightweight-tapered-trouser-stone-blue",True,"Core tapered trouser, six colours."),
("Bottoms","shaw-moss-green-tx-tech-shorts",False,"Tech short."),
("Accessories","green-cashmere-blend-course-beanie",True,"Cashmere-blend beanie."),
("Accessories","dark-green-tour-belt",True,"Tour belt."),
("Accessories","black-rope-course-snapback",True,"Rope snapback."),
("Accessories","camo-two-tone-scipt-snapback",False,"Camo script snapback."),
("Women's","ivy-knit-sweater-pine-green",False,"Women's knit."),
("Women's","storm-anorak-off-white",False,"Women's anorak."),
]
cards=[];n=0;rec=0
for cat,h,star,note in picks:
    p=d[h];n+=1;rec+=star
    av=any(v['available'] for v in p['variants']); img=p['images'][0]['src'] if p['images'] else ''
    sep='&' if '?' in img else '?'
    cards.append(f'<div class="c{" rec" if star else ""}">{"<span class=star>★</span>" if star else ""}<img src="{img}{sep}width=500" loading="lazy"><div class="id">M{n:02d} · {cat} · <span style="color:{"#2D4A2B" if av else "#b00"}">{"In stock" if av else "Sold out"}</span></div><div class="b">{html.escape(p["title"])}</div><div class="k">${float(p["variants"][0]["price"]):.0f} USD · {len(p["images"])} photos</div><div class="r">{html.escape(note)}</div><a href="https://macadegolf.com/products/{h}" target="_blank">product ↗</a></div>')
json.dump(picks,open('picks.json','w'))
css="body{font:14px/1.45 -apple-system,Helvetica,sans-serif;background:#f4f1ea;color:#1b1f1a;margin:0;padding:28px}h1{font:600 28px Georgia,serif;margin:0 0 8px}.key{background:#fff;border:1px solid #ddd;padding:12px 14px;max-width:980px;margin-bottom:18px}.key p{margin:6px 0}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}.c{background:#fff;border:1px solid #ddd;padding:10px;position:relative}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#eee}.c.rec{border:2px solid #2D4A2B}.id{font:600 10px ui-monospace,monospace;margin-top:6px}.b{font:600 16px Georgia,serif;margin:4px 0 2px}.k{color:#666}.r{font-size:13px;margin-top:4px}.star{position:absolute;top:14px;right:16px;color:#fff;background:#2D4A2B;padding:2px 6px;font-weight:700}a{color:#2D4A2B;font-size:12px;display:inline-block;margin-top:6px}"
key=f"""<div class="key"><p><b>Macade</b>: Stockholm, founded 2019 "to reimagine golf apparel for a new generation". Its global HQ is the <b>Macade Clubhouse</b> on Torsgatan in central Stockholm, with a simulator, a shop and every staffer's clubs on the wall ("Drinks are always one degree above freezing."). Macade says it has clothed over 150,000 golfers. Tour team: Ewen Ferguson (DP World Tour), Dylan Naidoo (2025 South African Open winner), Gabriella Then (LPGA), Harang Lee (LET) and long driver Cassandra Meyer. Stocked at TPC Scottsdale, Big Cedar Lodge, Te Arai Links and Pearl Valley. The US store ships from the US, in USD, with free shipping and returns.</p>
<p><b>Angle options:</b> (a) Scandinavian design for bad weather: Fall '26, the Knit Capsule and HydroCore rainwear all launched in the last six weeks, all built for cold and wet rounds. (b) The Clubhouse-as-HQ story.</p>
<p><b>★ with a green border</b> = my 18, weighted to the three new fall drops. {n} options; prices and stock read from the US store on 30 Sep 2026.</p>
<p style="background:#fff4d6;padding:4px 6px"><b>Correction needed:</b> older TGI posts describe Macade as Australian (technical brands roundup) or priced in pounds (hat edits). It's Swedish, and the US store sells in dollars. I'll fix those lines when I build this.</p>
<p>Founder: CB Insights names Erik Valentin Villadiego, but Macade's own site names no founder, so I'd leave the name out unless you want it.</p></div>"""
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/macade-options-2026-09-30.html','w').write(f'<!doctype html><meta charset=utf-8><title>Macade — options</title><style>{css}</style><h1>Brand to Know: Macade — {n} options, pick 18</h1>{key}<div class="g">{"".join(cards)}</div>')
print(n,rec)
