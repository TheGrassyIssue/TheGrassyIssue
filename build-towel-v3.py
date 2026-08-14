#!/usr/bin/env python3
# Builds /drops/the-towel-edit-vol-3.html from the Vol. 2 template.
import re, json, os

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(SITE, "drops/the-towel-edit-vol-2.html"), encoding="utf-8").read()
IMGDIR = os.path.join(SITE, "images/towel-edit-v3")

TITLE = "The Towel Edit, Vol. 3"
SLUG = "the-towel-edit-vol-3"
DESC = ("Eighteen golf towels from eighteen independent brands, every one pulled from the "
        "brands we actually follow. Pendleton jacquard from Seamus, Swedish terry from Local "
        "Rule, and a crumpled paper-bag print from Agronomy Workshop. Swipe every angle.")

# slug, brand, name, price, sold_out, url, copy
P = [
 ("agronomy","Agronomy Workshop","Unusual Lies Towel &middot; Earth",None,False,
  "https://agronomywork.shop/store/unusual-lies-towel",
  "Printed to look like a crumpled paper bag, down to the fake fold shadows and the small print about club membership. 100% woven terry cotton. Their own product copy ends with the line \"Won't improve your lies,\" which tells you the whole posture of the brand."),
 ("local-rule","Local Rule","LCLRL Towel &middot; Dark Green","399 SEK (~$42)",False,
  "https://local-rule.com/products/lclrl-towel",
  "The logo repeated in a tight grid until it stops reading as branding and starts reading as pattern. Swedish, and priced in kronor, so budget for the conversion and the shipping. Big enough that the product shot needs a person holding it."),
 ("parmore","Mogshade &times; Parmore","No Membership Required Towel","&pound;35",True,
  "https://parmoregolf.com/products/mogshade-x-parmore-no-membership-required-towel",
  "Two brands from our universe on one towel. Blackletter type on cream, shot against a graffitied wall rather than a seamless backdrop, which is the most honest photo in this entire list."),
 ("seamus","Seamus Golf","Pendleton Wyeth Trail Towel","$45",False,
  "https://seamusgolf.com/products/pendleton-wyeth-trail-golf-towel",
  "An actual Pendleton jacquard, not a print of one. The Wyeth Trail pattern in cream, rust and slate, with a leather hanging tab. Texture you can read from across the fairway."),
 ("devereux","Devereux","Smokin' Zaleas Knitted Towel &middot; White/Green","$38",False,
  "https://devereuxgolf.com/products/smokin-zaleas-knitted-golf-towel-white-green",
  "A knitted skeleton caddie with a cigar and a bag of clubs. Knitted rather than printed, so the graphic has depth and won't crack after twenty washes."),
 ("birdsofcondor","Birds of Condor","Tokyo Country Club Towel","$39.95",True,
  "https://birdsofcondor.com/products/tokyo-country-club-black-golf-towel",
  "Black ground, yellow border, Japanese and English type sharing the same panel. The loudest thing here and the one most likely to get asked about."),
 ("dormie","Dormie Workshop","Paisley Towel &middot; Navy","$30",False,
  "https://dormieworkshop.com/products/paisley-towel-navy",
  "Navy paisley with a checkerboard band top and bottom. Dormie built its name on leather headcovers, so the towels get less attention than they should. Cheapest thing on this list."),
 ("radry","Radry Golf","Pasture Towel","$45",True,
  "https://radrygolf.com/products/pasture-towel",
  "Cows, tonal, pale green on pale green. Radry is one artist in Wisconsin drawing everything by hand, and the restraint on this one is the opposite of what the category usually does."),
 ("walker","Walker Golf","Kooka Icon Towel &middot; Forest/Yellow","$44.95",False,
  "https://walkergolfthings.com/products/kooka-icon-towel-3",
  "Kookaburras scattered across forest green in mustard yellow. Vol. 1 ran a different colorway of this towel; the Forest/Yellow is the better one and it took us two volumes to admit it."),
 ("sugarloaf","Sugarloaf Social Club","Dancing Arrows Towel","$38",True,
  "https://sugarloafsocialclub.com/products/dancing-arrows-towel",
  "Small red and navy arrows on white, woven label at the corner. Reads like a vintage tea towel someone found in a pro shop drawer."),
 ("bluegrass","Bluegrass Fairway","Do Not Remove From Pool Caddie Towel","$40",True,
  "https://bluegrassfairway.com/products/bluegrass-fairway-caddie-towel-dont-remove-from-pool",
  "Blue stripe on white with a sewn-on patch reading DO NOT REMOVE FROM POOL. The country club joke landed well enough that it sold out."),
 ("winston","Winston Collection","Course Maps Caddie Towel","$39.99",False,
  "https://winstoncollection.com/products/course-maps-caddie-towel-copy",
  "Dozens of tiny green course-map ovals scattered across white terry. Close up you can pick out individual routings."),
 ("matchstick","Matchstick Golf","Roosevelt Pattern Towel","$29",False,
  "https://matchstickgolf.com/products/roosevelt-pattern-golf-towel",
  "Dense yellow iconography on black, hung from a carabiner. Matchstick came to us through ball markers; the towels are the better product."),
 ("swag","SWAG Golf","Texas Locals Only Towel","$44.44",False,
  "https://swaggolf.com/products/texas-locals-only-golf-towel",
  "Orange paisley, Texas edition, part of a state-by-state run. The Austin pick by default, and the one item here you can find without leaving the country."),
 ("malbon","Malbon Golf","Ironworks Caddy Towel &middot; Ivory","$58",False,
  "https://malbongolf.com/products/ironworks-caddy-towel-ivory",
  "Collegiate block lettering in pale blue on ivory, no border, no trim. Vol. 1 ran Malbon's black towel. This is the quieter one and the more expensive one."),
 ("jones","Jones Sports Co","Tour Towel &middot; All Black","$38",False,
  "https://jonessportsco.com/products/tour-towel-all-black",
  "Ribbed black with a woven Jones label at the fold. Jones has been making bags since 1971 and the towel is built like it belongs to one."),
 ("leftoffield","Left of Field","Flower Golf Towel &middot; Brown","A$35 (~$23)",True,
  "https://lofgolf.com/products/camo-towel",
  "Tonal flowers on tan, Sydney-made, sold in Australian dollars. The most muted thing in this list, which is why it survived the cut."),
 ("sounder","Sounder","Cleeve Hill Logo Bag Towel","&pound;30",False,
  "https://soundergolf.com/products/cleeve-hill-logo-bag-towel",
  "Black with white banding and a small tree mark at the base, named for the course in Gloucestershire. Sold in pounds."),
]

SECTIONS = [
 ("The Ones With a Story", ["agronomy","local-rule","parmore","seamus"]),
 ("Pattern and Print", ["devereux","birdsofcondor","dormie","radry","walker"]),
 ("Club Codes", ["sugarloaf","bluegrass","winston","matchstick","swag"]),
 ("Plain, Done Properly", ["malbon","jones","leftoffield","sounder"]),
]

FAQ = [
 ("How many golf towels does this list cover?",
  "Eighteen towels from eighteen different brands. Every brand is one The Grassy Issue already follows and has covered or is tracking."),
 ("Are any of these towels sold out?",
  "Six of the eighteen were sold out at the time of writing: Mogshade &times; Parmore, Birds of Condor, Radry Golf, Sugarloaf Social Club, Bluegrass Fairway and Left of Field. All six are repeat items their brands have restocked before."),
 ("What is the cheapest golf towel here?",
  "The Matchstick Golf Roosevelt Pattern towel at $29, followed by Dormie Workshop's Paisley Towel at $30."),
 ("What is the most expensive?",
  "Malbon Golf's Ironworks Caddy Towel at $58. Local Rule's LCLRL towel is 399 SEK, roughly $42 before shipping from Sweden."),
 ("Which towels are not priced in US dollars?",
  "Four. Local Rule prices in Swedish kronor, Mogshade &times; Parmore and Sounder in British pounds, and Left of Field in Australian dollars. Convert before you check out."),
 ("Does this overlap with Vol. 1 and Vol. 2?",
  "Some brands repeat, the products do not. Malbon, Jones, Walker Golf, Devereux, Birds of Condor, Sugarloaf Social Club and Seamus all appeared in earlier volumes with different towels."),
 ("Is the Seamus towel really Pendleton fabric?",
  "Yes. It is a collaboration, and the Wyeth Trail jacquard is woven by Pendleton rather than printed to imitate it."),
]

def imgs(slug):
    n = len([f for f in os.listdir(IMGDIR) if f.startswith(slug + "-")])
    return [f"/images/towel-edit-v3/{slug}-{i+1}.jpg" for i in range(n)]

def card(slug, brand, name, price, sold, url, copy):
    ims = imgs(slug)
    alt = re.sub(r"&\w+;", " ", f"{brand} {name}").strip()
    frames = "".join(
        f'<div class="pg-frame"><img src="{u}" alt="{alt} — view {i+1} of {len(ims)}" loading="lazy" /></div>'
        for i, u in enumerate(ims))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
                   for i in range(len(ims))) if len(ims) > 1 else ""
    nav = ('<button class="pg-arw prev" aria-label="Previous image">‹</button>'
           '<button class="pg-arw next" aria-label="Next image">›</button>') if len(ims) > 1 else ""
    count = f'<span class="pg-count">1/{len(ims)}</span>' if len(ims) > 1 else ""
    so = ' <span class="so">&middot; Sold out</span>' if sold else ""
    pr = f" &middot; {price}" if price else ""
    return f"""
    <div class="product-card" data-frames="{len(ims)}">
      <div class="product-gallery">
        <div class="pg-track">{frames}</div>
        {nav}{count}
        <div class="pg-dots">{dots}</div>
      </div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name}{pr}{so}</div>
        <div class="product-desc">{copy}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""

by = {p[0]: p for p in P}
grid = ""
for hdr, slugs in SECTIONS:
    grid += f'\n  <h2 class="products-hdr sec">{hdr}</h2>\n  <div class="products-grid">'
    grid += "".join(card(*by[s]) for s in slugs)
    grid += "\n  </div>\n"

faq_html = '\n  <h2 class="products-hdr sec">Questions</h2>\n  <div class="faq">' + "".join(
    f'\n    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "\n  </div>\n"

GALLERY_CSS = """
.products-hdr.sec{font-size:11px;letter-spacing:.2em;opacity:.75;margin:44px 0 20px;border-top:.5px solid var(--ink);padding-top:18px}
.products-hdr.sec:first-of-type{margin-top:0;border-top:0;padding-top:0}
.product-card{position:relative}
.product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}
.pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.pg-track::-webkit-scrollbar{display:none}
.pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}
.pg-frame img{width:100%;height:100%;object-fit:cover;display:block}
.pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:.5px solid var(--ink);background:var(--paper);color:var(--ink);font-size:17px;line-height:1;cursor:pointer;opacity:0;transition:opacity .18s;z-index:2;padding:0}
.pg-arw.prev{left:8px}.pg-arw.next{right:8px}
.product-card:hover .pg-arw{opacity:.9}
.pg-arw:hover{opacity:1}
.pg-count{position:absolute;top:8px;right:8px;font-family:var(--mono);font-size:9px;letter-spacing:.1em;background:var(--paper);border:.5px solid var(--ink);padding:2px 6px;z-index:2}
.pg-dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:5px;z-index:2}
.pg-dot{width:6px;height:6px;border-radius:50%;border:.5px solid var(--ink);background:var(--paper);padding:0;cursor:pointer;opacity:.55;transition:opacity .15s}
.pg-dot.on{background:var(--ink);opacity:1}
.so{opacity:.5;font-style:normal;font-family:var(--mono);font-size:10px;letter-spacing:.08em}
.faq{max-width:820px}
.faq-q{border-top:.5px solid var(--ink);padding:14px 0}
.faq-q summary{font-family:var(--serif);font-size:16px;cursor:pointer;list-style:none}
.faq-q summary::-webkit-details-marker{display:none}
.faq-q summary:before{content:"+ ";font-family:var(--mono);opacity:.5}
.faq-q[open] summary:before{content:"\\2212 "}
.faq-q p{font-family:var(--sans);font-size:13px;line-height:1.6;opacity:.8;margin:10px 0 0}
@media(max-width:900px){.pg-arw{opacity:.85}}
"""

GALLERY_JS = """
<script>
(function(){
  document.querySelectorAll('.product-gallery').forEach(function(g){
    var track=g.querySelector('.pg-track'),
        dots=[].slice.call(g.querySelectorAll('.pg-dot')),
        count=g.querySelector('.pg-count'),
        n=g.parentNode.dataset.frames|0;
    if(n<2) return;
    function idx(){ return Math.round(track.scrollLeft/track.clientWidth); }
    function go(i){ track.scrollTo({left:track.clientWidth*Math.max(0,Math.min(n-1,i)),behavior:'smooth'}); }
    function sync(){
      var i=idx();
      dots.forEach(function(d,j){ d.classList.toggle('on',j===i); });
      if(count) count.textContent=(i+1)+'/'+n;
    }
    track.addEventListener('scroll',function(){ window.requestAnimationFrame(sync); },{passive:true});
    dots.forEach(function(d){ d.addEventListener('click',function(e){ e.preventDefault(); go(+d.dataset.i); }); });
    var p=g.querySelector('.pg-arw.prev'), nx=g.querySelector('.pg-arw.next');
    if(p) p.addEventListener('click',function(e){ e.preventDefault(); go(idx()-1); });
    if(nx) nx.addEventListener('click',function(e){ e.preventDefault(); go(idx()+1); });
  });
})();
</script>
"""

h = BASE

# ---- head metadata ----
h = h.replace("The Towel Edit, Vol. 2 — The Grassy Issue", f"{TITLE} — The Grassy Issue")
h = h.replace("The Towel Edit, Vol. 2", TITLE)
h = h.replace("the-towel-edit-vol-2", SLUG)
h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), h)
h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), h)
h = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), h)

# ---- JSON-LD: rewrite Article, append FAQPage ----
def fix_article(m):
    d = json.loads(m.group(1))
    d["headline"] = TITLE
    d["description"] = DESC
    d["url"] = f"https://thegrassyissue.com/drops/{SLUG}"
    d["datePublished"] = "2026-08-14"
    d["dateModified"] = "2026-08-14"
    d["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"https://thegrassyissue.com/drops/{SLUG}"}
    return '<script type="application/ld+json">\n' + json.dumps(d, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix_article, h, count=1, flags=re.S)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":re.sub(r"&\w+;"," ",q),
     "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&\w+;"," ",a)}} for q,a in FAQ]}
h = h.replace("</head>", '<script type="application/ld+json">\n' + json.dumps(faq_ld, indent=2) + '\n</script>\n</head>')

# ---- CSS ----
h = h.replace("</style>", GALLERY_CSS + "\n</style>", 1)

# ---- hero ----
h = re.sub(r'<div class="drop-hero">.*?</div></div>',
    '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/towel-edit-v3/local-rule-1.jpg" '
    'alt="The Towel Edit Vol. 3 — Local Rule LCLRL towel held open" /></div></div>', h, count=1, flags=re.S)

# ---- writeup ----
new_writeup = """<div class="writeup">
  <div class="writeup-body">
    <p>Eighteen towels, eighteen brands, and for the first time every single one comes from the list we already follow. That was the whole constraint this round. No filler pulled off a marketplace to round the number out.</p>
    <p>The best of them are doing something a towel has no obligation to do. Agronomy Workshop printed theirs to look like a crumpled paper bag. Seamus went and got real Pendleton jacquard woven for the Wyeth Trail. Mogshade and Parmore put blackletter type on cream and shot it against a wall covered in graffiti.</p>
    <p>Prices run $29 to $58, plus four brands selling in kronor, pounds and Australian dollars. Six were sold out when we wrote this, which we have stopped treating as disqualifying. These are repeat items and the brands restock them. Every card below swipes through every photo the brand publishes.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>18 items</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$29 &ndash; $58</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#GearEdit</span>
        <span class="hashtag">#GolfTowels</span>
        <span class="hashtag">#TowelEdit</span>
      </div>
    </div>
  </aside>
</div>"""
h = re.sub(r'<div class="writeup">.*?</aside>\s*</div>', new_writeup, h, count=1, flags=re.S)

# ---- products grid ----
start = h.find('<section class="products">')
end = h.find('<section class="more"')
if end == -1:
    end = h.find('<div class="more"')
assert start != -1 and end != -1 and end > start, (start, end)
h = h[:start] + '<section class="products">\n' + grid + faq_html + '</section>\n\n' + h[end:]

# ---- JS before </body> ----
h = h.replace("</body>", GALLERY_JS + "</body>")

out = os.path.join(SITE, f"drops/{SLUG}.html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
