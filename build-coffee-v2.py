#!/usr/bin/env python3
"""Build the Austin coffee roundup (Vol. 2) from the Students Golf chassis."""
import re, os, glob, json, html

SLUG="fourteen-independent-austin-coffee-shops"
TITLE="Fourteen Independent Austin Coffee Shops We Keep Going Back To"
DESC=("The independent Austin coffee shops we actually use — Radio, Desnudo, Mozart's, Epoch and ten more, "
      "plus two that opened in the last year. Addresses, hours quirks and what each room is good for.")

REGULARS=[
 ("radio","Radio Coffee &amp; Beer","South Austin &middot; 4204 Menchaca Rd","https://radiocoffeeandbeer.com/",
  "Jack Wilson opened it with his father Greg in 2014, in a renovated 1940s house off Menchaca. The room turns over from coffee bar to beer bar without ever changing rooms, and it stays open to midnight, which is rare for a coffee room in Austin. They roast under their own label, RCB Roasters. Two more followed &mdash; Radio/East on Montopolis in 2023, on roughly two acres with three stages and a row of food trucks, and Radio Rosewood on East 11th in early 2025, in the space Try Hard Coffee left behind."),
 ("desnudo","Desnudo Coffee","East Austin &middot; 2505 Webberville Rd","https://desnudocoffee.com/",
  "Brothers Juan and Sergio Trujillo grew up in Huila, in Colombia&rsquo;s coffee and cacao country, and started here in 2022 with a single walk-up trailer on Webberville. It is now four locations. They buy direct with no intermediaries and name the farms on the bag, and they run an education program alongside the cafes. <em>Desnudo</em> means naked &mdash; the idea being the flavour stripped back to what the farm actually grew. Everything shuts by mid-afternoon."),
 ("mozarts","Mozart&rsquo;s Coffee Roasters","Lake Austin &middot; 3825 Lake Austin Blvd","https://mozartscoffee.com/",
  "The first on-premises coffee roaster in Austin, opened June 1993 by four local couples who brought in the German roasting consultancy Probat to spec the equipment. The draw has never really been the coffee: it is the multi-deck terrace hanging over Lake Austin, which at sunset is one of the better seats in the city. It was also the first shop in town to put in free wifi and a bottomless cup. A mile from Lions Muny, which makes it the default after a morning loop."),
 ("flitch","Flitch Coffee","East Austin &middot; 641 Tillery St","http://www.flitchcoffee.com/",
  "A remodeled 1952 Spartan trailer parked on a lot it shares with Harvest Lumber Company, a working sawmill. The name is the giveaway &mdash; a flitch is a slab cut from a log &mdash; and stacks of milled timber sit a few feet from where you order. Deliberately multi-roaster: Creature, Proud Mary and Onyx rotate through. Seven to three, every day, with live music on the lot often enough that you should check the calendar before you go."),
 ("cosmic","Cosmic Coffee + Beer Garden","South Austin &middot; 121 Pickle Rd","https://www.cosmichospitalitygroup.com/cosmiccoffee",
  "Paul Oveisi, an Austin native, opened this with Patrick Dean in January 2018, and the acre behind the building is the whole point. It is a certified wildlife habitat with an ecological pond, rainwater catchment and its own irrigation, plus a 1900s horse-drawn carriage repurposed as a chicken coop. Coffee in the morning, food trucks and beer by evening, and enough shade that it stays usable deep into an Austin summer."),
 ("epoch","Epoch Coffee","North Loop &middot; 221 W North Loop Blvd","https://epochcoffee.com/",
  "The 24-hour room, open since 2006 and running around the clock every day but Monday night. Co-owned by Randi Hensley, head roaster Chris Clarkson, Kevin Gary and Joe Rodriguez, roasting in-house on a Bellwether, and a long-standing hub for Austin&rsquo;s LGBTQIA+ community. There are other Epochs now, but only North Loop keeps the all-night clock. A mile and a half from Hancock, so it covers both an early tee time and whatever happens after."),
 ("cherrywood","Cherrywood Coffeehouse","Cherrywood &middot; 1400 E 38&frac12; St","https://cherrywoodcoffeehouse.com/",
  "A neighbourhood institution since 2009, co-owned by Jen Haberman, and much more restaurant than the name suggests: full brunch, a vegetarian and vegan menu, and 25 craft beers on tap. The shaded back yard and dog patio do the heavy lifting, and there is live music often. Open until nine most nights and ten on Saturday. The closest thing Morris Williams has to a clubhouse a mile and a half away."),
 ("jos","Jo&rsquo;s Coffee","South Congress","https://joscoffee.com/",
  "The original South Congress walk-up, open since 1999, and the wall everyone photographs. The &ldquo;i love you so much&rdquo; mural was sprayed on the side in 2010 by the musician Amy Cook after an argument with Liz Lambert, the hotelier who redeveloped the San Jos&eacute; next door; it was vandalised in January 2011 and restored within weeks. Jo&rsquo;s has since expanded south and into a modernist room at Symphony Square, but the SoCo counter is still the one."),
 ("fleet","Fleet Coffee","East Austin &middot; 2427 Webberville Rd","https://fleetcoffee.com/",
  "Four small rooms, each with a nickname &mdash; the Manor Road one is called The Long Goodbye &mdash; and a menu built around made-from-scratch signature drinks rather than a straight espresso card. They roast, and they also pour guest coffee from Sweet Bloom out of Colorado, which is a more honest way to run a bar than most. The newest is on Rainey."),
 ("buzzmill","The Buzz Mill","East Riverside &middot; 1505 Town Creek Dr","https://www.buzzmillcoffee.com/",
  "Open 24 hours a day since 2013, which is the entire pitch and a genuinely useful one. Coffee shop and full bar in the same lumber-camp room, with house-infused liquors and a large patio. After Radio/East it is the nearest independent coffee to Jimmy Clay and Roy Kizer, and it is the only one of the fourteen you can use at four in the morning."),
 ("flattrack","Flat Track Coffee","East Cesar Chavez &middot; 1619 E Cesar Chavez St","https://flattrackcoffee.com/",
  "Started in 2012 by Sterling Roberts and Matt Bolick, two friends out of BMX, first as a pop-up and then as a 150-square-foot kiosk in the back of Farewell Books. A $30,000 Kickstarter moved them up Cesar Chavez, where they now share a roof with the custom bike shop Cycleast. Roasting has shifted to their sister operation Palomino, which freed up the floor for people to actually sit down."),
 ("onceover","Once Over Coffee Bar","Bouldin Creek &middot; 2009 S 1st St","https://www.onceovercoffeebar.com/",
  "Jen&eacute;e and Rob Ovitt opened this in March 2009, and the back patio sits directly over East Bouldin Creek &mdash; an actual shaded creek deck, which is close to unheard of this near the centre of town. They pour Wild Gift, the local roaster, and keep a rotating pastry case with gluten-free and vegan options."),
]

NEW=[
 ("leona","Leona Botanical Caf&eacute; &amp; Bar","Sunset Valley &middot; 6405 Brodie Ln &middot; Opened Nov 2025","https://www.leonacafebar.com/",
  "The most ambitious opening of the year: Lakana and Justin Trubiana of DEE DEE joined the sisters Maritza and Reyna V&aacute;zquez of Veracruz All Natural, and the two Austin trucks went brick-and-mortar together on a five-acre site. There is a garden and a pavilion, designed by Clayton Korte, and the kitchen runs from 7:30 in the morning to eleven at night. It is a caf&eacute; and a bar in equal measure, which is the only caveat &mdash; go early for the coffee half."),
 ("cuvee","Cuv&eacute;e Coffee at The Code","Zilker &middot; 2323 S Lamar Blvd &middot; Opened Aug 2026","https://cuveecoffee.com/",
  "Cuv&eacute;e has been roasting in Austin since 1998, and after losing the East Sixth flagship in 2024, Mike and Rashelle McKim put the new one on South Lamar in the ground floor of The Code, which itself only opened in March. Espresso and nitro cold brew through the day, then wine, local beer and cocktails in the evening. The beans are direct-trade out of Brazil, Ethiopia, Colombia and El Salvador."),
]

def frames(slug):
    n=1
    while os.path.exists(f"images/austin-coffee-v2/{slug}-a{n+1}.jpg"): n+=1
    return n

def gallery(slug,name):
    n=frames(slug); plain=re.sub(r'<[^>]+>','',name)
    if n==1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="/images/austin-coffee-v2/{slug}.jpg" alt="{plain} &middot; Austin coffee shop" loading="lazy" /></div></div></div>')
    fr="".join(f'<div class="pg-frame"><img src="/images/austin-coffee-v2/{slug}{"" if i==0 else f"-a{i+1}"}.jpg" '
               f'alt="{plain} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots="".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def card(slug,name,meta,url,desc):
    return f"""<div class="product-card" data-frames="{frames(slug)}">
      {gallery(slug,name)}
      <div class="product-body">
        <div class="product-brand">{meta}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Visit ↗</a>
      </div>
    </div>"""

INTRO="""<div class="writeup">
  <div class="writeup-body">
    <p>Fourteen independent coffee shops in Austin, all locally owned, no chains, spread from Sunset Valley to Cherrywood. Twelve have been open for years. Two arrived in the last twelve months and earned their place immediately.</p>
    <p>It started as a practical problem. Austin&rsquo;s municipal courses open early and the good tee times are gone by mid-morning, which means most rounds here begin and end around coffee. Over a few years of that you stop caring which shop has the most elaborate pour-over and start caring which one is open at six, which one has shade in August, and which one you can sit in for two hours after a bad nine without anyone minding.</p>
    <p>So that is what this is sorted for. Where each room actually is, what it is good for, and the quirks to know before you drive &mdash; the ones that close at three, the two that never close at all, and the handful with enough tree cover to survive a Texas summer. If you play the munis, the proximity notes will matter. If you just live here, they won&rsquo;t, and the list still holds.</p>
  </div>
</div>
"""

def section(hdr,kicker,items):
    cards="\n    ".join(card(*i) for i in items)
    return f"""<section class="products">
  <h2 class="products-hdr">{hdr}</h2>
  <p class="cat-kicker">{kicker}</p>
  <div class="products-grid">
    {cards}
  </div>
</section>
"""

FAQ_ITEMS=[
 ("Which Austin coffee shops are open 24 hours?",
  "Two of them. Epoch Coffee on North Loop runs around the clock every day except Monday midnight to Tuesday 6am, and The Buzz Mill on Town Creek Drive has been open 24/7 since 2013."),
 ("Which of these is closest to the municipal golf courses?",
  "Mozart&rsquo;s is about a mile from Lions Muny. Epoch is a mile and a half from Hancock, and Cherrywood is a similar distance from Morris Williams. Jimmy Clay and Roy Kizer are the weak spot &mdash; Radio/East on Montopolis is the nearest independent option."),
 ("Which ones close early?",
  "Desnudo shuts between 2:30 and 4pm depending on the location, and Flitch runs 7am to 3pm daily. Both are morning rooms. Cherrywood, Radio, Cosmic, Leona and The Buzz Mill all run into the evening."),
 ("Are any of these chains?",
  "No. Every shop here is independently owned and Austin-based. Local mini-chains with a few Austin rooms &mdash; Epoch, Fleet, Jo&rsquo;s, Desnudo &mdash; are included; regional and national brands are not."),
]
FAQ="""<section class="products">
  <h2 class="products-hdr">The Questions</h2>
  <div class="faq">
"""+"\n".join(f'    <div class="faq-q">{q}</div>\n    <div class="faq-a">{a}</div>' for q,a in FAQ_ITEMS)+"""
  </div>
</section>
"""

SCHEMA={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":re.sub(r'&[a-z]+;','',q),
     "acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>|&[a-z]+;','',a)}} for q,a in FAQ_ITEMS]}

# ---- assemble from chassis ----
model=open("drops/students-golf-summer-2026.html",encoding="utf-8").read()
head=model[:model.find('<div class="breadcrumb">')]
tail=model[model.find('<section class="more"'):]

head=re.sub(r'<title>[^<]*</title>',f'<title>{TITLE} — The Grassy Issue</title>',head)
head=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+DESC+m.group(2),head)
head=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:title" content=")[^"]*(")',lambda m:m.group(1)+TITLE+m.group(2),head)
head=re.sub(r'(<meta property="og:description" content=")[^"]*(")',lambda m:m.group(1)+DESC+m.group(2),head)
head=re.sub(r'(<meta property="og:url" content=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:image" content=")[^"]*(")',lambda m:m.group(1)+"https://thegrassyissue.com/images/austin-coffee-v2/hero.jpg"+m.group(2),head)
head=re.sub(r'<script type="application/ld\+json">.*?</script>',
            '<script type="application/ld+json">'+json.dumps(SCHEMA)+'</script>',head,flags=re.S)

crumb=('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
       '  <a href="/#feed">Field Notes</a><span>/</span>\n  Austin Coffee</div>\n')
hero=('<div class="drop-hero"><div class="drop-hero-img">'
      '<img src="/images/austin-coffee-v2/hero.jpg" alt="The pavilion and garden at Leona Botanical Cafe and Bar in Sunset Valley, Austin" /></div></div>\n')

body=(crumb+hero+INTRO
      +section("The Regulars &mdash; 12 Rooms","Long-standing independents, sorted by what each one is actually good for.",REGULARS)
      +section("Just Opened &mdash; 2 New Arrivals","Both landed in the last twelve months and are already in the rotation.",NEW)
      +FAQ)

open(f"drops/{SLUG}.html","w",encoding="utf-8").write(head+body+tail)
words=len(re.sub(r'<[^>]+>',' ',head+body+tail).split())
print(f"wrote drops/{SLUG}.html  |  {len(REGULARS)+len(NEW)} shops  |  ~{words} words")
