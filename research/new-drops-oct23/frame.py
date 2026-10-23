"""New drops Oct 23 2026 frames: Malbon x Grateful Dead (Long Vacation), Gumtree x Wynn, Mogshade Re.Weave autumn.
Brand-own images only (malbon.com, gumtreegolfandnature.com, mogshadegolf.com product pages). p=flat on stone, c=cover crop."""
import numpy as np,json,glob,os,sys
from PIL import Image,ImageDraw
R='research/new-drops-oct23/raw/';O='images/new-drops-oct23/';W,H=1000,1250;STONE=np.array([232,226,214.])
def src(n):
    d={'m':'m/','g':'g/','s':'s/'}[n[0]]; f=glob.glob(R+d+n+'.*'); return Image.open(f[0]).convert('RGB')
def cover(im,W=W,H=H,cx=.5,cy=.5):
    s=max(W/im.width,H/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-W)*cx);y=int((im.height-H)*cy); return im.crop((x,y,x+W,y+H))
def frame(im,th=14,fill=(.80,.72)):
    im.thumbnail((1400,1400)); a=np.asarray(im).astype(float)
    ref=a[2,2]
    mk=Image.fromarray(((np.abs(a-ref).max(axis=2)<th)*255).astype('uint8')).copy()
    for pt in [(0,0),(mk.width-1,0),(0,mk.height-1),(mk.width-1,mk.height-1)]: ImageDraw.floodfill(mk,pt,128)
    bg=np.array(mk)==128; out=a.copy(); out[bg]=STONE
    ys,xs=np.where(~bg)
    if len(xs)==0: return cover(im)
    x0,x1=xs.min(),xs.max(); y0,y1=ys.min(),ys.max()
    g=Image.fromarray(out.clip(0,255).astype('uint8')).crop((x0,y0,x1+1,y1+1)); s=min(W*fill[0]/g.width,H*fill[1]/g.height); g=g.resize((round(g.width*s),round(g.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H),tuple(int(v) for v in STONE)); c.paste(g,((W-g.width)//2,(H-g.height)//2)); return c
C={
 'm1':['pm1-1','cm1-2','cm1-3','cm1-8'], 'm2':['pm6-1','cm6-2','cm6-4','cm6-5','cm6-8'],
 'm3':['pm8-1','cm8-2','pm9-1','cm9-2','cm8-6'], 'm4':['pm11-1','cm11-2','cm11-3','cm11-6'],
 'm5':['pm12-1','cm12-2','cm12-5','cm12-3'], 'm6':['cm15-1','cm15-2','pm16-1','cm16-4'],
 'm7':['pm13-1','cm13-2','pm14-1','cm13-6'], 'm8':['pm17-1','pm18-1','cm17-5','cm18-2'],
 'm9':['pm2-1','pm3-1','pm2-3'], 'm10':['pm4-1','pm4-2'], 'm11':['pm5-1','cm5-2','cm5-3','pm5-7','cm5-9'],
 'm12':['pm7-2','pm7-1'], 'm13':['pm10-1','pm10-2'],
 'g1':['cg1-1','cg1-2','cg1-3','cg1-4'],'g2':['cg2-1','cg2-2','cg2-3'],'g3':['cg3-1','cg3-2'],
 'g4':['cg4-1','cg4-2','cg4-4','cg4-3'],'g5':['cg5-1','cg5-2'],'g6':['cg6-1','cg6-3','cg6-4','cg6-5'],
 'g7':['cg7-1','cg7-7','cg7-2','cg7-4'],'g8':['cg8-1','cg8-2','cg8-3'],'g9':['cg9-1','cg9-2','cg9-3','cg9-4'],'g10':['cg10-1','cg10-4'],
}
for i in [1,2,3,4,5,7,8,9,10,11,12,13,14,15]: C[f's{i}']=[f'cs{i}-1']
only=sys.argv[1:]
FR=json.load(open('research/new-drops-oct23/frames.json')) if os.path.exists('research/new-drops-oct23/frames.json') else {}
for k,items in C.items():
    if only and k not in only: continue
    FR[k]=[]
    for j,it in enumerate(items,1):
        t,n=it[0],it[1:]; im=src(n)
        out=frame(im) if t=='p' else cover(im,cy=.4 if n[0]=='m' else .5)
        fn=f'p-{k}-{j}.jpg'; out.save(O+fn,quality=84,optimize=True); FR[k].append(fn)
json.dump(FR,open('research/new-drops-oct23/frames.json','w'),indent=1)
# lifestyle + hero
if not only:
    L=[('g4-4',.5),('g7-2',.5),('g4-2',.4),('g9-2',.5),('m8-2',.3),('m9-2',.3),('m11-2',.3),('m6-2',.3),('s1-1',.5),('s5-1',.5),('s14-1',.5)]
    for k,(n,cy) in enumerate(L,1): cover(src(n),1200,1500,cy=cy).save(f'{O}look-{k}.jpg',quality=84,optimize=True)
    tri=[('m8-2',.25),('g4-4',.5),('s1-1',.5)]
    hero=Image.new('RGB',(2000,857),(20,20,20)); x=0
    for n,cy in tri: hero.paste(cover(src(n),666,857,cy=cy),(x,0)); x+=667
    hero.save(O+'hero.jpg',quality=86,optimize=True)
    og=Image.new('RGB',(1200,630)); x=0
    for n,cy in tri: og.paste(cover(src(n),400,630,cy=cy),(x,0)); x+=400
    og.save(O+'og.jpg',quality=86)
    cover(src('g4-4'),1000,1250).save(O+'card-hero.jpg',quality=86)
print('ok',len(FR))
