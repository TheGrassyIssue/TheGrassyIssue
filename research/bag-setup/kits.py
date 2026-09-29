import json,io,base64,html,re,os
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from PIL import Image
from playwright.sync_api import sync_playwright
C=json.load(open('research/bag-setup/catalog.json'))['stores']
idx0={(d,x['handle']):x for d,v in C.items() if not d.startswith('_') for x in v}
class PI(dict):
    def get(self,k,default=None):
        if k in idx0: return idx0[k]
        for (d,h),x in idx0.items():
            if d==k[0] and h.startswith(k[1]): return x
        return default
    def __contains__(self,k): return self.get(k) is not None
idx=PI()
# kit: (name, palette hexes, idea, [(role, dom, handle, star)])
K=[
('Clubhouse Green',['#1f3b2c','#f1ead8','#b08d57'],'Forest green, cream and brass. The oldest colours in golf, and the easiest to get right.',[
 ('Bag','hirokigolf.com','hiroki-fte-sunday-golf-bag-green',1),('Bag alt','jonessportsco.com','michigan-st-rover-stand-dark-green',0),
 ('Driver','apresgolf.com','og-cream-dream-sherpa-fleece-headcover-w-green-tri',1),('Driver alt','sundaygolf.com','driver-headcover-midnight-green',0),
 ('Putter','dormieworkshop.com','dormie-chevron-green-room-xl-blade-putter-cover-co',1),
 ('Towel','dormieworkshop.com','dormie-signature-players-towel-green',1),
 ('Brush','dimpledivot.com','hickory-golf-brush-pro-hybrid-green',1)]),
('Tweed & Tan',['#5a4a3a','#8b5a2b','#2e3b2f'],'Harris Tweed, saddle leather and a wool towel. A bag that looks better with age.',[
 ('Bag','seamusgolf.com','macleod-tartan-sunday-bag',1),('Bag alt','seamusgolf.com','navy-harris-tweed-sunday-bag-copy',0),
 ('Driver','bluetross.com','the-old-tom-castagna-brown-leather-driver-hea',1),
 ('Putter','seamusgolf.com','macleod-tweed-blade-putter-cover',1),
 ('Irons','seamusgolf.com','british-tan-aniline-leather-iron-cover',1),
 ('Towel','seamusgolf.com','pendleton-canyonlands-golf-towel',1),
 ('Brush','dimpledivot.com','hickory-golf-brush-highland',1)]),
('Navy, With a Pop',['#1d2a44','#e9e4d8','#f08aa8'],'All navy, and one flash of colour: here pink, or sunshine yellow if you prefer.',[
 ('Bag','hirokigolf.com','hiroki-fte-sunday-golf-bag-navy',1),('Bag alt','hirokigolf.com','hiroki-luxury-leather-sunday-bag-navy',0),('Bag alt 2','jonessportsco.com','rover-stand-bag-navy',0),
 ('Pop driver','apresgolf.com','pink-sherpa-fleece-headcover-w-navy-trim',1),('Pop alt','apresgolf.com','yellow-jasmine-sherpa-fleece-headcover',0),
 ('Towel','dormieworkshop.com','paisley-towel-navy',1),
 ('Brush','dimpledivot.com','hickory-golf-brush-pro-hybrid-blue',1)]),
('Stone & Bone',['#e8e1d3','#c9bfae','#7a6a58'],'Tonal cream, stone and one soft brown. Quiet, and it never clashes with what you wear.',[
 ('Bag','jonessportsco.com','rover-stand-bag-bone',1),('Bag alt','hirokigolf.com','hiroki-fte-sunday-golf-bag',0),
 ('Driver','apresgolf.com','big-retro-logo-cream-sherpa-fleece-headcover',1),('Driver alt','apresgolf.com','sandy-mosaic-sherpa-fleece-headcover',0),
 ('Putter','dormieworkshop.com','white-french-seam-xl-blade-cover',1),
 ('Towel','malbon.com','ironworks-caddy-towel-ivory',1),
 ('Pouch','jonessportsco.com','rangefinder-pouch-ecru-kodiak',1)]),
('Black & White',['#111111','#f5f5f2','#8a8a86'],'Graphic and hard to mess up: one pattern, everything else plain.',[
 ('Bag','malbon.com','members-walking-bag-black',1),('Bag alt','jonessportsco.com','missouri-rider-bag-black-white',0),('Bag alt 2','hirokigolf.com','hiroki-stand-bag-anvers',0),
 ('Driver','ghostgolf.com','checkered-headcover-black',1),
 ('Putter','dormieworkshop.com','black-white-mallet-cover',1),
 ('Towel','hirokigolf.com','hiroki-golf-towel-black',1),
 ('Brush','dimpledivot.com','hickory-golf-brush-pro-hybrid-black',1)]),
('One Loud Note',['#9a9a94','#e6e3dc','#f26b1d'],'A quiet bag and one piece that shouts. The rule: only one.',[
 ('Bag','hirokigolf.com','hiroki-fte-sunday-golf-bag',1),
 ('Loud driver','hirokigolf.com','hiroki-nylon-headcover-orange',1),('Loud alt','birdsofcondor.com','lawn-pawn-driver-cover',0),('Loud alt 2','radmorgolf.com','pop-art-leather-mallet-putter-headcover-multi',0),
 ('Towel','hirokigolf.com','hiroki-golf-towel-grey',1),
 ('Brush','dimpledivot.com','hickory-golf-brush-gravel',1)]),
]
missing=[(d,h) for _,_,_,items in K for _,d,h,_ in items if (d,h) not in idx]
print('missing',missing)
json.dump([{'name':n,'pal':p,'idea':i,'items':[{'role':r,'dom':d,'handle':h,'star':s} for r,d,h,s in it]} for n,p,i,it in K],open('research/bag-setup/kits.json','w'),indent=1)
def b64(u,ctx):
    try:
        im=Image.open(io.BytesIO(ctx.request.get(u.split('?')[0]+'?width=500',timeout=30000).body())).convert('RGB');im.thumbnail((300,375));b=io.BytesIO();im.save(b,'JPEG',quality=75);return base64.b64encode(b.getvalue()).decode()
    except Exception as e: return ''
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context()
    for n,(name,pal,idea,items) in enumerate(K,1):
        cards=[]
        for role,d,h,s in items:
            x=idx.get((d,h))
            if not x: continue
            im=b64(x['imgs'][0],ctx) if x['imgs'] else ''
            cards.append(f'<div class="c{" rec" if s else ""}">{"<span class=star>★</span>" if s else ""}<div class="role">{role}</div><a href="https://{d}/products/{h}" target="_blank"><img src="data:image/jpeg;base64,{im}"></a><div class="b">{html.escape(x["title"][:60])}</div><div class="p">{d.replace(".com","").replace("www.","")} · {x["price"]:.2f}</div></div>')
        sw=''.join(f'<span class="sw" style="background:{c}"></span>' for c in pal)
        rows.append(f'<section><h2>K{n} · {name} {sw}</h2><p class="idea">{html.escape(idea)}</p><div class="g">{"".join(cards)}</div></section>')
    b.close()
out=f'''<!doctype html><meta charset=utf-8><title>Bag setup — kits</title><style>body{{font:14px/1.45 -apple-system,Helvetica,sans-serif;background:#f4f1ea;color:#1b1f1a;margin:0;padding:28px}}h1{{font:600 28px Georgia,serif;margin:0 0 8px}}h2{{font:600 21px Georgia,serif;margin:30px 0 4px;border-top:3px solid #2D4A2B;padding-top:10px;display:flex;align-items:center;gap:8px}}.sw{{display:inline-block;width:26px;height:26px;border:1px solid #0002}}.idea{{margin:0 0 10px;color:#444}}.key{{background:#fff;border:1px solid #ddd;padding:12px 14px;max-width:1000px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}}.c{{background:#fff;border:1px solid #ddd;padding:8px;position:relative}}.c.rec{{border:2px solid #2D4A2B}}.c img{{width:100%;aspect-ratio:4/5;object-fit:contain;background:#fafafa}}.role{{font:600 10px ui-monospace,monospace;text-transform:uppercase;color:#2D4A2B;margin-bottom:4px}}.b{{font-weight:600;font-size:13px;margin-top:4px}}.p{{font:11px ui-monospace,monospace;color:#555}}.star{{position:absolute;top:6px;right:8px;color:#2D4A2B;font-weight:700}}</style>
<h1>Curating the bag: six palette kits</h1>
<div class="key">Each kit is built around a three-colour palette and mixes makers. <b>★</b> = my pick for that slot; unstarred = alternates. Prices are in each store’s own currency, read 28 September 2026 (in-stock only); I’ll re-read every price on the day we build. In the post, each kit opens with inspiration photos (the makers’ own on-course and lifestyle shots in that palette), then the individual pieces for sale. A short guide opens the post: the 60-30-10 idea, one pattern per bag, matching metals and leathers, texture over colour.</div>
{"".join(rows)}'''
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/bag-setup-kits-2026-09-28.html','w').write(out)
print('ok',len(out)//1024)
