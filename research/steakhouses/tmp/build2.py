import json
old={e['slug']:e for e in json.load(open('options.json'))}
ML="https://guide.michelin.com/us/en/texas/austin_2958315/restaurants/page/1"
NL="not listed (absent from the Michelin Austin listing, 44 restaurants, 2025 guide; loaded 30 Sep 2026). 2026 Texas selection announced 8 Oct 2026, recheck then"
INF={"outlet":"The Infatuation: The Best Steakhouses In Austin (Feb 2026)","url":"https://www.theinfatuation.com/austin/guides/best-steakhouses-austin"}
CHR={"outlet":"Austin Chronicle Best of Austin 2026 readers poll: Steak","url":"https://calendar.austinchronicle.com/best-of/2026/food-and-drink-readers-poll/steak-14085518"}
AOT={"outlet":"The Austinot: 10 Best Steakhouse Austin Spots (Jun 2026)","url":"https://austinot.com/best-austin-steakhouse"}
TRB={"outlet":"Tribeza: The Best Steakhouses in Austin","url":"https://tribeza.com/austin-city-guides/food/best-steakhouse-restaurants-in-austin/"}
def addrecs(e,extra):
    seen={r['url'] for r in e.get('recs',[])}
    for r in extra:
        if r['url'] not in seen: e.setdefault('recs',[]).append(r); seen.add(r['url'])
out=[]
def reuse(slug,ownership,ourl,mich,murl,extra=[],flags_add="",**kw):
    e=dict(old[slug]); e['ownership']=ownership; e['ownership_url']=ourl; e['michelin']=mich; e['michelin_url']=murl
    addrecs(e,extra)
    if flags_add: e['flags']=(e.get('flags','')+" | ROUND 2: "+flags_add).strip()
    e.update(kw); out.append(e)

reuse('jeffreys',"MML Hospitality (McGuire Moorman Lambert), Austin-based group (bought Jeffrey's 2011). NOTE: MML also runs Clark's Oyster Bar outside Austin (Houston, Aspen, Menlo Park, Montecito) plus Aspen restaurants. Kept because the editor cleared MML by name.","https://mmlhospitality.com/restaurants/",
  "MICHELIN Recommended (no star/Bib; Contemporary, Steakhouse; 2025 guide)","https://guide.michelin.com/us/en/texas/austin_2958315/restaurant/jeffrey-s",[INF,CHR,AOT,TRB],"Won Steak in the Chronicle 2026 readers poll. Only 2 usable own-site images.")
reuse('j-carvers',"Chef-owner John Carver (also Red Ash Italia and The Kimberly, both in Austin). Independent, Austin only.","https://austinfoodmagazine.com/red-ash-italia-opens-downtown/amp/",NL,ML,[INF,CHR,TRB])
reuse('red-ash-italia',"Chef John Carver with partners Larry Foles and Guy Villavaso (Z'Tejas/Eddie V's founders). One location, Austin only. Sister restaurant to J. Carver's.","https://austinfoodmagazine.com/red-ash-italia-opens-downtown/amp/",NL,ML,[INF,AOT,TRB])
reuse('vanhorns',"Berg & Sons Hospitality (Daniel Berg & Dylan Salisbury), Austin-based (Bill's Oyster, Teddy's). Not Benjamin Berg's Houston group. No locations outside Austin found.","https://beta2.communityimpact.com/austin/north-central-austin/dining/2025/08/26/new-york-inspired-vanhorns-steakhouse-opening-in-downtown-austin",NL,ML,[INF,CHR])
reuse('driskill-grill',"Restaurant in the historic Driskill hotel, relaunched 18 May 2026 as a steakhouse run by MML Hospitality (Austin-based; also has Clark's outside Austin, see Jeffrey's). Hotel one-off concept.","https://communityimpact.com/central-austin/dining/the-driskill-grill-and-bar-steakhouse-reopens-in-austins-historic-hotel/",NL+" (reopened after the 2025 selection)",ML)
reuse('alc-steaks',"Independent and family-owned since 1993. One location.","https://tribeza.com/austin-city-guides/food/best-steakhouse-restaurants-in-austin/",NL,ML,[CHR,AOT,TRB])
reuse('bartletts',"Owner Trey Wolslager (bought it 2023). Hillstone sold it to founder Bartlett in 2010, so it is NOT Hillstone. A second Austin location (301 W Riverside) is planned with MML Hospitality.","https://whatnow.com/austin/restaurants/bartletts-expanding-with-new-location-opening-in-former-threadgills-space/",NL,ML,[CHR],
  "Chronicle 2026 Steak finalist and Established Restaurant finalist.")
reuse('steiner-ranch-steakhouse',"Steiner family (Bobby Steiner) and partner Don Burdette, who also own Vaqueros Cafe & Cantina (both Austin addresses). Austin-only.","https://communityimpact.com/lake-travis-westlake/news/vaqueros-restaurant-opening-former-site-tres-amigos-restaurant-cantina/",NL,ML,[TRB])
reuse('ciclo',"Four Seasons Hotel Austin restaurant. Created with Richard Sandoval (multi-city group, still features it on his site), but Ciclo itself is a single Austin concept. The current FS page credits hotel chef Abril Callender.","https://www.fourseasons.com/austin/dining/",NL,ML,[],"Still no images: Four Seasons returns 403 to downloads. Steak prices not listed. Sandoval link is borderline. NOT recommended.")
reuse('buenos-aires-cafe',"Mother and daughter Reina Morris & Paola Guerrero-Smith. Two locations: E 6th (Austin) and Hill Country Galleria (Bee Cave, a separate city in the Austin metro).","https://www.eastsideatx.com/buenos-aires-cafe-reina-morris-paola-guerrero-smith/",NL,ML,[],"Second location in Bee Cave (outside Austin city limits, same treatment as Estancia/Leander). Editor's call. Parrilla side-thread, not a full steakhouse. NOT in recommended 12.")

new=[
{"slug":"jacobys","name":"Jacoby's Restaurant & Mercantile","style":"Family ranch-to-table Southern supper house on the Colorado River; own Jacoby Brand Beef (family-raised in Melvin TX, hormone/antibiotic free, dry-aged 21-28 days)","hood":"East Austin (East Cesar Chavez, riverfront)","address":"3235 East Cesar Chavez St., Austin, TX 78702",
 "dishes":[{"name":"STEAK FRITES (House Cut Fries & Smoked Tomato Aioli)","price":"MKT"},{"name":"DAILY BUTCHER'S CUT (Mashed Potatoes, Roasted Carrots & House Demi)","price":"MKT"},{"name":"CHICKEN FRIED STEAK (Mashed Potatoes, Arugula Salad & Black Pepper Gravy)","price":"$29"}],
 "hours":"Supper Wed-Thu 5-9pm, Fri-Sat 5-10pm; Brunch Sat-Sun 10am-2pm; closed Mon-Tue (consistent across own pages)",
 "reservations":"https://www.opentable.com/restref/client/?rid=290005&restref=290005 (suggested, not required; 12+ via Events page)",
 "status":"Open (supper menu 'Week of 06.25.26', menu #26-7412, on own site; no closure notice)","ownership":"Family-owned, owner/operator Adam Jacoby. The family also runs Jacoby Feed & Seed / ranch in Melvin TX (not a restaurant). One restaurant, Austin only.","ownership_url":"https://www.jacobysaustin.com/general-info/",
 "near_muni":"Butler Pitch & Putt ~10 min (est.); Morris Williams ~10-12 min (est.)","michelin":NL,"michelin_url":ML,
 "recs":[AOT,{"outlet":"Tribeza guide listing","url":"https://tribeza.com/guide/jacobys-restaurant-mercantile/"},{"outlet":"Austin Chronicle review 'Ranch Dressing' (2014)","url":"https://www.austinchronicle.com/food/2014-11-07/ranch-dressing"}],
 "url":"https://www.jacobysaustin.com/",
 "images":[{"path":"research/steakhouses/img/jacobys-1.jpg","label":"Overhead family-style spread on a barnwood table: sliced medium-rare roast beef on a white platter, mashed potatoes, cornbread, mac and cheese, green beans with feta, antler decor (own site, 2023 upload)"},
           {"path":"research/steakhouses/img/jacobys-2.jpg","label":"Candlelit dining table: blue mason-jar glasses, striped napkins, bud vases"},
           {"path":"research/steakhouses/img/jacobys-3.jpg","label":"Bar: reclaimed-wood ceiling, copper-penny backsplash, milk-glass pitchers, pendant lights, stools"}],
 "flags":"Menu image JATX-Supper-6.25.26 says 'Steaks available on a Nightly Basis. Butcher's Cut, please ask your server or call 512.366.5808', so steak cuts and prices aren't published (MKT). Read the menu image directly. Image 1 shows sliced roast beef, probably a roast/prime-rib-style cut, not a single grilled steak. The site has no grilled-steak photo. Southern comfort-food house more than a classic steakhouse; value: CFS $29, cheeseburger $24, BBQ meatloaf $25. 20% gratuity for 6+, max 3 payments per table. Riverside patio. Editor-requested inclusion."},
]
# subagent data
G={"slug":"garrison","name":"Garrison (Fairmont Austin)","style":"Post-oak live-fire hotel restaurant, steak & seafood, open kitchen","hood":"Downtown (Fairmont Austin, Red River St near Lady Bird Lake)","address":"101 Red River Street, Austin, TX 78701",
 "dishes":[{"name":"25 oz Texas Wagyu Ribeye","price":"not listed"},{"name":"40 oz Oak-Grilled Porterhouse","price":"not listed"}],
 "hours":"Tue-Wed 5-9pm; Thu-Sat 5-10pm; closed Sun-Mon (garrisongrill.com and fairmont-austin.com agree)",
 "reservations":"https://www.opentable.com/r/garrison-reservations-austin?restref=732598 (from Fairmont page); garrisongrill.com uses its own form",
 "status":"Open (Fairmont page updated Mar 2026; own site lists 22 Oct 2026 event)","ownership":"In-house restaurant of Fairmont Austin (Accor hotel). One-off concept; no other Garrison found.","ownership_url":"https://www.fairmont-austin.com/dine/garrison/",
 "near_muni":"Butler Pitch & Putt ~5-7 min (est.)","michelin":"MICHELIN Recommended (2025 guide; $$$$, American)","michelin_url":"https://guide.michelin.com/us/en/texas/austin_2958315/restaurant/garrison-1208859",
 "recs":[TRB,{"outlet":"Eater Austin: Destination-Worthy Hotel Restaurants (found via the restaurant's press page; Eater blocked to fetch)","url":"https://austin.eater.com/maps/best-hotel-restaurants-austin"}],
 "url":"https://www.garrisongrill.com/",
 "images":[{"path":"research/steakhouses/img/garrison-1.jpg","label":"Sliced char-grilled steak on greens with jus, grilled asparagus, pickled onion; octopus behind"},{"path":"research/steakhouses/img/garrison-2.jpg","label":"Private dining room: long wood table, blue leather chairs, gold geometric chandelier"},{"path":"research/steakhouses/img/garrison-3.jpg","label":"Old fashioned on the counter with the live fire blazing behind"}],
 "flags":"No prices on either own site (undated HTML menu). Forbes 4-Star per own site. Hotel concept, not a chain. Also on the menu: 7oz Texas Wagyu Petite Tender."}
H={"slug":"hestia","name":"Hestia","style":"Michelin-starred live-fire restaurant built around a 20-ft hearth; tasting menu or a la carte","hood":"Downtown (Warehouse District, W 3rd St)","address":"607 W 3rd Street, Austin, TX 78701",
 "dishes":[{"name":"30 day dry aged Texas Wagyu ribeye","price":"$143"},{"name":"Texas Wagyu bavette","price":"$68"}],
 "hours":"Tue-Thu & Sun 5:30-10pm; Fri-Sat 5:30-11pm; closed Mon (own site; matches Michelin page)",
 "reservations":"https://www.opentable.com/r/hestia-reservations-austin-2?restref=1031956",
 "status":"Open (current menus, valet info on own site)","ownership":"Emmer & Rye Hospitality Group (Kevin Fink, Tavel Bristol-Joseph), Austin-based. NOTE: the group has San Antonio (Pullman Market) and an announced Houston project, so it's an Austin group WITH locations outside Austin, same situation as MML.","ownership_url":"https://diningout.com/houston/austin-based-emmer-rye-hospitality-to-open-first-houston-restaurant-at-autry-park/",
 "near_muni":"Butler Pitch & Putt ~5 min (est.); Lions Municipal ~8-10 min (est.)","michelin":"MICHELIN One Star (2025 guide; page loaded)","michelin_url":"https://guide.michelin.com/us/en/texas/austin_2958315/restaurant/hestia",
 "recs":[{"outlet":"Texas Monthly: 12 Best Texas-Raised Wagyu Steaks (via Hestia press page)","url":"https://www.texasmonthly.com/bbq/best-texas-wagyu-steaks-and-more/"},{"outlet":"Austin American-Statesman/Austin360 review (2020)","url":"https://www.austin360.com/story/entertainment/dining/restaurant-reviews/2020/02/27/hestia-new-live-fire-restaurant-from-emmer-rye-is-austins-most-ambitious-restaurant/1625530007/"}],
 "url":"https://hestiaaustin.com/",
 "images":[{"path":"research/steakhouses/img/hestia-1.jpg","label":"Wood-fired hearth: burning logs, embers, cast-iron pans under the grate"},{"path":"research/steakhouses/img/hestia-2.jpg","label":"Tasting-menu snacks on a torched-wood tray (uni bite, tart, caviar coupe)"},{"path":"research/steakhouses/img/hestia-3.jpg","label":"Dining room: tufted leather booths looking into the open kitchen"}],
 "flags":"Contemporary live-fire fine dining, not a steakhouse (2 of 6 mains are steaks); undated a la carte page. Own-site images max 800px wide. Group-outside-Austin caveat: editor to confirm, since the rule says Austin-based groups are fine."}
D={"slug":"dai-due","name":"Dai Due","style":"Texas-only butcher shop & supper club: wild game, whole-animal, beef-tallow cooking","hood":"Cherrywood / Manor Road (East Austin)","address":"2406 Manor Road, Ste. A, Austin, TX 78722",
 "dishes":[{"name":"95 Day Dry-Aged TX Wagyu Ribeye 20oz","price":"$162"},{"name":"Nilgai Antelope Leg Filet","price":"$66"}],
 "hours":"check before you go: own site says dinner Tue-Sat 5-10pm, Sun 5-9pm, brunch Fri-Sun 10am-3pm, closed Mon; Michelin page shows no weekend dinner",
 "reservations":"https://resy.com/cities/atx/dai-due","status":"Open (sample dinner menu 'Dinner Example 8.19.26' on own site)",
 "ownership":"Chef Jesse Griffiths (co-owner Tamara Mayfield per press). Austin only. Spin-off Dai Due Taqueria was also Austin; current status unverified.","ownership_url":"https://www.daidue.com/press",
 "near_muni":"Morris Williams ~5 min (est.); Hancock ~7 min (est.)","michelin":"MICHELIN Bib Gourmand + Green Star (2025 guide; page loaded)","michelin_url":"https://guide.michelin.com/us/en/texas/austin_2958315/restaurant/dai-due",
 "recs":[AOT,{"outlet":"The Infatuation: Top 25 Restaurants in Austin","url":"https://www.theinfatuation.com/austin/guides/best-restaurants-austin"},{"outlet":"Austin American-Statesman 2024 Dining Guide","url":"https://www.statesman.com/story/entertainment/dining/2024/11/07/best-restaurants-in-austin-tx-2024-dining-guide/75572526007/"},{"outlet":"CultureMap Tastemaker Awards best chefs 2025","url":"https://austin.culturemap.com/news/restaurants-bars/tastemaker-awards-best-chefs-2025/"}],
 "url":"https://www.daidue.com/",
 "images":[{"path":"research/steakhouses/img/dai-due-1.jpg","label":"Charred bone-in beef ribs over pickled cabbage, nopales, cilantro (not a steak)"},{"path":"research/steakhouses/img/dai-due-2.jpg","label":"Busy dining room: wood tables, blue leather booths, brick counter"},{"path":"research/steakhouses/img/dai-due-3.jpg","label":"Brunch plate: biscuit, bacon, fried eggs, potatoes"}],
 "flags":"Butcher-shop supper pick, not a steakhouse: one headline steak on a menu that changes often ('for example purposes only'). Value: $26 Dry-Aged Longhorn Cheeseburger. Own-site photos are around 2017. 20% gratuity for 6+."}
J={"slug":"justines","name":"Justine's Brasserie","style":"Moody late-night French brasserie; steak frites is the signature","hood":"East Austin (East 5th St)","address":"4710 East 5th Street, Austin, TX 78702",
 "dishes":[{"name":"Steak Frites: Grass-fed Angus Ribeye (12oz, wood-grilled)","price":"$58"},{"name":"Steak Frites: Texas Wagyu NY Strip","price":"$75"}],
 "hours":"check before you go: homepage says open daily except Tuesday, 6-11pm weekdays, 6pm-12am weekends; the site also carries a stale COVID-era 5-10pm notice",
 "reservations":"https://www.opentable.com/r/justines-brasserie-reservations-austin?restref=278569 (walk-ins encouraged)","status":"Open (menu PDF Food-menu-update-61126 uploaded Sep 2026)",
 "ownership":"Owner Justine Gilcrease, independent. A sister cafe is coming to the Blanton Museum in Austin. No locations outside Austin.","ownership_url":"https://www.aol.com/news/justines-team-updates-timeline-sister-215031020.html",
 "near_muni":"Morris Williams ~8-10 min (est.)","michelin":NL,"michelin_url":ML,
 "recs":[CHR,AOT,{"outlet":"The Infatuation review","url":"https://www.theinfatuation.com/austin/reviews/justines-brasserie"}],
 "url":"https://justines1937.com/",
 "images":[{"path":"research/steakhouses/img/justines-1.jpg","label":"Steak frites: ribeye with herb butter, frites, ramekin of sauce"},{"path":"research/steakhouses/img/justines-2.jpg","label":"Packed red-walled dining room at night"},{"path":"research/steakhouses/img/justines-3.jpg","label":"Table spread: frites, mussels, pasta, red wine on marble"}],
 "flags":"Brasserie, not a steakhouse; Chronicle 2026 Steak finalist. 22-25% service charge for 6+. Photos from 2021 uploads."}
P={"slug":"parkside","name":"Parkside","style":"Sixth Street gastropub & raw bar: oysters plus wood-fired USDA Prime steaks","hood":"Downtown (East 6th St)","address":"301 E. Sixth St., Austin, TX 78701",
 "dishes":[{"name":"usda prime ribeye* (18oz)","price":"$67"},{"name":"usda prime tri-tip* (9oz)","price":"$38"}],
 "hours":"'OPEN DAILY AT 5:00PM' (no closing time on own site): check before you go","reservations":"https://www.opentable.com/r/parkside-reservations-austin?restref=41920 (own site; group site links Resy)",
 "status":"Open (reopened Mar 2024; menu image dated 26.7.28)","ownership":"Parkside Projects (chef Shawn Cirkiel), all Austin projects.","ownership_url":"https://www.parksideprojects.com/",
 "near_muni":"Butler Pitch & Putt ~5 min (est.)","michelin":NL,"michelin_url":ML,
 "recs":[AOT,{"outlet":"Austin Chronicle First Plates","url":"https://www.austinchronicle.com/first-plates/parkside-12137462/"}],
 "url":"https://www.parkside-austin.com/",
 "images":[{"path":"research/steakhouses/img/parkside-1.jpg","label":"Sliced tri-tip with roasted garlic and herb butter, red wine"},{"path":"research/steakhouses/img/parkside-2.jpg","label":"Dining room: exposed brick, leather banquettes, art"},{"path":"research/steakhouses/img/parkside-3.jpg","label":"Booths and tables by the 6th Street windows"}],
 "flags":"Gastropub; only two steaks. Wednesday half-off oysters + bubbles. Alternate pick."}
E={"slug":"estancia","name":"Estância Brazilian Steakhouse","style":"Southern-Brazilian churrascaria: gauchos carving rodízio meats tableside, salad bar","hood":"Arboretum / Northwest Austin","address":"10000 Research Blvd, Ste B, Austin, TX 78759",
 "dishes":[{"name":"Full Churrasco Experience (incl. PICANHA*, PRIME AGED RIBEYE*, PRIME FILET MIGNON*)","price":"$65 per person"},{"name":"GRILLED TOMAHAWK*","price":"$140"}],
 "hours":"check before you go: shared site footer Mon-Thu 11-3:30 & 5-10, Fri 11-3:30 & 5-10:30, Sat 11-10:30, Sun 11-9; Austin dinner PDF says Sat/Sun dinner from 4pm",
 "reservations":"https://resy.com/cities/austin-tx/venues/estancia-brazilian-steakhouse","status":"Open (menu PDF footer 'Updated 8.9.2026 - Austin TX')",
 "ownership":"Owner Ironi DaRosa (per press). TWO locations: Austin + Leander (2132 Raider Way, opened Jan 2026). Leander is a separate city.","ownership_url":"https://estancia.com/",
 "near_muni":"none within 10 min (est.)","michelin":NL,"michelin_url":ML,"recs":[TRB],
 "url":"https://estancia.com/",
 "images":[{"path":"research/steakhouses/img/estancia-1.jpg","label":"Churrasco grill: skewered meats over open flame"},{"path":"research/steakhouses/img/estancia-2.jpg","label":"12-seat private dining room (Austin)"},{"path":"research/steakhouses/img/estancia-3.jpg","label":"Salad bar with Grana Padano wheel"}],
 "flags":"BORDERLINE CHAIN RULE: second location in Leander (outside Austin city limits). Kept out of the recommended 12; editor's call. Only independent churrascaria option."}
out+= new+[H,G,D,J,P,E]
for i,e in enumerate(out,1):
    e['id']="R%02d"%i
    e.pop('menu_date',None)
keys=["id","slug","name","style","hood","address","dishes","hours","reservations","status","ownership","ownership_url","near_muni","michelin","michelin_url","recs","url","images","flags"]
out=[{k:e.get(k) for k in keys} for e in out]
EX=[
 {"name":"Fogo de Chão","reason":"National/international churrascaria chain","url":"https://fogodechao.com/ausrw/"},
 {"name":"Perry's Steakhouse & Grille (Downtown, Domain)","reason":"Houston-based chain, ~22+ locations in TX and other states","url":"https://perryssteakhouse.com/our-story/"},
 {"name":"CARVE American Grille","reason":"Perry's Restaurants concept (group has locations outside Austin)","url":"https://austin.culturemap.com/news/restaurants-bars/04-20-22-perrys-restaurants-carve-steakhouse-new-location-the-grove-central-austin/"},
 {"name":"Gyu-Kaku","reason":"Global yakiniku franchise (incl. Dallas, Houston)","url":"https://www.matthews.com/press-release/gyu-kaku-opens-first-location-in-austin-tx-in-the-satillo-development"},
 {"name":"Dean's Italian Steakhouse","reason":"White Lodging brand: Dean's in Charlotte, San Antonio, Indianapolis","url":"https://www.whitelodging.com/case-studies/deans-italian-steakhouse"},
 {"name":"BOA Steakhouse","reason":"Innovative Dining Group (LA) chain: West Hollywood, Santa Monica, Las Vegas, etc.","url":"https://communityimpact.com/south-central-austin/dining/california-based-boa-steakhouse-debuts-first-texas-location-in-downtown-austin/"},
 {"name":"Lonesome Dove Western Bistro","reason":"Tim Love's Fort Worth flagship plus Knoxville TN","url":"https://fortworth.culturemap.com/news/restaurants-bars/12-21-15-tim-love-lonesome-dove-knoxville-tennessee/"},
 {"name":"Aris","reason":"Sof Hospitality (Houston: Doris Metropolitan, Hamsa, Októ; Doris Metropolitan New Orleans)","url":"https://whatnow.com/austin/restaurants/refined-mediterranean-dining-coming-to-downtown-austin/"},
 {"name":"La Wagyeria","reason":"Miami-based brand (Miami flagship)","url":"https://www.opentable.com/r/la-wagyeria-miami"},
 {"name":"J-Prime Steakhouse","reason":"Original location in San Antonio","url":"https://austinchamber.com/blog/j-prime-celebrates-new-austin-location-with-ribbon-cutting"},
 {"name":"Bob's Steak & Chop House","reason":"Texas-based multi-city chain (Tribeza calls it a chain)","url":"https://tribeza.com/austin-city-guides/food/best-steakhouse-restaurants-in-austin/"},
 {"name":"III Forks","reason":"Multi-city steakhouse chain","url":"https://www.3forks.com/"},
 {"name":"Eddie V's","reason":"National chain (founded in Austin, now Darden)","url":"https://tribeza.com/austin-city-guides/food/best-steakhouse-restaurants-in-austin/"},
 {"name":"The Capital Grille / Ruth's Chris / Saltgrass / STK","reason":"National chains seen in source lists","url":"https://www.theinfatuation.com/austin/reviews/the-capital-grille-downtown-austin"},
 {"name":"Estância Brazilian Steakhouse","reason":"BORDERLINE: second location in Leander (outside Austin city). Kept in candidates, flagged, not recommended","url":"https://estancia.com/"},
 {"name":"Maie Day","reason":"CLOSED: South Congress Hotel shut 31 May 2026 (rebrand to The Standard); Infatuation/OpenTable mark it permanently closed","url":"https://communityimpact.com/austin/central-austin/business/2026/03/31/south-congress-hotel-to-undergo-renovations-during-months-long-closure"},
 {"name":"Salt & Time","reason":"CLOSED July 2024 (own site)","url":"https://www.saltandtime.com/about"},
 {"name":"Olamaie","reason":"CLOSED 19 Jul 2026","url":"https://www.kut.org/austin/2026-07-09/austin-tx-olamaie-restaurant-closing-michelin-star"},
 {"name":"Vince Young Steakhouse","reason":"CLOSED 24 Jan 2026","url":"https://austin.culturemap.com/news/restaurants-bars/food-news-vince-young-closing/"},
 {"name":"The Original Hoffbrau Steakhouse","reason":"Not open: own site says 'closed until further notice for renovations' (shut since 2022)","url":"https://www.hoffbrausteakhouseaustin.com/"},
]
json.dump(out+[{"excluded":EX}],open('options2.json','w'),indent=1,ensure_ascii=False)
import os
for e in out:
    for im in e['images']:
        p=im['path'].replace('research/steakhouses/','')
        if not os.path.exists(p): print('MISSING',p)
print(len(out),'entries')
