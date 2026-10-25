"""Golf & mental health Field Note frames (23 Oct 2026). Kit: brands' own product shots (Jones, Seamus) + reused new-drops frames
(Gumtree pouch, Malbon quarter-zip). Hero + bands: Lenny's own photos (~/Desktop/Golf Pics)."""
import shutil,json
exec(open('research/new-drops-oct23/frame.py').read().split('C={')[0])
R='research/golf-mental-health/raw/';O='images/golf-mental-health/'
def L(n): return Image.open(R+n).convert('RGB')
FR={}
def save(k,ims):
    FR[k]=[]
    for j,im in enumerate(ims,1):
        fn=f'p-{k}-{j}.jpg'; im.save(O+fn,quality=84,optimize=True); FR[k].append(fn)
save('k1',[frame(L('j1.img')),frame(L('j2.img')),cover(L('j3.img')),frame(L('j4.img'))])
save('k3',[frame(L('s1.img')),frame(L('s2.img'))])
save('k4',[frame(L('t1.img')),frame(L('t2.img'))])
for k,src in [('k2','g9'),('k5','m4')]:
    FR[k]=[]
    for j in range(1,5):
        fn=f'p-{k}-{j}.jpg'; shutil.copy(f'images/new-drops-oct23/p-{src}-{j}.jpg',O+fn); FR[k].append(fn)
json.dump(FR,open('research/golf-mental-health/frames.json','w'),indent=1)
H=Image.new('RGB',(2000,857)); H.paste(cover(L('walk.jpg'),2000,857,cy=.62),(0,0)); H.save(O+'hero.jpg',quality=86,optimize=True)
cover(L('walk.jpg'),1200,630,cy=.6).save(O+'og.jpg',quality=86)
cover(L('walk.jpg'),1000,1250,cx=.35).save(O+'card-hero.jpg',quality=86)
for n,cy in [('pond',.5),('duck',.5),('dunes',.5),('tee',.4),('cart',.5),('swing',.3)]:
    cover(L(n+'.jpg'),1200,1500,cy=cy).save(O+f'look-{n}.jpg',quality=84,optimize=True)
print('ok')
