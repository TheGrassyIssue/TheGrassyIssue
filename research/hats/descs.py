import json, urllib.request, time, sys, os, re, html
from collections import defaultdict
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
R="research/hats/"
items=json.load(open(R+"grid18.json"))+json.load(open("research/towels/grid.json"))
out=json.load(open(R+"descs.json")) if os.path.exists(R+"descs.json") else {}
bydom=defaultdict(list)
for it in items:
    m=re.match(r"https?://([^/]+)/products/([^/?#]+)",it["url"])
    if m: bydom[m.group(1)].append((m.group(2),it))
todo=[d for d in sorted(bydom) if not all(it["url"] in out for _h,it in bydom[d])]
for dom in todo[:int(sys.argv[1])]:
    try:
        d=json.loads(urllib.request.urlopen(urllib.request.Request(
            f"https://{dom}/products.json?limit=250",headers=UA),timeout=18).read())
        idx={p["handle"]:p for p in d["products"]}
    except Exception: time.sleep(1); continue
    for h,it in bydom[dom]:
        p=idx.get(h)
        if not p: continue
        txt=html.unescape(re.sub(r"<[^>]+>"," ",p.get("body_html") or ""))
        out[it["url"]]={"desc":re.sub(r"\s+"," ",txt).strip()[:700],
                        "tags":p.get("tags",[])[:8],"type":p.get("product_type")}
    time.sleep(1.2)
json.dump(out,open(R+"descs.json","w"),indent=1)
print(f"  descriptions: {len(out)}/{len(items)}")
