/**
 * Wraps each card-title in a link to its standalone page.
 * <div class="card-title">Title</div>
 * becomes
 * <div class="card-title"><a href="/drops/slug">Title</a></div>
 */
const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// Build slug lookup from drop pages on disk
const dropSlugs = new Set(
  fs.readdirSync('drops')
    .filter(f => f.endsWith('.html') && f !== 'index.html')
    .map(f => f.replace('.html', ''))
);

// Also check for existing standalone pages in guides/events
const allPages = {};
for (const dir of ['drops', 'guides', 'events']) {
  if (!fs.existsSync(dir)) continue;
  fs.readdirSync(dir)
    .filter(f => f.endsWith('.html') && f !== 'index.html')
    .forEach(f => { allPages[f.replace('.html', '')] = dir; });
}

function slugify(s) {
  return s.toLowerCase()
    .replace(/['']/g, '')
    .replace(/&amp;/g, 'and').replace(/&/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
    .substring(0, 60);
}

let count = 0;

// Match card-title divs that don't already contain an <a> tag
html = html.replace(
  /<div class="card-title"([^>]*)>((?:(?!<a ).)*?)<\/div>/g,
  (match, attrs, inner) => {
    const plainTitle = inner.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
    const slug = slugify(plainTitle);
    
    // Check if there's a matching page
    if (allPages[slug]) {
      const dir = allPages[slug];
      count++;
      return `<div class="card-title"${attrs}><a href="/${dir}/${slug}" style="color:inherit;text-decoration:none;border-bottom:none;">${inner}</a></div>`;
    }
    return match; // no page found, leave unchanged
  }
);

fs.writeFileSync('index.html', html, 'utf8');
console.log(`Linked ${count} card titles to their standalone pages.`);
