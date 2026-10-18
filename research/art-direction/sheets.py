import json,glob,io,os,sys,urllib.request,concurrent.futures as cf
from PIL import Image,ImageDraw
UA={'User-Agent':'Mozilla/5.0'}
def sized(u,w): return u+('?width=%d'%w if ('cdn/shop' in u) else '?format=%dw'%w)
def th(r):
    f=f"thumbs/{r['s']}-{r['i']:03d}.jpg"
    if not os.path.exists(f):
        try:
            im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(sized(r['u'],300),headers=UA),timeout=30).read())).convert('RGB'); im.thumbnail((180,225)); im.save(f,quality=75)
        except Exception: return None
    return f
os.makedirs('thumbs',exist_ok=True)
for b in sys.argv[1:]:
    R=[r for r in json.load(open(f'harvest-{b}.json')) if r['light'] is False][:60]
    with cf.ThreadPoolExecutor(8) as ex: fs=list(ex.map(th,R))
    cols=12;tw,tht=160,215;rows=(len(R)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*tht+20),'white');d=ImageDraw.Draw(S);d.text((4,4),b,fill='black')
    for k,(r,f) in enumerate(zip(R,fs)):
        x,y=(k%cols)*tw,20+(k//cols)*tht
        if f: S.paste(Image.open(f),(x,y))
        d.text((x+2,y+tht-14),f"{r['i']} {r['k'][0]} {r['size'][0] if r['size'] else ''}",fill='red')
    S.save(f'/sessions/admiring-pensive-ritchie/mnt/outputs/ad-{b}.jpg',quality=72)
