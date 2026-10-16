import json,io,base64,urllib.request,html as H,re
from PIL import Image
D=[p for p in json.load(open('products.json'))['products'] if p['published_at']>='2026-10-01']
BY={}
for p in D: BY.setdefault(p['title'],[]).append(p)
REC={"Raglan Sleeve Blouson","Oasis Parka","Cotton Twill Parka","Contrast Zip Windbreaker","Western Yolk Track Jacket","SS V-Neck Windbreaker",
 "Frankenstein Button Up Shirt","Goalie Jersey","MW Place Button Up Shirt","Piped Longsleeve Quarter Zip Polo","Contrast Stitch Mock Neck Sweatshirt",
 "Dual Face T-Shirt","Skidmark T-Shirt","Prescription T-Shirt","Pleated Western Track Pant","Creature Pant","Buster Short","Heavyweight Mini Metal Logo T-Shirt","iGolf Dad Hat","Bomber Dad Hat"}
G=[("Outerwear",["Raglan Sleeve Blouson","Oasis Parka","Cotton Twill Parka","Contrast Zip Windbreaker","Western Yolk Track Jacket","SS V-Neck Windbreaker","Trail Mix Reversible Vest"]),
("Shirts, Jerseys & Polos",["Frankenstein Button Up Shirt","MW Place Button Up Shirt","Longsleeve Button Up Shirt","Goalie Jersey","King of the Greens Jersey","Piped Longsleeve Quarter Zip Polo","Surf Top"]),
("Sweatshirts",["Contrast Stitch Mock Neck Sweatshirt","Mountaineer Crewneck Sweatshirt"]),
("T-Shirts",["Dual Face T-Shirt","Heavyweight Mini Metal Logo T-Shirt","Skidmark T-Shirt","Prescription T-Shirt","MW Place T-Shirt","Creature T-Shirt","Flies T-Shirt"]),
("Pants & Shorts",["Pleated Western Track Pant","Creature Pant","Trophy Pant","Buster Short","My Serious Short","Trophy Short"]),
("Hats & Accessories",["iGolf Dad Hat","Bomber Dad Hat","Carlsbad Dad Hat","Cadet Hat","MW Place Snapback Hat","Pro Tip Snapback Hat","Metal Logo Sunglasses Strap"])]
assert set(t for _,ts in G for t in ts)==set(BY),set(BY)^set(t for _,ts in G for t in ts)
def color(p):
    if p["handle"]=="surf-top-green": return "Green"
    m=re.search(r'Color:\s*([A-Za-z/ ]+?)\s+(?:\d|Shell|100|[0-9])',H.unescape(re.sub('<[^>]+>',' ',p['body_html'] or '')))
    return m.group(1).strip() if m else p['handle'].split('-')[-1].title()
def blurb(p):
    t=re.sub(r'\s+',' ',H.unescape(re.sub('<[^>]+>',' ',p['body_html'] or '')))
    t=re.split(r'Chest \(Pit|Size Length|Size Waist',t)[0]
    return t
def thumb(url):
    im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url+('&' if '?' in url else '?')+'width=500',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())).convert('RGB')
    im.thumbnail((400,500));b=io.BytesIO();im.save(b,'JPEG',quality=78);return base64.b64encode(b.getvalue()).decode()
out=[];n=0;opts=[]
for g,ts in G:
    cards=[]
    for t in ts:
        ps=sorted(BY[t],key=lambda p:-sum(v['available'] for v in p['variants']));p=ps[0];n+=1
        cols=[f"{color(q)} ({sum(v['available'] for v in q['variants'])}/{len(q['variants'])})" if len(q['variants'])>1 else color(q) for q in ps]
        low=all(sum(v['available'] for v in q['variants'])<=2 and len(q['variants'])>1 for q in ps)
        b=thumb(p['images'][0]['src']);pr=float(p['variants'][0]['price']);rec=t in REC
        opts.append(dict(n=n,group=g,title=t,handles=[q['handle'] for q in ps],price=pr,colors=cols,rec=rec,blurb=blurb(p)))
        note=blurb(p)
        cards.append(f'<a class="c{" p" if rec else ""}" href="https://metalwood.studio/products/{p["handle"]}" target="_blank"><div class="im" style="background-image:url(data:image/jpeg;base64,{b})"></div><span class="n">#{n}</span>{"<span class=rec>REC</span>" if rec else ""}{"<span class=flag>low stock</span>" if low else ""}<div class="t">{H.escape(t)}</div><div class="m">${pr:.0f} &middot; {H.escape(", ".join(cols))}</div><div class="a">{H.escape(note[:230])}</div></a>')
    out.append(f'<h2>{g} <span class="cnt">{len(ts)}</span></h2><div class="grid">{"".join(cards)}</div>')
json.dump(opts,open('options.json','w'),indent=1)
css=open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/sunday-golf-btk-options.html').read().split('</style>')[0].split('<style>')[1]
story='''<div class="box"><strong>The collection:</strong> Metalwood&rsquo;s Fall/Winter 2026 dropped in two parts on October 11 and October 14, and the FW26 Pt 1 lookbook went up today (Oct 16): 31 photos shot in Los Angeles by Ryan Thomas Murray and Chase Thompson, starring Malcolm Amin and Erin Murray. ItIt&rsquo;s 39 styles (about 66 colorways)rsquo;s 36 styles in 65 colorways, $8 to $298. The mood is fall-workwear-meets-Y2K: western yokes on a track jacket, track pant and blouson; a faux-leather &ldquo;Oasis&rdquo; parka in black or ruby; patchwork &ldquo;Frankenstein&rdquo; button-up; a padded-sleeve Goalie Jersey (&ldquo;Golf is a contact sport&rdquo;); a reversible Dual Face tee; and the usual muni in-jokes (Skidmark tee about the men&rsquo;s room at Los Feliz Par-3, Prescription tee, iGolf hat). As always the product copy is half the fun and quotable (the clean lines anyway).<br><br><strong>Proposed format:</strong> a collection post, not a second Brand to Know (TGI already has Cole Young&rsquo;s BTK from June 15): &ldquo;Metalwood FW26: &hellip;&rdquo; with sections by category, lookbook bands between them, pull quotes from their product descriptions, a short &ldquo;what&rsquo;s new since June&rdquo; intro linking the BTK and the adidas/G.H. Bass collabs, and FAQ. It would lead the homepage and attach to the Metalwood brand page.<br><br><strong>Flags:</strong> no press coverage of FW26 yet (it&rsquo;s days old), so the story is the brand&rsquo;s own lookbook + copy. Low stock already on the Trophy pant/shorts, King of the Greens jersey and Trail Mix vest (in the Oct 11 drop). &ldquo;Pt 1&rdquo; implies a part 2 is coming. Left out: the G.H. Bass Sportocasin (August, covered separately).</div>'''
html=f'<!doctype html><meta charset="utf-8"><title>Metalwood FW26 &mdash; options</title><style>{css}</style><h1>Metalwood Studio FW26 &mdash; options</h1><div class="sub">{n} styles from metalwood.studio, released October 11 + 14, 2026 (USD, stock checked October 16; colorways listed with sizes in stock). REC = my suggested core. Pick by number.</div>{story}{"".join(out)}'
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/metalwood-fw26-options.html','w').write(html)
print(n,sum(o['rec'] for o in opts))
