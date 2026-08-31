#!/usr/bin/env python3
"""build-lions.py — Lions Muny deep dive on the Hancock chassis.

Clones the head CSS, nav, search block, ENT block and analytics tail from
drops/hancock-golf-course-austin.html (the proven Field Notes deep-dive
template) and injects all-new Lions content. Facts + verbatim quotes from
research/lions-muny-dossier.md — quotes are verbatim from the USGA piece
(Trostel, 2019). Slug: drops/lions-municipal-golf-course-austin.
"""
import re, os

S = os.path.dirname(os.path.abspath(__file__))
han = open(os.path.join(S, "drops", "hancock-golf-course-austin.html"), encoding="utf-8").read()

# ---- pieces reused from the chassis ----
css_main = re.search(r'(<link rel="preconnect".*?</style>)\s*<style>\s*/\*TGI-FAQ-V1\*/', han, re.S).group(1)
css_faq  = re.search(r'(<style>\s*/\*TGI-FAQ-V1\*/.*?</style>)', han, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', han, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', han, re.S).group(1)

URL   = "https://thegrassyissue.com/drops/lions-municipal-golf-course-austin"
TITLE = "Lions Municipal Golf Course — The Most Important Muni in Texas Is Still Open. Go Play It."
DESC  = ("Lions Municipal — Muny — has been Austin's public course since 1924, and in 1950 it became "
         "the first integrated municipal course in the South. The history, the fight over the UT lease, "
         "the Coore & Crenshaw restoration plan, and everything to know before you play it.")

FAQS = [
 ("Why is Lions Municipal Golf Course historically significant?",
  "In 1950, two Black youths — one of them Alvin Propps, a nine-year-old caddie at the course — played Muny in defiance of Jim Crow laws. Instead of prosecuting them, the city let them finish, and the council opened the course to all golfers. That made Lions the first integrated municipal course south of the Mason-Dixon Line, four years before Brown v. Board of Education. The course was listed on the National Register of Historic Places in 2016 as a civil rights landmark."),
 ("How much does it cost to play Lions Municipal?",
  "As of October 2025, a regular round is $35 Monday through Thursday, $41 on Friday and $44 on weekends and holidays. Evening rounds run $29 to $34, sunset is $28, juniors pay $20 and seniors $27 on weekdays. Nine holes is $28 any day. Carts are $18 per person. The pro shop takes cards only, no cash."),
 ("How long is Lions Municipal Golf Course?",
  "It is an 18-hole, par-71 layout at 5,825 yards from the back tees — short on the card, but the sharp doglegs ask for placement over distance, and the limestone ground runs the ball out when it's dry. The front nine leans on doglegs, bunkers and elevation; the water shows up on the back."),
 ("Why might Lions Municipal close?",
  "The course sits on 141 acres of the Brackenridge Tract, land deeded to the University of Texas in 1910. The city's long-term lease expired in 2019, and Muny has run on short rolling extensions since while UT has explored redeveloping the land. The Muny Conservancy, with Ben Crenshaw among its founders, is raising money toward a permanent agreement, and the Texas legislature extended the Save Historic Muny District through May 2027."),
 ("What is the Coore & Crenshaw plan for Muny?",
  "Bill Coore and Ben Crenshaw — the firm behind Sand Valley and Friar's Head — proposed a restoration of Muny in 2017 and have offered their design services at no cost. The plan restores the course toward its pre-1974 layout and turns the old clubhouse into an education center and golf museum honoring the course's civil rights history."),
 ("How do tee times work at Lions?",
  "Online tee times for Monday through Thursday open at 9 a.m. seven days in advance. Weekend times drop the preceding Monday at 8 p.m., online only, and you need a user account. The pro shop answers the phone 30 minutes before the first tee time at (512) 978-6869 — that spells MUNY."),
]

faq_schema = ",\n  ".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (repr(q).replace("'", '"', 1)[:0] or __import__("json").dumps(q), __import__("json").dumps(a))
    for q, a in FAQS)
faq_html = "\n    ".join(
    '<details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a)
    for q, a in FAQS)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITLE} &mdash; The Grassy Issue</title>
<meta name="description" content="{DESC}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{TITLE}" />
<meta property="og:description" content="{DESC}" />
<meta property="og:image" content="https://thegrassyissue.com/images/lions/hero.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE}" />
<meta name="twitter:description" content="1924. First integrated course in the South, 1950. Crenshaw learned here. Still $35 on a weekday." />
<link rel="canonical" href="{URL}" />
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "Article",
 "headline": "{TITLE}",
 "description": "{DESC}",
 "url": "{URL}",
 "datePublished": "2026-08-31",
 "dateModified": "2026-08-31",
 "author": {{"@type": "Organization", "name": "The Grassy Issue"}},
 "publisher": {{"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}},
 "mainEntityOfPage": {{"@type": "WebPage", "@id": "{URL}"}},
 "about": {{
  "@type": "GolfCourse",
  "name": "Lions Municipal Golf Course",
  "address": {{"@type": "PostalAddress", "streetAddress": "2901 Enfield Rd.", "addressLocality": "Austin", "addressRegion": "TX", "postalCode": "78703", "addressCountry": "US"}},
  "telephone": "+1-512-978-6869",
  "url": "https://www.austintexas.gov/golfatx/lions-municipal-course"
 }}
}}
</script>
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {faq_schema}
 ]
}}
</script>
{css_main}
{css_faq}
</head>
<body>
{nav}

<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Lions Municipal</div>

<header class="drop-header">
  <span class="drop-tag grass">[Field Notes]</span>
  <h1>Lions Municipal &mdash; The Most Important Muni in Texas Is Still Open. Go Play It.</h1>
  <div class="drop-meta">
    <span>August 31, 2026</span><span class="dot"></span>
    <span>Field Guide</span><span class="dot"></span>
    <span>Est. 1924 &middot; First Integrated Course in the South</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="/images/lions/hero.jpg" alt="The 16th hole at Lions Municipal Golf Course in Austin, Texas — fairway, water and live oaks" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>Two miles from the Capitol, on the west side where the streets go quiet and the live oaks close over the road, there are 141 acres that never got built on. Everyone in Austin calls it Muny. The scorecard says Lions Municipal, established 1924, and the practice green has a stone lion in the middle of it that kids climb while their parents putt.</p>
    <p>It is the city&rsquo;s oldest public course &mdash; about 60,000 rounds a year, $35 on a weekday, dogs welcome. Hogan played here. So did Byron Nelson, Sandra Haynie and Betsy Rawls. Tom Kite and Ben Crenshaw grew up on it. Texas&rsquo; oldest amateur tournament, the Firecracker Open, still runs here every Fourth of July weekend.</p>
    <p>And for most of the last decade, nobody has known how long any of that gets to continue. The land belongs to the University of Texas, the long-term lease ran out in 2019, and the course has been living on short extensions ever since &mdash; which is a strange way to treat the site of one of the quietest, earliest civil rights victories in the South.</p>
    <p>That story is below. First, the course.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1924</span></div>
      <div class="sidebar-detail"><span class="l">Layout</span><span>18 holes, par 71</span></div>
      <div class="sidebar-detail"><span class="l">Length</span><span>5,825 yards</span></div>
      <div class="sidebar-detail"><span class="l">Green fee</span><span>$35&ndash;$44</span></div>
      <div class="sidebar-detail"><span class="l">Address</span><span>2901 Enfield Rd.</span></div>
      <div class="sidebar-detail"><span class="l">Phone</span><span>512-978-MUNY</span></div>
      <a href="https://www.austintexas.gov/golfatx/lions-municipal-course" target="_blank" rel="noopener" class="sidebar-cta">Course Info at GolfATX ↗</a>
      <div class="hashtags">
        <span class="hashtag">#LionsMunicipal</span>
        <span class="hashtag">#SaveMuny</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#BenCrenshaw</span>
        <span class="hashtag">#Tarrytown</span>
      </div>
    </div>
  </aside>
</div>

<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;I can&rsquo;t imagine this place not being here. &lsquo;Muny&rsquo; means so much to this community.&rdquo;<span class="pull-quote-attr">&mdash; Ben Crenshaw, to the USGA, 2019</span></div>
</div>

<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr">The Course</h2>
  <div class="ig-grid">
    <figure><img src="/images/lions/aerial.jpg" alt="Aerial view of Lions Municipal Golf Course, 141 green acres in West Austin" loading="lazy" /><figcaption class="ig-cap">141 acres, city on every side &mdash; photo The Muny Conservancy</figcaption></figure>
    <figure><img src="/images/lions/hole16.jpg" alt="The 16th hole at Lions Municipal Golf Course, Austin" loading="lazy" /><figcaption class="ig-cap">Hogan&rsquo;s Hole, the 16th &mdash; photo Magnushopium, CC0</figcaption></figure>
    <figure><img src="/images/lions/dusk.jpg" alt="Evening light under the live oaks at Lions Municipal" loading="lazy" /><figcaption class="ig-cap">Under the oaks at dusk &mdash; photo The Muny Conservancy</figcaption></figure>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">1950 &mdash; &ldquo;Let Them Play&rdquo;</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>In the latter half of 1950, a nine-year-old Black caddie named Alvin Propps and another Black youth walked onto the course and played it, in open defiance of the Jim Crow laws of the era. They were detained. Mayor Taylor Glass conferred with council members and made a decision that took five words: let them play. The two finished their round. Rather than build a separate course, the council opened Muny to every golfer in Austin.</p>
    <p style="margin-top:16px">That made Lions the first integrated municipal course south of the Mason-Dixon Line &mdash; in 1950, four years before Brown v. Board of Education, at a time when the schools two miles away were still segregated. Word traveled. Through the fifties and sixties, Black golfers came from all over Texas to play here; buses shuttled players in from other parts of the state, and Joe Louis &mdash; the heavyweight champion, and a tireless advocate for Black golfers &mdash; held clinics at Lions that drew thousands.</p>
    <p style="margin-top:16px">General Marshall, who caddied at Lions from 1946 to 1950, put it this way to the USGA: &ldquo;I wish I could express how good I felt. When they integrated this course, black golfers from all over the state of Texas would come here to play golf.&rdquo;</p>
    <p style="margin-top:16px">This is why the course is on the National Register of Historic Places, and why the National Trust for Historic Preservation put it on its list of America&rsquo;s most endangered historic places. Not the architecture. The afternoon in 1950.</p>
  </div>
  <div class="ig-grid" style="margin-top:28px;max-width:1000px;">
    <figure><img src="/images/lions/hist-fairway.jpg" alt="Golfers on the fairway at Lions Municipal in the early years, black and white archival photo" loading="lazy" /><figcaption class="ig-cap">The early years &mdash; archival, via The Muny Conservancy</figcaption></figure>
    <figure><img src="/images/lions/hist-green.jpg" alt="Four golfers on a green at Lions Municipal, black and white archival photo" loading="lazy" /><figcaption class="ig-cap">On the green &mdash; archival, via The Muny Conservancy</figcaption></figure>
    <figure><img src="/images/lions/clubhouse.jpg" alt="The Lions Municipal clubhouse behind the practice green" loading="lazy" /><figcaption class="ig-cap">The clubhouse today &mdash; photo Larry D. Moore, CC BY 4.0</figcaption></figure>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">A Century, Short Version</h2>
  <div class="tl">
    <div class="tl-row"><div class="tl-year">1910</div><div class="tl-text">Colonel George Washington Brackenridge deeds 350 acres along the river to the University of Texas, &ldquo;for the purpose of advancing and promoting University education.&rdquo; Muny&rsquo;s 141 acres sit inside that tract &mdash; the fact that everything since hangs on.</div></div>
    <div class="tl-row"><div class="tl-year">1924</div><div class="tl-text">The Austin Lions Club leases part of the tract and opens the city&rsquo;s first public course &mdash; nine holes at first, later expanded to 18.</div></div>
    <div class="tl-row"><div class="tl-year">1936</div><div class="tl-text">The lease transfers to the City of Austin. The name &mdash; Lions Municipal &mdash; stays.</div></div>
    <div class="tl-row"><div class="tl-year">1950</div><div class="tl-text">Alvin Propps and a friend play in defiance of Jim Crow. The city lets them finish, then opens the course to all &mdash; the first integrated muni in the South.</div></div>
    <div class="tl-row"><div class="tl-year">1974</div><div class="tl-text">The course is redesigned into the routing you play today. The restoration plan on the table now aims back at the original.</div></div>
    <div class="tl-row"><div class="tl-year">2016</div><div class="tl-text">Listed on the National Register of Historic Places as a civil rights landmark.</div></div>
    <div class="tl-row"><div class="tl-year">2017</div><div class="tl-text">Bill Coore and Ben Crenshaw put forward a restoration proposal &mdash; their design work offered at no cost.</div></div>
    <div class="tl-row"><div class="tl-year">2019</div><div class="tl-text">The long-term lease expires. Muny begins operating on short rolling extensions. The Muny Conservancy forms to raise money for a permanent deal.</div></div>
    <div class="tl-row"><div class="tl-year">2024</div><div class="tl-text">The course turns 100. The Save Muny effort announces another $1 million raised.</div></div>
    <div class="tl-row"><div class="tl-year">2025</div><div class="tl-text">The Texas House votes to extend the Save Historic Muny District through May 2027.</div></div>
    <div class="tl-row"><div class="tl-year">2026</div><div class="tl-text">The inaugural Muny Cup and 19th Hole Party sell out in May. A hundred and two years in, the tee sheet is still full.</div></div>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">How It Plays</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>On the card it looks gentle: par 71, 5,825 from the tips, rating 69.8. It is not a bomber&rsquo;s course and it doesn&rsquo;t pretend to be. What it is, is a placement exam. The front nine turns hard &mdash; the doglegs at 1, 3 and 6 all punish the corner-cutter &mdash; and the water waits until the back, where it decides both par 5s and the best hole on the property.</p>
    <p style="margin-top:16px">The ground is the other half of it. Muny sits on limestone, and when Austin is dry &mdash; which is most of the time it&rsquo;s golf weather &mdash; the fairways run like cart paths. Land a ball on the front of these greens and let it release; fly it to the pin and you&rsquo;ll be putting from the collar behind. The course record is 60, so the scoring is there. The 123 slope says it still collects from anyone playing careless.</p>
  </div>
  <h2 class="products-hdr" style="margin-top:40px;">Five Holes That Decide Your Round</h2>
  <div class="tl">
    <div class="tl-row"><div class="tl-year">No. 1</div><div class="tl-text"><strong>359 yards, par 4.</strong> A hard dogleg right, downhill off the tee, and the regulars hit iron &mdash; cutting the corner mostly earns a kick off the firm fairway into the trees. The green slopes away sharply left and long, where a miss can be dead, but the fairway feeds gently left, so the old-fashioned running approach is live. You&rsquo;ll play your opening shot in front of a gallery: the practice green and its stone lion sit right beside the tee.</div></div>
    <div class="tl-row"><div class="tl-year">No. 2</div><div class="tl-text"><strong>495 yards, par 5.</strong> Out of bounds runs the entire right side along Lake Austin Boulevard, so favor the left half all day. The wrinkle is a tree standing in the middle of the fairway about 125 yards from the green &mdash; lay up to whichever side suits your shape in, or play a true three-shotter and slide your third under its branches. Bunkers pinch the front; putts drift toward the boulevard.</div></div>
    <div class="tl-row"><div class="tl-year">No. 6</div><div class="tl-text"><strong>367 yards, par 4, the No. 1 handicap.</strong> Downhill dogleg right with a big tree guarding the corner &mdash; a well-shaped fade catches the slope at the turn and runs out forever. Anything leaked right is a disaster, and even from the short grass you&rsquo;re playing a downhill approach off a downhill lie to a green that&rsquo;s easy to run off the back.</div></div>
    <div class="tl-row"><div class="tl-year">No. 12</div><div class="tl-text"><strong>493 yards, par 5, reachable &mdash; in theory.</strong> Length is rewarded off the tee and the fairway kicks shots forward, which is exactly how the water fronting the green talks you into going for it. There&rsquo;s almost no room to miss either side. The smart play is the layup to the right of the hazard and a short wedge in, avoiding the bunkers right, onto a green with real slope in it.</div></div>
    <div class="tl-row"><div class="tl-year">No. 16</div><div class="tl-text"><strong>395 yards, par 4 &mdash; Hogan&rsquo;s Hole.</strong> The name is local and earned. The tee shot pours downhill toward a pond that takes roughly 300 yards to carry, so the play is a conservative club that runs down near the water, leaving about 130 up the hill to a semi-volcano green. Miss right and the ball can kick thirty yards back down the slope. Walk off with par and tip your cap.</div></div>
  </div>
  <div style="max-width:760px;font-size:16px;line-height:1.7;margin-top:28px;">
    <p>The rest of the round: short par 3s at 13 and 15 that lull you and small greens that punish it, a comfortable walk under the best trees on any course in town, and dogs trotting alongside push carts, which is allowed. Leave the driver home, bring a fairway wood and your patience, and remember why golf in the middle of a city is a different sport from golf behind a gate.</p>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">Know Before You Go</h2>
  <div class="tl">
    <div class="tl-row"><div class="tl-year">Rates</div><div class="tl-text">$35 Mon&ndash;Thu, $41 Friday, $44 weekends and holidays. Evening rounds $29&ndash;$34, sunset $28, juniors $20, seniors $27 on weekdays, nine holes $28 any day. Cards only, no cash.</div></div>
    <div class="tl-row"><div class="tl-year">Tee times</div><div class="tl-text">Mon&ndash;Thu times open online at 9 a.m., seven days out. Weekend times drop the preceding Monday at 8 p.m., online only &mdash; set an alarm, they go fast. You need a (free) account to book. Pro shop: (512) 978-6869, which spells MUNY.</div></div>
    <div class="tl-row"><div class="tl-year">Carts</div><div class="tl-text">$18 per golfer, $12 at sunset &mdash; but this is one of the best walks in Austin golf. Bring the carry bag.</div></div>
    <div class="tl-row"><div class="tl-year">Practice</div><div class="tl-text">Driving range is irons only &mdash; $7 small bucket, $10 large &mdash; plus putting greens under the stone lion. The range closes Mondays at 1 p.m.</div></div>
    <div class="tl-row"><div class="tl-year">Food</div><div class="tl-text">Cisco&rsquo;s Muny Cafe is on site. A breakfast-taco institution attached to a civil rights landmark is about as Austin as it gets.</div></div>
    <div class="tl-row"><div class="tl-year">Closures</div><div class="tl-text">Closed the third Monday of each month for maintenance, and Oct. 6&ndash;7 this fall for overseeding.</div></div>
    <div class="tl-row"><div class="tl-year">Dogs</div><div class="tl-text">Welcome &mdash; non-golfers 13 and up (pets included) ride for $10, kids 12 and under free.</div></div>
    <div class="tl-row"><div class="tl-year">Annual card</div><div class="tl-text">The GolfATX annual card drops weekday rounds here to a $3.50 rate. If Muny is your home course, it pays for itself in a month.</div></div>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">Ben Crenshaw Grew Up Here</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Crenshaw&rsquo;s middle school, O. Henry, sits directly across the street. He walked over nearly every day to practice and play. He won his first trophy at Muny as a fourth grader, shot 74 here at ten, made his first hole-in-one at eleven, and won the Firecracker Open twice before going on to three straight NCAA titles at Texas, nineteen PGA Tour wins and two green jackets.</p>
    <p style="margin-top:16px">He never really left. When the course&rsquo;s future came into question, Crenshaw and his design partner Bill Coore &mdash; the firm behind Sand Valley, Friar&rsquo;s Head and the Kapalua Plantation Course &mdash; offered to restore Muny for free, aiming the course back toward its pre-1974 bones, with the old clubhouse reimagined as an education center and museum for the 1950 story. He helped found the Muny Conservancy to get it funded and has spent years lobbying his own alma mater for a permanent lease.</p>
    <p style="margin-top:16px">Standing in the clubhouse in 2019, he told the USGA: &ldquo;As someone for whom golf has been my whole life, I see what this course means to people. It would be a horror show if Muny went away. It gives them a reason for being, a reason for friendship and fellowship in a beautiful place. And not just golfers&rsquo; lives.&rdquo;</p>
    <p style="margin-top:16px">And then, plainly: &ldquo;I am going to put up whatever reputation I have to save this course.&rdquo;</p>
  </div>
</section>

<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">The Fight, Plainly</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>The numbers underneath the standoff are simple. The city has paid roughly $500,000 a year to lease the land; UT has valued its use at something closer to $6 million a year. The 1910 deed says the tract exists to advance university education, and what that means in 2026 &mdash; student housing, labs, a land-lease income stream, or a historic greenspace two miles from campus that teaches something no classroom can &mdash; is the whole argument. Since the lease lapsed in 2019, the course has run on rolling extensions, at one point month to month with five months&rsquo; notice of termination.</p>
    <p style="margin-top:16px">Meanwhile the machinery to save it keeps building: the Conservancy&rsquo;s fundraising, the legislature&rsquo;s Save Historic Muny District, the National Register listing, a centennial, a sold-out Muny Cup. Mary Arnold, who has advocated for the course for decades, made the case to the USGA in a sentence: &ldquo;Lions has always been accessible to all people since it opened in 1924. It&rsquo;s a beautiful walk, there are many wildlife habitats and it has some of the most gorgeous trees in all of Texas.&rdquo;</p>
    <p style="margin-top:16px">We&rsquo;re not neutral on this one. A city gets a very small number of places where its whole history is still playable for the price of a nice lunch. The best thing you can do for Muny is the same thing we said about <a href="/drops/hancock-golf-course-austin" style="border-bottom:1px solid var(--ink)">Hancock</a>: show up, pay the green fee, and be one more number on the tee sheet that makes the course impossible to argue away.</p>
  </div>
</section>

<div style="max-width:1400px;margin:48px auto 40px;padding:0 32px;"><a href="/field-guide/" style="display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border:.5px solid var(--ink);padding:10px 14px;">&larr; Part of the Austin Golf Field Guide</a></div>

<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">Frequently Asked</h2>
  <div class="faq">
    {faq_html}
  </div>
</section>

<section class="more">
  <div class="more-hdr">
    <span class="more-label">More from TGI</span>
    <a href="/" class="more-link">Back to Feed &rarr;</a>
  </div>
  <div class="more-grid">
    <a href="/drops/hancock-golf-course-austin" class="more-card">
      <div class="more-card-img"><img src="/images/hancock/hero.jpg" alt="Hancock Golf Course — the oldest course in Texas" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Hancock Golf Course &mdash; The Oldest Course in Texas Is a $20 Nine</div><div class="more-card-tag">Field Notes</div></div>
    </a>
    <a href="/drops/the-firecracker-open-81-years-at-the-muny" class="more-card">
      <div class="more-card-img"><img src="/images/feed/4f4867f3-Lions9329-1246x700.jpg" alt="The Firecracker Open at Lions Municipal" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Firecracker Open &mdash; 81 Years at the Muny</div><div class="more-card-tag">Field Notes</div></div>
    </a>
    <a href="/field-guide/" class="more-card">
      <div class="more-card-img"><img src="/images/field-guide/hero-austin-golf.jpg" alt="The Austin Golf Field Guide" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Austin Golf Field Guide</div><div class="more-card-tag">Field Notes</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "lions-municipal-golf-course-austin.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
print("wrote", out, "| words:", words)
