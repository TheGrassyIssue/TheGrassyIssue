import json,re,os,base64
P={
'aberdeen-west':[('beige-satin-trucker-jacket',1),('black-satin-trucker-jacket',1),('sycamore-nylon-pullover-jacket',1),('black-nylon-pullover-jacket',0),('100-cashmere-checker-cardigan',1),('brown-striped-knit-long-sleeve-polo',1),('navy-striped-knit-long-sleeve-polo',0),('classic-plaid-pant',1),('classic-gingham-pant',0),('cordura-track-jacket-copy',0),('pine-aw-wing-tip',1),('oxblood-ghost',1),('harmony-white',0),('aw-golf-stand-bag',1),('navy-checker-crew-sock',0),('houdstooth-logo-bucket-hat',0)],
'we-hit-fairways':[('checkered-q-zip-mint-blue',1),('champions-cardigan-off-white',1),('champions-knit-sweater-ivory',1),('signature-knit-zip-sweater-oat',1),('tour-v-neck-polo-mustard',1),('waffle-knit-polo-clay-red',1),('medalist-knit-polo-sky-blue',1),('champions-performance-polo-fairway-green',0),('tour-striped-sweater-tour-white',0),('fairway-stripe-vest-shadow-black',0),('lightweight-core-pants-beige',0),('lion-cap-green',1),('the-fairway-tour-cap-green-checkered',0),('okeh-cap-unstructured-beige',0)],
'grind-city-golf':[('sphere-study-crew-knit',1),('the-unofficial-cardigan-copy',1),('v-neck-copy',1),('v-vest-1',1),('two-tone-fleeced-varsity-jacket-1',1),('pinstripe-protocol-polo',1),('unisex-plaid-full-zip-track-jacket',1),('men-s-barrel-leg-pants',1),('unisex-plaid-quarter-zip-sweatshirt',0),('the-sunday-stripe-shirt',0),('essential-heavyweight-vest',0),('low-fade-polo',0),('slow-play-sucks-jockey',0),('ladies-first-polo-shirt',0)]}
NAME={'aberdeen-west':'Aberdeen West','we-hit-fairways':'We Hit Fairways','grind-city-golf':'Grind City Golf'}
def th(s,h,i):
    f=f'thumbs/{s[:2]}_{re.sub(r"[^a-z0-9-]","",h)[:50]}_{i}.jpg'
    return 'data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode() if os.path.exists(f) else ''
out=[];opts=[];n=0
css='body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h2{margin:28px 0 6px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c.st{outline:3px solid #2D4A2B}.im{display:grid;grid-template-columns:1fr 1fr;gap:4px}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px;z-index:2}.t{font-size:13px;margin:6px 0 3px}.p{font:12px monospace;color:#555}p.s{max-width:860px;font-size:14px;line-height:1.5}'
out.append(f'<!doctype html><meta charset="utf-8"><title>On our radar Vol. 3 — options</title><style>{css}</style><h1>Three small brands on our radar, Vol. 3 — options</h1><p class="s">Live catalogues checked Oct 27, 2026. Prices are what a US shopper sees on each store (We Hit Fairways and Grind City set separate US prices; home-currency price in brackets). Outlined cards are my starred picks (8 or 9 per brand). Pick by number or say "stars".</p>')
for s,items in P.items():
    d={p['handle']:p for p in json.load(open(s+'.json'))['products']}
    out.append(f'<h2>{NAME[s]}</h2><div class="g">')
    for k,(h,star) in enumerate(items):
        p=d[h]; n+=1; code=f'{s[0].upper()}{k+1}'
        imgs=''.join(f'<img src="{th(s,h,i)}">' for i in (0,1) if th(s,h,i))
        hp='' if p['currency']=='USD' else f' ({p["currency"]} {float(p["price"]):.0f})'
        out.append(f'<div class="c{" st" if star else ""}"><div class="n">{code}{" ★" if star else ""}</div><div class="im">{imgs}</div><div class="t">{p["title"]}</div><div class="p">${float(p["usd_price"]):.0f}{hp} · {p["available_variant_count"]}/{p["total_variant_count"]} sizes</div></div>')
        opts.append(dict(code=code,brand=NAME[s],handle=h,title=p['title'],usd=p['usd_price'],home=p['price'],cur=p['currency'],star=bool(star),url=p['url']))
    out.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/radar-three-3-options.html','w').write(''.join(out))
json.dump(opts,open('options.json','w'),indent=1); print(n,sum(o['star'] for o in opts))
