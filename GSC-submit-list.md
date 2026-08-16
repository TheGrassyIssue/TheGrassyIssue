# Search Console — What To Do After This Deploy

## First, a correction worth making

Search Console doesn't make you rank higher. It's a reporting tool. Submitting a URL for indexing tells Google to come crawl it sooner — it has no effect on where you land once crawled. Ranking comes from what's on the page and who links to it.

So there are two lists below. The first is the five-minute GSC job. The second is the work that actually moves position.

---

## 1. In Search Console (after Deploy TGI.command)

**Resubmit the sitemap.** Index → Sitemaps → enter `sitemap.xml` → Submit. It's now 161 URLs and validates clean. I added `sugarloaf-summer-sailing`, which was the only page missing.

**Request indexing** for these, in this order. Retitled pages matter most — Google is still showing the old title in results until it recrawls.

Retitled today, highest priority:

1. `/drops/brand-to-know-devereux-golf` — new title, +1,400 words, FAQ schema
2. `/drops/reebok-x-manors-ii` — teaser converted to full drop post
3. `/drops/walker-golf-the-par-tec-drop` — retitled, +600 words, FAQ schema

New URLs:

4. `/drops/the-towel-edit-vol-3` — new page, 18 products, FAQ schema, swipeable galleries
5. `/drops/the-ball-marker-atlas` — new page, 77 markers, 9 categories, FAQ schema
6. `/drops/brand-to-know-casualist` — Brand Revisited, retitled, all 12 prices corrected USD→GBP
7. `/drops/the-payntr-collab-edit` — new page, 33 items, FAQ schema, swipeable galleries
8. `/drops/brand-to-know-sugarloaf-social-club` — new page, 33 projects, FAQ schema, swipeable galleries
9. `/drops/the-hydration-edit`

Still outstanding from previous deploys:

5. `/drops/ssc-hidden-gem-collection`
6. `/drops/no-budget`
7. `/drops/hancock-golf-course-austin`
8. `/drops/brand-to-know-kingfisher-golf`
9. `/drops/brand-to-know-read-the-green`
10. `/drops/students-golf-summer-2026`
11. `/drops/the-magazine-edit`
12. `/drops/brand-to-know-jones-sports-co`

GSC caps manual indexing requests at roughly 10–12 a day, so do 1–4 first and the rest tomorrow.

**Then check, don't just submit:** Pages → look at "Crawled – currently not indexed" and "Discovered – currently not indexed." If pages are sitting in those buckets, that's a content-quality signal from Google and no amount of resubmitting fixes it. That's what the thin-page list below is for.

---

## 2. The work that actually affects ranking

I audited all 148 drop pages. Every one has an H1, a meta description, and a canonical — that's clean. Three real gaps:

### FAQ schema is on 17 of 148 pages

Every brand page we've given a FAQ has climbed. It's the single highest-leverage change available, because it wins the "People Also Ask" box and it forces the page to answer real queries. 131 pages don't have it.

Best candidates — brand pages that already rank top 10 and would move with a FAQ:
Sentinel, Cloud & Wind, Odd Ritual, Olydoe, TwentyFour, Mogshade, Metalwood, Huega House, Quiet Golf, Fella, Morning People, Takomo, BEAMS, Gramicci, Siegelman Stable, Random Golf Club, Nature Club.

### 24 pages are under 450 words

These are the ones most likely stuck in "Crawled – currently not indexed." The worst:

| Page | Words |
|---|---|
| the-ball-marker-edit | 257 |
| the-mackenzie-collab-edit | 261 |
| the-shoe-edit | 264 |
| the-bag-edit | 265 |
| the-headcover-edit | 267 |
| vessel-season-opener-26 | 267 |
| the-hat-edit | 268 |
| the-best-non-golfing-golf-shoe | 271 |
| the-jordan-golf-spring-edit | 271 |
| 7-divot-tools | 286 |

Two options per page: expand to 800+ words, or merge into a stronger related page with a 301. Several of these overlap heavily — there's a headcover edit, a bag edit, a hat edit and a shoe edit that could each be folded into their larger equivalents.

### 15 pages have no H2

Same fix as the sitewide pass in August. Worst offenders include `ald-golf-ss26-new-releases`, `bold-tees-carousel`, `hats-carousel`, `malbon-summer-gallo-colorido`, `manors-gentleman-jack`.

---

---

## Swipeable galleries — 24 pages updated 14 Aug 2026

Product cards on 24 existing posts were converted to swipeable image galleries, adding 946
new product photos pulled from each brand's own site. The page content and copy are unchanged;
only the image markup and card structure differ.

These do NOT need manual reindexing — Google will pick up the changes on its normal recrawl,
and the text content is identical. Do not burn daily indexing quota on them.

One real fix went out with this: the Kingfisher "Golf Tee Box" card had been using the Logo
Golfer photo. It now shows the actual tee box.

Three sites no longer expose product data, so those pages show single images:
Manors (endpoint pulled), Cloud & Wind (Squarespace), Metalwood Studio (moved to a custom build).


## Note

You already have a page at `/drops/lions-muny-is-getting-a-world-class-renovation-heres-whats-c`. Worth a look next to what the city's site currently says — their only posted project is the May driving-range resurfacing.
