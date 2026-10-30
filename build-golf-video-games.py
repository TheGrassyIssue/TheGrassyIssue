#!/usr/bin/env python3
"""build-golf-video-games.py — The Best Golf Video Games of All Time (clocks fall back Nov 1, 2026). 30 October 2026.
Options sheet golf-video-games-options.html (Oct 13, TGI PICK 16) -> Lenny 30 Oct: "Let's finish up that video game post - now that
we're losing an hour of daylight", plus Normal Golf Game (Steam 3510740), "can't stop watching livestreams of, delightfully frustrating".
Cloned from build-angus-grace-btk.py; wide single-column cards with 16:9 official screenshots.
FACTS + PRICES checked 30 Oct 2026 on Steam appdetails, Nintendo eShop, PS Store, Apple; Guinness (NES Golf 4,009,599);
Iwata Asks; Nintendo Life; Siliconera; GameSpot; Metacritic; TechRadar; Push Square; Triband press kit; IGF 2015; Game Developer;
Mighty Coconut "5 years in numbers"; EA press release (Tiger 12); PlayStation LifeStyle (2K25 servers). Corrections applied:
Tiger 12 = first Augusta in the Tiger series (not first ever); 1997 Everybody's Golf was Camelot; NES Golf = best-selling golf game
per Guinness (not "best-selling NES sports game"). Links 386 / Tiger 04 / Tiger 12 / Toadstool Tour have no official images: text only.
No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Best New Golf Video Games to Play When the Clocks Fall Back"
DESC = ("The clocks fall back November 1. The best golf video games of the last few years, from PGA Tour 2K25 and Mario Golf: "
        "Super Rush to Super Battle Golf and Normal Golf Game, with where to play them and prices.")
H1 = "The Best New Golf Video Games"
BC = "The Best New Golf Video Games"
SLUG = "best-new-golf-video-games"
IMG = "/images/best-golf-video-games"
SHOP = ""
P = {
 "pga2k25": ("2025 &middot; HB Studios / 2K", "PGA Tour 2K25", "Steam or PS5, $39.99; Switch 2 $17.99 on sale to Nov 6", "https://store.steampowered.com/app/2385530/",
   "The best current golf sim. The swing grades contact, rhythm and path, the course designer is deep, and it is the first in the series with the PGA Championship, the U.S. Open and The Open. It scored 80 on Metacritic for PS5 and came to Switch 2 in February. One thing to know: online play ends February 28, 2029. &ldquo;Just like real-life golf, PGA Tour 2K25 is a hearty mix of satisfaction and frustration,&rdquo; TechRadar said."),
 "eapga": ("2023 &middot; EA Tiburon / Electronic Arts", "EA Sports PGA Tour", "Steam $69.99; also PS5 and Xbox Series", "https://store.steampowered.com/app/1677350/",
   "The other big sim, and the home of the majors: EA&rsquo;s own store copy calls it &ldquo;the exclusive home of the Majors,&rdquo; with ball flight from its Pure Strike system powered by the Tour&rsquo;s ShotLink data. Courses look photographed, links holes included. Critics liked it more than Steam players did (OpenCritic 75, Steam reviews mixed), and Metro called it &ldquo;the best golf game of the modern era.&rdquo; Since EA shut down Rory McIlroy PGA Tour in January 2025, it is the only EA golf game you can still play online."),
 "golfplus": ("2021 &middot; GOLF+", "GOLF+ (VR)", "Meta Quest; 3 free courses, more with the GOLF+ Pass", "https://www.meta.com/experiences/golf/2412327085529357/",
   "The closest thing to a simulator you can stand up in. The PGA Tour named it its official VR golf game in December 2022, and its Meta store page lists Pebble Beach, TPC Sawgrass and St Andrews among more than 50 real-world destinations. On Quest 3 you can now putt with a real putter and a real ball. A Steam version for PC VR is listed as coming soon."),
 "hotshots": ("1997&ndash;2025 &middot; Camelot, Clap Hanz, now Bandai Namco", "Everybody&rsquo;s Golf / Hot Shots Golf", "Steam or PS5, $39.99; Switch $25.99 on sale to Oct 31", "https://store.steampowered.com/app/2730810/",
   "The series that taught a generation the three-press swing. Camelot made the 1997 original on PlayStation and Clap Hanz took over from the second game. In September 2025 Bandai Namco revived it as Everybody&rsquo;s Golf Hot Shots, the first entry without Clap Hanz. Reviews were mixed, but Push Square said &ldquo;the core gameplay remains fun and accessible most of the time,&rdquo; and it is the easiest way to play the series on current hardware."),
 "easy": ("2021 &middot; Clap Hanz", "Easy Come Easy Golf", "Switch eShop $19.99; Apple Arcade", "https://www.nintendo.com/us/store/products/easy-come-easy-golf-switch/",
   "The other Hot Shots. Clap Hanz, the studio that made most of the Everybody&rsquo;s Golf games, launched it on Apple Arcade in 2021 as Clap Hanz Golf and brought it to Switch in 2022. It is the same bright, three-press arcade golf, and the first Clap Hanz golf game on a Nintendo console. &ldquo;That&rsquo;s a hole in one,&rdquo; wrote Thumbsticks."),
 "superrush": ("2021 &middot; Camelot / Nintendo", "Mario Golf: Super Rush", "Switch eShop, $59.99", "https://www.nintendo.com/us/store/products/mario-golf-super-rush-switch/",
   "The newest Mario Golf, from Camelot, the studio that has made the series since the N64. Its big idea is Speed Golf, where everyone hits at once and then sprints after the ball, but the regular stroke play is where it shines. &ldquo;Running between shots can be chaotic fun, but Mario Golf truly lives in its ever-soothing standard mode,&rdquo; Eurogamer wrote. Best with four on a couch."),
 "switchsports": ("2006&ndash;2026 &middot; Nintendo", "Wii Sports Golf to Switch Sports", "Switch Sports, $39.99; Switch Sports Resort (Switch 2), $49.99", "https://www.nintendo.com/us/store/products/nintendo-switch-sports-switch/",
   "The motion swing that got your parents to swing a Wii Remote in the living room. Nintendo counted 82.79 million copies of Wii Sports by 2016, most of them bundled with the console. The same 21 holes came back free in Nintendo Switch Sports in November 2022, and golf is one of the 12 sports in Nintendo Switch Sports Resort, out on Switch 2 on October 22. &ldquo;Bowling and Golf still rule,&rdquo; Nintendo Life wrote in its review."),
 "normal": ("2026 &middot; Luke Muscat", "Normal Golf Game", "Steam (Windows), $9.99", "https://store.steampowered.com/app/3510740/Normal_Golf_Game/",
   "The one we cannot stop watching people stream, and it is delightfully frustrating. Luke Muscat, who made Fruit Ninja and Jetpack Joyride, built it almost entirely by himself and calls it a sadistically accurate recreation of golf. You control the path of the club with physics while managing your stance, direction and the face angle, on a giant course that is both a trap and a playground. The setup: you owe a $100,000 fee and you are not leaving until Muscat is satisfied. It came out on September 21. Hit anything, shoot from anywhere, and expect to yell."),
 "cursed": ("2022 &middot; Chuhai Labs / Thunderful", "Cursed to Golf", "Steam $1.99 on sale to Nov 9 ($19.99); Switch $19.99", "https://store.steampowered.com/app/1726120/",
   "The Halloween pick. You died mid-round and wake up in Golf Purgatory, and the only way out is to play your way through, one roguelike course at a time, with a shot limit, ace cards and idols that buy you strokes back. GameSpot gave it 9 out of 10 and called it &ldquo;a brilliant golf game that plays like a wildly experimental precision-platformer.&rdquo; It is $1.99 on Steam until November 9."),
 "wasteland": ("2021 &middot; Demagog Studio", "Golf Club: Wasteland", "Steam $1.99 on sale to Nov 3 ($9.99)", "https://store.steampowered.com/app/1556870/",
   "The moodiest game here. Humanity is gone, Earth has become a golf course for the ultra-rich who left for Mars, and you play through the ruins while a radio station called Radio Nostalgia tells the story of what happened.  Critics rated it 77 on OpenCritic, and Steam now lists it as Golf Club Nostalgia."),
 "wtg": ("2019 &middot; Triband", "What the Golf?", "Steam $19.99; Switch $9.99 on sale to Oct 31; Apple Arcade", "https://store.steampowered.com/app/785790/",
   "A golf parody in which almost nothing is golf. In one level you hit the house instead of the ball, in another you are the ball, and the joke keeps changing for hours. It won Best Mobile Game at the 2020 GDC Awards and IGN&rsquo;s best mobile game of 2019. PCGamesN promised &ldquo;none of the crushing disappointment so often associated with actual golf.&rdquo;"),
 "battle": ("2026 &middot; Brimstone / Oro Interactive", "Super Battle Golf", "Steam, $12.99", "https://store.steampowered.com/app/4069520/",
   "The breakout golf game of 2026. Up to eight players tee off at the same time and race to the hole, and you are allowed to knock your friends out of the way with weapons. It sold 100,000 copies in its first 48 hours and passed a million in about a month, and Steam reviews are 93% positive. Gaming Age compared it to Mario Party and Mario Kart. Console versions have been announced but not dated."),
 "gwyf": ("2020 &middot; Team17", "Golf With Your Friends", "Steam $3.74 on sale ($14.99); Switch $19.99", "https://store.steampowered.com/app/431240/",
   "The online mini golf game for a group chat on a Tuesday night. Big groups, courses from pirate coves to neon tunnels, and power-ups that ruin friendships. Team17 bought the game for &pound;12 million in 2021, when it had about 5.5 million owners. A sequel from Radical Forge is still listed for fall 2026 with no date, so the original is the one to play this month."),
 "walkabout": ("2020 &middot; Mighty Coconut", "Walkabout Mini Golf", "Steam VR $24.99; Meta Quest; PS VR2", "https://store.steampowered.com/app/1408230/",
   "The best mini golf in VR, made by Mighty Coconut here in Austin. Players have taken more than 2 billion putts and played over 23 million hours, and its glowing night courses fit a dark November evening. &ldquo;Everything you see in Walkabout has been funded 100% by people purchasing the game, courses and growing our community,&rdquo; CEO Lucas Martell wrote. New courses are $4.99 each."),
}
SECTIONS = [
 ("The Sims", "sims", ["pga2k25", "eapga", "golfplus"],
  "<strong>Three games &middot; from $17.99</strong>Real courses, real swings and, in one case, a real putter."),
 ("Arcade and Couch", "couch", ["hotshots", "easy", "superrush", "switchsports"],
  "<strong>Four games &middot; $19.99&ndash;$59.99</strong>Three-press swings, Mario and the motion swing, for the living room."),
 ("The Indies", "indies", ["normal", "cursed", "wasteland", "wtg"],
  "<strong>Four games &middot; $1.99&ndash;$19.99</strong>The strangest and most interesting golf games of the last few years, two of them $1.99 this week."),
 ("Golf With Other People", "friends", ["battle", "gwyf", "walkabout"],
  "<strong>Three games &middot; online and VR</strong>For when the group chat cannot get a tee time."),
]
N = 14
PQ = {
 "indies": ("A golf game for people that don&rsquo;t like golf.", "PlayStation Universe, on Golf Club: Wasteland"),
}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The clocks fall back on Sunday, November 1, and the after-work nine goes with them. For the next few months the light will be gone before most of us can get to the course, which makes this a good week to look at how good golf games have gotten.</p>
    <p>This is our list of the best ones from the last few years, from PGA Tour 2K25 and EA&rsquo;s PGA Tour to Super Battle Golf, the breakout of 2026, and Normal Golf Game, which came out in September and which we cannot stop watching people stream. We picked for how well each one plays, whether it does something new and whether you can play it tonight. Every price was checked on October 30, and a lot of them are on sale.</p>
    <p><strong>Where to start.</strong> If you want a sim, PGA Tour 2K25 is down to $39.99, or $17.99 on Switch 2 until November 6. If you want something different, Cursed to Golf and Golf Club: Wasteland are both $1.99 on Steam this week. If you want to laugh with friends, Super Battle Golf. And if you want to stay off a screen entirely, we understand; there is always the range under the lights.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Clocks fall back</span><span>Sunday, Nov 1</span></div>
      <div class="sidebar-detail"><span class="l">Games</span><span>14, from 2020 to 2026</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>Switch Sports Resort, Oct 22</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Cursed to Golf, $1.99 on sale</span></div>
      <div class="sidebar-detail"><span class="l">Breakout</span><span>Super Battle Golf</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>PGA Tour 2K25</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfGames</span>
        <span class="hashtag">#FallBack</span>
        <span class="hashtag">#AfterDark</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
LOST = """
<section class="products" data-btk="lost" style="margin-top:8px;">
  <div class="drop-tag grass">The classics</div>
  <h2 class="products-hdr" id="where-it-started">Where It Started</h2>
  <div class="writeup-body">
    <p>Every game above owes something to these. A few are still easy to play.</p>
    <p><strong>Golf (NES, 1984).</strong> Programmed by Satoru Iwata, who later ran Nintendo, and listed by Guinness as the best-selling golf video game, at 4,009,599 copies. After Iwata died, a copy was hidden inside the first Switch firmware, playable only on July 11. It is in the NES library on Nintendo Switch Online now, along with Kirby&rsquo;s Dream Course in the SNES library.</p>
    <p><strong>Mario Golf (N64, 1999).</strong> Camelot&rsquo;s first Mario Golf, after making the first Everybody&rsquo;s Golf in 1997. It scored 91 on Metacritic and is on Switch Online&rsquo;s Expansion Pack.</p>
    <p><strong>Links 386 Pro (1992) and Tiger Woods PGA Tour 2004 (2003).</strong> The PC benchmark and, for a lot of people, the golf game. Neither is sold anymore.</p>
    <p><strong>Golf Story (2017) and Desert Golfing (2014).</strong> The two older indies we still recommend most. Golf Story is $5.99 on Switch until November 20; Desert Golfing is $1.99 on iOS and Steam.</p>
  </div>
</section>
"""
ROWS = [("PGA Tour 2K25", "Steam, PS5 / Switch 2", "$39.99 / $17.99 sale to Nov 6"),
 ("EA Sports PGA Tour", "Steam, PS5, Xbox Series", "$69.99 on Steam"),
 ("GOLF+", "Meta Quest", "3 free courses; GOLF+ Pass for more"),
 ("Everybody&rsquo;s Golf Hot Shots", "Steam, PS5 / Switch", "$39.99 / $25.99 sale to Oct 31"),
 ("Easy Come Easy Golf", "Switch / Apple Arcade", "$19.99 / subscription"),
 ("Mario Golf: Super Rush", "Switch", "$59.99"),
 ("Nintendo Switch Sports", "Switch / Switch 2 (Resort)", "$39.99 / $49.99"),
 ("Normal Golf Game", "Steam (Windows)", "$9.99"),
 ("Cursed to Golf", "Steam / Switch", "$1.99 sale to Nov 9 / $19.99"),
 ("Golf Club: Wasteland", "Steam", "$1.99 sale to Nov 3"),
 ("What the Golf?", "Steam / Switch / Apple Arcade", "$19.99 / $9.99 sale to Oct 31 / subscription"),
 ("Super Battle Golf", "Steam", "$12.99"),
 ("Golf With Your Friends", "Steam / Switch", "$3.74 sale / $19.99"),
 ("Walkabout Mini Golf", "Steam VR, Meta Quest, PS VR2", "$24.99 on Steam")]
TABLE = ('\n<section id="gg-table">\n<style>#gg-table{padding:40px 20px 8px;border-top:1px solid var(--ink,#141414)}#gg-table .t-in{max-width:960px;margin:0 auto}'
 '#gg-table h2{font-family:var(--serif,Georgia,serif);font-size:clamp(22px,3vw,30px);text-align:center;margin:0 0 6px;font-weight:400}'
 '#gg-table .t-sub{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-align:center;opacity:.6;margin-bottom:18px}'
 '#gg-table .t-wrap{overflow-x:auto}#gg-table table{width:100%;border-collapse:collapse;font-size:14px}#gg-table th{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;padding:8px 10px;border-bottom:1px solid var(--ink,#141414)}'
 '#gg-table td{padding:9px 10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top}#gg-table td:first-child{font-weight:500}</style>\n'
 '<div class="t-in"><h2 id="where-to-play">Where to Play Them Tonight</h2><div class="t-sub">US prices &middot; checked October 30, 2026</div><div class="t-wrap"><table>\n'
 '<thead><tr><th>Game</th><th>Where</th><th>Price</th></tr></thead><tbody>\n'
 + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in ROWS) + '\n</tbody></table></div></div>\n</section>\n')
STORY = LOST + TABLE
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/golf-games/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GG-WIDE*/.products-grid[data-wide]>.product-card{flex:0 0 100%!important;display:grid;grid-template-columns:3fr 2fr}.products-grid[data-wide] .product-gallery{aspect-ratio:16/9}.products-grid[data-wide] .product-body{display:flex;flex-direction:column;justify-content:center;text-align:left!important;padding:22px 26px}@media(max-width:820px){.products-grid[data-wide]>.product-card{grid-template-columns:1fr}}</style>'
            '<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
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
            f'<div class="product-name">{item}</div><div class="product-brand">Play it: {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Where to play &#8599;</a></div></div>')


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(P[h][1])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-30", "dateModified": "2026-10-30",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"game" if len(ids)==1 else "games"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}" data-wide="1">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Golf Video Games</span><span class="dot"></span>
    <span>14 games from 2020 to 2026 &middot; prices checked October 30, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="An island green surrounded by water and grandstands in EA Sports PGA Tour" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
