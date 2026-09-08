#!/usr/bin/env python3
"""assign-taste-tags.py — fill the taste-tag gap on brands that had none.

Rules taken from TAGS.md: 1-3 tags per brand; tags describe the BRAND not one
product; never invent a tag; and an empty array is a valid answer — under-tagging
beats wrong-tagging. Mutually exclusive pairs enforced below:
  quiet-luxury / loud-on-purpose · dad-golf / gorpcore · member-guest / range-rat

Deliberately left EMPTY (evidence too thin to defend a judgement):
  3 Putt Round, Pluto Golf, Rebolf, Badlands  — one mention each and the index
    line is the generic White Tee Edit placeholder, so there is nothing to read
  Big Dog Golf Co., Bluetross, Gray + Haast, P53 Irons, Penta Golf, Rhoback,
  Hedge — single mention, and the distinguishing claim (hand-made? price band?)
    is not established anywhere we have checked
  Owala — drinkware; no taste tag in the list applies, and inventing one is
    explicitly against rule 5
  water when dry — storefront is password-gated, so the range cannot be assessed;
    gets the drops-and-vanishes ATTRIBUTE instead, which is a checkable fact
"""
import json, sys

TAGS={  # slug -> taste tags, with the criterion each one is claimed under
 "anti-country-club-tokyo":["loud-on-purpose"],
 "bettinardi":["design-nerd"],
 "devant":["course-merch"],
 "eastside-golf":["collab-machine","post-round-friendly"],
 "edison-golf":["design-nerd"],
 "found-golf":["loud-on-purpose"],
 "ghost-golf":["design-nerd"],
 "gumtree-golf":["made-by-hand","loud-on-purpose"],
 "piretti":["design-nerd"],
 "pins-and-aces":["loud-on-purpose"],
 "puma-golf":["loud-on-purpose"],
 "sounder":["quiet-luxury","post-round-friendly"],
 "stitch-golf":["quiet-luxury"],
 "sunday-golf":["muni-energy"],
 "vessel":["quiet-luxury"],
 "winston-collection":["made-by-hand"],
 "dormie-workshop":["made-by-hand","quiet-luxury"],
 "gfore":["loud-on-purpose"],
 "bag-boy":["range-rat"],
 "aime-leon-dore":["post-round-friendly","collab-machine"],
 "agronomy-workshop":["gorpcore"],
 "vuori":["post-round-friendly"],
 "peter-millar":["member-guest"],
 "ovo":["loud-on-purpose","collab-machine"],
 "no-laying-up":["muni-energy"],
 "lululemon":["post-round-friendly"],
 "evnroll":["design-nerd"],
 "carhartt-wip":["gorpcore","post-round-friendly"],
}
# attributes are FACTS — only where the brand's own index line states them
ATTRS={
 "bettinardi":["heritage"],            # "since 1998"
 "devant":["heritage"],   # "Founded 1976"
 "bag-boy":["heritage"],               # "since 1946"
 "lululemon":["heritage"],             # "since 1998"
 "carhartt-wip":["heritage"],          # "since 1994"
 "water-when-dry":["drops-and-vanishes"],  # "sold in timed online drops"
 "gamut-golf":["drops-and-vanishes"],      # catalogue is mostly sold out
}
EXCL=[("quiet-luxury","loud-on-purpose"),("dad-golf","gorpcore"),("member-guest","range-rat")]
VALID={'muni-energy','design-nerd','quiet-luxury','loud-on-purpose','dad-golf','gorpcore',
 'post-round-friendly','made-by-hand','collab-machine','course-merch','member-guest','range-rat'}
VALID_ATTR={'women-founded','tour-proven','heritage','drops-and-vanishes','new-to-index'}

APPLY="--apply" in sys.argv
B=json.load(open("data/brands.json")); idx={b["slug"]:b for b in B}
bad=[]
for s,t in TAGS.items():
    if s not in idx: bad.append(f"unknown slug {s}"); continue
    if not set(t)<=VALID: bad.append(f"{s}: invalid tag {set(t)-VALID}")
    if len(t)>3: bad.append(f"{s}: {len(t)} tags, max 3")
    for a,c in EXCL:
        if a in t and c in t: bad.append(f"{s}: mutually exclusive {a}+{c}")
for s,a in ATTRS.items():
    if s not in idx: bad.append(f"unknown slug {s}")
    elif not set(a)<=VALID_ATTR: bad.append(f"{s}: invalid attr")
    elif "new-to-index" in a: bad.append(f"{s}: new-to-index is computed, never hand-assigned")
if bad:
    print("VALIDATION FAILED:"); [print("  ",x) for x in bad]; sys.exit(1)
print("validation passed\n")

nt=na=0
for s,t in TAGS.items():
    b=idx[s]; keep=[x for x in b.get("tags",[]) if x not in VALID]  # preserve 'independent' etc.
    new=keep+t
    if new!=b.get("tags"): b["tags"]=new; nt+=1
    print(f"  {b['name'][:26]:28} {', '.join(t)}")
for s,a in ATTRS.items():
    b=idx[s]; cur=b.get("attrs",[])
    add=[x for x in a if x not in cur]
    if add: b["attrs"]=cur+add; na+=1; print(f"  + attr {b['name'][:24]:26} {', '.join(add)}")
if APPLY:
    json.dump(B,open("data/brands.json","w"),indent=1,ensure_ascii=False)
print(f"\n{nt} brands tagged, {na} given attributes")
print("applied" if APPLY else "DRY RUN — pass --apply")
