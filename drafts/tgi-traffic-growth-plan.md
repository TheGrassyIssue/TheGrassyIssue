# The Grassy Issue — Traffic Growth Plan
*May 12, 2026 · From zero organic to a self-sustaining audience*

---

## The Diagnosis

Google has no idea TheGrassyIssue.com exists. A `site:thegrassyissue.com` search returns zero results. Searching for "the grassy issue golf" returns nothing relevant. The site has no `robots.txt`, no `sitemap.xml`, and no Google Search Console verification — which means Google's crawlers have no roadmap for your pages and likely haven't indexed most of them.

The good news: the site itself is well-built. You've got clean HTML, proper meta descriptions, Open Graph tags on the homepage, structured data (JSON-LD), canonical URLs, and real content across 12 live pages. The foundation is solid — it just needs to be made visible.

---

## Phase 1: Quick Wins (This Week)

These are the highest-impact, lowest-effort fixes. Do them all — they take an afternoon combined.

### 1. Add robots.txt
Create a file at the root of your site that tells search engines they're welcome to crawl everything. Without it, some crawlers won't bother.

```
User-agent: *
Allow: /
Sitemap: https://thegrassyissue.com/sitemap.xml
```

### 2. Add sitemap.xml
A sitemap lists every page you want Google to find. Right now you have ~12 live pages — list them all. This is the single most important thing you can do today.

### 3. Submit to Google Search Console
Go to search.google.com/search-console, verify ownership of thegrassyissue.com (easiest method: add a TXT record to your domain DNS, or upload a verification HTML file), then submit your sitemap. Google will start crawling within days.

### 4. Add OG tags to every page
Your homepage has Open Graph tags, but check that every subpage (guides, drops, events, field guide) also has them. When someone shares a link on Instagram Stories, Twitter, or a group chat, the OG image and description are what people see. Missing tags = a blank preview card = nobody clicks.

### 5. Link Instagram bio → site
Make sure your IG bio has the direct link to thegrassyissue.com. This is your only traffic bridge right now. Consider a Linktree alternative if you want to point to specific guides or drops.

### 6. Set up analytics
Install something to measure what's happening. Options from simplest to most detailed:
- **Vercel Analytics** (you're already on Vercel — may be one toggle)
- **Plausible** (privacy-friendly, simple, ~$9/mo)
- **Google Analytics 4** (free, more complex, better for SEO tracking)

You can't improve what you can't measure.

---

## Phase 2: Content Engine (Weeks 2–6)

This is where you go from "site exists" to "site ranks." The strategy: own a few specific keyword niches before trying to compete broadly.

### Your unfair advantage: Austin muni guides

You already have hole-by-hole guides for Hancock, Lions, Roy Kizer, and Morris Williams. Nobody else on the internet is publishing this level of detail for Austin's municipal courses. The competitive landscape for "Austin muni golf guide" or "Hancock golf course Austin guide" is almost empty — the top results are generic GolfPass listings and TripAdvisor reviews.

**Action items:**
- Create an index page at `/guides/` that links to all four course guides and positions itself as "The definitive guide to Austin's municipal golf courses."
- Write meta descriptions targeting specific long-tail keywords: "Hancock Golf Course hole by hole guide Austin TX," "Lions Municipal Golf Course tips," "Roy Kizer Golf Course guide."
- Add internal links between guides ("Played Hancock? Lions is 10 minutes away — here's our guide").
- Expand to the remaining Austin munis over time (Jimmy Clay, Grey Rock, Bluebonnet Hill).

### Brand profile pages

You're already writing about these brands in drop cards. Expand them into standalone profile pages at `/brands/[name]` — a short intro to the brand, why TGI covers them, and links to every drop card you've published for them. These pages rank for "[brand name] review" and "[brand name] golf" searches, and they give your drop coverage a permanent home.

### "Best of" roundup content

Create 2–3 pillar articles that cast a wider net:
- "The Best Golf Streetwear Brands in 2026" (you literally track 12 of them)
- "Austin Muni Golf: The Complete Guide to Public Golf in Austin"
- "Best Golf Accessories Under $100" (curated from your drop coverage)

These longer pages rank for broader keywords and link down into your specific drop and guide pages, building internal link authority.

### Keywords to target

| Keyword | Competition | Your advantage |
|---------|-------------|----------------|
| austin muni golf guide | Very low | You have 4 hole-by-hole guides — nobody else does |
| hancock golf course austin | Low | Your guide is more detailed than anything on page 1 |
| golf streetwear brands 2026 | Medium | You cover 12+ brands with weekly updates |
| malbon golf new drop | Medium | Your drop cards are fresher than Hypebeast coverage |
| quiet golf brand | Low | Profile page + drop history would rank easily |
| lions municipal golf course tips | Very low | Your hole-by-hole guide is unmatched |

---

## Phase 3: Audience Building (Ongoing)

SEO takes weeks to months. Meanwhile, build direct traffic through social and community.

### Instagram strategy

You already have an account. Here's how to make it a traffic driver:

- **Carousel posts for drops**: Turn your draft cards into Instagram carousels — 3–5 slides per post with the product image, your three-sentence writeup, and a "link in bio" CTA. This is your most repeatable content format.
- **Muni photo series**: Post course photos from your Austin rounds with the hole number, yardage, and one tip. Tag the course, use location. These get local engagement and build your identity as the Austin muni voice.
- **Tag brands**: When you post drop coverage, tag the brand. Some will reshare you, which puts TGI in front of their audience. This is especially effective with smaller brands (Gumtree, Sentinel, Fyfe) who are more likely to engage.
- **Stories with poll stickers**: "Would you pay $130 for a fleece from a PUMA x nature club collab?" — this drives engagement and the algorithm loves it.

### Reddit r/golf

r/golf has 1M+ members. Share your Austin muni guides there — "I wrote a hole-by-hole guide to Hancock, the oldest muni in Texas" will get upvotes. Don't spam; contribute genuinely. One good Reddit post can drive more traffic than a month of Instagram.

### Email newsletter

Even a simple monthly email keeps people coming back. Use Buttondown (free up to 100 subscribers) or Substack. Content: a recap of the month's best drops, one muni tip, and a link to any new guides. The newsletter is also a future monetization path if you want it.

### Pitch to golf culture accounts

Skratch Golf, The Fried Egg, No Laying Up, and similar accounts cover golf culture. Your Austin muni guides and brand coverage are the kind of content they share. A DM to Skratch saying "I wrote the most detailed guide to Austin's municipal courses — here it is" could get you real exposure.

---

## Technical SEO Checklist

Things I found during the audit that should be cleaned up:

- [x] Homepage has meta description, OG tags, canonical URL, JSON-LD ✓
- [ ] **Add `robots.txt`** — missing entirely
- [ ] **Add `sitemap.xml`** — missing entirely
- [ ] **Submit to Google Search Console** — site has zero indexed pages
- [ ] **Add canonical URLs to all subpages** — check guides, drops, events
- [ ] **Add OG tags to all subpages** — some may be missing
- [ ] **Create a `/guides/` index page** — right now guides are orphaned (no parent page links to them as a collection)
- [ ] **Add internal cross-links** — guides don't link to each other, drops don't link to brand pages
- [ ] **Verify OG image exists** — homepage references `/images/og-image.jpg`, confirm it's there and looks good when shared

---

## What I Can Do Right Now

If you want, I can:
1. **Generate the `robots.txt` and `sitemap.xml` files** and add them to the site
2. **Create a `/guides/` index page** that links to all four Austin muni guides
3. **Audit every page for missing meta tags** and fix them
4. **Build a content calendar** for the next 4 weeks of posts (drops + guides + roundups)

Just say the word.
