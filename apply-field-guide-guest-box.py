#!/usr/bin/env python3
"""apply-field-guide-guest-box.py — compact "Guest Field Guide" box under the Field Guide hero.
Lenny, 26 Nov 2026: "a smaller box more towards the top"; dropped "Not in Austin?". Approved from mockups/guest-box-*.jpg.
Idempotent (marker comments). Update GUIDE when a new guest guide publishes. Dry run by default; --apply writes.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "field-guide/index.html"
M0, M1 = "<!--TGI-GUEST-BOX-->", "<!--/TGI-GUEST-BOX-->"
C0, C1 = "<!--TGI-GUEST-BOX-CSS-->", "<!--/TGI-GUEST-BOX-CSS-->"
GUIDE = {
    "url": "/drops/guest-field-guide-san-francisco-sloat",
    "img": "/images/guest-sf-sloat/hero.jpg",
    "alt": "A surfer at the end of a coastal path in San Francisco",
    "kicker": "New &middot; Guest Field Guide No. 01",
    "title": "San Francisco, according to SLOAT.",
    "dek": "The founders of SLOAT on the courses they play, where they eat after, and an interview. A new city with a new brand each time.",
}
CSS = ('<style>.ggb-wrap{max-width:1400px;margin:0 auto;padding:22px 32px 6px}'
       '.ggb{display:grid;grid-template-columns:200px minmax(0,1fr) auto;align-items:center;gap:22px;border:.5px solid var(--ink);background:#efe9dc;text-decoration:none;color:inherit}'
       '.ggb:hover{background:#e8e1d2}.ggb img{width:200px;height:118px;object-fit:cover;display:block}'
       '.ggb-k{font:500 9.5px/1.4 "JetBrains Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:#2D4A2B}'
       '.ggb-t{font-family:var(--serif);font-size:22px;line-height:1.15;margin:4px 0}'
       '.ggb-d{font-size:14px;line-height:1.45;opacity:.8;margin:0}'
       '.ggb-go{font:500 10px/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--ink);padding:10px 12px;margin-right:18px;white-space:nowrap}'
       '@media(max-width:820px){.ggb-wrap{padding:16px 20px 4px}.ggb{grid-template-columns:96px minmax(0,1fr);gap:14px}.ggb img{width:96px;height:96px}.ggb-go{display:none}.ggb-t{font-size:18px}.ggb-d{font-size:13px}}</style>')


def box():
    g = GUIDE
    return (f'{M0}<div class="ggb-wrap"><a class="ggb" href="{g["url"]}"><img src="{g["img"]}" alt="{g["alt"]}" loading="lazy" />'
            f'<div><div class="ggb-k">{g["kicker"]}</div><div class="ggb-t">{g["title"]}</div><p class="ggb-d">{g["dek"]}</p></div>'
            f'<span class="ggb-go">Read it &rarr;</span></a></div>{M1}\n')


def strip(s, a, b):
    while a in s:
        i = s.index(a); j = s.index(b, i) + len(b)
        s = s[:i] + s[j:].lstrip("\n")
    return s


def main(apply_):
    s = PAGE.read_text(encoding="utf-8")
    s = strip(strip(s, M0, M1), C0, C1)
    anchor = '<div class="fgq fgq-top"'
    if anchor not in s:
        sys.exit("! anchor not found")
    s = s.replace("</head>", C0 + CSS + C1 + "\n</head>", 1)
    i = s.index(anchor)
    s = s[:i] + box() + s[i:]
    if not (ROOT / GUIDE["img"].lstrip("/")).is_file() or not (ROOT / (GUIDE["url"].lstrip("/") + ".html")).is_file():
        sys.exit("! image or guide missing")
    if not apply_:
        print("  dry run — pass --apply"); return
    PAGE.write_text(s, encoding="utf-8")
    print("  wrote field-guide/index.html — guest guide box under the hero")


if __name__ == "__main__":
    main("--apply" in sys.argv)
