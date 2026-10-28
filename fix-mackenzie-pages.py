#!/usr/bin/env python3
"""fix-mackenzie-pages.py — 27 Oct 2026 formatting pass on the MacKenzie pages (Lenny: "make sure all the Mackenzie bag
pages are formatted and looking correct"). Idempotent; safe to rerun after either page is rebuilt.
  1. Collab Archive + Fyfe x MacKenzie: centre short last rows (a lone 4th card sat hard left under a 3-up grid).
  2. Collab Archive: the FAQ block had no heading or spacing and ran straight on from the last grid.
  3. Fyfe x MacKenzie: the What's Next card nested a link inside the card link, which breaks the card in two.
Images: research/mackenzie-frame-fix.py moves the white-sweep product shots onto stone.
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
ARCH = ROOT / "drops/the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site.html"
FYFE = ROOT / "drops/fyfe-x-mackenzie-every-edition.html"
GRID = ('<style>/*TGI-MK-GRID*/.products-grid{display:flex!important;flex-wrap:wrap;justify-content:center;gap:24px}'
        '.products-grid>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
        '@media(max-width:820px){.products-grid>.product-card{flex-basis:calc((100% - 24px)/2)}}'
        '@media(max-width:480px){.products-grid>.product-card{flex-basis:100%}}</style>\n')
FAQCSS = ('<style>/*TGI-MK-FAQ*/.mk-faq{margin:72px 0 0;padding:48px 0 0;border-top:.5px solid var(--ink)}'
          '.mk-faq .products-hdr{margin-bottom:20px}@media(max-width:640px){.mk-faq{padding-top:36px}}</style>\n')
NEST = re.compile(r' Watch the collection page, or read our full profile of <a href="/drops/brand-to-know-fyfe-golf">the workshop behind them</a>\.')

def main(apply_):
    out = {}
    a = ARCH.read_text(encoding="utf-8")
    a = re.sub(r"<style>/\*TGI-MK-(GRID|FAQ)\*/.*?</style>\n", "", a, flags=re.S)
    a = a.replace("</head>", GRID + FAQCSS + "</head>", 1)
    if 'class="mk-faq"' not in a:
        i = a.find('<div class="faq">'); j = a.find('</div>\n', a.find('</details>', a.rfind('<details', i, a.find('<!-- TGI-ONE-FOOTER -->'))))
        assert i > 0 and j > i, "faq block not found"
        a = a[:i] + '<section class="mk-faq"><h2 class="products-hdr" id="faq">The Questions</h2>\n' + a[i:j + 7] + '</section>\n' + a[j + 7:]
    out[ARCH] = a
    f = FYFE.read_text(encoding="utf-8")
    f = re.sub(r"<style>/\*TGI-MK-GRID\*/.*?</style>\n", "", f, flags=re.S)
    f = f.replace("</head>", GRID + "</head>", 1)
    f = NEST.sub(" Watch the collection page for the next drop.", f)
    out[FYFE] = f
    for p, s in out.items():
        print("  %s: grid %s, faq-heading %s, nested-link %s" % (p.name, 'TGI-MK-GRID' in s, 'class="mk-faq"' in s, bool(NEST.search(s))))
    if apply_:
        for p, s in out.items(): p.write_text(s, encoding="utf-8")
        print("  written")
    else: print("  dry run — pass --apply")

if __name__ == "__main__":
    main("--apply" in sys.argv)
