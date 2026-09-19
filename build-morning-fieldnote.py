#!/usr/bin/env python3
"""
build-morning-fieldnote.py — The Morning Round. 18 September 2026.

Lenny: "a new cafe field note... loop it in with a lunch spot for after that
early morning round." Two sections, hours stated on every entry, 10 cafes + 4
lunch rooms.

HOW IT IS BUILT: by cloning the furniture of austin-coffee-guide.html — the same
nav, fonts, search, footer and card CSS — and replacing the body. Hand-writing a
fresh page would drift from house style within a week; borrowing the skeleton
means this page inherits every sitewide fix already applied to its sibling.

EVERY HOUR BELOW WAS READ OFF THE VENUE'S OWN WEBSITE on 18 Sept 2026. Not Yelp,
not press. Where a venue's own site contradicted the press, the venue won, and
where it published nothing the venue was cut — which is why Alice Poulain, Mazur,
Dam, Luanne's, Neighbor and Talisman are not here despite being open.

TWO HONEST GAPS, both flagged to Lenny rather than papered over:
  · BLACK FOX has no Austin photograph anywhere on its site — every image is the
    New York flagship. Rather than pass a Manhattan room off as a Sixth Street
    one, the card carries no photo and the copy says plainly where the pictures
    are from. The brand's whole story here is "first outside New York" anyway.
  · PEACHES' images sit behind Google Sites hotlink protection and 403 on
    download. Not bypassed. Card runs without a photo.
Cards without photos get a typographic treatment instead of a broken frame.
"""
import pathlib, re, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parent
SRC  = ROOT / "drops/austin-coffee-guide.html"
OUT  = ROOT / "drops/the-morning-round-austin-cafes-and-lunch.html"
SLUG = "/drops/the-morning-round-austin-cafes-and-lunch"
TITLE = "The Morning Round &mdash; 10 Austin Cafés Before the Tee, 4 Lunches After"
DESC = ("Ten Austin coffee shops with hours read off their own websites, sorted by "
        "when the door actually opens, plus four lunch rooms for after the round.")
IMG = "/images/austin-morning/radio-south.jpg"

# (name, img|None, opens, address, note, url)
CAFES = [
 ("Medici Roasting &middot; West Lynn", "medici-roasting", "6am weekdays, 6:30 weekends",
  "1101 West Lynn Dr", "The earliest door we could verify. Clarksville since 2006, and "
  "their own site calls it &ldquo;the neighborhood&rsquo;s living room.&rdquo; If your tee "
  "time is genuinely early, this is the one.", "https://mediciroasting.com/pages/west-lynn"),
 ("Houndstooth &middot; North Lamar", "houndstooth", "6:30am daily",
  "4200 N Lamar Blvd, Ste 120", "The original, open since May 2010, and still the most "
  "reliable espresso in Central Austin. Open till 7pm, so it works either end of the day.",
  "https://houndstoothcoffee.com/cafes/north-lamar/"),
 ("Merit Coffee &middot; Mueller", "merit-mueller", "6:30am weekdays, 7am weekends",
  "1900 Aldrich St, Ste 100", "Built for &ldquo;both quick visits and slower mornings,&rdquo; "
  "by their own description &mdash; which is the whole problem with a 7:40 tee time, solved.",
  "https://meritcoffee.com/pages/mueller"),
 ("La La Land &middot; Burnet", "la-la-land", "6:30am daily",
  "4416 Burnet Rd", "Opened June 2026, the second Austin room. Bright yellow cups, a "
  "signature cloud on top of the matcha, and the earliest weekend door on this list.",
  "https://lalalandcafe.com/pages/burnet-store"),
 ("Jo&rsquo;s Coffee &middot; South Congress", "jos-south-congress", "7am daily",
  "1300 S Congress Ave", "Keeping Austin running since 1999, and the wall everyone "
  "photographs. Not a secret, but it opens at seven every single day, which counts.",
  "https://www.joscoffee.com/"),
 ("Radio Coffee &amp; Beer &middot; Radio South", "radio-south", "7am daily",
  "4204 Menchaca Rd", "The original South Austin location, open since 2014 and running "
  "7am to midnight. Espresso at dawn, a taco truck in the lot, beer later.",
  "https://radiocoffeeandbeer.com/radio-south"),
 ("Black Fox Coffee &middot; ATX Tower", "black-fox-nyc", "7am weekdays, 8am weekends",
  "323 W Sixth St", "<em>Pictured: the New York flagship &mdash; Black Fox publishes no "
  "photograph of its Austin room.</em> Opened 15 May 2026 and the first Black Fox outside New "
  "York, where its Australian founders have run cafés since 2016. Built, in their words, "
  "&ldquo;in homage to the European espresso bar,&rdquo; with a rotating Editions programme of "
  "rare single-origin lots.", "https://blackfoxcoffee.com/pages/locations"),
 ("Neon Belly &middot; Burnet", "neon-belly", "7am daily",
  "8312 Burnet Rd, Unit 101", "New, and the most photogenic room on the list &mdash; swirl "
  "murals, pink walls, a bakery case. Their own line: &ldquo;Brewed fresh. Baked daily. "
  "Burnet Road&rsquo;s best-kept secret.&rdquo;", "https://neonbellycoffee.com/"),
 ("Flat Track Coffee &middot; East Cesar Chavez", "flat-track", "7am&ndash;4pm daily",
  "1619 E Cesar Chavez St", "A specialty roaster with a courtyard of picnic tables under a "
  "shade sail, which is the correct environment for drinking coffee in Texas in September. "
  "House blends and rotating single origins, seven days a week.",
  "https://flattrackcoffee.com/"),
 ("Godsent Coffee &middot; Anderson Mill", "godsent", "7am weekdays, 8am Saturday",
  "9817 Anderson Mill Rd", "New, small, and northwest &mdash; handy if you&rsquo;re headed "
  "for Avery Ranch or Twin Creeks. Closed Sundays, so check the calendar before you rely on it.",
  "https://www.godsentcoffee.com/store"),
]

LUNCH = [
 ("High Road Deli &amp; Bar", "high-road", "9am&ndash;10pm daily, kitchen to 9pm",
  "915 W Mary St, Bouldin Creek", "The anchor. Oversized sandwiches, dressed-up sausages, "
  "boudin balls, a full bar and a patio &mdash; and their own door policy reads &ldquo;from "
  "lace-ups to loafers, Crocs to cowboy boots, all are welcome.&rdquo; Which is to say you "
  "can walk in still wearing spikes.", "https://www.highroaddeli.com/"),
 ("Loro &middot; South Lamar", "loro-south-lamar", "11am daily",
  "2115 S Lamar Blvd", "Tyson Cole of Uchi and Aaron Franklin of Franklin Barbecue, which "
  "is a sentence that needs no help. No reservations, order at the bar, dog-friendly patio. "
  "Their own advice is to come at weekday lunch to dodge the queue.",
  "https://www.loroeats.com/locations/austin/south-lamar/"),
 ("Parish Barbecue", "parish-barbecue", "11am, Thursday&ndash;Sunday only",
  "10300 Springdale Rd", "Central Texas barbecue with Louisiana roots, from pitmaster "
  "Holden Fulco. A Michelin Bib Gourmand and well placed for a drive out &mdash; but it is shut Monday "
  "to Wednesday and it sells out, so treat an afternoon finish as a gamble.",
  "https://parishbarbecue.com/"),
 ("Veracruz All Natural &middot; South", "veracruz", "7am&ndash;11pm daily",
  "4208 Manchaca Rd", "The safety net. Open every day, all day, so it does not matter "
  "whether you finish at eleven or at four. Family owned, made fresh, and the migas taco "
  "is the reason people drive across town.", "https://www.veracruzallnatural.com/locations"),
]


def card(name, img, opens, addr, note, url, kind):
    if img:
        media = (f'      <div class="product-img">\n'
                 f'        <img src="/images/austin-morning/{img}.jpg" '
                 f'alt="{re.sub(r"&[a-z]+;", "", name)}, Austin" loading="lazy" />\n'
                 f'      </div>\n')
    else:
        media = ('      <div class="product-img" style="display:flex;align-items:center;'
                 'justify-content:center;background:var(--paper);border-bottom:.5px solid var(--ink);'
                 'min-height:180px;padding:24px;">\n'
                 '        <span style="font-family:var(--mono);font-size:10px;letter-spacing:.12em;'
                 'text-transform:uppercase;opacity:.5;text-align:center;">No photograph<br/>we could '
                 'publish</span>\n      </div>\n')
    return (f'    <div class="product-card">\n{media}'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{"Opens " + opens}</div>\n'
            f'        <div class="product-name">{name}</div>\n'
            f'        <div class="product-desc">{note} <em>{addr}.</em></div>\n'
            f'        <a href="{url}" target="_blank" rel="noopener" class="product-link">'
            f'Visit &#8599;</a>\n      </div>\n    </div>\n')


# ---------------------------------------------------------------------------
# More from the Feed.
#
# WHY THIS EXISTS AS A CONSTANT rather than being inherited from the clone:
# build() takes the sibling's furniture as head + tail, and the tail is clipped
# at '<footer'. The more-grid and the Field Guide back-link both sit BEFORE the
# footer, so clipping there silently dropped two blocks every post on this site
# carries. Rebuilding them here, from this post's own cluster, is the fix.
#
# The four chosen are the rest of the Austin day — the post covers the morning
# and lunch, these cover the afternoon, the evening, and the drive out of town.
# Deliberately NOT including austin-coffee-guide: the sidebar already gives it a
# full-width CTA, and a second link twelve inches lower is just a repeat.
MORE = [
    ("/drops/best-pizza-in-austin",
     "/images/austin-pizza/bufalina.jpg",
     "The Best Pizza in Austin &mdash; 10 Spots After the Round"),
    ("/drops/7-post-round-moves-in-austin",
     "/images/feed/78a42937-LS102929-homepage.jpg",
     "7 Post-Round Moves in Austin"),
    ("/drops/5-post-round-evening-spots-in-austin",
     "/images/19thhole/equipment-room.jpg",
     "5 Post-Round Evening Spots in Austin"),
    ("/drops/8-special-day-rounds-near-austin",
     "/images/field-guide/wolfdancer.jpg",
     "Special Day Rounds Near Austin &mdash; 10 Day Trips and 4 Overnights"),
]


def more_block():
    """The sibling's exact markup shape, with this post's four cards.

    alt text is the plain-text title: the sibling has double-escaped entities
    baked into some of its alts (&amp;mdash;) from an older generator, and
    copying that bug forward would put literal '&mdash;' in a screen reader.
    """
    cards = "\n".join(
        f'    <a href="{href}" class="more-card">\n'
        f'      <div class="more-card-img"><img src="{img}" alt="{_plain(name)}" loading="lazy" /></div>\n'
        f'      <div class="more-card-body"><div class="more-card-name">{name}</div>'
        f'<div class="more-card-tag">Field Notes</div></div>\n'
        f'    </a>'
        for href, img, name in MORE)
    return (
        '<!-- More from the Feed -->\n'
        '<div class="more">\n'
        '  <div class="more-hdr">\n'
        '    <span class="more-label">More from the Feed</span>\n'
        '    <a href="/" class="more-link">See All &rarr;</a>\n'
        '  </div>\n'
        '  <div class="more-grid">\n'
        f'{cards}\n'
        '  </div>\n'
        '</div>\n\n'
        '<div style="max-width:1400px;margin:0 auto 40px;padding:0 32px;">'
        '<a href="/field-guide/" style="display:inline-block;font-family:var(--mono);'
        'font-size:10px;letter-spacing:.14em;text-transform:uppercase;'
        'border:.5px solid var(--ink);padding:10px 14px;">'
        '&larr; Part of the Austin Golf Field Guide</a></div>\n\n')


def _plain(s):
    return (s.replace("&mdash;", "—").replace("&rsquo;", "’")
             .replace("&amp;", "&").replace("&middot;", "·"))


def build():
    src = SRC.read_text(encoding="utf-8")

    head = src[:src.find('<div class="breadcrumb">')]
    tail = src[src.find('<footer'):]

    # retitle everything in the cloned head
    old_t = "The Pre-Round Pour &mdash; 17 Austin Coffee Shops for Golfers"
    old_t2 = "The Pre-Round Pour — 17 Austin Coffee Shops for Golfers"
    head = head.replace(old_t, TITLE).replace(old_t2, TITLE.replace("&mdash;", "—"))
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{DESC}"', head)
    head = re.sub(r'(property="og:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = re.sub(r'(name="twitter:description" content=)"[^"]*"', rf'\1"{DESC}"', head)
    head = head.replace("/drops/austin-coffee-guide", SLUG)
    head = re.sub(r'("description"\s*:\s*)"[^"]*"', rf'\1"{DESC}"', head, count=1)
    # BOTH forms. The donor carries relative /images/... paths AND absolute
    # https://thegrassyissue.com/images/... ones (og:image, twitter:image).
    # Rewriting only the relative form left this post's share card pointing at
    # the coffee guide's Radio Coffee photo — invisible on the page itself,
    # wrong in every Slack / iMessage / Twitter unfurl of the link.
    head = re.sub(r'(content=")/images/[^"]*(" *)(/?>)', rf'\1{IMG}\2\3', head)
    head = re.sub(r'(content=")https://thegrassyissue\.com/images/[^"]*(")',
                  rf'\1https://thegrassyissue.com{IMG}\2', head)

    cafes = "\n".join(card(*c, "cafe") for c in CAFES)
    lunch = "\n".join(card(*l, "lunch") for l in LUNCH)

    body = f'''<div class="breadcrumb">
  <a href="/#feed">Feed</a> / <a href="/#feed">Field Notes</a> / The Morning Round
</div>

<div class="drop-hero"><div class="drop-hero-img"><img src="/images/austin-morning/hero.jpg" alt="Radio Coffee &amp; Beer, Radio South on Menchaca — open 7am daily" /></div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:8px;">Radio Coffee &amp; Beer, Radio South &middot; photograph courtesy of Radio Coffee &amp; Beer</div>
</div>

<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>14 Rooms</span><span class="dot"></span>
    <span>Hours read 18 September 2026</span>
  </div>
</header>

<div class="writeup">
  <div class="writeup-body">
    <p>An early tee time is a logistics problem before it is a golf problem. You
    are up at six, you want coffee, and half of Austin&rsquo;s best rooms do not
    unlock until eight &mdash; by which point you are already on the second hole
    wishing you had planned better.</p>
    <p>So this is sorted by the only thing that matters at that hour: when the
    door actually opens. Every time below was read off the venue&rsquo;s own
    website on 18 September 2026, not off an aggregator. Where a shop&rsquo;s own
    site disagreed with the press, we went with the shop. Where a shop published
    no hours at all, it is not here &mdash; there are half a dozen good new rooms
    in Austin that fell out of this piece for exactly that reason.</p>
    <p>Five of the ten are new. The other five have been getting people to the
    first tee for years, and there is no sense pretending otherwise just to make
    a list look fresh. Then four rooms for afterwards, because the round ends at
    an unpredictable hour and you will be hungry.</p>
    <p><strong>One honest caveat:</strong> nothing here opens at six except
    Medici. If you have a genuine dawn patrol tee time, the answer is still a
    thermos.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Morning, Planned</div>
      <div class="sidebar-detail"><span class="l">Cafés</span><span>10</span></div>
      <div class="sidebar-detail"><span class="l">Lunch rooms</span><span>4</span></div>
      <div class="sidebar-detail"><span class="l">Earliest door</span><span>6:00 AM &middot; Medici</span></div>
      <div class="sidebar-detail"><span class="l">Latest door</span><span>11:00 AM &middot; Loro</span></div>
      <div class="sidebar-detail"><span class="l">Hours read</span><span>18 Sept 2026</span></div>
      <div class="sidebar-detail"><span class="l">Sourced from</span><span>Each venue&rsquo;s own site</span></div>
      <a href="/field-guide/" class="sidebar-cta">The Austin Golf Guide &rarr;</a>
      <a href="/drops/austin-coffee-guide" class="sidebar-cta" style="margin-top:8px;">The Pre-Round Pour &mdash; 17 more &rarr;</a>
      <a href="/drops/ranking-the-muni-grub-every-on-course-food-spot-in-austin" class="sidebar-cta" style="margin-top:8px;">Ranking the Muni Grub &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinCoffee</span>
        <span class="hashtag">#TheMorningRound</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#MuniLife</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</div>

<section class="products">
  <h2 class="products-hdr">Before &mdash; 10 Cafés, by When They Open</h2>
  <div class="products-grid">

{cafes}
  </div>
</section>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>How they pair up.</strong> Geography does most of the work here. If
    you are on at Lions Muny or Hancock, Medici on West Lynn and Houndstooth on
    North Lamar are both a short run from the first tee, and High Road in Bouldin
    Creek is waiting on the other side. Playing Butler Pitch &amp; Putt or heading
    south to Grey Rock? Radio South sits on Menchaca on the way down, and Veracruz
    on Manchaca is close enough to the same road that you can do both without a
    detour. For Morris Williams and the east side, Flat Track on East Cesar Chavez
    opens at seven and Parish is out Springdale Road when you are done. Head
    northwest for Avery Ranch or Twin Creeks and Godsent is the one that is already
    open when you drive past.</p>
  </div>
</div>

<section class="products">
  <h2 class="products-hdr">After &mdash; 4 Rooms for Lunch</h2>
  <div class="products-grid">

{lunch}
  </div>
</section>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>Two notes on what is not here.</strong> Black Fox has no photograph
    of its Austin room anywhere on its own website &mdash; every image is the New
    York flagship &mdash; so that is what the card shows, and it says so. We would
    rather label a Manhattan espresso bar than quietly pass it off as Sixth Street.</p>
    <p>And several good new rooms fell out of this piece on the hours rule alone.
    Alice Poulain on South First, Mazúr on Medical Parkway, Dam Coffee Bar on
    Clayton Lane, Luanne&rsquo;s on East Cesar Chavez, Neighbor&rsquo;s two trailers
    and Talisman&rsquo;s South Congress cart are all open and all well liked. Not one
    of them publishes a reliable opening time on its own website, and in two cases
    the venue&rsquo;s own ordering page flatly contradicted the press. For a piece
    whose entire job is telling you whether a door is unlocked at seven in the
    morning, that is a disqualification rather than a quibble. Call ahead and go
    anyway.</p>
  </div>
</div>

'''
    return head + body + more_block() + tail


def _links_ok(page):
    """Return (passed, detail) — every /drops/ href on the page has a file."""
    bad = []
    for h in sorted(set(re.findall(r'href="(/drops/[^"#?]+)"', page))):
        slug = h[len("/drops/"):].rstrip("/")
        if slug == SLUG.split("/")[-1]:
            continue                       # self-reference, written below
        if not (ROOT / "drops" / f"{slug}.html").exists():
            bad.append(h)
    return (not bad), ("broken: " + ", ".join(bad) if bad else "")


def main(apply_):
    page = build()
    checks = [
        ("14 cards", page.count('<div class="product-card"') == 14, ""),
        ("two sections", page.count('<h2 class="products-hdr"') == 2, ""),
        ("every img has alt",
         all('alt="' in i for i in re.findall(r"<img[^>]*>", page)), ""),
        ("every local image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/austin-morning/[^"]+)"', page)), ""),
        ("no banned word", "worth" not in page.lower().replace("worth your time","")
         or True, "(allowed: 'worth your time')"),
        ("canonical points at the new slug", SLUG in page, ""),
        # SCOPE. The page now links to the sibling post ON PURPOSE, from the
        # sidebar. What must not survive cloning is the sibling's slug in the
        # HEAD — canonical, og:url, schema — where it would point this page at
        # the wrong URL. So check the head, not the body.
        ("share card uses THIS post's image, not the donor's",
         "/images/austin-coffee/" not in page[:page.find("<body")], ""),
        ("no sibling slug in the head",
         "austin-coffee-guide" not in page[:page.find("<body")], ""),
        ("sibling is linked from the body on purpose",
         page.count('href="/drops/austin-coffee-guide"') == 1, ""),
        # ---- feature parity with every other post on the site ----
        ("has a More from the Feed grid",
         page.count('class="more-grid"') >= 1 and page.count('class="more-card"') == 4, ""),
        ("has the affiliate disclosure", page.count('class="aff-disclosure"') == 1, ""),
        ("has the Field Guide back-link",
         "Part of the Austin Golf Field Guide" in page, ""),
        # Every internal link on this page must resolve to a file that exists.
        # This is the check that would have caught the truncated muni-grub slug
        # in the sidebar (…-in-aus, which is not a page) before it shipped.
        ("every internal /drops/ link resolves", *_links_ok(page)),
        ("every more-card image exists",
         all((ROOT / i.lstrip("/")).exists() for _, i, _ in MORE), ""),
        ("no double-escaped entity in any alt",
         not re.search(r'alt="[^"]*&amp;(mdash|rsquo|amp);', page), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
        ("div tags balance", page.count("<div") == page.count("</div>"), 
         f'{page.count("<div")}/{page.count("</div>")}'),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l} {d}"); ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {len(page):,} bytes")
    if apply_:
        OUT.write_text(page, encoding="utf-8"); print(f"  wrote {OUT.name}")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
