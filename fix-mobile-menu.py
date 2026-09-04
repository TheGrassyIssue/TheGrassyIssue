#!/usr/bin/env python3
"""
fix-mobile-menu.py — give every page a working mobile navigation menu.

THE BUG (measured 2026-09-03)
-----------------------------
276 pages render the hamburger button with onclick="toggleMenu()". Exactly ONE
page (index.html) actually defines toggleMenu() and contains the #navDrawer it
operates on. On the other 275, tapping the hamburger threw
"toggleMenu is not defined" and nothing opened — so a phone visitor on any post,
brand page or guide had NO route to Brands / Field Guide / Events / About except
manually going back to the homepage. Silent: the button looked normal.

It was also invisible until fix-mobile-nav.py ran: `.nav-toggle` was being
squeezed to width 0 by the same nowrap flex row that caused the overflow, so the
dead button was also un-tappable, which is presumably why this went unnoticed.

THE FIX
-------
Port index.html's drawer to every page carrying a toggle, with two corrections:
  - hrefs are root-absolute ("/#feed" not "#feed") so they work from /drops/,
    /brands/, /guides/ etc. The homepage version used a bare "#feed", which from
    a subdirectory would have gone nowhere.
  - the About link is included (the homepage drawer predates /about).

Idempotent via the marker. Dry-run by default; --apply writes; --revert removes.
RE-RUN after apply-header.py or build-brands.py.
"""
import sys, glob, re

MARK = "<!--TGI-MOBILE-MENU-V1-->"

DRAWER = MARK + """
<div class="nav-drawer" id="navDrawer" role="dialog" aria-label="Navigation menu">
  <a href="/#feed" onclick="closeMenu();">The Feed</a>
  <a href="/brands/" onclick="closeMenu();">Brands</a>
  <a href="/field-guide/" onclick="closeMenu();">Field Guide</a>
  <a href="/events/" onclick="closeMenu();">Events</a>
  <a href="/about" onclick="closeMenu();">About</a>
</div>
<script>
function toggleMenu(){var b=document.querySelector('.nav-toggle'),d=document.getElementById('navDrawer');
  if(!b||!d)return; var o=b.classList.toggle('open'); d.classList.toggle('open',o);
  b.setAttribute('aria-expanded',o); document.body.style.overflow=o?'hidden':'';}
function closeMenu(){var b=document.querySelector('.nav-toggle'),d=document.getElementById('navDrawer');
  if(!b||!d)return; b.classList.remove('open'); d.classList.remove('open');
  b.setAttribute('aria-expanded','false'); document.body.style.overflow='';}
/* Most pages ship the toggle with NO onclick attribute (only index.html has one),
   so bind here. Strip any inline handler first or index.html would fire twice and
   cancel itself out. */
(function(){var b=document.querySelector('.nav-toggle');
  if(!b)return; b.removeAttribute('onclick');
  if(!b.hasAttribute('aria-expanded'))b.setAttribute('aria-expanded','false');
  b.addEventListener('click',function(e){e.preventDefault();toggleMenu();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu();});})();
</script>
"""

CSS = """/*TGI-MOBILE-MENU-CSS-V1*/
.nav-drawer{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:var(--paper);z-index:14;flex-direction:column;align-items:center;justify-content:center;gap:28px;font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;opacity:0;transition:opacity .25s}
.nav-drawer.open{display:flex;opacity:1}
.nav-drawer a{padding:12px 24px;border-bottom:1px solid transparent;transition:border-color .15s;min-height:44px;display:flex;align-items:center}
.nav-drawer a:hover{border-bottom-color:var(--ink)}
"""


BUTTON = ('<button class="nav-toggle" aria-label="Open menu" aria-expanded="false">'
          '<span></span><span></span><span></span></button>')

BTN_CSS = """/*TGI-MOBILE-BTN-V1*/
.nav-toggle{display:none;width:28px;height:20px;flex-direction:column;justify-content:space-between;padding:0;background:none;border:none;cursor:pointer}
.nav-toggle span{display:block;width:100%;height:1.5px;background:var(--ink);transition:transform .25s,opacity .25s}
.nav-toggle.open span:nth-child(1){transform:translateY(9.25px) rotate(45deg)}
.nav-toggle.open span:nth-child(2){opacity:0}
.nav-toggle.open span:nth-child(3){transform:translateY(-9.25px) rotate(-45deg)}
@media(max-width:820px){.nav-toggle{display:flex}}
"""

APPLY  = "--apply"  in sys.argv
REVERT = "--revert" in sys.argv
pages = sorted(set(glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")))

done = already = skip = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    orig = s
    if 'class="nav-links"' not in s and "nav-toggle" not in s:
        skip += 1; continue
    # 88 brand pages + 1 guide ship .nav-links with NO hamburger button, so on a
    # phone their nav is display:none with nothing to open it. Add the button.
    if not REVERT and '<button class="nav-toggle"' not in s:
        m = re.search(r'(<div class="nav-links">.*?</div>)', s, re.S)
        if m:
            s = s.replace(m.group(1), m.group(1) + "\n    " + BUTTON, 1)
            if "/*TGI-MOBILE-BTN-V1*/" not in s:
                k = s.rfind("</style>")
                if k >= 0: s = s[:k] + BTN_CSS + s[k:]
    if REVERT:
        if MARK not in s: already += 1; continue
        s = s[:s.find(MARK)] + s[s.find("</script>", s.find(MARK)) + 9:]
        s = s.replace(CSS, "")
        done += 1
    else:
        if MARK in s or 'id="navDrawer"' in s:
            # drawer already present; the button may still be missing (brand pages)
            if s != open(p, encoding="utf-8").read() if False else (s != orig):
                pass
            if s != orig:
                done += 1
                if APPLY: open(p, "w", encoding="utf-8").write(s)
            else:
                already += 1
            continue
        i = s.rfind("</style>")
        if i >= 0: s = s[:i] + CSS + s[i:]
        j = s.rfind("</body>")
        if j < 0: skip += 1; continue
        s = s[:j] + DRAWER + s[j:]
        done += 1
    if APPLY:
        open(p, "w", encoding="utf-8").write(s)

print(f"{'reverted' if REVERT else 'installed'}: {done} | already had one: {already} | no toggle: {skip} | scanned: {len(pages)}")
print("DRY RUN — pass --apply to write" if not APPLY else "applied")
