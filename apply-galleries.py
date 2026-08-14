#!/usr/bin/env python3
"""Convert static .product-img cards into swipeable .product-gallery cards on existing pages."""
import re, json, os, sys, html as _h

S = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open("/tmp/alts_manifest.json"))

GALLERY_CSS = """
.product-card{position:relative}
.product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}
.pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.pg-track::-webkit-scrollbar{display:none}
.pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}
.pg-frame img{width:100%;height:100%;object-fit:cover;display:block}
.pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:.5px solid var(--ink);background:var(--paper);color:var(--ink);font-size:17px;line-height:1;cursor:pointer;opacity:0;transition:opacity .18s;z-index:2;padding:0}
.pg-arw.prev{left:8px}.pg-arw.next{right:8px}
.product-card:hover .pg-arw{opacity:.9}
.pg-arw:hover{opacity:1}
.pg-count{position:absolute;top:8px;right:8px;font-family:var(--mono);font-size:9px;letter-spacing:.1em;background:var(--paper);border:.5px solid var(--ink);padding:2px 6px;z-index:2}
.pg-dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:5px;z-index:2}
.pg-dot{width:6px;height:6px;border-radius:50%;border:.5px solid var(--ink);background:var(--paper);padding:0;cursor:pointer;opacity:.55;transition:opacity .15s}
.pg-dot.on{background:var(--ink);opacity:1}
@media(max-width:900px){.pg-arw{opacity:.85}}
"""

GALLERY_JS = """
<script>
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
</script>
"""

CARD_START = re.compile(r'<a\s+href="(https?://[^"]+)"[^>]*class="product-card"\s*>')
IMG_BLOCK  = re.compile(r'<div class="product-img"([^>]*)>\s*<img src="([^"]+)"([^>]*?)/>\s*</div>', re.S)

def find_card_end(s, start):
    """Return index just past the </a> that closes the card opened at `start`."""
    depth = 0; i = start
    while i < len(s):
        a = s.find('<a', i); c = s.find('</a>', i)
        if c == -1: return -1
        if a != -1 and a < c:
            depth += 1; i = a + 2
        else:
            if depth == 0: return c + 4
            depth -= 1; i = c + 4
    return -1

def gallery(imgs, alt_attr, alt_text, style=""):
    n = len(imgs)
    frames = "".join(
        '<div class="pg-frame"><img src="%s" alt="%s" loading="lazy"%s /></div>'
        % (u, (alt_text + (" &middot; view %d of %d" % (i+1, n)) if alt_text else ""), style)
        for i, u in enumerate(imgs))
    if n < 2:
        return ('<div class="product-gallery"><div class="pg-track">%s</div></div>' % frames)
    dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                   % (" on" if i == 0 else "", i, i+1) for i in range(n))
    return ('<div class="product-gallery">'
            '<div class="pg-track">%s</div>'
            '<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            '<span class="pg-count">1/%d</span>'
            '<div class="pg-dots">%s</div></div>' % (frames, n, dots))

def process(page):
    path = os.path.join(S, "drops", page + ".html")
    h = open(path, encoding="utf-8").read()
    if 'class="product-gallery"' in h:
        return page, "already has galleries", 0, 0
    lookup = {r["img"]: r["alts"] for r in MAN[page]}
    out = []; pos = 0; converted = 0; multi = 0
    while True:
        m = CARD_START.search(h, pos)
        if not m: break
        end = find_card_end(h, m.end())
        if end == -1: break
        href = m.group(1)
        block = h[m.end():end-4]          # inner HTML of the card
        im = IMG_BLOCK.search(block)
        if not im:
            out.append(h[pos:end]); pos = end; continue
        divattrs = im.group(1)
        src = im.group(2)
        attrs = im.group(3)
        am = re.search(r'alt="([^"]*)"', attrs)
        alt_text = am.group(1) if am else ""
        imgs = [src] + lookup.get(src, [])
        newblock = block[:im.start()] + gallery(imgs, attrs, alt_text, (" style=\"%s\"" % sm.group(1)) if (sm:=re.search(r'style="([^"]*)"', attrs)) else "") + block[im.end():]
        # span.product-link -> real anchor
        newblock = re.sub(r'<span class="product-link">(.*?)</span>',
                          lambda mm: '<a href="%s" target="_blank" rel="noopener" class="product-link">%s</a>'
                                     % (href, mm.group(1)), newblock, count=1, flags=re.S)
        out.append(h[pos:m.start()])
        out.append('<div class="product-card" data-frames="%d">' % len(imgs))
        out.append(newblock)
        out.append('</div>')
        pos = end; converted += 1
        if len(imgs) > 1: multi += 1
    out.append(h[pos:])
    nh = "".join(out)
    if converted:
        nh = nh.replace("</style>", GALLERY_CSS + "\n</style>", 1)
        nh = nh.replace("</body>", GALLERY_JS + "</body>", 1)
        open(path, "w", encoding="utf-8").write(nh)
    return page, "ok", converted, multi

if __name__ == "__main__":
    tot = tm = 0
    for page in sorted(MAN):
        p, status, c, m = process(page)
        print("  %-44s %-22s converted=%-4d swipeable=%d" % (p[:44], status, c, m))
        tot += c; tm += m
    print("\n  TOTAL converted %d cards, %d swipeable" % (tot, tm))
