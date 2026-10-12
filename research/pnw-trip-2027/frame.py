"""Frames for the PNW 2027 field note. 12 October 2026. All photos are each course's / venue's own (Gamble Sands, Chambers Bay,
The Home Course, Gold Mountain, OGA for Wildwood, USFS for Multnomah Falls, restaurants' own sites)."""
import json,numpy as np
from PIL import Image, ImageFilter
R='research/pnw-trip-2027/raw/'; O='images/pnw-trip-2027/'
W,H=1000,1250
def cover(im,py=.5,px=.5):
    s=max(W/im.width,H/im.height); im2=im.resize((max(W,round(im.width*s)),max(H,round(im.height*s))),Image.LANCZOS)
    x=int((im2.width-W)*px); y=int((im2.height-H)*py); return im2.crop((x,y,x+W,y+H))
def blurfill(im):
    bg=cover(im).filter(ImageFilter.GaussianBlur(40)); bg=Image.blend(bg,Image.new('RGB',bg.size,(24,40,23)),.35)
    s=W/im.width; fg=im.resize((W,round(im.height*s)),Image.LANCZOS); bg.paste(fg,(0,(H-fg.height)//2)); return bg
SEL={
 "inn":[("The-Inn-Panorama-River-View-scaled-2.jpg",'c',.5,.5),("AJB9374-HDR-scaled.jpg",'c',.5,.5),("94A3353-1-scaled.jpg",'c',.5,.5),("The-Inn-2-scaled.jpg",'c',.5,.5)],
 "quicksands":[("Quicksands-scaled.jpg",'c',.5,.5),("quicksands.jpeg",'c',.5,.5),("Flags-QuickSands-Hole-1-scaled.jpg",'c',.5,.5)],
 "cascades":[("Cascade-scaled.jpg",'c',.5,.5),("cascade.jpeg",'c',.5,.6)],
 "barn":[("BUNCH-DJI_0177-Enhanced-NR-Edit-scaled.jpeg",'c',.5,.45),("GAMBLE-SANDS-FOOD-_OAR0190-Enhanced-NR-scaled.jpg",'c',.5,.5),("GAMBLE-SANDS-FOOD-_OAR0283-Enhanced-NR-scaled.jpg",'c',.5,.5),("DSC03826.webp",'c',.5,.5)],
 "sands":[("Gamble-2024-Marsh-Sands-Course-70-scaled.jpg",'c',.5,.5),("Gamble-2024-Marsh-Sands-Course-72-scaled.jpg",'c',.5,.5),("Copy-of-DJI_20240907100213_0979_D-scaled.jpg",'c',.5,.5),("Copy-of-DJI_20240907101256_0993_D-scaled.jpg",'c',.5,.5)],
 "scarecrow":[("1-view-SCARECROW-DJI_20250501203336_0105_D-NR-Pano-OAR-scaled.jpg",'c',.5,.6),("11-viewSCARECROW-DJI_20250430071628_0262_D-Enhanced-NR-OAR-2-scaled.jpg",'c',.5,.5),("GambleSands-Scarecrow-10Green-DarinBunch-scaled.jpg",'c',.5,.5),("2-view-SCARECROW-DJI_20250430081042_0447_D-Enhanced-NR-OAR-scaled.jpeg",'c',.5,.5)],
 "dannyboy":[("GAMBLE-SANDS-FOOD-_OAR0252-Enhanced-NR-scaled.jpg",'c',.5,.5),("GAMBLE-SANDS-FOOD-_OAR0299-Enhanced-NR-scaled.jpg",'c',.5,.5),("GAMBLE-SANDS-FOOD-_OAR0210-Enhanced-NR-scaled.jpg",'c',.5,.5),("Gamble-2021-Marsh-114-scaled.jpg",'c',.5,.5)],
 "tsillan":[("tsillan__cc80fe8b.jpg",'c',.5,.5),("tsillan__281e489c.jpg",'c',.5,.5)],
 "munchen":[("munchen__8fadd1d5.jpg",'c',.5,.5)],
 "homecourse":[("home-thc-scenic-slider.jpg",'b',0,0),("home-slideshow12b.jpg",'b',0,0)],
 "copper":[("copper-bar.jpg",'c',.5,.5),("copper-kitchen.jpg",'c',.5,.5)],
 "chambers":[("chambers__2277ccd3.jpg",'c',.5,.6),("chambers__61489c05.jpg",'c',.5,.5),("chambers-golf__1ee6cd52.jpg",'c',.5,.5),("chambers__c9af5e6b.jpg",'c',.5,.5),("chambers__2e381d4e.jpg",'c',.5,.5)],
 "gold":[("gold-sig.jpg",'c',.5,.5),("gold-DSC3219-Edit-1.jpg",'c',.5,.5),("gold-Cascade1-1.jpg",'c',.5,.5)],
 "tides":[("tides-dock.jpg",'c',.5,.5),("tides-rainier.jpg",'b',0,0)],
 "pinestate":[("pine-1.jpg",'c',.5,.5),("pine-alberta.jpg",'c',.5,.5),("pine-2.jpg",'c',.5,.5)],
 "wildwood":[("wildwood.png",'b',0,0)],
 "lepigeon":[("lepigeon__5a592d74.jpg",'c',.5,.5),("lepigeon__58a8b522.jpg",'c',.5,.5),("lepigeon__73175ecf.jpg",'c',.5,.5),("lepigeon__370554e6.jpg",'c',.5,.5)],
 "multnomah":[("multnomah.jpg",'b',0,0)],
}
fr={}
for k,lst in SEL.items():
    fr[k]=[]
    for n,(f,m,py,px) in enumerate(lst,1):
        im=Image.open(R+f).convert('RGB'); out=(cover(im,py,px) if m=='c' else blurfill(im))
        p=f'{O}{k}-{n}.jpg'; out.save(p,quality=86); fr[k].append('/'+p)
json.dump(fr,open('research/pnw-trip-2027/frames.json','w'),indent=1)
def wide(f,Wd,Hd,py=.5):
    im=Image.open(R+f).convert('RGB'); s=max(Wd/im.width,Hd/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-Wd)//2; y=int((im.height-Hd)*py); return im.crop((x,y,x+Wd,y+Hd))
wide('Gamble-Alex-6-scaled.jpg',2000,857,.55).save(O+'hero.jpg',quality=88)
wide('Gamble-Alex-6-scaled.jpg',1200,630,.55).save(O+'og.jpg',quality=88)
# bands
for n,(f,py,px) in enumerate([('10-view-SCARECROW-DJI_20250429204742_0709_D-NR-OAR-scaled.jpeg',.5,.5),('Copy-of-DJI_20240907101148_0991_D-scaled.jpg',.5,.5),('Inn-RiverView-HZ-Drone-Oar-CascadesViewFromScarecrow-scaled.jpg',.5,.5),
   ('chambers__057522ee.jpg',.5,.6),('chambers-golf__2e63125a.jpg',.5,.5),('chambers__54d9b6d7.jpg',.5,.5)],1):
    cover(Image.open(R+f).convert('RGB'),py,px).save(f'{O}band-{n}.jpg',quality=86)
cover(Image.open(R+'Gamble-2024-Marsh-Sands-Course-70-scaled.jpg').convert('RGB')).save(O+'card.jpg',quality=86)
print(sum(map(len,fr.values())))
