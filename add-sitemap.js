const fs = require('fs');

let sitemap = fs.readFileSync('sitemap.xml', 'utf8');
const today = '2026-06-15';

// Get all drop page files
const dropFiles = fs.readdirSync('drops')
  .filter(f => f.endsWith('.html') && f !== 'index.html')
  .map(f => f.replace('.html', ''));

// Find which are already in sitemap
const existing = new Set();
const locRe = /<loc>([^<]+)<\/loc>/g;
let m;
while ((m = locRe.exec(sitemap)) !== null) {
  existing.add(m[1]);
}

let newEntries = '';
let count = 0;
for (const slug of dropFiles.sort()) {
  const url = `https://thegrassyissue.com/drops/${slug}`;
  if (existing.has(url)) continue;
  newEntries += `  <url>
    <loc>${url}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>\n`;
  count++;
}

// Insert before </urlset>
sitemap = sitemap.replace('</urlset>', newEntries + '</urlset>');
fs.writeFileSync('sitemap.xml', sitemap, 'utf8');
console.log(`Added ${count} new URLs to sitemap.xml (total: ${existing.size + count})`);
