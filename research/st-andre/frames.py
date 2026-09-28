import json,io,os
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from PIL import Image,ImageOps
from playwright.sync_api import sync_playwright
R='research/st-andre/'; OUT='images/st-andre/'
c={x['handle']:x for x in json.load(open(R+'catalog.json'))['items']}
irl=json.load(open(R+'irl/log.json'))
# handle -> list of ('irl',idx) or ('p',imgindex)
PLAN={
 'pspsps-jacquard-towel':[('irl',22),('irl',24),('p',0),('p',1),('p',2)],
 'palm-x-st-andre-glove':[('irl',3),('irl',20),('p',0),('p',1)],
 'st-andre-classic-driver-cover':[('irl',36),('irl',44),('irl',47),('p',0),('p',2)],
 'st-andre-classic-blade-putter-cover':[('irl',39),('irl',29),('p',0),('p',1)],
 'st-andre-classic-ball-marker':[('irl',46),('irl',37),('p',0),('p',1)],
 'classy-lettermark-socks':[('irl',8),('p',0),('p',2)],
 'launched-crewneck-sweatshirt':[('irl',12),('p',0),('p',2)],
 'patch-performance-hat-white-black':[('p',3),('p',0),('p',1),('p',2),('p',5)],
 'puff-mid-crown-cotton-hat':[('p',0),('p',1),('p',2),('p',4)],
 'wordmark-trucker-hat':[('p',0)],
 'meow-tee':[('p',0),('p',2),('p',1),('p',3)],
 'mermaid-tee':[('p',0),('p',2),('p',1),('p',3)],
}
def edge_uniform(im):
    g=im.convert('L'); w,h=g.size
    px=[g.getpixel((x,y)) for x in range(0,w,max(1,w//40)) for y in (0,h-1)]+[g.getpixel((x,y)) for y in range(0,h,max(1,h//40)) for x in (0,w-1)]
    return max(px)-min(px)<18
def frame(im,cent=(.5,.5)):
    im=im.convert('RGB')
    if edge_uniform(im):
        bg=im.getpixel((2,2)); im2=im.copy(); im2.thumbnail((920,1150),Image.LANCZOS)
        cv=Image.new('RGB',(1000,1250),bg); cv.paste(im2,((1000-im2.width)//2,(1250-im2.height)//2)); return cv
    return ImageOps.fit(im,(1000,1250),Image.LANCZOS,centering=cent)
fr={}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context()
    for h,plan in PLAN.items():
        fr[h]=[]
        for j,(k,i) in enumerate(plan,1):
            if k=='irl':
                im=Image.open(R+'irl/'+irl[i]['file']); src=irl[i]['src']
            else:
                src=c[h]['imgs'][i].split('?')[0]+'?width=1600'
                im=Image.open(io.BytesIO(ctx.request.get(src).body()))
            local=f'{OUT}{h}-{j}.jpg'; frame(im).save(local,quality=84,optimize=True,progressive=True)
            fr[h].append({'local':'/'+local,'src':src})
    b.close()
json.dump(fr,open(R+'frames.json','w'),indent=1)
# bands
BANDS={'band-a1':5,'band-a2':45,'band-a3':49,'band-b1':32,'band-b2':38,'band-b3':28,'band-c1':11,'band-c2':9,'band-c3':40}
for k,i in BANDS.items():
    im=Image.open(R+'irl/'+irl[i]['file']).convert('RGB')
    ImageOps.fit(im,(900,1125),Image.LANCZOS,centering=(.5,.4)).save(f'{OUT}{k}.jpg',quality=82,optimize=True,progressive=True)
print({h:len(v) for h,v in fr.items()})
