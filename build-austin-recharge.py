#!/usr/bin/env python3
"""build-austin-recharge.py — The Austin Recharge (field note), 22 November 2026.
Lenny: "Let's do a recharge in Austin after the holidays - think Ottine Mineral springs, hikes, a nice solo morning round";
"swap out Joe Balander for something a little nicer" (-> Lost Pines); "Think less day one vs two, but more of what the ideal
vibe needs to be" -> eight ideas; "build it".
FACTS: every price/hour/rule is from the venue's own site or the City of Austin / TPWD / St. Edward's page, read Nov 22, 2026
(see research/austin-recharge/). Photos: venues' own sites (Ottine, Bathe, Mantle, Ceremony), TGI's own course photos, and
Wikimedia Commons (credited). No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
SLUG = "austin-recharge-after-the-holidays"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/austin-recharge"
TITLE = "The Austin Recharge: Mineral Springs, Quiet Trails and a Solo Morning Round"
DESC = ("A reset for after the holidays in and around Austin: Ottine Mineral Springs, saunas and cold plunges, winter hikes, "
        "and a walking round on a weekday morning. Prices and hours checked November 22, 2026.")
H1 = "The Austin Recharge"
DEK = "Mineral springs, quiet trails and a solo morning round, for the weeks after the holidays."

# key: (area, name, meta line, copy, url, credit)
P = {
 "barton": ("Zilker Park", "Barton Springs Pool",
   "Free until March 13, 2027 · 5am–10pm, swim at your own risk 5–8am · closed Thursdays 9am–7pm · 68–70°F",
   "Three acres of spring water that holds at 68 to 70 degrees all year, which makes it the city&rsquo;s own cold plunge. In January the 5am crowd is a handful of lap swimmers and steam coming off the water. It is free until mid-March, so there is no reason not to.",
   "https://www.austintexas.gov/services/visit-barton-springs-pool", "Photo: Wordandgesture / Wikimedia Commons, CC BY-SA 3.0"),
 "lions": ("Old West Austin", "Lions Municipal",
   "$35 Monday–Thursday (walking; cart $18) · book online 7 days ahead from 9am · closed the 3rd Monday",
   "Austin&rsquo;s first public course, opened in 1924, and by the city&rsquo;s own account one of the first in the South to desegregate. Take the first tee time you can get on a Tuesday and carry your bag. Read <a href=\"/drops/lions-municipal-golf-course-austin\">our Lions story</a> and the <a href=\"/guides/lions-6\">hole guide</a> before you go.",
   "https://www.austintexas.gov/golfatx", "Photo: The Grassy Issue"),
 "wildbasin": ("West Lake Hills", "Wild Basin Wilderness Preserve",
   "Free on weekdays, no reservation · weekends $5 with a reserved 3-hour pass · about 3 miles of trail",
   "Austin&rsquo;s first nature preserve, 50 years old this year. On a weekday you just drive in; the gate closes when the lot fills. No dogs, no bikes, no picnics, which is most of the point.",
   "https://www.stedwards.edu/academics/centers-institutes-arts/wild-basin/visit", "Photo: Larry D. Moore / Wikimedia Commons, CC BY 4.0"),
 "ottine": ("Gonzales · about 1 hr 15 min", "Ottine Mineral Springs",
   "Tue–Thu $65 all day · Fri $75 · Sat–Sun $75 half day, $125 all day · Thu &amp; Fri sunset soak $35 · closed Mondays · reservations only · 13+",
   "The reason to make the drive. In 1909 oil wildcatters hit an artesian spring here; the water later fed the Gonzales Warm Springs polio hospital, which the site calls &ldquo;the only desegregated place for polio care in the country at the time.&rdquo; Now it is mineral pools around 102 degrees, a hot and cold plunge, a barrel sauna, hammocks and firepits. Go on a Wednesday: they call it Whisper Wednesday and keep it quiet on purpose.",
   "https://ottinemineralsprings.com", "Photo: Ottine Mineral Springs"),
 "mantle": ("East Austin", "Mantle Thermal Haus",
   "Single sessions bookable online · memberships from $100 a month for four hours · Mon 7–11am, Tue–Sat 9am–7pm, Sun 10am–5pm",
   "Two cedar barrel saunas, three cold plunges and a red-light lounge on Curtis Avenue. Small enough to feel like a secret. Their line: &ldquo;discomfort is a pathway.&rdquo;",
   "https://www.mantlethermal.com", "Photo: Mantle Thermal Haus"),
 "ceremony": ("South Lamar", "Ceremony Social Spa",
   "Walk-ins and same-day bookings · weekdays 10am–11pm, weekends 8am–11pm · swimsuits required",
   "&ldquo;Austin&rsquo;s Original BathHouse,&rdquo; with two cedar saunas, indoor and outdoor cold plunges and a tea lounge. The easiest one to say yes to on the way home.",
   "https://ceremonyspa.com", "Photo: Ceremony Spa"),
 "bathe": ("East Austin", "Bathe",
   "Soak passes from $29 · 8am–10pm daily · 18+ · free parking",
   "Saunas, steam, cold plunges and thermal soaking pools, and a Soaking Garden where devices are not allowed. Bathe&rsquo;s own line sums up the whole post: &ldquo;HEAT. COLD. WATER. STILLNESS.&rdquo; Sauna House on North Loop runs the same rule, phone-free, with wood-burning saunas.",
   "https://www.batheaustin.com", "Photo: Bathe"),
 "pedernales": ("Johnson City · 30 miles west", "Pedernales Falls State Park",
   "$6 (13 and up) · reserve a day pass; the park often fills and turns away cars",
   "Twin Falls Nature Trail is half a mile to the overlook; Wolf Mountain is six miles if you want to be tired. TPWD calls it &ldquo;a great place to relax and recharge,&rdquo; which is close enough to the brief.",
   "https://tpwd.texas.gov/state-parks/pedernales-falls", "Photo: Aleksomber / Wikimedia Commons, CC BY-SA 4.0"),
 "hancock": ("Hyde Park", "Hancock Golf Course",
   "$20 any day · 9 holes, par 35 · walking only · no tee times, first come first served · closed January 14",
   "The oldest course in Texas and the purest solo round in town: no pro shop, a pay station, and you play when you get there. Bring a carry bag and nothing else. More in <a href=\"/drops/hancock-golf-course-austin\">our Hancock story</a> and the <a href=\"/guides/hancock-1\">hole guide</a> for the first.",
   "https://www.austintexas.gov/golfatx", "Photo: The Grassy Issue"),
 "kizer": ("Southeast Austin", "Roy Kizer",
   "$35 Monday–Thursday · cart $18 · closed the 4th Monday",
   "Open, flat and windy, and quiet on a weekday morning. A walk you can switch off on. See our <a href=\"/guides/roy-kizer-15\">Kizer hole guide</a> for the par 3 that ruins cards.",
   "https://www.austintexas.gov/golfatx", "Photo: The Grassy Issue"),
 "greenbelt": ("South Austin", "Barton Creek Greenbelt",
   "Free · 7.5-mile main trail · the 360 trailhead has a free lot and restrooms",
   "As long or as short as you want, no reservation, ten minutes from downtown. Start at the 360 trailhead, turn around when you feel like it, and finish with Barton Springs.",
   "https://www.austintexas.gov/parks/locations/barton-creek-greenbelt", "Photo: Julia Duffy / Wikimedia Commons, public domain"),
 "turkey": ("Emma Long Metropolitan Park", "Turkey Creek Trail",
   "$5 a car Mon–Thu, $10 Fri–Sun (buy online ahead on weekends) · no water or fountains until about January 15",
   "Creek crossings and shade on the far west side. Weekdays are the move, and bring your own water this winter.",
   "https://www.austintexas.gov/parks/emma-long-metropolitan-park", "Photo: sbmeaper1 / Wikimedia Commons, CC0"),
 "mayfield": ("Tarrytown", "Mayfield Park",
   "Free · 5am–10pm daily · 23 acres",
   "Ponds, walled gardens and peacocks. The city&rsquo;s page says it best: &ldquo;When you enter Mayfield time slows.&rdquo; A thirty-minute walk, not a hike, and the right way to end an afternoon.",
   "https://www.austintexas.gov/parks/locations/mayfield-park", "Photo: LoneStarMike / Wikimedia Commons, CC BY 3.0"),
 "mckinney": ("Southeast Austin · 13 miles from the Capitol", "McKinney Falls State Park",
   "$6 · gates 8am–10pm · day-pass reservations recommended",
   "&ldquo;Find solitude and beauty in Austin&rsquo;s city limits,&rdquo; says TPWD, and it delivers. The Rock Shelter Trail is 0.6 miles past a 100-foot bald cypress called Old Baldy; the Onion Creek Trail is 2.8.",
   "https://tpwd.texas.gov/state-parks/mckinney-falls", "Photo: Larry D. Moore / Wikimedia Commons, CC BY 4.0"),
 "erock": ("Fredericksburg", "Enchanted Rock",
   "$8 · reserve a pass, January is busy season · trails open 30 minutes before sunrise",
   "The Summit Trail at first light, the whole Hill Country going pink underneath you. The biggest outing here; pack your own water and make a day of it.",
   "https://tpwd.texas.gov/state-parks/enchanted-rock", "Photo: Ligocsicnarf89 / Wikimedia Commons, CC BY 4.0"),
 "lakeaustin": ("Lake Austin", "Lake Austin Spa Resort, LakeHouse Spa",
   "Spa day pass $150 Mon–Thu, $225 Fri–Sun, plus service charge and tax · adults only · book by phone, 512.372.7380",
   "Pool, whirlpool, steam room, dry sauna, quiet rooms, lunch and a robe. The resort lists the pass as ideal for &ldquo;solo retreats,&rdquo; which is the only endorsement this post needs.",
   "https://www.lakeaustin.com/resort/offers/day_pass/", "Photo: Daniel Ziegler / Wikimedia Commons, CC BY-SA 4.0 (Lake Austin)"),
 "lostpines": ("Bastrop · about 20 minutes", "Lost Pines Golf Club",
   "Public tee times online; the rate shows at booking · Arthur Hills, 7,300 yards, par 72",
   "Still Wolfdancer to most of us. The course runs from open pasture down into the loblolly pines and the Colorado River bottom, and the resort singles out the 603-yard 3rd and the downhill 155-yard 12th. Book the first tee time, then the resort spa&rsquo;s sauna. More in our <a href=\"/drops/8-special-day-rounds-near-austin\">special day rounds</a>.",
   "https://www.lostpinesresortandspa.com/golf/", "Photo: The Grassy Issue"),
}

SECTIONS = [
 ("Go When Everyone Else Is at Work", "early", ["barton", "lions", "wildbasin"],
  "The whole thing works because it is a Tuesday. The places that are packed on a Saturday in spring are close to empty on a weekday morning in January: the first tee is yours, the parks don&rsquo;t need a reservation, and Barton Springs opens at five. Take the day off, and take it in the middle of the week."),
 ("Heat, Cold, Stillness", "contrast", ["ottine", "mantle", "ceremony"],
  "The contrast routine is simple. Get hot in a sauna, get cold in a plunge, sit still for a while, and repeat. Austin finally has the places to do it properly, and an hour and a quarter south there is a spring that has been doing it for over a century."),
 ("Leave the Phone in the Car", "phones", ["bathe", "pedernales"],
  "The hardest part of a reset is the thing in your pocket. Pick places that make the decision for you: a bathhouse garden where devices aren&rsquo;t allowed, a sauna with a no-phone rule, a canyon thirty miles out where you won&rsquo;t be checking anything."),
 ("Walk Everything", "walk", ["hancock", "kizer", "greenbelt", "turkey"],
  "No cart, no hurry. A walking round is a different round: you see the course, you talk to nobody, and the score matters less by the ninth hole. Hancock doesn&rsquo;t even offer carts, and we have made <a href=\"/drops/in-defense-of-the-slow-round\">the case for the slow round</a> before. The trails are the long version of the same idea."),
 ("Somewhere Time Slows", "slow", ["mayfield", "mckinney", "erock"],
  "Some places reset your clock just by being old and quiet: a garden of peacocks in Tarrytown, a bald cypress in southeast Austin, a pink granite dome above Fredericksburg."),
 ("Alone, on Purpose", "alone", ["lakeaustin"],
  "Go by yourself. Book a single tee time and see who you get paired with, or nobody. Soak somewhere no one needs anything from you. The holidays are a month of other people&rsquo;s plans, and the reset is the one plan that is only yours."),
 ("One Small Luxury", "luxury", ["lostpines"],
  "Almost everything here is cheap or free, so spend in one place and make it count: the full day at Ottine, the LakeHouse Spa pass, or a first-tee-time morning at Lost Pines with the sauna after."),
]

CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">After</div>
    <h2 class="products-hdr rc-cap" id="food" style="font-size:clamp(28px,4vw,48px)">Warm Food, Slow Coffee</h2>
    <p>Eat something warm, drink your coffee sitting down, and don&rsquo;t take a call. We have already done the work on where: <a href="/drops/the-morning-round-austin-cafes-and-lunch">The Morning Round</a> pairs a café and a lunch with every muni in town, and our <a href="/drops/austin-coffee-guide">Austin coffee guide</a> covers the rest.</p>
    <div class="drop-tag grass" style="margin-top:36px">The Last Word</div>
    <h2 class="products-hdr rc-cap" id="last-word" style="font-size:clamp(28px,4vw,48px)">Do Less, on Purpose</h2>
    <p>None of this needs a plan. Pick one soak, one walk and one round, do them on a weekday, and leave the phone in the car for at least one of them. That is the whole reset. Prices and hours were checked on official sites on November 22, 2026; Deep Eddy Pool is closed for maintenance from November 30, so we left it out. If you have a place that belongs on this list, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""

RELATED = [  # more Austin from TGI in the same spirit (Lenny, 22 Nov: "link this post to other good austin resources of a similar idea")
 ("/drops/in-defense-of-the-slow-round", "/images/slow-round/card-hero.jpg", "In Defense of the Slow Round", "Why the long, unhurried round is the point, not the problem."),
 ("/drops/the-morning-round-austin-cafes-and-lunch", "/images/austin-morning/hero.jpg", "The Morning Round", "Ten cafés before the tee and four lunches after, matched to every muni."),
 ("/drops/8-special-day-rounds-near-austin", "/images/special-day/v2/c7-b0.jpg", "Special Day Rounds Near Austin", "Ten day trips and five overnights, Lost Pines included."),
 ("/drops/golf-trips-mind-body-spirit", "/images/mbs-trips/card-hero.jpg", "Mind, Body, Spirit", "Fifteen public golf trips, and why you should take them alone."),
]


def related():
    cards = "".join(f'<a class="rc-rel" href="{u}"><img src="{i}" alt="" loading="lazy" /><span class="rc-rel-t">{t}</span><span class="rc-rel-d">{d}</span></a>' for u, i, t, d in RELATED)
    return ('\n<section class="products" style="margin-top:8px;padding-top:40px">\n  <div class="drop-tag grass">Keep Going</div>\n'
            '  <h2 class="products-hdr rc-cap" id="more-austin" style="font-size:clamp(28px,4vw,48px)">More Austin, Same Idea</h2>\n'
            '  <p class="rc-sec-intro">If this is your speed, these are the TGI guides that go with it.</p>\n'
            f'  <div class="rc-rels">{cards}</div>\n</section>\n')

CSS = ('<style>/*TGI-RECHARGE v2: denser grid, Lenny 22 Nov "feels like a lot of dead space"*/'
       '.rc-head{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:40px;align-items:end;margin:4px 0 28px}.rc-head .products-hdr{margin:10px 0 0!important}'
       '.rc-sec-intro{font-size:18px;line-height:1.6;margin:0}'
       '.rc-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:36px 28px}'
       '.rc-place{margin:0;display:flex;flex-direction:column}.rc-img{margin:0 0 14px}.rc-img img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;background:#e8e2d6}'
       '.rc-img figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin-top:6px}'
       '.rc-txt{min-width:0}.rc-area{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;margin:0 0 6px}'
       '.rc-name{font-family:var(--serif,Georgia,serif);font-size:clamp(26px,2.6vw,34px);line-height:1.05;margin:0 0 10px}'
       '.rc-meta{font-family:var(--mono);font-size:11px;line-height:1.6;letter-spacing:.03em;margin:0 0 12px;padding:8px 0;border-top:1px solid rgba(45,74,43,.25);border-bottom:1px solid rgba(45,74,43,.25)}'
       '.rc-copy{font-size:16px;line-height:1.6;margin:0 0 12px}.rc-copy a,.rc-link{border-bottom:1px solid currentColor}.rc-link{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase}'
       '.rc-list.solo{display:block}.rc-list.solo .rc-place{flex-direction:row;gap:36px;align-items:center}.rc-list.solo .rc-img{flex:0 0 56%;margin:0}.rc-list.solo .rc-name{font-size:clamp(30px,3.4vw,44px)}'
       '.products.rc-sec{padding-top:0!important}'
       '.rc-open{position:relative;margin:56px 0 0}.rc-open img{width:100%;aspect-ratio:21/9;object-fit:cover;display:block;filter:brightness(.7)}.rc-open .t{position:absolute;left:0;right:0;bottom:0;padding:0 44px 38px;color:#F4F1EA;text-align:left}section.products.rc-sec .rc-open .t h2{color:#F4F1EA;text-align:left!important;margin-left:0!important}.rc-open .n,.rc-plain .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.85}.rc-open h2,.rc-plain h2,.rc-cap{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:clamp(34px,6vw,84px);line-height:1;margin:8px 0 0}.rc-plain{margin:64px 0 0;padding:8px 0 0;text-align:center}.rc-plain h2{color:#2D4A2B}.rc-plain .n{opacity:.6}.rc-cr{font-family:var(--mono);font-size:9px;letter-spacing:.06em;text-transform:uppercase;opacity:.55;margin:6px 0 0;text-align:right}.rc-pill{max-width:820px;margin:28px auto 40px;font-family:var(--serif);font-size:20px;line-height:1.55;text-align:center;opacity:.85}.rc-hd{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:end;border-bottom:.5px solid var(--ink);padding-bottom:10px;margin-bottom:12px}.rc-num{font-family:var(--serif);font-size:64px;line-height:.8;color:#2D4A2B}.rc-hd .rc-name{font-weight:400;margin:0;letter-spacing:-.01em}.rc-hd .rc-area{margin:8px 0 0;opacity:.6}.rc-meta{border-top:0!important}.rc-toc{margin:8px 0 0;display:grid;grid-template-columns:repeat(4,1fr);border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}.rc-toc>div{padding:22px 24px;border-right:.5px solid rgba(20,20,20,.2);border-bottom:.5px solid rgba(20,20,20,.2)}.rc-toc>div:nth-child(4n){border-right:none}.rc-toc>div:nth-last-child(-n+4){border-bottom:none}.rc-toc h3{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:16px;line-height:1.2;color:#2D4A2B;margin:0 0 10px}.rc-toc h3 a,.rc-toc li a{border-bottom:none;text-decoration:none;color:inherit}.rc-toc ol{list-style:none;padding:0;margin:0}.rc-toc li{font-family:var(--serif);font-size:16px;padding:5px 0;border-bottom:.5px dotted rgba(20,20,20,.2)}.rc-toc li span{font-family:var(--mono);font-size:10px;opacity:.5;margin-right:10px}@media(max-width:900px){.rc-toc{grid-template-columns:1fr 1fr}.rc-toc>div{border-right:.5px solid rgba(20,20,20,.2)!important;border-bottom:.5px solid rgba(20,20,20,.2)!important}.rc-toc>div:nth-child(2n){border-right:none!important}}@media(max-width:760px){.rc-open img{aspect-ratio:4/3}.rc-open .t{padding:0 18px 22px}.rc-toc{grid-template-columns:1fr}.rc-toc>div{border-right:none!important}.rc-num{font-size:48px}.rc-pill{font-size:18px}}'
       '.drop-tag.grass{background:none!important;color:#2D4A2B!important;border:0!important;padding:0!important;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.75}'  # Lenny 22 Nov: green label boxes threw off the design -> plain text labels
       '.rc-rels{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:20px}.rc-rel{display:block;text-decoration:none;color:inherit}.rc-rel img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#e8e2d6;margin-bottom:10px}.rc-rel-t{display:block;font-family:var(--serif,Georgia,serif);font-size:20px;line-height:1.15;margin-bottom:4px}.rc-rel-d{display:block;font-size:14px;line-height:1.45;opacity:.8}@media(max-width:820px){.rc-rels{grid-template-columns:repeat(2,1fr)}}'
       '@media(max-width:760px){.rc-head{grid-template-columns:1fr;gap:12px}.rc-list.solo .rc-place{flex-direction:column;align-items:stretch;gap:0}.rc-list.solo .rc-img{margin:0 0 14px}}</style>\n')


BANDS = {  # Lenny 22 Nov "needs more TGI flavor": Mind/Body/Spirit-style opener bands
 "early": ("Diving board at Barton Springs Pool", "Photo: Todd Dwyer / Wikimedia Commons, CC BY-SA 2.0"),
 "contrast": ("Barrel sauna beside the cold plunge at Ottine Mineral Springs", "Photo: Ottine Mineral Springs"),
 "phones": ("The Pedernales River bending through the canyon", "Photo: Corey Leopold / Wikimedia Commons, CC BY 2.0"),
 "walk": ("Cypress trees on the Lake Austin shore at Emma Long Park", "Photo: Larry D. Moore / Wikimedia Commons, CC BY 4.0"),
 "slow": ("Aerial view of Enchanted Rock", "Photo: Jmbuytaert / Wikimedia Commons, CC BY-SA 4.0"),
}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
NUM = {k: n + 1 for n, k in enumerate(k for sec in SECTIONS for k in sec[2])}


def place(k):
    area, name, meta, copy, url, credit = P[k]
    return (f'  <div class="rc-place" id="{k}">\n'
            f'    <figure class="rc-img"><img src="{IMG}/{k}.jpg" alt="{H.escape(H.unescape(name))}" loading="lazy" /><figcaption>{credit}</figcaption></figure>\n'
            f'    <div class="rc-txt"><div class="rc-hd"><div class="rc-num">{NUM[k]:02d}</div><div><h3 class="rc-name">{name}</h3><p class="rc-area">{area}</p></div></div><p class="rc-meta">{meta}</p>'
            f'<p class="rc-copy">{copy}</p><a class="rc-link" href="{url}" target="_blank" rel="noopener">Official site &#8599;</a></div>\n  </div>\n')


def section(i, sec):
    h2, anchor, keys, intro = sec
    solo = " solo" if len(keys) == 1 else ""
    n = f'Part {ROMAN[i-1]} &middot; {len(keys)} place{"s" if len(keys) > 1 else ""}'
    if anchor in BANDS:
        alt, cr = BANDS[anchor]
        opener = (f'<div class="rc-open"><img src="{IMG}/band-{anchor}.jpg" alt="{alt}" loading="lazy" />'
                  f'<div class="t"><div class="n">{n}</div><h2 id="{anchor}">{h2}</h2></div></div>'
                  f'<p class="rc-cr">{cr}</p>')
    else:
        opener = f'<div class="rc-plain"><div class="n">{n}</div><h2 id="{anchor}">{h2}</h2></div>'
    return (f'\n<section class="products rc-sec" style="margin-top:8px;">\n  {opener}\n'
            f'  <p class="rc-pill">{intro}</p>\n  <div class="rc-list{solo}">\n' + "".join(place(k) for k in keys) + '  </div>\n</section>\n')


def toc():
    cols = "".join(f'<div><h3><a href="#{s[1]}">{s[0]}</a></h3><ol>' + "".join(f'<li><span>{NUM[k]:02d}</span><a href="#{k}">{P[k][1]}</a></li>' for k in s[2]) + '</ol></div>' for s in SECTIONS)
    cols += ('<div><h3><a href="#food">After</a></h3><ol><li><span>&mdash;</span><a href="#food">Warm Food, Slow Coffee</a></li>'
             '<li><span>&mdash;</span><a href="#last-word">The Last Word</a></li><li><span>&mdash;</span><a href="#more-austin">More Austin</a></li></ol></div>')
    return f'<nav class="rc-toc" aria-label="The vibes and the places">{cols}</nav>\n'


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-22", "dateModified": "2026-11-22",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "The Austin Recharge", "item": URL}]},
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
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  The Austin Recharge</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 22, 2026</p><!--/TGI-BY-->
  <p style="font-size:20px;font-style:italic;max-width:640px;margin:10px auto 0">{DEK}</p>
  <div class="drop-meta">
    <span>Field Note</span><span class="dot"></span>
    <span>{len(P)} places &middot; checked November 22, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The mineral pools at Ottine Mineral Springs at sunset, loungers and umbrellas around the water" fetchpriority="high" /></div></div>

<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The holidays end and January starts and most of us need about a week of nothing before we are any use to anyone. This is a guide to doing that nothing well, without leaving Central Texas.</p>
    <p>It isn&rsquo;t a schedule. It is eight ideas about what a reset actually needs, with the places in and around Austin that do each one best: hot mineral water an hour south, saunas and cold plunges in town, winter trails, and a round of golf on a weekday morning with nobody waiting behind you.</p>
    <p>Every price, hour and rule below comes from the place&rsquo;s own site, or the city or state parks page, read on November 22, 2026. Things change in winter, so check before you drive.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Best days</span><span>Tuesday to Thursday</span></div>
      <div class="sidebar-detail"><span class="l">The drive</span><span>Ottine, about 1 hr 15 min</span></div>
      <div class="sidebar-detail"><span class="l">Free</span><span>Barton Springs, the Greenbelt, Mayfield, Wild Basin on weekdays</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest round</span><span>Hancock, $20, walking</span></div>
      <div class="sidebar-detail"><span class="l">The splurge</span><span>LakeHouse Spa pass or Lost Pines</span></div>
    </div>
  </aside>
</section>
"""
    body += '<section class="products" style="padding-top:0;margin-top:0">' + toc() + '</section>\n'
    for i, s in enumerate(SECTIONS, 1):
        body += section(i, s)
    body += CLOSE
    body += related()
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Mackem"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html · {len(P)} places")


if __name__ == "__main__":
    main("--apply" in sys.argv)
