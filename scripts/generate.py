import os
import json
import random
from PIL import Image
from .config import (
    IMAGE_SIZE, ASSETS_DIR, COLORS, LAYERS,
    TOTAL_PER_COLOR, NFT_NAME_PREFIX, DESCRIPTION
)


OUTPUT_ROOT = "output"
META_ROOT = "metadata"

def list_png(path: str):
    if not os.path.isdir(path):
        return []
    return [f for f in os.listdir(path) if f.lower().endswith(".png")]

def pick_png(path: str):
    files = list_png(path)
    return random.choice(files) if files else None

def ensure_size(img: Image.Image):
    if img.size != IMAGE_SIZE:
        img = img.resize(IMAGE_SIZE)
    return img

def generate_one(color: str, token_id: int):
    base = Image.new("RGBA", IMAGE_SIZE)
    attributes = [{"trait_type": "Color", "value": color}]

    for layer in LAYERS:
        layer_dir = os.path.join(ASSETS_DIR, color, layer)
        chosen = pick_png(layer_dir)

        # strict: kalau ada layer kosong -> error biar kamu langsung tau asset mana yang belum lengkap
        if not chosen:
            raise RuntimeError(f"Layer kosong / tidak ada PNG: {layer_dir}")

        layer_img = Image.open(os.path.join(layer_dir, chosen)).convert("RGBA")
        layer_img = ensure_size(layer_img)
        base.alpha_composite(layer_img)

        attributes.append({
            "trait_type": layer.capitalize(),
            "value": os.path.splitext(chosen)[0]
        })

    # buat folder output per warna
    out_img_dir = os.path.join(OUTPUT_ROOT, color)
    out_meta_dir = os.path.join(META_ROOT, color)
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_meta_dir, exist_ok=True)

    # save image
    out_img_path = os.path.join(out_img_dir, f"{token_id}.png")
    base.save(out_img_path)

    # metadata (image pakai placeholder ipfs, nanti gampang diganti)
    meta = {
        "name": f"{NFT_NAME_PREFIX} ({color}) #{token_id}",
        "description": DESCRIPTION,
        "image": f"ipfs://REPLACE_ME/{color}/{token_id}.png",
        "attributes": attributes
    }

    # save metadata
    out_meta_path = os.path.join(out_meta_dir, f"{token_id}.json")
    with open(out_meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def main():
    for color in COLORS:
        for token_id in range(1, TOTAL_PER_COLOR + 1):
            generate_one(color, token_id)

    total = TOTAL_PER_COLOR * len(COLORS)
    print(f"✅ Selesai generate {total} NFT")
    print(f"📁 Output  : {OUTPUT_ROOT}/(abu|orange|putih)")
    print(f"📁 Metadata: {META_ROOT}/(abu|orange|putih)")

if __name__ == "__main__":
    main()
