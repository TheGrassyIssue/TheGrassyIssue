#!/usr/bin/env python3
# Builds /drops/brand-to-know-sugarloaf-social-club.html
import re, json, os

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(SITE, "drops/the-towel-edit-vol-3.html"), encoding="utf-8").read()
IMGDIR = os.path.join(SITE, "images/ssc-brand")
META = json.load(open("/tmp/sscm/meta.json"))

TITLE = "Sugarloaf Social Club — The Group Chat That Became a Golf Brand"
SLUG = "brand-to-know-sugarloaf-social-club"
DESC = ("Sugarloaf Social Club started as a 2011 group chat between college roommates and is now "
        "one of golf's most prolific collaborators. Ian Gilley's McLean, Virginia brand, the dead "
        "Coore & Crenshaw course it's named after, and 32 projects with MacKenzie, THE PLAYERS, "
        "Clubhaus, PAYNTR and the Evans Scholars.")

# slug: (partner, display name, blurb)
COPY = {
"mackenzie-sail":("MacKenzie Golf Bags","Sail Bag “8185”","Built from retired sailcloth, so each one carries the number of the sail it came from. Three were made. This is the piece people bring up when they talk about SSC, and the reason the waitlist exists."),
"mackenzie-white":("MacKenzie Golf Bags","White Leather Double Seve 8”","The most expensive thing SSC has ever put its name on. White leather on a Double Seve body, which is a bold choice for a bag you carry across wet grass."),
"mackenzie-seve":("MacKenzie Golf Bags","Double Seve 8”","The standard-issue version of the above, in canvas. Still $850, still gone."),
"mackenzie-shoe":("MacKenzie Golf Bags","Shoe Bag","Navy canvas with the club crest. One of the few MacKenzie pieces you can still buy, and the cheapest way into that collaboration by a factor of four."),
"players-polo":("THE PLAYERS","“Major” Stripe Sport Polo","Navy, gold and white block stripe made for TPC Sawgrass. An officially licensed PGA Tour product that doesn't look like one, which is harder than it sounds."),
"players-crew":("THE PLAYERS","Caddie Crew","Powder blue crewneck with the championship mark ringed on the chest. Reads collegiate rather than corporate."),
"players-vest":("THE PLAYERS","Tech Vest","Black, quarter-zip, minimal branding. The most wearable thing in the Sawgrass capsule."),
"players-cap":("THE PLAYERS","Runner Cap","Nylon five-panel. $45 and still in stock, which makes it the easy entry point to the tournament work."),
"wga-tee":("Western Golf Association","Evans Scholars T-Shirt","Washed green with a chest-pocket flag. The Evans Scholars program sends caddies to college on full housing-and-tuition scholarships, and this line supports it. The best reason on this page to want something restocked."),
"wga-sling":("Western Golf Association","Caddie Sling","Pistachio green pouch on a webbing strap, shot on a bag drop. Small, cheap, and the one accessory here people ask about."),
"wga-polo":("Western Golf Association","Sport Polo","Still in stock at $95, which is the exception in this section."),
"evans-bag":("Evans Scholars","“Team Bag”","A black carry bag done for the scholarship program. $375, long gone."),
"clubhaus-hedgehog":("Clubhaus","Hedgehog Knit Headcover","Navy knit with a multicolour tassel and a hedgehog at the crown. Clubhaus is a Japanese golf media brand, and the whole capsule reads that way."),
"clubhaus-fan":("Clubhaus","Sensu Fan","A folding paper sensu fan, printed with the Clubhaus mark, $14. The cheapest thing SSC sells and the one that best explains the brand."),
"clubhaus-windshirt":("Clubhaus","Windshirt","Black, cropped, quarter-zip. Sold out in the first run."),
"clubhaus-pouch":("Clubhaus","Valuables Pouch","$135 for a zip pouch, which is a Japanese-collaboration price if ever there was one."),
"payntr-87":("PAYNTR Golf","“SUMMER P.O.P.” Eighty Seven","White with red outsole detailing, released June 2026 around the U.S. Open. PAYNTR builds the shoe, SSC did the colorway."),
"payntr-slides":("PAYNTR Golf","Summer Slides","Cream slides for the walk from the 18th to the car. $50."),
"sentinel-case":("Sentinel Golf","Rangefinder Case","Tan cordura with a blue stripe and a purple tab. Sentinel makes everything in Japan, and it shows in the hardware."),
"sentinel-jacket":("Sentinel Golf","Red Field Jacket","$355, the most substantial garment the two brands have made together."),
"students-polo":("Students Golf","Students of SSC Polo","Pale grey, three-button, no visible branding beyond the collar. Students is on our roster in its own right."),
"students-hat":("Students Golf","Scout Hat","White bucket with a scalloped brim and the Students wordmark. $50, in stock."),
"makino":("Makino","TOUR 3 Putter","A milled putter with the SSC arrow stamped into the flange, shot on a park bench rather than a studio table. $750, and there is an $800 version too."),
"bellroy":("Bellroy","Lite Sling","Bellroy is a leather-goods company from Melbourne that had never made anything for golf. Cream ripstop, $90."),
"totem":("TOTEM","3-Piece Divot Tool","Brass, three pieces, $130. The nicest object here that costs less than a bag."),
"charlie":("Charlie","Junior Golf Bag","A red, white and blue stand bag sized for a kid, $220. There is a toddler version at $135. Nobody else on our roster makes anything like it."),
"gleezy-tee":("Gleezy","Queen City Quail T-Shirt","A cartoon quail in golf shoes, drawn by the artist Gleezy for a Charlotte-specific run."),
"queencity-hc":("Gleezy","Queen City Quail Knit Headcover","Purple and teal knit with a lilac tassel. The loudest thing SSC has made."),
"trellis":("Trellis Coffee Bar","Soccer Kit","A teal-striped soccer jersey for a coffee bar, sold by a golf brand. This is the clearest evidence that SSC is a creative agency first."),
"jain-hoody":("Jain","Grownup Hoody","$50, part of a kids-and-parents capsule that also includes a Jainasaurus t-shirt and a Fore Ewe headcover."),
"tour-towel":("Sugarloaf Social Club","The Tour Towel","Teal stripe, $95, and the towel that made our Vol. 1 towel list. In stock."),
"terry-anorak":("Sugarloaf Social Club","The Terry Anorak","Green terry cloth, quarter-zip, $165. Part of a full terry run that includes a cabana shirt, a short and a mini skirt."),
}

SECTIONS = [
 ("The MacKenzie Bags", ["mackenzie-sail","mackenzie-white","mackenzie-seve","mackenzie-shoe"]),
 ("THE PLAYERS, Officially", ["players-polo","players-crew","players-vest","players-cap"]),
 ("The Caddie Scholarship Work", ["wga-tee","wga-sling","wga-polo","evans-bag"]),
 ("Clubhaus, Japan", ["clubhaus-hedgehog","clubhaus-fan","clubhaus-windshirt","clubhaus-pouch"]),
 ("Brand on Brand", ["payntr-87","payntr-slides","sentinel-case","sentinel-jacket","students-polo","students-hat"]),
 ("Objects", ["makino","bellroy","totem","charlie"]),
 ("The Ones That Make No Sense", ["gleezy-tee","queencity-hc","trellis","jain-hoody"]),
 ("What You Can Buy Today", ["tour-towel","terry-anorak"]),
]

FAQ = [
 ("Who founded Sugarloaf Social Club?",
  "Ian Gilley. He is the founder and CEO, and the brand is based in McLean, Virginia."),
 ("How did Sugarloaf Social Club start?",
  "As a group chat in 2011 between college roommates who had just graduated. It became an annual golf trip, then an Instagram account, then a brand. The LLC was filed in 2017. Gilley has described the whole thing as “a happy little accident.”"),
 ("Where does the name Sugarloaf come from?",
  "Sugarloaf Mountain Golf &amp; Town Club in Minneola, Florida, the college hangout. It was Coore &amp; Crenshaw's first Florida design, built in 2008 with more than 250 feet of elevation change, and it opened into the financial crisis. The course is permanently closed."),
 ("Who owns Sugarloaf Social Club?",
  "Sugarloaf Social Club is a subsidiary of Pro Shop, Inc., the golf media company founded by Chad Mumm and Joe Purzycki that raised roughly $20 million from the PGA Tour and Powerhouse Capital. Pro Shop also owns Skratch and GolfWRX. Skratch discloses the shared ownership in its own coverage of the brand."),
 ("What is the most collectible Sugarloaf collaboration?",
  "The SSC x MacKenzie Sail Bags, built from retired sailcloth and numbered for the sail each one came from. They sold at $975. The white leather Double Seve at $1,400 is the most expensive piece the brand has released."),
 ("What are the Evans Scholars products?",
  "A line made with the Western Golf Association supporting the Evans Scholars program, which sends caddies to college on full tuition and housing scholarships."),
 ("Is Sugarloaf Social Club gear hard to get?",
  "Most of the collaboration work is. Of the thirty-two projects catalogued here, the majority are sold out. The current in-house range — the Terry run, the Tour Towel, headwear — restocks more reliably."),
 ("What is the cheapest Sugarloaf collaboration?",
  "The SSC x Clubhaus Sensu Fan at $14, a folding paper fan printed with the Clubhaus mark."),
]

def imgs(slug):
    n = len([f for f in os.listdir(IMGDIR) if f.startswith(slug + "-") and f[len(slug)+1].isdigit()])
    return [f"/images/ssc-brand/{slug}-{i+1}.jpg" for i in range(n)]

def card(slug):
    m = META[slug]; partner, name, blurb = COPY[slug]
    ims = imgs(slug)
    alt = f"{partner} {name}".replace('"', "")
    frames = "".join(f'<div class="pg-frame"><img src="{u}" alt="{alt} · view {i+1} of {len(ims)}" loading="lazy" /></div>'
                     for i, u in enumerate(ims))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
                   for i in range(len(ims))) if len(ims) > 1 else ""
    nav = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
           '<button class="pg-arw next" aria-label="Next image">&#8250;</button>') if len(ims) > 1 else ""
    count = f'<span class="pg-count">1/{len(ims)}</span>' if len(ims) > 1 else ""
    so = ' <span class="so">&middot; Sold out</span>' if not m["avail"] else ""
    price = "$" + str(int(float(m["price"]))) if float(m["price"]) == int(float(m["price"])) else "$" + m["price"]
    return f"""
    <div class="product-card" data-frames="{len(ims)}">
      <div class="product-gallery">
        <div class="pg-track">{frames}</div>
        {nav}{count}
        <div class="pg-dots">{dots}</div>
      </div>
      <div class="product-body">
        <div class="product-brand">{partner}</div>
        <div class="product-name">{name} &middot; {price}{so}</div>
        <div class="product-desc">{blurb}</div>
        <a href="{m['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""

grid = ""
for hdr, slugs in SECTIONS:
    grid += f'\n  <h2 class="products-hdr sec">{hdr}</h2>\n  <div class="products-grid">'
    grid += "".join(card(s) for s in slugs if s in META)
    grid += "\n  </div>\n"

faq_html = '\n  <h2 class="products-hdr sec">Questions</h2>\n  <div class="faq">' + "".join(
    f'\n    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "\n  </div>\n"

h = BASE
h = h.replace("The Towel Edit, Vol. 3 &mdash; The Grassy Issue", f"{TITLE} &mdash; The Grassy Issue")
h = h.replace("The Towel Edit, Vol. 3 — The Grassy Issue", f"{TITLE} — The Grassy Issue")
h = h.replace("The Towel Edit, Vol. 3", TITLE)
h = h.replace("the-towel-edit-vol-3", SLUG)
for k in ["description", "og:description", "twitter:description"]:
    h = re.sub(r'(<meta (?:name|property)="%s" content=")[^"]*(")' % re.escape(k),
               lambda m: m.group(1) + DESC + m.group(2), h)

def fix_article(m):
    d = json.loads(m.group(1))
    d["headline"] = TITLE; d["description"] = DESC
    d["url"] = f"https://thegrassyissue.com/drops/{SLUG}"
    d["datePublished"] = "2026-08-14"; d["dateModified"] = "2026-08-14"
    d["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"https://thegrassyissue.com/drops/{SLUG}"}
    return '<script type="application/ld+json">\n' + json.dumps(d, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix_article, h, count=1, flags=re.S)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub(r"&\w+;"," ",q),
   "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&\w+;"," ",a)}} for q,a in FAQ]}
_faq_block = '<script type="application/ld+json">\n' + json.dumps(faq_ld, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda m: _faq_block, h, count=1, flags=re.S)

h = h.replace('<span class="drop-tag grass">[The Edit]</span>', '<span class="drop-tag grass">[Brand to Know]</span>')
h = h.replace('<a href="/#feed">The Edit</a>', '<a href="/#feed">Brand to Know</a>')
h = re.sub(r'<div class="drop-hero">.*?</div></div>',
  '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/ssc-brand/hero.jpg" '
  'alt="SSC x MacKenzie Sail Bag, built from retired sailcloth" /></div></div>', h, count=1, flags=re.S)

writeup = """<div class="writeup">
  <div class="writeup-body">
    <p>Sugarloaf Social Club was a group chat. In 2011 a few college roommates were graduating and wanted somewhere to keep talking about golf, so they named the thread after the course they had spent four years on. The chat became an annual trip. The trip became an Instagram account. At one point that account had more followers than Golf Digest. Ian Gilley filed the LLC in 2017 and has described the whole sequence as &ldquo;a happy little accident.&rdquo;</p>
    <p>The course they named it after is dead. Sugarloaf Mountain in Minneola, Florida was Coore &amp; Crenshaw's first design in the state, built in 2008 across more than 250 feet of elevation, and it opened directly into the financial crisis. It never recovered and it is permanently closed. A brand named after a course you can no longer play is a fairly on-the-nose metaphor for how golf nostalgia works, and to their credit SSC has never leaned on it.</p>
    <p>One thing to state plainly, because it explains a lot: Sugarloaf is a subsidiary of Pro Shop, Inc., the media company founded by <em>Full Swing</em> producer Chad Mumm and Joe Purzycki, which raised around $20 million from the PGA Tour and Powerhouse Capital and also owns Skratch and GolfWRX. Skratch discloses this in its own coverage. It is why an independent-looking brand from McLean, Virginia has an officially licensed THE PLAYERS capsule.</p>
    <p>What follows is thirty-two projects. Bags made from retired sailcloth, a $14 paper fan from a Japanese golf magazine, a soccer kit for a coffee bar, and a line supporting the scholarship program that puts caddies through college. Most of it is sold out. That is the point of an archive.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2011 &middot; LLC 2017</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Ian Gilley</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>McLean, VA</span></div>
      <div class="sidebar-detail"><span class="l">Projects</span><span>32 catalogued</span></div>
      <a href="https://sugarloafsocialclub.com" target="_blank" rel="noopener" class="sidebar-cta">sugarloafsocialclub.com &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#SugarloafSocialClub</span>
      </div>
    </div>
  </aside>
</div>"""
h = re.sub(r'<div class="writeup">.*?</aside>\s*</div>', writeup, h, count=1, flags=re.S)

start = h.find('<section class="products">')
end = h.find('<section class="more"')
if end == -1: end = h.find('<div class="more"')
assert start != -1 and end != -1 and end > start
h = h[:start] + '<section class="products">\n' + grid + faq_html + '</section>\n\n' + h[end:]

out = os.path.join(SITE, f"drops/{SLUG}.html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
