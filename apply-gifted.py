#!/usr/bin/env python3
"""apply-gifted.py — gifted-product label on posts listed in data/gifted.json. 24 November 2026.
Lenny: fix 2 for the PGA Show media credential — gifted product disclosed on the post itself.
The label sits right under the byline: "Gifted: <Brand> sent us <item> ... How we handle gifted product."
Idempotent (block between <!--TGI-GIFT--> markers is regenerated); a post removed from the
JSON loses its label on the next run. Runs after apply-author.py in Deploy TGI.command.
Dry run by default; --apply writes.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
MARK, END = "<!--TGI-GIFT-->", "<!--/TGI-GIFT-->"
CSS = ('<style id="tgi-gift-css">.tgi-gift{max-width:680px;margin:14px auto 0;padding:10px 14px;border:.5px solid #2D4A2B;'
       'color:#2D4A2B;font-size:14px;line-height:1.5;text-align:center}.tgi-gift b{font-family:var(--mono,monospace);font-size:10px;'
       'letter-spacing:.14em;text-transform:uppercase;margin-right:6px}.tgi-gift a{color:inherit;border-bottom:1px solid currentColor}</style>')


def label(items):
    parts = [f"{b} sent us {i}" for b, i in items]
    txt = "; ".join(parts)
    return (f'{MARK}<p class="tgi-gift"><b>Gifted</b>{txt}. They did not see or approve this piece before it ran. '
            f'<a href="/disclosure#gifted">How we handle gifted product</a>.</p>{END}')


def main(apply_):
    data = json.load(open(os.path.join(ROOT, "data/gifted.json"), encoding="utf-8")).get("posts", {})
    changed, bad = 0, []
    for d in ("drops", "guides"):
        for f in os.listdir(os.path.join(ROOT, d)):
            if not f.endswith(".html") or re.search(r" \d+\.html$", f):
                continue
            p = os.path.join(ROOT, d, f)
            s = open(p, encoding="utf-8").read()
            key = f"/{d}/{f[:-5]}"
            new = re.sub(r"\n?" + re.escape(MARK) + r".*?" + re.escape(END), "", s, flags=re.S)
            if key in data:
                m = re.search(r"<!--/TGI-BY-->", new) or re.search(r"</h1>", new)
                if not m:
                    bad.append(key); continue
                new = new[:m.end()] + "\n" + label(data[key]) + new[m.end():]
                if 'id="tgi-gift-css"' not in new:
                    new = new.replace("</head>", CSS + "\n</head>", 1)
            if new != s:
                changed += 1
                if apply_:
                    open(p, "w", encoding="utf-8").write(new)
    missing = [k for k in data if not os.path.exists(os.path.join(ROOT, k.lstrip("/") + ".html"))]
    print(f"{'wrote' if apply_ else 'DRY RUN'}: gifted labels — {len(data)} listed, {changed} posts changed")
    for k in missing + bad:
        print("  !! no such post / no byline: " + k)


if __name__ == "__main__":
    main("--apply" in sys.argv)
