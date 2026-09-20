#!/usr/bin/env python3
"""recheck-pants-prices.py — re-read every figure on the Pants Edit, live.

Walker Golf Things repriced its entire trouser shelf inside the hour during
the first sweep: the Members Pant went $110/5-of-5 to $119.95/0-of-5, the Kooka
$88 to $119.95. Any price on this page is therefore a claim with a shelf life,
and the house rule is that every figure is read from the brand's own store with
the date stated.

This reads each pick again and DIFFS it against what localize-pants.py holds.
It does not silently update: a moved price is printed and the exit code is
non-zero, because the copy on the page may reference the number.

Sentinel is Squarespace and Manors is Sanity — neither serves products.json, so
both are marked MANUAL and must be eyeballed. Saying "checked" about a store we
cannot machine-read would be the same class of lie as a guard that reads its
own return value.
"""
import importlib.util, json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-fetch"}

spec = importlib.util.spec_from_file_location("lp", ROOT / "localize-pants.py")
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)

# slug -> (host, handle). Absent = not machine-readable.
SHOPIFY = {
 "odd-ritual": ("oddritualgolf.com", "pleated-daily-trouser-black"),
 "walker": ("walkergolfthings.com", "kooka-all-day-twill-pant-forest"),
 "quiet-golf": ("quietgolf.com", "san-merino-pant"),
 "casualist": ("casualist.com", "pleated-trousers"),
 "students": ("studentsgolf.com", "tradition-double-pleated-wool-pants"),
 "public-drip": ("publicdrip.com", "anywhere-pleated-pants-pinstripe"),
 "criquet": ("criquetshirts.com", "comfort-corduroy-pant-khaki"),
 "gramicci": ("gramicci.com", "japanese-5-pocket-denim-pant"),
 "malbon": ("malbon.com", "station-pant-military-green"),
 "siegelman": ("siegelmanstable.com", "retro-track-pant-1"),
 "birds-of-condor": ("us.birdsofcondor.com", "black-ranger-golf-walk-pants"),
 "merrill": ("merrillgolf.com", "baggy-trousers-black"),
 "stitch": ("stitchgolf.com", "231sa5003"),
 "anti-country-club": ("anticountryclubtokyo.com",
                       "anti-country-club-tokyo-2026-ss-chino-pants-beige"),
 "olydoe": ("olydoe.com", "pleated-walker-pant"),
 "eastside": ("eastsidegolf.com", "el2090952-254-khaki-field-pant"),
}
MANUAL = {"sentinel": "Squarespace — no products.json",
          "manors": "Sanity-backed — no products.json"}

# Non-USD stores. The price field these return is in the store's OWN currency
# when read without a country hint, and we never convert.
NATIVE = {"odd-ritual": "ZAR", "anti-country-club": "JPY"}


def live(host, handle):
    """products.json carries `available`; the single-product .json does not."""
    for pg in range(1, 8):
        u = f"https://{host}/products.json?limit=250&page={pg}"
        d = json.load(urllib.request.urlopen(
            urllib.request.Request(u, headers=UA), timeout=60))["products"]
        if not d:
            return None
        for p in d:
            if p["handle"] == handle:
                av = [v for v in p["variants"] if v["available"]]
                return (float(av[0]["price"]) if av else None, len(av), len(p["variants"]))
    return None


def held(price_str):
    return float(re.sub(r"[^\d.]", "", price_str.replace("&yen;", "")))


def main():
    moved, gone, ok, manual = [], [], [], []
    for slug, brand, name, price, avail, kind, url, img in lp.PICKS:
        if slug in MANUAL:
            manual.append((brand, price, avail, MANUAL[slug])); continue
        host, handle = SHOPIFY[slug]
        try:
            r = live(host, handle)
        except Exception as e:
            moved.append((brand, f"store unreachable: {str(e)[:60]}")); continue
        if r is None:
            gone.append((brand, "product no longer listed")); continue
        now, a, t = r
        if now is None:
            gone.append((brand, "sold out in every size")); continue
        was = held(price)
        cur = NATIVE.get(slug, "USD")
        now_av = f"{a} of {t} sizes" if t > 1 else "in stock"
        if abs(now - was) > 0.01:
            moved.append((brand, f"{cur} {was:,.0f} -> {now:,.0f}"))
        elif now_av != avail and avail != "in stock":
            moved.append((brand, f"sizes {avail} -> {now_av}"))
        else:
            ok.append(brand)

    for b in ok:            print(f"  ok      {b}")
    for b, price, avail, why in manual:
        print(f"  MANUAL  {b:24} holds {price} / {avail} — {why}")
    for b, w in moved:      print(f"  MOVED   {b:24} {w}")
    for b, w in gone:       print(f"  GONE    {b:24} {w}")

    print(f"\n  {len(ok)} unchanged, {len(moved)} moved, {len(gone)} gone, "
          f"{len(manual)} need a human eye ({', '.join(m[0] for m in manual)})")
    if moved or gone:
        sys.exit("\n! figures have moved since the sweep — fix localize-pants.py "
                 "AND any copy that cites them, then re-run")


if __name__ == "__main__":
    main()
