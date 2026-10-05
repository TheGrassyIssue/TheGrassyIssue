#!/usr/bin/env python3
"""rank-field-guide-munis.py — rank the five Austin munis in the Field Guide and beef up their facts.

5 Oct 2026. Lenny: "I like the style and design that we have currently, maybe we just need to beef up some of the
sections and then rank the Munis - morris williams #1, then kizer, lions, Clay and hancock last. but that's our
personal preference."

What it does (idempotent; safe to re-run):
  1. Reorders the five muni articles to ORDER and renumbers "No. 0N" as the rank.
  2. Adds a one-line note under the section header saying the order is ours and personal.
  3. Adds Green fee / Booking / Practice stats to each muni card from research/austin-courses/dataset.json
     (facts read from the City of Austin's Golf ATX pages, checked 5 Oct 2026).
  4. Re-sorts the "All five, side by side" table into rank order with a Rank column and a Practice column,
     and the munis in the quick-guide table into rank order.
  5. Re-orders the munis ItemList in the page's JSON-LD to match, with positions.
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
P = ROOT / "field-guide/index.html"
ORDER = ["Morris Williams", "Roy Kizer", "Lions", "Jimmy Clay", "Hancock"]
NOTE = ('<p class="muni-rank-note" style="font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;'
        'opacity:.7;margin:-6px 0 22px">Ranked, and it is personal: Morris Williams first, then Kizer, Lions, Jimmy Clay '
        'and Hancock. Green fees and booking rules checked on the City of Austin&rsquo;s Golf ATX pages, 5 October 2026.</p>')
FACTS = {  # from the dataset; same Golf ATX schedule for the four 18-hole courses
 "Morris Williams": ("$35&ndash;$44", "7 days online; weekends open Mon 8pm CT", "Range"),
 "Roy Kizer":       ("$35&ndash;$44", "7 days online; weekends open Mon 8pm CT", "Range + short game"),
 "Lions":           ("$35&ndash;$44", "7 days online; weekends open Mon 8pm CT", "Range + putting complex"),
 "Jimmy Clay":      ("$35&ndash;$44", "7 days online; weekends open Mon 8pm CT", "Range + short game"),
 "Hancock":         ("$20, all day", "No tee times; walk up and pay", "None"),
}
def key(name):
    for k in ORDER:
        if k.lower() in name.lower(): return k
    raise SystemExit(f"unknown muni {name}")

s = P.read_text(encoding="utf-8"); s0 = s
i = s.index('<section class="index" id="munis">'); j = s.index("</section>", i)
sec = s[i:j]
arts = re.findall(r'\n?\s*<article class="muni">.*?</article>', sec, re.S)
assert len(arts) == 5, len(arts)
named = {key(re.search(r'<div class="muni-name">([^<]*)</div>', a).group(1)): a for a in arts}
first = sec.index(arts[0]); last = sec.index(arts[-1]) + len(arts[-1])
new_arts = []
for n, k in enumerate(ORDER, 1):
    a = named[k]
    a = re.sub(r'<div class="muni-num">No\. \d\d', f'<div class="muni-num">No. {n:02d}', a, count=1)
    a = re.sub(r'\s*<div class="muni-stat muni-stat-x">.*?</div>\s*</div>', "", a, flags=re.S)  # idempotent: drop old extras
    fee, book, prac = FACTS[k]
    extra = "".join(f'\n            <div class="muni-stat muni-stat-x">\n              <div class="label">{l}</div>\n              <div class="value">{v}</div>\n            </div>'
                    for l, v in (("Green fee", fee), ("Booking", book), ("Practice", prac)))
    a = re.sub(r'(<div class="muni-stats">.*?)(\n\s*</div>\s*<div class="muni-links">)', lambda m: m.group(1) + extra + m.group(2), a, count=1, flags=re.S)
    new_arts.append(a)
sec = sec[:first] + "".join(new_arts) + sec[last:]
sec = re.sub(r'\s*<p class="muni-rank-note".*?</p>', "", sec, flags=re.S)
_a = sec.index('<article class="muni">'); sec = sec[:_a] + NOTE.replace('margin:-6px 0 22px', 'margin:18px 0 30px;max-width:72ch') + "\n  " + sec[_a:]
sec = re.sub(r'(<div class="right">)[^<]*(</div>)', r'\1Five public courses · Ranked, our personal order\2', sec, count=1)
s = s[:i] + sec + s[j:]

# side-by-side table
t0 = s.index("All five, side by side."); tb0 = s.index("<tbody>", t0); tb1 = s.index("</tbody>", tb0)
rows = re.findall(r"<tr>.*?</tr>", s[tb0:tb1], re.S)
rk = {key(re.search(r'class="course-name">([^<]*)<', r).group(1)): r for r in rows}
def fix(r, n, k):
    r = re.sub(r'<td class="num rank">\d+</td>\s*', "", r); r = re.sub(r'\s*<td class="prac">[^<]*</td>', "", r)
    r = r.replace("<tr>", f'<tr>\n                <td class="num rank">{n}</td>', 1)
    return r.replace("</tr>", f'  <td class="prac">{FACTS[k][2]}</td>\n              </tr>')
s = s[:tb0] + "<tbody>\n              " + "\n              ".join(fix(rk[k], n, k) for n, k in enumerate(ORDER, 1)) + "\n            " + s[tb1:]
th0 = s.index("<thead>", t0); th1 = s.index("</thead>", th0)
head = s[th0:th1]
if "<th>Rank</th>" not in head:
    head = head.replace("<th>Course</th>", "<th>Rank</th>\n                <th>Course</th>", 1).replace("<th>Walk</th>", "<th>Walk</th>\n                <th>Practice</th>", 1)
    s = s[:th0] + head + s[th1:]
s = s.replace("Green fees read 17 September 2026 &middot; City schedule effective 1 Oct 2025",
              "Ranked, our personal order &middot; Green fees rechecked 5 October 2026 &middot; City schedule effective 1 Oct 2025")

# quick-guide: munis into rank order (other rows untouched, in place)
q0 = s.index('id="quick-guide"'); qb0 = s.index("<tbody>", q0); qb1 = s.index("</tbody>", qb0)
qrows = re.findall(r"\s*<tr>.*?</tr>", s[qb0:qb1], re.S)
mun = [r for r in qrows if 'href="#munis"' in r]
if len(mun) == 5:
    order = sorted(mun, key=lambda r: ORDER.index(key(re.search(r'href="#munis">([^<]*)<', r).group(1))))
    body = s[qb0:qb1]; it = iter(order)
    body = re.sub(r"\s*<tr>.*?</tr>", lambda m: next(it) if 'href="#munis"' in m.group(0) else m.group(0), body, flags=re.S)
    s = s[:qb0] + body + s[qb1:]

# JSON-LD ItemList holding the munis -> rank order
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
    try: data = json.loads(m.group(1))
    except Exception: continue
    def walk(o):
        if isinstance(o, dict):
            if o.get("@type") == "ItemList" and isinstance(o.get("itemListElement"), list):
                els = o["itemListElement"]; names = [json.dumps(e) for e in els]
                if sum(any(k.lower() in n.lower() for k in ORDER) for n in names) >= 5 and len(els) == 5:
                    els.sort(key=lambda e: ORDER.index(next(k for k in ORDER if k.lower() in json.dumps(e).lower())))
                    for n, e in enumerate(els, 1): e["position"] = n
                    o["name"] = "Austin's five municipal golf courses, ranked by The Grassy Issue"
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    new = json.dumps(data, ensure_ascii=False, indent=1)
    s = s.replace(m.group(1), "\n" + new + "\n", 1)

print("  munis ranked:", " > ".join(ORDER) + ("" if "--apply" in sys.argv else "  (dry run)"))
if "--apply" in sys.argv and s != s0:
    P.write_text(s, encoding="utf-8"); print("  wrote field-guide/index.html")
