# Drop Scout — Signal Upgrade Plan

Two upgrades to make the scout faster and stop the recurring "old release read as new" problem. Both replace lossy web search with authoritative, dated sources.

---

## Upgrade A — Newsletter inbox (highest signal, lowest noise)

Indie golf drops hit email first: dated, authoritative, straight from the brand. A dedicated inbox subscribed to all 41 brands becomes the scout's primary feed.

### Setup (one-time, ~30–45 min)
1. **Create a dedicated Gmail** — e.g. `tgi.scout@gmail.com`. Keep it separate from your personal mail so the scout only sees brand newsletters, no clutter.
2. **Subscribe to all 41 brands.** Go to each brand's site, scroll to the footer, enter the scout address in their newsletter signup. Most also give a first-order discount code for signing up — harmless to ignore. (Checklist of all 41 at the bottom of this doc.)
3. **Connect the inbox.** Once Gmail is connected to me, I read the scout inbox at the start of each run instead of (or before) searching.
4. **Optional: Gmail filters.** Auto-label brand mail as `drops/` and skip the inbox, so it stays tidy. I can read by label.

### How the scout uses it
- Each run: read everything in the scout inbox since the last run.
- Email has a real send date → no more misdating 2023/2025 releases as new.
- A "New Drop" / "Just Launched" subject line from a watchlist brand = a draft-worthy card, with a dated source built in.
- Newsletters often include the price and product name, which fills the card fields automatically.

### Why it's the best single fix
Most of the false positives this year (Bogey Boys 2023, Gumtree State Flower 2023, LIV x Malbon 2025) came from search snippets with no reliable date. A newsletter can't be misdated — it arrived when it arrived.

---

## Upgrade B — Whitelist brand domains for direct fetch

Right now I can only fetch URLs that first appear in a web search result, so I can never read a brand's site directly. That forces everything through search, which lags and strips dates.

If the watchlist domains are whitelisted for direct fetching, I can read each brand's **product feed** — which lists every product with `created_at`, `updated_at`, and `published_at` timestamps. That turns "is this new?" from a judgment call into a timestamp comparison.

### What I'd fetch (most of these run on Shopify)
For a Shopify store at `example.com`:
- `example.com/products.json?limit=250` → JSON of all products with creation/publish dates
- `example.com/collections/new-arrivals` → curated new page
- `example.com/sitemap_products_1.xml` → full product sitemap with `<lastmod>` dates

For non-Shopify (Squarespace, etc.), `example.com/sitemap.xml` still gives `<lastmod>` dates per page.

### What you need to do
Whitelist the 41 watchlist domains (listed below) for direct fetch in my settings. After that I can pull feeds directly each run — no search round-trip, no date guessing.

### Pairs well with Upgrade C (a brand ledger)
Once I can read feeds, I can keep a `brands.json` of the last-seen latest product per brand and simply **diff** each run. Anything with a `created_at` newer than last run = a real new drop. This is the structural fix that kills false positives for good. Say the word and I'll build the ledger.

---

## The 41 watchlist domains

**Core (1–12)**
- manorsgolf.com
- malbon.com
- metalwood.studio
- eastsidegolf.com
- quietgolf.com
- bogeyboys.com
- devereuxgolf.com
- randomgolfclub.com
- gumtreegolfandnature.com
- sentinelgolf.us
- fyfegolf.com
- mackenziegolfbags.com

**Extended (13–41)**
- agronomywork.shop
- casualist.co
- lofgolf.com
- studentsgolf.com
- late-nine.com
- sugarloafsocialclub.com
- publicdrip.com
- whimgolf.com
- forewindgolf.com
- hamegolf.com
- soundergolf.com
- bluegrassfairway.com
- fielddaysportingco.com
- tremontsportingco.com
- dormieworkshop.com
- winstoncollection.com
- seamusgolf.com
- dimpledivot.com
- radmorgolf.com
- headgolf.com
- heathlander.com
- macadegolf.com
- local-rule.com
- fantlsport.com
- rebolf.com
- angusandgracegogolfing.com
- merrillgolf.com
- flagbaggolfco.com
- shaplandbags.com

---

## Suggested order
1. **Whitelist domains** (your action, ~5 min) — unblocks direct feed reads immediately.
2. **Newsletter inbox** (your action, ~30–45 min) — best ongoing signal; catches what feeds and search miss.
3. **Brand ledger** (my action, once A or B is live) — diff against known state, no more guessing newness.
