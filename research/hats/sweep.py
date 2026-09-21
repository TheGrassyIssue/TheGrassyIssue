import json, urllib.request, re, time, sys, os
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
R="research/hats/"
stores=json.load(open("data/brand-stores.json"))["stores"]
res=json.load(open(R+"raw.json"))
done=set(json.load(open(R+"done.json"))) if os.path.exists(R+"done.json") else set(res)
HAT=re.compile(r"\b(hat|cap|snapback|5.?panel|five.?panel|bucket|visor|beanie|trucker|rope|dad hat|headwear)\b",re.I)
NOT=re.compile(r"headcover|head cover|club cover|towel|shirt|polo|tee\b|sock|glove|bag\b|putter|pin\b|caddy|gift card|marker",re.I)
todo=[(k,v) for k,v in sorted(stores.items()) if k not in done]
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else 25
for slug,meta in todo[:LIMIT]:
    # DO NOT mark done before the fetch succeeds.
    # The first version added the slug to `done` on entry, so a 429 counted as
    # "swept" and the store was never retried — the sweep reported 70/104 done
    # while having actually read 15. Only a real response marks a store read.
    dom=meta.get("domain")
    if not dom: done.add(slug); continue
    d=None
    for attempt in (1,2):
        try:
            d=json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://{dom}/products.json?limit=250",headers=UA),timeout=15).read()); break
        except Exception as e:
            if getattr(e,"code",None)==429 and attempt==1: time.sleep(3); continue
            break
    time.sleep(3.5)
    if not d: continue          # left out of `done`, so a later pass retries it
    done.add(slug)
    out=[]
    for p in d.get("products",[]):
        hay=" ".join([p.get("title",""),p.get("product_type","") or ""]+list(p.get("tags",[])))
        if not HAT.search(hay) or NOT.search(p.get("title","")): continue
        vs=[v for v in p.get("variants",[]) if v.get("available")]
        if not vs: continue
        pr=sorted({float(v["price"]) for v in vs})
        img=(p.get("images") or [{}])[0]
        out.append({"brand":slug,"title":p["title"],"handle":p["handle"],"price":pr[0],
                    "url":f"https://{dom}/products/{p['handle']}","img":img.get("src"),
                    "w":img.get("width"),"h":img.get("height"),"type":p.get("product_type")})
    if out: res[slug]=out
json.dump(res,open(R+"raw.json","w"),indent=1)
json.dump(sorted(done),open(R+"done.json","w"))
print(f"  swept {len(done)}/{len(stores)} stores | {len(res)} brands with hats | {sum(len(v) for v in res.values())} hats")
