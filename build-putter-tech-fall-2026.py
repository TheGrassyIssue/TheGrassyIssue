"""build-putter-tech-fall-2026.py — Putter Tech Roundup, Fall 2026 (12 November 2026).
Lenny: "lets do a Putter tech round up post, LAB just released a new putter among others, okay to include the big names".
Options sheet (10 putters, Aug–Nov 2026, grouped by tech story) -> "let's finish up that putter post" (all ten, grouped).
FACTS: prices read live 12 Nov 2026 on each brand's site (Scotty Cameron via Fairway Jockey, which lists the Spec III at $800).
Specs from brand press releases / product pages. Frames: brand CDN images (Odyssey and Scotty via Fairway Jockey's Shopify CDN).
"""
import html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/hidden-details-golf-gear.html"
SLUG = "putter-tech-roundup-fall-2026"
TITLE = "New Putters, Fall 2026: L.A.B. MEZZ.2i, Odyssey TRTL, Scotty Cameron Spec III and the Tech Behind Them"
DESC = ("Fifteen new putters from August to November 2026, grouped by the tech behind them: zero torque from L.A.B., Odyssey, PXG and Mizuno, "
        "low-torque designs from Scotty Cameron, Toulon and Takomo, Evnroll's reverse torque and new faces from Bettinardi, Evnroll and PING.")
H1 = "Putter Tech, Fall 2026: L.A.B.&rsquo;s MEZZ.2i and 14 More New Putters, Explained"
BC = "Putter Tech, Fall 2026"
IMG = "/images/putter-tech-fall-2026"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
FR = json.loads((ROOT / "research/putter-tech-frames.json").read_text())
FR["takomo"] = [f for f in FR["takomo"] if not f.endswith("takomo-3.jpg")]  # tak-1 source looked rendered; drop
def L(slug, text): return f'<a href="/drops/{slug}">{text}</a>'

# key: (brand, name, price, url, released, desc)
P = {
 "lab": ("L.A.B. Golf", "MEZZ.2i", "$499 stock &middot; from $599 custom", "https://labgolf.com/products/mezz2i-stock-putter", "Nov 10",
   "The first update to the MEZZ in more than four years, and the reason for this post. A fanged mid-mallet milled from 6061 aluminum with a deep fly-milled 303 stainless insert, more weight pushed out for forgiveness, and two ways to pick up the ball. Lie Angle Balance does the rest: the face has no reason to twist, so it does not. In stores from November 19; direct from L.A.B. now."),
 "trtlmax": ("Odyssey", "Square 2 Square TRTL Max", "$399.99", "https://odyssey.callawaygolf.com/putters/putters-2027-square-2-square-trtl-max.html", "Nov 6",
   "Odyssey&rsquo;s new TRTL shape built as a zero-torque putter, with about 20 percent more MOI than the standard TRTL. Four sole weights let a fitter move the center of gravity, and the Twin Track alignment runs long, unbroken lines back from the face."),
 "pxg": ("PXG", "Torpedo ZT", "$449", "https://www.pxg.com/products/torpedo-zt-putters", "Oct 8",
   "PXG&rsquo;s Torpedo mallet rebuilt around an onset hosel that puts the shaft axis just above the center of gravity. A milled 303 stainless front and an aluminum rear body, a pyramid-milled face, two swappable sole weights (357 to 392 grams) and a pocket in the sole for picking the ball up."),
 "miz": ("Mizuno", "M.Craft X, Zero Torque (Z) Neck", "$400", "https://mizunogolf.com/us/golf-clubs/m-craft-x-putters/", "Oct 30",
   "Mizuno&rsquo;s take fires the shaft axis straight through the center of gravity, so the head balances wherever you hold it rather than pointing toe-up. The neck is a reverse plumber&rsquo;s, and because M.Craft X is modular, the neck pairs with the line&rsquo;s other heads and hosels for 20 combinations in all. It ships with 1&deg; of shaft lean and a SuperStroke TLT Pistol grip."),
 "scotty": ("Scotty Cameron", "Phantom 5 &amp; 11R OC Spec III", "$800, limited", "https://fairwayjockey.com/products/scotty-cameron-2026-phantom-5-oc-spec-lll-custom-putter", "Oct 1",
   "Cameron&rsquo;s answer to zero torque is the OC, or Onset Center: the shaft sits behind the leading edge and in line with the center of gravity to cut down twisting. The Spec III editions come in black PVD with three high-contrast sightlines and a full-face Studio Carbon Steel insert with chain-link milling. Limited run."),
 "takomo": ("Takomo", "Lumo M1", "$219 &middot; $239 in black", "https://takomogolf.com/products/lumo-m1-putter", "Oct",
   "The first putters from the direct-to-consumer brand we covered in our "+L("brand-to-know-takomo-golf","Takomo Brand to Know")+". A low-torque mallet with a balanced head, sold direct at a price well below the big brands. A blade version, the Lumo B1, launched alongside it."),
 "evnroll": ("Evnroll", "EZPZ Reverse Torque", "$449", "https://www.evnroll.com/products/ezpz", "Aug 15",
   "The contrarian of the season. Instead of removing torque, Evnroll leans the hosel inward and adds torque the other way, which it says keeps the face square through the stroke."),
 "queenb": ("Bettinardi", "2027&ndash;28 Queen B (QB2, QB6, QB17)", "$499.99", "https://bettinardi.com/products/queen-b-17-center-shaft-putter", "Pre-order Nov 3",
   "The return of Bettinardi&rsquo;s showpiece line, milled from 303 stainless steel in Tinley Park, Illinois, in a French Gold PVD finish. The news is the face: a new Macro Honeycomb mill, a scaled-up version of the classic pattern and the firmest feel Bettinardi makes. Three models (QB2, QB6 and QB17), 362 grams, in stores November 19."),
 "trtl": ("Odyssey", "TRTL (S-Neck, Double Bend, Crank Hosel)", "$349.99", "https://odyssey.callawaygolf.com/putters/putters-2027-trtl-db.html", "Nov 6",
   "The standard TRTL, for golfers who want the new shape with a traditional hang. The story is the new Ai-Star insert, a dual-layer urethane and aluminum face that Odyssey describes as firmer than the old Ai-ONE, plus four adjustable sole weights."),
 "ping": ("PING", "PLD Milled SE DZB", "$500, limited", "https://ping.com/en-us/golf-clubs/putters/all-putters/pld-milled-2026-se-dzb", "Aug",
   "A fully milled carbon steel blade from PING&rsquo;s PLD tour line, in a patina finish with heel and toe weighting for stability. A 350-gram head and a limited production run make it the collector&rsquo;s pick of the fall."),
 "labbc": ("L.A.B. Golf", "VZN.1i in Black Cherry", "$599 custom", "https://labgolf.com/products/vzn1i-custom-putter?color=Black%20Cherry", "Fall, limited",
   "L.A.B.&rsquo;s seasonal color for fall, a deep purple Cerakote offered on seven of its putters while supplies last. The VZN.1i is the pick: an easy-aiming head shape with a stainless steel insert, built on the same Lie Angle Balance as everything L.A.B. makes. Same zero-torque tech as the MEZZ.2i, in the best-looking finish of the season."),
 "toulon": ("Toulon Golf", "Houston Double Bend", "$600", "https://toulongolf.com/products/26-houston-db", "Aug 24",
   "Toulon developed the Houston head as a zero-torque design, then gave it a traditional face-balanced double bend for golfers who want the stability without the toe-up hang. It is an ultra-high MOI, multi-material mallet and the most forgiving putter in Toulon&rsquo;s 2026 collection, with a square, angular shape and sharp rails meant to keep the head square to the line. A plumber&rsquo;s neck version, the Houston H1, came out the same day."),
 "takb1": ("Takomo", "Lumo B1", "$219 &middot; $239 in black", "https://takomogolf.com/products/lumo-b1-putter", "Oct",
   "The blade half of Takomo&rsquo;s first putter launch, and, with the M1, the lowest-priced putter in this roundup. A classic blade shape built for stability, with a SuperStroke grip and a headcover made from recycled fabric included. For golfers who want a modern blade without paying Scotty Cameron prices."),
 "origin": ("Evnroll", "ORIGIN ER2cs", "$399", "https://www.evnroll.com/products/origin-er2cs-satin", "Aug 20",
   "A center-shafted mid-blade based on the ER2, Evnroll&rsquo;s most awarded shape, milled from a single block of 303 stainless steel in a satin finish. The face is SweetFace 2.0, Evnroll&rsquo;s groove pattern, which it says keeps ball speed and roll consistent across the face so mishits come up closer to the hole. A rocker sole and tungsten heel and toe weights round it out. There is a square-back mallet version, the ER8cs, at the same price."),
 "bb1ff": ("Bettinardi", "BB1 Fitz Flow, Evergreen TourTone", "$650, limited", "https://bettinardi.com/products/evergreen-tourtone-bb1-fitz-flow-bb1-ff-limited-run-blade-putter", "Nov 12",
   "The newest putter here, released the day we checked prices. A limited run of Matt Fitzpatrick&rsquo;s blade, milled from 303 stainless to 350 grams with a thinner flange. The face is the Fitz Face, a semi-circular milling pattern developed with Fitzpatrick for his preferred feel and roll, and the two-tone Evergreen and Diamond Blast finish frames the topline for alignment."),
}

SECTIONS = [
 ("zero-torque", "Zero Torque Goes Mainstream", "The big brands all have one now",
  ["Two years ago, zero torque mostly meant L.A.B. This fall, almost every major brand has its own version, and they disagree on how to get there. L.A.B. balances the head on the lie angle. Odyssey&rsquo;s Square 2 Square shapes hang toe-up. PXG uses an onset hosel set just above the center of gravity. Mizuno runs the shaft straight through the center of gravity so the head balances wherever you hold it.",
   f"The goal is the same in every case: a face that does not want to open or close as you swing it, so the putter returns square without you doing anything. We ranked the field earlier this year in our {L('5-zero-torque-putters-worth-your-attention','zero-torque putter edit')}; these are the new arrivals."],
  ["lab", "trtlmax", "pxg", "miz", "labbc"]),
 ("low-torque", "Low Torque, Traditional Looks, and One Contrarian", "For golfers who want less twist without the look",
  ["Not everyone wants a putter that sits toe-up. The middle ground this fall is low torque in familiar shapes. Scotty Cameron&rsquo;s OC putters set the shaft back from the leading edge and in line with the center of gravity. Toulon took a head it designed for zero torque and put a traditional double bend on it, and Takomo&rsquo;s first mallet and blade chase the same idea at a fraction of the price.",
   "Then there is Evnroll, which went the other way. The EZPZ adds torque on purpose, leaning the hosel inward so the putter wants to close a little as you swing it. Whether that suits you is a fitting question, which is the point the whole category keeps coming back to."],
  ["scotty", "toulon", "takomo", "takb1", "evnroll"]),
 ("face-tech", "Face Tech and Milling", "What happens at impact",
  ["The other half of the story is the face. Bettinardi scaled up its signature honeycomb into a Macro Honeycomb mill, the firmest feel in its range, and gave Matt Fitzpatrick&rsquo;s blade its own semi-circular Fitz Face. Odyssey&rsquo;s new Ai-Star insert layers urethane over aluminum. Evnroll&rsquo;s SweetFace grooves aim to keep ball speed even across the face, and PING went back to a fully milled carbon steel head with no insert at all.",
   "Face technology changes the sound and feel more than the line, so if you can, hit these before you buy. Feel is personal in a way that torque is not."],
  ["queenb", "bb1ff", "trtl", "origin", "ping"]),
]

CSS = ('<style>/*TGI-PUTTER*/.tr-sec{max-width:1180px;margin:0 auto;padding:56px 0 8px;border-top:1px solid rgba(20,20,20,.12)}'
 '.tr-head{max-width:760px;margin:0 auto 24px}.tr-head p{font-size:17px;line-height:1.65;margin:0 0 14px}'
 '.tr-head .writeup-body a{border-bottom:1px solid var(--grass,#2D4A2B)}'
 '.products-grid.tr-grid[data-n]{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px;max-width:1040px;margin:0 auto}'
 '.products-grid.tr-grid[data-n]>.product-card{flex:none;min-width:0}'
 '.tr-grid .product-name{font-size:19px;line-height:1.3}.tr-grid .product-body{padding:18px 20px 22px}.tr-grid .product-desc{font-size:15px;line-height:1.6}'
 '.pt-rel{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin:4px 0 8px}'
 '.drop-hero-img img{object-position:50% 50%}'
 '@media(max-width:820px){.tr-head{padding-left:20px;padding-right:20px}}'
 '@media(max-width:640px){.products-grid.tr-grid[data-n]{grid-template-columns:1fr;gap:22px;padding:0 16px}.drop-hero-img{aspect-ratio:4/3!important}}'
 '.pt-pick{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;max-width:1040px;margin:8px auto 0}'
 '.pt-box{border:.5px solid var(--ink,#141414);padding:22px 22px 18px;background:rgba(45,74,43,.04)}'
 '.pt-box h3{font-size:21px;margin:10px 0 8px;line-height:1.2}.pt-box .pt-if{font-size:15px;line-height:1.55;margin:0 0 14px}'
 '.pt-box ul{list-style:none;margin:0;padding:12px 0 0;border-top:1px solid rgba(20,20,20,.12)}'
 '.pt-box li{display:flex;justify-content:space-between;gap:10px;font-size:14px;padding:5px 0}.pt-box li a{border-bottom:1px solid rgba(20,20,20,.25)}.pt-box li span{white-space:nowrap;opacity:.7}'
 '@media(max-width:900px){.pt-pick{grid-template-columns:1fr;padding:0 20px}}</style>\n')

def card(k, idx):
    brand, name, price, url, rel, desc = P[k]; fr = FR[k]
    label = H.unescape(f"{brand} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div><div class="product-name">{name} &middot; {price}</div>'
            f'<div class="pt-rel">Released {rel}</div><div class="product-desc">{desc}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')

KIND = {"lab": "Zero torque (Lie Angle Balance)", "trtlmax": "Zero torque (toe-up)", "pxg": "Zero torque (onset hosel)", "miz": "Zero torque (shaft through CG)",
        "scotty": "Low torque (onset center)", "takomo": "Low torque", "evnroll": "Reverse torque", "queenb": "Face milling", "trtl": "Face insert", "ping": "Fully milled"}

def body_html(n):
    keys_idx, c = {}, 1
    for sec in SECTIONS:
        keys_idx[sec[0]] = [(c + j, k) for j, k in enumerate(sec[4])]; c += len(sec[4])
    IFS = {"zero-torque": "Your putts start off line, or the face opens and closes more than you want. These putters resist twisting, so the face comes back square on its own.",
           "low-torque": "You want less twist but still like a putter that looks like a putter. Or you want to try the one brand going the other way.",
           "face-tech": "You already like your shape and want it to sound and feel different at impact. Milling and inserts change feel more than line."}
    picks = ""
    for n_, (a, title, kicker, paras, keys) in enumerate(SECTIONS, 1):
        li = "".join(f'<li><a href="#p-{idx}">{P[k][0]} {P[k][1].split(" (")[0]}</a><span>{P[k][2].split(" &middot;")[0].split(",")[0]}</span></li>' for idx, k in keys_idx[a])
        picks += f'<div class="pt-box"><div class="drop-tag grass">{n_:02d} &middot; <a href="#{a}" style="color:inherit">{len(keys)} putters</a></div><h3>{title}</h3><p class="pt-if"><strong>For you if:</strong> {IFS[a]}</p><ul>{li}</ul></div>'

    o = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>L.A.B. Golf released the MEZZ.2i on November 10, the first update to the putter that put the company on tour, and it lands at the end of the busiest fall for new putters we can remember. Fifteen putters from August to now, from a $219 direct-to-consumer mallet to an $800 limited Scotty Cameron.</p>
    <p>Most of them are answering the same question: how do you stop the face from twisting during the stroke? L.A.B. made that question famous, and now everyone has an answer, each slightly different. So instead of a ranked list, this roundup groups the new putters by the idea behind them, explains each idea in plain terms, and lets you decide which one fits your stroke.</p>
    <p><strong>The short version.</strong> If your putts start off line, look at the zero-torque group. If you like a traditional look, start with the low-torque putters. If you already like your shape and want it to feel different, the face tech is where to look.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">New putters</span><span>{n}</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>Aug&ndash;Nov 2026</span></div>
      <div class="sidebar-detail"><span class="l">Price range</span><span>$219&ndash;$800</span></div>
      <div class="sidebar-detail"><span class="l">Headline release</span><span>L.A.B. MEZZ.2i</span></div>
      <div class="hashtags"><span class="hashtag">#Putters</span><span class="hashtag">#ZeroTorque</span><span class="hashtag">#GolfGear</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products tr-sec" style="border-top:0;padding-top:24px">
  <div class="tr-head"><div class="drop-tag grass">Start Here</div><h2 class="products-hdr" id="start-here">Which Group Fits Your Stroke?</h2></div>
  <div class="pt-pick">{picks}</div>
</section>
"""
    i = 1
    for num, (a, title, kicker, paras, keys) in enumerate(SECTIONS, 1):
        cards = "".join(card(k, i + j) for j, k in enumerate(keys)); i += len(keys)
        ps = "".join(f"<p>{p}</p>" for p in paras)
        o += (f'\n<section class="products tr-sec">\n  <div class="tr-head"><div class="drop-tag grass">{num:02d} &middot; {len(keys)} putters</div>\n'
              f'  <h2 class="products-hdr" id="{a}">{title}</h2>\n  <p class="cat-kicker"><strong>{kicker}</strong></p>\n  <div class="writeup-body">{ps}</div></div>\n'
              f'  <div class="products-grid tr-grid" data-n="{len(keys)}">{cards}</div>\n</section>\n')
    o += f"""
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Get Fit Before You Pick a Side</h2>
    <p>Zero torque, low torque and reverse torque all fix the same problem in different ways, and the right one depends on how much your putter face rotates in your stroke. A putting fitting will tell you in about twenty minutes. If you are switching for the off-season, our {L('late-season-putter-switch','late-season putter switch')} post covers twenty more options, from $170 to $799.</p>
    <p>Prices are as each brand showed them to a US visitor on November 12, 2026. The Scotty Cameron Spec III is sold through golf shops; the price and link are from Fairway Jockey. Several of these are limited runs, so stock may change quickly.</p>
  </div>
</section>
"""
    return o

def head_top(n):
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    keys = [k for s in SECTIONS for k in s[4]]
    items = [{"@type": "ListItem", "position": i + 1, "url": P[k][3], "name": H.unescape(f"{P[k][0]} {P[k][1]}")} for i, k in enumerate(keys)]
    blocks = [{"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
               "datePublished": "2026-11-12", "dateModified": "2026-11-12",
               "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
               "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
              {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
                  {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
                  {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]}]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            f'<title>{t} | The Grassy Issue</title>\n<meta name="description" content="{d}" />\n<link rel="icon" href="/favicon.ico" />\n<link rel="apple-touch-icon" href="/apple-touch-icon.png" />\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com" />\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
            f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />\n'
            f'<meta property="og:type" content="article" />\n<meta property="og:url" content="{URL}" />\n<meta property="og:title" content="{t}" />\n<meta property="og:description" content="{d}" />\n'
            f'<meta property="og:image" content="{og}" />\n<meta property="og:site_name" content="The Grassy Issue" />\n<meta name="twitter:card" content="summary_large_image" />\n'
            f'<meta name="twitter:title" content="{t}" />\n<meta name="twitter:description" content="{d}" />\n<link rel="canonical" href="{URL}" />\n<link rel="preload" as="image" href="{IMG}/hero.jpg" />\n{ld}')

def main(apply_):
    keys = [k for s in SECTIONS for k in s[4]]
    assert len(keys) == len(set(keys)) and all(k in P and FR.get(k) for k in keys)
    n = len(keys)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = (f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  {BC}</div>\n\n'
            f'<header class="drop-header">\n  <h1>{H1}</h1>\n  <div class="drop-meta">\n    <span>The Kit &middot; Putter Tech Roundup</span><span class="dot"></span>\n'
            f'    <span>{n} new putters &middot; prices checked November 12, 2026</span>\n  </div>\n</header>\n\n'
            f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Looking down at address over a red L.A.B. Golf MEZZ.2i putter and ball, with long evening shadows across the green" fetchpriority="high" /></div></div>\n')
    body += body_html(n)
    out = head_top(n) + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    print(f"  {n} putters, {len(SECTIONS)} sections")
    if not apply_: return
    (ROOT / f"drops/{SLUG}.html").write_text(out, encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", out[:out.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if "18 Pieces With Tee Pockets" in above: bad.append("donor leak")
    txt = re.sub(r"<[^>]+>", " ", above)
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned " + w)
    for f in set(re.findall(r'src="(/images/[^"]+)"', out)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for s in set(re.findall(r'href="/drops/([^"#]+)"', above)):
        if not (ROOT / f"drops/{s}.html").is_file(): bad.append("deadlink " + s)
    if bad: sys.exit("! " + "; ".join(bad))
    print("  wrote", f"drops/{SLUG}.html")
if __name__ == "__main__": main("--apply" in sys.argv)
