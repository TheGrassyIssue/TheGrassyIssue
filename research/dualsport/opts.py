import json,io,base64,urllib.request,html as H
from PIL import Image
P={p['handle']:p for p in json.load(open('p1.json'))['products']}
G=[
("Polos",[
 ("flight-knit-polo-light-grey","Raglan knit, bowling-shirt collar, knitted sleeve stripes. Also seafoam, black, cream",True),
 ("flight-knit-polo-seafoam-green","Flight Knit in seafoam",False),
 ("diamond-blade-polo-green","New Blade polo: diamond steel-plate pattern sleeves. Also black",True),
 ("icon-polo-electric-blue","Next-gen Icon, contrast dark-grey collar. Also white, dark grey",True),
 ("icon-polo-galaxy","Galaxy pattern 2.0, the loud one",True),
 ("signature-polo-v2-matte-navy","Signature Polo V2, the house polo. White, cream, navy, black",False),
 ("signature-mock-neck","Signature paneling as a mock (1 size left)",False),
 ("vintage-ds-polo","Vintage DS micro-pattern, $48 (was $68)",False),
 ("signature-polo-dark-floral","Midnight Bloom floral, $34 (was $68), 3 sizes",False),
]),
("Layers & Windbreakers",[
 ("elite-windbreaker","Wide boxy quarter-zip windbreaker, mock neck, mesh lined",True),
 ("pursuit-windbreaker-black","Short-sleeve hooded windbreaker. Also electric blue (1 size)",True),
 ("cloud-performance-quarter-zip-grey","\"The softest performance quarter zip you'll own\"",True),
 ("cloud-performance-hoodie-black","Cloud fabric hoodie, black or light grey",False),
 ("shiver-quarter-zip-mist","Contrast forearm nylon quarter-zip, mist or black",True),
 ("knit-jersey","Heavy-knit classic football jersey, 100% cotton, $60 (was $98)",True),
 ("volt-knit-vest","Knit sweater vest, contrast paneling, $60 (was $88)",False),
 ("performance-cargo-vest","Nylon cargo vest, $54 (was $74)",False),
 ("vintage-ds-hoodie","Vintage DS hoodie, $50 (was $68)",False),
]),
("Shorts & Pants",[
 ("pursuit-shorts-electric-blue","5.5\" nylon, wider leg, belt loops. Also sage, black",True),
 ("motion-pants-black","\"Our best selling\" pant: high waist, straight leg, slight flare. Also platinum grey",True),
 ("motion-shorts-platinum-grey","7\" wider-leg stretch short. Also navy, black",False),
]),
("Hats",[
 ("arch-athletic-club-hat-white","5-panel perforated performance snapback. Also black + unstructured",True),
 ("ds-camo-hat","Military camo, 3D DS logo",True),
 ("mini-dual-unstructured-hat-green","Mini Dual unstructured, green or black",False),
 ("dual-athletic-club-hat-green","Dual Athletic Club, green or black",False),
 ("2-performance-hat-black","2 Performance hat (the two-sport mark)",False),
 ("slant-performance-hat-white","Slant performance hat, white or black",False),
 ("vintage-ds-classic-unstructured-hat-camo","Vintage DS classic unstructured, camo / black / white",False),
]),
("Accessories",[
 ("dual-driver-headcover","DUAL x CMC Designs faux-leather driver cover",True),
 ("dual-mallet-cover","DUAL x CMC mallet cover, motto on the tongue",True),
 ("the-gray-t-shirt-1","2 Sport ball marker by CMC Designs, the first thing they ever sold (May 2024)",True),
 ("dual-motto-wristband","Silicone band: DESIGNED TO BE VERSATILE",False),
 ("elite-socks-quarter","Elite quarter socks ($9)",False),
]),
("Football Tees",[
 ("pro-day-tshirt","Pro Day graphic, garment dyed, $28 (was $48)",True),
 ("vintage-football-tshirt","Vintage Football tee, $24",False),
 ("baller-tshirt","Baller tee, $28",False),
 ("throwback-tshirt","Throwback tee, $24",False),
]),
]
def thumb(url):
    im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url+('&' if '?' in url else '?')+'width=500',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()))
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA');bg=Image.new('RGB',im.size,(236,230,216));bg.paste(im,mask=im.split()[-1]);im=bg
    im=im.convert('RGB');im.thumbnail((400,500));b=io.BytesIO();im.save(b,'JPEG',quality=78);return base64.b64encode(b.getvalue()).decode()
out=[];n=0;opts=[]
for g,items in G:
    cards=[]
    for h,note,pick in items:
        p=P[h];n+=1;v=p['variants'][0]
        nav=sum(1 for x in p['variants'] if x['available'])
        img=p['images'][0]['src'];b=thumb(img);w=p['images'][0]['width']
        ca=v.get('compare_at_price');sale=ca and float(ca)>float(v['price'])
        opts.append(dict(n=n,group=g,handle=h,title=p['title'],price=v['price'],compare=ca if sale else None,sizes=f"{nav}/{len(p['variants'])}",note=note,pick=pick,imgs=len(p['images']),w=w))
        flag='' if w>=1000 else f'<span class="flag">{w}px</span>'
        pr=f'${float(v["price"]):.0f}'+(f' <s>${float(ca):.0f}</s>' if sale else '')
        sz='' if len(p['variants'])==1 else f' &middot; {nav}/{len(p["variants"])} sizes'
        cards.append(f'<a class="c{" p" if pick else ""}" href="https://dualsportbrand.com/products/{h}" target="_blank"><div class="im" style="background-image:url(data:image/jpeg;base64,{b})"></div><span class="n">#{n}</span>{"<span class=rec>REC</span>" if pick else ""}{flag}<div class="t">{H.escape(p["title"])}</div><div class="m">{pr}{sz}</div><div class="a">{H.escape(note)}</div></a>')
    out.append(f'<h2>{g} <span class="cnt">{len(items)}</span></h2><div class="grid">{"".join(cards)}</div>')
json.dump(opts,open('options.json','w'),indent=1)
css=open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/sunday-golf-btk-options.html').read().split('</style>')[0].split('<style>')[1]
story='''<div class="box"><strong>The story:</strong> Dual Sport is Evan Thompson&rsquo;s brand. He grew up in Clermont, Florida, played <em>both</em> football (linebacker) and golf at Kennesaw State, and now plays off about +5 as one of golf&rsquo;s bigger creators (around 250k on TikTok as of 2024). He qualified for the U.S. Amateur and has been chasing U.S. Open qualifying; this year he joined the Grass League (Scottsdale Strikers). The brand launched in spring 2024 (first product: a 2 Sport ball marker, May 4, 2024) &ldquo;built to help athletes who play more than one sport.&rdquo; Their about page is a manifesto, not a founder story: &ldquo;Be More, Be Versatile, and Be Dual,&rdquo; with six values (Commitment, Versatility, Determination, Discipline, Unique, Resilient). The look is football locker room meets golf: raglan knit polos, a heavy knit football jersey, boxy windbreakers, Pro Day and Baller tees, a wristband that reads DESIGNED TO BE VERSATILE. Their models include a 6&rsquo;5&rdquo; guy named Cornelius, which says a lot about who it&rsquo;s cut for. Stockists: Grass Clippings (Tempe, the Grass League&rsquo;s home), Iron Horse GC (Alpharetta), Badlands (NJ) and Clermont National, in his hometown.<br><br><strong>Proposed format:</strong> Brand to Know, sections for Polos, Layers, Shorts &amp; Pants, Hats &amp; Accessories (football tees as a short closing row), a &ldquo;Built for the two-sport athlete&rdquo; explainer of the six values, quotes from the about page, and FAQ (fit runs big-guy friendly, hang-dry the knits, free US shipping over $200).<br><br><strong>Flags:</strong> no long-form interview with Evan quoting him on the brand, so pull quotes would come from the brand&rsquo;s own copy and the podcast blurbs, unless you know of one. &ldquo;All-American&rdquo; only appears in his Grass League bio, so I&rsquo;d say &ldquo;former Kennesaw State linebacker&rdquo; instead. Lifestyle photos: the May 2026 drop has 4000px studio and on-course shots, so the hero is covered. Left out: sold-out items (Pursuit Windbreaker sage, several hats), the $0 Yeti bottle, old logo hats/tees down to 1 size.</div>'''
html=f'<!doctype html><meta charset="utf-8"><title>Brand to Know: Dual Sport &mdash; options</title><style>{css}</style><h1>Brand to Know: Dual Sport &mdash; options</h1><div class="sub">{n} options from dualsportbrand.com, all in stock October 16, 2026 (USD; struck price = their current sale). REC = my suggested core. Pick by number.</div>{story}{"".join(out)}'
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/dualsport-btk-options.html','w').write(html)
print(n,sum(o['pick'] for o in opts))
