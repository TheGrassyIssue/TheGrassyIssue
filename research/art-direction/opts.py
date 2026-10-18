import json,io,base64,html as H
from PIL import Image
R='/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site'
M=json.load(open(R+'/data/brand-mentions.json')); B={x['slug']:x for x in json.load(open(R+'/data/brands.json'))}
C=[
("whim-golf","/images/off-course-vol2/whim-cupola.jpg","A design label that treats objects as seriously as garments (the Cupola, the Reebok collab). No profile yet on TGI.",True),
("left-of-field-golf","/images/left-of-field-golf/btk-hero.jpg","Surf and skate silhouettes; every collection named for a stretch of Australian coast.",True),
("sentinel-golf","/images/sentinel-golf/btk-hero.jpg","Product design pick: Dyneema walker bags, Danish textiles, no logos shouting.",True),
("found-golf","/images/found-golf/hero.jpg","Half gallery, half golf label: art-first objects from Melbourne.",True),
("kingfisher-golf","/images/kingfisher-golf/hero-package.jpg","Founded by a former PepsiCo art director; graphics and packaging are the point.",True),
("cloud-and-wind-golf","/images/cloud-and-wind-golf/btk-hero.jpg","Grips as design objects: Eastern aesthetics, Chinese verse printed on the box.",True),
("forden-golf","/images/forden/hero-tee-picks.jpg","The Swingman logo comes from Doc Edgerton's 1938 strobe photo of a golf swing at MIT. Great graphic story.",True),
("radry-golf","/images/radry-golf/btk-hero.jpg","A Wisconsin artist's label: the bird-in-a-bucket-hat logo is drawn before it's stitched.",True),
("axxa","/images/axxa/golfer-knit.jpg","Sydney surf-meets-golf with jacquard heavyweight knits; one TGI mention.",True),
("slice-town","/images/slice-town/btk-hero.jpg","Copenhagen golf streetwear: wide nylon track suits, reflective layers, a yellow knit balaclava.",True),
("mogshade","/images/brand-heroes/mogshade.jpg","Portuguese handmade covers and towels with a strong color sense.",True),
("fyfe-golf","/images/fyfe-golf/btk-hero.jpg","Harris Tweed, tartan and RAF flight suits cut into covers; material-led design.",False),
("mackenzie","/images/mackenzie/life-affric-set.jpg","Handmade carry bags since 1985; product design and collab craft.",False),
("puttwell","/images/puttwell/hero.jpg","Hawaii music-and-art crew: DJ-culture tees, Know Your Roll covers, Sig Zane collab.",True),
("hidden-links-society","/images/hidden-links-society/btk-hero.jpg","Anti-country-club graphics and heavyweight cotton.",False),
("f-and-co","/images/hat-brands/band-fandco-2.jpg","Gold Coast headwear only: corduroy, gingham and pinstripe caps sampled until the shape is right.",False),
("morning-people-clothiers","/images/morning-people-clothiers/performance-hat-icon.jpg","Early-tee-time clothes with a clean icon system.",False),
]
def thumb(p):
    im=Image.open(R+p).convert('RGB'); im.thumbnail((500,500)); b=io.BytesIO(); im.save(b,'JPEG',quality=78); return base64.b64encode(b.getvalue()).decode()
cards=[];n=0;opts=[]
for s,img,note,rec in C:
    n+=1;x=B[s];cov=len(M.get(s,[]))
    opts.append(dict(n=n,slug=s,img=img,rec=rec))
    cards.append(f'<a class="c{" p" if rec else ""}" href="https://thegrassyissue.com/brands/{s}" target="_blank"><div class="im" style="background-image:url(data:image/jpeg;base64,{thumb(img)})"></div><span class="n">#{n}</span>{"<span class=rec>REC</span>" if rec else ""}<div class="t">{H.escape(x["name"])}</div><div class="m">{H.escape(x["loc"])} &middot; {cov} TGI posts</div><div class="a">{H.escape(note)}</div></a>')
json.dump(opts,open(R+'/research/art-direction/options.json','w'),indent=1)
css=open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/sunday-golf-btk-options.html').read().split('</style>')[0].split('<style>')[1]
box='''<div class="box"><strong>The idea:</strong> &ldquo;12 Independent Golf Brands With the Best Art Direction&rdquo;, judged on lookbooks and photography, graphics and logos, and product design (packaging and websites left out, per your call). Independents only, so no Malbon-size or big-company labels.<br><br><strong>Each brand would get:</strong> a short TGI take on what makes its look work; a band of 3&ndash;4 images from its latest lookbook or campaign (pulled fresh from the brand, not our old posts, with photographer credits where the brand gives them); 3&ndash;4 products that show the design best, with live prices; and a link to its TGI brand page. Plus an intro on why art direction matters in golf now, and an FAQ.<br><br><strong>Format question for you:</strong> ranked 1&ndash;10, or unranked and grouped (e.g. &ldquo;Photography&rdquo;, &ldquo;Graphics&rdquo;, &ldquo;Product&rdquo;)? I&rsquo;d lean unranked and grouped.<br><br><strong>Notes:</strong> thumbnails here are from our existing coverage, just to jog memory. None of these 20 appears in our last 10 posts (Metalwood, Dual Sport, Technical Vol. 2, club makers, Sunday Golf, Matchstick, Gumtree, the Hoodie Edit, Mount Tee, CPH Golf), so Metalwood, Sounder, Quiet Golf, Walker, Merrill, Local Rule, Late Nine, Casualist, Students and Sugarloaf came off. Whim, Engel and Axxa have barely been covered, which makes them good discoveries. Also left out on purpose: Malbon, Eastside (Jordan Brand), CPH Golf and BEAMS Golf (big-company lines).</div>'''
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/art-direction-options.html','w').write(f'<!doctype html><meta charset="utf-8"><title>Best art direction &mdash; options</title><style>{css}</style><h1>Best Art Direction &amp; Design &mdash; options</h1><div class="sub">17 independent brands from our index, none in our last 10 posts. REC = my suggested 12. Pick 12 by number.</div>{box}<h2>Candidates <span class="cnt">17</span></h2><div class="grid">{"".join(cards)}</div>')
print(n)
