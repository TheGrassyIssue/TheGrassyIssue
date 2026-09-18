#!/usr/bin/env python3
"""
add-merrill-card.py — the Brand Revisited feed card for Merrill Golf.
18 September 2026. Idempotent.

Built on the exact markup of the Devereux and Radry Revisited cards already in
the feed, so it inherits the gear-carousel behaviour rather than reinventing it.
Six slides, the ones Lenny approved, in the order that tells the story: the polo
we said they would never make, then the range that grew around it, then the
Japanese-made covers.

Prices read off merrillgolf.com on 18 September 2026.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
IDX  = ROOT / "index.html"
KEY  = "merrillrevisited1"
MARK = "<!-- BRAND REVISITED — Merrill Golf -->"
POST = "/drops/brand-to-know-merrill-golf"
SHOP = "https://merrillgolf.com/products/"

SLIDES = [
 ("birds-stripe-polo-navy-white","01-birds-stripe-polo",
  "Birds Stripe Polo &middot; $65","Merrill Golf Birds Stripe Polo in Navy and White"),
 ("work-jacket-sky-blue","04-work-jacket",
  "Work Jacket &middot; Sky Blue &middot; $150","Merrill Golf Work Jacket in Sky Blue"),
 ("palmer-cardigan-fire-red","06-palmer-red",
  "Palmer Cardigan &middot; $160","Merrill Golf Palmer Cardigan in Fire Red"),
 ("baggy-trousers-black","08-baggy-trousers",
  "Baggy Trousers &middot; $125","Merrill Golf Baggy Trousers in Black"),
 ("golf-company-tee-vintage-green","13-golfco-tee-green",
  "Golf Company Tee &middot; $55","Merrill Golf Golf Company Tee in Vintage Green"),
 ("headcovers-olive-green","17-headcovers-olive",
  "Headcovers &middot; $110","Merrill Golf Headcovers in Olive Green"),
]

LEAD = ("Birds Stripe Polo &mdash; the piece that undoes our own first sentence "
        "about this brand. Short sleeve, three buttons, in a cotton jersey Merrill "
        "custom-dyes, with the mark embroidered at the chest. $65.")


def slide(handle, stem, name, alt):
    return f'''          <div class="gear-slide">
            <a href="{SHOP}{handle}" target="_blank" rel="noopener">
              <img src="/images/merrill-golf/{stem}.jpg" alt="{alt}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">Merrill Golf</div><div class="gear-slide-name">{name}</div></div>
            </a>
          </div>
'''


def card():
    return f'''{MARK}
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{"".join(slide(*s) for s in SLIDES)}        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{POST}" style="color:inherit;text-decoration:none;border-bottom:none;">Brand Revisited &mdash; Merrill Golf, and the Polo They Never Made</a></div>
      <div class="card-text" data-slidetext="{KEY}">{LEAD}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <div class="card-source"><a href="https://merrillgolf.com" target="_blank" rel="noopener">merrillgolf.com</a></div>
      <a href="{POST}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>
    </div>
  </div>

'''


def run(apply_):
    html = IDX.read_text(encoding="utf-8")
    if MARK in html:
        html = re.sub(re.escape(MARK) + r".*?(?=<!-- )", card(), html, flags=re.S)
        how = "replaced existing card"
    else:
        anchor = "<!-- BRAND REVISITED — Devereux Golf -->"
        if anchor not in html:
            sys.exit("! anchor card not found — refusing to guess where the card goes")
        html = html.replace(anchor, card() + "  " + anchor, 1)
        how = "inserted above the Devereux Revisited card"

    checks = [
      ("exactly one Merrill card", html.count(MARK) == 1, ""),
      (f"{len(SLIDES)} slides", html.count(f'data-carousel="{KEY}"') == 1
       and card().count("gear-slide\">") == len(SLIDES), ""),
      ("every slide image exists",
       all((ROOT / f"images/merrill-golf/{s[1]}.jpg").exists() for s in SLIDES), ""),
      ("every img has alt", all('alt="' in i for i in re.findall(r"<img[^>]*>", card())), ""),
      ("carousel key is unique",
       html.count(f'data-carousel="{KEY}"') == 1
       and html.count(f'data-slidetext="{KEY}"') == 1
       and html.count(f'data-dots="{KEY}"') == 1
       and html.count(f'data-counter="{KEY}"') == 1, ""),
      ("no banned word", "worth" not in card().lower(), ""),
      ("div tags balance in the card",
       card().count("<div") == card().count("</div>"), ""),
    ]
    ok = True
    for l, p_, d in checks:
        print(f"  {'OK  ' if p_ else 'FAIL'} {l} {d}"); ok &= p_
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {how}")
    if apply_:
        IDX.write_text(html, encoding="utf-8"); print("  written")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    run("--apply" in sys.argv)
