# TGI Consistency Audit — 30 August 2026

174 drop pages scanned for structure, formatting and copy conventions.
21 distinct structural signatures are live. The house has one vein; the site
has five. Everything below is ranked by how visible it is to a reader.

---

## Tier 1 — visibly different site (fix these)

### 1. Seven pages have none of the house structure
No breadcrumb, no drop-header, no tag, no sidebar, no More-from-Feed —
pre-generator relics that render as a different website:

- bold-tees-carousel · hats-carousel · premium-tees-carousel (the three
  "carousel" relics)
- malbon-summer-gallo-colorido · manors-gentleman-jack · metalwood-ss26-picks
- muni-kids-10-years · rodeo-dunes-the-great-divide

**Fix:** rebuild on the house template (content survives, chrome replaced), or
retire + 301 the three thin "carousel" pages into their newer equivalents.

### 2. Swipeable galleries: 57 of 161 product pages
104 multi-product pages still run flat single-image cards. This is the known
26→57/136 migration, stalled about 40% through. It is the single biggest
"two eras" signal when browsing post to post.

**Fix:** resume the gallery migration in batches (the scripts and traps are
already documented in memory).

### 3. Homepage feed: 27 legacy static cards vs 177 carousel cards
The 27 old-style cards (no carousel, no arrows) sit alongside modern ones in
the same feed.

**Fix:** convert to gear-carousel cards, or accept as archive style and stop.

---

## Tier 2 — noticeable inside a page

### 4. Eight pages carry a tag of "(no tag)"
Violates the three-category rule (every post is Field Notes / Drops & Brands /
News). Same seven relic pages plus one. Fix falls out of item 1.
Homepage card tags match dedicated pages 171/171 — that part is clean.

### 5. Kickers exist on only 28 pages
`cat-kicker` (the bold-lede section intro) is the current house move but only
recent posts have it. Old section headers go straight from h2 to grid.
**Fix:** optional back-fill on the ~20 highest-traffic old pages only; writing
146 kickers is not worth it.

### 6. Sidebar label drift — 10 variants
"Details" (129) is the standard; also live: Quick Look, Quick look, Quick
Stats, The Edit, Collection Details, Quick Facts, Trip details, Tags, The
Archive. **Fix:** mechanical sweep → "Details" everywhere (keep "Trip details"
on the trip recap if you like the flavor).

### 7. h2 conventions — 116 headers not using .products-hdr
107 id-only + 9 bare h2, all on older pages, so section headers render at a
different size/tracking than recent posts. **Fix:** mechanical classing sweep.

### 8. Product-link copy — 20+ variants
"Shop ↗" (1,707) is the standard. "View ↗" (112) and "Visit ↗" (64) are fine
as venue/brand-page conventions. The stragglers — "Shop at Nike", "Shop Rouqe
Golf", "fordengolf.com", "Shop Gumtree", "Shop PUMA Golf", "Shop at ALD" —
name the destination inconsistently. **Fix:** collapse to Shop ↗ / Visit ↗ /
View on Maps ↗ / Sold Out.

---

## Tier 3 — policy decisions, not sweeps

### 9. Dates in drop-meta: 48 pages show one, 118 don't
Two philosophies live at once (dated posts vs evergreen). Pick one: either
every post shows its date, or only status-checked ranking pages do.

### 10. "Status checked" line exists on exactly 1 page
The streetwear rebuild introduced it. If it's the new standard for ranking
pages, it should roll out to the other rankings (putters, wedges, bags, etc.);
if not, it's a one-page quirk.

### 11. Word-count floor: 116 of 174 pages under 1,200 (median 904)
Known and previously accepted. Listed for completeness — this is the biggest
"vein" difference of all (deep 2,700-word rebuilds vs 600-word card pages),
but fixing it is an editorial program, not a formatting sweep.

### 12. FAQ coverage: 60 of 174
Formatting is now uniform (today's fix), but which pages *get* a FAQ is
arbitrary. Suggested rule: rankings + Brand to Knows get one; drops and
Austin food posts don't need one.

---

## Already clean (verified today)
- FAQ structure/CSS: 61/61 identical
- Search live on every page with a nav (2 no-nav relics excepted)
- Homepage/dedicated tag agreement: 100%
- Writeup body styles consistent (760px/16px standard, 3 stragglers)
- No hot-linked images, 0 console errors sitewide
