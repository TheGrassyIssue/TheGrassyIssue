#!/usr/bin/env python3
"""apply-mobile-home.py — tighter homepage on phones (Lenny, 15 Oct 2026: "we need to tighten up the
mobile experience for the homepage"). Idempotent: one <style id="tgi-mobile-home"> block, replaced on
every run, plus a footer markup fix. Runs in Deploy TGI.command after paginate-feed, so a rebuilt
index.html gets it back. Desktop is untouched: every rule sits inside a max-width:640px query.

What it changes on a 390px phone (measured before/after in the commit notes):
  * weather bar: one line, date dropped (it is on the phone already), smaller tee-time button
  * hero: shorter (190px instead of 253px)
  * filters: not sticky, pills scroll sideways instead of being cut off, "Newest" label hidden
  * feed cards: square carousel images instead of 4:5, no arrow buttons on touch (swipe + dots),
    tighter padding, no "1 / 4" counter
  * events: a sideways swipe row of cards instead of a cramped 2-column grid
  * vibe board: 2 columns, first 8 pins (was a 2,000px wall)
  * footer: links in two columns; About / Work With Us / Contact no longer run together
"""
import re
import sys

PATH = "index.html"
MARK = 'id="tgi-mobile-home"'
CSS = """<style id="tgi-mobile-home">/* TGI mobile homepage, 15 Oct 2026 — see apply-mobile-home.py */
@media (max-width:640px){
  .weather-banner{padding:7px 14px!important;gap:10px!important;font-size:9.5px!important;flex-wrap:nowrap!important;justify-content:space-between!important}
  .weather-banner .wb-date,.weather-banner .wb-date+.wb-dot{display:none!important}
  .weather-banner .wb-tee{padding:5px 9px!important;white-space:nowrap;font-size:9.5px!important}
  .hero{height:auto!important;min-height:190px!important;max-height:210px!important}
  .filters{position:static!important;padding:10px 0!important}
  .filters-inner{padding:0 14px!important;gap:10px!important}
  .filter-pills{flex-wrap:nowrap!important;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;min-width:0;flex:1}
  .filter-pills::-webkit-scrollbar{display:none}
  .pill{white-space:nowrap;flex:0 0 auto}
  .sort-select{display:none!important}
  .feed{padding:14px 0 44px!important}
  .gear-slide img{aspect-ratio:1/1!important}
  .feed .card{width:calc(100% - 36px)!important;margin-left:18px!important}
  .card-body{padding:12px 13px 12px!important}
  .card-title{font-size:17px!important;margin-bottom:6px!important}
  .card-text{margin-bottom:6px!important}
  .gear-dots{padding:6px 0 0!important}
  .gear-counter{display:none!important}
  .card-readmore{margin-top:8px!important}
  .events{padding-left:14px!important;padding-right:0!important}
  .events-header{padding-right:14px}
  .events-grid{display:flex!important;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;gap:12px!important;padding-right:14px;scrollbar-width:none}
  .events-grid::-webkit-scrollbar{display:none}
  .event-card{flex:0 0 78%;scroll-snap-align:start}
  .event-img{height:auto!important;aspect-ratio:16/10}
  .event-desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .vibe-grid{column-count:2!important}
  .vibe-pin:nth-child(n+9){display:none!important}
  .footer-inner{grid-template-columns:1fr 1fr!important;gap:26px 18px!important}
  .footer-brand{grid-column:1/-1}
  .footer-bottom{flex-direction:column;gap:6px}
}
@media (max-width:640px) and (hover:none){ .gear-arrow{display:none!important} }
</style>
"""
FOOT_OLD = '<li><a href="/about">About</a><a href="/work-with-us">Work With Us</a><a href="mailto:Lenny@thegrassyissue.com">Contact</a></li>'
FOOT_NEW = ('<li><a href="/about">About</a></li>\n        <li><a href="/work-with-us">Work With Us</a></li>\n'
            '        <li><a href="mailto:Lenny@thegrassyissue.com">Contact</a></li>')


def main(apply_):
    s0 = open(PATH, encoding="utf-8").read()
    s = re.sub(r'<style id="tgi-mobile-home">.*?</style>\n?', "", s0, flags=re.S)
    s = s.replace(FOOT_OLD, FOOT_NEW)
    i = s.rindex("</head>")
    s = s[:i] + CSS + s[i:]
    changed = s != s0
    print(f"apply-mobile-home: {'updated' if changed else 'unchanged'}")
    if apply_ and changed:
        open(PATH, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main("--apply" in sys.argv)
