#!/usr/bin/env python3
"""sweep-homegoods.py — find every home-goods product across TGI's brand
universe. 22 September 2026.

Lenny: "any other homes goods type items from our brand universe?"

Reads data/brands.json (140 brands with their own store URLs) and asks each
store for its catalogue. Shopify answers /products.json; Squarespace answers
/shop?format=json; anything else is recorded as unreachable rather than guessed
at.

STOCK IS READ FROM THE NUMBERS, NOT THE WORDS. A Shopify product page prints
"sold out" whenever ANY variant is gone, so the phrase fires on products with
24 units on the shelf — that is how the Gumtree mug set nearly got cut. This
uses variants[].available on Shopify and qtyInStock on Squarespace.

HOME GOODS MEANS THINGS FOR A ROOM, not things for a bag. Headcovers, towels,
divot tools and ball markers are excluded even though every golf brand sells
them; a caddy towel is not homeware. Apparel is excluded outright.

Writes research/homegoods/sweep.json. Read-only against the network.
"""
import json, pathlib, re, sys, urllib.request, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "research/homegoods/sweep.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}

HOME = re.compile(r"\b(mug|glass(?:es|ware)?|tumbler|stein|carafe|pitcher|candle|"
                  r"coaster|blanket|throw|pillow|cushion|rug|doormat|mat\b|print|"
                  r"poster|art\b|artwork|frame[ds]?|book|vase|bowl|tray|ashtray|"
                  r"incense|ceramic|pottery|stool|chair|lamp|clock|puzzle|"
                  r"playing card|pennant|banner|soap|matches|matchbook|bookend|"
                  r"coffee|moka|kettle|teapot|napkin|placemat|tablecloth|"
                  r"cutting board|decanter|flask|shaker|bottle opener|"
                  r"wall hanging|tapestry|sign\b|wastebasket|bin\b|crate|shelf)\b",
                  re.I)
# Things every golf brand sells that are NOT homeware.
NOT_HOME = re.compile(r"headcover|head cover|divot|ball marker|tee\b|glove|"
                      r"polo|shirt|hat|cap\b|pant|short|jacket|vest|hoodie|"
                      r"sock|belt|shoe|bag\b|towel|beanie|sweater|crewneck|"
                      r"pullover|quarter.?zip|gift card|sticker|patch|keychain|"
                      r"grip\b|shaft|putter|driver|iron\b|wedge|umbrella", re.I)


def get(url, timeout=25):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=timeout).read()


def probe(b):
    name, url = b["name"], (b.get("url") or "").rstrip("/")
    if not url.startswith("http"):
        return {"brand": name, "status": "no url"}
    hits, status = [], None
    try:                                              # Shopify
        d = json.loads(get(url + "/products.json?limit=250"))
        status = "shopify"
        for p in d.get("products", []):
            t = p["title"]
            if NOT_HOME.search(t) or not HOME.search(t):
                continue
            v = p["variants"][0]
            hits.append({"t": t, "usd": float(v["price"]),
                         "in": bool(v.get("available")),
                         "u": f"{url}/products/{p['handle']}",
                         "imgs": len(p.get("images", []))})
    except Exception:
        try:                                          # Squarespace
            d = json.loads(get(url + "/shop?format=json"))
            status = "squarespace"
            for i in d.get("items", []):
                t = i.get("title", "")
                if NOT_HOME.search(t) or not HOME.search(t):
                    continue
                vs = (i.get("structuredContent") or {}).get("variants") or []
                if not vs:
                    continue
                q = sum(v.get("qtyInStock") or 0 for v in vs)
                hits.append({"t": t, "usd": vs[0]["price"] / 100, "in": q > 0,
                             "u": url + i.get("fullUrl", ""),
                             "imgs": len(i.get("items") or [])})
        except Exception as e:
            status = f"unreachable ({type(e).__name__})"
    return {"brand": name, "status": status, "hits": hits}


def main():
    # data/brands.json's "url" is the brand's page ON TGI, not its shop — the
    # first run of this read 1 store out of 140 because of that. The real store
    # domains are harvested from the site's own product-link hrefs into
    # research/homegoods/domains.json.
    doms = json.loads((ROOT / "research/homegoods/domains.json").read_text())
    todo = [{"name": d, "url": "https://" + d} for d in doms]
    print(f"  probing {len(todo)} brand stores...")
    res = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for r in ex.map(probe, todo):
            res.append(r)
    ok = [r for r in res if r.get("hits")]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))
    live = [(r["brand"], h) for r in ok for h in r["hits"] if h["in"]]
    print(f"  {sum(1 for r in res if r['status'] in ('shopify','squarespace'))} stores read, "
          f"{len(ok)} have home goods, {len(live)} items in stock\n")
    for brand, h in sorted(live, key=lambda x: -x[1]["usd"]):
        print(f"   ${h['usd']:>7.0f}  {brand[:22]:<24}{h['t'][:52]:<54}{h['imgs']}img")


if __name__ == "__main__":
    main()
