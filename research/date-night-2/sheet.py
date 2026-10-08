import json,urllib.request,io,base64,os
from PIL import Image
C=json.load(open('c.json')); cards=[]
for i,c in enumerate(C,1):
  b64=''; f=f'raw/{i:02d}-0.jpg'
  if c[6]:
    if not os.path.exists(f):
      u=c[6]+('?format=1500w' if 'squarespace' in c[6] else '')
      try:
        d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
        Image.open(io.BytesIO(d)).convert('RGB').save(f,quality=90)
      except Exception as e: print('fail',c[0],e)
    if os.path.exists(f):
      t=Image.open(f); t.thumbnail((640,480)); bf=io.BytesIO(); t.save(bf,'JPEG',quality=78); b64=base64.b64encode(bf.getvalue()).decode()
  cards.append((i,c,b64))
css="body{font-family:Georgia,serif;background:#f2eee6;color:#1e2a1c;margin:0;padding:32px}h1{font-size:30px;margin:0 0 6px}p.s{font:13px/1.5 ui-monospace,monospace;opacity:.7;margin:0 0 24px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}.c{background:#fff;border:1px solid #d8d0c0}.c img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#ddd}.b{padding:12px 14px}.n{font-size:19px;font-weight:bold}.m{font:11px ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;opacity:.65;margin:4px 0 8px}.w{font-size:14px;line-height:1.45}.o{font-size:13px;margin-top:6px}.f{font:11px ui-monospace,monospace;color:#9a3b1c;margin-top:6px}.num{display:inline-block;background:#2d4a2b;color:#fff;font:12px ui-monospace,monospace;padding:2px 7px;margin-right:6px}"
h=f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Date Night Vol. 2 options</title><style>{css}</style></head><body><h1>Date Night Vol. 2: Restaurants for Reconnecting</h1><p class='s'>23 options, none from Vol. 1. Each was checked as open on 8 Oct 2026; the 2026 Michelin Texas list came out today. Fish Shop is locked in. Pick by number.</p><div class='g'>"
for i,c,b in cards:
  img=f"<img src='data:image/jpeg;base64,{b}'>" if b else "<img alt=''>"
  flag=f"<div class='f'>⚑ {c[7]}</div>" if c[7] else ""
  h+=f"<div class='c'>{img}<div class='b'><div class='n'><span class='num'>{i}</span>{c[0]}</div><div class='m'>{c[1]} · {c[2]}</div><div class='w'>{c[3]}</div><div class='o'><b>Order:</b> {c[4]}</div><div class='o'><b>Book:</b> {c[5]}</div>{flag}</div></div>"
h+="</div></body></html>"
open('/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/date-night-2-options.html','w').write(h)
print('ok')
