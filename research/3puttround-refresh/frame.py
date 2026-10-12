"""Frames for the 3 Putt Round refresh. 12 October 2026. Brand's own product and lifestyle photos."""
import json,glob,numpy as np,sys
from PIL import Image
sys.path.insert(0,'.')
from destark import destark
R='research/3puttround-refresh/raw/'; O='images/3puttround-2026/'
W,H=1000,1250
def cover(im,py=.5,px=.5):
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=int((im2.width-W)*px); y=int((im2.height-H)*py); return im2.crop((x,y,x+W,y+H))
F=lambda h,i: f'{R}{h}-{i}.jpg'
LB='the-lost-balls-x-3-putt-round-'
SEL={
 "addiction":[F('set-of-3-golf-golf-addiction-tee-packs',2),F('set-of-3-golf-golf-addiction-tee-packs',1),F('the-gold-golf-addiction-tee-pack-collectable-carton',0),F('set-of-3-golf-golf-addiction-tee-packs',0)],
 "scented":[F('the-watermelon-scented-red-tee-pack',1),F('the-mint-scented-green-tee-pack',1),F('the-lemon-scented-yellow-tee-pack',1),F('the-club-champion',0),F('members-only',0)],
 "upperdecky":[F('3-upper-decky-tee-packs',1),F('3-upper-decky-tee-packs',0)],
 "matches":[F('set-of-4-golf-matches',1),F('set-of-4-golf-matches',0),F('the-lost-balls-x-vecchio-golf-tee-matches',1),F('the-lost-balls-x-vecchio-golf-tee-matches',0)],
 "teecase":[F('the-tee-case-iphone-17',2),F('the-tee-case-iphone-17',1),F('the-tee-case-iphone-17',0)],
 "vecchiotowel":[F('the-vecchio-x-lost-balls-golf-towel',1),F('the-vecchio-x-lost-balls-golf-towel',0),F('the-vecchio-x-lost-balls-golf-towel',2)],
 "morningtowel":[F('the-drive-to-survive-tour-towel-50cm-x-100cm-copy',1),F('the-drive-to-survive-tour-towel-50cm-x-100cm-copy',0)],
 "capgreen":[F(LB+'addicted-cap-green',1),F(LB+'addicted-cap-green',0),F(LB+'addicted-cap-green',2)],
 "captweed":[F(LB+'addicted-cap-tweed',1),F(LB+'addicted-cap-tweed',0),F(LB+'addicted-cap-tweed',2)],
 "capnot3putt":[F('the-i-will-not-3-putt-baseball-cap',1),F('the-i-will-not-3-putt-baseball-cap',0),F('the-i-will-not-3-putt-baseball-cap',2)],
 "capdangerous":[F('the-golf-is-dangerous-baseball-cap',1),F('the-golf-is-dangerous-baseball-cap',0),F('the-golf-is-dangerous-baseball-cap',3)],
 "caposlock":[F('the-its-golf-oclock-baseball-cap-copy',1),F('the-its-golf-oclock-baseball-cap-copy',0),F('the-its-golf-oclock-baseball-cap-copy',3)],
 "capcaddie":[F('the-whos-your-caddy-baseball-cap-1',1),F('the-whos-your-caddy-baseball-cap-1',0),F('the-whos-your-caddy-baseball-cap-1',4)],
 "knitpolo":[F(LB+'golf-shop-ls-tee',0),F(LB+'golf-shop-ls-tee',1),F(LB+'golf-shop-ls-tee',2),F(LB+'golf-shop-ls-tee',3)],
 "lstee":[F('the-its-just-another-addiction-knit-polo-green',0),F('the-its-just-another-addiction-knit-polo-green',1),F('the-its-just-another-addiction-knit-polo-green',2),F('the-its-just-another-addiction-knit-polo-green',3)],
 "morningtee":[F('the-morning-thruth-t-shirt-c',0),F('the-morning-thruth-t-shirt-c',3),F('the-morning-thruth-t-shirt-c',2),F('the-morning-thruth-t-shirt-c',1)],
 "sundaytee":[F('unisex-organic-cotton-t-shirt',0),F('unisex-organic-cotton-t-shirt',1)],
 "buggytee":[F('the-golf-buggy-t-shirt',0),F('the-golf-buggy-t-shirt',2),F('the-golf-buggy-t-shirt',1),F('the-golf-buggy-t-shirt',3)],
}
fr={}
for k,lst in SEL.items():
    fr[k]=[]
    for n,f in enumerate(lst,1):
        p=f'{O}{k}-{n}.jpg'; cover(Image.open(f).convert('RGB'),.45).save(p,quality=86); destark(p,min_white=0.25); fr[k].append('/'+p)
json.dump(fr,open('research/3puttround-refresh/frames.json','w'),indent=1)
def lp(f,w,h,py=.5,px=.5):
    im=Image.open(f).convert('RGB'); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*px); y=int((im.height-h)*py); return im.crop((x,y,x+w,y+h))
# single-image hero (Lenny, 12 Oct): the brand's scented-tee-pack banner
for (W2,H2,name) in [(2000,857,'hero.jpg'),(1200,630,'og.jpg')]:
    lp(R+'banner-scented.jpg',W2,H2,.5,.5).save(O+name,quality=90)
for n,(f,py) in enumerate([(F('3-upper-decky-tee-packs',2),.5),(F('the-golf-is-social-baseball-cap',1),.5),(F('the-foreee-right-baseball-cap',1),.5)],1):
    cover(Image.open(f).convert('RGB'),py).save(f'{O}band-{n}.jpg',quality=86)
print(sum(map(len,fr.values())))
