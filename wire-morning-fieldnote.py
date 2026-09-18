#!/usr/bin/env python3
"""wire-morning-fieldnote.py — feed card + sitemap for The Morning Round. Idempotent."""
import pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parent
IDX=ROOT/"index.html"; SM=ROOT/"sitemap.xml"
SLUG="/drops/the-morning-round-austin-cafes-and-lunch"
MARK="<!-- FIELD NOTES — The Morning Round -->"
KEY="morninground1"
SLIDES=[("medici-roasting","Medici Roasting &middot; West Lynn","Opens 6am &mdash; the earliest door we verified"),
        ("houndstooth","Houndstooth &middot; North Lamar","Opens 6:30am daily"),
        ("la-la-land","La La Land &middot; Burnet","New in June &mdash; opens 6:30am"),
        ("flat-track","Flat Track &middot; E Cesar Chavez","Opens 7am daily"),
        ("high-road","High Road Deli &amp; Bar","Lunch after &mdash; 9am to 10pm"),
        ("parish-barbecue","Parish Barbecue","Bib Gourmand &mdash; Thursday to Sunday")]
LEAD=("Ten Austin coffee rooms sorted by the only thing that matters at 6am &mdash; when the "
      "door actually opens &mdash; with every hour read off the venue&rsquo;s own website. "
      "Then four places to eat when you walk off.")
def card():
    sl="".join(f'''          <div class="gear-slide">
            <a href="{SLUG}">
              <img src="/images/austin-morning/{i}.jpg" alt="{re.sub(r"&[a-z]+;","",n)}, Austin" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{n}</div><div class="gear-slide-name">{d}</div></div>
            </a>
          </div>
''' for i,n,d in SLIDES)
    return f'''{MARK}
  <div class="card" data-type="fieldnote">
    <div class="card-media" style="position:relative;">
      <span class="card-tag">[Field Notes]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{sl}        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">The Morning Round &mdash; 10 Austin Cafés Before the Tee, 4 Lunches After</a></div>
      <div class="card-text" data-slidetext="{KEY}">{LEAD}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <div class="card-source">Hours read 18 September 2026</div>
      <a href="{SLUG}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>
    </div>
  </div>

'''
def run(a):
    h=IDX.read_text(encoding="utf-8")
    if MARK in h:
        h=re.sub(re.escape(MARK)+r".*?(?=<!-- )",card(),h,flags=re.S); how="replaced"
    else:
        first=re.search(r'<!-- [^>]{3,70} -->\s*<div class="card"',h)
        h=h[:first.start()]+card()+"  "+h[first.start():]; how="inserted at top of feed"
    ck=[("one card",h.count(MARK)==1),
        ("6 slides",card().count('class="gear-slide"')==6),
        ("images exist",all((ROOT/f"images/austin-morning/{i}.jpg").exists() for i,_,_ in SLIDES)),
        ("alt on every img",all('alt="' in x for x in re.findall(r"<img[^>]*>",card()))),
        ("carousel key unique",h.count(f'data-carousel="{KEY}"')==1),
        ("divs balance",card().count("<div")==card().count("</div>"))]
    ok=True
    for l,p_ in ck: print(f"  {'OK  ' if p_ else 'FAIL'} {l}"); ok&=p_
    if not ok: sys.exit("! refusing")
    sm=SM.read_text(encoding="utf-8")
    if SLUG not in sm:
        sm=sm.replace("</urlset>",f"  <url><loc>https://thegrassyissue.com{SLUG}</loc>"
                                  f"<lastmod>2026-09-18</lastmod></url>\n</urlset>")
        print("  OK   sitemap row added")
    else: print("  OK   sitemap already has it")
    print(f"\n  card {how}")
    if a: IDX.write_text(h,encoding="utf-8"); SM.write_text(sm,encoding="utf-8"); print("  written")
    else: print("  dry run")
if __name__=="__main__": run("--apply" in sys.argv)
