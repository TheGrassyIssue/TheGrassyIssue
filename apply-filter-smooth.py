#!/usr/bin/env python3
"""apply-filter-smooth.py — stop the homepage feed jumping when you tap a filter pill (8 Nov 2026).
Lenny: "when you filter onto the field notes on the home page is glitches a bit".
Cause: cards that were hidden have lazy images, so the first layout measures them short and every card jumps
as each image arrives. Fix: fade the feed out, load the lead image of every card that will show, wait for them
(max 900 ms), lay out once, fade back in. Idempotent; dry run by default, pass --apply."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
MARK = "/*TGI-FILTER-SMOOTH*/"
OLD = """      // Re-layout masonry and re-trigger entrance animation
      requestAnimationFrame(() => {
        layoutMasonry();
        document.querySelectorAll('.card:not(.hidden)').forEach((c, i) => {
          c.classList.remove('visible');
          setTimeout(() => c.classList.add('visible'), i * 60);
        });
      });"""
NEW = """      /*TGI-FILTER-SMOOTH*/
      const feedEl = document.querySelector('.feed');
      feedEl.style.transition = 'opacity .18s ease';
      feedEl.style.opacity = '0';
      const leads = [];
      document.querySelectorAll('.feed .card:not(.hidden)').forEach((c, i) => {
        if (i >= cardsShown) return;
        const img = c.querySelector('img');
        if (img) { img.loading = 'eager'; if (!img.complete) leads.push(new Promise(r => { img.addEventListener('load', r, { once: true }); img.addEventListener('error', r, { once: true }); })); }
      });
      await Promise.race([Promise.all(leads), new Promise(r => setTimeout(r, 900))]);
      requestAnimationFrame(() => {
        layoutMasonry();
        document.querySelectorAll('.card:not(.hidden)').forEach(c => c.classList.add('visible'));
        feedEl.style.opacity = '1';
        setTimeout(layoutMasonry, 400);
      });"""
def main(apply_):
    s = HOME.read_text(encoding="utf-8")
    if MARK in s: print("  already applied"); return
    if OLD not in s: sys.exit("! filter block not found")
    s = s.replace(OLD, NEW, 1)
    if not apply_: print("  dry run — pass --apply"); return
    HOME.write_text(s, encoding="utf-8"); print("  patched index.html filter pills")
if __name__ == "__main__":
    main("--apply" in sys.argv)
