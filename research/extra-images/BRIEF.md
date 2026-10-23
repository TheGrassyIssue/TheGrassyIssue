# Extra product images — brief (23 Oct 2026)

The Grassy Issue's product cards are swipeable galleries. Three recent posts show only ONE image per product; the editor wants
MULTIPLE images of each product. Your job: collect 2–3 ADDITIONAL images per product from the brand's own product page.

Input: `research/extra-images/<post>/list.json` — each entry has `card` (number), `name`, `url` (the product page), and
`existing` (the image already used; look at it so you don't repeat the same shot).

For each product:
- Open the product page and collect 2–3 more images of THE SAME product: other angles (back, side, detail), an on-model shot,
  or a lifestyle shot from that product's gallery. Prefer the same colorway as the existing image; a second colorway of the same
  product is fine as one of the extras. Never use a different product.
- Use the largest size the brand's own CDN serves (aim ≥1200px on the long side; Shopify: strip size suffixes or add ?width=2000;
  other CDNs: look for the largest rendition in srcset/JSON).
- Save to `research/extra-images/<post>/c<card>-<n>.jpg` (n = 1,2,3), converted to RGB JPEG quality 90. Verify each opens.
- Record `research/extra-images/<post>/extras.json`: {"<card>": [{"file": "c5-1.jpg", "src": "url", "px": "WxH", "kind": "back|side|detail|model|lifestyle|alt-color"}]}.
- If a product page is gone, sold out with no gallery, or only has one image, record `"<card>": []` with a "note".

Rules: brand's own site/CDN only (an official retailer page only if the brand page has a single image — say so in the note).
Do NOT use Reddit, Pinterest or random reposts. Don't add to cart or create accounts. Some sites block the sandbox (429
"local_rate_limited" or JS shells): slow down and retry, use web_fetch, or use the Claude in Chrome browser tools (load via
ToolSearch; close any tabs you open). Sandbox shell is mcp__workspace__bash; site root there is
/sessions/admiring-pensive-ritchie/mnt/TheGrassyIssue/site (file tools: /Users/margaretharrington/Desktop/TheGrassyIssue/site).
Do not edit any site HTML or builders.

Return a short summary: products done, products with no extras (and why), total images saved.
