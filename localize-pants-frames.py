#!/usr/bin/env python3
"""localize-pants-frames.py — gallery frames for the Pants Edit. 20 Sept 2026.

Lenny: "let's add the carosels to the pants edit so we can cylce through the
pics." So each of the eighteen product cards becomes a .product-gallery the
reader can swipe, instead of one still image.

THE TRAP HERE IS COLOURWAY, NOT COUNT. A Shopify product page carries every
colourway's photography under one handle. Pulling "the first four images" would
have put a Bone trouser in Quiet Golf's Navy gallery, a taupe pair in
Casualist's ivory one, and four TRUEBLACK frames in Gramicci's indigo card.
Checked and excluded, per brand, below — each exclusion says what it is:

  quiet-golf   4-7  are the BONE colourway; the pick is Navy
  casualist    2,3  are TAUPE, 6 is a brown detail; the pick is the ivory pair
  gramicci     1-4  are TRUEBLACK; the pick is RINSEDINDIGO
  anti         6,7  are size-chart PNGs, not photographs
  criquet      10   is a flat colour swatch
  siegelman    2 AND 3 are the women's frames. The first pass excluded only
               index 2 on a filename guess; the contact sheet showed Artboard16
               is a second women's look. Siegelman ships two frames, not three.
  students     the filenames fall into two upload groups, 6a70f72* and
               6a947382*; the pick is in the second, so the gallery uses that
               group only
  stitch       25 images in six hash groups, one group per colourway. The pick
               sits in the 691b4838* group, so the gallery is that group.

THE HASH GROUPS ARE AN INFERENCE, and a contact sheet was rendered and looked
at before this file was committed — filename reasoning is how the Bone trousers
would have got through.

FRAME ONE IS ALWAYS THE CARD IMAGE. Whatever the gallery does afterwards, the
first frame is the shot the grid was approved on, so the page opens the way
Lenny signed it off.

4:5, because .product-gallery is aspect-ratio 4/5. The 1:1 squares the first
build used would be cropped top and bottom by object-fit:cover.

NEVER RETYPE A CDN HASH. Three of these URLs were reconstructed by hand from
an earlier listing and three of them 404'd, because Shopify appends a random
suffix per upload and the eye does not reliably copy 32 hex characters. Every
URL here is now pasted from the live products.json rather than retyped.

Idempotent. Dry run by default.
"""
import io, json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/pants-edit"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"}
W, H = 1200, 1500          # 4:5

SHOP = "https://cdn.shopify.com/s/files/"
SQSP = "https://images.squarespace-cdn.com/content/v1/5f7b7302cb6064569d654760/"
SAN = "https://cdn.sanity.io/images/9aznesrq/production/"

# slug -> [(url, crop-kind), ...]  frame 1 first.
#   "model" full-length person, square centred at 0.66 of the height
#   "far"   person small in a square frame
#   "waist" already cropped at waist/thigh, centre it
#   "pack"  garment fills the frame, take from near the top
FRAMES = {
 "odd-ritual": [
   (SHOP+"1/0584/7551/1907/files/DSC05802.jpg?v=1783855922", "model"),
   (SHOP+"1/0584/7551/1907/files/DSC05872.jpg?v=1783855838", "model"),
   (SHOP+"1/0584/7551/1907/files/DSC05877.jpg?v=1783855878", "waist"),
   (SHOP+"1/0584/7551/1907/files/COL03_TROU_BLACK.jpg?v=1783855773", "pack"),
 ],
 "manors": [
   (SAN+"322765569270d9db007d40d7813ecc153e9f254f-4000x5000.jpg?auto=format&fit=max&q=90&w=2000", "model"),
   (SAN+"fd30c632b088c2fa20de0399967e8c8be8db0a93-4000x5000.jpg?auto=format&fit=max&q=90&w=2000", "model"),
   (SAN+"cd275ed91fad0e0c82efc02d021e59eeb240ede5-4000x5000.jpg?auto=format&fit=max&q=90&w=2000", "pack"),
   (SAN+"768546dc36d29d1a2f267c00f3daa8f8e89e33ae-4000x5000.jpg?auto=format&fit=max&q=90&w=2000", "pack"),
 ],
 "walker": [
   (SHOP+"1/0558/3346/0817/files/11aa93875-1486-4da0-b936-73144ded0d61.jpg?v=1779755416", "pack"),
   (SHOP+"1/0558/3346/0817/files/8070009d-c8ef-4013-99ce-c445e08a33563.jpg?v=1779755416", "pack"),
   (SHOP+"1/0558/3346/0817/files/14_6a4e107e-e8d0-4251-9767-03d68ee6caac.jpg?v=1769486194", "waist"),
   (SHOP+"1/0558/3346/0817/files/Walker_Golf_Sept_00_0161.jpg?v=1769486194", "waist"),
 ],
 "sentinel": [
   (SQSP+"3e581738-ddc5-45bf-a9b0-2b4589cfb7bd/FW26GRP2_0033_IMG_4194.jpg?format=2500w", "far"),
   (SQSP+"50f5900d-0422-48d7-8441-278d494657c7/FW26GRP2_0034_IMG_4197.jpg?format=2500w", "far"),
   (SQSP+"a0be7b6f-1bce-4aa3-a790-65e076ceda28/odt1.jpg?format=2500w", "pack"),
   (SQSP+"6c0a3616-54c9-4d0c-9e21-b3c8374d5c76/PRODUCT+FW26_0042_IMG_4385.jpg?format=2500w", "waist"),
 ],
 # 4-7 are the BONE colourway — the pick is Navy.
 "quiet-golf": [
   (SHOP+"1/0569/7205/0614/files/QQGSanMerinoPantNavy1.jpg?v=1789057768", "pack"),
   (SHOP+"1/0569/7205/0614/files/QQGSanMerinoPantNavy3.jpg?v=1789057768", "waist"),
   (SHOP+"1/0569/7205/0614/files/QQGSanMerinoPantNavy2.jpg?v=1789057768", "pack"),
   (SHOP+"1/0569/7205/0614/files/QQGSanMerinoPantNavy4.jpg?v=1789057769", "waist"),
 ],
 # 2,3 TAUPE and 6 a brown detail are excluded; the pick is the ivory pair.
 "casualist": [
   (SHOP+"1/0743/5350/8646/files/Casualist_No_Idea_sweatshirt_worn_model_lifestyle_shot.png?v=1777111107", "model"),
   (SHOP+"1/0743/5350/8646/files/Casualist_pleated_golf_trousers_front_view_ivory.png?v=1777110564", "pack"),
   (SHOP+"1/0743/5350/8646/files/Casualist_pleated_trousers_back_view_ivory.png?v=1777110580", "pack"),
   (SHOP+"1/0743/5350/8646/files/Close_up_Casualist_pleated_trousers_ivory_fabric_detail.png?v=1777110654", "waist"),
 ],
 # the 6a947382* upload group, which is the colourway the pick came from.
 "students": [
   (SHOP+"1/0565/3581/0232/files/Studentsgolf6a947382b145e76a947382b16a9.462068066a947382b16a9.jpg?v=1788113832", "model"),
   (SHOP+"1/0565/3581/0232/files/Studentsgolf6a94738269f1866a9473826a15d.672364336a9473826a15d.jpg?v=1788113832", "model"),
   (SHOP+"1/0565/3581/0232/files/Studentsgolf6a9473827dd7f06a9473827dfc9.957364426a9473827dfc9.jpg?v=1788113832", "waist"),
   (SHOP+"1/0565/3581/0232/files/Studentsgolf6a9473829a50366a9473829a7a7.547492216a9473829a7a7.jpg?v=1788113832", "waist"),
 ],
 "public-drip": [
   (SHOP+"1/0475/7218/9333/files/DSC09470.jpg?v=1784829247", "model"),
   (SHOP+"1/0475/7218/9333/files/DSC09395_5f620c26-323f-4a59-a55b-a7c8a60813cd.jpg?v=1784829245", "waist"),
   (SHOP+"1/0475/7218/9333/files/PublicDrip_FW26_ECOMM_FW26_anywhere_double_pleated_pants_pinstripe_hero_webres.png?v=1784829246", "pack"),
   (SHOP+"1/0475/7218/9333/files/PublicDrip_FW26_ECOMM_FW26_anywhere_double_pleated_pants_pinstripe_detail_1_webres.png?v=1784829246", "waist"),
 ],
 # index 10 is a flat colour swatch, not a photograph.
 "criquet": [
   (SHOP+"1/2546/6304/files/R6SF9904.jpg?v=1788898918", "waist"),
   (SHOP+"1/2546/6304/files/R6SF8557.jpg?v=1788898919", "waist"),
   (SHOP+"1/2546/6304/files/R6SF1366.jpg?v=1788898918", "waist"),
   (SHOP+"1/2546/6304/files/FW26LookbookJan26Studio-458_a31553a3-87ce-4e6a-94c1-2dbd665c0e0d.jpg?v=1788898918", "waist"),
 ],
 # 1-4 are TRUEBLACK. Indigo only.
 "gramicci": [
   (SHOP+"1/0060/2030/0890/files/Gramicci-G6FM-P030_RINSEDINDIGO_unisex-pants_W1.jpg?v=1785359679", "model"),
   (SHOP+"1/0060/2030/0890/files/Gramicci-G6FM-P030_RINSEDINDIGO_unisex-pants_W2.jpg?v=1785359679", "model"),
   (SHOP+"1/0060/2030/0890/files/Gramicci-G6FM-P030_RINSEDINDIGO_unisex-pants_1.jpg?v=1785359679", "pack"),
   (SHOP+"1/0060/2030/0890/files/Gramicci-G6FM-P030_RINSEDINDIGO_unisex-pants-detail_1.jpg?v=1785359679", "waist"),
 ],
 "malbon": [
   (SHOP+"1/1770/9541/files/M-10201-MIL-A.jpg?v=1786388359", "model"),
   (SHOP+"1/1770/9541/files/M-10201-MIL-1.jpg?v=1786387560", "pack"),
   (SHOP+"1/1770/9541/files/M-10201-MIL-2.jpg?v=1786387560", "pack"),
   (SHOP+"1/1770/9541/files/M-10201-MIL-C.jpg?v=1786388359", "waist"),
 ],
 # indices 2 and 3 are the women's looks from the same shoot — both excluded.
 "siegelman": [
   (SHOP+"1/0260/6625/5908/files/Artboard13_4cc8d3a2-5084-4768-b714-5d78d27fe1cc.jpg?v=1753712457", "model"),
   (SHOP+"1/0260/6625/5908/files/Artboard14_f299d46d-7b4a-4027-be0c-d743243cbe32.jpg?v=1753712463", "model"),
 ],
 "birds-of-condor": [
   (SHOP+"1/0765/5486/2911/files/BIRDS-OF-CONDOR-MENS-RANGER-PANT-PT23100-BLACK-LIFESTYLE-00034.jpg?v=1788335179", "waist"),
   (SHOP+"1/0765/5486/2911/files/BIRDS-OF-CONDOR-MENS-RANGER-PANT-PT23100-BLACK-LIFESTYLE-00049.jpg?v=1788335170", "waist"),
   (SHOP+"1/0765/5486/2911/files/BIRDS-OF-CONDOR-MENS-RANGER-PANT-PT23100-BLACK-FRONT2535_21d78e38-d482-48d0-8c51-5c9d376fa9ce.jpg?v=1788335164", "pack"),
   (SHOP+"1/0765/5486/2911/files/BIRDS-OF-CONDOR-MENS-RANGER-PANT-PT23100-BLACK-BACK2538.jpg?v=1788335187", "pack"),
 ],
 # Merrill publishes exactly two images for this SKU. Two frames, then.
 "merrill": [
   (SHOP+"1/0560/2646/4443/files/Blackpantfront.jpg?v=1764294691", "pack"),
   (SHOP+"1/0560/2646/4443/files/Blackpantback.jpg?v=1764294704", "pack"),
 ],
 # the 691b4838* group — one upload group per colourway.
 "stitch": [
   (SHOP+"1/0150/9084/files/StitchGolf691b4838e18d73691b4838e1d3c.45050505691b4838e1d3c_dadc6d32-4fcd-432b-a826-812e8f680444.jpg?v=1787069017", "far"),
   (SHOP+"1/0150/9084/files/StitchGolf691b48384478b9691b4838449ff.02872419691b4838449ff_1e7c1852-4822-4037-bc26-bc974bbcd4e4.jpg?v=1787069017", "far"),
   (SHOP+"1/0150/9084/files/StitchGolf691b4838668cf4691b483866dca.24273618691b483866dca_902c39a1-008a-49c6-b9ab-4f9e6713bf16.jpg?v=1787069017", "far"),
 ],
 # 6,7 are size-chart PNGs.
 "anti-country-club": [
   (SHOP+"1/0459/5633/3732/files/ANTiCOUNTRYCLUB00232_34ff0845-a9c4-4ff4-9cbe-531d3663c7c1.jpg?v=1774173088", "waist"),
   (SHOP+"1/0459/5633/3732/files/ANTiCOUNTRYCLUB00580_82788158-8f17-4bee-964e-c6774efa23f2.jpg?v=1774173088", "waist"),
   (SHOP+"1/0459/5633/3732/files/022AD155-E47E-45F9-9912-694FD85A828D.jpg?v=1774173088", "pack"),
   (SHOP+"1/0459/5633/3732/files/DSC07247.jpg?v=1774173088", "waist"),
 ],
 "olydoe": [
   (SHOP+"1/0756/5017/1098/files/Olydoe_Early_Previews-27_websize.jpg?v=1789425718", "waist"),
   (SHOP+"1/0756/5017/1098/files/Olydoe_Early_Previews-4_websize.jpg?v=1789428358", "waist"),
   (SHOP+"1/0756/5017/1098/files/NewOlydoe22Large.jpg?v=1789403242", "pack"),
   (SHOP+"1/0756/5017/1098/files/NewOlydoe23Large.jpg?v=1789403242", "pack"),
 ],
 "eastside": [
   (SHOP+"1/0542/2419/1681/files/EL2090952-254-FieldPants-Khaki-Front_54b3e598-942b-448d-93fa-fa9a0420f2fc.png?v=1788549560", "pack"),
   (SHOP+"1/0542/2419/1681/files/EL2090952-254-FieldPants-Khaki-Back.png?v=1786281827", "pack"),
   (SHOP+"1/0542/2419/1681/files/EL2090952-254-FieldPants-Khaki-Detail-0609.png?v=1786285320", "waist"),
   (SHOP+"1/0542/2419/1681/files/EL2090952-254-FieldPants-Khaki-Detail-0605.png?v=1786285320", "waist"),
 ],
}

FOCUS = {"model": 0.66, "waist": 0.50, "far": 0.68}
PACK_TOP = 0.02
FAR_SIDE = 0.66


def bg_of(im):
    """The sweep colour, sampled from the corners — used to pad a packshot."""
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    px = [im.getpixel(p) for p in pts]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))


def fit_pack(im):
    """FIT, don't crop. A packshot exists to show the whole garment, and a 4:5
    crop of a 2:3 packshot cuts 17% off the bottom — which is the hems. Eastside
    lost its cuffs that way in the first pass. So a tall packshot is scaled to
    fit and padded out to 4:5 in the sweep colour taken from its own corners."""
    tw, th = W, H
    scale = min(tw / im.width, th / im.height)
    im2 = im.resize((max(1, round(im.width * scale)),
                     max(1, round(im.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGB", (tw, th), bg_of(im))
    canvas.paste(im2, ((tw - im2.width) // 2, (th - im2.height) // 2))
    return canvas


def cut(im, kind):
    """4:5 out of whatever shape came in, placed by what the photo is."""
    tw, th = W, H
    if kind == "pack":
        return fit_pack(im)
    if kind == "far":
        # person small in frame: take a narrower window, then fit 4:5
        side = round(min(im.width, im.height) * FAR_SIDE)
        cx = (im.width - side) // 2
        cy = max(0, min(im.height - side,
                        round(im.height * FOCUS["far"]) - side // 2))
        im = im.crop((cx, cy, cx + side, cy + side))
        kind = "waist"
    scale = max(tw / im.width, th / im.height)
    im2 = im.resize((max(tw, round(im.width * scale)),
                     max(th, round(im.height * scale))), Image.LANCZOS)
    cx = (im2.width - tw) // 2
    if kind == "pack":
        cy = min(im2.height - th, round(im2.height * PACK_TOP))
    else:
        cy = round(im2.height * FOCUS.get(kind, 0.5)) - th // 2
    cy = max(0, min(im2.height - th, cy))
    return im2.crop((cx, cy, cx + tw, cy + th))


def main(apply_):
    global Image
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []
    manifest = {}

    for slug, frames in FRAMES.items():
        names = []
        for i, (url, kind) in enumerate(frames, 1):
            name = f"{slug}-f{i}"
            names.append(name)
            dest = OUT / f"{name}.jpg"
            if dest.exists():
                skipped.append(name); continue
            if not apply_:
                made.append((name, f"would fetch ({kind})")); continue
            try:
                raw = urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=90).read()
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                cut(im, kind).save(dest, "JPEG", quality=88, optimize=True)
                made.append((name, f"{kind} from {im.width}x{im.height}"))
            except Exception as e:
                failed.append((name, str(e)[:90]))
        manifest[slug] = names

    for n, d in made:    print(f"  ok    {n:24} {d}")
    for n in skipped:    print(f"  skip  {n:24} already local")
    for n, e in failed:  print(f"  FAIL  {n:24} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — a gallery with a hole in it is "
                 f"worse than no gallery")
    if apply_:
        for slug, names in manifest.items():
            for n in names:
                if not (OUT / f"{n}.jpg").exists():
                    sys.exit(f"! {n}.jpg missing after the run")
        (ROOT / "research/pants-frames.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8")
        tot = sum(len(v) for v in manifest.values())
        print(f"\n  {tot} frames across {len(manifest)} products "
              f"(min {min(len(v) for v in manifest.values())}, "
              f"max {max(len(v) for v in manifest.values())})")
        print("  manifest: research/pants-frames.json")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
