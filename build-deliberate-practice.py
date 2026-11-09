"""build-deliberate-practice.py — Field Note: thoughtful, deliberate practice for the off season, 8 November 2026. Cloned from build-hidden-details.py.
Lenny: "I want to do a post about Thoughtful deliberate practice, it's getting into the off season and a good time to get dialed in", picked
Field Note + gear with home/range/course sessions, then "just do 8 items and make this mostly about the practice".
FACTS: research summaries linked in the post (PubMed / journal pages); product pages for the eight tools.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Deliberate Practice for Golf: An Off-Season Plan to Get Dialed In (What the Research Says)"
DESC = ("How to practice golf with intent this off season: what deliberate practice is, why mixing up your shots works, where to put your focus, "
        "three sessions for home, range and course, a 12-week plan, and eight tools that help.")
H1 = "Practice With a Purpose: An Off-Season Plan for Deliberate, Thoughtful Golf Practice"
BC = "Deliberate Practice"
SLUG = "deliberate-golf-practice-off-season"
IMG = "/images/deliberate-practice"
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "ac": ("Edel Golf", "Aim Check", "$70", U("edelgolf.com","aim-check"),
   "Feedback for your aim. Edel says its research shows 97% of golfers cannot aim at their intended target; this laser kit, taken from its fittings, shows where you really aim and trains you out of it."),
 "ga": ("Edel Golf", "Grip Analyzer and Trainer", "$150", U("edelgolf.com","grip-analyzer-and-trainer"),
   "Measures the grip that is most natural for your hands and body, then trains you to repeat it, for full swings and putting. Left or right handed."),
 "fd": ("Fyfe Golf", "Golfer&rsquo;s Diary", "$67", U("fyfegolf.com","golfers-diary"),
   "The practice log. 64 pages for scores, matches and stats by hand, bound in Scottish cowhide by second-generation bookbinders in Glasgow, with a pencil loop."),
 "sc": ("Seamus Golf", "Hand Forged Drain It Putting Cup", "$200", U("seamusgolf.com","hand-forged-putting-cup-drain-it"),
   "Hand-forged mild steel, built to make the sound of a ball dropping. A target for the living room or office that you will actually leave out."),
 "hb": ("Hudson Sutler", "Heritage Range Bucket", "$145", U("hudsonsutler.com","heritage-range-bucket"),
   "Waxed canvas and leather, holds up to 100 balls with room for tees. Count them out and you know exactly how many shots a session gets."),
 "sb": ("Shoal Golf Co.", "Shag Bag", "$70", U("shoalgolfco.com","the-shoal-shag-bag"),
   "Waxed canvas with a drawstring, holds roughly 60 to 65 balls. For the short-game area, where most of the off-season work should happen."),
 "th": ("Thwack Sporting Co.", "Pioneer Series Alignment Stick Set", "$109", U("thwacksportingco.com","pioneer-series-alignment-stick-set"),
   "Two hand-wrapped 42-inch American hickory sticks. One on your target line, one for ball position. More in our <a href=\"/drops/the-alignment-stick-edit\">Alignment Stick Edit</a>."),
 "dy": ("Dormie Workshop", "Shaka Leather Yardage Book", "$110", U("dormieworkshop.com","shaka-yardage-book"),
   "Handmade leather cover for notes on the course: carry numbers, misses, the one thing you are working on this week."),
}
SECS = [
 ("the-kit", "Eight Tools for Practicing With Intent", "Feedback, targets and a place to write it down", ["ac","ga","fd","sc","hb","sb","th","dy"],
  "Anything that gives honest feedback, a real target or a place to keep score."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 8
PAIRS = {}
BANDS = {
 "a": ("On the range", "Practice with a reason", [("life-a-1","A golfer swinging on a range with a duffel and a pyramid of balls beside him","Hudson Sutler"),("life-a-2","A golfer seen from behind at a full range ball basket","SAHA Golf"),("life-a-3","Golfers practicing at a range at twilight","Walker Golf Things")]),
 "b": ("Short game", "Where the off season pays off", [("life-b-1","A golfer in a white sweater playing a chip","Ashworth"),("life-b-2","A golfer chipping from the rough in striped polo and cream shorts","Woodgrain Golf"),("life-b-3","A golfer chipping from a grassy slope","Sunday Golf")]),
 "c": ("On the green", "Read it, roll it, check it", [("life-c-1","A golfer crouching to read a putt","Odd Ritual"),("life-c-2","A golfer lying flat on a green lining up a putt","Slice Town"),("life-c-3","A golfer lining up a putt with a mallet putter","Dual Sport")]),
 "d": ("Practice golf", "Take it to the course", [("life-d-1","A golfer addressing a shot on a hillside course","Rookline"),("life-d-2","A golfer putting by a lake","Masterpiece Sports Club"),("life-d-3","Two golfers on a green under tall palms, one putting","Howie Benson")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most range sessions look the same: a big bucket, the 7-iron that felt good last week, swing until it is empty. It feels productive. It mostly isn&rsquo;t.</p>
    <p>The off season is the time to fix that. No match on Saturday, nothing to lose by trying something that feels worse before it feels better. The plan is simple: practice less, practice harder. One goal per session. Honest feedback. Never the same shot twice. Same test every week, written down.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Sessions</span><span>Home, range, course</span></div>
      <div class="sidebar-detail"><span class="l">Plan</span><span>12 weeks</span></div>
      <div class="sidebar-detail"><span class="l">Tools</span><span>8, $67&ndash;$200</span></div>
      <div class="sidebar-detail"><span class="l">Start with</span><span>20 minutes of putting</span></div>
      <div class="hashtags">
        <span class="hashtag">#DeliberatePractice</span>
        <span class="hashtag">#OffSeason</span>
        <span class="hashtag">#IndieGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
PCSS = """<style>/*TGI-PRACTICE*/
.pr-row{max-width:1100px;margin:0 auto;padding:52px 32px 8px;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.pr-row.flip{grid-template-columns:.85fr 1.15fr}.pr-row.flip .pr-txt{order:2}
.pr-txt h2{font-family:var(--serif);font-weight:400;font-size:32px;line-height:1.15;margin:10px 0 14px}
.pr-txt p{font-family:var(--serif);font-size:17.5px;line-height:1.62;margin:0 0 14px}
.pr-fig{margin:0}.pr-fig img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.pr-fig figcaption{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin-top:8px}
.pr-dia{margin:18px 0 6px}.pr-dia svg{width:100%;height:auto;display:block}
.pr-dia .cap{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:6px}
.pr-wide{max-width:1100px;margin:0 auto;padding:44px 32px 6px;text-align:center}
.pr-wide h2{font-family:var(--serif);font-weight:400;font-size:32px;margin:10px 0 8px}
.pr-wide p{font-family:var(--serif);font-size:17.5px;line-height:1.6;max-width:640px;margin:0 auto 18px}
.pr-sessions{max-width:1100px;margin:0 auto;padding:6px 32px 10px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;text-align:left}
.pr-card img{width:100%;aspect-ratio:5/4;object-fit:cover;display:block}
.pr-card .in{border:.5px solid var(--ink);border-top:0;padding:16px 18px 6px}
.pr-card .k{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;opacity:.7}
.pr-card h3{font-family:var(--serif);font-weight:400;font-size:22px;margin:4px 0 10px}
.pr-card ol{margin:0 0 12px 18px;padding:0;font-family:var(--serif);font-size:15.5px;line-height:1.5}
.pr-card li{margin-bottom:7px}
.pr-src{max-width:1100px;margin:0 auto;padding:6px 32px 0;font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;opacity:.55;line-height:1.7;text-align:center}
.products-grid[data-n="8"]>.product-card{flex-basis:calc((100% - 72px)/4)}
.pr-vs{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:18px 0 6px}
.pr-vs div{border:.5px solid var(--ink);padding:16px 16px 14px;font-family:var(--serif)}
.pr-vs div.on{background:var(--grass,#2f4f2f);color:#f6f1e6;border-color:var(--grass,#2f4f2f)}
.pr-vs b{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;margin-bottom:10px}
.pr-vs span{display:block;font-size:17px;line-height:1.35;margin-bottom:6px;font-style:italic}
.pr-vs em{display:block;font-style:normal;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;margin-top:10px}
.pr-study{max-width:1100px;margin:0 auto;padding:8px 32px 10px;display:grid;grid-template-columns:1fr 1fr;gap:28px;text-align:left}
.pr-study h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;margin:0 0 6px;padding-bottom:8px;border-bottom:.5px solid var(--ink)}
.pr-study .it{padding:12px 0;border-bottom:.5px solid rgba(26,26,26,.2);font-family:var(--serif);font-size:16px;line-height:1.5}
.pr-study .it b{font-weight:500}.pr-study .it i{opacity:.7}
@media(max-width:900px){.pr-study,.pr-vs{grid-template-columns:1fr}}

@media(max-width:900px){.pr-row,.pr-row.flip{grid-template-columns:1fr;gap:22px}.pr-row.flip .pr-txt{order:0}.pr-sessions{grid-template-columns:1fr}.products-grid[data-n="8"]>.product-card{flex-basis:calc((100% - 24px)/2)}}
@media(max-width:480px){.products-grid[data-n="8"]>.product-card{flex-basis:100%}.pr-txt h2,.pr-wide h2{font-size:26px}}
</style>
"""
LOOP = """<svg viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" font-family="JetBrains Mono, monospace" font-size="11" letter-spacing="1.2">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2f4f2f"/></marker></defs>
<g fill="none" stroke="#2f4f2f" stroke-width="1.5" marker-end="url(#ar)">
<path d="M150,52 L232,52"/><path d="M330,52 L412,52"/><path d="M455,78 C455,150 420,165 330,165"/><path d="M232,165 C120,165 65,150 65,78"/></g>
<g fill="#f1ece2" stroke="#1a1a1a" stroke-width=".8"><rect x="10" y="30" width="140" height="46"/><rect x="235" y="30" width="95" height="46"/><rect x="415" y="30" width="95" height="46"/><rect x="235" y="142" width="95" height="46"/></g>
<g fill="#1a1a1a" text-anchor="middle"><text x="80" y="57">ONE GOAL</text><text x="282" y="57">FOCUS</text><text x="462" y="57">FEEDBACK</text><text x="282" y="169">ADJUST</text></g>
<text x="260" y="122" text-anchor="middle" fill="#2f4f2f" font-size="10">just past what you can already do</text></svg>"""
BLOCK = """<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" font-family="JetBrains Mono, monospace" font-size="10.5" letter-spacing="1">
<text x="0" y="16" fill="#1a1a1a">BLOCKED</text>
<g fill="#2f4f2f">""" + "".join(f'<circle cx="{110+i*34}" cy="12" r="9"/>' for i in range(12)) + """</g>
<g fill="#f1ece2" font-size="9" text-anchor="middle">""" + "".join(f'<text x="{110+i*34}" y="15">7</text>' for i in range(12)) + """</g>
<text x="0" y="58" fill="#1a1a1a">RANDOM</text>
<g>""" + "".join(f'<circle cx="{110+i*34}" cy="54" r="9" fill="{c}"/>' for i,c in enumerate(["#2f4f2f","#a8743c","#6b8f71","#1a1a1a","#a8743c","#2f4f2f","#6b8f71","#1a1a1a","#2f4f2f","#a8743c","#6b8f71","#1a1a1a"])) + """</g>
<g fill="#f1ece2" font-size="9" text-anchor="middle">""" + "".join(f'<text x="{110+i*34}" y="57">{t}</text>' for i,t in enumerate(["7","W","5","D","W","7","5","D","7","W","5","D"])) + """</g>
<line x1="60" y1="208" x2="500" y2="208" stroke="#1a1a1a" stroke-width=".8"/><line x1="60" y1="208" x2="60" y2="90" stroke="#1a1a1a" stroke-width=".8"/>
<text x="150" y="224" text-anchor="middle" fill="#1a1a1a">IN PRACTICE</text><text x="390" y="224" text-anchor="middle" fill="#1a1a1a">A WEEK LATER</text>
<rect x="105" y="110" width="38" height="98" fill="#2f4f2f"/><rect x="150" y="138" width="38" height="70" fill="#a8743c"/>
<rect x="345" y="160" width="38" height="48" fill="#2f4f2f"/><rect x="390" y="118" width="38" height="90" fill="#a8743c"/>
<g font-size="9"><rect x="400" y="84" width="10" height="10" fill="#2f4f2f"/><text x="415" y="93" fill="#1a1a1a">BLOCKED</text><rect x="400" y="98" width="10" height="10" fill="#a8743c"/><text x="415" y="107" fill="#1a1a1a">RANDOM</text></g></svg>"""
FOCUS = """<div class="pr-vs"><div><b>Internal</b><span>&ldquo;Keep my left arm straight.&rdquo;</span><span>&ldquo;Turn my hips.&rdquo;</span><em>Fine for learning a position at home</em></div><div class="on"><b>External</b><span>&ldquo;Swing the clubhead at the flag.&rdquo;</span><span>&ldquo;Start it over that tree.&rdquo;</span><em>More accurate on the range and the course</em></div></div>"""
WEEKS = """<svg viewBox="0 0 1000 120" xmlns="http://www.w3.org/2000/svg" font-family="JetBrains Mono, monospace" font-size="11" letter-spacing="1.2">
<rect x="0" y="30" width="330" height="34" fill="#a8743c"/><rect x="335" y="30" width="330" height="34" fill="#6b8f71"/><rect x="670" y="30" width="330" height="34" fill="#2f4f2f"/>
<g fill="#f6f1e6"><text x="14" y="52">WEEKS 1&#8211;4 &#183; FUNDAMENTALS</text><text x="349" y="52">WEEKS 5&#8211;8 &#183; SKILL</text><text x="684" y="52">WEEKS 9&#8211;12 &#183; PLAY</text></g>
<g fill="#1a1a1a" font-size="10"><text x="0" y="18">MID-NOVEMBER</text><text x="1000" y="18" text-anchor="end">MID-FEBRUARY</text>
<text x="0" y="86">Grip, aim, setup. Mostly at home.</text><text x="335" y="86">Range work, random practice,</text><text x="335" y="101">wedge distances.</text><text x="670" y="86">Pressure games, practice nines,</text><text x="670" y="101">attention on the target.</text></g></svg>"""
PRACTICE = """
<div class="pr-row" id="what-it-is">
  <div class="pr-txt">
    <div class="drop-tag grass">01 &middot; The idea</div>
    <h2>What Deliberate Practice Is</h2>
    <p>The term comes from psychologist Anders Ericsson, whose work was later squeezed into the &ldquo;10,000-hour rule.&rdquo; He spent years correcting that. Hours were never the point; the kind of practice was.</p>
    <p>A specific goal (&ldquo;start 8 of 10 four-footers on line,&rdquo; not &ldquo;putt better&rdquo;), full focus, honest feedback, and drills just past what you can already do. Hitting balls with a vague hope of improving is what researchers call naive practice.</p>
    <div class="pr-dia">""" + LOOP + """<div class="cap">The loop, every session</div></div>
  </div>
  <figure class="pr-fig"><img src="@@IMG@@/life-a-3.jpg" alt="Golfers practicing at a range at twilight" loading="lazy" /><figcaption>Walker Golf Things</figcaption></figure>
</div>

<div class="pr-row flip" id="mix-it-up">
  <div class="pr-txt">
    <div class="drop-tag grass">02 &middot; The research</div>
    <h2>Mix It Up, Even Though It Feels Worse</h2>
    <p><strong>Blocked</strong> practice repeats one shot. <strong>Random</strong> practice changes it every swing. Blocked looks better on the day; random is what sticks.</p>
    <p>In a 2017 trial with 30 new golfers, the random group putted worse in practice but better on the retention test. A 2018 study found the same for chipping. The studies are small and mostly beginners, but on the course you never hit the same shot twice, so practice that way. If it feels a little frustrating, it is probably working.</p>
    <div class="pr-dia">""" + BLOCK + """<div class="cap">Illustration of the pattern, not study data</div></div>
  </div>
  <figure class="pr-fig"><img src="@@IMG@@/life-b-2.jpg" alt="A golfer chipping from the rough in a striped polo and cream shorts" loading="lazy" /><figcaption>Woodgrain Golf</figcaption></figure>
</div>

<div class="pr-row" id="focus">
  <div class="pr-txt">
    <div class="drop-tag grass">03 &middot; Attention</div>
    <h2>Think Target, Not Elbow</h2>
    <p>Gabriele Wulf&rsquo;s studies found golfers hit more accurate pitches focusing on the club or the target than on their arms, beginners and experts alike. Body cues still have a place: use them to learn a new position at home, then put your attention back on the target when you play.</p>
    """ + FOCUS + """
  </div>
  <figure class="pr-fig"><img src="@@IMG@@/life-c-1.jpg" alt="A golfer crouching to read a putt" loading="lazy" /><figcaption>Odd Ritual</figcaption></figure>
</div>

<div class="pr-wide" id="sessions">
  <div class="drop-tag grass">04 &middot; The sessions</div>
  <h2>Three Sessions a Week</h2>
  <p>Two at home, one at the range, one round of practice golf. Each starts with one written goal and ends with a number.</p>
</div>
<div class="pr-sessions">
  <div class="pr-card"><img src="@@IMG@@/life-c-2.jpg" alt="A golfer lying flat on a green lining up a putt" loading="lazy" /><div class="in"><div class="k">Home &middot; 20 min</div><h3>The putting block</h3><ol>
    <li><strong>Start line.</strong> Two tees just wider than the ball, a foot ahead of it. Roll 4-footers through the gate.</li>
    <li><strong>Ladder.</strong> 3, 6 and 9 feet in random order. A point per make.</li>
    <li><strong>Test.</strong> Ten 4-footers from different spots. Write the number down.</li>
  </ol></div></div>
  <div class="pr-card"><img src="@@IMG@@/life-a-1.jpg" alt="A golfer swinging on a range with a duffel beside him" loading="lazy" /><div class="in"><div class="k">Range &middot; 45 min</div><h3>No two shots alike</h3><ol>
    <li><strong>Warm up.</strong> Ten wedges, stick on your target line.</li>
    <li><strong>Play a hole.</strong> Driver, the approach you would leave, a wedge. New club and target every swing.</li>
    <li><strong>Pressure.</strong> Ten shots at a target; three misses and you start over.</li>
  </ol></div></div>
  <div class="pr-card"><img src="@@IMG@@/life-d-1.jpg" alt="A golfer addressing a shot on a hillside course" loading="lazy" /><div class="in"><div class="k">Course &middot; 9 holes</div><h3>Practice golf</h3><ol>
    <li><strong>Go late, no card.</strong></li>
    <li><strong>Score targets.</strong> A point each for fairway, green or fringe, and up and down.</li>
    <li><strong>Worst ball inside 100.</strong> Hit two, play the worse. The costliest shot is next week&rsquo;s goal.</li>
  </ol></div></div>
</div>

<div class="pr-row flip" id="track-it">
  <div class="pr-txt">
    <div class="drop-tag grass">05 &middot; Feedback</div>
    <h2>Keep Score on Your Practice</h2>
    <p>Every session gets a date, one goal and a test score. Keep the tests the same week to week so the numbers mean something. Change one thing at a time, and expect scores to dip before they climb.</p>
  </div>
  <figure class="pr-fig"><img src="@@IMG@@/pfd-2.jpg" alt="The Fyfe Golf Golfer's Diary open to its score pages" loading="lazy" /><figcaption>Fyfe Golf Golfer&rsquo;s Diary</figcaption></figure>
</div>

<div class="pr-wide" id="twelve-weeks">
  <div class="drop-tag grass">06 &middot; The plan</div>
  <h2>Twelve Weeks</h2>
  <div class="pr-dia" style="max-width:1000px;margin:18px auto 0">""" + WEEKS + """</div>
</div>

<div class="pr-wide" id="study">
  <div class="drop-tag grass">07 &middot; Study hall</div>
  <h2>Read and Watch</h2>
  <p>For the nights it is too cold or too dark. Book links go to Bookshop.org, which supports independent bookstores. For the classics, see our <a href="/drops/7-books-to-elevate-your-golf-game">seven books to elevate your game</a>.</p>
</div>
<div class="pr-study">
  <div><h3>Books</h3>
    <div class="it"><b><a href="https://bookshop.org/search?keywords=Peak+Anders+Ericsson+Robert+Pool" target="_blank" rel="noopener">Peak</a></b> <i>by Anders Ericsson and Robert Pool</i>. The source: what deliberate practice is, from the researcher who named it.</div>
    <div class="it"><b><a href="https://bookshop.org/search?keywords=The+Practice+Manual+Adam+Young+golf" target="_blank" rel="noopener">The Practice Manual</a></b> <i>by Adam Young</i>. Motor-learning research turned into golf practice you can actually run.</div>
    <div class="it"><b><a href="https://bookshop.org/search?keywords=Every+Shot+Counts+Mark+Broadie" target="_blank" rel="noopener">Every Shot Counts</a></b> <i>by Mark Broadie</i>. The strokes-gained book. Shows where your shots are really lost, so you know what to practice.</div>
    <div class="it"><b><a href="https://bookshop.org/search?keywords=The+Talent+Code+Daniel+Coyle" target="_blank" rel="noopener">The Talent Code</a></b> <i>by Daniel Coyle</i>. Why slow, focused, mistake-filled practice builds skill, across sports and music.</div>
  </div>
  <div><h3>YouTube</h3>
    <div class="it"><b><a href="https://www.youtube.com/@adamyounggolf" target="_blank" rel="noopener">Adam Young Golf</a></b>. The Practice Manual author on strike, variability and how people learn.</div>
    <div class="it"><b><a href="https://www.youtube.com/@AthleticMotionGolf" target="_blank" rel="noopener">Athletic Motion Golf</a></b>. Clear drills, many needing nothing more than an alignment stick.</div>
    <div class="it"><b><a href="https://www.youtube.com/@meandmygolf." target="_blank" rel="noopener">Me and My Golf</a></b>. PGA coaches Piers Ward and Andy Proudman; drills for every level.</div>
    <div class="it"><b><a href="https://www.youtube.com/@CogornoGolf" target="_blank" rel="noopener">Eric Cogorno Golf</a></b>. Practice drills and plain-spoken swing fixes.</div>
  </div>
</div>
<p class="pr-src">Research: <a href="https://pubmed.ncbi.nlm.nih.gov/28449601/" target="_blank" rel="noopener">random vs blocked putting (2017)</a> &middot; <a href="https://www.tandfonline.com/doi/full/10.1080/24748668.2018.1475199" target="_blank" rel="noopener">contextual interference in chipping (2018)</a> &middot; <a href="https://pubmed.ncbi.nlm.nih.gov/17941543/" target="_blank" rel="noopener">Wulf &amp; Su, external focus (2007)</a> &middot; <a href="https://pubmed.ncbi.nlm.nih.gov/12875310/" target="_blank" rel="noopener">focus and skill (2003)</a></p>
"""
PRACTICE = PRACTICE.replace("@@IMG@@", IMG)
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:680px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Less, but Better</h2>
    <p>The golfers who come out of winter better rarely hit the most balls. They knew what they were working on, got honest feedback and kept score. Start with twenty minutes on the living room floor, twice a week, and a number written down at the end.</p>
    <p>For the range work, see <a href="/drops/8-best-practice-facilities-around-austin">the best practice facilities around Austin</a>. Tool prices are in US dollars as of November 8, 2026.</p>
  </div>
</section>
"""
HERO_ALT = "Two golfers on a clifftop links course above the sea, one crouching to read a putt, from Sounder's own shoot"
FRN = json.loads((ROOT / "research/practice/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-08", "dateModified": "2026-11-08",
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



def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


CBY = {s[0]: s for s in SECS}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    s = CBY[anchor]
    num = 8
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} tools</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;"><p style="margin:0 0 16px;">{s[4]}</p></div>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
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
    <span>Field Notes &middot; The off-season practice plan</span><span class="dot"></span>
    <span>3 sessions, 12 weeks, 8 tools &middot; checked November 8, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE + PRACTICE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    if "end" in BANDS: body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + PCSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Vest Edit", "Collab "):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
