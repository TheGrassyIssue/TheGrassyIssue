#!/usr/bin/env python3
"""make-preview.py — render a site page as a preview that ACTUALLY SHOWS IMAGES.

THE BUG THIS EXISTS TO FIX (17 September 2026)
----------------------------------------------
Every preview built before today rewrote root-relative image paths to

    file:///sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site/images/...

which is the path THE SANDBOX sees. That directory does not exist on the Mac, so
every single image came up broken the moment Lenny opened the file. The HTML was
fine; the paths pointed into a filesystem only the build process can see.

There are two honest ways to fix it, and the absolute path is the fragile one —
it hard-codes one machine and one folder location. So this copies every asset the
page actually references into a sibling folder and rewrites to RELATIVE paths:

    preview.html
    preview_files/images/hls/hero-followthrough.jpg
    preview_files/images/...

The result is portable: it works on any machine, survives being moved to the
desktop or emailed, and needs no server. Only the assets the page references are
copied, so a post preview costs a few MB rather than mirroring the whole site.

USAGE
    python3 make-preview.py drops/some-post.html
    python3 make-preview.py index.html --fragment TGI-HLS   # just one feed card

--fragment MARKER pulls the region between <!--MARKER--> and <!--/MARKER--> and
wraps it in the page's own <style>, which is how the homepage card gets previewed
without rendering the entire feed.
"""
import os, re, sys, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = "/sessions/admiring-pensive-ritchie/mnt/outputs"

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    raise SystemExit(__doc__)
SRC = args[0]
FRAG = None
if "--fragment" in sys.argv:
    FRAG = sys.argv[sys.argv.index("--fragment") + 1]

name = os.path.splitext(os.path.basename(SRC))[0]
if FRAG:
    name += "-" + FRAG.lower().replace("tgi-", "")
name += "-preview"
assets = os.path.join(OUT, name + "_files")

page = open(os.path.join(ROOT, SRC), encoding="utf-8").read()

if FRAG:
    s, e = f"<!--{FRAG}-->", f"<!--/{FRAG}-->"
    if s not in page:
        raise SystemExit(f"fragment marker {s} not found in {SRC}")
    body = page[page.index(s):page.index(e) + len(e)]
    css = "\n".join(m.group(0) for m in re.finditer(r"<style.*?</style>", page, re.S))
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(name)}</title>"
           f"{css}</head><body style='padding:40px;max-width:780px;margin:0 auto'>{body}</body></html>")
else:
    doc = page

# ---------------------------------------------------- collect + copy assets
if os.path.isdir(assets):
    shutil.rmtree(assets)
copied, missing = 0, []
seen = set()

# Every root-relative asset reference the page makes: src=, href= on links,
# and url(...) inside inline CSS.
# (?!/) excludes PROTOCOL-RELATIVE urls like //gc.zgo.at/count.js — those are
# external and start with a slash but are not site paths.
pat = re.compile(r'(?:src|href)="(/(?!/)[^"]+\.(?:jpg|jpeg|png|gif|webp|svg|ico|css|js))"'
                 r'|url\((["\']?)(/(?!/)[^"\')]+)\2\)', re.I)
for m in pat.finditer(doc):
    rel = m.group(1) or m.group(3)
    if not rel or rel in seen:
        continue
    seen.add(rel)
    src = os.path.join(ROOT, rel.lstrip("/"))
    if not os.path.exists(src):
        missing.append(rel)
        continue
    dst = os.path.join(assets, rel.lstrip("/"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    copied += 1

# Rewrite to relative. The trailing-slash form matters: "preview_files/images/x"
# resolves next to the html file wherever that file ends up.
base = name + "_files/"
doc = pat.sub(lambda m: (m.group(0).replace(m.group(1), base + m.group(1).lstrip("/"))
                         if m.group(1) else
                         m.group(0).replace(m.group(3), base + m.group(3).lstrip("/"))), doc)

# ------------------------------------------------------------------ guards
problems = []
if re.search(r'file:///sessions/', doc):
    problems.append("a sandbox file:// path survived — that is the original bug")
left = re.findall(r'(?:src|href)="(/images/[^"]+)"', doc)
if left:
    problems.append(f"{len(left)} image path(s) still root-relative, e.g. {left[0]}")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

path = os.path.join(OUT, name + ".html")
open(path, "w", encoding="utf-8").write(doc)

size = sum(os.path.getsize(os.path.join(dp, f))
           for dp, _, fs in os.walk(assets) for f in fs) if os.path.isdir(assets) else 0
print(f"wrote {name}.html  +  {name}_files/")
print(f"  {copied} assets copied ({size/1_048_576:.1f} MB)")
if missing:
    print(f"  {len(missing)} referenced file(s) missing from the site:")
    for x in missing[:6]:
        print("    !!", x)
