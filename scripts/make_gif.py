import os
import json
from PIL import Image
from .config import (
    IMAGE_SIZE,
    ASSETS_DIR,
    COLORS,
    LAYERS,
    GIF_ROOT,
    GIF_DURATION
)


OUTPUT_ROOT = "output"
META_ROOT = "metadata"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def build_gif(color: str, token_id: int):
    meta_path = os.path.join(META_ROOT, color, f"{token_id}.json")
    if not os.path.exists(meta_path):
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    base = Image.new("RGBA", IMAGE_SIZE)
    frames = []

    # urutan frame sesuai layer
    for attr in meta["attributes"]:
        if attr["trait_type"].lower() not in LAYERS:
            continue

        layer = attr["trait_type"].lower()
        value = attr["value"]
        if value == "None":
            continue

        img_path = os.path.join(ASSETS_DIR, color, layer, f"{value}.png")
        if not os.path.exists(img_path):
            continue

        img = Image.open(img_path).convert("RGBA")
        base = base.copy()
        base.alpha_composite(img)
        frames.append(base.copy())

    if not frames:
        return

    gif_dir = os.path.join(GIF_ROOT, color)
    ensure_dir(gif_dir)

    gif_path = os.path.join(gif_dir, f"{token_id}.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=GIF_DURATION,
        loop=0,
        disposal=2,
        optimize=True
    )

def main():
    for color in COLORS:
        for file in os.listdir(os.path.join(META_ROOT, color)):
            if not file.endswith(".json"):
                continue
            token_id = int(file.replace(".json", ""))
            build_gif(color, token_id)

    print("✅ Semua GIF berhasil dibuat.")

if __name__ == "__main__":
    main()
