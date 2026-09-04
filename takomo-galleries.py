#!/usr/bin/env python3
"""
takomo-galleries.py — migrate the Takomo product cards to swipeable galleries.

The page's cards were <a class="product-card"> anchors wrapping a single image.
The site standard (see [[swipe-galleries]]) is a <div class="product-card"
data-frames="N"> with .product-gallery > .pg-track > .pg-frame, plus arrows, a
counter and one dot per frame. verify-post fails the page if data-frames does
not match the actual pg-frame count or if the controls are incomplete.

The Takomo page carried NEITHER the gallery CSS nor the JS, so both are ported
from the Swag post rather than re-invented.

Frame counts are real, not padded: 4 frames for everything except the Ignis D1,
which is sold out and noindex'd, so only 2 usable frames exist.

Idempotent. Dry-run default; --apply writes.
"""
import re, sys, os

P = "drops/brand-to-know-takomo-golf.html"
MARK = "/*TGI-PG-CSS-V1*/"

CSS = MARK + """
.product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}
.pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.pg-track::-webkit-scrollbar{display:none}
.pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}
.pg-frame img{width:100%;height:100%;object-fit:cover;display:block}
.pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:.5px solid var(--ink);background:var(--paper);color:var(--ink);font-size:17px;line-height:1;cursor:pointer;opacity:.85;transition:opacity .18s;z-index:2;padding:0}
.pg-arw.prev{left:8px}
.pg-arw.next{right:8px}
.pg-arw:hover{opacity:1}
.pg-count{position:absolute;top:8px;right:8px;font-family:var(--mono);font-size:9px;letter-spacing:.1em;background:var(--paper);border:.5px solid var(--ink);padding:2px 6px;z-index:2}
.pg-dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:5px;z-index:2}
.pg-dot{width:6px;height:6px;border-radius:50%;border:.5px solid var(--ink);background:var(--paper);padding:0;cursor:pointer;opacity:.55;transition:opacity .15s}
.pg-dot.on{background:var(--ink);opacity:1}
"""

JS = """<script>
(function(){
  document.querySelectorAll('.product-gallery').forEach(function(g){
    var track=g.querySelector('.pg-track'),
        dots=[].slice.call(g.querySelectorAll('.pg-dot')),
        count=g.querySelector('.pg-count'),
        n=parseInt(g.parentNode.getAttribute('data-frames'),10)||1;
    if(n<2) return;
    function idx(){ return Math.round(track.scrollLeft/track.clientWidth); }
    function go(i){ track.scrollTo({left:track.clientWidth*Math.max(0,Math.min(n-1,i)),behavior:'smooth'}); }
    function sync(){ var i=idx();
      dots.forEach(function(d,j){ d.classList.toggle('on',j===i); });
      if(count) count.textContent=(i+1)+'/'+n; }
    track.addEventListener('scroll',function(){ window.requestAnimationFrame(sync); },{passive:true});
    dots.forEach(function(d){ d.addEventListener('click',function(e){ e.preventDefault(); go(+d.dataset.i); }); });
    var p=g.querySelector('.pg-arw.prev'), nx=g.querySelector('.pg-arw.next');
    if(p) p.addEventListener('click',function(e){ e.preventDefault(); go(idx()-1); });
    if(nx) nx.addEventListener('click',function(e){ e.preventDefault(); go(idx()+1); });
  });
})();
</script>"""

def frames_for(base):
    """count real files on disk — never claim a frame that isn't there"""
    n = 1
    while os.path.exists(f"images/takomo-golf/{base}-a{n+1}.jpg"):
        n += 1
    return n

APPLY = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
orig = h

if MARK not in h:
    k = h.rfind("</style>"); h = h[:k] + CSS + h[k:]
    j = h.rfind("</body>");  h = h[:j] + JS + "\n" + h[j:]
    print("gallery CSS + JS ported")

converted = 0
def convert(m):
    global converted
    card = m.group(0)
    href = re.search(r'href="([^"]+)"', card).group(1)
    img  = re.search(r'<img src="/images/takomo-golf/([^".]+)\.jpg" alt="([^"]*)"', card)
    if not img: return card
    base, alt = img.group(1), img.group(2)
    body = re.search(r'<div class="product-body">(.*?)</div>\s*</a>', card, re.S)
    if not body: return card
    inner = body.group(1)
    inner = inner.replace('<span class="product-link">',
                          f'<a href="{href}" target="_blank" rel="noopener" class="product-link">')
    inner = inner.replace('</span>', '</a>') if 'product-link">' in inner else inner
    n = frames_for(base)
    srcs = [base] + [f"{base}-a{i}" for i in range(2, n+1)]
    fr = "".join(f'<div class="pg-frame"><img src="/images/takomo-golf/{s}.jpg" alt="{alt}" loading="lazy" /></div>' for s in srcs)
    ctrls = ""
    if n > 1:
        dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
        ctrls = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
                 '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
                 f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div>')
    converted += 1
    return (f'<div class="product-card" data-frames="{n}">'
            f'<div class="product-gallery"><div class="pg-track">{fr}</div>{ctrls}</div>'
            f'<div class="product-body">{inner}</div></div>')

h = re.sub(r'<a href="[^"]+"[^>]*class="product-card">.*?</a>\s*(?=\n)', convert, h, flags=re.S)

if APPLY and h != orig:
    open(P, "w", encoding="utf-8").write(h)

fr = re.findall(r'data-frames="(\d+)"', h)
print(f"cards converted: {converted} | data-frames values: {fr}")
print("applied" if APPLY else "DRY RUN — pass --apply")
