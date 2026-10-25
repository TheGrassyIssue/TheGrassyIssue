#!/usr/bin/env python3
"""apply-one-footer.py — one "Keep Reading" section at the foot of every post. 25 Oct 2026.
Lenny (screenshot of Keep Reading + The Brand Index strip + More from TGI): "this section across the site needs to be
streamlined and reduced to one section".
Every post ended with three stacked blocks: the static Keep Reading row (apply-related-links.py, 3 related posts), the
Brand Index strip, and the More from TGI grid (rotate-more-from-tgi.py, 4 cards redrawn by JS). This merges them into one:
  KEEP READING ........................................ EXPLORE ALL BRANDS ->
  [related] [related] [related] [one more post from the old grid]
The three related posts stay first (fixed and crawlable, chosen by shared brands, so the SEO links survive); the fourth
card comes from the post's More from TGI grid. The Brand Index strip becomes the header link. The rotation script tag is
removed from merged pages so the row doesn't reshuffle after load. Runs in Deploy TGI.command AFTER rotate-more-from-tgi.py
and apply-related-links.py (both keep working: they re-add their blocks, this re-merges them). Idempotent. Dry run by default.
"""
import glob, html, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
S, E = "<!-- TGI-ONE-FOOTER -->", "<!-- /TGI-ONE-FOOTER -->"
RS, RE_ = "<!-- TGI-RELATED -->", "<!-- /TGI-RELATED -->"
TAG = '<script src="/assets/js/more-rotate.js" defer></script>'


def div_end(s, i):
    """index just past the </div> that closes the <div ...> starting at i"""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        depth += 1 if m.group() == "<div" else -1
        if depth == 0:
            return i + m.end()
    return -1


def card(href, img, title, cat):
    t = html.escape(html.unescape(title), quote=True)
    return (f'    <a href="{href}" class="more-card">\n'
            f'      <div class="more-card-img"><img src="{img}" alt="{t}" loading="lazy" /></div>\n'
            f'      <div class="more-card-body"><div class="more-card-name">{title}</div><div class="more-card-tag">{cat}</div></div>\n'
            f'    </a>')


def merge(s, self_url):
    rel = []
    m = re.search(re.escape(RS) + r"(.*?)" + re.escape(RE_) + r"\n?", s, re.S)
    if m:
        for a in re.findall(r'<a href="([^"]+)"><img src="([^"]+)"[^>]*/><div class="tgi-rel-c">(.*?)</div><div class="tgi-rel-t">(.*?)</div></a>', m.group(1)):
            rel.append((a[0], a[1], a[3], a[2]))
    old = re.search(re.escape(S) + r".*?" + re.escape(E) + r"\n?", s, re.S)
    if not rel and old:
        return s  # already merged and nothing new to merge
    # cards from any More grid still on the page (the old More from TGI block, or our previous merged row)
    grid_cards = re.findall(r'<a href="([^"]+)" class="more-card">\s*<div class="more-card-img"><img src="([^"]+)"[^>]*/></div>\s*'
                            r'<div class="more-card-body"><div class="more-card-name">(.*?)</div><div class="more-card-tag">(.*?)</div></div>\s*</a>', s, re.S)
    if not rel:
        return s
    taken = {r[0] for r in rel} | {self_url}
    extra = [c for c in grid_cards if c[0] not in taken][:4 - len(rel)]
    cards = [card(*r) for r in rel] + [card(*c) for c in extra]
    block = (f'{S}\n<div class="more" data-tgi="one-footer">\n  <div class="more-hdr">\n    <span class="more-label">Keep Reading</span>\n'
             f'    <a href="/brands" class="more-link">Explore All Brands &rarr;</a>\n  </div>\n  <div class="more-grid">\n'
             + "\n".join(cards) + f'\n  </div>\n</div>\n{E}\n')
    # remove the pieces being merged
    if old:
        s = s[:old.start()] + s[old.end():]
    first = s.index(RS) if RS in s else None
    s = re.sub(re.escape(RS) + r".*?" + re.escape(RE_) + r"\n?", "", s, flags=re.S)
    for pat in (r'<div class="more" data-brandindex="1">', r'(?:<!-- More from the Feed -->\s*)?<div class="more">'):
        while True:
            mm = re.search(pat, s)
            if not mm:
                break
            start = mm.start()
            j = div_end(s, s.index("<div", mm.start()))
            if j < 0:
                break
            s = s[:start] + s[j:].lstrip("\n")
    at = first if first is not None and first <= len(s) else s.find('<footer')
    if at < 0:
        return None
    s = s[:at] + block + s[at:]
    s = s.replace(TAG + "\n", "").replace(TAG, "")
    return s


def main(apply_):
    changed = total = 0
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in ("research", "drafts", "previews", ".git") or re.search(r" \d+\.html$", rel):
            continue
        try:
            s = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        if RS not in s and S not in s:
            continue
        total += 1
        url = "/" + rel[:-5] if rel.endswith(".html") else "/" + rel
        new = merge(s, url)
        if new and new != s:
            changed += 1
            if apply_:
                open(f, "w", encoding="utf-8").write(new)
    print(f"apply-one-footer: {total} page(s) with a footer row, {changed} {'merged' if apply_ else 'would merge'}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
