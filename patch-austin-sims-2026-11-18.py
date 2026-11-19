import re, json, importlib, sys
sys.path.insert(0,'.')
F='drops/austin-indoor-golf-simulators.html'
h=open(F,encoding='utf-8').read()
def R(old,new,count=1):
    global h
    n=h.count(old)
    assert n==count, (n, old[:90])
    h=h.replace(old,new)

# --- meta / counts
OLD_DESC="Fourteen indoor golf simulators across the Austin metro you can book this week — verified tech, bay counts, hourly rates and membership pricing — plus the five on the way and the two that are not open yet despite what you have read."
NEW_DESC="Fifteen indoor golf simulators across the Austin metro you can book this week — verified tech, bay counts, hourly rates and membership pricing — plus the ones on the way, including Five Iron downtown."
R(OLD_DESC,NEW_DESC,h.count(OLD_DESC) or 1)
R("one of fourteen indoor golf simulators","one of fifteen indoor golf simulators",h.count("one of fourteen indoor golf simulators"))
R("Updated September 29, 2026","Updated November 18, 2026")
R("Austin, Texas &middot; 14 Rooms","Austin, Texas &middot; 15 Rooms")

# --- intro
R("Austin has fourteen indoor golf simulators you can book this week, and four of them did not exist eighteen months ago.",
  "Austin has fifteen indoor golf simulators you can book this week, and six of them did not exist eighteen months ago.")
R("The new rooms opened in <strong>Georgetown, Hutto, San Marcos and far southwest Austin</strong>. Downtown still has none. The one announced for Congress Avenue has a signed lease and no date.",
  "The new rooms opened in <strong>Cedar Park, Georgetown, Hutto, San Marcos, Manchaca and far southwest Austin</strong>. Downtown still has none. The one coming to Congress Avenue now says December.")
i=h.index("Two housekeeping notes before the list"); j=h.index("</p>",i)
h=h[:i]+("Two housekeeping notes before the list. <strong>Five Iron Golf is not open yet.</strong> The lease at 501 Congress was signed in January, and Five Iron now lists Austin as coming soon with a December opening, so it sits in the Coming section below. <strong>Southside Golf Co is open.</strong> When we first published this guide it was still an opening list; its TrackMan bays are now bookable online, and it has moved into the main list.")+h[j:]

# --- at-a-glance table
R("All Fourteen, At a Glance","All Fifteen, At a Glance")
R("every figure here was read on the venue&rsquo;s own site on 9/16/26.","every figure here was read on the venue&rsquo;s own site on 9/16/26 and rechecked on 11/18/26 wherever the site would load.")
rows=re.findall(r'        <tr><td[^\n]*</tr>\n',h)
def row(dom): return [r for r in rows if dom in r][0]
r1872=row('1872gc.com'); rx=row('playxgolf.com'); ratx=row('atxindoorgolfclub.com')
new1872=re.sub(r'<span style="opacity:.55;">not published</span>','$40',r1872)
assert new1872!=r1872
southside=rx.replace(re.search(r'href="([^"]+)"',rx).group(1),"https://southsidegolfco.com/golf-simulator-austin?utm_source=thegrassyissue&amp;utm_medium=referral&amp;utm_campaign=editorial&amp;utm_content=austin-indoor-golf-simulators")
southside=southside.replace(">X-Golf Cedar Park<",">Southside Golf Co<").replace(">Cedar Park<",">Manchaca<",1).replace(">X-Golf<",">TrackMan<").replace("$55&ndash;65","$60&ndash;75")
assert ">Southside Golf Co<" in southside and ">Manchaca<" in southside and ">TrackMan<" in southside and "$60&ndash;75" in southside, southside[-400:]
h=h.replace(r1872,"")
h=h.replace(ratx,new1872+ratx)          # $40 sorts just before ATX ($40-50)
h=h.replace(rx,rx+southside)            # $60-75 sorts after X-Golf ($55-65), before Fiber ($70)
R("Four venues do not publish an hourly figure anywhere; those entries link straight","Three venues do not publish an hourly figure anywhere; those entries link straight")

# --- Spare Birdie contradiction
R("The cheapest confirmed bay in the metro and it is not close:","The cheapest in-town bay, beaten only by Austin Indoor Golf out in Pflugerville:")

# --- Fiber
R("memberships at $250 and $350 a month.","memberships from $300 a month.")

# --- Dr. Golf
R("Memberships run on promotional pricing through 9/30/26 with the $49 initiation waived &mdash; $90 a month single off-peak up to $270 family regular, plus tax.",
  "Memberships run on promotional pricing through 12/31/26 with the $49 initiation waived &mdash; $90 a month single off-peak up to $220 family, plus tax.")

# --- 1872
R("Members get 24/7; the public gets Monday to Friday 2 to 8, Saturday 12 to 8 and Sunday 12 to 6.",
  "Members get 24/7; the public gets Monday to Friday 2 to 8, Saturday 12 to 8 and Sunday 12 to 6, though the hours shift around football season and the homepage advertises walk-ins from 10, so check the day you go.")
R("Memberships are Eagle at $299 a month, Birdie at $250, and corporate tiers",
  "Memberships are Eagle at $299 a month, Birdie at $250, Par at $175 and Bogey at $99, with corporate tiers")
R("They publish membership dues but not a public hourly rate.","The public rate is now published: $40 a bay per hour.")
R("Three of the four rooms that opened in the last year are out here, not in town.","Most of the rooms that opened in the last year are out here, not in town.")

# --- Halftime caveat
R("No rate is published, and no street address either &mdash; which is also why they are the one room missing from the map above.",
  "No rate is published, and no street address either &mdash; which is also why they are the one room missing from the map above. We could not confirm its current status online in November, so call before you drive out.")

# --- Southside into the coaching section
R("One room in Austin is a coaching academy that happens to rent bays, rather than the reverse.",
  "Two rooms in Austin are built around coaching first and bay rental second.")
sec_i=h.index("Two rooms in Austin are built around coaching first"); sec_end=h.index("</section>",sec_i)
SS=("""  <div class="writeup-body">
    <p><strong>Southside Golf Co &mdash; 11215 Conroy Lane, Manchaca.</strong> The newest room in the metro, and the reason this guide was updated. Private TrackMan bays from PGA professional Justin Aragon, booked online up to five days ahead with a two-hour maximum. <strong>$60 per bay per hour Monday through Thursday and Friday until 3, $75 from Friday at 3 through Sunday</strong>, up to four players with no per-player fee, tax added. Founding memberships run from $89 a month up to $299 for unlimited range time. Instruction, fitting, club repair and regripping all happen alongside the bays. Open 10 to 10, and until 11 on Friday and Saturday.</p>
  </div>
""")
h=h[:sec_end]+SS+h[sec_end:]

# --- tech
R("Five systems are in use across these fourteen rooms","Five systems are in use across these fifteen rooms")
R("In Austin: Golfinity upstairs, ROK, Bogey Master, Man Cave, Dr. Golf Studio&rsquo;s Studio Bay 5.","In Austin: Golfinity upstairs, ROK, Southside, Bogey Master, Man Cave, Dr. Golf Studio&rsquo;s Studio Bay 5.")
R("1872 Golf Club in Georgetown runs Foresight, 512 Golf Co will, and Dr. Golf Studio keeps a GCQuad in Bay 6.","1872 Golf Club in Georgetown runs Foresight, and Dr. Golf Studio keeps a GCQuad in Bay 6.")

# --- breakeven
fib=[r for r in re.findall(r'<tr><td[^\n]*?</tr>',h) if '>Fiber Golf</td>' in r][0]
nf=fib.replace('>$250<','>$300<').replace('about 3.5 hrs','just over 4 hrs'); assert nf!=fib and 'just over 4' in nf
h=h.replace(fib,nf)
b9b=[r for r in re.findall(r'<tr><td[^\n]*?</tr>',h) if 'The Back Nine &mdash; Birdie' in r][0]
ss_row=(b9b.replace('The Back Nine &mdash; Birdie','Southside Golf Co &mdash; Range').replace('>$295<','>$299<')
        .replace('unlimited, 2-hr slots','unlimited').replace('$60 South','$60 weekday').replace('about 5 hrs','5 hrs'))
assert ss_row!=b9b
h=h.replace(b9b,b9b+'\n        '+ss_row)
R("ROK, Bogey Master, Halftime Co. and 1872 are absent because none publishes an hourly rate to measure a membership against. Dr. Golf Studio&rsquo;s figures are promotional through 9/30/26.",
  "ROK, Bogey Master and Halftime Co. are absent because none publishes an hourly rate to measure a membership against, and 1872 does not spell out the hours its tiers include. Dr. Golf Studio&rsquo;s figures are promotional through 12/31/26.")

# --- coming section
ci=h.index('<h2 class="products-hdr">On the Way</h2>'); ce=h.index("</section>",ci)
COMING='''<h2 class="products-hdr">On the Way</h2>
  <p class="cat-kicker">Four more, with what is actually known about each. None of these is bookable today.</p>
  <div class="writeup-body">
    <p><strong>Five Iron Golf &mdash; 501 Congress Avenue. December 2026.</strong> Thirteen and a half thousand square feet, twelve TrackMan simulators, a full bar and restaurant, duckpin bowling, event space, Callaway Tour fitting and a connected fitness facility with locker rooms. The lease was signed 1/20/26, and Five Iron&rsquo;s locations page now lists Austin Congress as coming soon, opening in December, with founding memberships from $159 a month. When it lands it will be the only simulator downtown, which remains the strangest gap on this map.</p>
    <p><strong>Another Nine &mdash; 210 Blue Springs Blvd, Suite 102, Georgetown. Late January 2027.</strong> TrackMan iO on Virtual Golf 3 with 350-plus courses, and a different shape to everyone else: <strong>fully private self-service suites</strong> rather than open bays, up to five guests each, 24/7, hourly, no membership required, mini fridge in every suite. Franchise owner Soham Thakker told What Now Austin in late October that permitting and design pushed the opening back a month, though the chain&rsquo;s own page still says December. The chain now lists twenty-five locations, and a second Austin-area suite is listed as coming soon at 1060 Hero Way in Leander, with no date yet.</p>
    <p><strong>Golf Lounge 18 &mdash; 12901 N I-35, Shops at Tech Ridge. Early 2027.</strong> Twelve thousand square feet, twelve TrackMan bays, 450-plus courses, full bar and kitchen. The state filing puts a $500,000 interior build across 11,600 square feet; the chain&rsquo;s homepage now says spring 2027 and its Austin page says just after New Year&rsquo;s. It would be the chain&rsquo;s first location in Texas, and the largest sim project announced for the metro.</p>
    <p><strong>The Mackenzie Club &mdash; 260 Addie Roy Road, West Lake Hills. Spring 2027.</strong> A private, three-story indoor golf club with eight TrackMan suites, which Community Impact reported in October is now targeting spring 2027. Members only, like Man Cave, so it will not be a drop-in option.</p>
  </div>
'''
h=h[:ci]+COMING+h[ce:]

# --- choose
R("Answer these four and fourteen rooms come down to two.","Answer these four and fifteen rooms come down to two.")

# --- FAQ visible + schema
FAQ_NEW={
 "Is Five Iron Golf open in Austin yet?":"Not yet. Five Iron signed a lease for 501 Congress Avenue on 1/20/26 for a 13,500 square foot flagship with twelve TrackMan simulators. As of 11/18/26 its locations page lists Austin Congress as coming soon, and the Austin page says it opens in December 2026, with founding memberships from $159 a month.",
 "Is Southside Golf Co open?":"Yes. Southside Golf Co at 11215 Conroy Lane in Manchaca is open, and its private TrackMan bays are bookable online up to five days ahead. Rates are $60 per bay per hour Monday through Thursday and Friday until 3pm, and $75 from Friday at 3pm through Sunday, covering up to four players.",
 "Which simulator has TrackMan?":"Golfinity's upstairs bays, ROK Golf at both locations, Southside Golf Co, Bogey Master, Man Cave and Dr. Golf Studio's Studio Bay 5 all run TrackMan. Fiber Golf and ATX Indoor Golf Club run the newer TrackMan iO. The Back Nine, Spare Birdie, Swing Station and Austin Indoor Golf run Full Swing; 1872 runs Foresight; X-Golf runs its own proprietary system.",
 "Is there a golf simulator in downtown Austin?":"Not yet. As of 11/18/26 there is no indoor simulator in downtown Austin. Five Iron's 501 Congress location would be the first, and it says it opens in December 2026. The nearest options today are ROK Golf in Westlake and ATX Indoor Golf Club on US 290.",
}
def ent(s): return s.replace("'","&rsquo;")
for q,a in FAQ_NEW.items():
    m=re.search(r'(<summary>'+re.escape(q)+r'</summary><p>)(.*?)(</p>)',h,re.S); assert m,q
    h=h[:m.start(2)]+ent(a)+h[m.end(2):]
    m=re.search(r'("name": "'+re.escape(q)+r'", "acceptedAnswer": \{"@type": "Answer", "text": ")(.*?)(")',h); assert m,("schema",q)
    h=h[:m.start(2)]+json.dumps(a)[1:-1]+h[m.end(2):]

# --- map: regenerate from sims_map with Southside open
import sims_map
src=open('sims_map.py').read()
src=src.replace(' ("southside","Southside Golf Co",    30.14077, -97.83306, "coming", False),\n','')
src=src.replace(' ("b9rr",   "Back Nine Round Rock",   30.53900, -97.55600, "open",   False),\n',
                ' ("b9rr",   "Back Nine Round Rock",   30.53900, -97.55600, "open",   False),\n ("southside","Southside Golf Co",    30.14077, -97.83306, "open",   False),\n')
src=src.replace('aria-label="Map of 21 open and 4 upcoming','aria-label="Map of 22 open and 3 upcoming')
src=src.replace('Austin metro &#183; 9/16/26','Austin metro &#183; 11/18/26')
src=src.replace('Twenty-one open rooms and four on the way, plotted','Twenty-two open rooms and three on the way, plotted')
src=src.replace('<strong>Halftime Co.</strong> in Kyle and <strong>512 Golf Co</strong> are missing from the map entirely because neither publishes a street address to plot. Coordinates from OpenStreetMap, 9/16/26.',
                '<strong>Halftime Co.</strong> in Kyle is missing from the map entirely because it publishes no street address to plot, and Another Nine&rsquo;s Leander suite and The Mackenzie Club are not plotted yet. Coordinates from OpenStreetMap, 9/16/26; Southside moved to open on 11/18/26.')
src=src.replace('the only pin inside the urban core is an amber one that has no opening date.','the only pin inside the urban core is an amber one, Five Iron, which says December.')
for k in ['"open",   False),\n ("southside"','22 open and 3','11/18/26','Twenty-two open','Halftime Co.</strong> in Kyle is missing','Five Iron, which says December']:
    assert k in src,k
open('sims_map.py','w').write(src)
importlib.reload(sims_map)
ms=sims_map.section()
mi=h.index('<section class="products">\n  <h2 class="products-hdr">The Map</h2>'); me=h.index('</section>',mi)+len('</section>\n')
h=h[:mi]+ms+h[me:]

# --- guards
txt=re.sub(r'<[^>]+>',' ',h[h.index('<h1'):h.index('<!-- TGI-ONE-FOOTER -->') if '<!-- TGI-ONE-FOOTER -->' in h else len(h)])
for bad in ['512 Golf','fourteen','Fourteen','9/30/26','$270','$75 anytime','No date.','nineteen-location']:
    assert bad not in txt, bad
assert not re.search(r'\bworth\b',re.sub(r'Fort\s+Worth','',txt),re.I)
open(F,'w',encoding='utf-8').write(h)
print('ok')
