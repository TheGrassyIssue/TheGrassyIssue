/**
 * Adds "See Full Drop →" links to feed cards that now have standalone pages.
 * Reads index.html, finds carousel cards, matches them to generated pages,
 * and injects readmore links where missing.
 */
const fs = require('fs');
const path = require('path');

let html = fs.readFileSync('index.html', 'utf8');

// Collect all drop page slugs
const dropFiles = fs.readdirSync('drops')
  .filter(f => f.endsWith('.html') && f !== 'index.html')
  .map(f => f.replace('.html', ''));

function slugify(s) {
  return s.toLowerCase()
    .replace(/['']/g, '')
    .replace(/&amp;/g, 'and').replace(/&/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
    .substring(0, 60);
}

// Find each card that has a carousel but no readmore link yet
const cardRe = /<div class="card"[^>]*data-type="[^"]*"[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*(?=\s*(?:<!--|<div class="card"|<div class="load-more"|<\/section))/g;

let count = 0;
let match;

// Simpler approach: find each </div>\s*</div> before next card that has data-carousel but not card-readmore
// Actually let me just find each card-title, get title text, match to slug, and inject after card-meta

const lines = html.split('\n');
const output = [];
let i = 0;

while (i < lines.length) {
  const line = lines[i];
  
  // Look for card-title to capture title
  const titleMatch = line.match(/<div class="card-title"[^>]*>(.*?)<\/div>/);
  if (titleMatch) {
    const rawTitle = titleMatch[1].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
    const slug = slugify(rawTitle);
    
    // Check if this slug has a page
    if (dropFiles.includes(slug)) {
      // Look ahead: does this card already have a readmore link?
      let hasReadmore = false;
      let insertIdx = -1;
      for (let j = i + 1; j < Math.min(i + 20, lines.length); j++) {
        if (lines[j].includes('card-readmore')) { hasReadmore = true; break; }
        // Find the closing </div> of card-body (after card-meta or gear-counter)
        if (lines[j].match(/^\s*<\/div>\s*$/) && j > i + 1) {
          // Check if next line is also </div> (closing the card)
          if (j + 1 < lines.length && lines[j + 1].match(/^\s*<\/div>\s*$/)) {
            insertIdx = j;
            break;
          }
        }
      }
      
      if (!hasReadmore && insertIdx > 0) {
        // Insert readmore link before the closing </div> of card-body
        const readmoreHtml = `      <a href="/drops/${slug}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid #141414;padding-bottom:2px;">See Full Drop →</a>`;
        
        // Output lines up to insertIdx, add readmore, then continue
        while (i < insertIdx) {
          output.push(lines[i]);
          i++;
        }
        output.push(readmoreHtml);
        count++;
        // Continue from insertIdx (the closing </div>)
        continue;
      }
    }
  }
  
  output.push(lines[i]);
  i++;
}

fs.writeFileSync('index.html', output.join('\n'), 'utf8');
console.log(`Added ${count} readmore links to index.html`);
