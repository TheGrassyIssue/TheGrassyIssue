#!/usr/bin/env python3
"""build-indie-scale.py — Field Note essay: How Big Can an Independent Golf Brand Get? 1 November 2026.
Lenny: explore how big a golf company can get and still be independent; six fringe cases, most corporate to least
(Ping, Bettinardi, Miura, L.A.B. Golf, Malbon, per Lenny's final order; Mizuno dropped); private-equity context and how to be a more informed buyer.
"Less of an expose and more of how golf has grown." Truly independent brands deliberately left out (the rest of the site covers them).
Layout cloned from build-mind-body-spirit.py (editorial, no product cards).
FACTS (read Nov 1 2026): Golf Digest/MyGolfSpy/Front Office Sports (L.A.B. + L Catterton, Jul 2025); Mizuno Wikipedia, Simply Wall St,
mizunogolf.com/us/art-of-forging (Chuo plant, Hiroshima, 1968; hammer apprenticeship); GOLF.com Feb 17 2026 (Ping family, ~1,000 staff,
John A. chairman, John K. president and CEO); PitchBook/Crunchbase (Malbon ~$30M, 2025); GOLF.com + The Golf Wire (Bettinardi, Valspar 2026);
GOLF.com Feb 1 2017 + Miura statement 2025 (8AM / Howard Milstein distribution rights); Golf Digest, Front Office Sports (TaylorMade/Centroid);
Golf Monthly/Pulse2 (Topgolf/Leonard Green); Richemont + SGI Europe (Peter Millar). Revenue estimates deliberately not printed.
IMAGES: each brand's own site (research/indie-scale/raw). Hero: Bettinardi putter lineup (bettinardi.com).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
TITLE = "How Big Can an Independent Golf Brand Get?"
DESC = ("Private equity owns more of golf than most people realize. Five well-known brands, from family-owned Ping to founder-led Malbon, "
        "the hazy line in the middle, and how to know who you are buying from.")
H1 = "How Big Can an Independent Golf Brand Get?"
BC = "How Big Can an Independent Golf Brand Get?"
SLUG = "how-big-can-an-independent-golf-brand-get"
IMG = "/images/independent-scale"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
ORDER = ["ping", "bettinardi", "miura", "lab", "malbon"]
N = 5

B = {}
B["lab"] = dict(name="L.A.B. Golf", tag="Owned by private equity since 2025", url="https://labgolf.com/",
 alt="A purple L.A.B. Golf DF3 putter resting on a putting green, casting a long shadow",
 cap="The DF3, the putter that made L.A.B.&rsquo;s name.",
 paras=[
  "L.A.B. Golf is the most recent example of a brand crossing the line, and the gentlest. Sam Hahn took over the company in 2018, buying out the original investors behind founder Bill Presse&rsquo;s putters, and for years he ran it without outside backers. The putters looked like nothing else in golf, the lie-angle balance idea caught on, and by 2025 L.A.B. was the putter in J.J. Spaun&rsquo;s bag when he won the U.S. Open.",
  "That July, L Catterton, the private equity firm backed by LVMH, bought a majority stake at a reported valuation of more than $200 million. Hahn stayed on as CEO, after a run in which he says sales grew 18,000 percent in seven years. Presse, the founder, kept a stake in the new company. From the outside, the putters look the same. What changed is who owns the company, and with it, who will eventually decide when and how it grows.",
  "That is how most brands cross over. It isn&rsquo;t a scandal, it is a success, and it usually happens right when a small company proves it can be a big one."],
 facts=[("Owner","Majority-owned by L Catterton since July 2025"),("Run by","Sam Hahn, CEO since 2018"),("Reported value","More than $200 million"),("The case","A brand built without backers, now owned by a fund, with the same leadership")])
B["ping"] = dict(name="Ping", tag="Family-owned, corporate-sized", url="https://ping.com/",
 alt="A silver Ping putter on a workbench with bottles of paint-fill behind it",
 cap="A putter in Ping&rsquo;s custom shop, waiting for its paint-fill.",
 paras=[
  "By the usual test, Ping is as independent as any company in golf. Karsten Solheim started the company with a putter in 1959, and the business has never had an outside owner. His son John A. is now chairman, and his grandson John K. is president and CEO. There are no investors and nobody to sell to.",
  "It is also huge. Ping has about 1,000 employees in Phoenix, and its name is on the Solheim Cup. GOLF.com&rsquo;s Michael Bamberger described the family business this way: it is &ldquo;not a business at all, not in the conventional sense.&rdquo;",
  "Ping is the case that size alone does not decide independence. It just changes what independence looks like. Nobody would call Ping indie, but nobody owns it except the family that started it."],
 facts=[("Owner","The Solheim family"),("Run by","John K. Solheim, president and CEO; John A. Solheim, chairman"),("Size","About 1,000 employees"),("The case","No outside owners at all, at the scale of a major")])
B["malbon"] = dict(img="malbon-founders", name="Malbon Golf", tag="Founder-led, investor-backed", url="https://malbon.com/",
 alt="Stephen and Erica Malbon standing together against a pale blue backdrop, Stephen in a green cap and yellow Malbon sweatpants",
 cap="The founders, together.",
 paras=[
  "Stephen and Erica Malbon started Malbon in Los Angeles in 2017, and more than almost anyone they made golf look like part of culture, not apart from it. The bucket logo, the collaborations and the stores all came from the two of them, and they still lead it.",
  "In 2025 Malbon raised about $30 million, with Avenir named as the lead investor in most deal trackers. That money pays for stores, staff and growth, and it also puts other people at the table. Nobody owns Malbon but its founders and investors yet. But this is the stage where the line starts to blur, and one more round could move it.",
  "This is how most fashion brands grow. Taking investment is a choice about speed, not a betrayal, and Malbon chose to move fast."],
 facts=[("Owner","Founders, with minority investors since 2025"),("Run by","Stephen and Erica Malbon"),("Raised","About $30 million in 2025"),("The case","The founders still steer, and investors are on board")])
B["bettinardi"] = dict(name="Bettinardi Golf", tag="Family-owned, built like a big company", url="https://bettinardi.com/",
 alt="A workbench covered in Bettinardi putter heads, headcovers, tools and drawings",
 cap="The bench in Bettinardi&rsquo;s Workshop, where custom putters are put together.",
 paras=[
  "Bettinardi is family-owned and proud of it. Robert Bettinardi founded the company, his son Sam is now president, and the putters are milled in Tinley Park, Illinois, as they have been since 1998. Sam joined in 2013, and Bob says the company has grown by double digits every year since Sam took over day-to-day. There are no outside owners.",
  "But it runs like a much bigger company: a tour staff, a full line of putters and wedges, licensed college and pro collaborations, and as many as 200 employees. In 2026 Matt Fitzpatrick won the Valspar Championship with a Bettinardi in his bag.",
  "That is the corporate side of independent. The structure looks like any major equipment maker. The ownership is still the family, and the putters are still made down the road from where they are designed."],
 facts=[("Owner","The Bettinardi family"),("Run by","Robert Bettinardi; Sam Bettinardi, president"),("Made in","Tinley Park, Illinois"),("The case","No outside owners, but the reach and structure of a major")])
B["miura"] = dict(name="Miura", tag="Family-made, outside distribution", url="https://miuragolf.com/",
 alt="A craftsman standing at a forging press inside the Miura factory in Himeji, Japan",
 cap="The forge at Miura&rsquo;s factory in Himeji, Japan.",
 paras=[
  "Miura has a real claim to being independent, and it is the most interesting one here. Katsuhiro Miura spent his life forging irons at a single factory in Himeji, Japan, and after his death in 2025 the company said the factory still designs and forges every club. His sons, Shinei and Yoshitaka, run it day to day.",
  "The complication is everywhere else. In 2017, Howard Milstein, the investor behind 8AM Golf, bought the rights to distribute Miura in the U.S. and abroad, and Miura now describes itself as part of the 8AM Golf family. So the business of selling Miura outside Japan runs through a larger company, which also owns GOLF.com, where a lot of Miura coverage appears. When the deal was new, the company&rsquo;s U.S. president, Hoyt McGarity, put the split plainly to LINKS: the Miura family owns the warehouse, and his side owns the distribution rights.",
  "Our read: what makes Miura Miura is still in Himeji, in family hands. The money and the marketing come from outside, but nobody outside the family decides how a Miura iron is made. If independence is about who controls the work, Miura still has it."],
 facts=[("Made by","The Miura family, Himeji, Japan"),("Run by","Shinei and Yoshitaka Miura"),("Sold by","8AM Golf, outside Japan, since 2017"),("The case","Outside money and distribution, family craft")])

EXTRA = {
 "ping": [("ping-2", "A copper-finish Ping PLD Milled putter on a putting green next to a ball", "A Ping PLD Milled putter."),
          ("ping-3", "Ping's practice facility with a hitting bay and desert mountains behind it", "Ping&rsquo;s proving grounds in Phoenix.")],
 "bettinardi": [("bettinardi-2", "A set of chrome Bettinardi irons on a black background", "Bettinardi irons."),
                ("bettinardi-3", "Bettinardi putters standing among pink and yellow golf balls", "Putters from Bettinardi&rsquo;s Junior Series.")],
 "miura": [("miura-2", "A pile of fine steel shavings from grinding iron heads", "Shavings from the grinding wheel in Himeji."),
           ("miura-3", "A gloved hand holding a freshly ground Miura iron head", "Checking a head by hand.")],
 "lab": [("lab-2", "An L.A.B. Golf putter behind a golf ball on a green", "On the green with L.A.B."),
         ("lab-3", "Three L.A.B. Golf OZ.1 putter heads lined up on a white surface", "The OZ.1 family.")],
 "malbon": [("malbon-3", "A man in a red knit polo and navy cap standing in a forest of ferns", "From Malbon&rsquo;s fall campaign."),
            ("malbon-2", "A person in a blue and orange Malbon ski jacket in a snowy forest, seen from behind", "From Malbon&rsquo;s winter campaign.")],
}

QUOTES = {
 "ping": ("We&rsquo;ve just started to scratch the surface.", "Karsten Solheim, as remembered by retired Ping rep Robin McCool, to GOLF.com"),
 "bettinardi": ("Now that I&rsquo;m running the business, Bob&rsquo;s the bank.", "Sam Bettinardi, on working with his father, to GOLF&rsquo;s Fully Equipped, 2025"),
 "miura": ("He tells us what he&rsquo;s launching. We don&rsquo;t tell him.", "Hoyt McGarity, then president of Miura&rsquo;s distribution business, to LINKS Magazine"),
 "lab": ("From start to finish my dreams have all been realized.", "Bill Presse, L.A.B.&rsquo;s founder, after the 2025 sale, via Golf Digest"),
 "malbon": ("Malbon is a family brand started by my husband and myself.", "Erica Malbon, to the Philippine Daily Inquirer"),
}

FOUNDERS = {
 "ping": "Ping, founded by Karsten Solheim in 1959.",
 "bettinardi": "Bettinardi Golf, founded by Bob Bettinardi in 1998.",
 "miura": "Miura, founded by Katsuhiro Miura.",
 "lab": "L.A.B. Golf, founded by Bill Presse; run by Sam Hahn since 2018.",
 "malbon": "Malbon Golf, founded by Stephen and Erica Malbon in 2017.",
}

WIDE = {}

INTRO = """
<section class="mbs-intro">
  <p class="mbs-epi">Independent isn&rsquo;t a size. It&rsquo;s a question of who decides.</p>
  <div class="mbs-lede">
    <p>Golf has grown fast in the last few years, and the money has followed. TaylorMade has been owned by the private equity firm Centroid since 2021, when it paid about $1.7 billion, and in 2026 the company was for sale again at a reported $3.4 to $3.5 billion. Callaway sold 60% of Topgolf to the private equity firm Leonard Green at a $1.1 billion valuation, in a deal that closed on January 1, 2026. Peter Millar went from a private equity owner to the luxury group Richemont back in 2012. Most of the logos in a golf shop now sit inside a larger company.</p>
    <p>None of that is a secret, and it is part of how a sport grows. But it raises a question we get asked a lot: how big can a golf brand get and still be called independent?</p>
    <p>We don&rsquo;t think the answer is a number. So here are five well-known brands that sit near the line, from the most corporate in size and structure to the most independent in spirit, with who owns each one, who runs it and our case for where it lands. The small makers we cover every week aren&rsquo;t here on purpose. This is about the gray area.</p>
  </div>
</section>
"""

SHOP = """
<section class="mbs-solo">
  <h2 class="mbs-h2" id="shop-with-your-eyes-open">How to Shop With Your Eyes Open</h2>
  <div class="mbs-solo-grid">
    <div><h3>Read past the logo</h3><p>Start with the brand&rsquo;s About page, then search its name with &ldquo;acquired&rdquo; or &ldquo;investment.&rdquo; Deals between golf companies are usually reported, and two minutes will tell you who owns what.</p></div>
    <div><h3>Ask who makes it</h3><p>Where a thing is made, and by whom, says more than any label. Miura forges in Himeji. Bettinardi mills in Illinois. Ping builds in Phoenix. None of that changes with ownership unless someone decides it should.</p></div>
    <div><h3>Watch what happens after a deal</h3><p>Look at what follows a sale: prices, quality, whether the founders stay and whether the product keeps its point of view. If things are going to slip, that is where you will see it first.</p></div>
    <div><h3>Spend where you want the money to go</h3><p>When it matters to you, buy direct from the people who make the thing. And know who is talking to you about it: some golf media is owned by companies that also own brands. We earn commissions on some links too, and that is spelled out in our <a href="/disclosure" style="border-bottom:1px solid currentColor">disclosure</a>.</p></div>
  </div>
</section>
"""

TAKE = """
<section class="mbs-solo" id="the-hazy-middle" style="margin-top:96px">
  <h2 class="mbs-h2">The Hazy Middle</h2>
  <div class="writeup-body" style="max-width:820px">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The ends of this list are easy. Ping is a family company the size of a major, and nobody would call it indie. Malbon still feels like two founders with a point of view, even with investors on board. The interesting part is the middle, where the usual tests stop agreeing with each other.</p>
    <p>Look at Miura and L.A.B. side by side. Miura has outside money and an outside company selling its clubs, but the family still decides how every iron is made. L.A.B. is owned by a private equity fund, but the same CEO runs it and, from the outside, the putters look the same. By ownership, L.A.B. is the less independent of the two. By how the product gets made, it is hard to tell them apart. And Bettinardi, with no outside owners at all, runs more like a big company than either.</p>
    <p>That is the hazy line. Independence isn&rsquo;t one thing. It is at least four questions: who owns the company, who makes the decisions, who makes the product and who takes the money when it sells. Most brands answer them differently, and the answers change as a brand grows. The putter maker you loved for its backstory can be owned by a fund next year and still make the same putter.</p>
    <p>So we don&rsquo;t think the useful question is &ldquo;is this independent?&rdquo; It is &ldquo;who decides?&rdquo; If the people who started it still decide what gets made, that counts for a lot, whatever the cap table says. If they don&rsquo;t, take a closer look before you buy.</p>
    <p><strong>Where we stand.</strong> We try to avoid private equity. Not because a fund ruins a product overnight. Most don&rsquo;t, and none of the brands here has shown us that it has. The concern is what the job becomes. A private equity firm buys a company in order to sell it again for more, usually within a few years. Centroid bought TaylorMade in 2021 and had it back on the market by 2026. When the next sale becomes the measure of success, every decision gets weighed against it: a cheaper material if the margin needs to grow, a faster release calendar if the numbers need to climb, wider distribution if the next buyer wants scale.</p>
    <p>Sometimes a brand comes through that with everything that made it good intact. Sometimes the thing you loved about it is the first cost to go. Bringing in investor money isn&rsquo;t the dealbreaker for us. Plenty of great brands need it to grow. Handing the reins to an investor is.</p>
    <p>Keeping the reins has a cost, and it is fair to say so. A company that stays independent may have to grow more slowly, turn down the deal that would have put it in every pro shop, or accept that its audience will stay smaller than it could be. Miura&rsquo;s U.S. president once told LINKS the brand couldn&rsquo;t become &ldquo;some $100 million business&rdquo; because every club is made by hand. That isn&rsquo;t a weakness in the plan. Sometimes those limits are exactly what keep a brand&rsquo;s character intact.</p>
    <p>So the question isn&rsquo;t only how big a golf brand can get and still be independent. It&rsquo;s how much growth a brand is willing to give up to remain itself.</p>
  </div>
</section>
"""

CSS = """<style>/*TGI-INDIE*/
.mbs-hero{position:relative;width:100%;max-width:1600px;margin:0 auto 8px;padding:0 32px}
.mbs-hero img{width:100%;aspect-ratio:16/7;object-fit:cover;display:block;border:.5px solid var(--ink)}
.mbs-cap{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-intro{max-width:1100px;margin:56px auto 24px;padding:0 32px;display:grid;grid-template-columns:1fr 2fr;gap:56px;align-items:start}
.mbs-epi{font-family:var(--serif);font-size:30px;line-height:1.2;color:var(--grass);border-top:.5px solid var(--ink);padding-top:18px}
.mbs-lede p{font-family:var(--serif);font-size:19px;line-height:1.6;margin-bottom:18px}
.mbs-lede p:first-child::first-letter{font-size:64px;float:left;line-height:.9;padding:6px 10px 0 0;color:var(--grass)}
.ind-scale{max-width:1200px;margin:56px auto 8px;padding:0 32px}
.ind-scale .ends{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:10px}
.ind-scale ol{list-style:none;margin:0;padding:18px 0 0;display:grid;grid-template-columns:repeat(5,1fr);position:relative;border-top:2px solid var(--grass)}
.ind-scale li{position:relative;padding:14px 8px 0;text-align:center}
.ind-scale li::before{content:"";position:absolute;top:-26px;left:50%;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--grass);border:3px solid #F4F1EA}
.ind-scale a{border-bottom:none;font-family:var(--serif);font-size:18px;display:block}
.ind-scale span{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.55;margin-top:6px;line-height:1.4}
.ind-b{max-width:1300px;margin:96px auto 0;padding:0 32px}
.ind-b-hd{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:end;border-bottom:.5px solid var(--ink);padding-bottom:14px;margin-bottom:28px}
.ind-b-hd .num{font-family:var(--serif);font-size:84px;line-height:.8;color:var(--grass)}
.ind-b-hd h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,48px);line-height:1;letter-spacing:-.01em}
.ind-b-hd .tag{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-top:10px}
.ind-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);gap:56px;align-items:start}
.ind-b.flip .ind-row{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)}.ind-b.flip figure{order:2}
.ind-row figure{margin:0}.ind-row img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.ind-row figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px;line-height:1.5}
.ind-q{max-width:900px;margin:48px auto 0;padding:24px 0;border-top:.5px solid var(--ink);border-bottom:.5px solid var(--ink);font-family:var(--serif);font-size:clamp(24px,3vw,34px);line-height:1.25;color:var(--grass);text-align:center}
.ind-q cite{display:block;font-style:normal;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:.55;margin-top:14px}
.ind-strip{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:40px}.ind-strip.one{grid-template-columns:1fr}
.ind-strip figure{margin:0}.ind-strip img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}.ind-strip.one img{aspect-ratio:12/5}.ind-strip.wide img{aspect-ratio:1340/550}
.ind-strip figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-top:8px}
.mbs-text p{font-family:var(--serif);font-size:18px;line-height:1.65;margin-bottom:18px}
.mbs-text a{border-bottom:1px solid currentColor}
.mbs-facts{border:.5px solid var(--ink);padding:20px 22px;margin-top:10px;background:rgba(45,74,43,.04);display:grid;grid-template-columns:1fr 1fr;gap:4px 24px}
.mbs-facts .k{font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;opacity:.5;margin-top:10px}
.mbs-facts .v{font-family:var(--serif);font-size:15px;line-height:1.45}
.mbs-facts .cell{min-width:0}
.mbs-facts a.go{grid-column:1/3;display:inline-block;margin-top:14px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;justify-self:start}
.mbs-solo{max-width:1300px;margin:120px auto 0;padding:48px 32px 0;border-top:.5px solid var(--ink)}
.mbs-h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,44px);margin-bottom:28px}
.mbs-solo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.mbs-solo h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:10px}
.mbs-solo p{font-family:var(--serif);font-size:16px;line-height:1.55}
@media(max-width:900px){.mbs-intro{grid-template-columns:1fr;gap:28px}.ind-row,.ind-b.flip .ind-row{grid-template-columns:1fr;gap:28px}.ind-b.flip figure{order:0}
.mbs-solo-grid{grid-template-columns:1fr 1fr}.ind-scale ol{grid-template-columns:repeat(3,1fr);row-gap:28px}}
@media(max-width:600px){.ind-strip{grid-template-columns:1fr}.ind-strip.one img{aspect-ratio:4/3}.mbs-hero,.mbs-intro,.ind-b,.mbs-solo,.ind-scale{padding-left:18px;padding-right:18px}.mbs-hero img{aspect-ratio:4/3}
.ind-b-hd .num{font-size:56px}.mbs-solo-grid{grid-template-columns:1fr}.mbs-facts{grid-template-columns:1fr}.mbs-facts a.go{grid-column:1}
.ind-scale ol{grid-template-columns:repeat(2,1fr)}.mbs-lede p,.mbs-text p{font-size:17px}}
</style>
"""


def scale_html():
    lis = "".join(f'<li><a href="#{k}">{B[k]["name"]}</a><span>{B[k]["tag"]}</span></li>' for k in ORDER)
    return (f'\n<nav class="ind-scale" aria-label="From most corporate to least">'
            f'<div class="ends"><span>More corporate</span><span>More independent</span></div><ol>{lis}</ol></nav>\n')


def quote_html(k):
    if k not in QUOTES: return ""
    q, who = QUOTES[k]
    return f'<blockquote class="ind-q">&ldquo;{q}&rdquo;<cite>&mdash; {who}</cite></blockquote>'


def strip_html(k):
    ex = EXTRA.get(k, [])
    w = ""
    if k in WIDE:
        f, a, c = WIDE[k]
        w = f'<div class="ind-strip one wide"><figure><img src="{IMG}/{f}.jpg" alt="{H.escape(a, quote=True)}" loading="lazy" /><figcaption>{c} Photo: {B[k]["name"]}</figcaption></figure></div>'
    if not ex: return w
    figs = "".join(f'<figure><img src="{IMG}/{f}.jpg" alt="{H.escape(a, quote=True)}" loading="lazy" /><figcaption>{c} Photo: {B[k]["name"]}</figcaption></figure>' for f, a, c in ex)
    return w + f'<div class="ind-strip{" one" if len(ex) == 1 else ""}">{figs}</div>'


def brand_html(k, n):
    b = B[k]
    text = "".join(f"<p>{p}</p>" for p in b["paras"])
    fx = "".join(f'<div class="cell"><div class="k">{H.escape(l)}</div><div class="v">{v}</div></div>' for l, v in b["facts"])
    flip = " flip" if n % 2 == 0 else ""
    return (f'\n<article class="ind-b{flip}" id="{k}">\n  <div class="ind-b-hd"><div class="num">{n:02d}</div><div><h2>{b["name"]}</h2>'
            f'<div class="tag">{b["tag"]}</div></div></div>\n'
            f'  <div class="ind-row"><figure><img src="{IMG}/{b.get("img", k)}.jpg" alt="{H.escape(b["alt"], quote=True)}" loading="lazy" />'
            f'<figcaption><strong>{FOUNDERS[k]}</strong> {b["cap"]} Photo: {b["name"]}</figcaption></figure>\n'
            f'  <div class="mbs-text">{text}<div class="mbs-facts">{fx}<a class="go" href="{b["url"]}" target="_blank" rel="noopener">Visit {b["name"]} &#8599;</a></div></div></div>\n'
            f'  {quote_html(k)}{strip_html(k)}\n</article>\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": B[k]["url"], "name": H.unescape(B[k]["name"])} for i, k in enumerate(ORDER)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-01", "dateModified": "2026-11-01",
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
    assert len(ORDER) == N == len(set(ORDER)) and set(ORDER) == set(B)
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
    <span>Five brands on the line &middot; November 1, 2026</span>
  </div>
</header>

<div class="mbs-hero"><img src="{IMG}/hero.jpg" alt="An older craftsman inspecting a freshly ground iron head while a younger worker in a mask points to it, inside the Miura factory in Himeji" fetchpriority="high" />
<div class="mbs-cap">The Miura family at work in the Himeji factory. Photo: Miura</div></div>
"""
    body += INTRO + scale_html()
    for n, k in enumerate(ORDER, 1):
        body += brand_html(k, n)
    body += SHOP + TAKE
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))
    bad = []
    if fin.count('<article class="ind-b') != N: bad.append("brand count")
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
