import json,re,os,base64,urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
d=json.load(open('catalogue.json')); P={p['handle']:p for p in d['products']}
SKIP_IN={'hypegolf-exclusive-pare-putang-ina-t-shirt'}
SOLD=["pare-94-am-sensation-mockneck","pare-5-panel-camp-hat","pare-x-mogshade-driver-headcover","pare-x-mogshade-fairway-wood-headcover",
 "barnabys-x-pare-driver-headcover","little-sundays-x-pare-toddler-golf-bag","pare-x-paris-golf-gallery-snapback-hat","pare-ube-mockneck",
 "pare-faces-rope-hat","pare-kanin-snapback-hat","pare-azalea-mockneck","pare-hex-weave-mockneck-2-pack"]
def h_of(t): 
    for h,p in P.items():
        if p['title']==t: return h
ins=[h for h,p in P.items() if p['available'] and 'Putang' not in p['title'] and not p['title'].startswith('[FREE')]
sold=[]
for s in SOLD:
    if s in P: sold.append(s)
    else:
        m=[h for h in P if s.replace('pare-','') in h]; sold+=m[:1]
STAR={'pare-x-imperial-manila-hat-walnut','pare-x-imperial-manila-hat-white','pare-x-bluetross-driver-headcover','pare-x-bluetross-blade-putter-headcover',
 'pare-club-shirt','pare-cool-grey-short-sleeve-wind-shirt','pare-plisse-pants-2-0','pare-plisse-pants','pare-adobo-mockneck-shirt','pare-manila-mockneck-shirt',
 'pare-maganda-ang-buhay-mockneck-shirt','pare-gulay-hooded-pullover-sweatshirt','pare-tex-waterproof-5-panel-long-bill-hat','pare-for-good-long-sleeve-shirt','pare-blonde-eldrick-long-sleeve-shirt','pare-classic-new-york-logo-t-shirt'}
def th(h,i):
    imgs=P[h].get('images') or []
    if i>=len(imgs): return ''
    f=f'thumbs/{h[:60]}_{i}.jpg'
    if not os.path.exists(f):
        try:
            u=imgs[i]['src'] if isinstance(imgs[i],dict) else imgs[i]
            b=urllib.request.urlopen(urllib.request.Request(u+'?width=500',headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
            open(f+'.t','wb').write(b); im=Image.open(f+'.t').convert('RGB'); im.thumbnail((420,420)); im.save(f,quality=80); os.remove(f+'.t')
        except Exception as e: print('ERR',h,e); return ''
    return f
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda a: th(*a), [(h,i) for h in ins+sold for i in (0,1)]))
def uri(f): return 'data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode() if f and os.path.exists(f) else ''
css='body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h2{margin:28px 0 6px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c.st{outline:3px solid #2D4A2B}.im{display:grid;grid-template-columns:1fr 1fr;gap:4px}.c img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px;z-index:2}.t{font-size:13px;margin:6px 0 3px}.p{font:12px monospace;color:#555}p.s{max-width:880px;font-size:14px;line-height:1.5}'
o=[f'<!doctype html><meta charset="utf-8"><title>Pare Golf — options</title><style>{css}</style><h1>Brand to Know: Paré Golf — options</h1><p class="s">Live catalogue checked Oct 27, 2026 (USD). 26 of 112 products in stock; most of the range sells out. Section 1 is everything in stock (minus the HYPEGOLF tee with a Tagalog swear word in its name); section 2 is notable sold-out pieces the brand is known for. Outlined = my starred picks. "Kapamilya Only" pieces need a members login to buy. Pick by number or say "stars".</p>']
opts=[]
for title,lst,pre in (('In stock',ins,'P'),('Sold out — the signature pieces',sold,'S')):
    o.append(f'<h2>{title}</h2><div class="g">')
    for k,h in enumerate(lst):
        p=P[h]; code=f'{pre}{k+1}'; st=h in STAR
        imgs=''.join(f'<img src="{uri(th(h,i))}">' for i in (0,1) if th(h,i))
        o.append(f'<div class="c{" st" if st else ""}"><div class="n">{code}{" ★" if st else ""}</div><div class="im">{imgs}</div><div class="t">{p["title"]}</div><div class="p">${float(p["usd_price"] or p["price"]):.0f}{" · sold out" if not p["available"] else ""}</div></div>')
        opts.append(dict(code=code,handle=h,title=p['title'],usd=p['usd_price'] or p['price'],available=p['available'],star=st,url=p['url']))
    o.append('</div>')
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/pare-options.html','w').write(''.join(o))
json.dump(opts,open('options.json','w'),indent=1)
print(len(ins),len(sold),sum(x['star'] for x in opts),[h for h in STAR if h not in P])
