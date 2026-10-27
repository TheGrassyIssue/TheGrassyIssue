"""Quiet luxury golf brands: 6 picks per brand from the live catalogues read 26 Oct 2026 (this folder).
Late Nine and Local Rule price in SEK (no USD market); converted at 0.1005 (SEK/USD mid, 27 Oct 2026, poundsterlinglive)."""
import json, re, html
SEK = 0.1005
PICKS = {
 'late-nine': ['Cable Knit Polo Dark Brown','Double Pleat Slacks Dark Navy','Knit Crepe Polo Ivory','Ribbed Knit Vest Sage','Instructors Jacket Navy','5-Pocket Cords Cream'],
 'alba-golf': ['Voar Ls Polo','Cheviot Mockneck','Nevis Tech Trouser','Glen Padded Vest','Crest Jacket','Shire Quarter Zip Jacket'],
 'whim-golf': ['White Embroidered Navy Merino Long Sleeve','Sky Embroidered Slate Merino Long Sleeve','Woven Merino Swing Jacket','Merino Short Sleeve Golf Shirt','Dark Navy Woven Merino Golf Hat','Spell-Out Knit Beanie in Natural'],
 'rookline': ['Ottoman Rib Cashmere Crew','Ottoman Rib Cashmere Hoodie','Signature Blend Polo','Brushed Twill Pivot Pant','Cashmere Watch Cap','Grid Fleece Windbreaker'],
 'sloat': ['MERINO POLO','ORGANIC VENTILE JACKET','ORGANIC COTTON FLEECE QUARTER ZIP','ORGANIC COTTON DAY PANT','ORGANIC VENTILE VEST','ORGANIC COTTON SIX PANEL HAT'],
 'quiet-golf': ['Montecito Cashmere Cable Knit Sweater','Mesa Cashmere Sweater','Vintage Supima Cotton Polo','San Marino Pant','Cardroom Corduroy Jacket','Monogram Cotton Dad Hat'],
 'local-rule': ['Knit Polo - Off-White','Pleated Trousers - Navy','Fleece Pullover - Beige','Long-Sleeve Performance Polo - Whi','Tech Vest - Black','Beanie - Offwhite'],
 'sounder': ['Fine Cut Knitted Polo - Deep Navy','Chunky Knit - Natural','Capri Collar Polo - Deep Navy','Clubhouse Five Pocket Cord - Khaki','Good Walk Chino - Navy Moleskin','Himalayas Fleece Jacket - Grey'],
 'casualist': ['Grazer Cardigan Vest','Pleated Golf Trousers','Weekend Pique Polo','Dress Code Mockneck Tee','Cart Path Ripstop Jacket','Legacy Wool 5 Panel Cap'],
}
def strip(h): return html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',h or ''))).strip()
out = {}
for slug, names in PICKS.items():
    if slug == 'late-nine':
        P=[]
        for p in json.load(open('late-nine-raw.json'))['products']:
            if not any(v['available'] for v in p['variants']): continue
            P.append(dict(handle=p['handle'],title=p['title'],price=p['variants'][0]['price'],currency='SEK',images=[i['src'].split('?')[0] for i in p['images']][:6],desc=strip(p['body_html'])[:400],url=f"https://late-nine.com/products/{p['handle']}"))
    else:
        d=json.load(open(slug+'.json')); P=d['products']
        for p in P: p.setdefault('currency', d.get('currency'))
    rows=[]
    for n in names:
        m=[p for p in P if p['title'].lower().startswith(n.lower())]
        if not m: print('!! no match', slug, n); continue
        p=m[0]
        cur=p.get('currency') or 'USD'; pr=float(p['price'])
        usd = pr*SEK if cur=='SEK' else pr
        rows.append(dict(t=p['title'], handle=p['handle'], price=pr, cur=cur, usd=round(usd), url=p.get('url') or p.get('product_url'), imgs=(p.get('images') or p.get('image_urls') or [])[:6], desc=(p.get('desc') or p.get('body_text') or p.get('description') or '')[:400]))
    out[slug]=rows
json.dump(out, open('picks.json','w'), indent=1, ensure_ascii=False)
for s,r in out.items():
    print('##',s); [print('  ',x['t'][:50],x['price'],x['cur'],'$',x['usd'],len(x['imgs']),'|',x['desc'][:150]) for x in r]
