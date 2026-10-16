"""Pull wide lifestyle candidates from each brand's own homepage (og:image + top-of-page banners)."""
import json,re,os,io,urllib.request,urllib.parse,concurrent.futures as cf,html as H
from PIL import Image
C=json.load(open('research/brand-page-redesign/hero-cands.json'))
S=json.load(open('data/brand-socials.json'))
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
def get(u,n=3000000):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25); return r.read(n),r.geturl()
def cands(slug):
    site=(S.get(slug) or {}).get('website')
    if not site: return slug,[]
    try: raw,final=get(site); h=raw.decode('utf-8','ignore')
    except Exception as e: return slug,[]
    urls=[]
    for m in re.finditer(r'<meta[^>]+(?:property|name)="(?:og:image|twitter:image)(?::secure_url)?"[^>]+content="([^"]+)"',h): urls.append(m.group(1))
    for m in re.finditer(r'<meta[^>]+content="([^"]+)"[^>]+(?:property|name)="og:image"',h): urls.append(m.group(1))
    top=h[:int(len(h)*.45)]
    for m in re.finditer(r'(?:src|srcset|data-src|data-srcset)="([^"]+)"',top):
        for part in m.group(1).split(','):
            u=part.strip().split(' ')[0]
            if re.search(r'\.(jpe?g|png|webp)',u,re.I) and re.search(r'cdn/shop/files|cdn\.shopify\.com/s/files|squarespace-cdn|wixstatic|images\.ctfassets|cloudfront',u) and not re.search(r'logo|icon|favicon|badge|payment|flag',u,re.I):
                urls.append(u)
    seen=[];out=[]
    for u in urls:
        u=H.unescape(u)
        if u.startswith('//'): u='https:'+u
        elif u.startswith('/'): u=urllib.parse.urljoin(final,u)
        base=re.sub(r'([?&])(width|w|height|h|crop)=[^&]*','',re.sub(r'_(\d+x\d*|\d*x\d+)(?=\.\w+(\?|$))','',u)).rstrip('?&')
        key=base.split('?')[0]
        if key in seen: continue
        seen.append(key)
        if len(seen)>10: break
        sep='&' if '?' in base else '?'
        tryu=base+(sep+'width=2400' if ('shopify' in base or '/cdn/shop/' in base) else '')
        try:
            b,_=get(tryu,20000000); im=Image.open(io.BytesIO(b)); w,hh=im.size
        except Exception: continue
        if w>=1500 and w/hh>=1.3:
            fn=f'research/brand-page-redesign/web/{slug}-{len(out)+1}.jpg'
            im.convert('RGB').save(fn,quality=90); out.append(dict(src=tryu,file=fn,size=[w,hh]))
        if len(out)>=3: break
    return slug,out
todo=[k for k,v in C.items() if (S.get(k) or {}).get('website')]
res={}
with cf.ThreadPoolExecutor(10) as ex:
    for slug,out in ex.map(cands,todo): res[slug]=out
json.dump(res,open('research/brand-page-redesign/web-cands.json','w'),indent=1)
print(len(todo),'checked;',sum(1 for v in res.values() if v),'with wide web candidates;',sum(len(v) for v in res.values()),'images')
