"""gift_guide_series.py — shared series navigation for the 2026 Gift Guide (Parts 1-3). 9 November 2026.
Lenny: "make sure the parts link to each other in the page themselves". Imported by build-gift-guide-1b/2b/3b.py.
"""
PARTS = [
    (1, "golf-gift-guide-2026-everyday-range-rat-stocking-stuffers", "Everyday Upgrades, Range Rats and Stocking Stuffers",
     ["The Everyday Item as Well Done as Possible", "For the Range Rat", "Small Enough for a Stocking"]),
    (2, "golf-gift-guide-2026-statement-pieces-colorways-splurges", "Statement Pieces, Fresh Colorways and Splurges",
     ["Compliments Guaranteed", "A Fresh New Colorway", "The One They&rsquo;d Never Buy Themselves"]),
    (3, "golf-gift-guide-2026-heirlooms-tiny-makers-off-season", "Heirlooms, Tiny Makers and Off-Season Gifts",
     ["Will Last a Lifetime", "Made by a Handful of People", "For the Off-Season"]),
]
CSS = ('<style>/*TGI-GG-SERIES*/.gg-series-wrap{display:block;margin:44px auto 0;padding:0 20px}.gg-series{max-width:1180px;margin:14px auto 8px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}'
       '.gg-series a,.gg-series .gg-here{display:block;border:1px solid rgba(20,20,20,.18);padding:16px 18px;text-decoration:none;border-bottom:1px solid rgba(20,20,20,.18);color:inherit}'
       '.gg-series a:hover{border-color:#2d4a2b}.gg-series .gg-here{background:#2d4a2b;color:#f4efe4;border-color:#2d4a2b}'
       '.gg-series .gg-pn{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.75}'
       '.gg-series .gg-pt{font-size:17px;line-height:1.3;margin:6px 0 8px;font-weight:500}.gg-series .gg-pc{font-size:13px;line-height:1.5;opacity:.8}'
       '.gg-series-lbl{max-width:1180px;margin:0 auto;text-align:center;font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.6}'
       '@media(max-width:900px){.gg-series{grid-template-columns:1fr}}</style>\n')
def nav(current, label="The 2026 Gift Guide, in three parts"):
    cells = []
    for n, slug, title, cats in PARTS:
        inner = (f'<div class="gg-pn">Part {n} of 3{" &middot; You are here" if n == current else ""}</div>'
                 f'<div class="gg-pt">{title}</div><div class="gg-pc">{" &middot; ".join(cats)}</div>')
        cells.append(f'<div class="gg-here">{inner}</div>' if n == current else f'<a href="/drops/{slug}">{inner}</a>')
    return (f'\n<nav class="gg-series-wrap" aria-label="2026 Gift Guide parts"><div class="gg-series-lbl">{label}</div>'
            f'<div class="gg-series">{"".join(cells)}</div></nav>\n')
