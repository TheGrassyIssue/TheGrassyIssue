#!/usr/bin/env python3
"""Add the design-led day-trip courses to the Field Guide's Day trips section.

Idempotent: re-running replaces the marked blocks in place.
  - TGI-DAYTRIPS block: four true day trips, inserted after the Day trips intro
  - TGI-STAY block: "Stay the night" label before Horseshoe Bay
  - TGI-TPC block: TPC San Antonio Canyons, after La Cantera
  - JSON-LD: the five courses are appended to the special-day ItemList
Images live in images/field-guide/ and come from each course's own site.
"""
import json, re, sys
from pathlib import Path

PAGE = Path(__file__).parent / "field-guide" / "index.html"

INTRO_OLD = re.compile(r'(<h2 class="guide-section-h2">Day trips &mdash; golf courses near Austin worth the drive\.</h2>\s*<p>).*?(</p>)', re.S)
INTRO_NEW = ("Two kinds of trip. The first four are 18-hole courses you can drive to, play and be home from by dinner, "
             "chosen for the architect, the routing or the ground they sit on. The four after that are sold with a room, "
             "so the number you are quoted depends on the package and the time of year.")

DAY = [
    dict(name="Canyon Springs Golf Club.", img="canyon-springs.jpg",
         alt="Aerial view of a fairway curving past a pond and oak woodland at Canyon Springs Golf Club, San Antonio",
         meta="Public · San Antonio · 1 hr 15 south",
         body=("Canyon Springs is the purest Hill Country routing within reach of Austin, a course laid over an old ranch "
               "rather than bulldozed into one. Thomas Walker opened it in 1998 with a brief to let the land lead, and it was "
               "named the best new public course in America that year. Each hole sits in its own pocket of oaks, past limestone "
               "waterfalls and the stonework of the Classen family homestead. Longhorns graze off the edges."),
         stats=[("Designer", "Thomas Walker"), ("Opened", "1998"), ("Setting", "Ranch land, limestone falls"), ("Best for", "A full Saturday away")],
         link="https://arcisgolf.com/clubs/canyon-springs-golf-club/book-a-tee-time"),
    dict(name="Cedar Creek Golf Course.", img="cedar-creek.jpg",
         alt="Aerial view of Cedar Creek Golf Course rolling through Hill Country on the northwest side of San Antonio",
         meta="City course · San Antonio · 1 hr 25 south",
         body=("Cedar Creek is the strongest case for San Antonio's city golf: a hilly, strategic 18 at municipal rates. "
               "Finger Dye Spann routed it through the hills northwest of town in 1989, with big elevation changes, doglegs that "
               "make you choose a side and greens built in at least two tiers. Jeffrey Blume renovated it in 2024. It hosts the "
               "San Antonio Open every year, and the views from the high tees are part of the round."),
         stats=[("Designer", "Finger Dye Spann"), ("Yards", "5,500 – 7,100"), ("Greens", "Two tiers or more"), ("Best for", "Big golf, city price")],
         link="https://alamocitygolftrail.com/tee-times/"),
    dict(name="The Golf Club of Texas.", img="golf-club-of-texas.jpg",
         alt="Native grasses and a green below the clubhouse at sunset at The Golf Club of Texas, San Antonio",
         meta="Semi-private · San Antonio · 1 hr 30 south",
         body=("The Golf Club of Texas is the place to feel what zoysia does under a golf ball. Lee Trevino designed the course in "
               "2000. It closed in the drought of 2013, and Roy Bechtol rebuilt it the next year, stretched it to 7,121 yards and "
               "grassed it in zoysia from tee to green, which the club says made it the first course in the country to do so. "
               "The lighted practice area stays open until 11pm."),
         stats=[("Designer", "Lee Trevino, Roy Bechtol"), ("Yards", "7,121"), ("Grass", "Zoysia, tee to green"), ("Best for", "Ball strikers")],
         link="https://golfclubtexas.com/tee-times/"),
    dict(name="Memorial Park Golf Course.", img="memorial-park.jpg",
         alt="Sunrise over the water and a closely mown fairway at Memorial Park Golf Course, Houston",
         meta="City course · Houston · 2 hr 45 east",
         body=("Memorial Park is the best-designed public golf in Texas, and it belongs to a city park. John Bredemus laid out the "
               "course in 1936 and, by local legend, called it his greatest. Tom Doak rebuilt it in 2019, and it now hosts the "
               "Houston Open and the Chevron Championship. Visitors from outside Houston pay $120 Monday to Thursday and $140 "
               "Friday to Sunday, with twilight from $90. The course is closed on Tuesdays."),
         stats=[("Designer", "Tom Doak (2019)"), ("Hosts", "Houston Open"), ("Non-resident", "$90 – $140"), ("Best for", "The long day of the year")],
         link="https://www.memorialparkgolf.com/memorial-park-golf-course"),
]

TPC = dict(name="TPC San Antonio &mdash; Canyons Course.", img="tpc-san-antonio-canyons.jpg",
           alt="Bunkered green set into Hill Country woodland on the Canyons Course at TPC San Antonio",
           meta="Resort · San Antonio · 1 hr 15 south",
           body=("The Canyons is Pete Dye in the Hill Country, and the way on is a room at the JW Marriott or a member's invitation. "
                 "Dye let the land set the strategy, with dramatic elevation changes and corridors that look out over a 700-acre "
                 "nature preserve. It hosted a PGA Tour Champions event from 2011 to 2015, while Greg Norman's Oaks Course next door "
                 "has held the Valero Texas Open since 2010."),
           stats=[("Designer", "Pete Dye"), ("Par / Yards", "72 · 7,106"), ("Access", "Resort guests, members"), ("Best for", "A Dye pilgrimage")],
           link="https://tpc.com/sanantonio/golf/vacations/")

LD = [
    {"name": "Canyon Springs Golf Club", "url": "https://arcisgolf.com/clubs/canyon-springs-golf-club/golf-course",
     "address": {"streetAddress": "24405 Wilderness Oak", "addressLocality": "San Antonio", "postalCode": "78260"}, "telephone": "+1-210-497-1770"},
    {"name": "Cedar Creek Golf Course", "url": "https://alamocitygolftrail.com/cedar-creek-golf-course/",
     "address": {"addressLocality": "San Antonio"}, "telephone": "+1-210-695-5050"},
    {"name": "The Golf Club of Texas", "url": "https://golfclubtexas.com/",
     "address": {"streetAddress": "13600 Briggs Ranch", "addressLocality": "San Antonio", "postalCode": "78245"}, "telephone": "+1-210-504-2550"},
    {"name": "Memorial Park Golf Course", "url": "https://www.memorialparkgolf.com/memorial-park-golf-course",
     "address": {"addressLocality": "Houston"}, "telephone": "+1-832-968-7486", "priceRange": "$90-$140"},
    {"name": "TPC San Antonio — Canyons Course", "url": "https://tpc.com/sanantonio/canyons-course/",
     "address": {"streetAddress": "23808 Resort Parkway", "addressLocality": "San Antonio", "postalCode": "78261"}, "telephone": "+1-210-491-5800"},
]


def block(c):
    stats = "".join(f'<div class="special-course-stat"><span class="label">{k}</span><span class="value">{v}</span></div>' for k, v in c["stats"])
    return f'''
  <div class="special-course">
    <img class="special-course-img" src="/images/field-guide/{c["img"]}" alt="{c["alt"]}" loading="lazy" />
    <div>
      <div class="special-course-name">{c["name"]}</div>
      <div class="special-course-meta">{c["meta"]}</div>
      <div class="special-course-body">{c["body"].replace("'", "&rsquo;")}</div>
      <div class="special-course-stats">{stats}</div>
      <a href="{c["link"]}" target="_blank" rel="noopener" class="special-course-link">Book a tee time ↗</a>
    </div>
  </div>
'''


def put(h, tag, html, anchor_re, after=True):
    start, end = f"<!-- {tag}:start -->", f"<!-- {tag}:end -->"
    blk = f"{start}{html}{end}\n"
    if start in h:
        return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", lambda m: blk, h, flags=re.S)
    m = re.search(anchor_re, h, re.S)
    if not m:
        sys.exit(f"anchor not found for {tag}")
    i = m.end() if after else m.start()
    return h[:i] + "\n" + blk + h[i:]


def main():
    h = PAGE.read_text()
    h, n = INTRO_OLD.subn(lambda m: m.group(1) + INTRO_NEW + m.group(2), h)
    if not n:
        sys.exit("intro not found")
    # day trips right after the subhead block
    h = put(h, "TGI-DAYTRIPS", "".join(block(c) for c in DAY),
            r'Day trips &mdash; golf courses near Austin worth the drive\.</h2>\s*<p>.*?</p>\s*</div>')
    stay = ('\n  <div class="guide-subhead tgi-stay"><div class="guide-section-kicker">Stay the night</div>'
            '<p>Four courses where the golf is sold with a room.</p></div>\n')
    h = put(h, "TGI-STAY", stay, r'\n  <div class="special-course">\s*<img class="special-course-img" src="/images/feed/89123d8f-Ram-Rock', after=False)
    # TPC after La Cantera
    h = put(h, "TGI-TPC", block(TPC), r'lacanteragolfclub\.com/" target="_blank" rel="noopener" class="special-course-link">Book a tee time ↗</a>\s*</div>\s*</div>')
    css = ".guide-subhead.tgi-stay { margin: 8px 0 0; padding-top: 32px; border-top: none; }"
    h = re.sub(r"\.guide-subhead\.tgi-stay \{[^}]*\}\n?", "", h)
    h = h.replace("</style>", css + "\n</style>", 1)

    # JSON-LD: special-day ItemList
    m = re.search(r'<script type="application/ld\+json">\s*(\{\s*"@context"[^<]*?"name": "Golf Courses Near Austin for a Special Day or Day Trip".*?)</script>', h, re.S)
    if not m:
        sys.exit("ItemList not found")
    data = json.loads(m.group(1))
    els = [e for e in data["itemListElement"] if e["item"]["name"] not in {x["name"] for x in LD}]
    for x in LD:
        addr = {"@type": "PostalAddress", **x["address"], "addressRegion": "TX", "addressCountry": "US"}
        item = {"@type": "GolfCourse", "name": x["name"], "url": x["url"],
                "subjectOf": {"@type": "WebPage", "url": "https://thegrassyissue.com/field-guide/#special-day"},
                "address": addr, "telephone": x["telephone"]}
        if "priceRange" in x:
            item["priceRange"] = x["priceRange"]
        els.append({"@type": "ListItem", "position": 0, "item": item})
    for i, e in enumerate(els, 1):
        e["position"] = i
    data["itemListElement"] = els
    data["numberOfItems"] = len(els)
    h = h[:m.start(1)] + json.dumps(data, indent=1, ensure_ascii=False) + "\n" + h[m.end(1):]
    PAGE.write_text(h)
    print(f"day trips wired: {len(DAY)} + TPC; ItemList now {len(els)}")


if __name__ == "__main__":
    main()
