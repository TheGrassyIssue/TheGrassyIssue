#!/usr/bin/env python3
"""Re-fetch product images from source and reframe them fit-and-pad instead of crop-to-fill.
Padding colour is sampled from each image so it stays seamless."""
import json, os, re, ssl, sys, time, urllib.request, subprocess

S = os.path.dirname(os.path.abspath(__file__))
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def g(u, t=25):
    if u.startswith("//"): u = "https:" + u
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=t, context=ctx)

def reframe(src_bytes, dst):
    open("/tmp/_rf.bin", "wb").write(src_bytes)
    bg = subprocess.run(["convert", "/tmp/_rf.bin", "-format", "%[pixel:p{4,4}]", "info:"],
                        capture_output=True, text=True).stdout.strip() or "white"
    r = subprocess.run(["convert", "/tmp/_rf.bin", "-background", bg, "-alpha", "remove", "-alpha", "off",
                        "-resize", "780x975", "-gravity", "center", "-background", bg,
                        "-extent", "800x1000", "-strip", "-quality", "86", dst], capture_output=True)
    return r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 3000

CARD = re.compile(r'<div class="product-card"[^>]*>(.*?)(?=<div class="product-card"|</div>\s*</section>|</section>)', re.S)

def page_cards(h):
    """yield (shop_url, [img srcs in gallery order]) per card"""
    out = []
    for m in CARD.finditer(h):
        b = m.group(1)
        u = re.search(r'href="(https?://[^"]+)"[^>]*class="product-link"', b)
        srcs = re.findall(r'<img src="(/images/[^"]+)"', b)
        if u and srcs: out.append((u.group(1), srcs))
    if not out:  # older markup: whole card is an anchor
        for m in re.finditer(r'<a href="(https?://[^"]+)"[^>]*class="product-card">(.*?)</a>', h, re.S):
            srcs = re.findall(r'<img src="(/images/[^"]+)"', m.group(2))
            if srcs: out.append((m.group(1), srcs))
    return out

def run(page):
    fp = os.path.join(S, "drops", page + ".html")
    if not os.path.exists(fp): return page, "missing", 0, 0
    h = open(fp, encoding="utf-8").read()
    cards = page_cards(h)
    done = fail = 0
    for url, srcs in cards:
        m = re.match(r'(https?://[^?#]*/products/[^/?#]+)', url)
        if not m: fail += len(srcs); continue
        try:
            d = json.load(g(m.group(1) + ".js", 15))
            imgs = [x.split("?")[0] for x in d.get("images", [])]
        except Exception:
            fail += len(srcs); continue
        for i, rel in enumerate(srcs):
            if i >= len(imgs): break
            dst = S + rel
            try:
                if reframe(g(imgs[i]).read(), dst): done += 1
                else: fail += 1
            except Exception: fail += 1
        time.sleep(0.2)
    return page, "ok", done, fail

if __name__ == "__main__":
    pages = sys.argv[1:]
    td = tf = 0
    for p in pages:
        name, status, d, f = run(p)
        print("  %-50s %-8s reframed=%-4d failed=%d" % (name[:50], status, d, f), flush=True)
        td += d; tf += f
    print("\n  TOTAL reframed %d, failed %d" % (td, tf))
