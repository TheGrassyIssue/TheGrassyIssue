#!/usr/bin/env python3
"""build-loraloma-radar.py — On Our Radar: Loraloma, David McLay Kidd's first Texas course. 19 October 2026.
Lenny: "Let's do a on our radar - Loroloma" (after the new-Texas-courses roundup), then "add a plug for my real estate service - homes
are available for purchase" -> the apartments-post editor's-note block (TREC 535.155 elements kept), placed in Can You Play It?
FACTS (all read October 19, 2026; copies in research/loraloma/):
  - Opening release, Oct 27 2025 (firstcallgolf.com): 120 acres, par 72, 7,400 yards from the back tees, more than half the holes on the
    Pedernales cliffs, Balcones Escarpment views, all-zoysia (Stadium / Zeon / Lazer, Lazer from Texas A&M, second US course with Lazer
    greens), Hole 2 double green, Hole 8 cliffside par 5, Hole 18 "590-yard par-5", 1958 Bambi Airstream turn stand with a mural by
    Soledad Fernandez-Whitechurch, Tipsy's Wellhouse dollar-on-the-ceiling tradition, Kidd and Rentfro quotes.
  - Club golf FAQ (Aug 2025 PDF): 5 tee boxes, 4,407-7,222 yards, forced carries only from the back tees, 400+ yard range, short-game area,
    future covered bays with TrackMan, 5 indoor bays + 2 simulators.
  - Club FAQ (Mar 2026 PDF): opened October 2025; ~25 miles west of downtown Austin; "lore of the hills"; golf memberships not available
    to non-residents, no plans to offer them; Comfort Station #9 fall 2026; Golf House fall 2027; irrigation 20-30% less water, moving to
    effluent; aiming for International Dark Sky Community designation.
  - Club golf page: Kidd "tread very lightly" quote; Rentfro "100-foot ravines" quote; photo labels (Hole 4, Hole 13 and Double Green ...).
  - Golf Today, M. James Ward, Mar 30 2026: 18th is 573 yards on the scorecard, 5,036 sq ft green; Spencer Scheeler (Director of Golf) quotes.
PHOTOS: the club's own (course photography by Evan Schiller, credited by Golf Today and Golf Course Industry). research/loraloma/frame.py.
"""
import html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Loraloma Golf Club: David McLay Kidd's First Texas Course"
DESC = "Loraloma in Spicewood is David McLay Kidd's first Texas course: 18 all-zoysia holes on the Pedernales River cliffs, 25 miles west of Austin."
H1 = "On Our Radar: Loraloma, David McLay Kidd&rsquo;s First Course in Texas"
BC = "On Our Radar: Loraloma"
SLUG = "loraloma-david-mclay-kidd-texas-golf-course"
IMG = "/images/loraloma"
DATE = "2026-10-19"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
CSS = ('<style>/*TGI-RADAR-COURSE*/.ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0 10px}.ig-grid figure{margin:0}'
       '.ig-grid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5}'
       '.ig-cap,.lw figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:8px;line-height:1.5}'
       '.lw{margin:10px 0 8px}.lw img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;background:#eceae5}'
       '.rc{max-width:760px;margin:0 auto}.rc p{font-size:18px;line-height:1.7;margin:0 0 18px}.rc h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;margin:34px 0 10px}'
       '.ad-group{text-align:center;padding:64px 0 8px;border-top:.5px solid var(--ink);margin-top:40px}.ad-group h2{font-size:clamp(30px,4vw,44px);margin:10px 0 8px}.ad-group p{max-width:640px;margin:0 auto;opacity:.75}'
       '.rc p.credit{font-family:var(--mono);font-size:10px;line-height:1.5;letter-spacing:.12em;text-transform:uppercase;opacity:.5;text-align:center;margin:28px 0 0}'
       '@media(max-width:720px){.ig-grid{gap:6px}.ig-cap{display:none}.rc p{font-size:17px}}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>David McLay Kidd built the first course at Bandon Dunes, the Castle Course at St Andrews and Gamble Sands, the one we keep talking about from our <a href="/drops/pnw-golf-trip-gamble-sands-chambers-bay" style="border-bottom:1px solid currentColor">Pacific Northwest trip</a>. Until last October he had never built anything in Texas. Now he has, about 25 miles west of downtown Austin, on the limestone cliffs above the Pedernales River in Spicewood.</p>
    <p>Loraloma is a private residential club inside the 2,200-acre Thomas Ranch development, and the course opened to its members in October 2025. Over half the holes run along the river cliffs, the whole thing is grassed in zoysia from tee to green, and the turn stand is a 1958 Airstream. It is the most interesting new golf near Austin in years.</p>
    <p>It is also not ours to play. The club says golf memberships are for Loraloma residents only, with no plans to open them up. We cover public golf first, so take this as a look over the fence: what Kidd built, the holes people are talking about, the small touches we like, and how it fits into an Austin golf scene that keeps growing west.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Loraloma at a Glance</div>
      <div class="sidebar-detail"><span class="l">Where</span><span>Spicewood, TX &middot; ~25 mi west of Austin</span></div>
      <div class="sidebar-detail"><span class="l">Architect</span><span>David McLay Kidd</span></div>
      <div class="sidebar-detail"><span class="l">Opened</span><span>October 2025, members only</span></div>
      <div class="sidebar-detail"><span class="l">Par</span><span>72 &middot; five sets of tees</span></div>
      <div class="sidebar-detail"><span class="l">Yardage</span><span>4,407&ndash;7,222 (club FAQ)</span></div>
      <div class="sidebar-detail"><span class="l">Grass</span><span>Zoysia, wall to wall</span></div>
      <div class="sidebar-detail"><span class="l">Access</span><span>Residents and members</span></div>
      <a href="https://loralomaclub.com/golf/" target="_blank" rel="noopener" class="sidebar-cta">Loraloma Golf &#8599;</a>
      <div class="hashtags"><span class="hashtag">#OnOurRadar</span><span class="hashtag">#TexasGolf</span><span class="hashtag">#HillCountry</span></div>
    </div>
  </aside>
</section>
"""


UTM = "utm_source=thegrassyissue&amp;utm_medium=referral&amp;utm_campaign=loraloma&amp;utm_content=loraloma-radar"
SITE = "https://lennyharrington.papasanproperties.com"
def lenny(where):
    sms = "sms:+19143188472?&amp;body=Hi%20Lenny%2C%20I%20found%20you%20through%20The%20Grassy%20Issue%20post%20on%20Loraloma.%20I%27m%20interested%20in%20buying%20there."
    return f'''
<aside class="lre" aria-label="A note from the editor">
 <div class="lre-in">
  <img class="lre-img" src="/images/lenny/headshot.jpg" alt="Lenny Harrington" width="112" height="112" loading="lazy" />
  <div>
   <div class="lre-k">A note from the editor &middot; Lenny&rsquo;s day job</div>
   <p class="lre-h">The way onto this course is a front door.</p>
   <p class="lre-p">Homes and homesites at Loraloma are for sale now, from golf-front lots along the 15th to turn-key residences, and buying in is how you get on the tee sheet. When I&rsquo;m not writing The Grassy Issue, I&rsquo;m a real estate agent in Austin. I can walk you through what&rsquo;s available, what each option includes and how the club side works, and help you buy anywhere else in the Hill Country, too.</p>
   <a class="lre-btn" href="{sms}" data-goatcounter-click="loraloma-text-lenny-{where}">Text Lenny &rarr;</a>
   <a class="lre-btn lre-btn2" href="{SITE}/property-search/results/?{UTM}" target="_blank" rel="noopener" data-goatcounter-click="loraloma-view-listings-{where}">View listings &rarr;</a>
   <a class="lre-tel" href="tel:+19143188472">(914) 318-8472</a>
   <div class="lre-c">
    Lenny Harrington &middot; TX License 795491 &middot; Papasan Properties Group<br>
    <span class="lre-b">KELLER WILLIAMS</span> &middot; 1801 S. MoPac Expy., Ste. 100, Austin<br>
    <a href="{SITE}/res/includes/TREC-IABS.pdf?{UTM}" target="_blank" rel="noopener">Texas Real Estate Commission Information About Brokerage Services</a> &middot;
    <a href="{SITE}/assets/docs/TREC-CPN.pdf?{UTM}" target="_blank" rel="noopener">Texas Real Estate Commission Consumer Protection Notice</a><br>
    This is Lenny&rsquo;s own business. Loraloma did not pay TGI for this post.
   </div>
  </div>
 </div>
</aside>
'''
LRE_CSS = '''<style>/*TGI-LENNY-RE-CSS*/
.lre{max-width:880px;margin:56px auto;padding:0 32px}
.lre-in{border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:28px 0 24px;display:grid;grid-template-columns:112px 1fr;gap:28px;align-items:start}
.lre-img{width:112px;height:112px;border-radius:50%;object-fit:cover;object-position:center 22%;display:block}
.lre-k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:12px}
.lre-h{font-family:var(--serif);font-size:34px;line-height:1.1;margin:0 0 12px;font-weight:400}
.lre-p{font-family:var(--serif);font-size:18px;line-height:1.55;margin:0 0 16px}
.lre-btn{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;background:var(--grass);color:var(--paper)!important;padding:11px 16px;margin:0 14px 8px 0;border-bottom:none!important;text-decoration:none}
.lre-btn2{background:transparent;color:var(--grass)!important;box-shadow:inset 0 0 0 1px var(--grass)}
.lre-tel{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:inherit;border-bottom:none!important;text-decoration:none}
.lre-c{font-family:var(--mono);font-size:10px;letter-spacing:.06em;line-height:1.7;opacity:.75;margin-top:18px}
.lre-c a{border-bottom:1px solid currentColor;color:inherit;text-decoration:none}
.lre-b{font-size:11px;letter-spacing:.1em}
@media(max-width:640px){.lre{padding:0 20px}.lre-in{grid-template-columns:1fr;gap:16px}.lre-img{width:84px;height:84px}.lre-h{font-size:28px}.lre-p{font-size:17px}}
</style>
'''
def fig3(items):
    s = "\n".join(f'  <figure><img src="{IMG}/{f}" alt="{H.escape(a)}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in items)
    return f'<div class="ig-grid">\n{s}\n</div>\n'
def wide(f, alt, cap):
    return f'<figure class="lw"><img src="{IMG}/{f}" alt="{H.escape(alt)}" loading="lazy" /><figcaption>{cap}</figcaption></figure>\n'
def group(key, tag, h2, sub):
    return f'\n<section class="ad-group" id="{key}"><div class="drop-tag grass">{tag}</div><h2>{h2}</h2><p>{sub}</p></section>\n'
def pq(q, who):
    return f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n'

LAND = group("the-land", "The Land", "Cliffs, Ravines and Two Rivers", "Why this ground is not typical Texas golf.") + f"""
<section class="products" style="margin-top:8px;border-top:none"><div class="rc">
{fig3([("land-1.jpg", "Aerial view of a Loraloma fairway beside a bend in the Pedernales River", "Hole 9, above the river"),
       ("land-2.jpg", "A Loraloma fairway running past a pond at sunrise", "Hole 15"),
       ("land-3.jpg", "Aerial view of a Loraloma hole cut through Hill Country scrub", "Hole 10")])}
<p>Loraloma sits on more than two miles of frontage where the Pedernales meets the Colorado, a few minutes from Lake Travis. The club&rsquo;s own pitch is short: you will be hitting over ravines more than 100 feet deep. Kidd&rsquo;s course covers about 120 acres of it. More than half the holes trace the cliffs above the Pedernales, and the rest climb to ridges that look out over the Hill Country and the Balcones Escarpment.</p>
<p>Kidd is known for big, wide, firm golf that lets the land do most of the talking, and the club describes this one the same way, calling it &ldquo;the art of restraint.&rdquo; It plays from 4,407 to 7,222 yards across five sets of tees, according to the club&rsquo;s golf FAQ; the opening release rounds the tips up to 7,400. There are forced carries from the back tees, but every hole has a forward tee with a straight path to the fairway, so a 20-handicap is not spending the day reloading.</p>
<p>The other thing that sets it apart is the grass. Loraloma is zoysia everywhere: Stadium zoysia on the tees and fairways, Zeon in the rough, and Lazer zoysia on the greens, a variety developed at Texas A&amp;M. The opening release says it is only the second course in the country with Lazer greens. Zoysia plays tight and firm, which suits a Kidd course.</p>
</div></section>
"""
LAND_PQ = pq("Our goal is to open up this compelling landscape to golfers for a world-class experience, and I will tread very lightly to preserve and protect this land so that it can be enjoyed and embraced for generations to come.", "David McLay Kidd, on Loraloma")

HOLES = group("holes", "Three Holes", "The Holes to Know", "The three the club and the early reviews keep coming back to.") + f"""
<section class="products" style="margin-top:8px;border-top:none"><div class="rc">
<h3>No. 2 &middot; The double green</h3>
{wide("hole-2.jpg", "Aerial view of Loraloma's second hole with the river beyond", "Hole 2")}
<p>Kidd sets the tone early. The second plays to an enormous double green, the kind you see on old links and almost never in Texas, where the flag can be a long walk from where your ball finishes. The club&rsquo;s own photos pair it with the 13th. Before you tee off here, stop at Tipsy&rsquo;s Wellhouse, a historic wellhouse where players pin a dollar to the ceiling with a note, a bit of advice or a thank-you.</p>
<h3>No. 8 &middot; The cliffside par 5</h3>
{wide("hole-8.jpg", "Aerial view of Loraloma's eighth hole running along the cliffs above the Pedernales River", "Hole 8, on the cliffs")}
<p>The eighth rises along the cliff edge above the Pedernales, and it is the hole in almost every photo the club puts out. The opening release calls it a dramatic cliffside par 5, with views over the river and the Hill Country, and the aerials explain why: there is fairway, there is a long drop to the water, and not much in between.</p>
<h3>No. 18 &middot; The arroyo finish</h3>
{wide("hole-18.jpg", "Aerial view of Loraloma's 18th fairway in morning light with the river in the distance", "Hole 18")}
<p>The closer is a long par 5: 573 yards on the scorecard Golf Today published, 590 in the opening release. Director of Golf Spencer Scheeler says the tee shot looks scarier than it is, and the real question comes on the second, where an arroyo cuts across. Big hitters can get home in two with the wind behind them. Everyone else has to pick a line that leaves the best angle into a 5,036-square-foot green.</p>
</div></section>
"""
HOLES_PQ = pq("Hole 18 presents a visually intimidating tee shot yet offers more room than it first suggests.", "Spencer Scheeler, Director of Golf, to Golf Today")

LITTLE = group("details", "The Details", "The Small Things We Like", "A course says a lot in the bits between the holes.") + f"""
<section class="products" style="margin-top:8px;border-top:none"><div class="rc">
{fig3([("day-1.jpg", "A golfer hitting a tee shot at Loraloma's opening event", "Opening event"),
       ("day-2.jpg", "A golfer in a kilt putting on a Loraloma green at the opening event", "On the green"),
       ("day-3.jpg", "Aerial view of a Loraloma hole at sunset", "Hole 16")])}
<p><strong>The Airstream.</strong> Between nine and ten, a retrofitted 1958 Bambi Airstream works as the turn stand, with a mural by local artist Soledad Fernandez-Whitechurch, cocktails and club merch. A permanent comfort station on nine is scheduled for fall 2026.</p>
<p><strong>The wellhouse.</strong> Tipsy&rsquo;s Wellhouse, by the second tee, is the kind of tradition a new club usually takes 50 years to grow: leave a dollar on the ceiling with a note for whoever comes next.</p>
<p><strong>The practice ground.</strong> A range of more than 400 yards with a variety of targets, a short-game area built to mimic the course, and plans for covered TrackMan bays plus a training building with five indoor bays and two simulators.</p>
<p><strong>The water.</strong> The club says the irrigation uses 20 to 30 percent less water than comparable courses and will eventually run entirely on recycled effluent. Loraloma is also working toward International Dark Sky Community status, which matters out here, where the stars still show up.</p>
<p>The name, by the way, means &ldquo;lore of the hills.&rdquo; The developer, Aret&eacute; Collective, made it up.</p>
</div></section>
"""

PLAY = group("access", "Access", "Can You Play It?", "The honest answer.") + f"""
<section class="products" style="margin-top:8px;border-top:none"><div class="rc">
{wide("hole-4.jpg", "Aerial view of Loraloma's fourth hole beside the river", "Hole 4")}
<p>Not unless you live there, or know someone who does. Loraloma&rsquo;s own FAQ says golf and social memberships are not available to people outside the community, and that the club does not plan to offer them, while keeping the right to change that. The golf house, with a pro shop, restaurant and bar, is slated for fall 2027, and more of the community&rsquo;s amenities follow through 2030.</p>
<p>So why is it on our radar? Because it raises the bar for what gets built around Austin. A world-class architect chose the Hill Country, chose firm zoysia over soft overseed, and built something with the bones of his best work on ground few people would have called golf country a few years ago. That tends to change what comes next, public courses included. If you get the invitation, take it. If not, the eighth hole alone is a good reason to make a friend in Spicewood.</p>
</div></section>
""" + lenny("access") + """<section class="products" style="margin-top:0;border-top:none"><div class="rc">
<p>Want Kidd you can book yourself? Gamble Sands in Washington is public, and it is on our <a href="/drops/pnw-golf-trip-gamble-sands-chambers-bay" style="border-bottom:1px solid currentColor">2027 Pacific Northwest list</a>. Closer to home, our <a href="/field-guide" style="border-bottom:1px solid currentColor">Austin Golf Guide</a> covers the public courses in town.</p>
<p class="credit">Course photography by Evan Schiller, courtesy of Loraloma</p>
</div></section>
"""

FAQ = [
 ("What is Loraloma?", "Loraloma Private Club & Estates is a private residential club inside the 2,200-acre Thomas Ranch development in Spicewood, Texas, about 25 miles west of downtown Austin. Its 18-hole golf course was designed by David McLay Kidd and opened to members in October 2025."),
 ("Who designed the Loraloma golf course?", "David McLay Kidd of DMK Golf Design, the Scottish architect behind the first course at Bandon Dunes, the Castle Course at St Andrews and Gamble Sands. Loraloma is his first course in Texas."),
 ("Can the public play Loraloma?", "No. The club's FAQ says golf and social memberships are not available to people outside the Loraloma community and that it does not plan to offer them, though it reserves the right to change the membership structure."),
 ("How long is the Loraloma course?", "It is a par 72 that plays from 4,407 to 7,222 yards across five sets of tees, according to the club's golf FAQ. The opening release gave 7,400 yards from the back tees."),
 ("Can you buy a home at Loraloma?", "Yes. Loraloma sells homesites and turn-key residences, including golf-front lots along the 15th hole, and owning there is the route to golf membership. TGI editor Lenny Harrington is an Austin real estate agent with Keller Williams and can help."),
 ("What grass is on the course?", "Zoysia throughout: Stadium zoysia on tees and fairways, Zeon zoysia in the rough and Lazer zoysia, developed at Texas A&M, on the greens."),
]
def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return f'\n<section class="products" style="border-top:none;padding-top:48px">\n  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n'

def head_top():
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    blocks = [
     {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
      "about": {"@type": "GolfCourse", "name": "Loraloma Golf Club", "address": {"@type": "PostalAddress", "addressLocality": "Spicewood", "addressRegion": "TX", "addressCountry": "US"}},
      "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
      "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
      {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"}, {"@type": "ListItem", "position": 3, "name": H.unescape(BC), "item": URL}]}]
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
{ld}"""

def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 19, 2026</span><span class="dot"></span>
    <span>On Our Radar &middot; Spicewood, Texas</span><span class="dot"></span>
    <span>Members only</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Aerial view of Loraloma's eighth hole on the cliffs above the Pedernales River in Spicewood, Texas" fetchpriority="high" /></div></div>
"""
    body += TAKE + LAND + LAND_PQ + HOLES + HOLES_PQ + LITTLE + PLAY + faq_html()
    out = head_top() + head_rest.replace("</head>", CSS + LRE_CSS + "</head>", 1) + body + tail
    if not apply_: print("  dry run"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie"):
        if leak in above: bad.append("leak " + leak)
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")
if __name__ == "__main__":
    main("--apply" in sys.argv)
