#!/usr/bin/env python3
"""One carousel per brand for the Gorpcore page.

REPLACES the earlier eight single-product galleries. Each of the ten brands on
/brands/tag/gorpcore now gets its own swipeable carousel showing four DIFFERENT
products from its range, plus a priced line-up beneath it. The point of the
change: a reader who has never heard of Sounder learns more from four Sounder
products than from one, and every brand on the page gets equal standing rather
than eight of ten being singled out.

EVERY PRICE HERE WAS READ FROM THE BRAND'S OWN STORE ON 9/17/26.
Four currencies appear because four currencies are what these brands charge:
  Sounder and Carhartt WIP   -> GBP   (British and European stores)
  Left of Field Golf         -> AUD   (Sydney; do NOT reuse the site's older
                                       USD figures, which do not reconcile)
  Odd Ritual                 -> ZAR   (Cape Town)
  everyone else              -> USD
Nothing is converted. A converted price is a price nobody is charging.

REALTREE CARRIES NO PRICES, deliberately. Realtree licenses a camouflage
pattern; it does not sell clothing. The pieces shown are PUMA Golf's, sold by
PUMA, and PUMA's storefront could not be read programmatically today, so rather
than print figures we could not verify this morning the entry describes the
pieces and points at our own drop post.

IMAGE RULE: every frame is a locally hosted file. Frames come from
images/gorpcore/ (fetched for this page) or from the brand's existing local
library under images/<brand>/.
"""

# (slug, brand, place, blurb, [(file stem or path, alt, product label, price)])
GORP_BRANDS = [

 ("sentinel-golf", "Sentinel Golf", "Minneapolis, MN",
  "The most literal answer on the page to what happens when outdoor materials science is pointed "
  "at golf. Sentinel organises its range by fabric rather than by feature list, builds to order, "
  "and lets the material carry the whole argument &mdash; laminate at the top, leather at the top "
  "of that, machined titanium at the bottom.",
  [("/images/sentinel-golf/basecamp-walker-black-dyneema-1.jpg",
    "Sentinel Golf Basecamp Walker carry bag in black Dyneema",
    "Basecamp Walker &middot; Black Dyneema", "$890"),
   ("/images/sentinel-golf/sorensen-walker-dark-nubuck-0.jpg",
    "Sentinel Golf Sørensen Walker in dark nubuck leather",
    "Sørensen Walker &middot; Dark Nubuck", "$1,750"),
   ("/images/sentinel-golf/1733-duffle-saltex-coyote-0.jpg",
    "Sentinel Golf 1733 duffle in coyote Saltex nylon",
    "Duffle &middot; Saltex Coyote", "$320"),
   ("/images/sentinel-golf/jimmy-bar-0.jpg",
    "Sentinel Golf Jimmy Bar titanium divot tool and bottle opener",
    "Jimmy Bar &middot; Grade 5 titanium", "$68")]),

 ("sounder", "Sounder", "London, United Kingdom",
  "Founded by the people behind Folk and Urban Golf, which shows in how little any of it "
  "announces itself. The outerwear is where Sounder does its best work, and it spans the full "
  "range of the category in one rail: a jacket that folds into its own pocket, a mountain-grade "
  "waterproof, Italian fleece, and a cotton hat with nothing technical about it whatsoever.",
  [("/images/gorpcore/sounder-pacmach-1.jpg",
    "Sounder Pac Mach Jacket in deep navy ripstop",
    "Pac Mach Jacket &middot; Deep Navy Ripstop", "&pound;145"),
   ("/images/gorpcore/sounder-protsp-1.jpg",
    "Sounder x Protected Species waterproof jacket in olive",
    "&times; Protected Species Waterproof &middot; Olive", "&pound;275"),
   ("/images/gorpcore/sounder-gilet-1.jpg",
    "Sounder Himalayas Gilet in grey Italian polar fleece",
    "Himalayas Gilet &middot; Grey", "&pound;145"),
   ("/images/gorpcore/sounder-bucket-1.jpg",
    "Sounder Star Bucket Hat in spice cotton",
    "Star Bucket Hat &middot; Spice", "&pound;40")]),

 ("left-of-field-golf", "Left of Field Golf", "Sydney, Australia",
  "Elements is where the technical work sits, and it came back with the team from a trip to "
  "Barnbougle. The naming follows that coastline &mdash; Anderson is the bay the course overlooks, "
  "Bridport the town beside it. "
  "It is the rare case where a naming convention tells you something real about how the clothes "
  "were designed. Prices are in Australian dollars, which is what the brand's own store charges.",
  [("/images/left-of-field/xelements-weather-jacket-sand-moss-2-0.jpg",
    "Left of Field Elements Weather Jacket in sand and moss",
    "Elements Weather Jacket &middot; Sand/Moss", "A$299"),
   ("/images/left-of-field/xanderson-insulated-vest-4-0.jpg",
    "Left of Field Anderson insulated gilet",
    "Anderson Insulated Gilet", "A$230"),
   ("/images/left-of-field/xbridport-wind-breaker-crew-neck-green-3-0.jpg",
    "Left of Field Bridport crewneck pullover in green",
    "Bridport Crewneck Pullover &middot; Green", "A$250"),
   ("/images/left-of-field/xelements-polo-0-0.jpg",
    "Left of Field Elements polo with yardage print",
    "Elements Polo", "A$140")]),

 ("ghost-golf", "Ghost Golf", "Irvine, CA",
  "Founded in 2020 around a patented magnetic towel, and the thinking has carried through the "
  "whole range: everything attaches, closes or stows in a way somebody clearly argued about. The "
  "Anyday runs to seven colourways at one price, which is a deliberate choice &mdash; the bag does "
  "not get better as it gets louder.",
  [("/images/gorpcore/ghost-kovert-1.jpg", "Ghost Golf Anyday Kovert Ops stand bag in matte black",
    "Anyday &middot; Kovert Ops", "$415"),
   ("/images/gorpcore/ghost-katana-1.jpg", "Ghost Golf Anyday Katana stand bag",
    "Anyday &middot; Katana", "$415"),
   ("/images/gorpcore/ghost-awol-1.jpg", "Ghost Golf AWOL golf travel bag",
    "AWOL&reg; Travel Bag", "$350"),
   ("/images/gorpcore/ghost-bladecover-1.jpg", "Ghost Golf Katana blade putter cover",
    "Blade Putter Cover &middot; Katana", "$50")]),

 ("sunday-golf", "Sunday Golf", "San Diego, CA",
  "The counterweight to everything else here. Sunday builds for the short course, the twilight "
  "nine and the walk where a full bag is more equipment than the round deserves, and prices it so "
  "that keeping a second, smaller setup is a reasonable thing to do rather than an indulgence.",
  [("/images/gorpcore/sunday-elcamino-1.jpg", "Sunday Golf El Camino mid-size stand bag in cool gray",
    "El Camino &middot; Cool Gray", "$200"),
   ("/images/gorpcore/sunday-blade-1.jpg", "Sunday Golf blade putter headcover in black",
    "Blade Putter Headcover &middot; Black", "$45"),
   ("/images/gorpcore/sunday-frosty-1.jpg", "Sunday Golf Big Frosty cooler in Mossy Oak Bottomland camo",
    "Big Frosty Cooler &middot; Mossy Oak Bottomland", "$40"),
   ("/images/gorpcore/sunday-elcamino-3.jpg", "Sunday Golf El Camino bag strap and pocket detail",
    "El Camino &middot; carry detail", "")]),

 ("gramicci", "Gramicci", "Est. 1982, Yosemite",
  "The oldest company on this page and the one that never set out to be here. Gramicci makes "
  "climbing clothes; golfers took them. The two details that matter are both structural and both "
  "date to the first pattern &mdash; a diamond gusset at the crotch and a webbing belt you work "
  "with one hand &mdash; and neither has needed revising in forty-odd years.",
  [("/images/gramicci/gramicci-pant.jpg", "Gramicci Pant in organic cotton twill",
    "Gramicci Pant", "$100"),
   ("/images/gramicci/g-short.jpg", "Gramicci G-Short climbing short",
    "G-Short", "$70"),
   ("/images/gramicci/taos-canvas-jacket.jpg", "Gramicci Taos canvas jacket",
    "Taos Canvas Jacket", "$127.50"),
   ("/images/gramicci/guide-cap.jpg", "Gramicci Guide Cap",
    "Guide Cap", "$65")]),

 ("odd-ritual", "Odd Ritual", "Cape Town, South Africa",
  "The workwear half of gorpcore rather than the technical half &mdash; heavy cotton twill, brass "
  "hardware, no membranes and no ratings. Named for the small habits players repeat before every "
  "shot, made locally in Cape Town, and priced in rand on its own store.",
  [("/images/odd-ritual/c03-caddie-jacket-navy.jpg", "Odd Ritual Caddie Jacket in navy cotton twill",
    "The Caddie Jacket &middot; Navy", "R3,200"),
   ("/images/odd-ritual/c03-crewneck-burgundy.jpg", "Odd Ritual ORGC Traditions crewneck in burgundy",
    "ORGC Traditions Crewneck &middot; Burgundy", "R2,100"),
   ("/images/odd-ritual/c03-heritage-polo.jpg", "Odd Ritual 1990s Heritage Polo",
    "1990s Heritage Polo", "R1,850"),
   ("/images/odd-ritual/c03-trouser-black.jpg", "Odd Ritual pleated daily trouser in black",
    "Pleated Daily Trouser &middot; Black", "R1,300")]),

 ("agronomy-workshop", "Agronomy Workshop", "San Francisco, CA",
  "Founded by Rob Junge on a single garment and a single idea: a mock-neck cotton shirt with room "
  "in the chest pocket for three tees. The range is still only four ideas wide and better for it "
  "&mdash; two weights of that shirt, hand-dyed and hand-sewn in Los Angeles, a rope cap with a "
  "slot for a pencil, and a terry towel whose print is a trompe-l&rsquo;oeil of creased brown "
  "paper, fake fold shadows included.",
  [("/images/gorpcore/agronomy-ss-shirt-1.jpg",
    "Agronomy Workshop short sleeve heavyweight work shirt in earth brown",
    "S/S Heavyweight Work Shirt", "$136"),
   ("/images/gorpcore/agronomy-ls-shirt-1.jpg",
    "Agronomy Workshop long sleeve heavyweight work shirt",
    "L/S Heavyweight Work Shirt", "$172"),
   ("/images/gorpcore/agronomy-treehat-1.jpg",
    "Agronomy Workshop five-panel rope hat in recycled nylon",
    "Tree Hat &middot; recycled nylon rope cap", "$64"),
   ("/images/gorpcore/agronomy-towel-1.jpg",
    "Agronomy Workshop Unusual Lies terry cotton golf towel",
    "Unusual Lies Towel", "$56")]),

 ("carhartt-wip", "Carhartt WIP", "Weil am Rhein, Germany",
  "The European arm, designing separately from the American workwear parent under a licence held "
  "since 1994. It earns a place here for one reason: the "
  "Chase Pique is quietly among the better casual polos you can take to a course, at a price the "
  "golf aisle does not often reach. Nothing in the range was designed for golf, which is the whole "
  "point of the adopted route in.",
  [("/images/gorpcore/carhartt-chase-black-1.jpg", "Carhartt WIP S/S Chase Pique Polo in black and gold",
    "S/S Chase Pique Polo &middot; Black/Gold", "&pound;50"),
   ("/images/gorpcore/carhartt-chase-white-1.jpg", "Carhartt WIP S/S Chase Pique Polo in white and gold",
    "S/S Chase Pique Polo &middot; White/Gold", "&pound;50"),
   ("/images/gorpcore/carhartt-wayne-1.jpg", "Carhartt WIP S/S Wayne Polo in dark navy, garment dyed",
    "S/S Wayne Polo &middot; Dark Navy", "&pound;75"),
   ("/images/gorpcore/carhartt-painter-1.jpg", "Carhartt WIP S/S Painter Polo in black with splatter wash",
    "S/S Painter Polo &middot; Black", "&pound;75")]),

 ("realtree", "Realtree &times; PUMA Golf", "Columbus, GA",
  "Realtree turns forty as a licensor rather than a clothing company: it owns the camouflage and "
  "partners with the people who cut the garments. This collection is PUMA Golf's, and it runs the "
  "full spread from a vest in head-to-toe Legacy pattern to a polo where the camo is confined to a "
  "collar tip. Prices sit with PUMA, so they are not printed here.",
  [("/images/realtree-puma/realtree-fleece-golf-vest-0.jpg",
    "Realtree x PUMA Golf fleece vest in Legacy camouflage",
    "Fleece Golf Vest", ""),
   ("/images/realtree-puma/realtree-helsinki-g-spikeless-golf-shoes-0.jpg",
    "Realtree x PUMA Golf HELSINKI G spikeless golf shoe",
    "HELSINKI G &middot; spikeless", ""),
   ("/images/realtree-puma/realtree-cloudspun-tech-golf-hoodie-0.jpg",
    "Realtree x PUMA Golf CLOUDSPUN tech hoodie",
    "CLOUDSPUN Tech Hoodie", ""),
   ("/images/realtree-puma/realtree-solid-golf-polo-0.jpg",
    "Realtree x PUMA Golf solid polo with camo collar tip",
    "Solid Golf Polo &middot; pattern at the collar", "")]),
]


# ---- every frame must exist on disk before this renders --------------------
import os as _os
_ROOT = _os.path.dirname(_os.path.abspath(__file__))
_missing = [f for _s, _b, _p, _bl, fr in GORP_BRANDS for f, *_ in fr
            if not _os.path.exists(_os.path.join(_ROOT, f.lstrip("/")))]
if _missing:
    raise SystemExit("tax_brands.py references image files that do not exist:\n  "
                     + "\n  ".join(_missing))
_dupes = [f for f in {f for _s, _b, _p, _bl, fr in GORP_BRANDS for f, *_ in fr}
          if sum(1 for _s, _b, _p, _bl, fr in GORP_BRANDS for g, *_ in fr if g == f) > 1]
if _dupes:
    raise SystemExit(f"the same frame is used twice: {_dupes}")


def _gallery(frames):
    slides = "".join(f'<div class="pg-frame"><img src="{f}" alt="{a}" loading="lazy"></div>'
                     for f, a, _l, _p in frames)
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
                   f'aria-label="Frame {i + 1}"></button>' for i in range(len(frames)))
    return (f'<div class="product-media" data-frames="{len(frames)}"><div class="product-gallery">'
            f'<div class="pg-track">{slides}</div>'
            f'<button class="pg-arw prev" aria-label="Previous">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next">&#8250;</button>'
            f'<span class="pg-count">1/{len(frames)}</span>'
            f'<div class="pg-dots">{dots}</div></div></div>')


def brands_section(rows):
    cards = []
    for slug, brand, place, blurb, frames in rows:
        lineup = "".join(
            f'<li><span>{label}</span>{f"<b>{price}</b>" if price else ""}</li>'
            for _f, _a, label, price in frames if label)
        cards.append(
            f'<article class="product-card brand-card">{_gallery(frames)}'
            f'<div class="product-body">'
            f'<div class="cat-kicker">{place}</div>'
            f'<h3><a href="/brands/{slug}">{brand}</a></h3>'
            f'<p>{blurb}</p>'
            f'<ul class="tx-lineup">{lineup}</ul>'
            f'<a class="tx-more" href="/brands/{slug}">All {brand} coverage &rarr;</a>'
            f'</div></article>')
    return ('<section class="tx-sec" id="picks">\n'
            '  <h2>Ten brands, four pieces each</h2>\n'
            '  <p class="tx-sec-lead">Swipe each carousel for four products from that brand&rsquo;s '
            'current range. Every price was read from the brand&rsquo;s own store on 9/17/26 and is '
            'printed in the currency that store charges &mdash; sterling for Sounder and Carhartt '
            'WIP, Australian dollars for Left of Field, rand for Odd Ritual &mdash; because a '
            'converted figure is one nobody is actually asking for.</p>\n'
            '  <div class="tx-picks">\n' + "\n".join(cards) + '\n  </div>\n</section>')
