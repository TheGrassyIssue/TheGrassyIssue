# Outdoor brands that pair with golf — research brief (22 Oct 2026)

Site: The Grassy Issue (thegrassyissue.com), an Austin golf-culture site that covers independent and
culture-led golf/lifestyle brands. Editor: Lenny.

## The post
"Outdoor brands that pair perfectly with golf." Brands: Arc'teryx, Salomon, Gramicci, Purple Mountain
Observatory, plus a fifth brand in the same vein.

Lenny's thesis, in his words: "I like my golf gear durable, stain resistant, weather resistant and I wanna
know it will last more than just one season. If it can survive the mountain, it will be fine for my local
muni especially in January."

Austin munis in January: roughly 35–60°F, windy, sometimes drizzly, wet grass in the morning.

## What to pick (10–12 candidates per brand; Lenny will choose 6–8)
Pieces that work for a GOLFER, not just an outdoorsman:
- Swing mobility: stretch, articulated/gusseted, not boxy or stiff at the shoulders.
- Weather: wind-resistant, water-repellent (DWR) or waterproof but quiet and light enough to swing in.
- Durable and stain resistant (grass, mud, sweat), lasts years.
- Muni-appropriate: pants/shorts that look fine on a course, layers (fleece, midlayers, light shells,
  vests), hats/caps, low shoes with traction that are OK on wet grass (spikeless-style; NOT heavy boots),
  small bags/accessories only if a golfer would use them (no 40L packs).
- Prefer men's or unisex. Avoid ski-only, mountaineering-only, heavy down parkas, harnesses.
- Mix of categories per brand; a range of prices.

## Facts and rules
- Every product: exact name, product URL, CURRENT USD price on the brand's own US store (or the brand's
  store shipping to the US, in USD), in stock (note limited sizes), color(s), and 1–2 concrete material /
  feature facts copied from the product page (fabric, DWR, Gore-Tex, stretch %, pockets, weight).
- Write a short golf-angle note (why it works on a course) per product. Plain words; never use the word
  "worth". Do not invent facts.
- Product image: the best single image URL at full resolution from the brand's own site/CDN (model shot or
  clean product shot). Note if the background is white/light studio.
- Lookbook: 4–6 of the brand's OWN campaign / editorial / lifestyle images (outdoor, mood, people wearing
  it), full resolution, landscape preferred for one hero-able image. Record URL + one-line description.
- Brand facts: founding year/place, founder(s), what the brand is known for — each with the source URL.
  1–2 verbatim quotes from the brand or founder (from interviews or the brand's own site) with source URL.
- Do NOT use Reddit or try to get around any blocked site. If a site blocks the sandbox, use the browser
  tools (Claude in Chrome) to read pages, or a reputable US retailer page only for confirming facts.
- Do not create accounts, add to cart, or submit anything.

## Output
Write JSON to `research/outdoor-golf/<slug>.json` (site root:
/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site in bash, or
/Users/margaretharrington/Desktop/TheGrassyIssue/site with file tools):
{
 "brand": "...", "slug": "...", "store": "...", "checked": "2026-10-22",
 "facts": [{"fact": "...", "source": "url"}],
 "quotes": [{"quote": "...", "who": "...", "source": "url"}],
 "products": [{"id": "x1", "name": "...", "url": "...", "price_usd": "$000", "stock": "...",
   "colors": "...", "category": "pants|shorts|shell|midlayer|fleece|vest|top|hat|shoe|accessory",
   "features": ["..."], "golf_note": "...", "img": "full-res url", "img_bg": "light|photo"}],
 "lookbook": [{"img": "full-res url", "desc": "...", "orientation": "landscape|portrait"}]
}
Also download every product image and lookbook image into `research/outdoor-golf/<slug>/` (p-<id>.jpg,
look-<n>.jpg), at the largest size available (aim ≥1600px on the long side), and verify each opens and
note its pixel size in the JSON ("img_px").
