"""build-gift-guide-2b.py — 2026 Holiday Gift Guide, Part 2 of 3, brand-by-brand format (9 November 2026).
Categories 4-6: Compliments Guaranteed, A Fresh New Colorway, The One They'd Never Buy Themselves. Brand map approved by Lenny.
FACTS: product pages read November 9, 2026; prices as shown to a US visitor (Chrome). Brand facts from TGI brand index + product pages.
"""
import html as H, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gift_guide_series as GS
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "The 2026 Golf Gift Guide, Part 2: Statement Pieces, Fresh Colorways and Splurges, Brand by Brand"
DESC = ("30 independent golf brands and the gifts each one does best: pieces that get noticed on the first tee, colorways nobody else "
        "in the group is wearing, and the splurge they would never buy themselves.")
H1 = "The 2026 Golf Gift Guide, Part 2: Statement Pieces, Fresh Colorways and Splurges"
BC = "Gift Guide 2026, Part 2"
SLUG = "golf-gift-guide-2026-statement-pieces-colorways-splurges"
IMG = "/images/gift-guide-2b"
D = json.loads((ROOT / "research/gift-guide-2026/p2b-data.json").read_text())
FRN = json.loads((ROOT / "research/gift-guide-2026/frames2b.json").read_text())
BH = json.loads((ROOT / "research/gift-guide-2026/brandhero2.json").read_text())
AUD = {"mountteegolf.com.au"}
NAME_FIX = {"swing-vest-patchwork": "AKASHI-KAMA x Public Drip Swing Vest, Patchwork", "camo-1-4-zip-rebrand": "Camo Quarter-Zip",
            "green-1-4-zip-rebrand": "Varsity Quarter-Zip", "forest-green-unstructured-corduroy-cap": "Forest Green Corduroy Cap",
            "copper-orange-unstructured-ripstop-nylon-cap": "Copper Orange Ripstop Cap", "monochrome-enamel-logo-silver-ball-marker": "Enamel Logo Ball Marker",
            "cordura-track-jacket-copy": "Cordura Track Jacket", "harmony-silver": "Harmony Golf Shoe, Silver", "highly-addictive-crew": "Highly Addictive Crew, Black",
            "the-awakening-timascus-golf-ball-marker": "The Awakening Ball Marker, Timascus", "seigaiha-wood-set-abyss-edition": "Seigaiha Wood Set, Abyss Edition",
            "the-signet-stainless-steel-pitch-tool": "The Signet Pitch Tool", "hiroki-luxury-leather-sunday-golf-bag-brown": "Luxury Leather Sunday Bag, Brown",
            "hiroki-fte-sunday-golf-bag-green": "FTE Sunday Bag, Forest Green", "hiroki-leather-putter-cover": "Leather Putter Cover",
            "hiroki-wool-headcover-tartan-1": "Wool Headcover, Tartan", "white-embroidered-navy-merino-long-sleeve-golf-shirt": "Navy Merino Long Sleeve Golf Shirt",
            "glen-padded-vest-in-chocolate-brown": "Glen Padded Vest, Chocolate", "haar-reversible-vest-in-navy-blue": "Haar Reversible Vest, Navy",
            "alba-barrel-driver-wood-cover-in-black": "Barrel Driver Cover", "mackenzie-golf-bag-x-fyfe-23rd-edtion": "MacKenzie x Fyfe 23rd Edition Bag",
            "pare-x-minted-greens-mahjong-set": "Paré x Minted Greens Mahjong Set", "pare-x-bluetross-blade-putter-headcover": "Paré x Bluetross Blade Putter Cover",
            "sherwood-x-dormie-hockey-sock-fairway-headcover-red": "Sherwood x Dormie Hockey Sock Fairway Cover", "wynn-golf-club-headcover-cxkd8": "Cochineal Bug Dyed Headcover",
            "camelback-polo-brown-white-stripe": "Camelback Polo, Brown Stripe", "braker-pullover-mineral-snake": "Breaker Pullover, Mineral Snake",
            "links-plaid-golf-trousers": "Links Plaid Wide-Leg Trousers", "the-caddie-golf-polo": "The Caddie Retro Polo",
            "rib-zip-up-cardigan-1": "Rib Zip-Up Cardigan", "radmerino-long-sleeve-polo": "Whitman Long Sleeve Knit Polo",
            "iconic-golf-greens-belt-dark-navy": "Iconic Golf Greens Belt", "gopher-golf-life-flask-dark-navy": "Gopher Golf Life Flask",
            "gopher-golf-life-wallet-dark-navy": "Gopher Golf Life Wallet", "3-pack-drip-marker": "Script Drip 3-Pack Marker Set", "nacre-golf-ball-marker": "Nacre Ball Marker", "pare-plisse-pants-2-0": "Paré Plissé Pants 2.0"}
def nm(k):
    v = D[k]; h = k.split("|")[1]
    t = NAME_FIX.get(h) or v["title"]
    t = re.sub(r"\s*[-–|]\s*(Pre-Order|Preorder)\b.*", "", t)
    t = t.replace("™", "").replace(" - ", ", ").replace(" | ", ", ").replace(" – ", ", ")
    t = re.sub(r"\s*\(([^)]+)\)$", r", \1", t)
    if t.isupper(): t = t.title()
    return t
def pr(k):
    v = D[k]; p = v["price"]
    s = f"{p:,.2f}".replace(".00", "")
    return f"A${s} (~${round(p*0.65)})" if v["d"] in AUD else (f"from ${s}" if v["d"] in FROM and "iron" in k else f"${s}")
def K(d, h):
    k = f"{d}|{h}"; assert k in D and "err" not in D[k], k; return k
FROM = {"takomogolf.com"}
CATS = [
 ("compliments", "Compliments Guaranteed", "The piece somebody asks about before the first tee shot",
  "Some gifts get used. These get noticed. Every brand in this category makes at least one thing that starts a conversation on the first tee, whether it&rsquo;s a camo quarter-zip, a headcover cut from an old camp tent or a hat with a cowboy and a martini on it. Pick the brand that matches how loud the person you&rsquo;re buying for likes to be.",
  [("Public Drip", "Brooklyn, New York", "Neil Tan rediscovered golf at Van Cortlandt Park in 2020 and built the label muni New York now wears. The patchwork swing vest, rebuilt with the Japanese menswear brand AKASHI-KAMA, is the loudest thing in the shop. The green leather Script driver cover and the three gold markers in a suede pouch get the same reaction for less.",
    [K("publicdrip.com","swing-vest-patchwork"),K("publicdrip.com","the-herringbone-half-zip"),K("publicdrip.com","script-driver-cover-green"),K("publicdrip.com","3-pack-drip-marker")]),
   ("Parmore", "Bournemouth, England", "Parmore&rsquo;s banner is No Membership Required, and the camo quarter-zip proves it: realistic hunting camo with a big arched PARMORE across the chest. The varsity quarter-zip is wind and water resistant with cream stripe trim, and the brown stripe polo is the quieter way in.",
    [K("parmoregolf.com","camo-1-4-zip-rebrand"),K("parmoregolf.com","green-1-4-zip-rebrand"),K("parmoregolf.com","brown-stripes-polo-rebrand")]),
   ("Slice Town", "Copenhagen, Denmark", "Started in late 2024 by a Dane and a Swede. The cobalt nylon track jacket has a golf ball printed on the back, the pitch repair tool folds like a butterfly knife (it&rsquo;s on pre-order), and the yellow knitted balaclava is sold for golfers whose game calls for full anonymity.",
    [K("slice-town.com","track-jacket-cobalt"),K("slice-town.com","knitted-golf-balaclava"),K("slice-town.com","butterfly-divot-tool"),K("slice-town.com","short-sleeve-windbreaker-charcoal")]),
   ("Gumtree Golf &amp; Nature Club", "Brooklyn, New York", "Gumtree cuts headcovers in Brooklyn from old quilts, camp tents and fly-fishing waders, so nobody else in the group will have the same one. The Camp Tent and Cochineal covers are the conversation pieces, the quilt pouch holds the valuables, and the ripstop work jacket from the Wynn collaboration is the one to wear.",
    [K("gumtreegolfandnature.com","camp-tent-headcover"),K("gumtreegolfandnature.com","wynn-golf-club-headcover-cxkd8"),K("gumtreegolfandnature.com","vintage-floral-quilt-valuables-pouch"),K("gumtreegolfandnature.com","wynn-golf-club-work-jacket")]),
   ("Mogshade", "Portugal", "Mogshade handmakes its covers in Portugal. The Deco cover uses rescued wool woven in the Serra da Estrela mountains, and the High Sun is merino woven on manual wooden looms. The Risca course case has a pocket for markers, loops for tees and room for a rangefinder. Covers are made to order, so allow about three weeks.",
    [K("mogshadegolf.com","deco-petrol-headcover"),K("mogshadegolf.com","high-sun-headcover"),K("mogshadegolf.com","risca-dark-course-case-1")]),
   ("Dormie Workshop", "Halifax, Canada", "Handmade leather headcovers from Nova Scotia since 2014. The Sherwood collaboration rebuilds real red hockey socks as a fairway cover, with a matching range bag in soft black leather. The Shaka barrel throws a shaka in blue appliqu&eacute;, and the navy paisley cover goes with everything.",
    [K("dormieworkshop.com","sherwood-x-dormie-hockey-sock-fairway-headcover-red"),K("dormieworkshop.com","shaka-barrel-driver-headcover-bone"),K("dormieworkshop.com","paisley-headcovers-navy"),K("dormieworkshop.com","sherwood-x-dormie-range-ball-bag")]),
   ("Draw Golf", "", "Every Draw cap has a small pouch sewn into the side that holds a tee. That&rsquo;s the detail people notice second. The first is the color: forest green corduroy with a pastel blue logo, or copper orange ripstop. The enamel ball marker is the stocking-sized version.",
    [K("drawgolf.co","forest-green-unstructured-corduroy-cap"),K("drawgolf.co","copper-orange-unstructured-ripstop-nylon-cap"),K("drawgolf.co","monochrome-enamel-logo-silver-ball-marker")]),
   ("Read The Green", "New York, New York", "New York golf with &rsquo;90s energy. The Back &rsquo;90s Windbreaker comes in seven two-tone colorways; Jazz and Mallard are the two we&rsquo;d pick. The Swisher Zip has &ldquo;Gotta Be You&rdquo; printed along the back neckline, and the Grounds Crew Jacket is cotton twill with a corduroy collar and cuffs.",
    [K("readthegreen.com","back-90s-windbreaker-jazz"),K("readthegreen.com","back-90s-windbreaker-mallard"),K("readthegreen.com","the-swisher-zip"),K("readthegreen.com","the-grounds-crew-jacket-green")]),
   ("Communal MFG", "Austin, Texas", "An Austin headwear company where every hat is $60 and comes with a lifetime warranty. The Cowboy Martini is the one that gets talked about. The Siren, the Captain and the C Patch lean nautical.",
    [K("communalmfg.com","cowboy-martini-hat"),K("communalmfg.com","the-siren-hat"),K("communalmfg.com","the-captain-hat"),K("communalmfg.com","c-patch-hat")]),
   ("Three Putt", "West Yorkshire, England", "Heavyweight cotton golf streetwear with hand-drawn prints and a dairy cow that turns up everywhere. The Links trousers are wide plaid with an elastic waist. The 445gsm Clubhouse jacket, the Halfway Hut gilet and the retro Caddie polo all carry the cow caddie on the chest.",
    [K("threeputtgolfclothing.co.uk","links-plaid-golf-trousers"),K("threeputtgolfclothing.co.uk","clubhouse-golf-jacket"),K("threeputtgolfclothing.co.uk","halfway-hut-golf-gilet"),K("threeputtgolfclothing.co.uk","the-caddie-golf-polo")])]),
 ("colorway", "A Fresh New Colorway", "The color nobody else in the group is wearing",
  "Most golfers own a navy quarter-zip, a white polo and a gray sweater. This category is for the color they don&rsquo;t have yet: rifle green, wattle yellow, maroon scallop, jade, mineral snake. Each of these ten brands builds its range around a palette, so the gift says something before anyone reads the label.",
  [("Criquet", "Austin, Texas", "Austin&rsquo;s original players shirt brand, est. 2010, and its fall colors are the best they&rsquo;ve been. A treetop green baby alpaca hoodie, a rifle green quilted jacket with a corduroy-lined collar, khaki corduroy quilted over a plaid lining, and the Chill-Knit jacket in bark.",
    [K("criquetshirts.com","alpaca-sweater-hoodie-treetop"),K("criquetshirts.com","barton-quilted-jacket-rifle-green"),K("criquetshirts.com","corduroy-box-quilted-jacket-khaki"),K("criquetshirts.com","chill-knit-quilted-shacket-bark")]),
   ("Radmor", "Seattle, Washington", "Two former University of Washington teammates and no virgin polyester. The Inness knit polo is a blue stripe nod to the &rsquo;90s 3D knit, the Langley is a jacquard in organic cotton and silk, and the RADMerino crew is 90% merino and 10% cashmere.",
    [K("radmorgolf.com","inness-knit-polo"),K("radmorgolf.com","langley-jacquard-knit-polo"),K("radmorgolf.com","radmerino-long-sleeve-polo"),K("radmorgolf.com","radmerino-cashmere-blend-sweater-crew")]),
   ("Golden Hour", "United Kingdom", "Started in 2024 by two friends and named for the last light of the day. A black-and-white Social stripe polo, a cream full-zip knit, a navy track jacket and a rugby sweatshirt: a small range with a clear palette.",
    [K("goldenhourclubhouse.co.uk","the-social-stripe-polo"),K("goldenhourclubhouse.co.uk","the-members-knit"),K("goldenhourclubhouse.co.uk","lightweight-track-jacket"),K("goldenhourclubhouse.co.uk","rugby-sweatshirt")]),
   ("Mount Tee Golf", "Melbourne, Australia", "Three friends in Melbourne making knit polos and plush headcovers. The Parklands waffle polo in the yellow Wattle stripe, the long sleeve Woodlands knit in sand, a ripstop nylon quarter-zip and a mustard checkered putter cover. Mount Tee prices in Australian dollars.",
    [K("mountteegolf.com.au","parklands-waffle-polo-wattle-stripe"),K("mountteegolf.com.au","woodlands-knit-polo-long-sleeve-sand"),K("mountteegolf.com.au","nylon-quarter-zip"),K("mountteegolf.com.au","putter-headcovers-mustard-checkered")]),
   ("Devereux", "Scottsdale, Arizona", "Scottsdale brothers, est. 2013, named after their grandfather. The Camelback polo pairs brown stripes with a contrast collar, the Breaker pullover comes in a mineral snake print, and the open-knit quarter-zip is 100% cotton. The last three here are final sale.",
    [K("devereuxgolf.com","camelback-polo-brown-white-stripe"),K("devereuxgolf.com","braker-pullover-mineral-snake"),K("devereuxgolf.com","loose-knit-quarter-zip-polo-mineral"),K("devereuxgolf.com","highly-addictive-crew")]),
   ("Kingfisher Golf", "Dallas, Texas", "Started at a kitchen counter in East Dallas by a former PepsiCo art director. Four performance polos at $65 each: Vega in a light blue scallop, Antares in a maroon scallop, an olive pattern and a black-and-gray stripe.",
    [K("kingfisher-golf.com","new-blue-polo"),K("kingfisher-golf.com","scallop-polo-in-maroon"),K("kingfisher-golf.com","olive-patterned-polo"),K("kingfisher-golf.com","black-striped-polo")]),
   ("Students", "United States", "Students builds on varsity graphics and a long run of collaborations. The Denali stadium jacket is 100% wool with thick ribbing, the Scholls cardigan is a navy mohair-blend, the Knight polo sweater is a brown waffle knit, and the Aiken beanie is a loose-gauge checker.",
    [K("studentsgolf.com","denali-stadium-jacket"),K("studentsgolf.com","scholls-cardigan-sweater-2"),K("studentsgolf.com","knight-knitted-l-s-polo-sweater-1"),K("studentsgolf.com","aiken-checker-beanie")]),
   ("Howie Benson", "New York, Boston and San Diego", "Resort shirts rebuilt as golf polos. The Resort polo is a stretchy textured knit in brunette, the Ottoman in forest green is the lighter one, and the brown single-button pullover is a golf layer that doesn&rsquo;t look like one. The textured crew in natural layers over all three.",
    [K("howiebenson.com","resort-camp-collar-polo-brunette"),K("howiebenson.com","ottoman-camp-collar-polo-forest-green"),K("howiebenson.com","single-button-pullover-brown"),K("howiebenson.com","relaxed-fit-crew-natural")]),
   ("Aberdeen West", "Aberdeen, Scotland, meets Los Angeles", "A small label built around golf shoes. The Harmony comes in silver, the Cordura track jacket is olive with contrast piping, the gingham pant uses Japanese fabric, and the stand bag pairs brown and tan with a matching hood.",
    [K("aberdeenwest.com","harmony-silver"),K("aberdeenwest.com","cordura-track-jacket-copy"),K("aberdeenwest.com","classic-gingham-pant"),K("aberdeenwest.com","aw-golf-stand-bag")]),
   ("Macade", "Stockholm, Sweden", "Scandinavian golf clothes built for cold, wet rounds. A pine green merino knit hoodie, a jade Therma quarter-zip, a palm green polo sweatshirt with a contrast collar, and a tan wool bomber with striped trim.",
    [K("macadegolf.com","flow-light-knit-hoodie-pine"),K("macadegolf.com","jade-green-therma-quarter-zip"),K("macadegolf.com","blades-palm-polo-sweatshirt"),K("macadegolf.com","downs-wool-bomber-tan")])]),
 ("splurge", "The One They&rsquo;d Never Buy Themselves", "The splurge that outlasts the guilt",
  "Everyone has a short list of things they look at every season and never buy: a leather Sunday bag, forged blades, a cashmere sweater, a marker that costs more than a dozen balls. That&rsquo;s the gift. These ten brands make the version they&rsquo;d choose if somebody else were paying.",
  [("Takomo", "Turku, Finland", "Finnish direct-to-consumer irons, est. 2021: tour-quality forgings at about half the usual shop price. The 301 MB is the muscle back for pure ball strikers, the 201T MKII is the players cavity, and Stand Bag 02 carries the set. Iron prices are where each build starts on Takomo&rsquo;s site.",
    [K("takomogolf.com","iron-301-mb"),K("takomogolf.com","iron-201t-mkii"),K("takomogolf.com","stand-bag-02")]),
   ("Fyfe x MacKenzie", "Scotland", "Fyfe makes tartan and Harris Tweed covers to order in Fife. The 23rd Edition MacKenzie bag is midnight black waxed canvas with tan leather and a tartan-lined pocket. The shawl cardigan is knitted in Scotland from Geelong lambswool, and the Keeper scorecard holder is made in Glasgow by second-generation bookbinders. The Glove Caddy is on pre-order.",
    [K("fyfegolf.com","mackenzie-golf-bag-x-fyfe-23rd-edtion"),K("fyfegolf.com","shawl-neck-cardigan-flannel-grey"),K("fyfegolf.com","the-keeper-leather-scorecard"),K("fyfegolf.com","the-glove-caddy-dark-green")]),
   ("Hiroki", "Auckland, New Zealand", "Sunday bags, stand bags and covers from Auckland. The Luxury Leather Sunday bag is genuine leather from body to base, with a suede divider. The FTE Sunday bag is built from waterproof expanded PTFE. The leather putter cover closes with a magnet.",
    [K("hirokigolf.com","hiroki-luxury-leather-sunday-golf-bag-brown"),K("hirokigolf.com","hiroki-fte-sunday-golf-bag-green"),K("hirokigolf.com","hiroki-leather-putter-cover"),K("hirokigolf.com","hiroki-wool-headcover-tartan-1")]),
   ("Alba", "Milan, Italy", "A Milan label launched in October 2026, shaped by Scottish weather. The Crest jacket is a three-layer waterproof shell, the Haar vest is technical wool on one side and microfiber on the other, and the Glen padded vest comes in chocolate.",
    [K("albagolf.it","crest-jacket"),K("albagolf.it","haar-reversible-vest-in-navy-blue"),K("albagolf.it","glen-padded-vest-in-chocolate-brown"),K("albagolf.it","alba-barrel-driver-wood-cover-in-black")]),
   ("Whim", "New York, New York", "Whim treats objects as seriously as clothes. The long sleeve golf shirt is 100% American merino with natural horn buttons. The Spell-Out beanie is knit in Queens, the cap is Japanese oxford cotton, and the sheep driver cover is made from merino scraps left over from shirt production.",
    [K("whimgolf.com","white-embroidered-navy-merino-long-sleeve-golf-shirt"),K("whimgolf.com","spell-out-knit-beanie-in-blue-sea"),K("whimgolf.com","oxford-cotton-hat"),K("whimgolf.com","merino-fleece-sheep-driver-headcover")]),
   ("Siegelman Stable", "New York, New York", "Max Siegelman&rsquo;s New York label borrows from horse racing. A gray cotton cable knit with the stable logo, a black track jacket with white panels and gold piping, and a ribbed zip cardigan for the walk from the car park.",
    [K("siegelmanstable.com","cable-knit-sweater"),K("siegelmanstable.com","track-jacket"),K("siegelmanstable.com","rib-zip-up-cardigan-1")]),
   ("Smathers &amp; Branson", "Rockville, Maryland", "Needlepoint, started in 2004 by two college roommates who couldn&rsquo;t find a second belt to buy. Every piece is hand-stitched and finished in Italian leather. The Golf Greens belt stitches famous greens by name, the Gopher flask and wallet are for the Caddyshack fan, and the valet tray takes a monogram.",
    [K("smathersandbranson.com","iconic-golf-greens-belt-dark-navy"),K("smathersandbranson.com","gopher-golf-life-flask-dark-navy"),K("smathersandbranson.com","gopher-golf-life-wallet-dark-navy"),K("smathersandbranson.com","monogrammed-valet-tray")]),
   ("Kraken Golf", "Acushnet, Massachusetts", "Markers and pitch tools in steel and Timascus. The Awakening shows a ship under full sail with tentacles breaking the surface, the Nacre is milled steel with a shell-like inlay, and the Signet slides onto a finger like a ring. The Seigaiha set embroiders a Japanese wave in hot pink across navy.",
    [K("krakengolf.com","the-awakening-timascus-golf-ball-marker"),K("krakengolf.com","nacre-golf-ball-marker"),K("krakengolf.com","seigaiha-wood-set-abyss-edition"),K("krakengolf.com","the-signet-stainless-steel-pitch-tool")]),
   ("Par&eacute;", "United States", "Filipino-American golf streetwear. The Minted Greens mahjong set marks Par&eacute;&rsquo;s third anniversary: 144 tiles, a green table mat and a green leather briefcase. The Bluetross putter cover is waxed canvas, the Club Shirt is Par&eacute;&rsquo;s first collared shirt, and the Pliss&eacute; Pants are on their second version.",
    [K("pare.golf","pare-x-minted-greens-mahjong-set"),K("pare.golf","pare-x-bluetross-blade-putter-headcover"),K("pare.golf","pare-club-shirt"),K("pare.golf","pare-plisse-pants-2-0")]),
   ("Quiet Golf", "Costa Mesa, California", "Quiet Golf makes considered golf clothes with a flag crest on the chest. Two 100% cashmere sweaters, a cable knit and a striped crew, plus a Harris Tweed driver cover cut to order in the US and a corduroy jacket for after.",
    [K("quietgolf.com","montecito-cashmere-cable-knit-sweater"),K("quietgolf.com","mesa-cashmere-sweater"),K("quietgolf.com","harris-tweed-driver-head-cover"),K("quietgolf.com","cardroom-corduroy-jacket")])]),
]
GIFTED = set()
SECTIONS = [(c[1], c[0], [k for b in c[4] for k in b[3]], c[2]) for c in CATS]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
CSS = ('<style>/*TGI-GG-BRAND*/.gg-brand{max-width:1180px;margin:0 auto;padding:44px 0 8px;border-top:1px solid rgba(20,20,20,.12)}'
 '.gg-bhero{margin:0 0 18px;aspect-ratio:2000/860;overflow:hidden}.gg-bhero img{width:100%;height:100%;object-fit:cover;display:block}.gg-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.gg-bhead{max-width:760px;margin:0 auto 22px;text-align:center}.gg-cat{margin-top:72px;padding-top:56px;border-top:3px solid #2d4a2b}.gg-cat .products-hdr{font-size:clamp(40px,6.2vw,72px);line-height:1.02;letter-spacing:-.01em;margin:10px 0 10px}.gg-bname{font-size:30px;margin:8px 0 10px;line-height:1.15}'
 '.gg-bwhy{font-size:17px;line-height:1.6;margin:0}.gg-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
 '.gg-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr));max-width:900px;margin:0 auto}'
 '.gg-grid .product-name{font-size:15px}.gg-grid .product-body{padding:12px 12px 14px}'
 '@media(max-width:900px){.gg-grid,.gg-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
 '.gg-nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px auto 0;max-width:900px}.gg-nav a{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid rgba(20,20,20,.25);padding:4px 8px}</style>\n')
def card(k, idx):
    v = D[k]; fr = FRN[k]; brand = v.get("brand", "")
    label = H.unescape(nm(k)).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-name">{nm(k)} &middot; {pr(k)}</div>'
            f'<a href="{v["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')
def bslug(n): return re.sub(r"[^a-z0-9]+", "-", H.unescape(n).lower()).strip("-")
def category(c, n0, num):
    anchor, title, kicker, intro, brands = c
    nav = "".join(f'<a href="#b-{bslug(b[0])}">{b[0]}</a>' for b in brands)
    o = (f'\n<section class="products gg-cat">\n  <div class="drop-tag grass">{num:02d} &middot; {len(brands)} brands</div>\n'
         f'  <h2 class="products-hdr" id="{anchor}">{title}</h2>\n  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
         f'  <div class="writeup-body" style="max-width:760px;margin:0 auto 10px;"><p>{intro}</p></div>\n  <div class="gg-nav">{nav}</div>\n')
    for name, loc, why, keys in brands:
        cards = "".join(card(k, n0 + j) for j, k in enumerate(keys)); n0 += len(keys)
        lc = f'<div class="drop-tag grass" style="display:inline-block">{loc}</div>' if loc else ""
        hero = BH[H.unescape(name)]
        o += (f'  <div class="gg-brand" id="b-{bslug(name)}"><figure class="gg-bhero"><img src="{hero}" alt="{H.escape(H.unescape(name))}" loading="lazy" /><h3 class="gg-sr">{name}</h3></figure>'
              f'<div class="gg-bhead">{lc}<p class="gg-bwhy">{why}</p></div>'
              f'<div class="products-grid gg-grid" data-n="{len(keys)}">{cards}</div></div>\n')
    return o + "</section>\n", n0
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Part 2 is the part of the list where the gift has to say something. <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">Part 1</a> covered the things a golfer uses every round; this one covers the things other people notice. Same format: each brand gets its own block, why it belongs in the category, and three or four gifts that prove it. Every brand is independent, and none of them appears in <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">Part 1</a> or <a href="/drops/golf-gift-guide-2026-heirlooms-tiny-makers-off-season">Part 3</a>.</p>
    <p>Three categories, thirty brands: pieces that get a reaction on the first tee, colorways nobody else in the group owns, and the splurge they would never put in their own basket. Prices run from a $10 ball marker to an $888 carry bag.</p>
    <p><strong>Where to start.</strong> For compliments, Parmore&rsquo;s camo quarter-zip. For a new colorway, Criquet&rsquo;s treetop green alpaca hoodie. For the splurge, the MacKenzie x Fyfe 23rd Edition bag.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Gifts</span><span>@@N@@</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$10&ndash;$888</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>3 of 9</span></div>
      <div class="hashtags"><span class="hashtag">#GolfGiftGuide</span><span class="hashtag">#GolfGifts</span><span class="hashtag">#IndieGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Buy the Thing They Keep Looking At</h2>
    <p>The best statement gift is one they have already noticed on someone else. The best splurge is one they have already priced and closed the tab on. If you know which brand they follow, you are most of the way there.</p>
    <p><strong>Check the timing.</strong> Mogshade makes covers to order on about a three-week lead. Slice Town&rsquo;s pitch tool and Fyfe&rsquo;s Glove Caddy are on pre-order. Devereux&rsquo;s quarter-zip, Breaker pullover and crew are final sale, so get the size right. Takomo&rsquo;s iron prices are where each build starts.</p>
    <p>Prices are as each store shows them to a US visitor. Mount Tee shows Australian dollars, so those dollar figures are approximate. Everything was available to order on November 9, 2026. <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">Part 1</a> covers everyday upgrades, range gifts and stocking stuffers; <a href="/drops/golf-gift-guide-2026-heirlooms-tiny-makers-off-season">Part 3</a> covers heirlooms, tiny makers and the off-season.</p>
  </div>
</section>
"""
HERO_ALT = "Three gifts: a man in a Public Drip patchwork swing vest in a vintage shop, a man in a rifle green Criquet quilted jacket among fall leaves, and a Fyfe canvas golf bag leaning on a flagstick above the sea"
def head_top(n):
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": D[k]["url"], "name": H.unescape(nm(k))} for i, k in enumerate(k for c in CATS for b in c[4] for k in b[3])]
    blocks = [{"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
               "datePublished": "2026-11-09", "dateModified": "2026-11-09",
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
    keys = [k for c in CATS for b in c[4] for k in b[3]]
    assert len(keys) == len(set(keys))
    for k in keys: assert FRN.get(k), k
    n = len(keys)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = (f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  {BC}</div>\n\n'
            f'<header class="drop-header">\n  <h1>{H1}</h1>\n  <div class="drop-meta">\n    <span>The Guide &middot; Holiday Gift Guide 2026, Part 2 of 3</span><span class="dot"></span>\n'
            f'    <span>30 brands &middot; {n} gifts &middot; in stock, checked November 9, 2026</span>\n  </div>\n</header>\n\n'
            f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>\n')
    body += GS.nav(2)
    body += TAKE.replace("@@N@@", str(n))
    i = 1
    for num, c in enumerate(CATS, 4):
        o, i = category(c, i, num); body += o
    body += CLOSE
    body += GS.nav(2, "Keep going: the rest of the 2026 Gift Guide")
    out = head_top(n) + head_rest.replace("</head>", CSS + GS.CSS + "</head>", 1) + body + tail
    print(f"  {n} cards, {sum(len(c[4]) for c in CATS)} brands")
    if not apply_: return
    OUT.write_text(out, encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", out[:out.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if "Mackem" in above: bad.append("leak")
    txt = re.sub(r"<[^>]+>", " ", above)
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', out)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! " + "; ".join(bad))
    print("  wrote", OUT.relative_to(ROOT))
if __name__ == "__main__": main("--apply" in sys.argv)
