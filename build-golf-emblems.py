#!/usr/bin/env python3
"""build-golf-emblems.py — Our 12 Favorite Golf Brand Emblems, 23 November 2026.
Lenny: "post of our 12 favorite golf brand logos" -> "Think more like Walker golfs Kookaburra or Three Putts Cow, and let's
also give the story behind the emblem if possible" -> "Hidden links is a great one" -> "Move Radry up to top 5" -> "build the post".
Lenny didn't send a final 12, so the 12 (then 14: Rhoback/Swannies/Dim Sum dropped for Jain + Matchstick, Lenny 23 Nov) are the strongest emblem + sourced-story pairs from the options sheet
(../logo-options.html), Radry in the top five, plus a three-course bonus (Lahinch, Pinehurst, Del Monte).
FACTS: every story line is from the brand's own site, a founder interview, or TGI's own earlier reporting
(research/logos/). Where nobody has published the story we say so. No prices (nothing to go stale). No FAQ.
Images: each brand's own site, framed on stone (research/logos/prep.py).
"""
import html as H
import json
import pathlib
import re
import sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
SLUG = "golf-brand-emblems-and-the-stories-behind-them"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/golf-emblems"
TITLE = "Our 14 Favorite Golf Brand Emblems, and the Stories Behind Them"
DESC = ("A kookaburra on a club, a cow carrying a golf bag, a goat caddie and a face with one round eye and one square: "
        "the 14 golf brand emblems we like best, from Walker, Three Putt, Eastside, Radry and more, and where each one came from.")
H1 = "Our 14 Favorite Golf Brand Emblems"
DEK = "A kookaburra, a cow caddie, a goat and a face that keeps score. The characters on our favorite golf brands, and where they came from."

# key: (emblem name, brand, place, site, [images], story paragraphs, (quote, who) or None, source line, TGI link or None)
E = [
 ("walker", "The Kooka", "Walker Golf Things", "Australia", "https://www.walkergolfthings.com/",
  [("walker-2.jpg", "Walker's Dancing Kooka leather driver cover, kookaburras stitched in gold on black"),
   ("walker-1.jpg", "A golfer in a Walker cap and white tee with the Kooka embroidered at the chest")],
  ["A kookaburra perched on top of a golf club. Walker was started by Jack Fardell, the Australian pro skater, and the bird is two things at once: about as Australian a symbol as there is, and his own family&rsquo;s emblem.",
   "It has been on every Walker drop since the first. Sometimes it sits small on a sleeve, sometimes it dances across a whole leather headcover, and the core line, Kooka Classics, is named for it."],
  None, "Walker Golf Things", "/drops/walker-golf-the-par-tec-drop"),
 ("threeputt", "The Cow Caddie", "Three Putt Golf Clothing", "Horsforth, West Yorkshire", "https://threeputtgolfclothing.co.uk/",
  [("threeputt-1.jpg", "Three Putt's cow caddie: a dairy cow on two legs with a golf bag over its shoulder"),
   ("threeputt-2.jpg", "A navy Three Putt polo sweatshirt with the cow caddie at the chest")],
  ["A dairy cow standing on two legs with a golf bag slung over its shoulder. Founder Graeme Whiles first played golf at eight, in one of his grandad&rsquo;s fields, and the cow is the brand&rsquo;s way of pointing back to it.",
   "It is the most honest origin story on this list. No country club, no heritage crest. A field, a farmer and his grandson."],
  ("Three Putt started in a field. &hellip; No ego. No pretense. No elitism. Just a farmer and his grandson making memories.", "Three Putt&rsquo;s About page"),
  "Three Putt&rsquo;s own About page and product copy", "/drops/uk-independent-golf-brands"),
 ("eastside", "The Swingman", "Eastside Golf", "United States", "https://eastsidegolf.com/",
  [("eastside-1.jpg", "Eastside Golf's Swingman logo: a golfer in jeans and a chain, mid-swing"),
   ("eastside-2.jpg", "A washed black Eastside Golf dad cap with the Swingman embroidered on the front")],
  ["A golfer at the top of his swing in jeans, a sweatshirt and a chain. Eastside&rsquo;s own blog says it was built from two photos of co-founder Olajuwon Ajanaku: one of him as a kid swinging a club, one of him as an adult in a gold chain.",
   "It started as a drawing for his own golf bag. People kept asking about it, co-founder Earl Cooper pushed him to put it on T-shirts, and he wore them around downtown Detroit before there was a brand at all."],
  ("If sponsors keep telling me no, I&rsquo;ll create my own brand and sponsor myself.", "Olajuwon Ajanaku, on Eastside&rsquo;s blog"),
  "Eastside&rsquo;s blog post on the Swingman&rsquo;s origins", "/drops/fall-drops-eastside-students-devereux"),
 ("radry", "The Birdie-Bogey Face", "Radry Golf", "Sheboygan, Wisconsin", "https://radry.com/",
  [("radry-1.jpg", "A Radry rubber keychain with the face logo: one round eye, one square eye and a wave for a mouth"),
   ("radry-2.jpg", "A black Radry zip hoodie with the face embroidered small at the chest")],
  ["It looks like a smiley face. It is not. Tony Knapton, the Wisconsin artist who runs Radry, drew one eye as a circle for birdies and the other as a square for bogeys, and the wave where the mouth should be is the up and down of a round.",
   "That makes it the cleverest mark here: a logo about coming to terms with the game rather than beating it, hiding in plain sight on every hat he makes."],
  ("One eye in the logo is a circle (birdies) and one is a square (bogies) &mdash; to represent both sides of par and both sides to golf.", "Tony Knapton, Radry founder"),
  "Tony Knapton, in an interview a few months after he started Radry", "/drops/brand-to-know-radry-golf"),
 ("seamus", "The Goat Caddie", "Seamus Golf", "Portland, Oregon", "https://www.seamusgolf.com/",
  [("seamus-1.jpg", "A hand-forged copper Seamus ball marker stamped with the goat caddie"),
   ("seamus-2.jpg", "Seamus&rsquo;s hand-forged goat caddie bag tag, which doubles as a bottle opener")],
  ["Real goats caddie at Silvies Valley Ranch in eastern Oregon. In 2018 the ranch called Seamus and asked for something nobody had made before: a golf bag for a goat. Seamus built custom saddlebags, the goats went to work, and the goat became the Seamus mascot.",
   "It now turns up on hand-forged copper ball markers, a bottle-opener bag tag and a money clip."],
  ("These charming companions have become icons of the ranch&mdash;and the inspiration behind our Seamus Goat logo.", "Seamus Golf&rsquo;s blog"),
  "Seamus&rsquo;s own blog and product pages; Akbar Chisti on the first goat bag, 2018", "/drops/brand-to-know-seamus"),
 ("pare", "The Par&eacute; Boy", "Par&eacute; Golf", "United States", "https://pare.golf/",
  [("pare-1.jpg", "A white Par&eacute; crew sock with a large Par&eacute; Boy putting down the side"),
   ("pare-2.jpg", "A green Par&eacute; mockneck on a hanger with the Par&eacute; Boy at the chest")],
  ["A line drawing of a kid leaning over a putt in jean shorts. The kid is founder Matt Sakdalan, on the green as a boy in his Girbaud jorts.",
   "Par&eacute;&rsquo;s About page says the mark tips its hat to PING and Karsten Solheim, whose own logo is a little man putting. So a brand built on Filipino culture borrowed golf&rsquo;s most famous putting figure and put its own founder in the picture."],
  None, "Par&eacute;&rsquo;s own About page and founder Matt Sakdalan&rsquo;s interviews", "/drops/brand-to-know-pare-golf"),
 ("hls", "The Running Man", "Hidden Links Society", "United States", "https://hiddenlinkssociety.com/",
  [("hls-1.jpg", "Hidden Links Society's running man: a sketchy line drawing of a golfer sprinting with a club, over HIDDEN LINKS SOC."),
   ("hls-2.jpg", "A black-and-white Hidden Links Society campaign photo of a golfer finishing a swing under cypress trees")],
  ["A scratchy, hand-drawn golfer in a cap and shorts, sprinting with a club in his hand. He looks late for his tee time, or like he is playing through.",
   "Hidden Links has never published where he came from, and doesn&rsquo;t name a founder anywhere. What it does have is a PLAY FASTER hat, and a running man fits that better than any crest could. We would like to know who drew him."],
  None, "No published origin story; description from the brand&rsquo;s own artwork", "/drops/brand-to-know-hidden-links-society"),
 ("malbon", "Buckets", "Malbon Golf", "Los Angeles", "https://malbon.com/",
  [("malbon-1.jpg", "A white Malbon x BEAMS driver cover printed with six versions of the Buckets golf-ball character"),
   ("malbon-2.jpg", "A Malbon Buckets ball marker: a golf ball with a face and a green bucket hat")],
  ["A golf ball with a face. Before there was a brand, Stephen Malbon kept a golf Instagram that worked like a mood board, and from 2012 a cartoon golf-ball character kept turning up in his sketches.",
   "When Stephen and Erica Malbon launched the brand in 2017, that character, Buckets, became the logo. It has since been redrawn by everyone from BEAMS to Daniel Arsham, which is the surest sign a character has outgrown its first job."],
  None, "CNN&rsquo;s 2024 reporting on Malbon&rsquo;s start; Malbon&rsquo;s own About page", "/drops/arsham-malbon-chapter-three"),
 ("ssc", "The Tourasaurus", "Sugarloaf Social Club", "Virginia", "https://www.sugarloafsocialclub.com/",
  [("ssc-1.jpg", "Sugarloaf's Tourasaurus: a red dinosaur in a blue bucket hat leaning on a golf club"),
   ("ssc-2.jpg", "A navy Sugarloaf sweater knitted with the Tourasaurus")],
  ["A red dinosaur in a blue bucket hat, leaning on a club like he is waiting on the group ahead. He comes painted and in 8-bit pixels, and the brand says the pixel version is &ldquo;ready for his Mario Golf tee time.&rdquo;",
   "Founder Ian Gilley gives the best reason anyone has for a mascot at all: nobody told him he couldn&rsquo;t."],
  ("Our club logo also changes frequently, because no grownups are around to tell us we can&rsquo;t do that.", "Ian Gilley, Sugarloaf founder"),
  "Sugarloaf&rsquo;s own About page and product copy", "/drops/brand-to-know-sugarloaf-social-club"),
 ("siegel", "The Horse and Sulky", "Siegelman Stable", "New York", "https://siegelmanstable.com/",
  [("siegel-1.jpg", "Siegelman Stable's emblem: a harness driver behind a trotting horse and sulky"),
   ("siegel-2.jpg", "A black Siegelman Stable cap with the horse and sulky stitched in gold")],
  ["A harness driver crouched behind a trotting horse. It is not a golf image at all, and that is the point: Robbie Siegelman started the Siegelman Racing Stable in 1982, and his son Max launched the clothing in 2020 partly as a tribute to the family&rsquo;s racing logo.",
   "Of everything here it is the one with the most history behind it before it ever touched a golf course."],
  ("The story is already built through horse racing and equine therapy, now being retold through fashion.", "Max Siegelman"),
  "Siegelman Stable&rsquo;s own About page", "/drops/brand-revisited-siegelman-stable"),
 ("radmor", "BobRad", "Radmor", "Seattle", "https://radmorgolf.com/",
  [("radmor-1.jpg", "A black leather Radmor barrel headcover covered in the BobRad golf-ball face"),
   ("radmor-2.jpg", "A white leather Radmor blade putter cover with BobRad and the RADMOR wordmark")],
  ["A cartoon golf ball peeking out, which most people read as a little UFO. Radmor runs two logos on purpose: the Dead Center ball-and-cup for the serious, green-grass side, and BobRad for everyone who finds golf a bit stuffy.",
   "The name RADMOR blends its co-founders, Scott Morrison and Bob Conrad, and BobRad is the half of the brand that doesn&rsquo;t take itself seriously."],
  None, "Radmor&rsquo;s own launch announcement", "/drops/brand-to-know-radmor"),
 ("rolo", "Rolo the Dog", "Rolo Golf", "Toronto", "https://rolo.golf/",
  [("rolo-1.jpg", "Rolo Golf's logo: a pink-and-white bulldog head in a gold chain"),
   ("rolo-2.jpg", "A black Rolo Golf cap with the bulldog embroidered on the front")],
  ["A pink-and-white bulldog in a gold chain. He is Rolo, founder Chase Dobbie&rsquo;s actual dog, and the brand is named after him.",
   "The shortest story on the list, and maybe the most relatable: they had a dog, the dog had a face, and that was that."],
  ("We named the company after my dog&hellip; He&rsquo;s the logo, and we made the name in a day.", "Chase Dobbie, Rolo Golf founder"),
  "Chase Dobbie, to Golf Town", None),
 ("jain", "Jain, the Worldly Golf Ball", "Jain Golf", "Los Angeles", "https://jain.golf/",
  [("jain-1.jpg", "The Jain plush: a golf ball printed like a globe, in a yellow bucket hat, white gloves and orange sneakers"),
   ("jain-3.jpg", "Jain Golf's cream Sport headcover, with Jain's cartoon gloved hand gripping the club")],
  ["A golf ball printed like a little globe, in a yellow bucket hat with a J on it, white gloves and orange-and-white sneakers. He comes as a drawing, a plush, and a hand that reaches out of a headcover to grip the shaft.",
   "The brand&rsquo;s About page is the best on this list. Jain is &ldquo;a worldly little golf ball who loves golf more than anything,&rdquo; founder Chris Hovsepian is listed as &ldquo;Asst. to Jain,&rdquo; and the CEO is his four-year-old daughter, Ella. It is the one character here built to get kids into the game."],
  ("Jain&rsquo;s only goal is to make kids fall in love with golf. And I think a character can do that better than a club.", "Chris Hovsepian, to The Golfer&rsquo;s Journal"),
  "Jain Golf&rsquo;s own About page; Chris Hovsepian in The Golfer&rsquo;s Journal No. 34", None),
 ("matchstick", "The Match", "Matchstick Golf", "Portland, Oregon", "https://matchstickgolf.com/",
  [("match-1.jpg", "Matchstick Golf's logo: a red M crossed by a single red-tipped match"),
   ("match-2.jpg", "A white golf glove holding a handful of Matchstick enamel ball markers: a cash stack, a burger, a popsicle and more")],
  ["A red M with a single red-tipped match laid across it. It is the plainest mark on this list and still one of the smartest, because the whole brand is built around it: every Matchstick ball marker ships in its own little matchbox.",
   "Founder Dane Delgado got there from the golf course itself. Players smoke cigars on the course, cigars need matches, and a matchbox turned out to be the right size for a ball marker. He has a mascot too, a match called Woody, who rides on the side of the shipping mailers."],
  ("A matchbox, I thought, was the perfect packaging for a golf ball marker.", "Dane Delgado, Matchstick founder"),
  "Dane Delgado, in an interview with CanvasRebel", "/drops/brand-to-know-matchstick-golf"),
]

COURSE = [
 ("lahinch", "The Goats", "Lahinch Golf Club", "County Clare, Ireland", "https://lahinchgolf.com/",
  [("lahinch-1.jpg", "The Lahinch Golf Club crest: a white goat rearing in a green roundel"), ("lahinch-2.jpg", "A navy enamel Lahinch ball marker with the goat")],
  "A rearing goat on the crest. The club&rsquo;s own history says that when the clubhouse barometer broke, the manager wrote a note on it by hand: &ldquo;See Goats.&rdquo;"),
 ("putterboy", "Putter Boy", "Pinehurst", "North Carolina", "https://www.pinehurst.com/",
  [("putterboy-1.jpg", "A Pinehurst pin flag with the Putter Boy putting over a sundial, 1895")],
  "A boy in knickers putting over a sundial, sculpted in 1912, with Donald Ross said to have shown the sculptor the grip. &ldquo;He&rsquo;s the little boy in all of us.&rdquo;"),
 ("delmonte", "The Golfing Scotsman", "Del Monte Golf Course", "Pebble Beach, California", "https://www.pebblebeach.com/",
  [("delmonte-1.jpg", "A Del Monte pin flag with a knickered Scotsman mid-follow-through above blackletter Del Monte")],
  "A knickered Scotsman finishing his swing under an enormous curled moustache, drawn by New Yorker cartoonist Eldon Dedini. Pebble Beach calls the moustache Dal&iacute;-esque, and it is."),
]

CSS = ('<style>/*TGI-EMBLEMS v1*/'
       '.em-toc{display:grid;grid-template-columns:repeat(4,1fr);border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink);margin:8px 0 0}'
       '.em-toc a{display:block;padding:14px 16px;border-right:.5px solid rgba(20,20,20,.2);border-bottom:.5px solid rgba(20,20,20,.2);text-decoration:none;color:inherit;font-family:var(--serif);font-size:17px;line-height:1.2}'
       '.em-toc a:nth-child(4n){border-right:none}.em-toc a:nth-last-child(-n+4){border-bottom:none}.em-toc a span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-bottom:4px}'
       '.em{padding-top:0!important;padding-bottom:0!important}.em-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;padding:56px 0;border-top:.5px solid rgba(20,20,20,.25)}.em-row.flip .em-imgs{order:2}.em-imgs{display:grid;grid-template-columns:1fr 1fr;gap:8px}.em-imgs.one{grid-template-columns:1fr}.em-imgs img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#E8E2D6}.em-imgs.one img{aspect-ratio:4/3}.em-who{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:10px}section.products.em .em-txt h2{font-family:var(--serif);font-weight:400;font-size:clamp(34px,4vw,50px);line-height:1;letter-spacing:-.01em;margin:0 0 18px!important;text-align:left!important}.em-txt p{font-size:17px;line-height:1.62;margin:0 0 14px}.em-txt a{border-bottom:1px solid currentColor}.em-q{font-family:var(--serif);font-size:23px;line-height:1.35;color:#2D4A2B;margin:8px 0 18px;padding:2px 0 2px 18px;border-left:2px solid #2D4A2B}.em-q cite{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#2D4A2B;opacity:.75;margin-top:10px}.em-foot{border-top:.5px solid rgba(20,20,20,.2);padding-top:12px;margin-top:6px}.em-src{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.55;margin:0 0 10px}.em-links{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;display:flex;gap:18px;flex-wrap:wrap}'
       '.em-course{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:22px}.em-course img{width:100%;aspect-ratio:1;object-fit:cover;display:block;margin-bottom:12px}.em-course h3{font-family:var(--serif);font-weight:400;font-size:28px;line-height:1.05;margin:0}.em-course p{font-size:15px;line-height:1.55;margin:8px 0 0}'
       '.em-cap{font-family:var(--serif);font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:clamp(28px,4vw,46px);line-height:1.05;text-align:center!important;color:#2D4A2B}'
       '.drop-tag.grass{background:none!important;color:#2D4A2B!important;border:0!important;padding:0!important;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.75}'
       'section.products.em .em-txt p.em-src{font-size:10px!important;line-height:1.6!important;letter-spacing:.1em}section.products.em .em-course p{font-size:15px!important}'
       '@media(max-width:820px){.em-row{grid-template-columns:1fr;gap:20px;padding:40px 0}.em-row.flip .em-imgs{order:0}.em-toc{grid-template-columns:1fr 1fr}.em-toc a{border-right:.5px solid rgba(20,20,20,.2)!important;border-bottom:.5px solid rgba(20,20,20,.2)!important}.em-toc a:nth-child(2n){border-right:none!important}.em-course{grid-template-columns:1fr}}'
       '</style>\n')


def entry(i, e):
    k, name, brand, place, site, imgs, paras, quote, src, link = e
    im = "".join(f'<img src="{IMG}/{f}" alt="{a}" loading="lazy" />' for f, a in imgs)
    q = f'<blockquote class="em-q">&ldquo;{quote[0]}&rdquo;<cite>{quote[1]}</cite></blockquote>' if quote else ""
    links = f'<a href="{site}" target="_blank" rel="noopener">Visit {brand} &#8599;</a>'
    if link:
        links += f'<a href="{link}">More on {brand} &rarr;</a>'
    body = f"<p>{paras[0]}</p>{q}" + "".join(f"<p>{p}</p>" for p in paras[1:])
    flip = " flip" if i % 2 == 0 else ""
    return (f'\n<section class="products em" id="{k}">\n'
            f'  <div class="em-row{flip}"><div class="em-imgs{" one" if len(imgs) == 1 else ""}">{im}</div>'
            f'<div class="em-txt"><div class="em-who">{brand} &middot; {place}</div><h2>{name}</h2>{body}'
            f'<div class="em-foot"><p class="em-src">Story: {src}</p><div class="em-links">{links}</div></div></div></div>\n</section>\n')


def course():
    cards = "".join(f'<div><img src="{IMG}/{imgs[0][0]}" alt="{imgs[0][1]}" loading="lazy" /><div class="em-who">{c} &middot; {pl}</div>'
                    f'<h3>{n}</h3><p>{t}</p><p class="em-links" style="margin-top:10px"><a href="{u}" target="_blank" rel="noopener">Visit &#8599;</a></p></div>'
                    for k, n, c, pl, u, imgs, t in COURSE)
    return ('\n<section class="products em" id="course">\n  <div class="drop-tag grass" style="text-align:center">Bonus</div>\n'
            '  <h2 class="products-hdr em-cap">Three From the Course</h2>\n'
            '  <p style="max-width:720px;margin:10px auto 0;text-align:center;font-size:17px;line-height:1.6">Brands didn&rsquo;t invent this. Some of the best characters in golf have been on pin flags and ball markers for a century.</p>\n'
            f'  <div class="em-course">{cards}</div>\n</section>\n')


def toc():
    return '<nav class="em-toc" aria-label="The emblems">' + "".join(
        f'<a href="#{e[0]}"><span>{e[2]}</span>{e[1]}</a>' for i, e in enumerate(E, 1)) + '</nav>\n'


def images():
    """Single hero (Lenny 23 Nov): Seamus's real goat caddie in its saddlebag, from Seamus's own site."""
    d = ROOT / IMG.lstrip("/")
    _s = (ROOT / "research/far-wide/frame.py").read_text(); g = {"Image": Image}
    import numpy as np; g["np"] = np; g["STONE"] = np.array([232, 226, 214], float)
    exec(_s[_s.index("def cover"):_s.index("\n\nWHITE=")], g)
    im = Image.open(ROOT / "research/logos/emb/seamus-goat.jpg").convert("RGB")
    g["cover"](im, 2000, 857, .5, .12).save(d / "hero.jpg", quality=86)
    g["cover"](im, 1200, 630, .5, .12).save(d / "og.jpg", quality=86)
    g["cover"](im, 1000, 1250, .55, .5).save(d / "card-hero.jpg", quality=86)


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-23", "dateModified": "2026-11-23",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": [
            {"@type": "ListItem", "position": i, "name": f"{H.unescape(e[2])}: {H.unescape(e[1])}", "url": f"{URL}#{e[0]}"} for i, e in enumerate(E, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Golf Brand Emblems", "item": URL}]},
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
    side = "\n".join(f'      <div class="sidebar-detail"><span class="l">{e[2]}</span><span><a href="#{e[0]}" style="border-bottom:none">{e[1]}</a></span></div>' for e in E) + '\n      <div class="sidebar-detail"><span class="l">Bonus</span><span><a href="#course" style="border-bottom:none">Three from the course</a></span></div>'
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Golf Brand Emblems</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 23, 2026</p><!--/TGI-BY-->
  <p style="font-size:20px;font-style:italic;max-width:680px;margin:10px auto 0">{DEK}</p>
  <div class="drop-meta">
    <span>The Edit</span><span class="dot"></span>
    <span>14 emblems &middot; 3 from the course</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A goat caddie at Silvies Valley Ranch in Oregon carrying golf clubs in a leather Seamus saddlebag" fetchpriority="high" /></div></div>

<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The biggest names in golf spend fortunes on logos that say very little: a script, a set of initials, a crest drawn to look like it has been around since 1895. Small brands can&rsquo;t buy that kind of recognition, so the good ones do something better. <strong>They draw a character.</strong></p>
    <p>Golf has always had a soft spot for these. Pinehurst has had its Putter Boy since 1912. Lahinch has its goats. PING&rsquo;s little putting man started in 1967 as a clay figure Karsten Solheim&rsquo;s son made at home. The brands below are working in that tradition, just with skate decks, group chats and embroidery machines instead of sundials.</p>
    <p><strong>A character does work a wordmark can&rsquo;t.</strong> It&rsquo;s funny, and golf could use more funny. It starts conversations on the first tee. And it gives a brand somewhere to go. A wordmark can change color. A character can dance across a leather headcover, turn up in 8-bit for a Mario Golf joke, get redrawn by a Japanese retailer or a contemporary artist, and still be the same character. Malbon&rsquo;s Buckets has been every one of those things.</p>
    <blockquote class="em-q em-pq">Nobody has ever asked what the initials on a polo stand for. Everyone asks about the cow.</blockquote>
    <p><strong>For a small brand the logo is also, very often, the product.</strong> Hats, headcovers, ball markers, towels: most of what an independent golf label sells is a place to put the mark. People buy a Radry hat for the face on it. A mark that people want on their head is the whole business plan.</p>
    <p><strong>The part we like most is how personal they are.</strong> Nearly every one on this list started as somebody&rsquo;s grandad&rsquo;s field, a family emblem, a founder&rsquo;s dog, or a photo of a kid with a golf club, and a surprising number were drawn by the founders or their friends rather than an agency. You can see it in the line work. Hidden Links&rsquo; running man is all scratchy, hand-drawn line. Radry&rsquo;s face was drawn by the artist who runs the brand. Malbon&rsquo;s Buckets started as Stephen Malbon&rsquo;s own sketches, years before there was a brand.</p>
    <blockquote class="em-q em-pq">A brand that puts a goat or a dinosaur on its chest isn&rsquo;t pretending to be a hundred years old.</blockquote>
    <p><strong>It&rsquo;s also a tell.</strong> Nobody with a cartoon goat on the chest is pretending to be a heritage brand. It&rsquo;s telling you who made it, and that they take the clothes seriously and the game a little less so. That is most of what we look for in a brand anyway.</p>
    <p>These are our fourteen favorites, in no particular order, plus three from golf courses that were doing this long before anyone printed a hat. Every story comes from the brand&rsquo;s own site or the founder&rsquo;s own words; where nobody has written it down, we say so rather than guess.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Fourteen &middot; in no order</div>
{side}
    </div>
  </aside>
</section>
"""
    for i, e in enumerate(E, 1):
        body += entry(i, e)
    body += course()
    body += """
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr em-cap" id="last-word" style="font-size:clamp(26px,3.6vw,40px)">Give It a Reason</h2>
    <p>The best of these weren&rsquo;t designed by committee. Somebody drew their dog, their grandad&rsquo;s cow, themselves as a kid. If you are starting a golf brand, that is the lesson: the mark people remember is the one with a story you can tell in a sentence.</p>
    <p>If we missed your favorite, or you know who drew the Hidden Links running man, <a href="/work-with-us">tell us</a>.</p>
  </div>
</section>
"""
    if apply_:
        images()
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
    print(f"  wrote drops/{SLUG}.html · {len(E)} emblems + {len(COURSE)} course")


if __name__ == "__main__":
    main("--apply" in sys.argv)
