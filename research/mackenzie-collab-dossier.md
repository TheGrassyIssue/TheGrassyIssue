# MacKenzie Golf Bags — collab research dossier

Compiled 2026-08-27/28 for the rebuild of
`drops/the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site.html`.

**Lenny's decisions (2026-08-27):**
- Rebuild the EXISTING post at the SAME slug (keeps SEO equity). Title/H1 must change — "6 bags" will be wrong.
- Scope: **every partner, 2–4 standout editions each** (~35–40 bags). Not the full ~71-SKU archive.
- Unverifiable entries: **include with an explicit note.** Honest gaps are a credibility signal.
- Additional asks (2026-08-28): **quotes about the bags**, **IRL/lifestyle pictures**, and MacKenzie becomes a
  **TGI staple brand** — the "Staple Brands" build-out is its own piece of work, planned for the next session.

Live SKU data (71 MacKenzie items across 10 Shopify stores, pulled 2026-08-27) is in
`research/mackenzie-live-skus.json` — title, handle, published date, price, availability, variants, image URLs.
`research/` is vercelignored, so none of this deploys.

---

## The verified live inventory

Counts are MacKenzie-matching SKUs found in each store's `products.json`.

| Store | Catalogue | MacKenzie SKUs | Notes |
|---|---|---|---|
| Sugarloaf Social Club | 297 | 17 | Deepest US partner. Bags + headcovers + pouches |
| Bandon Dunes Golf Shop | 396 | 14 | Course-specific, standing programme not a drop |
| ACL Golf | 68 | 11 | Vendor field literally reads "MacKenzie x ACL GOLF" |
| Fyfe Golf (UK) | 155 | 9 | Only 19th–22nd editions live; 1–18 delisted |
| Donald Ross Sportswear | 493 | 7 | Numbered series I–V |
| Miura | 203 | 5 | Incl. Kaicho and the Miura × Sentinel |
| Students Golf | 607 | 4 | Three-way with SSC |
| Top 100 Golf Courses | 15 | 2 | GBP pricing, incl. members-only Lockhart |
| Jain Golf | 120 | 1 | 1st Edition only; no later editions exist |
| PowerBilt | 133 | 1 | See warning below |
| Bettinardi | 750 | **0** | Betti Boy is fully delisted |

### Key dated releases (from Shopify `published_at`)

- **Fyfe 19th & 20th "Between Tides"** — 2026-04-23, £650, both sold out
- **Fyfe 21st & 22nd "Coastal Tones"** — 2026-08-11, £650, both sold out
- **SSC Sail Bags "1492" / "8185" / "4923"** — 2026-07-28, $975 each, recycled Laser sailcloth
- **SSC White Leather Double Seve 8"** — 2026-03-15, $1,400
- **SSC Double Seve 8"** — 2026-03-15, $850
- **SSC Hidden Gem** — 2026-08-11, $850
- **Students × SSC × MacKenzie** — 2026-02-10, $875, 500D Cordura camo
- **Miura × Sentinel Walker** — 2026-07-23, $1,360, 1680D CORDURA woven in Japan
- **Miura Kaicho Walker** — 2025-08-02, $1,250, black leather, Miura Hanko stamp
- **Donald Ross I–V** — 2026-07-08 (plus the original, 2025-11-11), $795 each
- **Bandon "Custom Ghost Tree"** — 2026-08-26, $735 — newest course edition anywhere
- **Jain 1st Edition** — 2023-03-06, $720, Colonial Blue treated canvas
- **Top 100 Exclusive Edition** — £795; **Lockhart Edition** — £795, members-only passcode

---

## Warnings — do not publish without resolving

1. **PowerBilt is suspect.** Real Shopify product (published 2026-03-13, $699, sold out) BUT the copy describes a
   *stand bag with integrated legs and dual straps*, which is not a MacKenzie product type; image filenames say
   "Olive" while variants say Sand/Orange/Black; and the lead SKU is literally `Hireko Ignore`. Reads as templated
   boilerplate. Either verify with a real photo or leave it out.
2. **Fyfe back-catalogue prices are low confidence.** The 12th ($811), 13th ($819) and 18th ($895) figures came
   from search-engine caches of dead pages, not live sources, and the cache visibly blended copy between adjacent
   edition numbers. Do not print these as fact.
3. **Fyfe editions 4, 14, 15, 16 have no public product record.** Editions 2, 3, 8, 9 exist only as a bare URL slug
   or a social caption. Editions 1–18 are all delisted. Wayback and archive.today are blocked to the agent tooling.
   *Note:* a lookbook page for editions 14–16 DOES exist even though the products don't —
   `fyfegolf.com/pages/fyfe-x-mackenzie-lookbook-editions-14-16`. Good imagery source, and partial proof they shipped.
4. **The "July 2026" Fyfe collab did not land in July.** Their sign-up block still says July 2026; the bags that
   fulfilled it (21st/22nd) were created 28 Jul but published 11 Aug 2026. No 23rd edition announced.
5. **Miura's core three-bag Walker line is 2020**, outside the 3–4 year window. Miura's own Collaborations page does
   not list MacKenzie as a collaborator at all — it treats MacKenzie as a maker/supplier and Sentinel as the partner.

---

## Partner roster (confirmed)

**Apparel / lifestyle:** Sugarloaf Social Club (+ three-ways with Students Golf and Quiet Golf), Holderness & Bourne
(10th anniversary, navy ballistic nylon, page now dead), Donald Ross Sportswear, Jain Golf, ACL Golf, Imperfects,
Bogey Boys (Youth on Course charity, Aug 2022), Gumtree Golf & Nature Club, SWAG (2020, $666.66, five-minute lottery).

**Equipment:** Miura (Original Walker line 2020, Kaicho 2025, Miura × Sentinel 2026), Sentinel Golf (4 own models:
Ultracomp Walker 2.0 $890, X50 Walker $810, Basecamp Walker $890, Sørensen Walker $1,750), Bettinardi (Betti Boy,
$900, HIVE-only, delisted), PowerBilt (see warning).

**Media / community:** Broken Tee Society / The Golfer's Journal (Vol. 1, **10 physical bags**, dispatched
2024-03-07; at least two later un-numbered drops incl. one July 2025 — **do NOT print "Vol. 2", it isn't published**),
Top 100 Golf Courses + Lockhart Travel Club.

**Courses / institutions:** Bandon Dunes (12 SKUs across Bandon Dunes, Pacific Dunes, Bandon Trails, Old Macdonald,
Sheep Ranch, Bandon Preserve, Ghost Tree), plus — from MacKenzie's own blog only, nothing publicly listed —
**Walker Cup (30 drop-ship bags ordered at Cypress in September 2025)**, **the R&A**, **Punta Brava** (new Doak
course in Baja), and a 60-bag order for **Golf Pride**.

**International:** Fyfe Golf (Scotland, 22 numbered editions, Halley Stevenson mill canvas from Dundee),
**BEAMS Golf Japan** — 別注 digital camouflage caddie bag, released 2026-01-17, ¥143,000 incl. tax, ships with a
wooden stand; companion pouch ¥16,500. Genuine Japanese exclusive and a strong story beat.

**Checked, nothing found:** Malbon, Todd Snyder, Manors, Devereux, Eastside, Metalwood, Random Golf Club, Criquet,
Jones Sports Co, Linksoul, Seamus, Ghost Golf, Birds of Condor, Duca del Cosma, Good Good, Barstool, No Laying Up,
The Fried Egg, Ping, Titleist, Callaway, TaylorMade, Cobra, Mizuno, Vessel, Stitch, all Korean partners.

**False-positive traps:** The Fried Egg's "MacKenzie Bunker" headcover is an *Alister MacKenzie* motif by Handcrafted
Golf — different MacKenzie. Linksoul's "MacKenzie Stretch Cord" pant is a fabric-mill name. Silvies Valley Ranch bags
are Seamus, not MacKenzie.

---

## The one great quote we have

MacKenzie CEO **Nic Mulflur**, company blog, 2026-11-05 — verified verbatim at
`https://www.mackenziegolfbags.com/about/blog/mackenzie-update/`:

> "On the docket right now is a 60 golf bag order for Golf Pride, a couple of Sugarloaf projects, a large stock order
> for the new Doak course in Baja called Punta Brava (place looks unreal). 30 drop ship Walker Cup bags that were
> ordered at Cypress in September, a batch of Sentinel x Miura bags, a batch of bags for the R&A, our normal flow of
> Sentinel, Miura and Gumtree orders, as well as a big project with Fyfe Golf in Scotland."

This single passage is the backbone of the piece — it is the only public evidence of the Walker Cup, R&A and Punta
Brava work, and it shows the order book rather than describing it.

Also verified: **Ian Gilley**, founder of Sugarloaf Social Club, to Boardroom (2026-02-27),
`https://boardroom.tv/sugarloaf-students-collab-golf-interview/`:

> "A thousand-dollar bag with MacKenzie, but also t-shirts."

**Quote hunt is INCOMPLETE** — the agent running it was cut off by an API error before reporting. Re-run it next
session. Targets: Nic Mulflur interviews/podcasts, the founder/origin story (bags since ~1985), partner founders
(Fyfe, H&B, Donald Ross, ACL, Sentinel), and any maker/craftsperson on the bench.

---

## Imagery — where the good stuff is

Full ranked URL list is in the session transcript; the essentials:

**Fyfe Golf is the only rich source of MacKenzie lifestyle photography on the open web.** Their lookbooks:
- Between Tides (19th/20th, Isle of Seil GC + a boat crossing + Crinan Harbour) — `/pages/between-tides-lookbook-fyfe-golf`
- Shooters Club (17th/18th, Glen Affric estate, gundogs, Land Rover, stalker's hut) — `/pages/the-shooters-club-lookbook`
- Editions 14–16 (coastal dunes) — `/pages/fyfe-x-mackenzie-lookbook-editions-14-16`
- Editions 5/6/7 (VW Westfalia, seaside) — `/pages/mackenzie-golf-bags-fyfe-golf-limited-editions`

Shopify trick: drop the `&width=` param for the master original, or use `&width=2400`.

**MacKenzie's own on-course images** (only good ones they host): Winter Park night golf with glowing balls, Aiken
Golf Club (Jay Revell essay), Sweetens Cove, and two winners collecting bags at the SSC Shindig.

**Workshop photography essentially does not exist as stills.** Best available are frame-grabs from their "Process"
and "Ethos" films on Vimeo. If we want real Oregon bench photography, email MacKenzie for press assets.

**Skip:** MacKenzie's `/mackenzie-gallery/` (250 images, all grey-sweep packshots) and any Fyfe file named
`*pack*`, `*packshot*`, `*silo*`, or the 19th/20th `*natural*`/`*Blue1-3*` seamless shots.

**Fetch gotcha:** fyfegolf.com dedupes aggressively and falsely returns "already fetched" — append `?utm_source=x`
to bust it. Do NOT append `?view=full`; Shopify reads `view` as a template selector and serves a different page.

---

## Next session — running order

1. Re-run the quote hunt (it died mid-flight). Also finish the imagery sweep for the partner retailers and
   editorial outlets, which never ran.
2. Lock the ~35–40 bag lineup from `mackenzie-live-skus.json`; resolve or drop PowerBilt.
3. Download ALL imagery locally (never hot-link), lifestyle frames first.
4. Rebuild the post at the same slug. House format: `h2` + `cat-kicker` + `products-grid`. GQ voice per VOICE.md —
   opener about the brand/idea, never an individual item. New title, since "6 bags" is wrong.
5. Add MacKenzie to `data/brands.json` + the brand index — it is currently NOT in there at all, despite being the
   maker behind dozens of items we already cover. This is the prerequisite for staple-brand status.
6. Verify (`verify-post.py`, `voice-lint.py`), fact-check every price/date, render a preview for approval, then sync.
