import json,io,base64,urllib.request,html as H
from PIL import Image
P={p['handle']:p for p in json.load(open('p1.json'))['products']}
G=[
("Handmade Headcovers",[
 ("osu-beavers-black-driver-no-1","Matchstick x OSU, from a reclaimed OSU knit jacket + waxed canvas; officially licensed",True),
 ("osu-beavers-golf-headcover-driver-no-3","Same OSU jacket, different panel layout",False),
 ("osu-beavers-golf-headcover-wood-hybrid-no-1","OSU wood/hybrid",False),
 ("osu-beavers-golf-headcover-wood-hybrid-no-2","OSU wood/hybrid",False),
 ("osu-beavers-golf-headcover-wood-hybrid-no-3","OSU wood/hybrid",False),
 ("usa-dream-team-basketball-upcycled-headcover-drive","From a USA Basketball 'Dream Team' piece; one of one",True),
 ("u-s-soccer-upcycled-headcover-driver","From a USMNT snap-up jacket; back panel reads USA around the cover",True),
 ("usa-olympic-starter-jacket-upcycled-headcover-wood","From a USA Olympic Starter jacket's sleeves, cuff logo kept",False),
 ("new-york-basketball-driver-golf-headcover","From a vintage New York basketball jersey, Champion tag moved to the top",True),
 ("new-york-basketball-wood-hybrid-golf-headcover","Matching wood/hybrid",False),
 ("roosevelt-pattern-driver-headcover","Roosevelt High School pattern; proceeds to the Roosevelt Golf Fund",True),
 ("team-edition-roosevelt-pattern-driver-headcover","What the Roosevelt HS golf teams actually play",False),
 ("custom-golf-headcovers","Bring your own garment: jersey, jacket, a kid's shirt",True),
]),
("Ball Markers",[
 ("cash","Cash Stack: one of the 2021 launch designs",True),
 ("putterade-frost","Putterade: the late-90s sports drink bottle. 8 colors in stock",True),
 ("devil-horns-black-gold","Devil Horns, new Sept. 6 colors",False),
 ("old-fashioned","Started as a custom for a friend's golf trip; now a best seller",True),
 ("transfusion","Golf's favorite cocktail",True),
 ("iced-coffee-golf-ball-marker","Iced Coffee",False),
 ("pirate-flag","Pirate Flag",False),
 ("skeleton-key","Skeleton Key",False),
 ("truffle-shuffle","Truffle Shuffle",False),
 ("chef-skull","Chef Skull, collab with The Generous Chef",False),
 ("teddy-roosevelt","Teddy Roosevelt (Roosevelt Golf Fund line)",False),
 ("gas-pump-golf-ball-marker","Gas Pump",False),
 ("fire-truck-golf-ball-marker","Fire Truck",False),
 ("poker-chip","Poker Chip",False),
 ("red-dice","Red Dice",False),
 ("vw-bus","VW Bus",False),
 ("oregon-state-beavers-head-golf-ball-marker-brushed-gold","OSU Beaver, licensed. 8 OSU markers in stock",False),
 ("oregon-state-beavers-football-helmet-golf-ball-mar","OSU football helmet",False),
 ("lady-liberty-ball-marker","Lady Liberty ($30)",False),
 ("build-your-own-custom-golf-ball-marker","Custom markers for trips, weddings, events",False),
]),
("Towels, Ferrules and More",[
 ("roosevelt-pattern-golf-towel","Roosevelt pattern towel; proceeds to the Roosevelt Golf Fund",True),
 ("blue-putterade-golf-towel","Putterade towel",False),
 ("pink-sugar-skull-golf-towel","Sugar Skull towel",False),
 ("key-lime-pie","Key Lime Pie ferrules (set of 10); only ferrule in stock",True),
 ("matchstick-man-jones-ranger-r-shag-bag-black","Jones x Matchstick Ranger shag bag/cooler, made to order",True),
 ("matchstick-man-jones-rangefinder-pouch-navy","Jones x Matchstick rangefinder pouch",False),
 ("tiger-roar-relief-print","Linocut of Tiger at the Masters by Portland artist Audrey Delgado (Dane's mother)",True),
 ("matchstick-bamboo-golf-tees","Bamboo tees ($6)",False),
 ("flame-magnetic-hat-clip","Flame magnetic hat clip ($6)",False),
 ("matchstick-man-keychain","Woody keychain ($5)",False),
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
        hs=[k for k in P if k.startswith(h) and any(x['available'] for x in P[k]['variants'])] or [k for k in P if k.startswith(h)]; h=sorted(hs,key=len)[0]; p=P[h];n+=1;v=p['variants'][0]
        nav=sum(1 for x in p['variants'] if x['available'])
        img=(p['images'][2 if h.startswith('build-your-own') else 0]['src']) if p['images'] else ''
        b=thumb(img) if img else ''
        w=p['images'][0]['width'] if p['images'] else 0
        opts.append(dict(n=n,group=g,handle=h,title=p['title'],price=v['price'],note=note,pick=pick,imgs=len(p['images']),w=w))
        flag='' if w>=1000 else f'<span class="flag">{w}px</span>'
        cards.append(f'<a class="c{" p" if pick else ""}" href="https://matchstickgolf.com/products/{h}" target="_blank"><div class="im" style="background-image:url(data:image/jpeg;base64,{b})"></div><span class="n">#{n}</span>{"<span class=rec>REC</span>" if pick else ""}{flag}<div class="t">{H.escape(p["title"])}</div><div class="m">${float(v["price"]):.0f} &middot; {len(p["images"])} photos</div><div class="a">{H.escape(note)}</div></a>')
    out.append(f'<h2>{g} <span class="cnt">{len(items)}</span></h2><div class="grid">{"".join(cards)}</div>')
json.dump(opts,open('options.json','w'),indent=1)
css=open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/sunday-golf-btk-options.html').read().split('</style>')[0].split('<style>')[1]
story='''<div class="box"><strong>The story (from Matchstick&rsquo;s own site and blog):</strong> Dane Delgado, a Willamette Valley native who learned the game tagging along with his uncle at par 3s in Salem, spent the first half of his career as an NBA writer. In 2020 he lost his favorite ball marker, couldn&rsquo;t find a replacement he liked at a fair price, and drew his own. Matchstick went live on July 17, 2021 with eight designs, run at night from the front room of a small apartment; by month three it was a real business, and within seven months it had 800+ orders shipped as far as Japan, Ireland and Sweden. The rules haven&rsquo;t changed: no logos on the marker, small enough not to deflect a putt (&ldquo;they shouldn&rsquo;t be the size of a goddamn poker chip&rdquo;), fair prices, every marker hand painted and polished, sold in matchbox packaging. Since 2024 Matchstick has a shop in Dane&rsquo;s work-live loft in St. Johns, North Portland, down the road from Wildwood. His mom Audrey made the Tiger linocut. Now the most interesting thing they make: <strong>handmade headcovers cut from reclaimed jackets and jerseys</strong> (a Dream Team piece, a USMNT jacket, an Olympic Starter jacket, an officially licensed OSU line) with Polartec lining, plus a Roosevelt High pattern whose proceeds fund the school&rsquo;s golf teams. He also writes about munis: 33 rounds at Glendoveer in three years.<br><br><strong>Proposed format:</strong> Brand to Know, &ldquo;In His Words&rdquo; from Dane&rsquo;s blog, sections for Headcovers, Markers, and Towels/Ferrules/Collabs, a short &ldquo;What makes a Matchstick marker&rdquo; explainer, and FAQ. TGI already covers Matchstick in 7 posts (marker atlas, towel and hat edits); this would become its profile page.<br><br><strong>Flags:</strong> no founder portrait yet, I&rsquo;ll check their Instagram-linked site photos; product shots vary in resolution (red tag = under 1000px, softer on the page). Left out: Native Headdress marker, the Josh Allen marker, sold-out pieces, option/fee listings, sticker pack, gift card.</div>'''
html=f'<!doctype html><meta charset="utf-8"><title>Brand to Know: Matchstick Golf &mdash; options</title><style>{css}</style><h1>Brand to Know: Matchstick Golf &mdash; options</h1><div class="sub">{n} options from matchstickgolf.com, all in stock October 15, 2026 (USD, no sale on). REC = my suggested core. Pick by number.</div>{story}{"".join(out)}'
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/matchstick-btk-options.html','w').write(html)
print(n)
