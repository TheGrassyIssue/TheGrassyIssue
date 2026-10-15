import json,re,html,subprocess,hashlib,base64,os,sys
sys.path.insert(0,'.')
from browser import B
from PIL import Image
S='/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site/'
names={b['slug']:b['name'] for b in json.load(open(S+'data/brands.json'))}
st=json.load(open(S+'data/brand-stores.json'))['stores']
PJ={'aime-leon-dore':['wool-ribbed-knit-hoodie','olive-tree-hoodie','full-zip-pavilion-cashmere-hoodie-4','mulberry-letterman-hoodie'],
'criquet':['chill-knit-hoodie-stone','herringbone-field-hoodie-light-brown','quilted-hoodie-olive'],
'devereux-golf':['lonestar-country-club-hoodie-navy','fisherman-hoodie-brown','waffle-hoodie-bone','paynes-bay-knit-hoodie-light-blue'],
'eastside-golf':['plki-merino-wool-hooded-sweater','el2070544-410-midnight-navy-eastside-a-brushed-back-pique-hoodie','eo2030410-312-surplus-green-siganture-hoodie-camo'],
'foray-golf':['sweater-knit-hoodie-w-contrast-tipping'],
'ghost-golf':['clubhouse-hoodie','spectator-hoodie'],
'golf-gods':['clubhouse-script-hoodie-in-green'],
'jlindeberg':['kolton-wool-hoodie-kelp','rigby-fleece-hoodie-tofu','comona-pile-hood-tofu','clinton-hood-jl-navy-1'],
'jones-sports-co':['range-hoodie-loden-green','range-sweater-hoodie-jet-black'],
'bunker-mentality':['the-driver-hoodie-desert-dust'],
'bettinardi':['bettinardi-retro-wordmark-classic-fit-solid-hoodie'],
'huega-house':['warm-up-hoodie-black']}
CUR={'bunker-mentality':'£','ghost-golf':'£','golf-gods':'A$','mount-tee-golf':'A$','jlindeberg':'€?'}
items=[]
for k,hs in PJ.items():
    P={p['handle']:p for p in json.load(open(S+f'research/vest-edit/pj/{k}.json'))}
    for h in hs:
        h2=h if h in P else next(x for x in P if x.startswith(h[:40]))
        p=P[h2]
        items.append(dict(slug=k,brand=names.get(k,k),t=re.sub(r'\s+',' ',p['title']),url=f"https://{st[k]['domain']}/products/{h2}",pr=float(p['variants'][0]['price']),img=p['images'][0]['src'].split('?')[0],d=p['published_at'][:10],colors=0))
for brand,slug,dom,L in B:
    for t,h,pr,img,d in L:
        items.append(dict(slug=slug,brand=brand,t=t,url=f'https://{dom}/products/{h}',pr=pr,img='https://cdn.shopify.com/s/files/'+img,d=d,colors=0))
# colorway counts from available data
def grp(i):
    t=i['t'].lower()
    if re.search(r'knit|cashmere|merino|wool|sweater|fisherman|luxe soft',t): return 'Knit, Wool & Cashmere'
    if re.search(r'nylon|tech|performance|pique|range hoodie|grid|scuba|polartec|bonded|therma|monterey|tx course|quilted',t) and 'range sweater' not in t: return 'Tech & On-Course'
    if re.search(r'fleece|pile|sherpa|waffle|zip|terry|canvas|herringbone|hedge|applique|snap|camp|warm up|union made|classic fit|clinton|rigby',t): return 'Heavyweight & Fleece'
    return 'Clubhouse & Graphic'
PICK={'Find Your Line Après-Golf® Hoodie','Sunset Twirl Original Blue Logo Hoodie','Lonestar Country Club Hoodie - Navy','Fisherman Hoodie - Brown','Chill-Knit Hoodie - Stone','Herringbone Field Hoodie - Light Brown','Olive Tree Hoodie','Wool Ribbed Knit Hoodie','Range Hoodie - Loden Green','Kolton Wool Hoodie / Kelp','Ottoman Rib Cashmere Hoodie, Stone Blue','Flow Light Knit Hoodie, Pine','Union Made Hoodie, Heather Oatmeal','Fesque Department of Game Hoodie, Sunfaded Olive','Camargo Nylon Hoodie','Grid Tech Hoody, Oatmeal','Monterey Hoodie','Hedge Hood, Navy','Canvas Hood, Olive','Merino Aire Hoodie','Racing Stable Hoodie','Go For Broke Hoodie, Olive','Clubhouse Hoodie','Luxe Soft Hoodie','Tech Knit Hoodie','Graphic Hoodie, Motorsport Print'}
G={}
for i in items:
    i['pick']=i['t'].lower() in {x.lower() for x in PICK}; G.setdefault(grp(i),[]).append(i)
os.makedirs('/tmp/ht',exist_ok=True)
def thumb(u):
    f='/tmp/ht/'+hashlib.md5(u.encode()).hexdigest()
    if not os.path.exists(f+'.jpg'):
        subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0','-o',f,u+'?width=500'])
        im=Image.open(f).convert('RGB'); im.thumbnail((360,450)); im.save(f+'.jpg',quality=80)
    return 'data:image/jpeg;base64,'+base64.b64encode(open(f+'.jpg','rb').read()).decode()
order=['Clubhouse & Graphic','Heavyweight & Fleece','Knit, Wool & Cashmere','Tech & On-Course']
n=0;rows=''
for g in order:
    L=sorted(G.get(g,[]),key=lambda x:(not x['pick'],x['brand']!='Après Golf',x['brand']))
    rows+=f'<h2>{g} <span class="cnt">{len(L)}</span></h2><div class="grid">'
    for i in L:
        n+=1
        try: im=thumb(i['img'])
        except Exception as e: im=''; print('IMG FAIL',i['t'])
        c=CUR.get(i['slug'],'$'); p=i['pr']; ps=f"{c}{p:,.0f}" if p==int(p) else f"{c}{p:,.2f}"
        rows+=f'''<a class="c{' p' if i['pick'] else ''}" href="{i['url']}" target="_blank"><div class="im" style="background-image:url('{im}')"></div><div class="n">{n}{'<span class="rec">TGI PICK</span>' if i['pick'] else ''}</div><div class="b">{html.escape(i['brand'])}</div><div class="t">{html.escape(i['t'])}</div><div class="m">{ps} &middot; added {i['d']}</div></a>'''
    rows+='</div>'
picks=sum(i['pick'] for i in items)
doc=f'''<!doctype html><meta charset="utf-8"><title>The Hoodie Edit &mdash; options</title>
<style>body{{font:14px/1.5 Georgia,serif;background:#f3efe6;color:#1d2a1c;margin:0;padding:28px 36px;max-width:1240px}}h1{{font-size:26px;margin:0 0 6px}}h2{{font-size:19px;margin:30px 0 10px;border-bottom:1px solid #1d2a1c;padding-bottom:4px}}.cnt{{font:12px monospace;opacity:.6}}.sub{{font:12px/1.55 monospace;opacity:.85}}.box{{background:#fff;border:1px solid #ddd6c6;padding:12px 16px;margin:18px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}.c{{background:#fff;border:1px solid #e3dccb;padding:8px;color:inherit;text-decoration:none;display:block}}.c.p{{border:2px solid #2d4a2b}}.im{{aspect-ratio:4/5;background:#ece6d8 center/cover no-repeat;margin-bottom:6px}}.n{{font:bold 11px monospace;color:#2d4a2b}}.b{{font:bold 10px monospace;text-transform:uppercase;letter-spacing:.06em;opacity:.7}}.t{{font-weight:bold;font-size:13px;line-height:1.3}}.m{{font:11px monospace}}.rec{{background:#2d4a2b;color:#fff;font:bold 9px monospace;padding:1px 5px;margin-left:4px}}</style>
<h1>The Hoodie Edit &mdash; options</h1>
<div class="sub">{len(items)} men&rsquo;s hoodies from {len(set(i['slug'] for i in items))} brands in the TGI index, every one in stock in a medium as of October 14, 2026, pulled from each brand&rsquo;s own store. I swept more than 80 stores and kept one or two colorways per style; click a card to see every color. Prices are in store currency: Bunker Mentality and Ghost are &pound;, Golf Gods and Mount Tee are A$, and I&rsquo;ll confirm J.Lindeberg&rsquo;s currency at build. Each gets a (~$X) conversion.</div>
<div class="box"><strong>Proposed format:</strong> &ldquo;The Hoodie Edit&rdquo; (The Edit), opening with <strong>Après Golf</strong> (your call-out) as the lead card and hero. Short TGI Take: the hoodie went from range-only to clubhouse-acceptable, and this fall the split is a graphic clubhouse hoodie or a knit/wool hoodie that passes as a sweater. Grouped like below, one card per hoodie with brand, price, colorways and a line of copy. Brands&rsquo; own images only, framed on stone. <strong>{picks} marked TGI PICK</strong>; a tighter 15&ndash;20 would read better than all {len(items)}.<br><br><strong>Heads-up on Après Golf:</strong> their hoodies are older drops (2024) and two of the four product images are screenshots. For the hero I&rsquo;d pull a lifestyle shot from their site or Instagram-linked lookbook; I&rsquo;ll check what they have at build.<br><br><strong>Left out:</strong> Three Putt (mockup images, not real product photos), MLB-licensed Siegelman styles, women&rsquo;s styles, and anything without a medium in stock. Manors and Random Golf Club block automated checks. Woodgrain, Lazyface, St. Andr&eacute;, Late Nine, Local Rule, Sounder and Tarraing don&rsquo;t have a hoodie in stock right now.</div>
{rows}
<p class="sub" style="margin-top:22px">Every card links to the brand&rsquo;s own product page. Stock and prices get rechecked at build.</p>'''
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/hoodie-edit-options.html','w').write(doc)
json.dump(items,open('options.json','w'),indent=1,ensure_ascii=False)
print(len(items),picks,{g:len(G.get(g,[])) for g in order})
missing={x.lower() for x in PICK}-{i['t'].lower() for i in items}; print('unmatched picks',missing)
