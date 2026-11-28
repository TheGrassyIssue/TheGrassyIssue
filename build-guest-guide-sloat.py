#!/usr/bin/env python3
"""build-guest-guide-sloat.py — Guest Field Guide No. 01: San Francisco, according to SLOAT. 25 November 2026.
SOURCE: SLOAT's answers, Google Doc "SLOAT — San Francisco City Guide | Working Draft" (saved to
research/guest-guides/sloat/answers.md). Quotes are word for word, trimmed only; Lenny: credit to both founders / SLOAT
unless a name is explicit; run Drink with two picks. Photos: SLOAT Journal Vol. 1 (Drive), SLOAT's own site/IG
(research/sloat/life), PGA West site banner. Products: sloat.cc/products.json, USD, read Nov 25, 2026.
Course and venue facts checked Nov 25, 2026 (see research/guest-guides/sloat/facts.md). No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "guest-field-guide-san-francisco-sloat"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/guest-sf-sloat"
TITLE = "San Francisco, According to SLOAT: Where the Founders Play, Eat and Surf"
DESC = ("Guest Field Guide No. 01. SLOAT founders Dan Fibiger and Teague Moriarty on golf along Sloat Boulevard: "
        "the Presidio, Harding Park and Crystal Springs, two rounds they travel for, where they eat after, and an interview.")
H1 = "San Francisco, According to SLOAT"
FR = json.loads((ROOT / "research/sloat/frames.json").read_text(encoding="utf-8"))

CSS = ('<style>/*TGI-GUEST-GUIDE*/'
       '.gg-kick{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#2D4A2B;margin:0 0 14px}'
       '.gg-dek{font-family:var(--serif);font-size:clamp(19px,2vw,23px);line-height:1.45;max-width:760px;margin:14px auto 0;text-align:center;opacity:.85}'
       '.gg-guides,.gg-iv,.gg-cols,.gg-wrap,.writeup-body,.gg-day{text-align:left}.gg-guides,.gg-day{margin-left:auto!important;margin-right:auto!important}.writeup-body{margin-left:auto!important;margin-right:auto!important}.writeup-body p,.gg-guides p,.gg-iv p,.gg-course p{text-align:left!important}'
       '.gg-wrap{max-width:1300px;margin:0 auto}'
       '.products{padding-top:28px!important}.products-hdr{margin-bottom:10px}.pull-quote{margin-top:34px!important;margin-bottom:14px!important}'
       '.gg-band{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:22px 0 6px}.gg-band img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}.gg-band figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:5px}'
       '.gg-iv{max-width:1000px!important}.gg-iv .gg-q,.gg-iv .gg-a{max-width:760px;margin-left:auto;margin-right:auto}.gg-iv h3{max-width:760px;margin-left:auto!important;margin-right:auto!important}'
       '.gg-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:34px;align-items:center;margin-top:30px}.gg-split .gg-band{margin:0;grid-template-columns:repeat(2,minmax(0,1fr))}'
       '@media(max-width:820px){.gg-split{grid-template-columns:1fr}.gg-band{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '.gg-two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.gg-wide{max-width:1000px;margin:26px auto 0}.gg-wide img{width:100%;display:block}.gg-wide figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:6px}'
       '.gg-guides{display:grid;grid-template-columns:400px 1fr;gap:28px;align-items:start;max-width:900px}'
       '.gg-guides img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}.gg-wide img{aspect-ratio:auto!important}'
       '.gg-guides .cap{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:6px;line-height:1.5}'
       '.gg-guides h3{font-family:var(--serif);font-weight:600;font-size:24px;margin:0 0 8px}'
       '.gg-hits{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:.5px solid var(--ink);margin:10px 0 0}'
       '.gg-hit{padding:16px 14px 18px 0;border-bottom:.5px solid rgba(20,20,20,.18)}'
       '.gg-hit .k{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:#2D4A2B;display:block;margin-bottom:6px}'
       '.gg-hit .v{font-family:var(--serif);font-size:17px;line-height:1.4}'
       '.gg-course{display:grid;grid-template-columns:70px minmax(0,1fr) minmax(0,440px);gap:26px;padding:26px 0;border-top:.5px solid rgba(20,20,20,.2);align-items:start}'
       '.gg-num{font-family:var(--serif);font-size:54px;line-height:1;color:#2D4A2B;opacity:.35}'
       '.gg-course h3{font-family:var(--serif);font-weight:600;font-size:clamp(24px,2.6vw,32px);margin:0 0 4px}'
       '.gg-where{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.6;margin-bottom:16px}'
       '.gg-course p{font-size:16.5px;line-height:1.7;margin:0 0 12px;max-width:760px}'
       '.gg-lbl{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2D4A2B;margin-right:8px}'
       '.gg-facts{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;opacity:.7;line-height:1.7;margin-top:10px}'
       '.gg-facts a{border-bottom:1px solid currentColor}'
       '.gg-photos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:0}.gg-photos figure:only-child{grid-column:1/-1}.gg-photos img{aspect-ratio:4/5;object-fit:cover}.gg-photos figure:only-child img{aspect-ratio:5/4}'
       '.gg-photos.one{grid-template-columns:1fr}.gg-photos img{width:100%;display:block}.gg-photos figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin-top:6px}'
       '.gg-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px;margin-top:18px}'
       '.gg-col h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#2D4A2B;border-bottom:.5px solid var(--ink);padding-bottom:8px;margin:0 0 4px}'
       '.gg-spot{padding:12px 0;border-bottom:.5px solid rgba(20,20,20,.15)}'
       '.gg-rests{display:grid;gap:0}.gg-rest{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:24px;padding:18px 0;border-top:.5px solid rgba(20,20,20,.2);align-items:start}.gg-rt b{font-family:var(--serif);font-weight:600;font-size:22px;display:block;margin:4px 0 2px}.gg-rt .w{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;display:block;margin-bottom:8px}.gg-rt .t{font-family:var(--serif);font-size:17px;line-height:1.5;display:block;margin-bottom:8px}.gg-kind{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:#2D4A2B}.gg-rimgs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}.gg-rimgs img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}.gg-rimgs[data-n="1"]{grid-template-columns:1fr}.gg-rimgs[data-n="1"] img{aspect-ratio:4/1}.gg-rimgs[data-n="2"] img{aspect-ratio:3/2}.gg-rimgs[data-n="2"]{grid-template-columns:repeat(2,minmax(0,1fr))}.gg-rimgs[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}.gg-rimgs[data-n="3"] img{aspect-ratio:4/3}@media(max-width:820px){.gg-rest{grid-template-columns:1fr;gap:12px}.gg-rimgs{grid-template-columns:repeat(2,minmax(0,1fr))!important}.gg-rimgs[data-n="1"]{grid-template-columns:1fr!important}.gg-rimgs img{aspect-ratio:1/1!important}}.gg-cap{font-family:var(--mono);font-size:8.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:4px}.gg-spot b{font-family:var(--serif);font-weight:600;font-size:18px;display:block;margin-bottom:2px}'
       '.gg-spot .w{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;display:block;margin-bottom:6px}'
       '.gg-spot span.t{font-size:15px;line-height:1.55}'
       '.gg-iv{max-width:760px;margin:0 auto}'
       '.gg-iv h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#2D4A2B;margin:44px 0 8px;padding-top:14px;border-top:.5px solid var(--ink)}'
       '.gg-q{font-family:var(--serif);font-weight:600;font-size:19px;line-height:1.4;margin:26px 0 8px}'
       '.gg-q:before{content:"TGI \\2014  ";font-family:var(--mono);font-weight:400;font-size:10px;letter-spacing:.12em;opacity:.5}'
       '.gg-a p{font-size:16.5px;line-height:1.7;margin:0 0 10px}'
       '.gg-who{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;opacity:.55}'
       '.gg-day{font-family:var(--serif);font-size:clamp(19px,2vw,22px);line-height:1.55;max-width:760px;margin:10px 0 0}'
       '.products-grid[data-n="5"]{grid-template-columns:repeat(5,minmax(0,1fr));gap:16px}'
       '@media(max-width:1100px){.products-grid[data-n="5"]{grid-template-columns:repeat(3,minmax(0,1fr))}.gg-cols{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '@media(max-width:820px){.gg-guides{grid-template-columns:1fr}.gg-guides img{max-width:260px}.gg-hits{grid-template-columns:repeat(2,minmax(0,1fr))}'
       '.gg-course{grid-template-columns:1fr;gap:10px}.gg-num{font-size:40px}.products-grid[data-n="5"]{grid-template-columns:repeat(2,minmax(0,1fr))}.gg-cols{grid-template-columns:1fr}}'
       '</style>\n')


def esc_attr(s):
    return H.escape(H.unescape(re.sub(r"<[^>]+>", "", s)), quote=True)


def pq(text, who):
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def section(tag, title, hid, inner, intro=""):
    i = f'  <p class="cat-kicker">{intro}</p>\n' if intro else ""
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{tag}</div>\n'
            f'  <h2 class="products-hdr" id="{hid}">{title}</h2>\n{i}{inner}\n</section>\n')


# ---------- WHERE WE PLAY ----------
COURSES = [
 ("01", "Crystal Springs Golf Course", "Burlingame &middot; public &middot; 18 holes",
  "It&rsquo;s a challenging track with a great community, particularly through the men&rsquo;s club.",
  "Nine. It&rsquo;s one of the more challenging holes, with a really narrow window for your drive and an approach into a very tiered green. You have to know where to land it depending on the pin position. It&rsquo;s not an easy hole, but getting a par or birdie on it is very satisfying.",
  "Don&rsquo;t try to smash driver. You can often hit it 200 yards and get around the dogleg. It&rsquo;s safer, with red stakes right and OB left, and it&rsquo;s easy to lose a ball.",
  'Public, 18 holes, south of the city off I-280. <a href="https://www.crystalspringsgolf.com/" target="_blank" rel="noopener">crystalspringsgolf.com</a>',
  [("crystal-1.jpg", "Crystal Springs Reservoir below the hills south of San Francisco", "Crystal Springs Reservoir, beside the course &middot; Kglavin, CC BY 2.5"),
   ("crystal-2.jpg", "Crystal Springs Reservoir from the air", "Crystal Springs from above &middot; Pi.1415926535, CC BY-SA 3.0")]),
 ("02", "TPC Harding Park", "Lake Merced, San Francisco &middot; city-owned &middot; 18 holes",
  "It&rsquo;s ten minutes from my house, it&rsquo;s beautiful, and you can spray your driver around without losing your ball most of the time. It&rsquo;s also hosted a PGA Championship, so you&rsquo;re playing a course with some serious history.",
  "Thirteen and fourteen. They&rsquo;re both fun par fours where you have to know where to place your drive to have a good approach shot in.",
  "Check how thick the rough is. If it&rsquo;s recently cut, being off the fairway isn&rsquo;t very punishing. When they let it grow out, it can be really challenging and cost you distance.",
  'Owned by the City of San Francisco, beside Lake Merced; it hosted the 2020 PGA Championship. The nine-hole Fleming course sits next door. <a href="https://www.tpc.com/harding-park/" target="_blank" rel="noopener">tpc.com/harding-park</a>',
  [("harding-1.jpg", "Sun through cypress trees over the first hole at TPC Harding Park", "First hole, Harding Park &middot; Tinou Bao, CC BY 2.0"),
   ("harding-2.jpg", "A mower in the fog on the ninth hole at TPC Harding Park", "Ninth hole in the fog &middot; Tinou Bao, CC BY 2.0")]),
 ("03", "Presidio Golf Course", "The Presidio, San Francisco &middot; public &middot; 18 holes",
  "I&rsquo;ve always loved the Presidio in general &mdash; the landscape and nature, and how it feels like this hidden place within San Francisco, so far removed from the big city. The golf course really carries that same feeling through.",
  "Eleven. It&rsquo;s a very hard par four, and you really have to hit a good drive to have an approach. Otherwise, you&rsquo;re looking at 180 or 200 yards in.",
  "Carry it over the right edge of the bunkers on the left side of the fairway. If you hit a good drive, you&rsquo;ll get a good roll down to the bottom of the hill.",
  'Public, 18 holes, inside the Presidio. SLOAT holds a monthly round here. <a href="https://www.presidiogolf.com/" target="_blank" rel="noopener">presidiogolf.com</a>',
  [("presidio-1-wide.jpg", "A black and white swing study at Presidio Golf Course", "A study in recovery &middot; Presidio &middot; SLOAT"),
   ("presidio-3-wide.jpg", "Fairways and cypress trees at Presidio Golf Course", "Presidio Golf Course &middot; Daderot, CC0")]),
]
SPECIAL = [
 ("04", "PGA West, Pete Dye Mountain Course", "La Quinta, near Palm Springs &middot; resort &middot; 18 holes",
  "I love getting out of the cold Northern California weather and going down to Palm Springs in the winter. It&rsquo;s such a beautiful course, especially on the back nine when you get up into the little canyons and valleys.",
  None,
  "The greens are raised and slope away, so they&rsquo;re always very fast. Play the distance to the front of the green, not the middle or back, or you&rsquo;ll roll off the back a lot.",
  'Pete Dye designed it; it opened in 1981 and sits against the Santa Rosa Mountains. Resort course; book through PGA West. <a href="https://www.pgawest.com/golf/pete-dye-mountain-course" target="_blank" rel="noopener">pgawest.com</a>',
  [("pgawest-1.jpg", "Palm trees and mountains over a green at PGA West in La Quinta", "PGA West, La Quinta &middot; PGA West")]),
 ("05", "Waiehu Municipal Golf Course", "Wailuku, Maui &middot; county muni &middot; 18 holes",
  "When I go to Maui, I&rsquo;m mostly there to surf, but I golf a little too. I&rsquo;ve played some of the nicer bucket-list courses there, which were great, but I kept coming back to Waiehu. It&rsquo;s super affordable, fun, not very busy, and right against the ocean.",
  None, "Don&rsquo;t go left into the ocean.",
  "Run by Maui County, on the coast just north of Wailuku. Residents pay less than visitors; check the county&rsquo;s current rates before you go.",
  [("waiehu-a.jpg", "A pond and fairway at Waiehu Golf Course with the ocean behind", "Waiehu on the water &middot; Forest and Kim Starr, CC BY 3.0"),
   ("waiehu-b.jpg", "A wide fairway and ironwood trees at Waiehu Golf Course under the West Maui Mountains", "Waiehu &middot; Forest and Kim Starr, CC BY 3.0")]),
]


def photos(ps):
    if not ps:
        return ""
    out = []
    for f, a, c in ps:
        wide = "-wide" in f
        fs = "margin:0"
        ist = ' style="aspect-ratio:5/4"' if wide else ""
        out.append(f'<figure style="{fs}"><img src="{IMG}/{f}" alt="{a}" loading="lazy"{ist} /><figcaption>{c}</figcaption></figure>')
    return '<div class="gg-photos">' + "".join(out) + "</div>"


def course(c, hole_label="The hole we love", tip_label="One tip"):
    n, name, where, why, hole, tip, facts, ps = c
    lead = "Why we play it" if hole else "What makes it special"
    tl = tip_label if hole else "Insider knowledge"
    h = f'<p><span class="gg-lbl">{hole_label}</span>{hole}</p>' if hole else ""
    return (f'<div class="gg-course"><div class="gg-num">{n}</div><div><h3>{name}</h3><div class="gg-where">{where}</div>'
            f'<p><span class="gg-lbl">{lead}</span>{why}</p>{h}<p><span class="gg-lbl">{tl}</span>{tip}</p>'
            f'<div class="gg-facts">{facts}</div></div>{photos(ps)}</div>')


# ---------- AFTER THE ROUND ----------
AFTER = [
 ("Eat", [
   ("La Ciccia", "Noe Valley &middot; Sardinian", "One of my favorite restaurants in San Francisco. It&rsquo;s Sardinian and seafood-focused. A husband-and-wife couple ran it for years and were amazing. They retired and sold it, but it&rsquo;s actually been just as good since they left, which is refreshing."),
   ("El Buen Comer", "Mission Street, Bernal Heights", "Really delicious, authentic Mexican food. My move is the huarache."),
   ("Saigon BBQ Noodle House", "Irving Street, Inner Sunset", "I go for the classic beef pho with raw beef and tendon.")]),
 ("Drink", [
   ("The Coffee Movement", "Washington Street, Chinatown", "Hands down the best espresso in San Francisco."),
   ("Trick Dog", "The Mission", "I&rsquo;m not a big drinker, but they always have really thoughtful non-alcoholic cocktails.")]),
 ("Hang out", [
   ("Home", "First stop", "My first move after a round is usually to go home and shower."),
   ("The course restaurant", "Wherever we played", "I always try to have a drink or a little snack at the golf course&rsquo;s restaurant afterward, just to support it."),
   ("A coffee shop on the way home", "Late morning", "I like early rounds, so ideally I&rsquo;m done around 10:30 or 11. I usually find a good coffee shop on my way home for a black coffee or espresso.")]),
 ("Visit", [
   ("Portugal", "Lisbon to Porto", "We&rsquo;re doing a lot of manufacturing there, and we flew into Lisbon, drove up to Porto and surfed along the way. It&rsquo;s such a beautiful, friendly country, and the climate is almost exactly like the San Francisco area, so you don&rsquo;t need to change what you wear."),
   ("New York", "and Bethpage", "We visited Dan&rsquo;s brother near Boston, played some great courses there, then took a ferry to Long Island and played Bethpage. There are so many amazing golf courses there in the summer."),
   ("Japan", "For the craft", "There&rsquo;s such an amazing history of craftsmanship and food in Japan. It&rsquo;s an incredible place to see what generational skills look like across so many different industries.")]),
]


SP = {'La Ciccia': ('sp-laciccia.jpg', 'The red awnings of La Ciccia in Noe Valley', 'La Ciccia'), 'El Buen Comer': ('sp-elbuencomer.jpg', 'Guisados, rice and beans on the table at El Buen Comer', 'El Buen Comer'), 'Saigon BBQ Noodle House': ('sp-irving.jpg', "Irving Street in San Francisco's Sunset District", 'Irving Street &middot; Goldrock95, CC0'), 'The Coffee Movement': ('sp-coffeemovement.jpg', 'The white espresso bar at The Coffee Movement', 'The Coffee Movement'), 'Trick Dog': ('sp-trickdog.jpg', 'Tables by the window at Trick Dog in the Mission', 'Trick Dog &middot; Christopher Michel, CC BY 2.0'), 'Portugal': ('sp-porto.jpg', "Porto's Ribeira on the Douro River", 'Porto &middot; Jakub Ha&#322;un, CC BY 4.0'), 'New York': ('sp-bethpage.jpg', 'The warning sign at the first tee of Bethpage Black', 'Bethpage Black &middot; E S Lee, CC BY 2.0'), 'Japan': ('sp-japan.jpg', 'Giant knife signs on a kitchen-knife shop on Kappabashi-dori in Tokyo', 'Kappabashi, Tokyo &middot; Photocapy, CC BY-SA 2.0')}


def spimg(n):
    if n not in SP:
        return ""
    f, a, c = SP[n]
    return f'<figure style="margin:0 0 10px"><img src="{IMG}/{f}" alt="{a}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block" /><figcaption class="gg-cap">{c}</figcaption></figure>'


RIMG = {
 "La Ciccia": [("r-lc-1.jpg", "The red awnings of La Ciccia in Noe Valley"), ("r-lc-2.jpg", "A plate of spaghetti at La Ciccia"),
               ("r-lc-3.jpg", "Octopus in a red stew at La Ciccia"), ("r-lc-4.jpg", "Plates of Sardinian food on a set table at La Ciccia")],
 "El Buen Comer": [("r-ebc-1.jpg", "The red front of El Buen Comer on Mission Street"), ("r-ebc-2.jpg", "Guisados, rice and beans on the table at El Buen Comer"),
                   ("r-ebc-3.jpg", "A plate with green salsa, rice and beans at El Buen Comer"), ("r-ebc-4.jpg", "Tostadas and white wine at El Buen Comer")],
 "Saigon BBQ Noodle House": [("r-sg-a.jpg", "Sweet and sour shrimp soup with basil and pineapple at Saigon BBQ Noodle House"),
                             ("r-sg-b.jpg", "A bowl of egg noodle soup with bok choy and a plate of pickles and jalape\u00f1os at Saigon BBQ Noodle House"),
                             ("r-sg-c.jpg", "Braised pork and eggs in a clay pot at Saigon BBQ Noodle House")],
 "The Coffee Movement": [("r-tcm-b.jpg", "A customer drinking coffee outside The Coffee Movement at 1030 Washington Street"), ("r-tcm-a.jpg", "A flight of espresso drinks on the counter at The Coffee Movement"),
                         ("r-tcm-1.jpg", "The white espresso bar at The Coffee Movement")],
 "Trick Dog": [("r-td-a.jpg", "Pendant lamps glowing over the bar at Trick Dog"), ("r-td-b.jpg", "A full bar at Trick Dog in black and white"),
               ("r-td-c.jpg", "A table under the big factory windows at Trick Dog"), ("r-td-d.jpg", "Red chairs and set tables by the window at Trick Dog")],
}
RCRED = {"La Ciccia": "Photos: La Ciccia", "El Buen Comer": "Photos: El Buen Comer", "Saigon BBQ Noodle House": "Photos: Saigon BBQ Noodle House (@saigonbbqinc)",
         "The Coffee Movement": "Photos: The Coffee Movement (@thecoffeemovementsf)", "Trick Dog": "Trick Dog &middot; Christopher Michel, CC BY 2.0"}


def after():
    rows = []
    for h in ("Eat", "Drink"):
        for n, w, t in dict(AFTER)[h]:
            imgs = RIMG.get(n, [])
            g = "".join(f'<img src="{IMG}/{f}" alt="{a}" loading="lazy" />' for f, a in imgs)
            rows.append(f'<div class="gg-rest"><div class="gg-rt"><span class="gg-kind">{h}</span><b>{n}</b><span class="w">{w}</span>'
                        f'<span class="t">&ldquo;{t}&rdquo;</span><span class="gg-cap">{RCRED.get(n, "")}</span></div>'
                        f'<div class="gg-rimgs" data-n="{len(imgs)}">{g}</div></div>')
    ho = "".join(f'<div class="gg-spot"><b>{n}</b><span class="w">{w}</span><span class="t">{t}</span></div>' for n, w, t in dict(AFTER)["Hang out"])
    vi = "".join(f'<div class="gg-spot">{spimg(n)}<b>{n}</b><span class="w">{w}</span><span class="t">{t}</span></div>' for n, w, t in dict(AFTER)["Visit"])
    return ('<div class="gg-rests">' + "".join(rows) + '</div>'
            '<div class="gg-col" style="margin-top:30px"><h3>Hang out</h3><div class="gg-cols" style="margin-top:0">' + ho + '</div></div>'
            '<div class="gg-col" style="margin-top:30px"><h3>Visit</h3><div class="gg-cols" style="margin-top:0">' + vi + '</div></div>')


# ---------- INTERVIEW ----------
IV = [
 ("Just for SLOAT", [
  ("SLOAT is named for Sloat Boulevard, which runs past the city&rsquo;s courses to Ocean Beach. What does a golf day along it look like?",
   ["Within a two- or three-mile radius of Sloat Boulevard, you can play at some of the most exclusive private clubs in the country or some of the best public courses in California. The experiences couldn&rsquo;t be more different, but the through line is the climate.",
    "You can encounter wind, fog, warmth, cold, wet, and dry conditions, sometimes within the same 18 holes. The clubs themselves are incredibly varied, but the weather is every bit as dynamic. That&rsquo;s part of what makes golf in this little corner of San Francisco so interesting."], None),
  ("You both surf and play. On a good morning, how do you fit in both, and which one wins when you can&rsquo;t?",
   ["That&rsquo;s the holy grail, isn&rsquo;t it? Ideally, you tee off at 6 or 6:30 in the morning, squeeze in a three-and-a-half-hour round, and still make it to Ocean Beach before the wind turns on and blows out the surf.",
    "As for which one wins when you can&rsquo;t do both, I think Teague and I might have different answers. For me, surfing still wins ten times out of ten. I&rsquo;ll let Teague speak for himself."], "Dan"),
  ("Your founders&rsquo; letter says most golf apparel is built around a version of the game neither of you found interesting. What&rsquo;s the version you do find interesting?",
   ["The version of golf I find interesting is less about performance and more about the social side of the game. I&rsquo;ve always thought of golf a bit like running marathons. As an amateur, I&rsquo;m never going to win the race, but I can always try to do better than I did previously.",
    "A lot of what appeals to me is the camaraderie with other players, getting out in nature, the rules and history of the game, and having this framework to meet people you might never have met otherwise and have a great time."], None),
  ("How do the fog and wind out in the Outerlands change a round, and how did it shape what you make?",
   ["First, we wanted to make clothes that actually work where we play golf. Second, we wanted them to have an aesthetic that didn&rsquo;t necessarily announce to the world that you&rsquo;d just been golfing.",
    "The fog and wind out here are very real. Anyone who&rsquo;s played enough golf in San Francisco has experienced a round where visibility drops to 30 or 40 feet, or where you&rsquo;re playing in 30-mile-an-hour winds.",
    "We wanted to make clothes that could handle all of that without looking like conventional technical golf apparel."], None),
  ("You launched with a party at Golden Gate Park Golf Course. Why there?",
   ["It&rsquo;s arguably one of the best nine-hole courses in the country. It was renovated a couple of years ago and is now an incredibly fun little track.",
    "It sits at the western edge of Golden Gate Park, practically on Ocean Beach, and the people who work there are awesome. Given that it&rsquo;s just down the street from Sloat Boulevard, it felt like the perfect symbol of the brand and what we&rsquo;re trying to build."], None),
  ("Teague, what has running a kitchen taught you that shows up in how you make clothes, or how you play?",
   ["The biggest thing that&rsquo;s carried over from running kitchens to SLOAT and golf is how foundational systems are. You don&rsquo;t start out operating at a two- or three-star restaurant level, or as a scratch golfer. You get there over time by coming in every day and trying to be a little better than you were the day before. Those small gains in quality and skill add up if you keep at it."], None),
  ("Dan, after nearly 20 years in apparel, what did you decide SLOAT would never do?",
   ["I&rsquo;ve always thought it would be interesting to build a brand within a very specific set of constraints. Constraints force focus and discipline, but I also think they can be an incredible engine for innovation.",
    "For us, the hard-and-fast rule is that we won&rsquo;t use synthetic fabrics. At the same time, we want to make extraordinarily high-performing apparel. Reconciling those two ambitions gives us a pretty interesting mandate to work within, and I think it ultimately pushes us to make better things."], None),
  ("Golden Gate Park, Lincoln Park, Sharp Park, the Presidio: which one do you send a visiting friend to first?",
   ["Probably the Presidio. Visiting friends usually want to play 18, and it&rsquo;s an awesome course with some special San Francisco scenery. All four are great and offer very different experiences, but I find myself recommending the Presidio most often."], None),
 ]),
 ("The game and you", [
  ("How did you get hooked on golf?",
   ["I grew up near a golf course, and from about age seven I spent almost every summer day there. I&rsquo;d take the bus over in the morning, hit balls, play nine holes, and eventually work my way up to playing 36 holes a day.",
    "The best part was the friendships. At seven or eight, I was hanging out with kids who were 11 or 12, which felt like the coolest thing in the world. We spent entire summers playing golf, drinking Coke, eating French fries, and generally having the time of our lives. That&rsquo;s what got me hooked."], None),
  ("How many times have you quit golf, and what pulled you back?",
   ["Just once. I stopped playing when I was about 16 or 17, partly because I was starting to suspect that being a really good golfer wasn&rsquo;t particularly impressive to girls. I also skateboarded and snowboarded, which seemed like a better use of my time from a social standpoint.",
    "I didn&rsquo;t pick up the game again until 2025, when Teague dragged me back out. So I took a very legitimate 27-year break. Turns out I still love it."], "Dan"),
  ("What&rsquo;s the best shot you&rsquo;ve ever hit, and did anyone see it?",
   ["The one that sticks with me came at the Old Course at Half Moon Bay, after I got back into golf. I was playing a match against my brother, who was four strokes up on me.",
    "We were on the 15th, a long par five with water running down the left side and the wind in our faces. I was about 250 yards into the green and pulled out my three-wood. My natural shot is a fade, so I aimed out over the water, flushed it, and watched it fade back onto the green to about 15 feet.",
    "I missed the eagle putt but made a birdie. My brother made a triple, and suddenly the match was even. I ended up losing the match, but whatever."], None),
  ("What golf superstition or habit can&rsquo;t you shake?",
   ["I think the problem with quitting golf at 16 and picking it back up at 43 is that my approach to course management is still firmly rooted in the mind of a 16-year-old.",
    "Given a choice between logic, common sense and sound course management on one hand and the chance of pulling off something heroic on the other, I&rsquo;ll choose the hero shot every time. It fails 99 times out of 100."], "Dan"),
  ("What&rsquo;s the round you still tell people about?",
   ["The first time I broke 80. I shot a 79, but I had two eagles, three birdies, a bunch of doubles, and a couple of triples. I always joke that the other times I&rsquo;ve broken 80, it&rsquo;s been by making a bunch of pars and bogeys. That feels like a much more sustainable way to do it than relying on eagles and birdies."], None),
  ("What&rsquo;s your most embarrassing moment on a course?",
   ["Anytime I&rsquo;m playing with Teague, I&rsquo;m generally embarrassed by my association with him."], None),
 ]),
 ("Your people", [
  ("Who&rsquo;s in your regular group?",
   ["It&rsquo;s a mix of friends from different parts of my life. Any friend of mine who plays golf, I&rsquo;ll play with. And through golf, you inevitably end up making new friends. It&rsquo;s just this great hodgepodge of guys who all happen to love this weird little game."], None),
  ("Who made you feel like you belonged in golf?",
   ["When I was a kid, it was the older boys I played with. When you&rsquo;re 11 and hanging around with 13- or 14-year-olds, they&rsquo;re definitely going to make fun of you, but there&rsquo;s also this big-brother dynamic where they take you under their wing.",
    "There&rsquo;s a camaraderie to the game that makes you feel like you&rsquo;re part of something, even when you&rsquo;re getting relentlessly teased."], None),
  ("What has golf taught you that works off the course too?",
   ["Nobody cares. And I mean that in the best possible way. Nobody cares if you shot 73. Nobody cares if you shot 103. Straight up, nobody cares.",
    "Just do you, enjoy yourself, and stop worrying so much about what everyone else thinks."], None),
  ("What would make someone who&rsquo;s never played feel at home on your course?",
   ["Follow the basic rules, be chill, and don&rsquo;t be a jerk. That&rsquo;s pretty much it."], None),
 ]),
 ("Your style", [
  ("Whose golf style do you borrow from?",
   ["I don&rsquo;t really look to golf for style inspiration. We&rsquo;re much more interested in clothes that work on the golf course but don&rsquo;t necessarily look like golf clothes.",
    "Ideally, you can walk off the 18th green and go about the rest of your day without looking like you just played 18 holes."], None),
  ("What&rsquo;s the worst outfit you&rsquo;ve ever worn on a course?",
   ["When I came back to golf in 2025, I needed some golf clothes, so I went into a local pro shop and did the best I could with what was available.",
    "I came home with a full polyester performance outfit, and I remember showing my wife, who looked at me with a combination of shock and horror. She wanted to know what had happened to me. It was one of the early arguments for starting SLOAT."], None),
  ("What&rsquo;s the first piece of golf gear you bought with your own money?",
   ["I saved up for a Scotty Cameron putter when I was about 15. My dad agreed to pay for half, and I covered the rest. At the time, it was the coolest thing I&rsquo;d ever owned."], None),
  ("Besides clubs, what three things do you never play without?",
   ["An apple, trail mix, and a bottle of water."], None),
 ]),
 ("Your brand", [
  ("When did a stranger first ask about something you made?",
   ["We had some graphic hoodies made early on, and our friend Lee, who designed our logo, absolutely smashed it. We started getting a lot of people coming up and asking what SLOAT was.",
    "It was pretty cool to see people take an interest in something we&rsquo;d created before they even knew what it was."], None),
  ("How does an idea turn into a finished piece?",
   ["It starts with a simple question: what problem are we trying to solve? From there, we think about what the product should be, what it might look like, and how it needs to function.",
    "Then comes the technical design, sourcing fabrics, working with mills and factories, developing colors, reviewing lab dips, and going through multiple rounds of sampling and revisions until we feel like we&rsquo;ve nailed the fit, proportions, and details.",
    "The funny thing is, you can start with an idea as simple as &ldquo;let&rsquo;s make a vest,&rdquo; but between that initial thought and the finished garment, there are probably a thousand little decisions to make."], None),
  ("What&rsquo;s the piece you&rsquo;re proudest of?",
   ["I&rsquo;m most stoked on our use of Ventile cotton. It&rsquo;s this extraordinary fabric that, for whatever reason, fell out of favor over the years, and we think that&rsquo;s a real shame. Our Ventile outerwear is the best expression of what we&rsquo;re trying to do with SLOAT.",
    "We want these pieces to be treated as heirlooms. If someone buys one of our jackets, vests, or wind shirts, we want them to hold on to it forever.",
    "And as romantic as it sounds, I love the idea that one day some kid might inherit his dad&rsquo;s old golf jacket. That it becomes something he treasures, not just because it&rsquo;s a great piece of clothing, but because it reminds him of his dad and of a relationship forged through golf."], None),
  ("How do you want someone to feel when they put on something you made?",
   ["We want them to feel like they got incredible value for their money, that they look really, really good, and that they&rsquo;re about to go out and shoot a personal best."], None),
  ("What&rsquo;s one thing you&rsquo;d like to try making?",
   ["Shoes. We&rsquo;ve already spent a lot of time on footwear, about as much as on some of the clothes we&rsquo;ve brought to market.",
    "We&rsquo;ve got some pretty incredible prototypes sitting in our office, but we put the project on hold for a few reasons. I stare at those samples almost every day, wondering when we&rsquo;ll have the time and capacity to pick the project back up."], None),
  ("What do you hope golf looks like in ten years?",
   ["I hope it&rsquo;s even more diverse than it is today, in every sense of the word. At the same time, I hope there&rsquo;s a renewed appreciation for the traditions and etiquette of the game.",
    "Most importantly, I hope we return to a world where every sprinkler head has a yardage marker. Frankly, I think there should be a federal law mandating it."], None),
 ]),
]


IVB = {
 "Just for SLOAT": [("b-lincoln.jpg", "The Golden Gate Bridge seen across Lincoln Park Golf Course", "Lincoln Park &middot; David Ohmer, CC BY 2.0"),
                    ("b-sharp.jpg", "Sharp Park Golf Course in Pacifica at golden hour", "Sharp Park &middot; CarmenEsparzaAmoux, CC BY-SA 4.0"),
                    ("b-cypress.jpg", "Cypress trunks over the Pacific", "The Outerlands &middot; SLOAT")],
 "The game and you": [("b-swing.jpg", "A golfer's swing in silhouette against a pale sky", "Merino Polo &middot; SLOAT"),
                      ("b-hoodie.jpg", "A golfer in a black hoodie and six-panel hat on a coastal course", "Coastal round &middot; SLOAT"),
                      ("b-hmb.jpg", "Half Moon Bay's coastal fairways above the beach", "Half Moon Bay &middot; Cornellrockey, CC BY-SA 4.0")],
 "Your people": [("b-wave2.jpg", "A green wave curling under a rainbow", "Before the wind turns on &middot; SLOAT Journal"),
                 ("w-umbrella.jpg", "A lone figure with an umbrella crossing a green hillside", "Fog days &middot; SLOAT Journal"),
                 ("w-board.jpg", "Ocean Beach and the Outer Sunset seen from above", "The Outer Sunset &middot; SLOAT")],
 "Your style": [("b-vest.jpg", "SLOAT fleece hoodies hanging on a rail", "Fleece hoodies &middot; SLOAT"),
                ("w-qz.jpg", "A teal SLOAT fleece quarter zip laid on wood", "Fleece quarter zip &middot; SLOAT Journal"),
                ("b-green.jpg", "A golfer standing on a green in black and white", "On the green &middot; SLOAT")],
}


def band(items):
    return '<div class="gg-band">' + "".join(f'<figure style="margin:0"><img src="{IMG}/{s_}" alt="{a}" loading="lazy" /><figcaption>{c}</figcaption></figure>' for s_, a, c in items) + "</div>"


def interview():
    out = []
    for grp, qs in IV:
        out.append(f"<h3>{grp}</h3>")
        for q, a, who in qs:
            w = f' <span class="gg-who">&middot; {who}</span>' if who else ""
            out.append(f'<div class="gg-q">{q}{w}</div><div class="gg-a">' + "".join(f"<p>{p}</p>" for p in a) + "</div>")
        if grp in IVB:
            out.append(band(IVB[grp]))
    return '<div class="gg-iv">' + "".join(out) + "</div>"


# ---------- FAVORITE PIECES ----------
PIECES = [
 ("mens-golf-quarter-zip", "Organic Cotton Fleece Quarter Zip", "$225", "I wear it most often. It&rsquo;s super comfortable and nice to golf in, but also great to throw on for a workday."),
 ("mens-ventile-windbreaker", "Organic Ventile&reg; Jacket", "$595", "My go-to outerwear piece. It&rsquo;s thin, easy to wear, keeps the cold and wind off, and packs away in my backpack when I get too warm."),
 ("mens-merino-wool-golf-polo", "Merino Polo", "$215", "My favorite polo to golf in. It keeps you warm in winter, breathes really well when it&rsquo;s warm, and it&rsquo;s naturally antimicrobial so it doesn&rsquo;t get stinky."),
 ("organic-cotton-caddie-pant", "Organic Cotton Caddie Pant", "$195", "My go-to for a nice, comfortable pair of pants, either for golf or for a weekend."),
 ("organic-cotton-six-panel-hat", "Organic Cotton Six Panel Hat", "$65", "Always got to wear a SLOAT hat."),
]


def piece(h, name, price, why):
    fr = FR[h]
    label = esc_attr(f"SLOAT {name}")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{label} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    nav = (f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
           f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>')
    return (f'<div class="product-card" id="p-{h}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>{nav}</div>'
            f'<div class="product-body"><div class="product-brand">SLOAT</div><div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">&ldquo;{why}&rdquo;</div><a href="https://sloat.cc/products/{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


WORLD = [("w-surf.jpg", "A surfer on a big wave in black and white", "Ocean Beach energy &middot; SLOAT Journal"),
         ("w-fleece.jpg", "A golfer in a blue SLOAT fleece holding a driver against a blue sky", "Fleece &middot; SLOAT Journal"),
         ("w-cypress.jpg", "A lone golfer on a foggy fairway at Sharp Park", "Sharp Park in the fog &middot; SLOAT"),
         ("w-ventile.jpg", "The Ventile label inside a SLOAT jacket", "Ventile label &middot; SLOAT"),
         ("w-road.jpg", "A golfer putting at Half Moon Bay in the evening haze", "Half Moon Bay &middot; SLOAT"),
         ("w-rail.jpg", "Three SLOAT Ventile vests hanging on a rail", "Ventile vests &middot; SLOAT")]


def world():
    figs = "".join(f'<figure><img src="{IMG}/{s}" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for s, a, c in WORLD)
    return f'<div class="ig-grid" style="margin-top:18px">{figs}</div>'


HITS = [("Handicap", "Around 6.6"), ("Walk or ride", "Walk. Ten times out of ten."),
        ("Club you&rsquo;d keep", "Mizuno irons. &ldquo;I don&rsquo;t think anyone does it better.&rdquo;"),
        ("Dream course", "Shaughnessy in Vancouver, with his dad and brothers"),
        ("Post-round order", "Chicken tenders and fries, or a club sandwich"), ("One word for your swing", "Don&rsquo;t ask."),
        ("One word for your crew", "Chill."), ("On the speaker", "Nothing. &ldquo;Music sounds best, and beer tastes best after a round.&rdquo;")]

RELATED = [
 ("/drops/brand-to-know-sloat", "Brand to Know: SLOAT", "Our profile of the brand, the Ventile and the factories."),
 ("/drops/favorite-golf-fabrics-2026-cordura-dyneema-organic-cotton", "Our Favorite Fabrics of 2026", "Why Ventile closes itself in the rain."),
 ("/field-guide", "The Austin Field Guide", "The format SLOAT borrowed: our own city, course by course."),
]


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-25", "dateModified": "2026-11-25",
         "author": [{"@type": "Person", "name": "Dan Fibiger"}, {"@type": "Person", "name": "Teague Moriarty"}],
         "editor": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "about": {"@type": "Place", "name": "San Francisco, California"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Guide", "item": "https://thegrassyissue.com/field-guide"},
            {"@type": "ListItem", "position": 3, "name": "Guest Field Guide No. 01: San Francisco", "item": URL}]},
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
    head_rest = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\s*', "", head_rest, flags=re.S)
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    rel = "".join(f'<li style="padding:10px 0;border-bottom:.5px solid rgba(20,20,20,.2)"><a href="{u}">{t}</a> &mdash; {d_}</li>' for u, t, d_ in RELATED)
    hits = "".join(f'<div class="gg-hit"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in HITS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/field-guide">Field Guide</a><span>/</span>
  Guest Field Guide No. 01</div>

<header class="drop-header">
  <div class="gg-kick">Guest Field Guide No. 01 &middot; San Francisco &middot; with SLOAT</div>
  <h1>{H1}</h1>
  <p class="gg-dek">&ldquo;Some of the best and most varied golf in the country, with legendary private clubs, incredible public courses, and weather that can humble anyone.&rdquo;</p>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 25, 2026</p><!--/TGI-BY-->
  <div class="drop-meta">
    <span>Guides: Dan Fibiger &amp; Teague Moriarty</span><span class="dot"></span>
    <span>5 courses &middot; 11 spots &middot; 1 interview</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A surfer with a board at the end of a coastal path into the fog" fetchpriority="high" /></div></div>

<section class="products" style="margin-top:8px;">
  <div class="writeup-body" style="max-width:760px">
    <div class="drop-tag grass">The Idea</div>
    <p><strong>We handed our Field Guide to the people who make the clothes.</strong> Each Guest Field Guide is a city told by the founders of an independent golf brand: the courses they play, where they eat after, what they wear, and an interview about the game. They write it; we edit, check the facts and lay it out. No one paid for this.</p>
    <p><strong>No. 01 is San Francisco, by SLOAT.</strong> SLOAT is named for Sloat Boulevard, which runs west past some of the city&rsquo;s best courses and ends at Ocean Beach. Dan Fibiger and Teague Moriarty founded it in 2026 with one rule: no synthetic fabrics. Both of them surf, and both of them play. Their words below are their own, trimmed for length.</p>
  </div>
  <div class="gg-guides" style="margin-top:34px">
    <div class="gg-two"><figure style="margin:0"><img src="{IMG}/guide-dan.jpg" alt="SLOAT co-founder Dan Fibiger on the course at Sharp Park" loading="lazy" /><div class="cap">Dan Fibiger &middot; Sharp Park &middot; SLOAT</div></figure>
    <figure style="margin:0"><img src="{IMG}/guide-teague.jpg" alt="SLOAT co-founder Teague Moriarty gripping a club at the Presidio" loading="lazy" /><div class="cap">Teague Moriarty &middot; the Presidio &middot; SLOAT</div></figure></div>
    <div>
      <div class="drop-tag grass">Your Guides</div>
      <h3>Dan Fibiger &amp; Teague Moriarty, SLOAT</h3>
      <p style="font-size:16.5px;line-height:1.7;margin:0 0 10px">&ldquo;We&rsquo;re the founders of SLOAT, a San Francisco-based golf apparel brand endeavoring to make the future heirlooms of golf. Clothes you&rsquo;ll want to keep forever.&rdquo;</p>
      <p style="font-size:15px;line-height:1.65;opacity:.8;margin:0">Dan spent nearly 20 years in the human rights and environmental side of the apparel industry. Teague spent much of his career as a chef and is an owner of Sons &amp; Daughters and Kiln, two Michelin-starred restaurants in San Francisco. <a href="https://www.instagram.com/sloat.cc/" target="_blank" rel="noopener">@sloat.cc</a> &middot; <a href="https://sloat.cc/" target="_blank" rel="noopener">sloat.cc</a></p>
    </div>
  </div>
  <figure class="gg-wide"><img src="{IMG}/founders-lisbon.jpg" alt="SLOAT&rsquo;s two co-founders walking up a cobbled street in Lisbon" loading="lazy" /><figcaption>The founders in Portugal, from SLOAT&rsquo;s founders&rsquo; letter &middot; SLOAT</figcaption></figure>
</section>
"""
    body += pq("You can encounter wind, fog, warmth, cold, wet, and dry conditions, sometimes within the same 18 holes.", "Dan Fibiger &amp; Teague Moriarty, SLOAT")
    body += section("Quick Hits", "Dan, in One Line Each", "quick-hits", f'<div class="gg-hits">{hits}</div>')
    body += section("Where We Play", "Three Rounds We Play All the Time", "every-week",
                    '<div class="gg-wrap">' + "".join(course(c) for c in COURSES) + "</div>",
                    "<strong>Every week.</strong> Two public courses in the city and one just south of it. Notes in mono are ours, checked November 25, 2026.")
    body += section("Where We Play", "Two Rounds We Travel For", "special-days",
                    '<div class="gg-wrap">' + "".join(course(c) for c in SPECIAL) + "</div>",
                    "<strong>Special days.</strong> The rounds they save up for, both a flight away.")
    body += pq("Nobody cares if you shot 73. Nobody cares if you shot 103. Straight up, nobody cares.", "SLOAT")
    body += section("After the Round", "Where We Eat, Drink and Go", "after",
                    after() + '<div class="gg-split"><div><div class="drop-tag grass">A Perfect Day</div>'
                    '<p class="gg-day">&ldquo;An early morning round of golf, followed by a surf at Ocean Beach, then a burrito somewhere in the Outer Sunset or a bowl of pho in the Inner Sunset. Pick up my kids from school, hang out with them for the afternoon, then take my wife out for dinner at Mission Chinese and finish with a drink at the Royal Cuckoo.&rdquo;</p>'
                    '<p class="gg-day" style="margin-top:14px;font-size:17px;opacity:.75">And the best tee time: &ldquo;6:30 a.m. The course is wet, the air is chilly, and you can just start to see slivers of sunlight breaking over the eastern horizon.&rdquo;</p></div>'
                    + band([("ob-1.jpg", "The Cliff House above Ocean Beach at sunset", "Ocean Beach &middot; Brocken Inaglory, CC BY-SA 3.0"),
                            ("ob-2.jpg", "Waves and a shorebird at Ocean Beach in black and white", "Ocean Beach &middot; Brocken Inaglory, CC BY-SA 3.0")]) + '</div>')
    body += section("Golden Gate Park Golf Course", "Where SLOAT Launched", "ggp",
                    '<div class="gg-split" style="margin-top:6px"><div class="writeup-body" style="max-width:560px;margin:0!important">'
                    '<p><strong>Nine holes by Ocean Beach.</strong> SLOAT went live on August 28, 2026, with a party at Golden Gate Park Golf Course.</p>'
                    '<p class="gg-day" style="margin:0">&ldquo;It&rsquo;s arguably one of the best nine-hole courses in the country. It sits at the western edge of Golden Gate Park, practically on Ocean Beach, and the people who work there are awesome.&rdquo;</p></div>'
                    '<div class="gg-band" style="grid-template-columns:repeat(2,minmax(0,1fr))">'
                    f'<figure style="margin:0"><img src="{IMG}/ggp-1.jpg" alt="A SLOAT pin flag at Golden Gate Park Golf Course on launch day" loading="lazy" /><figcaption>Launch day &middot; SLOAT</figcaption></figure>'
                    f'<figure style="margin:0"><img src="{IMG}/ggp-2.jpg" alt="An afternoon at Golden Gate Park Golf Course" loading="lazy" /><figcaption>An afternoon at Golden Gate Park &middot; SLOAT</figcaption></figure></div></div>')
    body += section("In Your Words", "The Interview", "interview", interview(),
                    "<strong>Answers from Dan and Teague.</strong> Where one founder is speaking, we say so.")
    body += pq("I love the idea that one day some kid might inherit his dad&rsquo;s old golf jacket.", "SLOAT, on its Ventile outerwear")
    body += section("Favorite Pieces", "What They Wear Here", "pieces",
                    '<div class="products-grid" data-n="5">' + "\n".join(piece(*p) for p in PIECES) + "</div>",
                    "<strong>In their words.</strong> SLOAT only uses natural fibers. Prices in USD from sloat.cc, checked November 25, 2026.")
    body += section("The Bag and the Go-To", "What&rsquo;s in the Bag", "bag",
                    '<div class="gg-split" style="margin-top:6px"><div class="writeup-body" style="max-width:600px;margin:0!important"><p><strong>The bag.</strong> &ldquo;Titleist Pro V1 balls, Callaway woods with ATTOMAX shafts (shoutout to the team at ATTOMAX), and Mizuno irons.&rdquo;</p>'
                    '<p><strong>The go-to.</strong> &ldquo;Our SLOAT Merino Polo. It&rsquo;s incredibly comfortable, looks dope, and works pretty much everywhere. On the course, off the course, wherever.&rdquo;</p></div>'
                    + '<div class="gg-band">' + "".join(f'<figure style="margin:0"><img src="{f}" alt="SLOAT Merino Polo" loading="lazy" /><figcaption>Merino Polo &middot; SLOAT</figcaption></figure>' for f in FR["mens-merino-wool-golf-polo"][:2]) + '</div></div>')
    body += section("SLOAT in the World", "From the Journal", "world", world(),
                    "<strong>SLOAT Journal, Edition 001.</strong> Pictures from the brand&rsquo;s first printed magazine, Fall/Winter 2026.")
    body += f"""
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">Come Play</div>
    <h2 class="products-hdr" id="come-play">The Monthly SLOAT Round</h2>
    <p>SLOAT holds a round at the Presidio every month. We asked what it should feel like for someone who shows up alone: &ldquo;I want it to feel like a fun, casual round where you get to meet some new people who are into the same things as you.&rdquo; Watch <a href="https://www.instagram.com/sloat.cc/" target="_blank" rel="noopener">@sloat.cc</a> for dates.</p>
    <p>If you run a small golf brand and want to write a guide to your city, <a href="/work-with-us">tell us</a>. If we got a detail wrong, tell us that too.</p>
    <p class="gg-facts" style="margin-top:18px">Photos: SLOAT and SLOAT Journal, Edition 001; PGA West. Course photos via Wikimedia Commons: Harding Park by <a href="https://commons.wikimedia.org/wiki/File:TPC_Harding_Park_-_First_Hole_(15332653189).jpg" target="_blank" rel="noopener">Tinou Bao</a> (<a href="https://creativecommons.org/licenses/by/2.0/" target="_blank" rel="noopener">CC BY 2.0</a>); Presidio by <a href="https://commons.wikimedia.org/wiki/File:Presidio_Golf_Course_-_San_Francisco,_CA.jpg" target="_blank" rel="noopener">Daderot</a> (CC0); Waiehu by <a href="https://commons.wikimedia.org/wiki/File:Starr-170328-0640-Cocos_nucifera-golfer_teeing_off-Waiehu_Golf_Course-Maui_(33978419031).jpg" target="_blank" rel="noopener">Forest and Kim Starr</a> (<a href="https://creativecommons.org/licenses/by/3.0/us/" target="_blank" rel="noopener">CC BY 3.0 US</a>); Lincoln Park by David Ohmer (CC BY 2.0); Sharp Park by CarmenEsparzaAmoux (CC BY-SA 4.0); Half Moon Bay by Cornellrockey (CC BY-SA 4.0); Crystal Springs by Kglavin (CC BY 2.5) and Pi.1415926535 (CC BY-SA 3.0); Trick Dog by Christopher Michel (CC BY 2.0); Porto by Jakub Ha&#322;un (CC BY 4.0); Bethpage by E S Lee (CC BY 2.0); Kappabashi by Photocapy (CC BY-SA 2.0); all via Wikimedia Commons. Venue photos from La Ciccia, El Buen Comer and The Coffee Movement. Ocean Beach by <a href="https://commons.wikimedia.org/wiki/File:Cliff_House_from_Ocean_Beach.jpg" target="_blank" rel="noopener">Brocken Inaglory</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC BY-SA 3.0</a>). Cropped.</p>
    <div class="drop-tag grass" style="margin-top:34px">More Like This</div>
    <ul style="list-style:none;padding:0;margin:10px 0 0;font-size:17px">{rel}</ul>
  </div>
</section>
"""
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Manors"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(r'src="(/images/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html")


if __name__ == "__main__":
    main("--apply" in sys.argv)
