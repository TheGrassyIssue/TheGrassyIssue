#!/usr/bin/env python3
"""sweep-swap.py — resumable catalogue sweep for the Hat & Towel Edit swaps.
RESUMABLE AND INCREMENTAL because the first attempt lost everything: the bash
call was killed at ~178s and state was only written at the end. It also used a
0.4s delay, which 429'd 187 of 220 stores and silently returned a pool missing
Huega House, Students, Odd Ritual and ~180 others.
A 429 is NOT marked done — it is left for the next pass to retry."""
import json, urllib.request, time, re, pathlib, sys
from urllib.parse import urlparse
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
ROOT=pathlib.Path(__file__).resolve().parent
IN={"sinking-birdies","rebolf","devereux-golf","hidden-links-society","morning-people-clothiers",
"apres-golf","3-putt-round","random-golf-club","kingfisher-golf","bluegrass-fairway","sunday-golf",
"bettinardi","sugarloaf-social-club","stitch-golf","eastside-golf","read-the-green","merrill-golf",
"public-drip","forden-golf","rouqe-golf","sierra-madre","dormie-workshop","ghost-golf",
"jones-sports-co","sentinel-golf","malbon","radry-golf","seamus","hiroki-golf","puma-golf"}
doms=json.load(open(ROOT/"research/brand-domains.json"))
brands=json.load(open(ROOT/"data/brands.json"))
d2b={urlparse(b.get("url") or "").netloc.replace("www.",""):b["slug"] for b in brands if b.get("url")}
st=ROOT/"research/hats/swap-sweep.json"
S=json.loads(st.read_text()) if st.exists() else {"done":[],"buckets":[],"towels":[],"dead":[]}
done,dead=set(S["done"]),set(S["dead"])
def save(): S["done"],S["dead"]=sorted(done),sorted(dead); st.write_text(json.dumps(S,indent=1))
todo=[h for h in doms if h not in done and h not in dead and d2b.get(h.replace("www.","")) not in IN]
budget=float(sys.argv[1]) if len(sys.argv)>1 else 130
t0=time.time(); n=hit429=0
for h in todo:
    if time.time()-t0>budget: break
    slug=d2b.get(h.replace("www.",""), h.split(".")[0])
    try:
        j=json.loads(urllib.request.urlopen(urllib.request.Request(
            f"https://{h}/products.json?limit=250",headers=UA),timeout=12).read())
    except urllib.error.HTTPError as e:
        if e.code==429: hit429+=1; time.sleep(1.5); continue   # retry next pass
        dead.add(h); save(); time.sleep(0.8); continue
    except Exception:
        dead.add(h); save(); time.sleep(0.8); continue
    for p in j.get("products",[]):
        t=p["title"]; tl=t.lower(); vs=p.get("variants") or []
        if not any(v.get("available") for v in vs): continue
        pr=min(float(v["price"]) for v in vs)
        imgs=[i["src"] for i in (p.get("images") or [])]
        if not imgs: continue
        rec=dict(brand=slug,host=h,title=t,price=pr,cur=j.get("products") and None,
                 url=f"https://{h}/products/{p['handle']}",img=imgs[0],n_img=len(imgs))
        if "bucket" in tl and not re.search(r"beanie|visor|headcover|cover|towel|tee\b|sock|bag",tl):
            S["buckets"].append(rec)
        if "towel" in tl and not re.search(r"beanie|visor|paper|holder|putter",tl):
            S["towels"].append(rec)
    done.add(h); n+=1; save(); time.sleep(1.0)
rem=len([h for h in doms if h not in done and h not in dead and d2b.get(h.replace("www.","")) not in IN])
print(f"  +{n} swept · 429 deferred {hit429} · done {len(done)} · no-store {len(dead)} · remaining {rem}")
print(f"  pool: {len(S['buckets'])} buckets · {len(S['towels'])} towels")
