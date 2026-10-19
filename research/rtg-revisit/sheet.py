import json,io,base64,urllib.request,html,concurrent.futures as cf
from PIL import Image
ps={p['handle']:p for p in json.load(open('products.json'))['products']}
G=[("The Swish Collection (new, Sep 27)",["the-swisher-zip","founders-cap-swish","fairway-performance-cap-home","fairway-performance-cap-away","the-swish-collection-bundle-1"]),
("Back '90s Windbreaker (new, Sep 12)",["back-90s-windbreaker-tux","back-90s-windbreaker-cash","back-90s-windbreaker-black-purple","back-90s-windbreaker-patriot","back-90s-windbreaker-regal","back-90s-windbreaker-jazz","back-90s-windbreaker-mallard"]),
("Fairway 1/4 Zip (new, Aug 21)",["fairway-pullover-white","fairway-windbreaker-black","fairway-windbreaker-grey-copy","fairway-windbreaker-forest","fairway-windbreaker-atlantic"]),
("New hats (Jun–Oct)",["fairway-performance-cap-black-white","fairway-performance-cap-sky","fairway-performance-cap-navy-white","fairway-performance-cap-green-white","club-cap-orange","club-cap-intrepid","founders-cap-knicks","founders-cap-ny","founders-cap-stars-stripes"]),
("Returning staples for fall (already in the first post)",["the-grounds-crew-jacket-green","the-97-vintage-pullover-navy","the-knit-sweater","the-grey-crewneck","the-green-crewneck"])]
def th(h):
    p=ps[h]; u=p['images'][0]['src'].split('?')[0]+'?width=500'
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB'); im.thumbnail((360,360))
        o=io.BytesIO(); im.save(o,'JPEG',quality=78); return h,'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
    except Exception as e: return h,''
hs=[h for _,l in G for h in l]
with cf.ThreadPoolExecutor(8) as ex: T=dict(ex.map(th,hs))
css="body{font-family:Georgia,serif;background:#F3EFE6;color:#1d2a1c;margin:24px}h1{font-size:26px}h2{margin:28px 0 10px;border-bottom:2px solid #2D4A2B;padding-bottom:4px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}.c{background:#fff;border:1px solid #d9d3c4;padding:8px;position:relative}.c img{width:100%;aspect-ratio:1;object-fit:contain;background:#E8E2D6}.n{position:absolute;top:6px;left:6px;background:#2D4A2B;color:#fff;font:600 12px monospace;padding:2px 6px}.t{font-size:13px;margin:6px 0 3px;line-height:1.25}.p{font:12px monospace;color:#555}p.s{max-width:860px;font-size:14px;line-height:1.5}"
out=[f"<!doctype html><meta charset='utf-8'><title>Read The Green revisit — options</title><style>{css}</style><h1>Read The Green, Revisited — options</h1><p class='s'>Live catalogue checked Oct 19, 2026. 26 new products since our June 15 Brand to Know, all in stock. Headline: <b>The Swish Collection</b>, a capsule with Nick's signature, #33, '09 and a &ldquo;World Series Champion&rdquo; lining (Nick Swisher's Yankees number and title year, though the brand's copy only says &ldquo;Nick&rdquo;). Pick by number.</p>"]
n=0; num={}
for sec,l in G:
    out.append(f"<h2>{sec}</h2><div class='g'>")
    for h in l:
        n+=1; num[n]=h; p=ps[h]; av=sum(v['available'] for v in p['variants']); tot=len(p['variants'])
        st='' if av==tot else (' · SOLD OUT' if av==0 else f' · {av}/{tot} sizes')
        out.append(f"<div class='c'><div class='n'>{n}</div><a href='https://readthegreen.com/products/{h}' target='_blank'><img src='{T[h]}'></a><div class='t'>{html.escape(p['title'])}</div><div class='p'>${float(p['variants'][0]['price']):.0f}{st}</div></div>")
    out.append("</div>")
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/rtg-revisit-options.html','w').write(''.join(out))
json.dump(num,open('opts.json','w'),indent=1); print(n, sum(1 for v in T.values() if not v))
