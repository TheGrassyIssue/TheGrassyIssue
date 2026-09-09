#!/usr/bin/env python3
"""Pick which feed card is the homepage lead (the full-width story above the filters).

    python3 set-lead.py <post-slug> [--img /images/...] --apply

Replaces the <section class="lead"> that apply-cleaner.py created, un-hides the
previous lead's source card (removes is-lead-source + the inline display:none) and
hides the new one the same way. Inline display:none is deliberate: layoutMasonry
measures visibleCards[0].offsetWidth and a class-hidden card still counts.
--img overrides the lead photo (defaults to the card's first slide). Dry-run default.
"""
import re, sys

SRC = "index.html"


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def main(slug, img_override=None, apply_=False):
    doc = open(SRC, encoding="utf-8").read()
    assert '<section class="lead"' in doc, "no lead section — run apply-cleaner.py first"

    # 1. restore the current source card
    doc, n = re.subn(r'<div class="card is-lead-source" data-type="(\w+)" style="display:none">',
                     r'<div class="card" data-type="\1">', doc)
    assert n == 1, f"expected 1 lead source, found {n}"

    # 2. find the target card (card whose title link is the slug)
    href = f"/drops/{slug}"
    fi = doc.index('class="feed"')
    starts = [m.start() + fi for m in re.finditer(r'<div class="card" data-type="\w+">', doc[fi:])]
    # bound each chunk at the NEXT card start — a fixed 20 KB window once ran past
    # a short card and matched the title of the card after it (coffee shops became
    # the lead instead of the NY trip)
    target = None
    for i, s in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else s + 20000
        if re.search(r'<div class="card-title"><a href="' + re.escape(href) + '"', doc[s:end]):
            target, tend = s, end; break
    assert target is not None, f"no card with title link {href}"
    m = re.match(r'<div class="card" data-type="(\w+)">', doc[target:])
    card = doc[target:tend]
    img = img_override or re.search(r'<img[^>]+src="([^"]+)"', card).group(1)
    tag = re.search(r'<span class="card-tag[^"]*">(.*?)</span>', card, re.S)
    ttl = re.search(r'<div class="card-title">\s*<a href="([^"]+)"[^>]*>(.*?)</a>', card, re.S)
    txt = re.search(r'<(?:p|div) class="card-text"[^>]*>(.*?)</(?:p|div)>', card, re.S)
    lnk = re.search(r'<a href="([^"]+)" class="card-link"[^>]*>(.*?)</a>', card, re.S)
    assert tag and ttl and txt and lnk, (bool(tag), bool(ttl), bool(txt), bool(lnk))
    assert re.search(r'src="' + re.escape(img) + '"', doc), f"{img} not referenced anywhere in index.html"

    lead = f'''<section class="lead" id="lead">
  <div class="lead-img"><img src="{img}" alt=""></div>
  <div class="lead-body">
    <span class="card-tag grass">{strip_tags(tag.group(1))}</span>
    <div class="lead-title"><a href="{ttl.group(1)}">{ttl.group(2).strip()}</a></div>
    <div class="lead-text">{strip_tags(txt.group(1))}</div>
    <a href="{lnk.group(1)}" class="card-link">{lnk.group(2).strip()}</a>
  </div>
</section>'''

    # 3. hide the target, swap the lead
    doc = (doc[:target] + f'<div class="card is-lead-source" data-type="{m.group(1)}" style="display:none">'
           + doc[target + len(m.group(0)):])
    doc, n = re.subn(r'<section class="lead" id="lead">.*?</section>', lambda _: lead, doc, count=1, flags=re.S)
    assert n == 1

    print(f"lead -> {strip_tags(ttl.group(2))}\nimage: {img}")
    if apply_:
        open(SRC, "w", encoding="utf-8").write(doc); print("written")
    else:
        print("(dry run — pass --apply)")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    img = sys.argv[sys.argv.index("--img") + 1] if "--img" in sys.argv else None
    main(a[0], img, "--apply" in sys.argv)
