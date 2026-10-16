import json,io,base64,urllib.request,html as H,concurrent.futures as cf
from PIL import Image
I={it['urlId']:it for it in json.load(open('items.json'))}
G=[
("Headcovers: one of a kind, from old textiles",[
 ("west-coast-surf-tent-headcover","1970s California canvas camp tent, waxed, 55 years of patina",True,""),
 ("tree-frog-green-camp-tent-headcover","Green vintage camp tent",True,""),
 ("khaki-scout-tent-headcover","Khaki scout tent",False,""),
 ("burnt-orange-camp-tent-headcover","Burnt orange camp tent",False,""),
 ("camp-tent-headcover","The original Camp Tent cover",False,""),
 ("state-flower-headcover-20","Vintage hand-embroidered state flower patch on 16oz canvas; 2 left, on sale",True,""),
 ("state-bird-crest-headcover","State Flower Crest cover; 1 left, on sale",False,""),
 ("heirloom-quilt-putter-cover-2","Heirloom quilt putter cover, 1 of 1",True,""),
 ("nature-club-camo-headcover","Nature Club camo cover",False,""),
 ("nature-club-neoprene-wetsuit-headcover","Herringbone wetsuit neoprene, made in NYC",True,""),
]),
("Headcovers: the in-line range",[
 ("ny-wool-headcovers","100% American wool, knit in Oregon. Driver/fairway/hybrid, navy or black",True,"LENNY OWNS (navy driver)"),
 ("american-wool-headcover","American Wool, Fall (also Spring, Summer, Winter)",True,""),
 ("american-wool-headcover-p9yzx","American Wool, Summer",False,""),
 ("studio-collection-headcover","16oz canvas twill, handmade in the garment district; 6+ colors",True,""),
 ("studio-collection-putter-cover","Studio Collection putter cover",False,""),
 ("ggnc-x-malbon-birds-of-georgia-embroidered-driver-cover","GGNC x Malbon Birds of Georgia (Masters 2026), on sale",True,""),
]),
("Tees",[
 ("to-fight-a-mockingbird-tee","Mockingbird mimicry tee, 6.5oz American cotton",True,"LENNY OWNS"),
 ("state-flower-reference-tee","State Flower reference tee (the one Josh Allen wore)",True,""),
 ("nature-club-tee","Nature Club tee, reclaimed waste cotton, 5 colors",False,""),
 ("nature-club-shells-tee","Rare & Common Shells tee",False,""),
 ("anatomy-of-a-fly-reference-tee","Anatomy of a Fly reference tee",True,""),
 ("how-to-tie-a-fly-ls-tee","How To Tie a Fly L/S tee",False,""),
 ("nature-club-best-birdies-tee","Best Birdies tee",True,""),
 ("lose-your-ball-find-yourself-tee","Lose Your Ball, Find Yourself (mental health line)",True,""),
 ("negroni-club-tee","Negroni Club 1919 tee",False,""),
 ("club-di-golf-e-natura-gumtree-tee","Club di Golf e Natura Gumtree tee (Italy)",False,""),
 ("earth-day-everyday-20-tee-bundle","Earth Day Everyday 2.0",False,""),
 ("just-out-for-a-walk-premium-ls-tee","Just Out For A Walk L/S",False,""),
]),
("Clothing",[
 ("nature-club-deadstock-lace-shirt","Deadstock cotton lace shirt, made in Manhattan",True,""),
 ("nature-club-rockaway-stripe-shirt","Rockaway stripe L/S shirt",True,""),
 ("nature-club-the-end-ls-linen-shirt","The End linen shirt",False,""),
 ("studio-collection-ss-polo","Studio Collection S/S polo",True,""),
 ("studio-collection-ls-polo","Studio Collection L/S polo",False,""),
 ("made-in-manhattan-vest","Made in Manhattan vest, on sale",True,""),
 ("nature-club-vintage-wash-barrel-jeans","Barrel jeans, made in Portugal",False,""),
 ("nature-club-beachcomber-short","Beachcomber short, 4-way stretch ripstop",True,""),
 ("heirloom-quilt-vest-44lwp-9dsj8-3927a","Heirloom Quilt Vest 4.0, on sale, 1 left",True,""),
]),
("Hats",[
 ("texas-state-flower-5-panel","Texas bluebonnet 5-panel (Austin tie-in)",True,""),
 ("new-york-branches-unstructured-5-panel","NY Branches 5-panel (Nick Jonas wore the dad hat)",True,""),
 ("ny-branches-dad-hat","NY Branches dad hat",False,""),
 ("new-york-state-flower-5-panel","NY State Flower 5-panel",False,""),
 ("nature-club-unstructured-5-panel-1","Nature Club 5-panel",False,""),
 ("beachcomber-5-panel","Beachcomber 5-panel, art by Evan Ortolani",False,""),
 ("just-out-for-a-walk-hat-1","Just Out For A Walk hat",False,""),
 ("club-di-golf-e-natura-gumtree-dad-hat","Club di Golf e Natura dad hat",False,""),
]),
("Collabs",[
 ("ggnc-x-puma-field-notes-polo","GGNC x PUMA Field Notes polo (Rickie Fowler wore it), on sale",True,""),
 ("ggnc-x-puma-helsinki-g","GGNC x PUMA Helsinki G shoe, on sale",True,""),
 ("ggnc-x-puma-conservation-dept-fleece","GGNC x PUMA Conservation Dept. fleece, on sale",False,""),
 ("ggnc-x-puma-wildflowers-tee","GGNC x PUMA Wildflowers tee, on sale",False,""),
 ("ggnc-x-mackenzie-ny-bag-navy","GGNC x Mackenzie NY bag, handmade to order in Portland",True,""),
 ("ggnc-x-mackenzie-ny-shoe-bag","GGNC x Mackenzie NY shoe bag",False,""),
 ("ggnc-x-malbon-birds-of-georgia-nocs","GGNC x Malbon x Nocs binoculars, on sale",False,""),
 ("ggnc-x-almond-6-6-single-fin-surfboard","GGNC x Almond 6'6\" single fin surfboard ($1,850)",False,""),
 ("ggnc-x-samuel-falzone-leather-card-holder","GGNC x Samuel Falzone Italian leather card holder",False,""),
]),
("Around the bag",[
 ("member-caddy-towel","Member Caddy Towel",True,""),
 ("vintage-floral-quilt-valuables-pouch","Vintage floral quilt valuables pouch, 1 of 1",False,""),
 ("nature-club-socks","Nature Club socks",False,""),
 ("nature-club-surfwear-zip-tote","Nature Club Surfwear zip tote",False,""),
 ("studio-espresso-coffee","GUMTREE (COFFEE) Studio Espresso",False,""),
]),
]
def money(it):
    v=it['variants']; p=float(v[0]['priceMoney']['value']); s=None
    for x in v:
        if x.get('onSale'): s=float(x['salePriceMoney']['value']); break
    return p,s
def instock(it): return sum(1 for x in it['variants'] if x.get('unlimited') or (x.get('qtyInStock') or 0)>0)
def thumb(u):
    try:
        b=urllib.request.urlopen(urllib.request.Request(u+'?format=500w',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
        im=Image.open(io.BytesIO(b)).convert('RGB');im.thumbnail((400,500));o=io.BytesIO();im.save(o,'JPEG',quality=78);return base64.b64encode(o.getvalue()).decode(),Image.open(io.BytesIO(b)).size
    except Exception as e: return '',(0,0)
flat=[(g,u,n,r,l) for g,items in G for u,n,r,l in items]
for g,u,n,r,l in flat: assert u in I,u
urls=[(I[u].get('items') or [{'assetUrl':I[u]['assetUrl']}])[0]['assetUrl'] for g,u,n,r,l in flat]
with cf.ThreadPoolExecutor(10) as ex: TH=list(ex.map(thumb,urls))
out=[];opts=[];k=0;cur=None;cards=[]
def flush():
    if cur: out.append(f'<h2>{cur} <span class="cnt">{len(cards)}</span></h2><div class="grid">{"".join(cards)}</div>')
for (g,u,n,r,l),(b,sz) in zip(flat,TH):
    if g!=cur: flush(); cur=g; cards=[]
    k+=1; it=I[u]; p,s=money(it); st=instock(it)
    pr=f'${s:,.0f} <s>${p:,.0f}</s>' if s else f'${p:,.0f}'
    opts.append(dict(n=k,group=g,urlId=u,title=it['title'],price=p,sale=s,instock=st,variants=len(it['variants']),note=n,lenny=l,imgs=len(it.get('items',[]))))
    badge=(f'<span class="rec" style="background:#9a3b2a">{l}</span>' if l else '')+('<span class="rec">REC</span>' if r else '')
    cards.append(f'<a class="c{" p" if r else ""}" href="https://www.gumtreegolfandnature.com{it["fullUrl"]}" target="_blank"><div class="im" style="background-image:url(data:image/jpeg;base64,{b})"></div><span class="n">#{k}</span>{badge}<div class="t">{H.escape(it["title"])}</div><div class="m">{pr} &middot; {st}/{len(it["variants"])} in stock &middot; {len(it.get("items",[]))} photos</div><div class="a">{H.escape(n)}</div></a>')
flush()
json.dump(opts,open('options.json','w'),indent=1)
css=open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/sunday-golf-btk-options.html').read().split('</style>')[0].split('<style>')[1]
story='''<div class="box"><strong>The story:</strong> Karsten Jurkschat grew up surfing in Melbourne and started out as a photographer in the surf industry before becoming one of advertising's best-known creative directors (the Knicks, NBA, Apple Music; an industry trade magazine's Creative Director of the Year in 2020). He moved to New York in 2017, missed the ocean, burned out, and found golf during the pandemic: "getting up at 6 a.m. or 5 a.m. and going to one of the courses in the city and just walking around before everybody's up." His dad was a landscape gardener ("That's where I learned all my plant knowledge"); his German grandmother taught him to sew. He bought a $300 sewing machine and made every product himself for the first six months. Gumtree launched in Brooklyn in 2022; the studio is at 55 Nassau Avenue in Greenpoint. What makes it different: headcovers cut from 1940s–80s heirloom quilts, 1950s–80s camp tents, fly-fishing waders and coffee sacks, each one different, retired when the textile runs out; in-line wool knit in Oregon and canvas sewn in the garment district; 2% of sales to carbon removal; three-day Field Trips (Sonoran Desert, Zion, Catskills); collabs with PUMA (Rickie Fowler wore it), Malbon (Birds of Georgia at the Masters), Mackenzie, Almond Surfboards, Nocs. Best line: "It's not for everybody. And that's the point."<br><br><strong>Your angle:</strong> one of your personal favorites. I'd open the TGI Take in first person with the Mockingbird tee and the navy NY driver cover in your bag, if you're good with that.<br><br><strong>Proposed format:</strong> full treatment: hero, TGI Take, founder story, "In His Words — Karsten Jurkschat", a "What It's Made From" section (quilts, tents, waders, sacks, wool), Field Trips band, product sections (One-of-a-Kind Covers, In-Line Covers, Tees, Clothing, Hats, Collabs, Around the Bag), pull quotes, FAQ. Replaces the Nature Club drop post as the brand's profile page.<br><br><strong>Flags:</strong> founding year: the brand says 2022, one interview says he started it in 2020 in his spare time; I'd say "started during the pandemic, launched 2022." One-of-a-kind covers sell out fast, so I'll re-check stock right before building. Left out: sold-out pieces, field trip listings, gift card.</div>'''
html=f'<!doctype html><meta charset="utf-8"><title>Brand to Know: Gumtree Golf &amp; Nature Club — options</title><style>{css}s{{opacity:.55}}</style><h1>Brand to Know: Gumtree Golf &amp; Nature Club &mdash; options</h1><div class="sub">{k} options from gumtreegolfandnature.com, all in stock October 15, 2026 (USD; sale prices shown with the regular price struck through). REC = my suggested core. Pick by number.</div>{story}{"".join(out)}'
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/gumtree-btk-options.html','w').write(html)
print(k)
