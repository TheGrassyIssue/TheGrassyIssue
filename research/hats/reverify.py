"""Re-read price + stock from the COLLECTION feed, one fetch per domain.

WHY NOT THE PRODUCT FEED. The first version hit /products/<handle>.json and
came back with 29 of 30 items "sold out" — an absurd result that would have
killed the whole post. That endpoint is the same one that claimed Sugarloaf's
Arrow Cap had 0 of 8 variants available while the collection feed said 4 and
the actual product page said in stock with a live Add to cart. The collection
feed is the one that agreed with what a customer sees, so it is the one used
here. Trust the artifact the reader sees.
"""
import json, urllib.request, time, sys, os, re
from collections import defaultdict
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
R="research/hats/"
items=json.load(open(R+"grid18.json"))+json.load(open("research/towels/grid.json"))
out=json.load(open(R+"verified2.json")) if os.path.exists(R+"verified2.json") else {}
bydom=defaultdict(list)
for it in items:
    m=re.match(r"https?://([^/]+)/products/([^/?#]+)",it["url"])
    if m: bydom[m.group(1)].append((m.group(2),it))
    else: out.setdefault(it["url"],{"price":it["price"],"available":True,"src":"browser (non-Shopify)"})
todo=[d for d in sorted(bydom) if not all(it["url"] in out for _h,it in bydom[d])]
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else 8
for dom in todo[:LIMIT]:
    try:
        d=json.loads(urllib.request.urlopen(urllib.request.Request(
            f"https://{dom}/products.json?limit=250",headers=UA),timeout=18).read())
        idx={p["handle"]:p for p in d["products"]}
    except Exception as e:
        for _h,it in bydom[dom]: out[it["url"]]={"error":str(getattr(e,'code',None) or type(e).__name__)}
        time.sleep(1.0); continue
    for h,it in bydom[dom]:
        p=idx.get(h)
        if not p:
            out[it["url"]]={"error":"handle not in collection feed"}; continue
        av=[v for v in p["variants"] if v.get("available")]
        out[it["url"]]={"price":min(float(v["price"]) for v in p["variants"]),
                        "available":bool(av),"in_stock":len(av),"total":len(p["variants"]),
                        "title":p["title"],"src":"collection feed"}
    time.sleep(1.2)
json.dump(out,open(R+"verified2.json","w"),indent=1)
print(f"  domains done: {sum(1 for d in bydom if all(it['url'] in out for _h,it in bydom[d]))}/{len(bydom)}  ({len(out)} items)")
