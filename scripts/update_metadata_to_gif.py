import os
import json
from .config import COLORS

META_ROOT = "metadata"

def update_one(meta_path: str):
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update field image -> .gif
    img = data.get("image", "")
    if isinstance(img, str) and img:
        if img.endswith(".png"):
            data["image"] = img[:-4] + ".gif"
        elif not img.endswith(".gif"):
            # kalau bukan png/gif tapi ada id, kita coba biarkan saja
            # (umumnya tidak kejadian, tapi aman)
            pass

    # OPTIONAL (kalau kamu pakai animation_url di marketplace)
    # data["animation_url"] = data.get("image")

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    total = 0
    changed = 0

    for color in COLORS:
        color_dir = os.path.join(META_ROOT, color)
        if not os.path.isdir(color_dir):
            print(f"⚠️ Skip, folder tidak ada: {color_dir}")
            continue

        for filename in os.listdir(color_dir):
            if not filename.endswith(".json"):
                continue

            meta_path = os.path.join(color_dir, filename)

            # cek sebelum-sesudah untuk hitung changed
            with open(meta_path, "r", encoding="utf-8") as f:
                before = json.load(f)
            before_img = before.get("image", "")

            update_one(meta_path)

            with open(meta_path, "r", encoding="utf-8") as f:
                after = json.load(f)
            after_img = after.get("image", "")

            total += 1
            if before_img != after_img:
                changed += 1

    print(f"✅ Metadata diproses: {total} file")
    print(f"✅ Image diubah ke .gif: {changed} file")

if __name__ == "__main__":
    main()
