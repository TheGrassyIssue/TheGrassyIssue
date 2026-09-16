#!/usr/bin/env python3
"""The venue cards. Lenny, 9/16/26: "lean more on the boxes formats."

Ten of the fourteen open rooms now carry real, location-specific photography and
get a .product-card box with a swipe gallery. The four that do not — Golfinity,
Spare Birdie, The Back Nine and Halftime Co. — stay as prose inside the section,
because the alternative is illustrating a room with somebody else's room and we
do not do that.

WHAT WAS THROWN OUT AT THE CONTACT SHEET, and why it matters that we looked:
  bogey-a/b/c   a polo, a rope hat and a ball marker. Merch, not a facility.
  bogey-d/e     logos.
  drg-a         a logo disc.
  rok-c         a "MEMBERSHIPS" text overlay.
  1872-d        an event flyer for a beginner clinic — a graphic, not a photo.
  atx-c/e/f     screen captures of the simulated course and the game UI. These
                show TrackMan's render, not ATX's room, and a reader would take
                them for the room.
  unsplash-*    two genuine stock files sitting in ATX's Squarespace library.
                Stock photography of somebody else's golf is the exact thing
                this guide refuses to do.
  fiber-lounge, fiber-social  CGI renders (cut on 9/16 before the first build).

Bogey Master yields exactly ONE usable frame, so its box carries a single image
and no gallery chrome. A one-frame gallery with arrows that go nowhere is worse
than an honest single photograph.

GALLERY MARKUP must match the house pattern verify-post.py enforces:
.product-gallery > .pg-frame > .pg-track, plus .pg-arw prev/next, .pg-dots with
one .pg-dot per frame, and .pg-count. Image count and dot count must agree.
"""
import os

IMG = "/images/austin-sims/"

# key, brand, headline, body, url, [(stem, alt)]
CARDS = {
"xgolf": ("X-Golf", "Cedar Park &middot; $55&ndash;65/hr",
  "Seven X-Golf simulators fill about 6,000 square feet on West Parmer, running the brand&rsquo;s own camera-plus-infrared-laser-plus-impact-sensor rig rather than a radar. $55 Monday to Thursday, $65 Friday to Sunday and holidays, $10 more for a private bay, and 10% off for first responders, veterans and anyone 65 or over. Memberships run $175 to $325 a month with a $1,000 corporate tier. Full restaurant, full bar, twelve TVs, two party rooms, and PXG Master Fitter fittings added since opening. Opened 8/6/25 &mdash; the fourth X-Golf in Texas.",
  "https://playxgolf.com/locations/cedar-park/",
  [("xgolf-building", "The X-Golf Cedar Park building on West Parmer Lane"),
   ("xgolf-group", "A group playing at X-Golf Cedar Park with food and drinks on the table")]),

"rok": ("ROK Golf", "Westlake &amp; Bee Cave &middot; TrackMan",
  "Two staffed rooms, TrackMan throughout &mdash; one radar and two cameras, RCT balls, Virtual Golf 3 on 400-plus courses. Every session is filmed in HD and the video and shot data are emailed to you afterward, which is the part most places do not do. <strong>GEARS three-dimensional swing analysis has returned to Westlake</strong> as a 90-minute evaluation run only by senior instructor Phil Snow. The new Champions Club membership is six or twelve months, unlimited, capped at a hundred members. Three coaches, beer and wine, all ages from about five up. They publish no hourly rate anywhere, so the link goes to booking.",
  "https://www.rokgolf.com/",
  [("rok-1", "A coach reviewing swing data with a golfer at ROK Golf"),
   ("rok-2", "A TrackMan unit set up in a bay at ROK Golf"),
   ("rok-3", "One-to-one instruction in a simulator bay at ROK Golf")]),

"fiber": ("Fiber Golf", "Southwest Austin &middot; $70/hr",
  "Two private bays on Circle Drive running TrackMan iO against <strong>40-foot wall-to-wall impact screens</strong> &mdash; the largest in the metro by a distance, and the reason to come. Virtual Golf 3, 500-plus courses, 24/7 keyless entry, no staff at all. $70 an hour; memberships at $250 and $350 a month. Opened 5/30/26 and sitting on a 5.0 Google average.",
  "https://fibergolf.com/",
  [("fiber-bay", "A TrackMan iO bay at Fiber Golf lit up against the 40-foot impact screen"),
   ("fiber-interior", "Wide interior view of the two-bay Fiber Golf room in southwest Austin"),
   ("fiber-pebble", "A course rendered across the full 40-foot screen at Fiber Golf"),
   ("fiber-player", "A golfer mid-swing in a bay at Fiber Golf")]),

"atx": ("ATX Indoor Golf Club", "SW Austin &middot; $40&ndash;50/hr",
  "Two bays on the US 290 service road, TrackMan iO projected in 4K UHD laser, 500-plus courses. <strong>$50 an hour, or $40 before 4pm Monday through Thursday</strong>, with memberships from $150 a month including 24/7 access. The bays are built for privacy rather than sightlines, each with its own 54-inch TV, and there is a self-serve pantry of cold drinks and snacks. Bring your own beer if you want it.",
  "https://atxindoorgolfclub.com/",
  [("atx-1", "The ATX Indoor Golf Club storefront on the US 290 service road"),
   ("atx-2", "A private bay at ATX Indoor Golf Club with a wall-mounted TV"),
   ("atx-3", "A golfer hitting into the screen in a darkened bay at ATX Indoor Golf Club")]),

"bogey": ("Bogey Master", "Hutto &middot; 24/7",
  "Hutto&rsquo;s first, opened 10/14/25, veteran-owned, and sited inside a self-storage facility next door to a brewery &mdash; the strangest and most Austin address in this entire guide. TrackMan, 200-plus courses, up to eight golfers a bay. A door code arrives by text and the door opens fifteen minutes before your slot. Bring your own clubs and your own beer. 30% off Monday to Thursday between 2am and 2pm, and 10% off for life for military, veterans, first responders and students. Rates sit behind their booking widget.",
  "https://bogeymastergolf.com/",
  [("bogey-1", "Green-lit simulator bays with players at Bogey Master in Hutto")]),

"drg": ("Dr. Golf Studio", "NW Austin &middot; $30&ndash;60/hr",
  "Six bays on Highway 183, and the split matters: Open Bays 1 through 4 are <strong>$30 an hour to the public and free to members</strong>, while Studio Bay 5 (TrackMan) and Bay 6 (GCQuad) are $60 to the public and $20 to members. There is an automatic ball feeder, which anyone who has spent an hour bending over a bucket will appreciate. Memberships run on promotional pricing through 9/30/26 with the $49 initiation waived &mdash; $90 a month single off-peak up to $270 family regular, plus tax. Lessons are $100 for members and $130 otherwise for fifty minutes. Four certified instructors, including a PhD who is also a PGA Class A general manager. No food, no bar, no bowling. That is the point.",
  "https://www.drgolfstudio.com/",
  [("drg-1", "A darkened practice bay and screen at Dr. Golf Studio"),
   ("drg-2", "A TrackMan unit positioned on the floor of a bay at Dr. Golf Studio")]),

"1872": ("1872 Golf Club", "Georgetown &middot; Foresight",
  "Four Foresight bays in Wolf Ranch, and the only new room in the metro running a real cocktail programme rather than a beer fridge. Members get 24/7; the public gets Monday to Friday 2 to 8, Saturday 12 to 8 and Sunday 12 to 6. Memberships are Eagle at $299 a month, Birdie at $250, and corporate tiers at $399, $699 and $1,399 for five, ten and twenty hours. Bring your own food or order through their catering partners. There is a junior programme for ages twelve to seventeen. Soft-opened 10/5/25, bar from 10/13, grand opening 11/1. They publish membership dues but not a public hourly rate.",
  "https://1872gc.com/",
  [("1872-1", "The bar and lounge at 1872 Golf Club in Georgetown, with screens above the stools"),
   ("1872-2", "A golfer mid-swing in a simulator bay at 1872 Golf Club"),
   ("1872-3", "A player lining up a shot in a bay at 1872 Golf Club")]),

"swing": ("Swing Station", "San Marcos &middot; $45&ndash;60/hr",
  "San Marcos had no indoor golf at all until Tyler and Laci Gescheidle opened this on 11/7/25. Full Swing, 85-plus licensed courses, <strong>$45 an hour Monday through Thursday and $60 Friday through Sunday</strong>, charged per bay rather than per player, with multi-hour discounts running from $20 to $60 off. Bring your own beer; there is no bar. It is also the most family-first room on this list &mdash; the multi-sport catalogue includes zombie dodgeball, which is exactly as advertised.",
  "https://swingstationgolf.com/",
  [("swing-1", "A golfer putting under the Swing Station sign in San Marcos"),
   ("swing-2", "The bay floor at Swing Station with multiple screens lit"),
   ("swing-3", "Two players in a bay at Swing Station, one mid-swing")]),

"aig": ("Austin Indoor Golf", "Pflugerville &middot; $25&ndash;35/hr",
  "Do not go looking for the Austin address you remember. This is now a <strong>single</strong> Full Swing bay on the mezzanine inside Pickleball Kingdom, and their own FAQ is blunt about it: &ldquo;we have one premium bay and prime slots go fast.&rdquo; It is also the cheapest staffed hour in the metro at <strong>$25 off-peak and $35 peak</strong>, and that rate covers the whole bay up to four players with no per-guest fee. Pro V1s and tees included; right-handed rental sets $20 and no left-handed sets at all. Memberships at $49.99, $149.99 and $249.99 carry Pickleball Kingdom perks. TABC licensed for beer, wine and seltzers; outside food explicitly welcome, outside alcohol not. One thing a guide should say plainly because they do: <strong>the bay is up a flight of stairs with no elevator and is not wheelchair accessible.</strong>",
  "https://www.austinindoorgolf.com/",
  [("aig-1", "The Pickleball Kingdom building in Pflugerville that houses Austin Indoor Golf upstairs"),
   ("aig-2", "The single Full Swing bay at Austin Indoor Golf with seating alongside"),
   ("aig-3", "A golfer mid-swing in the bay at Austin Indoor Golf")]),

"cave": ("Man Cave Golf Club", "Dripping Springs &middot; Members only",
  "Three TrackMan bays on Fitzhugh Road, 24/7 keycode, a climate-controlled lounge, and a club pro &mdash; Keith Rader, thirty-three years in the industry. Membership is <strong>$107.17 a month including tax</strong>, or $1,081.42 for the year, with thirty days&rsquo; notice to cancel. That is roughly a third of what the in-town clubs charge for unlimited access, and guest privileges are included at no extra cost, which is the only way a non-member gets through the door. Midland and Houston are listed as coming.",
  "https://mancavegolfclub.com/",
  [("cave-1", "The Man Cave Golf Club building and sign in Dripping Springs"),
   ("cave-2", "The darkened lounge and bay corridor inside Man Cave Golf Club")]),
}


def gallery(key, frames):
    fr = "\n        ".join(f'<img src="{IMG}{s}.jpg" alt="{a}" loading="lazy" />' for s, a in frames)
    if len(frames) == 1:
        # One honest photograph beats gallery chrome that goes nowhere.
        return f'<div class="product-gallery" data-gallery="{key}">\n' \
               f'      <div class="pg-frame"><div class="pg-track">\n        {fr}\n      </div></div>\n    </div>'
    dots = "".join(f'<span class="pg-dot{" on" if i == 0 else ""}"></span>' for i in range(len(frames)))
    return f"""<div class="product-gallery" data-gallery="{key}">
      <div class="pg-frame"><div class="pg-track">
        {fr}
      </div></div>
      <button class="pg-arw prev" aria-label="Previous">&#8249;</button>
      <button class="pg-arw next" aria-label="Next">&#8250;</button>
      <div class="pg-dots">{dots}</div>
      <div class="pg-count">1 / {len(frames)}</div>
    </div>"""


def card(key):
    brand, name, desc, url, frames = CARDS[key]
    return f"""<div class="product-card">
    {gallery(key, frames)}
    <div class="product-body">
      <div class="product-brand">{brand}</div>
      <div class="product-name">{name}</div>
      <div class="product-desc">{desc}</div>
      <a href="{url}" class="product-link" target="_blank" rel="noopener">Book a bay &#8599;</a>
    </div>
  </div>"""


def grid(keys):
    return '<div class="products-grid">\n    ' + "\n    ".join(card(k) for k in keys) + '\n  </div>'


def check():
    missing = []
    for k, (_b, _n, _d, _u, frames) in CARDS.items():
        for s, a in frames:
            if not os.path.exists(f"images/austin-sims/{s}.jpg"):
                missing.append(s)
            if len(a) < 25:
                raise SystemExit(f"alt text for {s} is too thin: {a!r}")
    if missing:
        raise SystemExit(f"card images missing on disk: {missing}")
    stems = [s for _k, v in CARDS.items() for s, _a in v[4]]
    if len(stems) != len(set(stems)):
        raise SystemExit("an image is used in two different cards")
    return len(CARDS), len(stems)


if __name__ == "__main__":
    n, f = check()
    print(f"{n} venue cards, {f} frames, all present and unique")
