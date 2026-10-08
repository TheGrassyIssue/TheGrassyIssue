#!/usr/bin/env python3
"""apply-agronomy-refresh.py — formatting and image refresh for the Agronomy Workshop post. 8 Oct 2026.
Lenny: "give this page a refresh on the formatting and images- don't change any of the writing or product choices".

Writing and the twelve product cards are untouched. What changes:
  * each card's single image becomes a swipe gallery (on-model/IRL frame first, then the flat, then details),
    from Agronomy Workshop's own store photography (research/agronomy-refresh/frames.json), 1000x1250 frames with
    white studio backgrounds softened to the TGI gradient;
  * the three product grids centre their last row instead of leaving a hole (5 shirts, 5 hats, 2 towels);
  * gallery CSS + JS added (same as the Brand to Know pages).
Idempotent (marked blocks). NOTE: build-agronomy.py predates this; rerunning it would undo the refresh, so rerun
this script after it. Dry run by default.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no.html")
FR = json.load(open(os.path.join(ROOT, "research/agronomy-refresh/frames.json")))
CSS = ('<style id="tgi-ag-refresh">.product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}'
 '.pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}'
 '.pg-track::-webkit-scrollbar{display:none}.pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}'
 '.pg-frame img{width:100%;height:100%;object-fit:cover;display:block}'
 '.pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:.5px solid var(--ink);background:var(--paper);color:var(--ink);font-size:17px;line-height:1;cursor:pointer;opacity:.85;z-index:2}'
 '.pg-arw.prev{left:8px}.pg-arw.next{right:8px}.pg-arw:hover{opacity:1}'
 '.pg-count{position:absolute;top:8px;right:8px;font-family:var(--mono);font-size:9px;letter-spacing:.1em;background:var(--paper);border:.5px solid var(--ink);padding:2px 6px;z-index:2}'
 '.pg-dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:5px;z-index:2}'
 '.pg-dot{width:6px;height:6px;border-radius:50%;border:.5px solid var(--ink);background:var(--paper);padding:0;cursor:pointer;opacity:.55}'
 '.pg-dot.on{background:var(--ink);opacity:1}'
 '.products-grid[data-ag=flex]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
 '.products-grid[data-ag=flex]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
 '@media(max-width:820px){.products-grid[data-ag=flex]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
 '@media(max-width:480px){.products-grid[data-ag=flex]>.product-card{flex-basis:100%}}</style>')


LAYOUT_CSS = ('<style id="tgi-ag-layout">'
 '.drop-header{text-align:center}.drop-header h1{margin-left:auto;margin-right:auto}'
 '.drop-header .drop-meta{justify-content:center}.drop-header .drop-tag{margin-bottom:18px}'
 '.writeup{grid-template-columns:1fr;justify-items:center;gap:32px}'
 '.writeup-body{max-width:760px;margin:0 auto;text-align:center}'
 'section[data-btk="take"]{display:grid;grid-template-columns:minmax(0,1fr) 300px;column-gap:56px;max-width:1400px;margin:0 auto;padding-top:34px;padding-bottom:48px}'
 'section[data-btk="take"] .writeup-body{max-width:760px;margin:0 auto 0 0;text-align:left;font-size:17px}'
 'section[data-btk="take"] .drop-tag{margin-left:0;margin-right:auto}'
 'section[data-btk="take"] .sidebar{position:sticky;top:88px;align-self:start}'
 '@media(max-width:1000px){section[data-btk="take"]{grid-template-columns:1fr;row-gap:28px}section[data-btk="take"] .sidebar{position:static;max-width:760px}}'
 '.writeup .sidebar{width:100%;max-width:420px;text-align:left}'
 '.products-hdr,.sec-note,.btk-wild-credit{text-align:center}.sec-note{max-width:760px;margin-left:auto;margin-right:auto}'
 '.q-list,.faq{max-width:760px;margin-left:auto;margin-right:auto;text-align:center}'
 '.faq-q summary{list-style:none;cursor:pointer}.faq-q summary::-webkit-details-marker{display:none}'
 '.ag-faq-sub{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin:40px 0 4px;text-align:center}'
 '.pull-quote-inner{margin:0 auto;text-align:center;color:var(--grass);border-top:.5px solid rgba(20,20,20,.15);border-bottom:.5px solid rgba(20,20,20,.15)}'
 '.pull-quote-inner:before{display:none!important}'
 '.pull-quote-attr{margin-left:auto;margin-right:auto}</style>')

def pq(text, attr):
    return (f'<!--AG-PQ--><div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div><!--/AG-PQ-->\n\n')

def layout(s):
    """Lenny, 8 Oct: tag in a weird spot, centre all text, one section for the Five Questions + FAQ,
    quotes in the usual pull-quote format, and label the TGI Take. Wording untouched."""
    # 1. Brand Revisited tag: from loose above the header into the header, above the h1
    s = s.replace('<div class="drop-tag grass">Brand Revisited</div>\n\n<header class="drop-header">',
                  '<header class="drop-header">\n  <div class="drop-tag grass">Brand Revisited</div>')
    # 2. label the TGI Take (the opening essay, the one with the sidebar)
    if '<!--AG-TAKE-->' not in s:
        s = s.replace('<div class="writeup">\n  <div class="writeup-body">\n    <p><strong>The moodboard',
                      '<div class="writeup">\n  <div class="writeup-body">\n    <!--AG-TAKE--><div class="drop-tag grass">The TGI Take</div>\n    <p><strong>The moodboard', 1)
    # 2b. the opening essay + info box follow the Brand to Know template: take section, info box on the right
    if '<section class="products" data-btk="take">' not in s:
        i = s.index('<!--AG-TAKE-->')
        st = s.rfind('<div class="writeup">', 0, i)
        en = s.index('</aside>', i) + len('</aside>')
        close = s.index('</div>', en)
        block = s[st:close + len('</div>')]
        inner = block[len('<div class="writeup">'):-len('</div>')]
        s = s[:st] + '<section class="products" data-btk="take">' + inner + '</section>' + s[close + len('</div>'):]
    # 2c. the essay's second half ("There is a through-line...") continues in the take column, as in the template
    if '<!--AG-TAKE2-->' not in s:
        t = s.index('<section class="products" data-btk="take">')
        te = s.index('</section>', t)
        w = s.index('<div class="writeup">', te)
        assert s[te + len('</section>'):w].strip() == '', "unexpected content between take and second write-up"
        wb = s.index('<div class="writeup-body">', w) + len('<div class="writeup-body">')
        we = s.index('</div>', wb)
        paras = s[wb:we]
        wend = s.index('</div>', we + 6) + len('</div>')
        s = s[:te + len('</section>')] + s[wend:]
        aside = s.index('<aside class="sidebar">', t)
        body_end = s.rfind('</div>', t, aside)
        s = s[:body_end] + '<!--AG-TAKE2-->' + paras.rstrip() + '\n  ' + s[body_end:]
    # 3. pull quotes (brand's own words, already quoted on the page), between the product sections
    s = re.sub(r'<!--AG-PQ-->.*?<!--/AG-PQ-->\n\n', '', s, flags=re.S)
    def before(hdr, block):
        nonlocal s
        i = s.index(f'<h2 class="products-hdr">{hdr}</h2>')
        j = s.rfind('<section class="products">', 0, i)
        s = s[:j] + block + s[j:]
    before('The Work Shirt &mdash; 5', pq("Designed to last and get better with age.", "Agronomy Workshop, on the Work Shirt"))
    before('The Hats &mdash; 5', pq("Does everything need to be so obvious?", "Agronomy Workshop, questions asked before designing a golf shirt"))
    before('The Towel &mdash; 2', pq("Won&rsquo;t improve your lies.", "Agronomy Workshop, on the Unusual Lies towel"))
    # 4. one section: the Five Questions + the FAQ (FAQ details, ids and schema unchanged)
    if '<!--AG-QFAQ-->' not in s:
        qs = s.index('<section class="products">\n  <h2 class="products-hdr">The Five Questions</h2>')
        qe = s.index('</section>', qs) + len('</section>')
        qsec = s[qs:qe]
        mid_s = qe
        fs = s.index('<section class="products">\n  <h2 class="products-hdr" id="faq">')
        fe = s.index('</section>', fs) + len('</section>')
        between = s[mid_s:fs]                     # the "answers are checkable" write-up
        faq_inner = re.search(r'<div class="faq">.*?</div>\n', s[fs:fe], re.S).group(0)
        qlist = re.search(r'<div class="sec-note">.*?</ol>', qsec, re.S).group(0)
        merged = ('<!--AG-QFAQ--><section class="products">\n  <h2 class="products-hdr" id="faq">The Questions</h2>\n  '
                  + qlist + '\n  <div class="ag-faq-sub">And the ones readers ask</div>\n  ' + faq_inner + '</section>')
        s = s[:qs] + between.strip() + '\n\n' + merged + s[fe:]
    s = re.sub(r'<style id="tgi-ag-layout">.*?</style>\n?', '', s, flags=re.S).replace("</head>", LAYOUT_CSS + "\n</head>", 1)
    return s

def main(apply_):
    s = open(F, encoding="utf-8").read(); o = s
    donor = open(os.path.join(ROOT, "drops/brand-to-know-manors.html"), encoding="utf-8").read()
    js = [m.group(0) for m in re.finditer(r"<script>.*?</script>", donor, re.S) if "pg-track" in m.group(0)][0]
    js = js.replace("<script>", '<script id="tgi-ag-gallery-js">', 1)
    def repl(m):
        card = m.group(0)
        h = re.search(r'agronomywork\.shop/store/([a-z0-9-]+)', card).group(1)
        fr = FR[h]
        name = re.search(r'<div class="product-name">(.*?)</div>', card).group(1)
        alt = re.sub(r"<[^>]+>|&[a-z]+;", "", name)
        imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="Agronomy Workshop {alt} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        gal = (f'<div class="product-gallery"><div class="pg-track">{imgs}</div>'
               f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>')
        card = re.sub(r'<div class="product-img">.*?</div>|<div class="product-gallery">.*?<div class="pg-dots">.*?</div></div>', gal, card, count=1, flags=re.S)
        card = re.sub(r'<div class="product-card"(?: data-frames="\d+")?>', f'<div class="product-card" data-frames="{len(fr)}">', card, count=1)
        return card
    # The in-situ band repeated six photos that now lead the galleries; swap in unused frames from the brand's shoot.
    BAND = {
        "life-11": ("life-2", "A golfer in the Natural Work Shirt standing on a links fairway"),
        "life-12": ("life-3", "A golfer in the Earth Work Shirt and cap on the course"),
        "life-16": ("life-4", "Close-up of a golfer in an Agronomy Workshop cap and the Earth Work Shirt"),
        "life-20": ("life-5", "A giant inflatable yellow polo hung on the side of a brick building"),
        "life-14": ("life-21", "A golfer in the Earth Tree Hat looking out over the water"),
        "life-22": ("life-24", "Close-up of the lettering woven into the Navy Unusual Lies towel"),
    }
    for old, (new, alt) in BAND.items():
        s = re.sub(rf'<img src="/images/agronomy/{old}\.jpg" alt="[^"]*"', f'<img src="/images/agronomy/{new}.jpg" alt="{alt}"', s)
    s, n = re.subn(r'<div class="product-card"[^>]*>.*?class="product-link">.*?</a>', repl, s, flags=re.S)
    s = s.replace('<div class="products-grid ag-flex">', '<div class="products-grid" data-ag="flex">').replace('<div class="products-grid">', '<div class="products-grid" data-ag="flex">')
    s = re.sub(r'<style id="tgi-ag-refresh">.*?</style>\n?', '', s, flags=re.S).replace("</head>", CSS + "\n</head>", 1)
    s = re.sub(r'<script id="tgi-ag-gallery-js">.*?</script>\n?', '', s, flags=re.S)
    k = s.rfind("</body>"); s = s[:k] + js + "\n" + s[k:]
    s = layout(s)
    assert n == 12, n
    assert s.count('class="product-gallery"') == 12 and 'class="product-img"' not in s
    print(f"apply-agronomy-refresh: {n} cards -> galleries ({sum(len(v) for v in FR.values())} frames); {'updated' if s != o else 'unchanged'}")
    if apply_ and s != o:
        open(F, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    main("--apply" in sys.argv)
