#!/usr/bin/env python3
"""paginate-feed.py — keep the homepage light without changing how the feed feels.

1 October 2026. Lenny: "I think the homepage is getting too large, what can we do to keep the file
size low", then "Let'd do Feed pagination - will it keep the style of a continuous feed on the homepage?"

index.html had all ~238 feed cards (1.36 MB of HTML, 277 KB of it carousel captions). This keeps the
newest KEEP cards in index.html and moves the rest, with their carousel captions and any inline card
scripts, into /feed/page-2.html, /feed/page-3.html ... (PER cards each). The homepage script fetches the
next page when the reader clicks Load more (no infinite scroll, per Lenny 1 Oct 2026); the button is a
real link, so crawlers can follow it. Filter pills load every page before filtering.

IDEMPOTENT and SAFE TO RE-RUN. Each run first MERGES: the cards still in index.html (including any new
card a wire-*-home.py script just put in slot 1) followed by every card already in /feed/page-*.html,
de-duplicated by the post each card links to (first occurrence wins, so a re-wired card moves to the top).
Then it re-splits. Run with --merge to write the full single-file feed back into index.html.

Runs in Deploy TGI.command right after field-notes-red.py. Dry run by default.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
FEED_DIR = ROOT / "feed"
MANIFEST = FEED_DIR / "pages.json"
KEEP = 24
PER = 24
FEED_OPEN = re.compile(r'<section class="feed"[^>]*>\n?')
LOADMORE = re.compile(r'\n?\s*<div class="load-more" id="loadMore"[^>]*>.*?</div>\n', re.S)
JS_MARK = "/*TGI-FEED-PAGED-V2*/"


# ---------------------------------------------------------------- feed units
def units_of(body):
    """Split feed HTML into contiguous slices, one per top-level card. A slice starts at the opening
    comment(s) right before a top-level <div class="card ..."> (or at the div itself) and runs to the next
    slice, so trailing inline scripts, closing marker comments and any stray markup ride with their card
    and joining the slices reproduces the original HTML exactly."""
    tok = re.compile(r"<div\b[^>]*>|</div>|<script\b.*?</script>|<!--.*?-->", re.S)
    starts, depth, pending = [], 0, None
    for m in tok.finditer(body):
        t = m.group(0)
        if depth == 0:
            if t.startswith("<!--") and not (t.startswith("<!-- /") or t.startswith("<!--/")):
                if pending is None:
                    pending = m.start()
            elif re.match(r'<div class="card(?:\s[^"]*)?"', t):
                starts.append(pending if pending is not None else m.start())
                pending = None
            else:
                pending = None
        if t.startswith("<div"):
            depth += 1
        elif t.startswith("</div"):
            depth = max(0, depth - 1)
    if not starts:
        return []
    starts[0] = 0
    bounds = starts + [len(body)]
    return [body[bounds[i]:bounds[i + 1]] for i in range(len(starts))]


def unit_key(u):
    m = re.search(r"<!--\s*(TGI-[A-Z0-9-]+)\s*-->", u)
    return m.group(1) if m else u.strip()


def carousel_keys(u):
    return re.findall(r'data-carousel="([\w-]+)"', u)


# ---------------------------------------------------------- slide-text map
def find_map(s):
    i = s.find("window._slideTexts = {")
    if i < 0:
        return None
    j = i + len("window._slideTexts = {")
    depth, k, q = 1, j, None
    while k < len(s):
        c = s[k]
        if q:
            if c == "\\": k += 2; continue
            if c == q: q = None
        elif c in "\"'`": q = c
        elif c in "{[": depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return i, j, k  # map text is s[j:k]
        k += 1
    return None


def split_entries(text):
    """'  key: [ ... ],' entries -> ordered list of (key, entry_source_without_trailing_comma)."""
    out, k = [], 0
    rx = re.compile(r'\s*["\']?([\w-]+)["\']?\s*:\s*\[')
    while True:
        m = rx.match(text, k)
        if not m:
            break
        depth, p, q = 1, m.end(), None
        while p < len(text):
            c = text[p]
            if q:
                if c == "\\": p += 2; continue
                if c == q: q = None
            elif c in "\"'`": q = c
            elif c == "[": depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    break
            p += 1
        out.append((m.group(1), text[m.start():p + 1].strip()))
        k = p + 1
        c = re.match(r"\s*,", text[k:])
        if c: k += c.end()
    return out


# ------------------------------------------------------------- fragments
def page_doc(n, units, texts, nxt):
    st = ""
    if texts:
        st = ("<script>window._slideTexts=window._slideTexts||{};Object.assign(window._slideTexts,{\n"
              + ",\n".join(texts) + "\n});</script>\n")
    more = (f'<p class="feed-next"><a href="{nxt}" rel="next">Older posts &rarr;</a></p>\n' if nxt else "")
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\" />\n"
            f"<title>The Grassy Issue — the feed, page {n}</title>\n"
            "<meta name=\"robots\" content=\"noindex,follow\" />\n"
            # self-canonical (SEO audit 4 Oct 2026): these pages are not copies of the homepage
            f"<link rel=\"canonical\" href=\"https://thegrassyissue.com/feed/page-{n}\" />\n</head>\n<body>\n"
            "<!-- Feed page fragment, written by paginate-feed.py. The homepage fetches this and moves the cards\n"
            "     inside .feed-page into its own feed. Edit cards on the homepage source, not here. -->\n"
            f"<p><a href=\"/\">The Grassy Issue</a></p>\n<div class=\"feed-page\" data-page=\"{n}\">\n"
            + "".join(units) + "\n<!--/feed-page-->\n</div>\n" + st + more + "</body>\n</html>\n")


def read_pages():
    if not MANIFEST.exists():
        return [], []
    units, entries = [], []
    for name in json.loads(MANIFEST.read_text())["pages"]:
        h = (FEED_DIR / name).read_text(encoding="utf-8")
        a = h.index('<div class="feed-page"'); a = h.index(">", a) + 1
        b = h.index("<!--/feed-page-->")
        units += units_of(h[a:b])
        m = re.search(r"Object\.assign\(window\._slideTexts,\{\n(.*?)\n\}\);</script>", h, re.S)
        if m:
            entries += split_entries(m.group(1))
    return units, entries


# --------------------------------------------------------------- JS patch
def patch_css(s):
    if ".load-more a {" in s or ".load-more button, .load-more a" in s:
        return s
    s = s.replace("  .load-more button {", "  .load-more a { display: inline-block; text-decoration: none; border-bottom: 0.5px solid var(--ink); }\n  .load-more button, .load-more a {", 1)
    s = s.replace("  .load-more button:hover {", "  .load-more button:hover, .load-more a:hover {", 1)
    return s


def patch_js(s):
    # keep the Load more button on screen while older pages remain to fetch
    a = "loadMoreBtn.style.display = overflowCards.length > 0 ? '' : 'none';"
    if a in s:
        s = s.replace(a, "loadMoreBtn.style.display = (overflowCards.length > 0 || loadMoreBtn.dataset.next) ? '' : 'none';")
    if JS_MARK in s:
        return s
    if "/*TGI-FEED-PAGED-V1*/" in s:  # replace the first version of the loader block wholesale
        i = s.index("/*TGI-FEED-PAGED-V1*/"); k = s.index("\n  })();\n", i) + len("\n  })();\n")
        s = s[:i] + s[k:]
        return insert_loader(s)
    reps = [
        # filters: query cards live, and load every page before filtering
        ("""    pill.addEventListener('click', () => {
      pills.forEach(p => {""",
         """    pill.addEventListener('click', async () => {
      if (pill.dataset.filter !== 'all' && window.tgiLoadAllPages) await window.tgiLoadAllPages();
      pills.forEach(p => {"""),
        ("""      cardsShown = CARDS_PER_PAGE; // reset pagination on filter change
      cards.forEach(card => {""",
         """      cardsShown = CARDS_PER_PAGE; // reset pagination on filter change
      document.querySelectorAll('.feed .card').forEach(card => {"""),
        # carousels: initialise each one once, so fetched cards can be initialised later
        ("""    document.querySelectorAll('.gear-carousel').forEach(carousel => {
      const id = carousel.dataset.carousel;""",
         """    document.querySelectorAll('.gear-carousel').forEach(carousel => {
      if (carousel.dataset.ready) return; carousel.dataset.ready = '1';
      const id = carousel.dataset.carousel;"""),
        ("""  // Touch/swipe support for gear carousels
  document.querySelectorAll('.gear-carousel').forEach(carousel => {
    let startX = 0;""",
         """  // Touch/swipe support for gear carousels
  function initTouch() { document.querySelectorAll('.gear-carousel').forEach(carousel => {
    if (carousel.dataset.touch) return; carousel.dataset.touch = '1';
    let startX = 0;"""),
    ]
    for a, b in reps:
        if a not in s:
            sys.exit("! homepage script changed shape; could not find:\n" + a[:120])
        s = s.replace(a, b, 1)
    # close the initTouch wrapper: the touch block ends with '      diff = 0;\n    });\n  });'
    a = "      diff = 0;\n    });\n  });\n"
    i = s.index("function initTouch()")
    k = s.index(a, i)
    s = s[:k] + "      diff = 0;\n    });\n  }); }\n  initTouch();\n" + s[k + len(a):]
    return insert_loader(s)


def insert_loader(s):
    loader = JS_MARK + """
  // --- Paged feed (paginate-feed.py): fetch older cards as the reader nears the bottom ---
  (function () {
    const lm = document.getElementById('loadMore');
    let busy = false;
    function nextUrl() { return lm ? lm.dataset.next || '' : ''; }
    async function fetchPage() {
      const url = nextUrl(); if (!url || busy) return false; busy = true;
      try {
        const r = await fetch(url); if (!r.ok) return false;
        const doc = new DOMParser().parseFromString(await r.text(), 'text/html');
        const page = doc.querySelector('.feed-page'); const feed = document.querySelector('.feed');
        if (!page || !feed) return false;
        const fresh = [];
        Array.from(page.childNodes).forEach(n => {
          let node = n;
          if (n.nodeName === 'SCRIPT') { node = document.createElement('script'); node.textContent = n.textContent; }
          else { node = document.importNode(n, true); }
          feed.insertBefore(node, lm);
          if (node.classList && node.classList.contains('card')) fresh.push(node);
        });
        doc.querySelectorAll('body > script').forEach(sc => { const x = document.createElement('script'); x.textContent = sc.textContent; document.body.appendChild(x); });
        const nx = doc.querySelector('.feed-next a');
        lm.dataset.next = nx ? nx.getAttribute('href') : '';
        const a = lm.querySelector('a'); if (a) { if (lm.dataset.next) a.href = lm.dataset.next; }
        initGearCarousels(); initTouch();
        const pill = document.querySelector('.pill.active');
        const f = pill ? pill.dataset.filter : 'all';
        fresh.forEach(c => {
          if (f !== 'all' && c.dataset.type !== f) { c.classList.add('hidden'); c.style.display = 'none'; }
          observer.observe(c);
          c.querySelectorAll('img').forEach(img => img.addEventListener('load', layoutMasonry));
        });
        return true;
      } catch (e) { return false; } finally { busy = false; }
    }
    window.tgiLoadAllPages = async function () { while (nextUrl()) { if (!(await fetchPage())) break; } layoutMasonry(); };
    const show = window.loadMoreCards;
    window.loadMoreCards = async function (ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      const hiddenLeft = document.querySelectorAll('.feed .card.card-overflow:not(.hidden)').length;
      if (hiddenLeft < CARDS_PER_PAGE && nextUrl()) await fetchPage();
      show();
    };
    // No infinite scroll (1 Oct 2026, Lenny: "I don't love the endless scroll, can we go back to the load more style?").
    // Older cards load only when the reader clicks Load more.
  })();
/*/TGI-FEED-PAGED*/
"""
    anchor = "  initTouch();\n"
    k = s.index(anchor) + len(anchor)
    return s[:k] + loader + s[k:]


# ------------------------------------------------------------------- main
def main(apply_, merge_only):
    s = HOME.read_text(encoding="utf-8")
    m = FEED_OPEN.search(s)
    lmm = LOADMORE.search(s, m.end())
    if not m or not lmm:
        sys.exit("! could not find the feed section or the load-more block")
    body = s[m.end():lmm.start()]
    home_units = units_of(body)
    page_units, page_entries = read_pages()
    seen, units = set(), []
    for u in home_units + page_units:
        k = unit_key(u)
        if k in seen:
            continue
        seen.add(k); units.append(u)

    mp = find_map(s)
    entries = split_entries(s[mp[1]:mp[2]])
    have = {k for k, _ in entries}
    entries += [(k, e) for k, e in page_entries if k not in have]
    by_key = dict(entries)

    keep, rest = (units, []) if merge_only else (units[:KEEP], units[KEEP:])
    rest_keys = {k for u in rest for k in carousel_keys(u)}
    home_entries = [e for k, e in entries if k not in rest_keys]
    pages = [rest[i:i + PER] for i in range(0, len(rest), PER)]
    names = [f"page-{n + 2}.html" for n in range(len(pages))]

    new_body = "".join(keep)
    nxt = f"/feed/{names[0]}" if names else ""
    lm_html = (f'\n  <div class="load-more" id="loadMore" data-next="{nxt}">\n'
               f'    <a href="{nxt or "/"}" onclick="loadMoreCards(event)" class="load-more-link">Load more &rarr;</a>\n'
               f'  </div>\n')
    map_txt = "\n" + ",\n".join("    " + e for e in home_entries) + "\n  "
    s2 = s[:mp[1]] + map_txt + s[mp[2]:]
    m = FEED_OPEN.search(s2); lmm = LOADMORE.search(s2, m.end())
    s2 = s2[:m.end()] + new_body + lm_html + s2[lmm.end():]
    if not merge_only:
        s2 = patch_css(patch_js(s2))

    print(f"  cards: {len(units)} total ({len(home_units)} on the homepage now, {len(page_units)} in pages) "
          f"-> {len(keep)} on the homepage, {len(rest)} across {len(pages)} page(s)")
    print(f"  index.html {len(s):,} -> {len(s2):,} bytes; captions kept {len(home_entries)}, moved {len(rest_keys & set(by_key))}")
    if not apply_:
        print("  dry run — pass --apply"); return

    FEED_DIR.mkdir(exist_ok=True)
    for old in FEED_DIR.glob("page-*.html"):
        old.unlink()
    for i, (name, us) in enumerate(zip(names, pages)):
        ks = [k for u in us for k in carousel_keys(u)]
        texts = [by_key[k] for k in dict.fromkeys(ks) if k in by_key]
        (FEED_DIR / name).write_text(page_doc(i + 2, us, texts, f"/feed/{names[i + 1]}" if i + 1 < len(names) else ""), encoding="utf-8")
    if names:
        MANIFEST.write_text(json.dumps({"pages": names}, indent=1))
    elif MANIFEST.exists():
        MANIFEST.unlink()
    HOME.write_text(s2, encoding="utf-8")

    # verify: every card is somewhere exactly once
    back_units, _ = read_pages()
    fin = HOME.read_text(encoding="utf-8")
    fm = FEED_OPEN.search(fin); fl = LOADMORE.search(fin, fm.end())
    now = [unit_key(u) for u in units_of(fin[fm.end():fl.start()]) + back_units]
    if sorted(now) != sorted(unit_key(u) for u in units) or len(now) != len(set(now)):
        HOME.write_text(s, encoding="utf-8")
        sys.exit("! card check failed — index.html restored")
    print(f"  wrote index.html and {len(names)} feed page(s)")


if __name__ == "__main__":
    main("--apply" in sys.argv, "--merge" in sys.argv)
