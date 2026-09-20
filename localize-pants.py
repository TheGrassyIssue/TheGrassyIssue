#!/usr/bin/env python3
"""localize-pants.py — the pants roundup candidates, localised. 20 Sept 2026.

Eighteen trousers, one per brand, swept across the TGI universe. Every price
read live from the brand's own store on 20 September 2026.

ON-MODEL FIRST (Lenny's call, 20 Sept).
Pants are a silhouette item: a flat packshot tells you nothing about the break,
the rise or how wide the leg actually reads on a body. So for every pick this
script walks the brand's OWN product gallery and takes the on-model frame where
one exists. Fourteen of the eighteen now have one. The four that do not —
Walker, Quiet Golf, Merrill and Eastside — genuinely shoot no model for that
SKU; their galleries are packshot and fabric detail only. That is a fact about
those brands, not a gap in the sweep, and it is why the `kind` column below is
explicit rather than inferred.

CROPPING IS DRIVEN BY `kind`, NOT BY A SINGLE GLOBAL RULE.
The first cut used one top-bias (18%) for everything, which is right for a
packshot and wrong for a full-length model shot — it framed the model's face
and cut the trousers off at the knee. So:
  * "pack"  — garment fills the frame; square taken from near the top.
  * "model" — full-length person; square centred on 0.66 of the height, which
              is where the trouser lives on a standing figure.
  * "far"   — full-length person shot SMALL inside a square frame (Sentinel and
              STITCH both deliver 2500x2500 and 1365x1365 with the figure
              occupying maybe half the frame). A full-height square crop is a
              no-op on a square source, so these take a sub-square at 62% of
              the height instead. Without this the card is mostly backdrop.
  * "waist" — the frame is already cropped at the waist or thigh; centre it.

TWO BRANDS SWAPPED, 20 Sept, at Lenny's request — same brands, different piece:
  * Malbon: Bushmills Track Pant (green plaid) OUT, STATION PANT (military
    green) IN. $228, 7 of 7 sizes, and Malbon shot it on a model head to toe.
  * Siegelman Stable: Coaches Pant OUT, Retro Track Pant IN. $212, 5 of 6, and
    the studio frame is the strongest on-model image in their whole trouser
    shelf. It also puts a silhouette in the set that nothing else covers now
    that the Malbon plaid is gone.

THREE CURRENCIES, AND NONE OF THEM CONVERTED.
  * Odd Ritual is South African and prices in ZAR. Their store served ZAR to a
    US-located browser, i.e. they run no US market and the rand is the real
    number.
  * ANTi Country Club Tokyo is Japanese and prices in JPY. Their storefront
    served $169.06 with Shopify.currency.rate = 0.0065022858 — an explicit
    conversion multiplier. country=JP returns 28,600. The yen is the price ANTi
    set; the dollars are Shopify arithmetic. Same trap as Local Rule.
  * Everyone else prices in USD natively.

ANTi'S ON-MODEL FRAME READS SAGE, NOT BEIGE — READ THIS BEFORE PUBLISHING.
ANTiCOUNTRYCLUB00232 is on ANTi's own product page for the BEIGE One-Tuck
Chino, but it was shot in a dim tungsten room and the cloth reads grey-green.
Checked: ANTi makes this trouser in Black and Beige only — there is no sage
colourway, and the Black page carries different frames (00498, 00540), so this
is the beige garment under a colour cast, not a different SKU. Taking it
because it is the brand's own on-model image for this product; flagged here
because the hanger shot on the same page is visibly a different colour and
someone will ask.

PRICES MOVE FASTER THAN YOU THINK.
Walker Golf Things repriced its entire trouser shelf DURING this sweep. The
Members Pant Tan read $110 and 5 of 5 sizes at the first pass and $119.95 and
0 of 5 about an hour later; the Kooka went $88 to $119.95 over the same window.
That is why the pick here is the Kooka (4 of 7 live) and why every figure on the
page carries the read date. Re-read before publishing.

EXCLUDED, WITH REASONS
  * Sierra Madre Golf — the store is explicitly women's; house default is
    menswear/unisex.
  * Forden Golf — carries sweatpants only, no trousers.
  * Bunker Mentality — the cheap listings are all "(Sample)" one-offs.
  * Kingfisher Golf — storefront is password-protected. Not probed.
  * Devereux, Random Golf Club, Read The Green, Apres, Sugarloaf, Whim, Okka,
    Hidden Links, Morning People, Rouqe — swept, carry no trousers at all.

Idempotent. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/pants-edit"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}
SQUARE = 1200

# slug, brand, product, currency+price, availability, kind, store url, image url
PICKS = [
    # on-model: DSC05802, full length, holding a coffee. Was COL03_TROU_BLACK,
    # a flat packshot.
    ("odd-ritual", "Odd Ritual", "Pleated Daily Trouser | Black", "R1,300", "3 of 5 sizes", "model",
     "https://oddritualgolf.com/products/pleated-daily-trouser-black",
     "https://cdn.shopify.com/s/files/1/0584/7551/1907/files/DSC05802.jpg?v=1783855922"),

    # on-model: floral polo, cream trouser, full length. Was the flat front.
    ("manors", "Manors Golf", "Recycled Greenskeeper Trouser", "$175", "in stock", "model",
     "https://manorsgolf.com/products/recycled-greenskeeper-trouser",
     "https://cdn.sanity.io/images/9aznesrq/production/322765569270d9db007d40d7813ecc153e9f254f-4000x5000.jpg?auto=format&fit=max&q=90&w=2000"),

    # NO on-model frame exists — Walker's gallery for this SKU is packshot,
    # a back-pocket detail and a fabric macro. Packshot stands.
    ("walker", "Walker Golf Things", "Kooka All Day Twill Pant | Forest", "$119.95", "4 of 7 sizes", "pack",
     "https://walkergolfthings.com/products/kooka-all-day-twill-pant-forest",
     "https://cdn.shopify.com/s/files/1/0558/3346/0817/files/11aa93875-1486-4da0-b936-73144ded0d61.jpg?v=1779755416"),

    # on-model: FW26GRP2_0033, three-quarter, cap and crew. Was odt1, a fold.
    ("sentinel", "Sentinel Golf", "MajoTech Trouser | Olive", "$210", "in stock", "far",
     "https://sentinelgolf.us/shop/p/8t95uvw1ec28h1za76ycshtzy2kvha-57hyk-8trkf-6g8w5-b2y36-a7r98-ldyan-4y4zm-x76y7-t9lmw-2mc83-t5y3y-tl3d6-zn6k2-n4wxj",
     "https://images.squarespace-cdn.com/content/v1/5f7b7302cb6064569d654760/3e581738-ddc5-45bf-a9b0-2b4589cfb7bd/FW26GRP2_0033_IMG_4194.jpg?format=2500w"),

    # NO on-model frame — eight images, all packshot and hardware detail.
    ("quiet-golf", "Quiet Golf", "San Marino Pant | Navy", "$178", "8 of 10 sizes", "pack",
     "https://quietgolf.com/products/san-merino-pant",
     "https://cdn.shopify.com/s/files/1/0569/7205/0614/files/QQGSanMerinoPantNavy1.jpg?v=1789057768"),

    # on-model: the ivory pair, full length. Was front_view_ivory, a packshot.
    # PRICE CORRECTED 20 Sept, $199 -> $160. This was NOT a price move: every
    # one of the eight variants reads 160.00 with no compare_at, and the census
    # run the same afternoon also read 160. The 199 was a misread in the first
    # sweep and it shipped to the grid. recheck-pants-prices.py is what caught
    # it, which is the argument for re-reading rather than trusting the notes.
    ("casualist", "Casualist", "Pleated Golf Trousers | Organic Cotton", "$160", "8 of 8 sizes", "model",
     "https://casualist.com/products/pleated-trousers",
     "https://cdn.shopify.com/s/files/1/0743/5350/8646/files/Casualist_No_Idea_sweatshirt_worn_model_lifestyle_shot.png?v=1777111107"),

    # on-model: full length, vest and cap. Was a packshot.
    ("students", "Students Golf", "Tradition Double Pleated Wool Pants", "$158", "5 of 6 sizes", "model",
     "https://studentsgolf.com/products/tradition-double-pleated-wool-pants",
     "https://cdn.shopify.com/s/files/1/0565/3581/0232/files/Studentsgolf6a947382b145e76a947382b16a9.462068066a947382b16a9.jpg?v=1788113832"),

    # DSC09470 was already the on-model frame — kept.
    ("public-drip", "Public Drip", "Anywhere Pleated Pants | Pinstripe", "$170", "6 of 6 sizes", "model",
     "https://publicdrip.com/products/anywhere-pleated-pants-pinstripe",
     "https://cdn.shopify.com/s/files/1/0475/7218/9333/files/DSC09470.jpg?v=1784829247"),

    # R6SF9904 — the FW26 shoot, on a person on a porch. The old pick was the
    # studio lookbook frame, which crops to legs only against white.
    ("criquet", "Criquet Shirts", "Comfort Corduroy Pant | Khaki", "$154", "21 of 21 sizes", "waist",
     "https://criquetshirts.com/products/comfort-corduroy-pant-khaki",
     "https://cdn.shopify.com/s/files/1/2546/6304/files/R6SF9904.jpg?v=1788898918"),

    # RINSEDINDIGO_W1 — on-model, full length, the indigo colourway (the black
    # frames on the same page are a different SKU).
    ("gramicci", "Gramicci", "Japanese 5-Pocket Denim Pant", "$170", "10 of 10 sizes", "model",
     "https://gramicci.com/products/japanese-5-pocket-denim-pant",
     "https://cdn.shopify.com/s/files/1/0060/2030/0890/files/Gramicci-G6FM-P030_RINSEDINDIGO_unisex-pants_W1.jpg?v=1785359679"),

    # SWAPPED 20 Sept: Bushmills Track Pant out, Station Pant in.
    ("malbon", "Malbon Golf", "Station Pant | Military Green", "$228", "7 of 7 sizes", "model",
     "https://malbon.com/products/station-pant-military-green",
     "https://cdn.shopify.com/s/files/1/1770/9541/files/M-10201-MIL-A.jpg?v=1786388359"),

    # SWAPPED 20 Sept: Coaches Pant out, Retro Track Pant in.
    ("siegelman", "Siegelman Stable", "Retro Track Pant", "$212", "5 of 6 sizes", "model",
     "https://siegelmanstable.com/products/retro-track-pant-1",
     "https://cdn.shopify.com/s/files/1/0260/6625/5908/files/Artboard13_4cc8d3a2-5084-4768-b714-5d78d27fe1cc.jpg?v=1753712457"),

    # LIFESTYLE-00034 — the fuller on-course frame. Was 00049, cropped tighter.
    ("birds-of-condor", "Birds of Condor", "Ranger Pant | Black", "$100", "5 of 5 sizes", "waist",
     "https://us.birdsofcondor.com/products/black-ranger-golf-walk-pants",
     "https://cdn.shopify.com/s/files/1/0765/5486/2911/files/BIRDS-OF-CONDOR-MENS-RANGER-PANT-PT23100-BLACK-LIFESTYLE-00034.jpg?v=1788335179"),

    # NO on-model frame — the SKU has exactly two images, both packshot.
    ("merrill", "Merrill Golf", "Baggy Trousers | Black", "$125", "4 of 4 sizes", "pack",
     "https://merrillgolf.com/products/baggy-trousers-black",
     "https://cdn.shopify.com/s/files/1/0560/2646/4443/files/Blackpantfront.jpg?v=1764294691"),

    # on-model: full length, navy polo. Was a packshot from the same set.
    ("stitch", "STITCH", "Heston Five Pocket Pant", "$148", "66 of 90 sizes", "far",
     "https://stitchgolf.com/products/231sa5003",
     "https://cdn.shopify.com/s/files/1/0150/9084/files/StitchGolf691b4838e18d73691b4838e1d3c.45050505691b4838e1d3c_dadc6d32-4fcd-432b-a826-812e8f680444.jpg?v=1787069017"),

    # on-model: ANTiCOUNTRYCLUB00232. See the colour-cast note in the docstring.
    ("anti-country-club", "ANTi Country Club Tokyo", "One-Tuck Chino Pants | Beige", "&yen;28,600", "3 of 3 sizes", "waist",
     "https://anticountryclubtokyo.com/products/anti-country-club-tokyo-2026-ss-chino-pants-beige",
     "https://cdn.shopify.com/s/files/1/0459/5633/3732/files/ANTiCOUNTRYCLUB00232_34ff0845-a9c4-4ff4-9cbe-531d3663c7c1.jpg?v=1774173088"),

    # already an on-model frame from Olydoe's early previews, cropped at the hip.
    ("olydoe", "Olydoe", "Pleated Walker Pant", "$115", "5 of 5 sizes", "waist",
     "https://olydoe.com/products/pleated-walker-pant",
     "https://cdn.shopify.com/s/files/1/0756/5017/1098/files/Olydoe_Early_Previews-27_websize.jpg?v=1789425718"),

    # NO on-model frame — five images, all packshot and pocket detail.
    ("eastside", "Eastside Golf", "Khaki Field Pant", "$125", "6 of 6 sizes", "pack",
     "https://eastsidegolf.com/products/el2090952-254-khaki-field-pant",
     "https://cdn.shopify.com/s/files/1/0542/2419/1681/files/EL2090952-254-FieldPants-Khaki-Front_54b3e598-942b-448d-93fa-fa9a0420f2fc.png?v=1788549560"),
]

# Where the square sits vertically, as a fraction of the source height for the
# CENTRE of the crop. "pack" is expressed as a top offset instead, because a
# packshot's garment starts near the top of the frame.
FOCUS = {"model": 0.66, "waist": 0.50, "far": 0.68}
PACK_TOP = 0.04
FAR_SIDE = 0.62          # fraction of the source height, for "far"


def square_crop(im, kind):
    """Square crop whose size and vertical placement depend on what the photo is."""
    s = min(im.size)
    if kind == "far":
        s = min(s, round(im.height * FAR_SIDE))
    cx = (im.width - s) // 2
    if kind == "pack":
        cy = min(im.height - s, round(im.height * PACK_TOP))
    else:
        cy = round(im.height * FOCUS[kind]) - s // 2
    cy = max(0, min(im.height - s, cy))          # clamp inside the frame
    return im.crop((cx, cy, cx + s, cy + s)).resize((SQUARE, SQUARE), Image.LANCZOS)


def main(apply_):
    global Image
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []

    for slug, brand, name, price, avail, kind, url, img in PICKS:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug); continue
        if not apply_:
            made.append((slug, f"would fetch ({kind})")); continue
        try:
            req = urllib.request.Request(img, headers=UA)
            raw = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            square_crop(im, kind).save(dest, "JPEG", quality=88, optimize=True)
            made.append((slug, f"{kind} from {im.width}x{im.height}"))
        except Exception as e:
            failed.append((slug, str(e)[:90]))

    for n, d in made:    print(f"  ok    {n:20} {d}")
    for n in skipped:    print(f"  skip  {n:20} already local")
    for n, e in failed:  print(f"  FAIL  {n:20} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — do NOT build a grid with holes in it")
    if apply_:
        want = {p[0] for p in PICKS}
        have = {p.stem for p in OUT.glob("*.jpg")}
        if want - have:
            sys.exit(f"\n! missing: {sorted(want - have)}")
        n_model = sum(1 for p in PICKS if p[5] != "pack")
        print(f"\n  {len(want)} pants local in images/pants-edit/ "
              f"({len(want)} brands, one piece each; {n_model} on-model)")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
