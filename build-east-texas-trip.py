#!/usr/bin/env python3
"""build-east-texas-trip.py — Field Note: 90 holes in three days in East Texas. 10 November 2026.
Lenny: "We're gonna do a in depth field note about my recent trip to East Texas, we played Tempest, Wild Spring Dunes,
LumberJack National and Pine Dunes. 90 holes of golf in 3 days." Trip details are Lenny's own (10 Nov message), written up
in his words; nothing about the rounds is added. Layout cloned from build-mind-body-spirit.py (editorial, no product cards),
organised by day instead of by pillar.
PHOTOS: Lenny's and the group's own phone photos from the trip (Golf Pics folder, EXIF Nov 6-8, 2026, GPS matches each course).
FACTS checked Nov 10, 2026: Tempest = Gladewater, Jeff Brauer's renovation of the old Southern Hills course, reopened 2018,
not a private club, #16 public in Texas per the Dallas Morning News (tempestgolfclub.com). Wild Spring Dunes = Tom Doak, Mount Enterprise,
Michael Keiser Jr., opened Sept 8 2026, $275 peak / $195 Dec-Feb, walking only (TGI On Our Radar post, Oct 2026).
LumberJack National = Nacogdoches, formerly Piney Woods Country Club, par 72, ~6,190 yards (GolfLink/GolfPass); bookable
online per Lenny (Nov 10), GolfNow page linked. Pine Dunes = Frankston, Jay Morrish with Carter Morrish,
2001 (GolfPass/GolfN); rates $99 Mon-Thu / $149 Fri-Sun per pinedunes.com/golf/rates-fees; history from /history/breaking-ground and /history/awards (read Nov 10, 2026).
Tempest card and awards from tempestgolfclub.com/scorecard and /awards-honors; LumberJack from lumberjacknational.com/about and /rates.
WSD routing, holes and plans from TGI On Our Radar post (GolfPass/D CEO/GOLF, cited there). Drive times are rough map estimates and labelled as such.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "90 Holes in 3 Days: An East Texas Golf Trip"
DESC = ("Four of us, four courses, 90 holes in three days in the East Texas pines: Tempest twice, Wild Spring Dunes, "
        "LumberJack National and Pine Dunes. What each course is like, how we played it and how to plan the trip.")
H1 = "90 Holes in Three Days: Tempest, Wild Spring Dunes, LumberJack National and Pine Dunes"
BC = "East Texas Golf Trip"
SLUG = "east-texas-golf-trip-90-holes"
IMG = "/images/east-texas"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
N = 4

# course: (day, name, place, designer line, url, lead alt, lead caption, paras[], facts{}, mosaic[(alt, caption)])
C = {}
C["tempest"] = ("friday", "Tempest Golf Club", "Gladewater, Texas", "Jeff Brauer redesign &middot; reopened 2018", "https://www.tempestgolfclub.com/",
 "A green guarded by two white bunkers at Tempest, with pines and a fairway climbing behind it under a heavy sky",
 "Friday afternoon at Tempest, second time around.",
 ["Friday was Tempest, twice. The club sits outside Gladewater and is Jeff Brauer&rsquo;s complete redesign of the old Southern Hills course, reopened in 2018. It isn&rsquo;t a private club: anyone can book a tee time, and the Dallas Morning News has rated it the 16th-best public course in Texas.",
  "The land has been through a few lives. The Webb family opened a nine-hole course called Shallow Creek here in 1989, with a double-wide trailer for a clubhouse. It grew to 18 holes as Southern Hills in 1996, then struggled. New Orleans attorney Joe Bruno bought it in 2006 and brought in Brauer for a total renovation in 2016. What was meant to take eight months took more than two years, and the course reopened in the summer of 2018 with a dozen new holes. It has since hosted a local U.S. Amateur qualifier. The giant American flag you see from half the course went up on Veterans Day 2020 and stands over the 9th green.",
  "From the black tees it runs 7,229 yards, par 72, rated 73.7 with a 130 slope, and there are five sets of tees down to 4,512. There are four par 5s, two on each nine, and the front side finishes with back-to-back long ones at the 6th and 9th, both over 560 from the tips. The rankings have followed: the Dallas Morning News has it 68th among the top 100 courses in Texas and 16th among those open to the public in 2026, Golf Digest named it the 18th-best course you can play in Texas in 2022, and Texas Monthly put it third on its 2023 list of public courses.",
  "What got me first was the elevation. The course climbs and drops through the pines more than you expect from East Texas, the layout is tight, and it was as well manicured as anything we played all weekend. We rode both loops.",
  "Round one was straight play. Round two was match play: the top player from the morning partnered the bottom player, and the middle two played together. The scores were tight and competitive all weekend.",
  "The front nine is the more interesting side, with some great risk/reward holes. Playing the course twice in one day gave us a real sense of where to go for it off the tee."],
 {"Where": "Gladewater, about two hours east of Dallas",
  "Architect": "Jeff Brauer, a full redesign of the former Southern Hills course",
  "Card": "Par 72, 7,229 yards from the blacks, 73.7/130. Neptune&rsquo;s Bar &amp; Grill in the clubhouse, stay-and-play packages",
  "Access": "Public tee times, with memberships offered",
  "How we played it": "36 holes in one day, riding. Stroke play, then match play",
  "Tell a friend": "Play it twice if you can. The second loop is where it clicks"},
 [("A lone pine in a wide Tempest fairway under a big sky of broken cloud", "The back nine opens up."),
  ("The flag over the Tempest clubhouse at dusk, the cart path curving toward a green", "Finishing the second loop at dusk."),
  ("A cart path running down a Tempest fairway toward bunkers and pines under a low, bright sky", "Friday morning, before round one.")])

C["wild-spring-dunes"] = ("saturday", "Wild Spring Dunes", "Mount Enterprise, Texas", "Tom Doak &middot; opened 2026", "https://www.wildspringdunes.com/golf",
 "Sandy waste bunkers and native grass in front of a green at Wild Spring Dunes, tall pines behind",
 "Sand, wire grass and pines at Wild Spring Dunes.",
 ["Saturday started with one of the first tee times at Wild Spring Dunes, the Tom Doak course outside Mount Enterprise that opened all 18 holes on September 8. We wrote about it before it opened in <a href=\"/drops/on-our-radar-wild-spring-dunes\">On Our Radar</a>. Now we&rsquo;ve played it.",
  "The short version of how it happened: in 2021 a Dallas office worker named Brett Messerall, who had taught himself to read topo maps and soil surveys, found the land while a timber company was clear-cutting it. Underneath the pines was sand. He cold-emailed Tom Doak, who walked the site and later told D CEO, &ldquo;This is a really good site.&rdquo; Michael Keiser Jr., whose family built Bandon Dunes and Sand Valley, came in as developer. It sits on 2,400 acres, and a second course by Coore &amp; Crenshaw is already being built.",
  "The course plays in two counterclockwise loops. The front eight ramble over gentler hills, then the 9th sends you back off the starting hilltop into heavier ground and along deeper ravines. The fairways are zoysia, and eleven bridges tie the property together. Two holes get the most attention: the 10th, a long par 3 that reaches past 240 yards from the tips to a green perched above bunkers and a ravine, and the 17th, a 331-yard par 4 back across the same ravine to a skinny two-level green. There is no hotel yet, and the clubhouse is a temporary one called The Hitching Post. Keiser says the property could one day hold as many as five 18-hole courses.",
  "Very, very nice. They threw an incredible amount of money at this course, and it shows. It is dynamic and stunning, and the greens were extremely fast. Some of the pin locations were wildly difficult: an inch or two past the hole and the ball rolled off the green.",
  "We had a forecaddie, Dexter, who gave us good intel all morning, though he had a bias toward overreading putts. The marshal was a little pushy about pace of play, which might have been because members were playing right behind us.",
  "The merch was solid, but it isn&rsquo;t taking any risks."],
 {"Where": "Mount Enterprise, in the Piney Woods south of Henderson",
  "Architect": "Tom Doak. Developed by Michael Keiser Jr.",
  "Card": "Par 72, 6,962 yards from the Pine tees, 74.6/147",
  "Fee": "$275 in peak season, $195 December to February (course rates, October 2026)",
  "Walking": "Walking only. Caddies and forecaddies available",
  "Tell a friend": "Book the first tee time and mind the pins. Past the hole can mean off the green"},
 [("Dry native grass and sandy scrub framing a fairway and green at Wild Spring Dunes", "Native grass all the way to the green."),
  ("A sandy bunker and wire grass in front of a green at Wild Spring Dunes, pines behind", "Sand and wire grass."),
  ("A wide fairway in low morning light at Wild Spring Dunes, pines lining both sides", "First light, first tee time.")])

C["lumberjack-national"] = ("saturday", "LumberJack National", "Nacogdoches, Texas", "Formerly Piney Woods Country Club", "https://www.lumberjacknational.com/book-a-tee-time/",
 "Low sun bursting through tall hardwoods over a tree-lined fairway at LumberJack National",
 "Late Saturday sun at LumberJack National.",
 ["Jeff and Todd headed home after Wild Spring, and Matt and I drove over to LumberJack National in Nacogdoches for the afternoon. It is a very casual track with a muni feel, the course that used to be Piney Woods Country Club, and it could not be more different from the morning.",
  "LumberJack dates to 1926, which makes it the oldest course on this trip by a long way. It sits off Highway 59 on the south side of Nacogdoches, which bills itself as the oldest town in Texas, and the club calls itself the &ldquo;Hidden Gem of East Texas&rdquo; for its towering pines and big oaks. The fairways are narrow and the greens are small and quick, recently renovated, so position matters more than distance. It plays par 72 at about 6,190 yards from the back tees, short by modern standards, but the hills and trees make up for it. Today it runs as a golf course and event venue, with a pro shop, a pool, a bar and a restaurant, and tee times open five days ahead with the cart included in the rate.",
  "It&rsquo;s hilly and tree-lined, and very booby-trapped for wild hogs. We were pretty dialed in by then. We played very well, and fast."],
 {"Where": "Nacogdoches, under an hour from Wild Spring Dunes",
  "Course": "Par 72, about 6,190 yards from the back tees. Established 1926",
  "Booking": "Book online up to five days ahead. Cart included",
  "How we played it": "18 holes on Saturday afternoon, after Wild Spring",
  "Tell a friend": "Casual, quick and hilly. The second round of a 36-hole day"},
 [("A golfer in a red polo mid-swing on a tee box framed by pines and oaks at LumberJack National", "Dialed in by Saturday afternoon."),
  ("A narrow fairway dropping into shade between big hardwoods at LumberJack National", "Hills and hardwoods."),
  ("Evening light on a tee box at LumberJack National with oaks either side", "Finishing before dark.")])

C["pine-dunes"] = ("sunday", "Pine Dunes Resort &amp; Golf Club", "Frankston, Texas", "Jay Morrish and Carter Morrish &middot; 2001", "https://www.pinedunes.com/golf/tee-times",
 "A tee shot over a wide sandy waste area to a fairway framed by oaks at Pine Dunes",
 "Sand off the tee at Pine Dunes.",
 ["Sunday, Matt and I finished at Pine Dunes in Frankston, a Jay Morrish design built with his son Carter, opened in 2001. It&rsquo;s a tight course, and the starter pulled his old Buick right up to the first tee box, which is awesome.",
  "The story behind it is a good one. Jodi Lutz, who had never played golf, found the property in 1994 as a nine-hole course with an 88-acre lake; the pines reminded her of growing up in northern Minnesota. A few years later PGA Tour player David Frost walked the land, saw what it could be and introduced her to Jay Morrish. Morrish and his son Carter started work in late 1999, and it opened in 2001. The club&rsquo;s own pitch is that there are no trick holes, no forced carries and water rarely comes into play.",
  "The praise piled up fast. Golf Digest put it sixth on its list of America&rsquo;s best new upscale public courses in 2002 and gives it 4.5 stars, Golfweek ranked it the No. 1 course you can play in Texas from 2010 to 2012 and again from 2014 to 2018, and the Golf Channel called it America&rsquo;s No. 1 hidden gem. From the gold tees it stretches to 7,117 yards (74.4/131). Rates are $99 Monday to Thursday and $149 Friday to Sunday with cart and range balls included, replays are half price Sunday to Thursday, and there are guest condos on site that sleep a group of up to 80.",
  "We lost a good bit of balls. By round five we were happy to take bigger risks off the tee, and unless it was a par or a birdie we were pretty generous with our scores."],
 {"Where": "Frankston, southwest of Tyler",
  "Architect": "Jay Morrish with Carter Morrish",
  "Card": "Par 72, 7,117 yards from the golds. On-site condos for stay-and-play",
  "Fee": "$99 Mon&ndash;Thu, $149 Fri&ndash;Sun, cart and range included (club rates, November 2026)",
  "How we played it": "18 holes on Sunday, round five of five",
  "Tell a friend": "Bring extra balls. It&rsquo;s tight"},
 [("The starter's red sedan parked beside the cart path at the first tee at Pine Dunes, our cart alongside", "The starter&rsquo;s Buick, parked at the first tee."),
  ("A tee box looking down a Pine Dunes fairway toward a bunker and a wall of pines under grey sky", "Round five."),
  ("A long sandy waste area crossing in front of a fairway under grey sky at Pine Dunes", "More sand than you expect in Texas.")])

DAYS = [
 ("friday", "Friday", "I", "36 holes &middot; Tempest, twice", "The drive out was the dull part. Once the road gets into the Pines, the country changes fast: pines close in on both sides and the ground starts to roll. Friday was all Tempest. The four of us rode two loops under a heavy, shifting sky, straight stroke play in the morning and the pairs match in the afternoon. By the end of the second loop the light was going, with the big flag over the 9th green still flying.",
  "A Tempest green guarded by bunkers, with fairways and pines rolling away under a heavy late-afternoon sky", ["tempest"]),
 ("saturday", "Saturday", "II", "36 holes &middot; Wild Spring Dunes, then LumberJack National", "Saturday was the big one. We had one of the first tee times at Wild Spring Dunes and stood on the first tee with the sun barely over the pines, all four of us, push carts lined up because the course is walking only. Dexter forecaddied us around. After the round Jeff and Todd peeled off for home, and Matt and I drove south to Nacogdoches for a second 18 at LumberJack National, a different kind of golf entirely, played fast and finished in the long shadows of late afternoon.",
  "Tall pines casting long morning shadows across a Wild Spring Dunes fairway", ["wild-spring-dunes", "lumberjack-national"]),
 ("sunday", "Sunday", "III", "18 holes &middot; Pine Dunes", "Sunday came in grey. Matt and I drove to Frankston for the last round of the trip, the fifth in three days, at Pine Dunes. The starter met us at the first tee in his old Buick. By then the scoring was generous and we were happy to swing hard off every tee. Then the long drive home.",
  "A wide sandy waste area in front of a fairway framed by oaks at Pine Dunes under a grey sky", ["pine-dunes"]),
]

PQ = {
 "wild-spring-dunes": ("They threw an incredible amount of money at this course.", "Lenny, on Wild Spring Dunes"),
 "pine-dunes": ("The starter pulled his old Buick up to the first tee box, which is awesome.", "Lenny, on Pine Dunes"),
}

NUMS = [("90", "holes"), ("4", "courses"), ("3", "days"), ("450+", "shots"), ("0", "waits on a tee box")]

INTRO = """
<section class="mbs-intro">
  <p class="mbs-epi">&ldquo;For the weekend it was our golf mecca.&rdquo;<span>&mdash; Lenny</span></p>
  <div class="mbs-lede">
    <p>Four of us went: me, Jeff, Matt and Todd, the guys coming in from all over. Ninety holes in three days across four courses: Tempest twice on Friday, Wild Spring Dunes and LumberJack National on Saturday, Pine Dunes on Sunday.</p>
    <p>The drive out was very boring. Then you get into the Pines and the ecology becomes a lot more interesting. It&rsquo;s wild how much, and how quickly, Texas can change ecosystems.</p>
    <p>East Texas is completely out of the way for most people. It&rsquo;s isolated, and we didn&rsquo;t find a single great restaurant. But there was variety, there were deeply challenging holes, and the best part of the golf was simple: we did not have to wait on a tee box once all weekend.</p>
  </div>
</section>
"""

OFF = """
<section class="mbs-solo">
  <h2 class="mbs-h2" id="off-the-course">Off the Course</h2>
  <div class="mbs-solo-grid">
    <div><h3>Dinner</h3><p>We got Costco lasagna and big ribeyes and grilled at the Airbnb.</p></div>
    <div><h3>The format</h3><p>Friday&rsquo;s second loop was match play: top player with the bottom player, the middle two together. The scores were tight and competitive all weekend.</p></div>
    <div><h3>The pace</h3><p>We never waited on a tee box. Not once, at any of the four courses, across all 90 holes.</p></div>
    <div><h3>The scoring</h3><p>By Sunday we were happy to take bigger risks off the tee, and unless it was a par or a birdie we were pretty generous with the card.</p></div>
  </div>
</section>
"""

VERDICT = """
<section class="mbs-intro" id="verdict" style="margin-top:96px">
  <h2 class="mbs-epi" style="font-weight:400">The verdict</h2>
  <div class="mbs-lede">
    <p>East Texas is absolutely coming into its own as a golf destination. It&rsquo;s out of the way and there is nowhere great to eat, but for one weekend it was our golf mecca: Tempest&rsquo;s elevation, Wild Spring&rsquo;s greens, a fast casual round at LumberJack and a starter&rsquo;s Buick at Pine Dunes.</p>
    <p>As for my own game, it has never felt further from where I want it. I had some truly great drives and approach shots, and I made some long putts. But putting it all together for 450-plus shots over three days makes me feel like we still have a ways to go.</p>
  </div>
</section>
"""

ALSO = [
 ("Wild Spring Dunes, course two", "Mount Enterprise", "Coore &amp; Crenshaw &middot; in build",
  "Bill Coore and Ben Crenshaw are building a second course on the same 2,400 acres. When it opens, Mount Enterprise becomes a two-course stop and the whole trip can pivot around it.",
  "/drops/on-our-radar-wild-spring-dunes", "Our Wild Spring Dunes preview", "also-wsd", "Wild Spring Dunes"),
 ("Woodland Hills Golf Course", "Nacogdoches", "Don January &middot; 1971",
  "A public daily-fee course in the same town as LumberJack, designed by former PGA Championship winner Don January. An easy add if you want a second Nacogdoches round.",
  "https://woodlandhillsgolfclub.com/", "Book a tee time", "also-woodland", "Woodland Hills via GolfNow"),
 ("Oak Hurst Golf Course", "Bullard, between Tyler and Jacksonville", "Carlton Gipson &middot; 1993",
  "A daily-fee course off Highway 69, about half an hour from Pine Dunes. It pairs with a Sunday at Frankston if you want 36 to finish the trip.",
  "https://www.golfnow.com/courses/-6701-oak-hurst-golf-course-details", "Tee times", "also-oakhurst", "Oak Hurst via GolfNow"),
 ("Rayburn Country Resort", "Brookeland, on Sam Rayburn Reservoir", "27 holes",
  "Further south, a 27-hole resort course in the pines near the largest lake entirely inside Texas, with tee times you can book online. Good for a fourth day, or a trip built around the lake.",
  "https://rayburnresort.com/activities/golf-course/", "Book golf", "also-rayburn", "Rayburn Resort"),
]

ROUTE = [
 ("Friday", "Tempest Golf Club", "Gladewater", "36", "Public tee times. Rode both loops"),
 ("Saturday a.m.", "Wild Spring Dunes", "Mount Enterprise", "18", "Walking only, $275 peak"),
 ("Saturday p.m.", "LumberJack National", "Nacogdoches", "18", "Book online. Casual and quick"),
 ("Sunday", "Pine Dunes", "Frankston", "18", "Book online, $99&ndash;$149"),
]

CSS = """<style>/*TGI-MBS*/
.mbs-hero{position:relative;width:100%;max-width:1600px;margin:0 auto 8px;padding:0 32px}
.mbs-hero img{width:100%;aspect-ratio:16/8;object-fit:cover;object-position:50% 45%;display:block;border:.5px solid var(--ink)}
.mbs-cap{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-intro{max-width:1100px;margin:56px auto 24px;padding:0 32px;display:grid;grid-template-columns:1fr 2fr;gap:56px;align-items:start}
.mbs-epi{font-family:var(--serif);font-size:30px;line-height:1.2;color:var(--grass);border-top:.5px solid var(--ink);padding-top:18px}
.mbs-epi span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:14px}
.mbs-lede p{font-family:var(--serif);font-size:19px;line-height:1.6;margin-bottom:18px}
.mbs-lede p:first-child::first-letter{font-size:64px;float:left;line-height:.9;padding:6px 10px 0 0;color:var(--grass)}
.mbs-toc{max-width:1400px;margin:48px auto;padding:0 32px;display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}
.mbs-toc>div{padding:24px 28px;border-right:.5px solid rgba(20,20,20,.2)}.mbs-toc>div:last-child{border-right:none}
.mbs-toc h3{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.14em;font-size:22px;color:var(--grass);margin-bottom:6px}
.mbs-toc p{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.55;margin-bottom:14px}
.mbs-toc ol{list-style:none;padding:0;margin:0;counter-reset:t}.mbs-toc li{font-family:var(--serif);font-size:17px;padding:5px 0;border-bottom:.5px dotted rgba(20,20,20,.2)}
.mbs-toc li a{border-bottom:none}.mbs-toc li span{font-family:var(--mono);font-size:10px;opacity:.5;margin-right:10px}
.mbs-open{position:relative;max-width:1600px;margin:96px auto 0;padding:0 32px}
.mbs-open img{width:100%;aspect-ratio:21/9;object-fit:cover;display:block;filter:brightness(.72)}
.mbs-open .t{position:absolute;left:32px;right:32px;bottom:0;padding:0 48px 44px;color:#F4F1EA}
.mbs-open .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.85}
.mbs-open h2{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.16em;font-size:clamp(48px,9vw,128px);line-height:1;margin:8px 0 10px}
.mbs-open .d{font-family:var(--serif);font-size:22px;max-width:640px}
.mbs-pill{max-width:820px;margin:36px auto 0;padding:0 32px;font-family:var(--serif);font-size:20px;line-height:1.55;text-align:center;opacity:.85}
.mbs-c{max-width:1400px;margin:96px auto 0;padding:0 32px}
.mbs-c-hd{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:end;border-bottom:.5px solid var(--ink);padding-bottom:14px;margin-bottom:20px}
.mbs-c-hd .num{font-family:var(--serif);font-size:84px;line-height:.8;color:var(--grass)}
.mbs-c-hd h3{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,48px);line-height:1;letter-spacing:-.01em}
.mbs-c-hd .where{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.mbs-lead img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.mbs-body{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:56px;margin-top:32px}
.mbs-text p{font-family:var(--serif);font-size:18px;line-height:1.65;margin-bottom:18px}
.mbs-text a{border-bottom:1px solid currentColor}
.mbs-facts{border:.5px solid var(--ink);padding:22px 24px;align-self:start;background:rgba(45,74,43,.04)}
.mbs-facts .k{font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;opacity:.5;margin-top:14px}
.mbs-facts .k:first-child{margin-top:0}.mbs-facts .v{font-family:var(--serif);font-size:15px;line-height:1.45;margin-top:3px}
.mbs-facts .v.solo{color:var(--grass)}
.mbs-facts a.go{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px}
.mbs-mos{display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:1fr 1fr;gap:12px;margin-top:36px;height:min(64vw,760px)}
.mbs-mos.flip{grid-template-columns:1fr 1.25fr}
.mbs-mos figure{margin:0;position:relative;overflow:hidden;min-height:0}
.mbs-mos figure:first-child{grid-row:1/3}.mbs-mos.flip figure:first-child{grid-column:2}.mbs-mos.flip figure:nth-child(2){grid-column:1;grid-row:1}.mbs-mos.flip figure:nth-child(3){grid-column:1;grid-row:2}
.mbs-mos img{width:100%;height:100%;object-fit:cover;display:block}
.mbs-mos figcaption{position:absolute;left:0;bottom:0;right:0;padding:24px 14px 10px;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#F4F1EA;background:linear-gradient(transparent,rgba(0,0,0,.55))}
.mbs-lead figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-solo{max-width:1400px;margin:120px auto 0;padding:48px 32px 0;border-top:.5px solid var(--ink)}
.mbs-h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,44px);margin-bottom:28px}
.mbs-solo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.mbs-solo h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:10px}
.mbs-solo p{font-family:var(--serif);font-size:16px;line-height:1.55}
.mbs-table{max-width:1400px;margin:72px auto 0;padding:0 32px;overflow-x:auto}
.mbs-table table{width:100%;border-collapse:collapse;font-family:var(--serif);font-size:15px}
.mbs-table th{font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;text-align:left;padding:10px 12px;border-bottom:.5px solid var(--ink);opacity:.7}
.mbs-table td{padding:11px 12px;border-bottom:.5px solid rgba(20,20,20,.15);vertical-align:top}
.mbs-table td.p{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--grass)}
@media(max-width:900px){.mbs-intro{grid-template-columns:1fr;gap:28px}.mbs-toc{grid-template-columns:1fr}.mbs-toc>div{border-right:none;border-bottom:.5px solid rgba(20,20,20,.2)}
.mbs-body{grid-template-columns:1fr;gap:28px}.mbs-solo-grid{grid-template-columns:1fr 1fr}.mbs-open img{aspect-ratio:4/3}.mbs-open .t{padding:0 22px 26px}}
@media(max-width:600px){.mbs-hero,.mbs-intro,.mbs-toc,.mbs-open,.mbs-c,.mbs-solo,.mbs-table,.mbs-pill{padding-left:18px;padding-right:18px}
.mbs-open .t{left:18px;right:18px}.mbs-hero img{aspect-ratio:4/3}.mbs-c-hd .num{font-size:56px}.mbs-solo-grid{grid-template-columns:1fr}
.mbs-mos,.mbs-mos.flip{grid-template-columns:1fr 1fr;grid-template-rows:auto auto;height:auto}
.mbs-mos figure:first-child,.mbs-mos.flip figure:first-child{grid-column:1/3;grid-row:1;aspect-ratio:4/3}.mbs-mos figure:nth-child(2),.mbs-mos.flip figure:nth-child(2){grid-column:1;grid-row:2;aspect-ratio:1}.mbs-mos figure:nth-child(3),.mbs-mos.flip figure:nth-child(3){grid-column:2;grid-row:2;aspect-ratio:1}
.mbs-lede p{font-size:17px}.mbs-text p{font-size:17px}}
</style>
"""


EXTRA_CSS = """<style>/*TGI-ETX*/
.etx-nums{max-width:1400px;margin:40px auto 0;padding:0 32px;display:grid;grid-template-columns:repeat(5,1fr);border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink)}
.etx-nums div{padding:22px 18px;border-right:.5px solid rgba(20,20,20,.2);text-align:center}.etx-nums div:last-child{border-right:none}
.etx-nums b{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(36px,5vw,64px);line-height:1;color:var(--grass)}
.etx-nums span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
@media(max-width:700px){.etx-nums{grid-template-columns:repeat(3,1fr);padding-left:18px;padding-right:18px}.etx-nums div:nth-child(3){border-right:none}.etx-nums div:nth-child(n+4){border-top:.5px solid rgba(20,20,20,.2)}}
.etx-also p.etx-w{font-family:var(--mono)!important;font-size:10px!important;letter-spacing:.12em;text-transform:uppercase;opacity:.55;line-height:1.5!important;margin:0 0 10px}
.mbs-pill{text-align:left!important;font-size:19px!important;line-height:1.65!important}
.etx-af{margin:0 0 14px}.etx-af img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;border:.5px solid var(--ink)}.etx-af figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;opacity:.5;margin-top:6px}
.etx-also h3{font-family:var(--serif)!important;font-size:21px!important;letter-spacing:0!important;text-transform:none!important;color:var(--ink)!important;margin-bottom:6px!important}
</style>
"""

ORDER = [k for d in DAYS for k in d[6]]


def course_html(k, n, flip):
    day, name, place, des, url, lalt, lcap, paras, facts, mos = C[k]
    fx = "".join(f'<div class="k">{H.escape(lbl)}</div><div class="v{" solo" if lbl == "Tell a friend" else ""}">{v}{"" if v.endswith(".") else "."}</div>' for lbl, v in facts.items())
    text = "".join(f"<p>{p}</p>" for p in paras)
    figs = "".join(f'<figure><img src="{IMG}/{SHORT[k]}-{i+2}.jpg" alt="{H.escape(a, quote=True)}" loading="lazy" /><figcaption>{c}</figcaption></figure>' for i, (a, c) in enumerate(mos))
    mosaic = f'<div class="mbs-mos{" flip" if flip else ""}">{figs}</div>'
    q = ""
    if k in PQ:
        qq, who = PQ[k]
        q = (f'\n<div class="pull-quote" style="margin:72px auto 0"><div class="pull-quote-inner">&ldquo;{qq}&rdquo;'
             f'<span class="pull-quote-attr">&mdash; {who}</span></div></div>\n')
    return (f'\n<article class="mbs-c" id="{k}">\n  <div class="mbs-c-hd"><div class="num">{n:02d}</div><div><h3>{name}</h3>'
            f'<div class="where">{place} &middot; {des}</div></div></div>\n'
            f'  <figure class="mbs-lead"><img src="{IMG}/{SHORT[k]}-1.jpg" alt="{H.escape(lalt, quote=True)}" loading="lazy" /><figcaption>{lcap} Photo: The Grassy Issue</figcaption></figure>\n'
            f'  <div class="mbs-body"><div class="mbs-text">{text}</div><aside class="mbs-facts">{fx}'
            f'<a class="go" href="{url}" target="_blank" rel="noopener">{"Book at " + name if "golfnow" not in url else "Tee times"} &#8599;</a></aside></div>\n  {mosaic}\n</article>\n{q}')


SHORT = {"tempest": "tempest", "wild-spring-dunes": "wsd", "lumberjack-national": "lumberjack", "pine-dunes": "pinedunes"}


def toc_html():
    cols = []
    n = 1
    for key, name, roman, line, _, _, ids in DAYS:
        lis = ""
        for k in ids:
            lis += f'<li><span>{n:02d}</span><a href="#{k}">{C[k][1]}</a></li>'
            n += 1
        cols.append(f'<div><h3><a href="#{key}" style="border-bottom:none">{name}</a></h3><p>{line}</p><ol>{lis}</ol></div>')
    return f'\n<nav class="mbs-toc etx" aria-label="The three days">{"".join(cols)}</nav>\n'


def nums_html():
    return '\n<div class="etx-nums">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in NUMS) + "</div>\n"


def route_html():
    rows = "".join(f'<tr><td class="p">{d}</td><td>{c}</td><td>{t}</td><td>{h}</td><td>{note}</td></tr>' for d, c, t, h, note in ROUTE)
    return (f'\n<section class="mbs-table"><h2 class="mbs-h2" id="plan-it">Plan It Yourself</h2><table><thead><tr>'
            f'<th>When</th><th>Course</th><th>Town</th><th>Holes</th><th>Good to know</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<p class="mbs-text" style="margin-top:22px;max-width:820px"><span style="font-family:var(--serif);font-size:17px;line-height:1.6">All four courses sit in the Piney Woods, '
            f'roughly three and a half to four hours from Austin. Rough drive times between them: Gladewater to Mount Enterprise about an hour, '
            f'Mount Enterprise to Nacogdoches well under an hour, Nacogdoches to Frankston a little over an hour. Book a house somewhere in the middle and grill. '
            f'For more Texas golf road trips, see <a href="/drops/10-texas-courses-worth-the-trip">10 Texas courses to travel for</a> '
            f'and our <a href="/drops/on-our-radar-wild-spring-dunes">Wild Spring Dunes preview</a>.</span></p>'
            f'<p class="mbs-cap" style="margin-top:12px">Played November 6&ndash;8, 2026. Course facts checked November 10, 2026. Drive times are rough estimates.</p></section>\n')


def also_html():
    cards = "".join(f'<div><figure class="etx-af"><img src="{IMG}/{im}.jpg" alt="{H.escape(H.unescape(n), quote=True)}" loading="lazy" /><figcaption>Photo: {cr}</figcaption></figure><h3>{n}</h3><p class="etx-w">{w} &middot; {d}</p><p>{t}</p>'
                    f'<p style="margin-top:10px"><a href="{u}" style="font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--ink)"'
                    f'{"" if u.startswith("/") else " target=&quot;_blank&quot; rel=&quot;noopener&quot;".replace("&quot;", chr(34))}>{l} &#8599;</a></p></div>'
                    for n, w, d, t, u, l, im, cr in ALSO)
    return (f'\n<section class="mbs-solo etx-also">\n  <h2 class="mbs-h2" id="also">A Few More for Next Time</h2>\n'
            f'  <p class="mbs-text" style="max-width:820px;margin:-8px 0 28px"><span style="font-family:var(--serif);font-size:17px;line-height:1.6">We didn&rsquo;t play these on this trip. Each one fits the same route if you have an extra day or want a different mix.</span></p>\n'
            f'  <div class="mbs-solo-grid">{cards}</div>\n</section>\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": C[k][4], "name": H.unescape(C[k][1])} for i, k in enumerate(ORDER)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-10", "dateModified": "2026-11-10",
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
    assert len(ORDER) == N == len(set(ORDER)) and set(ORDER) == set(C), set(C) ^ set(ORDER)
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
    <span>East Texas &middot; played November 6&ndash;8, 2026</span>
  </div>
</header>

<div class="mbs-hero"><img src="{IMG}/hero.jpg" alt="Early-morning light and long shadows across a Wild Spring Dunes fairway running toward a green framed by pines" fetchpriority="high" style="object-position:50% 60%" />
<div class="mbs-cap">Saturday morning at Wild Spring Dunes. Photo: The Grassy Issue</div></div>
"""
    body += nums_html() + INTRO + toc_html()
    n = 1
    for key, name, roman, line, para, alt, ids in DAYS:
        body += (f'\n<section class="mbs-open" id="{key}"><img src="{IMG}/open-{key}.jpg" alt="{H.escape(alt, quote=True)}" loading="lazy" />'
                 f'<div class="t"><div class="n">Day {roman}</div><h2>{name}</h2><div class="d">{line}</div></div></section>\n'
                 f'<p class="mbs-pill">{para}</p>\n')
        for j, k in enumerate(ids):
            body += course_html(k, n, j % 2 == 1)
            n += 1
    body += OFF + VERDICT + route_html() + also_html()
    out = head_top() + head_rest.replace("</head>", CSS + EXTRA_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} courses")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    if fin.count('class="mbs-c"') != N: bad.append("course count")
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", re.sub(r"Fort Worth|worth the trip", "", txt), re.I): bad.append("banned word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
