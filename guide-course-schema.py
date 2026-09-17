#!/usr/bin/env python3
"""Machine-readable course data for the Austin Golf Guide — 17 September 2026.

WHY
---
The guide describes nineteen golf courses and, until now, published almost no
machine-readable facts about any of them. Its ItemList held five bare ListItems
carrying a name and a fragment URL and nothing else — no address, no telephone,
no price. An assistant asked "where is Roy Kizer and what does it cost" had
nothing on the page it could lift with confidence, so it cited somebody else.

This replaces that with GolfCourse entities carrying address, telephone, official
URL and — where a rate card actually exists — priceRange.

THE VERIFICATION RULE (Lenny's call, 17 Sept 2026)
--------------------------------------------------
EVERY FIELD BELOW WAS READ TODAY FROM THE COURSE'S OWN SITE OR THE CITY OF
AUSTIN'S. Nothing is inferred, nothing is carried over from an aggregator, no ZIP
or area code is guessed. Where a field could not be verified it is ABSENT rather
than estimated — an empty field costs us nothing, a wrong address is the kind of
error that gets a source dropped permanently.

Consequences of that rule, all deliberate:

  * SHADOWGLEN gets name and URL only. Every sub-page on its site returned an
    empty body, and its two homepages serve different content — the www one is
    visibly stale (reviews dated 2012). The only readable phone number came off
    that stale page, so it is not published here.
  * CRYSTAL FALLS gets no address or telephone: neither appears on any page of
    its site that returns content. Its rate table does render, and is dated by
    the club itself, so priceRange is published.
  * KISSING TREE gets no address. The only source for one was the title of a PDF
    that would not load. Its telephone did render, so that is published. SEE THE
    WARNING AT THE BOTTOM OF THIS FILE — its homepage carries a closure notice.
  * NO GREEN FEE is published for any of the seven resort courses. Not one of
    them prints a rate on its own site; every figure available came from booking
    engines or aggregators.

  * OMNI BARTON CREEK is marked publicAccess: false. Its own site says golf is
    "reserved exclusively for resort guests" in three separate places. Marking it
    publicly playable would be a factual error with a booking consequence.
  * ROY KIZER AND JIMMY CLAY share a street address and telephone. That is not a
    bug — the City prints the same values on both pages because they are one
    36-hole complex at 5400 Jimmy Clay Dr.

Telephone numbers are normalised to +1-XXX-XXX-XXXX. That is a formatting choice
about the same digits, not a change to the fact.

ALSO FIXED HERE
---------------
  * dateModified was 2026-08-07. The page has been edited twice today. Recency is
    a retrieval signal and the old date was simply wrong.
  * The author was a bare Person with no identity. Now carries url and sameAs, so
    the byline resolves to something.
"""
import re, os, sys, json

apply_ = "--apply" in sys.argv
P = "field-guide/index.html"
TODAY = "2026-09-17"

# name, url, street, city, zip, phone, priceRange, publicAccess
# "" means NOT VERIFIED TODAY — the field is omitted from the output entirely.
MUNIS = [
 ("Lions Municipal Golf Course", "https://www.austintexas.gov/golfatx/lions-municipal-course",
  "2901 Enfield Rd", "Austin", "78703", "+1-512-978-6869", "$35-$44", True),
 ("Morris Williams Golf Course", "https://www.austintexas.gov/golfatx/morris-williams-course",
  "3851 Manor Road", "Austin", "78723", "+1-512-974-8333", "$35-$44", True),
 ("Hancock Golf Course", "https://www.austintexas.gov/golfatx/hancock-course",
  "811 E. 41st St.", "Austin", "78751", "+1-512-974-9350", "$20", True),
 ("Roy Kizer Golf Course", "https://www.austintexas.gov/golfatx/roy-kizer-course",
  "5400 Jimmy Clay Dr.", "Austin", "78744", "+1-512-974-4653", "$35-$44", True),
 ("Jimmy Clay Golf Course", "https://www.austintexas.gov/golfatx/jimmy-clay-course",
  "5400 Jimmy Clay Dr.", "Austin", "78744", "+1-512-974-4653", "$35-$44", True),
]

COURSES = [
 ("Falconhead Golf Club", "https://www.falconheadaustin.com/",
  "15201 Falconhead Blvd", "Austin", "78738", "+1-512-402-1558", "", True),
 ("Avery Ranch Golf Club", "https://averyranch.com/",
  "10500 Avery Club Drive", "Austin", "78717", "+1-512-248-2442", "", True),
 ("Grey Rock Golf Club", "https://www.greyrockgolfandtennis.com/",
  "7401 State Highway 45", "Austin", "78739", "+1-512-288-4297", "$90-$105", True),
 ("The Golf Club at Star Ranch", "https://www.starranchgolf.com/",
  "2500 FM 685", "Hutto", "78634", "+1-512-252-4653", "$62-$139", True),
 # ShadowGlen: site unreadable, only phone came off a visibly stale page — omitted.
 ("ShadowGlen Golf Club", "https://www.shadowglengolf.com/", "", "", "", "", "", True),
 # Crystal Falls: no address or phone renders anywhere on its site; rates do.
 ("Crystal Falls Golf Club", "https://www.crystalfallsgolf.com/",
  "", "", "", "", "$18-$75", True),
 ("Vaaler Creek Golf Club", "https://www.vaalercreekgolfclub.com/",
  "228 Jeff Vaughn", "Blanco", "78606", "+1-830-833-0706", "$45-$110", True),
 # Kissing Tree: address only ever appeared in a PDF title that would not load.
 ("Kissing Tree Golf Club", "https://www.kissingtreegolfclub.com/",
  "", "", "", "+1-512-749-1043", "", True),
 ("The Quarry Golf Club", "https://quarrygolf.com/",
  "444 East Basse Road", "San Antonio", "78209", "+1-210-824-4500", "", True),
 ("Lost Pines Resort Golf Club", "https://www.lostpinesresortandspa.com/golf/",
  "575 Hyatt Lost Pines Road", "Lost Pines", "78612", "+1-855-923-7851", "", True),
 # Omni: "reserved exclusively for resort guests", stated three times on its site.
 ("Omni Barton Creek Resort & Spa Golf", "https://www.omnihotels.com/hotels/austin-barton-creek/golf",
  "8212 Barton Club Drive", "Austin", "78735", "+1-512-329-4018", "", False),
 ("Horseshoe Bay Resort Golf", "https://www.hsbresort.com/golf/",
  "200 Hi Circle North", "Horseshoe Bay", "78657", "+1-877-611-0112", "", True),
 ("La Cantera Golf Club", "https://www.lacanteragolfclub.com/",
  "16641 La Cantera Pkwy", "San Antonio", "78256", "+1-210-558-4653", "", True),
 ("Lajitas Golf Resort — Black Jack's Crossing", "https://www.lajitasgolfresort.com/golf/",
  "21701 FM 170", "Lajitas", "79852", "+1-432-424-5080", "", True),
]


def course(rec, anchor):
    name, url, street, city, zp, phone, price, public = rec
    d = {"@type": "GolfCourse", "name": name, "url": url,
         "subjectOf": {"@type": "WebPage",
                       "url": f"https://thegrassyissue.com/field-guide/#{anchor}"}}
    if street:                      # address only when every part was verified
        d["address"] = {"@type": "PostalAddress", "streetAddress": street,
                        "addressLocality": city, "addressRegion": "TX",
                        "postalCode": zp, "addressCountry": "US"}
    if phone:
        d["telephone"] = phone
    if price:
        d["priceRange"] = price
    if public is False:             # only assert the restriction, never the opposite
        d["publicAccess"] = False
    return d


def itemlist(name, recs, anchor):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListOrder": "https://schema.org/ItemListUnordered",
            "numberOfItems": len(recs),
            "itemListElement": [{"@type": "ListItem", "position": i,
                                 "item": course(r, anchor)}
                                for i, r in enumerate(recs, 1)]}


t = open(P, encoding="utf-8").read()
orig = t
problems, log = [], []

# ------------------------------------------- replace the thin muni ItemList
ms = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
      if '"ItemList"' in m.group(1)]
if len(ms) != 1:
    raise SystemExit(f"expected exactly 1 ItemList block, found {len(ms)}")
m = ms[0]
new = ('<script type="application/ld+json">' +
       json.dumps(itemlist("Austin Municipal Golf Courses", MUNIS, "munis"),
                  ensure_ascii=False) + "</script>\n"
       '<script type="application/ld+json">' +
       json.dumps(itemlist("Golf Courses Near Austin for a Special Day or Day Trip",
                           COURSES, "special"), ensure_ascii=False) + "</script>")
t = t[:m.start()] + new + t[m.end():]
log.append(f"ItemList: 5 bare ListItems -> {len(MUNIS)} + {len(COURSES)} GolfCourse entities")

# ------------------------------------------ dateModified + author identity
ms = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
      if '"Article"' in m.group(1)]
if len(ms) != 1:
    problems.append(f"expected exactly 1 Article block, found {len(ms)}")
else:
    m = ms[0]
    d = json.loads(m.group(1))
    was = d.get("dateModified")
    d["dateModified"] = TODAY
    d["author"] = {"@type": "Person", "name": "Lenny Harrington",
                   "url": "https://thegrassyissue.com/about",
                   "sameAs": ["https://www.instagram.com/thegrassyissue/"]}
    d["publisher"] = {"@type": "Organization", "name": "The Grassy Issue",
                      "url": "https://thegrassyissue.com",
                      "sameAs": ["https://www.instagram.com/thegrassyissue/"]}
    t = t[:m.start()] + ('<script type="application/ld+json">' +
                         json.dumps(d, ensure_ascii=False) + "</script>") + t[m.end():]
    log.append(f"Article dateModified {was} -> {TODAY}; author and publisher given identity")

# ----------------------------------------------------------------- guards
names = [r[0] for r in MUNIS + COURSES]
if len(set(names)) != len(names):
    problems.append("a course is listed twice")

for r in MUNIS + COURSES:
    name, url, street, city, zp, phone, price, _pub = r
    # partial addresses are worse than none — all four parts or nothing
    parts = [bool(street), bool(city), bool(zp)]
    if any(parts) and not all(parts):
        problems.append(f"{name}: partial address — publish all of it or none of it")
    if zp and not re.fullmatch(r"\d{5}", zp):
        problems.append(f"{name}: ZIP {zp!r} is not five digits")
    if phone and not re.fullmatch(r"\+1-\d{3}-\d{3}-\d{4}", phone):
        problems.append(f"{name}: telephone {phone!r} is not normalised +1-XXX-XXX-XXXX")
    if price and not re.fullmatch(r"\$[\d,]+(-\$[\d,]+)?", price):
        problems.append(f"{name}: priceRange {price!r} is malformed")
    if not url.startswith("http"):
        problems.append(f"{name}: url is not absolute")

# the guide must actually mention every course we mark up
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
for name in names:
    stem = name.split(" Golf")[0].split(" —")[0].split(" Resort")[0].strip()
    if stem not in plain:
        problems.append(f"schema names {name!r} but the page never mentions {stem!r}")

# every JSON-LD block must parse, and the FAQ must still match its schema
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
for b in blocks:
    json.loads(b)
vis = len(re.findall(r'<details class="faq-q">', t))
sch = 0
for b in blocks:
    if '"FAQPage"' in b:
        sch = len(json.loads(b)["mainEntity"])
if vis != sch:
    problems.append(f"visible FAQ {vis} != FAQPage schema {sch}")

# nothing about the visible page may have moved
for tag in ("<div", "<section", "<a ", "<details", "<img"):
    if t.count(tag) != orig.count(tag):
        problems.append(f"{tag!r} count changed — schema work touched the visible page")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — course schema on {P}")
for l in log:
    print("  ·", l)

full = [r for r in MUNIS + COURSES if r[2]]
ph = [r for r in MUNIS + COURSES if r[5]]
pr = [r for r in MUNIS + COURSES if r[6]]
print(f"\n  {len(MUNIS)+len(COURSES)} courses marked up")
print(f"    address    {len(full):2}/{len(names)}")
print(f"    telephone  {len(ph):2}/{len(names)}")
print(f"    priceRange {len(pr):2}/{len(names)}")
print("\n  omitted as unverified today:")
for r in MUNIS + COURSES:
    gaps = [n for n, v in (("address", r[2]), ("telephone", r[5]), ("priceRange", r[6])) if not v]
    if gaps:
        print(f"    {r[0]:44} {', '.join(gaps)}")
print(f"\n  {len(blocks)} JSON-LD blocks, all parse | FAQ {vis} visible / {sch} schema")
if not apply_:
    print("\npass --apply to write")

# ---------------------------------------------------------------------------
# FLAG FOR LENNY, not fixed here because it is an editorial call, not a schema one:
# kissingtreegolfclub.com currently posts on its homepage that "the golf course
# will temporarily close to the public and undergo a transition ... We look
# forward to reopening in early May". No year is given and the surrounding site
# is stale, so the notice may be old — but the guide presents Kissing Tree as
# bookable today. Worth a phone call to +1-512-749-1043 before the next deploy.
# ---------------------------------------------------------------------------
