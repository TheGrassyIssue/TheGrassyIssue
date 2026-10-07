#!/usr/bin/env python3
"""make-preview.py — self-contained, zoomable preview of a page for Lenny (6 Oct 2026).
Lenny: "the preview still wont let me zoom it in and out". Screenshots are taken at full resolution
(desktop 1400px, mobile 390px at 2x) and shown in a viewer with − / + / Fit / 100% buttons, keyboard
+ / − / 0, ctrl/cmd-scroll zoom, and click-to-zoom. Usage: python3 make-preview.py <page.html> <out.html> "Title"
Needs LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu and a local http.server on PORT.
"""
import base64, io, sys, subprocess, time, socket
from PIL import Image
from playwright.sync_api import sync_playwright
Image.MAX_IMAGE_PIXELS = None
page, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
s = socket.socket(); s.bind(("", 0)); PORT = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
shots = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, vw, scale in [("Desktop", 1400, 1), ("Mobile", 390, 2)]:
            pg = b.new_page(viewport={"width": vw, "height": 900}, device_scale_factor=scale)
            pg.goto(f"http://localhost:{PORT}/{page}", wait_until="networkidle")
            pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
            pg.wait_for_timeout(2500)
            im = Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB")
            # JPEG tops out at 65,500px, so long pages are cut into stacked tiles.
            tiles = []
            for y in range(0, im.height, 12000):
                buf = io.BytesIO(); im.crop((0, y, im.width, min(im.height, y + 12000))).save(buf, "JPEG", quality=78, optimize=True, progressive=True)
                tiles.append(base64.b64encode(buf.getvalue()).decode())
            shots.append((name, vw, im.width, tiles))
        b.close()
finally:
    srv.terminate()
tabs = "".join(f'<button class="tab{" on" if i == 0 else ""}" data-i="{i}">{n}</button>' for i, (n, *_r) in enumerate(shots))
panes = "".join(f'<div class="pane{" on" if i == 0 else ""}" data-w="{vw}">' + "".join(f'<img src="data:image/jpeg;base64,{t}" alt="{n} preview">' for t in d) + '</div>'
                for i, (n, vw, w, d) in enumerate(shots))
html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Preview: {title}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#e9e4d8;font-family:-apple-system,Helvetica,sans-serif;color:#141414}}
.bar{{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 16px;background:#2f4a2a;color:#f4f1ea}}
.bar h1{{font-size:14px;font-weight:600;margin:0 12px 0 0}}.bar button{{font:inherit;font-size:13px;padding:6px 12px;border:1px solid #f4f1ea;background:transparent;color:#f4f1ea;cursor:pointer;border-radius:3px}}
.bar button.on{{background:#f4f1ea;color:#2f4a2a}}.bar .z{{min-width:52px;text-align:center;font-size:13px}}.sp{{flex:1}}
.pane{{display:none;overflow:auto;height:calc(100vh - 52px);padding:20px}}.pane.on{{display:block}}
.pane img{{display:block;margin:0 auto;box-shadow:0 2px 14px #0003;cursor:zoom-in;max-width:none}}.pane img+img{{box-shadow:0 6px 14px #0003}}
.pane.zoomed img{{cursor:zoom-out}}</style></head><body>
<div class="bar"><h1>{title} &middot; preview, not deployed</h1>{tabs}<span class="sp"></span>
<button id="out" title="Zoom out (−)">−</button><span class="z" id="zl">Fit</span><button id="in" title="Zoom in (+)">+</button>
<button id="fit" title="Fit to window (0)">Fit</button><button id="one" title="Actual size">100%</button></div>{panes}
<script>
var panes=[].slice.call(document.querySelectorAll('.pane')),tabs=[].slice.call(document.querySelectorAll('.tab')),cur=0,z=[null,null];
function imgs(){{return [].slice.call(panes[cur].querySelectorAll('img'))}}
function fitZ(){{var p=panes[cur],w=+p.dataset.w;return Math.min(1,(p.clientWidth-40)/w)}}
function apply(){{var p=panes[cur],w=+p.dataset.w,k=z[cur]==null?fitZ():z[cur];imgs().forEach(function(i){{i.style.width=(w*k)+'px'}});
document.getElementById('zl').textContent=z[cur]==null?'Fit':Math.round(k*100)+'%';p.classList.toggle('zoomed',k>fitZ()+0.01)}}
function set(k,cx,cy){{var p=panes[cur],old=z[cur]==null?fitZ():z[cur];k=Math.max(0.15,Math.min(4,k));
var fx=(p.scrollLeft+(cx==null?p.clientWidth/2:cx))/p.scrollWidth,fy=(p.scrollTop+(cy==null?p.clientHeight/2:cy))/p.scrollHeight;
z[cur]=k;apply();p.scrollLeft=fx*p.scrollWidth-(cx==null?p.clientWidth/2:cx);p.scrollTop=fy*p.scrollHeight-(cy==null?p.clientHeight/2:cy)}}
function k(){{return z[cur]==null?fitZ():z[cur]}}
document.getElementById('in').onclick=function(){{set(k()*1.25)}};document.getElementById('out').onclick=function(){{set(k()/1.25)}};
document.getElementById('fit').onclick=function(){{z[cur]=null;apply()}};document.getElementById('one').onclick=function(){{set(1)}};
tabs.forEach(function(t,i){{t.onclick=function(){{tabs[cur].classList.remove('on');panes[cur].classList.remove('on');cur=i;t.classList.add('on');panes[i].classList.add('on');apply()}}}});
panes.forEach(function(p){{p.addEventListener('click',function(e){{if(e.target.tagName!=='IMG')return;var r=p.getBoundingClientRect();
if(k()>fitZ()+0.01){{z[cur]=null;apply()}}else set(Math.max(1,k()*2),e.clientX-r.left,e.clientY-r.top)}});
p.addEventListener('wheel',function(e){{if(e.ctrlKey||e.metaKey){{e.preventDefault();var r=p.getBoundingClientRect();set(k()*(e.deltaY<0?1.1:1/1.1),e.clientX-r.left,e.clientY-r.top)}}}},{{passive:false}})}});
document.addEventListener('keydown',function(e){{if(e.key=='+'||e.key=='=')set(k()*1.25);else if(e.key=='-')set(k()/1.25);else if(e.key=='0'){{z[cur]=null;apply()}}}});
window.addEventListener('resize',apply);panes.forEach(function(p,i){{cur=i;apply()}});cur=0;apply();
</script></body></html>"""
open(out, "w").write(html)
print("wrote", out, f"{len(html)//1024} KB")
