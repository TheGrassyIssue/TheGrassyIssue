"""Quiet luxury post (12 brands, single Late Nine hero, 28 Oct 2026): lifestyle bands (3 per brand) and hero, from each brand's own photos already on the site. 26 Oct 2026."""
from PIL import Image
O='images/quiet-luxury/'
def cover(f,W,H,fx=.5,fy=.5):
    im=Image.open(f).convert('RGB'); s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
B={
 'ln':[('research/late-nine/originals/newsletter.orig.jpg',.5,.3),('research/late-nine/originals/fw26-lookbook.orig.jpg',.5,.4),('images/quiet-luxury/ln5-2.jpg',.5,.5)],
 'al':[('images/alba-golf/lb-0.jpg',.3,.5),('images/alba-golf/lb-4.jpg',.5,.5),('images/alba-golf/lb-5.jpg',.5,.5)],
 'wh':[('images/whim-golf/about-founders.jpg',.5,.3),('images/whim-golf/about-michigan.jpg',.5,.5),('research/whim/raw/IMG_7444.jpg',.5,.5)],
 'rk':[('images/rookline/band-7.jpg',.5,.5),('images/rookline/band-5.jpg',.5,.5),('images/rookline/band-6.jpg',.5,.5)],
 'mc':[('images/macade/band-a1.jpg',.5,.4),('images/macade/band-b2.jpg',.5,.4),('images/macade/band-c1.jpg',.5,.4)],
 'wg':[('images/woodgrain/band-1.jpg',.5,.4),('images/woodgrain/band-3.jpg',.5,.4),('images/woodgrain/band-5.jpg',.5,.4)],
 'sp':[('images/shapland/rye-4-group.jpg',.5,.5),('images/shapland/rye-4-collar.jpg',.5,.5),('images/shapland/kantle-31-a.jpg',.5,.5)],
 'mk':[('images/mackenzie/life-dunes-15.jpg',.5,.5),('images/mackenzie/life-elie-33.jpg',.5,.5),('images/mackenzie/life-affric-fairway.jpg',.5,.5)],
 'qg':[('images/quiet-golf-2026/band-2.jpg',.5,.5),('images/quiet-golf-2026/band-5.jpg',.6,.5),('images/quiet-golf-2026/band-9.jpg',.5,.5)],
 'lr':[('images/local-rule/life-collegekids-1.jpg',.5,.4),('images/local-rule/life-pompom-course.jpg',.5,.5),('images/local-rule/life-cotton-cap-course.jpg',.5,.5)],
 'sd':[('images/sounder/life-trevose.jpg',.5,.5),('images/sounder/life-spain.jpg',.5,.5),('images/sounder/life-first-tee.jpg',.5,.5)],
 'cs':[('images/casualist/band-coast.jpg',.5,.5),('images/casualist/band-links.jpg',.5,.5),('images/casualist/btk-hero-2026.jpg',.5,.5)],
}
for k,items in B.items():
    for n,(f,fx,fy) in enumerate(items): cover(f,1000,1250,fx,fy).save(f'{O}band-{k}-{n}.jpg',quality=84,optimize=True)
W,H=2000,857
hero=cover('research/late-nine/originals/newsletter.orig.jpg',W,H,.5,.3)
hero.save(O+'hero.jpg',quality=84,optimize=True)
cover(O+'hero.jpg',1200,630).save(O+'og.jpg',quality=84)
cover('research/late-nine/originals/newsletter.orig.jpg',1000,1250,.5,.3).save(O+'card-hero.jpg',quality=84,optimize=True)
print('ok')
