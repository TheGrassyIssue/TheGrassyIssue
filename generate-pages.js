#!/usr/bin/env node
/**
 * TGI Post Page Generator — Layer 2 (v2)
 *
 * Extracts carousel data + per-slide descriptions from index.html
 * and generates standalone pages with full product writeups.
 *
 * Usage:  node generate-pages.js [--dry-run] [--force]
 *   --dry-run   List what would be generated without writing
 *   --force     Overwrite existing generated pages
 */

const fs = require('fs');
const path = require('path');

const SITE = __dirname;
const html = fs.readFileSync(path.join(SITE, 'index.html'), 'utf8');
const DRY  = process.argv.includes('--dry-run');
const FORCE = process.argv.includes('--force');

/* ── 0. Load editorial writeups ──────────────────────────── */
const writeupsFile = path.join(SITE, 'writeups-all.json');
const editorialWriteups = fs.existsSync(writeupsFile) ? JSON.parse(fs.readFileSync(writeupsFile,'utf8')) : {};
console.log(`Loaded ${Object.keys(editorialWriteups).length} editorial writeups.\n`);

/* ── helpers ──────────────────────────────────────────────── */
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const strip = s => s.replace(/<[^>]+>/g, '').trim();
const squeeze = s => s.replace(/\s+/g, ' ').trim();
const slugify = s => s.toLowerCase().replace(/['']/g,'').replace(/&amp;/g,'and').replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'').substring(0,60);

/* ── 1. Extract _slideTexts from JS ──────────────────────── */
const slideTexts = {};  // carouselId → string[]
const stBlock = html.match(/window\._slideTexts\s*=\s*\{([\s\S]*?)\n  \};/);
if (stBlock) {
  const entries = stBlock[1].matchAll(/(\w+):\s*\[([\s\S]*?)\]/g);
  for (const [, id, body] of entries) {
    // Parse the string array — handle escaped quotes
    const texts = [];
    const strRe = /"((?:[^"\\]|\\.)*)"/g;
    let m;
    while ((m = strRe.exec(body)) !== null) {
      texts.push(m[1].replace(/\\"/g, '"').replace(/\\n/g, '\n'));
    }
    slideTexts[id] = texts;
  }
}
console.log(`Loaded _slideTexts for ${Object.keys(slideTexts).length} carousels.\n`);

/* ── 2. Find card boundaries in feed ─────────────────────── */
const feedStart = html.indexOf('<section class="feed" id="feed"');
const feedEnd   = html.indexOf('</section>', feedStart + 100);

const cardStarts = [];
const startRe = /(?:<div|<a[^>]*href)[^>]*class="card"[^>]*data-type="([^"]+)"[^>]*>/g;
let sm;
while ((sm = startRe.exec(html)) !== null) {
  if (sm.index >= feedStart && sm.index <= feedEnd) {
    cardStarts.push({ idx: sm.index, type: sm[1] });
  }
}

/* ── 3. Parse each card ──────────────────────────────────── */
const allCards = [];
// Pre-existing manually-named pages we don't overwrite
const manualSlugs = new Set([
  'ald-golf-ss26-new-releases', 'muni-kids-10-years', 'manors-gentleman-jack',
  'malbon-summer-gallo-colorido', 'metalwood-ss26-picks', 'sugarloaf-ss26',
  'premium-tees-carousel', 'bold-tees-carousel', 'hats-carousel',
  'best-golf-streetwear-brands-2026', 'manors-ss26',
  'brand-to-know-read-the-green',
  'austin-bbq-field-guide',
  'arsham-malbon-chapter-three',
  'the-glove-edit'
]);

for (let i = 0; i < cardStarts.length; i++) {
  const start = cardStarts[i].idx;
  const end = (i + 1 < cardStarts.length) ? cardStarts[i + 1].idx : feedEnd;
  const c = html.substring(start, end);
  const type = cardStarts[i].type;

  // Skip link-only, field-note, and non-carousel cards
  if (/^<a[^>]*href="https?:\/\//.test(c)) continue;
  if (/^<a[^>]*href="\//.test(c)) continue;
  if (type === 'field') continue;

  const carouselM = c.match(/data-carousel="([^"]+)"/);
  if (!carouselM) continue;
  const carouselId = carouselM[1];

  // Title — handle both <div> and <h2>
  const titleM = c.match(/<(?:div|h[1-6])\s+class="card-title"[^>]*>(?:<a[^>]*>)?([\s\S]*?)(?:<\/a>)?<\/(?:div|h[1-6])>/);
  const title = titleM ? squeeze(strip(titleM[1])) : '';
  if (!title) continue;

  // Tag
  const tagM = c.match(/<span class="card-tag[^"]*">\[?([^\]<]+)\]?<\/span>/);
  const tag = tagM ? strip(tagM[1]) : 'Drop';

  // Card-level description (initial text shown)
  const textM = c.match(/<(?:div|p) class="card-text"[^>]*>([\s\S]*?)<\/(?:div|p)>/);
  const cardDesc = textM ? squeeze(strip(textM[1])) : '';

  // Source link + price
  const srcM = c.match(/<(?:div|span) class="card-source"[^>]*>[\s\S]*?<a href="(https?:\/\/[^"]+)"[^>]*>([^<]+)<\/a>([\s\S]*?)<\/(?:div|span)>/);
  const sourceUrl = srcM ? srcM[1] : '';
  const sourceDomain = srcM ? strip(srcM[2]) : '';
  const priceM = srcM ? (srcM[3] || '').match(/·\s*(\$[\d,]+\s*[–\-]\s*\$[\d,]+)/) : null;
  const priceRange = priceM ? priceM[1] : '';

  // Slides: linked products <a href><img><slide-info></a>
  const slides = [];
  const slideRe = /<div class="gear-slide">\s*<a href="([^"]+)"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"([\s\S]*?)<\/a>\s*<\/div>/g;
  let lm;
  while ((lm = slideRe.exec(c)) !== null) {
    const brandM = lm[4].match(/gear-slide-brand">([^<]+)/);
    const nameM  = lm[4].match(/gear-slide-name">([^<]+)/);
    slides.push({
      href: lm[1], src: lm[2], alt: lm[3],
      brand: brandM ? strip(brandM[1]) : '',
      name: nameM ? strip(nameM[1]) : ''
    });
  }
  // Unlinked slides
  if (!slides.length) {
    const ulRe = /<div class="gear-slide"[^>]*>[\s\S]*?<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"([\s\S]*?)<\/div>/g;
    let um;
    while ((um = ulRe.exec(c)) !== null) {
      const brandM = um[3].match(/gear-slide-brand">([^<]+)/);
      const nameM  = um[3].match(/gear-slide-name">([^<]+)/);
      slides.push({
        href: sourceUrl, src: um[1], alt: um[2],
        brand: brandM ? strip(brandM[1]) : '',
        name: nameM ? strip(nameM[1]) : ''
      });
    }
  }

  // Per-slide descriptions from _slideTexts
  const perSlide = slideTexts[carouselId] || [];

  const slug = slugify(title);
  const pagePath = `drops/${slug}`;

  allCards.push({ carouselId, title, tag, cardDesc, sourceUrl, sourceDomain,
                  priceRange, slides, perSlide, slug, pagePath, type });
}

console.log(`Parsed ${allCards.length} carousel cards.`);

/* ── 4. Determine which pages to generate ────────────────── */
const toGen = [];
for (const card of allCards) {
  if (manualSlugs.has(card.slug)) {
    console.log(`  SKIP  ${card.pagePath} (manual page)`);
    continue;
  }
  const fp = path.join(SITE, 'drops', card.slug + '.html');
  if (fs.existsSync(fp) && !FORCE) {
    console.log(`  SKIP  ${card.pagePath} (exists)`);
    continue;
  }
  toGen.push(card);
}
console.log(`\nPages to generate: ${toGen.length}`);
if (DRY) { toGen.forEach(c => console.log(`  ${c.pagePath} (${c.slides.length} slides, ${c.perSlide.length} texts)`)); process.exit(0); }

/* ── 5. Hashtag helper ───────────────────────────────────── */
function hashtags(title, tag) {
  const t = new Set(['#TheGrassyIssue','#GolfCulture']);
  const lo = tag.toLowerCase();
  if (lo.includes('drop'))    t.add('#NewDrop');
  if (lo.includes('edit'))    t.add('#GearEdit');
  if (lo.includes('guide'))   t.add('#GolfGuide');
  if (lo.includes('brand'))   t.add('#BrandToKnow');
  if (lo.includes('roundup')) t.add('#TheRoundup');
  if (lo.includes('news'))    t.add('#GolfNews');
  const tl = title.toLowerCase();
  if (tl.includes('golf'))    t.add('#GolfStyle');
  if (tl.includes('austin'))  t.add('#AustinGolf');
  if (tl.includes('ss26') || tl.includes('2026')) t.add('#SS26');
  if (tl.includes('putter'))  t.add('#Putters');
  if (tl.includes('hat') || tl.includes('bucket')) t.add('#GolfHats');
  if (tl.includes('shoe') || tl.includes('jordan') || tl.includes('nike')) t.add('#GolfShoes');
  if (tl.includes('bag'))     t.add('#GolfBags');
  if (tl.includes('driver'))  t.add('#GolfDrivers');
  if (tl.includes('rangefinder')) t.add('#Rangefinders');
  if (tl.includes('towel'))   t.add('#GolfTowels');
  if (tl.includes('headcover') || tl.includes('cover')) t.add('#Headcovers');
  t.add('#GolfFashion');
  return [...t].slice(0,10);
}

/* ── 6. Page template ────────────────────────────────────── */
function buildPage(card) {
  const editText = editorialWriteups[card.carouselId] || card.cardDesc || '';
  const metaDesc = editText
    ? editText.replace(/\n+/g,' ').substring(0,155).replace(/\s+\S*$/,'') + '…'
    : `${card.title} — curated by The Grassy Issue.`;
  const url = `https://thegrassyissue.com/${card.pagePath}`;
  const today = new Date().toISOString().split('T')[0];
  const tags = hashtags(card.title, card.tag);
  const tagColor = /drop|news/i.test(card.tag) ? 'flag' : 'grass';

  // Product grid with per-slide descriptions
  const productCards = card.slides.map((s, i) => {
    const displayName = s.name || s.alt || `Item ${i + 1}`;
    const brand = s.brand || '';
    const link = s.href || card.sourceUrl || '#';
    const desc = (card.perSlide[i] || '').trim();

    return `
    <a href="${esc(link)}" target="_blank" rel="noopener" class="product-card">
      <div class="product-img">
        <img src="${esc(s.src)}" alt="${esc(s.alt || displayName)}" loading="lazy" />
      </div>
      <div class="product-body">
        ${brand ? `<div class="product-brand">${esc(brand)}</div>` : ''}
        <div class="product-name">${esc(displayName)}</div>
        ${desc ? `<div class="product-desc">${esc(desc)}</div>` : ''}
        ${link !== '#' ? '<span class="product-link">Shop ↗</span>' : ''}
      </div>
    </a>`;
  }).join('\n');

  // "More from the Feed" cross-links
  const related = allCards
    .filter(c => c.carouselId !== card.carouselId && c.slides.length > 0)
    .sort(() => Math.random() - 0.5).slice(0,4);

  const moreHtml = related.map(rc => {
    const img = rc.slides[0];
    return `
    <a href="/${rc.pagePath}" class="more-card">
      <div class="more-card-img"><img src="${esc(img.src)}" alt="${esc(rc.title)}" loading="lazy" /></div>
      <div class="more-card-body">
        <div class="more-card-name">${esc(rc.title.substring(0,45))}</div>
        <div class="more-card-tag">${esc(rc.tag)}</div>
      </div>
    </a>`;
  }).join('\n');

  // Use editorial writeup if available, fall back to card description
  const editorial = editorialWriteups[card.carouselId];
  let descParas;
  if (editorial) {
    descParas = editorial.split(/\n\n+/).map(p => `<p>${p.trim()}</p>`).join('\n    ');
  } else if (card.cardDesc) {
    descParas = card.cardDesc.split(/(?<=\.)\s+/).reduce((a,s,i)=>{if(i%3===0)a.push([]);a[a.length-1].push(s);return a;},[]).map(g=>`<p>${g.join(' ')}</p>`).join('\n    ');
  } else {
    descParas = '<p>Curated by The Grassy Issue.</p>';
  }

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>${esc(card.title)} — The Grassy Issue</title>
<meta name="description" content="${esc(metaDesc)}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:type" content="article" />
<meta property="og:url" content="${url}" />
<meta property="og:title" content="${esc(card.title)} — The Grassy Issue" />
<meta property="og:description" content="${esc(metaDesc)}" />
<meta property="og:image" content="https://thegrassyissue.com/images/og-image.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${esc(card.title)}" />
<meta name="twitter:description" content="${esc(metaDesc)}" />
<link rel="canonical" href="${url}" />
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${card.title.replace(/"/g, '\\"')}",
  "description": "${metaDesc.replace(/"/g, '\\"')}",
  "url": "${url}",
  "datePublished": "${today}",
  "dateModified": "${today}",
  "author": { "@type": "Organization", "name": "The Grassy Issue" },
  "publisher": {
    "@type": "Organization",
    "name": "The Grassy Issue",
    "url": "https://thegrassyissue.com/"
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "${url}" }
}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400;1,9..144,500&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>
:root{--ink:#141414;--paper:#F4F1EA;--grass:#2D4A2B;--rough:#A8A878;--flag:#C7362C;--serif:'Fraunces',Georgia,serif;--sans:'Inter',-apple-system,sans-serif;--mono:'JetBrains Mono',monospace}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
html,body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}a:focus-visible,button:focus-visible{outline:2px solid var(--grass);outline-offset:2px}img{max-width:100%;display:block}button{font:inherit;cursor:pointer;border:none;background:none}
.nav{position:sticky;top:0;background:var(--paper);border-bottom:.5px solid var(--ink);z-index:15}
.nav-inner{max-width:1400px;margin:0 auto;padding:18px 32px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.nav-wordmark{font-family:var(--serif);font-style:italic;font-weight:400;font-size:26px;letter-spacing:-.01em;line-height:1;white-space:nowrap}
.nav-links{display:flex;gap:24px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase}
.nav-links a{padding:6px 0;border-bottom:1px solid transparent;transition:border-color .15s}.nav-links a:hover{border-bottom-color:var(--ink)}
.nav-cta{padding:9px 16px;background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;transition:background .2s;display:inline-block}.nav-cta:hover{background:var(--grass)}
.nav-toggle{display:none;width:28px;height:20px;flex-direction:column;justify-content:space-between;padding:0}.nav-toggle span{display:block;width:100%;height:1.5px;background:var(--ink)}
.breadcrumb{max-width:1400px;margin:0 auto;padding:16px 32px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.6}.breadcrumb a:hover{opacity:1}.breadcrumb span{margin:0 8px}
.drop-header{max-width:1400px;margin:0 auto;padding:0 32px 40px}
.drop-tag{display:inline-block;padding:5px 10px;font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;margin-bottom:16px}
.drop-tag.flag{background:var(--flag);color:var(--paper)}.drop-tag.grass{background:var(--grass);color:var(--paper)}
.drop-header h1{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(32px,4.5vw,56px);line-height:1.05;letter-spacing:-.02em;margin-bottom:16px;max-width:800px}
.drop-meta{display:flex;align-items:center;gap:24px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;flex-wrap:wrap}
.drop-meta .dot{width:3px;height:3px;border-radius:50%;background:var(--ink);opacity:.4}
.drop-hero{max-width:1400px;margin:0 auto;padding:0 32px}.drop-hero-img{width:100%;aspect-ratio:21/9;border:.5px solid var(--ink);overflow:hidden}.drop-hero-img img{width:100%;height:100%;object-fit:cover}
.writeup{max-width:1400px;margin:0 auto;padding:40px 32px;display:grid;grid-template-columns:2fr 1fr;gap:60px;align-items:start}
.writeup-body{font-size:16px;line-height:1.7;max-width:700px}.writeup-body p+p{margin-top:16px}
.sidebar{position:sticky;top:80px}
.sidebar-card{border:.5px solid var(--ink);padding:24px}
.sidebar-label{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.55;margin-bottom:16px}
.sidebar-detail{font-size:13px;margin-bottom:8px;display:flex;justify-content:space-between}.sidebar-detail .l{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.55}
.sidebar-cta{display:block;margin-top:20px;padding:14px 24px;background:var(--ink);color:var(--paper);text-align:center;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;transition:background .2s}.sidebar-cta:hover{background:var(--grass)}
.hashtags{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;padding-top:16px;border-top:.5px solid rgba(20,20,20,.12)}
.hashtag{display:inline-block;padding:4px 10px;border:.5px solid var(--ink);font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.6;transition:opacity .15s,background .15s}.hashtag:hover{opacity:1;background:var(--ink);color:var(--paper)}
.products{max-width:1400px;margin:0 auto;padding:0 32px;border-top:.5px solid var(--ink);padding-top:40px}
.products-hdr{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.55;margin-bottom:24px}
.products-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.product-card{border:.5px solid var(--ink);overflow:hidden;transition:transform .2s,box-shadow .2s;display:block}.product-card:hover{transform:translateY(-3px);box-shadow:0 6px 0 -2px var(--ink)}
.product-img{aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}.product-img img{width:100%;height:100%;object-fit:cover;transition:transform .3s}.product-card:hover .product-img img{transform:scale(1.03)}
.product-body{padding:20px 22px}
.product-brand{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.5;margin-bottom:6px}
.product-name{font-family:var(--serif);font-style:italic;font-size:20px;line-height:1.25;margin-bottom:10px}
.product-desc{font-family:var(--sans);font-size:13px;line-height:1.55;opacity:.75;margin-bottom:12px}
.product-link{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;opacity:.7;transition:opacity .15s}.product-link:hover{opacity:1}
.more{max-width:1400px;margin:48px auto 0;padding:0 32px;border-top:.5px solid var(--ink);padding-top:32px}
.more-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.more-label{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.55}
.more-link{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px}
.more-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.more-card{border:.5px solid var(--ink);overflow:hidden;transition:transform .2s;display:block}.more-card:hover{transform:translateY(-2px)}
.more-card-img{aspect-ratio:1/1;overflow:hidden;background:#e8e5dc}.more-card-img img{width:100%;height:100%;object-fit:cover}
.more-card-body{padding:12px}
.more-card-name{font-family:var(--serif);font-style:italic;font-size:14px;line-height:1.25;margin-bottom:4px}
.more-card-tag{font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;opacity:.55}
footer{border-top:.5px solid var(--ink);margin-top:80px;padding:40px 32px 24px}
footer .inner{max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;opacity:.55}
@media(max-width:820px){.nav-links,.nav-cta{display:none}.nav-toggle{display:flex}.nav-inner{padding:14px 20px}.breadcrumb{padding:12px 20px}.drop-header{padding:0 20px 32px}.drop-hero{padding:0 20px}.writeup{padding:32px 20px;grid-template-columns:1fr;gap:24px}.sidebar{position:static}.products{padding:0 20px;padding-top:32px}.products-grid{grid-template-columns:repeat(2,1fr)}.more{padding:0 20px;padding-top:24px}.more-grid{grid-template-columns:repeat(2,1fr)}footer{padding:32px 20px 20px;margin-top:48px}}
@media(max-width:480px){.products-grid{grid-template-columns:1fr}.more-grid{grid-template-columns:1fr 1fr}.drop-header h1{font-size:28px}}
</style>
</head>
<body>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-wordmark">The Grassy Issue</a>
    <div class="nav-links">
      <a href="/#feed">The Feed</a>
      <a href="/field-guide/">Field Guide</a>
      <a href="/events/">Events</a>
      <a href="/scoreboard">Scoreboard</a>
    </div>
    <button class="nav-toggle" aria-label="Open menu"><span></span><span></span><span></span></button>
    <a href="/scoreboard#submit" class="nav-cta">Post a score →</a>
  </div>
</nav>

<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">${esc(card.tag)}</a><span>/</span>
  ${esc(card.title.substring(0,40))}
</div>

<header class="drop-header">
  <span class="drop-tag ${tagColor}">[${esc(card.tag)}]</span>
  <h1>${esc(card.title)}</h1>
  <div class="drop-meta">
    ${card.sourceDomain ? `<span>${esc(card.sourceDomain)}</span><span class="dot"></span>` : ''}
    ${card.priceRange ? `<span>${esc(card.priceRange)}</span><span class="dot"></span>` : ''}
    <span>${card.slides.length} Pieces</span>
  </div>
</header>

${card.slides.length > 0 ? `<div class="drop-hero"><div class="drop-hero-img"><img src="${esc(card.slides[0].src)}" alt="${esc(card.title)}" /></div></div>` : ''}

<div class="writeup">
  <div class="writeup-body">
    ${descParas}
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>${card.slides.length} items</span></div>
      ${card.priceRange ? `<div class="sidebar-detail"><span class="l">Price range</span><span>${esc(card.priceRange)}</span></div>` : ''}
      <a href="${esc(card.sourceUrl || '/')}" ${card.sourceUrl ? 'target="_blank" rel="noopener"' : ''} class="sidebar-cta">${card.sourceUrl ? 'Shop the Collection ↗' : '← Back to Feed'}</a>
      <div class="hashtags">
        ${tags.map(h=>`<span class="hashtag">${h}</span>`).join('\n        ')}
      </div>
    </div>
  </aside>
</div>

${card.slides.length > 0 ? `<section class="products">
  <div class="products-hdr">The Collection — ${card.slides.length} Pieces</div>
  <div class="products-grid">
${productCards}
  </div>
</section>` : ''}

<section class="more">
  <div class="more-hdr">
    <span class="more-label">More from the Feed</span>
    <a href="/" class="more-link">Back to Feed →</a>
  </div>
  <div class="more-grid">
${moreHtml}
  </div>
</section>

<footer><div class="inner"><span>© 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
</body>
</html>`;
}

/* ── 7. Write pages ──────────────────────────────────────── */
let created = 0;
for (const card of toGen) {
  const dir = path.join(SITE, 'drops');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(path.join(dir, card.slug + '.html'), buildPage(card), 'utf8');
  console.log(`  CREATE  ${card.pagePath}  (${card.slides.length} slides, ${card.perSlide.length} texts)`);
  created++;
}
console.log(`\n✓ Created ${created} pages with per-slide descriptions.`);
