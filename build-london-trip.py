#!/usr/bin/env python3
"""build-london-trip.py — Field Note: Drawing It Up, a five-day golf trip to London. 17 November 2026.
Lenny: "Let's build a field note- Drawing it up, a trip to London ... I want to play cool historic courses, see cool art, and shop
interesting stores, eat good food." Picks (17 Nov): 5 days; Sunningdale Old, The Addington, Royal Blackheath, Wimbledon Common,
Swinley Forest; Beyond the Streets at Saatchi, Leake Street tunnel, Design Museum Nue Black Aesthetic; TrendyGolf at Pitch Wharf,
Dover Street Market, Palace Soho; Rules, St. JOHN, Quality Chop House, Dishoom; plus Borough Market and Fallow. "Also let's see
which friends of TGI are worth reaching out to for a round."
v2 (17 Nov): "For the locations, let's do much larger more focused images and write ups. Review other field notes for the layout.
Let's make it more editorial and interesting." -> rebuilt on the Mind/Body/Spirit editorial chassis (build-mind-body-spirit.py):
full-bleed hero, intro with epigraph, day-by-day contents, a 21:9 opener per day, one long-form spread per stop with a 16:9 lead
image, a facts panel and a three-image mosaic. No product cards. No FAQ.
FACTS: official sites read 17 Nov 2026 (club visitor/green fee/history pages, Saatchi press release, Design Museum, Leake Street
Arches, Pitch Wharf venue page, restaurant sites, Borough Market). Sunningdale's own pages would not load beyond the homepage, so
its visitor days come from third-party listings and no fee is quoted. TrendyGolf store: Golf Retailing, Mar 2025. Palace Poland
Street: brand site + FAD Magazine, Nov 2026. GBP shown with approx USD at 0.752.
PHOTOS: each club's and venue's own (research/london-trip/g-sources.json, g-frames-script.py). Beyond the Streets: the installation
photography (David Owens) Hypebeast ran, per Lenny 17 Nov. v3 (17 Nov): Sunningdale -> Walton Heath (Sunningdale's site has a
broken certificate, no usable photos); Design Museum -> Tate Modern (Lenny: "I don't love 13"); swipe galleries; friends images.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Drawing It Up: A Five-Day Golf Trip to London"
DESC = ("The London golf trip I am drawing up for spring 2027: Royal Blackheath, Walton Heath, Swinley Forest, The Addington and "
        "Wimbledon Common, plus Beyond the Streets at Saatchi, Palace, Dover Street Market and where we would eat.")
H1 = "Field Note: Drawing It Up, a Golf Trip to London"
BC = "Drawing It Up: London"
SLUG = "london-golf-trip-drawing-it-up"
IMG = "/images/london-trip"
ED = IMG + "/g"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
FR = json.loads((ROOT / "research/london-trip/g-frames.json").read_text())
L = 'style="border-bottom:1px solid currentColor"'

# stop: (name, where line, url, link label, lead caption, paras[], facts{}, mosaic captions[])
S = {}
S["saatchi"] = ("Beyond the Streets", "Saatchi Gallery &middot; King&rsquo;s Road, Chelsea",
 "https://www.saatchigallery.com/press/release/beyond-the-streets-one-of-the-worlds-most-influential-contemporary-platforms-launches-an-all-new-exhibition-dedicated-to-street-culture", "Exhibition details",
 "Installation views of Beyond the Streets at Saatchi Gallery. Photos: David Owens, via Hypebeast.",
 ["This is the stop the whole trip is built around. Roger Gastman&rsquo;s Beyond the Streets has come back to the Saatchi Gallery with an all-new show: more than 100 artists across more than ten rooms of the Duke of York&rsquo;s HQ, tracing six decades of graffiti, hip-hop, 2Tone, fashion and protest.",
  "The details are what make it. Part of a New York subway car has been rebuilt inside the gallery. There is a history of graffiti on the London Underground, a spray-paint infinity room, early Polaroids of hip-hop stars from 1971, an archive of English football firms&rsquo; calling cards and 35 covers from The Big Issue. On the walls: KAWS, FUTURA 2000, LADY PINK, Kenny Scharf, Jenny Holzer, Shepard Fairey and Goldie.",
  "Gastman&rsquo;s first London show here in 2023 drew more than 150,000 people in three months, so we will book a morning slot and give it a few hours. The gallery shop is selling a 500-page catalogue for the show, which would be the one souvenir I&rsquo;d carry home."],
 {"Runs": "November 11, 2026 to May 5, 2027", "Hours": "10am&ndash;6pm daily, last entry 5pm", "Tickets": "From &pound;15 (~$20). Walk-ins welcome, booking advised",
  "Getting there": "Sloane Square station, then a short walk down the King&rsquo;s Road"},
 [])
S["shops"] = ("Palace and Dover Street Market", "8 Poland Street, Soho &middot; 18&ndash;22 Haymarket, St James&rsquo;s",
 "https://london.doverstreetmarket.com/", "Visit DSM",
 "Palace&rsquo;s new Poland Street flagship, outside and in, and its space inside Dover Street Market. Photos: Palace.",
 ["From Chelsea, east to Soho for the two best stores in town. Palace closed its original Brewer Street shop in September and opened a new London flagship around the corner on Poland Street on November 5, 2026. The press around the opening describes a store built from London references, with stained glass and raw oak seating, and it launched with a London-only Burberry collaboration and a run of pieces carrying the number eight for the address.",
  "Then a 10-minute walk south to Dover Street Market. Comme des Gar&ccedil;ons&rsquo; store left Dover Street for a bigger building on Haymarket in 2016 and kept the old name. It is less a shop than a rotating exhibition of the labels it rates, and Palace has its own space inside. Go in through the Orange Street entrance and work your way up.",
  "Between the two you see where the clothes golf keeps borrowing from are going next. Dinner is a few doors down."],
 {"Palace": "8 Poland Street, Soho. Opened November 5, 2026", "Dover Street Market": "18&ndash;22 Haymarket, entrance on Orange Street",
  "DSM hours": "Mon&ndash;Sat 11am&ndash;7pm, Sun noon&ndash;6pm", "Walk": "About 10 minutes between the two"},
 [])
S["fallow"] = ("Fallow", "52 Haymarket &middot; St James&rsquo;s",
 "https://fallowrestaurant.com/", "Book a table",
 "The counter at Fallow, facing the open kitchen. Photo: Fallow.",
 ["Dinner is a few doors down from Dover Street Market, so the shopping bags only have to travel one block. Fallow describes itself as &ldquo;creative cooking, sustainable thinking,&rdquo; and it is a certified B Corp. There is a long counter that faces straight into the kitchen.",
  "That counter is where we want to sit on the first night: watching the line work, sharing plates and keeping jet lag at bay. The same team runs Fowl and Roe, and their gift vouchers work at all three if a second visit happens."],
 {"Hours": "Mon&ndash;Fri 7:30am&ndash;11pm, Sat 9am&ndash;11pm, Sun 11:30am&ndash;10pm", "Book": "Online via SevenRooms", "Sit": "At the counter, if there is room"},
 ["One of Fallow&rsquo;s signature plates.", "The dining room.", "Bread and butter, done properly."])
S["blackheath"] = ("Royal Blackheath Golf Club", "Eltham, southeast London &middot; Thomas Dunn &middot; 1892",
 "https://royalblackheath.intelligentgolf.co.uk/green_fees", "Green fees and booking",
 "Royal Blackheath, with Eltham Lodge behind the green. Photo: Royal Blackheath Golf Club.",
 ["The club&rsquo;s story starts with a Scottish king. When James VI of Scotland became James I of England in 1603 and moved his court to Greenwich, his courtiers brought golf with them and played on the high ground at Blackheath. The club says it was &ldquo;instituted&rdquo; in 1608, and is honest that there is no paper to prove the date, because its accounts before 1787 are missing. What it can say for certain is that it is the oldest golf club in England.",
  "The clubhouse is Eltham Lodge, a Grade I house built in 1664 for the banker to Charles I. The club moved here from the heath in 1923, onto a course Thomas Dunn laid out in 1892 and James Braid later added to. Inside is a museum with the club&rsquo;s trophies, including the silver claret jug Blackheath won at St Andrews in 1857, the first time a claret jug was used as a golf trophy. The Spring Medal, first played here in 1792, is the oldest golfing medal in the world.",
  "The club&rsquo;s own aerial photo, the one that opens this post, has the City and Canary Wharf on the horizon. It is the most London round of the week, and at &pound;80 the best value."],
 {"Fee": "&pound;80 Mon&ndash;Thu (~$106), &pound;100 Fri (~$133), April 2026 rates", "Visitors": "Monday to Friday. Book online up to four weeks ahead",
  "Don&rsquo;t miss": "The golf museum in Eltham Lodge", "Where": "Eltham, southeast London"},
 ["The Royal Blackheath crest, carved in wood.", "The approach, with the 17th-century clubhouse behind.", "Heather and pines on the back nine."])
S["borough"] = ("Borough Market", "8 Southwark Street &middot; London Bridge",
 "https://boroughmarket.org.uk/visit-us/", "Plan a visit",
 "Borough Market at dusk, beside London Bridge station. Photo: Borough Market.",
 ["The train back from Eltham comes into London Bridge, and Borough Market is right outside the station. The sign over the entrance says established 1756, and it is free to walk in. Lunch is whatever looks best on the day.",
  "The market is in three parts: Three Crown Square for the bigger producers and merchants, the Green Market for small specialist traders and Borough Market Kitchen for street food. Come hungry and do a lap before buying anything. It is closed on Mondays, which is part of why this is a Tuesday."],
 {"Hours": "Tue&ndash;Fri 10am&ndash;5pm, Sat 9am&ndash;5pm, Sun 10am&ndash;4pm, closed Monday", "Cost": "Free to enter", "Getting there": "Right next to London Bridge station"},
 ["Cheese at the Market.", "The Green Market.", "Lunch crowd under the roof."])
S["leake"] = ("Leake Street Arches", "Beneath Waterloo Station",
 "https://www.leakestreetarches.london/", "Visit",
 "The tunnel under Waterloo, repainted constantly. Photo: Leake Street Arches.",
 ["After yesterday&rsquo;s gallery version, the real thing. A walk west along the river ends at the tunnel under Waterloo station, home to what the arches call London&rsquo;s longest legal graffiti wall. It started with a festival Banksy organised in 2008, and nothing on the walls lasts long.",
  "Anyone can bring a can and paint, and the official artists in residence run graffiti workshops. The arches also hold bars and restaurants: Passyunk Avenue, an American dive bar, and Draughts, a board-game caf&eacute; with more than 1,000 games. An afternoon beer underground before dinner is the plan."],
 {"Cost": "Free", "Paint": "Bring your own can, or book a workshop", "Drink": "Passyunk Avenue or Draughts, both in the arches",
  "Getting there": "Waterloo station, or a walk along the South Bank from Borough"},
 ["One of the murals in the tunnel.", "The tunnel on a weekday.", "Looking toward Waterloo."])
S["stjohn"] = ("St. JOHN Smithfield", "26 St John Street &middot; Clerkenwell",
 "https://stjohnrestaurant.com/restaurants/smithfield/", "Reserve",
 "The dining room at St. JOHN Smithfield. Photo: St. JOHN.",
 ["St. JOHN opened in 1994 in a derelict Georgian smokehouse beside Smithfield Meat Market, and to us it is still the reference point for eating in London. The idea was nose-to-tail cooking: every cut, the innards and the extremities that usually get thrown away, cooked simply and served in a plain white room.",
  "The menu is still written twice a day, every day, and the bread is baked each morning. Their own words for the place are &ldquo;simplicity, seasonality, and the whole beast.&rdquo; This is the dinner we would book first."],
 {"Opened": "1994", "Book": "Online, Smithfield location", "Order": "Whatever is on the board that night"},
 ["The kind of plate St. JOHN is known for.", "The bar.", "The menu, written twice a day."])
S["walton"] = ("Walton Heath, the Old Course", "Walton on the Hill, Surrey &middot; Herbert Fowler &middot; 1903",
 "https://waltonheath.intelligentgolf.co.uk/green_fees", "Green fees",
 "Walton Heath&rsquo;s Old Course in the heather. Photos: Walton Heath Golf Club.",
 ["The morning round is Walton Heath, and the history here is the best of the trip. The club was founded in 1903. The club lists King Edward VIII as its first captain, its first professional was James Braid, who won five Opens and stayed for some forty-five years, and Winston Churchill played here regularly. It hosted the Ryder Cup in 1981.",
  "Herbert Fowler designed the Old Course, and the club says it has been in the world&rsquo;s top 100 every year since the rankings began in 1938. It is open heathland under a big sky, longer than most of its neighbors with generally smaller greens, so it asks for what the club calls &ldquo;Scottish shots.&rdquo; Jack Nicklaus described the two courses as &ldquo;wonderfully pure.&rdquo;",
  "There is no halfway hut, so we will buy water before the 1st. Caddies are &pound;80 plus tip, paid in cash on the day, and the club has no cash machine. No handicap certificate is needed, only that visitors are competent golfers."],
 {"Fee": "&pound;275 Mon&ndash;Thu (~$366), &pound;350 Fri&ndash;Sun (~$465), April&ndash;November 2025 rates", "Visitors": "Weekdays from 9:30am, weekends from midday",
  "Caddies": "&pound;80 plus tip, cash only, book ahead", "Bring": "Water and snacks. There is no halfway hut"},
 [])
S["swinley"] = ("Swinley Forest Golf Club", "Ascot, Berkshire &middot; Harry Colt",
 "https://www.swinleyfgc.co.uk/Page/CustomPage?pageId=4920", "Visitor information",
 "A long par 4 through the pines at Swinley Forest. Photo: Swinley Forest Golf Club.",
 ["After lunch, west into Berkshire for the quieter round of the day. Harry Colt designed Swinley through pine and heather, and the club has stayed small and private. On weekdays it welcomes a limited number of visitors &ldquo;strictly by prior arrangement,&rdquo; so this is an email to the club office, not a booking page.",
  "The house rules are part of the experience. Tailored shorts are fine, but no collarless shirts, jeans or trainers. Phones stay in the car park or the changing room. Jackets are required in the upstairs dining room, where the club serves a carvery that looks out over the course. If we get the afternoon, it will be the most peaceful round of the trip."],
 {"Visitors": "Weekdays only, strictly by prior arrangement", "Contact": "office@swinleyfgc.co.uk, 01344 620197", "Dress": "Collared shirts, no jeans or trainers; jacket upstairs",
  "Phones": "Not on the course or in the clubhouse"},
 ["Heather and fairway.", "Pines and bunkering.", "The clubhouse."])
S["rules"] = ("Rules", "35 Maiden Lane &middot; Covent Garden",
 "https://rules.co.uk/", "Book a table",
 "The main dining room at Rules. Photo: Rules.",
 ["Back into town for the oldest restaurant in London. Thomas Rule opened it on Maiden Lane in 1798, and in more than two centuries it has had just four owning families. The cooking is traditional British with a focus on game.",
  "After 36 holes of heathland, this is the right kind of dinner: old paintings on the walls, white tablecloths and a cocktail bar for after."],
 {"Opened": "1798", "Known for": "Classic British cooking and game", "After": "The cocktail bar and its Winter Gardens room"},
 ["Game on the plate.", "The Winter Gardens.", "Paintings over the banquettes."])
S["addington"] = ("The Addington", "Croydon, Surrey &middot; J.F. Abercromby and Harry Colt &middot; 1913",
 "https://addingtongolf.com/visitors/", "Visitors and green fees",
 "The Addington in early light. Photo: The Addington Golf Club.",
 ["The closest of the great heathland courses to central London, and the one with a cult following. John Frederick Abercromby designed it with Harry Colt in 1913: pine, heather, rolling ground, light bunkering and a par of 69, with the city skyline in the background on many holes.",
  "Since 2020 the club has been restoring the course to how it looked originally, and the recent drone photography shows it. It is less famous than its Surrey neighbors, which is part of the appeal. Visitors book online every day of the week.",
  "Bring a camera. With the morning light coming through the pines and London on the horizon, it might give us the best photos of the trip."],
 {"Fee": "&pound;175 Mon&ndash;Thu (~$233), &pound;195 Fri&ndash;Sun (~$259)", "Par": "69", "Book": "Online", "Where": "205 Shirley Church Road, Croydon"},
 ["Pines and heather from above.", "The course from the air.", "Adirondack chairs by the fire pit."])
S["tate"] = ("Tate Modern", "Bankside &middot; Monet and Julio Le Parc",
 "https://www.tate.org.uk/whats-on/tate-modern/monet", "Book Monet",
 "Julio Le Parc and the gallery itself. Photos: Tate.",
 ["After the Addington, back up to Bankside. Tate Modern is free to walk into, and in late April it has two shows to plan around, from opposite ends of art history.",
  "Monet: Painting Time is the gallery&rsquo;s first exhibition devoted only to Claude Monet, with loans from around the world, including rarely seen works from private collections. It follows how Monet answered railways, the modern city and standardized time, from Arrival of the Normandy Train, Gare Saint-Lazare (1877) to the Poplars series and the Water Lilies he painted at Giverny.",
  "Then the opposite: the Julio Le Parc show, the Argentine artist&rsquo;s rooms of moving light, mirrors and color, on until May 3. After a morning in the heather, it is the most fun hour of the trip."],
 {"Monet": "February 25 to June 27, 2027. &pound;26 (~$35)", "Julio Le Parc": "Until May 3, 2027", "Hours": "10am&ndash;6pm Sun&ndash;Thu, until 9pm Fri&ndash;Sat",
  "Where": "Bankside, SE1. Free to enter the building"},
 [])
S["qch"] = ("The Quality Chop House", "94 Farringdon Road &middot; Clerkenwell",
 "https://thequalitychophouse.com/", "Book a table",
 "The Quality Chop House in an earlier era. Photo: The Quality Chop House.",
 ["A chop house since 1869, which turned 150 in 2019. The current owners say they are proud of the site&rsquo;s &ldquo;meaty&rdquo; past but don&rsquo;t lean on it, and the menu is modern British built on relationships with the best suppliers in the country.",
  "It is close to St. JOHN, and the two make a good pair of bookends to the week. Nathan Chapman runs the kitchen. Dinner is served until 9:45pm. Order the chop."],
 {"Since": "1869", "Dinner": "Mon&ndash;Sat 6pm&ndash;9:45pm", "Lunch": "Tue&ndash;Sat, and Sunday until 3:30pm", "Book": "OpenTable"},
 ["Dinner.", "The stairs.", "The team outside on Farringdon Road."])
S["wimbledon"] = ("Wimbledon Common Golf Club", "19 Camp Road, Wimbledon &middot; Founded 1908",
 "https://www.wcgc.co.uk/greenfees.html", "Green fees",
 "Wimbledon Common in summer. Photo: Wimbledon Common Golf Club.",
 ["The last round, and the most fun on paper. Wimbledon Common is a woodland course eight miles from central London that runs across public common land, shared with walkers, dogs and a second club, London Scottish. Because of that there is a local rule: every golfer wears a plain pillar-box red top so everyone else can see you coming.",
  "Forget yours and the club will sell or hire you one. No handicap certificate is needed, you just have to know the rules and etiquette. Denim is banned. Tee times open five days ahead online, and you pay when you arrive. The course closes at 2pm on Sundays so the public can use the common.",
  "At &pound;35 (~$47) it is the cheapest round of the week, and the best place to play with friends. If anyone from the list below joins us, this is the round."],
 {"Fee": "&pound;35 Mon&ndash;Fri (~$47), twilight &pound;25 (~$33). Saturday after 11:30am &pound;45 (~$60)", "Wear": "A plain pillar-box red top. No denim",
  "Book": "Online, five days ahead. Pay on arrival", "Handicap": "Not required"},
 ["Red tops on the first tee.", "Lining up a putt in red.", "The common in spring."])
S["trendy"] = ("TrendyGolf at Pitch Wharf", "30 Churchill Place &middot; Canary Wharf",
 "https://london.pitchgolf.com/venue/canary-wharf/", "Pitch Wharf",
 "Pitch Wharf, the indoor golf club where TrendyGolf has its first UK store. Photo: Pitch.",
 ["TrendyGolf has sold golf clothes online since 2004, and in 2025 it opened its first UK concept store inside Pitch Wharf. The store is 2,300 square feet. Malbon, Manors, G/FORE, J.Lindeberg and KJUS are on the rails, and FootJoy, Nike and Puma are on the shoe wall. Several of those brands are hard to find in person in the UK.",
  "Pitch Wharf is Pitch&rsquo;s flagship and its largest London venue: 11 Trackman bays, a bar and kitchen and a terrace on the water. Shop first, then book a bay and settle the week&rsquo;s bets on a simulator before dinner."],
 {"Where": "30 Churchill Place, E14 5RE", "Hours": "Fri 11am&ndash;10:30pm (Pitch Wharf)", "Bays": "11 Trackman bays. Book online",
  "Shop": "Malbon, Manors, G/FORE, J.Lindeberg, KJUS and more"},
 ["The TrendyGolf store.", "The shoe wall.", "The terrace."])
S["dishoom"] = ("Dishoom Covent Garden", "12 Upper St Martin&rsquo;s Lane &middot; Covent Garden",
 "https://www.dishoom.com/covent-garden/", "Visit",
 "The dining room at Dishoom Covent Garden. Photo: Dishoom.",
 ["The last night. Dishoom&rsquo;s Covent Garden caf&eacute; is built around 1949 Bombay and its picture houses, with old film posters and photographs on every wall. It is open all day, from breakfast until late.",
  "It is mostly walk-in, and after 6pm it only books groups of six or more, so we will expect a line. Waits can run 30 minutes to an hour, but they bring you chai while you wait and seat you at the bar first. On Fridays it stays open until midnight, which is exactly what the last night needs."],
 {"Hours": "Mon&ndash;Thu 8am&ndash;11pm, Fri&ndash;Sat 8am&ndash;midnight, Sun 9am&ndash;11pm", "Book": "Daytime any size; after 6pm groups of 6+", "Wait": "30 minutes to an hour on busy nights"},
 ["The table, mid-feast.", "Something from the grill.", "A corner of the caf&eacute;."])

DAYS = [
 ("day-1", "One", "Art and Shopping", "Chelsea, Soho and St James&rsquo;s",
  "Land, drop the bags and go straight to the show the trip is planned around. Then Palace&rsquo;s new flagship and Dover Street Market, and dinner at a counter on Haymarket.",
  "The Subway Art room at Beyond the Streets, Saatchi Gallery", ["saatchi", "shops", "fallow"]),
 ("day-2", "Two", "England&rsquo;s Oldest Club", "Eltham, London Bridge and Waterloo",
  "A morning round at the oldest golf club in England, lunch at Borough Market, an afternoon in the graffiti tunnel and dinner at St. JOHN.",
  "Royal Blackheath's 18th green and Eltham Lodge in evening light", ["blackheath", "borough", "leake", "stjohn"]),
 ("day-3", "Three", "36 Holes of Heathland", "Surrey and Berkshire",
  "The big day: Walton Heath in the morning, Swinley Forest after lunch, 36 holes of heathland, then the oldest restaurant in London.",
  "Heather and pines at Swinley Forest", ["walton", "swinley", "rules"]),
 ("day-4", "Four", "Abercromby and Monet", "Croydon, Bankside and Farringdon",
  "The closest great heathland course to the city, an afternoon at Tate Modern and dinner at a chop house that has been serving since 1869.",
  "Sunrise over The Addington", ["addington", "tate", "qch"]),
 ("day-5", "Five", "Red Tops and the Wharf", "Wimbledon, Canary Wharf and Covent Garden",
  "A round in red on Wimbledon Common, golf shopping and simulator bays by the water at Canary Wharf, and one last dinner.",
  "Wimbledon Common Golf Club in summer", ["wimbledon", "trendy", "dishoom"]),
]
ORDER = [k for d in DAYS for k in d[6]]
N = 16

SLOT = {
 "saatchi": ("Afternoon", "After landing"), "shops": ("Late afternoon", "Soho to Haymarket"), "fallow": ("Dinner", "Haymarket"),
 "blackheath": ("Morning", "Tee time"), "borough": ("Lunch", "London Bridge"), "leake": ("Afternoon", "Waterloo"), "stjohn": ("Dinner", "Smithfield"),
 "walton": ("Morning", "From 9:30am"), "swinley": ("Afternoon", "Second 18"), "rules": ("Dinner", "Covent Garden"),
 "addington": ("Morning", "Tee time"), "tate": ("Afternoon", "Bankside"), "qch": ("Dinner", "Farringdon"),
 "wimbledon": ("Morning", "Tee time, in red"), "trendy": ("Afternoon", "Canary Wharf"), "dishoom": ("Last night", "Covent Garden"),
}

SHORT = {"saatchi": "Beyond the Streets", "shops": "Palace and DSM", "blackheath": "Royal Blackheath", "leake": "Leake Street",
 "stjohn": "St. JOHN", "walton": "Walton Heath", "swinley": "Swinley Forest", "qch": "Quality Chop House",
 "wimbledon": "Wimbledon Common", "trendy": "TrendyGolf at Pitch", "dishoom": "Dishoom"}

PQ = {
 "saatchi": ("This exhibition is not about nostalgia or spectacle; it is about respect and truth.", "Roger Gastman, Beyond the Streets founder and curator"),
 "blackheath": ("We are, by birth, a Scottish club.", "Royal Blackheath Golf Club"),
 "swinley": ("Swinley welcomes a limited number of golfing groups and visitors strictly by prior arrangement.", "Swinley Forest Golf Club"),
}

INTRO = """
<section class="mbs-intro">
  <p class="mbs-epi">&ldquo;This is the epitome of golf, on open heathland, under a big sky.&rdquo;<span>&mdash; Walton Heath Golf Club</span></p>
  <div class="mbs-lede">
    <p>This one started with an art show. Beyond the Streets is back at the Saatchi Gallery until May 5, 2027, and once I saw it I started drawing up a trip around it. Nothing is booked yet. This is the plan on paper: five days in London with old golf courses, good art, interesting stores and long dinners.</p>
    <p>The golf is the reason to go. London is ringed by some of the oldest and best heathland golf in the world, and most of it takes visitors if you know how to ask. We would play the oldest club in England with the City on the horizon, give a full day to Walton Heath and Swinley Forest, play Abercromby&rsquo;s course at The Addington, and finish in a red shirt on Wimbledon Common, where the rules say you have to wear one.</p>
    <p>We are thinking late April 2027, Monday to Friday, before the show closes. Swinley only takes visitors on weekdays, Borough Market is closed Mondays and Royal Blackheath is weekdays only, which is how the days fell into this order. Below is every stop, what it costs, how to book it and why it is on the list.</p>
  </div>
</section>
"""

FRIENDS = f"""
<section class="mbs-solo">
  <h2 class="mbs-h2" id="friends">Friends of TGI on the Tee Sheet</h2>
  <p class="mbs-pill" style="text-align:left;margin:0 0 32px;padding:0;max-width:820px">A trip like this is better with locals. These are the British brands we have written about and would most like to play with while we are there. If that is you, the invite is open.</p>
  <div class="ld-friends">
    <a class="ld-fr" href="/brands/three-putt-golf-clothing"><img src="{FR['friend-three-putt']}" alt="Three Putt" loading="lazy" /><h3>Three Putt</h3><p>Graeme Whiles learned the game in his grandad&rsquo;s field and runs Three Putt from West Yorkshire. He reached out to us first, so he gets the first text.</p></a>
    <a class="ld-fr" href="/brands/parmore-golf"><img src="{FR['friend-parmore']}" alt="Parmore" loading="lazy" /><h3>Parmore</h3><p>&ldquo;No Membership Required,&rdquo; printed on half the range. That is the right attitude for a red-shirt round on Wimbledon Common.</p></a>
    <a class="ld-fr" href="/brands/manors"><img src="{FR['friend-manors']}" alt="Manors" loading="lazy" /><h3>Manors</h3><p>The London brand Jojo Regan and Luke Davies started in 2019, and it&rsquo;s on the rails at TrendyGolf. A round with them would be the trip&rsquo;s home game.</p></a>
    <a class="ld-fr" href="/brands/casualist"><img src="{FR['friend-casualist']}" alt="Casualist" loading="lazy" /><h3>Casualist</h3><p>The West London label that started in Melbourne as Casual Pro. Pleated trousers at Walton Heath feel right.</p></a>
    <a class="ld-fr" href="/brands/sounder"><img src="{FR['friend-sounder']}" alt="Sounder" loading="lazy" /><h3>Sounder</h3><p>London knitwear people since 2021. If late April is cold on the heath, we know who to call.</p></a>
    <a class="ld-fr" href="/brands/borde-golf"><img src="{FR['friend-borde']}" alt="Bord&eacute;" loading="lazy" /><h3>Bord&eacute;</h3><p>Tailored polos from St Albans, close enough to London to make The Addington.</p></a>
  </div>
  <p class="mbs-cap" style="margin-top:28px">Back home, this is what <a href="/events/social-club" {L}>the TGI Social Club</a> is for: small groups playing good courses around Austin, no dues.</p>
</section>
"""

MORE = f"""
<section class="mbs-solo" style="margin-top:72px">
  <h2 class="mbs-h2" id="more-time">If We Have More Time</h2>
  <div class="mbs-solo-grid" style="grid-template-columns:repeat(3,1fr)">
    <div><h3>A handroll lunch</h3><p><a href="https://www.timeout.com/london/restaurants/kumori" target="_blank" rel="noopener" {L}>Kumori</a> opened its first permanent handroll bar at 26 Denman Street in Soho, a few minutes from Palace.</p></div>
    <div><h3>A rainy day</h3><p>Pitch also has clubhouses in Soho and the City, so a wet afternoon can still be golf.</p></div>
    <div><h3>A can of paint</h3><p>Leake Street Arches runs graffiti workshops with its resident artists. If the walls get to us, we will book one.</p></div>
  </div>
</section>
"""

GLANCE = [
 ("1", "Beyond the Streets", "From &pound;15", "Online, walk-ins welcome"), ("1", "Palace / Dover Street Market", "&mdash;", "Walk in"), ("1", "Fallow", "&mdash;", "SevenRooms"),
 ("2", "Royal Blackheath", "&pound;80 (~$106)", "Online, 4 weeks out"), ("2", "Borough Market / Leake Street", "Free", "Walk in"), ("2", "St. JOHN", "&mdash;", "Book early"),
 ("3", "Walton Heath Old", "&pound;275 (~$366)", "Call reception"), ("3", "Swinley Forest", "Ask the club", "Email the office"), ("3", "Rules", "&mdash;", "Book early"),
 ("4", "The Addington", "&pound;175 (~$233)", "Online"), ("4", "Tate Modern: Monet", "&pound;26 (~$35)", "Online"), ("4", "Quality Chop House", "&mdash;", "OpenTable"),
 ("5", "Wimbledon Common", "&pound;35 (~$47)", "Online, 5 days out"), ("5", "TrendyGolf / Pitch Wharf", "Bays extra", "Online"), ("5", "Dishoom", "&mdash;", "Walk in, expect a line"),
]

CSS_EXTRA = """<style>/*TGI-LONDON*/
.mbs-toc.ld{grid-template-columns:repeat(5,1fr)}
.mbs-toc.ld>div{padding:22px 20px}
.mbs-toc.ld h3{font-size:16px}
.mbs-toc.ld li{font-size:15px}
.ld-noimg{border:.5px solid var(--ink);background:rgba(45,74,43,.06);aspect-ratio:21/9;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.ld-noimg .a{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.16em;font-size:clamp(34px,6vw,84px);color:var(--grass);line-height:1}
.ld-noimg .b{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-top:14px}
.mbs-mos.one{grid-template-columns:1fr;grid-template-rows:1fr;height:min(56vw,640px)}
.mbs-mos.one figure:first-child{grid-row:auto}
.ld-fig{margin:0}
.ld-stop{margin-top:72px}
.ld-slot{border-left:3px solid var(--grass);padding:4px 0 4px 14px;min-width:150px}
.ld-slot b{display:block;font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--grass)}
.ld-slot span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:4px}
.ld-strip{max-width:1036px;margin:32px auto 0;padding:0;display:flex;border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}
.ld-strip a{flex:1;padding:16px 18px;border-bottom:none!important;border-right:.5px solid rgba(20,20,20,.2)}
.ld-strip a:last-child{border-right:none}
.ld-strip b{display:block;font-family:var(--mono);font-weight:500;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--grass)}
.ld-strip span{display:block;font-family:var(--serif);font-size:17px;line-height:1.3;margin-top:6px}
.mbs-toc.ld li{padding:8px 0}@media(min-width:901px) and (max-width:1200px){.mbs-toc.ld p{min-height:2.8em}}.mbs-toc.ld li span{display:block;margin:0 0 3px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);opacity:.8}.mbs-toc.ld li a{display:block;line-height:1.3}
.ld-gal{aspect-ratio:16/10;border:.5px solid var(--ink)}
.ld-gal .pg-arw{width:46px;height:46px;font-size:22px}
.ld-fig figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.ld-friends{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.ld-fr{display:block;border-bottom:none!important}
.ld-fr img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;margin-bottom:14px}
.ld-fr h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:8px}
.ld-fr p{font-family:var(--serif);font-size:16px;line-height:1.55}
@media(max-width:900px){.mbs-toc.ld{grid-template-columns:1fr 1fr}.ld-friends{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.ld-stop .mbs-c-hd{grid-template-columns:1fr;gap:14px}.ld-strip{flex-direction:column;margin-left:18px;margin-right:18px}.ld-strip a{border-right:none;border-bottom:.5px solid rgba(20,20,20,.2)!important}.ld-gal{aspect-ratio:4/3}.mbs-open h2{font-size:30px;letter-spacing:.08em;overflow-wrap:anywhere}.mbs-open{overflow:hidden}.mbs-toc.ld,.ld-friends{grid-template-columns:1fr}.mbs-mos.one{height:auto}.mbs-mos.one figure:first-child{aspect-ratio:4/5}.ld-noimg{aspect-ratio:4/3}}
</style>
"""


def mbs_css():
    src = (ROOT / "build-mind-body-spirit.py").read_text(encoding="utf-8")
    return src[src.index('CSS = """') + 9:src.index('</style>\n"""', src.index('CSS = """')) + 9]


def stop_html(k, n, flip):
    name, where, url, lab, lcap, paras, facts, mcaps = S[k]
    fr = FR[k]
    fx = "".join(f'<div class="k">{lbl}</div><div class="v">{v}{"" if v.endswith((".", ")")) else "."}</div>' for lbl, v in facts.items())
    text = "".join(f"<p>{p}</p>" for p in paras)
    alt = H.escape(H.unescape(name), quote=True)
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{alt}, photo {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    if len(fr) > 1:
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="Photo {j+1}"></button>' for j in range(len(fr)))
        ctrl = (f'<button class="pg-arw prev" aria-label="Previous photo">&#8249;</button>'
                f'<button class="pg-arw next" aria-label="Next photo">&#8250;</button>'
                f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>')
    else:
        ctrl = ""
    gal = (f'  <figure class="ld-fig" data-frames="{len(fr)}"><div class="product-gallery ld-gal"><div class="pg-track">{imgs}</div>{ctrl}</div>'
           f'<figcaption>{lcap}{" Swipe for more." if len(fr) > 1 else ""}</figcaption></figure>\n')
    q = ""
    if k in PQ:
        qq, who = PQ[k]
        q = (f'\n<div class="pull-quote" style="margin:72px auto 0"><div class="pull-quote-inner">&ldquo;{qq}&rdquo;'
             f'<span class="pull-quote-attr">&mdash; {who}</span></div></div>\n')
    ext = ' target="_blank" rel="noopener"'
    return (f'\n<article class="mbs-c ld-stop" id="{k}">\n  <div class="mbs-c-hd"><div class="ld-slot"><b>{SLOT[k][0]}</b><span>{SLOT[k][1]}</span></div><div><h3>{name}</h3>'
            f'<div class="where">{where}</div></div></div>\n{gal}'
            f'  <div class="mbs-body"><div class="mbs-text">{text}</div><aside class="mbs-facts">{fx}'
            f'<a class="go" href="{url}"{ext}>{lab} &#8599;</a></aside></div>\n</article>\n{q}')


def day_strip(ids):
    cells = "".join(f'<a href="#{k}"><b>{SLOT[k][0]}</b><span>{SHORT.get(k, S[k][0])}</span></a>' for k in ids)
    return f'<nav class="ld-strip" aria-label="The day">{cells}</nav>\n'


def toc_html():
    cols, n = [], 1
    for key, num, name, place, _, _, ids in DAYS:
        lis = ""
        for k in ids:
            lis += f'<li><span>{SLOT[k][0]}</span><a href="#{k}">{SHORT.get(k, S[k][0])}</a></li>'
            n += 1
        cols.append(f'<div><h3><a href="#{key}" style="border-bottom:none">Day {num}</a></h3><p>{name}</p><ol>{lis}</ol></div>')
    return f'\n<nav class="mbs-toc ld" aria-label="The five days">{"".join(cols)}</nav>\n'


def glance_html():
    rows = "".join(f'<tr><td class="p">Day {d}</td><td>{s}</td><td>{c}</td><td>{b}</td></tr>' for d, s, c, b in GLANCE)
    return (f'\n<section class="mbs-table"><h2 class="mbs-h2" id="at-a-glance">The Plan at a Glance</h2><table><thead><tr>'
            f'<th>Day</th><th>Stop</th><th>Cost</th><th>Book</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<p class="mbs-cap" style="margin-top:12px">Green fees for the four courses with published rates come to about &pound;565 (~$751) a person, before Swinley, using the latest published rates. Prices checked November 17, 2026; USD at &pound;1 = $1.33.</p></section>\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": S[k][2], "name": H.unescape(S[k][0])} for i, k in enumerate(ORDER)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-17", "dateModified": "2026-11-17",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t} | The Grassy Issue</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    assert len(ORDER) == N == len(set(ORDER)) and set(ORDER) == set(S), set(S) ^ set(ORDER)
    for k in ORDER:
        for f in FR[k]:
            assert (ROOT / f.lstrip("/")).is_file(), f
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Field Note</span><span class="dot"></span>
    <span>London, Surrey and Berkshire</span><span class="dot"></span>
    <span>5 days &middot; 5 rounds &middot; checked November 17, 2026</span>
  </div>
</header>

<div class="mbs-hero"><img src="{IMG}/hero.jpg" alt="Royal Blackheath Golf Club at sunset with the London skyline on the horizon" fetchpriority="high" />
<div class="mbs-cap">Royal Blackheath at sunset, with the City and Canary Wharf on the horizon. Photo: Royal Blackheath Golf Club</div></div>
"""
    body += INTRO + toc_html()
    n = 1
    for key, num, name, place, para, alt, ids in DAYS:
        body += (f'\n<section class="mbs-open" id="{key}"><img src="{ED}/open-{key}.jpg" alt="{H.escape(alt, quote=True)}" loading="lazy" />'
                 f'<div class="t"><div class="n">Day {num} &middot; {place}</div><h2>{name}</h2></div></section>\n'
                 f'<p class="mbs-pill">{para}</p>\n' + day_strip(ids))
        for j, k in enumerate(ids):
            body += stop_html(k, n, j % 2 == 1)
            n += 1
    body += glance_html() + FRIENDS + MORE
    css = mbs_css() + CSS_EXTRA
    out = head_top() + head_rest.replace("</head>", css + "</head>", 1) + body + tail
    print(f"  {n-1} stops")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="mbs-c ld-stop"') != N: bad.append("stop count")
    txt = re.sub(r"<[^>]+>", " ", above)
    if re.search(r"\b(worth|genuinely|honestly|straightforward|selling out|grey|colour|favourite|centre)\b", txt, re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
