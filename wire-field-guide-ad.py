#!/usr/bin/env python3
"""wire-field-guide-ad.py — Lenny's own real estate note in the Field Guide (4 Oct 2026).

Lenny: "I want to add an ad for myself in the field guide for people looking for real estate
in Austin or an apartment rental", then "go with A but add my headshot", then "Let's have it automatically just compile a text to me" (button opens a pre-written SMS to his cell), then "also include the link to view listings" (map search on his Papasan site).
Option A (editor's note) from research/field-guide-ad-blocks.py, plus his headshot from his
Papasan agent page. Sits after the five munis, before the "All five, side by side" table.

TREC 535.155: license holder's name + broker's name (Keller Williams) at least half the size of
the largest contact info; links to the TREC IABS and Consumer Protection Notice (his Papasan PDFs).
Idempotent: a rerun replaces the block between the markers. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "field-guide/index.html"
MARK, END = "<!-- TGI-LENNY-RE-NOTE -->", "<!-- /TGI-LENNY-RE-NOTE -->"
SITE = "https://lennyharrington.papasanproperties.com"

BLOCK = f'''{MARK}
<style>
.lre{{max-width:880px;margin:56px auto;padding:0 32px}}
.lre-in{{border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:28px 0 24px;display:grid;grid-template-columns:112px 1fr;gap:28px;align-items:start}}
.lre-img{{width:112px;height:112px;border-radius:50%;object-fit:cover;object-position:center 22%;display:block}}
.lre-k{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:12px}}
.lre-h{{font-family:var(--serif);font-size:34px;line-height:1.1;margin:0 0 12px;font-weight:400}}
.lre-p{{font-family:var(--serif);font-size:18px;line-height:1.55;margin:0 0 16px}}
.lre-btn{{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;background:var(--grass);color:var(--paper)!important;padding:11px 16px;margin-right:14px;border-bottom:none!important;text-decoration:none}}
.lre-btn2{{background:transparent;color:var(--grass)!important;box-shadow:inset 0 0 0 1px var(--grass)}}
.lre-btn{{margin-bottom:8px}}
.lre-tel{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:inherit;border-bottom:none!important;text-decoration:none}}
.lre-c{{font-family:var(--mono);font-size:10px;letter-spacing:.06em;line-height:1.7;opacity:.75;margin-top:18px}}
.lre-c a{{border-bottom:1px solid currentColor;color:inherit;text-decoration:none}}
.lre-b{{font-size:11px;letter-spacing:.1em}}
@media(max-width:640px){{.lre{{padding:0 20px}}.lre-in{{grid-template-columns:1fr;gap:16px}}.lre-img{{width:84px;height:84px}}.lre-h{{font-size:28px}}.lre-p{{font-size:17px}}}}
</style>
<aside class="lre" aria-label="A note from the editor">
 <div class="lre-in">
  <img class="lre-img" src="/images/lenny/headshot.jpg" alt="Lenny Harrington" width="112" height="112" loading="lazy" />
  <div>
   <div class="lre-k">A note from the editor &middot; Lenny&rsquo;s day job</div>
   <p class="lre-h">Moving to Austin for the golf?</p>
   <p class="lre-p">When I&rsquo;m not writing this guide, I&rsquo;m a real estate agent in Austin. If you&rsquo;re buying, selling or looking for an apartment to rent, I&rsquo;ll help you find a place close to the course you&rsquo;ll actually play.</p>
   <a class="lre-btn" href="sms:+19143188472?&amp;body=Hi%20Lenny%2C%20I%20found%20you%20through%20The%20Grassy%20Issue%20Field%20Guide.%20I%27m%20looking%20to%20buy%20%2F%20sell%20%2F%20rent%20in%20Austin." data-goatcounter-click="field-guide-text-lenny">Text Lenny &rarr;</a>
   <a class="lre-btn lre-btn2" href="{SITE}/property-search/results/?searchtype=3" target="_blank" rel="noopener" data-goatcounter-click="field-guide-view-listings">View listings &rarr;</a>
   <a class="lre-tel" href="tel:+19143188472">(914) 318-8472</a>
   <div class="lre-c">
    Lenny Harrington &middot; TX License 795491 &middot; Papasan Properties Group<br>
    <span class="lre-b">KELLER WILLIAMS</span> &middot; 1801 S. MoPac Expy., Ste. 100, Austin<br>
    <a href="{SITE}/res/includes/TREC-IABS.pdf" target="_blank" rel="noopener">Texas Real Estate Commission Information About Brokerage Services</a> &middot;
    <a href="{SITE}/assets/docs/TREC-CPN.pdf" target="_blank" rel="noopener">Texas Real Estate Commission Consumer Protection Notice</a><br>
    This is Lenny&rsquo;s own business. No one paid TGI to run it.
   </div>
  </div>
 </div>
</aside>
{END}
'''

def main(apply_):
    s = PAGE.read_text(encoding="utf-8")
    orig = s
    if MARK in s:
        s = s[:s.index(MARK)] + s[s.index(END) + len(END):].lstrip("\n")
    anchor = s.index("All five, side by side.")
    i = s.rfind("<section", 0, anchor)
    s = s[:i] + BLOCK + s[i:]
    assert s.count(MARK) == 1 and not re.search(r"\bworth\b", BLOCK, re.I)
    assert (ROOT / "images/lenny/headshot.jpg").is_file()
    print("  block placed before the 'All five, side by side' table" + ("" if apply_ else " (dry run — pass --apply)"))
    if apply_ and s != orig:
        PAGE.write_text(s, encoding="utf-8")
        print("  wrote field-guide/index.html")

if __name__ == "__main__":
    main("--apply" in sys.argv)
