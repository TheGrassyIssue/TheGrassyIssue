#!/usr/bin/env python3
"""Wire the Austin topic cluster: hub -> spokes in the Field Guide, spokes -> hub on each page."""
import re, os, sys

S = os.path.dirname(os.path.abspath(__file__))
FG = os.path.join(S, "field-guide/index.html")

# section heading text -> cards to append
ADD = {
 "Where to sharpen your game.": [
   ("summer-practice-guide-austin", "/images/summer-practice/round-rock-range.jpg",
    "Practice · Summer",
    "The Summer Practice Guide — Where to Hit Balls at 105&deg;",
    "Ranges with shade and misters, short-game areas that stay open in August, and the indoor bays worth the money when it's genuinely too hot.",
    "Golfer hitting balls at the Round Rock driving range"),
 ],
 "Where to eat, drink, and decompress.": [
   ("austin-coffee-guide", "/images/austin-coffee/radio-coffee.jpg",
    "Coffee · 18 Shops",
    "The Pre-Round Pour — 18 Austin Coffee Shops for Golfers",
    "Eighteen independent shops for the drive to the first tee. Institutions, roasters and patio spots, sorted by which course they're actually near.",
    "Outdoor seating at Radio Coffee and Beer in South Austin"),
   ("best-wings-in-austin", "/images/best-wings/wingzup.jpg",
    "Wings · 16 Spots",
    "The Best Wings in Austin — 16 Spots After the Round",
    "From Wingzup's 28 sauces to the dive-bar orders nobody writes about. Sixteen spots, ranked, with the closest course to each.",
    "A basket of saucy chicken wings from an Austin wing spot"),
   ("best-pizza-in-austin", "/images/austin-pizza/bufalina.jpg",
    "Pizza · 10 Spots",
    "The Best Pizza in Austin — 10 Spots After the Round",
    "Ten pizzerias worth the detour, from Bufalina's 900&deg; wood-fired Neapolitan down to the by-the-slice places open late.",
    "A wood-fired Neapolitan pizza at Bufalina in Austin"),
   ("sandwiches-before-the-round", "/images/sandwiches/hero.jpg",
    "Sandwiches · 12 Spots",
    "Sandwiches Before the Round — 12 Paired to a Muni",
    "Twelve of the best sandwiches in Austin, each matched to the municipal course closest to it. Eat first, then go play.",
    "A stacked deli sandwich cut in half on butcher paper"),
 ],
 "What's happening and what came before.": [
   ("hancock-golf-course-austin", "/images/hancock/hero.jpg",
    "History · Hancock",
    "Hancock Golf Course — The Oldest Course in Texas",
    "Opened 1899 and still the oldest surviving course in Texas. Nine holes, par 35, $20 to walk, and the ground Harvey Penick learned the game on.",
    "The ninth green at Hancock Golf Course in central Austin"),
   ("roy-kizer-from-sewage-plant-to-links-style-gem", "/images/feed/0d3a6cc4-Parks20and20Recreation20-20Web_kizer-golf-course.jpg",
    "History · Roy Kizer",
    "Roy Kizer — From Sewage Plant to Links-Style Gem",
    "Built on a decommissioned wastewater treatment plant in southeast Austin, and somehow the best-looking muni in the system.",
    "Links-style fairway and pond at Roy Kizer Golf Course"),
 ],
}

BACKLINK_PAGES = [
 "austin-coffee-guide","summer-practice-guide-austin","best-wings-in-austin","best-pizza-in-austin",
 "hancock-golf-course-austin","roy-kizer-from-sewage-plant-to-links-style-gem","sandwiches-before-the-round",
 "austin-golf-road-trip","austin-bbq-field-guide","8-best-practice-facilities-around-austin",
 "where-to-watch-the-world-cup-in-austin","7-post-round-moves-in-austin","10-of-the-best-post-round-burgers",
 "8-special-day-rounds-near-austin","ranking-the-muni-grub-every-on-course-food-spot-in-austin",
 "7-indoor-simulators-for-austins-gross-rainy-days","5-post-round-evening-spots-in-austin",
 "the-firecracker-open-81-years-at-the-muny",
 "lions-muny-is-getting-a-world-class-renovation-heres-whats-c","10-texas-courses-worth-the-trip",
]

def match_div(s, start):
    """start = index of a '<div'; return index of its matching '</div>' opening bracket."""
    i, depth = start, 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return start + m.start()
        else:
            depth += 1
    return -1

def card(slug, img, tag, title, desc, alt):
    return (f'\n    <a href="/drops/{slug}" class="guide-card">\n'
            f'      <img class="guide-card-img" src="{img}" alt="{alt}" loading="lazy" />\n'
            f'      <div class="guide-card-body">\n'
            f'        <div class="guide-card-tag">{tag}</div>\n'
            f'        <div class="guide-card-title">{title}</div>\n'
            f'        <div class="guide-card-desc">{desc}</div>\n'
            f'        <span class="guide-card-link">Read the guide &rarr;</span>\n'
            f'      </div>\n'
            f'    </a>')

def wire_hub():
    h = open(FG, encoding="utf-8").read()
    # fix the broken road-trip link
    if "/drops/the-austin-golf-road-trip" in h:
        h = h.replace("/drops/the-austin-golf-road-trip", "/drops/austin-golf-road-trip")
        print("  fixed broken link: the-austin-golf-road-trip -> austin-golf-road-trip")
    added = 0
    for heading, cards in ADD.items():
        hm = re.search(re.escape(heading), h)
        if not hm:
            print(f"  !! heading not found: {heading}"); continue
        cb = h.find('<div class="guide-cards">', hm.end())
        if cb == -1:
            print(f"  !! no cards block after: {heading}"); continue
        close = match_div(h, cb)
        if close == -1:
            print(f"  !! unbalanced block after: {heading}"); continue
        new = ""; cnt = 0
        for c in cards:
            if f'/drops/{c[0]}"' in h:
                print(f"     already linked, skipping: {c[0]}"); continue
            new += card(*c); added += 1; cnt += 1
        if new:
            h = h[:close] + new + "\n  " + h[close:]
            print(f"  + {cnt} card(s) -> {heading}")
    open(FG, "w", encoding="utf-8").write(h)
    return added

BACK = ('\n<div class="fg-backlink" style="max-width:1400px;margin:0 auto 40px;padding:0 32px;">'
        '<a href="/field-guide/" style="display:inline-block;font-family:var(--mono);font-size:10px;'
        'letter-spacing:.14em;text-transform:uppercase;border:.5px solid var(--ink);padding:10px 14px;">'
        '&larr; Part of the Austin Golf Field Guide</a></div>\n')

def wire_spokes():
    n = 0
    for slug in BACKLINK_PAGES:
        p = os.path.join(S, "drops", slug + ".html")
        if not os.path.exists(p):
            print(f"  !! missing page: {slug}"); continue
        h = open(p, encoding="utf-8").read()
        if 'class="fg-backlink"' in h:
            continue
        anchor = h.find('<section class="more"')
        if anchor == -1:
            anchor = h.rfind("<footer")
        if anchor == -1:
            print(f"  !! no anchor: {slug}"); continue
        h = h[:anchor] + BACK + h[anchor:]
        open(p, "w", encoding="utf-8").write(h)
        n += 1
    return n

if __name__ == "__main__":
    print("HUB -> SPOKES")
    a = wire_hub()
    print(f"\nSPOKES -> HUB")
    b = wire_spokes()
    print(f"  added backlink to {b} pages")
    print(f"\nTOTAL: {a} new hub cards, {b} backlinks")
