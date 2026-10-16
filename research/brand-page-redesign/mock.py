import json,base64,io,re,html as H
from PIL import Image
B={b['slug']:b for b in json.load(open('data/brands.json'))}
M=json.load(open('data/brand-mentions.json')); T=json.load(open('data/post-thumbs.json'))
def b64(path,w=1400,h=None,crop=None):
    im=Image.open(path.lstrip('/')).convert('RGB')
    if crop:
        W,Hh=crop; s=max(W/im.width,Hh/im.height); im=im.resize((round(im.width*s+.5),round(im.height*s+.5)),Image.LANCZOS)
        x=(im.width-W)//2;y=int((im.height-Hh)*.45); im=im.crop((x,y,x+W,y+Hh))
    else: im.thumbnail((w,h or w))
    b=io.BytesIO(); im.save(b,'JPEG',quality=80); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def posts(slug):
    out=[]
    for e in M[slug]:
        u=e['url'].split('#')[0]; f=u.lstrip('/')+'.html'
        try: s=open(f).read()
        except: continue
        d=re.search(r'"datePublished":\s*"([\d-]+)"',s); d=d.group(1) if d else ''
        th=T.get(u,{}).get('img')
        if not th: continue
        out.append(dict(url=u,title=H.unescape(e['title']).split(' — The Grassy')[0],date=d,img=th,cat=T[u].get('cat','Drops & Brands'),profile=e.get('profile')))
    out.sort(key=lambda x:(not x['profile'],x['date']),reverse=False)
    prof=[p for p in out if p['profile']]; rest=sorted([p for p in out if not p['profile']],key=lambda x:x['date'],reverse=True)
    return prof+rest
def fmt(d):
    import datetime
    try: return datetime.date.fromisoformat(d).strftime('%b %-d, %Y')
    except: return ''
FONT=lambda f:base64.b64encode(open('assets/fonts/'+f,'rb').read()).decode()
CSS="""@font-face{font-family:ENT;src:url(data:font/woff2;base64,FONTB) format('woff2');font-weight:700}
@font-face{font-family:ENT;src:url(data:font/woff2;base64,FONTR) format('woff2');font-weight:400}
:root{--paper:#F4F1EA;--ink:#141414;--grass:#2D4A2B;--rough:#A8A878;--mono:ui-monospace,'SF Mono',Menlo,monospace;--serif:ENT,Georgia,serif}
*{box-sizing:border-box}body{margin:0;background:#d9d4c7;font-family:var(--serif);color:var(--ink)}
.lab{max-width:1320px;margin:40px auto 10px;padding:0 20px;font:600 13px/1.5 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:#2D4A2B}
.lab span{display:block;font:400 13px/1.6 Georgia,serif;letter-spacing:0;text-transform:none;color:#333;max-width:860px;margin-top:6px}
.frame{max-width:1320px;margin:0 auto 30px;background:var(--paper);box-shadow:0 10px 40px rgba(0,0,0,.18);overflow:hidden}
.nav{display:flex;justify-content:space-between;align-items:center;padding:18px 32px;border-bottom:.5px solid rgba(20,20,20,.15)}
.wm{font:700 18px/1 var(--serif);letter-spacing:.14em;text-transform:uppercase;color:var(--grass)}
.nl{font:11px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.7;display:flex;gap:26px}
.crumb{font:10px var(--mono);letter-spacing:.16em;text-transform:uppercase;opacity:.6}
.kick{font:11px var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--grass)}
.btn{display:inline-flex;align-items:center;gap:8px;font:11px var(--mono);letter-spacing:.14em;text-transform:uppercase;padding:12px 18px;border:1px solid var(--ink);color:var(--ink);text-decoration:none;background:transparent}
.btn.solid{background:var(--ink);color:var(--paper)}
.btn.light{border-color:rgba(255,255,255,.85);color:#fff}.btn.light.solid{background:#fff;color:var(--ink)}
.ico{width:14px;height:14px;display:inline-block}
.tag{font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;border:1px solid rgba(20,20,20,.25);border-radius:20px;padding:6px 12px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:#fff;border:.5px solid rgba(20,20,20,.15);text-decoration:none;color:inherit}
.card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.card .b{padding:16px 18px 20px}.card .c{font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:8px}
.card .t{font:700 20px/1.2 var(--serif)}
.feat{display:grid;grid-template-columns:300px 1fr;max-width:900px;background:var(--grass);color:#fff;text-decoration:none;margin-bottom:26px}
.feat img{width:100%;height:100%;object-fit:cover;display:block;min-height:0;aspect-ratio:4/3}
.feat .b{padding:22px 28px;display:flex;flex-direction:column;justify-content:center}
.feat .c{font:10px var(--mono);letter-spacing:.18em;text-transform:uppercase;opacity:.8;margin-bottom:8px}
.feat .t{font:700 22px/1.2 var(--serif);margin-bottom:8px}.feat .d{font:14px/1.5 var(--serif);opacity:.9}
.h2{font:700 30px/1.15 var(--serif);margin:0 0 6px}
.row{display:grid;grid-template-columns:160px 1fr auto;gap:24px;align-items:center;padding:18px 0;border-top:.5px solid rgba(20,20,20,.18);text-decoration:none;color:inherit}
.row img{width:160px;aspect-ratio:4/3;object-fit:cover}
.row .t{font:700 22px/1.2 var(--serif)}.row .m{font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.6}
.foot{padding:26px 32px;border-top:.5px solid rgba(20,20,20,.15);font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.5}
""".replace("FONTB",FONT('editors-note-text-bold.woff2')).replace("FONTR",FONT('editors-note-text-regular.woff2'))
IG='<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
NAV='<div class="nav"><div class="wm">The Grassy Issue</div><div class="nl"><span>The Feed</span><span>Brands</span><span>Field Guide</span><span>Events</span><span>About</span></div></div>'
FOOT='<div class="foot">&copy; 2026 The Grassy Issue</div>'
def buttons(site,ig,light=False):
    L=' light' if light else ''
    return (f'<a class="btn solid{L}">Visit {H.escape(site.split("//")[1].strip("/"))} &#8599;</a>'
            f'<a class="btn{L}">{IG} @{ig}</a>')
def cards(ps,n=6):
    return '<div class="grid">'+''.join(f'<a class="card"><img src="{b64(p["img"],800)}"><div class="b"><div class="c">{H.escape(p["cat"])} &middot; {fmt(p["date"])}</div><div class="t">{H.escape(p["title"])}</div></div></a>' for p in ps[:n])+'</div>'
def feat(p,desc):
    return f'<a class="feat"><img src="{b64(p["img"],1100)}"><div class="b"><div class="c">Brand to Know &middot; {fmt(p["date"])}</div><div class="t">{H.escape(p["title"])}</div><div class="d">{desc}</div><div style="margin-top:12px;font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid rgba(255,255,255,.7);align-self:flex-start;padding-bottom:2px">Read the profile &#8594;</div></div></a>'
FEATIMG=None
def A(slug,hero,site,ig,desc,meta,since):
    b=B[slug];ps=posts(slug);prof=[p for p in ps if p['profile']];rest=[p for p in ps if not p['profile']]
    hero_html=(f'<div style="position:relative;height:620px;background:#222 url({b64(hero,2000,crop=(2000,900))}) center/cover">'
      f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,rgba(0,0,0,.72))"></div>'
      f'<div style="position:absolute;left:48px;right:48px;bottom:44px;color:#fff"><div class="crumb" style="opacity:.8;color:#fff">Feed / The Brand Index / {H.escape(b["name"])}</div>'
      f'<div style="font:700 88px/1 var(--serif);letter-spacing:-.02em;margin:14px 0 14px">{H.escape(b["name"])}</div>'
      f'<div style="font:11px var(--mono);letter-spacing:.18em;text-transform:uppercase;opacity:.9">{meta}</div></div></div>')
    bar=(f'<div style="display:grid;grid-template-columns:1.4fr 1fr;gap:48px;padding:40px 48px;border-bottom:.5px solid rgba(20,20,20,.15)">'
      f'<div><div style="font:21px/1.55 var(--serif)">{H.escape(b["line"])}</div><div style="display:flex;gap:8px;margin-top:20px">'+''.join(f'<span class="tag">{t.replace("-"," ")}</span>' for t in b.get('tags',[]))+'</div></div>'
      f'<div style="border-left:.5px solid rgba(20,20,20,.2);padding-left:36px"><div class="kick" style="margin-bottom:14px">Find them</div><div style="display:flex;flex-direction:column;gap:10px;align-items:flex-start">{buttons(site,ig)}</div>'
      f'<div style="font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin-top:18px">{since} &middot; {len(ps)} TGI stories</div></div></div>')
    body=f'<div style="padding:44px 48px 56px"><div class="kick" style="margin-bottom:8px">On The Grassy Issue</div><div class="h2" style="margin-bottom:24px">Every story featuring {H.escape(b["name"])}</div>'
    if prof: body+=feat(dict(prof[0],img=FEATIMG or prof[0]["img"]),desc)
    body+=cards(rest)+'</div>'
    return NAV+hero_html+bar+body+FOOT
def Btri(slug,imgs,site,ig,meta,since):
    b=B[slug];ps=posts(slug)
    tri='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px">'+''.join(f'<img src="{b64(i,700,crop=(700,875))}" style="width:100%;display:block">' for i in imgs)+'</div>'
    head=(f'<div style="padding:42px 48px 36px;display:grid;grid-template-columns:1.5fr 1fr;gap:40px;align-items:end;border-bottom:.5px solid rgba(20,20,20,.15)">'
      f'<div><div class="crumb">Feed / The Brand Index / {H.escape(b["name"])}</div><div style="font:700 76px/1.02 var(--serif);letter-spacing:-.02em;margin:14px 0 12px">{H.escape(b["name"])}</div>'
      f'<div class="kick" style="opacity:.8">{meta}</div><div style="font:20px/1.55 var(--serif);margin-top:18px;max-width:640px">{H.escape(b["line"])}</div></div>'
      f'<div style="display:flex;flex-direction:column;gap:10px;align-items:flex-start">{buttons(site,ig)}<div style="font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin-top:8px">{since} &middot; {len(ps)} TGI stories</div></div></div>')
    body=f'<div style="padding:44px 48px 56px"><div class="kick" style="margin-bottom:8px">On The Grassy Issue</div><div class="h2" style="margin-bottom:24px">Every story featuring {H.escape(b["name"])}</div>{cards(ps)}</div>'
    return NAV+tri+head+body+FOOT
def C(slug,hero,site,ig,desc,meta,since):
    b=B[slug];ps=posts(slug)
    hero_html=(f'<div style="display:grid;grid-template-columns:1.25fr 1fr;min-height:640px">'
      f'<div style="background:url({b64(hero,1400,crop=(1400,1300))}) center/cover"></div>'
      f'<div style="padding:56px 52px;display:flex;flex-direction:column;justify-content:center;border-left:.5px solid rgba(20,20,20,.15)">'
      f'<div class="crumb">Feed / The Brand Index</div><div style="font:700 72px/1.02 var(--serif);letter-spacing:-.02em;margin:18px 0 14px">{H.escape(b["name"])}</div>'
      f'<div class="kick">{meta}</div><div style="font:19px/1.6 var(--serif);margin:22px 0 28px">{H.escape(b["line"])}</div>'
      f'<div style="display:flex;gap:10px;flex-wrap:wrap">{buttons(site,ig)}</div>'
      f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:34px;border-top:.5px solid rgba(20,20,20,.2)">'
      + ''.join(f'<div style="padding:14px 0"><div style="font:10px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.55">{k}</div><div style="font:17px var(--serif);margin-top:4px">{v}</div></div>' for k,v in since)+'</div></div></div>')
    rows=''.join(f'<a class="row"><img src="{b64(p["img"],500)}"><div><div class="m" style="margin-bottom:6px">{"Brand to Know" if p["profile"] else H.escape(p["cat"])}</div><div class="t">{H.escape(p["title"])}</div></div><div class="m">{fmt(p["date"])} &#8594;</div></a>' for p in ps)
    body=f'<div style="padding:48px 52px 56px"><div class="kick" style="margin-bottom:8px">On The Grassy Issue &middot; {len(ps)} stories</div><div class="h2" style="margin-bottom:18px">Every story featuring {H.escape(b["name"])}</div>{rows}</div>'
    return NAV+hero_html+body+FOOT
FEATIMG='/images/matchstick/life-1.jpg'
MS=dict(slug='matchstick-golf',site='https://matchstickgolf.com/',ig='matchstickgolf',meta='Portland, Oregon &middot; Ball markers &middot; Headcovers')
desc='How a former NBA writer lost his favorite ball marker, drew his own, and built a Portland brand on hand-painted $20 markers.'
pages=[
 ("Option A &middot; Full-bleed hero (revised)","Feature card under the heading is now a compact strip, about half the height, with a smaller title and a text link. A big photo across the full width with the name over it, then the brand line and a &ldquo;Find them&rdquo; box (website + Instagram). If we&rsquo;ve done a Brand to Know, it leads the stories as a green feature card, then every other story in a 3-up grid, newest first.",
  A(MS['slug'],'/images/matchstick/btk-hero.jpg',MS['site'],MS['ig'],desc,MS['meta'],'Since 2021')),
 ("Option A for a brand without a profile &middot; triptych hero","Most brands only have 4:5 product photos, not a wide shot. For those the hero becomes three photos side by side, so it still feels big without stretching one image. Here: B.O.T.H., which has 3 TGI stories and no Brand to Know yet.",
  Btri('bet-on-the-horses',['/images/hat-brands/band-both-1.jpg','/images/hat-brands/band-both-2.jpg','/images/hat-brands/band-both-3.jpg'],'https://betonthehorses.co/','betonthehorses','Los Angeles, CA &middot; Headwear &middot; Apparel','Since 2026')),
]
out=f'<!doctype html><meta charset="utf-8"><title>Brand page redesign &mdash; mockups</title><style>{CSS}</style>'
out+='<div class="lab" style="margin-top:28px;font-size:16px">Brand page redesign &mdash; mockups<span>Static previews at desktop width with real data. Buttons and cards are not clickable here. Socials need a new data file: today we only store the website for 120 of 180 brands and no Instagram handles; I&rsquo;d collect both before building.</span></div>'
for lab,note,html_ in pages:
    out+=f'<div class="lab">{lab}<span>{note}</span></div><div class="frame">{html_}</div>'
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/brand-page-mockups.html','w').write(out)
print(len(out)//1024,'KB')
