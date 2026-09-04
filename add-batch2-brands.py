#!/usr/bin/env python3
"""
add-batch2-brands.py — add the 14 indie/lifestyle brands that appear in 2+ posts
but were absent from the brand index (audit 2026-09-04, Lenny picked this group
over the 7 big OEMs, which stay out deliberately).

Facts researched and ownership verified 2026-09-04. The `independent` tag is
applied ONLY where there is no parent, no public listing and no institutional
equity — several of these look boutique but are not:
  G/FORE + Peter Millar -> both Richemont (PM bought G/FORE 2018; Richemont made
                           G/FORE a standalone Maison Feb 2025)
  Bag Boy               -> Dynamic Brands
  Owala                 -> Trove Brands (BlenderBottle)
  Evnroll               -> Creatz/Uneekor took 70% in April 2023
  lululemon             -> Nasdaq: LULU
  Vuori                 -> SoftBank / General Atlantic / Stripes / Norwest
  Aime Leon Dore        -> LVMH Luxury Ventures minority stake, Jan 2022
  Carhartt WIP          -> WIP Trading AG, family-owned but operates under
                           licence from Carhartt, Inc. (judgment call: not tagged)

water when dry: storefront is password-gated, so HQ and founding year could not
be verified. loc "—" follows the Merrill Golf precedent rather than inventing a
city; region "world". FLAGGED for Lenny — may not even be a golf brand.
"""
import json, re, glob, os, html, sys

NEW = [
 dict(slug="water-when-dry", name="water when dry", loc="—", regions=["world"],
      cats=["apparel","headwear","accessories"], indep=True,
      line="Tees, hats, socks and accessories sold in timed online drops.",
      doms=["waterwhendry.com"]),
 dict(slug="dormie-workshop", name="Dormie Workshop", loc="Halifax, Canada", regions=["world"],
      cats=["headcovers","accessories"], indep=True,
      line="Handmade leather golf headcovers, belts and accessories, made in Nova Scotia since 2014.",
      doms=["dormieworkshop.com"]),
 dict(slug="gfore", name="G/FORE", loc="Los Angeles, California", regions=["usa"],
      cats=["apparel","headwear","accessories"], indep=False,
      line="Golf apparel, shoes, gloves and accessories, designed in Los Angeles since 2011.",
      doms=["gfore.com"]),
 dict(slug="bag-boy", name="Bag Boy", loc="Richmond, Virginia", regions=["usa"],
      cats=["bags","equipment","accessories"], indep=False,
      line="Golf bags, push carts, travel covers and accessories, out of Richmond, Virginia since 1946.",
      doms=["bagboy.com"]),
 dict(slug="aime-leon-dore", name="Aimé Leon Dore", loc="Queens, New York", regions=["usa"],
      cats=["apparel","headwear","accessories"], indep=False,
      line="Menswear, footwear and accessories from Queens, New York, in business since 2014.",
      doms=["aimeleondore.com"]),
 dict(slug="agronomy-workshop", name="Agronomy Workshop", loc="San Francisco, California", regions=["usa"],
      cats=["apparel","headwear","accessories"], indep=True,
      line="Cotton work shirts, rope hats and towels for golf, out of San Francisco.",
      doms=["agronomywork.shop"]),
 dict(slug="vuori", name="Vuori", loc="Carlsbad, California", regions=["usa"],
      cats=["apparel","accessories"], indep=False,
      line="Performance apparel for men and women, designed in Carlsbad, California since 2015.",
      doms=["vuoriclothing.com"]),
 dict(slug="peter-millar", name="Peter Millar", loc="Raleigh, North Carolina", regions=["usa"],
      cats=["apparel","headwear","accessories"], indep=False,
      line="Golf and lifestyle apparel for men and women, out of Raleigh, North Carolina.",
      doms=["petermillar.com"]),
 dict(slug="owala", name="Owala", loc="Lehi, Utah", regions=["usa"],
      cats=["accessories"], indep=False,
      line="Insulated water bottles and drinkware, from Utah-based Trove Brands, launched in 2020.",
      doms=["owalalife.com"]),
 dict(slug="ovo", name="OVO", loc="Toronto, Canada", regions=["world"],
      cats=["apparel","headwear","accessories"], indep=True,
      line="Streetwear, outerwear and accessories from Toronto, run as Drake's clothing label since 2011.",
      doms=["octobersveryown.com"]),
 dict(slug="no-laying-up", name="No Laying Up", loc="Jacksonville, Florida", regions=["usa"],
      cats=["community","apparel"], indep=True,
      line="Golf podcasts, video and merchandise, produced by a small team in Jacksonville, Florida.",
      doms=["nolayingup.com"]),
 dict(slug="lululemon", name="lululemon", loc="Vancouver, Canada", regions=["world"],
      cats=["apparel","accessories","bags"], indep=False,
      line="Athletic and lifestyle apparel, footwear and accessories, headquartered in Vancouver since 1998.",
      doms=["lululemon.com"]),
 dict(slug="evnroll", name="Evnroll", loc="Carlsbad, California", regions=["usa"],
      cats=["equipment","grips"], indep=False,
      line="Milled putters and grips, built in Carlsbad, California since 2016.",
      doms=["evnroll.com"]),
 dict(slug="carhartt-wip", name="Carhartt WIP", loc="Weil am Rhein, Germany", regions=["europe"],
      cats=["apparel","headwear","bags"], indep=False,
      line="Workwear-derived apparel, hats and bags, made in Europe under licence from Carhartt since 1994.",
      doms=["carhartt-wip.com"]),
]

ROOT=os.path.dirname(os.path.abspath(__file__))
APPLY="--apply" in sys.argv
B=json.load(open(f"{ROOT}/data/brands.json")); M=json.load(open(f"{ROOT}/data/brand-mentions.json"))
have={b["slug"] for b in B}

def strip_chrome(h):
    h=re.sub(r'<head>.*?</head>','',h,flags=re.S); h=re.sub(r'<nav\b.*?</nav>','',h,flags=re.S)
    h=re.sub(r'<footer\b.*?</footer>','',h,flags=re.S)
    return re.sub(r'<a[^>]*class="more-card"[^>]*>.*?</a>','',h,flags=re.S)

for n in NEW:
    if n["slug"] in have: print(f"  !! {n['slug']} already present, skipped"); continue
    hits=[]
    for f in sorted(glob.glob(f"{ROOT}/drops/*.html")):
        h=strip_chrome(open(f,encoding='utf-8',errors='ignore').read())
        hosts={re.sub(r'^www\.','',u.lower()) for u in re.findall(r'href="https?://([^/"]+)',h)}
        hosts|={re.sub(r'^(shop|store|us|eu)\.','',x) for x in hosts}
        if not any(x==d or x.endswith('.'+d) for x in hosts for d in n["doms"]): continue
        t=re.search(r"<title>([^<]*)</title>",h) or re.search(r"<title>([^<]*)</title>",open(f,encoding='utf-8').read())
        title=re.sub(r"\s*[—|]\s*The Grassy Issue\s*$","",html.unescape(t.group(1))).strip() if t else ""
        hits.append({"url":"/drops/"+os.path.basename(f)[:-5],"title":title,"profile":False})
    M[n["slug"]]=hits
    B.append({"slug":n["slug"],"name":n["name"],"loc":n["loc"],"regions":n["regions"],
              "cats":n["cats"],"line":n["line"],"url":hits[0]["url"] if hits else "/brands/",
              "tags":["independent"] if n["indep"] else [], "attrs":["new-to-index"],
              "added":"2026-09-04"})
    print(f"  {n['name']:20} {len(hits):2} posts  indep={str(n['indep']):5} {n['cats']}")

if APPLY:
    json.dump(B,open(f"{ROOT}/data/brands.json","w"),indent=1,ensure_ascii=False)
    json.dump(M,open(f"{ROOT}/data/brand-mentions.json","w"),indent=1,ensure_ascii=False)
print(f"\nbrands.json -> {len(B)} | mentions -> {len(M)}")
print("applied" if APPLY else "DRY RUN — pass --apply")
