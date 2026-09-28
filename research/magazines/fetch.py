import os,json,io
os.environ['LD_LIBRARY_PATH']='/tmp/libs/root/usr/lib/aarch64-linux-gnu'
from playwright.sync_api import sync_playwright
from PIL import Image
dg=json.load(open('research/magazines/depeche-products.json'))['products']
D={p['handle']:[i['src'] for i in p['images']] for p in dg}
S='https://cdn.shopify.com/s/files/1/0501/4277/3404/files/'
W='https://static.wixstatic.com/media/'
U={
 'depeche':[D['depeche-golf-issue-5'][0]]+D['depeche-golf-issue-5'][1:6]+[D['depeche-golf-issue-4'][0]]+D['depeche-golf-issue-4'][1:5],
 'hiatus':['https://cdn.shopify.com/s/files/1/0909/3890/0845/files/hiatus_no2_magazine-C1.png?v=1778866695','https://cdn.shopify.com/s/files/1/0909/3890/0845/files/hiatus_no2_magazine-C4.png?v=1778866701','https://cdn.shopify.com/s/files/1/0909/3890/0845/files/hiatus_Magazine-C1.png?v=1758336620','https://cdn.shopify.com/s/files/1/0909/3890/0845/files/hiatus_Magazine-C4.png?v=1758336620','https://cdn.prod.website-files.com/666b6380177c95bb63260f25/68d0764decf408940f3e775f_HiatusGolf_creditClaraLacasse-13.jpg','https://cdn.prod.website-files.com/666b6380177c95bb63260f25/6a26e4e8e3da22a9d6f74b48_Hiatus_V2_creditClaraLacasse-12.jpg'],
 'loop':['https://cdn.shopify.com/s/files/1/0957/8538/6310/files/Untitled-2.png?v=1784536966','https://cdn.shopify.com/s/files/1/0957/8538/6310/files/Journal-cover.png?v=1770294185','https://theloopgc.com/wp-content/uploads/2026/02/journal-banner.jpg','https://theloopgc.com/wp-content/uploads/2026/02/download.jpeg'],
 'gq':[W+'d8e5d6_ede2f3b910814995bf8c78805d1ff0d2~mv2.jpg',W+'d8e5d6_5540ab32742745848a4a88c089699dd3~mv2.jpg',W+'d8e5d6_0cd092037d63449f94836eeb613f45e9~mv2.jpg',W+'d8e5d6_0ccf1026057c415980aab54118a532d8~mv2.jpg'],
 'aagd':['https://africanamericangolfersdigest.com/wp-content/uploads/2026/05/Cover_Summer-2026_Emily-Odwin.png','https://africanamericangolfersdigest.com/wp-content/uploads/2026/03/Spring-2026_Cover_Triple-Nickles.png','https://africanamericangolfersdigest.com/wp-content/uploads/2026/07/Cover_Gladys-Lee_July-2026.png'],
 'sagca':['https://sagca.com.au/wp-content/uploads/SAGCA-Magazine-Cover-2025.jpg','https://sagca.com.au/wp-content/uploads/Issue-No.25.jpg','https://sagca.com.au/wp-content/uploads/Cover-Image-1.jpg'],
 'lftr':[S+'Volume2Cover.jpg?v=1743501673',S+'LFTR_Volume_2_Royal_Lytham_St_Annes_Mock-up_copy_1.png?v=1743502132',S+'LFTR_Volume_2_Silloth-on-Solway_Mock-up_copy_1.png?v=1743502132',S+'LFTR_Cover_Main_Image.jpg?v=1732094125',S+'LFTR_Volume_1_Royal_Liverpool_Mock-up_1.png?v=1731347810',S+'LFTR_Volume_1_What_Makes_a_Links_Mock-up_2.png?v=1731347810'],
 'manors':['https://cdn.shopify.com/s/files/1/0713/1693/0869/files/Manors_Scrambler_Magazine_Mockup_Bleed.jpg?v=1790243204','https://cdn.shopify.com/s/files/1/0713/1693/0869/collections/ManorsZineDigis-7930.jpg?v=1788762698'],
}
log={}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(user_agent='Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36')
    for k,urls in U.items():
        log[k]=[]
        for j,u in enumerate(urls,1):
            try:
                r=ctx.request.get(u,timeout=40000); im=Image.open(io.BytesIO(r.body()))
                if im.mode in('RGBA','LA','P'):
                    im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(244,241,234)); bg.paste(im,mask=im.split()[3]); im=bg
                im=im.convert('RGB'); im.thumbnail((2400,2400))
                f=f'research/magazines/img/{k}-{j}.jpg'; im.save(f,quality=88)
                log[k].append({'file':f,'src':u,'w':im.width,'h':im.height})
            except Exception as e:
                log[k].append({'src':u,'err':str(e)[:80]})
    b.close()
json.dump(log,open('research/magazines/img/log.json','w'),indent=1)
for k,v in log.items(): print(k,[(x.get('w'),x.get('h')) if 'w' in x else x['err'] for x in v])
