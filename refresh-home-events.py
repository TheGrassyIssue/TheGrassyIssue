#!/usr/bin/env python3
"""refresh-home-events.py — drop finished events from the homepage Austin Events module.

4 Oct 2026. The SEO audit found the homepage still calling the Oct 1 and Oct 3 events "upcoming"
on Oct 4. wire-austin-events.py refuses to write past events but only runs when it is run; this
script just removes any card whose last day is before today and fixes the "N upcoming" count.
Safe to run any time (and from the deploy script). Dry run by default.
"""
import datetime, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}

def end_date(label, today):
    label = label.replace("&ndash;", "-").replace("–", "-")
    m = re.match(r"([A-Z][a-z]{2})\s+(\d+)(?:\s*-\s*(?:([A-Z][a-z]{2})\s+)?(\d+))?", label.strip())
    if not m:
        return None
    mon = MON[m.group(3) or m.group(1)]
    day = int(m.group(4) or m.group(2))
    year = today.year
    # cards run forward from now: a month well behind today belongs to next year
    if mon < today.month - 2:
        year += 1
    return datetime.date(year, mon, day)

def main(apply_):
    today = datetime.date.today()
    h = HOME.read_text(encoding="utf-8")
    i = h.find('<section class="events">'); j = h.find("</section>", i)
    if i < 0:
        sys.exit("no events module")
    block = h[i:j]
    cards = re.findall(r'\n    <a [^>]*class="event-card">.*?\n    </a>', block, re.S)
    keep, drop = [], []
    for c in cards:
        lbl = re.search(r'class="event-date">([^<]*)<', c).group(1)
        d = end_date(lbl, today)
        (drop if d and d < today else keep).append((lbl, c))
    new = block
    for lbl, c in drop:
        new = new.replace(c, "")
    new = re.sub(r"\d+ upcoming", f"{len(keep)} upcoming", new)
    print(f"  today {today}: {len(cards)} cards, dropping {[l for l, _ in drop]}, {len(keep)} left"
          + ("" if apply_ else " (dry run — pass --apply)"))
    if apply_ and new != block:
        HOME.write_text(h[:i] + new + h[j:], encoding="utf-8")
        print("  wrote index.html")

if __name__ == "__main__":
    main("--apply" in sys.argv)
